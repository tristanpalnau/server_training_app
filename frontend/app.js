console.log("Frontend is running!");

// Grab the app container once
const app = document.getElementById("app");

// Global variables for the module and steps
let currentModule = null;
let currentIndex = 0;


// ============================================================
// LOAD ORIENTATION SCENARIO FROM BACKEND
// ============================================================

async function loadOrientationScenario() {
    try {
        const res = await fetch("http://127.0.0.1:8000/modules/orientation/first_5_minutes");

        if (!res.ok) {
            throw new Error(`Failed to load scenario: ${res.status}`);
        }

        currentModule = await res.json();
        currentIndex = 0;

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
// RENDER THE CURRENT STEP
// ============================================================

function renderStep() {
    if (!currentModule || !currentModule.scenario) {
        app.innerHTML = "<p>Loading training...</p>";
        return;
    }

    const steps = currentModule.scenario.steps;

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
    app.innerHTML = `
        <h2>Lesson</h2>
        <p>${step.text}</p>
        <button onclick="nextStep()">Next</button>
    `;
}

function renderQuiz(step) {
    app.innerHTML = `
        <h2>Quiz</h2>
        <p><strong>Question:</strong> ${step.question}</p>

        <p style="opacity: 0.6;">(Quiz UI coming next — placeholder for now)</p>

        <pre>${JSON.stringify(step, null, 2)}</pre>

        <button onclick="nextStep()">Next (placeholder)</button>
    `;
}

function renderReflection(step) {
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

function nextStep() {
    currentIndex++;
    renderStep();
}


// ============================================================
// AUTO-LOAD ORIENTATION SCENARIO
// ============================================================

loadOrientationScenario();
