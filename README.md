<div align="center">

```
██╗    ██╗██████╗  █████╗ ████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗
██║    ██║██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝
██║ █╗ ██║██████╔╝███████║   ██║   ███████║██║   ██║██████╔╝███████╗
██║███╗██║██╔══██╗██╔══██║   ██║   ██╔══██║██║   ██║██╔═══╝ ╚════██║
╚███╔███╔╝██║  ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║     ███████║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝
```

### 🔐 AI-Powered Secret Detection, Understanding, and Prevention

<br/>

[![License](https://img.shields.io/badge/license-MIT-crimson?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyPI](https://img.shields.io/badge/install-pip-FF6B35?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-ready-FAB040?style=for-the-badge&logo=precommit&logoColor=black)](https://pre-commit.com)
[![Security](https://img.shields.io/badge/security-first-00C896?style=for-the-badge&logo=shieldsdotio&logoColor=white)](#)

<br/>

> *Stop secrets before they stop you.*
> WrathOps doesn't just detect — it **understands**, **explains**, and **protects**.

<br/>

</div>

---

## ⚡ Why WrathOps?

Most security tools scream at you with a vague `Secret detected` and leave you stranded. **WrathOps is built differently.**

```
Traditional Tools    →    "Secret detected. Good luck."
WrathOps             →    "Here's what it is, how dangerous it is,
                           whether it's active, and exactly how to fix it."
```

| Question | WrathOps Answers It |
|---|---|
| 🎯 **What is it?** | Identifies the exact provider and secret type |
| ⚠️ **How dangerous?** | Classifies risk from 0–100 with confidence scoring |
| 💥 **Why does it matter?** | Explains real-world impact in plain language |
| 🔍 **Is it even active?** | Validates key status without external exposure |
| 🔧 **How do I fix it?** | Guides you toward safe, immediate remediation |

---

## 🧠 Key Features

<br/>

### `01` — Context-Aware Secret Detection

> Beyond regex. WrathOps **reads the room.**

- Distinguishes **test keys** from **production keys**
- Understands intent based on file type and usage context
- Adapts detection logic per developer environment

<br/>

### `02` — AI-Based Risk Classification

Every finding gets an intelligent verdict:

```
┌─────────────────────────────────────────────┐
│  Classifications                            │
│                                             │
│  🟢  fake_or_test       → Safe to ignore    │
│  🟡  expired_or_invalid → Low priority      │
│  🔴  real_and_dangerous → Act immediately   │
│                                             │
│  + Risk Score    (0 – 100)                  │
│  + Confidence Score                         │
└─────────────────────────────────────────────┘
```

<br/>

### `03` — Developer-Friendly Explanations

No jargon. No vague warnings. Just clarity:

```
💬  "This appears to be a production AWS key. If exposed, attackers
     could access your cloud infrastructure and incur billing charges."
```

<br/>

### `04` — Safe Validation Layer

Key status — determined **without** sending your secrets anywhere:

- ✅ **Likely Active** — Matches known production patterns
- ⚠️ **Likely Inactive** — Test/example pattern detected
- ❓ **Unknown** — Valid format, status unverified

<br/>

### `05` — False Positive Reduction

Tired of your example docs getting flagged?

- Detects known dummy/test key patterns automatically
- Filters noise so you focus on **real threats only**

<br/>

### `06` — Pre-Commit Protection

```
Write code → Stage changes → WrathOps checks → ✅ Clean commit  OR  ❌ Blocked
```

- Runs **entirely locally** — fast and lightweight
- Stops secrets at the source, before they ever touch a remote

---

## ⚙️ How It Works

```
  ┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
  │              │     │                  │     │                  │     │                  │
  │  DETECTION   │────▶│  CLASSIFICATION  │────▶│  EXPLANATION     │────▶│  VALIDATION      │
  │              │     │                  │     │                  │     │                  │
  │  Scans your  │     │  AI determines   │     │  Human-readable  │     │  Safely checks   │
  │  codebase    │     │  severity &      │     │  risk summary    │     │  key format &    │
  │  for secrets │     │  category        │     │  is generated    │     │  status          │
  │              │     │                  │     │                  │     │                  │
  └──────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
```

---

## 💻 Getting Started

### Installation

```bash
pip install git+https://github.com/tulu-g559/WrathOps-cli.git
wrathops install
```

### Scan a File or Directory

```bash
wrathops scan ./my_project
```

### Pre-Commit Setup *(Recommended)*

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/your-org/wrathops
    rev: v1.0.0
    hooks:
      - id: wrathops
```

Then install the hook:

```bash
pre-commit install
```

---

## 🛠️ Example Output

```
🚨 Secrets Detected in ./app.py
════════════════════════════════════════════════════════════

  → AWS_SECRET_KEY
    Risk: 100/100  │  Class: real_and_dangerous  │  Confidence: 0.99
    ──────────────────────────────────────────────────────
    This appears to be a production AWS secret key. If exposed,
    attackers could access your cloud resources and incur costs.
    Status: ❓ Unknown (valid format, not externally verified)

  → GOOGLE_API_KEY
    Risk: 82/100   │  Class: real_and_dangerous  │  Confidence: 0.82
    ──────────────────────────────────────────────────────
    This appears to be a Google API key. It could allow access to
    your services and lead to data exposure or abuse.
    Status: ⚠️ Likely Inactive (test/example pattern detected)

════════════════════════════════════════════════════════════
❌ Commit blocked: 2 secret(s) detected. Remediate before committing.
```

---

## 🔒 Safety & Privacy

WrathOps is designed with **absolute privacy** at its core.

```
✅  No secrets stored         — ever.
✅  No external API calls     — your keys never leave your machine.
✅  Fully local execution     — runs entirely on your system.
✅  Masked outputs & logs     — sensitive values are never printed raw.
```

> **Your code is your business. WrathOps keeps it that way.**

---

## 📦 Use Cases & Target Audience

### Who Is It For?

| Audience | Use Case |
|---|---|
| 👨‍💻 **Jr. Software Engineers** | Lightweight, noise-free pre-commit security hook |
| 🎓 **Students & Learners** | Learn security best practices and env variable hygiene |
| 👔 **Engineering Managers** | Improve team-wide security culture and code hygiene |

### When Should You Use It?

- Before pushing any code to **GitHub / GitLab**
- To secure **hackathon**, student, or beginner projects
- As a **final safety net** in any development workflow

---

## 🚀 Roadmap

The vision for WrathOps is to become a **complete Developer Security Assistant**.

- [x] **Automated Fix Generation** — Move hardcoded secrets to `.env` and replace with `os.getenv()` automatically
- [x] **GitHub PR Remediation** — Automated PR comments explaining risks, natively in GitHub
- [x] **CI/CD Integration** — Native GitHub Actions and GitLab CI plugins
- [x] **Provider-Level Safe Validation** — Secure, non-intrusive validation against AWS, OpenAI, and more
- [x] **Org-Level Analytics** — Dashboards to monitor security hygiene trends across teams

---

<div align="center">

<br/>

**Built for developers who care about security — without sacrificing speed.**

<br/>

*WrathOps — Detect. Understand. Prevent.*

<br/>

[![Star on GitHub](https://img.shields.io/badge/⭐_Star_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/tulu-g559/WrathOps-cli)

</div>
