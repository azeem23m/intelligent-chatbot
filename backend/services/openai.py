import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from openai import AzureOpenAI
import asyncio

from dotenv import load_dotenv
load_dotenv()

class OpenAI():
  def __init__(self, api_key = os.getenv("OPEN_AI_KEY"), end_point='https://mm303-mabeif8e-eastus2.cognitiveservices.azure.com/', api_version = "2024-12-01-preview"):
    self.api_key = api_key
    self.url = end_point

    self.client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=self.url,
    api_key=self.api_key,
)

  def infere(self, prompt, context):

    full_prompt = f"""Answer the question based on the given context, the answer is not directly given \
    you must comprehened the context, if the answer isn't in the context or isn't comprehended neither \
    provide you answer and say that you didn't find it in the System and write you own answer
    ##Question
    {prompt}

    ##Context
    {context}
    
    ##Answer: 
    """

    response = self.client.chat.completions.create(
      messages=[
          {
              "role": "user",
              "content": full_prompt,
          }
      ],
      max_tokens=1024,
      temperature=1.0,
      top_p=1.0,
      model="gpt-4o"
  )

    return {
      "response": response.choices[0].message.content,
      "model": response.model,
      "usage":{
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
        "completion_tokens": response.usage.completion_tokens
      }
    }


  def summarize(self, transcription, summary_so_far=""):

    full_prompt = f"""Given summary so far, append information from previous summary into transcription \
    if the previous summary is not related to current transcription discard the previous summary.
    ## Summary So Far:
    {summary_so_far}

    ## New Transcription:
    {transcription}
    
    ## Updated Summary:
    """

    response = self.client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
        max_tokens=1024,
        temperature=1.0,
        top_p=1.0,
        model="gpt-4o"
    )

    return {
      "response": response.choices[0].message.content,
      "model": response.model,
      "usage":{
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
        "completion_tokens": response.usage.completion_tokens
      }
    }
  
  async def stream(self, prompt):


    client = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=self.url,
        api_key=self.api_key,
    )

    try:
      response = await asyncio.to_thread(
          client.chat.completions.create,
          stream=True,
          messages=[{"role": "user", "content": prompt}],
          max_tokens=1024,
          temperature=1.0,
          top_p=1.0,
          model="gpt-4o",
      )

      for update in response:
          if update.choices:
              chunk = update.choices[0].delta.content or ""
              yield chunk  # Yielding the chunk to the streaming response
              await asyncio.sleep(0.1)  # Optional: Delay between chunks

    except HttpResponseError as e:
        print(f"Error: {e}")
    finally:
        client.close()