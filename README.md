# 💚 Youth Mental Wellness AI

An empathetic AI companion prototype for youth mental wellness, built for the GenAI Exchange Hackathon 2025.  

## 🌍 Problem
Youth in India face stigma around mental health and lack access to timely support. Early intervention is often missing.

## 💡 Solution
Youth Mental Wellness AI provides:
- Mood check-ins (😊, 😐, 😟, 😢)
- Supportive AI responses
- Crisis detection & safe escalation
- Anonymous usage (no personal data stored)
- Scalable deployment on Google Cloud Vertex AI & Cloud Run

## ⚙️ Tech Stack
- **Frontend**: Streamlit (Python)
- **AI Engine**: Vertex AI Gemini (Dummy AI fallback for demo)
- **Safety**: Custom keyword checks + Vertex AI Safety Settings
- **Storage (Optional)**: Firestore (anonymized logs)
- **Deployment**: Docker + Cloud Run
- **Collaboration**: GitHub

## 🚀 Run Locally
```bash
git clone https://github.com/USERNAME/youth-mental-wellness-ai.git
cd youth-mental-wellness-ai
pip install -r requirements.txt
streamlit run app.py
