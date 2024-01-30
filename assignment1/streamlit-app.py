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
    result = doc.get_entities_formatted(mode="st")
    st.info(result)
