/**
 * renderer.js
 * -----------
 * Responsible for rendering the current training step to the DOM.
 *
 * Responsibilities:
 * - Read the current application state
 * - Select the correct renderer based on step type
 * - Render the appropriate UI for the active step
 *
 * Design notes:
 * - This module is intentionally state-read-only
 * - It does NOT mutate application state directly
 * - It delegates control flow (e.g. advancing steps) to controls.js
 *
 * Rendering is entirely driven by appState.currentModule
 * and appState.currentIndex.
 */

import { appState } from "../state/appState.js";
import { nextStep } from "./controls.js";

const app = document.getElementById("app");

/**
 * Renders the current step of the active scenario.
 *
 * Handles:
 * - Loading state
 * - Completion state
 * - Step-type-based rendering dispatch
 */
export function renderStep() {
  const currentModule = appState.currentModule;
  const currentIndex = appState.currentIndex;

  if (!currentModule || !currentModule.scenario) {
    app.innerHTML = "<p>Loading training...</p>";
    return;
  }

  const steps = currentModule.scenario.steps;

  // Scenario complete
  if (currentIndex >= steps.length) {
    app.innerHTML = `
      <h2>Nice work.</h2>
      <p>You’ve completed this training scenario.</p>
    `;
    return;
  }

  const step = steps[currentIndex];

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
// Step renderers
// ============================================================

/**
 * Renders a basic instructional text step.
 *
 * @param {Object} step
 */
function renderText(step) {
  app.innerHTML = `
    <h2>Lesson</h2>
    <p>${step.text}</p>
    <div id="controls"></div>
  `;

  mountNextButton("controls", "Next");
}

/**
 * Renders a quiz step.
 *
 * NOTE:
 * Quiz interaction logic is intentionally deferred.
 * This currently serves as a structural placeholder.
 *
 * @param {Object} step
 */
function renderQuiz(step) {
  app.innerHTML = `
    <h2>Quiz</h2>
    <p><strong>Question:</strong> ${step.question}</p>

    <p style="opacity: 0.6;">(Quiz UI coming next — placeholder for now)</p>

    <pre>${escapeHtml(JSON.stringify(step, null, 2))}</pre>

    <div id="controls"></div>
  `;

  mountNextButton("controls", "Next (placeholder)");
}

/**
 * Renders a reflection step with a freeform textarea.
 *
 * @param {Object} step
 */
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

    <div id="controls"></div>
  `;

  mountNextButton("controls", "Next");
}

/**
 * Renders a quiz result step.
 *
 * @param {Object} step
 */
function renderQuizResult(step) {
  app.innerHTML = `
    <h2>Results</h2>
    <p>${step.correct_text || step.incorrect_text}</p>
    <div id="controls"></div>
  `;

  mountNextButton("controls", "Next");
}

// ============================================================
// Helpers
// ============================================================

/**
 * Mounts a "Next" button into the specified container.
 *
 * Uses an explicit button type to prevent accidental
 * form submissions and page reloads.
 *
 * @param {string} containerId
 * @param {string} label
 */
function mountNextButton(containerId, label) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const btn = document.createElement("button");
  btn.type = "button"; // critical: prevents form submit / reload
  btn.textContent = label;
  btn.addEventListener("click", (e) => nextStep(e));

  container.appendChild(btn);
}

/**
 * Escapes HTML characters for safe rendering inside <pre> blocks.
 *
 * Prevents JSON content from being interpreted as markup.
 *
 * @param {string} str
 * @returns {string}
 */
function escapeHtml(str) {
  return str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}
