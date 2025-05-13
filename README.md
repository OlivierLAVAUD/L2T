<img src="img/L2T_img.png" alt="Description de l'image" />

# L2T - Language 2 Translate

## Purpose and Scope
L2T (Language 2 Translate) is a command-line translation system that leverages the NLLB-200 (No Language Left Behind) neural machine translation model to provide translation capabilities across 200+ languages. 

## System Overview
L2T is structured as a modular command-line application that allows users to translate text directly or from files, with support for both text files and PDFs. The system handles language detection, translation, and output generation through a pipeline of specialized components.

## Language Support

The system supports over 200 languages through the NLLB-200 model, using language codes in the format xxx_Latn (e.g., eng_Latn for English, fra_Latn for French, ...).

# File Structure
The codebase follows a clean, modular organization:

```markdown
Directory structure:
└── olivierlavaud-l2t/
    ├── README.md
    ├── pyproject.toml
    ├── .python-version
    ├── app/
    │   ├── README.md
    │   ├── __init__.py
    │   ├── cli.py
    │   ├── file_handlers.py
    │   ├── logger.py
    │   ├── main.py
    │   ├── optimizations.py
    │   ├── translator.py
    │   └── utils.py  
    ├── docs/
    └── gpu/
        
```
# Prerequisite
    . uv: The extremely fast Python package and project manager (https://docs.astral.sh/uv/getting-started/installation/)
    . Hugginface Cli Access

# Installation

Step 1: Clone the Repository

```bash
git clone https://github.com/OlivierLAVAUD/L2T.git
cd L2T
```

Step 2: Verify Installation

Run a simple command to verify that L2T is functioning correctly:
```bash
uv run -m app.main --list-languages

This command should display a list of supported languages, indicating that the system is properly installed and the NLLB-200 model is accessible.
```

For more details see manual
```bash
uv run -m app.main --help
```

# Usage

1. Translate a text string to French:
```bash
uv run -m app.main "Text to translate" -l fra_Latn
```

2. Translate a text string from French to English and specifying source language:
```bash

uv run -m app.main "Texte à traduire" -l eng_Latn -s fra_Latn
```

3. Translate a file and save the output:
```bash

uv run -m app.main "Texte à traduire" -l eng_Latn -s fra_Latn -o my_translated_file.txt
```

4. Translate a PDF document:
```bash
# Generate automatically a T2L file: my_file_to_translate.T2L.txt
uv run  -m app.main my_file_to_translate.txt -l eng_Latn -s fra_Latn

# Others samples
uv run -m app.main docs/Le_Lievre_et_la_Tortue.txt -l eng_Latn -s fra_Latn
uv run -m app.main docs/Le_Petit_Prince_ASE.pdf -l eng_Latn -s fra_Latn
```
