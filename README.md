ConsultantGPT – Project Documentation

1. Overview
ConsultantGPT is a Streamlit-based AI assistant designed to help Data & AI interns or professionals break down business use cases into actionable technical tasks, suggest solution architectures, generate developer code modules, and recommend contextual learning resources. It leverages OpenAI's API (via LiteLLM and CrewAI) to produce outputs.

2. Project Structure
The repository is organized into the following files and folders:

ConsultantGPT/
│
├── app.py                   # Main Streamlit app entry point
├── modules/
│   ├── planner.py           # Generates technical tasks from a business use case
│   ├── architecture.py      # Internal architecture logic
│   ├── learning.py          # Suggests learning resources based on architecture
│   └── agents/
│       ├── architect_agent.py  # Wraps CrewAI/LLM call to generate architecture
│       └── developer_agent.py  # Wraps CrewAI/LLM call to generate developer code
│
├── .env                     # Stores API keys (not committed, add locally)
├── .gitignore               # Ensures .env and venv folders are ignored
└── README.md                # Documentation file (this)

3. Requirements
• Python 3.11 or above
• A virtual environment (venv or consult)
• Install dependencies using:

pip install -r requirements.txt
Example requirements.txt:
streamlit
python-dotenv
crewai
litellm
openai

4. Configuration
4.1. Create a .env file in the project root with the following content:

OPENAI_API_KEY=your_api_key_here
CREWAI_TRACING_ENABLED=true

4.2. Do not commit .env — it’s listed in .gitignore.

3.3. The app automatically loads your .env file for local development. If no key is present, you can also input the key at runtime in the UI.

5. Running the App
Activate your environment:
source consult/bin/activate   # or .venv depending on your setup

Run Streamlit:
streamlit run app.py

Open the app in your browser. Streamlit displays the link in your console.

6. How to Use
• Tab 1 – Use Case Planner: Enter a business use case and your OpenAI API key (if not in .env). Click 'Generate Technical Tasks'.
• Tab 2 – Architecture Designer: Select cloud providers and tools, then click 'Generate Architecture' to call the Architect Agent.
• Tab 3 – Developer Agent: Generate modular code based on your tasks and architecture.
• Tab 4 – Learning Resources: Get recommended learning content based on your generated architecture.

7. Contributing
• Fork the repository.
• Make changes in a feature branch.
• Open a pull request.

Never commit secrets — .env and API keys must stay local.

8. License
You may use MIT License or any other license as per your preference.
