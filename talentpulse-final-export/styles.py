PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

/* Base Theme: Obsidian Dark */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important;
}

/* Radical Background for the whole page */
.stApp {
    background: 
        radial-gradient(ellipse at top left, #1e103c 0%, transparent 40%),
        radial-gradient(ellipse at bottom right, #003344 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, #050508 0%, #020202 100%) !important;
    background-attachment: fixed !important;
}

/* Hide Default Streamlit Elements completely */
#MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; } 

/* 🌟 THE GLASS COMMAND CENTER HACK 🌟 */
[data-testid="block-container"] { 
    background: rgba(12, 12, 16, 0.45) !important;
    backdrop-filter: blur(40px) saturate(120%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(120%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 28px !important;
    box-shadow: 0 40px 80px -20px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    padding: 3rem 4rem 4rem 4rem !important;
    margin: 4vh auto !important;
    max-width: 1400px !important;
    min-height: 85vh !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.02em;
    color: #ffffff;
}

/* Custom Nav / Top Bar inside the Command Center */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 2rem;
}
.nav-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff, #a0aab5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}
.nav-powered {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #64748b;
    font-weight: 600;
}
.nav-powered span { color: #00F0FF; }

/* Dashboard Metrics Cutouts */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}
.dash-metric {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
}
.dash-metric .val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.dash-metric .val.accent { color: #00F0FF; text-shadow: 0 0 20px rgba(0,240,255,0.3); }
.dash-metric .label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #888;
    font-weight: 600;
}

/* Candidate Grid */
.candidate-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.2rem;
    margin-top: 1rem;
}

/* Redesigned Candidate Card (Minimalist Dark inside Glass) */
.cand-widget {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.cand-widget:hover {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(0, 240, 255, 0.3);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.widget-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.w-name { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 700; color: #fff; }
.w-role { font-size: 0.8rem; color: #888; }
.w-rank {
    background: rgba(255,255,255,0.1);
    color: #fff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 20px;
}
.w-rank.top { background: linear-gradient(90deg, #00F0FF, #0080FF); color: #000; }

.w-scores { display: flex; gap: 0.5rem; margin-bottom: 0.8rem; flex-wrap: wrap; }
.w-score-chip {
    font-size: 0.7rem; font-weight: 600;
    padding: 3px 8px; border-radius: 4px;
    background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); color: #aaa;
}
.w-score-chip span { color: #fff; }

.w-skills { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 0.6rem; }
.skill-tag {
    font-size: 0.65rem; background: #000; color: #666; padding: 2px 6px; border-radius: 4px; border: 1px solid #222;
}
.skill-tag.match { background: rgba(0, 240, 255, 0.1); color: #00F0FF; border-color: rgba(0, 240, 255, 0.3); }

/* ── NEW: Risk Flag Badge ── */
.risk-flag {
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-top: 0.4rem;
    font-weight: 600;
}
.risk-flag.warning { background: rgba(255, 165, 0, 0.15); color: #ffa500; border: 1px solid rgba(255,165,0,0.3); }
.risk-flag.danger { background: rgba(255, 60, 60, 0.15); color: #ff5555; border: 1px solid rgba(255,60,60,0.3); }
.risk-flag.info { background: rgba(100, 140, 255, 0.15); color: #6495ed; border: 1px solid rgba(100,140,255,0.3); }

/* ── NEW: Action Badge ── */
.action-badge {
    font-size: 0.7rem;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
    margin-top: 0.3rem;
    font-weight: 600;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.06);
    color: #bbb;
}

/* ── NEW: Strengths & Gaps Pills ── */
.sg-pills { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 0.4rem; }
.sg-pill {
    font-size: 0.6rem;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 500;
}
.sg-pill.strength { background: rgba(0, 200, 100, 0.12); color: #00c864; border: 1px solid rgba(0,200,100,0.25); }
.sg-pill.gap { background: rgba(255, 100, 100, 0.1); color: #ff6b6b; border: 1px solid rgba(255,100,100,0.2); }

/* ── NEW: Conversation Timeline ── */
.convo-timeline {
    margin: 0.8rem 0;
    padding: 0;
    list-style: none;
}
.convo-bubble {
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    line-height: 1.4;
    max-width: 85%;
    position: relative;
}
.convo-bubble.recruiter {
    background: rgba(0, 240, 255, 0.08);
    border: 1px solid rgba(0, 240, 255, 0.2);
    color: #b0e0e8;
    margin-right: auto;
    border-bottom-left-radius: 2px;
}
.convo-bubble.candidate {
    background: rgba(138, 43, 226, 0.1);
    border: 1px solid rgba(138, 43, 226, 0.25);
    color: #d0b0e8;
    margin-left: auto;
    border-bottom-right-radius: 2px;
}
.convo-label {
    font-size: 0.55rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 700;
    margin-bottom: 0.2rem;
    display: block;
}
.convo-bubble.recruiter .convo-label { color: #00F0FF; }
.convo-bubble.candidate .convo-label { color: #8A2BE2; }

/* ── NEW: JSON Code Block ── */
.json-block {
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1rem;
    font-family: 'Courier New', monospace;
    font-size: 0.75rem;
    color: #a8d8a8;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 400px;
    overflow-y: auto;
}

/* ── NEW: Insights Card ── */
.insight-card {
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.insight-card h4 {
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
    color: #fff;
}
.insight-card p, .insight-card li {
    font-size: 0.78rem;
    color: #aaa;
    line-height: 1.6;
}
.insight-card ul { padding-left: 1rem; }
.insight-card .highlight { color: #00F0FF; font-weight: 600; }

/* Inputs & Buttons Customization */
.stButton > button {
    background: linear-gradient(90deg, #222, #333) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { 
    border-color: #00F0FF !important; 
    box-shadow: 0 0 20px rgba(0,240,255,0.2) !important; 
}
/* Primary Button Override */
.stButton > button[data-testid="baseButton-primary"] {
    background: #ffffff !important;
    color: #000000 !important;
}
.stButton > button[data-testid="baseButton-primary"]:hover {
    background: #e0e0e0 !important;
    box-shadow: 0 0 20px rgba(255,255,255,0.4) !important;
}

.stTextArea textarea {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #fff !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 1rem !important;
}
.stTextArea textarea:focus { border-color: #00F0FF !important; box-shadow: 0 0 0 1px #00F0FF !important; }

/* Control Expanders */
.streamlit-expanderHeader {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    color: #aaa !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.streamlit-expanderContent {
    background: transparent !important;
    border: none !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: rgba(0,0,0,0.2);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #888 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 240, 255, 0.1) !important;
    color: #00F0FF !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.4); }

hr { border-color: rgba(255,255,255,0.05) !important; margin: 2rem 0 !important; }
</style>
"""
