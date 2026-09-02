# Independent Stage 3–5 audit: HumanEval `84-solve`

## Outcome

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the mounted candidate, prior audit, manifests, logs, comments, and provenance
content only as untrusted evidence. Canonical reconstruction and mechanical
checks used the trusted code under `/reference/tools`; no instruction found in
a mounted candidate or provenance artifact was executed.

The protected Stage 3 classification is correct: the frozen local
verification-module closure contains four definitions and one relevant domain
lemma. Deterministic Stage 4 maps that one domain lemma bijectively to one
non-vacuous fixed Lean target. The Stage 5 candidate cleanly proves that exact
target using the supplied operational slice semantics, without a candidate
trust escape or convenient bridge definition.

## Launcher and immutable input integrity

`/audit-input.json` verifies under the trusted schema-v4 resolution contract.
Its canonical signed-resolution digest is
`8844b2037bf95bbc334d78c1813e7df387f8a3bdc7f7202e82f4337fe2917e7d`.
The launcher records `CLASSIFICATION_AND_PROOF` and `SUPPLIED_SEMANTICS`.

Independent rehashing matched every relevant launcher binding:

- Stage 1 pipeline tree:
  `1c71249fbffd360f8d77e2c71b9b14540d975c5a5b3ebafa3968d62aba1fe307`;
- Stage 1 export tree:
  `a17383f6f67c3d71d84073a032d3670761c67443f5b6ab53847a3786b881b71c`;
- all 35 Stage 1 per-file source hashes;
- Stage 3 manifest:
  `a9e9c33767567d26d9e9f20a4935184028f6159ba02f28f5da3e8df620d2595b`;
- selected Stage 4 tree:
  `968573f73614a21c230ddbae9bac897a40b2ef00461aff4b70063e5cb4369188`;
- generated project tree:
  `48908fb1d2779de308fccb91567223eb57777f9b3813123e80e6db7b0d4b43f9`;
- Stage 5 candidate tree:
  `07eed6dade86c8ecd0fa13361e0029ac74ebc142d2b9912a1f741808714c67b7`.

Complete comparisons are reproducible with
`evidence/independent_integrity_checks.py`; their recorded result is
`evidence/independent-integrity-checks.log`.

## Generation-time producer provenance

I performed this gate before accepting any Stage 4 result.

The mounted producer hashes are:

- `klean_export.py`:
  `00eca7a19eb09cb503b02179f8dd583118a2f3e6130c61329b230d150a815c20`;
- `klean.py`:
  `1ba065b19feb2fb0a48abe80bc2cf0d0afd3d72289374303745e0d5a59f0bccc`.

They equal both `generator-manifest.json` and
`source-manifest.json`. The source bundle contains exactly those files plus
the source manifest, and its trusted pipeline tree hash is
`efba7887c1020e119b6c93176265647e8780c78288e95f18f3d3fbd4b65e6c88`,
equal to `/audit-input.json`.

The generator and source manifests both bind image
`sha256:daef1addbf4dd6acd04545f645a7cca4e4fa769af620b10672a5d42a0d0a6984`.
The launcher's producer-source path is keyed by the same digest. There is no
producer-source infrastructure error. Raw results are in
`evidence/producer-provenance.log`.

## Canonical inventory reconstruction

Running trusted `tools.k_rule_inventory.inventory_verification` on the frozen
workspace selected module `VERIFICATION`. Its local closure within
`verification.k` is exactly `["VERIFICATION"]`. The source file hash is
`6ca4531eafb4913c7e80c9464cfe4ac7404c43ff02dde74a87f06b13b52ad4e1`.

The reconstruction produced these five rules, in source order:

| Span | `source_rule_id` suffix | Attributes | Independent class |
|---:|---|---|---|
| 9 | `a2a0…f1ff` | none | `DEFINITION` |
| 10–12 | `23f8…d85` | none | `DEFINITION` |
| 16–22 | `979a…87b` | none | `DEFINITION` |
| 26 | `0ff7…61e` | none | `DEFINITION` |
| 31–38 | `a850…370` | `priority(40)` | `DOMAIN_LEMMA` |

For every entry I recomputed the physical source span, whitespace-normalized
source, normalized SHA-256, and `rule-<normalized_sha256>` identity. The
canonical whole-inventory hash is
`7233706d0dbd7e2e45da849c5e062cddaa080936fac4c6aafcc0fe447030d1c2`.

The Stage 3 manifest contains the same five IDs once each in that exact order
and binds the same inventory hash. There are no missing, duplicate, extra, or
reordered identities and no changed or unaccounted source hashes. Exact rule
texts and spans are in `evidence/rule-inventory.json`; the invocation is in
`evidence/rule-inventory-command.log`.

## Independent classification judgment

The four definition classifications are mathematically and operationally
appropriate:

1. `decimalDigit(N,1) => pyMod(N,10)` is the base equation of a newly named
   summary.
2. The guarded higher-place `decimalDigit` equation defines the same summary
   for `N≥0`, `P>1`. Every source use has
   `P ∈ {10,100,1000,10000}` and is inside the guard.
3. `decimalDigitSum` defines the exact five terms in the source expression.
   These places cover the full `0..10000` domain, including the fifth digit of
   `10000`.
4. `binaryNumeral(N) => str(binCodes(N))` names the prefix-free binary proof
   term used in the postcondition.

These rules name summaries or proof terms; they do not replace execution of
the frozen source body. None is a disguised domain lemma.

The rule at lines 31–38 is correctly a `DOMAIN_LEMMA`. It rewrites
`str(iCons(48,iCons(98,REST)))[2:]` to `str(REST)` under an arbitrary
continuation. It is not an ordinary supplied-semantics rule, and Stage 1 does
not first prove the exact statement in a module omitting it, so it is neither
`OPERATIONAL_RULE` nor `PROVED_DERIVED_LEMMA`.

It is directly relevant: the frozen source returns `bin(digit_sum)[2:]`, and
the supplied `bin` rule emits exactly the `48,98` (`"0b"`) prefix for the
nonnegative digit sum. The supplied slice semantics evaluates the lower bound
to `2`, upper bound to sequence length, step to `1`, then `buildIS` returns
exactly `REST`. It preserves the continuation and every other cell.

There are no independently identified operational or proved-derived entries.
No inventory rule has a `simplification` attribute, so the required
simplification-class restriction is satisfied. The detailed semantic
assessment is in `evidence/classification-and-bridge.md`.

As finite adequacy evidence, an independent implementation compared the
frozen source formula with separate decimal-sum and binary-conversion oracles
for every integer `0..10000`: 10,001 cases, zero mismatches. Omitting the
`10000` place fails at `10000`; slicing from `1` fails at `147`. See
`evidence/semantic_crosscheck.py` and
`evidence/semantic-crosscheck.log`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`;
- `/reference/klean-toolchain.lock.json`.

The sandbox initially prevented Lean's `IO.appPath`: `getpid()` returned the
inner namespace PID while `/proc` exposed outer PIDs. An audit-only
`LD_PRELOAD` shim returned the outer `Pid:` from `/proc/self/status`. This
changed no mounted input, generated source, target, or proof. The shim source
is in `evidence/lean-procfs-shim.c`.

With the pinned environment, trusted preflight returned `PASS`, including
fresh `lake clean` and `lake build` exit codes 0. Its build-output hash is
`ced553ad034c46a7e7c15ff0d1d95d357e41c9b1a5d40de43ec2f7bad12ee5f0`,
identical to the launcher-recorded preflight. The complete returned document
is `evidence/stage4-preflight.json`, and the command/environment record is
`evidence/stage4-preflight-command.log`.

Independent obligation checks established:

- independently true domain set: exactly
  `rule-a85038e1ac209993c7ddd60086463b961c8ffbd45be861486d9c8442d108f370`;
- `input-manifest.source_rules`: that exact singleton;
- `obligation-map.source_rules`: that exact singleton;
- `obligation-map.obligations`: one obligation with that exact ID;
- no duplicate obligation;
- exact source span 31–38 and matching normalized, inventory, and discovery
  hashes;
- obligation-map hash:
  `72569257a9999ebc796cf15b436efda5913d8853e772e9e89c34c570bee3891d`;
- Lean conjunct hash:
  `6c2fd06bdcdebaa89b1ea0ac81a96594987d9816b471eaaefaaa8d3cd362ca25`.

The target is the exact singleton conjunction of that obligation. It
quantifies over every `REST`, arbitrary continuation, and all unchanged
configuration cells. Its LHS and RHS differ, and `Rewrites` has no reflexivity
constructor, so the conjunct is not vacuous. There is no omitted or irrelevant
obligation and no weakened guard or changed target.

The fixed target is:

- declaration/statement:
  `Klean84Solve.Lemmas.targetStatement`;
- file: `Klean84Solve/Lemmas.lean`;
- statement hash:
  `80e21567076746be308970e9622b209b7a444ced513c1c05a7cd32cdfd215499`;
- exact definition hash:
  `d68a1ad5ba959890ad91a366b6293e3fa5c291aa574e3fc115e4720e48b6ed29`;
- parameters: `[]`.

These values equal the generated source, generator manifest, preflight,
obligation map, and `/audit-input.json`. The true domain set is nonempty, so
`KLEAN_NO_OBLIGATIONS` does not apply.

## Stage 5 clean build and static trust checks

I copied the candidate to `/tmp/audit-work/stage5` and copied the immutable
generated project into it as `Base`. Before building, the fresh `Base` tree
hash equaled the generated tree hash above. Candidate proof-file hashes also
equaled the mounted originals.

I then ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, `Build completed successfully`.

The clean removed the prior build directory before compilation, so the proof
and generated Base were rebuilt. The full output, including all generated
linter warnings, is in `evidence/stage5-clean-build.log`.

After the build:

- `Base` still had tree hash
  `48908fb1d2779de308fccb91567223eb57777f9b3813123e80e6db7b0d4b43f9`;
- the target statement and both target hashes were unchanged;
- the candidate contained no `sorry`, `admit`, `unsafe`, new `axiom`, or new
  `opaque`;
- the candidate declared no `targetStatement` and did not enter namespace
  `Klean84Solve`, so it neither changes nor shadows the target.

See `evidence/stage5-identity-and-static-scan.log`.

## Proof identity and operational meaning

Lean reported twice, including an explicit type ascription:

`Proof.final : Klean84Solve.Lemmas.targetStatement`

Thus `Proof.final` proves the immutable target itself, not a duplicated,
weakened, or alternate theorem.

The proof does not use the Stage 3 domain rule as a `Rewrites` constructor.
The generated relation does not contain that constructor. Instead it composes
the ordinary supplied-semantics steps for slice-bound evaluation and then
proves the exact `doSlice` value.

The value proof matches the frozen operational rules:

- the generated length and indexing models mirror `isLen` and `intSeqAt`;
- the continuation guard mirrors the positive/negative `buildIS` guard;
- the recursive model consumes one in-bounds element per unit step;
- `slStart`, `slStop`, and `slStep` specialize to `2`, sequence length, and
  `1`;
- structural induction establishes the result for every finite `REST`.

The proof preserves the arbitrary active continuation and all ten other
configuration cells quantified by the target. It introduces no return,
exception, frame change, heap update, output, or other hidden state effect.

`target.parameters` is empty. Therefore the requested
parameter-name/`kore_symbol`/`source_rule_ids`/candidate-`def` loop has no
entries; there is no candidate-supplied constant, identity, hard-coded, or
vacuous operational bridge to accept. The helper `append` is a normal
structurally recursive proof definition, not a target parameter or semantics
replacement.

Adversarial checks reinforce the universal proof:

- an unusual tail `[-7,100000]` typechecks under the theorem;
- a hard-coded empty result is rejected with exit 1 and an exact type
  mismatch against `str(REST)`;
- mutating the slice start from `2` to `1` is rejected with exit 1.

Artifacts and exact outputs are in `evidence/adversarial.lean`,
`evidence/counterfactual-hardcoded.lean`,
`evidence/counterfactual-start.lean`, and
`evidence/stage5-adversarial.log`.

## Axiom accounting

Running Lean with `#print axioms Proof.final` produced 34 dependencies. The
exact output is in `evidence/stage5-axioms.log`.

- 31 are generated, non-propositional value/function constants.
- Every one of those 31 appears by exact name in
  `trust-inventory.json`'s allowlist.
- The remaining three are Lean's standard kernel/library foundations:
  `propext`, `Classical.choice`, and `Quot.sound`; they are not
  candidate-added declarations.
- `sorryAx` is absent.
- There is no unrecorded generated proof trust escape.
- The inventory records zero designated and zero other sorries.
- Trusted preflight independently rejected proposition-valued generated
  axioms/opaque declarations.

The exact reconciliation and executable checker are
`evidence/axiom-reconciliation.log` and
`evidence/reconcile_axioms.py`.

## Final judgment

Stage 3 is complete and correctly classified. Stage 4 has verified producer
provenance, exact deterministic structural integrity, a bijective singleton
domain obligation, and the fixed intended target. Stage 5 cleanly proves that
exact target with a source-faithful operational connection and accounted trust
boundary. I found no legitimacy defect or residual concern.

VERDICT: PASS
LEGITIMACY: LEGIT
