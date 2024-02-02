# run with `python3 flask-webserver.py`

from flask import Flask, request, render_template

from nlp import SpacyDocument


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("Text", type=str)
        doc = SpacyDocument(text)  # type: ignore
        ents = doc.get_entities_formatted(mode="html")
        deps = doc.get_dependencies_formatted(mode="html")
        return render_template("index.html", ents=ents, deps=deps)
    else:  # request.method == "GET"
        return render_template("index.html", result=None)


if __name__ == "__main__":
    app.run(debug=True)
