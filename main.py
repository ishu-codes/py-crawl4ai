import asyncio
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crawl import get_markdown
from crawl4ai import *

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://your-frontend-domain.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "title": "py-crawl4ai",
        "version": "0.1",
        "author": "Ishu"
    }

@app.get("/api/markdown")
async def get_markdown_endpoint(q: Union[str, None] = None, depth:Union[int, None]=0):
    if q is None:
        return {"status": "error", "message":"query not provided"}
    result = await get_markdown(q, depth or 0)
    return {"result": result}

