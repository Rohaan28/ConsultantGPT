import streamlit as st
from modules import planner, architecture, learning
from modules.agents.architect_agent import run_architect_agent
from modules.agents.developer_agent import run_developer_agent

# Set Streamlit page config
st.set_page_config(page_title="ConsultantGPT", layout="wide")

# Sidebar
st.sidebar.markdown("🔍 **ConsultantGPT**")
st.sidebar.caption("Your AI Assistant for Data & AI Interns")

# Initialize session state
if "technical_tasks" not in st.session_state:
    st.session_state.technical_tasks = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "architecture_output" not in st.session_state:
    st.session_state.architecture_output = ""
if "cloud_stack" not in st.session_state:
    st.session_state.cloud_stack = []
if "tools_stack" not in st.session_state:
    st.session_state.tools_stack = []

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Use Case Planner", 
    "🏗️ Architecture Designer", 
    "👷 Developer Agent", 
    "📚 Learning Resources"
])

# -------------------------------
# Tab 1: Use Case Planner
# -------------------------------
with tab1:
    st.subheader("🧠 Business Use Case to Technical Breakdown")

    use_case = st.text_area(
        "Describe your business use case:",
        placeholder="e.g., Build a real-time fraud detection system for a fintech app.",
        height=150,
        value=st.session_state.get("use_case", "")  # 🔧 Load old value
    )
    st.session_state.api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

    if st.button("Generate Technical Tasks"):
        if not use_case or not st.session_state.api_key:
            st.error("❌ Please enter both a use case and your OpenAI API key.")
        else:
            with st.spinner("🛠️ Generating technical task breakdown..."):
                response = planner.generate_technical_tasks(use_case, st.session_state.api_key)
                st.session_state.use_case = use_case               # 🔧 Save use_case
                st.session_state.technical_tasks = response        # 🔧 Save plan
            st.markdown("#### ✅ Technical Task Breakdown")
            st.markdown(response)

# -------------------------------
# Tab 2: Architecture Designer
# -------------------------------
with tab2:
    st.subheader("🏗️ Architecture Designer")
    if st.session_state.technical_tasks:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.cloud_stack = st.multiselect("☁️ Choose Cloud Providers:", ["AWS", "Azure", "GCP"], default=["AWS"])
        with col2:
            st.session_state.tools_stack = st.multiselect("🧰 Choose Tools:", ["S3", "DBT", "Power BI", "BigQuery", "Redshift"], default=["DBT", "Power BI"])

        if st.button("🚀 Generate Architecture via Agent"):
            with st.spinner("Calling Architect Agent..."):
                output = run_architect_agent(st.session_state.technical_tasks, st.session_state.cloud_stack, st.session_state.tools_stack, st.session_state.api_key)
                st.session_state.architecture_output = output
                st.markdown("### ✅ Suggested Architecture")
                st.markdown(output)
        elif st.session_state.architecture_output:
            st.markdown("### ✅ Last Generated Architecture")
            st.markdown(st.session_state.architecture_output)
    else:
        st.warning("⚠️ Please generate the technical tasks first in the 'Use Case Planner' tab.")

# -------------------------------
# Tab 3: Developer Agent
# -------------------------------
with tab3:
    st.subheader("👷 Developer Agent")
    if st.session_state.technical_tasks and st.session_state.architecture_output:
        if st.button("🧑‍💻 Generate Developer Code"):
            with st.spinner("Calling Developer Agent to code..."):
                code_result = run_developer_agent(
                    st.session_state.technical_tasks,
                    st.session_state.architecture_output,
                    st.session_state.cloud_stack,
                    st.session_state.tools_stack,
                    st.session_state.api_key
                )
                st.markdown("### 🧩 Generated Modular Code")
                st.code(code_result)
    else:
        st.warning("⚠️ You need to generate both technical tasks and architecture first.")

# -------------------------------
# Tab 4: Learning Resources
# -------------------------------
with tab4:
    st.subheader("📚 Learning Resources")

    if st.session_state.architecture_output:
        with st.spinner("🔍 Finding relevant learning resources based on your architecture..."):
            learning_output = learning.suggest_learning_resources(
                st.session_state.architecture_output,
                st.session_state.api_key
            )
            st.markdown(learning_output)
    else:
        st.warning("⚠️ Please generate your architecture first to get contextual learning resources.")
