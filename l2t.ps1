<#
.SYNOPSIS
Defines the Invoke-L2T function and its alias l2t to launch the translation app.

.DESCRIPTION
Handles complex arguments including spaces and special characters properly.
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Clean existing definitions
Remove-Item Function:Invoke-L2T -ErrorAction SilentlyContinue
Remove-Item Alias:l2t -ErrorAction SilentlyContinue

function Invoke-L2T {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$PassthruArgs
    )

    try {
        if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
            throw "'uv' command not found. Install with: pip install uvicorn"
        }

        # Reconstruct properly quoted command
        $processedArgs = @()
        $buffer = ""
        
        foreach ($arg in $PassthruArgs) {
            if ($arg -match '^-') { # New parameter
                if ($buffer) {
                    $processedArgs += "`"$buffer`""
                    $buffer = ""
                }
                $processedArgs += $arg
            } else { # Continuation of text
                if ($buffer) { $buffer += " " }
                $buffer += $arg
            }
        }
        
        if ($buffer) { $processedArgs += "`"$buffer`"" }

        $command = "uv run -m app.main $($processedArgs -join ' ')"
        Invoke-Expression $command
    }
    catch {
        Write-Host "[ERROR] Launch failed: $_" -ForegroundColor Red
        return 1
    }
}

# Create global alias
Set-Alias -Name l2t -Value Invoke-L2T -Force -Scope Global

# ===== Tests =====
Write-Host "`n[TEST] Running validations..." -ForegroundColor Cyan

# Test complex argument handling
try {
    $test = l2t "this is a test. does it work?" -t fra_Latn --debug 2>&1
    if ($test -match "usage:" -or $test -match "Configuration") {
        Write-Host "[PASS] Complex arguments handled correctly" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Argument handling issue" -ForegroundColor Red
    }
} catch {
    Write-Host "[FAIL] Test failed: $_" -ForegroundColor Red
}

Write-Host "`n[READY] Setup complete. Usage examples:" -ForegroundColor Cyan
Write-Host "  l2t `"text with spaces and ? marks`" -t fra_Latn -s"
Write-Host "  l2t -f `"path/with spaces/file.txt`" -t spa_Latn`n"