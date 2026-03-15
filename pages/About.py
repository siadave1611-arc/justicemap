import streamlit as st

st.set_page_config(page_title="About — Justice Map", page_icon="⚖️", layout="centered")

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
.block-container { max-width: 700px; padding: 3rem 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("# Justice Map")
st.markdown("#### Legal empowerment for everyone, everywhere.")

st.markdown("""
Justice Map exists because the law is one of the most powerful forces in a person's life — 
and most people have no idea how it works where they live. Whether you're facing an unfair 
eviction, an employer who won't pay you, or a government that ignores your complaint, 
your first step is knowing your rights. Justice Map gives you that.
""")

st.markdown("---")

st.markdown("### How it works")
st.markdown("""
- **The map** shows rule-of-law scores for 143 countries, sourced from the World Justice Project Rule of Law Index 2025 — the world's most credible independent legal measurement, built from 150,000+ household surveys and 4,000+ legal experts annually.
- **The 7 categories** (Employment, Housing, Consumer, Family, Debt, Immigration, Government) each map to the closest WJP sub-indicator. These are approximations — no single score perfectly captures a legal category, but each is grounded in real data.
- **The AI Legal Guide** is powered by Claude (Anthropic). Every response is grounded in that country's actual WJP scores. It tells you what your rights look like, what the risks are, and what to do next — in plain language. It is not a lawyer and does not give legal advice.
- **The corruption warnings** appear when a country's F2 (Absence of Corruption) score falls below 0.50 — meaning courts or officials in that country have a documented history of improper influence.
""")

st.markdown("---")

st.markdown("### Built by")
st.markdown("""
**Sia Kukreja** — Year 1 IB Diploma, Dwight Global Online School, Dubai.

Studying Math AA HL, Computer Science HL, and Global Politics HL. 
Interested in applied mathematics, AI, and the intersection of technology and justice systems.

This project is part of a broader vision to make legal systems legible to the people they're 
supposed to serve — inspired by watching legal technology deployed in courtrooms, and asking 
why the same tools aren't available to the people on the other side of the bench.
""")

st.markdown("---")
st.markdown("<p style='font-size:12px;color:#9B9893;'>Data: World Justice Project Rule of Law Index 2025 · AI: Claude by Anthropic · <a href='https://github.com/siadave1611-arc/justicemap'>View on GitHub</a></p>", unsafe_allow_html=True)

if st.button("← Back to Justice Map"):
    st.switch_page("app.py")
