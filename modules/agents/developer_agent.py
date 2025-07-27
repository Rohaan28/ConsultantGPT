from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatOpenAI
import re

def extract_sections_from_architecture(architecture_summary):
    architecture_markdown = str(architecture_summary)
    section_headers = re.findall(r"(?<=### )[\w\s/()\-]+", architecture_markdown)
    return section_headers

def clean_llm_output(output):
    if not output or "I now can give a great answer" in output or "No real code" in output:
        return "# ⚠️ No real code was generated. Please refine input."
    return output.strip()

def run_developer_agent(technical_tasks: str, architecture_summary: str, cloud_stack: list, tools_stack: list, api_key: str):
    # 🔑 Create a fresh LLM with user's API key
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-4", openai_api_key=api_key)

    # 👷 Create Developer Agent dynamically
    developer = Agent(
        role="Cloud Data Developer",
        goal="Generate clean, working Python or SQL code for each section of a cloud data pipeline",
        backstory="You're a Python backend developer who builds modular data workflows using pandas, dbt, SQL, boto3, etc.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 📎 Extract sections from architecture
    sections = extract_sections_from_architecture(architecture_summary)
    architecture_text = str(architecture_summary)
    full_code_output = ""

    # 🧠 Loop through each architecture section
    for section in sections:
        base_prompt = f"""
You are a backend data engineer.

Your task is to write **real, working Python or SQL code** that implements the **{section}** part of the data architecture below.

💡 Guidelines:
- Use the provided tools and cloud stack: {', '.join(cloud_stack)} and {', '.join(tools_stack)}.
- Refer to the technical tasks and architecture to understand what to build.
- ONLY output valid Python/SQL code. Do not include reasoning.
- If the section doesn’t require actual code (e.g. it's a BI tool setup), just write a comment like:
  `# Skipped - configuration or manual step.`

---
Technical Tasks:
{technical_tasks}

Architecture Summary:
{architecture_summary}
---

Write production-level code that a real developer would contribute to a repo.
"""

        task = Task(
            description=base_prompt,
            agent=developer,
            expected_output=f"Python or SQL code for {section}"
        )

        crew = Crew(agents=[developer], tasks=[task], verbose=True)
        result = crew.kickoff()

        raw_output = getattr(result, "output", str(result)).strip()
        final_output = clean_llm_output(raw_output)

        full_code_output += f"### 🔹 {section} Code\n```python\n{final_output}\n```\n\n"

    return full_code_output
