import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="🏷️ Thought Tagger", page_icon="🏷️", layout="centered")

st.title("🏷️ Thought Tagger – Build Emotional Clarity with Tags")

# --- What is Thought Tagging? ---
st.markdown("""
### What is Thought Tagging?
Thought tagging is the practice of writing down your thoughts and attaching descriptive tags (like 'anxiety', 'gratitude', 'goals', or 'self-doubt') to each one.  
This simple act helps you:
- **Restore inner chaos:** By labeling your thoughts, you externalize and organize them, making them less overwhelming.
- **Gain clarity:** Tagging helps you recognize patterns, triggers, and recurring themes in your thinking.
- **Foster self-awareness:** Over time, you’ll see which thoughts dominate your mind, empowering you to make positive changes.
- **Support emotional wellbeing:** Understanding your thought patterns is a key step toward emotional regulation and mental clarity.
""")

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

# --- Thought Tagging Section ---
st.header("📝 Add a Thought and Tag It")
with st.form("thought_form", clear_on_submit=True):
    thought = st.text_area("Enter your thought")
    tags = st.text_input("Enter tags for this thought (comma-separated, e.g., anxiety, gratitude, goals)")
    submitted = st.form_submit_button("Add Thought")
    if submitted:
        if not thought.strip() or not tags.strip():
            st.error("Please enter both a thought and at least one tag.")
        else:
            tag_list = [tag.strip().lower() for tag in tags.split(",") if tag.strip()]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.thought_data.append({
                "thought": thought.strip(),
                "tags": tag_list,
                "time": timestamp,
                "date": today.isoformat()
            })
            st.success("Thought tagged and saved!")

# --- Review Tagged Thoughts ---
if st.session_state.thought_data:
    st.header("📂 Review Your Tagged Thoughts")
    all_tags = sorted({tag for entry in st.session_state.thought_data for tag in entry["tags"]})
    selected_tag = st.selectbox("Filter by tag", options=["All"] + all_tags)
    filtered = st.session_state.thought_data if selected_tag == "All" else [
        entry for entry in st.session_state.thought_data if selected_tag in entry["tags"]
    ]
    for entry in filtered:
        st.markdown(f"- **{entry['time']}**: {entry['thought']}  \n  _Tags: {', '.join(entry['tags'])}_")

    # Show daily progress
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
