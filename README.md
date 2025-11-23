# 🏛️ CPF Information Companion  
*AIBC Capstone 2025 – Web Application using Streamlit, RAG, and LLMs*

This project demonstrates how AI and retrieval systems can help citizens better understand CPF policies  
through clear explanations and personalised simulations. It is built as part of the **AIBC 2025 Capstone**.

---

# 📘 Overview

The application helps Singaporeans and PRs explore two key domains:

1. **Understand CPF retirement policies**  
2. **Simulate basic CPF retirement projections**

It brings together:
- A curated knowledge base of publicly available CPF information  
- Retrieval-Augmented Generation (RAG)  
- OpenAI LLMs  
- Interactive visualisations using Streamlit  
- A lightweight vector store for efficient search  

---

# 🚀 Features

## **1️⃣ CPF Policy Explainer (Chat with RAG)**  
Ask natural-language questions about:
- BRS / FRS / ERS  
- Withdrawals at age 55  
- CPF LIFE  
- Extra interest  
- Housing vs retirement trade-offs  

The system:
- Embeds your query  
- Retrieves relevant CPF policy chunks  
- Generates grounded explanations using LLMs  

---

## **2️⃣ Retirement Planning Simulator**  
Enter simple, non-PII parameters to project CPF balances:
- Current age  
- Planned retirement age  
- Current savings  
- Monthly contributions  
- Expected contribution growth  

The simulator:
- Applies a simple projection model  
- Compares your results to BRS / FRS / ERS  
- Generates an LLM explanation and a growth chart  

---

# 🧠 System Architecture

```
data/raw/                → curated markdown files (CPF policies)
data/processed/          → JSONL vector database (embeddings)
backend/build_corpus.py  → chunking + embeddings
backend/vector_store.py  → similarity search
backend/rag.py           → RAG pipeline, prompt construction
Streamlit pages          → interactive UI and visualisations
```

---

# 📚 Data Sources

All content is derived from **public, non-sensitive CPF webpages**, manually summarised and converted  
into markdown. No private or confidential information is used.

---

# ⚠️ Disclaimer

This application is a **prototype for educational purposes only**.

- Not intended for real-world financial, legal, or healthcare decisions  
- LLM-generated information may contain inaccuracies  
- Always consult official CPF calculators and professional advisers  

---

# 🛠️ Installation & Running Locally

## 1. Clone repository  
```
git clone https://github.com/<your-username>/<your-repo>.git
```

## 2. Create virtual environment  
```
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

## 3. Install dependencies  
```
pip install -r requirements.txt
```

## 4. Run Streamlit  
```
streamlit run Home.py
```

---

# 🔒 Deployment

This application is deployed using **Streamlit Community Cloud**:

- API keys stored securely in **Streamlit Secrets**
- User access protected via **password gate**
- All data processing runs within the app session  
- Fully serverless deployment

---

# 👥 Authors

Developed for **AIBC Capstone 2025**.  
Demonstrates practical use of LLMs and RAG for public digital services.

---
