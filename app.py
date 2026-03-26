import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="ეროვნულების ტუტორი", page_icon="📚")

st.title("🎓 მომზადება ეროვნული გამოცდებისთვის")

api_key_input = st.text_input("Enter OpenAI API Key:", type="password")

# შენი საგამოცდო საგნები
subject = st.sidebar.selectbox("აირჩიე საგანი:", [
    "ინგლისური (გრამატიკა/ტექსტის გააზრება)",
    "ისტორია (თარიღები/წყაროების ანალიზი)",
    "ქართული ენა და ლიტერატურა",
    "ლოგისტიკა (სამომავლო ფაკულტეტი)"
])

level = st.sidebar.radio("სირთულე:", ["საბაზისო", "საგამოცდო (რთული)"])

if st.button("მომეცი დავალება"):
    if not api_key_input:
        st.warning("გთხოვთ, შეიყვანოთ გასაღები!")
    else:
        try:
            client = OpenAI(api_key=api_key_input)
            
            # ინსტრუქცია AI-სთვის, რომ იყოს მკაცრი და ზუსტი
            prompt = (
                f"შენ ხარ ეროვნული გამოცდების რეპეტიტორი საქართველოში. "
                f"მომეცი კონკრეტული საკითხი საგნიდან: {subject}, სირთულის დონე: {level}. "
                "1. მოკლედ ამიხსენი ერთი მნიშვნელოვანი წესი ან ფაქტი. "
                "2. დამისვი 1 საგამოცდო ტიპის კითხვა (Multiple choice ან ღია). "
                "უპასუხე მხოლოდ აკადემიური ქართულით."
            )
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            st.markdown(f"### 📝 {subject}")
            st.info(response.choices[0].message.content)
            st.balloons()
            
        except Exception as e:
            st.error(f"შეცდომა: {e}")

# პატარა წამახალისებელი სექცია
st.sidebar.markdown("---")
st.sidebar.write("🎯 **მიზანი:** უნივერსიტეტი და ლოგისტიკის ფაკულტეტი!")
