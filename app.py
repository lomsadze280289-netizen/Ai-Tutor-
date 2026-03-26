import streamlit as st
import os

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

st.title("AI Tutor Test")

# ამჯერად OpenAI-ს გარეშე ვტესტავთ, რომ შეცდომა გაქრეს
subject = st.selectbox("Choose Subject:", ["History", "English", "Geography"])

if st.button("Get Task"):
    st.balloons()
    if subject == "History":
        st.success("Fact: The Mongol Empire was the largest contiguous land empire in history.")
        st.info("Question: Who was the founder of the Mongol Empire?")
    elif subject == "English":
        st.success("Fact: 'Queue' is the only word in the English language that is still pronounced the same way when the last four letters are removed.")
        st.info("Question: Can you name three irregular verbs?")
    else:
        st.success("Ready! We will add more subjects soon.")
