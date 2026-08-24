/* theme ------------------------------------------------------------------ */

const root = document.documentElement;
const toggle = document.querySelector(".theme-toggle");
const themeColor = document.querySelector('meta[name="theme-color"]');
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

const PAGE_BG = { light: "#ffffff", dark: "#16181c" };

function getPreferredTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "light" || saved === "dark") return saved;
  return systemTheme.matches ? "dark" : "light";
}

function setTheme(theme) {
  const next = theme === "dark" ? "light" : "dark";
  root.dataset.theme = theme;
  if (toggle) toggle.setAttribute("aria-label", `Switch to ${next} theme`);
  if (themeColor) themeColor.content = PAGE_BG[theme];
}

setTheme(getPreferredTheme());

toggle?.addEventListener("click", () => {
  const next = root.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("theme", next);
  setTheme(next);
});

systemTheme.addEventListener("change", (event) => {
  if (!localStorage.getItem("theme")) setTheme(event.matches ? "dark" : "light");
});

/* footer ----------------------------------------------------------------- */

const yearEl = document.querySelector("#year");
if (yearEl) yearEl.textContent = String(new Date().getFullYear());

const clock = document.querySelector("#clock");
const formatter = new Intl.DateTimeFormat("en-GB", {
  timeZone: "Asia/Seoul",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false,
});

function updateClock() {
  if (clock) clock.textContent = formatter.format(new Date());
}

if (clock) {
  updateClock();
  window.setInterval(updateClock, 1000);
}
