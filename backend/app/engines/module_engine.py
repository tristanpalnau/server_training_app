import json
import os
from typing import Dict


def load_module(filename: str) -> Dict:
    """
    Load a lesson module JSON file from /content/modules/.

    Parameters
    ----------
    filename : str
        The module file name, e.g. "lesson_1.json".

    Returns
    -------
    dict
        Parsed module data containing:
        - id
        - title
        - steps (list of step dictionaries)
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, "..", "content", "modules", filename)

    with open(full_path, "r") as file:
        return json.load(file)
    

def get_step(module: dict, index: int) -> dict:
    """
    Retrieve a specific step from a loaded module.

    Parameters
    ----------
    module : dict
        The module dictionary returned by load_module().
    index : int
        The zero-based index of the step to retrieve.

    Returns
    -------
    dict
        The step dictionary for the requested index.

    Raises
    ------
    IndexError
        If the index is outside the range of available steps.
    """
    steps = module["steps"]

    if index < 0 or index >= len(steps):
        raise IndexError(f"Step index {index} is out of range.")

    return steps[index]


def process_step(step: dict, **kwargs) -> dict:
    """
    Route a step dictionary to the correct handler function based on 'type'.

    Parameters
    ----------
    step : dict
        A single step from the module's 'steps' list.

    Returns
    -------
    dict
        A standardized, backend-ready step dictionary for the frontend.
    """
    step_type = step.get("type")

    if step_type == "text":
        return handle_text(step)

    elif step_type == "reflection":
        return handle_reflection(step)

    elif step_type == "quiz":
        return handle_quiz(step)

    elif step_type == "quiz_result":
        return handle_quiz_result(step, **kwargs)

    else:
        raise ValueError(f"Unknown step type: {step_type}")


def handle_text(step: dict) -> dict:
    """Return a simple text step."""
    return {
        "type": "text",
        "content": step["content"]
    }


def handle_reflection(step: dict) -> dict:
    """Return a reflection prompt step."""
    return {
        "type": "reflection",
        "prompt": step["prompt"]
    }


def handle_quiz(step: dict) -> dict:
    """
    Minimal quiz handler.
    Returns only the quiz ID.
    The frontend will request the quiz content from /quiz/<id>/content.
    """
    return {
        "type": "quiz",
        "quiz_id": step["quiz_id"]
    }


def handle_quiz_result(step: dict, primary_style=None, strategist=None, guide=None, anchor=None, spark=None) -> dict:
    """
    Inserts quiz results into the quiz_result step.
    primary_style is REQUIRED.
    Breakdown counts are optional.
    """

    # If frontend didn't provide a style, show an error (expected MVP behavior).
    if primary_style is None:
        return {
            "type": "quiz_result",
            "error": "Missing primary_style. Quiz results must be passed as query parameters."
        }

    # Optional breakdown (only included if provided).
    breakdown = {}

    if strategist is not None:
        breakdown["strategist"] = strategist
    if guide is not None:
        breakdown["guide"] = guide
    if anchor is not None:
        breakdown["anchor"] = anchor
    if spark is not None:
        breakdown["spark"] = spark

    return {
        "type": "quiz_result",
        "primary_style": primary_style,
        "breakdown": breakdown if breakdown else None
    }

