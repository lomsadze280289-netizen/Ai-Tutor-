import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

# აქ ჩასვი შენი გასაღები (ბრჭყალებში)
client = OpenAI(api_key="sk-proj-შენი_გასაღები_აქ")

st.title("🎓 შენი პერსონალური ტუტორი")

# საგნების სია ინგლისურად, რომ სერვერმა არ იჩხუბოს
subjects = {
    "ისტორია": "History",
    "ინგლისური": "English Language",
    "ქართული": "Georgian Literature"
}

chosen_subject_ge = st.selectbox("რა ვისწავლოთ დღეს?", list(subjects.keys()))

if st.button("მიიღე დღევანდელი გამოწვევა"):
    with st.spinner("მასწავლებელი ფიქრობს..."):
        try:
            # AI-ს ვეტყვით ინგლისურად, რომ ქართულად გვიპასუხოს
            subject_en = subjects[chosen_subject_ge]
            prompt = f"You are a helpful tutor. Give me one interesting short fact and one question about {subject_en}. Respond strictly in Georgian language."
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            st.markdown("---")
            st.write(response.choices[0].message.content)
            st.balloons()
        except Exception as e:
            st.error(f"შეცდომაა: {e}")
