# Supprimer la fonction si elle existe
if (Get-Command Invoke-L2T -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] Delete function Invoke-L2T..."
    Remove-Item Function:Invoke-L2T
}

# Supprimer l’alias s’il existe
if (Get-Alias l2t -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] Delete alias l2t..."
    Remove-Item Alias:l2t
}

# Définir la fonction
function Invoke-L2T {
    Write-Host "[INFO] Launch L2T app.main..."
    uv run -m app.main @args
}

# Créer l’alias
Write-Host "[INFO] Create alias l2t..."
Set-Alias -Name l2t -Value Invoke-L2T -Force

# Vérification finale
Write-Host "[SUCCES] Alias 'l2t' configured. Test with: l2t"
Get-Alias l2t
