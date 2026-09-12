const tabButtons = document.querySelectorAll(".tab-btn");
const tabPanels = document.querySelectorAll(".tab-panel");

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabButtons.forEach((b) => b.classList.remove("active"));
    tabPanels.forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
    if (btn.dataset.tab === "manage") loadQaList();
  });
});

// ---- 질문하기 ----
const askForm = document.getElementById("ask-form");
const askInput = document.getElementById("ask-input");
const askResult = document.getElementById("ask-result");

askForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = askInput.value.trim();
  if (!question) return;

  askResult.textContent = "생각 중...";
  askResult.classList.remove("empty");

  const res = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  const data = await res.json();

  if (res.ok) {
    const meta = data.matched
      ? `\n\n[매칭된 질문: "${data.matched_question}" · 유사도 ${data.score}]`
      : `\n\n[유사도 ${data.score} · 등록된 항목 없음]`;
    askResult.textContent = data.answer;
    const metaEl = document.createElement("div");
    metaEl.className = "meta";
    metaEl.textContent = meta.trim();
    askResult.appendChild(metaEl);
  } else {
    askResult.textContent = data.error || "오류가 발생했습니다.";
  }
});

// ---- 답변 관리 ----
const qaForm = document.getElementById("qa-form");
const qaIdInput = document.getElementById("qa-id");
const qaQuestionInput = document.getElementById("qa-question");
const qaAnswerInput = document.getElementById("qa-answer");
const qaSubmitBtn = document.getElementById("qa-submit");
const qaCancelBtn = document.getElementById("qa-cancel");
const qaList = document.getElementById("qa-list");

function resetForm() {
  qaIdInput.value = "";
  qaQuestionInput.value = "";
  qaAnswerInput.value = "";
  qaSubmitBtn.textContent = "등록";
  qaCancelBtn.hidden = true;
}

qaCancelBtn.addEventListener("click", resetForm);

qaForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = qaIdInput.value;
  const question = qaQuestionInput.value.trim();
  const answer = qaAnswerInput.value.trim();
  if (!question || !answer) return;

  const url = id ? `/api/qa/${id}` : "/api/qa";
  const method = id ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, answer }),
  });

  if (res.ok) {
    resetForm();
    loadQaList();
  } else {
    const data = await res.json();
    alert(data.error || "저장에 실패했습니다.");
  }
});

async function loadQaList() {
  const res = await fetch("/api/qa");
  const entries = await res.json();

  qaList.innerHTML = "";

  if (entries.length === 0) {
    qaList.innerHTML = '<li class="empty-state">아직 등록된 질문이 없어요. 위에서 첫 질문/답변을 등록해보세요.</li>';
    return;
  }

  entries.forEach((entry) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="q">${escapeHtml(entry.question)}</div>
      <div class="a">${escapeHtml(entry.answer)}</div>
      <div class="row-actions">
        <button data-action="edit">수정</button>
        <button data-action="delete" class="danger">삭제</button>
      </div>
    `;
    li.querySelector('[data-action="edit"]').addEventListener("click", () => {
      qaIdInput.value = entry.id;
      qaQuestionInput.value = entry.question;
      qaAnswerInput.value = entry.answer;
      qaSubmitBtn.textContent = "수정 완료";
      qaCancelBtn.hidden = false;
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    li.querySelector('[data-action="delete"]').addEventListener("click", async () => {
      if (!confirm("이 질문/답변을 삭제할까요?")) return;
      await fetch(`/api/qa/${entry.id}`, { method: "DELETE" });
      loadQaList();
    });
    qaList.appendChild(li);
  });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
