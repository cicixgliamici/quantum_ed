"""Report indented display-math delimiters without rewriting lesson content."""

from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def indented_delimiters(document: Path) -> list[int]:
    """Return suspect display-math line numbers outside fenced code examples."""
    line_numbers = []
    fence = None
    for number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[0]
            length = len(stripped) - len(stripped.lstrip(marker))
            if fence is None:
                fence = (marker, length)
            elif marker == fence[0] and length >= fence[1] and not stripped[length:].strip():
                fence = None
        elif fence is None and line.strip() == "$$" and line != line.lstrip():
            line_numbers.append(number)
    return line_numbers


def main() -> int:
    """Offer a review aid; indentation can be intentional inside Markdown lists."""
    findings = [
        f"{document.relative_to(REPOSITORY_ROOT).as_posix()}:{number}: indented display-math delimiter"
        for document in sorted((REPOSITORY_ROOT / "docs").rglob("*.md"))
        for number in indented_delimiters(document)
    ]
    print("\n".join(findings) if findings else "No indented display-math delimiters found.")
    # This is a diagnostic, not a formatter: list context requires human review.
    return 0


if __name__ == "__main__":
    sys.exit(main())
