from langchain_ollama import ChatOllama
import os

def chatOllamaMistral():
    mistral_model = os.getenv("MISTRAL_MODEL", "MISTRAL")
    mistral_agent = ChatOllama(model=mistral_model, temperature= 0.1)
    return mistral_agent


def chatOllamaGemma():
    gemma_model = os.getenv("GEMMA_MODEL", "GEMMA")
    gemma_agent = ChatOllama(model=gemma_model, temperature= 0.1)
    return gemma_agent

def chatOllamaLlama():
    llama_model = os.getenv("LLAMA_MODEL", "LLAMA3.2")
    llama_agent = ChatOllama(model=llama_model, temperature= 0.1)
    return llama_agent

def chatOllamaGemma4():
    model = os.getenv("GEMMA4_MODEL", "gemma4:e2b")
    agent = ChatOllama(model=model, temperature= 0.1)
    return agent




if __name__ == "__main__":
    message = "how are you?"
    from pathlib import Path
    env_path = Path.cwd().parent.parent.parent.joinpath("env").joinpath(".env")
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path, override=True)
    print("TESTING AGENT 1")
    mistral_agent = chatOllamaMistral()
    mistral_response  = mistral_agent.invoke(message)
    print(mistral_response.content)

    print("TESTING AGENT 2")
    gemma_agent = chatOllamaGemma()
    gemma_response  = gemma_agent.invoke(message)
    print(gemma_response.content)

    print("TESTING AGENT 3")
    llama_agent = chatOllamaLlama()
    llama_response  = llama_agent.invoke(message)
    print(llama_response.content)

    print("TESTING AGENT 4")
    gemma4_agent = chatOllamaGemma4()
    gemma4_response  = gemma4_agent.invoke(message)
    print(gemma4_response.content)


