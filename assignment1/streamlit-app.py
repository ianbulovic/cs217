# run with `streamlit run streamlit-app.py`

import pandas as pd
import streamlit as st
from nlp import SpacyDocument

st.markdown("### SpaCy NER")

default_text = (
    "When Sebastian Thrun started working on self-driving cars at "
    "Google in 2007, few people outside of the company took him "
    "seriously. “I can tell you very senior CEOs of major American "
    "car companies would shake my hand and turn away because I wasn’t "
    "worth talking to,” said Thrun, in an interview with Recode earlier "
    "this week."
)

text = st.text_area("Text to analyze", default_text)
if st.button("run"):
    doc = SpacyDocument(text)
    ents = doc.get_entities_formatted(mode="st")
    st.info(ents)
    table_tab, graph_tab = st.tabs(("Table", "Graph"))
    with table_tab:
        deps = doc.get_dependencies()
        df = pd.DataFrame(deps, columns=["Parent Index", "Child Index", "Dependency"])
        df.insert(
            0,
            "Parent Token",
            [doc.doc[idx].text for idx in map(lambda dep: dep[0], deps)],
        )
        df.insert(
            2,
            "Child Token",
            [doc.doc[idx].text for idx in map(lambda dep: dep[1], deps)],
        )
        st.dataframe(df)
    with graph_tab:
        deps_graphviz: str = doc.get_dependencies_formatted(mode="st")  # type: ignore
        st.graphviz_chart(deps_graphviz)
