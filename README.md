# require-suppression-comments

A [pre-commit](https://pre-commit.com/) hook that requires explanatory comments on lint suppression annotations (`# nosec`, `# noqa`).

Lint suppressions silence a tool without leaving any trace of why. Over time this leads to suppressions that nobody remembers adding, can't be safely removed, and may be hiding real issues. This hook ensures every suppression has a documented reason, making them reviewable and eventually removable.

## Rules

- Every suppression annotation must have a non-empty comment on the immediately preceding line (or as part of a contiguous comment block above it).
- If the annotation specifies a rule ID (e.g. `# nosec B404`, `# noqa: C901`), that ID must appear somewhere in the preceding comment block.

## Usage

### As a pre-commit hook

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/wizzu/require-suppression-comments
  rev: v0.1.2
  hooks:
    - id: require-suppression-comments
```

### As a uv dev dependency

Add to your `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["require-suppression-comments"]

[tool.uv.sources]
require-suppression-comments = { git = "https://github.com/wizzu/require-suppression-comments", tag = "v0.1.2" }
```

Then call it from your `Makefile` or CI:

```
uv run --extra dev require-suppression-comments src/ tests/
```

## Examples

**Bad** — suppression with no explanation:

```python
import subprocess  # nosec B404
```

**Good** — subprocess is intentional and the reason is on record:

```python
# B404: subprocess is required here; input is validated by the caller
import subprocess  # nosec B404
```

---

**Bad** — rule ID suppressed silently:

```python
API_KEY = os.getenv("API_KEY", "")  # noqa: S105
```

**Good** — explains why the false positive is safe to suppress:

```python
# S105: this is an env var lookup, not a hardcoded secret
API_KEY = os.getenv("API_KEY", "")  # noqa: S105
```

---

**Bad** — broad suppression with no context:

```python
result = eval(user_input)  # nosec
```

**Good** — acknowledges the risk explicitly:

```python
# input is pre-validated against an allowlist before reaching this point
result = eval(user_input)  # nosec
```

## Standalone use

```
python3 require_suppression_comments.py [path ...]
```

Defaults to `src/` and `tests/` if no paths are given. Exits 0 if compliant, 1 if violations found.

## Development

```
make setup    # create venv and install dev deps
make check   # lint + tests
make lint    # ruff, bandit, mypy, self-check
make test    # pytest
make format  # reformat with ruff
```
