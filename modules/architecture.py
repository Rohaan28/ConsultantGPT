import streamlit as st
import openai

def generate_architecture_ui(tech_breakdown):
    st.markdown("### 📋 Technical Task Breakdown")
    st.text_area("Received Technical Tasks", tech_breakdown, height=250, disabled=True)

    st.markdown("### 🛠️ Choose Your Stack")

    cloud_providers = st.multiselect(
        "Select cloud provider(s):",
        ["AWS", "Azure", "GCP"],
        default=["AWS"]
    )

    tools = st.multiselect(
        "Select tools and platforms you'd like to include:",
        [
            "Snowflake", "BigQuery", "Power BI", "Tableau", "Looker",
            "dbt", "Apache Kafka", "Apache Airflow", "Databricks",
            "Redshift", "Synapse", "Delta Lake", "S3", "Google Cloud Storage"
        ],
        default=["dbt", "Power BI"]
    )

    api_key = st.session_state.get("api_key", "")
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please enter it in the Use Case Planner tab.")
        return

    if st.button("🚀 Generate Architecture"):
        try:
            client = openai.OpenAI(api_key=api_key)

            full_prompt = f"""
You are a cloud data architect. Based on the following technical breakdown and user preferences, suggest a modern cloud-based data architecture.

Technical Tasks:
{tech_breakdown}

Cloud Preferences: {", ".join(cloud_providers) if cloud_providers else "No preference"}
Tool Preferences: {", ".join(tools) if tools else "No preference"}

Return a structured description of the architecture, tools used at each layer (ingestion, processing, storage, visualization), and reasoning behind choices.
"""

            with st.spinner("🔧 Designing architecture..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a senior cloud data architect with experience in building scalable data platforms."
                        },
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.5
                )

            st.session_state.architecture_output = response.choices[0].message.content
            st.markdown("### 🧱 Suggested Cloud Architecture")
            st.markdown(st.session_state.architecture_output)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
