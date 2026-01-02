# Build Release and Publish Repository to GitHub
# This script builds the repository and prepares it for GitHub release

param(
    [string]$Version = "",
    [switch]$SkipBuild = $false,
    [switch]$CreateGitTag = $false,
    [string]$GitHubRepo = "seranov/kodi-play-random"
)

# Get script directory (repository root)
$ScriptDir = Split-Path -Parent $PSScriptRoot
Set-Location $ScriptDir

# Define colors for output
function Write-Info { param($msg) Write-Host $msg -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host $msg -ForegroundColor Green }
function Write-Error { param($msg) Write-Host $msg -ForegroundColor Red }
function Write-Warning { param($msg) Write-Host $msg -ForegroundColor Yellow }

Write-Info "=== Kodi Repository Release Builder ==="
Write-Info ""

# Check if Python is available
try {
    $PythonVersion = python --version 2>&1
    Write-Info "Python found: $PythonVersion"
}
catch {
    Write-Error "Python not found. Please install Python 3.x"
    exit 1
}

# Build repository if not skipped
if (-not $SkipBuild) {
    Write-Info ""
    Write-Info "Building repository..."
    Write-Info "Running: python scripts/generate_repo.py"
    Write-Info ""
    
    python scripts/generate_repo.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Repository build failed!"
        exit 1
    }
    
    Write-Success "Repository built successfully"
}

# Check if repo directory exists
if (-not (Test-Path "repo")) {
    Write-Error "Repository directory 'repo' not found. Run build first."
    exit 1
}

# Get repository addon info
$RepoAddonXml = "repository.seranov\addon.xml"
if (-not (Test-Path $RepoAddonXml)) {
    Write-Error "Repository addon.xml not found: $RepoAddonXml"
    exit 1
}

# Parse version from repository addon.xml if not provided
if ([string]::IsNullOrEmpty($Version)) {
    [xml]$AddonXml = Get-Content $RepoAddonXml
    $Version = $AddonXml.addon.version
    Write-Info "Detected repository version: $Version"
}

# List files in repo directory
Write-Info ""
Write-Info "=== Repository Contents ==="
Get-ChildItem -Path "repo" | ForEach-Object {
    $Size = if ($_.PSIsContainer) { "DIR" } else { "{0:N2} MB" -f ($_.Length / 1MB) }
    Write-Info "  $($_.Name) - $Size"
}

# Check if repository.seranov zip exists
$RepoZipName = "repository.seranov-$Version.zip"
$RepoZipPath = Join-Path "repo" $RepoZipName

if (-not (Test-Path $RepoZipPath)) {
    Write-Error "Repository zip not found: $RepoZipPath"
    exit 1
}

Write-Info ""
Write-Success "Repository package ready: $RepoZipName"

# Create git tag if requested
if ($CreateGitTag) {
    Write-Info ""
    Write-Info "Creating git tag: v$Version"
    
    try {
        git tag -a "v$Version" -m "Release version $Version"
        Write-Success "Git tag created: v$Version"
        Write-Warning "Don't forget to push the tag: git push origin v$Version"
    }
    catch {
        Write-Error "Failed to create git tag: $_"
    }
}

Write-Info ""
Write-Info "=== Next Steps ==="
Write-Info ""
Write-Info "To publish the repository to GitHub:"
Write-Info ""
Write-Info "1. Commit and push changes:"
Write-Info "   git add repo/"
Write-Info "   git commit -m 'Release version $Version'"
Write-Info "   git push origin main"
Write-Info ""
Write-Info "2. Push git tag (if created):"
Write-Info "   git push origin v$Version"
Write-Info ""
Write-Info "3. Create GitHub Release:"
Write-Info "   - Go to: https://github.com/$GitHubRepo/releases/new"
Write-Info "   - Tag version: v$Version"
Write-Info "   - Release title: Release $Version"
Write-Info "   - Upload: repo/$RepoZipName"
Write-Info ""
Write-Info "4. Users can install the repository from:"
Write-Info "   https://raw.githubusercontent.com/$GitHubRepo/main/repo/$RepoZipName"
Write-Info ""
Write-Info "Or add the repository URL to Kodi:"
Write-Info "   https://raw.githubusercontent.com/$GitHubRepo/main/repo/"
Write-Info ""

# Display installation instructions
Write-Info "=== Installation Instructions ==="
Write-Info ""
Write-Info "Method 1: Direct ZIP installation"
Write-Info "  1. Download: https://github.com/$GitHubRepo/raw/main/repo/$RepoZipName"
Write-Info "  2. In Kodi: Settings → Add-ons → Install from zip file"
Write-Info "  3. Select the downloaded ZIP file"
Write-Info ""
Write-Info "Method 2: Add repository source (automatic updates)"
Write-Info "  1. In Kodi: Settings → File Manager → Add source"
Write-Info "  2. Enter URL: https://raw.githubusercontent.com/$GitHubRepo/main/repo/"
Write-Info "  3. Name it: Seranov Repository"
Write-Info "  4. Settings → Add-ons → Install from zip file → Seranov Repository"
Write-Info "  5. Select: $RepoZipName"
Write-Info ""

Write-Success "Release build complete!"
