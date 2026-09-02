# K proof trust-boundary discovery

## Inventory and method

This classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory. Its copied inventory digest is
`c04282fc757603f0913951a3cb0f2efdda4db8509cb2b8147081a93a2fafd6a5`.
All 42 canonical rules appear exactly once and in canonical order in
`trust-boundary.json`.

The classifications were determined from rule behavior, attributes, the module
import closure in `/reference/k-proof/verification.k`, the exact connection
claims, and the command order in `/reference/k-proof/prove.sh`. Comments in the
K files were treated only as navigation, not as proof evidence.

The totals are:

- `DEFINITION`: 34
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 3
- `DOMAIN_LEMMA`: 5

Every inventory rule carrying a `simplification` attribute is classified as
either `DEFINITION` or `DOMAIN_LEMMA`, as required.

## Definitions

The 34 definitions consist of:

- the three exact-body macros;
- the structurally recursive score, last-value, domain-predicate, scan, and
  expected-result equations;
- constructor projections `codesOf` and `codesProject`; and
- the concrete, string-sorted, and guarded symbolic evaluator equations that
  define the fresh `projectStrTotal` proof term.

The strict and complementary branches of `bestCodes` and `bestScore` are
definitions of the left-to-right scan. Their `simplification` attributes do not
turn those recurrences into independent mathematical assumptions.

## Separately proved derived lemmas

Exactly three inventory rules qualify as `PROVED_DERIVED_LEMMA`. Although each
has an operational effect when reused, the requested derived-lemma class
applies because Stage 1 first proves the exact rule statement in a module
closure that does not contain that rule.

### Yield transition

- Rule:
  `rule-05fb239fa7d84ad38b130f860d5cad75a99454c981299773ce0d33be967377c1`
  (`verification.k` lines 227–242).
- Exact prior claim: `CONNECTION-SPEC.yield-connection`
  (`connection-spec.k` lines 12–27).
- Exclusion evidence: the claim imports `VERIFICATION-BASE`; `prove.sh` lines
  28–34 compile with `--main-module VERIFICATION-BASE`. The rule exists only in
  the later `VERIFICATION` module.
- Result: the first connection-proof command exits 0 and its aggregate result
  is `#Top` in `prove.log` line 161.

The claim and rule have the same guarded
`#iterYield`/`#loopStep` transition, target, body, remaining list, and arbitrary
continuation frame.

### Inner-loop transition

- Rule:
  `rule-d4fd40e7ad8014f7bfbe85e55672a9223d483b4340406df7a11b164baad18f9a`
  (`verification.k` lines 246–272).
- Exact prior claim: `CONNECTION-SPEC.inner-loop`
  (`connection-spec.k` lines 30–55).
- Exclusion evidence: this claim is proved by the same
  `VERIFICATION-BASE` compilation at `prove.sh` lines 28–34, while the reusable
  rule is declared only in `VERIFICATION`.
- Result: the connection specification, including this claim, exits 0 with
  aggregate `#Top` at `prove.log` line 161.

The rule and claim match the same complete seven-binding scope, environment,
continuation frame, loop target/body, strength update, and character update.

### Outer-loop transition

- Rule:
  `rule-bda0da317a1b8673b460bc4e897723f6797b27172c3dd91e797bbae2cd92b9f0`
  (`verification.k` lines 280–313).
- Exact prior claim: `OUTER-CONNECTION-SPEC.outer-loop`
  (`outer-connection-spec.k` lines 7–39).
- Exclusion evidence: `prove.sh` lines 37–43 compile
  `--main-module VERIFICATION`. That closure contains the two already proved
  rules above but excludes the later `TARGET-VERIFICATION` module where this
  outer rule is declared.
- Result: the outer connection proof exits 0 with `#Top` at `prove.log` line
  290.

The rule and claim have the same `allStrings(VS)` guard, complete scope,
arbitrary continuation frame, loop term, and updates to all five loop-modified
locals.

The final target build occurs only afterward at `prove.sh` lines 46–52, where
all three derived transitions are reusable and the target specification
finishes with `#Top` at `prove.log` line 443.

No canonical rule remains classified as `OPERATIONAL_RULE`: all three
verification-local operational bridges meet the stronger exact-prior-proof
criterion above.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these five rules:

1. `rule-5d8f9b167e5284a82cd2a8ee7541fd69dfe8a2bfa3b401b3e610658fe9b05de3`
   characterizes `#Ceil` of K's existing partial `Val`-to-`Str` projection.
2. `rule-db9d27e9548a05d29d1ed50dae5699e3007e66b4be241553668c21d60b3a10ae`
   rewrites that existing projection back to `projectStrTotal`.
3. `rule-f85e27b93f985712e161e1d9f93c9edc4bb9b998f80b67e076ae37e57255f5e0`
   adds idempotence of `projectStrTotal`.
4. `rule-334fd615c749b4780fa187ec0618b959d5589b042350fb2e8ff133c457d4d2f1`
   characterizes equality between a `Val` and its total string projection.
5. `rule-10e1728036a93b9cdbc0c9743281a9e89436ffbf8433c0b87d6741769b463133`
   characterizes equality between a `Val` and its reconstruction through
   `codesProject`.

These are reusable simplification facts about K's datatype projection,
definedness, equality, or a derived idempotence property. Stage 1 does not
first prove any of their exact statements in a module lacking the rule.
In particular, `CONNECTION-SPEC.projection-identity` is not exact prior evidence
for them: it is a differently oriented reachability claim, and `prove.log`
records it as `WarnTrivialClaim` before the connection specification's `#Top`.
Consequently none of these five is labeled `PROVED_DERIVED_LEMMA`.

The remaining simplification-bearing rules are definitional evaluator or scan
equations. No unproved helper was promoted to `PROVED_DERIVED_LEMMA` on the
strength of a source comment.
