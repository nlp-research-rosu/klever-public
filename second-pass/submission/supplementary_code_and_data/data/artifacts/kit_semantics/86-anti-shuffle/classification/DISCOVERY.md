# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, whose canonical
inventory digest is
`b6a5c8a6de1f4db5b68d5cc26578cacf31fb03dfb7b59d122c3544c81b30760c`.
It contains nine rules from `VERIFICATION`. `trust-boundary.json` preserves
their inventory order and classifies each `source_rule_id` exactly once.

## Classification result

Eight rules are classified `DEFINITION`, and one is classified
`DOMAIN_LEMMA`.

- `antiInnerBody()`, `antiPostInsert()`, `antiOuterBody()`, and `antiTail()`
  are fresh zero-argument symbols introduced by `VERIFICATION`. Their rules
  define those symbols as exact translated AST fragments. They construct named
  proof terms and perform no MPY execution.
- The two `insertGo` rules and two `antiGo` rules define fresh mathematical
  summary symbols introduced by `VERIFICATION`. Their empty/nonempty cases are
  structural recurrence equations over `IntSeq`.
- Canonical rule
  `rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1`
  states
  `strLt(iCons(C, .IntSeq), iCons(D, .IntSeq)) => C <Int D` and carries
  `[simplification]`. `strLt` is defined in the reference semantics; it is not
  a fresh symbol introduced by `VERIFICATION`. The fresh-symbol requirement
  therefore excludes `DEFINITION`. Since a simplification-attributed rule must
  be either `DEFINITION` or `DOMAIN_LEMMA`, this rule is `DOMAIN_LEMMA`.

No canonical rule is an `OPERATIONAL_RULE`: none is an ordinary MPY machine
transition or observation rule. No canonical rule is classified
`PROVED_DERIVED_LEMMA`; the special simplification classification constraint
requires the only separately proved reusable fact to remain `DOMAIN_LEMMA`.

## Separately proved derived lemma and Stage 1 evidence

The singleton-string `strLt` fact above is the only reusable inventory rule
for which Stage 1 supplies separate derivation evidence.

1. `/reference/k-proof/lemma-spec.k` requires only
   `reference-semantics/semantics.k`, and `LEMMA-SPEC` imports `MPY`, not
   `VERIFICATION`. The proof module therefore does not contain the local
   simplification rule.
2. Its claims `single-char-str-lt-less`,
   `single-char-str-lt-greater`, and `single-char-str-lt-equal` partition all
   pairs of integer character codes. They prove `strLt` returns respectively
   `true`, `false`, and `false`, exactly matching the evaluation of
   `C <Int D` in all three cases.
3. `/reference/k-proof/prove.sh` compiles the unextended reference semantics
   with main module `MPY` into `lemma-kompiled` and runs
   `kprove lemma-spec.k --definition lemma-kompiled --spec-module LEMMA-SPEC`
   before it compiles `verification.k`, which introduces the simplification.
4. `/reference/k-proof/PROOF.md` records that this bridge-free lemma proof
   printed `#Top` and exited 0.

This is machine-checked supporting evidence for the domain lemma. It does not
change the required JSON class: the rule is a simplification fact about a
non-fresh reference-semantics operation, so it remains `DOMAIN_LEMMA` rather
than `DEFINITION` or `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly
`rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1`,
the singleton-string `strLt` simplification. The separate Stage 1 proof is
evidence for this fact, but under the required taxonomy it remains the one
additional mathematical fact in the local verification closure.

## Trust-boundary consequence

Within the launcher-defined local verification-module closure, the proof adds
eight fresh-symbol syntax/summary definitions and one singleton-order domain
lemma. It adds no operational model rules. This classification concerns only
the nine rules in the canonical inventory; it does not reclassify the supplied
reference semantics, K toolchain, translator, or generated program artifacts
outside that inventory.
