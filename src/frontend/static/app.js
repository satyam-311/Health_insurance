const form = document.getElementById("predict-form");
const submitBtn = document.getElementById("submit-btn");
const resultBox = document.getElementById("result");
const resultValue = document.getElementById("result-value");
const errorEl = document.getElementById("error");
const modelStatusEl = document.getElementById("model-status");
const modelFieldsEl = document.getElementById("model-fields");

function resetMessages() {
  resultBox.classList.add("hidden");
  errorEl.classList.add("hidden");
  errorEl.textContent = "";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  resetMessages();

  const payload = {
    age: Number(document.getElementById("age").value),
    bmi: Number(document.getElementById("bmi").value),
    children: Number(document.getElementById("children").value),
    gender: document.getElementById("gender").value,
    discount_eligibility: document.getElementById("discount_eligibility").value,
    sex: document.getElementById("gender").value,
    smoker: document.getElementById("discount_eligibility").value,
    region: document.getElementById("region").value
  };

  submitBtn.disabled = true;
  submitBtn.textContent = "Estimating...";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const body = await response.json();

    if (!response.ok) {
      const detail = body.detail || `Request failed (${response.status})`;
      throw new Error(detail);
    }

    const value = Number(body.predicted_expenses);
    if (Number.isNaN(value)) {
      throw new Error("Invalid prediction response");
    }

    resultValue.textContent = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 2
    }).format(value);

    resultBox.classList.remove("hidden");
  } catch (error) {
    errorEl.textContent = `Unable to generate prediction: ${error.message}`;
    errorEl.classList.remove("hidden");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Estimate Premium";
  }
});

async function loadModelInfo() {
  try {
    const response = await fetch("/model-info");
    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.detail || `Request failed (${response.status})`);
    }

    modelStatusEl.textContent = "Ready";
    modelStatusEl.classList.remove("neutral", "bad");
    modelStatusEl.classList.add("ok");
    modelFieldsEl.textContent = body.expected_columns.length
      ? body.expected_columns.join(", ")
      : "unknown";
  } catch (error) {
    modelStatusEl.textContent = "Unavailable";
    modelStatusEl.classList.remove("neutral", "ok");
    modelStatusEl.classList.add("bad");
    modelFieldsEl.textContent = "Model missing or failed to load";
  }
}

loadModelInfo();
