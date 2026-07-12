# 🛡️ SENTRYX - AI Powered Endpoint Detection & Response (EDR)

SENTRYX is a lightweight AI-powered Endpoint Detection & Response (EDR) system developed in Python. It continuously monitors endpoint systems, detects suspicious behavior using both a rule-based detection engine and a Machine Learning model, and displays real-time security telemetry through a web dashboard.

---

## 🚀 Features

- Real-time endpoint monitoring
- CPU, Memory and Disk usage monitoring
- Running process monitoring
- Rule-based threat detection
- AI-based anomaly detection using Random Forest
- Real-time dashboard
- Multi-host monitoring
- Active alert management
- Process risk visualization
- SQLite database for telemetry storage
- REST API using FastAPI

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- SQLite

### Machine Learning
- Scikit-learn
- Random Forest Classifier
- Pandas
- NumPy

### Frontend
- HTML
- CSS
- JavaScript

### Libraries
- psutil
- requests
- joblib
- pydantic

---

## 📂 Project Structure

```
SENTRYX-EDR
│
├── agent/
│   ├── agent.py
│   └── modules_for_agents/
│
├── server/
│   ├── dashboard/
│   ├── database/
│   ├── ml/
│   ├── models/
│   └── server.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Biswajit-masanta/SENTRYX-EDR.git
```

Move into the project

```bash
cd SENTRYX-EDR
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Start the Server

```bash
cd server
uvicorn server:app --reload
```

### Start the Agent

Open another terminal.

```bash
cd agent
python agent.py
```

Open your browser:

```
http://127.0.0.1:8000/dashboard
```

---

## 🤖 Machine Learning

The AI module is built using a Random Forest Classifier.

Features used:

- CPU Usage
- Memory Usage
- Disk Usage
- Process Count
- Browser Count
- Python Process Running
- CMD Running
- PowerShell Running
- Unknown Process Count
- High CPU Processes
- High Memory Processes
- Total Active Alerts

The trained model predicts whether the endpoint behavior is:

- LOW Risk
- HIGH Risk

---

## 📊 Dashboard Modules

- Dashboard
- Systems
- Resource Monitoring
- Processes
- Alerts
- AI Anomaly Detection

---

## 🔐 Detection Engine

SENTRYX combines two independent detection mechanisms:

### Rule-Based Engine

Uses predefined security rules to detect:

- High CPU usage
- High Memory usage
- High Disk usage
- Suspicious process activity

### AI Detection

A Random Forest model analyzes endpoint telemetry and predicts whether the system behavior is LOW or HIGH risk.

---

## 📸 Screenshots

> Screenshots will be added soon.

---

## 👨‍💻 Author

**Biswajit Masanta**

GitHub:
https://github.com/Biswajit-masanta

LinkedIn:
https://www.linkedin.com/in/biswajit-masanta-735545400/

---

## ⭐ Star the Repository

If you found this project useful, consider giving it a ⭐ on GitHub.
