/**
 * app.js
 * ------
 * Frontend application entry point.
 *
 * Responsibilities:
 * - Perform initial backend availability check
 * - Wire rendering logic into control handlers
 * - Kick off the initial UI screen
 *
 * Design notes:
 * - This file intentionally contains no business logic
 * - It serves as the composition root for the frontend
 * - All rendering, state, and control logic is delegated
 */

import { renderModulePicker } from "./ui/screens.js";
import { setRenderStepHandler } from "./ui/controls.js";
import { renderStep } from "./ui/renderer.js";
import { checkHealth } from "./api/trainingApi.js";

// Wire the renderer into controls (prevents circular-import headaches)
setRenderStepHandler(renderStep);

/**
 * Application startup sequence.
 *
 * Verifies backend availability before rendering the UI.
 * Provides a clear failure state if the backend is unreachable.
 */
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await checkHealth();
    console.log("✅ Backend connected");
    renderModulePicker();
  } catch (err) {
    console.error("❌ Backend unavailable", err);
    document.getElementById("app").innerHTML = `
      <h2>Backend unavailable</h2>
      <p>Please try again later.</p>
    `;
  }
});
