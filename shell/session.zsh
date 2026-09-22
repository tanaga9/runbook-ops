# Interactive workspace lifecycle. Do not load from subprocesses.
function _ops_session_prompt() {
  local previous_status=$?
  if (( $+commands[starship] )); then
    # zsh must know that ANSI color sequences occupy no screen columns.
    # Without STARSHIP_SHELL, redraw/history navigation counts them as text.
    PROMPT=$(STARSHIP_SHELL=zsh STARSHIP_CONFIG="$_ops_session_root/shell/starship.toml" \
      starship prompt --status="$previous_status" --terminal-width="${COLUMNS:-80}")
  else
    PROMPT='%F{cyan}[runbook]%f %~ %# '
  fi
  RPROMPT=''
}

function ops-leave() {
  [[ ${OPS_RUNBOOK_ACTIVE:-} == 1 ]] || return 0
  fc -P
  local setting
  for setting in sharehistory incappendhistory incappendhistorytime appendhistory; do
    if [[ ${_ops_saved_options[$setting]} == on ]]; then
      setopt "$setting"
    else
      unsetopt "$setting"
    fi
  done
  path=("${_ops_saved_path[@]}")
  if (( _ops_had_venv )); then
    export VIRTUAL_ENV=$_ops_saved_venv
  else
    unset VIRTUAL_ENV
  fi
  if (( _ops_had_pythonhome )); then
    export PYTHONHOME=$_ops_saved_pythonhome
  else
    unset PYTHONHOME
  fi
  precmd_functions=("${(@)precmd_functions:#_ops_session_prompt}")
  PROMPT=$_ops_saved_prompt
  RPROMPT=$_ops_saved_rprompt
  unset OPS_RUNBOOK_ACTIVE
  rehash
  print 'Runbook mode ended; previous environment and history restored.'
}

function _ops_session_enter() {
  [[ ${OPS_RUNBOOK_ACTIVE:-} == 1 ]] && return 0
  local root=$1
  local venv=${OPS_VENV:-$root/.venv}
  local history_file=${OPS_HISTORY_FILE:-$root/.state/runbook-history}
  if [[ ! -x "$venv/bin/python" || ! -f "$venv/pyvenv.cfg" ]]; then
    print -u2 -- "Runbook mode needs a prepared venv: $venv"
    print -u2 -- "Create it once: python3 -m venv ${(q)venv}"
    return 1
  fi
  venv=${venv:A}
  history_file=${history_file:A}
  (umask 077; mkdir -p -- "${history_file:h}" && touch -- "$history_file") || return 1
  typeset -ga _ops_saved_path=("${path[@]}")
  typeset -g _ops_saved_prompt=$PROMPT _ops_saved_rprompt=$RPROMPT
  typeset -gi _ops_had_venv=${+VIRTUAL_ENV} _ops_had_pythonhome=${+PYTHONHOME}
  typeset -g _ops_saved_venv=${VIRTUAL_ENV-} _ops_saved_pythonhome=${PYTHONHOME-}
  typeset -gA _ops_saved_options
  local setting
  for setting in sharehistory incappendhistory incappendhistorytime appendhistory; do
    _ops_saved_options[$setting]=$options[$setting]
  done
  # Push both the history list and its file/size settings; pop on ops-leave.
  fc -p "$history_file" 10000 10000 || return 1
  unsetopt sharehistory incappendhistorytime
  setopt appendhistory incappendhistory
  typeset -g _ops_session_root=$root
  export VIRTUAL_ENV=$venv
  typeset -g OPS_RUNBOOK_ACTIVE=1
  unset PYTHONHOME
  path=("$venv/bin" "${path[@]}")
  # Keep existing hooks; render our prompt after their normal updates.
  precmd_functions+=(_ops_session_prompt)
  _ops_session_prompt
  rehash
  print -- "Runbook mode: $venv"
  print -- "History: $history_file | Leave: ops-leave"
}
