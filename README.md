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
| [run-runbook](plugins/runbook-ops/skills/run-runbook/SKILL.md) | Run a ready procedure; report results and write improvement proposals |

Specify the runbook and request guidance or execution through completion. Inputs and decision criteria come from the runbook; add only overrides or limits. See the [CLI examples](#start-codex-for-a-runbook).

Humans and agents follow the same Steps. Headings describe the work; **Check / Act / Verify** guide the necessary checks, operations, and verification. Commands remain visible in the Markdown.

Keep one procedure per case under the project's `ops/runbooks/`; `ops/inbox/` is optional. General Notes can remain in their Vault. Improve instructions with lessons learned, without adding execution logs or usage dates. Extract a Skill or script only after the work has been validated.

## Start Codex for a runbook

Run from this checkout root; workspace activation is optional. Both examples authorize Codex to execute the runbook.

- **Model:** edit [codex-model.txt](codex-model.txt), containing one model name without quotes or comments. It also applies to the runbook's optional Codex recommendation.
- **Paths:** for another case, change the runbook path and each `--add-dir` to match its external write locations.
- **Permissions:** these examples enable automatic approval review and network access for API retrieval. Adjust them for the case; see the official [Codex configuration reference](https://developers.openai.com/codex/config-reference).

### Interactive execution

Start here: execute the runbook and resolve operational questions through conversation. The execution model writes improvement proposals instead of changing the procedure:

```zsh
codex -m "$(< codex-model.txt)" \
  -c 'model_reasoning_effort="medium"' \
  -c 'sandbox_workspace_write.network_access=true' \
  --approve-for-me \
  --add-dir "$HOME/Downloads" \
  --add-dir "/Volumes/EHDD/AIModels/Lora" \
"Use the run-runbook Skill at $PWD/plugins/runbook-ops/skills/run-runbook/SKILL.md.
Runbook: $PWD/ops/runbooks/organize-downloaded-model-pairs.md.
Execute the runbook through completion, including its decisions and operations.
When issues arise, pause the affected operation and resolve them with me.
Do not edit the runbook, code, Skills, or documentation.
Save actionable improvement proposals using the Skill's proposal workflow."
```

### Non-interactive execution

Once the procedure is stable, use `codex exec` to execute and report results. It can also save improvement proposals without waiting for a conversation:

```zsh
codex exec --ephemeral \
  -m "$(< codex-model.txt)" \
  -c 'model_reasoning_effort="medium"' \
  -c 'sandbox_workspace_write.network_access=true' \
  --approve-for-me \
  --add-dir "$HOME/Downloads" \
  --add-dir "/Volumes/EHDD/AIModels/Lora" \
"Use the run-runbook Skill at $PWD/plugins/runbook-ops/skills/run-runbook/SKILL.md.
Runbook: $PWD/ops/runbooks/organize-downloaded-model-pairs.md.
Execute the runbook through completion, including its decisions and operations.
Stop dependent work on unresolved questions or failures.
Do not edit the runbook, code, Skills, or documentation.
Save actionable improvement proposals using the Skill's proposal workflow."
```

### Review and improve separately

Use the lower-cost model in `codex-model.txt` for execution. In a separate session with a more capable model, pass the proposal path and request `develop-runbook`. Review the evidence and related runbooks, documentation, Skills, and code before choosing the smallest coherent change. Proposals are inputs for review, not instructions to apply verbatim; keep case-specific logic out of shared infrastructure.

Example request: “Use develop-runbook to review this proposal and improve the affected procedure and related documentation: `<proposal path>`. Validate changed behavior without operating on real targets.”

## Reference

- [Concept](docs/concept.md): purpose and progression toward reusable automation.
- [Usage](docs/runbook-usage.md): workspace settings and execution conventions.
- [Design](docs/design.md): the small responsibility boundary.
- [Policy](plugins/runbook-ops/references/runbook-policy.md): shared authoring rules.
- [Model organization](ops/runbooks/organize-downloaded-model-pairs.md): one case, not the basis of every runbook.
