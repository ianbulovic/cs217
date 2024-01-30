"""ner.py

Run spaCy NER over an input string and insert XML tags for each entity.

"""

import io
from typing import Literal
import spacy

nlp = spacy.load("en_core_web_sm")


class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_tokens(self):
        return [token.lemma_ for token in self.doc]

    def get_entities(self):
        entities: list[tuple[int, int, str, str]] = []
        for e in self.doc.ents:
            entities.append((e.start_char, e.end_char, e.label_, e.text))
        return entities

    def get_entities_formatted(self, mode: Literal["html", "st"] = "html"):
        entities = self.doc.ents
        starts = {e.start_char: e.label_ for e in entities}
        ends = {e.end_char: e.label_ for e in entities}
        buffer = io.StringIO()

        if mode == "html":
            for i, char in enumerate(self.text):
                if i in ends:
                    buffer.write("</entity>")
                if i in starts:
                    buffer.write(f'<entity class="{starts[i]}">')
                buffer.write(char)
            markup = buffer.getvalue()
            return f"<markup>{markup}</markup>"
        else:  # mode == "st"
            color_idx = 0
            colors = ["red", "orange", "green", "blue", "violet", "gray"]
            for i, char in enumerate(self.text):
                if i in ends:
                    buffer.write(f"** (*{ends[i]}*)]")
                if i in starts:
                    buffer.write(f":{colors[color_idx % len(colors)]}[**")
                    color_idx += 1
                buffer.write(char)
            return buffer.getvalue()


if __name__ == "__main__":

    example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week."
    )

    doc = SpacyDocument(example)
    print(doc.get_tokens())
    for entity in doc.get_entities():
        print(entity)
    print(doc.get_entities_formatted())
