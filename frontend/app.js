/**
 * Phase 1 frontend controller for the Server Training App.
 *
 * Responsibilities:
 * - Fetch module metadata and scenarios from the backend
 * - Manage in-memory scenario progression
 * - Render step content based on step type
 *
 * This file intentionally avoids persistence, routing, or complex UI state.
 */

// Debug logging (safe to remove later)
console.log("Frontend is running!");

// Root DOM container for the app
const app = document.getElementById("app");

// In-memory state for the active module scenario
// Reset whenever a new scenario is loaded
let currentModule = null;
let currentIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    // Entry point for the frontend
    renderModulePicker();
});


// ============================================================
// LOAD SCENARIO FROM BACKEND
// ============================================================
/**
 * Fetches a scenario payload from the backend and initializes step progression.
 *
 * @param {string} endpoint - Backend endpoint for the scenario.
 */
async function loadScenario(endpoint) {
    try {
        const res = await fetch(`http://127.0.0.1:8000${endpoint}`);

        if (!res.ok) {
            throw new Error(`Failed to load scenario: ${res.status}`);
        }

        // Backend returns { module_id, title, scenario }
        currentModule = await res.json();
        currentIndex = 0;

        // Debug logging (safe to remove later)
        console.log("Scenario loaded:", currentModule);
        renderStep();
    } catch (err) {
        console.error("Error loading scenario:", err);
        app.innerHTML = `
            <p style="color:red;">Error loading scenario.<br>${err.message}</p>
        `;
    }
}


// ============================================================
// MODULE PICKER
// ============================================================
/**
 * Fetches available modules and renders the Module Picker UI.
 */
async function renderModulePicker() {
    app.innerHTML = "<p>Loading modules...</p>";

    try {
        const res = await fetch("http://127.0.0.1:8000/modules");

        if (!res.ok) {
            throw new Error(`Failed to load modules: ${res.status}`);
        }

        const modules = await res.json();

        // Debug logging (safe to remove later)
        console.log("Modules loaded:", modules);

        app.innerHTML = `
            <h2>Choose a training module</h2>
            <div id="moduleList"></div>
        `;

        const list = document.getElementById("moduleList");

        modules.forEach(module => {
            const button = document.createElement("button");

            button.style.display = "block";
            button.style.margin = "8px 0";

            button.textContent = `${module.title} (~${module.estimated_minutes} min)`;

            button.onclick = () => {
                // Load the module's default scenario
                loadScenario(`/modules/${module.id}/scenario/${module.default_scenario_id}`);
            };


            list.appendChild(button);
        });

    } catch (err) {
        console.error(err);
        app.innerHTML = `
            <p style="color:red;">
                Error loading modules.<br>${err.message}
            </p>
        `;
    }
}


// ============================================================
// RENDER THE CURRENT STEP
// ============================================================
/**
 * Renders the current step of the active scenario.
 * Routes rendering based on step.type.
 */
function renderStep() {
    if (!currentModule || !currentModule.scenario) {
        app.innerHTML = "<p>Loading training...</p>";
        return;
    }

    const steps = currentModule.scenario.steps;
    // Step progression is purely index-based (Phase 1)

    if (currentIndex >= steps.length) {
        app.innerHTML = `
            <h2>Nice work.</h2>
            <p>You’ve completed this training scenario.</p>
        `;
        return;
    }

    const step = steps[currentIndex];

    // Route to the correct renderer based on step.type
    switch (step.type) {
        case "text":
            renderText(step);
            break;

        case "quiz":
            renderQuiz(step);
            break;

        case "reflection":
            renderReflection(step);
            break;

        case "quiz_result":
            renderQuizResult(step);
            break;

        default:
            app.innerHTML = `<p style="color:red;">Unknown step type: ${step.type}</p>`;
            break;
    }
}


// ============================================================
// RENDER FUNCTIONS
// ============================================================

function renderText(step) {
    // Simple text-based instructional step
    app.innerHTML = `
        <h2>Lesson</h2>
        <p>${step.text}</p>
        <button onclick="nextStep()">Next</button>
    `;
}

function renderQuiz(step) {
    // Placeholder quiz renderer (UI + grading not implemented yet)
    app.innerHTML = `
        <h2>Quiz</h2>
        <p><strong>Question:</strong> ${step.question}</p>

        <p style="opacity: 0.6;">(Quiz UI coming next — placeholder for now)</p>

        <pre>${JSON.stringify(step, null, 2)}</pre>

        <button onclick="nextStep()">Next (placeholder)</button>
    `;
}

function renderReflection(step) {
    // Reflection input is not persisted in Phase 1
    app.innerHTML = `
        <h2>Reflection</h2>
        <p>${step.prompt}</p>

        <textarea
            id="reflectionInput"
            rows="5"
            cols="40"
            placeholder="Write your thoughts here..."
        ></textarea>
        <br><br>

        <button onclick="nextStep()">Next</button>
    `;
}

function renderQuizResult(step) {
    app.innerHTML = `
        <h2>Results</h2>
        <p>${step.correct_text || step.incorrect_text}</p>
        <button onclick="nextStep()">Next</button>
    `;
}


// ============================================================
// STEP NAVIGATION
// ============================================================
/**
 * Advances to the next step and re-renders.
 */
function nextStep() {
    currentIndex++;
    renderStep();
}
