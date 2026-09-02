# K proof trust-boundary discovery

The canonical inventory has SHA-256
`65a80456e2486aba2385525ca47f8bd379c67748ed794c2522038958351743f4`
and contains three rules, all from the `VERIFICATION` module. Each inventory
rule appears exactly once in `trust-boundary.json`, in canonical inventory
order.

## Classification

- `rule-f99627839f69163b45f7724548ffd1e71c6f80dfb7bdbd7578083347002cc84e`
  is a `DEFINITION`. It introduces the named `ascending` summary by expansion
  to the list-equality and sorting helpers.
- `rule-3b19f7a8e59183f961c42635af0892ad86d88a1503a978ee2d19b6ebbbbfbe18`
  is a `DEFINITION`. It expands `duplicateBound` to the at-most-two counting
  summary.
- `rule-15283af6a5fb0ffd622a25de42f40dce807a8a9fa5cc8d22f978f38853963a27`
  is a `DEFINITION`. It expands the named overall contract to the conjunction
  of its two components.

All three canonical entries have empty attribute lists, so there are no
`simplification`-attributed rules requiring a separate check.

## Stage 1 proof evidence

There are no separately proved derived lemmas. Stage 1 `prove.sh` compiles
`semantic.k`—whose module closure already contains all three inventory
rules—and then runs `kprove` on the end-to-end claim in `spec.k`. It does not
first prove the exact statement of any inventory rule against a module lacking
that rule, nor does it subsequently install such a proved statement as a
reusable rule. The mutation proof is an expected-failure validation probe and
does not establish an inventory rule.

The domain-lemma set is empty.
