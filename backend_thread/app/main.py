from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from .routers import chat
from .services.speech_to_text_streaming import deepgram_stream
from .services.text_to_speech import synthesize_speech
from .services.llm import query_llm

app = FastAPI(title="Lucian AI Backend")

# CORS Middleware for WebSocket connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the chat router
app.include_router(chat.router)

@app.websocket("/ws/audio")
async def audio_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for data in websocket.iter_bytes():
        transcript = await deepgram_stream(data)  # Convert audio to text
        response = await query_llm(transcript)  # Use ChatGPT API for response
        tts_audio = synthesize_speech(response)  # Convert LLM response to audio
        await websocket.send_bytes(tts_audio)

@app.get("/")
async def root():
    return {"message": "Lucian AI Backend is running."}
