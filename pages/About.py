import streamlit as st

st.set_page_config(page_title="About — Justice Map", page_icon="⚖️", layout="wide")

st.markdown("# About Justice Map")
st.markdown("**Justice Map** is a legal empowerment platform that gives every person — regardless of income, education, or country — the awareness to understand their rights, recognise when they are being wronged, and know what to do next.")

st.markdown("---")

st.markdown("### Why this exists")
st.markdown("The law is complex, expensive, and different in every country. Most people don't know their rights until it's too late. Justice Map was built to change that — not by replacing lawyers, but by giving ordinary people a compass.")

st.markdown("### The data")
st.markdown("All scores come from the **World Justice Project Rule of Law Index 2025** — an independent, peer-reviewed annual survey covering 143 countries, 150,000+ household surveys, and 4,000+ legal experts.")

st.markdown("### Category score mappings")
st.table({
    "Category": ["Employment", "Housing", "Consumer", "Family", "Debt", "Immigration", "Government"],
    "WJP Indicator": ["F4.8 — Fundamental labour rights", "F7.1 — Access to civil justice", "F6 — Regulatory enforcement", "F7 — Civil justice system", "F2.1 — Absence of executive corruption", "F4.2 — Right to life & security", "F3 — Open government"],
})

st.markdown("### The AI Legal Guide")
st.markdown("Powered by Claude (Anthropic), grounded in each country's actual WJP scores. Provides legal **awareness** — not legal advice. Always consult a qualified lawyer for your specific situation.")

st.markdown("### Limitations")
st.markdown("- Data updated annually — not real-time\n- Coverage: 143 countries\n- Category mappings are approximations\n- AI responses are for awareness only")

st.markdown("### Built by")
st.markdown("**Sia Dave** · Year 1 IB Diploma · Dwight Global Online School · Dubai")
st.markdown("Inspired by Tech Unicorn — legal technology across US and GCC jurisdictions.")
st.markdown("[View source on GitHub](https://github.com/siadave1611-arc/justicemap)")
