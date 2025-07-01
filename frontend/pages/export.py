import streamlit as st
import pandas as pd

def download_results():
    try:
        df = pd.read_csv("exports/shortlist.csv")
        st.download_button("Download Shortlist", df.to_csv(index=False), file_name="shortlist.csv")
    except FileNotFoundError:
        st.warning("No shortlist file found. Run analysis first.")
