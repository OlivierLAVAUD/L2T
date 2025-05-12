## L2T - Language 2 Translate

# Structure
```markdown
Directory structure:
└── olivierlavaud-l2t/
    ├── README.md
    ├── pyproject.toml
    ├── requirements.txt
    ├── uv.lock
    ├── .python-version
    ├── app/
    │   ├── README.md
    │   ├── __init__.py
    │   ├── cli.py
    │   ├── file_handlers.py
    │   ├── logger.py
    │   ├── main.py
    │   ├── optimizations.py
    │   ├── pyproject.toml
    │   ├── translator.py
    │   ├── utils.py
    │   └── minimal/
    │       ├── README.md
    │       ├── cli-nllb.py
    │       ├── nllb copy 2.py
    │       └── test-nllb.py
    ├── docs/
    │   ├── Le_Lievre_et_la_Tortue.txt
    │   └── Le_Petit_Prince_ASE.eng-Latn.T2L.txt
    └── gpu/
        ├── gpu_check.py
        ├── gpu_sync.py
        ├── gpu_verif.py
        └── gpu_version.py
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
