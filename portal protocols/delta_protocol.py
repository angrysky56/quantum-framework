import json
import os
import subprocess
from pathlib import Path
import docker
from typing import Dict, Any
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

class DeltaProtocol:
    def __init__(self):
        self.base_path = Path(r"C:\Users\angry\OneDrive\Desktop\ai_workspace\containers")
        self.docker_client = docker.from_env()
        self.deployment_configs = {
            'both-and-agent': {
                'image': 'node:18-alpine',
                'ports': {'5000/tcp': 5000},
                'networks': ['dev-environment_default'],
                'dependencies': ['dev-redis', 'dev-postgres']
            }
        }

    async def _verify_dependency(self, dependency: str) -> bool:
        """Verify if a dependency container is running"""
        try:
            container = self.docker_client.containers.get(dependency)
            return container.status == 'running'
        except:
            return False

    async def prepare_environment(self) -> Dict[str, Any]:
        """Prepare environment with smart path detection"""
        try:
            # Parallel dependency verification
            dependency_tasks = [
                self._verify_dependency(dep)
                for config in self.deployment_configs.values()
                for dep in config.get('dependencies', [])
            ]
            
            results = await asyncio.gather(*dependency_tasks)
            missing_deps = [
                dep for dep, running in zip(
                    [dep for config in self.deployment_configs.values() 
                     for dep in config.get('dependencies', [])],
                    results
                ) if not running
            ]

            if missing_deps:
                return {
                    "success": False,
                    "error": f"Missing dependencies: {', '.join(missing_deps)}"
                }

            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_container(self, name: str, config: Dict) -> Dict[str, Any]:
        """Create container with smart configuration"""
        try:
            # Ensure networks exist
            for network in config.get('networks', []):
                try:
                    self.docker_client.networks.get(network)
                except:
                    self.docker_client.networks.create(network, driver='bridge')

            # Smart volume mounting
            volume_path = self.base_path / name
            volume_path.mkdir(parents=True, exist_ok=True)

            # Create container with retry logic
            for attempt in range(3):
                try:
                    container = self.docker_client.containers.run(
                        image=config['image'],
                        name=name,
                        ports=config.get('ports', {}),
                        volumes={str(volume_path): {'bind': '/app', 'mode': 'rw'}},
                        network=config['networks'][0],
                        detach=True,
                        environment={
                            "NODE_ENV": "development",
                            "REDIS_HOST": "dev-redis",
                            "REDIS_PORT": "6379",
                            "POSTGRES_HOST": "dev-postgres",
                            "POSTGRES_PORT": "5432"
                        }
                    )
                    break
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        raise e
                    await asyncio.sleep(1)

            # Connect to additional networks
            for network in config.get('networks', [])[1:]:
                network_obj = self.docker_client.networks.get(network)
                network_obj.connect(container)

            return {"success": True, "container_id": container.id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def execute(self) -> Dict[str, Any]:
        """Execute Delta protocol with parallel processing"""
        print("Starting Emergency Docker Compose Protocol Delta...")
        
        # Prepare environment
        env_result = await self.prepare_environment()
        if not env_result["success"]:
            print(f"Warning: Environment preparation failed: {env_result['error']}")
            # Continue despite warning in emergency protocol

        # Create containers in parallel
        container_tasks = [
            self.create_container(name, config)
            for name, config in self.deployment_configs.items()
        ]
        
        results = await asyncio.gather(*container_tasks, return_exceptions=True)
        
        success = all(
            isinstance(r, dict) and r.get("success", False)
            for r in results
        )

        return {
            "success": success,
            "results": {
                name: result
                for name, result in zip(self.deployment_configs.keys(), results)
            }
        }

if __name__ == "__main__":
    protocol = DeltaProtocol()
    asyncio.run(protocol.execute())