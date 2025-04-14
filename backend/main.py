from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.groq_ai import process_query
from backend.screen_capture import get_screen_data

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "guys this is basic template of codes with files we need to use groq tools and also screen pipe tools and integrate them further"}

@app.get("/query")
def handle_query(q: str):
    return process_query(q)

@app.get("/screens")
def get_screens():
    return get_screen_data()
