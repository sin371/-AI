"""내가 등록해둔 질문에는 내가 원하는 답을 그대로 돌려주는 커스텀 답변 AI."""
from __future__ import annotations

from flask import Flask, jsonify, render_template, request

import store
from matcher import find_best_match

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/qa")
def api_list_qa():
    return jsonify(store.list_entries())


@app.post("/api/qa")
def api_add_qa():
    body = request.get_json(silent=True) or {}
    question, answer = body.get("question", ""), body.get("answer", "")
    try:
        entry = store.add_entry(question, answer)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(entry), 201


@app.put("/api/qa/<int:entry_id>")
def api_update_qa(entry_id: int):
    body = request.get_json(silent=True) or {}
    question, answer = body.get("question", ""), body.get("answer", "")
    try:
        entry = store.update_entry(entry_id, question, answer)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if entry is None:
        return jsonify({"error": "해당 항목을 찾을 수 없습니다."}), 404
    return jsonify(entry)


@app.delete("/api/qa/<int:entry_id>")
def api_delete_qa(entry_id: int):
    deleted = store.delete_entry(entry_id)
    if not deleted:
        return jsonify({"error": "해당 항목을 찾을 수 없습니다."}), 404
    return jsonify({"ok": True})


@app.post("/api/ask")
def api_ask():
    body = request.get_json(silent=True) or {}
    question = body.get("question", "").strip()
    if not question:
        return jsonify({"error": "질문을 입력해 주세요."}), 400

    entries = store.list_entries()
    result = find_best_match(question, entries)

    if result.matched and result.entry is not None:
        return jsonify(
            {
                "matched": True,
                "answer": result.entry["answer"],
                "matched_question": result.entry["question"],
                "score": round(result.score, 3),
            }
        )

    return jsonify(
        {
            "matched": False,
            "answer": "아직 이 질문에 등록된 답변이 없어요. 원하는 답변을 등록해 주시면 다음부터 그대로 답해드릴게요.",
            "score": round(result.score, 3),
        }
    )


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
