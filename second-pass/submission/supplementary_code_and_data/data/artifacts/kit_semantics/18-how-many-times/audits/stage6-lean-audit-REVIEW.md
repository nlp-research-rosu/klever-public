# Independent Stage 3–5 audit: `18-how-many-times`

## Result

The protected Stage 3 classification is complete and mathematically correct.
The deterministic Stage 4 generation contains exactly one obligation, which is
the exact nonempty-string slice lemma from the frozen K source. The Stage 5
candidate clean-builds, proves the fixed target without changing or shadowing
it, has no forbidden proof escape, and supplies operationally faithful
definitions for all six target parameters.

Audit mode was independently read as `CLASSIFICATION_AND_PROOF`; condition was
`kit-semantics` and semantics mode was `SUPPLIED_SEMANTICS`.

## Producer-source and immutable-input integrity

This check was performed before judging Stage 4.

- `/reference/generation-tools/klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `/reference/generation-tools/klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- Generator image:
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

The two file hashes agree with `source-manifest.json` and
`generator-manifest.json`. The image ID agrees between those manifests and the
immutable producer-source path recorded in `/audit-input.json`. The producer
bundle's launcher hash also recomputes exactly as
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
There is no producer-source infrastructure error.

The independent hash audit also recomputed:

- Stage 1 pipeline tree:
  `7fe0c5b51252e8cc3d20df8e1bb40004d1cffdbe3a46c7905166dd7246745072`
- Stage 1 export tree:
  `d110a88cd3d90500fc55be3305147e2a6f91c2313267aedc27dc6a9a9b00ac82`
- Stage 3 manifest:
  `0e34f604f34922750a6f7b420b8e70495d0d242ab1a82e3db2aabe6704f0f0d2`
- selected K audit:
  `ccccb076cfdc52337bbf9aaa5bd639f7a2d341a02095baecf5e0742f7ab1d0cd`
- Stage 4 generation tree:
  `b1bcce3d6661dcbc5acd7c0ad22415f28fb2a129b5bbb1cbc93fa8e1de87f04d`
- generated Lean tree:
  `050ecdd48f124daf73d66ef36857ad8b9d1d211d7535be452d2b80188aebbcf9`
- mounted Stage 5 candidate:
  `922a0669041cbeed73d0d2b68c4dcf93e998a3358a47c78d407cb0db61ced14f`

All 792 keys and values in `stage1_source_hashes` match the mounted Stage 1
tree. The recorded Stage 5 invocation directory itself is not a mounted audit
input, so its aggregate invocation hash is not independently rehashable; the
mounted successful workspace is rehashable and matches exactly. Full results
are in
[36_independent_hash_target_audit_success.txt](evidence/36_independent_hash_target_audit_success.txt).

## Inventory reconstruction and Stage 3 classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. Its local verification-module closure consists
only of `VERIFICATION`, because imported `MPY` is in the supplied required
semantics rather than another local module in `verification.k`.

Reconstructed values:

- `verification.k` SHA-256:
  `c97ba73673f656207939f9601f6cc58dde491a996532444cc082991bd753b529`
- inventory SHA-256:
  `197dc991c50e36d5ad237696d7faf9e483d8344bd1affc10da338a7be6a8093d`
- rule count: 6

| Span | Normalized hash / `source_rule_id` suffix | Independent class | Judgment |
|---|---|---|---|
| 11 | `993f1ddeb82f8ec3058462bbc0bc6a359326253665e58baa0229c8ff3387f51e` | `DEFINITION` | Empty constructor equation for the named proof helper `tailIS`. |
| 12 | `76f74f31823745350d94934f77a8b1740fb37bf6ce4be8986b32cd0e40ea55d6` | `DEFINITION` | Nonempty constructor equation completing `tailIS`. |
| 14–16 | `7d8832f9476a30d90c0dc5ff351d655f77be7e3f7d280223e5275d3f137e948f` | `DEFINITION` | Empty-pattern branch of the named `overlapCount` summary: every boundary counts. |
| 18–20 | `29f9efb6fc47c221fe5c4d6a8b72995b4966c7b257bd75c9928ce9d7ccbf0a9b` | `DEFINITION` | Empty-source/nonempty-pattern base case of that summary. |
| 22–27 | `48a4b84d7a4f49eddd82fbf489ed5db68e8505668dbff98cd6bb049cbb651062` | `DEFINITION` | Structural recurrence: test the current prefix and recur on the tail. |
| 31–38 | `5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536` | `DOMAIN_LEMMA` | Nonempty slice-to-tail theorem over supplied `buildIS`, `clampHi`, `isLen`, and `tailIS`. |

The five definitions name proof terms or a mathematical recurrence; they do
not replace source-program execution. Their guards are disjoint and exhaustive:
empty pattern; nonempty pattern with empty source; and both nonempty.
`overlapCount` matches the source: the empty substring returns
`len(string)+1`, while a nonempty substring is tested at every successive
nonempty suffix.

The final rule has `[simplification]`, and `DOMAIN_LEMMA` is its only legitimate
class. It is not an operational rule or definition. It was also not first
proved as an exact bridge-free Stage 1 theorem: an independent rerun against
the rule-free `lemma-kompiled` module exits 1 with
`WarnStuckClaimState`, as recorded in
[40_bridge_free_slice_lemma_rerun.txt](evidence/40_bridge_free_slice_lemma_rerun.txt).
It therefore cannot be `PROVED_DERIVED_LEMMA`.

The domain lemma is relevant and true. Source line 9 executes
`string = string[1:]`; supplied slice semantics lowers that operation to
`buildIS(S, clampHi(1,isLen(S),1), isLen(S), 1)`. For a nonempty sequence of
length one, start and stop are both one and `buildIS` is empty. For length at
least two, it emits indices `1` through `length-1`, exactly the constructor
tail. This is the fact needed to re-establish the loop invariant.

The reconstructed and protected inventories have the same six ordered
identities, with no omissions, extras, duplicates, reordered entries, or
unaccounted classifications. Every `source_rule_id` is exactly
`rule-<normalized_sha256>`. See
[05_reconstructed_rule_inventory.txt](evidence/05_reconstructed_rule_inventory.txt)
and
[09_stage3_bijection_and_input_hashes.txt](evidence/09_stage3_bijection_and_input_hashes.txt).

## Stage 4 generation and mathematical obligation

The independently classified domain set is nonempty and contains exactly the
slice-to-tail rule, so `KLEAN_NO_OBLIGATIONS` would have been invalid. The
selected export correctly has status `OK` and one obligation.

The source-rule and obligation lists are bijective:

- source rule:
  `rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536`
- source span: 31–38
- normalized hash:
  `5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536`
- Lean conjunct hash:
  `ac8018a6f1e1c44d0e5a363c9b5dc0728a523b01b69db75cf152b1722158e45a`
- obligation-map hash:
  `40a3ee2fc4dd54b21edb85871a4086d772e05533e123f0c40d9aab8859db580a`

The generated conjunct universally quantifies `S`, carries the exact translated
guard `notBool (S ==K .IntSeq) = true`, and states the exact equation

`buildIS(S, clampHi(1,isLen(S),1), isLen(S),1) = tailIS(S)`.

There is no changed target, extra conjunct, weakened result, duplicate, or
omitted domain rule. With the operational bindings used by the candidate, the
guard is satisfiable on every concrete nonempty sequence; it is not vacuous.

The generated target is unique:

- declaration: `Klean18HowManyTimes.Lemmas.targetStatement`
- definition hash:
  `8f82c1ed26e32aefac9063d68a1f5a68c6466c84501458b108c57490de617861`
- fully applied statement hash:
  `fd515c944fc8badacbe94ba1a26914992d09e00d420edd2d3b4615507d968608`

All six binding hashes recompute, their KORE symbols occur in the frozen
compiled definition, and the target object agrees among the generator
manifest, Stage 4 preflight record, and audit input. See
[23_generated_obligation_and_trust_sources.txt](evidence/23_generated_obligation_and_trust_sources.txt),
[36_independent_hash_target_audit_success.txt](evidence/36_independent_hash_target_audit_success.txt),
and
[42_kore_parameter_symbol_occurrences.txt](evidence/42_kore_parameter_symbol_occurrences.txt).

I reran the required function directly:

`PYTHONPATH=/reference python3 ...check_generation(...)`

The rerun returns `PASS`, one obligation, the fixed target above, zero
designated sorries, `lake clean` exit 0, and `lake build` exit 0. The complete
returned JSON is
[22_generation_preflight_success.txt](evidence/22_generation_preflight_success.txt).

### Lean toolchain namespace workaround

The first rerun exposed an audit-container defect, not a project failure:
Lean 4.22 calls `readlink("/proc/<getpid>/exe")`, but this container's process
PID was not present in its mounted `/proc`. This caused Lake's
“could not detect the configuration” error. I used a narrow `LD_PRELOAD` shim
that changes only `/proc/<digits>/exe` reads to `/proc/self/exe`. Its source and
hash are recorded in
[44_audit_runner_and_shim_sources.txt](evidence/44_audit_runner_and_shim_sources.txt)
and
[21_proc_shim_validation.txt](evidence/21_proc_shim_validation.txt).
With it, Lean reports version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the pinned toolchain.
The shim does not alter Lean source, project source, theorem statements,
elaboration, kernel checking, or axiom reporting.

## Stage 5 clean build, target identity, and trust

I created `/tmp/audit-work/proof-audit-001`, copied only the protected generated
project into `Base`, and copied the candidate's three top-level files around it.
The protected Base digest remained
`050ecdd48f124daf73d66ef36857ad8b9d1d211d7535be452d2b80188aebbcf9`.

The exact required commands were run in that fresh project:

1. `lake clean` — exit 0
2. `lake build` — exit 0; Base and `Proof` rebuilt successfully

Complete output is in
[26_candidate_clean_build.txt](evidence/26_candidate_clean_build.txt).
The trusted independent proof mechanical gate separately repeated the clean
build and passed; see
[37_proof_mechanical_gate.txt](evidence/37_proof_mechanical_gate.txt).

Candidate-source inspection found:

- exactly one `Proof.final`;
- its normalized type is exactly the manifest's fully applied fixed statement;
- exactly one candidate `def` for each of the six target parameters;
- no candidate definition of `targetStatement`;
- no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`;
- no modification or shadowing of the protected Base target.

`#print axioms Proof.final` produced exactly:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

The exact output is
[27_proof_final_axioms.txt](evidence/27_proof_final_axioms.txt).
`trust-inventory.json` records 44 generated trust declarations, but none is a
dependency of `Proof.final`. The trusted gate's foundational allowance consists
of exactly `propext`, `Classical.choice`, and `Quot.sound`; the observed set is
that set and nothing else. There is no `sorryAx` and no unrecorded proof trust
escape.

## Operational-bridge audit

The generated equation is parametric in six functions, so a clean proof alone
cannot establish their K meaning. Indeed, an audit-only counterfactual with
coordinated constant `buildIS` and `tailIS` also proves the bare equation. This
was used as an adversarial test, not accepted as evidence. The submitted
definitions were then checked independently:

| Parameter | Frozen operational meaning | Candidate definition and judgment |
|---|---|---|
| `«_==K_»` | Ground K syntactic equality | Structural equality on the generated `SortK` inductive value, returning `true` iff equal. Equal and unequal injected `IntSeq` witnesses distinguish it. PASS. |
| `buildIS` | Supplied rules at `subscript.k:116–121`: emit `intSeqAt(IS,i)` while the signed-stride guard holds, then recur at `i+step`; otherwise empty | Unit stride uses the extensionally equal `drop`/`take`; other strides follow the recurrence with source length as fuel. On every K-defined normalized-slice domain, all indices are in bounds and at most the source length are emitted. Its total fallback is only on domains where K's partial `intSeqAt` has no result, and the fixed target never enters those domains. Positive, negative, zero, length-one, and multi-element witnesses all agree. PASS. |
| `clampHi` | Return `i` when `i < len`; otherwise `len-1` for negative step and `len` for nonnegative step | Exact same guarded expression over Lean integers; boundary and negative-step witnesses agree. PASS. |
| `isLen` | Zero on `.IntSeq`; `1 + isLen(tail)` on `iCons` | Converts the same inductive sequence to a list and takes its integer length. Empty and multi-element witnesses, plus structural induction used in the proof, agree. PASS. |
| `notBool_` | Boolean negation | Lean Boolean negation; both truth-table rows checked. PASS. |
| `tailIS` | Empty maps to empty; `iCons(_,CS)` maps to `CS` | Exact constructor recursion from frozen `verification.k:11–12`; empty, singleton, and multi-element witnesses agree. PASS. |

The supplied K runtime independently reduced:

- `"abc"[1:]` to code sequence `[98,99]` (`"bc"`);
- `"abcd"[0::2]` to `[97,99]` (`"ac"`);
- `"abc"[::-1]` to `[99,98,97]` (`"cba"`).

See
[34_supplied_semantics_slice_ground_tests.txt](evidence/34_supplied_semantics_slice_ground_tests.txt).
The corresponding Lean boundary/adversarial checks, including the constant
counterfactual and proofs that the submitted functions differ from it, compile
successfully in
[29_operational_bridge_adversarial_tests_success.txt](evidence/29_operational_bridge_adversarial_tests_success.txt);
their full source is
[43_adversarial_test_sources.txt](evidence/43_adversarial_test_sources.txt).

Finally, on a concrete nonempty length-three witness satisfying the translated
guard, mutating the correct result from the tail back to the original sequence
is rejected by Lean with exit 1. This confirms non-vacuity under the actual
bindings; see
[38_false_equation_mutation_expected_failure.txt](evidence/38_false_equation_mutation_expected_failure.txt).

## Conclusion

Stage 3 correctly exposes the only unproved, relevant mathematical fact as a
`DOMAIN_LEMMA`. Stage 4 deterministically and bijectively generates its exact
Lean obligation and fixed target. Stage 5 proves that target with honest
operational bindings, a clean kernel dependency set, and no trust escape.

VERDICT: PASS
LEGITIMACY: LEGIT
