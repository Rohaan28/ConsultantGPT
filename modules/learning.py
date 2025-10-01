import openai
import streamlit as st

def suggest_learning_resources(architecture_output, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""
You are a career mentor for Data and AI professionals.

Given the following cloud data architecture design, suggest a curated list of learning resources that a data or AI intern can use to master the technologies mentioned in the architecture.

Architecture Description:
\"\"\"
{architecture_output}
\"\"\"

Provide 5–8 bullet points that cover learning resources like tutorials, courses, or documentation for specific tools and technologies mentioned in the architecture (e.g., Snowflake, dbt, Power BI, AWS S3, etc.).

Your output should be grouped by technology and contain:
- Tool/tech name (bold)
- 1-2 resource links with short descriptions

Avoid generic resources. Focus only on tools or platforms explicitly mentioned in the architecture text above.
"""

        with st.spinner("🎓 Gathering tailored learning resources..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful Data & AI mentor providing curated learning resources."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4
            )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error:\n\n{str(e)}"
