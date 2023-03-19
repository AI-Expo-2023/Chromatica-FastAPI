from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def test():
    return {'test':356}

if __name__ == '__main__':
    uvicorn.run("main:app", port=3000, reload=True)