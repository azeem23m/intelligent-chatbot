import os
import cohere
from dotenv import load_dotenv

load_dotenv()


class CohereChat:

  def __init__(self):
    self.client = cohere.ClientV2(api_key=os.getenv("COHERE_KEY"))
  
  def infere(self, prompt: str, context: str=None):
    full_prompt = f"""Answer the question based on the given context, if the answer is not directly given \
    you must comprehened the context, if the answer isn't in the context or isn't comprehended in at least one paragraph \
    say that you didn't find it in the System and write you own answer
    ##Question
    {prompt}

    ##Context
    {context}
    
    ##Answer: 
    """

    if not context:
      full_prompt = prompt

    response = self.client.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": full_prompt}],
    )

    return response.message.content[0].text
  
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

    ##Chunk:
    {chunk} 
    """

    response = self.client.chat(
          model="command-a-03-2025",
          messages=[{"role": "user", "content": full_prompt}],
      )


    return response.message.content[0].text
