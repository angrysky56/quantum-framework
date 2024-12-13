# Monitoring Systems Deployment Script
Write-Host "Starting Monitoring Systems Deployment..." -ForegroundColor Green

# Step 1: Set up the collections
Write-Host "Setting up Milvus collections..." -ForegroundColor Blue
python setup_collections.py

# Step 2: Verify vector database configuration
Write-Host "Verifying Milvus configuration..." -ForegroundColor Blue
python verify_milvus.py

# Step 3: Monitor initial system state
Write-Host "Initializing system monitoring..." -ForegroundColor Blue
$monitoringDir = "monitoring_dashboards"
if (Test-Path $monitoringDir) {
    Set-Location $monitoringDir
    if (Test-Path "docker-compose.yml") {
        Write-Host "Deploying monitoring stack..." -ForegroundColor Cyan
        docker compose up -d
    }
}

Write-Host "Deployment script completed!" -ForegroundColor Green