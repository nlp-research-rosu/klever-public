# Independent audit: HumanEval 144-simplify

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. Stage 5 proof
checks are therefore not applicable. `/candidate` is absent, as the launcher
record requires for the selected `KLEAN_NO_OBLIGATIONS` status.

The mounted artifacts are structurally intact and the deterministic Stage 4
project passes the trusted mechanical preflight. The mathematical
classification is nevertheless wrong: the two program-specific loop bridge
rules are not `PROVED_DERIVED_LEMMA`s under the required exact-rule criterion.
They are relevant `DOMAIN_LEMMA`s. Consequently, the true domain set has two
members, while Stage 4 generated zero obligations and no target. The selected
`KLEAN_NO_OBLIGATIONS` result is not legitimate.

## Producer-source and launcher integrity

Before judging Stage 4, I hashed the immutable generation-time producer
sources:

```text
0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b  klean_export.py
0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4  klean.py
```

Those values equal both `generator-manifest.json` and
`generation-tools/source-manifest.json`. Both manifests record generator image
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`.
The basename of the immutable producer-source path recorded in
`/audit-input.json` is the same digest. The producer bundle has exactly the two
producer files and its source manifest; its recomputed tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching the audit input.

I independently recomputed every launcher hash using the trusted hash
algorithms. The Stage 1 pipeline tree, Stage 1 export tree, selected Stage 2
tree, selected Stage 4 tree, generated project tree, discovery manifest, and
producer bundle all match `/audit-input.json`. All 788 individual Stage 1 file
paths and SHA-256 values also match exactly. The detailed values and zero
mismatch counts are in
[`evidence/04_recorded_hashes_and_producers.json`](evidence/04_recorded_hashes_and_producers.json).

## Canonical rule-inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen `/reference/k-proof` workspace and independently rechecked each returned
span against the physical `verification.k` lines. For every rule I recomputed
the whitespace-normalized source hash and `source_rule_id`.

The local verification-module closure is, in source order:

```text
VERIFICATION-SYNTAX
VERIFICATION-BASE
VERIFICATION
```

It contains 21 rules. Every span, text, normalized hash, and rule ID passed the
independent check. The whole canonical inventory hash is:

```text
377ee46b909ba5c403e738ed5881c00cd31e73905dce6f16656b3a11ce90bc86
```

`lemma-discovery.json` contains the same 21 unique IDs, in exactly the same
order, and records the same inventory hash. There are no omissions,
duplicates, extras, reordered identities, changed hashes, or unaccounted
entries. Full reconstructed rule texts and fields are in
[`evidence/02_reconstructed_inventory.json`](evidence/02_reconstructed_inventory.json).

## Independent classification

Nineteen rules are correctly classified as `DEFINITION`:

- Lines 20-112 define the exact loop-body AST, return AST, function-body AST,
  and callee-scope map under named proof terms.
- Lines 114-143 define the base, recursive, and `owise` totalizing equations
  of the named summary predicate `validScan`.
- Lines 145-163 define the terminal and recursive equations of the named
  summary function `scanResult`.

These are structural definitions or summary recurrences, not assertions of an
unproved program property. No inventory rule has a `simplification` attribute,
so the special simplification-category restriction has no additional member
to check.

The last two entries are misclassified:

| Source rule | Span | Recorded | Independent |
|---|---:|---|---|
| `rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543` | 169-200 | `PROVED_DERIVED_LEMMA` | `DOMAIN_LEMMA` |
| `rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650` | 202-232 | `PROVED_DERIVED_LEMMA` | `DOMAIN_LEMMA` |

The supplied semantics makes their role unambiguous. Its `#loop` rules iterate
a `str` one character at a time, bind `ch`, execute the loop body, and continue.
The ordinary semantics then performs name lookup, integer/string comparison,
assignment, the `ord` call, return evaluation, frame popping, and `pyMod`.
Each questioned rule instead rewrites the complete live loop-plus-return call
configuration directly to `scanResult` while deallocating the callee frame.
Thus each is a program-specific operational bridge, neither a named definition
nor an ordinary language execution rule.

The bridges are materially relevant: they summarize the exact loop in
`solution.py`, and their `scanResult` result is the right-hand side of the
top-level reachability postcondition. They are therefore legitimate domain
obligations rather than irrelevant lemmas.

## Exact-rule proof-order check

`prove.sh` does compile `VERIFICATION-BASE` first, prove `loop-spec.k`, then
compile `VERIFICATION` with the bridges and prove the final spec. The compiled
base main module is `VERIFICATION-BASE`, and neither bridge occurs in its KORE;
both occur only in the later full definition. Rerunning all seven Stage 1
specialized claims against the base exits 0 with `#Top`.

That does not satisfy the audit's requirement that Stage 1 first prove the
exact same rule. `loop-spec.k` proves four claims with `P` fixed separately to
0, 1, 2, and 3 for digit heads and three claims with `P` fixed separately to
0, 1, and 2 for slash heads. The admitted rules are single `P`-parametric rules
with range and `validScan` guards. Stage 1 contains no claim equal to either
admitted rule and no machine-checked theorem combining the specialized claims
into those generic rules.

For a direct check, I copied each admitted rule's complete configuration,
rewrite, and guard into a claim, changing `rule` to `claim` and omitting only
the operational `priority(40)` attribute, and ran it against the bridge-free
`verification-base-kompiled` definition. Both exact generic claims exit 1 with
`WarnStuckClaimState`; neither reaches `#Top`. The digit residual retains a
symbolic `P` branch, and the slash residual likewise cannot establish the
generic summary. The exact command artifact is
[`evidence/exact-bridges-spec.k`](evidence/exact-bridges-spec.k), with outputs
in [`evidence/09_exact_generic_bridges_against_base.txt`](evidence/09_exact_generic_bridges_against_base.txt)
and [`evidence/10b_exact_slash_bridge_against_base.txt`](evidence/10b_exact_slash_bridge_against_base.txt).

Accordingly, the independently classified domain set is exactly those two
bridge IDs. The complete 21-entry classification record is in
[`evidence/11_classification_and_stage4.json`](evidence/11_classification_and_stage4.json).

## Trusted Stage 4 preflight and manifest checks

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on the required Stage 1 workspace, discovery manifest, generation, and trusted
toolchain lock. The first attempt exposed an audit-container PID namespace
problem: Lean 4.22 reads `/proc/<getpid>/exe`, but that numeric entry is not
mounted even though `/proc/self/exe` is available. I recorded that failed
attempt, diagnosed it, and used the narrow shim in
[`evidence/proc_self_readlink_shim.c`](evidence/proc_self_readlink_shim.c),
which changes only that equivalent self-executable lookup. No mounted input was
changed.

With that environment repair, the unchanged trusted checker returned:

```text
lake clean: exit 0
lake build: exit 0
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
generated_tree_sha256: 8327a3412fb80a6b3c9d274a4a2c85324bc2feff07846e83ceb28f5f80b2cfdf
```

The complete commands, build output, and returned JSON are in
[`evidence/12_preflight_rerun_with_pid_shim.txt`](evidence/12_preflight_rerun_with_pid_shim.txt).
The successful rerun's command-output hashes exactly equal the recorded
preflight: empty output for `lake clean` and
`0ccb9664976f492a34e107dcb490a43b8f649157582af1115424b02c210b6518`
for `lake build`.

I also independently checked the input-manifest hashes, verification source
hash, discovery hash, inventory hash, generator provenance, obligation-map
hash, export-result bindings, preflight copy in `/audit-input.json`, and target
identity. Every recorded field is internally consistent.

For the recorded Stage 3 classification, the source-rule list and obligation
list are both empty and form a structural bijection. `obligation-map.json`
contains no conjuncts or trust parameters, the generated files contain no
`targetStatement`, and the generator manifest and audit input both fix the
target to `null`. Thus there is no changed, weakened, duplicated, irrelevant,
or vacuous generated conjunct within the recorded empty set.

For the independently correct classification, however, the required
source-rule list is the ordered pair of bridge IDs above. The actual source-rule
list is empty, the actual obligation list is empty, and the target is absent.
Stage 4 therefore omits two relevant obligations and has no target for them.
The fixed-target and obligation bijection fail mathematically even though all
hashes and recorded manifests are self-consistent.

## Stage 5 applicability and final judgment

The launcher mode is `CLASSIFICATION_ONLY`, the selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`, `/candidate` is absent, and both Stage 5 hashes in the
audit input are null. Therefore no candidate clean build, `Proof.final`, axiom
print, or operational-parameter bridge audit applies in this mode.

The absence of Stage 5 cannot rescue Stage 4. The audit instructions require
`KLEAN_NO_OBLIGATIONS` only for a genuinely empty independently classified
domain set and explicitly require `FAIL` / `NOT_LEGIT` for a nonempty true
domain set. Here that set has two members.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
