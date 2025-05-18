<#
.SYNOPSIS
Defines the Invoke-L2T function and its alias l2t to launch a Uvicorn application.

.DESCRIPTION
This script:
1. Removes previous definitions of Invoke-L2T and l2t if they exist
2. Creates a new function to launch the application via Uvicorn
3. Configures the l2t alias
4. Includes validation tests
#>

# Set encoding for special characters
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Remove function if it exists
if (Get-Command Invoke-L2T -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] Removing old Invoke-L2T function..."
    Remove-Item Function:Invoke-L2T -ErrorAction SilentlyContinue
}

# Remove alias if it exists
if (Get-Alias l2t -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] Removing old l2t alias..."
    Remove-Item Alias:l2t -ErrorAction SilentlyContinue
}

# Define main function
function Invoke-L2T {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        $PassthruArgs
    )

 #   Write-Host "[INFO] Launching L2T via Uvicorn..."
    try {
        # Verify uv is available
        if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
            throw "'uv' command not found. Install with: pip install uvicorn"
        }

        # Execute application
        $command = "uv run -m app.main $PassthruArgs"
    #    Write-Host "[EXEC] $command"
        Invoke-Expression $command
    }
    catch {
        Write-Host "[ERROR] Launch failed: $_" -ForegroundColor Red
        return 1
    }
}

# Create alias
Write-Host "[INFO] Creating l2t alias..."
Set-Alias -Name l2t -Value Invoke-L2T -Force -Description "Alias for Invoke-L2T"

# ======================================
# AUTOMATED TESTS
# ======================================
Write-Host "`n[TEST] Starting validations..." -ForegroundColor Cyan

# Test 1: Alias verification
if (-not (Get-Alias l2t -ErrorAction SilentlyContinue)) {
    Write-Host "[TEST FAILED] l2t alias not created" -ForegroundColor Red
} else {
    Write-Host "[TEST PASSED] l2t alias configured" -ForegroundColor Green
}

# Test 2: Function verification
if (-not (Get-Command Invoke-L2T -ErrorAction SilentlyContinue)) {
    Write-Host "[TEST FAILED] Invoke-L2T function not created" -ForegroundColor Red
} else {
    Write-Host "[TEST PASSED] Invoke-L2T function available" -ForegroundColor Green
}

# Test 3: Uvicorn verification
try {
    $uvCheck = Get-Command uv -ErrorAction Stop
    Write-Host "[TEST PASSED] Uvicorn found: $($uvCheck.Source)" -ForegroundColor Green
} catch {
    Write-Host "[TEST FAILED] Uvicorn not installed" -ForegroundColor Red
}

Write-Host "`n[READY] Setup complete. Test with:" -ForegroundColor Cyan
Write-Host "  l2t            # Launch application"
Write-Host "  Get-Alias l2t  # Verify alias`n"