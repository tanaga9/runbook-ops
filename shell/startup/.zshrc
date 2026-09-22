# Restore normal startup paths so child shells do not re-enter runbook mode.
if (( OPS_LAUNCH_HAD_ZDOTDIR )); then
  export ZDOTDIR=$OPS_LAUNCH_ZDOTDIR
else
  unset ZDOTDIR
fi
# macOS /etc/zshrc chooses HISTFILE before this file restores ZDOTDIR.
if [[ $HISTFILE == "$OPS_LAUNCH_ROOT/shell/startup/.zsh_history" ]]; then
  HISTFILE="${ZDOTDIR:-$HOME}/.zsh_history"
fi
if (( _ops_launch_had_sessions_disable )); then
  SHELL_SESSIONS_DISABLE=$_ops_launch_sessions_disable
else
  unset SHELL_SESSIONS_DISABLE
fi
unset _ops_launch_had_sessions_disable _ops_launch_sessions_disable
[[ -r "${ZDOTDIR-$HOME}/.zshrc" ]] && source "${ZDOTDIR-$HOME}/.zshrc"
cd -- "$OPS_LAUNCH_ROOT" && source "$OPS_LAUNCH_ROOT/shell/ops.zsh"
unset OPS_LAUNCH_ROOT OPS_LAUNCH_ZDOTDIR OPS_LAUNCH_HAD_ZDOTDIR
