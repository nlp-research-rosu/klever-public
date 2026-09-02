from pathlib import Path


source = Path("solution.py").read_text(encoding="utf-8")
needle = '    return "YES"'
if source.count(needle) != 1:
    raise SystemExit("expected exactly one final YES return")
print(source.replace(needle, '    return "NO"'), end="")
