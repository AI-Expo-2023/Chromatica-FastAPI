from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import uvicorn


class Item(BaseModel):
    prompt: str
    W: Union[int, None] = None
    H: Union[int, None] = None
    steps: Union[int, None] = None
    format: Union[str, None]
    samples: Union[int, None] = None


app = FastAPI()

@app.get('/')
def test():
    return {'test':356}

@app.post('/test/')
def post_test(item: Item):
    return item


if __name__ == '__main__':
    uvicorn.run("main:app", port=3000, reload=True)