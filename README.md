# AccessLens

**Benefit Access Risk Simulator — India**

AccessLens is an educational Streamlit application that simulates how non-financial barriers affect people's ability to access welfare benefits in India. It uses an LLM (Groq / Llama 3.3 70B) to generate plausible, illustrative access scenarios based on abstract user profiles called *personas*.

> **This is not an eligibility checker.** AccessLens does not connect to government systems, determine eligibility, or provide legal advice. All generated scenarios are fictional and for educational purposes only.

---

## What It Does

Given an abstract *access profile* (a set of systemic frictions like poor digital access, biometric issues, or documentation gaps) and a welfare *scheme category*, AccessLens generates 2–4 narrative trajectories showing how access might succeed, stall, or fail through the delivery chain.

It also includes a **What-If mode**: hypothetically improve one access barrier and see how the simulated narrative changes.

---

## Access Profiles (Personas)

Each persona represents a set of environmental and systemic conditions — not a real individual. The dimensions assessed are:

| Dimension | Description |
|---|---|
| Information Awareness | Awareness of available schemes |
| Documentation Status | Completeness of required documents |
| Digital Access Quality | Quality of internet / device access |
| Biometric Authentication | Reliability of fingerprint/iris auth |
| Mobility & Distance | Physical access constraints |
| Local Institutional Support | Support from local bodies / CSCs |
| Grievance Navigation | Ability to resolve access failures |
| Language Barrier | Communication friction at service points |

---

## Scheme Categories

- Food & Nutrition
- Social Security / Pensions / DBT
- Employment & Wage Programs
- Health Insurance / Health-linked Benefits

---

## Project Structure

```
AccessLens/
├── app.py                        # Streamlit UI and application logic
├── llm_engine.py                 # Groq API integration and scenario generation
├── system_prompt.txt             # LLM system role and safety constraints
├── scenario_generation_prompt.txt # Structured prompt template for scenarios
├── persona_schema.json           # JSON schema defining persona dimensions
├── sample_personas.json          # Pre-defined abstract access profiles
├── test_run.py                   # Manual test script for the LLM engine
└── .env                          # API key (not committed — see .gitignore)
```

---

## Setup & Running

### 1. Clone the repository

```bash
git clone https://github.com/Lalit-Hire110/AccessLens.git
cd AccessLens
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS / Linux
```

### 3. Install dependencies

```bash
pip install streamlit groq python-dotenv
```

### 4. Set up the API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

### 5. Run the app

```bash
streamlit run app.py
```

---

## LLM Configuration

| Parameter | Value |
|---|---|
| Provider | Groq |
| Model | `llama-3.3-70b-versatile` |
| Temperature | 0.7 |

The model, system prompt, and scenario template are all configurable via plain text files — no code changes needed for prompt iteration.

---

## Safety & Design Constraints

The LLM engine enforces these constraints at the prompt level:

- No eligibility decisions or determinations
- No connection to official government data or registries
- No probability scores or deterministic outcome predictions
- No inference of religion, caste, or specific identity markers
- No legal thresholds, cutoff dates, or specific income rules
- All outputs framed in illustrative, third-person language

---

## Who Is This For

- **NGOs and civil society** studying last-mile access failures
- **Students and researchers** exploring welfare delivery barriers
- **Policymakers** examining systemic friction points in benefit delivery
- **Curious citizens** learning how access challenges arise in practice

---

## License

This project is released for educational and research purposes.
