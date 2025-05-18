function Invoke-L2T {
    uv run -m app.main @args
}

# Supprime un alias existant s’il y en a un
if (Get-Alias l2t -ErrorAction SilentlyContinue) {
    Remove-Item Alias:l2t
}

. $PROFILE

# Crée l’alias
Set-Alias -Name l2t -Value Invoke-L2T

. $PROFILE