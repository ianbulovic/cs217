# run with `uvicorn fastapi-restful:app`

import json
from fastapi import FastAPI, Response
from pydantic import BaseModel

from nlp import SpacyDocument

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.get("/")
def get_api_info(pretty=False):
    content = "Content-Type: application/json"
    url = "http://127.0.0.1:8000/<ner|dep><?pretty=true>"
    response = {
        "description": "Interface to the spaCy entity extractor",
        "usage": f'curl {url} -H "{content}" -d@input.json',
    }
    if pretty:
        response = prettify(response)
    return response


@app.post("/ner")
def ner(request: TextRequest, pretty=False):
    doc = SpacyDocument(request.text)
    response = doc.get_entities()
    if pretty:
        response = prettify(response)
    return response


@app.post("/dep")
def dep(request: TextRequest, pretty=False):
    doc = SpacyDocument(request.text)
    if pretty:
        response = doc.get_dependencies_formatted("json")
        response = prettify(response)
    else:
        response = doc.get_dependencies()
    return response


def prettify(result):
    json_str = json.dumps(result, indent=2)
    return Response(content=json_str, media_type="application/json")
