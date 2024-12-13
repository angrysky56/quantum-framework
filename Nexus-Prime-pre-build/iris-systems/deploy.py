import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def deploy_iris_systems():
    """Deploy the IRIS system containers"""
    base_path = Path(r"C:\Users\angry\OneDrive\Desktop\ai_workspace\containers\iris-systems")
    
    print("\nStarting IRIS systems deployment...")
    
    # Step 1: Build the images
    print("\nBuilding Docker images...")
    success, output = run_command(f"cd {base_path} && docker-compose build")
    if not success:
        print("Error building images:")
        print(output)
        return False
    
    # Step 2: Start the containers
    print("\nStarting containers...")
    success, output = run_command(f"cd {base_path} && docker-compose up -d")
    if not success:
        print("Error starting containers:")
        print(output)
        return False
    
    # Step 3: Verify containers are running
    print("\nVerifying container status...")
    success, output = run_command(f"cd {base_path} && docker-compose ps")
    if not success:
        print("Error checking container status:")
        print(output)
        return False
    
    print("\n✓ IRIS systems deployment completed successfully!")
    return True

def main():
    # First run the verification script
    print("Running environment verification...")
    verify_result = subprocess.run([sys.executable, "verify_environment.py"], check=False)
    
    if verify_result.returncode != 0:
        print("Environment verification failed! Please fix the issues before deploying.")
        sys.exit(1)
    
    # If verification passed, proceed with deployment
    if not deploy_iris_systems():
        print("\nDeployment failed! Please check the errors above.")
        sys.exit(1)
    
    print("\nProtocol Delta execution completed successfully!")

if __name__ == "__main__":
    main()