# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256` `fbc118c61ac46ccc2058ad89ed82f5555f2d49875c3ba47ba8a25b1bc24792e6`.
It contains 21 rules in the local `VERIFICATION` closure. Every rule is present
once in `trust-boundary.json`, in canonical inventory order.

## Classification result

| Classification | Count | Canonical inventory positions |
|---|---:|---|
| `DEFINITION` | 16 | 3–18 |
| `OPERATIONAL_RULE` | 0 | none |
| `PROVED_DERIVED_LEMMA` | 3 | 0–2 |
| `DOMAIN_LEMMA` | 2 | 19–20 |

Rules 3–6 define four fresh macro names for exact MPY constructor terms:
`isVowelBody`, `getClosestLoopBody`, `getClosestBody`, and
`getClosestProgram`. Rules 7–18 are equations of fresh verification functions:
`closestCandidate`, `vowelPred`, `isVowelCode`, `closestQualifies`,
`closestScan`, and `closestVowel`. In particular, the six `[simplification]`
rules at positions 12–17 are defining cases *of* the fresh recursive symbol
`closestScan`, so they are definitions rather than additional facts about an
operation defined elsewhere.

There are no residual `OPERATIONAL_RULE` entries. The three
configuration-rewrite rules that operationally summarize execution satisfy the
stricter separately-proved classification described below.

## Separately proved derived lemmas

### Helper true case

- Installed rule:
  `rule-284c4c4d20e7564f3b85f9ae093aa32298e088fc96aae41906f05d8ef3f0ef15`
  in `helper-verification.k`.
- Prior exact claim: `[helper-vowel]` in `connection-spec.k`.
- Ordering evidence: `prove.sh` first compiles `foundation.k` as
  `connection-kompiled` and runs
  `kprove connection-spec.k --definition connection-kompiled --spec-module CONNECTION-SPEC`.
  `foundation.k` does not import `helper-verification.k`, so this definition
  lacks the installed rule. Only after that proof does `prove.sh` compile
  `helper-verification.k`. `PROOF.md` records `#Top` and exit 0 for this proof.
- Correspondence: after macro expansion and alpha-renaming, the call, `true`
  result, `vowelPred(C)` guard, arbitrary K continuation, and all ordinary
  cells are identical.

### Helper false case

- Installed rule:
  `rule-08d6a79c00e8974a6bd055b18bc2d39ca1d25c682c2008be19c209f460d89d5d`
  in `helper-verification.k`.
- Prior exact claim: `[helper-consonant]` in `connection-spec.k`.
- Ordering evidence: it is proved by the same earlier `connection-spec.k`
  command against `connection-kompiled`, which lacks both helper rules;
  `helper-verification.k` is compiled only afterward. `PROOF.md` records
  `#Top` and exit 0.
- Correspondence: after macro expansion and alpha-renaming, the call, `false`
  result, `notBool vowelPred(C)` guard, arbitrary K continuation, and all
  ordinary cells are identical.

### Loop/return/frame-pop case

- Installed rule:
  `rule-c20cac6fc636336fce2d7dbc24f7aa987c09ce9dd8b4b8e10851db71031a2574`
  in `verification.k`.
- Prior exact claim: `[loop-invariant]` in `loop-connection-spec.k`.
- Ordering evidence: `prove.sh` compiles `helper-verification.k` as
  `loop-connection-kompiled` and runs
  `kprove loop-connection-spec.k --definition loop-connection-kompiled --spec-module LOOP-CONNECTION-SPEC`.
  That module has the previously justified helper rules but does not import
  `verification.k`, so it lacks the installed loop rule. Only after the claim
  proves does `prove.sh` compile `verification.k`. `PROOF.md` records `#Top`
  and exit 0.
- Correspondence: expansion of `getClosestLoopBody` makes the loop syntax
  identical; the exact return/`#endcall` suffix, guard, LHS and RHS state
  changes, and all ordinary cells correspond.

### Mandatory generated-counter residual caveat

This caveat applies separately to all three rules above. K 7.1.293 compiles
each prior claim with an explicit
`<generatedCounter> _Gen0 => ?_Gen1 </generatedCounter>` cell. Thus the proved
claim leaves the final counter existential. The corresponding installed rule
instead carries one preserved `_DotVar:GeneratedCounterCell`. Therefore the
installed rule's counter-preservation assertion is **not credited as proved by
the claim**.

The generated-counter rendering is the only compiled delta: every other cell,
guard, LHS, and RHS term corresponds exactly. The structural side-fact is also
applicable here. `<generatedCounter>` is compiler bookkeeping for fresh-variable
allocation; neither the fixed semantics nor the local source contains a rule
that reads this cell, and the summarized helper and loop computations perform
no fresh-variable allocation. Counter preservation is therefore structurally
expected, while remaining explicitly outside what the reachability claims
established.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly two rules:

- `rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7`
  states that `intSeqAt(CS,I)` is defined under its in-bounds guard. This is a
  `[simplification]` fact about the externally defined `#Ceil` observation and
  the reference-semantics `intSeqAt` operation, not an equation defining a
  fresh verification symbol.
- `rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5`
  states guarded `#Ceil`-definedness of `closestScan`. Although `closestScan`
  itself is fresh, this rule is a fact about its definedness under `#Ceil`, not
  one of its defining equations.

Both rules are already present in `foundation.k` when the first auxiliary
proof definition is compiled. `prove.sh` contains no earlier proof of either
exact statement against a module lacking it. Comments and the Stage 1 prose
describe structural-induction arguments, but that is not separately ordered
machine-checked evidence, so both are classified `DOMAIN_LEMMA` rather than
`PROVED_DERIVED_LEMMA`.
