from fastapi import FastAPI
import uvicorn
from app import api_router

app = FastAPI()
app.include_router(api_router)

@app.get('/')
async def test():
    return {'test':12345678910}


if __name__ == '__main__':
    uvicorn.run("main:app", port=3000, reload=True)