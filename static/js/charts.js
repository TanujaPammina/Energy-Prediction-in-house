/**
 * EnergyIQ — charts.js
 * Chart logic is now embedded inline in each template for
 * direct access to Flask-injected data. This file is kept
 * for any shared chart utilities that may be needed in future.
 */

/**
 * Animate a numeric counter from 0 to `target`.
 * @param {string} id       - Element ID
 * @param {number} target   - Final value
 * @param {number} decimals - Decimal places
 */
function countUp(id, target, decimals = 2) {
  const el = document.getElementById(id);
  if (!el) return;
  let cur = 0;
  const step = target / 50;
  const timer = setInterval(() => {
    cur += step;
    if (cur >= target) {
      el.textContent = target.toFixed(decimals);
      clearInterval(timer);
      return;
    }
    el.textContent = cur.toFixed(decimals);
  }, 18);
}

/**
 * Animate progress bar widths after a short delay.
 * Expects elements with class `.feat-bar-fill` and `data-pct` attribute.
 */
function animateProgressBars(delay = 300) {
  setTimeout(() => {
    document.querySelectorAll(".feat-bar-fill[data-pct]").forEach(el => {
      el.style.width = el.dataset.pct + "%";
    });
  }, delay);
}
