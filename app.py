from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

JIRA_BASE_URL = "https://evolve24.atlassian.net"
EMAIL = "loganj@evolve24.com"
API_TOKEN = os.getenv("JIRA_API_TOKEN")
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {os.getenv('JIRA_AUTH')}"
}

DESCRIPTION_TEMPLATE = """
---

### 🔗 Epic-Level User Story
Who is this work for, and what does it solve?  
_Copy the user story from the parent epic that this ticket supports._

---

### 🧑‍💻 Story-Specific User Statement  
As a _______________,  
I want to _______________  
So that _______________

---

### ✅ Success Criteria / Acceptance Criteria  
What does “done” look like?  
_Metrics like model performance, accuracy, latency, usability, etc._

---

### 🧬 Data Sources  
What data is needed and where is it located?  
- Table names / Databricks schema paths:  
- API endpoints:  
- Documentation links:  

---

### 🚨 Data Quality / Known Issues  
Are there any concerns about data completeness, freshness, or anomalies?

---

### 📊 Exploration / Baseline Expectations  
Any known benchmarks, previous outputs, or expected results?

---

### 🧱 Technical Constraints  
Are there constraints (compute, libraries, environment, model type)?

---

### 🔗 Dependencies  
Does this depend on another story, team, or dataset?

---

### 📦 Deliverables  
What will be delivered with this story?  
- [ ] Code / Notebook  
- [ ] Model Artifact  
- [ ] Dashboard / Output File  
- [ ] Presentation / Summary  
- [ ] Other: ______________

---

### 👥 Reviewer / Collaborator  
Who is reviewing or consuming this work?  
_Name(s), title(s), or teams:_

---
"""

ACCEPTANCE_CRITERIA_TEMPLATE = """Acceptance criteria reminders:
As applicable, review from [e.g., DS VP / Eng tech lead]
As applicable, Review from Design
As applicable, Review from Product
Include links to artifacts produced as outcome of this work (e.g., figma files+screenshot)
"""

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    issue_key = data.get("issue", {}).get("key")

    if not issue_key:
        return jsonify({"error": "No issue key"}), 400

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    payload = {
        "fields": {
            "description": DESCRIPTION_TEMPLATE,
            "customfield_10404": ACCEPTANCE_CRITERIA_TEMPLATE
        }
    }

    response = requests.put(url, headers=HEADERS, json=payload)

    return jsonify({"status": response.status_code, "text": response.text})

if __name__ == "__main__":
    app.run(port=5000)
