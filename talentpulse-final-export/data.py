import pandas as pd
import os

def generate_mock_data():
    candidates = [
        # ── Software Engineers ──────────────────────────────────────────────────────
        {
            "Name": "Anjali Verma", "Role": "Senior Python Developer",
            "Location": "Bengaluru", "Current Company": "Infosys", "Experience": 8,
            "Skills": "Python, FastAPI, Docker, PostgreSQL, CI/CD, AWS, REST API",
            "Availability": "2 weeks", "Notice Period": "30 days",
            "Response": "Absolutely thrilled to learn about this! This perfectly aligns with my next career steps. Let's schedule something ASAP!",
            "Response2": "Yes, I can do a call this Thursday or Friday. My notice period is 30 days but negotiable. Very excited to move forward!"
        },
        {
            "Name": "Rahul Sharma", "Role": "Software Engineer",
            "Location": "Hyderabad", "Current Company": "Wipro", "Experience": 5,
            "Skills": "Python, Django, AWS, SQL, React, Docker",
            "Availability": "Immediate", "Notice Period": "15 days",
            "Response": "I am very interested in this role! Building scalable systems is my passion. When can we chat?",
            "Response2": "I'm available any day this week. Currently serving a 15-day notice, so I can start almost immediately. Let's do it!"
        },
        {
            "Name": "Karthik Iyer", "Role": "Senior Software Engineer",
            "Location": "Chennai", "Current Company": "TCS", "Experience": 6,
            "Skills": "Java, Spring Boot, Microservices, AWS, Kubernetes, SQL",
            "Availability": "1 month", "Notice Period": "45 days",
            "Response": "Sounds like a great opportunity. I'd love to learn more about the tech stack and team structure.",
            "Response2": "I could do a call next week. I have a 45-day notice period. The role sounds promising — happy to explore further."
        },
        {
            "Name": "Divya Choudhury", "Role": "Software Engineer",
            "Location": "Pune", "Current Company": "Accenture", "Experience": 4,
            "Skills": "Python, Flask, React, MySQL, Docker, REST API",
            "Availability": "2 weeks", "Notice Period": "30 days",
            "Response": "Yes, I am actively exploring new roles. This one sounds exciting! Let's definitely chat.",
            "Response2": "I'm free this week for a call. My notice period is 30 days. I'd love to know more about the team and growth path."
        },
        {
            "Name": "Sanjay Das", "Role": "Backend Engineer",
            "Location": "Kolkata", "Current Company": "Cognizant", "Experience": 4,
            "Skills": "C++, Java, Algorithms, PostgreSQL, Linux",
            "Availability": "Immediate", "Notice Period": "0 days",
            "Response": "I prefer working strictly backend. If this fits that, let's talk.",
            "Response2": "OK, if it's a pure backend role I'm in. I can start immediately since I'm between contracts."
        },
        {
            "Name": "Pooja Joshi", "Role": "Junior Python Developer",
            "Location": "Mumbai", "Current Company": "Startup", "Experience": 1,
            "Skills": "Python, Flask, HTML, CSS, MySQL",
            "Availability": "Immediate", "Notice Period": "0 days",
            "Response": "I'm very interested! I'm eager to learn and grow in a new position.",
            "Response2": "I can start right away! I'm currently free and would love the opportunity to prove myself."
        },
        {
            "Name": "Arjun Kapoor", "Role": "Lead Software Engineer",
            "Location": "Delhi", "Current Company": "HCL", "Experience": 12,
            "Skills": "Java, Python, Microservices, Kafka, AWS, Leadership, Agile",
            "Availability": "1 month", "Notice Period": "60 days",
            "Response": "Happy to explore options. I'm looking for a role with strong engineering culture.",
            "Response2": "Let's set up a technical discussion. I have a 60-day notice but can negotiate. Culture fit is key for me."
        },
        # ── Frontend & Fullstack ─────────────────────────────────────────────────
        {
            "Name": "Priya Patel", "Role": "Frontend Developer",
            "Location": "Ahmedabad", "Current Company": "Razorpay", "Experience": 3,
            "Skills": "React, JavaScript, HTML, CSS, Tailwind, Webpack, TypeScript",
            "Availability": "2 weeks", "Notice Period": "30 days",
            "Response": "Sounds interesting, maybe we can hop on a call next week.",
            "Response2": "Sure, next Wednesday works for me. I'm on a 30-day notice. What's the tech stack like?"
        },
        {
            "Name": "Aditya Sengupta", "Role": "Senior React Engineer",
            "Location": "Bengaluru", "Current Company": "Swiggy", "Experience": 5,
            "Skills": "React, Redux, Next.js, TypeScript, GraphQL, CSS, Jest",
            "Availability": "Immediate", "Notice Period": "30 days",
            "Response": "I am absolutely looking for my next React challenge! Please send calendar links.",
            "Response2": "Sent you my calendar link! I can interview this week itself. Super pumped about this one!"
        },
        {
            "Name": "Rohan Desai", "Role": "Fullstack Developer",
            "Location": "Bengaluru", "Current Company": "Freshworks", "Experience": 2,
            "Skills": "Node.js, Express, React, MongoDB, TypeScript",
            "Availability": "Immediate", "Notice Period": "15 days",
            "Response": "Yeah, I could take a look. Send over more details.",
            "Response2": "I've read the JD. It's decent. I'd want to know about the comp before committing to interviews."
        },
        {
            "Name": "Suresh Menon", "Role": "Frontend Developer",
            "Location": "Kochi", "Current Company": "UST Global", "Experience": 4,
            "Skills": "Vue.js, JavaScript, SASS, Nuxt.js, CSS",
            "Availability": "1 month", "Notice Period": "30 days",
            "Response": "Sorry, I am only looking for Vue positions at the moment.",
            "Response2": ""
        },
        {
            "Name": "Meera Pillai", "Role": "Fullstack Developer",
            "Location": "Hyderabad", "Current Company": "Zoho", "Experience": 6,
            "Skills": "React, Node.js, Python, PostgreSQL, Docker, AWS, GraphQL",
            "Availability": "2 weeks", "Notice Period": "30 days",
            "Response": "This looks great! I have been looking for exactly this kind of role. Can we schedule a call this week?",
            "Response2": "Thursday 3 PM works for me. My notice period is 30 days. I'm very keen on this opportunity!"
        },
        # ── Data Science & ML ───────────────────────────────────────────────────
        {
            "Name": "Amit Kumar", "Role": "Data Scientist",
            "Location": "Mumbai", "Current Company": "Mu Sigma", "Experience": 4,
            "Skills": "Python, Machine Learning, Scikit-Learn, Pandas, NLP, SQL",
            "Availability": "1 month", "Notice Period": "30 days",
            "Response": "I am excited to hear more about the AI initiatives at your company. Let's definitely talk.",
            "Response2": "I can do a call this Friday. 30-day notice. I'd love to understand the ML infra and team size."
        },
        {
            "Name": "Sneha Reddy", "Role": "Machine Learning Engineer",
            "Location": "Hyderabad", "Current Company": "NVIDIA", "Experience": 3,
            "Skills": "Python, PyTorch, Deep Learning, MLOps, Hugging Face, NLP",
            "Availability": "2 months", "Notice Period": "60 days",
            "Response": "I'm open to new opportunities if the compensation is right. Happy to chat.",
            "Response2": "Let's discuss comp ranges first. I have a 60-day notice at NVIDIA. Interested if it's competitive."
        },
        {
            "Name": "Manish Tiwari", "Role": "AI Engineer",
            "Location": "Bengaluru", "Current Company": "Google", "Experience": 10,
            "Skills": "Python, AI, Machine Learning, LLM, PyTorch, TensorFlow, RAG, LangChain",
            "Availability": "3 months", "Notice Period": "90 days",
            "Response": "Sounds interesting. I'm selective, but I'd consider a conversation. What's the problem space?",
            "Response2": "The problem space is intriguing. I have a 90-day notice. Let's do a deep technical discussion first."
        },
        {
            "Name": "Nandini Mishra", "Role": "Data Scientist",
            "Location": "Delhi", "Current Company": "Deloitte", "Experience": 6,
            "Skills": "Python, Machine Learning, SQL, Salesforce, Marketing Automation, Pandas",
            "Availability": "1 month", "Notice Period": "30 days",
            "Response": "Interesting intersection of skills required. I'd consider chatting about it.",
            "Response2": "I can do a call next week. My notice is 30 days. I'd want to understand the data maturity level."
        },
        {
            "Name": "Ravi Krishnamurthy", "Role": "Senior Data Scientist",
            "Location": "Bengaluru", "Current Company": "Amazon", "Experience": 9,
            "Skills": "Python, Scikit-Learn, NLP, Pandas, AWS, Spark, Deep Learning",
            "Availability": "2 months", "Notice Period": "60 days",
            "Response": "Very excited about this! I've been wanting to work on product-side ML. Let's connect soon.",
            "Response2": "Can we do a call this week? I'm highly motivated to switch. 60-day notice but I'll push for early release."
        },
        # ── Cloud & DevOps ───────────────────────────────────────────────────────
        {
            "Name": "Vikram Singh", "Role": "Cloud Architect",
            "Location": "Noida", "Current Company": "Microsoft", "Experience": 10,
            "Skills": "AWS, Azure, Terraform, Kubernetes, Linux, Networking, Prometheus",
            "Availability": "3 months", "Notice Period": "90 days",
            "Response": "Not looking right now, thanks though.",
            "Response2": ""
        },
        {
            "Name": "Dhruv Malhotra", "Role": "DevOps Engineer",
            "Location": "Pune", "Current Company": "ThoughtWorks", "Experience": 5,
            "Skills": "Jenkins, Ansible, Docker, Kubernetes, AWS, CI/CD, Terraform",
            "Availability": "Immediate", "Notice Period": "30 days",
            "Response": "I might be interested, but I'd need to know more about the team culture first.",
            "Response2": "OK, the culture sounds good. I'm on 30-day notice. Can we schedule a technical round next week?"
        },
        {
            "Name": "Priyanka Chatterjee", "Role": "Senior DevOps Engineer",
            "Location": "Kolkata", "Current Company": "IBM", "Experience": 7,
            "Skills": "Kubernetes, Docker, AWS, GCP, Terraform, Linux, Prometheus, Grafana",
            "Availability": "1 month", "Notice Period": "45 days",
            "Response": "This aligns with my current trajectory. I'm actively looking and would love to hear more!",
            "Response2": "Absolutely, let's move fast. I have 45-day notice but can negotiate. I'm very excited about this!"
        },
        {
            "Name": "Deepak Bhatt", "Role": "System Administrator",
            "Location": "Jaipur", "Current Company": "Infosys BPO", "Experience": 15,
            "Skills": "Windows Server, Linux, Active Directory, Networking",
            "Availability": "Immediate", "Notice Period": "30 days",
            "Response": "I'll pass, thank you.",
            "Response2": ""
        },
        # ── Data Engineering ─────────────────────────────────────────────────────
        {
            "Name": "Meera Rao", "Role": "Data Engineer",
            "Location": "Bengaluru", "Current Company": "Flipkart", "Experience": 5,
            "Skills": "Python, Spark, Airflow, Snowflake, SQL, Kafka, dbt",
            "Availability": "1 month", "Notice Period": "30 days",
            "Response": "Thank you for the message. I'm highly interested in learning more about the data infrastructure.",
            "Response2": "I'd love a call this week. 30-day notice period. The data stack sounds very modern — excited!"
        },
        {
            "Name": "Siddharth Bose", "Role": "Senior Data Engineer",
            "Location": "Hyderabad", "Current Company": "Walmart Labs", "Experience": 8,
            "Skills": "Python, Spark, Airflow, BigQuery, SQL, Kafka, GCP",
            "Availability": "2 months", "Notice Period": "60 days",
            "Response": "Absolutely, this sounds like the kind of scale I want to work at. Very interested!",
            "Response2": "Let's schedule something ASAP! I have 60-day notice but highly motivated. This is exactly what I want."
        },
        # ── Backend & Specialist ─────────────────────────────────────────────────
        {
            "Name": "Neha Gupta", "Role": "Senior Backend Engineer",
            "Location": "Mumbai", "Current Company": "Paytm", "Experience": 7,
            "Skills": "Java, Spring Boot, Microservices, Kubernetes, Docker, Redis, Kafka",
            "Availability": "1 month", "Notice Period": "45 days",
            "Response": "To be honest, I'm quite happy where I am right now, but I appreciate you reaching out.",
            "Response2": ""
        },
        {
            "Name": "Kavita Nair", "Role": "Senior Backend Engineer",
            "Location": "Bengaluru", "Current Company": "Dunzo", "Experience": 6,
            "Skills": "Go, Python, gRPC, Redis, PostgreSQL, Docker, Kubernetes",
            "Availability": "2 weeks", "Notice Period": "30 days",
            "Response": "This sounds like an incredible opportunity. I would love to interview for this!",
            "Response2": "I'm free any day this week! 30-day notice. Can we start with a technical discussion? Very keen!"
        },
        {
            "Name": "Tarun Jain", "Role": "Backend Developer",
            "Location": "Gurgaon", "Current Company": "MakeMyTrip", "Experience": 3,
            "Skills": "Node.js, Express, MongoDB, Redis, REST API, Docker",
            "Availability": "Immediate", "Notice Period": "15 days",
            "Response": "I've been exploring options and this caught my eye. Would love to know more!",
            "Response2": "I can interview this week. 15-day notice and ready to move. What are the next steps?"
        },
        # ── Miscellaneous / Edge cases ───────────────────────────────────────────
        {
            "Name": "Ananya Bhattacharya", "Role": "UI/UX Designer & Frontend Developer",
            "Location": "Mumbai", "Current Company": "Razorpay", "Experience": 4,
            "Skills": "Figma, CSS, React, HTML, JavaScript, Tailwind, Design Systems",
            "Availability": "1 month", "Notice Period": "30 days",
            "Response": "I'd love to see the product first before committing. It sounds fun!",
            "Response2": "The product looks interesting! I have 30-day notice. Let's set up a portfolio review call."
        },
        {
            "Name": "Gaurav Mehta", "Role": "Project Manager",
            "Location": "Delhi", "Current Company": "TCS", "Experience": 12,
            "Skills": "Agile, Scrum, Jira, Leadership, Project Management, Communication",
            "Availability": "2 months", "Notice Period": "60 days",
            "Response": "Happy to discuss if the role involves technical leadership. Let me know!",
            "Response2": "If there's a leadership component, I'm interested. 60-day notice. Let's chat about scope."
        },
        {
            "Name": "Ishaan Malhotra", "Role": "Junior Software Engineer",
            "Location": "Bengaluru", "Current Company": "Startup", "Experience": 1,
            "Skills": "Python, JavaScript, HTML, CSS, React, SQL",
            "Availability": "Immediate", "Notice Period": "0 days",
            "Response": "Super excited about this! This would be a huge opportunity for me to grow.",
            "Response2": "I can start tomorrow if needed! No notice period. I'm all in on this opportunity!"
        },
        {
            "Name": "Farhan Qureshi", "Role": "Senior Full Stack Developer",
            "Location": "Bengaluru", "Current Company": "PhonePe", "Experience": 8,
            "Skills": "Python, Django, React, TypeScript, AWS, Docker, PostgreSQL, CI/CD",
            "Availability": "1 month", "Notice Period": "30 days",
            "Response": "This is exactly what I'm looking for. I'm happy to fast-track the process!",
            "Response2": "Let's do the first call tomorrow! 30-day notice, negotiable. I'm extremely motivated for this switch."
        },
        {
            "Name": "Lakshmi Subramaniam", "Role": "Principal Engineer",
            "Location": "Chennai", "Current Company": "Oracle", "Experience": 15,
            "Skills": "Java, Python, Architecture, Microservices, AWS, Leadership, Agile, SQL",
            "Availability": "3 months", "Notice Period": "90 days",
            "Response": "Intriguing opportunity. I'm very selective at my career stage, but this is worth a conversation.",
            "Response2": "Let's have a principal-level technical conversation. 90-day notice. I'd need to see strong alignment."
        },
    ]
    df = pd.DataFrame(candidates)
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_candidates.csv")
    df.to_csv(csv_path, index=False)
    print(f"[OK] Mock dataset generated: {len(df)} candidates saved to {csv_path}")

if __name__ == "__main__":
    generate_mock_data()
