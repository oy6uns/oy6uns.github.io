const root = document.documentElement;
const toggle = document.querySelector(".theme-toggle");
const currentLabel = document.querySelector(".theme-current");
const nextLabel = document.querySelector(".theme-next");
const themeColor = document.querySelector('meta[name="theme-color"]');
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

function getPreferredTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "light" || saved === "dark") return saved;
  return systemTheme.matches ? "dark" : "light";
}

function setTheme(theme) {
  const next = theme === "dark" ? "light" : "dark";
  root.dataset.theme = theme;
  if (currentLabel) currentLabel.textContent = theme;
  if (nextLabel) nextLabel.textContent = `→${next}`;
  if (toggle) toggle.setAttribute("aria-label", `Switch to ${next} theme`);
  if (themeColor) themeColor.content = theme === "dark" ? "#151512" : "#f7f4ec";
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

updateClock();
window.setInterval(updateClock, 1000);
