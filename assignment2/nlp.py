"""nlp.py

Run spaCy NER and dependency parsing over an input string."""

import io
from dataclasses import dataclass
import spacy

nlp = spacy.load("en_core_web_sm")


@dataclass
class LabeledEntity:
    text: str
    label: str | None
    start_idx: int
    end_idx: int


@dataclass
class Dependency:
    parent: str
    rel: str
    child: str
    parent_idx: int
    child_idx: int


class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_tokens(self):
        return [token.lemma_ for token in self.doc]

    def get_entities(self):
        """This generator iterates over the document and
        yields `LabeledEntity` objects, split on entity boundaries.
        For chunks of text that are not part of an entity, this will yield a
        `LabeledEntity` with `le.label == None`."""

        # map boundary indices to entity label
        boundaries: dict[int, str | None] = {0: None}
        for e in self.doc.ents:
            boundaries.setdefault(e.end_char, None)
            boundaries[e.start_char] = e.label_

        current_label = None
        buffer = io.StringIO()
        start_idx = 0
        end_idx = 0

        for i, char in enumerate(self.text):
            if i in boundaries:
                start_idx = end_idx
                end_idx = i
                yield LabeledEntity(
                    buffer.getvalue(), current_label, start_idx, end_idx
                )
                buffer = io.StringIO()
                current_label = boundaries[i]
            buffer.write(char)

        yield LabeledEntity(buffer.getvalue(), current_label, start_idx, end_idx)

    def get_dependencies(self) -> list[Dependency]:
        dependencies: list[Dependency] = []
        for token in self.doc:
            dependencies.append(
                Dependency(
                    token.head.text, token.dep_, token.text, token.head.i, token.i
                )
            )
        return dependencies
