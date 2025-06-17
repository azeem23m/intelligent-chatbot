import os
from openai import OpenAI
from dotenv import load_dotenv

import time

load_dotenv()


class LLM:

  def __init__(self):
    self.client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=os.getenv("OPEN_ROUTER_KEY"),
    )
  

  def chat(self, prompt):
    completion = self.client.chat.completions.create(
      model=os.getenv("OPEN_ROUTER_MODEL"),
      messages=[
        {
          "role": "user",
          "content": prompt
        }
      ],
      # think=False
    )

    return completion.choices[0].message.content

  def infere(self, prompt: str, context: str=None):
    full_prompt = f"""You are a knowledgeable, helpful assistant. Answer all user questions as if you possess extensive, general knowledge. You may have access to background knowledge, but you must never refer to it explicitly — do not mention "context", "documents", "sources", or anything similar.

Your behavior must follow these rules:
- Answer clearly, concisely, and factually.
- If you are confident in the answer, state it directly and professionally.
- If there isn't enough information to answer with confidence, say:
  "I don't have enough information to answer that definitively, but here's what I can share:"
  Then offer the most relevant, honest insight you can.
- Never mention that certain information is or isn’t relevant.
- Do not speculate wildly or hallucinate facts. If uncertain, say so plainly.
- Do not describe or refer to having access to any external documents or user-provided content.

Your goal is to behave like a human expert who simply knows things — not like a model using external inputs.

    ## Question
    {prompt}

    ## Context
    {context}
    
    ## Answer: 
    """

    if not context:
      full_prompt = prompt

    completion = self.client.chat.completions.create(
      model=os.getenv("OPEN_ROUTER_MODEL"),
      messages=[
        {
          "role": "user",
          "content": full_prompt
        }
      ],
      # think=False
    )

    return completion.choices[0].message.content
  
  def generate_context(self, chunk: str, history: str) -> str:

    full_prompt = f"""
    ## Document
    {history}
    Please give a succinct context to situate this chunk within the overall document for the purposes \
    of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
    You can use the following guidelines:
    1. If possible Identify the speakers and information they gave related to chunk.
    2. Relate the current information to previous ones without losing details.
    3. Don't use phrases like "This section provides" or similar.
    4. If the history is empty return the same chunk.

    ## Chunk:
    {chunk} 
    """

    completion = self.client.chat.completions.create(
      model=os.getenv("OPEN_ROUTER_MODEL"),
      messages=[
        {
          "role": "user",
          "content": full_prompt
        }
      ],
      # think=False
    )


    return completion.choices[0].message.content
  


# chat = LLM()

# start = time.time()
# print(
#   chat.chat("explain grandfather paradox")
# )
# print(time.time() - start)
