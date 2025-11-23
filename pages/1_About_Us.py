import streamlit as st

st.title("📘 About This Project")

st.markdown("""
## **🔍 Project Scope**

This project is developed as part of the *AIBC 2025 Capstone* to demonstrate how AI, 
retrieval systems, and modern web interfaces can help citizens better understand complex 
government processes—specifically, **CPF retirement policies in Singapore**.

CPF policies affect everyday decisions such as:
- Retirement planning  
- Age 55 withdrawal rules  
- Housing purchases  
- Top-ups and contribution strategies  
- CPF LIFE payouts  

However, many citizens find CPF information fragmented or difficult to interpret.  
This prototype aims to bring clarity, personalization, and ease of exploration to CPF topics.

---

## **🎯 Objectives**

This application is designed with four core objectives:

### **1. Consolidate Information**
Provide a unified reference by drawing from a curated set of publicly available CPF materials  
(e.g., Retirement Sums, CPF LIFE, Withdrawals at 55, Interest rates).

### **2. Personalize User Experience**
Allow citizens to enter *simple, non-identifiable inputs* (age, CPF savings, planned retirement age)  
and receive tailored explanations grounded in policy.

### **3. Enhance Understanding**
Use:
- Retrieval-Augmented Generation (RAG)  
- Visualisations  
- Scenario-based simulations  

…to help users grasp how CPF rules apply to real-life decisions.

### **4. Present Information Effectively**
Display insights through:
- Clear explanations in plain English  
- Tables and structured formatting  
- Graphs and scenario cards  
- Follow-up question support

All generated information is accompanied by disclaimers.

---

## **📦 Key Features**

### **✔ Use Case 1 — CPF Policy Explainer (Chat with RAG)**
Users can ask questions such as:
- “What is the Full Retirement Sum?”  
- “How much can I withdraw at age 55?”  
- “What happens to my OA and SA before CPF LIFE starts?”

The system:
- Retrieves relevant CPF text from the curated corpus  
- Uses the LLM to generate grounded explanations  
- Incorporates user context (age, income band)  
- Offers follow-up Q&A within the same session  

### **✔ Use Case 2 — Retirement Planning Simulator**
Users can simulate future CPF savings using inputs like:
- Current age  
- Planned retirement age  
- Monthly CPF contribution  
- Contribution growth  
- Current CPF savings  

The simulator:
- Projects future CPF balances  
- Compares them to BRS / FRS / ERS  
- Visualizes yearly growth  
- Generates an LLM explanation to interpret results  

---

## **📚 Data Sources**

All information used in the RAG system comes from **publicly available CPF resources**, manually curated into Markdown format:

- CPF Retirement Sums (BRS / FRS / ERS)  
- Withdrawals at age 55 and FAQs  
- CPF LIFE overview and payout rules  
- Top-up schemes and interest rates  
- Contribution rate tables (age-banded)  
- Housing usage rules and RA formation  

No real-time scraping is used.  
No personal data is stored or processed.

---

## **🛠️ Technologies Used**

- **Streamlit** for the web interface  
- **Python** backend with modular architecture  
- **OpenAI API** for LLM reasoning and embeddings  
- **Manual Markdown corpus** + **JSONL vector store** for retrieval  
- **Matplotlib** for CPF growth visualisations  

---

## **⚠️ Important Notes**

This prototype is built **purely for educational demonstration**.  
Information may be simplified, and model-generated responses may contain inaccuracies.  
Users should always refer to official CPF calculators and statements for real decisions.

---
""")
