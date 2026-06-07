# 🛡️ AgentMoat

### Localized Edge Security Layer for Autonomous AI Agents

**AgentMoat** is a lightweight, on-device security gateway that protects AI agents from prompt injection and jailbreak attacks before requests reach an LLM. Running entirely within the application's environment, it provides fast threat detection, improved privacy, and zero external API dependency.

---

## 🔗 Links

* **Live App:** https://agentmoat.streamlit.app/
* **Presentation Deck:** https://mahekbhambhani.github.io/AgentMoat/
* **GitHub Repository:** https://github.com/mahekbhambhani/AgentMoat

---

# 🚨 The Problem

As organizations adopt autonomous AI agents capable of interacting with databases, APIs, and enterprise systems, security becomes a critical challenge.

Prompt injection attacks can manipulate an agent's behavior, override system instructions, expose sensitive information, or trigger unintended actions.

Most existing guardrail solutions rely on cloud-based moderation APIs, creating three major challenges:

### 1. Latency Overhead

Every request must travel to an external service before reaching the LLM, introducing additional response time.

### 2. Operational Cost

Cloud moderation services often charge based on API usage or token consumption, increasing infrastructure costs as traffic grows.

### 3. Privacy Concerns

Sensitive prompts and internal business data must be transmitted to third-party services for evaluation.

---

# 💡 Our Solution

AgentMoat shifts AI security to the edge by running threat detection locally.

Instead of sending prompts to external safety services, AgentMoat evaluates requests within the application's environment and blocks potentially malicious inputs before they reach downstream AI systems.

### Key Benefits

* ⚡ Low-latency local inference
* 🔒 No external prompt transmission
* 💰 No per-request moderation costs
* 🏢 Enterprise-friendly deployment
* 🧩 Easy integration with agent frameworks

---

# ⚙️ How It Works

### 1. Threat Intelligence Ingestion (`ingest.py`)

Collects known jailbreak and prompt injection samples and converts them into vector representations stored locally.

### 2. Security Engine (`guard.py`)

Performs similarity analysis against the local threat database and calculates risk scores for incoming prompts in real time.

### 3. Monitoring Dashboard (`app.py`)

Provides a Streamlit-based interface for:

* Testing prompts
* Monitoring detections
* Adjusting sensitivity thresholds
* Evaluating system behavior

---

# 📊 Performance

| Metric            | Traditional Cloud Moderation | AgentMoat             |
| ----------------- | ---------------------------- | --------------------- |
| Deployment Model  | External API                 | Local Edge Runtime    |
| Data Processing   | Remote Service               | Local Processing      |
| Privacy           | Prompt Leaves Environment    | Prompt Remains Local  |
| Cost Model        | Usage-Based                  | No External API Costs |
| Response Overhead | Network Dependent            | Local Execution       |

> Note: Exact latency and accuracy metrics depend on hardware, deployment environment, and dataset size.

---

# 🏗️ Technology Stack

### Backend

* Python 3.9+

### Data Processing

* NumPy
* SciPy

### User Interface

* Streamlit

### Deployment

* Docker-ready Containers

---

# 🚀 Quick Start

## Clone Repository

```bash
git clone https://github.com/mahekbhambhani/AgentMoat.git
cd AgentMoat
```

## Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Build Threat Index

```bash
python ingest.py
```

## Launch Dashboard

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🔮 Roadmap

### Edge Synchronization

Distribute updated threat signatures across multiple deployments without service interruption.

### Framework Integrations

Native SDKs and middleware for:

* LangChain
* CrewAI
* AutoGen
* Semantic Kernel

### Automated Security Testing

Generate and evaluate synthetic adversarial prompts to continuously improve detection coverage.

### Enterprise Analytics

Threat dashboards, audit logs, and compliance reporting for production deployments.

---

# 🏆 Hackathon Value Proposition

**AgentMoat enables secure AI adoption by providing a local-first defense layer that protects autonomous agents from prompt injection attacks without sacrificing privacy, performance, or cost efficiency.**

By moving security closer to where AI executes, AgentMoat helps organizations deploy agentic systems with greater confidence and control.

---

## License

Released under the MIT License.
