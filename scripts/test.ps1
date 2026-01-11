param(
    [string[]]$AddonsToDeploy = @()
)

Write-Host "Test script"

foreach ($AddonName in $AddonsToDeploy) {
    Write-Host "Processing: $AddonName"

    try {
        Write-Host "  In try block"
    }
    catch {
        Write-Host "  In catch block"
    }
}

Write-Host "Done"

