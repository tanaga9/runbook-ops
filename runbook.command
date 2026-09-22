#!/bin/zsh

# Open an interactive runbook workspace from Finder or a terminal.
export OPS_LAUNCH_ROOT=${0:A:h}
export OPS_LAUNCH_ZDOTDIR=${ZDOTDIR-}
export OPS_LAUNCH_HAD_ZDOTDIR=${+ZDOTDIR}
cd -- "$OPS_LAUNCH_ROOT" || exit 1
ZDOTDIR="$OPS_LAUNCH_ROOT/shell/startup" exec /bin/zsh -i
