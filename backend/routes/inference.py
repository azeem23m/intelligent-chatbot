from typing import AsyncGenerator
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse, StreamingResponse

chat = APIRouter()

@chat.post("/infere")
async def infere(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    vector_db = request.app.vector_db
    model = request.app.model

    context = vector_db.query("rag", prompt)
    better_context = '\n'.join([
      f"Paragraph{i+1}:\n{item['text']}\n\nits Metadata: " +
      ', '.join(f"{k}: {v}" for k, v in item['metadata'].items()) + "\n"
      for i, item in enumerate(context)
    ])

    response = model.infere(prompt, better_context)

    return JSONResponse({
        "response": response,
        "context": better_context
    })

@chat.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            context = websocket.app.vector_db.query("rag", data)
            better_context = '\n'.join([
                f"Paragraph{i+1}:\n{item['text']}\nits metadata: " +
                ', '.join(f"{k}: {v}" for k, v in item['metadata'].items()) + "\n"
                for i, item in enumerate(context)
            ])
            await websocket.send_text(f"Context: {better_context}\n\n ##Response: {websocket.app.model.infere(data, better_context)}")

    except WebSocketDisconnect:
        print("Client disconnected")