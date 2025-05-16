from fastapi import APIRouter, UploadFile, Form, Request, File
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any
import os
import shutil

data = APIRouter()
UPLOAD_FOLDER = "recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@data.post("/audio-upload")
async def upload_audio(
    request: Request,
    audio: UploadFile,
    start_time: float = Form(...),
    end_time: float = Form(...)
) -> Dict[str, Any]:
    
    date_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    metadata = {
        'source': 'audio_transciption',
        'date_time': date_time,
        'start_time': start_time,
        'end_time': end_time
    }

    filename = f"audio_{date_time}.webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    whisper = request.app.whisper
    transcription = whisper.transcribe(filepath, start_time, end_time)
    os.remove(filepath)

    # model = request.app.model
    # summarized = model.summarize(transcription, request.app.previous_summary)
    # accumulated_summary = summarized['response']
    # previous_summary = accumulated_summary

    document = request.app.previous_chunk + '\n' + transcription

    vector_db = request.app.vector_db
    vector_db.add_document(
        collection_name="rag",
        document=document,
        metadata=metadata,
        id=int(date_time)
    )

    request.app.previous_chunk = transcription

    return JSONResponse({
        'metadata': metadata,
        'text': document,
    })


@data.post("/embed")
async def embed(request: Request, payload: Dict[str, Any]):
    response = request.app.vector_db.add_document(
        "rag",
        payload['text'],
        payload['metadata'],
        payload['id']
    )
    return {"response": response}

@data.post("/search")
async def search(request: Request, payload: Dict[str, Any]):
    result = request.app.vector_db.query("rag", payload['query'])
    return {"response": result}
