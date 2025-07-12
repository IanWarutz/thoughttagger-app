import streamlit as st
import pandas as pd
import datetime
import random
import os

# --- Optional: Google Sheets Integration ---
# import gspread
# from google.oauth2.service_account import Credentials

# # Uncomment and configure if you want Google Sheets integration
# SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# CREDS = Credentials.from_service_account_file("YOUR_SERVICE_ACCOUNT.json", scopes=SCOPE)
# SHEET_NAME = "ThoughtTaggerData"
# gc = gspread.authorize(CREDS)
# sh = gc.open(SHEET_NAME)
# worksheet = sh.sheet1

st.set_page_config(page_title="🏷️ Thought Tagger", page_icon="🏷️", layout="centered")
st.title("🏷️ Thought Tagger – Build Emotional Clarity with Tags")

# --- Tag explanations and suggestions ---
tag_info = {
    "anxiety": {
        "type": "negative",
        "explanation": "This thought may reflect anxiety or worry.",
        "tip": "Try deep breathing, journaling, or talking to someone you trust to manage anxious feelings."
    },
    "gratitude": {
        "type": "positive",
        "explanation": "This thought expresses gratitude or appreciation.",
        "tip": "Keep noticing and celebrating the good things in your life to maintain this positive outlook!"
    },
    "goals": {
        "type": "positive",
        "explanation": "This thought is focused on your goals and ambitions.",
        "tip": "Break big goals into small steps and celebrate your progress to keep up the momentum."
    },
    "self-doubt": {
        "type": "negative",
        "explanation": "This thought shows self-doubt or uncertainty.",
        "tip": "Remind yourself of past successes and talk kindly to yourself to build confidence."
    },
    "joy": {
        "type": "positive",
        "explanation": "This thought radiates joy or excitement.",
        "tip": "Share your joy with others and savor these moments to reinforce happiness."
    },
    "anger": {
        "type": "negative",
        "explanation": "This thought contains anger or frustration.",
        "tip": "Pause, breathe, and consider healthy ways to express or release your anger."
    },
    "sadness": {
        "type": "negative",
        "explanation": "This thought reflects sadness or feeling down.",
        "tip": "Reach out for support, practice self-care, and remember that it's okay to feel sad sometimes."
    },
    "calm": {
        "type": "positive",
        "explanation": "This thought reflects calmness or peace.",
        "tip": "Continue your calming routines and mindfulness practices to maintain this state."
    },
    "stress": {
        "type": "negative",
        "explanation": "This thought signals stress or overwhelm.",
        "tip": "Take breaks, prioritize tasks, and practice relaxation techniques to reduce stress."
    },
    "love": {
        "type": "positive",
        "explanation": "This thought is about love, care, or affection.",
        "tip": "Express your love and appreciation to others to strengthen your relationships."
    },
    "reflection": {
        "type": "positive",
        "explanation": "This thought shows self-reflection and awareness.",
        "tip": "Keep reflecting on your experiences to grow and learn."
    },
    "growth": {
        "type": "positive",
        "explanation": "This thought is about personal growth.",
        "tip": "Celebrate your progress and stay open to new learning opportunities."
    },
    "awareness": {
        "type": "positive",
        "explanation": "This thought demonstrates awareness and mindfulness.",
        "tip": "Stay present and mindful to continue building self-awareness."
    },
    "mindfulness": {
        "type": "positive",
        "explanation": "This thought is rooted in mindfulness.",
        "tip": "Practice mindfulness daily to maintain clarity and calm."
    }
}

# --- Data Privacy Notice and Consent ---
st.info(
    "🔒 **Data Collection & Privacy Notice**\n\n"
    "To help us understand thought patterns, we collect some basic demographic information (age, gender, profession) along with your tagged thoughts. "
    "All your data will be kept confidential and securely stored. By continuing, you consent to participate in this data collection. "
    "If you do not consent, you will not be able to use the thought tagger."
)

if "consent_given" not in st.session_state:
    st.session_state.consent_given = None

if st.session_state.consent_given is None:
    consent = st.radio(
        "Do you consent to the collection and safe storage of your demographic data and tagged thoughts?",
        ["Yes, I consent", "No, I do not consent"],
        index=None
    )
    if consent == "Yes, I consent":
        st.session_state.consent_given = True
        st.rerun()
    elif consent == "No, I do not consent":
        st.session_state.consent_given = False
        st.warning("You must provide consent to use the Thought Tagger. Thank you for considering.")
        st.stop()
else:
    if not st.session_state.consent_given:
        st.warning("You must provide consent to use the Thought Tagger. Thank you for considering.")
        st.stop()

# --- Demographics Collection with Age Restriction ---
if "demographics" not in st.session_state:
    with st.form("demographics_form", clear_on_submit=False):
        st.subheader("Tell us a bit about yourself (demographics)")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", options=["", "Prefer not to say", "Female", "Male", "Non-binary", "Other"])
        profession = st.text_input("Profession (e.g., Student, Engineer, Teacher, etc.)")
        submitted = st.form_submit_button("Submit Demographics")
        if submitted:
            if not (age and gender and profession.strip()):
                st.error("Please enter your age, gender, and profession.")
                st.stop()
            if age < 18:
                st.error("Sorry, you must be at least 18 years old to use this app.")
                st.stop()
            st.session_state.demographics = {
                "age": int(age),
                "gender": gender,
                "profession": profession.strip()
            }
            st.success("Demographics saved! Thank you.")
            st.rerun()

if "demographics" not in st.session_state:
    st.stop()

st.write(
    f"Welcome, {st.session_state.demographics['profession']}! "
    "Tag your thoughts, discover your mental patterns, and build clarity. "
    "Let’s restore inner calm and boost your self-awareness!"
)

# --- Thought Tracking for 2 Weeks ---
if "thought_data" not in st.session_state:
    st.session_state.thought_data = []

if "start_date" not in st.session_state:
    st.session_state.start_date = datetime.date.today()

today = datetime.date.today()
days_since_start = (today - st.session_state.start_date).days + 1
days_required = 14

st.info(f"🗓️ Day {min(days_since_start, days_required)} of your 14-day thought tagging journey!")
if days_since_start < days_required:
    st.info(f"Keep logging your thoughts daily for {days_required} days to build a powerful self-awareness habit! ({days_required - days_since_start} days to go)")
else:
    st.success("🎉 Congratulations! You've completed 14 days of thought tagging. Keep going for even deeper insights!")

# --- Automatic Tagging Logic (constant time/space) ---
auto_tags = [
    ("anxiety", ["worry", "nervous", "anxious", "panic", "afraid"]),
    ("gratitude", ["thank", "grateful", "appreciate", "blessed"]),
    ("goals", ["goal", "plan", "future", "ambition", "dream"]),
    ("self-doubt", ["doubt", "uncertain", "insecure", "not sure"]),
    ("joy", ["happy", "joy", "excited", "delight", "pleased"]),
    ("anger", ["angry", "mad", "furious", "annoyed"]),
    ("sadness", ["sad", "down", "unhappy", "depressed", "cry"]),
    ("calm", ["calm", "peace", "relaxed", "serene"]),
    ("stress", ["stress", "overwhelmed", "pressure", "tense"]),
    ("love", ["love", "affection", "care", "fond"]),
]

def assign_auto_tag(thought):
    thought_lower = thought.lower()
    for tag, keywords in auto_tags:
        if any(word in thought_lower for word in keywords):
            return tag
    return random.choice(["reflection", "growth", "awareness", "mindfulness"])

# --- Data Storage: Save to CSV (or Google Sheets if enabled above) ---
CSV_FILE = "thought_logs.csv"

def save_to_csv(entry):
    df = pd.DataFrame([entry])
    if not os.path.isfile(CSV_FILE):
        df.to_csv(CSV_FILE, index=False)
    else:
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)

# --- Thought Tagging Section ---
st.header("📝 Add a Thought and Tag It")
with st.form("thought_form", clear_on_submit=True):
    thought = st.text_area("Enter your thought")
    tags = st.text_input("Enter tags for this thought (comma-separated, e.g., anxiety, gratitude, goals) [Optional]")
    submitted = st.form_submit_button("Add Thought")
    if submitted:
        if not thought.strip():
            st.error("Please enter a thought.")
        else:
            tag_list = [tag.strip().lower() for tag in tags.split(",") if tag.strip()]
            auto_tag = assign_auto_tag(thought)
            if auto_tag not in tag_list:
                tag_list.append(auto_tag)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = {
                "thought": thought.strip(),
                "tags": ", ".join(tag_list),
                "auto_tag": auto_tag,
                "time": timestamp,
                "date": today.isoformat(),
                "user": st.session_state.demographics['profession']
            }
            st.session_state.thought_data.append(entry)
            save_to_csv(entry)
            # # For Google Sheets, uncomment below:
            # worksheet.append_row(list(entry.values()))
            info = tag_info.get(auto_tag, {"explanation": "No info.", "tip": ""})
            st.success(f"Thought tagged and saved! (Auto-tag: **{auto_tag}**)\n\n"
                       f"**Why this tag?** {info['explanation']}\n\n"
                       f"**Tip:** {info['tip']}")

# --- Review Tagged Thoughts ---
if st.session_state.thought_data:
    st.header("📂 Review Your Tagged Thoughts")
    all_tags = sorted({tag for entry in st.session_state.thought_data for tag in entry["tags"].split(", ")})
    selected_tag = st.selectbox("Filter by tag", options=["All"] + all_tags)
    filtered = st.session_state.thought_data if selected_tag == "All" else [
        entry for entry in st.session_state.thought_data if selected_tag in entry["tags"].split(", ")
    ]
    for entry in filtered:
        info = tag_info.get(entry["auto_tag"], {"explanation": "", "tip": ""})
        st.markdown(
            f"- **{entry['time']}**: {entry['thought']}  \n"
            f"  _Tags: {entry['tags']}_  \n"
            f"  _User: {entry['user']}_  \n"
            f"  _Auto-tag: {entry['auto_tag']} – {info['explanation']} Tip: {info['tip']}_"
        )

    unique_days = {entry["date"] for entry in st.session_state.thought_data}
    st.info(f"📅 You've logged thoughts on {len(unique_days)} out of {days_required} days.")
    st.info("Tip: Use this log to spot recurring thought patterns and gain clarity over time.")

# --- Call to Action & Advertisement ---
st.markdown("""
---
💡 **Want to share your experience or need support?**  
📧 Reach out to us at [loopbreakermd@gmail.com](mailto:loopbreakermd@gmail.com) – we’d love to hear from you!

---
### 🚀 Unlock Your Mind with LoopBreakerMD! 🚀

Are you ready to break free from mental clutter and gain true clarity?  
**LoopBreakerMD** offers innovative tools and expert guidance to help you:
- Tag and track your thoughts for deeper self-awareness
- Identify patterns and triggers that shape your wellbeing
- Build habits for a calmer, more focused mind

Join a growing community dedicated to mental clarity and emotional growth.  
Take the first step—reach out today and discover how LoopBreakerMD can help you restore balance and thrive!

🌐 loopbreakermd@gmail.com
---
""")

# --- Data Storage Notes ---
st.caption("🗂️ Your thoughts are saved locally in 'thought_logs.csv'. For cloud/Google Sheets integration, contact loopbreakermd@gmail.com.")
