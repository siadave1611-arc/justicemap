import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from anthropic import Anthropic

st.set_page_config(
    page_title="Justice Map",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Reset & base */
[data-testid="stAppViewContainer"] { background: #FFFFFF; }
[data-testid="stHeader"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
.block-container { padding: 1rem 2rem !important; max-width: 100% !important; }
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

/* Top nav */
.topnav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; height: 48px;
    border-bottom: 1px solid #E8E8E5; background: #fff;
}
.topnav-logo { display: flex; align-items: center; gap: 10px; font-size: 15px; font-weight: 600; color: #1A1A1A; }
.topnav-logo-icon { width: 28px; height: 28px; background: #1D9E75; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; }
.topnav-right { display: flex; align-items: center; gap: 12px; font-size: 12px; color: #6B6B6B; }
.badge { background: #F0EDE8; color: #6B6B6B; padding: 3px 10px; border-radius: 20px; font-size: 11px; }

/* Filter bar */
.filterbar {
    display: flex; align-items: center; gap: 16px;
    padding: 8px 24px; background: #F8F8F6;
    border-bottom: 1px solid #E8E8E5; flex-wrap: wrap;
}
.filter-label { font-size: 11px; color: #9B9893; font-weight: 500; white-space: nowrap; }
.pill { padding: 4px 12px; border-radius: 20px; font-size: 11px; cursor: pointer; border: 1px solid #E8E8E5; background: #fff; color: #6B6B6B; white-space: nowrap; }
.pill-active { background: #1D9E75; color: #fff; border-color: #1D9E75; }
.divider { width: 1px; height: 20px; background: #E8E8E5; }

/* Main layout */
.main-layout {
    display: grid;
    grid-template-columns: 300px 1fr 300px;
    height: calc(100vh - 97px);
    overflow: hidden;
}

/* Left panel */
.left-panel {
    border-right: 1px solid #E8E8E5;
    padding: 20px 18px;
    overflow-y: auto;
    background: #fff;
}
.country-name { font-size: 28px; font-weight: 700; color: #1A1A1A; margin-bottom: 6px; }
.country-badge { display: inline-block; background: #F0EDE8; color: #6B6B6B; padding: 3px 10px; border-radius: 20px; font-size: 11px; margin-bottom: 16px; }
.score-hero { font-family: 'Georgia', serif; font-size: 52px; font-weight: 400; color: #1A1A1A; line-height: 1; margin-bottom: 4px; }
.score-label { font-size: 10px; color: #9B9893; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 20px; }
.section-label { font-size: 10px; color: #9B9893; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 12px; font-weight: 500; }

/* Category rows */
.cat-row { padding: 8px 0; border-bottom: 1px solid #F4F2EE; }
.cat-row:last-child { border-bottom: none; }
.cat-row-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.cat-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; margin-right: 8px; }
.cat-name { font-size: 13px; font-weight: 600; color: #1A1A1A; }
.cat-score { font-size: 13px; font-weight: 600; }
.cat-bar-bg { height: 3px; background: #F0EDE8; border-radius: 2px; margin-bottom: 4px; }
.cat-bar-fill { height: 3px; border-radius: 2px; }
.cat-summary { font-size: 11px; color: #9B9893; padding-left: 15px; }
.score-red { color: #D85A30; }
.score-amber { color: #EF9F27; }
.score-green { color: #1D9E75; }
.dot-red { background: #D85A30; }
.dot-amber { background: #EF9F27; }
.dot-green { background: #1D9E75; }
.bar-red { background: #D85A30; }
.bar-amber { background: #EF9F27; }
.bar-green { background: #1D9E75; }

/* Ask AI button */
.ask-btn {
    width: 100%; margin-top: 20px; padding: 12px;
    background: #1D9E75; color: white; border: none;
    border-radius: 8px; font-size: 13px; font-weight: 500;
    cursor: pointer; text-align: center;
}

/* Map area */
.map-area { background: #F8F8F6; position: relative; overflow: hidden; }

/* Right panel — chat */
.chat-panel {
    border-left: 1px solid #E8E8E5;
    display: flex; flex-direction: column;
    background: #fff; height: 100%;
}
.chat-header { padding: 16px 18px 12px; border-bottom: 1px solid #F4F2EE; }
.chat-title { font-size: 14px; font-weight: 600; color: #1A1A1A; display: flex; align-items: center; gap: 8px; }
.chat-dot { width: 8px; height: 8px; border-radius: 50%; background: #1D9E75; }
.chat-subtitle { font-size: 11px; color: #9B9893; margin-top: 2px; }
.chat-chips { padding: 12px 18px; display: flex; flex-direction: column; gap: 6px; border-bottom: 1px solid #F4F2EE; }
.chip { padding: 7px 12px; border-radius: 20px; font-size: 11px; background: #F0FAF6; border: 1px solid #B8E8D4; color: #0F6E56; cursor: pointer; display: inline-block; }
.chat-messages { flex: 1; overflow-y: auto; padding: 14px 18px; display: flex; flex-direction: column; gap: 10px; }
.msg-user { align-self: flex-end; background: #1D9E75; color: white; padding: 10px 14px; border-radius: 16px 16px 4px 16px; font-size: 12px; max-width: 85%; line-height: 1.5; }
.msg-ai { align-self: flex-start; max-width: 95%; }
.msg-ai-card { background: #F8F8F6; border: 1px solid #E8E8E5; border-radius: 4px 16px 16px 16px; padding: 12px 14px; }
.msg-step { display: flex; gap: 10px; margin-bottom: 8px; font-size: 12px; line-height: 1.5; color: #1A1A1A; }
.msg-step:last-of-type { margin-bottom: 0; }
.step-num { width: 20px; height: 20px; border-radius: 50%; background: #E1F5EE; color: #085041; font-size: 10px; font-weight: 600; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }
.msg-legal-aid { font-size: 11px; color: #9B9893; font-style: italic; margin-top: 10px; }
.chat-input-area { padding: 12px 18px; border-top: 1px solid #E8E8E5; }
.chat-placeholder { font-size: 12px; color: #9B9893; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel(
        "2025_wjp_rule_of_law_index_HISTORICAL_DATA_FILE.xlsx",
        sheet_name="Historical Data"
    )
    df.columns = [
        'country', 'year', 'country_year', 'iso3', 'region',
        'overall', 'f1', 'f1_1', 'f1_2', 'f1_3', 'f1_4', 'f1_5', 'f1_6',
        'f2', 'f2_1', 'f2_2', 'f2_3', 'f2_4',
        'f3', 'f3_1', 'f3_2', 'f3_3', 'f3_4',
        'f4', 'f4_1', 'f4_2', 'f4_3', 'f4_4', 'f4_5', 'f4_6', 'f4_7', 'f4_8',
        'f5', 'f5_1', 'f5_2', 'f5_3',
        'f6', 'f6_1', 'f6_2', 'f6_3', 'f6_4', 'f6_5',
        'f7', 'f7_1', 'f7_2', 'f7_3', 'f7_4', 'f7_5', 'f7_6', 'f7_7',
        'f8', 'f8_1', 'f8_2', 'f8_3', 'f8_4', 'f8_5', 'f8_6', 'f8_7'
    ]
    numeric_cols = ['overall','f1','f2','f3','f4','f5','f6','f7','f7_1','f8',
                    'f2_1','f2_2','f2_3','f2_4']
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['year'] = df['year'].astype(str).str.extract(r'(\d{4})')[0].astype(str)
    return df

# ── Legal aid links ─────────────────────────────────────────────────────────────
LEGAL_AID = {
    "India": "NALSA — nalsa.gov.in",
    "United States": "LawHelp.org — lawhelp.org",
    "United Kingdom": "Legal Aid — gov.uk/legal-aid",
    "Kenya": "NLAS — nlakenya.org",
    "Nigeria": "LACON — laconigeria.org",
    "South Africa": "Legal Aid SA — legal-aid.co.za",
    "Brazil": "Defensoria Pública — anadep.org.br",
    "Pakistan": "PILDAT — pildat.org",
    "Bangladesh": "NLASO — nlaso.gov.bd",
    "Philippines": "PAO — pao.gov.ph",
}
DEFAULT_LEGAL_AID = "Search 'free legal aid' + your city name"

# ── Category mapping to WJP factors ────────────────────────────────────────────
CATEGORIES = {
    "Employment":   {"col": "f4_8", "label": "Labour rights protection"},
    "Housing":      {"col": "f7_1", "label": "Civil justice access & affordability"},
    "Consumer":     {"col": "f6",   "label": "Regulatory enforcement"},
    "Family":       {"col": "f7",   "label": "Civil justice system"},
    "Debt":         {"col": "f2_1", "label": "Absence of executive corruption"},
    "Immigration":  {"col": "f4_2", "label": "Right to life & security"},
    "Government":   {"col": "f3",   "label": "Open government"},
}

CATEGORY_SUMMARIES = {
    "Employment": {
        (0.0, 0.45): "Weak unfair dismissal and wage protections",
        (0.45, 0.60): "Some labour protections, enforcement varies",
        (0.60, 1.01): "Relatively strong worker rights framework",
    },
    "Housing": {
        (0.0, 0.45): "Limited eviction remedies, civil justice costly",
        (0.45, 0.60): "Some housing protections, access uneven",
        (0.60, 1.01): "Civil justice relatively accessible",
    },
    "Consumer": {
        (0.0, 0.45): "Weak buyer protections, poor enforcement",
        (0.45, 0.60): "Some consumer protections exist",
        (0.60, 1.01): "Reasonably strong consumer protection",
    },
    "Family": {
        (0.0, 0.45): "Family courts slow, costly and inconsistent",
        (0.45, 0.60): "Family law exists but enforcement is patchy",
        (0.60, 1.01): "Family justice system generally functional",
    },
    "Debt": {
        (0.0, 0.45): "Predatory lending poorly regulated",
        (0.45, 0.60): "Some debt protections, corruption risk present",
        (0.60, 1.01): "Reasonable debt and lending oversight",
    },
    "Immigration": {
        (0.0, 0.45): "High rate of unresolved cases, rights at risk",
        (0.45, 0.60): "Some protections for migrants, gaps remain",
        (0.60, 1.01): "Basic rights relatively protected",
    },
    "Government": {
        (0.0, 0.45): "Benefits and admin disputes hard to challenge",
        (0.45, 0.60): "Some accountability mechanisms exist",
        (0.60, 1.01): "Government relatively open and accountable",
    },
}

def get_summary(category, score):
    if score is None or pd.isna(score):
        return "Insufficient data"
    for (low, high), text in CATEGORY_SUMMARIES[category].items():
        if low <= score < high:
            return text
    return "Insufficient data"

def score_color(score):
    if score is None or pd.isna(score):
        return "grey", "grey", "grey"
    if score < 0.45:
        return "score-red", "dot-red", "bar-red"
    elif score < 0.60:
        return "score-amber", "dot-amber", "bar-amber"
    else:
        return "score-green", "dot-green", "bar-green"

# ── Session state ───────────────────────────────────────────────────────────────
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "India"
if "selected_year" not in st.session_state:
    st.session_state.selected_year = "2025"
if "selected_dimension" not in st.session_state:
    st.session_state.selected_dimension = "overall"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

df = load_data()

# ── Top nav ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topnav">
  <div class="topnav-logo">
    <div class="topnav-logo-icon"><svg width="20" height="20" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="50" y1="10" x2="50" y2="90" stroke="white" stroke-width="6" stroke-linecap="round"/><line x1="15" y1="25" x2="85" y2="25" stroke="white" stroke-width="6" stroke-linecap="round"/><path d="M 5,25 Q 15,45 25,25" stroke="white" stroke-width="5" stroke-linecap="round" fill="none"/><path d="M 75,25 Q 85,45 95,25" stroke="white" stroke-width="5" stroke-linecap="round" fill="none"/><line x1="35" y1="90" x2="65" y2="90" stroke="white" stroke-width="6" stroke-linecap="round"/></svg></div>
    Justice Map
  </div>
  <div class="topnav-right">
    <span class="badge">Source: WJP Rule of Law Index 2025</span>
    <span style="font-size:16px">🌐</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Filter bar ──────────────────────────────────────────────────────────────────
dims = {"Overall Score": "overall", "Civil Justice": "f7", "Fundamental Rights": "f4", "Criminal Justice": "f8"}
years = sorted(df['year'].dropna().unique().tolist(), reverse=True)
regions = ["All Regions"] + sorted(df['region'].dropna().unique().tolist())

col_f1, col_f2, col_f3 = st.columns([3, 1.2, 0.8])
with col_f1:
    dim_choice = st.radio("Dimension", list(dims.keys()), horizontal=True, label_visibility="collapsed")
    st.session_state.selected_dimension = dims[dim_choice]
with col_f2:
    region_filter = st.selectbox("Region", regions, label_visibility="collapsed")
with col_f3:
    year_choice = st.select_slider("Year", options=sorted(df['year'].dropna().unique().tolist()),
                                   value="2025", label_visibility="collapsed")
    st.session_state.selected_year = year_choice

st.divider()

# ── Filter data ─────────────────────────────────────────────────────────────────
year_df = df[df['year'] == st.session_state.selected_year].copy()
if region_filter != "All Regions":
    year_df = year_df[year_df['region'] == region_filter]

country_data = df[
    (df['country'] == st.session_state.selected_country) &
    (df['year'] == st.session_state.selected_year)
]
row = country_data.iloc[0] if len(country_data) > 0 else None

# ── Three columns ───────────────────────────────────────────────────────────────
spacer, left, centre, right = st.columns([0.05, 1.1, 2.2, 1.1], gap="small")

# ══ LEFT PANEL ══════════════════════════════════════════════════════════════════
with left:
    country = st.session_state.selected_country
    region_label = row['region'] if row is not None else "—"
    overall = round(float(row['overall']), 2) if row is not None and pd.notna(row['overall']) else None

    st.markdown(f"<h2 style='font-size:28px;font-weight:700;color:#1A1A1A;margin-bottom:4px;'>{country}</h2>", unsafe_allow_html=True)
    st.markdown(f"<span style='background:#F0EDE8;color:#6B6B6B;padding:3px 10px;border-radius:20px;font-size:11px;'>{region_label} · {st.session_state.selected_year}</span>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family:Georgia,serif;font-size:48px;color:#1A1A1A;line-height:1;margin:12px 0 4px;'>{overall if overall else '—'}</div>", unsafe_allow_html=True)
    st.caption("OVERALL RULE OF LAW SCORE")
    st.divider()
    st.caption("YOUR RIGHTS HERE")

    for cat_name, meta in CATEGORIES.items():
        col = meta["col"]
        score = round(float(row[col]), 2) if row is not None and pd.notna(row[col]) else None
        summary = get_summary(cat_name, score)
        sc, dc, bc = score_color(score)
        bar_w = int((score or 0) * 100)
        score_txt = f"{score:.2f}" if score else "—"

        st.markdown(f"""
        <div class="cat-row">
          <div class="cat-row-top">
            <span><span class="cat-dot {dc}"></span><span class="cat-name">{cat_name}</span></span>
            <span class="cat-score {sc}">{score_txt}</span>
          </div>
          <div class="cat-bar-bg"><div class="cat-bar-fill {bc}" style="width:{bar_w}%"></div></div>
          <div style="font-size:11px;color:#9B9893;padding-left:15px;">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Ask AI about your rights in " + country, use_container_width=True, type="primary"):
        prompt = f"Give me a plain-language overview of the most important rights people should know about in {country}."
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.rerun()

# ══ CENTRE — MAP ════════════════════════════════════════════════════════════════
with centre:
    dim_col = st.session_state.selected_dimension
    map_title = {
        "overall": "Rule of Law — Overall Score",
        "f7": "Civil Justice Score",
        "f4": "Fundamental Rights Score",
        "f8": "Criminal Justice Score"
    }.get(dim_col, "Score")

    map_data = year_df[['country', 'iso3', dim_col, 'region']].dropna(subset=[dim_col])
    map_data = map_data.rename(columns={dim_col: 'score'})
    map_data['score'] = pd.to_numeric(map_data['score'], errors='coerce')
    map_data = map_data.dropna(subset=['score'])
    map_data['score_fmt'] = map_data['score'].round(2)

    fig = px.choropleth(
        map_data,
        locations="iso3",
        color="score",
        hover_name="country",
        hover_data={"score_fmt": True, "iso3": False, "score": False},
        color_continuous_scale=["#D85A30", "#EF9F27", "#1D9E75"],
        range_color=[0, 1],
        labels={"score_fmt": map_title, "score": "Score"}
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#F8F8F6",
        plot_bgcolor="#F8F8F6",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#DDDDDA",
            showland=True,
            landcolor="#EEECEA",
            showocean=True,
            oceancolor="#F8F8F6",
            showlakes=False,
            bgcolor="#F8F8F6",
            projection_type="natural earth"
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Score", font=dict(size=11, color="#9B9893")),
            tickfont=dict(size=10, color="#9B9893"),
            thickness=10,
            len=0.4,
            x=0.01,
            xanchor="left",
            y=0.1,
            yanchor="bottom",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E8E8E5",
            borderwidth=1,
        ),
        height=580
    )

    clicked = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="map")

    if clicked and clicked.get("selection") and clicked["selection"].get("points"):
        pt = clicked["selection"]["points"][0]
        clicked_country = pt.get("hovertext") or pt.get("location")
        if clicked_country and clicked_country in df['country'].values:
            st.session_state.selected_country = clicked_country
            st.rerun()

    # Country selector fallback
    all_countries = sorted(df[df['year'] == st.session_state.selected_year]['country'].dropna().unique().tolist())
    selected = st.selectbox(
        "Or select a country:",
        all_countries,
        index=all_countries.index(st.session_state.selected_country) if st.session_state.selected_country in all_countries else 0,
        label_visibility="visible"
    )
    if selected != st.session_state.selected_country:
        st.session_state.selected_country = selected
        st.rerun()

# ══ RIGHT PANEL — AI CHAT ════════════════════════════════════════════════════════
with right:
    st.markdown(f"""
    <div class="chat-header">
      <div class="chat-title"><span class="chat-dot"></span> AI Legal Guide</div>
      <div class="chat-subtitle">Grounded in {st.session_state.selected_country}'s legal context</div>
    </div>
    """, unsafe_allow_html=True)

    # Suggested prompts
    country = st.session_state.selected_country
    suggestions = [
        f"Rights if fired without notice in {country}?",
        f"Can my landlord evict me in {country}?",
        f"How corrupt are courts in {country}?",
    ]

    for s in suggestions:
        if st.button(s, key=f"chip_{s}", use_container_width=False):
            st.session_state.chat_messages.append({"role": "user", "content": s})
            st.rerun()

    # Chat messages display
    chat_container = st.container(height=340)
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-ai-card" style="background:#F8F8F6;border:1px solid #E8E8E5;border-radius:4px 16px 16px 16px;padding:12px 14px;font-size:12px;line-height:1.6;color:#1A1A1A;">{msg["content"]}</div>', unsafe_allow_html=True)

    # AI response trigger
    if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "user":
        country = st.session_state.selected_country
        country_scores = ""
        if row is not None:
            country_scores = f"""
WJP Rule of Law scores for {country} ({st.session_state.selected_year}):
- Overall: {round(float(row['overall']),2) if pd.notna(row['overall']) else 'N/A'}
- Civil Justice (F7): {round(float(row['f7']),2) if pd.notna(row['f7']) else 'N/A'}
- Fundamental Rights (F4): {round(float(row['f4']),2) if pd.notna(row['f4']) else 'N/A'}
- Criminal Justice (F8): {round(float(row['f8']),2) if pd.notna(row['f8']) else 'N/A'}
- Absence of Corruption (F2): {round(float(row['f2']),2) if pd.notna(row['f2']) else 'N/A'}
- Access to Civil Justice (7.1): {round(float(row['f7_1']),2) if pd.notna(row['f7_1']) else 'N/A'}
"""

        system_prompt = f"""You are the AI Legal Guide for Justice Map, a legal empowerment platform.
You are currently helping a user in {country}.

{country_scores}

Your role:
- Give plain-language explanations of legal rights — no jargon
- Be specific to {country}'s legal context when possible
- Give practical, actionable steps (numbered)
- Always end with: "For your specific situation, consult a qualified lawyer."
- If relevant, mention free legal aid: {LEGAL_AID.get(country, DEFAULT_LEGAL_AID)}
- You are NOT providing legal advice — you are providing legal awareness
- Keep responses concise: 3-4 sentences or 3 numbered steps max
- Scores below 0.45 = serious concern, 0.45-0.60 = some risk, above 0.60 = relatively functional
- Be honest about corruption or systemic issues when scores indicate them"""

        client = Anthropic()
        messages_for_api = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_messages
        ]

        with st.spinner(""):
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=400,
                system=system_prompt,
                messages=messages_for_api
            )
            reply = response.content[0].text
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            user_input = st.text_input(
                "chat",
                placeholder=f"Ask about your rights in {st.session_state.selected_country}…",
                label_visibility="collapsed"
            )
        with col_btn:
            submitted = st.form_submit_button("→", use_container_width=True)

        if submitted and user_input.strip():
            st.session_state.chat_messages.append({"role": "user", "content": user_input.strip()})
            st.rerun()

    if st.button("Clear chat", key="clear_chat", use_container_width=False):
        st.session_state.chat_messages = []
        st.rerun()
