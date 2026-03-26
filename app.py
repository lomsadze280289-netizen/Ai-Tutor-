import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

st.title("🎓 AI მასწავლებელი (Duolingo Style)")

# --- Sidebar ---
subject = st.sidebar.selectbox(
    "საგანი",
    ["ინგლისური", "ისტორია", "ქართული"]
)

api_key = st.sidebar.text_input("API Key", type="password")

if not api_key:
    st.warning("შეიყვანე API Key")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Session State ---
if "question" not in st.session_state:
    st.session_state.question = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1

# --- Progress UI ---
st.sidebar.markdown("## 📊 პროგრესი")
st.sidebar.metric("ქულები", st.session_state.score)
st.sidebar.metric("ლეველი", st.session_state.level)

progress_value = min(st.session_state.score / 10, 1.0)
st.sidebar.progress(progress_value)

# --- ახალი კითხვა ---
if st.button("🎯 მომეცი კითხვა"):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": f"შენ ხარ {subject}-ის მასწავლებელი."
            },
            {
                "role": "user",
                "content": f"""
                მომეცი ერთი კითხვა სტუდენტის დონის მიხედვით.
                დონე: {st.session_state.level}

                არ დაწერო პასუხი.
                """
            }
        ]
    )

    st.session_state.question = response.choices[0].message.content

# --- კითხვა ---
if st.session_state.question:
    st.subheader("❓ კითხვა")
    st.write(st.session_state.question)

    user_answer = st.text_area("✍️ შენი პასუხი")

    if st.button("შეამოწმე"):

        if user_answer.strip() == "":
            st.error("დაწერე პასუხი")
        else:
            with st.spinner("შემოწმება..."):

                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": f"შენ ხარ {subject}-ის მასწავლებელი."
                        },
                        {
                            "role": "user",
                            "content": f"""
                            კითხვა: {st.session_state.question}
                            პასუხი: {user_answer}

                            შეაფასე:
                            - სწორია თუ არა (YES ან NO)
                            - დეტალური ახსნა
                            - სწორი პასუხი
                            """
                        }
                    ],
                    temperature=0
                )

                result = response.choices[0].message.content
                st.write(result)

                # --- Score logic ---
                if "YES" in result.upper():
                    st.success("სწორია! 🎉")
                    st.session_state.score += 1
                else:
                    st.error("არასწორია ❌")

                # --- Level up ---
                if st.session_state.score % 5 == 0:
                    st.session_state.level += 1
                    st.balloons()
                    st.success(f"🎉 ახალი ლეველი: {st.session_state.level}")

# --- Reset ---
if st.sidebar.button("🔄 Reset პროგრესი"):
    st.session_state.score = 0
    st.session_state.level = 1
