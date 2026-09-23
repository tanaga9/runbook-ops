# Design

| Location | Responsibility |
| --- | --- |
| `codex-model.txt` | Shared model name read by Codex invocation commands |
| `runbook.command` | macOS launcher for an interactive workspace |
| `shell/` | Enter/leave a venv, isolated history, and prompt; no task logic |
| `plugins/runbook-ops/` | Skills and policy for writing and following readable procedures |
| `ops/runbooks/` | Case-specific goals, inputs, choices, operations, and verification |
| `src/` | Small, domain-independent utilities; no case decisions or workflow execution |
| `tests/` | Automated tests for `src/` utilities only |
| `.venv/`, `.state/` | Untracked runtime and history |

The two Skills are the behavioral entrypoints: development changes the procedure; execution follows it within the request and reports results. The shell is optional workspace support, not the execution engine. Model selection belongs to Codex invocation, not the runbook format.

Runbooks own task-specific selection, decisions, operations, and verification. Shared utilities handle only narrowly defined mechanics; their use must not hide the procedure. Add shared code for demonstrated reuse, not to accommodate a single case.

See the [writing policy](../plugins/runbook-ops/references/runbook-policy.md) for procedure rules and [usage](runbook-usage.md) for workspace behavior.

`tests/` excludes shell startup and individual runbooks. Check those separately with syntax checks or temporary fixtures when needed; do not add their tests to the repository.

Validation:

```zsh
python3 -m unittest discover -s tests -v
for file in runbook.command shell/*.zsh shell/startup/.zshenv shell/startup/.zshrc; do
  zsh -n "$file" || break
done
```

Document project-specific conventions and runnable examples. Link to official tool documentation for general settings and behavior; repeat only what is necessary to use this project.
