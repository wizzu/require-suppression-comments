"""Tests for require_suppression_comments."""

from pathlib import Path

from require_suppression_comments import check_file


def write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "sample.py"
    p.write_text(content, encoding="utf-8")
    return p


# --- Passing cases ---


def test_no_suppressions(tmp_path: Path) -> None:
    assert check_file(write(tmp_path, "x = 1\ny = 2\n")) == []


def test_noqa_with_comment(tmp_path: Path) -> None:
    p = write(tmp_path, "# E501: long line is intentional\nx = 1  # noqa: E501\n")
    assert check_file(p) == []


def test_nosec_with_comment(tmp_path: Path) -> None:
    p = write(tmp_path, "# B404: subprocess is required here\nimport subprocess  # nosec B404\n")
    assert check_file(p) == []


def test_noqa_no_rule_id_needs_only_a_comment(tmp_path: Path) -> None:
    assert check_file(write(tmp_path, "# reason\nx = 1  # noqa\n")) == []


def test_nosec_no_rule_id_needs_only_a_comment(tmp_path: Path) -> None:
    assert check_file(write(tmp_path, "# reason\nimport subprocess  # nosec\n")) == []


def test_contiguous_comment_block_above_counts(tmp_path: Path) -> None:
    p = write(tmp_path, "# first line of explanation\n# E501: second line\nx = 1  # noqa: E501\n")
    assert check_file(p) == []


def test_prose_mention_in_comment_not_flagged(tmp_path: Path) -> None:
    p = write(tmp_path, "# This checks for # noqa annotations in source\nx = 1\n")
    assert check_file(p) == []


def test_prose_mention_in_docstring_not_flagged(tmp_path: Path) -> None:
    p = write(tmp_path, '"""Use # noqa to suppress warnings."""\nx = 1\n')
    assert check_file(p) == []


# --- Failing cases ---


def test_noqa_without_comment(tmp_path: Path) -> None:
    violations = check_file(write(tmp_path, "x = 1  # noqa: E501\n"))
    assert len(violations) == 1
    assert "explanatory comment" in violations[0]


def test_nosec_without_comment(tmp_path: Path) -> None:
    violations = check_file(write(tmp_path, "import subprocess  # nosec B404\n"))
    assert len(violations) == 1
    assert "explanatory comment" in violations[0]


def test_noqa_rule_id_not_in_comment(tmp_path: Path) -> None:
    violations = check_file(write(tmp_path, "# some reason without the ID\nx = 1  # noqa: E501\n"))
    assert len(violations) == 1
    assert "E501" in violations[0]


def test_nosec_rule_id_not_in_comment(tmp_path: Path) -> None:
    violations = check_file(write(tmp_path, "# some reason\nimport subprocess  # nosec B404\n"))
    assert len(violations) == 1
    assert "B404" in violations[0]


def test_blank_line_breaks_comment_block(tmp_path: Path) -> None:
    # A blank line between comment and annotation means the block is empty
    violations = check_file(write(tmp_path, "# reason\n\nx = 1  # noqa: E501\n"))
    assert len(violations) == 1


def test_multiple_violations(tmp_path: Path) -> None:
    content = "import subprocess  # nosec\nx = 1  # noqa\n"
    assert len(check_file(write(tmp_path, content))) == 2
