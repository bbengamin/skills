#!/usr/bin/env bash
# ralph-run.sh - drive a per-unit outreach Ralph stage one unit at a time.
#
# Each iteration is a fresh agent invocation that processes exactly one unit and
# prints a sigil line:
#   RALPH: stage=<stage> unit=<id> status=<ok|unreachable|skipped|drained|stopped> spend=<cost> remaining=<n>
# The driver stops when remaining=0, status is drained/stopped, the iteration cap
# is reached, or accumulated spend reaches the budget.
#
# Usage:
#   scripts/ralph-run.sh --run RL-XXX [--skill outreach-enrich] [--max 200] \
#       [--budget 50] [--sleep 2] [--agent "codex exec"]
#
# The agent command is whatever runs your coding agent non-interactively with a
# single prompt argument, e.g. "codex exec" or "claude -p". Override with --agent
# or the RALPH_AGENT env var.
set -euo pipefail

RUN=""; SKILL="outreach-enrich"; MAX=200; BUDGET=""; SLEEP=2
AGENT="${RALPH_AGENT:-codex exec}"

while [ $# -gt 0 ]; do
  case "$1" in
    --run) RUN="$2"; shift 2;;
    --skill) SKILL="$2"; shift 2;;
    --max) MAX="$2"; shift 2;;
    --budget) BUDGET="$2"; shift 2;;
    --sleep) SLEEP="$2"; shift 2;;
    --agent) AGENT="$2"; shift 2;;
    -h|--help) sed -n '2,17p' "$0"; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$RUN" ] || { echo "error: --run RUN_ID is required" >&2; exit 2; }

read -ra AGENT_ARR <<< "$AGENT"
spent=0; i=0

prompt() {
  cat <<PROMPT
Use the $SKILL skill to process exactly ONE unit of outreach run $RUN.
Resume from the Run Record, handle a single unit, write back through twenty-engine-sync, and checkpoint.
Do not loop over multiple units. End your output with exactly one sigil line of the form:
RALPH: stage=<stage> unit=<id> status=<ok|unreachable|skipped|drained|stopped> spend=<cost> remaining=<n>
PROMPT
}

echo "ralph-run: run=$RUN skill=$SKILL max=$MAX budget=${BUDGET:-none} agent='$AGENT'"
while [ "$i" -lt "$MAX" ]; do
  i=$((i+1))
  out="$("${AGENT_ARR[@]}" "$(prompt)" 2>&1 || true)"
  sigil="$(printf '%s\n' "$out" | grep -E '^RALPH:' | tail -n1 || true)"
  if [ -z "$sigil" ]; then
    echo "iter $i: no sigil found; stopping. Last output:"; printf '%s\n' "$out" | tail -n 20; exit 1
  fi
  status="$(sed -nE 's/.* status=([^ ]+).*/\1/p' <<< "$sigil")"
  remaining="$(sed -nE 's/.* remaining=([0-9]+).*/\1/p' <<< "$sigil")"
  spend="$(sed -nE 's/.* spend=([0-9.]+).*/\1/p' <<< "$sigil")"
  spend="${spend:-0}"
  spent="$(awk -v a="$spent" -v b="$spend" 'BEGIN{printf "%.4f", a+b}')"
  echo "iter $i: status=$status remaining=${remaining:-?} spend=$spend total_spend=$spent"

  case "$status" in drained|stopped) echo "stage $status; done."; break;; esac
  [ "${remaining:-1}" = "0" ] && { echo "segment drained; done."; break; }
  if [ -n "$BUDGET" ] && awk -v s="$spent" -v b="$BUDGET" 'BEGIN{exit !(s>=b)}'; then
    echo "budget $BUDGET reached (spent $spent); stopping."; break
  fi
  sleep "$SLEEP"
done
echo "ralph-run: finished after $i iteration(s), total spend $spent"
