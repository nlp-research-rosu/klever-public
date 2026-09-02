# Trust-boundary discovery

## Canonical inventory

The sole classification source is
`/reference/rule-inventory.json`. Its copied inventory digest is
`f14289f2f89f2d52117ca7ad185617a5fe6323e4f4b762382a75f2808399ca6a`.
The inventory contains 26 rules, and `trust-boundary.json` preserves their
inventory order and classifies every `source_rule_id` exactly once.

Classification totals:

- `DEFINITION`: 24
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 2

## Definitions

The `intVals` rules define a structural embedding from `IntSeq` to `ValSeq`.
The four `intAt` rules define and totalize a proof-local mathematical indexing
function. The nine `thirdFrom`, `pairFrom`, and `tripleFrom` rules define the
three nested finite searches used by the postcondition.

The remaining nine definition rules are nullary syntax or binding expansions:
`innerCond`, `innerBody`, `middleCond`, `middleBody`, `outerCond`,
`outerBody`, `programBody`, `triplesClosure`, and `solutionBindings`. They name
the translated program terms and closure setup. They do not add execution
behavior, so they are definitions rather than operational rules.

## Operational rules

The operational-rule set is empty. None of the 26 canonical rules has a K-cell
rewrite or adds an observation/execution transition to the verification model.
The source program is executed by the imported reference semantics; the
inventory's source-term rules only expand named proof terms.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1 `prove.sh` first kompiles `verification.k`, which already contains all
26 inventory rules, and then runs `kprove spec.k` against that compiled
definition. It does not first prove either simplification rule—or any other
inventory rule—against a module from which that exact rule is absent.
`spec-vacuity.k` imports `spec.k`, and `spec-body-mutation.k` imports
`verification.k`; their expected failures are ground validation probes, not
universal rule-free proofs of an inventory rule. Thus no mounted Stage 1
evidence satisfies the required ordering and exact-correspondence test for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It consists of exactly:

1. `rule-041ae6f97e0a64393d4fd3489adb8b7922f6bdd833dd98ec4a40214de3ea0864`
   — `vsLen(intVals(IS)) => isLen(IS) [simplification]`.
2. `rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4`
   — guarded
   `valSeqAt(intVals(IS), I) => intAt(IS, I) [simplification]`.

Both rules state additional correspondence facts about helper symbols supplied
by the frozen semantics. They are not equations defining their left-hand
symbols, and both contribute to symbolic loop execution: the first supplies
the symbolic list length and the second supplies indexed integer values.
Although comments and `PROOF.md` describe them as structurally derivable,
Stage 1 does not machine-prove either exact rule before compiling a definition
that contains it. Finite concrete and differential tests, plus result/body
mutation failures, do not establish those universal correspondences.
Accordingly, the required strict classification is `DOMAIN_LEMMA` for both.

Every rule carrying the `simplification` attribute is therefore classified as
`DOMAIN_LEMMA`; no simplification rule is mislabeled as a proved derived lemma.
