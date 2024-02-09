"""nlp.py

Run spaCy NER and dependency parsing over an input string.

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
        entities: dict[str, tuple[str, int, int]] = {}
        for e in self.doc.ents:
            entities[e.text] = (e.label_, e.start_char, e.end_char)
        return entities

    def get_entities_formatted(self, mode: Literal["html", "st"]):
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
            # mantain consistent mapping from entity labels to colors
            color_map = {}
            colors = ["red", "orange", "green", "blue", "violet"]
            for i, char in enumerate(self.text):
                if i in ends:
                    # close bold block and write label in italics, e.g. "** (*ORG*)"
                    buffer.write(f"** (*{ends[i]}*)]")
                if i in starts:
                    # if this is a new entity label, assign it the next color
                    if starts[i] not in color_map.keys():
                        color_map[starts[i]] = colors[len(color_map) % len(colors)]
                    # apply color and start bold block, e.g. ":red[**"
                    buffer.write(f":{color_map[starts[i]]}[**")
                buffer.write(char)
            return buffer.getvalue()

    def get_dependencies(self):
        dependencies: list[tuple[int, int, str]] = []
        for token in self.doc:
            dependencies.append((token.head.i, token.i, token.dep_))
        return dependencies

    def get_dependencies_formatted(
        self,
        mode: Literal[
            "json",
            "html",
            "st",
        ],
    ):
        buffer = io.StringIO()
        if mode == "json":
            result: dict[str, tuple[str, str]] = {}
            for parent_idx, child_idx, dep in self.get_dependencies():
                parent = self.doc[parent_idx].text
                child = self.doc[child_idx].text
                result[parent] = (dep, child)
            return result
        elif mode == "html":
            for parent_idx, child_idx, dep in self.get_dependencies():
                for grid_item in [
                    self.doc[parent_idx].text,
                    dep,
                    self.doc[child_idx].text,
                ]:
                    buffer.write(f'<div class="grid-item">{grid_item}</div>\n')
        else:  # mode == "st"
            buffer.write("digraph {\n")
            for parent_idx, child_idx, dep in self.get_dependencies():
                parent_text = self.doc[parent_idx].text
                child_text = self.doc[child_idx].text
                buffer.write(
                    f'    "{parent_text}" -> "{child_text}" [label = "{dep}"]\n'
                )
            buffer.write("}\n")
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

    print(doc.get_dependencies_formatted(mode="st"))
