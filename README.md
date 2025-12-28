# Server Training App

A modular, JSON-driven backend for a scenario-based restaurant training platform.  
Built with FastAPI, this backend currently powers **orientation and first-day training flows**, with extensible engines in place for deeper lesson and quiz-based learning.

---

## Current Focus (Active)

### Frontend (Phase 1)
- Frontend controls scenario progression
- Backend returns entire scenarios at once
- No user state or progress is persisted yet

### Module Picker (Phase 1)
- Frontend fetches available modules from the backend
- Modules are presented as selectable training options
- Each module defines a default scenario for entry

### Scenario-Based Orientation Modules
- Training content is defined as JSON modules composed of one or more scenarios
- Each scenario contains a sequence of steps such as:
  - text
  - reflection
  - quiz
  - quiz_result
- The frontend consumes **entire scenarios at once** and controls step progression
- Example active module:
  - `orientation.json`
    - Scenario: `first_5_minutes`

### Primary API Endpoint

GET /modules/{module_id}/scenario/{scenario_id}


Returns a frontend-ready payload:
- module metadata
- selected scenario
- ordered steps

This endpoint represents the **primary Phase 1 content delivery path**.

---

## Parked / Internal Engines (Phase 2+)

The backend includes fully implemented engines that are not yet part of the active frontend flow but are intentionally retained for future phases.

### Lesson Engine
- Lessons stored as JSON in `content/modules`
- Supports step-by-step retrieval and processing
- Step routing handled by `process_step`
- Enables future adaptive and personalized lesson delivery

### Quiz Engine
- Quizzes defined in `content/quizzes`
- Supports scoring across multiple styles:
  - strategist
  - guide
  - anchor
  - spark
- Designed to integrate into lessons via `quiz_result` steps

These systems are currently **parked**, not removed, and will be reintroduced as the product expands beyond orientation.

---

## Additional API Endpoints (Internal / Future Use)

- `GET /modules` — return module catalog metadata for the Module Picker UI
- `GET /modules/{id}/raw` — return raw module JSON
- `GET /modules/{id}/content` — return module metadata
- `GET /modules/{id}/step/{index}` — return processed lesson steps
- Quiz endpoints for loading quiz content and submitting results

---

## Project Structure

app/
│
├── content/
│ ├── modules/ # Scenario-based modules (active)
│ ├── lessons/ # Long-form lessons (parked)
│ ├── quizzes/ # Quiz definitions (parked)
│ ├── scenarios/ # Reserved for reusable scenario templates (parked)
│
├── engines/
│ ├── module_engine.py
│ └── quiz_engine.py
│
├── loaders/
│ ├── module_loader.py
│ └── scenario_loader.py
│
├── routers/
│ ├── modules.py
│ └── quiz.py
│
└── main.py


---

## Running the Server

Install dependencies and start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```
Open API documentation:
```
http://127.0.0.1:8000/docs
```

## Roadmap
- Expand orientation with additional scenarios
- Add restaurant-specific customization
- Reintroduce lesson engine for deeper training modules
- Implement user progress tracking (SQLite)
- Enable personalized coaching messages
- Add branching scenarios and richer step types
- Deploy backend (Railway or Render)
- Continue frontend development

## Contributing
This project is actively evolving. Contributions, issues, and suggestions are welcome.
