# 🛡️ RazorShield AI

### Autonomous Payment Risk Investigator
**Track 2 — AI Risk Manager**

RazorShield AI is an explainable payment-risk investigation platform designed to help risk teams detect suspicious transactions, understand why they are risky, uncover connected entities, and take auditable actions.

> **MVP:** Built for the Razorpay AI Builder / Buildathon track using synthetic payment data.

---

## 🚨 The Problem

Modern payment fraud is rarely visible from a single transaction.

A transaction can become suspicious because of a combination of signals:

- Unusually high transaction amounts
- Abnormal transaction velocity
- Devices shared across multiple accounts
- IP addresses shared across seemingly unrelated accounts
- Location anomalies
- Repeated behavioral patterns

Traditional rule-based dashboards often show a score without explaining the underlying relationships.

**RazorShield AI turns those scattered signals into an investigation.**

---

## 💡 Our Solution

RazorShield AI combines transaction-level risk scoring with relationship analysis.

For every suspicious transaction, the system can:

1. **Detect** anomalous payment behavior
2. **Score** the transaction from 0–100
3. **Explain** which signals contributed to the score
4. **Connect** related accounts, devices and IP addresses
5. **Summarize** the investigation
6. **Recommend** an operational response
7. **Record** the final action in an audit trail

This creates a simple workflow:

**Transaction → Risk Signals → Risk Score → Relationship Investigation → Decision → Audit Trail**

---

## ✨ Key Features

### 🎯 Explainable Risk Scoring

Every risk score is backed by visible signals rather than being a black box.

Example:

| Signal | Risk Contribution |
|---|---:|
| Unusual transaction amount | +25 |
| Device linked to multiple accounts | +20 |
| Shared IP across related activity | +15 |
| High transaction velocity | +20 |
| Suspicious behavioral pattern | +10 |

A transaction can therefore be investigated based on **why** it was flagged.

### 🕸️ Relationship-Based Investigation

RazorShield connects:

**Accounts ↔ Devices ↔ Transactions ↔ IP Addresses**

This helps investigators identify suspicious infrastructure shared across multiple transactions or accounts.

### 🤖 AI Investigation Summary

Instead of forcing an investigator to manually interpret every signal, RazorShield produces a concise investigation narrative describing:

- Number of triggered signals
- Related transactions
- Shared infrastructure
- Behavioral anomalies
- Recommended investigation priority

### ⚡ Risk Actions

Investigators can record operational decisions such as:

- **Manual Review**
- **Restrict**
- **Allow**

### 📋 Audit Trail

Every action is recorded with:

- Transaction ID
- Action taken
- Operator
- Timestamp

This provides traceability for risk decisions.

---

## 🖥️ MVP Dashboard

The dashboard provides a single Risk Command Center containing:

- Transaction statistics
- High-risk case count
- Average risk score
- Recent transactions
- AI investigation panel
- Risk relationship network
- Audit trail

### Example Investigation

`TX-10482` demonstrates a high-risk transaction:

**Risk Score: 90 / 100 — CRITICAL**

The transaction is connected to other activity through shared device and IP infrastructure, while also triggering amount, velocity and behavioral signals.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │  Synthetic Payment  │
                    │       Data          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Risk Signal       │
                    │     Engine          │
                    └──────────┬──────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
              ┌──────────────┐    ┌──────────────┐
              │ Risk Scoring │    │ Relationship │
              │   0–100      │    │    Graph     │
              └──────┬───────┘    └──────┬───────┘
                     │                   │
                     └─────────┬─────────┘
                               ▼
                    ┌─────────────────────┐
                    │ AI Investigation    │
                    │     Summary         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Risk Decision       │
                    │ Review/Restrict/    │
                    │ Allow               │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Audit Trail      │
                    └─────────────────────┘
```

---

## 🛠️ Technology

The MVP intentionally uses a lightweight architecture so it can run locally without external infrastructure.

- **Python 3**
- Python `http.server`
- HTML5
- CSS3
- Vanilla JavaScript
- JSON-based synthetic transaction data
- REST-style local API endpoints

### Why lightweight?

The goal of the MVP is to demonstrate the complete **risk investigation workflow** reliably without dependency-heavy setup.

The architecture can later be extended with:

- Spring Boot services
- PostgreSQL
- Redis
- Production payment event streams
- Graph databases
- LLM-based investigation agents
- Real-time fraud monitoring

---

## 🚀 Run Locally

### Requirements

- Python 3.10+
- A modern web browser

No external Python packages are required.

### 1. Clone the repository

```bash
git clone https://github.com/lojer21/RazorShield-AI---buildathon.git
cd RazorShield-AI---buildathon
```

### 2. Start the application

```bash
python3 app.py
```

### 3. Open the dashboard

Open:

```text
http://localhost:8000
```

---

## 🎬 Recommended Demo Flow

For a quick demonstration:

1. Open **Risk Command Center**
2. Show the transaction statistics
3. Select **TX-10482**
4. Highlight the **90/100 CRITICAL** score
5. Explain the individual risk signals
6. Show the **AI Investigation** summary
7. Show the **Risk Relationship Network**
8. Click **Manual Review** or **Restrict**
9. Show the resulting **Audit Trail**

This demonstrates the complete journey from **detection to decision**.

---

## 🔌 API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/summary` | Dashboard risk statistics |
| `GET /api/transactions` | Transaction list with risk scores |
| `GET /api/investigate?id=TX-10482` | Detailed transaction investigation |
| `GET /api/audit` | Audit events |
| `POST /api/action` | Record a risk decision |

---

## 🔐 Security & Privacy

This MVP uses **synthetic transaction data only**.

No real customer payment information, credentials, API keys, or production payment data are included.

For a production implementation, sensitive data should be protected using:

- Encryption in transit and at rest
- Strong authentication and authorization
- Secrets management
- Role-based access control
- Immutable audit logging
- PII minimization and masking
- Secure model/API access

---

## 🧪 Demo Data

The repository contains intentionally crafted synthetic scenarios representing:

- High-value transactions
- Shared devices
- Shared IP infrastructure
- High transaction velocity
- Location anomalies
- Normal transactions for comparison

This makes the MVP deterministic and easy to demonstrate.

---

## 🔮 Future Roadmap

### Phase 1 — MVP
- [x] Risk scoring
- [x] Explainable signals
- [x] Relationship analysis
- [x] Investigation summary
- [x] Risk actions
- [x] Audit trail
- [x] Interactive dashboard

### Phase 2 — Productionization
- [ ] Spring Boot backend
- [ ] PostgreSQL transaction store
- [ ] Authentication and RBAC
- [ ] Real-time event ingestion
- [ ] Redis-based velocity detection
- [ ] Persistent investigation cases

### Phase 3 — Advanced Intelligence
- [ ] LLM-powered investigator agent
- [ ] Graph-based fraud-ring detection
- [ ] Adaptive risk thresholds
- [ ] Model feedback loop
- [ ] Real-time alerts
- [ ] Investigator copilot

---

## 🎯 Track Alignment

**Selected Track: Track 2 — AI Risk Manager**

RazorShield AI focuses on the core responsibilities of a payment-risk manager:

**Detect → Investigate → Explain → Decide → Audit**

The MVP demonstrates how AI-assisted investigation and relationship-based risk analysis can help investigators move from a suspicious transaction to an actionable decision.

---

## 👨‍💻 Project

**RazorShield AI — Autonomous Payment Risk Investigator**

Built as an MVP for the Razorpay AI Builder / Buildathon.

**Repository:**  
https://github.com/lojer21/RazorShield-AI---buildathon.git

---

## ⚠️ Disclaimer

This is a hackathon/Buildathon MVP using synthetic data. Risk scores and recommendations are demonstration logic and should not be used to make real-world financial decisions without appropriate validation, controls, monitoring, and regulatory review.
