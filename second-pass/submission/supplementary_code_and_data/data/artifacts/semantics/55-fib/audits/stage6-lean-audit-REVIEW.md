# Independent audit: HumanEval 55-fib

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. I treated the
mounted workspaces, manifests, logs, comments, and earlier review as untrusted
evidence. I did not rely on the selected Stage 2 verdict or the protected Stage
3 classifications for the substantive judgment.

The independent result is that the frozen local verification-module closure
contains six rules, all six are genuinely `DEFINITION` rules, and the true
`DOMAIN_LEMMA` set is empty. The deterministic Stage 4 output therefore
correctly has no obligations, no target declaration, and no Stage 5 proof
candidate.

Raw commands and outputs are indexed in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## Producer-source authentication

I hashed the two generation-time producer files before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

These values exactly match:

- `generator-manifest.json`;
- `/reference/generation-tools/source-manifest.json`; and
- the producer file bindings resolved into `/audit-input.json`.

The immutable generator image ID is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest, source manifest, and the basename of the
launcher-recorded producer-source path. The producer bundle contains exactly
the two producer files and its source manifest. Its recomputed pipeline tree
hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`.

Evidence:
[`01_stage4_producer_authentication_raw.txt`](evidence/01_stage4_producer_authentication_raw.txt)
and
[`33_independent_manifest_and_hash_checks.txt`](evidence/33_independent_manifest_and_hash_checks.txt).
There is no producer-source infrastructure error.

## Rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. `prove.sh` selects `FIB-VERIFICATION`, and the
local closure contains only that module. The reconstructed
`verification.k` SHA-256 is
`306feac40eb38e734ff8a29f5a42735cb7655ad523c50c3cf2e074dd67da90d9`.

The canonical inventory, in source order, is:

| Order | Source span | Normalized SHA-256 / `source_rule_id` | Independent class |
|---:|---:|---|---|
| 1 | 10–21 | `951beb64fbce92e456fcd1184e719112a1dfae8f2920b4e92ea537317f07c8c5` / `rule-951beb64fbce92e456fcd1184e719112a1dfae8f2920b4e92ea537317f07c8c5` | `DEFINITION` |
| 2 | 23–24 | `b493b8e29897cc7c9832cedd71cf42347ac6c23cc41617ee3267d644fcb82fa4` / `rule-b493b8e29897cc7c9832cedd71cf42347ac6c23cc41617ee3267d644fcb82fa4` | `DEFINITION` |
| 3 | 26–27 | `3c19c1ace444c19fcd0440bc740ffbe7c0b8d126b80d72d81a12abde7a68205c` / `rule-3c19c1ace444c19fcd0440bc740ffbe7c0b8d126b80d72d81a12abde7a68205c` | `DEFINITION` |
| 4 | 34–35 | `0cfc2191eeac25cc4298d7ecca5a92d3f57f7715af391c09d3156408ff6479f1` / `rule-0cfc2191eeac25cc4298d7ecca5a92d3f57f7715af391c09d3156408ff6479f1` | `DEFINITION` |
| 5 | 37–39 | `8386dc93afab6158fba2ead31c4b2fbee2813be9182a6f184fca09c3dd0f7026` / `rule-8386dc93afab6158fba2ead31c4b2fbee2813be9182a6f184fca09c3dd0f7026` | `DEFINITION` |
| 6 | 41 | `aefa2ce110bb5a36b28fe6339c0379ad6d3bccd04b6da20c57f6208b69da53ee` / `rule-aefa2ce110bb5a36b28fe6339c0379ad6d3bccd04b6da20c57f6208b69da53ee` | `DEFINITION` |

For every entry I independently extracted the recorded source span, normalized
it with whitespace joining, recomputed SHA-256, and checked that
`source_rule_id` is `rule-` followed by that digest. The whole ordered
inventory hash recomputes to
`77a34be1066a3b4fb0f3b4eff8c5199ec1606c7cc2b8823a18c6c1ed4ff9c111`.

The protected Stage 3 manifest has exactly six unique entries. Its ordered ID
list equals the reconstructed ordered list, its set equals the reconstructed
set, and its whole-inventory hash matches. There are no omissions, duplicates,
extra rules, reordered identities, changed hashes, or unaccounted
classifications.

Evidence:
[`03_reconstructed_rule_inventory.json`](evidence/03_reconstructed_rule_inventory.json),
[`06_stage3_trust_boundary_result.json`](evidence/06_stage3_trust_boundary_result.json),
and
[`07_stage3_bijection_and_hash_checks.txt`](evidence/07_stage3_bijection_and_hash_checks.txt).

## Independent classification judgment

1. `fibBody => ...` is a `DEFINITION`. It expands a fresh, named proof term
   into the translated source body: docstring expression; initialization of
   `a`, `b`, and `_`; `for _ in range(n)`; simultaneous `(a,b) = (b,a+b)`;
   and `return a`. It does not rewrite a running `<k>` configuration or replace
   any operational construct.

2. `fibClosure => closureVal(("n", .ParamNames), fibBody, 0)` is a
   `DEFINITION`. It names the closure value that the supplied `FuncDef`
   operational rule creates in module environment 0. It does not intercept
   function definition or call execution.

3. `fibProgram => Module(FuncDef("fib", Params("n"), fibBody))` is a
   `DEFINITION`. It names the exact translated module term. The supplied
   `#loadAll` and `FuncDef` rules still execute that term.

4. `fibRun(A, _, I, N) => A requires I >=Int N` is the terminating equation
   of a new summary function and is a `DEFINITION`.

5. `fibRun(A, B, I, N) => fibRun(B, A +Int B, I +Int 1, N) requires I <Int N`
   is the recursive equation of that new summary and is a `DEFINITION`.
   “Recurrence” is expressly within the definition category; this rule does
   not assert a theorem between pre-existing symbols.

6. `fibSpec(N) => fibRun(0, 1, 0, N)` is a `DEFINITION` of the named
   postcondition summary.

The two `fibRun` guards are disjoint and exhaustive over integers. The
recursive branch increments `I`, so it reaches the base branch whenever
`I < N`. More importantly, the recurrence is operationally relevant and
matches the frozen program exactly:

- supplied `range(n)` semantics produces `rangeObj(0, N, 1)`;
- one range iteration advances `I` to `I + 1`;
- tuple-expression evaluation followed by unpacking updates the state from
  `(A, B)` to `(B, A + B)`; and
- exhausted iteration leaves `A`, which the source returns.

The circular loop claim uses precisely
`fibRun(A, B, I, N)`, and the all-natural claim initializes it as
`fibRun(0, 1, 0, N)` through `fibSpec`. Thus the summaries describe the source
program and postcondition rather than introducing an unrelated fact.

No local rule has an operational configuration or operational constructor as
its left-hand side. Therefore there are no `OPERATIONAL_RULE` entries. No rule
is claimed to be a `PROVED_DERIVED_LEMMA`, so there is no proof-order claim to
validate. No rule states an extra mathematical fact about an existing symbol,
so the true `DOMAIN_LEMMA` set is empty. All six rules have an empty attribute
list; there are no `simplification` rules, and the simplification-class
restriction is satisfied vacuously.

The relevant operational rules and the complete local symbol-use search are
preserved in
[`05_semantic_execution_path_full.txt`](evidence/05_semantic_execution_path_full.txt)
and
[`36_local_symbol_usage_and_bridge_check.txt`](evidence/36_local_symbol_usage_and_bridge_check.txt).

## Stage 4 deterministic generation and manifest bijection

The authenticated generation-time exporter deterministically constructs its
eligible source-rule list only from `validated["domain_lemmas"]`. It requires
the generated obligation IDs to equal that ordered source-rule list, enriches
each obligation with the exact source span and provenance hashes, and emits no
`targetStatement` when the obligation list is empty.

For this task, the independently derived relation is:

`DOMAIN_LEMMA source rules ∅` ↔ `generated obligations ∅`.

The following objects all contain the same empty set/list:

- reconstructed `domain_lemmas`;
- `input-manifest.json` `source_rules`;
- `obligation-map.json` `source_rules`;
- `obligation-map.json` `obligations`; and
- `obligation-map.json` `trust_parameters`.

The obligation-map file SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. There can be no omitted, duplicated,
weakened, irrelevant, or vacuous conjunct within an empty obligation list.
Crucially, the exporter did not turn emptiness into a vacuous `True` theorem:
`Klean55Fib/Lemmas.lean` contains no `targetStatement`, and the trusted target
parser returns `None`.

Target identity is consistently null in:

- `/audit-input.json`;
- `generator-manifest.json`;
- the selected `preflight.json`;
- the fresh preflight result; and
- independent inspection of the generated Lean tree.

The generated project tree digest recomputes to
`14d0abca5e098db9ea00d1da35f08d7335eede6ab553e11f33b79c0c83aae800`.
The Stage 1 export digest is
`0eb13358c67d466930b2530a91712a0b902e70f8880e306e38da61ca84ff64ac`.
Both match every relevant manifest and launcher field. I also recomputed the
launcher-recorded pipeline tree hashes for Stage 1, Stage 2, Stage 4, and the
producer bundle, as well as all 34 Stage 1 per-file hashes; all match. The
signed resolution digest recomputes to
`68c939c0b4b75c5689e2d8e7e3ddb20745f1f3428cfeb6f30b641ff60d18ba26`.

Evidence:
[`28_stage4_sidecars_and_target_search.txt`](evidence/28_stage4_sidecars_and_target_search.txt),
[`29_generated_target_files.txt`](evidence/29_generated_target_files.txt),
[`33_independent_manifest_and_hash_checks.txt`](evidence/33_independent_manifest_and_hash_checks.txt),
and
[`35_generation_producer_relevant_source.txt`](evidence/35_generation_producer_relevant_source.txt).

## Fresh preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, `/reference/k-proof`,
`/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the trusted toolchain lock.

The audit sandbox initially prevented Lean from locating itself: Lean 4.22's
`IO.appPath` reads `/proc/<getpid()>/exe`, but this sandbox reports namespace
PID 2 while exposing host PIDs in `/proc`. I preserved both failed attempts.
I then used the narrow shim in
[`evidence/lean_proc_exe_shim.c`](evidence/lean_proc_exe_shim.c), which changes
only numeric `/proc/<pid>/exe` `readlink` calls to `/proc/self/exe`. This
restores the intended executable lookup and does not modify the frozen input,
generated project, compiler, theorem, or manifests.

The fresh trusted check then returned:

- `status: KLEAN_NO_OBLIGATIONS`;
- `obligation_count: 0`;
- `target: null`;
- `lake clean` exit 0;
- `lake build` exit 0;
- no generated `sorry`; and
- 49 generated computational trust declarations, exactly matching
  `trust-inventory.json`.

The preflight independently forbids proposition-valued trust. The 49
allowlisted declarations are generated computational scaffolding; there is no
target proposition or proof in this mode.

Exact returned evidence is
[`27_fresh_check_generation_result.json`](evidence/27_fresh_check_generation_result.json).
The sandbox diagnosis and shim build are in evidence files 10–26.

## Stage 5

Stage 5 is inapplicable. `AUDIT_MODE` and `/audit-input.json` both say
`CLASSIFICATION_ONLY`; the true domain set is empty; the generated target is
absent; all Stage 5 paths/results are null; and `/candidate` does not exist.
Consequently no candidate clean build, `#print axioms Proof.final`, target
parameter bridge audit, or candidate forbidden-token scan is required or
permitted by this mode.

VERDICT: PASS
LEGITIMACY: LEGIT
