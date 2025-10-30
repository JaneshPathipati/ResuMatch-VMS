$env:PYTHONPATH = "$env:APPDATA\Python\Python313\site-packages"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " VOLUNTEER MANAGEMENT SYSTEM" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Green
Write-Host "Once started, open: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""

python app.py
