import os
import sys
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from api.v1.v1_api_router import api_v1_router

env_path = Path(__file__).resolve().parent.parent.joinpath("env/.env")
print("="*60)
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    print(f"env Loaded... {os.getenv("FAST_API_PORT")}")
else:
    sys.exit("Could not find .env file")
print("="*60)

port = (os.getenv("FAST_API_PORT", "8081"))
host = "127.0.0.1"

os.environ["PORT"] = port

app = FastAPI()
app.include_router(api_v1_router, prefix="/api/v1")



