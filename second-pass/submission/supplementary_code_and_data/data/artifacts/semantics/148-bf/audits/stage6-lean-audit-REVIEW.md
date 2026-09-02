# Independent Stage 3–5 Audit: HumanEval 148-bf

## Scope and outcome

The launcher and environment both record `CLASSIFICATION_ONLY` for problem
`148-bf`, condition `semantics`, semantics mode `SUPPLIED_SEMANTICS`.
Accordingly, this audit covers the Stage 3 classification and deterministic
Stage 4 generation. Stage 5 proof checks are not applicable. `/candidate` is
absent, and the launcher records null Stage 5 workspace, invocation, and
hashes.

I did not rely on the earlier Stage 2 verdict, Stage 3 rationales, Stage 4
status, or any prior review as authoritative. I reconstructed the rule
inventory from frozen Stage 1 source, reclassified the rules from their
syntax and operational behavior, authenticated the generation-time producer
sources, reran the trusted Stage 4 preflight, and independently checked the
hashes, obligation bijection, and target state.

## Producer-source authentication

Before judging Stage 4, I hashed the mounted producer sources:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Both match `source-manifest.json` and `generator-manifest.json`. The source
bundle contains exactly those two files plus `source-manifest.json`. Its
pipeline tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`.

The generator image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
It agrees between the generator manifest and source manifest, and its digest
is the exact bundle key recorded in the launcher's
`generation_producer_sources` path. Producer authentication therefore passes;
there is no infrastructure `AUDIT_ERROR`.

The complete checks and observed values are in
`evidence/17_stage4_authentication_result.json`.

## Inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. It selected the local verification-module closure
consisting solely of `BF-VERIFICATION`, as selected by the frozen `prove.sh`.
Required MPY semantics are external to the local modules declared in
`verification.k` and therefore are not additional local inventory entries.

The reconstructed results are:

- `verification.k` SHA-256:
  `2d81c776795ccf54f4b0ac4908953c451fe4a5557844b8739cfa4bfb0fbca70f`
- Rule count: 32
- Whole inventory SHA-256:
  `32b8f6680c4da8b95e04a35fe8a501b6b875819997e01433ae305f5d963eeb07`

For every rule, I independently checked that:

1. the reconstructed start/end lines select the exact source text;
2. SHA-256 of the whitespace-normalized source equals
   `normalized_sha256`;
3. `source_rule_id` is exactly `rule-` followed by that normalized hash; and
4. the complete ordered rule document hashes to the reconstructed inventory
   hash.

The Stage 3 manifest has exactly 32 unique IDs in the same order. There are
no missing, extra, duplicated, reordered, or changed identities. Its
inventory hash is identical. The trusted Stage 3 contract reconstructs the
same inventory and enriches it into the same category sets. This is an exact
bijection even though the protected manifest stores the source identity by
`source_rule_id` plus the whole inventory hash rather than duplicating every
source span and text field.

Raw reconstructed rules are in `evidence/05_reconstructed_inventory.json`;
all per-rule span/hash/identity checks are in
`evidence/09_inventory_bijection_result.json`.

## Independent classification judgment

My independent classification is 29 `DEFINITION` entries, three
`OPERATIONAL_RULE` entries, zero `PROVED_DERIVED_LEMMA` entries, and zero
`DOMAIN_LEMMA` entries.

| Frozen spans | Count | Classification | Independent reason |
|---|---:|---|---|
| 9–66 | 3 | `DEFINITION` | `bfBody`, `bfCall`, and `bfRun` are macros or named proof terms. They expand syntax; they do not rewrite an executing configuration to a precomputed result. |
| 71–87 | 2 | `DEFINITION` | `planetVals` names the canonical value sequence and `expectedBetween` defines the postcondition summary through supplied `doSlice` semantics. |
| 95–125 | 24 | `DEFINITION` | The `planetCodes`, `planetPosition`, and `planetExpr` constructor equations define finite representations. They state no independent equality or theorem. |
| 128–161 | 3 | `OPERATIONAL_RULE` | The `#validCases` rules rewrite `<k>`, schedule execution of `Assert(Compare(bfRun(...), ...))`, and advance or terminate the observation loop. |

The three `#validCases` rules form a finite recurrence syntactically, but
classification is by behavior: they are ordinary operational
execution/observation rules because they rewrite the live K configuration and
run the source body under the supplied semantics.

The operational bridge is not hidden in `bfRun`. It expands to a
`Call(closureVal(..., bfBody, 0), ...)`. Supplied call semantics evaluate the
arguments, bind both parameters, create a frame, execute `bfBody`, and perform
the ordinary return/pop transition. `bfBody` is the submitted statement AST,
matching the frozen solution's tuple construction, membership checks, index
calls, comparison, and slice returns. The postcondition's
`expectedBetween` is a definition of the open slice from the same canonical
eight-planet sequence; supplied `doSlice` semantics computes that slice.

Similarly, the observation loop does not assume successful comparisons.
Supplied `Assert` semantics removes a truthy assertion, while a false
assertion sets `AssertionError` and exit code 1, which conflicts with the
Stage 1 claim's terminal state. These are operational checks, not domain
facts.

There is no locally declared claim in `verification.k`, no rule first proved
in a bridge-free module and then reused, and thus no candidate for
`PROVED_DERIVED_LEMMA`. No rule asserts an independent mathematical fact
about the source program or postcondition, so there is no hidden
`DOMAIN_LEMMA`. Some representation definitions are unused by the final
valid-case claim, but being unused does not turn a constructor equation into
a domain lemma.

No inventory rule has a `simplification` attribute. Symbol attributes such as
`function`, `total`, and `macro` are not simplification-rule attributes.
Therefore the simplification classification constraint is satisfied.

The source, supplied operational rules, and all 32 independent decisions are
recorded in `evidence/06_classification_source_review.txt`,
`evidence/08_operational_semantics_core_excerpt.txt`, and
`evidence/41_independent_classification_result.json`.

## Deterministic Stage 4 preflight

I reran:

```text
PYTHONPATH=/reference python -c \
  '... tools.klean_preflight.check_generation(
       /reference/k-proof,
       /reference/lemma-discovery.json,
       /reference/klean-generation,
       toolchain_lock=/reference/klean-toolchain.lock.json) ...'
```

The audit sandbox denies Lean's lookup of `/proc/<pid>/exe`, causing an
unmodified launcher attempt to fail before project inspection with “could not
detect the configuration of the Lake installation.” A readlink trace recorded
`EACCES` for that exact lookup. I compiled the recorded compatibility shim
`evidence/proc_self_exe_compat.c`, which only redirects a numeric
`/proc/<pid>/exe` readlink to `/proc/self/exe`; both designate the current
process executable. The source SHA-256 is
`58393c135814b16597bf17c453fddb5a97e6268eb132404cb386eb79202259fc`.
No project source or checker logic was changed.

With that sandbox compatibility in the inherited environment, the trusted
function returned:

- Status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0
- `lake build`: exit 0
- Built modules: Prelude, Sorts, Inj, Lemmas, Func, Rewrite, and
  `Klean148Bf`
- Obligation count: 0
- Target: null
- Designated sorry count: 0

The exact returned evidence is in
`evidence/18_check_generation_returned_evidence.json`. The unshimmed
sandbox-only failure, readlink trace, shim test, and full successful build
output are preserved in
`evidence/18a_unshimmed_preflight_sandbox_failure.txt`,
`evidence/35_lean_readlink_trace.txt`, and
`evidence/36_lean_compat_test.txt`.

## Hashes, obligation bijection, and target identity

I independently recomputed all launcher-recorded file and tree hashes.
Notably:

- all 763 recorded Stage 1 file paths and SHA-256 values match exactly, with
  no missing or extra files;
- Stage 1 pipeline tree, Stage 1 export tree, selected Stage 2 tree,
  discovery manifest, selected Stage 4 tree, producer tree, and generated
  project tree all match `/audit-input.json`;
- Stage 1, discovery, inventory, verification, generated-tree, obligation-map,
  trust-inventory, and toolchain bindings agree across the input, generator,
  export, source, and launcher manifests; and
- the selected artifact hashes agree with the launcher's resolved hashes.

The independently classified domain set is genuinely empty. It matches,
in exact order:

- `input-manifest.json` `source_rules`: empty;
- `obligation-map.json` `source_rules`: empty;
- generated obligations: empty; and
- trust parameters: empty.

There are no omitted, duplicate, weakened, irrelevant, or vacuous conjuncts
because the source domain-lemma set and generated conjunct set are both
genuinely empty. Both recorded obligation counts are zero.

For an empty obligation set the only valid fixed target is no target. The
expected target definition is null, the generator manifest target is null,
the trusted target extractor returns null, and an independent scan finds zero
`def targetStatement` declarations in the generated Lean sources. Thus Stage
4 did not generate a changed, weakened, duplicated, or vacuous theorem.

All of these checks are recorded in
`evidence/40_stage4_structural_result.json`.

## Stage 5

Stage 5 is correctly absent in `CLASSIFICATION_ONLY` mode. There is no
candidate to copy or build, no `Proof.final`, no target parameters, and no
proof axiom list to reconcile. Performing proof-mode checks would invent a
Stage 5 artifact contrary to the launcher-recorded mode.

## Conclusion

The protected Stage 3 classification exactly matches the independently
reconstructed inventory and the operational meaning of every rule. The true
domain-lemma set is empty. The authenticated deterministic Stage 4 output
faithfully records zero obligations and no target, and all structural,
provenance, hash, and clean-build checks pass. Stage 5 is appropriately
inapplicable.

VERDICT: PASS
LEGITIMACY: LEGIT
