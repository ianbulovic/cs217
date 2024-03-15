from flask import render_template, request

from formatting import format_entities, format_dependencies
from nlp import SpacyDocument
from webserver.model import Entity, Dependency
from webserver import app


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("Text", type=str, default="")

        # store entities and dependencies in the database
        doc = SpacyDocument(text)
        for ent in doc.doc.ents:
            eid = Entity.add_entity(ent.label_, ent.text).id
            for token in ent:
                Dependency.add_dependency(token.head.text, token.dep_, token.text, eid)

        # display entities and dependencies
        ents = format_entities(doc)
        deps = format_dependencies(doc)
        return render_template("index.html", ents=ents, deps=deps)
    else:  # request.method == "GET"
        return render_template("index.html", result=None)


@app.route("/db_view")
def db_view():
    # construct a list of entities pair with their dependencies
    ents = []
    for ent in Entity.query.all():
        query = Dependency.query.filter_by(entity_id=ent.id).all()
        ents.append(
            (ent.text, [dep.parent + " " + dep.rel + " " + dep.child for dep in query])
        )

    return render_template("dbview.html", ents=ents)
