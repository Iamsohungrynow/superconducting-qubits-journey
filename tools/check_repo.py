"""Check local Markdown targets and Python syntax; no network or dependencies.

Run from any directory: python /path/to/repo/tools/check_repo.py
External URLs and Markdown heading anchors are outside this check's scope.
"""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    markdown = [*ROOT.glob("*.md"), *ROOT.glob("tutorial/*.md"),
                *ROOT.glob("hands-on/**/*.md"), *ROOT.glob("reading-list/*.md")]
    errors = []
    links = 0
    for path in markdown:
        source = path.read_text(encoding="utf-8")
        # Math such as [P(0)-P_inf](1-L-S) is not a Markdown hyperlink.
        source = re.sub(r"\$\$.*?\$\$", "", source, flags=re.S)
        source = re.sub(r"(?<!\\)\$.*?(?<!\\)\$", "", source)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", source):
            if target.startswith(("https:", "http:", "mailto:", "#")):
                continue
            if path == ROOT / "README.md" and target == "../../issues":
                continue  # GitHub repository-relative issues URL, not a local file.
            links += 1
            if not (path.parent / target.split("#", 1)[0]).exists():
                errors.append(f"{path.relative_to(ROOT)}: missing {target}")
    scripts = [*ROOT.glob("hands-on/**/*.py"), *ROOT.glob("tutorial/**/*.py"),
               *ROOT.glob("tools/*.py")]
    for path in scripts:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as error:
            errors.append(str(error))
    for error in errors:
        print(error)
    print(f"Checked {links} local links and {len(scripts)} Python files; {len(errors)} errors")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
