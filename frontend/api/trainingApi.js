/**
 * trainingApi.js
 * ----------------
 * Centralized API client for the Server Training frontend.
 *
 * Responsibilities:
 * - Provide a thin, fetch-based interface to backend API endpoints
 * - Normalize request/response handling for training data and persistence
 * - Remain stateless and UI-agnostic
 *
 * Design principles:
 * - Same-origin API calls (served by FastAPI under /api)
 * - No direct state mutation
 * - No rendering or DOM access
 * - Persistence calls should not block UI interactions
 *
 * This module acts as the single source of truth for
 * how the frontend communicates with the backend.
 */

const API_BASE = "/api";

/**
 * Fetches the list of available training modules.
 *
 * @returns {Promise<Object[]>} Array of module metadata objects
 * @throws {Error} If the request fails or returns a non-OK status
 */
export async function fetchModules() {
  const res = await fetch(`${API_BASE}/modules`);
  if (!res.ok) {
    throw new Error(`Failed to load modules: ${res.status}`);
  }
  return res.json();
}

/**
 * Fetches a full scenario payload from the backend.
 *
 * @param {string} endpoint - Scenario endpoint path (e.g. "/scenarios/first_5_minutes")
 * @returns {Promise<Object>} Scenario JSON payload
 * @throws {Error} If the request fails or returns a non-OK status
 */
export async function fetchScenario(endpoint) {
  const res = await fetch(`${API_BASE}${endpoint}`);
  if (!res.ok) {
    throw new Error(`Failed to load scenario: ${res.status}`);
  }
  return res.json();
}

/**
 * Loads persisted progress for a given client/module/scenario combination.
 *
 * If no progress exists, defaults to step index 0.
 *
 * @param {Object} params
 * @param {string} params.client_id
 * @param {string} params.module_id
 * @param {string} params.scenario_id
 * @returns {Promise<number>} Current step index
 */
export async function loadProgress({ client_id, module_id, scenario_id }) {
  const params = new URLSearchParams({
    client_id,
    module_id,
    scenario_id,
  });

  const res = await fetch(`${API_BASE}/progress?${params}`);
  const data = await res.json();

  return data.current_step_index ?? 0;
}

/**
 * Persists the user's current progress.
 *
 * This is intentionally implemented as fire-and-forget:
 * - Progress saving should never block the UI
 * - Failures are logged but do not interrupt training flow
 *
 * @param {Object} params
 * @param {string} params.client_id
 * @param {string} params.module_id
 * @param {string} params.scenario_id
 * @param {number} params.current_step_index
 */
export function saveProgress({
  client_id,
  module_id,
  scenario_id,
  current_step_index,
}) {
  fetch(`${API_BASE}/progress`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      client_id,
      module_id,
      scenario_id,
      current_step_index,
    }),
  }).catch((err) => {
    console.error("Failed to save progress:", err);
  });
}

/**
 * Verifies backend availability.
 *
 * Used as a lightweight health check during frontend startup
 * to provide early feedback if the backend is unreachable.
 *
 * @returns {Promise<Object>} Health check response payload
 * @throws {Error} If the backend responds with a non-OK status
 */
export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) {
    throw new Error("Backend health check failed");
  }
  return res.json();
}
