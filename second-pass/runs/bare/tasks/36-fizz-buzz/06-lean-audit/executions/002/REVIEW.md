# Independent review: HumanEval `36-fizz-buzz`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `bare`  
Semantics mode: `GENERATED_SEMANTICS`

## Conclusion

The protected Stage 3 classification is mathematically correct, the Stage 4
domain set and generated target are exact, and the Stage 5 candidate honestly
implements K integer addition and proves the fixed associativity theorem. The
classification/proof chain is legitimate.

I record `CONCERNS`, rather than an unqualified `PASS`, for a provenance
auditability limitation: the Stage 4 manifest's historical hashes for its
generator sources do not match the newer trusted checker sources mounted at
`/reference/tools`, and the historical source preimages are not mounted.
This does not affect the generated tree, target, proof, or operational-bridge
legitimacy; all of those independently pass.

## Audit execution and environment

All candidate and provenance text was treated only as evidence. I executed only
the requested trusted Python checks, the pinned K/Lean toolchains, and
audit-authored test files below `/tmp/audit-work`.

The sandbox exposes `/proc/self/exe` but not `/proc/<getpid()>/exe`: its shell
reported PID 2 while `/proc/2/exe` was absent. Lean 4.22 uses the latter lookup,
so the first preflight attempts failed before checking/building the project.
Evidence 36–40 isolates this environment issue. I compiled an audit-local
`LD_PRELOAD` shim that changes only decimal `/proc/<pid>/exe` `readlink` calls
to `/proc/self/exe`; with it, the pinned Lean binary reports the exact locked
version and all clean builds succeed. The shim source is
`evidence/proc_exe_compat.c`.

## Stage 3 inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` on the frozen `/reference/k-proof`. The local
verification-module closure is exactly `VERIFICATION`; its `SEMANTIC` import is
external to `verification.k`.

- Frozen `verification.k` SHA-256:
  `24034a2584fae5d039c164a46ecdba6763c893b5f9675d8b543d0c41897bae86`.
- Reconstructed inventory SHA-256:
  `736568ab7f1701fa76e06519c913488b7fd319b62eb88baa3958a177a3882787`.
- Protected Stage 3 file SHA-256:
  `73d00a9c43ca6be80e8c33b3a78b35c2f30b12231a3dd2f45b6973b1e7ed5020`.

For all 13 rules, the source slice exactly equals the reconstructed text; an
independent normalization and SHA-256 calculation equals both
`normalized_sha256` and the suffix of `source_rule_id`. The ordered ID list is
identical to the protected manifest, with no duplicate, omitted, extra, or
reordered entry. The whole-inventory canonical JSON hash also matches.
Complete spans, text, attributes, hashes, and comparison results are in
`evidence/04_reconstructed_inventory.json`.

## Independent rule classification

The frozen source, source program, specification, and operational semantics are
captured in evidence 05–06. My classifications are:

| Span | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 13–14 | `rule-e763c3f3ce388151393e428198722a36cf283185f5d31d700c07a4fea32b597b` | `DEFINITION` | Negative branch of the named `fizzEnd` summary. |
| 15–16 | `rule-1904e693aaf0033ea4c764af47f3256dcc77b731523dc22f4cfd10611f765237` | `DEFINITION` | Nonnegative branch of `fizzEnd`; together the guards are exhaustive and disjoint. |
| 18–19 | `rule-30079623688f5b570b38f8a2896ee5b74b79a4367acc2ab3e054817b7e0cb7a7` | `DEFINITION` | Base equation for the `digitSevens` recurrence. |
| 20–21 | `rule-729ad4a68b3299ff18b3488c12489276a4edfa8a890e236b5bcf981e6e3c6f89` | `DEFINITION` | Positive, last-digit-seven recurrence; division by 10 decreases the positive argument. |
| 22–23 | `rule-5d535d5211f655f272b25f28b219933239017014bc24e0eaa6e81b5985089d20` | `DEFINITION` | Complementary positive recurrence. |
| 25–26 | `rule-6f6d25b627a7de6753b30c8b1db33b14717b8740662705d84581dd0ddde88d72` | `DEFINITION` | First piece of `fizzContribution`, for divisibility by 11. |
| 27–28 | `rule-e81d3927655b90d37b43ae533110b18c623a05009b9e1e9a3e154a6f97ffeb44` | `DEFINITION` | Remaining divisible-by-13 piece after excluding divisibility by 11. |
| 29–30 | `rule-ebf295199abbea4dc9a90303c80ad6f55809586ff7eeb17f56389907d94e7c15` | `DEFINITION` | Complementary zero-contribution piece. |
| 32–33 | `rule-dde8b8487c0ea1e1e4fe6cb86253708342138e3bf3d5d148b5fe526cf90da8fe` | `DEFINITION` | Empty-interval base equation for `fizzFrom`. |
| 34–35 | `rule-7ba888d5c7f8ca80108339cec76a10640fa99b1108c9249858ebad2a85ebb7ef` | `DEFINITION` | Advancing interval recurrence for `fizzFrom`. |
| 38 | `rule-115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7` | `DOMAIN_LEMMA` | Integer-addition associativity. It is true over K `Int`, is not a definition, and is compiled before every claim rather than first proved without itself. |
| 43–48 | `rule-948f699a84e5f8aba9d6d2c7879d7807ab825a002416eb1275a55c26ada875ab` | `DEFINITION` | Macro definition of the exact translated inner-loop AST. |
| 51–59 | `rule-55f4df2bb36ada94a0fbce4dfb208de6119596fecc5a3da9f9260be5f4f2b937` | `DEFINITION` | Macro definition of the exact translated outer-loop AST. |

None is an `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA`. The macro rules expand
syntax and then leave execution to the frozen small-step rules; they do not
preempt program execution. The summary functions do not match operational AST
constructors.

The only `[simplification]` entry is integer associativity and is correctly a
`DOMAIN_LEMMA`. It is relevant, not decorative: the source updates `count` and
`i` by addition, while the inner/outer invariants and `fizzFrom` contain
symbolic accumulated sums whose association must be normalized. The protected
classification agrees entry-for-entry. A fuller semantic explanation is in
`evidence/07_independent_classification.md`.

## Stage 4 deterministic generation

The required direct call to `tools.klean_preflight.check_generation` returned
`PASS`, one obligation, zero designated sorries, 50 recorded trust
declarations, and the fixed target. Its returned evidence is
`evidence/41_check_generation_returned_evidence.txt`. The trusted final gate
independently reran the same preflight successfully in evidence 65.

All hashes with mounted preimages match:

- Stage 1 pipeline tree:
  `21ed0d0c7c006fb5f568f4efcc73e8db7a5bfbd68b03086d798c6c88f80f5f44`.
- Stage 1 deterministic-export tree:
  `b991023a78aa688227026b58ef3bbd7b5a46ae68901df9dec6d114506499e99d`.
- Stage 2 audit tree:
  `e43167e6b0259bde0888b0f1587634089cce5d6bb6dbf865844e1b0f2989ea11`.
- Stage 3 manifest:
  `73d00a9c43ca6be80e8c33b3a78b35c2f30b12231a3dd2f45b6973b1e7ed5020`.
- Whole Stage 4 generation tree:
  `07e986bbf490737cdac4f123108ac1abf112fa56fd8401fee557692cd4335095`.
- Generated project tree:
  `7796a58da3724bfe844e4ccc3ad5df12b23c95f7db60fbda59688db408db6904`.
- Stage 5 candidate tree:
  `e9ae0217f1381aadfe979c8f7d947bf327a8272b9de358cf5d3d384d0092a221`.

Every individual Stage 1 source hash also matches the launcher record.
`audit-input.json`'s canonical resolution digest recomputes to
`4994c603954d41b3ad4acdb27bc5ab331624254f9301b46891d42b028ecd673f`.
The obligation-map and trust-inventory file hashes match their sidecars.
See `evidence/47_stage4_independent_checks.json`.

The independently determined domain set has exactly one rule, and the
obligation map has exactly one unique entry with that same ID, span,
normalized hash, inventory hash, and discovery hash. Its nonvacuous conjunct is
exactly:

`∀ (A : SortInt) (B : SortInt) (C : SortInt), «_+Int_» («_+Int_» A B) C = «_+Int_» A («_+Int_» B C)`

No source rule is omitted or duplicated, and there is no weakened guard or
vacuous conjunct.

The generated target occurs once, only in
`Klean36FizzBuzz/Lemmas.lean`:

- declaration: `Klean36FizzBuzz.Lemmas.targetStatement`;
- statement:
  `Klean36FizzBuzz.Lemmas.targetStatement «_+Int_»`;
- definition SHA-256:
  `f5de4b2237c7af5067d9f684fd0ceeb08bc2caf891532eba3722805ed96c620e`;
- statement SHA-256:
  `83aeddd5dbd588726a15128801c81b7cd2d02c4ecef9f957e43beb4742104de6`;
- parameter-binding SHA-256:
  `c33da7c1697bfe5cd56f5a1028b13979a3aea7a57e3473723b2916b6004903a8`.

The parsed target equals the obligation-derived expected definition, generator
manifest, Stage 4 preflight, and audit input exactly.

## Stage 5 clean proof and identity

The corrected fresh workspace is
`/tmp/audit-work/36-fizz-buzz-proof-audit.mGE0Os`. The generated project was
copied directly into `Base`; after the build its deterministic tree digest is
still exactly the reference generated-tree hash.

Both required commands succeeded:

- `lake clean`: exit 0; complete output in
  `evidence/53_lake_clean_complete.txt`.
- `lake build`: exit 0; complete output in
  `evidence/54_lake_build_complete.txt`.

The trusted final gate independently made another clean copy and repeated the
clean, build, target type check, and axiom query, returning `PASS`
(`evidence/65_trusted_final_gate_returned_evidence.txt`).

The candidate defines the target parameter exactly once:

`def «_+Int_» (x0 x1 : SortInt) : SortInt := x0 + x1`

It contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.
It contains no `targetStatement` definition and does not enter the generated
target namespace, so it neither changes nor shadows the target. `Proof.final`
states the exact manifest statement once, not a duplicate or weakened theorem.
Compiled declaration printing confirms:

`theorem Proof.final : Klean36FizzBuzz.Lemmas.targetStatement Proof.«_+Int_»`

Candidate and target structural checks are in
`evidence/68_candidate_independent_checks.json`.

### Axiom accounting

The exact requested output is:

`'Proof.final' depends on axioms: [propext]`

(`evidence/55_print_axioms_proof_final_exact.txt`).

`targetStatement` and `Proof.«_+Int_»` themselves have no axiom dependencies;
`propext` comes from Lean core's `Int.add_assoc`. It is one of the trusted
final gate's fixed foundational allowlist `{Classical.choice, propext,
Quot.sound}`. No generated trust-inventory entry is used by `Proof.final`,
there is no `sorryAx`, and there is no unexpected or candidate-added trust
escape. Evidence 56–59 and 68 reconcile this with the 50 generated declarations
in `trust-inventory.json`.

## Operational bridge

The parameter binds:

- KORE symbol `Lbl'UndsPlus'Int'Unds'`;
- source rule
  `rule-115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7`;
- Lean type `SortInt → SortInt → SortInt`.

This bridge is exact:

1. Frozen `semantic.k` evaluates
   `Int(B) ~> binRight("+", A)` to `Int(A +Int B)`.
2. The domain lemma is associativity of that same `+Int`.
3. `SortInt` is definitionally Lean `Int`.
4. The deterministic generated integer hook is
   `some (x0 + x1)`.
5. The candidate removes only the hook's `Option` wrapper required by the
   target parameter and uses the same unbounded integer operation.
6. The source program uses addition for both `count := count + 1` and
   `i := i + 1`, so the binding is operationally relevant.

Adversarial Lean evaluations produced `-5`, `-5`, `-21`, `47`, `-47`, and
`1` for mixed-sign, zero, and large-cancellation cases. Independent execution
of those same expressions through a fresh compilation of the frozen K
small-step semantics produced exactly the same six results
(`evidence/61_operational_bridge_adversarial_and_mutation_tests_final.txt` and
`evidence/64_k_addition_oracle_results.txt`).

Counterfactual tests show that the equation alone would not establish the
bridge: constant-zero, left-projection, and right-projection definitions all
prove associativity but fail `2 + 3 = 5`. A subtraction mutation fails the
fixed target on the witness `(10,3,2)`. The candidate is none of these
convenient operations; its definition and ground behavior agree with the
frozen operational meaning over negative, positive, zero, and arbitrary-size
integers.

## Provenance concern

The generator manifest records historical source hashes
`235473b1...` for `klean_export.py` and `ddec66db...` for `klean.py`.
The current trusted audit copies hash to `0c18ea79...` and `92e9515a...`
respectively (evidence 47–48 and 69). These fields describe the generator
sources present at generation time; the corresponding historical files are
not mounted, so their preimages cannot be independently checked or used for a
byte-for-byte regeneration. Likewise, the recorded Stage 5 invocation-tree
hash has no mounted invocation-tree preimage.

This is an auditability concern, not evidence of an illegitimate theorem:
every mounted source/tree/sidecar hash verifies, the current hardened trusted
preflight and final gate both pass, the exact target is independently
reconstructed from the source rule, and the candidate's operational bridge is
validated against frozen K execution.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
