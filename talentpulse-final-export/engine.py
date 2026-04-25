import re
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import numpy as np

# ─────────────────────────────────────────────
# Comprehensive skill taxonomy for JD parsing
# ─────────────────────────────────────────────
SKILL_TAXONOMY = {
    "languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "go", "rust",
        "ruby", "scala", "kotlin", "swift", "r", "matlab", "php", "perl"
    ],
    "frontend": [
        "react", "vue", "angular", "next.js", "nuxt.js", "svelte", "html", "css",
        "sass", "tailwind", "redux", "webpack", "vite", "graphql"
    ],
    "backend": [
        "django", "fastapi", "flask", "spring boot", "express", "node.js", "nestjs",
        "ruby on rails", "asp.net", "laravel", "grpc", "rest api", "microservices"
    ],
    "data": [
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "snowflake", "bigquery", "spark", "airflow", "kafka", "dbt"
    ],
    "ml_ai": [
        "machine learning", "deep learning", "nlp", "computer vision", "pytorch",
        "tensorflow", "scikit-learn", "pandas", "numpy", "hugging face",
        "llm", "rag", "langchain", "mlops", "data science"
    ],
    "cloud_devops": [
        "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ansible",
        "jenkins", "ci/cd", "linux", "networking", "prometheus", "grafana"
    ],
    "soft": [
        "agile", "scrum", "kanban", "leadership", "communication", "problem solving",
        "teamwork", "mentoring", "project management", "jira"
    ]
}

ALL_SKILLS = [skill for category in SKILL_TAXONOMY.values() for skill in category]

SYNONYM_MAP = {
    "spring boot": ["java", "backend"], "django": ["python", "backend"],
    "fastapi": ["python", "backend"], "flask": ["python", "backend"],
    "react": ["javascript", "frontend"], "next.js": ["react", "javascript"],
    "vue": ["javascript", "frontend"], "angular": ["typescript", "frontend"],
    "node.js": ["javascript", "backend"], "express": ["node.js", "javascript"],
    "pytorch": ["python", "deep learning"], "tensorflow": ["python", "deep learning"],
    "scikit-learn": ["python", "machine learning"], "pandas": ["python", "data science"],
    "kubernetes": ["docker", "cloud_devops"], "terraform": ["cloud_devops"],
    "spark": ["python", "data engineering"], "airflow": ["python", "data engineering"],
    "docker": ["devops"], "aws": ["cloud"], "gcp": ["cloud"], "azure": ["cloud"],
}

SENIORITY_MAP = {
    "intern": 0, "junior": 1, "associate": 2, "mid": 3, "senior": 4,
    "lead": 5, "principal": 6, "staff": 6, "architect": 7, "director": 8, "vp": 9
}

URGENCY_KEYWORDS = ["asap", "immediately", "urgent", "fast-paced", "rapidly growing", "high priority", "critical hire"]
CULTURE_KEYWORDS = {
    "startup": ["startup", "fast-paced", "scrappy", "wear many hats", "entrepreneurial"],
    "enterprise": ["enterprise", "fortune 500", "large-scale", "global team", "established"],
    "collaborative": ["collaborative", "cross-functional", "team-oriented", "open culture"],
    "innovative": ["innovative", "cutting-edge", "state-of-the-art", "r&d", "research"],
}

CITIES = [
    "bengaluru", "bangalore", "hyderabad", "mumbai", "delhi", "pune", "chennai",
    "kolkata", "noida", "gurgaon", "gurugram", "ahmedabad", "kochi", "jaipur",
    "new york", "san francisco", "london", "berlin", "singapore", "dubai", "remote"
]


# ─────────────────────────────────────────────
# Job Parser
# ─────────────────────────────────────────────
class JobParser:
    def parse_jd(self, jd_text: str) -> dict:
        jd_lower = jd_text.lower()

        # 1. Extract skills + categories
        extracted_skills, skill_categories = [], {}
        for category, skills in SKILL_TAXONOMY.items():
            matched = []
            for skill in skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', jd_lower):
                    extracted_skills.append(skill)
                    matched.append(skill)
            if matched:
                skill_categories[category] = matched

        # 2. Synonym expansion
        inferred_skills = set()
        for skill in extracted_skills:
            for synonym in SYNONYM_MAP.get(skill, []):
                if synonym not in extracted_skills:
                    inferred_skills.add(synonym)

        # 3. Must-have vs good-to-have
        must_have, good_to_have = [], []
        bonus_patterns = r'(?:plus|bonus|preferred|nice to have|good to have|familiarity|optional)'
        required_patterns = r'(?:must|required|essential|core|mandatory|need)'
        sentences = re.split(r'[.\n]', jd_lower)
        for sent in sentences:
            for skill in extracted_skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', sent):
                    if re.search(bonus_patterns, sent):
                        if skill not in good_to_have:
                            good_to_have.append(skill)
                    elif re.search(required_patterns, sent) or skill not in good_to_have:
                        if skill not in must_have:
                            must_have.append(skill)
        # Skills not classified go to must-have
        for s in extracted_skills:
            if s not in must_have and s not in good_to_have:
                must_have.append(s)

        # 4. Experience
        exp_match = re.search(r'(\d+)\+?\s*(?:–|-|to)?\s*(\d+)?\s*years?', jd_lower)
        exp_min = int(exp_match.group(1)) if exp_match else 0
        exp_max = int(exp_match.group(2)) if exp_match and exp_match.group(2) else (exp_min + 2 if exp_min else 0)

        # 5. Seniority
        seniority, seniority_level = "mid", 3
        for level in SENIORITY_MAP:
            if re.search(r'\b' + level + r'\b', jd_lower):
                seniority, seniority_level = level, SENIORITY_MAP[level]
                break

        # 6. Role type
        role_keywords = {
            "software-engineer": ["software engineer", "swe", "software developer"],
            "data-scientist": ["data scientist", "machine learning engineer", "ml engineer"],
            "frontend-developer": ["frontend", "front-end", "ui developer"],
            "backend-developer": ["backend", "back-end", "server-side"],
            "devops-engineer": ["devops", "sre", "platform engineer", "cloud engineer"],
            "data-engineer": ["data engineer", "data pipeline", "etl"],
            "fullstack-developer": ["fullstack", "full-stack", "full stack"],
        }
        detected_role = "general"
        for role, keywords in role_keywords.items():
            if any(kw in jd_lower for kw in keywords):
                detected_role = role
                break

        # 7. Location / Work mode
        location, work_mode = "Not specified", "Not specified"
        for city in CITIES:
            if city in jd_lower:
                location = city.title()
                break
        if "remote" in jd_lower:
            work_mode = "Remote"
        elif "hybrid" in jd_lower:
            work_mode = "Hybrid"
        elif "onsite" in jd_lower or "on-site" in jd_lower or "office" in jd_lower:
            work_mode = "Onsite"

        # 8. Hidden signals
        urgency = any(kw in jd_lower for kw in URGENCY_KEYWORDS)
        culture_signals = []
        for culture_type, keywords in CULTURE_KEYWORDS.items():
            if any(kw in jd_lower for kw in keywords):
                culture_signals.append(culture_type)

        # 9. Soft skills
        soft_skills = skill_categories.get("soft", [])

        return {
            "role_title": detected_role.replace("-", " ").title(),
            "role_type": detected_role,
            "skills": extracted_skills,
            "must_have_skills": must_have,
            "good_to_have_skills": good_to_have,
            "inferred_skills": list(inferred_skills),
            "skill_categories": skill_categories,
            "experience_min": exp_min,
            "experience_max": exp_max,
            "seniority": seniority,
            "seniority_level": seniority_level,
            "location": location,
            "work_mode": work_mode,
            "soft_skills": soft_skills,
            "hidden_signals": {
                "urgency": urgency,
                "culture_fit": culture_signals,
                "domain_preference": detected_role,
            },
            "raw_text": jd_text
        }


# ─────────────────────────────────────────────
# Matcher
# ─────────────────────────────────────────────
class Matcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))

    def calculate_match_scores(self, jd_req: dict, df: pd.DataFrame) -> pd.Series:
        jd_skills = jd_req["skills"]
        jd_doc = " ".join(jd_skills)
        if not jd_doc.strip():
            return pd.Series([0.0] * len(df))

        candidate_docs = df["Skills"].apply(
            lambda x: x.lower().replace(",", " ") if isinstance(x, str) else ""
        ).tolist()
        all_docs = [jd_doc] + candidate_docs
        tfidf_matrix = self.vectorizer.fit_transform(all_docs)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Weighted skill overlap (0-50)
        must_have = set(s.lower() for s in jd_req.get("must_have_skills", jd_skills))
        good_to_have = set(s.lower() for s in jd_req.get("good_to_have_skills", []))
        skill_scores = np.zeros(len(df))
        for i, (_, row) in enumerate(df.iterrows()):
            c_skills = set(s.strip().lower() for s in str(row.get("Skills", "")).split(","))
            must_hits = len(must_have & c_skills)
            good_hits = len(good_to_have & c_skills)
            total_must = max(len(must_have), 1)
            total_good = max(len(good_to_have), 1)
            skill_scores[i] = (must_hits / total_must) * 35 + (good_hits / total_good) * 10
            skill_scores[i] += cosine_sim[i] * 5  # TF-IDF bonus

        # Experience (0-20)
        req_min = jd_req.get("experience_min", 0)
        exp_scores = np.zeros(len(df))
        for i, (_, row) in enumerate(df.iterrows()):
            cand_exp = row.get("Experience", 0)
            if req_min == 0:
                exp_scores[i] = 15
            elif cand_exp >= req_min:
                exp_scores[i] = 20
            else:
                exp_scores[i] = max(0, 20 - (req_min - cand_exp) * 4)

        # Seniority alignment (0-10)
        req_sen = jd_req.get("seniority_level", 3)
        sen_scores = np.zeros(len(df))
        for i, (_, row) in enumerate(df.iterrows()):
            role_text = str(row.get("Role", "")).lower()
            best = 3
            for level, val in SENIORITY_MAP.items():
                if level in role_text:
                    best = val
                    break
            sen_scores[i] = max(0, 10 - abs(req_sen - best) * 2)

        # Domain alignment (0-10)
        domain_scores = np.zeros(len(df))
        role_type = jd_req.get("role_type", "general")
        domain_keywords = {
            "software-engineer": ["software", "engineer", "developer", "swe"],
            "data-scientist": ["data scientist", "ml", "machine learning", "ai"],
            "frontend-developer": ["frontend", "front-end", "ui", "react"],
            "backend-developer": ["backend", "back-end", "server"],
            "devops-engineer": ["devops", "sre", "cloud", "platform"],
            "data-engineer": ["data engineer", "etl", "pipeline"],
            "fullstack-developer": ["fullstack", "full-stack", "full stack"],
        }
        kws = domain_keywords.get(role_type, [])
        for i, (_, row) in enumerate(df.iterrows()):
            role_lower = str(row.get("Role", "")).lower()
            if any(kw in role_lower for kw in kws):
                domain_scores[i] = 10
            elif any(kw in str(row.get("Skills", "")).lower() for kw in kws[:2]):
                domain_scores[i] = 5

        # Location compatibility (0-10)
        loc_scores = np.full(len(df), 7.0)  # default neutral
        jd_loc = jd_req.get("location", "Not specified").lower()
        if jd_loc != "not specified":
            for i, (_, row) in enumerate(df.iterrows()):
                c_loc = str(row.get("Location", "")).lower()
                if jd_loc in c_loc or c_loc in jd_loc:
                    loc_scores[i] = 10
                else:
                    loc_scores[i] = 5

        total = skill_scores + exp_scores + sen_scores + domain_scores + loc_scores
        return pd.Series(np.round(np.clip(total, 0, 100), 2))

    def extract_matched_skills(self, jd_req: dict, candidate_skills_str: str) -> str:
        if not isinstance(candidate_skills_str, str):
            return "None"
        c_skills = [s.strip().lower() for s in candidate_skills_str.split(",")]
        matched = [s for s in jd_req["skills"] if s in c_skills]
        return ", ".join(matched) if matched else "None"

    def get_strengths_and_gaps(self, jd_req: dict, row: pd.Series) -> dict:
        c_skills = set(s.strip().lower() for s in str(row.get("Skills", "")).split(","))
        must_have = set(s.lower() for s in jd_req.get("must_have_skills", jd_req["skills"]))
        good_to_have = set(s.lower() for s in jd_req.get("good_to_have_skills", []))

        matched_must = must_have & c_skills
        matched_good = good_to_have & c_skills
        missing_must = must_have - c_skills
        missing_good = good_to_have - c_skills

        strengths = []
        if matched_must:
            strengths.append(f"Covers {len(matched_must)}/{len(must_have)} must-have skills: {', '.join(sorted(matched_must))}")
        cand_exp = row.get("Experience", 0)
        req_exp = jd_req.get("experience_min", 0)
        if req_exp and cand_exp >= req_exp:
            strengths.append(f"{cand_exp} yrs experience (meets {req_exp}+ requirement)")
        if matched_good:
            strengths.append(f"Bonus skills: {', '.join(sorted(matched_good))}")

        gaps = []
        if missing_must:
            gaps.append(f"Missing must-have: {', '.join(sorted(missing_must))}")
        if req_exp and cand_exp < req_exp:
            gaps.append(f"Experience gap: has {cand_exp} yrs, needs {req_exp}+")
        if missing_good:
            gaps.append(f"Missing nice-to-have: {', '.join(sorted(missing_good))}")

        return {"strengths": strengths, "gaps": gaps}

    def generate_explanation(self, jd_req: dict, row: pd.Series) -> str:
        sg = self.get_strengths_and_gaps(jd_req, row)
        lines = []
        for s in sg["strengths"][:2]:
            lines.append(f"✅ {s}")
        for g in sg["gaps"][:2]:
            lines.append(f"⚠️ {g}")
        lines.append(f"📋 Current: {row.get('Role', 'N/A')} @ {row.get('Current Company', 'N/A')}")
        return " · ".join(lines)


# ─────────────────────────────────────────────
# Outreach Simulator (Multi-turn)
# ─────────────────────────────────────────────
class OutreachSimulator:
    OUTREACH_TEMPLATES = [
        "Hi {name}, we came across your profile and think you'd be a great fit for a {role_type} role. Your experience in {skills} really stands out. Are you open to a quick chat?",
        "Hello {name}! Your background in {skills} caught our eye. We have an exciting {role_type} opportunity — would you be interested in learning more?",
        "Hey {name}, we're building something great and your experience aligns perfectly. Would love to tell you more about this {role_type} position!",
    ]

    FOLLOWUP_TEMPLATES = [
        "That's great to hear, {name}! Just to confirm — are you available for a call this week? Also, what's your current notice period like?",
        "Wonderful, {name}! Could you share your availability for an initial discussion? We'd also love to know if you're open to {work_mode} work.",
        "Thanks for your response, {name}! To move forward, could you let us know your availability window and ideal start timeline?",
    ]

    def generate_outreach(self, name: str, skills: str, role_type: str) -> str:
        top_skills = ", ".join(skills.split(",")[:2]).strip()
        template = self.OUTREACH_TEMPLATES[hash(name) % len(self.OUTREACH_TEMPLATES)]
        return template.format(name=name.split()[0], skills=top_skills, role_type=role_type.replace("-", " "))

    def generate_followup(self, name: str, work_mode: str = "flexible") -> str:
        template = self.FOLLOWUP_TEMPLATES[hash(name + "follow") % len(self.FOLLOWUP_TEMPLATES)]
        return template.format(name=name.split()[0], work_mode=work_mode)

    def build_conversation(self, row: pd.Series, role_type: str, work_mode: str = "flexible") -> list:
        name = str(row["Name"])
        skills = str(row.get("Skills", ""))
        response1 = str(row.get("Response", "")) if pd.notna(row.get("Response")) else ""
        response2 = str(row.get("Response2", "")) if pd.notna(row.get("Response2")) else ""

        convo = [
            {"role": "recruiter", "message": self.generate_outreach(name, skills, role_type)},
        ]
        if response1:
            convo.append({"role": "candidate", "message": response1})
            if "pass" not in response1.lower() and "not looking" not in response1.lower():
                convo.append({"role": "recruiter", "message": self.generate_followup(name, work_mode)})
                if response2:
                    convo.append({"role": "candidate", "message": response2})
        return convo

    def generate_conversation_summary(self, convo, name: str) -> str:
        if not isinstance(convo, list):
            return f"{name}: No conversation data."
        turns = len(convo)
        candidate_msgs = [str(t["message"]) for t in convo if t["role"] == "candidate" and t.get("message")]
        if not candidate_msgs:
            return f"{name}: No response received."
        last = str(candidate_msgs[-1]).lower()
        if any(kw in last for kw in ["not looking", "pass", "no thanks"]):
            tone = "declined"
        elif any(kw in last for kw in ["excited", "thrilled", "love", "absolutely", "definitely"]):
            tone = "highly enthusiastic"
        elif any(kw in last for kw in ["interested", "open", "curious", "explore"]):
            tone = "interested"
        else:
            tone = "neutral"
        snippet = str(candidate_msgs[-1])[:80]
        return f"{name}: {turns}-turn exchange. Candidate tone: {tone}. Last signal: \"{snippet}...\""

    def compute_interest_score(self, response_text) -> float:
        if response_text is None or (isinstance(response_text, float) and pd.isna(response_text)) or str(response_text).strip() == "":
            return 30.0
        blob = TextBlob(str(response_text))
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        base = ((polarity + 1.0) / 2.0) * 70

        positive_kw = ["excited", "thrilled", "love", "interested", "absolutely", "definitely",
                        "asap", "schedule", "calendar", "yes", "great fit", "perfect", "looking forward"]
        negative_kw = ["not looking", "pass", "no thanks", "happy where", "not interested", "maybe", "depends"]
        resp_lower = str(response_text).lower()
        pos_hits = sum(1 for kw in positive_kw if kw in resp_lower)
        neg_hits = sum(1 for kw in negative_kw if kw in resp_lower)
        keyword_bonus = min(20, pos_hits * 5) - min(20, neg_hits * 8)
        subjectivity_bonus = subjectivity * 10

        total = base + keyword_bonus + subjectivity_bonus
        return round(float(np.clip(total, 0, 100)), 2)

    def compute_multi_turn_interest(self, row: pd.Series) -> float:
        r1_raw = row.get("Response", "")
        r2_raw = row.get("Response2", "")
        r1 = str(r1_raw) if pd.notna(r1_raw) else ""
        r2 = str(r2_raw) if pd.notna(r2_raw) else ""
        s1 = self.compute_interest_score(r1)
        has_r2 = bool(r2 and r2.strip() and r2 != "nan")
        s2 = self.compute_interest_score(r2) if has_r2 else s1
        return round(s1 * 0.4 + s2 * 0.6, 2) if has_r2 else s1

    def flag_risk(self, match_score: float, interest_score: float) -> str:
        if match_score >= 65 and interest_score < 40:
            return "⚠️ High match, low interest — passive candidate"
        if match_score < 35 and interest_score >= 65:
            return "🔸 Low match, high interest — potential misfit"
        if interest_score < 30:
            return "🔴 Disengaged — unlikely to convert"
        return ""

    def recommend_action(self, match_score: float, interest_score: float, availability: str) -> str:
        if match_score >= 60 and interest_score >= 60:
            return "🟢 Fast-track: Schedule interview immediately"
        if match_score >= 60 and interest_score >= 40:
            return "🟡 Nurture: Send detailed role brief, follow up in 3 days"
        if match_score >= 60 and interest_score < 40:
            return "🟠 Re-engage: Try alternative outreach channel (LinkedIn/referral)"
        if match_score >= 40:
            return "🔵 Keep warm: Add to talent pipeline for future roles"
        return "⚪ Deprioritize: Low alignment, focus efforts elsewhere"

    def generate_final_ranking(self, df: pd.DataFrame, match_w: float = 0.6, interest_w: float = 0.4) -> pd.DataFrame:
        df = df.copy()
        df["Final Score"] = (df["Match Score"] * match_w + df["Interest Score"] * interest_w).round(2)
        df = df.sort_values(by="Final Score", ascending=False).reset_index(drop=True)
        df.insert(0, "Rank", range(1, len(df) + 1))
        df["Risk Flag"] = df.apply(lambda r: self.flag_risk(r["Match Score"], r["Interest Score"]), axis=1)
        df["Recommended Action"] = df.apply(
            lambda r: self.recommend_action(r["Match Score"], r["Interest Score"], str(r.get("Availability", ""))), axis=1
        )
        return df

    def generate_structured_output(self, jd_req: dict, final_df: pd.DataFrame, matcher: 'Matcher') -> dict:
        job_summary = {
            "role_title": jd_req.get("role_title", ""),
            "must_have_skills": jd_req.get("must_have_skills", []),
            "good_to_have_skills": jd_req.get("good_to_have_skills", []),
            "experience": f"{jd_req.get('experience_min', 0)}+ years",
            "seniority": jd_req.get("seniority", "mid"),
            "location": jd_req.get("location", "Not specified"),
            "work_mode": jd_req.get("work_mode", "Not specified"),
            "hidden_signals": jd_req.get("hidden_signals", {}),
        }
        candidates_out = []
        for _, row in final_df.iterrows():
            sg = matcher.get_strengths_and_gaps(jd_req, row)
            candidates_out.append({
                "rank": int(row["Rank"]),
                "name": row["Name"],
                "match_score": float(row["Match Score"]),
                "interest_score": float(row["Interest Score"]),
                "final_score": float(row["Final Score"]),
                "strengths": sg["strengths"],
                "gaps": sg["gaps"],
                "explanation": row.get("Explanation", ""),
                "risk_flag": row.get("Risk Flag", ""),
                "recommended_action": row.get("Recommended Action", ""),
                "conversation_summary": row.get("Conversation Summary", ""),
            })
        return {"job_summary": job_summary, "candidates": candidates_out}
