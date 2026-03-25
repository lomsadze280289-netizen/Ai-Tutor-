import openai
import streamlit as st
import json
import os
from datetime import datetime

# --- 1. კონფიგურაცია ---
client = openai.OpenAI(api_key="შენი_API_კლავი")
DATA_FILE = "ai_tutor_master_data.json"

st.set_page_config(page_title="AI Tutor Pro", page_icon="🎓", layout="wide")

# --- 2. მონაცემების მართვის ფუნქციები ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "history": [], 
        "mistakes_bank": [], 
        "current_level": "Beginner",
        "last_session": ""
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

# --- 3. AI ლოგიკის ფუნქციები ---

def speak_text(text):
    """ტექსტის აუდიოდ გადაქცევა"""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text[:4096] # ლიმიტი
        )
        audio_path = "lesson_audio.mp3"
        response.stream_to_file(audio_path)
        return audio_path
    except: return None

def generate_ai_content(prompt_type, subject):
    """გენერირებს კონტენტს (დღიური, შეცდომები, ან გამოცდა)"""
    data = st.session_state.user_data
    level = data["current_level"]
    
    prompts = {
        "daily": f"მოამზადე {level} დონის გაკვეთილი {subject}-ში. თემა შეარჩიე ეროვნული პროგრამიდან.",
        "review": f"მომხმარებელს გაუჭირდა ეს საკითხები: {json.dumps(data['mistakes_bank'][-5:])}. შექმენი სავარჯიშო მათ გადასამეორებლად.",
        "exam": f"შექმენი შემაჯამებელი გამოცდა (10 კითხვა) ამ კვირის ისტორიიდან: {json.dumps(data['history'][-10:])}"
    }

    system_instr = "You are a Georgian Exam Expert. Output ONLY valid JSON."
    json_format = """
    {
      "topic": "თემა",
      "material": "ვრცელი სასწავლო ტექსტი",
      "questions": [
        {"q": "კითხვა", "options": ["ა", "ბ", "გ", "დ"], "correct": 0, "exp": "ახსნა"}
      ]
    }
    """
    
    full_prompt = f"{prompts[prompt_type]}. გამოიყენე ეს ფორმატი: {json_format}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_instr}, {"role": "user", "content": full_prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

# --- 4. დონის განახლების ლოგიკა ---
def check_level_up():
    history = st.session_state.user_data["history"]
    if len(history) >= 3:
        last_scores = [h['score']/h['total'] for h in history[-3:]]
        avg = sum(last_scores) / 3
        if avg > 0.85: st.session_state.user_data["current_level"] = "Intermediate"
        if avg > 0.95: st.session_state.user_data["current_level"] = "Expert"
        save_data(st.session_state.user_data)

# --- 5. ინტერფეისი (UI) ---

st.sidebar.title("🚀 AI პერსონალური რეპეტიტორი")
st.sidebar.subheader(f"დონე: {st.session_state.user_data['current_level']}")
st.sidebar.progress(0.3 if st.session_state.user_data['current_level']=="Beginner" else 0.7 if st.session_state.user_data['current_level']=="Intermediate" else 1.0)

menu = st.sidebar.radio("გადადი:", ["📅 დღის გაკვეთილი", "📕 შეცდომების რვეული", "🏆 გამოცდის სიმულატორი", "📊 სტატისტიკა"])

subject = st.sidebar.selectbox("საგანი:", ["ისტორია", "ქართული ენა", "ლიტერატურა", "ინგლისური"])

if menu == "📅 დღის გაკვეთილი":
    st.header("დღევანდელი გამოწვევა")
    if st.button("✨ ახალი მასალის მიღება"):
        with st.spinner("AI ამზადებს პერსონალურ მასალას..."):
            st.session_state.current_lesson = generate_ai_content("daily", subject)
    
    if "current_lesson" in st.session_state:
        lesson = st.session_state.current_lesson
        st.subheader(f"📘 {lesson['topic']}")
        
        # ხმის ღილაკი
        if st.button("🔊 მოუსმინე მასწავლებელს"):
            audio = speak_text(lesson['material'])
            if audio: st.audio(audio)
            
        st.info(lesson['material'])
        
        with st.form("lesson_form"):
            user_answers = []
            for i, q in enumerate(lesson['questions']):
                st.write(f"**{i+1}. {q['q']}**")
                user_answers.append(st.radio("აირჩიე:", q['options'], key=f"l_{i}"))
            
            if st.form_submit_button("დასრულება"):
                score = 0
                for i, q in enumerate(lesson['questions']):
                    if user_answers[i] == q['options'][q['correct']]:
                        score += 1
                        st.success(f"✅ {i+1}: სწორია!")
                    else:
                        st.error(f"❌ {i+1}: შეცდომაა. სწორია: {q['options'][q['correct']]}")
                        st.session_state.user_data["mistakes_bank"].append({"topic": lesson['topic'], "q": q['q']})
                
                # შენახვა
                st.session_state.user_data["history"].append({
                    "date": str(datetime.now().date()), 
                    "topic": lesson['topic'], 
                    "score": score, 
                    "total": len(lesson['questions'])
                })
                check_level_up()
                save_data(st.session_state.user_data)
                st.balloons()

elif menu == "📕 შეცდომების რვეული":
    st.header("📕 შეცდომების ანალიზი")
    mistakes = st.session_state.user_data["mistakes_bank"]
    if not mistakes:
        st.success("ყოჩაღ! შენი შეცდომების რვეული ცარიელია.")
    else:
        st.write(f"გაქვს {len(mistakes)} დასამუშავებელი საკითხი.")
        if st.button("🔄 დაიწყე შეცდომების გადამეორება"):
            st.session_state.review_task = generate_ai_content("review", subject)
            
        if "review_task" in st.session_state:
            # აქ ანალოგიური ფორმა იქნება რაც გაკვეთილში...
            st.write(st.session_state.review_task["material"])

elif menu == "🏆 გამოცდის სიმულატორი":
    st.header("🏆 კვირის დიდი გამოცდა")
    st.write("ეს ტესტი აჯამებს შენს მიერ ნასწავლ ყველა საკითხს.")
    if st.button("🚀 გამოცდის გენერირება"):
        st.session_state.exam = generate_ai_content("exam", subject)
    
    if "exam" in st.session_state:
        st.warning("ყურადღება: გამოცდა დაიწყო!")
        # გამოცდის ლოგიკა...

elif menu == "📊 სტატისტიკა":
    st.header("📈 შენი პროგრესი")
    if st.session_state.user_data["history"]:
        import pandas as pd
        df = pd.DataFrame(st.session_state.user_data["history"])
        st.line_chart(df.set_index("date")["score"])
        st.table(df)
    else:
        st.info("მონაცემები ჯერ არ არის.")
