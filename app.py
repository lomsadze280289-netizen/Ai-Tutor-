import streamlit as st
from openai import OpenAI
import json

st.set_page_config(page_title="AI მასწავლებელი", page_icon="🎓")

st.title("🎓 AI მასწავლებელი")

# --- SIDEBAR ---
st.sidebar.header("⚙️ პარამეტრები")

subject = st.sidebar.selectbox(
    "საგანი",
    ["ინგლისური", "ისტორია", "ქართული"]
)

mode = st.sidebar.radio(
    "რეჟიმი",
    ["📖 სწავლა", "📝 ტესტი"]
)

learning_mode = st.sidebar.radio(
    "სწავლების ტიპი",
    ["🤖 პირდაპირ პასუხი", "🧠 ჯერ იფიქრე"]
)

api_key = st.sidebar.text_input("API Key", type="password")

if not api_key:
    st.warning("შეიყვანე API Key")
    st.stop()

client = OpenAI(api_key=api_key)

# ------------------------
# 📖 სწავლა
# ------------------------
if mode == "📖 სწავლა":

    question = st.text_area("დასვი კითხვა")

    if st.button("გაგზავნა"):

        if learning_mode == "🧠 ჯერ იფიქრე":
            user_answer = st.text_area("შენი პასუხი")

            if user_answer:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": f"შენ ხარ {subject}-ის მასწავლებელი"},
                        {"role": "user", "content": f"""
                        კითხვა: {question}
                        მოსწავლის პასუხი: {user_answer}

                        შეაფასე:
                        - სწორია თუ არა
                        - ახსნა
                        - სწორი პასუხი
                        """}
                    ]
                )
                st.write(response.choices[0].message.content)

        else:
            prompt = f"""
            უპასუხე მოკლედ და გასაგებად:

            1. ახსნა
            2. მაგალითი
            3. წესები
            4. დასვი კითხვა

            კითხვა:
            {question}
            """

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": f"შენ ხარ {subject}-ის მასწავლებელი"},
                    {"role": "user", "content": prompt}
                ]
            )

            st.write(response.choices[0].message.content)

# ------------------------
# 📝 ტესტი
# ------------------------
if mode == "📝 ტესტი":

    num_questions = st.slider("კითხვების რაოდენობა", 1, 5, 3)

    if st.button("ტესტის შექმნა"):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": f"შენ ხარ {subject}-ის მასწავლებელი"},
                {"role": "user", "content": f"""
                შექმენი {num_questions} კითხვა JSON ფორმატში:

                [
                  {{
                    "question": "...",
                    "options": ["A", "B", "C", "D"],
                    "correct": "A",
                    "explanation": "..."
                  }}
                ]
                """}
            ]
        )

        quiz_data = json.loads(response.choices[0].message.content)

        st.session_state.quiz = quiz_data

    if "quiz" in st.session_state:

        answers = {}

        for i, q in enumerate(st.session_state.quiz):
            st.subheader(q["question"])

            answers[i] = st.radio(
                "აირჩიე პასუხი",
                q["options"],
                key=i
            )

        if st.button("შეფასება"):

            score = 0

            for i, q in enumerate(st.session_state.quiz):
                if answers[i].startswith(q["correct"]):
                    score += 1

            st.success(f"შენი ქულა: {score}/{len(st.session_state.quiz)}")

            for i, q in enumerate(st.session_state.quiz):
                st.write(f"{q['question']}")
                st.write(f"სწორი პასუხი: {q['correct']}")
                st.write(f"ახსნა: {q['explanation']}")
                st.write("---")
