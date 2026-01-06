import requests

LIBRETRANSLATE_URL = "http://127.0.0.1:5000/translate"

def translate_text(text, source_lang, target_lang):
    """
    Translate text using LibreTranslate API
    """
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    try:
        response = requests.post(LIBRETRANSLATE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("translatedText", "")
    except Exception as e:
        print("Translation error:", e)
        return text  # fallback: return original text
