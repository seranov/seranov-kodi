# Quick diagnostic script for Kodi context menu issues
# Быстрая диагностика проблем с контекстным меню Kodi

Write-Host "=== Kodi Context Menu Diagnostic ===" -ForegroundColor Cyan
Write-Host ""

$kodiPath = "$env:APPDATA\Kodi"
$addonsPath = "$kodiPath\addons"

# Check if Kodi is installed
Write-Host "[1/6] Checking Kodi installation..." -ForegroundColor Yellow
if (Test-Path $kodiPath) {
    Write-Host "  [OK] Kodi found at: $kodiPath" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Kodi not found at: $kodiPath" -ForegroundColor Red
    exit 1
}

# Check addons
Write-Host ""
Write-Host "[2/6] Checking addons installation..." -ForegroundColor Yellow
$addons = @(
    "context.seranov.screenshots",
    "plugin.video.seranov.browser",
    "plugin.video.seranov.recursive"
)

foreach ($addon in $addons) {
    $addonPath = Join-Path $addonsPath $addon
    if (Test-Path $addonPath) {
        Write-Host "  [OK] $addon is installed" -ForegroundColor Green

        # Check version
        $xmlPath = Join-Path $addonPath "addon.xml"
        if (Test-Path $xmlPath) {
            $xml = [xml](Get-Content $xmlPath)
            $version = $xml.addon.version
            Write-Host "       Version: $version" -ForegroundColor Gray
        }
    } else {
        Write-Host "  [ERROR] $addon is NOT installed" -ForegroundColor Red
        Write-Host "         Expected at: $addonPath" -ForegroundColor Gray
    }
}

# Check scripts exist
Write-Host ""
Write-Host "[3/6] Checking script files..." -ForegroundColor Yellow

$scripts = @{
    "context.seranov.screenshots" = @("contextitem_images.py", "context_menu_debug.py")
    "plugin.video.seranov.browser" = @("context_menu.py", "context_menu_debug.py")
    "plugin.video.seranov.recursive" = @("main.py", "context_menu_debug.py")
}

foreach ($addon in $scripts.Keys) {
    $addonPath = Join-Path $addonsPath $addon
    if (Test-Path $addonPath) {
        foreach ($script in $scripts[$addon]) {
            $scriptPath = Join-Path $addonPath $script
            if (Test-Path $scriptPath) {
                Write-Host "  [OK] $addon\$script" -ForegroundColor Green
            } else {
                Write-Host "  [ERROR] $addon\$script NOT FOUND" -ForegroundColor Red
            }
        }
    }
}

# Check Kodi log
Write-Host ""
Write-Host "[4/6] Checking Kodi log..." -ForegroundColor Yellow
$logPath = Join-Path $kodiPath "kodi.log"
if (Test-Path $logPath) {
    Write-Host "  [OK] Log file found: $logPath" -ForegroundColor Green

    # Check for addon loading
    Write-Host ""
    Write-Host "  Searching for addon loading messages..." -ForegroundColor Gray
    $content = Get-Content $logPath -Tail 500

    foreach ($addon in $addons) {
        $found = $content | Select-String -Pattern $addon -Quiet
        if ($found) {
            Write-Host "  [OK] $addon mentioned in log" -ForegroundColor Green
        } else {
            Write-Host "  [WARN] $addon not mentioned in log" -ForegroundColor Yellow
        }
    }

    # Check for errors
    Write-Host ""
    Write-Host "  Searching for errors..." -ForegroundColor Gray
    $errors = $content | Select-String -Pattern "ERROR.*seranov" | Select-Object -First 5
    if ($errors) {
        Write-Host "  [WARN] Found errors in log:" -ForegroundColor Yellow
        foreach ($error in $errors) {
            Write-Host "    $error" -ForegroundColor Red
        }
    } else {
        Write-Host "  [OK] No recent errors found" -ForegroundColor Green
    }

} else {
    Write-Host "  [WARN] Log file not found: $logPath" -ForegroundColor Yellow
    Write-Host "        Kodi might not have been started yet" -ForegroundColor Gray
}

# Check if Kodi is running
Write-Host ""
Write-Host "[5/6] Checking if Kodi is running..." -ForegroundColor Yellow
$kodiProcess = Get-Process -Name "kodi" -ErrorAction SilentlyContinue
if ($kodiProcess) {
    Write-Host "  [INFO] Kodi IS RUNNING (PID: $($kodiProcess.Id))" -ForegroundColor Cyan
    Write-Host "        You need to RESTART Kodi for changes to take effect!" -ForegroundColor Yellow
} else {
    Write-Host "  [OK] Kodi is not running" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "[6/6] Summary and recommendations" -ForegroundColor Yellow
Write-Host ""

if ($kodiProcess) {
    Write-Host "  ACTION REQUIRED:" -ForegroundColor Red
    Write-Host "  1. Close Kodi completely" -ForegroundColor White
    Write-Host "  2. Wait 5 seconds" -ForegroundColor White
    Write-Host "  3. Start Kodi again" -ForegroundColor White
    Write-Host "  4. Try opening context menu (right-click or press C)" -ForegroundColor White
} else {
    Write-Host "  NEXT STEPS:" -ForegroundColor Green
    Write-Host "  1. Start Kodi" -ForegroundColor White
    Write-Host "  2. Navigate to any folder or file" -ForegroundColor White
    Write-Host "  3. Open context menu (right-click or press C)" -ForegroundColor White
    Write-Host "  4. Look for these menu items:" -ForegroundColor White
    Write-Host "     - DEBUG: Screenshots" -ForegroundColor Cyan
    Write-Host "     - DEBUG: Browser" -ForegroundColor Cyan
    Write-Host "     - DEBUG: Recursive Player" -ForegroundColor Cyan
    Write-Host "     - Local Info" -ForegroundColor Cyan
    Write-Host "     - Unified Video Browser" -ForegroundColor Cyan
    Write-Host "     - Play Random Recursive" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "For detailed log analysis, see: doc\KODI_LOG_CHECK.md" -ForegroundColor Gray
Write-Host ""

