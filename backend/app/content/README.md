# Content Structure

This folder contains all training content used by the Server Training App.

## Currently Active

### `modules/`
- Source of truth for live training flows.
- Each module may contain one or more scenarios.
- Currently in use:
  - `orientation.json` → Orientation module
    - Scenario: `first_5_minutes`

The frontend consumes scenario-based modules via the FastAPI endpoint:

`/modules/{module_id}/{scenario_id}`

---

## Parked / Future Phases

These folders are intentionally kept for future expansion but are not actively used by the current frontend flow.

### `lessons/`
- Long-form, lesson-style training content
- Intended for deeper learning modules (Phase 2+)

### `scenarios/`
- Standalone or reusable scenario definitions
- May later be referenced or composed into modules

### `quizzes/`
- Centralized quiz definitions
- Intended for reuse across lessons and scenarios

---

## Notes

- The backend is the single source of truth for content.
- The frontend does not store or load content files directly.
- Only scenario-based module delivery is active at this stage.

This structure is intentional and designed to support future growth without refactoring.
