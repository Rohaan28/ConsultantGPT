# app.py
import os
from dotenv import load_dotenv
import streamlit as st

# ---- Load env first (so imports that read env are safe) ----
load_dotenv()  # reads OPENAI_API_KEY from a local .env if present

# Optional: prefer Streamlit Secrets in deployed environments
try:
    if "OPENAI_API_KEY" in st.secrets and st.secrets["OPENAI_API_KEY"]:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    # st.secrets may not exist locally; that's fine
    pass

# Now import app modules (these may create LLMs later)
from modules import planner, architecture, learning
from modules.agents.architect_agent import run_architect_agent
from modules.agents.developer_agent import run_developer_agent

# ---- Streamlit page config ----
st.set_page_config(page_title="ConsultantGPT", layout="wide")

# ---- Helpers ----
def ensure_openai_env_from_session():
    """
    Guarantee OPENAI_API_KEY is set for LiteLLM/CrewAI based on session_state.
    Call this before you invoke any agent/LLM code.
    """
    key = st.session_state.get("api_key", "")
    if key:
        os.environ["OPENAI_API_KEY"] = key
    return bool(os.getenv("OPENAI_API_KEY"))

# ---- Session state defaults ----
st.sidebar.markdown("🔍 **ConsultantGPT**")
st.sidebar.caption("Your AI Assistant for Data & AI Interns")

if "use_case" not in st.session_state:
    st.session_state.use_case = ""
if "technical_tasks" not in st.session_state:
    st.session_state.technical_tasks = ""
if "architecture_output" not in st.session_state:
    st.session_state.architecture_output = ""
if "cloud_stack" not in st.session_state:
    st.session_state.cloud_stack = []
if "tools_stack" not in st.session_state:
    st.session_state.tools_stack = []
if "api_key" not in st.session_state:
    # empty by default; user provides it once in Tab 1
    st.session_state.api_key = ""

# ---- Tabs ----
tab1, tab2, tab3, tab4 = st.tabs(
    ["🧠 Use Case Planner", "🏗️ Architecture Designer", "👷 Developer Agent", "📚 Learning Resources"]
)

# -------------------------------
# Tab 1: Use Case Planner
# -------------------------------
with tab1:
    st.subheader("🧠 Business Use Case to Technical Breakdown")

    st.session_state.use_case = st.text_area(
        "Describe your business use case:",
        placeholder="e.g., Build a real-time fraud detection system for a fintech app.",
        height=150,
        value=st.session_state.use_case,
    )

    # Enter key once. We keep the previous value so the user doesn't retype.
    entered_key = st.text_input(
        "🔑 Enter your OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        help="Your key is only kept in memory for this session and is not saved to disk."
    )
    if entered_key:
        st.session_state.api_key = entered_key
        os.environ["OPENAI_API_KEY"] = entered_key  # make it visible to LiteLLM immediately

    if st.button("Generate Technical Tasks"):
        if not st.session_state.use_case:
            st.error("❌ Please describe your business use case.")
        elif not st.session_state.api_key:
            st.error("❌ Please enter your OpenAI API key.")
        else:
            ensure_openai_env_from_session()
            with st.spinner("🛠️ Generating technical task breakdown..."):
                response = planner.generate_technical_tasks(
                    st.session_state.use_case,
                    st.session_state.api_key
                )
                st.session_state.technical_tasks = response
            st.markdown("#### ✅ Technical Task Breakdown")
            st.markdown(st.session_state.technical_tasks)

# -------------------------------
# Tab 2: Architecture Designer
# -------------------------------
with tab2:
    st.subheader("🏗️ Architecture Designer")

    if not st.session_state.technical_tasks:
        st.warning("⚠️ Please generate the technical tasks first in the 'Use Case Planner' tab.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.cloud_stack = st.multiselect(
                "☁️ Choose Cloud Providers:", ["AWS", "Azure", "GCP"], default=st.session_state.cloud_stack or ["AWS"]
            )
        with col2:
            st.session_state.tools_stack = st.multiselect(
                "🧰 Choose Tools:",
                ["S3", "DBT", "Power BI", "BigQuery", "Redshift"],
                default=st.session_state.tools_stack or ["DBT", "Power BI"]
            )

        if st.button("🚀 Generate Architecture via Agent"):
            if not st.session_state.api_key:
                st.error("❌ Please enter your OpenAI API key in the first tab.")
            else:
                ensure_openai_env_from_session()
                with st.spinner("Calling Architect Agent..."):
                    output = run_architect_agent(
                        st.session_state.technical_tasks,
                        st.session_state.cloud_stack,
                        st.session_state.tools_stack,
                        st.session_state.api_key
                    )
                    st.session_state.architecture_output = output
                st.markdown("### ✅ Suggested Architecture")
                st.markdown(st.session_state.architecture_output)
        elif st.session_state.architecture_output:
            st.markdown("### ✅ Last Generated Architecture")
            st.markdown(st.session_state.architecture_output)

# -------------------------------
# Tab 3: Developer Agent
# -------------------------------
with tab3:
    st.subheader("👷 Developer Agent")
    if not st.session_state.technical_tasks or not st.session_state.architecture_output:
        st.warning("⚠️ You need to generate both technical tasks and architecture first.")
    else:
        if st.button("🧑‍💻 Generate Developer Code"):
            if not st.session_state.api_key:
                st.error("❌ Please enter your OpenAI API key in the first tab.")
            else:
                ensure_openai_env_from_session()
                with st.spinner("Calling Developer Agent to code..."):
                    code_result = run_developer_agent(
                        st.session_state.technical_tasks,
                        st.session_state.architecture_output,
                        st.session_state.cloud_stack,
                        st.session_state.tools_stack,
                        st.session_state.api_key
                    )
                st.markdown("### 🧩 Generated Modular Code")
                st.code(code_result, language="python")

# -------------------------------
# Tab 4: Learning Resources
# -------------------------------
with tab4:
    st.subheader("📚 Learning Resources")
    if not st.session_state.architecture_output:
        st.warning("⚠️ Please generate your architecture first to get contextual learning resources.")
    else:
        if not st.session_state.api_key:
            st.warning("⚠️ Enter your OpenAI API key in the first tab to fetch learning resources.")
        else:
            ensure_openai_env_from_session()
            with st.spinner("🔍 Finding relevant learning resources..."):
                learning_output = learning.suggest_learning_resources(
                    st.session_state.architecture_output,
                    st.session_state.api_key
                )
            st.markdown(learning_output)
