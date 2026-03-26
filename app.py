import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

# აქ ჩასვი შენი გასაღები
client = OpenAI(api_key="sk-proj-შენი_კოდი_აქ")

st.title("AI Tutor")

# ვიყენებთ მხოლოდ ინგლისურს ტექნიკური ტესტისთვის
subject = st.selectbox("Choose Subject:", ["History", "English", "Geography"])

if st.button("Get Task"):
    with st.spinner("Thinking..."):
        try:
            prompt = f"Give me one fact and one question about {subject}. Respond in English."
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            st.markdown("---")
            st.write(response.choices[0].message.content)
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
