import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: #0a0a0f;
    color: #e2e2e8;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #3a3a5c; border-radius: 2px; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2.5rem;
}
.hero-badge {
    display: inline-block;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #6e6ef0;
    border: 1px solid #2d2d6e;
    border-radius: 2px;
    padding: 0.25rem 0.75rem;
    margin-bottom: 1.25rem;
    background: rgba(110,110,240,0.07);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    color: #f0f0ff;
    letter-spacing: -0.03em;
    line-height: 1.05;
    margin: 0 0 0.6rem;
}
.hero-title span { color: #6e6ef0; }
.hero-sub {
    font-size: 0.78rem;
    color: #5a5a7a;
    letter-spacing: 0.08em;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #10101a !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 4px !important;
    color: #e2e2e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #6e6ef0 !important;
    box-shadow: 0 0 0 2px rgba(110,110,240,0.15) !important;
}
.stTextInput label {
    color: #6a6a8a !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
.stButton > button {
    background: #6e6ef0 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #5555d0 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(110,110,240,0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline step cards ── */
.step-card {
    background: #0e0e1a;
    border: 1px solid #1e1e30;
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: #2a2a4a;
    transition: background 0.3s;
}
.step-card.active::before { background: #6e6ef0; }
.step-card.done::before { background: #34d399; }
.step-card.error::before { background: #f87171; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}
.step-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #3a3a5c;
    text-transform: uppercase;
}
.step-num.active { color: #6e6ef0; }
.step-num.done { color: #34d399; }

.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #9090b0;
}
.step-title.active { color: #f0f0ff; }
.step-title.done { color: #f0f0ff; }

.step-icon { font-size: 1rem; }

/* ── Output sections ── */
.output-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a4a6a;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}

.output-box {
    background: #08080f;
    border: 1px solid #1a1a2e;
    border-radius: 4px;
    padding: 1rem;
    font-size: 0.8rem;
    line-height: 1.7;
    color: #b0b0cc;
    max-height: 260px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Report output ── */
.report-box {
    background: #08080f;
    border: 1px solid #2a2a4a;
    border-radius: 6px;
    padding: 1.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.8;
    color: #c8c8e8;
    max-height: 450px;
    overflow-y: auto;
    white-space: pre-wrap;
}

/* ── Feedback box ── */
.feedback-box {
    background: #0a0f0a;
    border: 1px solid #1a2e1a;
    border-radius: 6px;
    padding: 1.5rem;
    font-size: 0.82rem;
    line-height: 1.8;
    color: #a8d8a8;
    max-height: 350px;
    overflow-y: auto;
    white-space: pre-wrap;
}

/* ── Status indicator ── */
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-right: 0.4rem;
    vertical-align: middle;
}
.status-dot.idle     { background: #3a3a5c; }
.status-dot.running  { background: #6e6ef0; animation: pulse 1.2s infinite; }
.status-dot.done     { background: #34d399; }
.status-dot.error    { background: #f87171; }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #1a1a2a;
    margin: 2rem 0;
}

/* ── Metric chips ── */
.metrics-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.metric-chip {
    background: #0e0e1a;
    border: 1px solid #1e1e30;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    font-size: 0.7rem;
    color: #5a5a8a;
    letter-spacing: 0.05em;
}
.metric-chip b { color: #9090d0; font-family: 'Syne', sans-serif; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #2a2a4a;
}
.empty-state h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    color: #3a3a5a;
    margin-bottom: 0.5rem;
}
.empty-state p { font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⬡ Multi-Agent Research System</div>
    <div class="hero-title">Research <span>Intelligence</span><br>Pipeline</div>
    <div class="hero-sub">Search · Scrape · Write · Critique — autonomously</div>
</div>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "running" not in st.session_state:
    st.session_state.running = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0.0


# ── Input + Run ───────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([4, 1], gap="medium")
with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="visible",
        disabled=st.session_state.running,
    )
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run_clicked = st.button(
        "⟶ Run Pipeline",
        disabled=st.session_state.running or not topic.strip(),
    )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ── Pipeline execution ────────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search Agent",   "Finding recent, reliable information across the web"),
    ("📄", "Reader Agent",   "Scraping the most relevant source for deep content"),
    ("✍️",  "Writer Chain",   "Synthesising research into a structured report"),
    ("🎯", "Critic Chain",   "Reviewing and scoring the generated report"),
]

def step_class(idx):
    if st.session_state.running and st.session_state.step == idx:
        return "active"
    if st.session_state.result and idx < 4:
        return "done"
    return ""

def label_class(idx):
    return step_class(idx) or ""


if run_clicked and topic.strip():
    st.session_state.running = True
    st.session_state.result = None
    st.session_state.step = 0
    st.rerun()


if st.session_state.running:
    # Show live pipeline progress
    step_placeholders = []
    for i, (icon, title, desc) in enumerate(STEPS):
        ph = st.empty()
        step_placeholders.append(ph)
        ph.markdown(f"""
        <div class="step-card">
            <div class="step-header">
                <span class="step-num">Step {i+1:02d}</span>
                <span class="step-icon">{icon}</span>
                <span class="step-title">{title}</span>
            </div>
            <div style="font-size:0.72rem;color:#3a3a5c;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    status_ph = st.empty()
    t0 = time.time()

    try:
        import io, sys, threading, queue

        result_queue = queue.Queue()
        error_queue = queue.Queue()

        def run_pipeline():
            try:
                res = run_research_pipeline(topic)
                result_queue.put(res)
            except Exception as e:
                error_queue.put(e)

        thread = threading.Thread(target=run_pipeline, daemon=True)

        # Animate step cards while running
        step_durations = [0, 0, 0, 0]   # will be filled heuristically
        step_labels = ["Searching ...", "Scraping ...", "Writing ...", "Critiquing ..."]

        thread.start()

        active_step = 0
        last_progress = time.time()

        while thread.is_alive():
            elapsed = time.time() - t0
            # Heuristic step progression based on elapsed time
            if elapsed < 10:
                active_step = 0
            elif elapsed < 25:
                active_step = 1
            elif elapsed < 50:
                active_step = 2
            else:
                active_step = 3

            for i, (icon, title, desc) in enumerate(STEPS):
                if i < active_step:
                    cls = "done"
                    num_cls = "done"
                    title_cls = "done"
                    indicator = "✓"
                elif i == active_step:
                    cls = "active"
                    num_cls = "active"
                    title_cls = "active"
                    indicator = f'<span class="status-dot running"></span>'
                else:
                    cls = ""
                    num_cls = ""
                    title_cls = ""
                    indicator = ""

                step_placeholders[i].markdown(f"""
                <div class="step-card {cls}">
                    <div class="step-header">
                        <span class="step-num {num_cls}">Step {i+1:02d}</span>
                        <span class="step-icon">{icon}</span>
                        <span class="step-title {title_cls}">{title}</span>
                        <span style="margin-left:auto;font-size:0.7rem;color:#34d399">{indicator if i < active_step else (indicator if i == active_step else '')}</span>
                    </div>
                    <div style="font-size:0.72rem;color:{'#5a5a8a' if i == active_step else '#2a2a4a'};">{step_labels[i] if i == active_step else desc}</div>
                </div>
                """, unsafe_allow_html=True)

            status_ph.markdown(f"""
            <div style="text-align:center;margin-top:1rem;font-size:0.72rem;color:#4a4a6a;">
                <span class="status-dot running"></span>
                Pipeline running &nbsp;·&nbsp; {elapsed:.0f}s elapsed
            </div>
            """, unsafe_allow_html=True)

            time.sleep(1.5)
            thread.join(timeout=0)

        # Thread finished
        if not error_queue.empty():
            raise error_queue.get()

        result = result_queue.get()
        elapsed = time.time() - t0

        # Mark all done
        for i, (icon, title, desc) in enumerate(STEPS):
            step_placeholders[i].markdown(f"""
            <div class="step-card done">
                <div class="step-header">
                    <span class="step-num done">Step {i+1:02d}</span>
                    <span class="step-icon">{icon}</span>
                    <span class="step-title done">{title}</span>
                    <span style="margin-left:auto;font-size:0.7rem;color:#34d399">✓</span>
                </div>
                <div style="font-size:0.72rem;color:#2a4a2a;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        status_ph.markdown(f"""
        <div style="text-align:center;margin-top:1rem;font-size:0.72rem;color:#34d399;">
            <span class="status-dot done"></span>
            Pipeline complete &nbsp;·&nbsp; {elapsed:.1f}s
        </div>
        """, unsafe_allow_html=True)

        st.session_state.result = result
        st.session_state.elapsed = elapsed
        st.session_state.running = False

    except Exception as e:
        status_ph.markdown(f"""
        <div style="text-align:center;margin-top:1rem;font-size:0.72rem;color:#f87171;">
            <span class="status-dot error"></span> Error: {e}
        </div>
        """, unsafe_allow_html=True)
        st.session_state.running = False

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Static step cards (all done)
    for i, (icon, title, desc) in enumerate(STEPS):
        st.markdown(f"""
        <div class="step-card done">
            <div class="step-header">
                <span class="step-num done">Step {i+1:02d}</span>
                <span class="step-icon">{icon}</span>
                <span class="step-title done">{title}</span>
                <span style="margin-left:auto;font-size:0.7rem;color:#34d399">✓</span>
            </div>
            <div style="font-size:0.72rem;color:#2a4a2a;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;margin:1rem 0 2rem;font-size:0.72rem;color:#34d399;">
        <span class="status-dot done"></span>
        Pipeline complete &nbsp;·&nbsp; {st.session_state.elapsed:.1f}s
    </div>
    <hr class='divider'>
    """, unsafe_allow_html=True)

    # Metrics row
    search_len = len(r.get("search_results", ""))
    scraped_len = len(r.get("scraped_content", ""))
    report_len = len(r.get("report", ""))
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-chip"><b>{search_len:,}</b> chars — search results</div>
        <div class="metric-chip"><b>{scraped_len:,}</b> chars — scraped content</div>
        <div class="metric-chip"><b>{report_len:,}</b> chars — final report</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

    # Tabs for each output
    tab1, tab2, tab3, tab4 = st.tabs(["📑 Report", "🎯 Critic Feedback", "🔍 Search Results", "📄 Scraped Content"])

    with tab1:
        st.markdown('<div class="output-label">Generated Report</div>', unsafe_allow_html=True)
        report_text = r.get("report", "No report generated.")
        if hasattr(report_text, 'content'):
            report_text = report_text.content
        st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇ Download Report",
            data=str(report_text),
            file_name=f"report_{topic[:30].replace(' ','_')}.txt",
            mime="text/plain",
        )

    with tab2:
        st.markdown('<div class="output-label">Critic Review</div>', unsafe_allow_html=True)
        feedback = r.get("feedback", "No feedback available.")
        if hasattr(feedback, 'content'):
            feedback = feedback.content
        st.markdown(f'<div class="feedback-box">{feedback}</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="output-label">Raw Search Results</div>', unsafe_allow_html=True)
        search = r.get("search_results", "")
        st.markdown(f'<div class="output-box">{search}</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="output-label">Scraped Web Content</div>', unsafe_allow_html=True)
        scraped = r.get("scraped_content", "")
        st.markdown(f'<div class="output-box">{scraped}</div>', unsafe_allow_html=True)

elif not st.session_state.running:
    # Static idle pipeline cards
    for i, (icon, title, desc) in enumerate(STEPS):
        st.markdown(f"""
        <div class="step-card">
            <div class="step-header">
                <span class="step-num">Step {i+1:02d}</span>
                <span class="step-icon">{icon}</span>
                <span class="step-title">{title}</span>
            </div>
            <div style="font-size:0.72rem;color:#2a2a4a;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="empty-state">
        <h3>Enter a topic above to begin</h3>
        <p>The pipeline will search, scrape, write, and critique — fully autonomously.</p>
    </div>
    """, unsafe_allow_html=True)