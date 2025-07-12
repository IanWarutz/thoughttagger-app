import streamlit as st
import pandas as pd
import datetime
import random
import re

st.set_page_config(page_title="🏷️ Thought Tagger", page_icon="🏷️", layout="centered")
st.title("🏷️ Thought Tagger – Build Emotional Clarity with Tags")

# --- Tag definitions with medically approved tips ---
tag_info = {
    "anxiety": {
        "keywords": ["worry", "nervous", "anxious", "panic", "afraid", "scared", "fear", "uneasy", "apprehensive"],
        "explanation": "This thought reflects anxiety or fear.",
        "tip": "Try slow, deep breathing, grounding exercises, or progressive muscle relaxation. If anxiety persists, consider reaching out to a mental health professional."
    },
    "sadness": {
        "keywords": ["sad", "down", "unhappy", "depressed", "cry", "hopeless", "tearful", "blue", "failure", "failed"],
        "explanation": "This thought reflects sadness or low mood.",
        "tip": "Acknowledge your feelings and talk to someone you trust. Engage in activities you usually enjoy, and seek professional support if sadness is persistent."
    },
    "self-doubt": {
        "keywords": ["doubt", "uncertain", "insecure", "not sure", "worthless", "inadequate", "failure", "can't", "useless"],
        "explanation": "This thought reflects self-doubt or low self-esteem.",
        "tip": "Challenge negative self-talk with evidence from your achievements. Practice self-compassion and consider cognitive behavioral strategies."
    },
    "anger": {
        "keywords": ["angry", "mad", "furious", "annoyed", "rage", "irritated", "resentful"],
        "explanation": "This thought reflects anger or frustration.",
        "tip": "Pause and take deep breaths. Express your feelings assertively, not aggressively. Physical activity can help release tension."
    },
    "stress": {
        "keywords": ["stress", "overwhelmed", "pressure", "tense", "burnout", "exhausted"],
        "explanation": "This thought reflects stress or overwhelm.",
        "tip": "Prioritize tasks, take regular breaks, and practice relaxation techniques. If stress is chronic, seek support from a healthcare provider."
    },
    "gratitude": {
        "keywords": ["thank", "grateful", "appreciate", "blessed", "fortunate"],
        "explanation": "This thought expresses gratitude.",
        "tip": "Keep a gratitude journal and regularly reflect on positive aspects of your life. Gratitude is linked to improved mental health."
    },
    "joy": {
        "keywords": ["happy", "joy", "excited", "delight", "pleased", "content", "elated", "cheerful"],
        "explanation": "This thought reflects happiness or joy.",
        "tip": "Share your positive feelings with others and savor the moment. Positive emotions can boost resilience."
    },
    "love": {
        "keywords": ["love", "affection", "care", "fond", "cherish", "adore"],
        "explanation": "This thought is about love or connection.",
        "tip": "Nurture your relationships and express appreciation to loved ones. Social support is vital for wellbeing."
    },
    "calm": {
        "keywords": ["calm", "peace", "relaxed", "serene", "tranquil", "at ease"],
        "explanation": "This thought reflects calmness or peace.",
        "tip": "Maintain your relaxation routines, such as mindfulness or gentle exercise, to support ongoing wellbeing."
    },
    "goals": {
        "keywords": ["goal", "plan", "future", "ambition", "dream", "aspire", "objective"],
        "explanation": "This thought is focused on goals or aspirations.",
        "tip": "Set realistic, achievable goals and break them into steps. Celebrate progress and adjust plans as needed."
    },
    "reflection": {
        "keywords": ["reflect", "reflection", "insight", "aware", "awareness", "mindful", "mindfulness", "learned"],
        "explanation": "This thought shows self-reflection or insight.",
        "tip": "Regular self-reflection can foster growth. Journaling or talking with a counselor can deepen your insights."
    },
    "growth": {
        "keywords": ["growth", "improve", "progress", "develop", "learn", "change", "better"],
        "explanation": "This thought is about personal growth.",
        "tip": "Embrace challenges as opportunities to learn. Track your progress and seek feedback for continued development."
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

# --- Improved Auto Tagging Logic ---
def assign_auto_tag(thought):
    thought_lower = thought.lower()
    tag_scores = {}
    for tag, info in tag_info.items():
        score = sum(1 for kw in info["keywords"] if re.search(r'\b' + re.escape(kw) + r'\b', thought_lower))
        if score > 0:
            tag_scores[tag] = score
    if tag_scores:
        # Return the tag with the highest keyword match count
        return max(tag_scores, key=tag_scores.get)
    # fallback: reflection
    return "reflection"

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
            st.session_state.thought_data.append({
                "thought": thought.strip(),
                "tags": tag_list,
                "auto_tag": auto_tag,
                "time": timestamp,
                "date": today.isoformat(),
                "user": st.session_state.demographics['profession']
            })
            info = tag_info.get(auto_tag, {"explanation": "No info.", "tip": ""})
            st.success(
                f"Thought tagged and saved! (Auto-tag: **{auto_tag}**)\n\n"
                f"**Why this tag?** {info['explanation']}\n\n"
                f"**Medical Tip:** {info['tip']}"
            )

# --- Review Tagged Thoughts ---
if st.session_state.thought_data:
    st.header("📂 Review Your Tagged Thoughts")
    all_tags = sorted({tag for entry in st.session_state.thought_data for tag in entry["tags"]})
    selected_tag = st.selectbox("Filter by tag", options=["All"] + all_tags)
    filtered = st.session_state.thought_data if selected_tag == "All" else [
        entry for entry in st.session_state.thought_data if selected_tag in entry["tags"]
    ]
    for entry in filtered:
        info = tag_info.get(entry["auto_tag"], {"explanation": "", "tip": ""})
        st.markdown(
            f"- **{entry['time']}**: {entry['thought']}  \n"
            f"  _Tags: {', '.join(entry['tags'])}_  \n"
            f"  _User: {entry['user']}_  \n"
            f"  _Auto-tag: {entry['auto_tag']} – {info['explanation']}  \n"
            f"  _Medical Tip: {info['tip']}_"
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
