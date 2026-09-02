# Independent audit: HumanEval 113-odd-count

## Scope and result

The launcher records `CLASSIFICATION_AND_PROOF`, condition `kit-semantics`,
and semantics mode `SUPPLIED_SEMANTICS`. I independently audited the frozen
Stage 1 rule closure, the protected Stage 3 classification, deterministic
Stage 4 generation, and the Stage 5 Lean proof. I did not rely on the selected
Stage 2 review or any earlier PASS/classification statement.

The audit found one genuine, relevant domain lemma. Stage 4 generated exactly
one matching obligation, and the Stage 5 candidate honestly implements the
four operational bindings on that obligation's complete domain and proves the
unchanged generated theorem without a proof trust escape.

## Input and producer provenance

The signed resolution envelope recomputes to
`88e81f8e578f4be183f7bf32b2adf324c66303689dd34155ea7ba8e386284069`.
The producer-source check was performed before judging Stage 4:

- `klean_export.py`:
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`:
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`
- generator image:
  `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`

The two file hashes agree exactly with `generator-manifest.json` and
`source-manifest.json`. The image ID agrees among the generator manifest,
source manifest, and image-key component of the launcher-recorded producer
path. The producer bundle tree hash recomputes to
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching `/audit-input.json`. There is therefore no producer-source
infrastructure error.

All hashes for mounted inputs were recomputed:

| Mounted input | Recomputed hash | Result |
|---|---|---|
| Stage 1 workspace tree | `6ffff7c8044fae66e7c0d3843ceb7c754fc8e59b11b30de38be376bd61fa6ed2` | matches |
| Stage 1 export tree | `b249b960b7cd75709620b7bba5e5916e9b9f0ebca221c40742019cd919a86878` | matches |
| Stage 3 manifest | `935d1a70268f8ab5e2f30f40547c818a521ace32216a1f872afb8d8393180729` | matches |
| Selected Stage 2 tree | `be8d8e753d138c016a4ed4afdd66dce9c2d7ff66ab731f6e0403206de39b2bb7` | matches |
| Stage 4 generation tree | `b693bbd7cc22ed66c375784f74971f40c1d13d30ba7ebbdd91702203894f1142` | matches |
| Generated project tree | `6ade260c504660e9f944ad2b028e766aadddb999ba47006ca4596b53bd78af3b` | matches |
| Stage 5 candidate tree | `bcbc236f5324c70dab00a09afbedc863b85656423746b30d9e4943e2d09fdb0a` | matches |

All 828 launcher-recorded Stage 1 file names and SHA-256 values also match
bijectively. The launcher records a separate Lean-invocation-tree digest, but
does not mount that invocation tree; it is not independently rehashable from
the supplied inputs. The mounted candidate workspace and its recorded
workspace digest do match and are the artifacts used for the proof audit.

Relevant raw evidence:
`05_stage4_producer_provenance.txt`,
`08_stage4_producer_provenance_validation.txt`,
`27_recorded_hash_recalculation.txt`, and
`46_audit_input_envelope_validation.txt`.

## Frozen rule inventory

Using `/reference/tools/k_rule_inventory.py`, I reconstructed the local
verification-module closure selected by `prove.sh`. It consists of
`VERIFICATION-SYNTAX` and `VERIFICATION` and contains 12 rules. The frozen
`verification.k` hash is
`aba4b686ec444497c9bcb6f8087dfff2799f89d0f7c08dd70b5db5f7eaa1b051`.
The canonical inventory hash is
`84c56c6d77a6c8573f9c1eff1b9d516b8e8f84abb998ce1cf8f36e219de6f41a`.

For every entry I recomputed the source span, whitespace-normalized source
hash, `rule-<normalized-sha256>` identity, attributes, text, and order. The 12
reconstructed identities equal the 12 Stage 3 identities in order. Both sets
are unique; there are no omitted, extra, duplicated, or reordered identities,
and there is no unaccounted classification. The inventory hash in Stage 3
matches the recomputation, binding all source text, spans, attributes, and
normalized hashes.

The complete reconstructed inventory is in
`09_reconstructed_inventory.json`; the explicit bijection check is in
`11_inventory_bijection_check.txt`.

## Independent Stage 3 classification

My classification is:

- 11 `DEFINITION` rules: two source-body macros; the two-case
  `isStringVal` recognizer; the `stringCodes` projection; the base/cons
  `allDigitStrings` predicate; and the `oddDigitCount`, `oddLine`, and
  base/cons `oddLinesAcc` summaries.
- 0 `OPERATIONAL_RULE` rules.
- 0 `PROVED_DERIVED_LEMMA` rules.
- 1 `DOMAIN_LEMMA`:
  `rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617`
  at lines 90–93.

The domain lemma is the guarded simplification
`applyMethod(V, "count", str(PATTERN), .Vals) =>
cntSub(stringCodes(V), PATTERN)` under `isStringVal(V)`. It does not define a
new symbol; it extends the pre-existing supplied-semantics `applyMethod`
operation from a constructor-statically-known string to a symbolic `Val`
known by the new recognizer. Stage 1's earlier `projection-spec.k` proves only
the constructor-specialized supplied rule with receiver `str(CODES)`. It does
not first prove this exact guarded rule in a module omitting it, so
`PROVED_DERIVED_LEMMA` would be invalid.

The lemma is relevant, not decorative: the frozen source loop invokes
`s.count` five times while `s` is represented symbolically as `Val`, and the
input predicate establishes that it is a digit string. The lemma is true
because the honest guard forces `V = str(CODES)`, `stringCodes` projects
`CODES`, and supplied `methods.k` has exactly
`applyMethod(str(CODES), "count", str(PATTERN), .Vals) =>
cntSub(CODES, PATTERN)`.

Both simplification rules have allowed classes: `stringCodes` is a new
projection `DEFINITION`; the `applyMethod` extension is the `DOMAIN_LEMMA`.
The protected Stage 3 classification exactly matches this independent result.
The per-rule analysis is in `15_independent_classification.md`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3
manifest, selected Stage 4 generation, and pinned toolchain lock. It returned
`PASS`, obligation count 1, designated sorry count 0, and successful
`lake clean`/`lake build` diagnostics. The exact returned JSON is
`16_fresh_klean_preflight.json`.

The audit sandbox exposes an outer `/proc` through an inner PID namespace,
which initially prevented Lean 4.22 from resolving `/proc/<pid>/exe`. The
successful rerun used the pinned Lean installation plus the narrowly scoped
compatibility shim recorded in `25_pid_shim_validation.txt`; it changes only
Lean's `getpid()` result to the outer PID visible in `/proc`. Lean reports the
pinned version and commit `4.22.0 / ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.
This workaround does not change parsing, elaboration, kernel checking, source,
or generated artifacts.

Independent of preflight:

- the independently found domain set, input-manifest source set,
  obligation-map source set, and obligation set are the same ordered singleton;
- the source span, normalized hash, inventory hash, discovery hash, source
  text, and source rule ID all match;
- the unique Lean conjunct hash recomputes to
  `af1e056cc5f3b2d62301022bc63093a24f83a45bab94bccf1d59b4fdc12432e8`;
- every one of the four parameter binding hashes recomputes and points only to
  that source rule;
- the obligation-map hash and trust-inventory hash match their manifests;
- the generator toolchain object equals the pinned lock.

The conjunct preserves the complete K rule: universal `PATTERN` and `V`, the
`isStringVal(V) = true` guard, method name `"count"`, exactly one injected
string argument with an empty `Vals` tail, the projected `stringCodes(V)`,
`cntSub`, and the `Int`-to-`Val` injection. It is neither irrelevant nor
weakened. There is one conjunct, so there are no duplicate or vacuous added
conjuncts. Its guard is satisfiable for every generated string constructor.

There is exactly one `targetStatement` declaration. Its exact reconstructed
definition equals the generated file and hashes to
`59e949ee5f27e6d6683e3705e4a3d51234d133470e9c8ea874da23b7b5f7af07`.
Its applied statement hashes to
`df006c913b270a25cfecebc3e57649d5bb749fb436b597a0cad05f7f13619622`.
Both hashes and the complete target object agree among the generated source,
generator manifest, and audit input. Evidence is in
`28_stage4_sidecars_and_target.txt` and
`31_stage4_independent_integrity.txt`.

## Stage 5 clean build and target identity

I created `/tmp/audit-work/113-odd-count-stage5`, copied the generated project
into it as `Base`, and copied the candidate sources around that immutable
base. Before and after the build, `Base` was byte-for-byte identical to the
selected generated project and retained tree hash
`6ade260c504660e9f944ad2b028e766aadddb999ba47006ca4596b53bd78af3b`.

Fresh commands:

- `lake clean`: exit 0.
- `lake build`: exit 0; all generated modules, `Proof.ValueEq`,
  `Proof.Operational`, and `Proof` built successfully.

Complete output is in `33_stage5_lake_clean.txt` and
`34_stage5_lake_build.txt`.

Candidate-source inspection found:

- no `sorry`, `admit`, or `unsafe`;
- no new `axiom` or `opaque` declaration;
- exactly one definition for each of the four required target bindings;
- no candidate declaration or namespace shadowing `targetStatement`;
- exactly one `Proof.final`.

`Proof.final` has exactly the generated applied target type. A separate Lean
example accepts `Proof.final` at that exact type; `#print Proof.final` shows
the proof eliminates impossible non-string guard cases and proves the string
case. It does not prove a duplicate or weakened theorem. See
`35_stage5_target_and_source_integrity.txt` and `37_proof_identity.txt`.

## Axiom accounting

The required Lean command produced:

`'Proof.final' depends on axioms: [propext, Quot.sound]`

There is no `sorryAx`. `propext` and `Quot.sound` are Lean foundational
axioms explicitly permitted by the trusted mechanical gate, not candidate or
generated declarations. None of the 66 generated declarations in
`trust-inventory.json` is a transitive dependency of `Proof.final`; there are
no unrecorded non-foundational dependencies. Exact output and reconciliation
are in `36_print_axioms_proof_final.txt` and
`38_axiom_reconciliation.txt`.

## Operational bridge

I compared every target parameter to its KORE symbol, bound source rule,
frozen rules, source solution, and supplied operational semantics:

- `isStringVal` returns true exactly for `SortVal.inj_SortStr` and false for
  every other generated `Val` constructor, matching lines 79–80.
- `stringCodes` returns the exact code sequence from the string constructor,
  matching line 82. Its off-string totalization is unreachable under the
  honest guard and does not contradict any frozen equation.
- `cntSub` implements the supplied non-overlapping recurrence. Source-length
  fuel is sufficient because every recursive rule consumes at least one
  source code. Its empty-pattern shortcut returns the same zero as the frozen
  recurrence.
- `applyMethod` destructs the exact string receiver and one-string/empty-tail
  argument representation, selects `"count"`, calls the honest count
  implementation, and injects the result into `SortVal`. This is exactly the
  supplied string-count rule. The candidate also contains branches
  corresponding to every other supplied `applyMethod` equation, although
  `Proof.final` depends only on the count match domain.

Lean ground checks cover empty source, empty pattern, overlapping and
non-overlapping patterns, distinct positive counts, the string/non-string
recognizer boundary, exact string projection, a non-string method receiver,
and an unknown method. The observed count vector `0, 0, 3, 1, 2` equals an
independently implemented reading of the K recurrence.

Two counterfactuals were also checked:

- replacing `cntSub` with constant zero while leaving `applyMethod` honest
  makes the fixed proof fail in the string case;
- replacing `isStringVal` with constant false makes the target provable by
  eliminating its impossible guard, demonstrating why a clean build alone
  would be insufficient.

The actual candidate passes the string witness and does neither. Its four
definitions are not constant, identity, hard-coded-to-the-equation, or
guard-vacuous on the obligation domain. Detailed analysis and outputs are in
`39_operational_ground_witnesses.txt`,
`41_cntsub_constant_mutation.txt`,
`42_false_recognizer_vacuity_mutation.txt`,
`44_independent_count_oracle.txt`, and
`47_operational_bridge_judgment.md`.

## Judgment

Stage 3 is complete and correctly classified. Stage 4 has authentic producer
provenance, an exact source/obligation bijection, and an unchanged,
mathematically adequate singleton target. Stage 5 cleanly proves that exact
target with fully accounted trust and an honest operational bridge. No issue
found changes the proof claim, classification, target, or legitimacy.

VERDICT: PASS
LEGITIMACY: LEGIT
