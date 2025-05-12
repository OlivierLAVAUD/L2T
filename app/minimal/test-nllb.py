from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Chargement du modèle et tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

# Texte à traduire
text = "Hello world"

# Encodage avec le code langue cible
inputs = tokenizer(text, return_tensors="pt")

# Traduction en français (fra_Latn)
translated = model.generate(
    **inputs,
    forced_bos_token_id=tokenizer.convert_tokens_to_ids("fra_Latn")  # Correction ici
)

# Décodage du résultat
print(tokenizer.decode(translated[0], skip_special_tokens=True))