import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

# აქ ჩასვი შენი გასაღები პირდაპირ ბრჭყალებში
# ყურადღება: არავის ანახო ეს კოდი მოგვიანებით!
client = OpenAI(api_key="sk-proj-აქ_ჩასვი_შენი_ახალი_კოდი")

st.title("🎓 შენი პერსონალური ტუტორი")

subject = st.selectbox("რა ვისწავლოთ დღეს?", ["ისტორია", "ინგლისური", "ქართული"])

if st.button("მიიღე დღევანდელი გამოწვევა"):
    with st.spinner("მასწავლებელი ფიქრობს..."):
        try:
            prompt = f"შენ ხარ გამოცდილი ტუტორი. მომეცი ერთი საინტერესო მოკლე ფაქტი და ერთი კითხვა საგნიდან: {subject}. გამოიყენე მეგობრული ტონი."
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            st.markdown("---")
            st.write(response.choices[0].message.content)
            st.balloons()
        except Exception as e:
            st.error(f"ოი, რაღაც შეცდომაა: {e}")
