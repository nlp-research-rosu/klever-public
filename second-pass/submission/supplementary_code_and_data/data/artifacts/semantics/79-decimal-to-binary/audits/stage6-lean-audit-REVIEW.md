# Independent audit: HumanEval 79-decimal-to-binary

## Result

The Stage 3 classifications and deterministic Stage 4 generation are sound. The Stage 5 project also clean-builds, proves the exact generated target, and uses no axioms. The overall submission is nevertheless not legitimate because the sole target parameter is not an honest implementation of the frozen K operation: the candidate's `doSlice` disagrees with the supplied semantics on a concrete zero-step slice for which K does reduce.

Audit mode was independently read as `CLASSIFICATION_AND_PROOF` from both `AUDIT_MODE` and `/audit-input.json`. I treated all mounted candidate and provenance content as untrusted evidence and reconstructed or reran the relevant checks.

## Producer provenance and frozen inputs

Before judging generation, I hashed the two mounted generation-time producer files:

- `klean_export.py`: `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`: `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

These hashes match both producer entries in `source-manifest.json`, both entries in `generator-manifest.json`, and the producer provenance bound by `/audit-input.json`. The immutable image identity is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
the image digest is also the basename of the launcher-recorded producer-source path. The reconstructed producer-source pipeline tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.
There is therefore no producer-source `AUDIT_ERROR`.

I independently recomputed every mounted tree or file digest used by the launcher:

| Input | Recomputed digest |
|---|---|
| Stage 1 K workspace | `01353420051a24e0acdc8b063ab5581b41a8fcccd8b1235703cc2ec0d7d8179a` |
| Stage 1 export | `78ce539b067539d19bcf29bcaa222d156f066da111476441e375254d9c5ffc67` |
| Stage 3 discovery manifest | `5e9c5dbf16eef703097945dd0f65b7b31457e840c99050e3e6d7b8f20f517a63` |
| Selected K audit | `830b720831519036f35cb31b8827dc6b1cab61a31c1653963dd291398685304c` |
| Stage 4 generation | `eac58105e2393db7fcde7659d44818d3b9f27b14a06a4133a0bd5a6d274b41e8` |
| Generated exporter tree | `7dae9580bfd2742201f0ac614474cb63b6b9ef060eb3979842bd7a790fff1b3c` |
| Candidate Lean workspace | `1ec284d70977aa9c0ccdc58dc1ff7823a0f3f17955ffc9859f674f3beabc68db` |

All 34 Stage 1 source-file hashes matched exactly, as did the launcher envelope's reconstructed `resolved_input_sha256`,
`cc98c820d9c19f2f23b21aac55e9114bcfd0c15bbeaf1d2563e65fa812cdcd90`.
The launcher records a Lean-invocation tree hash, but that separate tree is not mounted; the signed input envelope and every mounted source/project tree are internally consistent.

Evidence: `evidence/01_producer_provenance.log`, `evidence/03_mounted_hash_audit.log`.

## Rule inventory reconstruction

Using the trusted rule-inventory implementation with the frozen `verification.k`, I reconstructed the complete local verification-module closure. The closure contains only module `VERIFICATION`, its source SHA-256 is
`270fa8ad3dfaad71f930610c6b319cb5d2ac6cb3af473ca6749404517eb54c6c`,
and its inventory hash is
`ce0da57b41b493ecc9298585f08fd05a78a87b6d9bbbe0bd3ca904bd1cb58702`.

The complete ordered inventory is:

| Span | Reconstructed identity | Attributes | Independent classification |
|---|---|---|---|
| `verification.k:12-18` | `rule-d413ecca2d0d055a04bc2f4fe8404284cf3025dc1bb61dd03e2d09244027583b` | `priority(40)` | `DOMAIN_LEMMA` |
| `verification.k:20-36` | `rule-f0749fc6bd85fe62094ab4f801ecd2f6fd2b3797fe1fc9760ae63e8c1f50cb7e` | none | `DEFINITION` |

For each entry I re-extracted the exact source span, normalized it with the trusted code, rehashed it, and regenerated the `source_rule_id`. The resulting sequence is bijective and order-identical to `lemma-discovery.json`: no omitted, duplicated, extra, reordered, or altered identity exists. There are no `simplification` rules.

Evidence: `evidence/02_inventory_reconstruction.log`.

## Independent Stage 3 classification

The first rule states that slicing a string consisting of two arbitrary leading codes and symbolic tail `REST` at `[2:]` returns `REST`. It is not an ordinary operational equation: the supplied semantics already defines `doSlice` through `slStart`, `slStop`, `slStep`, and `buildIS`; this additional verification rule summarizes their result over an arbitrary symbolic sequence. It is not a definition, recurrence, macro, or named proof term. It is also not a proved-derived lemma: `prove.sh` compiles `verification.k` with the rule present and then proves the program claim, with no earlier proof of this exact rule against a module omitting it. `DOMAIN_LEMMA` is therefore the only valid classification.

The domain lemma is relevant. The source solution computes `"db" + bin(decimal)[2:] + "db"`. Under the supplied semantics and the precondition `N >=Int 0`, `bin(N)` has code prefix `48, 98` followed by `binCodes(N)`, precisely the lemma's pattern. As a direct relevance test, I rebuilt Stage 1 after removing only this rule. `kprove` then stopped at symbolic
`buildIS(iCons(48, iCons(98, binCodes(N))), ...)` and exited nonzero. Replaying the unmodified Stage 1 workspace produced `#Top`.

The second rule expands the named proof term `#runDecimalToBinary(N)` to the closure and exact translated body from `solution.mpy`. It is proof-harness definitional scaffolding and is correctly a `DEFINITION`, not a domain or operational lemma.

Thus the true domain set is nonempty and contains exactly the first rule.

Evidence: `evidence/13_domain_relevance_without_lemma.log`, `evidence/14_semantic_source_excerpts.log`, `evidence/15_stage1_k_replay.log`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` against `/reference/k-proof`, `/reference/lemma-discovery.json`, and `/reference/klean-generation`. It returned `PASS`, with one obligation, zero designated sorries, 47 generated trust declarations, and generated tree hash
`7dae9580bfd2742201f0ac614474cb63b6b9ef060eb3979842bd7a790fff1b3c`.
The trusted full mechanical final gate independently repeated this check and passed.

The audit sandbox exposes a namespace PID from `getpid()` for which `/proc/<pid>/exe` is absent, while Lean 4.22 discovers itself through that exact path. The first two preflight attempts therefore failed before inspecting the project. I used a minimal `LD_PRELOAD` compatibility shim that makes `getpid()` return the numeric PID represented by `/proc/self`; its complete source and build transcript are saved as `evidence/proc_pid_compat.c` and `evidence/05_build_proc_pid_compat.log`. The shim changes no generator, source, target, or proof content. The successful preflight output is the evidence used above.

The exact source-rule/obligation mapping is one-to-one:

- source: `rule-d413...`, span 12-18, normalized hash `d413...`;
- generated obligation: for all `REST`, `_SECOND`, and `_FIRST`,
  `doSlice(str(iCons(_FIRST, iCons(_SECOND, REST))), someB(2), noB, noB) =
  str(REST)`;
- parameter: the exact generated binding for KORE symbol
  `LbldoSlice'LParUndsCommUndsCommUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'Val'Unds'OptInt'Unds'OptInt'Unds'OptInt`.

There are no omitted conditions: the K rule has no `requires` clause. Every source variable is universally bound; no vacuous `True` conjunct, duplicate, unrelated obligation, or weakening was introduced. The `DEFINITION` rule appropriately generates no domain obligation.

The fixed target was independently reconstructed from generated source and exactly matches both manifests and `/audit-input.json`:

- declaration: `Klean79DecimalToBinary.Lemmas.targetStatement`;
- definition hash: `4910968b1097a78baaca49b9f8c36a9df7f36302d8861279452ef83982670443`;
- statement hash: `40a96376a08daa032535da221dec1de2324bf9c0d3a79398775032494220089e`;
- sole parameter binding hash: `a58cbcf42de91d10dda380de972adef8e3d507648061f11d4ef66413c313eca0`;
- obligation-map hash: `5b70b6d2b6473a630d35ead7f0f883439ec3e6499c7b31d697b66005819a6ec0`.

Stage 4 is therefore structurally and mathematically correct. This is not a `KLEAN_NO_OBLIGATIONS` case.

Evidence: `evidence/04c_stage4_preflight_proc_compat.log`, `evidence/09_fresh_mechanical_final_gate.log`, `evidence/03_mounted_hash_audit.log`.

## Stage 5 clean build, target identity, and trust

I created `/tmp/audit-work/stage5-fresh`, copied the candidate into it, and copied the exact generated project into `Base`. In that fresh tree, both `lake clean` and `lake build` completed successfully. The fresh `Base` tree retained the expected generated hash. Candidate source hashes also remained identical to the read-only candidate.

The candidate does not redefine or shadow `targetStatement`, and it contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. There is one `Proof.final`, whose printed type is exactly:

```text
Klean79DecimalToBinary.Lemmas.targetStatement
  Proof.«doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
```

`#print axioms Proof.final` reported exactly:

```text
'Proof.final' does not depend on any axioms
```

The generated trust inventory contains 47 allowlisted declarations and the generated project contains the same 47 declarations, but none is reachable from `Proof.final`. Consequently there is no `sorryAx`, no unrecorded proof escape, and no used dependency requiring further reconciliation. Mechanically, `Proof.final` proves the exact immutable target, not a duplicate or weakened variant.

Evidence: `evidence/07_stage5_fresh_build.log`, `evidence/08_axiom_audit.log`, `evidence/09_fresh_mechanical_final_gate.log`, `evidence/12b_candidate_integrity.log`.

## Operational bridge audit

There is one target parameter, so the candidate's exact definition at `Proof.lean:133-162` was compared with its KORE binding, `rule-d413...`, the source solution, and the frozen `subscript.k` equations. The candidate does correctly handle the target case, ordinary positive slices, clamping, negative indices, negative steps, and the frozen string/list/tuple constructors in the adversarial examples tested. I also constructed a deliberately wrong function that always drops two string codes: it proves the immutable target but fails an off-target positive slice. This counterfactual confirms why target provability alone does not establish the operational bridge.

The candidate has a decisive semantic defect. Its helper contains:

```lean
if step = 0 then none
```

and its public `doSlice` maps that `none` result back to the unchanged input. The accompanying candidate comment treats every zero-step operation as K-stuck. That is false in the frozen semantics when both bounds are explicit:

- `slStep(someB(0))` reduces to `0`;
- `slStart(someB(I), ...)` and `slStop(someB(I), ...)` reduce through `slAdjust` without a nonzero-step guard;
- in `buildIS`, the recursive guard is false for step zero and the terminal rule's negated guard is true, so the result is `.IntSeq`.

For the concrete term

```text
doSlice(str([10,20,30]), someB(0), someB(3), someB(0))
```

the unextended frozen K semantics proves the result is `str(.IntSeq)` (`#Top`). In Lean, the candidate definition reduces to the unchanged `str([10,20,30])`, and the independent audit file proves both that equality and its inequality with `str([])`. Thus the two sides disagree on a ground input to the bound operation.

The initial K adversarial run used bare functional claims, which this Haskell backend rejects as an unsupported claim form; I reformulated them as ordinary configured reachability claims. Those reruns passed, including the zero-step K result. The direct Lean audit also compiled successfully. The earlier preflight failures were the documented `/proc` issue, and the first candidate-integrity script failure was an audit-script schema assumption corrected in `12b`; none is used as evidence against the candidate.

Evidence: `evidence/10b_ground_k_operational_config.log`, `evidence/10c_zero_step_k_counterexample.log`, `evidence/11_lean_operational_adversarial.log`, `evidence/11b_zero_step_lean_counterexample.log`, `evidence/11c_zero_step_lean_counterexample_direct.log`, and the frozen/candidate excerpts in `evidence/14_semantic_source_excerpts.log`.

The target theorem happens to exercise only `someB(2), noB, noB`, so this incorrect zero-step branch does not prevent the short `rfl` proof. But the required target parameter is the bound `doSlice` operation, not an arbitrary target-specific witness. Because its supplied definition fails to implement the frozen operational meaning, this is an operational-bridge failure and requires `FAIL` / `NOT_LEGIT` despite the valid classifications, deterministic generation, clean build, exact theorem identity, and empty axiom dependency set.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
