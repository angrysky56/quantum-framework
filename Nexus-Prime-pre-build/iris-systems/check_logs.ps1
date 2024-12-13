# Get logs for each container
Write-Host "Getting logs for vector_qpre..." -ForegroundColor Blue
docker compose logs vector_qpre

Write-Host "`nGetting logs for vector_dss..." -ForegroundColor Blue
docker compose logs vector_dss

Write-Host "`nGetting logs for vector_tcw..." -ForegroundColor Blue
docker compose logs vector_tcw