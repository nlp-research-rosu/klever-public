#!/usr/bin/env bash
set -euo pipefail

nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
sed -n '1,220p' /reference/k-proof/prompt.py
sed -n '1,240p' /reference/k-proof/solution.py

rg -n \
  'validDateProgram|asciiDigit|validMonthDay|validDateResult|simplification' \
  /reference/k-proof/verification.k \
  /reference/k-proof/spec.k \
  /reference/k-proof/reference-semantics

cmp \
  <(tr -d '[:space:]' < /reference/k-proof/solution.mpy) \
  <(tr -d '[:space:]' < /reference/k-proof/verification-program.mpy)

python3 - <<'PY'
import json

def source_behavior(date):
    if len(date) != 10:
        return False
    if date[2] != '-' or date[5] != '-':
        return False
    codes = [ord(character) - 48 for character in date]
    for index in (0, 1, 3, 4, 6, 7, 8, 9):
        if codes[index] < 0 or codes[index] > 9:
            return False
    month = codes[0] * 10 + codes[1]
    day = codes[3] * 10 + codes[4]
    if month == 2:
        return 1 <= day <= 29
    if month in (4, 6, 9, 11):
        return 1 <= day <= 30
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 1 <= day <= 31
    return False

def summary(date):
    if len(date) != 10:
        return False
    code = list(map(ord, date))
    ascii_digit = lambda value: 48 <= value <= 57
    month = (code[0] - 48) * 10 + code[1] - 48
    day = (code[3] - 48) * 10 + code[4] - 48
    valid_month_day = (
        (month == 2 and 1 <= day <= 29)
        or (month in (4, 6, 9, 11) and 1 <= day <= 30)
        or (month in (1, 3, 5, 7, 8, 10, 12) and 1 <= day <= 31)
    )
    return (
        code[2] == 45
        and code[5] == 45
        and all(ascii_digit(code[index]) for index in (0, 1, 3, 4, 6, 7, 8, 9))
        and valid_month_day
    )

cases = [
    '', '03-11-2000', '15-01-2012', '04-0-2040', '06-04-2020',
    '06/04/2020', '02-29-2000', '02-30-2000', '04-30-2000',
    '04-31-2000', '01-31-2000', '01-32-2000', '00-01-2000',
    '13-01-2000', '03-11-20a0', '٠3-11-2000',
]

tested = set(cases)
for month in range(100):
    for day in range(100):
        tested.add(f'{month:02d}-{day:02d}-2000')
for position in range(10):
    for codepoint in range(128):
        value = list('03-11-2000')
        value[position] = chr(codepoint)
        tested.add(''.join(value))
for length in range(13):
    tested.add(('03-11-2000' + 'x' * 12)[:length])

mismatches = [
    value for value in sorted(tested)
    if source_behavior(value) != summary(value)
]

def february_28_mutant(date):
    if len(date) != 10:
        return False
    code = list(map(ord, date))
    if not all(48 <= code[index] <= 57 for index in (0, 1, 3, 4, 6, 7, 8, 9)):
        return False
    month = (code[0] - 48) * 10 + code[1] - 48
    day = (code[3] - 48) * 10 + code[4] - 48
    return code[2] == 45 and code[5] == 45 and (
        (month == 2 and 1 <= day <= 28)
        or (month in (4, 6, 9, 11) and 1 <= day <= 30)
        or (month in (1, 3, 5, 7, 8, 10, 12) and 1 <= day <= 31)
    )

print(json.dumps({
    'finite_scope_count': len(tested),
    'finite_mismatch_count': len(mismatches),
    'finite_mismatches': mismatches[:20],
    'named_cases': {
        value: {
            'source_behavior': source_behavior(value),
            'summary': summary(value),
        }
        for value in cases
    },
    'counterfactuals': {
        'february_28_at_02_29_2000': {
            'source_behavior': source_behavior('02-29-2000'),
            'mutant_summary': february_28_mutant('02-29-2000'),
        },
        'omitting_year_digit_check_at_03_11_20a0': {
            'source_behavior': source_behavior('03-11-20a0'),
            'would_change_result_to': True,
        },
        'omitting_separator_check_at_03_slash_11_2000': {
            'source_behavior': source_behavior('03/11/2000'),
            'would_change_result_to': True,
        },
    },
}, indent=2, sort_keys=True, ensure_ascii=False))
PY
