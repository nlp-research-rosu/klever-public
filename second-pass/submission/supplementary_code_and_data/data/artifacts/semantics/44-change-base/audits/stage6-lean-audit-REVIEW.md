# Independent audit: HumanEval `44-change-base`

Audit mode was independently read as `CLASSIFICATION_AND_PROOF` from
`/audit-input.json` and `AUDIT_MODE`.  The condition is `semantics` and the
semantics mode is `SUPPLIED_SEMANTICS`.

The protected Stage 3 classification is correct, and Stage 4 is byte-for-byte
the deterministic output of the recorded producer.  Nevertheless, the
generated theorem is not a faithful mathematical rendering of two of the
three domain lemmas: Stage 4 emits `SortScope` as an empty inductive type even
though frozen K defines and operationally constructs `Scope` values.  The
affected target conjuncts are vacuous.  The Stage 5 project builds and has a
clean candidate-level trust boundary, but its `freshScopes` definition also
does not implement the frozen K recurrence.  These are proof-legitimacy
failures, not infrastructure errors.

## Input and producer integrity

Before judging generation, I hashed the immutable producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `3a5a8be795d55a2bc01b73d47099f04795b9d64f6bbcf64494b57bcde8266582` |

Both hashes match `generator-manifest.json` and the generation-time source
manifest.  Their producer bundle tree hash is
`d51304d7acd70db93e839359fc003780b85d84d8ab4fd36ac2ec2a8227f4437b`,
matching `/audit-input.json`.  The generator manifest, source manifest, and
the audit input all identify the same immutable generator image:
`sha256:db04cbaec4c5ee7b34348393f5a7742991e12d63480de3eab85fe97022f51657`.
Thus producer provenance is intact and no `AUDIT_ERROR` applies.

I independently recomputed all recorded Stage 1 source hashes and the mounted
tree hashes.  They match the audit input, including:

- K workspace:
  `bf35f7abd3089fe22dc3395c66123fcc2a5ab11d5cccd02c5eeb42de4481b6b7`
- selected K audit:
  `3114994c621ade99de70f42c1cb45d43454b6eab0c79f8ab114beebce893905c`
- Stage 4 generation:
  `4a9daa58222dd404fde368deb74655321fdf129d66c2f3b1c8d763ad5d9b5e1c`
- Stage 5 candidate:
  `61210e517d845adb92c45566a89ee19d58a99ba9013a909bfb8bc6e17217d59a`

Full results are in
[`01-producer-provenance.log`](evidence/01-producer-provenance.log) and
[`05-hashes-obligations-target.log`](evidence/05-hashes-obligations-target.log).

## Verification-module inventory reconstruction

Using the trusted rule-inventory implementation, I reconstructed the complete
local verification-module closure of frozen `verification.k`.  The closure is
the single local module `VERIFICATION` and contains ten rules.  Independent
recomputation produced:

- `verification.k` SHA-256:
  `13e26a0aeaafdb572c8fa50e205cb7f037031d5928746db9ebee426a413acb5e`
- ordered inventory SHA-256:
  `6d22f78dc4e994c53e63142f6d44ae227e2c41a30f113c97810968f0c36e2308`
- protected manifest SHA-256:
  `c15a16b5f8644134ffb1b27b9db35def15bf64c5316594202e8b4e61134ba10c`

For every rule I independently recomputed its start/end source span,
normalized source text hash, and `source_rule_id`.  The resulting ordered
identity list is bijectively equal to `/reference/lemma-discovery.json`.
There are no omissions, additions, duplicate identities, reordered
identities, or hash changes.  The trusted manifest contract validator also
passes.  The full machine-readable reconstruction is
[`02-inventory-reconstruction.log`](evidence/02-inventory-reconstruction.log).

## Independent Stage 3 classification

The ten rules classify as follows:

| Frozen span | Rule | Judgment |
|---:|---|---|
| 8 | `rule-62ed89…` | `DEFINITION`: empty-map case for the local `freshScopes` summary |
| 9–10 | `rule-437465…` | `DOMAIN_LEMMA`: `freshScopes(L,S)` implies allocator key `L` is absent |
| 11–12 | `rule-5f7d67…` | `DEFINITION`: exact-predecessor recurrence for `freshScopes` |
| 17–18 | `rule-746c49…` | `DOMAIN_LEMMA`: fresh-key map update becomes singleton concatenation |
| 19–20 | `rule-82f2c7…` | `DOMAIN_LEMMA`: deleting that fresh singleton restores the old map |
| 24–43 | `rule-9389ac…` | `DEFINITION`: named translated function-body term |
| 46–49 | `rule-6a85e1…` | `DEFINITION`: named translated solution module |
| 52–53 | `rule-e42c4c…` | `DEFINITION`: named closure proof term |
| 58 | `rule-a24b26…` | `DEFINITION`: zero equation for `baseDigits` |
| 59–64 | `rule-91e339…` | `DEFINITION`: positive quotient/remainder recurrence for `baseDigits` |

There are seven definitions, three domain lemmas, no ordinary operational
rules in the local verification module, and no proved-derived lemmas.  Stage 1
does not first prove any of these exact rules against a module from which the
rule was removed.  Both `[simplification]` rules are definitions.

The domain lemmas are relevant to this program and postcondition.  The source
recursively computes the prefix at `x // base`, appends the character for
`x % base`, and returns the empty string at zero; the K postcondition uses the
matching `baseDigits` recurrence.  Operationally, `call.k` lines 69–74 adds a
new scope at the fresh allocator location, `functions.k` lines 63–66 updates
it when binding arguments, and lines 85–90 deletes it when returning.
Recursion repeats that frame lifecycle.  The three domain lemmas are exactly
the allocator absence, update, and deletion facts needed for it.  I therefore
accept the protected Stage 3 classifications.

The detailed judgment and frozen operational excerpts are in
[`03-independent-classification.md`](evidence/03-independent-classification.md),
[`03-verification-source.log`](evidence/03-verification-source.log),
[`03-operational-call.log`](evidence/03-operational-call.log), and
[`03-operational-functions.log`](evidence/03-operational-functions.log).

## Deterministic Stage 4 structure

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` against
the three specified paths and the trusted toolchain lock.  It returned
`status: PASS`, built the generated project cleanly, found three obligations,
zero designated sorries, and 50 recorded generated trust declarations.  The
complete returned object is
[`04-preflight-rerun-success.log`](evidence/04-preflight-rerun-success.log).

Independent checks also establish:

- generated tree SHA-256
  `abc17ba024518dea8fc6aa8e9394a007440a5d2481d7ff0cb5a91c70af6b2d7f`
  matches the export result, generator manifest, and audit input;
- obligation-map SHA-256 is
  `061e3ff214f03f4287101075fc96a6ebe8f6f9629f4ecb901793f89310602cde`;
- the three ordered source rules and obligations form an exact bijection:
  `rule-437465…`, `rule-746c49…`, and `rule-82f2c7…`;
- every Lean conjunct hash recomputes correctly;
- the generated target definition is the exact conjunction recorded by the
  producer, with SHA-256
  `b43e9673d8693e5757a3d1fed845040b09093eff429efa616a1390a877ed13d5`;
  and
- its fixed application statement has SHA-256
  `2a804177099020b3bed3c9f65c86b600719e83289e894e73dd3791741e22e009`.

The selected Stage 4 status is `PASS`, not `KLEAN_NO_OBLIGATIONS`, and the
independent classification confirms a genuinely nonempty set of three domain
lemmas.

### Mathematical generation failure

Those mechanical facts do not make the generated obligations faithful.
Frozen `reference-semantics/semantics/core.k` line 37 declares the constructor
`scope(Map, Parent)`.  The initial configuration and call rules construct
values with it, so K's `Scope` is inhabited.  Generated `Sorts.lean` line 7,
however, is only:

```lean
inductive SortScope : Type
```

It has no constructors.  Yet generated target conjuncts 2 and 3 quantify
`V : SortScope`.  Both map obligations are consequently true by elimination
from an empty type, without reasoning about K map update or deletion.  The
warnings that `h` is unused in those generated conjuncts are consistent with,
though not needed for, this finding.

I compiled an adversarial Lean theorem against the exact fresh project.  It
proves that `SortScope` is empty and then proves the exact fixed
`targetStatement` while supplying constant definitions for all seven target
parameters.  This is a direct counterfactual demonstrating target vacuity,
not just a source inspection.  See
[`Adversarial.lean`](evidence/Adversarial.lean) and its successful compiler
result in
[`09-adversarial-vacuity-and-bridge.log`](evidence/09-adversarial-vacuity-and-bridge.log).

Stage 4 is therefore structurally deterministic but mathematically invalid:
it changes inhabited operational data into an empty sort and weakens two
required domain lemmas into vacuous propositions.

## Stage 5 clean rebuild, identity, and trust

I created `/tmp/audit-work/proof-audit.QWcnih`, copied the deterministic
generated project into it as `Base`, and copied only the candidate
source/configuration around it.  `Base` remained exactly the generated tree
after the checks, and fresh `Proof.lean` is byte-identical to the candidate:

- fresh `Base` tree:
  `abc17ba024518dea8fc6aa8e9394a007440a5d2481d7ff0cb5a91c70af6b2d7f`
- candidate and fresh `Proof.lean`:
  `4b306bbfc2ac01960b1f96dab6fac36d4e38e0df74f3921f1f9209553d606c23`

Both required commands succeeded:

- `lake clean`: exit 0
- `lake build`: exit 0, `Build completed successfully.`

Evidence is in
[`13-fresh-copy-integrity.log`](evidence/13-fresh-copy-integrity.log),
[`06-lake-clean.log`](evidence/06-lake-clean.log), and
[`07-lake-build.log`](evidence/07-lake-build.log).

The candidate does not declare, alter, or shadow `targetStatement`, and
contains no token-level `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`.  `Proof.final` has exactly the fixed generated application statement
and proves it directly; it is not a duplicate or textually weakened theorem.
The printed declaration and proof term are in
[`10-print-proof-final.log`](evidence/10-print-proof-final.log).

The exact `#print axioms Proof.final` output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`.  These three are fixed Lean foundational declarations,
not candidate or generated declarations.  None of the 50 allowlisted
generated trust-boundary declarations in `trust-inventory.json` appears in
the dependency list, so there is no unrecorded candidate/generated trust
escape.  Full reconciliation is in
[`15-axiom-accounting.md`](evidence/15-axiom-accounting.md) and the raw output
is [`08-print-axioms.log`](evidence/08-print-axioms.log).

## Operational bridge

The clean formal proof is not an honest proof of the frozen operational
lemmas.

The seven candidate definitions were printed exactly and compared to each
target binding, its `kore_symbol`, source-rule IDs, frozen rule, source
program, and operational semantics:

- `_Map_` is list append.  It only models K's AC, partial disjoint map union
  on a restricted well-formed/disjoint representation; generated `SortMap`
  permits overlapping ordered bindings, and the candidate accepts them.
- `_in_keys`, deletion, singleton, and update are plausible list
  implementations on unique-key well-formed maps, but the target states no
  representation invariant.
- `notBool_` is the correct Boolean negation.
- `freshScopes` is not the frozen definition.  It merely checks that every
  integer key is less than `next`, ignores values, and allows gaps.  Frozen K
  reduces `freshScopes` only from the empty equation or by removing the exact
  predecessor binding `(L:Int |-> _:Scope)` under
  `next = L + 1` and recursive `freshScopes(L,S)`.

The compiled adversarial file gives a direct bridge counterexample: the
candidate returns `true` for `next = 2` and a one-entry map from integer key
`0` to integer value `99`.  Frozen K's recurrence requires a `Scope` value and
an exact predecessor key, so this term does not implement that operational
meaning.  It also compiles a duplicate-key overlap example for `_Map_`.

The complete per-parameter assessment is
[`14-operational-bridge-audit.md`](evidence/14-operational-bridge-audit.md);
the exact printed candidate definitions are
[`11-print-parameter-definitions.log`](evidence/11-print-parameter-definitions.log).

## Conclusion

Stage 3 correctly identifies three relevant domain lemmas.  Stage 4 preserves
all recorded files, hashes, identities, and obligation ordering, but its
empty encoding of an inhabited K `Scope` makes two generated obligations
vacuous.  Stage 5 proves exactly that defective target with no candidate trust
escape, yet also supplies a `freshScopes` bridge that accepts states excluded
by the frozen recurrence.  A clean build and clean axiom list cannot establish
the required operational meaning.

The raw command record is
[`COMMANDS.md`](evidence/COMMANDS.md), and all cited inputs/results are under
`/audit-output/evidence/`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
