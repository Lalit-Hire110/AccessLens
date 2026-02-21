"""
llm_engine.py — AccessLens core LLM runtime.

Loads prompt files from disk and calls the Groq API to generate
educational, non-deterministic access scenarios.

Constraints enforced:
- No persona data is logged.
- No conversation state is retained.
- API key is sourced exclusively from the environment.
- Prompt files are loaded from disk; never inlined.
"""

import json
import os
from pathlib import Path

from groq import Groq

# Resolve paths relative to this file so the module is location-agnostic.
_BASE_DIR = Path(__file__).parent
_SYSTEM_PROMPT_PATH = _BASE_DIR / "system_prompt.txt"
_SCENARIO_PROMPT_PATH = _BASE_DIR / "scenario_generation_prompt.txt"

# Model identifier — change here only if the model name changes upstream.
_MODEL = "llama-3.3-70b-versatile"


def _load_file(path: Path) -> str:
    """Read a text file and return its contents, raising clearly on failure."""
    if not path.exists():
        raise FileNotFoundError(f"Required prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def generate_scenarios(persona: dict, scheme_category: str) -> str:
    """
    Generate educational access scenarios for the given persona and scheme.

    Parameters
    ----------
    persona : dict
        A persona object conforming to persona_schema.json.
        Passed verbatim to the LLM; no summarisation is applied.
    scheme_category : str
        One of: "Food & Nutrition", "Social Security / Pensions / DBT",
        "Employment & Wage Programs", "Health Insurance / Health-linked Benefits".

    Returns
    -------
    str
        The raw text output from the LLM.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY environment variable is not set. "
            "Export it before running AccessLens."
        )

    system_prompt = _load_file(_SYSTEM_PROMPT_PATH)
    scenario_template = _load_file(_SCENARIO_PROMPT_PATH)

    # Inject persona and scheme into the scenario prompt.
    persona_json = json.dumps(persona, indent=2)
    user_message = scenario_template.replace(
        "[Insert Persona JSON here]", persona_json
    ).replace(
        "[Insert Scheme Category here]", scheme_category
    )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
