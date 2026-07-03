
import sys
import os
from pathlib import Path

PDF_PROCESSING_DIR = Path(__file__).resolve().parent
RETRIEVAL_DIR = PDF_PROCESSING_DIR / "retrieval"
PIPELINE_DIR = PDF_PROCESSING_DIR / "pipeline"

for _p in (PDF_PROCESSING_DIR, PIPELINE_DIR, RETRIEVAL_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import streamlit as st
import requests

from pipeline.ingest import ingest_pdf, list_papers

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ResearchGPT",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
<style>
/* ── global background ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background-color: #F8F4ED !important;
}

[data-testid="stHeader"] {
    background-color: #F8F4ED !important;
}

/* ── hide default Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }

/* ── typography ── */
h1 { color: #2C1A0E; font-weight: 700; letter-spacing: -0.5px; }
h2, h3 { color: #3D2B1F; }
p, li, label { color: #4A3728; }

/* ── card container ── */
.card {
    background: #FFFDF8;
    border: 1px solid #E8DDD0;
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* ── answer / result card ── */
.result-card {
    background: #FFFDF8;
    border: 1px solid #D4C4B0;
    border-left: 4px solid #8B6B4A;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
}

/* ── citation chip ── */
.cite-chip {
    display: inline-block;
    background: #EDE3D8;
    color: #5C3D2A;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin: 2px 3px;
    font-weight: 500;
}

/* ── pill badge ── */
.paper-badge {
    display: inline-block;
    background: #C8A882;
    color: #2C1A0E;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 2px 3px;
}

/* ── success / error banners ── */
.banner-success {
    background: #EEF8EE;
    border: 1px solid #9BC89B;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #2A5C2A;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
.banner-error {
    background: #FEF2F2;
    border: 1px solid #FCBCBC;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #7B2020;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
.banner-info {
    background: #F0F4FF;
    border: 1px solid #B8C8F8;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #1A2C6B;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

/* ── primary button ── */
.stButton > button {
    background: #7A5535 !important;
    color: #FFFDF8 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: background 0.2s ease;
    width: 100%;
}
.stButton > button:hover {
    background: #5E3E25 !important;
}

/* ── text inputs ── */
.stTextArea textarea, .stTextInput input {
    background: #FFFDF8 !important;
    border: 1px solid #D4C4B0 !important;
    border-radius: 10px !important;
    color: #2C1A0E !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #8B6B4A !important;
    box-shadow: 0 0 0 2px rgba(139,107,74,0.15) !important;
}

/* ── select box ── */
.stSelectbox > div > div {
    background: #FFFDF8 !important;
    border: 1px solid #D4C4B0 !important;
    border-radius: 10px !important;
    color: #2C1A0E !important;
}

/* ── file uploader ── */
[data-testid="stFileUploader"] {
    background: #FFFDF8 !important;
    border: 2px dashed #C8A882 !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7A5535 !important;
}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: #EDE3D8 !important;
    border-radius: 10px 10px 0 0 !important;
    color: #5C3D2A !important;
    font-weight: 600;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: #7A5535 !important;
    color: #FFFDF8 !important;
}

/* ── spinner ── */
.stSpinner > div { border-top-color: #7A5535 !important; }

/* ── divider ── */
hr { border-color: #E8DDD0; }

/* ── block container ── */
.block-container { padding-top: 1.5rem; max-width: 1100px; }
</style>
""",
    unsafe_allow_html=True,
)

if "session_papers" not in st.session_state:
    st.session_state.session_papers = []   # papers uploaded THIS session
if "ingest_results" not in st.session_state:
    st.session_state.ingest_results = []


st.markdown("## 📚 ResearchGPT")
st.markdown(
    "<p style='color:#7A5535;margin-top:-0.5rem;font-size:1rem;'>"
    "Upload research papers and ask questions, generate summaries, or compare them.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("### Upload Papers")
st.markdown(
    "<p style='color:#6B5040;font-size:0.9rem;'>Upload up to 2 PDF research papers. "
    "They will be processed automatically.</p>",
    unsafe_allow_html=True,
)

uploaded_files = st.file_uploader(
    "Drag & drop PDF files here, or click to browse",
    type=["pdf"],
    accept_multiple_files=True,
    help="Maximum 2 PDFs. Text-based PDFs only (not scanned).",
    label_visibility="collapsed",
)


if uploaded_files and len(uploaded_files) > 2:
    st.markdown(
        "<div class='banner-error'>⚠️ Please upload a maximum of 2 PDFs at a time.</div>",
        unsafe_allow_html=True,
    )
    uploaded_files = uploaded_files[:2]


if uploaded_files:
    filenames = [f.name for f in uploaded_files]
    st.markdown(
        f"<div class='banner-info'>📎 Selected: <strong>{', '.join(filenames)}</strong></div>",
        unsafe_allow_html=True,
    )

    if st.button("⚡ Process Papers", key="process_btn"):
        st.session_state.ingest_results = []
        st.session_state.session_papers = []

        progress_bar = st.progress(0, text="Starting pipeline…")
        results_container = st.container()

        total = len(uploaded_files)

        for idx, file in enumerate(uploaded_files):
            progress_bar.progress(
                int((idx / total) * 90),
                text=f"Processing {file.name}… (step {idx+1}/{total})",
            )

            
            with st.spinner(f"Running pipeline for **{file.name}**…"):

                response = requests.post(
        f"{API_URL}/upload",
        files={
            "file": (
                file.name,
                file.getvalue(),
                            "application/pdf"
                        )
                    },
                    timeout=600
                )

                response.raise_for_status()

                result = response.json()
            st.session_state.ingest_results.append(result)

            if result["error"] is None:
                st.session_state.session_papers.append(result["paper_name"])

        progress_bar.progress(100, text="Done!")

        with results_container:
            for res in st.session_state.ingest_results:
                if res["error"]:
                    st.markdown(
                        f"<div class='banner-error'>❌ <strong>{res['paper_name']}</strong> — "
                        f"{res['error']}</div>",
                        unsafe_allow_html=True,
                    )
                elif res["already_existed"]:
                    st.markdown(
                        f"<div class='banner-info'>ℹ️ <strong>{res['paper_name']}</strong> — "
                        f"Already indexed. Ready to use.</div>",
                        unsafe_allow_html=True,
                    )
                    if res["paper_name"] not in st.session_state.session_papers:
                        st.session_state.session_papers.append(res["paper_name"])
                else:
                    st.markdown(
                        f"<div class='banner-success'>✅ <strong>{res['paper_name']}</strong> — "
                        f"Indexed {res['chunks']} chunks successfully.</div>",
                        unsafe_allow_html=True,
                    )


all_db_papers = list_papers()

if all_db_papers:
    badge_html = " ".join(
        f"<span class='paper-badge'>📄 {p.title()}</span>"
        for p in all_db_papers
    )
    st.markdown(
        f"<p style='color:#6B5040;font-size:0.85rem;margin-top:0.5rem;'>"
        f"Available in database: {badge_html}</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")


if not all_db_papers:
    st.markdown(
        "<div class='banner-info' style='text-align:center;padding:2rem;'>"
        "📤 Upload at least one PDF above to get started.</div>",
        unsafe_allow_html=True,
    )
    st.stop()


tab1, tab2, tab3 = st.tabs(["💬  Ask a Question", "📝  Summarize", "⚖️  Compare"])



with tab1:
    st.markdown("### Ask a Question")
    st.markdown(
        "<p style='color:#6B5040;font-size:0.9rem;'>Select a paper and type your question. "
        "The AI will search the most relevant passages to answer.</p>",
        unsafe_allow_html=True,
    )

    selected_paper_qa = st.selectbox(
        "Paper",
        options=all_db_papers,
        format_func=lambda x: x.title(),
        key="qa_paper_select",
    )

    question = st.text_area(
        "Your question",
        placeholder="e.g. What is the multi-head attention mechanism?",
        height=100,
        key="qa_question",
    )

    if st.button("Ask ✦", key="ask_btn"):
        if not question.strip():
            st.markdown(
                "<div class='banner-error'>Please enter a question.</div>",
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("Searching and generating answer…"):
                try:
                    # Inject paper name into question so classify_paper picks right paper
                    response = requests.post(
                    f"{API_URL}/ask",
                    json={
                    "question": question,
                    "paper_name": selected_paper_qa
                },
                    timeout=120
)   
                    response.raise_for_status()
                    result = response.json()

                    st.markdown(
                        "<div class='banner-success'>✅ Answer generated</div>",
                        unsafe_allow_html=True,
                    )

                    st.markdown("#### Answer")
                    st.markdown(
                        f"<div class='result-card'>{result.get('answer','—')}</div>",
                        unsafe_allow_html=True,
                    )

                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown("**Paper**")
                        st.markdown(
                            f"<span class='paper-badge'>📄 {result.get('paper_name','').title()}</span>",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.markdown("**Sources (top chunks)**")
                        sources = result.get("sources", [])
                        chips = " ".join(
                            f"<span class='cite-chip'>Chunk {s['metadata']['chunk_id']}</span>"
                            for s in sources
                        )
                        if chips:
                            st.markdown(chips, unsafe_allow_html=True)
                        else:
                            st.markdown("—")

                except requests.exceptions.ConnectionError:
                    st.markdown(
                        "<div class='banner-error'>❌ Cannot connect to the backend API. "
                        "Make sure FastAPI is running at <code>http://127.0.0.1:8000</code>.</div>",
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.markdown(
                        f"<div class='banner-error'>❌ Error: {e}</div>",
                        unsafe_allow_html=True,
                    )




with tab2:
    st.markdown("### Summarize a Paper")
    st.markdown(
        "<p style='color:#6B5040;font-size:0.9rem;'>Select a paper to generate a "
        "comprehensive AI summary covering objectives, methodology, results, and more.</p>",
        unsafe_allow_html=True,
    )

    selected_paper_sum = st.selectbox(
        "Paper to summarize",
        options=all_db_papers,
        format_func=lambda x: x.title(),
        key="sum_paper_select",
    )

    if st.button("Generate Summary ✦", key="summary_btn"):
        with st.spinner(
            "Generating summary — this may take a minute for longer papers…"
        ):
            try:
                response = requests.post(
                    f"{API_URL}/summary",
                    json={
                    "paper_name": selected_paper_sum
    },
                        timeout=300
)
                response.raise_for_status()
                result = response.json()

                st.markdown(
                    "<div class='banner-success'>✅ Summary generated</div>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"<span class='paper-badge'>📄 {result.get('paper_name','').title()}</span>",
                    unsafe_allow_html=True,
                )

                st.markdown("#### Summary")
                st.markdown(
                    f"<div class='result-card'>{result.get('summary','—')}</div>",
                    unsafe_allow_html=True,
                )

                chunks_used = result.get("chunks_used")
                if chunks_used:
                    st.markdown(
                        f"<p style='color:#8B6B4A;font-size:0.82rem;'>"
                        f"Generated from {chunks_used} chunks.</p>",
                        unsafe_allow_html=True,
                    )

            except requests.exceptions.ConnectionError:
                st.markdown(
                    "<div class='banner-error'>❌ Cannot connect to the backend API. "
                    "Make sure FastAPI is running at <code>http://127.0.0.1:8000</code>.</div>",
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.markdown(
                    f"<div class='banner-error'>❌ Error: {e}</div>",
                    unsafe_allow_html=True,
                )



with tab3:
    st.markdown("### Compare Two Papers")

    if len(all_db_papers) < 2:
        st.markdown(
            "<div class='banner-info'>ℹ️ Upload and process a second paper to enable comparison.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<p style='color:#6B5040;font-size:0.9rem;'>Select two papers and ask a "
            "comparison question — the AI will analyse both and produce a structured comparison.</p>",
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)

        with col_a:
            paper_a = st.selectbox(
                "Paper A",
                options=all_db_papers,
                format_func=lambda x: x.title(),
                index=0,
                key="compare_paper_a",
            )

        with col_b:
            # Default to second paper
            default_b_idx = 1 if len(all_db_papers) > 1 else 0
            paper_b = st.selectbox(
                "Paper B",
                options=all_db_papers,
                format_func=lambda x: x.title(),
                index=default_b_idx,
                key="compare_paper_b",
            )

        comparison_question = st.text_area(
            "Comparison question",
            value=f"Compare the architecture and methodology of {paper_a.title()} and {paper_b.title()}",
            height=90,
            key="compare_question",
        )

        if st.button("Compare ✦", key="compare_btn"):
            if paper_a == paper_b:
                st.markdown(
                    "<div class='banner-error'>Please select two different papers.</div>",
                    unsafe_allow_html=True,
                )
            else:
                with st.spinner("Comparing papers — this may take a couple of minutes…"):
                    try:
                        response = requests.post(
                            f"{API_URL}/compare",
                            json={
                                "question": comparison_question,
                                "paper_a": paper_a,
                                "paper_b": paper_b,
                            },
                            timeout=600,
                        )
                        response.raise_for_status()
                        result = response.json()

                        st.markdown(
                            "<div class='banner-success'>✅ Comparison complete</div>",
                            unsafe_allow_html=True,
                        )

                        badge_a = f"<span class='paper-badge'>📄 {paper_a.title()}</span>"
                        badge_b = f"<span class='paper-badge'>📄 {paper_b.title()}</span>"
                        st.markdown(
                            f"{badge_a} vs {badge_b}", unsafe_allow_html=True
                        )

                        st.markdown("#### Comparison")
                        st.markdown(
                            f"<div class='result-card'>{result.get('comparision','—')}</div>",
                            unsafe_allow_html=True,
                        )

                    except requests.exceptions.ConnectionError:
                        st.markdown(
                            "<div class='banner-error'>❌ Cannot connect to the backend API. "
                            "Make sure FastAPI is running at <code>http://127.0.0.1:8000</code>.</div>",
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.markdown(
                            f"<div class='banner-error'>❌ Error: {e}</div>",
                            unsafe_allow_html=True,
                        )


st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#A08060;font-size:0.8rem;'>"
    "ResearchGPT · Powered by Gemini + ChromaDB + BGE Embeddings</p>",
    unsafe_allow_html=True,
)
