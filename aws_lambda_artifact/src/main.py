import uvicorn
from fastapi import FastAPI
from mangum import Mangum

from src.users.router import router as users_router
from src.auth.router import router as auth_router
from src.chat.router import router as chat_router

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(chat_router)

handler = Mangum(app)


@app.get("/")
async def hello():
    return {"message": "Hello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)