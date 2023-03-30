from fastapi import FastAPI
import uvicorn
from app import api_router

app = FastAPI()
app.include_router(api_router)

@app.get('/')
async def test():
    return "Hello, World!"


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=3333, reload=True)