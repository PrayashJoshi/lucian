# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat  # Use relative import

app = FastAPI()

# Allow CORS for development purposes (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register chat router
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Lucian AI Backend is running."}
