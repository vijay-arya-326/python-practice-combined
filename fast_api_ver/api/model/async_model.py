import asyncio
import os
from openai import AsyncOpenAI
ollama_baseurl =  os.getenv("OLLAMA_BASE_URL")
ollama_async = AsyncOpenAI(base_url= ollama_baseurl, api_key="ollamalocal")




async def chatCompletion(question):
    messages_stream = [{"role": "system",
                        "content": "You are very snarky assistant named eddie, give you name while providing response"}]
    messages_stream += [{"role": "user", "content": "Hi"}]
    messages_stream += [{"role": "user", "content": question    }]

    stream = await ollama_async.chat.completions.create(
        model=os.getenv("PHI_MODEL_3"),
        messages=messages_stream,
        stream= True
    )

    async for chunks in stream:
      msg = chunks.choices[0].delta.content or ""
      yield msg

if __name__ == "__main__":
     asyncio.run(chatCompletion())