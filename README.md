# 🎯 TalentPulse

### AI-Powered Talent Scouting & Engagement Agent

**Catalyst Hackathon 2025 | Built for Deccan AI**

---

## 🚀 Overview

**TalentPulse** is not just another recruitment tool — it’s an intelligent hiring assistant that thinks, evaluates, and engages like a recruiter.

Paste a Job Description, and the system will:

* 🔍 Discover the best-fit candidates
* 💬 Simulate real recruiter-candidate conversations
* ❤️ Measure genuine interest using sentiment analysis
* 📊 Deliver a ranked shortlist with clear insights

All of this — **without relying on external APIs**.

---

## 🌐 Live Demo

👉 https://deccan-talent-ai-agent.streamlit.app

---

## ✨ What Makes TalentPulse Special?

### 🧠 Smart JD Understanding

* Extracts **Must-Have & Good-to-Have skills**
* Detects hidden signals like urgency & company culture
* Infers **skill relationships** (e.g., FastAPI → Python)
* Identifies role type, experience, and work mode

---

### 🎯 Intelligent Candidate Matching

* Uses **TF-IDF + cosine similarity** for precision
* Prioritizes **Must-Have skills** intelligently
* Explains every match with:

  * ✅ Strengths
  * ⚠️ Gaps

---

### 💬 AI-Powered Engagement

* Simulates real conversations:

  * Outreach → Response → Follow-up → Final reply
* Calculates **Interest Score** from:

  * Sentiment
  * Keywords
  * Expression level
* Generates **human-like summaries**

---

### 📊 Insightful Ranking System

* Combines **Match Score + Interest Score**
* Flags risks 🚩 and suggests recruiter actions
* Produces a **ready-to-use shortlist**

---

### 📈 Visual Intelligence

* Interactive **Match vs Interest scatter plot**
* Quickly spot:

  * 🔥 High-potential candidates
  * ⚠️ Risky profiles

---

### 🎛 Real-Time Control

* Adjust weights dynamically
* Instantly re-rank candidates

---

### 🔎 Smart Filtering

* Filter by:

  * Location
  * Experience

---

### 📦 Export Ready

* Download structured **JSON reports** for further use

---

## 📐 Scoring System (Simplified)

### 🟢 Match Score (0–100)

* Skill Similarity → 70 pts
* Experience Match → 20 pts
* Seniority Fit → 10 pts

---

### 🔵 Interest Score (0–100)

* Sentiment → 70 pts
* Keywords → ±20 pts
* Expression Level → 10 pts

---

### 🏆 Final Score

```
Final Score = (Match × 0.6) + (Interest × 0.4)
```

⚙️ Fully adjustable in UI

---

## 🏗 Architecture

```
TalentPulse Engine
│
├── Job Parser
├── Candidate Matcher
├── Outreach Simulator
└── Ranking Engine
```

---

## 🛠 Tech Stack

| Layer         | Technology                 |
| ------------- | -------------------------- |
| Frontend      | Streamlit + Custom Dark UI |
| Visualization | Plotly                     |
| Matching      | Scikit-learn               |
| Sentiment     | TextBlob                   |
| Data          | Pandas + NumPy             |
| Database      | Mock CSV (31 profiles)     |

---

## 📁 Project Structure

```
talent-scout-agent/
│
├── app.py              # Streamlit UI
├── engine.py           # Core logic
├── data.py             # Candidate generator
├── mock_candidates.csv # Dataset
├── requirements.txt    # Dependencies
└── README.md
```

---

## ⚙️ Setup Guide

```bash
# Clone repo
git clone https://github.com/your-repo/talent-scout-agent.git
cd talent-scout-agent

# Install dependencies
pip install -r requirements.txt

# (Optional) Regenerate dataset
python data.py

# Run the app
streamlit run app.py
```

👉 Open: http://localhost:8501

---

## 🧪 Example

### Input

> Senior Data Scientist (5+ years)
> Skills: Python, ML, NLP, Pandas, Scikit-Learn

---

### Output

| Rank | Name               | Role              | Match | Interest | Final |
| ---- | ------------------ | ----------------- | ----- | -------- | ----- |
| 🥇   | Ravi Krishnamurthy | Sr Data Scientist | 82.4  | 88.0     | 84.7  |
| 🥈   | Amit Kumar         | Data Scientist    | 74.1  | 76.5     | 75.1  |
| 🥉   | Sneha Reddy        | ML Engineer       | 61.3  | 57.0     | 59.6  |

---

## 👤 Author

**Karthik Reddy**
Built with passion for **Catalyst Hackathon 2025 — Deccan AI**

---

## 💡 Final Thought

TalentPulse doesn’t just find candidates —
it identifies **who is both capable AND genuinely interested**.

That’s the difference between hiring…
and hiring right. 🚀
