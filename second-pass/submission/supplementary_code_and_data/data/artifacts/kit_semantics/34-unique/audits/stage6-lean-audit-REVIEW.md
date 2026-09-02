# Independent audit: HumanEval `34-unique`

Audit mode: `CLASSIFICATION_ONLY`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Scope and result

I independently audited the protected Stage 3 classification and selected
deterministic Stage 4 generation. Stage 5 is not present or applicable in the
launcher-recorded mode. I did not rely on the prior K review's verdict,
candidate comments, or recorded PASS statements. I used the frozen K sources,
the trusted rule-inventory and preflight code, and independent source-level
mathematical analysis.

The classification is correct. The local verification closure has nine
definitions, two genuinely proved derived lemmas, no ordinary operational
rules, and no domain lemmas. Therefore the Stage 4 status
`KLEAN_NO_OBLIGATIONS` is legitimate: the domain set is genuinely empty, the
obligation set is empty, and the fixed generated target is absent.

## Producer-source and immutable-input authentication

Before judging Stage 4, I hashed the mounted generation-time producer sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Each value matches both `source-manifest.json` and
`generator-manifest.json`. The immutable generator image is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in all three bindings: the final path component recorded by
`/audit-input.json`, `source-manifest.json`, and the generator manifest's
provenance. The producer-source tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly the launcher-recorded value. There is no producer-source
infrastructure error. Raw comparisons are in
[`evidence/02_producer_authentication.log`](evidence/02_producer_authentication.log).

I also recomputed every aggregate hash that can be resolved against the mounted
inputs:

| Binding | Recomputed value | Result |
|---|---|---|
| Stage 1 artifact | `c934348a7c09128729896d485dd2aec4cf38fedd8dd26389d3bc57a7436ab264` | match |
| Stage 2 audit artifact | `a006b58f8df26f247026f0af65350c77b82ec42a3a473f758230e7aee9a91036` | match |
| Stage 4 generation artifact | `7c52673397bc17a3b14b31dbe31b00daec1ce5955730a37020e19df1d9f2093d` | match |
| Frozen Stage 1 export | `40e50ba05908a86ec3ae6dcf277f4ed6d140928c2f27ea8a9a6902d8a37ec1ee` | match |
| Protected discovery manifest | `4a1f4b7f8a6984e659ec78a12e9bfec0aaa72fd60ba1d520779a2abf1b1195ee` | match |
| Generated tree | `0c49e07568500e130f4f3762b989e1e518549e3c50a47418237491d95794be01` | match |

All 843 launcher-recorded Stage 1 relative paths exist, there are no extra
files, and every per-file SHA-256 matches. See
[`evidence/05_hash_and_manifest_checks.log`](evidence/05_hash_and_manifest_checks.log)
and its reproducible checker
[`evidence/09_independent_checks.py`](evidence/09_independent_checks.py).

## Inventory reconstruction and Stage 3 bijection

I ran `tools.k_rule_inventory.inventory_verification` from the trusted
`/reference/tools` implementation on `/reference/k-proof`. It selected
`VERIFICATION` and reconstructed its local import closure in source order:

1. `VERIFICATION-BASE`
2. `VERIFICATION-MEMBER`
3. `VERIFICATION`

The reconstruction contains exactly 11 rules. It recomputed every source span,
normalized source hash, and `source_rule_id`. The whole canonical inventory
hash is
`36c8f6930fe11a0ef65a3e4475e90f089611977614efad399cb53f17c8cfdc3d`.

The comparison with `/reference/lemma-discovery.json` is bijective and ordered:

- inventory entries: 11;
- discovery entries: 11;
- duplicates on either side: 0;
- missing identities: none;
- extra identities: none;
- ordered identity sequence: exact match; and
- recorded versus recomputed inventory hash: exact match.

The complete reconstructed spans, texts, attributes, and hashes are in
[`evidence/03_inventory_reconstruction.log`](evidence/03_inventory_reconstruction.log).

## Independent classification judgment

### Nine definitions

The nine rules in `VERIFICATION-BASE` are all `DEFINITION`:

- `memberVS` has the empty, unequal-head recursive, and equal-head cases. It is
  a named structural summary of the supplied semantics' `#memberAcc` fold. The
  two guards cover the equal/unequal head cases, and recursion decreases the
  remaining sequence.
- `appendUnique` has complementary present/absent branches. The absent branch
  appends one value with `valSeqConcat`; the present branch preserves the
  accumulator.
- `dedupFromVS` has the empty base case and a structurally decreasing recurrence
  that threads `appendUnique` through the remaining source sequence.
- `lastFromVS` has the empty base case and a structurally decreasing recurrence
  that records the latest loop-target value.

These rules define summaries and recurrences; none asserts a human-facing
property as a theorem. The only `[simplification]` rules are the two guarded
`memberVS` defining equations, so every simplification is a `DEFINITION` as
required.

This interpretation agrees with the frozen operational semantics, not merely
with the comments. List iteration yields one head and remainder at a time
(`semantics/list.k:9-10`); membership performs the `#memberAcc` fold using
`==K` (`list.k:57-67`); the `for` loop binds the target, executes the body, and
continues over the remainder (`controls.k:62-75`); and `append` performs the
exact in-place heap update (`list.k:52-55`). The source program initializes an
empty result, appends `x` only when `x not in result`, and leaves the final
loop target in `x`. Thus the four named summaries have the frozen operational
meaning claimed above.

### Two proved derived lemmas

The rules in `VERIFICATION-MEMBER` and `VERIFICATION` look operational, so I
required the stronger `PROVED_DERIVED_LEMMA` criterion rather than accepting
their names or rationales.

For `rule-968e...`, the normalized body of `verification.k:41-43` is exactly
the body of `MEMBER-SPEC.member-summary` at `spec.k:8-10`, including the
arbitrary continuation. The earlier proof definition has main module
`VERIFICATION-BASE`; its local closure excludes the rule in
`VERIFICATION-MEMBER`. I independently reran:

```text
kprove spec.k --definition verification-base-kompiled --spec-module MEMBER-SPEC
```

It exited 0 with `#Top`.

For `rule-e256...`, the normalized body of `verification.k:52-75` is exactly
the body of `LOOP-SPEC.unique-loop` at `spec.k:18-40`. Identity includes the
complete source loop, arbitrary continuation, environment, local-scope
bindings and `x` update, and accumulator heap update. The earlier proof
definition has main module `VERIFICATION-MEMBER`; its local closure includes
the already-proved membership rule but excludes this rule in `VERIFICATION`.
I independently reran:

```text
kprove spec.k --definition verification-member-kompiled --spec-module LOOP-SPEC
```

It exited 0 with `#Top`. Only afterward does the final proof layer use main
module `VERIFICATION`, whose closure contains both derived rules. Exact-body
hashes, module layering, complete outputs, and warnings are recorded in
[`evidence/04_derived_lemma_reproof.log`](evidence/04_derived_lemma_reproof.log).

These two rules are exact machine-proved execution summaries, not unproved
ordinary operational rules and not disguised domain lemmas. The resulting
independent counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 9 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 2 |
| `DOMAIN_LEMMA` | 0 |

The rule-by-rule reasoning is in
[`evidence/08_classification_judgment.md`](evidence/08_classification_judgment.md).

## Stage 4 manifest and obligation bijection

The Stage 4 input manifest partitions the same 11 source rules as nine
definitions, zero operational rules, two proved derived lemmas, and zero
source/domain rules. Across those sections:

- there are no duplicates;
- the union is exactly the reconstructed inventory;
- the sequence agrees with source order; and
- every span, normalized hash, ID, attribute, source text, classification, and
  rationale agrees with the reconstructed inventory and protected Stage 3
  record.

The independently determined domain set is empty. The obligation map has zero
obligations, zero `source_rules`, and zero trust parameters. Therefore the
source-rule/obligation correspondence is the unique empty bijection. There are
no omitted, duplicated, irrelevant, weakened, or vacuous conjuncts because no
domain proposition exists to export.

Target identity is also exact for the no-obligation case:

- `generator-manifest.json`: `target: null`;
- `/audit-input.json`: `target: null`;
- trusted `klean_export.target_statement` on the generated tree: `None`;
- generated root module: imports only, with no theorem declaration; and
- `/candidate`: absent.

Thus no generated target was introduced, changed, shadowed, or weakened, and
the absence of Stage 5 is the required state for `KLEAN_NO_OBLIGATIONS`.

## Required Stage 4 preflight

I called `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the frozen Stage 1 workspace, protected Stage 3 discovery manifest, selected
Stage 4 generation, and trusted toolchain lock.

The first invocation reached the isolated build but Lake could not locate its
installation because this audit runner's PID namespace reports PID 2 while
`/proc/2/exe` is absent. I diagnosed and repaired only that environment lookup
with a recorded `LD_PRELOAD` shim that redirects numeric
`/proc/<pid>/exe` reads to `/proc/self/exe`. The shim does not alter source,
imports, declarations, theorem statements, elaboration, or kernel checking.
The failed invocation and exact error are preserved in
[`evidence/06_preflight_initial_failure.log`](evidence/06_preflight_initial_failure.log);
the shim source and toolchain identity check are in
[`evidence/01_proc_self_shim.c`](evidence/01_proc_self_shim.c) and
[`evidence/00_environment_and_mode.log`](evidence/00_environment_and_mode.log).

The corrected required invocation exited 0 and returned:

- status: `KLEAN_NO_OBLIGATIONS`;
- frozen/Stage 1 hash:
  `40e50ba05908a86ec3ae6dcf277f4ed6d140928c2f27ea8a9a6902d8a37ec1ee`;
- Stage 3 hash:
  `4a1f4b7f8a6984e659ec78a12e9bfec0aaa72fd60ba1d520779a2abf1b1195ee`;
- generated tree hash:
  `0c49e07568500e130f4f3762b989e1e518549e3c50a47418237491d95794be01`;
- obligation count: 0;
- target: null;
- designated sorry count: 0;
- trust declaration count: 41;
- isolated `lake clean`: exit 0, empty output; and
- isolated `lake build`: exit 0, output hash
  `8f631287bf43043db805c7d1d68d0dd4452a64137b90eaffa24a7dccaee64165`,
  ending in `Build completed successfully.`

This exactly reproduces the recorded Stage 4 preflight evidence. The complete
returned document is
[`evidence/07_preflight_result.json`](evidence/07_preflight_result.json).

## Stage 5 applicability

`AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`.
`lean_invocation_sha256`, `lean_workspace_sha256`, and `stage5_result` are
null, and `/candidate` is absent. Because the independently verified domain
set is empty, this is the only legitimate configuration: there must be no
generated target and no Stage 5 proof candidate. The proof-mode clean build,
`#print axioms Proof.final`, candidate trust scan, theorem identity check, and
parameter operational-bridge audit therefore do not apply.

## Conclusion

Stage 3 accounts for every rule in the frozen local verification closure in
the correct order and with correct classifications. Both execution-summary
rewrites meet the strict proved-derived-lemma criterion; neither imports
itself into its prerequisite proof. No domain lemma is hidden among the
definitions or simplifications. Stage 4 is authenticated to the immutable
producer image and sources, all recorded hashes and manifests agree, and the
empty obligation/target state exactly matches the genuinely empty domain set.

VERDICT: PASS
LEGITIMACY: LEGIT
