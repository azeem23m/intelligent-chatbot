from fastapi import FastAPI
from services import VectorDB, CohereChat, Whisper
from routes import data, chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import torch
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.vector_db = VectorDB()
app.model = CohereChat()
app.whisper = Whisper()
app.history = ""
app.time = 0

app.include_router(chat, prefix="/chat")
app.include_router(data, prefix="/data")


if __name__ == '__main__':
    app.run(debug=True)
