# Iris Systems Deployment Script
# This script should be run from PowerShell in the iris-systems directory

Write-Host "Starting Iris Systems Deployment..." -ForegroundColor Green

# Step 1: Verify we're in the correct directory
$expectedPath = "C:\Users\angry\OneDrive\Desktop\ai_workspace\containers\iris-systems"
if ($PWD.Path -ne $expectedPath) {
    Write-Host "Changing to correct directory..." -ForegroundColor Yellow
    Set-Location $expectedPath
}

# Step 2: Create or verify networks
Write-Host "Setting up networks..." -ForegroundColor Blue

# Get all networks
$networks = docker network ls --format "{{.Name}}"
Write-Host "Available networks:" -ForegroundColor Cyan
docker network ls

# Check for Milvus network - it might have a different name
$milvusNetworkFound = $false
$networks | ForEach-Object {
    if ($_ -like "*milvus*") {
        $milvusNetworkFound = $true
        Write-Host "Found Milvus network: $_" -ForegroundColor Green
        # Update the docker-compose.yml to use this network name
        $composeContent = Get-Content "docker-compose.yml" -Raw
        $composeContent = $composeContent -replace "milvus_network", $_
        $composeContent | Set-Content "docker-compose.yml"
    }
}

if (-not $milvusNetworkFound) {
    Write-Host "Creating milvus_network..." -ForegroundColor Yellow
    docker network create milvus_network
}

# Check for dev network
$devNetworkFound = $networks -contains "dev-environment_default"
if (-not $devNetworkFound) {
    Write-Host "Creating dev-environment_default network..." -ForegroundColor Yellow
    docker network create dev-environment_default
}

# Step 3: Verify required containers are running
Write-Host "Verifying required containers..." -ForegroundColor Blue
$requiredContainers = @(
    "milvus-standalone",
    "milvus-etcd",
    "milvus-minio",
    "dev-postgres",
    "dev-redis"
)

$missingContainers = @()
foreach ($container in $requiredContainers) {
    $status = docker ps --filter "name=$container" --format "{{.Status}}"
    if (-not $status) {
        $missingContainers += $container
    } else {
        Write-Host "$container is running" -ForegroundColor Green
    }
}

if ($missingContainers.Count -gt 0) {
    Write-Host "Warning: The following containers are not running:" -ForegroundColor Yellow
    $missingContainers | ForEach-Object { Write-Host "- $_" -ForegroundColor Yellow }
    $response = Read-Host "Do you want to continue anyway? (y/n)"
    if ($response -ne "y") {
        exit 1
    }
}

# Step 4: Deploy the iris systems
Write-Host "Deploying Iris Systems..." -ForegroundColor Green
try {
    # Stop any existing containers first
    Write-Host "Stopping any existing containers..." -ForegroundColor Blue
    docker compose down

    # Deploy with new configuration
    Write-Host "Starting deployment..." -ForegroundColor Blue
    docker compose up -d

    # Verify deployment
    Write-Host "Verifying deployment..." -ForegroundColor Blue
    Start-Sleep -Seconds 5  # Give containers time to start
    $vectorContainers = docker ps --filter "name=vector_" --format "{{.Names}}"
    
    $expectedContainers = @("vector_qpre", "vector_dss", "vector_tcw")
    foreach ($container in $expectedContainers) {
        if ($vectorContainers -notcontains $container) {
            Write-Host "Warning: $container not found in running containers!" -ForegroundColor Yellow
            Write-Host "Checking logs for $container..." -ForegroundColor Yellow
            docker compose logs $container
        } else {
            Write-Host "$container successfully deployed" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "Error during deployment: $_" -ForegroundColor Red
    Write-Host "Container logs:" -ForegroundColor Yellow
    docker compose logs
    exit 1
}

Write-Host "Deployment script completed!" -ForegroundColor Green
Write-Host "Run 'docker compose logs' to check container logs if needed." -ForegroundColor Cyan