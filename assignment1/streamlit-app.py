# run with `streamlit run streamlit-app.py`

import streamlit as st
from ner import SpacyDocument

st.markdown("### SpaCy NER")

text = (
    "When Sebastian Thrun started working on self-driving cars at "
    "Google in 2007, few people outside of the company took him "
    "seriously. “I can tell you very senior CEOs of major American "
    "car companies would shake my hand and turn away because I wasn’t "
    "worth talking to,” said Thrun, in an interview with Recode earlier "
    "this week."
)
txt = st.text_area("Text to analyze", text)
if st.button("run"):
    doc = SpacyDocument(txt)
    ents = doc.get_entities()
    result = []
    i = 0
    color_idx = 0
    colors = ["red", "orange", "green", "blue", "violet", "gray"]
    for start_idx, end_idx, label, content in ents:
        result.append(txt[i:start_idx])
        result.append(f":{colors[color_idx % len(colors)]}[**{content}** (*{label}*)]")
        color_idx += 1
        i = end_idx

    st.info("".join(result))
