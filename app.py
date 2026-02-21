"""
app.py — AccessLens Streamlit interface.

Minimal UI for educational benefit access scenario simulation.
Does not check eligibility, access government systems, or store data.
"""

import copy
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from llm_engine import generate_scenarios

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_SAMPLE_PERSONAS_PATH = Path(__file__).parent / "sample_personas.json"

SCHEME_CATEGORIES = [
    "Food & Nutrition",
    "Social Security / Pensions / DBT",
    "Employment & Wage Programs",
    "Health Insurance / Health-linked Benefits",
]

# Field labels for readable display of persona access conditions
FIELD_LABELS = {
    "information_awareness_level": "Information Awareness",
    "documentation_completeness": "Documentation Status",
    "digital_access_quality": "Digital Access Quality",
    "biometric_authentication_status": "Biometric Authentication",
    "mobility_and_distance_constraint": "Mobility & Distance",
    "local_institutional_support": "Local Institutional Support",
    "grievance_navigation_agency": "Grievance Navigation",
    "language_and_communication_barrier": "Language Barrier",
}

# Controlled What-If improvements: human label -> (field, improved enum value)
WHAT_IF_OPTIONS = {
    "Improved biometric reliability": (
        "biometric_authentication_status", "seamless_authentication"
    ),
    "Better digital access": (
        "digital_access_quality", "robust_digital_access"
    ),
    "Stronger local institutional support": (
        "local_institutional_support", "proactive_support"
    ),
    "Reduced mobility constraints": (
        "mobility_and_distance_constraint", "minimal_constraint"
    ),
    "Greater information awareness": (
        "information_awareness_level", "high_awareness"
    ),
}


@st.cache_data
def load_personas() -> list[dict]:
    return json.loads(_SAMPLE_PERSONAS_PATH.read_text(encoding="utf-8"))


def format_enum_value(value: str) -> str:
    """Convert snake_case enum values to readable title-case strings."""
    return value.replace("_", " ").title()


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AccessLens — Benefit Access Simulator",
    page_icon="🔍",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Header & disclaimer
# ---------------------------------------------------------------------------
st.title("🔍 AccessLens")
st.subheader("Benefit Access Risk Simulator · India")

st.warning(
    "**Educational Tool — Not an Eligibility Checker.** "
    "AccessLens shows how non-financial barriers can affect access to welfare benefits in India. "
    "It does not determine eligibility, connect to government systems, predict real outcomes, "
    "or provide legal advice. All generated scenarios are illustrative and non-deterministic.",
    icon="⚠️",
)

with st.expander("ℹ️ How to Use AccessLens", expanded=False):
    st.markdown(
        """
        **What is AccessLens?**
        AccessLens is an educational simulator that helps you explore how people face
        non-financial barriers — such as poor digital access, biometric issues, or language gaps —
        when trying to access welfare benefits in India. It does **not** check eligibility
        or make any real-world determinations.

        ---

        **Step-by-step guide:**

        1. **Select an Access Profile (Persona)** — Choose one of the pre-defined abstract
           profiles. Each represents a set of systemic access conditions, not a real individual.
        2. **Select a Scheme Category** — Pick the type of welfare benefit domain you want
           to simulate (e.g., food security, pensions, health insurance).
        3. **Click "Generate Access Scenarios"** — AccessLens will produce 2–4 plausible
           narratives showing how access might succeed, stall, or fail for that profile.
        4. **Optionally, use What-If mode** — Enable the toggle in the sidebar to explore
           how one improvement (e.g., better biometric reliability) might change the story.

        ---

        **What do the outputs mean?**
        - Each **trajectory** represents a common real-world pattern of access experience.
        - No single trajectory is guaranteed or presented as "most likely."
        - The tool generates multiple outcomes to highlight the range of possibilities.

        ---

        **Who is this tool for?**
        - 🏛️ **NGOs & civil society** — Understanding last-mile access failures
        - 🎓 **Students & researchers** — Studying welfare delivery barriers
        - 📋 **Policymakers** — Exploring systemic friction points
        - 💡 **Curious citizens** — Learning how benefit access challenges arise
        """
    )

st.divider()

# ---------------------------------------------------------------------------
# Sidebar: Simulation Inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Simulation Inputs")
    st.caption(
        "Select a profile and scheme category, then click Generate to run a simulation. "
        "Use the What-If toggle to explore how one improvement might change the narrative."
    )

    st.markdown("---")

    personas = load_personas()
    persona_labels = [p["label"] for p in personas]
    persona_map = {p["label"]: p for p in personas}

    selected_label = st.selectbox(
        "Access Profile (Persona)",
        options=persona_labels,
        help="Each persona represents an abstract set of access conditions, not a real individual.",
    )
    selected_scheme = st.selectbox(
        "Scheme Category",
        options=SCHEME_CATEGORIES,
        help="Select the welfare domain to simulate access barriers within.",
    )

    st.markdown("---")

    # What-If toggle
    st.markdown("#### What-If Exploration")
    st.caption(
        "Optionally simulate how one improvement to a friction point "
        "might change the access narrative. This is a **hypothetical only**."
    )

    enable_what_if = st.toggle(
        "What if one access barrier were improved?",
        value=False,
    )

    what_if_selection = None
    if enable_what_if:
        what_if_selection = st.selectbox(
            "Which barrier improves?",
            options=list(WHAT_IF_OPTIONS.keys()),
            help="The persona's profile is temporarily adjusted in-memory for this simulation only.",
        )
        st.info(
            "🔬 **Hypothetical Mode Active** — The scenario below reflects a modified "
            "profile and does not represent a real prediction or guarantee.",
            icon="🔬",
        )

    st.markdown("---")

    run_button = st.button(
        "Generate Access Scenarios",
        type="primary",
        use_container_width=True,
        help="Runs the AI simulation using the inputs above.",
    )

# ---------------------------------------------------------------------------
# Main panel: Access Conditions
# ---------------------------------------------------------------------------
selected_persona = persona_map[selected_label]

# Build the effective persona (with optional What-If modification)
effective_persona = copy.deepcopy(selected_persona)
what_if_label_applied = None

if enable_what_if and what_if_selection:
    field, improved_value = WHAT_IF_OPTIONS[what_if_selection]
    # Only highlight the change if it actually differs
    if effective_persona.get(field) != improved_value:
        effective_persona[field] = improved_value
        what_if_label_applied = (field, improved_value)

st.subheader(f"Access Profile: `{selected_label}`")
st.caption(selected_persona.get("description", ""))

st.markdown("#### Access Conditions")
st.caption(
    "These dimensions describe systemic and environmental friction, "
    "not personal characteristics or capabilities."
)

cols = st.columns(2)
schema_fields = [k for k in selected_persona if k not in ("label", "description")]

for i, field in enumerate(schema_fields):
    label = FIELD_LABELS.get(field, field.replace("_", " ").title())
    # Show effective (possibly modified) persona value
    value = format_enum_value(effective_persona[field])
    original_value = format_enum_value(selected_persona[field])

    if what_if_label_applied and field == what_if_label_applied[0]:
        # Visually flag the What-If change
        cols[i % 2].markdown(
            f"- **{label}**: ~~{original_value}~~ → **{value}** _(hypothetical)_"
        )
    else:
        cols[i % 2].markdown(f"- **{label}**: {value}")

st.divider()

# ---------------------------------------------------------------------------
# Scenario generation
# ---------------------------------------------------------------------------
if run_button:
    mode_label = "Hypothetical What-If Simulation" if what_if_label_applied else "Access Scenario Simulation"
    with st.spinner(f"Running {mode_label}…"):
        try:
            output = generate_scenarios(
                persona=effective_persona,
                scheme_category=selected_scheme,
            )

            st.subheader("Simulated Access Scenarios")

            if what_if_label_applied:
                field_label = FIELD_LABELS.get(
                    what_if_label_applied[0],
                    what_if_label_applied[0].replace("_", " ").title(),
                )
                improved_value_label = format_enum_value(what_if_label_applied[1])

                # --- Contrast framing section ---
                st.markdown("#### What Changed in This Simulation _(Hypothetical)_")
                st.info(
                    f"In this hypothetical simulation, one access barrier has been assumed "
                    f"to improve compared to the baseline scenario.\n\n"
                    f"Specifically, **{field_label}** is treated as more favourable "
                    f"(*{improved_value_label}*). "
                    f"All other access conditions remain unchanged from the original profile.\n\n"
                    f"_This comparison is illustrative only. It does not represent a real "
                    f"prediction, guarantee, or assessment of eligibility._",
                    icon="🔬",
                )
                st.divider()

            st.markdown(output)

        except Exception as exc:
            st.error(
                "The scenario generation could not be completed. "
                "Please verify your API key and connection.\n\n"
                f"**Details:** {exc}"
            )
