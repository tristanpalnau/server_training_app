/**
 * screens.js
 * ----------
 * High-level screen orchestration for the frontend UI.
 *
 * Responsibilities:
 * - Render the module selection screen
 * - Orchestrate loading of scenarios and persisted progress
 * - Initialize application state for a training session
 *
 * Design notes:
 * - This module coordinates API calls, state updates, and rendering
 * - It does NOT contain step-level rendering logic (see renderer.js)
 * - It does NOT handle user interaction beyond screen-level navigation
 */

import { fetchModules, fetchScenario, loadProgress } from "../api/trainingApi.js";
import { CLIENT_ID } from "../persistence/progressStore.js";
import { setCurrentModule, setCurrentIndex } from "../state/appState.js";
import { renderStep } from "./renderer.js";

const app = document.getElementById("app");

/**
 * Renders the module picker screen.
 *
 * Fetches available training modules from the backend and displays
 * them as selectable buttons.
 *
 * Selecting a module triggers loading of the module's default scenario.
 */
export async function renderModulePicker() {
  console.trace("🚨 renderModulePicker called");

  try {
    const modules = await fetchModules();

    console.log("Modules loaded:", modules);

    app.innerHTML = `
      <h2>Choose a training module</h2>
      <div id="moduleList"></div>
    `;

    const list = document.getElementById("moduleList");

    modules.forEach((module) => {
      const button = document.createElement("button");
      button.type = "button"; // defensive: never submit or navigate
      button.style.display = "block";
      button.style.margin = "8px 0";
      button.textContent = `${module.title} (~${module.estimated_minutes} min)`;

      button.addEventListener("click", () => {
        loadScenarioByEndpoint(
          `/modules/${module.id}/scenario/${module.default_scenario_id}`
        );
      });

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

/**
 * Loads a scenario by backend endpoint and initializes the training session.
 *
 * Sequence:
 * 1. Fetch full module + scenario payload
 * 2. Store module data in application state
 * 3. Load persisted progress for the current client
 * 4. Initialize the step index
 * 5. Render the first (or resumed) step
 *
 * @param {string} endpoint - Backend scenario endpoint
 */
async function loadScenarioByEndpoint(endpoint) {
  try {
    const modulePayload = await fetchScenario(endpoint);

    // Backend returns { module_id, title, scenario }
    setCurrentModule(modulePayload);

    const resumeIndex = await loadProgress({
      client_id: CLIENT_ID,
      module_id: modulePayload.module_id,
      scenario_id: modulePayload.scenario.id,
    });

    setCurrentIndex(resumeIndex);

    console.log("Scenario loaded:", modulePayload);
    console.log("Resuming at step:", resumeIndex);

    renderStep();
  } catch (err) {
    console.error("Error loading scenario:", err);
    app.innerHTML = `
      <p style="color:red;">
        Error loading scenario.<br>${err.message}
      </p>
    `;
  }
}
