import requests
import logging

logger = logging.getLogger(__name__)

def synthesize_speech(text: str) -> bytes:
    logger.info(f"Synthesizing speech for: {text}")
    try:
        response = requests.post(
            "https://api.text-to-speech-service.com/synthesize",
            json={"text": text, "voice": "en-US-Wavenet-D"},
        )
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logger.error(f"Text-to-Speech Error: {e}")
        return b""
