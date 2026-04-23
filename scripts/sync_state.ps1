# God-Level AI Developer System - State Synchronizer (Windows/PowerShell)

$BackupFile = "god_ai_state_backup.zip"
$SourceFolders = @(".env", "backend/data/memory")

function Show-Help {
    Write-Host "Usage:"
    Write-Host "  .\sync_state.ps1 -Export    # Backs up .env and AI Memory to $BackupFile"
    Write-Host "  .\sync_state.ps1 -Import    # Restores state from $BackupFile"
}

param (
    [switch]$Export,
    [switch]$Import
)

if ($Export) {
    Write-Host "🚀 Exporting system state..." -ForegroundColor Cyan
    if (Test-Path $BackupFile) { Remove-Item $BackupFile }
    
    $FilesToZip = @()
    foreach ($Path in $SourceFolders) {
        if (Test-Path $Path) {
            $FilesToZip += $Path
        }
    }
    
    if ($FilesToZip.Count -gt 0) {
        Compress-Archive -Path $FilesToZip -DestinationPath $BackupFile
        Write-Host "✅ Export complete! Shared '$BackupFile' with your other system." -ForegroundColor Green
    } else {
        Write-Host "❌ Nothing to export! Ensure .env or backend/data/memory exists." -ForegroundColor Red
    }
}
elseif ($Import) {
    if (-not (Test-Path $BackupFile)) {
        Write-Host "❌ Error: $BackupFile not found!" -ForegroundColor Red
        return
    }
    
    Write-Host "📥 Importing system state..." -ForegroundColor Cyan
    Expand-Archive -Path $BackupFile -DestinationPath "." -Force
    Write-Host "✅ Import complete! Your AI Memory and environment are now restored." -ForegroundColor Green
}
else {
    Show-Help
}
