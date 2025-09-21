import os
import uuid
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

from vertex_client import generate_supportive_reply
from safety import screen_text, is_crisis
from storage import save_log_optional

load_dotenv()

st.set_page_config(page_title="Youth Mental Wellness AI", page_icon="💚", layout="centered")

st.markdown("""
# 💚 Youth Mental Wellness AI
A confidential, empathetic companion powered by Google Cloud Vertex AI.

> This is not medical advice. If you're in immediate danger, please contact local emergency services.
""")

# Anonymous session id (no PII)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Lightweight mood check-in
mood = st.radio("How are you feeling right now?", ["😊 Good", "😐 Okay", "😟 Stressed", "😢 Low"], horizontal=True)

# Chat input
user_input = st.text_area("Share what's on your mind (confidential)", height=120, placeholder="You can write in English or Hinglish.")

if st.button("Get Support"):
    if not user_input.strip():
        st.warning("Please write a short message.")
        st.stop()

    # Safety screen
    screen_result = screen_text(user_input)
    if screen_result.blocked:
        st.error("Sorry, I can't continue with this content. Try rephrasing or keep it non-harmful.")
        st.stop()

    crisis_flag, crisis_reason = is_crisis(user_input)

    # Generate AI reply
    with st.spinner("Thinking..."):
        reply = generate_supportive_reply(user_input=user_input, mood=mood, crisis=crisis_flag)

    # Display
    st.markdown("### Ujjwal")
    st.write(reply)

    if crisis_flag:
        st.info("""
        **If you feel unsafe right now:** Consider reaching out to a trusted adult, friend, or local emergency services.  
        You may also contact national/local helplines available in your area for immediate support.
        """)

    # Optional anonymized log
    save_log_optional(
        session_id=st.session_state.session_id,
        mood=mood,
        user_input=user_input,
        ai_reply=reply,
        crisis=crisis_flag,
        screened=screen_result.model,
    )
