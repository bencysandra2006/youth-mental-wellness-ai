import os

# Toggle between dummy and real mode
USE_DUMMY_AI = True  # ✅ Change to False if you enable Google Cloud billing later

if not USE_DUMMY_AI:
    from google.cloud import aiplatform
    from vertexai.generative_models import GenerativeModel, SafetySetting

    PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    LOCATION = os.getenv("GCP_LOCATION", "asia-south1")
    MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    SYSTEM_PROMPT = (
        "You are 'Ujjwal', a kind, non-judgmental wellness companion for Indian youth. "
        "Goals: listen, validate, suggest simple coping (breathing, journaling, movement, "
        "positive reframing), and encourage seeking trusted people or professional help when appropriate. "
        "No diagnoses or medical advice. Use short, supportive paragraphs and simple language."
    )

    def _init():
        aiplatform.init(project=PROJECT_ID, location=LOCATION)
    _init()

    SAFETY_SETTINGS = [
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                      threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                      threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                      threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                      threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
    ]

    _model = GenerativeModel(MODEL)

    COACH_STYLE = {
        "😊 Good": "Celebrate the positives, encourage gratitude or sharing good news.",
        "😐 Okay": "Gently explore what's on their mind, suggest small self-care steps.",
        "😟 Stressed": "Offer grounding/breathing, chunk tasks, reassure it's okay to seek help.",
        "😢 Low": "Validate feelings, suggest small compassionate actions, encourage reaching out.",
    }

    BREATHING = "Try box breathing: inhale 4, hold 4, exhale 4, hold 4 — repeat 4 times."

    def generate_supportive_reply(user_input: str, mood: str, crisis: bool) -> str:
        style = COACH_STYLE.get(mood, "Offer gentle support.")
        crisis_line = (
            "If the user sounds in crisis, recommend contacting trusted people or emergency services."
            if crisis else ""
        )
        prompt = f"""{SYSTEM_PROMPT}
User mood: {mood}
Coaching focus: {style}
{crisis_line}
User message: {user_input}
Respond in 120-180 words max with supportive language.
"""
        resp = _model.generate_content(prompt, safety_settings=SAFETY_SETTINGS)
        return resp.text.strip() if hasattr(resp, "text") else "I'm here for you."

else:
    # Dummy AI mode (no Google Cloud needed)
    def generate_supportive_reply(user_input: str, mood: str, crisis: bool) -> str:
        if crisis:
            return ("💚 It sounds like you’re in deep distress. "
                "Please reach out to a trusted friend, a family member, "
                "or call your local helpline immediately. You are not alone.")
    
        mood_responses = {
            "😊 Good": "💚 I’m glad to hear that! Take a moment to celebrate this feeling. "
                   "Maybe share something positive with a friend, or write it down in a gratitude journal.",
            "😐 Okay": "💚 Thanks for checking in. It seems like you’re doing alright. "
                   "Sometimes a short walk, listening to music, or talking to someone you trust can lift your mood.",
            "😟 Stressed": "💚 I hear that you’re feeling stressed. Try box breathing — inhale 4, hold 4, exhale 4, hold 4. "
                       "Or break your tasks into smaller steps and take short breaks between them.",
            "😢 Low": "💚 I’m sorry you’re feeling low. Be kind to yourself today — maybe try journaling, "
                  "listening to calming music, or reaching out to someone you trust."
     }

        return mood_responses.get(mood, "💚 I’m here for you. Take things one step at a time.")

