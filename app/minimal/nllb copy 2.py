import argparse
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Chargement du modèle et tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

def main():
    # Configuration de l'argument en ligne de commande
    parser = argparse.ArgumentParser(description="Traduction de texte en français.")
    parser.add_argument("text", type=str, help="Texte à traduire")
    args = parser.parse_args()

    # Texte à traduire
    text = args.text

    # Encodage avec le code langue cible
    inputs = tokenizer(text, return_tensors="pt")

    # Traduction en français (fra_Latn)
    translated = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids("fra_Latn")  # Correction ici
    )

    # Décodage du résultat
    print(tokenizer.decode(translated[0], skip_special_tokens=True))

if __name__ == "__main__":
    main()