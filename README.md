# meetAI

**meetAI** is a real-time meeting assistant that transcribes speech, stores transcription data, and allows users to ask questions based on meeting content using LLMs.

It enhances retrieval by enabling semantic and lexical search over chunks, and contextualizes each chunk using an LLM to preserve conversational flow.

---

## Features

- **Real-time audio transcription** using [WhisperX](https://github.com/m-bain/whisperx) [✅]
- **Storage** of transcriptions in a vector database (Qdrant) [✅]
- **Contextual chunking**: Using LLM to link chunks by providing a context of previous information [✅]
- **Hybrid Search**: Supports both semantic (dense) and lexical (sparse) search for accurate results [✅]
- **File Uploads**: Supports PDF & PPTX files upload and processing [ ]

---

## Architecture

![](architecture.png)

---

## Installation

- Make a virtual enviroment and activate it
- Install requirements ```pip install -r requirements.txt``` and then inside frontend ```npm i```
- Run Qdrant Docker Image ```docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant```
- Make two terminals inside the folders frontend and backend
- Make .env file by ```mv .env.example .env``` and fill in API Keys
- Run backend by ```uvicorn main:app --port 8000 --reload```
- Run fronend by ```npm run dev```
- Open ```http://127.0.0.1:8501``` in your browser

---

## Tech Stack

- **Backend**: Python with FastAPI
- **Speech-to-Text**: WhisperX running `distil-large-v3-turbo`
- **LLM Interface**: [OpenRouter](https://openrouter.ai/) for unified access to various language models
- **Embeddings**:
  - **Dense**: Cohere’s `embed-multilingual-light-v3.0`
  - **Sparse**: BM25 via FastEmbed
- **Vector Store**: Qdrant
- **Frontend**: React, based on the [Chatbot UI template](https://github.com/ChristophHandschuh/chatbot-ui), with custom modifications
