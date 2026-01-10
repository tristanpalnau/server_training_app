/**
 * controls.js
 * -----------
 * User interaction and control flow handlers for training progression.
 *
 * Responsibilities:
 * - Respond to user actions (e.g. "Next" step)
 * - Update in-memory application state
 * - Trigger progress persistence
 * - Request re-rendering of the current step
 *
 * Design notes:
 * - This module does NOT perform any rendering itself
 * - Rendering is injected at runtime to avoid circular dependencies
 * - Persistence is fire-and-forget to preserve UI responsiveness
 */

import { appState, incrementIndex } from "../state/appState.js";
import { CLIENT_ID } from "../persistence/progressStore.js";
import { saveProgress } from "../api/trainingApi.js";

let renderStepHandler = null;

/**
 * Injects the renderStep function.
 *
 * This indirection prevents circular imports between
 * control logic and rendering logic.
 *
 * Called once during application startup.
 *
 * @param {Function} fn - Function responsible for rendering the current step
 */
export function setRenderStepHandler(fn) {
  renderStepHandler = fn;
}

/**
 * Advances the training flow to the next step.
 *
 * Sequence:
 * 1. Prevents default browser behavior (defensive)
 * 2. Advances the in-memory step index
 * 3. Persists progress to the backend (non-blocking)
 * 4. Triggers a re-render of the current step
 *
 * @param {Event} [event] - Optional DOM event
 */
export function nextStep(event) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }

  incrementIndex();

  if (appState.currentModule) {
    saveProgress({
      client_id: CLIENT_ID,
      module_id: appState.currentModule.module_id,
      scenario_id: appState.currentModule.scenario.id,
      current_step_index: appState.currentIndex,
    });
  }

  if (typeof renderStepHandler === "function") {
    renderStepHandler();
  }
}

