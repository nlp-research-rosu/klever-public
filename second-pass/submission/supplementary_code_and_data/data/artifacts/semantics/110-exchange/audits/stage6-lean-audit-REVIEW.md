# Independent audit: HumanEval 110-exchange

## Scope and result

I audited condition `semantics` in `SUPPLIED_SEMANTICS` mode. Both
`AUDIT_MODE` and the signed `/audit-input.json` select
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate`, the Stage 5 result, the Lean workspace,
and the Lean invocation are all absent/null.

I did not rely on the selected Stage 2 verdict, prior reviews, comments, or
logs as authority. I reconstructed the Stage 3 inventory from frozen source,
classified every rule against the supplied operational semantics and source
program, and independently reconciled the Stage 4 artifacts.

## Input and producer integrity

The signed audit-input contract verifies. Its canonical resolution digest
recomputes to
`550799cc4b4ba2f93c18ebfa4f051b7bd09fadd869f8f3a6bfb226954dab90a3`,
exactly the recorded value.

All launcher-recorded non-null hashes recompute exactly:

- Stage 1 mounted tree:
  `6176408af13f17096b223a03527bc9811fb3c56d25a1ceb4ae21d7fc3d97d837`
- Stage 1 deterministic export tree:
  `3370acdea8d0c594dbef8578cfc1426a9d77cd503d953838bae8c49bc31dbdca`
- all 35 Stage 1 per-file source hashes: exact, with no missing, extra, or
  mismatched entry
- selected Stage 2 tree:
  `307b6ed87dc5bc4e1dc2ad5cb5e93175ceaee471bd108df435162f3180a98c9e`
- Stage 3 manifest:
  `0613373deb260cba14df9e940f9ecd8364dffac7b49c3f4925b970136a4a0ef8`
- selected Stage 4 tree:
  `59f776aa5896ba468930faa49aef46a90ebf1c2194d95083a53fe0aa731dfb1b`
- generated Lean tree:
  `41268b3e75eedc21db6588eb7801dec0de0cc72aa12025487b7fce7ef7afd553`
- mounted producer-source tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`

The mandatory producer gate passes:

- `/reference/generation-tools/klean_export.py` hashes to
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`.
- `/reference/generation-tools/klean.py` hashes to
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`.
- Those values agree independently with `generator-manifest.json` and
  `source-manifest.json`.
- Both manifests record generator image
  `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
  the launcher-recorded producer-source path binds the same image ID.

The generator manifest also exactly matches the pinned toolchain lock. Its
Stage 1, Stage 3, inventory, generated-tree, and obligation-map hashes all
recompute. The export result's Stage 1, Stage 3, generated-tree, and
trust-inventory hashes also recompute. Evidence:
`09_generator_producer_provenance.txt`,
`38_all_recorded_input_hashes.txt`, and
`43_stage4_sidecar_hash_reconciliation.txt`.

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` code on the
read-only Stage 1 workspace selected module `EXCHANGE-VERIFICATION`. Its local
module closure is exactly that one module; its import `MPY` is supplied
externally and is not another local module in `verification.k`.

The reconstruction found 13 rules in frozen source order. For every entry I
recomputed:

- module and exact start/end source lines;
- normalized source text hash;
- `source_rule_id = "rule-" + normalized_sha256`; and
- the canonical whole-inventory hash.

Every per-rule recomputation succeeded. The inventory hash is
`abf5939fc8aa355bb81970ac2b1d2d6f440f70116c4662dbba6c00549cef528b`.
The Stage 3 manifest has exactly 13 unique IDs in the same order. The sets and
ordered lists are equal; there are no omissions, extras, duplicates, reordered
identities, or changed hashes. The trusted Stage 3 contract validator also
passes. Evidence: `04_reconstructed_rule_inventory.txt` and
`08b_inventory_bijection_and_contract_rerun.txt`.

## Independent classification

My independent classification agrees with Stage 3: 2
`OPERATIONAL_RULE`s, 11 `DEFINITION`s, no
`PROVED_DERIVED_LEMMA`, and no `DOMAIN_LEMMA`. None of the 13 rules has a
`simplification` attribute.

### Operational rules

The two rules at `verification.k` lines 10–12 are ordinary empty/nonempty
`#iterNext` transitions for the typed symbolic representation
`list(intVals(IntSeq))`. Empty produces `#iterDone`; nonempty yields the
integer head and retains the tail iterator. Both preserve the continuation
and frame every other cell.

These transitions match the supplied `MPY-LIST` iterator rules in
`reference-semantics/semantics/list.k` constructor for constructor:
`.ValSeq` produces done, while `vCons(V,R)` produces `#iterYield(V,list(R))`.
They define execution of a symbolic integer-list view. They do not assert a
mathematical fact, change the source body, discard a continuation, or abstract
an observable state effect. `OPERATIONAL_RULE` is therefore the correct
classification.

### Definitions

Six rules are base/recursive equations for `oddAcc` and `evenAcc`. On the
fixed positive divisor 2, supplied `pyMod` implements Python modulo; the
zero/nonzero guards are disjoint and exhaustive, and recursion strictly
descends from `iCons(I,R)` to `R`. These rules define exactly the accumulator
updates performed by the two source loops.

Two rules define `exchangeResult`: `YES` when
`oddAcc(0,lst1) <= evenAcc(0,lst2)`, and `NO` under the complementary `>`
guard. This is the source program's exact return test. It is also the intended
HumanEval property: every odd element in `lst1` needs one even element from
`lst2`; unlimited exchanges are possible exactly when the latter count is at
least the former.

The remaining three rules define the named macros `ODD-BODY`, `EVEN-BODY`,
and `exchangeDef`. Expanding the two body macros in `exchangeDef` gives the
exact frozen `solution.mpy` constructor sequence: the same three
initializations, loops over `lst1` and `lst2`, parity tests, increments,
`odd <= even` return of `YES`, and final `NO`.

All 11 rules therefore define summaries, recurrences, macros, or named proof
terms as required for `DEFINITION`. None is a domain fact disguised as a
definition. Conversely, no rule is a separately proved theorem that Stage 1
first establishes without the rule and only later uses, so the derived-lemma
set is correctly empty. Detailed per-rule reasoning is in
`42_independent_classification.md`; the relevant frozen sources and supplied
semantics excerpts are in `02_inventory_tool_and_frozen_sources.txt`,
`06_operational_semantics_excerpts.txt`, and
`07_source_translation_and_relevant_semantics.txt`.

The true domain-lemma set is therefore genuinely empty. This is a semantic
judgment about the frozen program, not an inference from Stage 4's recorded
status.

## Deterministic Stage 4 and obligation bijection

I reran exactly
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
`/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the trusted toolchain lock.

The first attempt exposed an audit-container infrastructure issue: Lean's
runtime asks `readlink("/proc/<getpid>/exe")`, while this command sandbox's
`/proc` exposes a different PID namespace, so the lookup returned `ENOENT`.
The syscall-level reproduction is saved in
`34_lean_readlink_syscall_probe.txt`. I recovered without changing any pinned
binary or generated source by preloading a narrow shim that only returns the
current process's actual invocation path when that specific `/proc/*/exe`
lookup fails with `ENOENT`. The shim source/hash and successful version probe
are in `35_proc_namespace_repair_probe.txt`. I also supplied the pinned
toolchain's `LEAN_SYSROOT`/`LAKE_HOME`; the exact Lean and Lake binaries still
report Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The recovered trusted preflight completed both `lake clean` and `lake build`
with exit code 0 and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1 hash
  `3370acdea8d0c594dbef8578cfc1426a9d77cd503d953838bae8c49bc31dbdca`;
- Stage 3 hash
  `0613373deb260cba14df9e940f9ecd8364dffac7b49c3f4925b970136a4a0ef8`;
- generated-tree hash
  `41268b3e75eedc21db6588eb7801dec0de0cc72aa12025487b7fce7ef7afd553`;
- zero obligations;
- null target;
- 48 generated trust declarations; and
- zero designated sorries.

The complete returned evidence is
`36_rerun_klean_preflight_final.txt`.

I separately reconstructed the Stage 4 mapping instead of treating preflight
as the mathematical verdict:

- `input-manifest.json`'s 11 definitions, 2 operational rules, and 0 derived
  lemmas are exact record-for-record matches to the independently validated
  Stage 3 inventory partitions.
- The independently classified domain source-rule list is empty.
- Both `input-manifest.json.source_rules` and
  `obligation-map.json.source_rules` equal that empty list.
- `obligation-map.json.obligations` and `trust_parameters` are empty.
- Thus the ordered source-rule/obligation identity lists are bijective
  (`[] = []`), with no omission, duplicate, extra, irrelevant, weakened, or
  vacuous conjunct.
- The obligation-map file hashes to
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly the generator manifest value.

Evidence: `39_generated_project_and_obligation_artifacts.txt` and
`41_independent_stage4_bijection_and_target.txt`.

## Fixed target and Stage 5

Because the true domain set is empty, Stage 4 must not create a theorem target.
Independent target parsing returns `None`. The generator manifest, recorded
preflight, signed audit input, and rerun preflight all record a null target;
the export result agrees on `KLEAN_NO_OBLIGATIONS` and count zero. There is
consequently no generated theorem that could have been weakened, duplicated,
or made vacuous.

`/candidate` does not exist, and the signed Stage 5 result, Lean workspace,
Lean invocation, and their hashes are null. That is exactly the required
classification-only/no-obligations state. Clean candidate builds,
`#print axioms Proof.final`, proof identity, and operational-bridge parameter
checks are not applicable because there is no target and no Stage 5 proof.

## Judgment

The Stage 3 manifest is a complete, ordered, hash-exact classification of the
frozen local rule closure. Its categories are mathematically and
operationally correct. The true domain-lemma set is empty. Stage 4 has valid
producer provenance, exact input/output hashes, an exact empty
source-rule/obligation bijection, no generated target, and a successful fresh
preflight build. The absence of Stage 5 is required and correct.

VERDICT: PASS
LEGITIMACY: LEGIT
