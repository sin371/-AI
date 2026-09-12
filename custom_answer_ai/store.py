"""질문-답변 쌍을 JSON 파일에 저장/조회하는 간단한 저장소."""
from __future__ import annotations

import json
import threading
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "qa_data.json"

_lock = threading.Lock()


def _ensure_file() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        DATA_PATH.write_text(json.dumps({"next_id": 1, "entries": []}, ensure_ascii=False, indent=2), encoding="utf-8")


def _load() -> dict:
    _ensure_file()
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def list_entries() -> list[dict]:
    with _lock:
        return _load()["entries"]


def add_entry(question: str, answer: str) -> dict:
    question, answer = question.strip(), answer.strip()
    if not question or not answer:
        raise ValueError("질문과 답변은 비어 있을 수 없습니다.")

    with _lock:
        data = _load()
        entry = {"id": data["next_id"], "question": question, "answer": answer}
        data["entries"].append(entry)
        data["next_id"] += 1
        _save(data)
        return entry


def update_entry(entry_id: int, question: str, answer: str) -> dict | None:
    question, answer = question.strip(), answer.strip()
    if not question or not answer:
        raise ValueError("질문과 답변은 비어 있을 수 없습니다.")

    with _lock:
        data = _load()
        for entry in data["entries"]:
            if entry["id"] == entry_id:
                entry["question"] = question
                entry["answer"] = answer
                _save(data)
                return entry
        return None


def delete_entry(entry_id: int) -> bool:
    with _lock:
        data = _load()
        before = len(data["entries"])
        data["entries"] = [e for e in data["entries"] if e["id"] != entry_id]
        if len(data["entries"]) != before:
            _save(data)
            return True
        return False
