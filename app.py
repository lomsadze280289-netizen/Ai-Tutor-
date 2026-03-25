import streamlit as st
import openai
import pandas as pd

# სათაური
st.title("🎓 ჩემი AI ტუტორი")

# OpenAI API გასაღების შეყვანა (უსაფრთხოებისთვის)
api_key = st.sidebar.text_input("შეიყვანეთ OpenAI API Key:", type="password")

if api_key:
    openai.api_key = api_key
    
    # მომხმარებლის შეკითხვა
    user_input = st.text_input("დაწერე შენი შეკითხვა აქ:")

    if st.button("კითხვის დასმა"):
        if user_input:
            # AI-სთვის მოთხოვნის გაგზავნა
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            
            # პასუხის გამოტანა
            st.write("### AI-ს პასუხი:")
            st.info(response.choices[0].message.content)
        else:
            st.warning("გთხოვთ, ჯერ დაწეროთ შეკითხვა.")
else:
    st.info("გთხოვთ, გვერდითა მენიუში შეიყვანოთ OpenAI-ს API გასაღები მუშაობის დასაწყებად.")
