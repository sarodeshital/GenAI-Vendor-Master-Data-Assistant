import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.data_quality import load_data, add_quality_metrics, summary
from src.duplicate_detection import find_possible_duplicates
from src.database import create_database
from src.assistant import deterministic_answer, llm_answer, build_context

load_dotenv()

st.set_page_config(page_title="GenAI Vendor Master Data Assistant", page_icon="🤖", layout="wide")

DATA_PATH = "data/vendor_master.csv"

@st.cache_data
def prepare():
    raw = load_data(DATA_PATH)
    scored = add_quality_metrics(raw)
    duplicates = find_possible_duplicates(scored)
    return scored, duplicates

df, duplicates = prepare()
metrics = summary(df)

st.title("🤖 GenAI Vendor Master Data Assistant")
st.caption("Explainable vendor master-data quality analysis with an optional LLM layer")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Vendors", metrics["vendors"])
c2.metric("Active Vendors", metrics["active"])
c3.metric("Review Required", metrics["review_required"])
c4.metric("Avg Quality Score", metrics["average_quality_score"])

st.divider()

tab1, tab2, tab3 = st.tabs(["Assistant", "Quality Findings", "Possible Duplicates"])

with tab1:
    st.subheader("Ask the assistant")
    question = st.text_input(
        "Question",
        placeholder="Which vendors have missing critical fields?"
    )

    if st.button("Analyze", type="primary") and question:
        context = build_context(df, duplicates)
        answer = llm_answer(question, context)

        if answer is None:
            answer = deterministic_answer(question, df, duplicates)
            st.info("Demo mode: deterministic answer engine is being used.")
        else:
            st.success("LLM mode enabled.")

        st.markdown(answer)

with tab2:
    st.subheader("Vendor quality findings")
    view = df[
        ["vendor_id", "vendor_name", "country", "status",
         "missing_critical_fields", "quality_score", "review_flag"]
    ].sort_values("quality_score")
    st.dataframe(view, use_container_width=True)

with tab3:
    st.subheader("Possible duplicate vendors")
    if duplicates.empty:
        st.success("No possible duplicate pairs detected.")
    else:
        st.dataframe(duplicates, use_container_width=True)

st.divider()
st.caption(
    "Control principle: automated checks identify records for investigation; "
    "they do not determine fraud or wrongdoing."
)
