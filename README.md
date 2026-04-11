WrathOps 🔐
===========

**AI-Powered Secret Detection, Understanding, and Prevention**

WrathOps is a developer-first security tool that goes beyond merely detecting secrets. It actively understands them, explains the associated risks, and helps you fix issues _before_ they ever reach your repository.

Designed for developers of all levels, WrathOps acts as a security assistant to keep your code safe without slowing you down.

📖 Table of Contents
--------------------

*   Why WrathOps?
*   Key Features
*   How It Works
*   Getting Started
*   Example Output
*   Safety & Privacy
*   Use Cases & Target Audience
*   Roadmap
    

🚀 Why WrathOps?
----------------

Most security tools just yell at you when something is wrong. They output a vague Secret detected warning and leave you to figure out the rest.

**WrathOps is different. It tells you:**

*   **What it is:** Identifies the exact provider and type of secret.
*   **How dangerous it is:** Classifies risk levels accurately.
*   **Why it matters:** Explains the real-world impact of a leak.
*   **Whether it’s actually usable:** Checks if the key is active or a dummy.
*   **How to fix it:** Guides you toward safe remediation.
    

🧠 Key Features
---------------

### 1\. Context-Aware Secret Detection

WrathOps goes beyond simple regex matching. It understands the context of the secret, differentiating between test vs. real keys, analyzing usage context, and adapting to different file types and developer intents.

### 2\. AI-Based Risk Classification

Every detected secret is intelligently classified:

*   fake\_or\_test
*   expired\_or\_invalid
*   real\_and\_dangerous
    

_Includes a granular_ _**Risk Score (0–100)**_ _and a_ _**Confidence Score**__._

### 3\. Developer-Friendly Explanations

Instead of a generic warning, WrathOps gives actionable insight.

> _"This appears to be a production AWS key. If exposed, attackers could access your cloud infrastructure and incur billing charges."_

### 4\. Safe Validation Layer

WrathOps determines the status of a key (Likely Active, Likely Inactive, or Unknown) **without exposing the secret externally**.

### 5\. False Positive Reduction

Tired of tools flagging your example documentation? WrathOps detects known example/test key patterns and filters out dummy values, significantly reducing noise.

### 6\. Pre-Commit Protection

Stop leaks at the source. WrathOps blocks commits containing sensitive data. It works completely locally, remaining fast and lightweight.

⚙️ How It Works
---------------

WrathOps evaluates your code through a streamlined, layered pipeline:

1.  **Detection** → Finds potential secrets in the codebase.
2.  **Classification** → AI determines the severity and category of the finding.
3.  **Explanation** → Generates a human-readable explanation of the risk and impact.
4.  **Validation** → Safely checks if the key has usable formatting or patterns.
    

💻 Getting Started
------------------

_(Note: Adjust installation instructions based on your actual distribution method)_

### Installation

Install WrathOps globally via pip:
```
pip install git+https://github.com/tulu-g559/WrathOps-cli.git
```

### Running Locally

Scan a specific file or directory:
```
wrathops scan ./my_project
```

### Setting up Pre-Commit (Recommended)

Add WrathOps to your .pre-commit-config.yaml to automatically block secrets before they are committed:
```
repos:
  - repo: https://github.com/your-org/wrathops
    rev: v1.0.0
    hooks:
      - id: wrathops
```

🛠 Example Output
-----------------

When WrathOps catches a secret, the output is clear, contextual, and actionable:
```  
🚨 Secrets in .\app.py

→ AWS_SECRET_KEY (risk=100, class=real_and_dangerous, confidence=0.99)
This appears to be an AWS secret key. If exposed, attackers could access your cloud resources and incur costs.
Status: Unknown (valid format, not verified)

→ GOOGLE_API_KEY (risk=82, class=real_and_dangerous, confidence=0.82)
This appears to be a Google API key. It could allow access to your services and lead to data exposure.
Status: Likely Inactive (test/example pattern detected)

❌ Commit blocked: secrets detected.
```

🔒 Safety First
---------------

Your code is your business. WrathOps is built with absolute privacy in mind:

*   **No secrets are stored.**
*   **No external exposure** (API calls to providers are not made with your raw keys).
*   **Fully local execution.**
*   Outputs and logs are safely **masked**.
    

📦 Use Cases & Target Users
---------------------------

**Who is it for?**

*   **Jr. Software Engineers** looking for a lightweight, noise-free pre-commit hook.
*   **Junior Developers & Students** learning security best practices and proper environment variable management.
*   **Engineering Managers** looking to improve team security hygiene.
    

**When to use it?**

*   To prevent accidental secret leaks to GitHub/GitLab.
*   To secure hackathon, student, and beginner projects.
*   As a definitive safety net before pushing any code.
    

🚀 Future Improvements
----------------------

The vision for WrathOps is to become a complete **Developer Security Assistant**. Upcoming features on our roadmap include:

*  [x] **Automated Fix Generation:** Automatically moving hardcoded secrets to .env files and replacing them with os.getenv().
*  [x] **GitHub PR Remediation:** Automated PR comments explaining risks natively in GitHub.
*  [x] **CI/CD Integration:** Native GitHub Actions and GitLab CI plugins.
*  [x] **Provider-Level Safe Validation:** Secure, non-intrusive validation against AWS, OpenAI, etc.
*  [x] **Organization-Level Analytics:** Dashboards to monitor security hygiene trends across your teams.