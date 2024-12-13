import json
import os
import subprocess
from pathlib import Path
import time

class BravoProtocol:
    def __init__(self):
        self.base_path = Path(r"C:\Users\angry\OneDrive\Desktop\ai_workspace\containers")
        self.emergency_steps = [
            self._rapid_core_access,
            self._essential_systems,
            self._emergency_integration
        ]
        self.minimal_containers = {
            'milvus-production/docker-compose.yml': ['milvus-standalone', 'milvus-etcd'],
            'dev-environment/docker-compose.yml': ['dev-redis', 'dev-postgres']
        }

    def _rapid_core_access(self):
        """Emergency step 1: Rapid core access with smart retries"""
        try:
            # Fast path verification
            critical_dirs = ['milvus-production', 'dev-environment', 'agent-systems']
            for dir_name in critical_dirs:
                dir_path = self.base_path / dir_name
                if not dir_path.exists():
                    try:
                        # Emergency directory creation if missing
                        dir_path.mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        return {'success': False, 'error': f"Critical directory {dir_name} failed: {str(e)}"}
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _essential_systems(self):
        """Emergency step 2: Essential systems with parallel startup"""
        try:
            for compose_file, containers in self.minimal_containers.items():
                compose_path = self.base_path / compose_file
                if compose_path.exists():
                    # Start only essential containers in parallel
                    subprocess.Popen([
                        'docker-compose',
                        '-f', str(compose_path),
                        'up', '-d',
                        *containers
                    ])
            
            # Quick verification
            time.sleep(5)  # Brief wait for containers
            for _, containers in self.minimal_containers.items():
                for container in containers:
                    try:
                        subprocess.run(['docker', 'inspect', container],
                                     capture_output=True, check=True)
                    except:
                        print(f"Warning: Container {container} not ready, continuing...")
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _emergency_integration(self):
        """Emergency step 3: Rapid full integration with minimal checks"""
        try:
            # Start remaining services in parallel
            compose_files = list(self.base_path.glob('*/docker-compose.yml'))
            for compose_file in compose_files:
                subprocess.Popen([
                    'docker-compose',
                    '-f', str(compose_file),
                    'up', '-d'
                ])
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def execute(self):
        """Execute the emergency Bravo protocol with parallel processing"""
        print("Starting Emergency Integration Protocol Bravo...")
        results = []
        
        for step in self.emergency_steps:
            try:
                result = step()
                results.append(result)
                if not result['success']:
                    print(f"Warning: Step {step.__name__} reported error: {result['error']}")
                    # Continue despite errors in emergency mode
            except Exception as e:
                print(f"Warning: Step {step.__name__} failed: {str(e)}")
                continue
        
        print("Emergency protocol completed with fast path execution")
        return {'success': True, 'steps': results}

if __name__ == "__main__":
    protocol = BravoProtocol()
    protocol.execute()