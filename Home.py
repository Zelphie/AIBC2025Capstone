import os
import streamlit as st

st.set_page_config(
    page_title="Gov Info Companion",
    page_icon="🏛️",
    layout="wide",
)

PASSWORD = os.getenv("APP_PASSWORD")

if PASSWORD:
    pw = st.text_input("Enter password to access:", type="password")
    if pw != PASSWORD:
        st.stop()

st.set_page_config(
    page_title="CPF Information Companion",
    page_icon="🏛️",
    layout="wide",
)

st.title("🏛️ CPF Information Companion")
st.markdown("""
Welcome to the **CPF Information Companion**, an interactive educational tool created as part of the  
*AIBC Capstone 2025*. This prototype is designed to help Singaporeans and PRs better understand  
important CPF retirement policies through two key features:

### **1️⃣ Policy Explainer (Chat with RAG)**
Ask natural-language questions — such as *“What is the FRS?”* or  
*“How much can I withdraw at age 55?”* — and get grounded explanations based on curated CPF material.

### **2️⃣ Retirement Planning Simulator**
Run a simple CPF retirement projection using inputs such as age, savings, and contributions, and see  
how your results compare to **BRS / FRS / ERS**, along with an LLM-generated explanation.

---

## 🔒 DISCLAIMER

""")

with st.expander("⚠️ IMPORTANT NOTICE — Please Read Before Using This App", expanded=False):
    st.markdown("""
This web application is a **prototype for educational purposes only**.

- The information presented is **not intended for real-world usage**.  
- Do **not** rely on any output for financial, legal, or healthcare-related decisions.  
- The LLM may generate **inaccurate or incomplete information**.  
- No personalised financial advice is provided.  

Always verify important decisions using **official CPF tools**, statements, and professional advisors.
""")

st.markdown("""
---

## 🚀 Getting Started

Use the sidebar on the left to navigate to:
- **Policy Explainer**  
- **Retirement Simulator**  
- **About Us**  
- **Methodology**

Each page includes descriptions and guidance to help you explore CPF-related topics safely and clearly.

---

## 🧭 How the App Works

This tool combines:
- A **hand-curated knowledge base** of CPF policies  
- A **vector store** for retrieval  
- **OpenAI LLMs** for generating grounded explanations  
- **Streamlit** for interactivity, charts, and UI  

The goal is to demonstrate how AI + structured information can make complex policies easier to understand.

---
""")
