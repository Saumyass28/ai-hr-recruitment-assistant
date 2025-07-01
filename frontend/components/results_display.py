import streamlit as st
import pandas as pd

def show_results(results):
    df = pd.DataFrame(results)
    st.dataframe(df)
    df.to_csv("exports/shortlist.csv", index=False)
    st.success("✅ Results saved to exports/shortlist.csv")