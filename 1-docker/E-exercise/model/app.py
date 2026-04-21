import streamlit as st
from run_model import main

st.title("Model Runner")

if st.button("Run model"):
    main()
    st.success("Model run complete!")

    st.image("/app/data/output/clustering.png")