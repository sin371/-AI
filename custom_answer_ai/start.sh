#!/usr/bin/env bash
# 커스텀 답변 AI 실행 스크립트
set -euo pipefail

cd "$(dirname "$0")"

PID_FILE=".server.pid"
LOG_FILE="server.log"
PORT="${PORT:-5000}"

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "이미 실행 중입니다. (PID: $(cat "$PID_FILE"))"
  echo "주소: http://localhost:${PORT}"
  exit 0
fi

if [ -f "requirements.txt" ]; then
  python3 -c "import flask" 2>/dev/null || pip install -q -r requirements.txt
fi

nohup python3 app.py > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

sleep 1

if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "실행되었습니다. (PID: $(cat "$PID_FILE"))"
  echo "주소: http://localhost:${PORT}"
  echo "종료하려면: ./stop.sh"
else
  echo "실행에 실패했습니다. $LOG_FILE 을 확인하세요."
  rm -f "$PID_FILE"
  exit 1
fi
