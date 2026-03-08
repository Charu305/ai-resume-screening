import streamlit as st
from agents.hiring_graph import hiring_graph

st.set_page_config(page_title="AI Hiring Agent", layout="wide")

st.title("AI Resume Screening & Interview Orchestrator")

jd_text = st.text_area("Paste Job Description")
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Run AI Screening") and jd_text and resume_file:
    with st.spinner("Running multi-agent system..."):
        result = hiring_graph.invoke({
            "jd_text": jd_text,
            "resume_file": resume_file
        })

    st.subheader("Final Decision")
    st.json(result)
