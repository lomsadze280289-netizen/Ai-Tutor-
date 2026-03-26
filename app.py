import streamlit as st
from openai import OpenAI

# 1. სათაური ინგლისურად
st.title("My AI Tutor")

# 2. გასაღების შეყვანა (მხოლოდ აქ ჩასვი შენი sk-proj-...)
client = OpenAI(api_key="sk-proj-აქ_ჩასვი_შენი_კოდი")

# 3. საგნის არჩევა
subject = st.selectbox("Select Subject:", ["History", "English", "Literature"])

if st.button("Start Lesson"):
    try:
        # AI-ს ვეტყვით, რომ ქართულად გვიპასუხოს, მაგრამ ბრძანება იქნება ინგლისური
        prompt = f"Give me one fun fact and one question about {subject}. Answer in Georgian language."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        st.write(response.choices[0].message.content)
        st.balloons()
    except Exception as e:
        st.error(f"Error: {e}")
