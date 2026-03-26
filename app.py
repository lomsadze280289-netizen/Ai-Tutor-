import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

st.title("My AI Tutor")

# გასაღებს შევიყვანთ საიტზევე, ველში
api_key_input = st.text_input("Enter OpenAI API Key:", type="password")

subject = st.selectbox("Select Subject:", ["History", "English", "Literature"])

if st.button("Start Lesson"):
    if not api_key_input:
        st.warning("Please enter your API Key first!")
    else:
        try:
            client = OpenAI(api_key=api_key_input)
            prompt = f"Give me one fun fact and one question about {subject}. Answer in Georgian language."
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            st.write(response.choices[0].message.content)
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
