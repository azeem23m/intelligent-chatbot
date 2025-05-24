from fastapi import APIRouter, UploadFile, Request
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
) -> Dict[str, Any]:
    
    date_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f"audio_{date_time}.webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    transcription, start, end = request.app.whisper.transcribe(filepath)
    os.remove(filepath)
    
    metadata = {
        'source': 'audio_transciption',
        'date_time': date_time,
        'start_time': request.app.time,
        'end_time': request.app.time + end
    }
    request.app.time += end

    processed_context = request.app.model.generate_context(transcription, request.app.history)
    request.app.history += f" {transcription} "


    # print(f"Transcription: {transcription}\n\nContext: {processed_context}\n\nHistory: {request.app.history}\n\n")
    
    document = f"Transcription: {transcription}\nSummary: {processed_context}"

    request.app.vector_db.add_document(
        collection_name="rag",
        document=document,
        metadata=metadata,
        id=int(date_time)
    )

    return JSONResponse({
        'metadata': metadata,
        'text': transcription,
        'start': start,
        'end': end
    })


@data.get("/reset-history")
async def reset(request: Request):
    request.app.history = ""
    request.app.time = 0
    return JSONResponse({"message": True})