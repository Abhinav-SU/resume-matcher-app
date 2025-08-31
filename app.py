"""
Streamlit Resume Matcher Application
"""

import streamlit as st
from matcher import rank_resumes
from utils import extract_text
from gemini_api import generate_fit_summary, MissingAPIKeyError
import base64
from concurrent.futures import ThreadPoolExecutor
from logger import logger
import time
import os

st.set_page_config(layout="wide")
st.title("🔍 Candidate Recommendation Engine")

if "results" not in st.session_state:
    st.session_state.results = []
if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""

# =========================
# ==== MAIN PAGE =====
# =========================
if "selected" not in st.session_state:
    job_desc = st.text_area("📝 Enter Job Description", height=300)
    resumes = st.file_uploader("📤 Upload Resumes (.pdf or .docx)", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("🚀 Match Candidates"):
        if not job_desc or not resumes:
            st.warning("Please upload resumes and enter a job description.")
            st.stop()

        logger.info("Match triggered with %d resumes", len(resumes))
        st.session_state.job_desc = job_desc  # Store for summary generation

        def parse_resume(file):
            start = time.time()
            filename = file.name
            display_name = os.path.splitext(filename)[0]
            file_bytes = file.read()
            file.seek(0)  # Reset pointer for future use
            text = extract_text(file_bytes, filename)
            logger.info("Parsed %s in %.2fs (%d bytes)", filename, time.time() - start, len(file_bytes))
            return display_name, text, file_bytes, filename

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(parse_resume, resumes))
        parsed = [r for r in results if r[1].strip()]
        if not parsed:
            st.error("No readable text found in uploaded resumes.")
            st.stop()
        names, texts, file_bytes, filenames = zip(*parsed)
        
        logger.info("Ranking candidates now")
        st.session_state.results = rank_resumes(job_desc, texts, names, file_bytes, filenames)

    # Display Top Matches Table
    if st.session_state.results:
        st.markdown("### 🎯 Top 10 Candidates")
        st.markdown("<hr>", unsafe_allow_html=True)
        header = st.columns([1, 4, 2, 2])
        header[0].markdown("**Rank**")
        header[1].markdown("**Candidate**")
        header[2].markdown("**Similarity**")
        header[3].markdown("**Profile**")

        for i, result in enumerate(st.session_state.results):
            cols = st.columns([1, 4, 2, 2])
            cols[0].markdown(f"{i+1}")
            cols[1].markdown(f"📄 {result['name']}")
            cols[2].markdown(f"`{result['score']:.3f}`")
            if cols[3].button("🔍 View", key=f"view_{i}"):
                st.session_state.selected = result["name"]
                st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# ==== CANDIDATE PAGE =====
# =========================
else:
    selected_name = st.session_state.selected
    candidate = next((r for r in st.session_state.results if r["name"] == selected_name), None)

    if candidate:
        st.header(f"👤 {candidate['name']} - Score: `{candidate['score']:.3f}`")

        # Lazy load summary only when viewing profile
        if "summary" not in candidate:
            with st.spinner("Generating AI summary..."):
                try:
                    summary = generate_fit_summary(st.session_state.job_desc, candidate["resume_text"])
                except MissingAPIKeyError:
                    st.error("GEMINI_API_KEY not configured. Unable to generate summary.")
                    summary = "_GEMINI_API_KEY not configured._"
                candidate["summary"] = summary
                logger.info("Generated summary on-demand for: %s", candidate["name"])
        else:
            summary = candidate["summary"]

        st.subheader("💡 AI Summary")
        st.markdown(summary)

        st.subheader("📄 Resume Preview")
        file_bytes = candidate['file_bytes']
        filename = candidate['file_name']
        ext = filename.lower().split(".")[-1]

        if ext == "pdf":
            try:
                base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
                logger.info("PDF viewer loaded for %s (%d bytes)", candidate["name"], len(file_bytes))
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception as e:
                logger.error("PDF render error for %s: %s", candidate["name"], str(e))
                st.error("Could not load PDF viewer.")
        elif ext == "docx":
            text = extract_text(file_bytes, filename)
            st.text_area("DOCX Resume (Text View)", value=text, height=600)

        st.download_button("⬇️ Download Resume", data=file_bytes, file_name=filename)

        st.markdown("---")
        if st.button("⬅️ Back to Top Candidates"):
            del st.session_state.selected
            st.rerun()
