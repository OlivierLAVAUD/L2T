# Supprimer la fonction si elle existe
if (Get-Command Invoke-L2T -ErrorAction SilentlyContinue) {
    Remove-Item Function:Invoke-L2T
}

# Supprimer l’alias s’il existe
if (Get-Alias l2t -ErrorAction SilentlyContinue) {
    Remove-Item Alias:l2t
}

# Définir la fonction
function Invoke-L2T {
    uv run -m app.main @args
}

# Créer l’alias
Set-Alias -Name l2t -Value Invoke-L2T
