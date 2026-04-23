# require-suppression-comments

A [pre-commit](https://pre-commit.com/) hook that requires explanatory comments on lint suppression annotations (`# nosec`, `# noqa`).

## Rules

- Every suppression annotation must have a non-empty comment on the immediately preceding line (or as part of a contiguous comment block above it).
- If the annotation specifies a rule ID (e.g. `# nosec B404`, `# noqa: C901`), that ID must appear somewhere in the preceding comment block.

## Usage

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/wizzu/require-suppression-comments
  rev: v1.0.0
  hooks:
    - id: require-suppression-comments
```

## Examples

**Bad** — suppression with no explanation:

```python
import subprocess  # noqa: S603
```

**Good** — suppression with an explanation that mentions the rule ID:

```python
# S603: input is validated by the caller; subprocess call is intentional
import subprocess  # noqa: S603
```

## Standalone use

```
python3 require_suppression_comments.py [path ...]
```

Defaults to `src/` and `tests/` if no paths are given. Exits 0 if compliant, 1 if violations found.
