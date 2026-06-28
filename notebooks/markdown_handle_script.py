""" ASYNC WITH CHAT COMPLETION """
from dotenv import load_dotenv
from pathlib import Path
import sys

lib_path = str(Path.cwd().parent.parent)
sys.path.append(lib_path)
cwd = Path.cwd().parent.joinpath("env/.env")

if cwd.exists():
    load_dotenv(dotenv_path=cwd, override=True)
else:
    print("No .env file found")
    sys.exit(1)

import asyncio
import os
from openai import AsyncOpenAI
from IPython.display import display, update_display, Markdown

ollama_baseurl =  os.getenv("OLLAMA_BASE_URL")
ollama_async = AsyncOpenAI(base_url= ollama_baseurl, api_key="ollamalocal")
#%%
messages_stream = [{
    "role":"system", "content":
    "You are very snarky assistant named eddie, give you name while providing response"
}]
messages_stream += [{"role":"user", "content":"Hi"}]
messages_stream +=[{"role":"user", "content":"Explain quntam computing"}]

async def chatCompletion():
    stream = await ollama_async.chat.completions.create(
        model=os.getenv("GEMMA4_MODEL"),
        messages=messages_stream,
        reasoning_effort="high",
        temperature=1,
        stream= True
    )
    printed_final_answer = False

    markdown_id = "test_markdown"

    # handle = display("QWQDWQWD", display_id=True)
    # if handle is not None:
    #     script_display_id = handle.display_id
    #     print(f"Successfully captured Display ID in script: {script_display_id}")
    # else:
    #     print("Display OBJECT NOT FOUND")


    async for chunks in stream:
        # print("Display Id : ", handle.display_id)
        # print("==========================\n")
        delta = chunks.choices[0].delta

        reasoning = getattr(delta, "reasoning", None)
        reasoning_content = getattr(delta, "reasoning_content", None)
        content = getattr(delta, "content", None)

        final_response = ""

        if reasoning:
            final_response += reasoning
            # print(reasoning, end="", flush=True)

        if reasoning_content:
            final_response += reasoning_content
            # print(reasoning_content, end="", flush=True)

        if content:
            if not printed_final_answer:
                final_response +="\n\n===== Final Answer: =====\n\n"
                # print("\n\n===== Final Answer: =====\n\n", end="", flush=True)
                printed_final_answer = True
            # print(content, end="", flush=True)
            final_response += content

        print(final_response, end="", flush=True)
        # update_display(Markdown(final_response))

if __name__ == "__main__":
    print("Started Working... ")
    asyncio.run(chatCompletion())