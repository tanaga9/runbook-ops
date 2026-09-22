# Preserve the user's environment setup before selecting our interactive startup.
if (( OPS_LAUNCH_HAD_ZDOTDIR )); then
  export ZDOTDIR=$OPS_LAUNCH_ZDOTDIR
else
  unset ZDOTDIR
fi
[[ -r "${ZDOTDIR-$HOME}/.zshenv" ]] && source "${ZDOTDIR-$HOME}/.zshenv"
export OPS_LAUNCH_ZDOTDIR=${ZDOTDIR-}
export OPS_LAUNCH_HAD_ZDOTDIR=${+ZDOTDIR}
# This dedicated shell owns its history; disable Terminal's parallel save/restore.
typeset -g _ops_launch_had_sessions_disable=${+SHELL_SESSIONS_DISABLE}
typeset -g _ops_launch_sessions_disable=${SHELL_SESSIONS_DISABLE-}
SHELL_SESSIONS_DISABLE=1
export ZDOTDIR="$OPS_LAUNCH_ROOT/shell/startup"
