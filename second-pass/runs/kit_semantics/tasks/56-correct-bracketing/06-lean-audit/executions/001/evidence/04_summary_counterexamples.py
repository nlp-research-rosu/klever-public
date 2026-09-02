#!/usr/bin/env python3
"""Independent finite checks; does not import or execute frozen candidate code."""
from itertools import product


def source_loop_model(text: str) -> bool:
    balance = 0
    valid = True
    for character in text:
        balance += 1 if character == '<' else -1
        if balance < 0:
            valid = False
    return valid and balance == 0


def bracket_delta(text: str) -> int:
    if not text:
        return 0
    return (1 if text[0] == '<' else -1) + bracket_delta(text[1:])


def bracket_prefix_ok(text: str, balance: int) -> bool:
    if not text:
        return True
    next_balance = balance + (1 if text[0] == '<' else -1)
    return next_balance >= 0 and bracket_prefix_ok(text[1:], next_balance)


def bracket_chars(text: str) -> bool:
    if not text:
        return True
    return text[0] in '<>' and bracket_chars(text[1:])


def bracket_correct(text: str) -> bool:
    return bracket_prefix_ok(text, 0) and bracket_delta(text) == 0


samples = [''.join(chars) for length in range(9) for chars in product('<>', repeat=length)]
extended = samples + ['x', '<x', 'x>', '><', '<', '>', '<<>>', '<><>', '<<>']
mismatches = [text for text in extended if bracket_correct(text) != source_loop_model(text)]
print('COMMAND: exhaustive compare independent recurrence model with independent source-loop model over all bracket strings of length <= 8 and adversarial non-domain cases')
print(f'bracket_domain_sample_count={len(samples)}')
print(f'extended_sample_count={len(extended)}')
print(f'mismatch_count={len(mismatches)}')
print(f'mismatches={mismatches!r}')

adversarial = {
    'constant_delta_zero_refuted_by_<': bracket_delta('<') != 0,
    'constant_prefix_true_refuted_by_>': bracket_prefix_ok('>', 0) is False,
    'constant_chars_true_refuted_by_x': bracket_chars('x') is False,
    'constant_correct_true_refuted_by_<': bracket_correct('<') is False,
    'identity_like_delta_length_refuted_by_>': bracket_delta('>') != len('>'),
    'prefix_only_correct_refuted_by_<': not (bracket_prefix_ok('<', 0) and bracket_correct('<')),
}
for name, passed in adversarial.items():
    print(f'{name}: {passed}')
if mismatches or not all(adversarial.values()):
    raise SystemExit('SUMMARY_OPERATIONAL_CHECK_FAILED')
print('SUMMARY_OPERATIONAL_CHECK: PASS')
