import streamlit as st
import os
from openai import OpenAI
from guard import AgentMoatGuard

# Set up the web page layout
st.set_page_config(page_title="AgentMoat Enterprise Gateway", page_icon="🛡️", layout="centered")

st.title("🛡️ AgentMoat Security Gateway")
st.markdown("""
This dashboard demonstrates a **Real-World Secure AI Gateway**. 
It acts as a reverse-proxy firewall intercepting prompts *before* they can exploit or consume tokens on your live LLM deployment.
""")

# Cache the guard initialization so it only loads the model ONCE when the app boots up
@st.cache_resource
def load_security_guard():
    return AgentMoatGuard()

with st.spinner("🧠 Booting up local embedding engine & connecting to ChromaDB..."):
    guard = load_security_guard()

st.write("---")

# Sidebar for interactive configurations
st.sidebar.header("⚙️ Gateway Calibration")

# OpenAI API Key Configuration input
openai_api_key = st.sidebar.text_input(
    "🔑 OpenAI API Key", 
    type="password", 
    placeholder="sk-...",
    help="Enter your OpenAI API key to simulate a real-world response generation for safe prompts."
)

threshold_val = st.sidebar.slider(
    "Sensitivity Threshold (Distance)", 
    min_value=0.1, 
    max_value=1.5, 
    value=0.85, 
    step=0.05,
    help="Lower distance means strict checking. 0.85 is recommended."
)

st.sidebar.markdown("""
💡 **Production Value Proposition:**
1. **Cost Savings:** Blocks malicious token spam at the edge.
2. **Context Safety:** Keeps system prompt parameters completely private.
""")

# Main Chat Interface Input
user_input = st.text_area(
    "💬 Live App User Prompt:", 
    placeholder="Type something completely innocent or try a malicious system jailbreak...",
    height=120
)

if st.button("Execute Secure Request 🚀", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please input a prompt to scan.")
    else:
        # Step 1: Intercept prompt with our semantic firewall
        with st.spinner("🕵️‍♂️ Intercepting & scanning prompt semantics..."):
            is_blocked = guard.inspect_prompt(user_input, threshold=threshold_val)
            
        st.subheader("Security Enforcement Status")
        
        if is_blocked:
            st.error("🚨 **[ACCESS DENIED] Malicious Payload Blocked at Edge!**")
            st.markdown(
                "**Reason:** Semantic alignment matches known adversarial prompt injection profiles. "
                "The transaction was dropped **before** hitting downstream cloud model endpoints to protect context privacy and save API costs."
            )
        else:
            st.success("✅ **[CLEARED] Prompt Verified Safe.**")
            st.markdown("Forwarding payload down the network stack to OpenAI pipeline...")
            
            # Step 2: Pass cleanly through the firewall to the live model if key exists
            if not openai_api_key:
                st.info("ℹ️ Prompt passed! Provide an OpenAI API key in the sidebar to see it generate a real-world response live.")
            else:
                with st.spinner("🤖 Fetching live model completion response..."):
                    try:
                        # Initialize OpenAI Client dynamically
                        client = OpenAI(api_key=openai_api_key)
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",  # Highly efficient, cost-effective model
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": user_input}
                            ],
                            max_tokens=300
                        )
                        
                        # Render the output
                        st.subheader("🤖 Live LLM Output Response")
                        st.write(response.choices[0].message.content)
                        
                    except Exception as e:
                        st.error(f"❌ OpenAI Gateway Error: {e}")