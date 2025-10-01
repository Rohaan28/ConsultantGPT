# ConsultantGPT

An AI-powered Streamlit app to help Data & AI interns (and pros) turn business use cases into:  
- actionable **technical task plans**  
- **solution architectures**  
- **developer code modules**  
- tailored **learning resources**  

Powered by OpenAI (via LiteLLM & CrewAI).  

---

## 1) Overview  
ConsultantGPT lets you describe a use case in plain English and then:  
1. Produces a technical task breakdown.  
2. Suggests a cloud/tooling architecture.  
3. Generates modular starter code.  
4. Recommends learning resources based on the chosen stack.  

---

## 2) Project Structure  

```text
ConsultantGPT/
│
├─ app.py                         # Main Streamlit app
├─ modules/
│  ├─ planner.py                  # Generates technical tasks from a business use case
│  ├─ architecture.py             # Architecture helper logic
│  ├─ learning.py                 # Learning resources recommender
│  └─ agents/
│     ├─ architect_agent.py       # CrewAI-based architecture agent
│     └─ developer_agent.py       # CrewAI-based developer/code agent
│
├─ .env                           # Local secrets (NOT committed)
├─ .gitignore                     # Ignores .env, venv, etc.
└─ README.md                      # This file
```

---

## 3) Requirements  

- Python **3.11+**  
- Virtual environment (`venv`, `.consult`, etc.)  

Install dependencies:  

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
streamlit
python-dotenv
crewai
litellm
openai
```

---

## 4) Configuration  

Create a `.env` file in the project root (do **not** commit this):  

```env
OPENAI_API_KEY=your_api_key_here
CREWAI_TRACING_ENABLED=true
```

The app loads `.env` automatically for local development.  
If no key is present, you can also paste your key into **Tab 1** inside the app.

---

## 5) Running the App  

Activate your environment (example):  

```bash
# macOS/Linux
source consult/bin/activate

# Windows PowerShell
.\consult\Scripts\Activate
```

Start Streamlit:  

```bash
streamlit run app.py
```

Open the link displayed in your terminal to launch the app in your browser.

---

## 6) How to Use  

**Tab 1 – Use Case Planner**  
Describe your business use case and (optionally) provide your OpenAI API key. Click **Generate Technical Tasks**.

**Tab 2 – Architecture Designer**  
Pick cloud(s) and tools, then click **Generate Architecture** to call the Architect Agent.

**Tab 3 – Developer Agent**  
Generate modular starter code based on the tasks + architecture.

**Tab 4 – Learning Resources**  
Get learning resources relevant to the proposed architecture and tools.

---

## 7) Contributing  

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Open a pull request  

**Never commit secrets** — keep `.env` local.

---

## 8) License  

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
