import re
from pathlib import Path


def compact(path):
    return re.sub(r"\s+", "", Path(path).read_text(encoding="utf-8"))


translated = compact("solution.mpy")
specification = compact("spec.k")

assert translated.startswith("Module(")
assert translated.endswith(")")
translated_function = translated[len("Module(") : -1]

occurrences = specification.count(translated_function)
print(f"translated_function_occurrences_in_entry_spec={occurrences}")
assert occurrences == 1
