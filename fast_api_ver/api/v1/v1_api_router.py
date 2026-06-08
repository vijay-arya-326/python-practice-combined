from fastapi import APIRouter
from fastapi.responses import Response,JSONResponse, StreamingResponse

from api.model.async_model import chatCompletion

api_v1_router = APIRouter()

@api_v1_router.get("/hello_world")
async def hello_world():
    return {"message": "Hello World"}

@api_v1_router.get("/health", tags=["health_check"])
async def health():
    return JSONResponse({"status": "server running"})

@api_v1_router.get("/chat-with-api", tags=["Chat With API"])
async def streamResponse(que=""):
    print(que)
    if que:
        return StreamingResponse(chatCompletion(que), media_type="text/plain")