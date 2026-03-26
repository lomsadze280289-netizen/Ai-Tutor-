import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

# პირდაპირ ვიღებთ გასაღებს Secrets-დან
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    st.title("🎓 ჩემი AI ტუტორი")
    st.success("API გასაღები ნაპოვნია! მზად ვართ სამუშაოდ.")
    
    subject = st.selectbox("აირჩიე საგანი:", ["ისტორია", "ინგლისური", "ქართული"])
    if st.button("მიიღე დღევანდელი გამოწვევა"):
        st.write(f"ამზადებს დავალებას {subject}-ში...")
        # აქ დაემატება AI-ს პასუხი
else:
    st.error("გთხოვთ, ჩაწეროთ OPENAI_API_KEY აპლიკაციის Secrets-ში.")
