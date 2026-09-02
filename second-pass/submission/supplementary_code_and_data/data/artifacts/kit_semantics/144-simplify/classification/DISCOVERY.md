# K proof trust-boundary discovery

## Canonical scope

This classification treats `/reference/rule-inventory.json` as exhaustive. Its
copied inventory digest is
`377ee46b909ba5c403e738ed5881c00cd31e73905dce6f16656b3a11ce90bc86`.
The canonical inventory contains 21 rules in order: 19 in
`VERIFICATION-BASE` and two in `VERIFICATION`. No inventoried rule carries the
`simplification` attribute.

| Classification | Count |
|---|---:|
| `DEFINITION` | 19 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 2 |

## Definitions of fresh verification symbols

All 19 `VERIFICATION-BASE` rules are defining equations of symbols introduced
by `VERIFICATION-SYNTAX`, which is the required distinction from facts about
operations defined elsewhere.

- `rule-0536ecbc6d3f76e04fef239eb46e11565972c969524a4846e4bfd312991728fc`,
  `rule-03341577c42ecf18c19a69fb0d413466667f1e67be8d33e40ec997c8089db425`,
  and
  `rule-dc4da1bba542df01424716eaa5cec1e8cb47a224139dcf3b50161a3a61a0fc2f`
  define the fresh named AST terms `simplifyLoopBody`, `simplifyReturn`, and
  `simplifyBody`.
- `rule-423f0ccc1d71ce2e8ab972feaa1a91a96473a1d5b2a97878ac879af42ebd7107`
  defines the fresh `simplifyScope` structural helper.
- Rules
  `rule-f1ef843071e8a6abf454b6596e19692d75252fccde56ee16f0023fd67e0751f8`
  through
  `rule-29420698c187a62acf4393474868871926be3d1f6638ad707eed539b6210cf42`
  are the base, consuming recurrence, and totalizing equations of the fresh
  `validScan` mathematical predicate.
- Rules
  `rule-72367b8115f3c7009ae95867ba6dec860fe55fec72d6ee2af65ef47581433ccd`
  through
  `rule-2f365406bfb7c5bb036e64ff8dc624e350765837cbe5e0d147e8649cf5d6b70e`
  are the terminal, slash, and phase-specific digit equations of the fresh
  `scanResult` summary.

These equations are definitions because their left-hand symbols are local and
fresh. None is merely a rewrite asserting a fact about a hook or a function
defined by the reference semantics.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules under the required identical-statement
test.

The mounted Stage 1 evidence does show a sound-looking proof order. In
`prove.sh`, `verification.k` is first compiled with
`--main-module VERIFICATION-BASE`; `kprove loop-spec.k` then runs against
`verification-base-kompiled`, a module closure that excludes both bridge rules.
The mounted `PROOF.md` records `#Top` and exit 0 for that seven-claim command.
Only afterward does `prove.sh` compile `--main-module VERIFICATION` and use the
two bridge rules in the target proof.

That ordering is insufficient for the stricter category because the installed
statements are not identical to any prior claim:

- The installed `loop-digit-bridge` has symbolic phase `P`, equality-guarded
  variables for the loop body, return statements, callee scope, and builtin
  scope, and a head-form `validScan` condition. `loop-spec.k` instead proves
  four statements named `loop-phase-0` through `loop-phase-3`, each fixing a
  literal phase and exact terms and using the corresponding unfolded tail
  condition.
- The installed `loop-slash-bridge` likewise has symbolic `P` and equality
  guards. `loop-spec.k` proves three distinct literal-phase statements named
  `loop-slash-0` through `loop-slash-2`.

The case families may support a mathematical argument that their union implies
the generic bridges after unfolding definitions, but neither generic rule's
identical statement is first submitted to `kprove`. Consequently no inventoried
rule meets the exact mounted-evidence requirement for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543`
  (`loop-digit-bridge`); and
- `rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650`
  (`loop-slash-bridge`).

Both priority rules rewrite an existing operational `#loop` configuration to
the fresh `scanResult` summary. They are not equations defining a fresh symbol,
and they are proof-specific execution summaries rather than ordinary execution
or observation rules inherited as part of the verification model. Because the
prior Stage 1 claims are specialized rather than identical, the two generic
bridge facts remain trusted mathematical additions for this classification.

There are no canonical local rules classified as `OPERATIONAL_RULE`; the
ordinary imported reference-semantics rules are outside the launcher-provided
local inventory by construction.
