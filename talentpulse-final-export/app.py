import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
import io

from engine import JobParser, Matcher, OutreachSimulator
from styles import PREMIUM_CSS

# ─────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentPulse — Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Initialise modules
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_modules():
    return JobParser(), Matcher(), OutreachSimulator()

parser, matcher, simulator = load_modules()

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            
    csv_path = os.path.join(os.path.dirname(__file__), "mock_candidates.csv")
    if not os.path.exists(csv_path):
        from data import generate_mock_data
        generate_mock_data()
    return pd.read_csv(csv_path)


# ─────────────────────────────────────────────────────────────
# Top Navigation Bar
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
    <div class="nav-brand">⚡ TalentPulse</div>
    <div class="nav-powered">Powered by <span>Deccan AI</span></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Dashboard Controls (Expander)
# ─────────────────────────────────────────────────────────────
with st.expander("⚙️ Dashboard Controls & Filters", expanded=False):
    st.markdown("**📂 Upload Custom Candidate Data**")
    uploaded_file = st.file_uploader("Upload Candidates CSV", type=["csv"], help="Upload a custom CSV. Otherwise, we'll use the default mock database.", label_visibility="collapsed")
    candidates_df = load_data(uploaded_file)
    
    # Safely handle missing columns to prevent KeyErrors
    req_cols = ["Name", "Role", "Skills", "Experience"]
    missing = [c for c in req_cols if c not in candidates_df.columns]
    if missing:
        st.error(f"⚠️ **Error:** Uploaded CSV is missing required columns: {', '.join(missing)}. Please update your CSV file.")
        st.stop()
        
    optional_cols = {
        "Location": "Not specified", 
        "Risk Flag": "", 
        "Recommended Action": "", 
        "Current Company": "Not specified", 
        "Availability": "Unknown", 
        "Notice Period": "Unknown", 
        "Response": "", 
        "Response2": ""
    }
    for col, default_val in optional_cols.items():
        if col not in candidates_df.columns:
            candidates_df[col] = default_val
            
    candidates_df["Experience"] = pd.to_numeric(candidates_df["Experience"], errors="coerce").fillna(0)
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Scoring Weights**")
        match_weight = st.slider("Match Score Weight", 0.0, 1.0, 0.6, 0.05)
        interest_weight = st.slider("Interest Score Weight", 0.0, 1.0, 0.4, 0.05)
        if abs(match_weight + interest_weight - 1.0) > 0.01:
            st.caption(f"⚠ Weights sum to {match_weight + interest_weight:.2f}")
    with c2:
        st.markdown("**Pool Filters**")
        top_n = st.slider("Show Top N Candidates", 5, 30, 10)
        all_locations = sorted(candidates_df["Location"].dropna().unique().tolist())
        selected_locations = st.multiselect("Filter by Location", all_locations)
    with c3:
        st.markdown("**Experience Filter**")
        min_exp = int(candidates_df["Experience"].min())
        max_exp = int(candidates_df["Experience"].max())
        exp_range = st.slider("Experience Range (years)", min_exp, max_exp, (min_exp, max_exp))

# ─────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────
for key, val in [("jd_parsed", False), ("reqs", {}), ("results_df", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────────────────────
# Main Dashboard Layout
# ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.markdown("### 📄 Job Description Input")
    
    preset_jds = {
        "Custom": "",
        "Senior Software Engineer (Python/AWS)": "We are hiring a Senior Software Engineer with 5+ years of experience.\nMust have: Python, Django or FastAPI, AWS, SQL, Docker.\nExperience with CI/CD pipelines and Agile methodologies required.\nFamiliarity with Kubernetes is a plus.",
        "Data Scientist (ML/NLP)": "Looking for a Data Scientist with 3+ years of experience in machine learning.\nCore skills: Python, scikit-learn, pandas, NLP, deep learning.\nExperience with PyTorch or TensorFlow preferred.\nFamiliarity with SQL and data pipelines is a plus.",
        "Frontend Developer (React)": "We need a Senior Frontend Developer with 4+ years of React experience.\nMust know: React, TypeScript, Next.js, CSS, HTML.\nExperience with GraphQL and Tailwind is a bonus.\nStrong eye for UI/UX design is required.",
        "DevOps / Cloud Engineer": "Seeking a DevOps Engineer with 5+ years of experience.\nMust have: Kubernetes, Docker, AWS or GCP, Terraform, Linux, CI/CD.\nExperience with Prometheus and Grafana for observability is preferred.",
    }
    
    selected_preset = st.selectbox("🗂 Load a sample JD:", list(preset_jds.keys()))
    default_jd = preset_jds[selected_preset]
    
    jd_input = st.text_area(
        "Paste your Job Description:",
        value=default_jd,
        height=200,
        placeholder="Describe the role, required skills, experience level..."
    )
    
    cb1, cb2 = st.columns([1.5, 1])
    with cb1:
        analyze_btn = st.button("🚀 Analyse & Match", type="primary", use_container_width=True)
    with cb2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.jd_parsed = False
            st.session_state.reqs = {}
            st.session_state.results_df = None
            st.rerun()

# ─────────────────────────────────────────────────────────────
# PROCESSING PIPELINE
# ─────────────────────────────────────────────────────────────
if analyze_btn and jd_input.strip():
    st.session_state.jd_parsed = False
    with st.spinner("🔍 Parsing JD..."):
        st.session_state.reqs = parser.parse_jd(jd_input)
        st.session_state.jd_parsed = True
        st.session_state.results_df = None

if st.session_state.jd_parsed and st.session_state.reqs:
    reqs = st.session_state.reqs

    # ── Left Panel: Parsed JD ──────────────────────────────
    with col_left:
        st.markdown("<br>### 🧠 Parsed Requirements", unsafe_allow_html=True)
        st.markdown(f"**Role:** {reqs.get('role_title', 'General')}")
        st.markdown(f"**Seniority:** {reqs['seniority'].title()}")
        st.markdown(f"**Experience:** {reqs['experience_min'] or 'Any'} years+")
        st.markdown(f"**Location:** {reqs.get('location', 'Not specified')}")
        st.markdown(f"**Work Mode:** {reqs.get('work_mode', 'Not specified')}")
        
        # Must-have skills
        if reqs.get("must_have_skills"):
            st.markdown("**Must-Have Skills:**")
            tags = "".join([f'<span class="skill-tag match">{s}</span>' for s in reqs["must_have_skills"]])
            st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
        
        # Good-to-have skills
        if reqs.get("good_to_have_skills"):
            st.markdown("**Good-to-Have:**")
            tags = "".join([f'<span class="skill-tag">{s}</span>' for s in reqs["good_to_have_skills"]])
            st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
        
        # Inferred skills
        if reqs.get("inferred_skills"):
            st.markdown("**Inferred Skills:**")
            tags = "".join([f'<span class="skill-tag" style="border-color:rgba(138,43,226,0.3);color:#b388ff;">{s}</span>' for s in reqs["inferred_skills"]])
            st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
        
        # Hidden signals
        signals = reqs.get("hidden_signals", {})
        if signals.get("urgency"):
            st.markdown("🔥 **Urgency detected** — prioritize fast responders")
        if signals.get("culture_fit"):
            st.markdown(f"🏢 **Culture:** {', '.join(signals['culture_fit'])}")
        
        # Structured JSON view
        with st.expander("📋 View Structured JD (JSON)", expanded=False):
            jd_json = {k: v for k, v in reqs.items() if k != "raw_text"}
            st.markdown(f'<div class="json-block">{json.dumps(jd_json, indent=2)}</div>', unsafe_allow_html=True)

    # ── Filter candidates ──────────────────────────────────
    filtered_df = candidates_df.copy()
    if selected_locations:
        filtered_df = filtered_df[filtered_df["Location"].isin(selected_locations)]
    filtered_df = filtered_df[
        (filtered_df["Experience"] >= exp_range[0]) &
        (filtered_df["Experience"] <= exp_range[1])
    ].reset_index(drop=True)

    # ── Right Panel: Results ───────────────────────────────
    with col_right:
        with st.spinner("⚡ Computing match scores..."):
            scores = matcher.calculate_match_scores(reqs, filtered_df)
            results = filtered_df.copy()
            results["Match Score"] = scores
            results["Matched Skills"] = results["Skills"].apply(lambda x: matcher.extract_matched_skills(reqs, x))
            results["Explanation"] = results.apply(lambda row: matcher.generate_explanation(reqs, row), axis=1)

        with st.spinner("💬 Simulating outreach & scoring interest..."):
            results["Outreach Message"] = results.apply(
                lambda row: simulator.generate_outreach(row["Name"], row["Skills"], reqs["role_type"]), axis=1
            )
            results["Interest Score"] = results.apply(lambda row: simulator.compute_multi_turn_interest(row), axis=1)
            results["Conversation"] = results.apply(
                lambda row: simulator.build_conversation(row, reqs["role_type"], reqs.get("work_mode", "flexible")), axis=1
            )
            results["Conversation Summary"] = results.apply(
                lambda row: simulator.generate_conversation_summary(row["Conversation"], row["Name"]), axis=1
            )

        final_df = simulator.generate_final_ranking(results, match_weight, interest_weight)
        top_df = final_df.head(top_n)
        st.session_state.results_df = final_df

        # ── Dashboard Metrics ──────────────────────────────
        avg_match = round(final_df["Match Score"].mean(), 1)
        avg_interest = round(final_df["Interest Score"].mean(), 1)
        top_score = round(final_df["Final Score"].iloc[0], 1) if not final_df.empty else 0
        hot_leads = len(final_df[(final_df["Match Score"] >= 50) & (final_df["Interest Score"] >= 55)])
        risky = len(final_df[final_df["Risk Flag"].fillna("").str.len() > 0])

        st.markdown(f"""
        <div class="metric-grid">
            <div class="dash-metric"><div class="val">{len(filtered_df)}</div><div class="label">Scanned</div></div>
            <div class="dash-metric"><div class="val accent">{avg_match}</div><div class="label">Avg Match</div></div>
            <div class="dash-metric"><div class="val accent">{avg_interest}</div><div class="label">Avg Interest</div></div>
            <div class="dash-metric"><div class="val">{top_score}</div><div class="label">Top Score</div></div>
            <div class="dash-metric"><div class="val">{hot_leads}</div><div class="label">Hot Leads</div></div>
            <div class="dash-metric"><div class="val">{risky}</div><div class="label">⚠ Flagged</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Quadrant Scatter Plot ──────────────────────────
        fig = go.Figure()
        fig.add_shape(type="rect", x0=50, y0=50, x1=105, y1=105, fillcolor="rgba(0,240,255,0.05)", line_width=0)
        fig.add_shape(type="rect", x0=0, y0=0, x1=50, y1=50, fillcolor="rgba(255,0,0,0.03)", line_width=0)
        fig.add_shape(type="line", line=dict(color="rgba(255,255,255,0.1)", dash="dot"), x0=50, x1=50, y0=0, y1=100)
        fig.add_shape(type="line", line=dict(color="rgba(255,255,255,0.1)", dash="dot"), x0=0, x1=100, y0=50, y1=50)
        fig.add_trace(go.Scatter(
            x=final_df["Match Score"], y=final_df["Interest Score"],
            mode="markers+text",
            text=final_df["Name"].apply(lambda n: n.split()[0]),
            textposition="top center",
            textfont=dict(size=10, color="rgba(255,255,255,0.6)"),
            marker=dict(
                size=final_df["Final Score"] / 3.5 + 8,
                color=final_df["Final Score"],
                colorscale=[[0, "#222"], [0.5, "#8A2BE2"], [1, "#00F0FF"]],
                showscale=True,
                colorbar=dict(title=dict(text="Score", font=dict(color="#888")), tickfont=dict(color="#888")),
                line=dict(color="rgba(0,0,0,0.5)", width=1)
            ),
            hovertemplate="<b>%{customdata[0]}</b><br>Match: %{x:.1f} | Interest: %{y:.1f}<br>Final: %{customdata[2]:.1f}<extra></extra>",
            customdata=list(zip(final_df["Name"], final_df["Role"], final_df["Final Score"]))
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,10,10,0.6)",
            font=dict(family="Inter", color="#888"),
            xaxis=dict(title="Match Score →", range=[0, 102], gridcolor="rgba(255,255,255,0.05)", zeroline=False),
            yaxis=dict(title="Interest Score →", range=[0, 102], gridcolor="rgba(255,255,255,0.05)", zeroline=False),
            margin=dict(l=40, r=40, t=20, b=40), height=360, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Candidate Shortlist Grid ────────────────────────────
    st.markdown("---")
    st.markdown(f"### 🏆 Top {top_n} Ranked Candidates")

    grid_html = '<div class="candidate-grid">'
    for _, row in top_df.iterrows():
        rank = int(row["Rank"])
        rank_class = "top" if rank <= 3 else ""
        all_skills = [s.strip() for s in str(row.get("Skills", "")).split(",")]
        matched_skills = [s.strip() for s in str(row.get("Matched Skills", "")).split(",") if s.strip() and s != "None"]
        risk = str(row.get("Risk Flag", "")) if pd.notna(row.get("Risk Flag")) else ""
        action = str(row.get("Recommended Action", "")) if pd.notna(row.get("Recommended Action")) else ""

        skill_tags = ""
        for sk in all_skills[:6]:
            cls = "skill-tag match" if sk.lower() in [m.lower() for m in matched_skills] else "skill-tag"
            skill_tags += f'<span class="{cls}">{sk}</span>'

        risk_html = ""
        if risk and risk.strip():
            risk_cls = "danger" if "🔴" in risk else ("warning" if "⚠️" in risk or "🟠" in risk else "info")
            risk_html = f'<span class="risk-flag {risk_cls}">{risk}</span>'

        action_html = f'<div class="action-badge">{action}</div>' if action and action.strip() else ""

        grid_html += f'''
<div class="cand-widget">
    <div class="widget-header">
        <div>
            <div class="w-name">{row["Name"]}</div>
            <div class="w-role">{row["Role"]} · {row.get("Experience",0)} yrs</div>
        </div>
        <div class="w-rank {rank_class}">#{rank}</div>
    </div>
    <div class="w-scores">
        <div class="w-score-chip">Match <span>{float(row["Match Score"]):.1f}</span></div>
        <div class="w-score-chip">Interest <span>{float(row["Interest Score"]):.1f}</span></div>
        <div class="w-score-chip" style="border-color:#8A2BE2;">Final <span>{float(row["Final Score"]):.1f}</span></div>
    </div>
    <div class="w-skills">{skill_tags}</div>
    <div class="w-badges">{risk_html}{action_html}</div>
</div>
'''
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # ── Tabbed Detail Section ──────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["🔎 Detailed Analysis", "💬 Conversations", "📊 Recruiter Insights", "📦 Data Export"])

    with tab1:
        for _, row in top_df.iterrows():
            with st.expander(f"#{int(row['Rank'])} — {row['Name']}", expanded=False):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown("**Explanation**")
                    st.write(row.get("Explanation", ""))
                    sg = matcher.get_strengths_and_gaps(reqs, row)
                    if sg["strengths"]:
                        st.markdown("**Strengths:**")
                        pills = "".join([f'<span class="sg-pill strength">✅ {s}</span>' for s in sg["strengths"]])
                        st.markdown(f'<div class="sg-pills">{pills}</div>', unsafe_allow_html=True)
                    if sg["gaps"]:
                        st.markdown("**Gaps:**")
                        pills = "".join([f'<span class="sg-pill gap">⚠ {g}</span>' for g in sg["gaps"]])
                        st.markdown(f'<div class="sg-pills">{pills}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown("**Quick Info**")
                    st.caption(f"📍 {row.get('Location', 'N/A')} · {row.get('Current Company', 'N/A')}")
                    st.caption(f"⏱ Availability: {row.get('Availability', 'N/A')}")
                    st.caption(f"📋 Notice: {row.get('Notice Period', 'N/A')}")
                    if row.get("Risk Flag"):
                        st.warning(row["Risk Flag"])
                    if row.get("Recommended Action"):
                        st.info(row["Recommended Action"])

    with tab2:
        for _, row in top_df.head(5).iterrows():
            with st.expander(f"💬 {row['Name']} — Conversation", expanded=False):
                convo = row.get("Conversation", [])
                if isinstance(convo, list) and convo:
                    timeline_html = '<div class="convo-timeline">'
                    for turn in convo:
                        role = turn["role"]
                        msg = turn["message"]
                        label = "Recruiter" if role == "recruiter" else "Candidate"
                        timeline_html += f'''<div class="convo-bubble {role}">
                            <span class="convo-label">{label}</span>{msg}
                        </div>'''
                    timeline_html += '</div>'
                    st.markdown(timeline_html, unsafe_allow_html=True)
                    st.caption(f"📝 {row.get('Conversation Summary', '')}")
                else:
                    st.caption("No conversation data available.")

    with tab3:
        st.markdown("#### 📊 Recruiter Intelligence")

        # Outreach tips
        st.markdown("""
        <div class="insight-card">
            <h4>💡 Outreach Improvement Tips</h4>
            <ul>
                <li>Personalize messages with <span class="highlight">specific project mentions</span> from the candidate's profile</li>
                <li>For passive candidates (high match, low interest), try <span class="highlight">LinkedIn InMail or warm referrals</span></li>
                <li>Include <span class="highlight">compensation range</span> early — several candidates flagged comp as a decision factor</li>
                <li>Highlight <span class="highlight">growth opportunities and culture</span> for senior candidates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Risky candidates
        risky_df = final_df[final_df["Risk Flag"].str.len() > 0].head(5)
        if not risky_df.empty:
            st.markdown("""
            <div class="insight-card">
                <h4>⚠️ Flagged Candidates</h4>
            </div>
            """, unsafe_allow_html=True)
            for _, r in risky_df.iterrows():
                st.caption(f"**{r['Name']}** — {r['Risk Flag']} → {r['Recommended Action']}")

        # Next actions
        fast_track = final_df[(final_df["Match Score"] >= 60) & (final_df["Interest Score"] >= 60)].head(3)
        if not fast_track.empty:
            st.markdown("""
            <div class="insight-card">
                <h4>🟢 Recommended Next Actions</h4>
            </div>
            """, unsafe_allow_html=True)
            for _, r in fast_track.iterrows():
                st.caption(f"📞 **Schedule interview with {r['Name']}** — Match {r['Match Score']:.0f}, Interest {r['Interest Score']:.0f}")

    with tab4:
        st.markdown("#### 📦 Structured Data Export")
        structured = simulator.generate_structured_output(reqs, top_df, matcher)
        json_str = json.dumps(structured, indent=2, ensure_ascii=False)
        st.markdown(f'<div class="json-block">{json_str}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download Full JSON Report",
                data=json_str,
                file_name="talentpulse_results.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col2:
            # Drop the complex list objects before exporting to CSV
            csv_df = top_df.drop(columns=["Conversation"], errors="ignore")
            csv_data = csv_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Candidates CSV",
                data=csv_data,
                file_name="shortlisted_candidates.csv",
                mime="text/csv",
                use_container_width=True
            )

elif analyze_btn and not jd_input.strip():
    st.warning("Please paste a Job Description before clicking 'Analyse & Match'.")

elif not st.session_state.jd_parsed:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 1rem; color: #444;">
        <div style="font-size:3rem; margin-bottom:1rem; opacity: 0.5;">⚡</div>
        <div style="font-size:1.2rem; font-family: 'Space Grotesk', sans-serif;">System Ready. Input Job Description to begin.</div>
    </div>
    """, unsafe_allow_html=True)
