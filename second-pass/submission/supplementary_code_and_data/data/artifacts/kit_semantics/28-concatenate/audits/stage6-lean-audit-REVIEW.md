# Independent audit: HumanEval 28-concatenate

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_AND_PROOF`, condition
`kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. I independently
audited the frozen Stage 1 verification-rule closure, the protected Stage 3
classification, deterministic Stage 4 generation, and the supplied Stage 5
Lean proof. I treated prior reviews, logs, comments, and classifications only
as evidence and did not rely on their conclusions.

All substantive gates pass. The only environment issue was a PID-namespace
incompatibility in Lean's executable discovery. It was isolated and repaired
with a narrow `readlink` preload shim described below; no frozen input,
generated source, candidate source, Lean binary, or theorem was changed.

## Producer-source and immutable-input integrity

I performed the producer check before judging Stage 4. The mounted bundle has
exactly `klean.py`, `klean_export.py`, and `source-manifest.json`.

| Item | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |
| producer bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

The two file hashes agree with `generator-manifest.json` and the source
manifest. Both manifests identify generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the image key is also the basename of the producer-source path recorded in
`/audit-input.json`. The producer bundle tree hash agrees with the audit input.
See `evidence/producer-integrity.log`.

I also recomputed the mounted tree/file hashes rather than accepting manifest
values:

| Mounted artifact | Recomputed hash | Recorded match |
|---|---|---|
| Stage 1 full tree | `898ef000b991ffd60d711d75e84b2550ca69ffeab57b77434c6a5e6bc8579f29` | yes |
| Stage 1 export tree | `82e6583db1a89891d9d3148dd8da71e3c5e838a75707090d86634ee108019b38` | yes |
| Stage 2 K audit tree | `25b228efd94f9058bcc45c74835ad526a470260ff6659cc82cd6d9b9ba185a3f` | yes |
| Stage 3 discovery file | `81bc5b664867124ac6040d98e2cda120346c9428ceba71d056cb98f0db7bd3cf` | yes |
| Stage 4 generation tree | `b897b0386025188c4a5e31f6cb0c50eaeb1edb97bc92a4cb478c1896cf4b92e3` | yes |
| generated project tree | `4aa7abbb3edc3f4a00297119ba6bdeeb714e10f313c33968496c974de3a198e7` | yes |
| Stage 5 candidate tree | `d81c038649662214d54f90225dd4f80c743bdccdd7121960bcb85594bf0045d0` | yes |

All 769 per-file Stage 1 hashes in `stage1_source_hashes` also match exactly.
The launcher does not mount the separate Stage 5 invocation transcript, so its
recorded invocation-tree hash is not a hash of an audit input; no conclusion
here relies on that prior transcript. The mounted successful candidate tree is
the Stage 5 input and its recorded hash matches. Full results are in
`evidence/recorded-hash-and-stage4-bijection.log`.

## Stage 3 inventory reconstruction and classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` over
`/reference/k-proof`. `prove.sh` selects `VERIFICATION`, and the local
verification-file closure is exactly `VERIFICATION`. The reconstructed
`verification.k` hash is
`2e889c33acb13e241a4fa27718fed136829aac513168f9b0f2bebbd6d7fcf5fa`;
the canonical inventory hash is
`db23f00c4d52498c8b55896d22cd454b5a735cc3d960bd225af2ec15cc2b9995`.

The reconstructed inventory, in source order, is:

| Span | `source_rule_id` | Attributes | Independent class | Judgment |
|---|---|---|---|---|
| 10 | `rule-d67f74749887fbf3e482ab3b5e009e306d6afabeb7e2bc1483cdcc5bc5d801aa` | — | `DEFINITION` | `stringCodes(str(S)) = S`, a projection equation |
| 11 | `rule-fd0940a4d6054e1358229d8416d82d1fdbd9fc9b81a95171ac29cc004419b996` | `owise` | `DEFINITION` | total fallback for that projection |
| 15 | `rule-dcec90ae81b6468389e91083acc95d81ead6981ccababa579f6172a0a877a7e3` | — | `DEFINITION` | empty `isStringSeq` equation |
| 16–17 | `rule-7a72869f4d1d964b627bb3b06d70211a5e2d1d60583ce2a867ccbb8d7b284747` | — | `DEFINITION` | structural `isStringSeq` recurrence |
| 23 | `rule-caaa68653c6b00f190e89bd450eb4b1da239abda96d0efd431698e876453410d` | — | `DEFINITION` | empty `concatFrom` equation |
| 24–26 | `rule-164607b7d03894ef15a07854149cb03c9b9031a6e6187bd89611899d0aaac54e` | — | `DEFINITION` | guarded structural `concatFrom` recurrence |
| 31 | `rule-2bc2a66c772aae97380ca3ab3abdcf702833b825027b9f8fc0da1fe4878d02ac` | — | `DEFINITION` | empty `lastFrom` equation |
| 32–34 | `rule-8d075e2e7a462abce866779cfe5fc6c30b077acc04bc848e0e0bb58c1da430da` | — | `DEFINITION` | guarded structural `lastFrom` recurrence |
| 39–42 | `rule-d77f984813dd200ec980ca7e00225a96be53f3a6ed10be91093061eb9e528506` | `simplification` | `DOMAIN_LEMMA` | guarded fact about pre-existing `applyBin` |

For every entry, the source span, normalized SHA-256, and `source_rule_id`
were recomputed. The Stage 3 identities occur exactly once and in the same
order; there are no omissions, extras, duplicates, reordered entries, changed
hashes, or unclassified rules. The protected classes equal the independent
classes above. The complete rule text and hashes are in
`evidence/inventory-reconstruction.log`.

The first eight rules define named proof terms or structural summaries. They
are not ordinary execution rules and do not assert the target property. The
last rule rewrites the pre-existing operational symbol `applyBin`; it defines
no new proof term. Stage 1 compiles it into `VERIFICATION` before its positive
proofs and does not first prove the same rule in a module that omits it, so it
cannot be `PROVED_DERIVED_LEMMA`.

The domain-lemma classification is mathematically correct. Under its guard
`V ==K str(stringCodes(V))`, `V` is a semantic string and the frozen
`MPY-STR` rule

```text
applyBin("+", str(A), str(B)) => str(seqConcat(A, B))
```

gives exactly the claimed result. It is relevant: the source loop performs
`result += string`; frozen `AugAssign` places precisely this `applyBin` term in
the result binding, while the loop summary and final postcondition use
`concatFrom`/`seqConcat`. Thus the simplification connects real source
execution to the stated summary. It is the only simplification rule and is
correctly classified as a domain lemma.

## Stage 4 deterministic generation

I invoked the required trusted function with `PYTHONPATH=/reference` and the
three required inputs. The first attempt exposed an environment-only Lean
failure: Lean 4.22 uses `/proc/<getpid>/exe`, but this sandbox's PID namespace
does not agree with the mounted `/proc`. `evidence/stage4-check-generation.log`
records that failure. `evidence/procself_readlink.c` is a 19-line preload shim
that redirects only `/proc/<pid>/exe` reads to `/proc/self/exe` and delegates
every other `readlink` unchanged. With that shim, the pinned toolchain reports
Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the same trusted
`check_generation` call returns `PASS`. The exact result is in
`evidence/stage4-check-generation-with-proc-shim.log`.

The preflight independently clean-built the generated project and reported:

- Stage 1 export hash: `82e6583db1a89891d9d3148dd8da71e3c5e838a75707090d86634ee108019b38`;
- discovery hash: `81bc5b664867124ac6040d98e2cda120346c9428ceba71d056cb98f0db7bd3cf`;
- generated tree hash: `4aa7abbb3edc3f4a00297119ba6bdeeb714e10f313c33968496c974de3a198e7`;
- one obligation, zero sorries, and 42 generated trust declarations; and
- successful `lake clean` and `lake build`.

There is a strict one-to-one map:

```text
rule-d77f984813dd200ec980ca7e00225a96be53f3a6ed10be91093061eb9e528506
    ↔ the sole Lean conjunct (SHA-256
      757af46e2e700bdd9d6f7ca12e7f97db5615fa6d62c5caac48292bc975dd6095)
```

The obligation carries the same source span 39–42, normalized hash, inventory
hash, and discovery hash. The source-rule and obligation ID sequences are
identical and duplicate-free. The obligation-map hash
`0ed08f8e6d2d68fcedac326113e5debe7902245ddfe37a5c313d40ba75d4cbac`
matches the generator manifest.

Mathematically, the Lean obligation says: for every `V` and `A`, if the K
injection of `V` equals the injection of
`str(stringCodes(V))`, then string `applyBin("+", str(A), V)` equals
`str(seqConcat(A, stringCodes(V)))`. This is the exact frozen rule above,
including its guard, operator, argument order, result constructor, and
quantification. It is neither irrelevant nor weakened. It has no duplicate or
vacuous conjunct, and its premise is satisfiable for every
`V = str(B)`; `evidence/stage5-operational-bridge-check.log` checks a concrete
nonempty inhabitant.

The generated target is exactly:

```text
Klean28Concatenate.Lemmas.targetStatement
  «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
  «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
  «stringCodes(_)_VERIFICATION_IntSeq_Val»
```

Its definition hash is
`8dca32cee5a4de83089284f41b25df5beb12774e7885224a28c9d1efc88970f4`,
and its statement hash is
`a67c9ad0a05bb83890d59b9a7b7c2a127b0fa5ea7b6d2fc2f031bb5cad203ae5`.
The extracted target equals the generator manifest, audit input, and recorded
preflight target byte-for-byte/field-for-field. Because the independently true
domain set contains one rule, status `OK` with one target is required; this is
not a `KLEAN_NO_OBLIGATIONS` case.

## Stage 5 Lean proof and trust audit

I created the fresh project
`/tmp/audit-work/concatenate-proof.Bq35lc`, copied the candidate into it, and
copied the immutable generated project contents into `Base`. I then ran both
commands required by the audit:

```text
lake clean  -> exit 0
lake build  -> exit 0; Built Proof; Build completed successfully.
```

Complete output is in `evidence/stage5-lake-clean.log` and
`evidence/stage5-lake-build.log`. The independent trusted Stage 5 mechanical
gate also returns `PASS`; see `evidence/stage5-trusted-final-gate.log`.

The fresh `Base/Klean28Concatenate/Lemmas.lean` is byte-identical to the
generated target file, and its extracted declaration and hashes remain the
manifest/audit-input target above. Outside `Base`, the candidate contains no
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. Each of the three target
parameters has exactly one `def`; the candidate neither declares nor shadows
`Klean28Concatenate.Lemmas.targetStatement`. It contains exactly one theorem
`Proof.final`, whose normalized statement is the fixed target and not a copy,
weakening, or alternate theorem. See
`evidence/stage5-static-target-trust-check.log` and
`evidence/stage5-proof-identity-lean.log`.

The exact requested axiom output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

`sorryAx` is absent. `propext` and `Classical.choice` are in the trusted
mechanical gate's Lean-core baseline (`Quot.sound` is the other permitted core
entry but is not used). None of the 42 generated declarations listed in
`trust-inventory.json` is a dependency of `Proof.final`, and there is no
unrecorded dependency. The exact command/output is in
`evidence/stage5-print-axioms.log`.

## Operational-bridge adequacy

I checked every `target.parameters` definition independently of the successful
equational proof.

| Parameter | Frozen meaning | Candidate judgment |
|---|---|---|
| `stringCodes` | `stringCodes(str(S)) = S`; all non-string `Val` constructors map to `.IntSeq` by `owise` | Exact constructor projection and exact fallback |
| `seqConcat` | empty left sequence returns the right; a left `iCons(I,S)` returns `iCons(I, seqConcat(S,T))` | `appendCodeSeq` has exactly these base/step equations and preserves left-to-right order |
| `applyBin` | source-relevant rule is string `+`, producing `str(seqConcat(A,B))`; the frozen table also has Int/Bool/Float cases | String arm is exact and calls the exact append function; every unique defined Int/Bool/Float rule head has a corresponding arm. `noneV` is used only to totalize inputs where the frozen function has no applicable rule or a failed guard, none of which is in this obligation/source path |

This alignment is load-bearing. The source program initializes a string
accumulator and visits its list left-to-right, so the only reachable
`applyBin` branch for the theorem is string `+`. The candidate returns the
actual string payload from `stringCodes`, appends the first code sequence in
front of the second, and wraps that result as a semantic string. It is not a
constant, identity, hard-coded example, or postcondition oracle.

Adversarial checks in `evidence/stage5-operational-bridge-check.log` cover empty
and multi-element code sequences, operand order, a non-string projection
fallback, string and integer `applyBin`, Bool/Int addition, and negative Python
modulo/floor-division boundaries. The observed candidate string result for
`"ab" + "c"` is code sequence `[97, 98, 99]`. A frozen K execution independently
produces `abc` and `xyz` for the source examples
(`evidence/stage5-k-operational-witness.log`), and the source differential
oracle reports `cases=255 mismatches=0`
(`evidence/stage5-source-differential-witness.log`). These finite checks support
the direct rule-by-rule comparison; they are not used as a substitute for it.

I also constructed coordinated bad definitions in Lean: constant
`stringCodes`, constant `seqConcat`, and an `applyBin` returning the matching
constant string. Those bad definitions still prove the raw generated equation,
confirming that a clean proof alone is insufficient. The same Lean file proves
that each actual candidate definition differs from the convenient mutation on
a concrete operational witness. Finally, a reversed concatenation result was
rejected with exit 1 and a non-definitional-equality error; see
`evidence/stage5-false-result-rejected.log`. The candidate therefore passes the
independent operational bridge gate.

## Evidence index

The principal raw command/result files are:

- `evidence/launcher-mode.log`
- `evidence/producer-integrity.log`
- `evidence/inventory-reconstruction.log`
- `evidence/recorded-hash-and-stage4-bijection.log`
- `evidence/stage4-obligation-map.log`
- `evidence/stage4-generated-target.log`
- `evidence/stage4-check-generation-with-proc-shim.log`
- `evidence/stage5-lake-clean.log`
- `evidence/stage5-lake-build.log`
- `evidence/stage5-trusted-final-gate.log`
- `evidence/stage5-proof-identity-lean.log`
- `evidence/stage5-print-axioms.log`
- `evidence/stage5-static-target-trust-check.log`
- `evidence/frozen-applybin-rules.log`
- `evidence/candidate-parameter-definitions.log`
- `evidence/stage5-operational-bridge-check.log`
- `evidence/stage5-false-result-rejected.log`
- `evidence/stage5-k-operational-witness.log`
- `evidence/stage5-source-differential-witness.log`

VERDICT: PASS
LEGITIMACY: LEGIT
