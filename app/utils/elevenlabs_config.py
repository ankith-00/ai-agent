import os
import httpx
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")

URL = "https://api.elevenlabs.io/v1"
HEADERS = {"xi-api-key": API_KEY}

# STT
async def stt(audio: bytes, filename: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{URL}/speech-to-text",
            headers=HEADERS,
            data={"model_id": "scribe_v1"},
            files={"file": (filename, audio)},
        )
        r.raise_for_status()
        return r.json()["text"]

# TTS
async def tts(text: str) -> bytes:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{URL}/text-to-speech/{VOICE_ID}",
            headers=HEADERS,
            json={"text": text, "model_id": "eleven_multilingual_v2"},
        )
        r.raise_for_status()
        return r.content