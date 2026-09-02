# Independent audit: HumanEval `63-fibfib`

## Result

The Stage 3 classification is complete and mathematically appropriate, the
Stage 4 generation is bound bijectively to the one genuine domain lemma, and
the Stage 5 candidate proves the immutable generated target with honest
implementations of both operational parameters. I did not rely on the earlier
Stage 2 verdict, Stage 3 rationale, generator logs, or Stage 5 success record
as authority.

The launcher and environment both report
`AUDIT_MODE=CLASSIFICATION_AND_PROOF`, condition `semantics`, and semantics
mode `SUPPLIED_SEMANTICS`.

## Producer and mounted-input integrity

I hashed the generation-time producer sources before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

These hashes agree exactly with `generator-manifest.json` and
`source-manifest.json`. The producer bundle contains exactly those two sources
and `source-manifest.json`; its recomputed tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`. The generator image ID is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest, source manifest, and audit-input producer-bundle
path.

All launcher hashes for mounted artifacts recompute exactly: the Stage 1
pipeline tree and export tree, every Stage 1 source-file hash, the protected
Stage 3 manifest, the selected Stage 2 audit tree, the Stage 4 generation tree,
the generated project tree, and the candidate tree. The exact values and
comparisons are in
[02_integrity_inventory.json](/audit-output/evidence/02_integrity_inventory.json).

## Inventory reconstruction and Stage 3 judgment

I ran the trusted local rule-inventory implementation afresh on the frozen
`verification.k`. Its local verification-module closure is exactly
`FIBFIB-VERIFICATION`, containing these three rules in source order:

| Span | Recomputed `source_rule_id` | Attributes | Independent class |
|---|---|---|---|
| 9–10 | `rule-b44371020fcd21e0007e7bee08ec628a112e7fcc8a28189045b1aa649eaab409` | none | `DEFINITION` |
| 11–13 | `rule-b6e2aed5571df740aad1436d238bffe16db53ff99d0f83547591a7173792f4c5` | none | `DEFINITION` |
| 17 | `rule-0680c25a908725567264bc3a1d17a1d702f13c46cc6da2b783839bbc14a5d477` | `simplification` | `DOMAIN_LEMMA` |

For every entry, I independently sliced the recorded source lines, normalized
whitespace, recomputed the normalized SHA-256 and `source_rule_id`, and then
recomputed the canonical whole-inventory hash:
`bbae6e2da8cdba3f911c23bae055842f362d768cc31f3bd1bb87c8e2c89cf1be`.
The protected Stage 3 file has exactly the same three identities in the same
order, with no duplicate, omission, extra entry, changed span, or changed
hash.

The classifications are substantively correct:

1. Lines 9–10 are the base equation of the named mathematical summary
   `fibFrom(A,B,C,N)`: for `N <= 0`, zero further tuple shifts return the first
   component `A`.
2. Lines 11–13 are its positive recurrence: one tuple shift maps
   `(A,B,C)` to `(B,C,A+B+C)` and decrements `N`. The two guards are disjoint,
   cover all mathematical integers, and positive recursion decreases.
   Neither rule replaces program execution; together they define the summary.
3. Line 17 is the unconditional integer identity
   `N - (I + 1) = (N - I) + (-1)`. It neither introduces a summary nor
   performs ordinary execution. It was compiled into the verification module
   before the claims; there is no earlier claim proving this exact rule in a
   module that omits it. It is therefore a `DOMAIN_LEMMA`, not a definition,
   operational rule, or proved-derived lemma.

The domain lemma is relevant. The source loop increments `i` by one, while
the loop claim summarizes the remaining iterations as `fibFrom(..., N - I)`;
the recurrence decreases that remaining count by one. Line 17 is exactly the
normalization connecting `N - (I + 1)` to that recurrence. It is also globally
true under the pinned K hooks `INT.add` and `INT.sub`. The only
`simplification` rule is thus correctly classified as a `DOMAIN_LEMMA`.

The frozen source, claims, supplied integer dispatch, and pinned K hook lines
are recorded in
[03_classification_sources.log](/audit-output/evidence/03_classification_sources.log).

## Stage 4 generation and target identity

I reran the required call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three specified mounted inputs. The launcher exposes a PID namespace whose
reported PID is absent from the mounted `/proc`; Lean 4.22 consequently could
not resolve `/proc/<pid>/exe`. I used the narrowly scoped audit-local shim in
[toolchain_path_shim.c](/audit-output/evidence/toolchain_path_shim.c), which
redirects only that lookup to the equivalent `/proc/self/exe`. It does not
alter sources, elaboration, compilation, or proof checking. With that
environment repair, the exact preflight returns `PASS`; its internal
`lake clean` and `lake build` both exit 0. The original environmental failure
and successful rerun are both preserved.

The independently classified domain set has exactly one member, so this is
correctly a normal `PASS` generation, not `KLEAN_NO_OBLIGATIONS`.

The source-rule list and obligation list are both the singleton line-17 rule,
in the same order. Their source span, normalized hash, inventory hash,
discovery-manifest hash, and obligation hash all match. The exact generated
conjunct is:

```lean
∀ (I : SortInt) (N : SortInt),
  («_-Int_» N («_+Int_» I 1) : SortInt) =
  («_+Int_» («_-Int_» N I) (-1) : SortInt)
```

This is a faithful translation of the unconditional K rule. It retains both
variables on both sides, has syntactically distinct sides, contains no
`True`/`False` or unused conjunct, and has no omitted guard because the K rule
has none. Its SHA-256 is
`d8e642e092e8427f2e5b4e755d433c60ddadc0c3bd252e417a0e1efef3a3f0ca`.

There is exactly one generated `targetStatement`; it is exactly the conjunction
above. Its definition hash is
`82d34fdb5c32b5659618adadca9f1336b206d4644fadf6af0c7dbda890b2fe8c`,
and the fixed applied-statement hash is
`65cfc3a7124782feb5e82d5839771f9df9e70d0ffcb01f4519c07f6b5d5382a0`.
The declaration, file, statement, parameters, binding hashes, and both target
hashes agree exactly among the generated source, obligation map, generator
manifest, fresh preflight, and `/audit-input.json`.

The complete fresh preflight result is
[04_preflight.json](/audit-output/evidence/04_preflight.json), and the
independent bijection/target reconstruction is
[05_stage4_bijection.json](/audit-output/evidence/05_stage4_bijection.json).

## Stage 5 clean build, proof identity, and trust

I created a fresh project at
`/tmp/audit-work/63-fibfib-stage5-audit-2`, copied the candidate into it, and
populated its existing empty `Base/` directory with the immutable generated
project. I then ran both required commands:

```text
LD_PRELOAD=/tmp/audit-work/toolchain_path_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/toolchain_path_shim.so lake build
```

Both exit 0; the clean rebuild compiles `Proof`. The generated
`Lemmas.lean` source hash is
`5b8ebc5bf988a67de2a4a975ae18091adb59b672a1522407f790898b82f40185`
before and after the build and matches the mounted generated source. An
earlier staging attempt nested the generated directory under the candidate's
already-present empty `Base/` and failed at configuration discovery before any
source was built; that failed attempt is retained as
`06a_failed_copy_layout.*` and is not the successful fresh build.

The successful complete log is
[06_fresh_stage5_build.log](/audit-output/evidence/06_fresh_stage5_build.log).
The trusted Stage 5 mechanical gate was also rerun independently and returns
`PASS` in
[10_mechanical_final_gate.json](/audit-output/evidence/10_mechanical_final_gate.json).

Outside immutable `Base`, the candidate has exactly one definition for each
target parameter and exactly one theorem `Proof.final`. It contains no
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque`, and does not declare or
shadow `targetStatement`. Its theorem statement is textually the exact fixed
application:

```lean
Klean63Fibfib.Lemmas.targetStatement «_-Int_» «_+Int_»
```

Lean prints the elaborated theorem at exactly that type. The required axiom
query reports:

```text
'Proof.final' depends on axioms: [propext]
```

`sorryAx` is absent. `propext` is one of the standard Lean foundational axioms
explicitly allowed by the trusted final-gate policy alongside
`Classical.choice` and `Quot.sound`; it is not a candidate-added or
Klean-generated trust declaration. None of the 49 declarations in
`trust-inventory.json` occurs in the dependency set. Thus every dependency is
accounted for: one standard foundational axiom, zero generated allowlist
axioms, and zero unrecorded proof escapes. The exact Lean output is
[07_axioms.log](/audit-output/evidence/07_axioms.log).

## Operational-bridge audit

The two target parameters bind the only domain rule as follows:

| KORE symbol | Frozen K meaning | Candidate definition |
|---|---|---|
| `Lbl'Unds'-Int'Unds'` | total integer hook `INT.sub` | `def «_-Int_» := Int.sub` |
| `Lbl'UndsPlus'Int'Unds'` | total integer hook `INT.add` | `def «_+Int_» := Int.add` |

`SortInt` is Lean `Int`, so these definitions implement the mathematical,
unbounded integer meanings used by the supplied semantics. Addition is the
operational result of source `+` on integers and implements both `d = a+b+c`
and `i = i+1`; subtraction implements the summary-distance expressions in the
loop claim and the bound domain rule. The candidate definitions are total,
argument-sensitive, and neither constant, identity, hard-coded, nor vacuous.

I compiled adversarial ground cases covering positive, negative, mixed-sign,
and large integers. Lean evaluated the candidate operations to:

```text
(4, -10, 10, -4, 100000000000000000003)
```

for `7-3`, `-7-3`, `7-(-3)`, `-7+3`, and
`100000000000000000000+3`, respectively.

I also compiled counterfactual mutations. Constant-zero subtraction/addition
and first-projection subtraction/addition both prove the generated equation,
yet evaluate to `(0, 7, 7)` where the real operations give `(4, 10)` on the
chosen witnesses. This confirms that the equation alone does not force the
operational bridge and that the separate definition audit is material. The
actual candidate uses the exact K meanings and passes that stronger check.
Commands and results are in
[08_bridge_adversarial.log](/audit-output/evidence/08_bridge_adversarial.log)
and
[09_stage5_identity.json](/audit-output/evidence/09_stage5_identity.json).

## Evidence summary

All raw audit scripts, commands, outputs, reconstructed JSON, build logs, and
the preserved environment diagnostic are under
[evidence/](/audit-output/evidence/). The mechanical checks establish the
recorded structural facts; the independent semantic judgment above establishes
that the only exported obligation is the relevant, true line-17 domain lemma
and that the Stage 5 parameter definitions implement the frozen operational
meaning.

VERDICT: PASS
LEGITIMACY: LEGIT
