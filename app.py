import streamlit as st
import sys
import os
import time
import threading
from io import StringIO

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --border:    #1e2230;
    --accent:    #00e5ff;
    --accent2:   #7b61ff;
    --warn:      #ff6b35;
    --success:   #00e5a0;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: var(--font-mono);
    background-color: var(--bg);
    color: var(--text);
}

/* Remove streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.5rem;
}
.hero-label {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.hero-title {
    font-family: var(--font-head);
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    color: var(--text);
    margin: 0;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    margin-top: 0.6rem;
    font-size: 0.8rem;
    color: var(--muted);
    letter-spacing: 0.05em;
}

/* ── Search bar area ── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.08) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.65rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline steps ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 2rem;
}
.step-card {
    background: var(--surface);
    padding: 1.1rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}
.step-num {
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.step-icon { font-size: 1.3rem; }
.step-label {
    font-family: var(--font-head);
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text);
}
.step-desc { font-size: 0.68rem; color: var(--muted); line-height: 1.4; }

/* active / done states */
.step-active { border-top: 2px solid var(--accent) !important; }
.step-active .step-label { color: var(--accent); }
.step-done { border-top: 2px solid var(--success) !important; }
.step-done .step-label { color: var(--success); }
.step-idle { border-top: 2px solid transparent; }

/* ── Result panels ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.panel-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.8rem 1.1rem;
    border-bottom: 1px solid var(--border);
    background: rgba(255,255,255,0.02);
}
.panel-tag {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 0.15rem 0.5rem;
    border-radius: 3px;
}
.tag-search  { background: rgba(123,97,255,0.15); color: var(--accent2); border: 1px solid rgba(123,97,255,0.3); }
.tag-scrape  { background: rgba(0,229,255,0.1);   color: var(--accent);  border: 1px solid rgba(0,229,255,0.25); }
.tag-report  { background: rgba(0,229,160,0.1);   color: var(--success); border: 1px solid rgba(0,229,160,0.25); }
.tag-critic  { background: rgba(255,107,53,0.12); color: var(--warn);    border: 1px solid rgba(255,107,53,0.3); }

.panel-title {
    font-family: var(--font-head);
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text);
}
.panel-body {
    padding: 1.1rem 1.2rem;
    font-size: 0.78rem;
    line-height: 1.75;
    color: #c5c9d6;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
}
/* scrollbar */
.panel-body::-webkit-scrollbar { width: 4px; }
.panel-body::-webkit-scrollbar-track { background: transparent; }
.panel-body::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Status bar ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 1rem;
    border-radius: 6px;
    font-size: 0.75rem;
    margin-bottom: 1.5rem;
    font-weight: 500;
}
.status-running { background: rgba(0,229,255,0.08); border: 1px solid rgba(0,229,255,0.2); color: var(--accent); }
.status-done    { background: rgba(0,229,160,0.08); border: 1px solid rgba(0,229,160,0.2); color: var(--success); }
.status-error   { background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.25); color: var(--warn); }
.pulse { display:inline-block; width:6px; height:6px; border-radius:50%; background:currentColor; animation: pulse 1s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Spinner override ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: var(--font-head) !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render pipeline step cards ────────────────────────────────────────
def render_pipeline(active_step: int, done_steps: set):
    steps = [
        ("01", "🔍", "Search", "Web search & source discovery"),
        ("02", "📄", "Read",   "Scrape & extract page content"),
        ("03", "✍️",  "Write",  "Synthesise research into report"),
        ("04", "🧐", "Critic", "Review & quality feedback"),
    ]
    cards_html = '<div class="pipeline-grid">'
    for i, (num, icon, label, desc) in enumerate(steps, 1):
        if i == active_step:
            cls = "step-card step-active"
        elif i in done_steps:
            cls = "step-card step-done"
        else:
            cls = "step-card step-idle"
        cards_html += f"""
        <div class="{cls}">
            <span class="step-num">step {num}</span>
            <span class="step-icon">{icon}</span>
            <span class="step-label">{label}</span>
            <span class="step-desc">{desc}</span>
        </div>"""
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)


def result_panel(tag_cls, tag_label, icon, title, content):
    st.markdown(f"""
    <div class="result-panel">
        <div class="panel-header">
            <span class="panel-tag {tag_cls}">{tag_label}</span>
            <span class="panel-title">{icon} {title}</span>
        </div>
        <div class="panel-body">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-label">Multi-Agent System</span>
    <h1 class="hero-title">Research<span>Mind</span></h1>
    <p class="hero-sub">Search → Scrape → Write → Critique &nbsp;|&nbsp; Powered by LangChain agents</p>
</div>
""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="Enter a research topic  e.g. 'Quantum computing in 2025'",
        key="topic_input",
    )
with col_btn:
    run_btn = st.button("▶  Run", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
for k, v in {
    "running": False,
    "state": {},
    "active_step": 0,
    "done_steps": set(),
    "error": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Run pipeline ───────────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.running    = True
    st.session_state.state      = {}
    st.session_state.active_step = 1
    st.session_state.done_steps  = set()
    st.session_state.error       = None

    # ── Step placeholders ──────────────────────────────────────────────────────
    pipeline_ph = st.empty()
    status_ph   = st.empty()

    def show_status(msg, kind="running"):
        dot = '<span class="pulse"></span>' if kind == "running" else ("✓" if kind == "done" else "✗")
        status_ph.markdown(f'<div class="status-bar status-{kind}">{dot} {msg}</div>', unsafe_allow_html=True)

    try:
        # dynamically import so the venv path works
        sys.path.insert(0, os.path.dirname(__file__))
        from pipeline import run_research_pipeline  # type: ignore

        # ── Step 1 ─────────────────────────────────────────────────────────────
        st.session_state.active_step = 1
        pipeline_ph.empty()
        with pipeline_ph.container():
            render_pipeline(1, st.session_state.done_steps)
        show_status("Step 1 / 4 — Searching the web…")

        # We run the whole pipeline and unpack; for live step feedback we wrap
        # each stage call directly from pipeline logic reproduced here.
        from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain  # type: ignore

        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about : {topic}")]
        })
        st.session_state.state["search_result"] = search_result["messages"][-1].content
        st.session_state.done_steps.add(1)

        # ── Step 2 ─────────────────────────────────────────────────────────────
        st.session_state.active_step = 2
        pipeline_ph.empty()
        with pipeline_ph.container():
            render_pipeline(2, st.session_state.done_steps)
        show_status("Step 2 / 4 — Scraping top sources…")

        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"Pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{st.session_state.state['search_result'][:800]}")]
        })
        st.session_state.state["scraped_content"] = reader_result["messages"][-1].content
        st.session_state.done_steps.add(2)

        # ── Step 3 ─────────────────────────────────────────────────────────────
        st.session_state.active_step = 3
        pipeline_ph.empty()
        with pipeline_ph.container():
            render_pipeline(3, st.session_state.done_steps)
        show_status("Step 3 / 4 — Writing the report…")

        research_combined = (
            f"SEARCH RESULTS:\n{st.session_state.state['search_result']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{st.session_state.state['scraped_content']}"
        )
        st.session_state.state["report"] = writer_chain.invoke({
            "topic":    topic,
            "research": research_combined,
        })
        st.session_state.done_steps.add(3)

        # ── Step 4 ─────────────────────────────────────────────────────────────
        st.session_state.active_step = 4
        pipeline_ph.empty()
        with pipeline_ph.container():
            render_pipeline(4, st.session_state.done_steps)
        show_status("Step 4 / 4 — Critic reviewing…")

        st.session_state.state["feedback"] = critic_chain.invoke({
            "report": st.session_state.state["report"]
        })
        st.session_state.done_steps.add(4)

        # ── Done ───────────────────────────────────────────────────────────────
        st.session_state.active_step = 0
        pipeline_ph.empty()
        with pipeline_ph.container():
            render_pipeline(0, st.session_state.done_steps)
        show_status("Research complete!", "done")

    except Exception as e:
        st.session_state.error = str(e)
        show_status(f"Error: {e}", "error")

    finally:
        st.session_state.running = False

elif run_btn and not topic.strip():
    st.warning("Please enter a topic before running.")


# ── Idle pipeline display ──────────────────────────────────────────────────────
if not st.session_state.running and not st.session_state.state:
    render_pipeline(0, set())


# ── Results ────────────────────────────────────────────────────────────────────
state = st.session_state.state

if state:
    if state.get("search_result"):
        result_panel(
            "tag-search", "SEARCH", "🔍",
            "Web Search Results",
            state["search_result"],
        )

    if state.get("scraped_content"):
        result_panel(
            "tag-scrape", "SCRAPE", "📄",
            "Scraped Source Content",
            state["scraped_content"],
        )

    if state.get("report"):
        # Report gets full-width prominent display
        st.markdown(f"""
        <div class="result-panel" style="border-color: rgba(0,229,160,0.3);">
            <div class="panel-header" style="background: rgba(0,229,160,0.05);">
                <span class="panel-tag tag-report">REPORT</span>
                <span class="panel-title">✍️ Final Research Report</span>
            </div>
            <div class="panel-body" style="max-height: 520px; font-size:0.82rem; line-height:1.85;">
{state["report"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇  Download Report (.txt)",
            data=state["report"],
            file_name=f"report_{topic[:40].replace(' ','_')}.txt",
            mime="text/plain",
        )

    if state.get("feedback"):
        result_panel(
            "tag-critic", "CRITIC", "🧐",
            "Critic Feedback",
            state["feedback"],
        )

# ── Error display ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f"""
    <div class="result-panel" style="border-color: rgba(255,107,53,0.35);">
        <div class="panel-header"><span class="panel-tag tag-critic">ERROR</span>
        <span class="panel-title">Pipeline failed</span></div>
        <div class="panel-body">{st.session_state.error}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem; padding-top:1rem; border-top:1px solid #1e2230;
     display:flex; justify-content:space-between; font-size:0.65rem; color:#3d4455;">
    <span>ResearchMind · Multi-Agent Pipeline</span>
    <span>Search → Scrape → Write → Critique</span>
</div>
""", unsafe_allow_html=True)