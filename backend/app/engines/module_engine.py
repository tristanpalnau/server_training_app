"""
Module execution engine.

This module provides minimal utilities for loading module content,
retrieving individual steps, and transforming raw step definitions
into frontend-ready payloads.

It is intentionally lightweight and stateless. Higher-level lesson
flow, persistence, and personalization are handled elsewhere.
"""
import json
import os
from typing import Dict


def load_module(filename: str) -> Dict:
    """
    Load a lesson module JSON file from disk for engine-based execution.

    This function is used by engine-driven flows and expects a full
    filename (including .json), unlike raw loaders that accept module IDs.
    """
    # Resolve module path relative to this file to avoid CWD dependence
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, "..", "content", "modules", filename)

    with open(full_path, "r") as file:
        return json.load(file)
    

def get_step(module: dict, index: int) -> dict:
    """
    Retrieve a specific step from a loaded module.

    This function performs no processing or mutation of the step.
    """
    steps = module["steps"]

    if index < 0 or index >= len(steps):
        raise IndexError(f"Step index {index} is out of range.")

    return steps[index]


def process_step(step: dict, **kwargs) -> dict:
    """
    Dispatch a raw step dictionary to the appropriate handler based on its type.

    This function acts as a router between step definitions and handler
    functions. It does not manage lesson flow or state.
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
    """Transform a text step into a frontend-ready payload."""
    return {
        "type": "text",
        "content": step["content"]
    }


def handle_reflection(step: dict) -> dict:
    """Transform a reflection step into a frontend-ready payload."""
    return {
        "type": "reflection",
        "prompt": step["prompt"]
    }


def handle_quiz(step: dict) -> dict:
    """
    Transform a quiz step into a frontend-ready payload.

    Only returns the quiz ID. The frontend is responsible for fetching
    quiz content from the quiz service.
    """
    return {
        "type": "quiz",
        "quiz_id": step["quiz_id"]
    }


def handle_quiz_result(step: dict, primary_style=None, strategist=None, guide=None, anchor=None, spark=None) -> dict:
    """
    Generate a quiz_result step payload using quiz outcome parameters.

    This handler expects quiz results to be passed via query parameters.
    This is MVP behavior and may be replaced by persisted quiz results
    in later phases.
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

