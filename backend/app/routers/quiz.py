from fastapi import APIRouter
from pydantic import BaseModel
from app.engines.quiz_engine import run_quiz, load_quiz

# Create a router object responsible for all quiz-related endpoints.
router = APIRouter(
    prefix="/quiz",
    # This organizes all quiz endpoints together inside the Swagger UI.
    tags=["quiz"]
)

######### HELPER FUNCTIONS #########
####################################

def sanitize_quiz(raw_quiz: dict) -> dict:
    """
    Remove scoring metadata ('style') and return only the text needed for the 
    front end.
    """
    # Store a list of dictionaries, each containing a question and its answer texts.
    safe_questions = []

    # Loop through each question and remove the 'style' metadata from its answers.
    for q in raw_quiz["questions"]:
        # List comprehension to extract only the text (not the style).
        safe_answers = [a["text"] for a in q["answers"]]
        # Append a dictionary containing the question and its answer texts.
        safe_questions.append({
            "question": q["question"],
            "answers": safe_answers
        })

    # Return a dictionary containing the sanitized data for the front end.
    return {"questions": safe_questions}

####################################
####################################

# FastAPI will validate incoming JSON against this model,
# and automatically convert the request body into a QuizSubmission instance.
class QuizSubmission(BaseModel):
    answers: list[int]

# Registers an endpoint.
@router.post("/server-style")
def submit_quiz(submission: QuizSubmission):
    """
    FastAPI reads the JSON request body, validates it using QuizSubmission,
    and injects the parsed model instance as 'submission'.
    """
    # Loads quiz content, evaluates the user's answers using run_quiz,
    # and returns the resulting score breakdown + primary style.
    result = run_quiz("server_style.json", submission.answers)
    # FastAPI serializes the Python dictionary to JSON and sends it as the response.
    return result

@router.get("/server-style/content")
def get_quiz_content():
    raw = load_quiz("server_style.json")   # Load raw quiz data (including style keys)
    safe = sanitize_quiz(raw)              # Strip style data before returning
    return safe                            # FastAPI serializes dictionary into JSON
