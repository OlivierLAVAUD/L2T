from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import torch

class NLLBTranslator:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._loaded = False
        self.translator_pipe = None
        self.supported_languages = {
            'afr_Latn': 'Afrikaans',
            'amh_Ethi': 'Amharique',
            'ara_Arab': 'Arabe',
            'asm_Beng': 'Assamais',
            'ast_Latn': 'Asturien',
            'azj_Latn': 'Azéri',
            'bel_Cyrl': 'Biélorusse',
            'ben_Beng': 'Bengali',
            'bos_Latn': 'Bosnien',
            'bul_Cyrl': 'Bulgare',
            'cat_Latn': 'Catalan',
            'ceb_Latn': 'Cebuano',
            'ces_Latn': 'Tchèque',
            'ckb_Arab': 'Kurde (Sorani)',
            'cym_Latn': 'Gallois',
            'dan_Latn': 'Danois',
            'deu_Latn': 'Allemand',
            'ell_Grek': 'Grec',
            'eng_Latn': 'Anglais',
            'est_Latn': 'Estonien',
            'fin_Latn': 'Finnois',
            'fra_Latn': 'Français',
            'fuv_Latn': 'Fulfulde',
            'gaz_Latn': 'Gayo',
            'gle_Latn': 'Irlandais',
            'glg_Latn': 'Galicien',
            'guj_Gujr': 'Gujarati',
            'hat_Latn': 'Créole haïtien',
            'hau_Latn': 'Haoussa',
            'heb_Hebr': 'Hébreu',
            'hin_Deva': 'Hindi',
            'hrv_Latn': 'Croate',
            'hun_Latn': 'Hongrois',
            'hye_Armn': 'Arménien',
            'ibo_Latn': 'Igbo',
            'ind_Latn': 'Indonésien',
            'isl_Latn': 'Islandais',
            'ita_Latn': 'Italien',
            'jav_Latn': 'Javanais',
            'jpn_Jpan': 'Japonais',
            'kam_Latn': 'Kamba',
            'kan_Knda': 'Kannada',
            'kat_Geor': 'Géorgien',
            'kaz_Cyrl': 'Kazakh',
            'kea_Latn': 'Créole du Cap-Vert',
            'khk_Cyrl': 'Khalkha Mongol',
            'khm_Khmr': 'Khmer',
            'kir_Cyrl': 'Kirghiz',
            'kor_Hang': 'Coréen',
            'lao_Laoo': 'Lao',
            'lit_Latn': 'Lituanien',
            'ltz_Latn': 'Luxembourgeois',
            'lug_Latn': 'Ganda',
            'luo_Latn': 'Luo',
            'lvs_Latn': 'Letton',
            'mai_Deva': 'Maithili',
            'mal_Mlym': 'Malayalam',
            'mar_Deva': 'Marathi',
            'mkd_Cyrl': 'Macédonien',
            'mlt_Latn': 'Maltais',
            'mni_Beng': 'Manipuri',
            'mya_Mymr': 'Birman',
            'nld_Latn': 'Néerlandais',
            'nno_Latn': 'Norvégien (Nynorsk)',
            'nob_Latn': 'Norvégien (Bokmål)',
            'npi_Deva': 'Népalais',
            'nya_Latn': 'Chichewa',
            'ory_Orya': 'Odia',
            'pan_Guru': 'Pendjabi',
            'pbt_Arab': 'Pachtou',
            'pes_Arab': 'Persan',
            'pol_Latn': 'Polonais',
            'por_Latn': 'Portugais',
            'ron_Latn': 'Roumain',
            'rus_Cyrl': 'Russe',
            'slk_Latn': 'Slovaque',
            'slv_Latn': 'Slovène',
            'sna_Latn': 'Shona',
            'snd_Arab': 'Sindhi',
            'som_Latn': 'Somali',
            'spa_Latn': 'Espagnol',
            'srp_Cyrl': 'Serbe',
            'swe_Latn': 'Suédois',
            'swh_Latn': 'Swahili',
            'tam_Taml': 'Tamoul',
            'tel_Telu': 'Télougou',
            'tgk_Cyrl': 'Tadjik',
            'tgl_Latn': 'Tagalog',
            'tha_Thai': 'Thaï',
            'tur_Latn': 'Turc',
            'ukr_Cyrl': 'Ukrainien',
            'urd_Arab': 'Ourdou',
            'uzn_Latn': 'Ouzbek',
            'vie_Latn': 'Vietnamien',
            'xho_Latn': 'Xhosa',
            'yor_Latn': 'Yoruba',
            'zho_Hans': 'Chinois simplifié',
            'zho_Hant': 'Chinois traditionnel',
            'zsm_Latn': 'Malais',
            'zul_Latn': 'Zoulou'
        }

    def load_model(self):
        """Charge le modèle optimisé pour la vitesse"""
        if self._loaded:
            return

        try:
            # Configuration pour performance maximale
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                "facebook/nllb-200-distilled-600M",
                device_map="auto",
                torch_dtype=torch_dtype
            )

            self.tokenizer = AutoTokenizer.from_pretrained(
                "facebook/nllb-200-distilled-600M",
                use_fast=True  # Tokenizer rapide
            )

            # Pipeline optimisé
            self.translator_pipe = pipeline(
                "translation",
                model=self.model,
                tokenizer=self.tokenizer,
            #    device=self.model,
                truncation=True,
                max_length=512  # Longueur optimale pour performance
            )

            self._loaded = True
        except Exception as e:
            raise RuntimeError(f"Erreur de chargement: {str(e)}")

    def translate_batch(self, texts: list, target_lang: str, source_lang: str = None) -> list:
        """Traduction par batch pour meilleure performance"""
        if not self._loaded:
            self.load_model()

        try:
            # Préfixe de langue pour NLLB
            if source_lang:
                src_prefix = f"{source_lang}>"
            else:
                src_prefix = ""

            results = self.translator_pipe(
                texts,
                src_lang=src_prefix,
                tgt_lang=target_lang,
                batch_size=8,  # Taille de batch optimale
                num_beams=2,   # Réduire pour plus de vitesse
                early_stopping=True
            )
            return [r['translation_text'] for r in results]
        except Exception as e:
            raise RuntimeError(f"Erreur de traduction: {str(e)}")

    def get_supported_languages(self):
        """Retourne les langues supportées avec leurs codes."""
        return self.supported_languages

    def is_language_supported(self, lang_code: str) -> bool:
        """Vérifie si une langue est supportée"""
        return lang_code in self.supported_languages

    def translate(self, text, target_lang, source_lang=None):
        """Version corrigée avec gestion explicite du device"""
        if not self._loaded:
            self.load_model()

        try:
            # Force le device GPU
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(device)
            
            if source_lang:
                self.tokenizer.src_lang = source_lang

            # Tokenize en spécifiant le device
            inputs = self.tokenizer(
                text, 
                return_tensors="pt",
                truncation=True,
                max_length=1024
            ).to(device)  # <-- Correction clé ici

            # Génération sur le bon device
            translated = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids([target_lang]),
                max_length=1024
            )
            
            return self.tokenizer.decode(translated[0], skip_special_tokens=True)
            
        except Exception as e:
            raise RuntimeError(f"Erreur de traduction: {str(e)}")