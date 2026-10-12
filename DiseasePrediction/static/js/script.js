const searchBox = document.getElementById("symptom-search");
const grid = document.getElementById("symptom-grid");
const chips = Array.from(grid.querySelectorAll(".symptom-chip"));
const countLabel = document.getElementById("selected-count");
const predictBtn = document.getElementById("predict-btn");
const resultCard = document.getElementById("result-card");
const resultContent = document.getElementById("result-content");

// --- live search filter ---
searchBox.addEventListener("input", () => {
  const q = searchBox.value.trim().toLowerCase();
  chips.forEach((chip) => {
    const label = chip.querySelector("span").textContent.toLowerCase();
    chip.classList.toggle("hidden", q.length > 0 && !label.includes(q));
  });
});

// --- track selected count ---
function updateCount() {
  const checked = grid.querySelectorAll("input[type=checkbox]:checked").length;
  countLabel.textContent = `${checked} symptom${checked === 1 ? "" : "s"} selected`;
}
grid.addEventListener("change", updateCount);

// --- run prediction ---
predictBtn.addEventListener("click", async () => {
  const selected = Array.from(grid.querySelectorAll("input[type=checkbox]:checked")).map(
    (el) => el.value
  );

  if (selected.length === 0) {
    showError("Select at least one symptom first.");
    return;
  }

  predictBtn.disabled = true;
  predictBtn.textContent = "Analyzing...";

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms: selected }),
    });
    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    renderResult(data);
  } catch (err) {
    showError("Could not reach the server. Is app.py running?");
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = "Analyze Symptoms";
  }
});

function showError(msg) {
  resultCard.style.display = "block";
  resultContent.innerHTML = `<div class="error-box">${msg}</div>`;
}

function renderResult(data) {
  resultCard.style.display = "block";

  const top3Html = data.top3
    .map(
      (item) => `
      <div class="top3-row">
        <span>${item.disease}</span>
        <span>${item.confidence}%</span>
      </div>`
    )
    .join("");

  resultContent.innerHTML = `
    <div class="primary-result">
      <span class="disease-name">${data.prediction}</span>
      <span class="confidence">${data.confidence}% confidence</span>
    </div>
    <div class="top3-list">
      <strong style="font-size:0.85rem;">Top 3 possibilities:</strong>
      ${top3Html}
    </div>
    <div class="used-symptoms">
      <strong>Based on:</strong> ${data.symptoms_used.join(", ")}
    </div>
  `;

  resultCard.scrollIntoView({ behavior: "smooth", block: "center" });
}
