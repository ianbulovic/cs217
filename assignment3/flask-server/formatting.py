from io import StringIO
from nlp import SpacyDocument, LabeledEntity


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
