import json
import os
from typing import List, Dict


def load_quiz(filename: str) -> dict:
    """
    Load a quiz JSON file from the /content/quizzes/ directory.

    This function is purely responsible for file loading and path resolution.
    It should not contain any scoring logic, formatting logic, or API concerns.

    Parameters
    ----------
    filename : str
        The name of the quiz file (e.g., "server_style.json").

    Returns
    -------
    dict
        The parsed quiz data as a Python dictionary.

    Notes
    -----
    - The path is resolved relative to this engine file, so this function
      works regardless of where the application is run from.
    - This is intentionally backend-only logic and does not sanitize or
      hide scoring metadata; routers handle that.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, "..", "content", "quizzes", filename)

    with open(full_path, "r") as file:
        return json.load(file)


def calculate_result(style_counts: Dict[str, int]) -> str:
    """
    Determine the user's primary style based on accumulated style counts.

    Parameters
    ----------
    style_counts : dict[str, int]
        A dictionary mapping style names to how many times each occurred.

    Returns
    -------
    str
        The style with the highest count.

    Notes
    -----
    - Because the MVP uses an odd number of questions, ties are impossible.
    - This function does not know which quiz is being used or how many styles exist;
      it simply finds the max value.
    """
    return max(style_counts, key=style_counts.get)


def run_quiz(filename: str, user_answers: List[int]) -> dict:
    """
    Evaluate a quiz submission and return style results.

    This is the core quiz scoring engine. It loads quiz content, matches each
    user-selected answer to its corresponding style tag, tallies the results, and
    determines the primary style.

    Parameters
    ----------
    filename : str
        The quiz file to load.
    user_answers : list[int]
        A list of answer indices from the frontend. Each index corresponds to the
        chosen answer for each question, in order. Example: [0, 2, 1, 3, 0]

    Returns
    -------
    dict
        {
            "primary_style": str,
            "breakdown": {style_name: count, ...}
        }

    Notes
    -----
    - The length of user_answers must match the number of questions in the quiz.
    - This engine does NOT validate input shapes; the router layer must ensure
      user_answers is valid.
    - This engine does NOT sanitize output; routers handle formatting for the
      frontend.
    - All scoring logic is handled here so multiple routers can reuse it.
    """
    data = load_quiz(filename)
    questions = data["questions"]

    # Initialize counters. These must correspond to the styles used in the quiz files.
    style_counts = {
        "strategist": 0,
        "guide": 0,
        "anchor": 0,
        "spark": 0
    }

    # Evaluate each answer.
    for q_index, q_obj in enumerate(questions):
        answer_index = user_answers[q_index]
        style = q_obj["answers"][answer_index]["style"]
        style_counts[style] += 1

    primary_style = calculate_result(style_counts)

    return {
        "primary_style": primary_style,
        "breakdown": style_counts
    }
