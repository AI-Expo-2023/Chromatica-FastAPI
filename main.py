from fastapi import FastAPI
import uvicorn
from app import api_router
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(title='Chromatica APP', version='1.0.0')
app.include_router(api_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def test():
    return 'Server is Working!'

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=3333, reload=True)