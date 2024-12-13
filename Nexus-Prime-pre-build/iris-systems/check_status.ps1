# Get container status including stopped containers
Write-Host "Checking all containers including stopped ones..." -ForegroundColor Blue
docker ps -a --filter "name=vector_"

# Get detailed container inspection
Write-Host "`nChecking detailed container info..." -ForegroundColor Blue
Write-Host "vector_qpre:" -ForegroundColor Yellow
docker inspect iris-systems-vector_qpre-1

Write-Host "`nvector_dss:" -ForegroundColor Yellow
docker inspect iris-systems-vector_dss-1

Write-Host "`nvector_tcw:" -ForegroundColor Yellow
docker inspect iris-systems-vector_tcw-1