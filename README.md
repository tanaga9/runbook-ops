# runbook-ops

A small terminal workspace for readable runbooks. Start with an idea, try understandable actions with AI, and improve the procedure through use.

## Enter the workspace

From this checkout, prepare Python once:

```zsh
[ ! -d ".venv" ] && python3 -m venv .venv
```

Enter from an interactive zsh:

```zsh
source ./shell/ops.zsh
```

On macOS, double-click `runbook.command` to open a terminal in this checkout with runbook mode enabled. It loads your usual zsh settings through `shell/startup/`, then enters the workspace.

This switches the venv, history, and prompt. Run `ops-leave` to restore the previous environment. The working directory and case variables remain unchanged. Do not source automatically from `.zshrc` unless every terminal should enter this mode.

## Tools

| Tool | Role |
| --- | --- |
| zsh | Workspace and interactive commands |
| Python 3.10+ | Dedicated venv and readable inline scripts |
| Starship (optional) | Dedicated prompt; a basic prompt works without it |
| Obsidian (optional) | Edit Notes and runbooks; any Markdown editor works |

Individual runbooks declare additional tools. No package installation, CLI registry, or framework is required.

## Use the Skills

| Skill | Responsibility |
| --- | --- |
| [develop-runbook](plugins/runbook-ops/skills/develop-runbook/SKILL.md) | Create or improve the procedure |
| [run-runbook](plugins/runbook-ops/skills/run-runbook/SKILL.md) | Run or resume a ready procedure; report results without editing it |

Specify the runbook and request guidance or execution through completion. Inputs and decision criteria come from the runbook; add only overrides or limits. See the [CLI examples](#start-codex-for-a-runbook).

Humans and agents follow the same Steps. Headings describe the work; **Check / Act / Verify** guide the necessary checks, operations, and verification. Commands remain visible in the Markdown.

Keep one procedure per case under the project's `ops/runbooks/`; `ops/inbox/` is optional. General Notes can remain in their Vault. Improve instructions with lessons learned, without adding execution logs or usage dates. Extract a Skill or script only after the work has been validated.

## Start Codex for a runbook

### Human-led execution

From this checkout root, start a new interactive session using `gpt-5.6-luna` with medium reasoning:

```zsh
codex -m gpt-5.6-luna \
  -c 'model_reasoning_effort="medium"' \
  "Use the run-runbook Skill at $PWD/plugins/runbook-ops/skills/run-runbook/SKILL.md.
   Runbook: $PWD/ops/runbooks/organize-downloaded-model-pairs.md.
   Start in human-led mode: inspect current state, explain the next action,
   and let me execute file changes. Do not edit the runbook."
```

Replace the runbook path for another case. Workspace activation is optional for starting Codex; it provides the dedicated venv, history, and prompt.

### Agent execution

The current CLI accepts `--ephemeral` only with `codex exec`, not interactive `codex`. To execute a runbook through completion without persisted Codex session files:

```zsh
codex exec --ephemeral \
  -m gpt-5.6-luna \
  -c 'model_reasoning_effort="medium"' \
  --sandbox workspace-write \
  "Use the run-runbook Skill at $PWD/plugins/runbook-ops/skills/run-runbook/SKILL.md.
   Runbook: $PWD/ops/runbooks/organize-downloaded-model-pairs.md.
   Execute the runbook through completion, including its decisions and operations.
   Stop and report unresolved questions or failures. Do not edit the runbook."
```

Configure any required external-directory write permissions and network access beforehand; `workspace-write` alone does not grant them. The runbook supplies the inputs and procedure.

`exec` is non-interactive and ends after reporting; use the first command for ongoing guidance. Ephemeral mode does not remove shell history or change service-side retention. The selected model must be available to your account.

## Reference

- [Concept](docs/concept.md): purpose and progression toward reusable automation.
- [Usage](docs/runbook-usage.md): workspace settings and execution conventions.
- [Design](docs/design.md): the small responsibility boundary.
- [Policy](plugins/runbook-ops/references/runbook-policy.md): shared authoring rules.
- [Model organization](ops/runbooks/organize-downloaded-model-pairs.md): one case, not the basis of every runbook.
