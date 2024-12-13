import json
import os
import subprocess
from pathlib import Path
import requests
import time

class AlphaProtocol:
    def __init__(self):
        self.base_path = Path(r"C:\Users\angry\OneDrive\Desktop\ai_workspace\containers")
        self.config_path = self.base_path / "config"
        self.docker_config = self._load_config("docker-config.json")
        self.network_config = self._load_config("network-config.json")

    def _load_config(self, filename):
        with open(self.config_path / filename) as f:
            return json.load(f)

    def verify_environment(self):
        verification_steps = [
            self._verify_network,
            self._verify_containers,
            self._verify_both_and,
            self._verify_iris_system
        ]
        
        results = []
        for step in verification_steps:
            result = step()
            results.append(result)
            if not result['success']:
                print(f"Verification failed at {step.__name__}: {result['error']}")
                return False
        return True

    def _verify_network(self):
        try:
            networks = ['dev-environment_default', 'milvus_network', 'agent-systems_network']
            for network in networks:
                result = subprocess.run(['docker', 'network', 'inspect', network], 
                                     capture_output=True, text=True)
                if result.returncode != 0:
                    return {'success': False, 'error': f"Network {network} not found"}
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _verify_containers(self):
        required_containers = {
            'dev-redis': 6379,
            'dev-postgres': 5432,
            'both-and-agent': 5000,
            'dev-frontend': 3000,
            'dev-backend': 4000
        }
        
        for container, port in required_containers.items():
            try:
                result = subprocess.run(['docker', 'inspect', container],
                                     capture_output=True, text=True)
                if result.returncode != 0:
                    return {'success': False, 'error': f"Container {container} not found"}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        return {'success': True}

    def _verify_both_and(self):
        endpoints = [
            'http://localhost:5000/health',
            'http://localhost:5000/metrics'
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint)
                if response.status_code != 200:
                    return {'success': False, 'error': f"Endpoint {endpoint} returned {response.status_code}"}
            except Exception as e:
                return {'success': False, 'error': f"Failed to connect to {endpoint}: {str(e)}"}
        return {'success': True}

    def _verify_iris_system(self):
        components = ["QPRE", "DSS", "TCW", "CSE", "EEP", "CCI", "MRE"]
        # This would be implemented based on your Iris system's actual verification methods
        return {'success': True}  # Placeholder for actual implementation

    def execute(self):
        """Execute the Alpha protocol"""
        print("Starting System Integration Protocol Alpha...")
        
        if not self.verify_environment():
            print("Environment verification failed")
            return False

        print("Environment verified successfully")
        return True

if __name__ == "__main__":
    protocol = AlphaProtocol()
    protocol.execute()