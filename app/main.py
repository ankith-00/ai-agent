import base64

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel

from agent.main import run_agent, sessions
from utils.elevenlabs_config import stt, tts

app = FastAPI()


@app.get("/health")
async def health():
    return {"ok": True}


class ChatIn(BaseModel):
    session_id: str
    message: str
    include_audio: bool = False


@app.post("/chat")
async def chat(body: ChatIn):
    reply = await run_agent(body.session_id, body.message)
    if not body.include_audio:
        return {"reply": reply}
    audio = await tts(reply)
    return {"reply": reply, "audio": base64.b64encode(audio).decode("ascii")}


@app.post("/voice")
async def voice(session_id: str = Form(...), audio: UploadFile = File(...)):
    text = await stt(await audio.read(), audio.filename or "audio.webm")
    reply = await run_agent(session_id, text)
    return Response(await tts(reply), media_type="audio/mpeg")


@app.delete("/session/{session_id}")
async def reset(session_id: str):
    sessions.pop(session_id, None)
    return {"ok": True}
