function Invoke-L2T {
    param(
        [string]$Text,
        [string]$Language = "fra_Latn"  # Valeur par défaut
    )
    uv run -m app.main $Text -l $Language
}

# Associer l'alias à la fonction
Set-Alias -Name l2t -Value Invoke-L2T