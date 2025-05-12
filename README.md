## L2T - Language 2 Translate

# Structure
```markdown
app/
│
├── __init__.py
├── cli.py            # Point d'entrée et gestion des arguments
├── translator.py     # Coeur de la traduction
├── file_handlers.py  # Gestion des fichiers PDF/text
├── utils.py         # Fonctions utilitaires
└── logger.py        # Configuration du logging
```

# Usage

- Help command line and language List
```bash
uv run -m app.main --help
uv run  -m app.main --list-languages
```

## Samples

```bash
uv run -m app.main "Texte à traduire" -l fra_Latn
uv run -m app.main "Texte à traduire" -l eng_Latn -s fra_Latn
uv run -m app.main "Texte à traduire" -l eng_Latn -s fra_Latn -o my_translated_file.txt

uv run  -m app.main my_file_to_translate.txt -l eng_Latn -s fra_Latn -o my_translated_file.txt

# for Generating automatically a T2L file: my_file_to_translate.T2L.txt
uv run  -m app.main my_file_to_translate.txt -l eng_Latn -s fra_Latn

uv run -m app.main docs/Le_Lievre_et_la_Tortue.txt -l eng_Latn -s fra_Latn
uv run -m app.main docs/Le_Petit_Prince_ASE.pdf -l eng_Latn -s fra_Latn
```
