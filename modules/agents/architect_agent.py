from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatOpenAI

def run_architect_agent(technical_tasks: str, cloud_stack: list, tools_stack: list, api_key: str):
    # ✅ Define LLM with user-provided API key
    llm = ChatOpenAI(temperature=0.4, model_name="gpt-3.5-turbo", openai_api_key=api_key)

    # ✅ Architect Agent using dynamic LLM
    architect = Agent(
        role="Cloud Architect",
        goal="Design a dynamic, layered architecture that fits the given technical tasks",
        backstory="You're an expert cloud solution architect skilled in customizing data pipelines per use case.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    prompt = f"""
You are a Cloud Solution Architect.

Design an end-to-end architecture **tailored** to the following technical tasks. 
DO NOT stick to fixed layers like Ingestion/Processing/Storage unless relevant.

Include only those components that are truly needed.

Use the cloud providers and tools listed if appropriate. Present the architecture using clear markdown with section headers like:

### Data Collection  
### Model Training  
### Monitoring  
...

---
Technical Tasks:
{technical_tasks}

Preferred Cloud: {', '.join(cloud_stack) or "Any"}
Preferred Tools: {', '.join(tools_stack) or "Any"}
---

Respond ONLY in Markdown.
"""

    task = Task(
        description=prompt,
        agent=architect,
        expected_output="Markdown-formatted architecture tailored to the use case"
    )

    crew = Crew(agents=[architect], tasks=[task], verbose=True)
    result = crew.kickoff()
    return getattr(result, "output", str(result)).strip()
