# Differential input scope

The executable input generator is preserved in `differential_test.py`.

- All four documented examples from the trusted prompt.
- Sixteen explicit values covering empty input and every branch boundary:
  empty; one-character ASCII letter/non-letter; two-or-more characters with an
  alphabetic/non-alphabetic final character; and alphabetic final characters
  with a space/non-space predecessor.
- Ten explicit Unicode boundaries, including accented Latin, Greek, CJK,
  combining marks, and sharp S.
- Every string of length zero through four over the eight-symbol alphabet
  `(" ", "a", "Z", "0", "!", "é", "Ω", "\t")`.
- 2,000 deterministic pseudorandom strings of length zero through sixteen over
  ASCII letters, digits, punctuation, whitespace, four non-ASCII letters, and a
  combining acute accent, using seed 134.

Duplicate strings are removed while preserving the first category and order.
The oracle is the trusted `/reference/canonical.py`; the implementation under
test is the scratch copy of `/candidate/solution.py`.
