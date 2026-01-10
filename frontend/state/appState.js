/**
 * appState.js
 * -----------
 * Centralized, in-memory application state for the frontend.
 *
 * Responsibilities:
 * - Hold the currently active training module payload
 * - Track the user's current step index within a scenario
 *
 * Design notes:
 * - This state is intentionally minimal and ephemeral
 * - It does NOT persist across page reloads (persistence is handled by the backend)
 * - It does NOT perform any rendering or side effects
 *
 * This module serves as a shared source of truth for
 * UI rendering and control logic during a training session.
 */

export const appState = {
  /**
   * The currently active module payload returned from the backend.
   *
   * Expected shape:
   * {
   *   module_id: string,
   *   title: string,
   *   scenario: {
   *     scenario_id: string,
   *     steps: Array
   *   }
   * }
   */
  currentModule: null,

  /**
   * Index of the current step within the active scenario.
   */
  currentIndex: 0,
};

/**
 * Sets the active module payload.
 *
 * @param {Object} modulePayload - Full module data returned from the backend
 */
export function setCurrentModule(modulePayload) {
  appState.currentModule = modulePayload;
}

/**
 * Sets the current step index explicitly.
 *
 * Used when:
 * - Restoring persisted progress
 * - Jumping to a specific step
 *
 * @param {number} index
 */
export function setCurrentIndex(index) {
  appState.currentIndex = index;
}

/**
 * Advances the current step index by one.
 *
 * Typically triggered by "Next" actions in the UI.
 */
export function incrementIndex() {
  appState.currentIndex += 1;
}
