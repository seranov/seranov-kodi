# Deploy Kodi Addons to Local Installation
# This script copies addon directories to local Kodi installation

param(
    [string]$KodiProgramPath = "C:\Program Files (x86)\Kodi",
    [string]$KodiDataPath = "$env:APPDATA\Kodi",
    [string[]]$AddonsToDeploy = @()  # Empty array means deploy all
)

# Get script directory (repository root)
$ScriptDir = Split-Path -Parent $PSScriptRoot
Set-Location $ScriptDir

# Define colors for output
function Write-Info { param($msg) Write-Host $msg -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host $msg -ForegroundColor Green }
function Write-Error { param($msg) Write-Host $msg -ForegroundColor Red }
function Write-Warning { param($msg) Write-Host $msg -ForegroundColor Yellow }

Write-Info "=== Kodi Addon Local Deployment ==="
Write-Info ""

# Check if Kodi directories exist
$KodiAddonsPath = Join-Path $KodiDataPath "addons"
if (-not (Test-Path $KodiDataPath)) {
    Write-Error "Kodi data directory not found: $KodiDataPath"
    Write-Warning "Please update the KodiDataPath parameter"
    exit 1
}

if (-not (Test-Path $KodiAddonsPath)) {
    Write-Warning "Addons directory not found, creating: $KodiAddonsPath"
    New-Item -ItemType Directory -Path $KodiAddonsPath -Force | Out-Null
}

# Find all addon directories
$AllAddons = Get-ChildItem -Directory | Where-Object {
    $_.Name -match '^(plugin\.|service\.|context\.|repository\.)'
}

if ($AllAddons.Count -eq 0) {
    Write-Error "No addon directories found in: $ScriptDir"
    exit 1
}

# Determine which addons to deploy
if ($AddonsToDeploy.Count -eq 0) {
    $AddonsToDeploy = $AllAddons | ForEach-Object { $_.Name }
    Write-Info "Deploying all addons: $($AddonsToDeploy -join ', ')"
} else {
    Write-Info "Deploying selected addons: $($AddonsToDeploy -join ', ')"
}

Write-Info ""

# Deploy each addon
$SuccessCount = 0
$FailCount = 0

foreach ($AddonName in $AddonsToDeploy) {
    $SourcePath = Join-Path $ScriptDir $AddonName
    
    if (-not (Test-Path $SourcePath)) {
        Write-Warning "Addon not found: $AddonName (skipping)"
        $FailCount++
        continue
    }
    
    $TargetPath = Join-Path $KodiAddonsPath $AddonName
    
    try {
        Write-Info "Deploying: $AddonName"
        
        # Remove existing addon if present
        if (Test-Path $TargetPath) {
            Remove-Item -Path $TargetPath -Recurse -Force
        }
        
        # Copy addon to Kodi addons directory
        Copy-Item -Path $SourcePath -Destination $TargetPath -Recurse -Force
        
        Write-Success "  ✓ Deployed successfully to: $TargetPath"
        $SuccessCount++
    }
    catch {
        Write-Error "  ✗ Failed to deploy: $_"
        $FailCount++
    }
}

Write-Info ""
Write-Info "=== Deployment Summary ==="
Write-Success "Successfully deployed: $SuccessCount addon(s)"
if ($FailCount -gt 0) {
    Write-Error "Failed: $FailCount addon(s)"
}

Write-Info ""
Write-Warning "Please restart Kodi for changes to take effect"
Write-Info ""

# Example usage information
Write-Info "Usage examples:"
Write-Info "  Deploy all addons:"
Write-Info "    .\scripts\deploy-local.ps1"
Write-Info ""
Write-Info "  Deploy specific addons:"
Write-Info "    .\scripts\deploy-local.ps1 -AddonsToDeploy @('plugin.video.random.recursive', 'context.screenshots')"
Write-Info ""
Write-Info "  Use custom Kodi paths:"
Write-Info "    .\scripts\deploy-local.ps1 -KodiDataPath 'D:\Kodi\portable_data'"
