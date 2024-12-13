# deploy.ps1
param(
    [switch]$cleanup = $false,
    [switch]$forceRebuild = $false
)

$ErrorActionPreference = "Stop"

function Write-Status {
    param($message)
    Write-Host "==> $message" -ForegroundColor Cyan
}

try {
    if ($cleanup) {
        Write-Status "Cleaning up existing containers and networks..."
        docker-compose -f docker-compose.integrated.yml down
        docker network prune -f
    }

    Write-Status "Pulling latest images..."
    docker-compose -f docker-compose.integrated.yml pull

    Write-Status "Starting core services (etcd, minio)..."
    docker-compose -f docker-compose.integrated.yml up -d etcd minio

    Write-Status "Waiting for core services initialization..."
    Start-Sleep -Seconds 10

    Write-Status "Starting Milvus standalone..."
    docker-compose -f docker-compose.integrated.yml up -d standalone

    Write-Status "Waiting for Milvus initialization..."
    Start-Sleep -Seconds 15

    Write-Status "Starting quantum framework services..."
    if ($forceRebuild) {
        docker-compose -f docker-compose.integrated.yml up -d --build nexus_prime quantum_engine
    } else {
        docker-compose -f docker-compose.integrated.yml up -d nexus_prime quantum_engine
    }

    Write-Status "Deployment complete! Access points:"
    Write-Host "Jupyter Lab: http://localhost:8888 (token: quantum_framework)"
    Write-Host "Milvus: localhost:19530"
    Write-Host "Nexus API: http://localhost:5000"
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Stack Trace: $($_.ScriptStackTrace)" -ForegroundColor Red
    exit 1
}