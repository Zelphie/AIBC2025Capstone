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
    page_title="Gov Info Companion",
    page_icon="🏛️",
    layout="wide",
)

st.title("🏛️ Gov Info Companion")
st.write(
    """
    Welcome! This app helps citizens explore CPF-related policies 
    and simulate retirement scenarios in a simple, interactive way.
    """
)

# ======================
# 🔻 Mandatory Disclaimer
# ======================
with st.expander("⚠️ IMPORTANT NOTICE (Click to expand)"):
    st.error(
        """
        **IMPORTANT NOTICE:**  
        This web application is a prototype developed for educational purposes only.  
        The information provided here is **NOT** intended for real-world usage and  
        should **not** be relied upon for making any decisions, especially those  
        related to **financial, legal, or healthcare matters**.

        Furthermore, please be aware that the LLM may generate **inaccurate or incorrect information**.  
        You assume full responsibility for how you use any generated output.

        Always consult with **qualified professionals** for accurate and personalized advice.
        """
    )

st.info(
    "Use the navigation menu on the left to explore the two main use cases, "
    "and read more about the project in the **About Us** and **Methodology** pages."
)
