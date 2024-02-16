# run with `python3 flask-webserver.py`

from io import StringIO
from flask import Flask, request, render_template

from nlp import SpacyDocument, LabeledEntity


app = Flask(__name__)


def format_entities(doc: SpacyDocument):
    def wrap_entity(le: LabeledEntity):
        if le.label is None:
            return le.text
        else:
            return f"<entity class={le.label}>{le.text}</entity>"

    full = "".join(wrap_entity(le) for le in doc.get_entities())
    return f"<markup>{full}</markup>"


def format_dependencies(doc: SpacyDocument):
    buffer = StringIO()
    for dep in doc.get_dependencies():
        for grid_item in [dep.parent, dep.rel, dep.child]:
            buffer.write(f'<div class="grid-item">{grid_item}</div>\n')
    return buffer.getvalue()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("Text", type=str, default="")
        doc = SpacyDocument(text)
        ents = format_entities(doc)
        deps = format_dependencies(doc)
        return render_template("index.html", ents=ents, deps=deps)
    else:  # request.method == "GET"
        return render_template("index.html", result=None)


if __name__ == "__main__":
    app.run(debug=True)
