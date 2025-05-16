from fastapi import FastAPI
from services import VectorDB, OpenAI, Whisper
from routes import data, chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.vector_db = VectorDB()
app.model = OpenAI()
app.whisper = Whisper()
app.previous_chunk = ""

app.include_router(chat, prefix="/chat")
app.include_router(data, prefix="/data")

@app.get("/")
async def home():
    return {
        'response': True
    }

if __name__ == '__main__':
    app.run(debug=True)
