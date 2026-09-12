"""질문 매칭 로직.

등록된 질문들 중 사용자의 질문과 가장 비슷한 것을 찾아 그 답변을 반환한다.
- 문자열 유사도(SequenceMatcher)와 키워드(토큰) 겹침 비율을 함께 사용해
  표현이 조금 달라도 매칭되도록 한다.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher

MATCH_THRESHOLD = 0.45


def normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^0-9a-z가-힣\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> set[str]:
    return set(normalize(text).split())


def similarity(a: str, b: str) -> float:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0

    ratio = SequenceMatcher(None, na, nb).ratio()

    ta, tb = tokenize(a), tokenize(b)
    if ta and tb:
        jaccard = len(ta & tb) / len(ta | tb)
    else:
        jaccard = 0.0

    return max(ratio, jaccard)


@dataclass
class MatchResult:
    matched: bool
    score: float
    entry: dict | None


def find_best_match(question: str, entries: list[dict]) -> MatchResult:
    best_entry = None
    best_score = 0.0

    for entry in entries:
        score = similarity(question, entry["question"])
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry is not None and best_score >= MATCH_THRESHOLD:
        return MatchResult(matched=True, score=best_score, entry=best_entry)
    return MatchResult(matched=False, score=best_score, entry=best_entry)
