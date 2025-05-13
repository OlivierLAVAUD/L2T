from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M", src_lang="en")

text = "Hello world"
tokenizer.tgt_lang = "fr"
inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(**inputs)
tokenizer.decode(outputs[0], skip_special_tokens=True)