# Runbook workspace only. No domain loading or operational execution.
if [[ ! -o interactive ]]; then
  return 0
fi
source "${${(%):-%x}:A:h}/session.zsh"
_ops_session_enter "${${(%):-%x}:A:h:h}"
