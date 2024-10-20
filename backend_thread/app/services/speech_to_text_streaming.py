from deepgram import Deepgram
import os
import aiohttp
import logging

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
deepgram_client = Deepgram(DEEPGRAM_API_KEY)

# Set up logging to confirm Deepgram interactions
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def deepgram_stream(audio_chunk: bytes) -> str:
    """Streams audio to Deepgram for transcription."""
    logger.info("Listening: Audio stream sent to Deepgram.")
    async with aiohttp.ClientSession() as session:
        try:
            response = await deepgram_client.transcription.prerecorded(
                audio=audio_chunk,
                mimetype="audio/wav",
                options={"punctuate": True, "language": "en"}
            )
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            logger.info(f"Transcription received: {transcript}")
            return transcript
        except Exception as e:
            logger.error(f"Error in Deepgram stream: {e}")
            return ""
