---
name: writing-semantics
description: 'Use when code needs a K language definition — creating semantics.k, reusing an existing semantics, or extending one after krun gets stuck on an unmodeled construct.'
---

## Artifact contract

`semantics.k` is a reusable definition of the language constructs exercised by
the program set. Check for it before writing:

| State | Action |
|---|---|
| A suitable semantics exists | Reuse it; do not create a task-specific copy |
| It exists but `krun` gets stuck | Extend only the unmodeled construct |
| None exists | Create the smallest executable semantics needed by the programs |

The result must parse the target programs, execute the modeled constructs, and
stop visibly on anything outside its supported subset.

## 1. Inventory the construct set

Read the target code and representative examples. List every expression,
statement, control-flow form, and state component they exercise. Use that list
as the scope: every listed construct needs syntax and behavior; absent
constructs stay unmodeled.

## 2. Choose the representation

Default to the smallest abstract syntax that stays recognizably aligned with the
source program. Use concrete source grammar when parsing the original files is
part of the goal. Use a lower IR only when the input already arrives in that
form, and use pure K functions only for stateless computations.

Record the choice and its reason in `semantics.k`. Do not present several
equivalent representations without selecting a default.

## 3. Define the configuration

Add one cell for each state component in the inventory:

- `<k>` for the current computation
- a bindings/state cell for program variables
- heap, stack, I/O, or other cells only when the target constructs require them

Keep the initial configuration explicit and avoid cells that no rule reads or
writes.

## 4. Add one construct at a time

For each inventory item:

1. Add the smallest syntax production that represents it.
2. Add its evaluation order when subterms must reduce first.
3. Add the operational rule or rules.
4. Run a focused example before moving to the next construct.

When creating a definition from scratch, adapt the single
[stateful semantics template](../shared/semantics-template.md). For concrete
grammar, read [K syntax and operational semantics](../shared/k-syntax.md)
for precedence groups, brackets, identifier tokens, cells, and rewrite syntax.

If a loop or recursive construct will be summarized by an invariant claim,
ensure its rules return to a stable recurring configuration. The claim must
match the term and cells the semantics actually reaches; do not copy an
unrelated loop encoding solely because it appears in an example.

## 5. Smoke-test the semantics

Compile and run every representative program using
[running-k.md](../shared/running-k.md):

- Compare the final configuration with a hand-calculated result.
- Include boundary behavior such as a loop with zero iterations.
- Confirm that each inventory construct is exercised by at least one example.
- Preserve the exact command, exit status, and output for failures.

Do not proceed to `writing-spec` until the examples execute as intended.

## 6. Extend from a stuck state

When `krun` stops with a residual term:

1. Read the front of `<k>` and the relevant side conditions.
2. Identify the single missing or non-applicable rule.
3. Add the minimum syntax or behavior needed for that construct.
4. Rerun the failing example.
5. Rerun earlier examples to detect regressions.

The unmatched term is evidence of an incomplete model, not permission to widen
the semantics speculatively.
