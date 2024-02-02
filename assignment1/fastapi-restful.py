# run with `uvicorn fastapi-restful:app`

from fastapi import FastAPI
from pydantic import BaseModel

from assignment1.nlp import SpacyDocument

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.get("/")
def get_api_info(pretty=False):
    return {"message": "API info goes here"}


@app.post("/")
def process(request: TextRequest, pretty=False):
    doc = SpacyDocument(request.text)
    if pretty:
        return doc.get_entities_formatted(mode="html")
    else:
        return doc.get_entities()
