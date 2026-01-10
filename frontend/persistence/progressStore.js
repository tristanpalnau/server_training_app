/**
 * progressStore.js
 * ----------------
 * Client identity management for progress persistence.
 *
 * Responsibilities:
 * - Generate a stable, anonymous client identifier
 * - Persist the identifier across sessions using localStorage
 *
 * Design notes:
 * - The client ID is intentionally anonymous (no auth, no PII)
 * - Persistence is scoped to the browser/device
 * - Backend progress records are keyed by this client ID
 *
 * This module provides a lightweight identity mechanism
 * suitable for early-stage training persistence without accounts.
 */

/**
 * Retrieves or generates a client identifier.
 *
 * If no client ID exists in localStorage, a new UUID is generated
 * and persisted for future sessions.
 *
 * @returns {string} Stable client identifier
 */
function getClientId() {
  let clientId = localStorage.getItem("client_id");

  if (!clientId) {
    clientId = crypto.randomUUID();
    localStorage.setItem("client_id", clientId);
  }

  return clientId;
}

/**
 * Public, stable client identifier used throughout the frontend
 * for progress persistence.
 */
export const CLIENT_ID = getClientId();
