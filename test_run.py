"""
test_run.py — Local verification harness for AccessLens LLM engine.

Loads the first persona from sample_personas.json and runs a single
scenario generation call. For local testing only; not for production use.
"""

import json
from pathlib import Path

from dotenv import load_dotenv
from llm_engine import generate_scenarios

_SAMPLE_PERSONAS_PATH = Path(__file__).parent / "sample_personas.json"
_SCHEME_CATEGORY = "Social Security / Pensions / DBT"


def main() -> None:
    load_dotenv()
    personas = json.loads(_SAMPLE_PERSONAS_PATH.read_text(encoding="utf-8"))
    persona = personas[0]

    print(f"Running scenario generation for persona: {persona['label']}")
    print(f"Scheme category: {_SCHEME_CATEGORY}")
    print("-" * 60)

    output = generate_scenarios(persona=persona, scheme_category=_SCHEME_CATEGORY)
    print(output)


if __name__ == "__main__":
    main()
