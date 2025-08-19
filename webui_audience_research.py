import streamlit as st
from src.open_deep_research.audience_research import perform_audience_research

st.set_page_config(page_title="Audience Research Assistant", layout="centered")
st.title("Audience Research Assistant")

mode = st.selectbox(
    "Choose your research mode:",
    [
        "Research Papers",
        "Surveys",
        "Statistica"
    ]
)

mode_map = {
    "Research Papers": "research_papers",
    "Surveys": "surveys",
    "Statistica": "statistica"
}

query = st.text_input("Enter your research question or topic:")

if st.button("Run Research") and query:
    with st.spinner("Running research, please wait..."):
        summary, links = perform_audience_research(mode_map[mode], query)
    st.subheader("Summary of Insights")
    st.write(summary)
    st.subheader("Source Links")
    for link in links:
        st.write(f"- [{link}]({link})")
