# God-Level AI Developer System - Windows Setup Script

Write-Host "🚀 Setting up God-Level AI Developer System..." -ForegroundColor Cyan

# Check for Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python not found! Please install Python 3.10+." -ForegroundColor Red
    return
}

# Create virtual environment
if (-not (Test-Path venv)) {
    Write-Host "📦 Creating virtual environment..."
    python -m venv venv
}

# Install dependencies
Write-Host "🛠️ Installing dependencies..."
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Create necessary directories
Write-Host "📁 Creating folders..."
$Folders = @("workspace", "logs", "deployments", "backend/data")
foreach ($f in $Folders) {
    if (-not (Test-Path $f)) { New-Item -ItemType Directory -Path $f }
}

# Check for Ollama models
Write-Host "🤖 Checking Ollama models..."
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    $Models = ollama list
    if ($Models -notmatch "llama3") { Write-Host "⚠️ Warning: 'llama3' model missing. Run: ollama pull llama3" -ForegroundColor Yellow }
    if ($Models -notmatch "deepseek-coder") { Write-Host "⚠️ Warning: 'deepseek-coder' model missing. Run: ollama pull deepseek-coder" -ForegroundColor Yellow }
} else {
    Write-Host "⚠️ Warning: Ollama not detected!" -ForegroundColor Yellow
}

# Copy environment file
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env from example..."
    Copy-Item .env.example .env
    Write-Host "⚠️ IMPORTANT: Edit .env and add your API keys!" -ForegroundColor Yellow
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "💡 To sync state from another system, run: .\scripts\sync_state.ps1 -Import"
Write-Host "🚀 Run the system: .\venv\Scripts\python.exe -m uvicorn backend.api.routes:app --reload --port 8000"
