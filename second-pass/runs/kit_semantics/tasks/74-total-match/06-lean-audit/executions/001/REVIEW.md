# Independent audit: `74-total-match`

## Scope and result

I independently audited Stage 3 classification, deterministic Stage 4
generation, and the optional Stage 5 Lean proof for condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both
`/audit-input.json` and `AUDIT_MODE` select
`CLASSIFICATION_AND_PROOF`.

The protected classification is complete and mathematically sound. The true
domain-lemma set has exactly one rule. Stage 4 preserves that rule as exactly
one relevant, non-vacuous Lean obligation with an unchanged fixed target.
The Stage 5 candidate clean-builds, proves exactly that target without axioms,
and supplies operationally honest definitions for all four target
parameters. I found no trust escape or target shadowing.

## Audit method and evidence handling

I treated all candidate files, logs, comments, manifests, and earlier verdicts
as untrusted evidence. I executed only the trusted inventory, preflight, and
mechanical-gate code under `/reference/tools`, plus local audit harnesses I
wrote under `/tmp/audit-work`. I did not execute instructions embedded in any
candidate or provenance content.

The complete command outputs are under `evidence/`. The most useful records
are:

- `10_reconstructed_rule_inventory.json` and
  `14_inventory_manifest_bijection.txt`;
- `35_rerun_klean_preflight_compatible_env.json`;
- `45_obligation_bijection_and_target_identity.txt`;
- `49_fresh_lake_clean_full.txt`, `50_fresh_lake_build_full.txt`,
  `51_print_axioms_exact.txt`, and `52_print_final_type_and_body.txt`;
- `59_operational_bridge_examples_and_mutations_final.txt` and
  `BridgeAudit.lean`;
- `76_candidate_trust_target_and_axiom_reconciliation_complete.txt`;
- `79_independent_classification_judgment.txt`.

## Producer and mounted-input integrity

Before evaluating Stage 4, I hashed the two exact generation-time producer
sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes exactly match `/reference/generation-tools/source-manifest.json`
and `/reference/klean-generation/generator-manifest.json`. Both manifests
identify the immutable generator image as
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the producer-source path recorded by `/audit-input.json` binds the same image
ID. The trusted tree digest of `/reference/generation-tools` is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly the audit-input value. There is therefore no producer-source
infrastructure error. Raw comparisons are in
`05_producer_integrity_and_manifests.txt`,
`06_producer_cross_reference.txt`, and
`42_audit_input_hash_reconciliation.txt`.

I also independently recomputed every mounted top-level digest recorded by
the audit input. The Stage 3 manifest, generated tree, producer tree, K audit,
K workspace, entire Stage 4 tree, candidate Lean workspace, and frozen Stage
1 export all match. All 770 recorded Stage 1 per-file hashes match
bijectively, with no missing, extra, or changed file. The audit input also
records hashes for prior Stage 5 invocation logs that are not among the
mounted inputs; I did not treat those unavailable prior logs as evidence. The
mounted candidate workspace digest itself is verified.

## Stage 3 inventory reconstruction

With `PYTHONPATH=/reference`, I ran the trusted
`tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof`. It reconstructed this local verification-module
closure:

- verification module closure: exactly `[VERIFICATION]`;
- frozen `verification.k` SHA-256:
  `faca9c79e3e682c7c55c83a5a3d8488cd94981b6a0a22672628775aaed76ac9e`;
- ordered rule count: 10;
- whole inventory SHA-256:
  `60eb713b2b76c3b7c275bba937b7723b878edafd277c1b79e528ce79ab39b6fd`.

For every rule, the reconstructed module, source span, source text,
attributes, normalized source hash, and `source_rule_id` match the protected
Stage 3 record. The ordered ID list is identical. There are no omissions,
extras, duplicates, reordered identities, hash changes, or unaccounted
classifications. This is an actual bijection rather than only a count match.

### Independent classification

I classified each entry from the frozen source and the supplied operational K
semantics, without relying on the protected labels:

| Frozen lines | Rule family | Independent class |
|---|---|---|
| 9 | `onlyStrings` empty case | `DEFINITION` |
| 10–11 | `onlyStrings` recurrence | `DEFINITION` |
| 16 | `stringCodes` string projection | `DEFINITION` |
| 17 | `stringCodes` exhaustive `owise` case | `DEFINITION` |
| 21–23 | guarded `seqLen`/`isLen` bridge | `DOMAIN_LEMMA` |
| 28 | `totalLen` wrapper | `DEFINITION` |
| 29 | `totalLenFrom` base case | `DEFINITION` |
| 30–31 | `totalLenFrom` recurrence | `DEFINITION` |
| 35 | `lastLoopValue` base case | `DEFINITION` |
| 36–37 | `lastLoopValue` recurrence | `DEFINITION` |

The sole domain lemma is:

`rule-b3f45b5d74172f8b06aeed730c933057ce5ded1254eac17997dee1565ec954d1`

```k
rule seqLen(V:Val) => isLen(stringCodes(V))
  requires isStrV(V)
  [simplification]
```

This rule is not a definition: it relates the already operational `seqLen`
observer to the separately defined `stringCodes` projection and existing
`isLen` observer. It is not an ordinary execution rule. Stage 1 does not first
prove this exact rule in a module omitting it and then use it later:
`spec.k` imports `verification.k` with the rule already present, and an exact
Stage 1 search finds the rule only at `verification.k:21`. It therefore cannot
be a `PROVED_DERIVED_LEMMA`.

The lemma is both true and relevant. The source program adds `len(string)` in
its loop, while the postcondition summary adds
`isLen(stringCodes(V))`. Supplied semantics gives
`isStrV(str(_)) => true`, `seqLen(str(IS)) => isLen(IS)`, and the frozen
definition gives `stringCodes(str(IS)) => IS`. This is the necessary bridge
from execution to the summary under the list-of-strings precondition. The
rule is the only `[simplification]` rule and is correctly classified as
`DOMAIN_LEMMA`, satisfying the simplification restriction.

The protected manifest agrees with all ten independent judgments. The true
domain set is genuinely nonempty and contains exactly the rule above.

## Stage 4 deterministic generation

I reran
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation)` with
`PYTHONPATH=/reference`. The successful result is saved verbatim in
`35_rerun_klean_preflight_compatible_env.json`:

- status `PASS`;
- one obligation;
- generated tree
  `d8bed56de0f6614a59a20b9984e4f5936fc3c8de2596ead7a2067fc5e1be5a6d`;
- frozen input
  `03d9cf1f44a803a47c93a7da985794a62b18e4d8ccea82848810250a2f1dbd01`;
- Stage 3 manifest
  `49cec90b5460c72c6a071aa63cda58c835ab4cd3670ad304eb7c16b9fcb88754`;
- generated `lake clean` and `lake build` both exit 0.

The sandbox exposes `/proc/self/exe` but not the numeric
`/proc/<current-pid>/exe` path Lean uses during process launch. The first
preflight attempt therefore failed before checking the project. I reran with
the pinned Lean 4.22.0 toolchain and a small, source-preserved `LD_PRELOAD`
compatibility shim that redirects only numeric self-PID `readlink` and
`readlinkat` requests to `/proc/self/exe`. Its source and diagnostics are in
`proc_exe_compat.c`, `33_proc_exe_c_probe.txt`, and
`34_proc_exe_compat_validation.txt`. It does not alter files, Lean
elaboration, axioms, or proof logic. The original environmental failure is
preserved in `16_rerun_klean_preflight.json`.

### Obligation bijection and mathematical adequacy

The independently determined one-element domain set maps bijectively to the
one source rule and one generated obligation. The generated source record
preserves the exact module, lines 21–23, normalized hash, attributes, and
classification. Its Lean conjunct is exactly:

```lean
∀ (V : SortVal)
  (h : («isStrV(_)_MPY-BUILTINS_Bool_Val» V) = true),
  («seqLen(_)_MPY-BUILTINS_Int_Val» V : SortInt) =
    («isLen(_)_MPY-CORE_Int_IntSeq»
      («stringCodes(_)_VERIFICATION_IntSeq_Val» V) : SortInt)
```

The premise is not vacuous merely because the proof-object name `h` is not
used in the conclusion; its type is the guard that restricts the universal
claim to strings. The conjunct preserves both sides of the K equation and the
guard. There are no missing, duplicated, irrelevant, weakened, or extra
conjuncts.

The selected Stage 4 status is `OK`, not `KLEAN_NO_OBLIGATIONS`, which is
correct for the nonempty true domain set.

### Fixed target identity

I recomputed the target hashes using the producer's canonical extraction and
normalization:

- declaration: `Klean74TotalMatch.Lemmas.targetStatement`;
- definition SHA-256:
  `63f9c25ae4fbc68a8471c2f6cabcd4f1c415e0ccfa20e2bb3ce2d4c6c02c8d86`;
- applied-statement SHA-256:
  `37ce194668b59289f44f0a55714ccf2d48f59c89caae4f0742b2a8a7bd4f406b`.

The direct values match the obligation map, generator manifest, preflight
result, and `/audit-input.json`. The target has exactly the four parameter
bindings (`isLen`, `isStrV`, `seqLen`, `stringCodes`) recorded in the
manifest, and every binding points to the sole source-rule ID. Thus Stage 4
did not change the target.

## Stage 5 Lean proof

I created the corrected fresh project at
`/tmp/audit-work/74-total-match-proof-audit-002`, copied the candidate into
it, and copied the immutable generated project into `Base`. The `Base` tree
hash before the build was the expected
`d8bed56de0f6614a59a20b9984e4f5936fc3c8de2596ead7a2067fc5e1be5a6d`.
I then ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, including `Base.Klean74TotalMatch.Lemmas` and
  `Proof`.

After the build the `Base` tree still has the same digest. An earlier copy
attempt placed generated files one directory too deep; I detected it,
discarded that worktree, and used only the corrected `-002` project. Both
attempts are retained in the raw evidence so the history is explicit.

The candidate's only Lean sources are `Proof.lean` and `lakefile.lean`.
Trusted lexical scanning and an independent token scan find no `sorry`,
`admit`, `unsafe`, new `axiom`, or new `opaque`. The fresh project contains
exactly one `def targetStatement`, at the immutable
`Base/Klean74TotalMatch/Lemmas.lean`; the candidate neither changes nor
shadows it.

`#print Proof.final` shows that `Proof.final` has exactly this type:

```lean
Klean74TotalMatch.Lemmas.targetStatement
  Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
  Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val»
  Proof.«seqLen(_)_MPY-BUILTINS_Int_Val»
  Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val»
```

It is the fixed applied target itself, not a separately duplicated,
weakened, or vacuous theorem. The trusted Stage 5 mechanical gate also
returns `PASS` with the same target and an empty used-axiom list.

### Axiom accounting

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' does not depend on any axioms
```

The used dependency set is therefore empty. It contains neither `sorryAx`
nor an unrecorded trust escape and is trivially a subset of the 41 declarations
recorded in `trust-inventory.json`. None of those generated trust declarations
is used by `Proof.final`.

## Operational-bridge audit

A clean theorem alone is insufficient here: the fixed equation is
underdetermined if dishonest parameter definitions are allowed. I therefore
located and reviewed the candidate's exact four `def`s against their
`kore_symbol`s, source-rule bindings, frozen K rules, generated constructors,
source solution, and supplied operational semantics.

| Target parameter | Operational judgment |
|---|---|
| `isLen` | Exact structural recurrence: empty `IntSeq` maps to 0 and `iCons` maps to one plus the tail length, matching `core.k:227–229`. |
| `isStrV` | Returns true exactly for the generated direct string injection and false for every other `SortVal`, matching `builtins.k:293–297`. |
| `stringCodes` | Projects the exact code sequence from a string and returns empty for the exhaustive non-string `owise` case, matching `verification.k:15–17`. |
| `seqLen` | Implements all five fixed rule domains: list and tuple through the exact `ValSeq` recurrence, string and set through `isLen`, and ranges through the three guarded `rangeLen` equations. Its fallback and zero-step branch totalize only inputs on which the partial K function has no applicable rule; they do not alter any frozen operational case or the guarded target. |

The range arithmetic agrees with the supplied K equations on each applicable
guard: positive nonempty, negative nonempty, and the two valid empty-range
branches. The source solution calls `len` only on strings in the theorem's
domain, where `seqLen`, `stringCodes`, and `isLen` reduce to the same code
sequence.

I compiled a separate Lean audit harness with examples for empty, singleton,
and three-element `IntSeq`s; strings and non-strings; exact projection and
fallback; list, tuple, string, set, positive range, negative range, empty
range, and totalization cases. It exits 0 and evaluates the representative
lengths to the expected values.

The harness also probes counterfactual definitions:

- an always-false recognizer makes the target vacuously provable;
- coordinated constant-zero length functions plus an empty projection also
  make it provable;
- changing only `seqLen`, only `isLen`, or only `stringCodes` to those
  convenient definitions is refuted by a concrete one-character string.

These mutations demonstrate why proof success by itself is not the basis for
the verdict. The actual candidate is nonconstant, nonidentity,
non-hard-coded, non-vacuous, and matches the operational equations on every K
rule domain.

As a supplemental check, I compiled a small K runner importing the frozen
verification module. Its Haskell execution process was killed by the sandbox
with exit 137, and the installed backend does not support the attempted
functional `kprove` claims. Those diagnostics are retained in evidence
`61`–`69` and were not used as positive evidence. They do not affect the
required trusted preflight, independent source/KORE comparison, clean Lean
build, or adversarial Lean checks.

## Final judgment

All required integrity checks, independent mathematical classifications,
Stage 4 obligation checks, fixed-target checks, proof checks, axiom checks,
and operational-bridge checks pass. I found no material concern.

VERDICT: PASS
LEGITIMACY: LEGIT
