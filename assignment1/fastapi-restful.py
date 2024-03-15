# run with `uvicorn fastapi-restful:app`

import json
from fastapi import FastAPI, Response
from pydantic import BaseModel

from nlp import SpacyDocument

app = FastAPI()


class TextRequest(BaseModel):
    text: str


def format_entities(doc: SpacyDocument):
    result: list[tuple[str, str, int, int]] = []
    for le in doc.get_entities():
        if le.label is not None:
            result.append((le.text, le.label, le.start_idx, le.end_idx))
    return result


def format_dependencies(doc: SpacyDocument):
    result: list[tuple[str, str, str]] = []
    for dep in doc.get_dependencies():
        result.append((dep.parent, dep.rel, dep.child))
    return result


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
    response = format_entities(doc)
    if pretty:
        response = prettify(response)
    return response


@app.post("/dep")
def dep(request: TextRequest, pretty=False):
    doc = SpacyDocument(request.text)
    if pretty:
        response = format_dependencies(doc)
        response = prettify(response)
    else:
        response = doc.get_dependencies()
    return response


def prettify(result):
    json_str = json.dumps(result, indent=2)
    return Response(content=json_str, media_type="application/json")
