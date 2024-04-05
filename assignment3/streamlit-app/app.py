# run with `streamlit run app.py`

from io import StringIO
import pandas as pd
import streamlit as st
from nlp import SpacyDocument, LabeledEntity

st.markdown("### SpaCy NER")

default_text = (
    "When Sebastian Thrun started working on self-driving cars at "
    "Google in 2007, few people outside of the company took him "
    "seriously. “I can tell you very senior CEOs of major American "
    "car companies would shake my hand and turn away because I wasn’t "
    "worth talking to,” said Thrun, in an interview with Recode earlier "
    "this week."
)


def format_entities(doc: SpacyDocument):
    color_map = {}
    colors = ["red", "orange", "green", "blue", "violet"]

    def wrap_entity(le: LabeledEntity):
        if le.label is None:
            return le.text
        else:
            next_color = colors[len(color_map) % len(colors)]
            color = color_map.setdefault(le.label, next_color)
            return f":{color}[**{le.text}** (*{le.label}*)]"

    return "".join(wrap_entity(le) for le in doc.get_entities())


def dependency_graph(doc: SpacyDocument) -> str:
    buffer = StringIO()
    buffer.write("digraph {\n")
    buffer.writelines(
        f'    "{dep.parent}" -> "{dep.child}" [label = "{dep.rel}"]'
        for dep in doc.get_dependencies()
    )
    buffer.write("}\n")
    return buffer.getvalue()


text = st.text_area("Text to analyze", default_text)

if st.button("run"):

    doc = SpacyDocument(text)

    ents = format_entities(doc)
    st.info(ents)

    deps = doc.get_dependencies()
    df = pd.DataFrame(
        {
            "Parent Index": dep.parent_idx,
            "Parent Token": dep.parent,
            "Child Index": dep.child_idx,
            "Child Token": dep.child,
            "Dependency": dep.rel,
        }
        for dep in deps
    )

    table_tab, graph_tab = st.tabs(("Table", "Graph"))
    with table_tab:
        st.dataframe(df)
    with graph_tab:
        deps_graphviz: str = dependency_graph(doc)
        st.graphviz_chart(deps_graphviz)
