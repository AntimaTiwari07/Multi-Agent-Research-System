import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #07070b;
    background-image:
        radial-gradient(ellipse 80% 50% at 15% -10%, rgba(255,140,50,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 60% 45% at 85% 0%, rgba(120,90,255,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 50% 115%, rgba(255,80,30,0.10) 0%, transparent 55%),
        repeating-linear-gradient(0deg, rgba(255,255,255,0.012) 0px, rgba(255,255,255,0.012) 1px, transparent 1px, transparent 3px);
    background-attachment: fixed;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1240px; }

/* ── Animations ── */
@keyframes floatGlow {
    0%, 100% { transform: translateY(0px); opacity: 0.9; }
    50% { transform: translateY(-6px); opacity: 1; }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulseDot {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(255,140,50,0.5); }
    50% { opacity: 0.6; box-shadow: 0 0 0 6px rgba(255,140,50,0); }
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.2rem 0 2.2rem;
    position: relative;
    animation: fadeUp 0.6s ease-out;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1.1rem;
    padding: 0.35rem 0.9rem;
    border: 1px solid rgba(255,140,50,0.3);
    border-radius: 30px;
    background: rgba(255,140,50,0.06);
}
.hero-eyebrow::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #ff8c32;
    animation: pulseDot 1.8s infinite;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5.2rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    background: linear-gradient(180deg, #f7f3ea 0%, #cbc4b8 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(120deg, #ff8c32 0%, #ff5a1a 50%, #ffb066 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.08rem;
    font-weight: 300;
    color: #a8a09430;
    color: #aba395;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.35), rgba(120,90,255,0.2), transparent);
    margin: 2rem 0;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 12px !important;
    color: #f5f1e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.02rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 4px rgba(255,140,50,0.14) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #6b645c !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.78rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 6px 24px rgba(255,140,50,0.35) !important;
    width: 100%;
    margin-top: 0.4rem;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(255,140,50,0.45) !important;
    opacity: 0.95 !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Example chips ── */
.chip-row {
    display:flex;
    gap:0.6rem;
    flex-wrap:wrap;
    align-items:center;
    margin: 0.4rem 0 1.6rem;
}
.chip-label {
    font-family:'DM Mono',monospace;
    font-size:0.68rem;
    color:#6b645c;
    letter-spacing:0.15em;
    margin-right: 0.2rem;
}
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 8px;
    padding: 0.35rem 0.85rem;
    font-size: 0.78rem;
    color: #b5ad9f;
    font-family: 'DM Sans', sans-serif;
    cursor: default;
    transition: border-color 0.2s, background 0.2s, color 0.2s;
}
.chip:hover {
    border-color: rgba(255,140,50,0.35);
    background: rgba(255,140,50,0.06);
    color: #ffb066;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.35s, background 0.35s, transform 0.2s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.45);
    background: linear-gradient(160deg, rgba(255,140,50,0.08), rgba(255,140,50,0.02));
    transform: translateX(2px);
}
.step-card.done {
    border-color: rgba(80,200,120,0.32);
    background: rgba(80,200,120,0.04);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 16px 0 0 16px;
    background: rgba(255,255,255,0.06);
    transition: background 0.3s;
}
.step-card.active::before {
    background: linear-gradient(180deg, #ff8c32, #ff5a1a);
    box-shadow: 0 0 12px rgba(255,140,50,0.6);
}
.step-card.done::before   { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.75;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.98rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.55rem;
    border-radius: 20px;
}
.status-waiting  { color: #777; background: rgba(255,255,255,0.03); }
.status-running  { color: #ff8c32; background: rgba(255,140,50,0.1); }
.status-done     { color: #50c878; background: rgba(80,200,120,0.1); }

.step-desc {
    font-size: 0.82rem;
    color: #837c72;
    margin-top: 0.35rem;
    line-height: 1.5;
}

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #cdc8bf;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: linear-gradient(160deg, rgba(255,140,50,0.05), rgba(255,255,255,0.015));
    border: 1px solid rgba(255,140,50,0.22);
    border-radius: 18px;
    padding: 2.2rem 2.6rem;
    margin-top: 1rem;
    box-shadow: 0 10px 36px rgba(0,0,0,0.3);
    animation: fadeUp 0.5s ease-out;
}
.feedback-panel {
    background: linear-gradient(160deg, rgba(80,200,120,0.05), rgba(255,255,255,0.015));
    border: 1px solid rgba(80,200,120,0.22);
    border-radius: 18px;
    padding: 2.2rem 2.6rem;
    margin-top: 1rem;
    box-shadow: 0 10px 36px rgba(0,0,0,0.3);
    animation: fadeUp 0.6s ease-out;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.3rem;
    padding-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-label.orange {
    color: #ff8c32;
    border-bottom: 1px solid rgba(255,140,50,0.18);
}
.panel-label.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80,200,120,0.18);
}

/* Make markdown text inside panels match the theme */
.report-panel p, .report-panel li, .feedback-panel p, .feedback-panel li {
    color: #d8d3c8 !important;
    line-height: 1.75;
}
.report-panel h1, .report-panel h2, .report-panel h3,
.feedback-panel h1, .feedback-panel h2, .feedback-panel h3 {
    font-family: 'Syne', sans-serif !important;
    color: #f0ebe0 !important;
}

/* ── Progress text ── */
.stSpinner > div { color: #ff8c32 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.015) !important;
    margin-bottom: 0.8rem;
}
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #b5ad9f !important;
    letter-spacing: 0.08em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f0ebe0;
    margin: 1.6rem 0 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::before {
    content: '';
    width: 4px;
    height: 1.1rem;
    border-radius: 2px;
    background: linear-gradient(180deg, #ff8c32, #ff5a1a);
    display: inline-block;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.04) !important;
    color: #ffb066 !important;
    border: 1px solid rgba(255,140,50,0.35) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,140,50,0.12) !important;
    border-color: #ff8c32 !important;
}

/* ── Toast-style notice ── */
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #4d473f;
    text-align: center;
    margin-top: 3.5rem;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    # Example chips
    chips_html = '<div class="chip-row"><span class="chip-label">TRY →</span>'
    for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]:
        chips_html += f'<span class="chip">{ex}</span>'
    chips_html += "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)