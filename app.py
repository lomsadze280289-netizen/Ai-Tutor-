import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="შენი რეპეტიტორი", page_icon="🎓")

st.title("🎓 მოემზადე ეროვნულებისთვის")

# გასაღების ველი
api_key = st.text_input("Enter API Key:", type="password")

# საგნის არჩევანი
subject = st.sidebar.selectbox("აირჩიე საგანი:", [
    "ინგლისური: Grammatical Structures",
    "ისტორია: მონღოლთა იმპერია და საქართველო",
    "ისტორია: ფეოდალიზმი",
    "ლოგისტიკა: ტრანსპორტირება და დასაწყობება"
])

if st.button("მიიღე დავალება"):
    if not api_key:
        st.error("გთხოვთ, შეიყვანოთ გასაღები!")
    else:
        try:
            client = OpenAI(api_key=api_key)
            st.session_state.client = client # ვინახავთ კლიენტს სესიაში
            
            prompt = f"შენ ხარ რეპეტიტორი. მომეცი 1 მოკლე საგამოცდო საკითხი თემაზე: {subject}. ჯერ ამიხსენი და მერე დამისვი 1 კითხვა. არ დაწერო პასუხი!"
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.question = response.choices[0].message.content
            st.session_state.answered = False
        except Exception as e:
            st.error(f"შეცდომა: {e}")

# თუ კითხვა უკვე დასმულია, გამოვაჩინოთ პასუხის ველი
if "question" in st.session_state:
    st.info(st.session_state.question)
    
    user_answer = st.text_area("ჩაწერე შენი პასუხი აქ:")
    
    if st.button("შეამოწმე პასუხი"):
        if user_answer:
            with st.spinner("მასწავლებელი ასწორებს..."):
                check_prompt = f"მოსწავლემ უპასუხა ასე: '{user_answer}' ამ კითხვაზე: '{st.session_state.question}'. შეაფასე პასუხი, აუხსენი შეცდომა თუ აქვს და დაუწერე წამახალისებელი სიტყვა."
                
                check_res = st.session_state.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": check_prompt}]
                )
                st.success(check_res.choices[0].message.content)
                st.balloons()
        else:
            st.warning("ჯერ ჩაწერე პასუხი!")
