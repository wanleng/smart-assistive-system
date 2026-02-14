# PowerShell script to run the Assistive Vision System
# This automatically uses the specific Python version where dependencies are installed.

# Check for Virtual Environment first
if (Test-Path ".\.venv\Scripts\python.exe") {
    $PythonPath = ".\.venv\Scripts\python.exe"
    Write-Host "Using Virtual Environment: $PythonPath" -ForegroundColor Green
}
else {
    $PythonPath = "C:\Users\Sai Swam Wan Hline\AppData\Local\Programs\Python\Python311\python.exe"
    Write-Host "Using Global Python: $PythonPath" -ForegroundColor Yellow
}

Write-Host "Starting Assistive Vision System..." -ForegroundColor Cyan
& $PythonPath "main.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "App exited with error code $LASTEXITCODE" -ForegroundColor Red
    Pause
}
