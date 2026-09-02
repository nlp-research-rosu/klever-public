# Independent audit: HumanEval 133-sum-squares

## Decision

The protected Stage 3 classification is correct, the selected deterministic
Stage 4 generation is structurally and mathematically consistent with the
frozen program, and `KLEAN_NO_OBLIGATIONS` is the correct status. The launcher
mode is `CLASSIFICATION_ONLY`, so Stage 5 is intentionally absent and no Lean
proof verdict is applicable.

This decision does not rely on the prior K review, old PASS/CONCERNS markers,
candidate comments, or generation logs as authority. The inventory,
classifications, hashes, domain set, obligation bijection, and target status
were recomputed from the frozen inputs.

## 1. Launcher mode and input integrity

Both `AUDIT_MODE` and `/audit-input.json` say `CLASSIFICATION_ONLY` for problem
`133-sum-squares`, condition `bare`, semantics mode
`GENERATED_SEMANTICS`. The launcher’s canonical resolution-object SHA-256
recomputes to
`52f77b36d91bf9f30f5b8f1450c37dbfae91e3dfb66e56957f3ead50edcde687`,
exactly the recorded `resolved_input_sha256`.

The two Stage 1 tree encodings both match their recorded values:

- pipeline tree:
  `c55d53506754749ffbf456d12fe4bc4003d7174b03ab366dd7058330b802304f`;
- deterministic Klean export tree:
  `3f7d23059ff4f4933a714e64768da9477df71124794c533c8ced9e7a4bf5017b`.

All eight recorded Stage 1 per-file hashes match. The other recomputed
launcher hashes also match:

- selected Stage 2 audit tree:
  `f5a4a01ccf82c1c2fb2d3221e5ae2ab1e479f4dd6cd02ba9ca9f53e367f71b20`;
- Stage 3 manifest:
  `2f3d7ae008c08299b6ea11e84b94ce6c038c9ab660ea89a65d6715be15c0a980`;
- Stage 4 generation tree:
  `7208b3ae4cd15fe8be3ffcd84e114fb14a0629514248491bfd71993b93129071`;
- generated Lean project tree:
  `d3403d983e0d86b3d12033a15feab2a698affc86ec3e3c1d6cddbc821e47d2e7`;
- producer-source bundle tree:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`.

The Lean invocation and workspace hashes are null, as required in
classification-only mode.

The launcher-recorded mechanical checker lock SHA-256,
`5bb56dc3b85793d8528e3eae842a7345c1fde1df86149695f26c6015396f521d`,
matches `/opt/humaneval/data/klean-audit-tools.lock.json`. Every one of its
eight file entries independently hashes to the exact mounted
`/reference/tools` file named by the lock. The pinned toolchain lock is
byte-identical between `/opt/humaneval/data/klean-toolchain.lock.json` and
`/reference/klean-toolchain.lock.json`, with SHA-256
`a3dc0270ff7cab64550e91f605d8f2b5f6076b75f4ec49629a0e13894455fa9f`.
The frozen-toolchain check reports K 7.1.293, pyk/Klean 7.1.293, Lean 4.22.0,
and Codex 0.144.6.

Evidence: `evidence/34_recompute_integrity.log`,
`evidence/83_resolved_input_hash_recompute.txt`, and
`evidence/98_independent_stage3_stage4_full.log`,
`evidence/105_frozen_toolchain_checker_run_with_compat.txt`, and
`evidence/112_mechanical_checker_lock_hash.txt` through
`evidence/114_mechanical_checker_bundle_verification.txt`.

## 2. Stage 4 producer provenance gate

This gate was checked before judging the generated output.

| Producer | Mounted SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same |

These hashes agree exactly among the mounted files,
`generation-tools/source-manifest.json`, and
`klean-generation/generator-manifest.json`. Both manifests record immutable
generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The launcher binds the same image through the terminal component of
`resolution.generation_producer_sources`, and its recorded bundle-tree hash
also matches. The producer bundle contains exactly the two producer files and
its source manifest.

No producer-source infrastructure error exists.

Evidence: `evidence/08_critical_file_hashes.txt`,
`evidence/09_generation_source_manifest.txt`,
`evidence/10_generator_manifest.txt`, and
`evidence/98_independent_stage3_stage4_full.log`.

## 3. Canonical rule-inventory reconstruction

The trusted `tools.k_rule_inventory.inventory_verification` selected module
`VERIFICATION`. Its local import closure inside frozen `verification.k` is
only `VERIFICATION`; `MPY` is supplied by required `semantic.k`, not another
module declared in `verification.k`.

The frozen `verification.k` SHA-256 is
`bca993294d4ff15ac1df81472bbb05c3c0e07f5b53cb619884c7999cd3aeaad9`.
The trusted inventory found exactly four rules. I separately sliced the same
physical source spans, normalized each as whitespace-separated source, and
recomputed both the per-rule digests and the canonical JSON inventory digest.
The independent result is byte-for-byte equal to the trusted inventory.

| Span | `source_rule_id` / normalized SHA-256 | Source |
|---|---|---|
| 10 | `rule-67fd8c59e2fc35ff2a07fcdaea7d2aaa6c4dd53810a8021d8483da75bed7a064` | `squareCeil(V) => ceilInt(V) *Int ceilInt(V)` |
| 12 | `rule-cd47a694aad7fc4cff62a687eed4d4986a504a21721343a11f8b34e034f4469d` | `sumSquares(VS) => sumSquaresFrom(0, VS)` |
| 13 | `rule-8ee4a875ab908dea4a779e52ac8c31348b0cdb6ade1b0e853b193ef30dd1e744` | `sumSquaresFrom(A, nil) => A` |
| 14–15 | `rule-b3c5d69397360a5ef5baa35f89507bff4187d6261cfa6ab5c7cc1583f460484b` | `sumSquaresFrom(A, cons(V, VS)) => sumSquaresFrom(A +Int squareCeil(V), VS)` |

The whole inventory SHA-256 is
`466fc13b9de0e11b43c4e7f406c3d0e75585b799ee989944d663341a2b6c91ad`.

The Stage 3 manifest lists these same four identities in the same order. They
are unique, with no omission, duplication, extra identity, changed source
span, changed normalized hash, or changed whole-inventory hash.

Evidence: `evidence/15_verification_k_numbered.txt`,
`evidence/34_recompute_integrity.log`, and
`evidence/98_independent_stage3_stage4_full.log`.

## 4. Independent Stage 3 classification judgment

All four rules are `DEFINITION`:

1. `squareCeil` names the mathematical square of the semantics’ `ceilInt`
   result. In fixed semantics, the source call to `ceil` evaluates through
   `ceilValue(V) => intVal(ceilInt(V))`, after which multiplication is integer
   multiplication. This rule defines the exact value summarized by the
   source’s `rounded * rounded`.
2. `sumSquares` defines the top-level summary by initializing the accumulator
   summary to zero, matching `total = 0`.
3. The `nil` equation is the base case of the named accumulator recurrence and
   returns the current accumulator.
4. The `cons` equation is the decreasing recursive case. It consumes one list
   element and adds precisely its ceiling-square before recurring on the tail.

Together the last two equations exhaust the `PList` constructors and mirror
the operational `loop` rules: the empty list ends the loop, while a `cons`
binds its head, executes the body, and continues with the tail. This is a
truthful named recurrence, not a free arithmetic fact.

The summary symbols do not occur in `semantic.k` or `solution.mpy`; their K
left-hand sides are only the freshly declared summary functions. They never
match or preempt `exec`, `loop`, `Call`, `Return`, a program AST, or a K cell.
They therefore do not replace program execution and are not
`OPERATIONAL_RULE`s. Their uses outside `verification.k` are only the
universal postcondition and loop-invariant right-hand sides in `spec.k`.

None is a `PROVED_DERIVED_LEMMA`: Stage 1 does not first prove any exact rule
against a module omitting it and later add it. None is a `DOMAIN_LEMMA`:
every left-hand side introduces or recursively defines a named proof summary;
none states an independent mathematical proposition or rewrite over
pre-existing domain operations.

No rule has a `simplification` attribute, so the simplification-class
restriction is also satisfied. There are no irrelevant claimed domain lemmas
because there are no domain lemmas at all.

Independent Stage 3 domain set: **empty**.

Evidence: `evidence/16_semantic_k_numbered.txt`,
`evidence/17_spec_k_numbered.txt`,
`evidence/95_summary_symbol_usage.txt`,
`evidence/97_operational_correspondence_index.txt`, and
`evidence/98_independent_stage3_stage4_full.log`.

## 5. Stage 4 manifest bijection and fixed target

The Stage 4 input manifest carries the exact four reconstructed classified
definitions, in canonical order, and empty `operational_rules`,
`proved_derived_lemmas`, and `source_rules` arrays. Its inventory,
verification, Stage 1 tree, and Stage 3 manifest hashes all recompute exactly.
The generator toolchain object equals the pinned
`klean-toolchain.lock.json`.

Because the independently classified true domain set is empty, the expected
source-rule/obligation bijection is the unique empty bijection. The generated
`obligation-map.json` contains exactly:

- `source_rules: []`;
- `obligations: []`;
- `trust_parameters: []`.

Its SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The generator obligation count is zero.
There is no vacuous conjunct because there is no conjunct and no proposition.

An independent scan finds zero `def targetStatement` declarations in every
generated Lean source. The trusted target parser also returns null. The
generator manifest, recorded preflight, launcher preflight, and launcher
top-level target all record null. Thus the fixed generated target is
correctly absent; it was not weakened, duplicated, replaced with `True`, or
silently changed.

The generated project contains 44 allowlisted operational data/hook trust
declarations, and the preflight reconciles them exactly with
`trust-inventory.json`. They do not manufacture a missing target theorem:
there is no target proposition or proof in this mode.

Evidence: `evidence/11_stage4_input_manifest.txt`,
`evidence/35_stage4_sidecars_and_lock.txt`,
`evidence/36_generated_lean_sources.txt`,
`evidence/89_target_name_and_declaration_search.txt`, and
`evidence/98_independent_stage3_stage4_full.log`.

## 6. Trusted preflight rerun

I reran the unmodified
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required inputs:

```text
/reference/k-proof
/reference/lemma-discovery.json
/reference/klean-generation
/reference/klean-toolchain.lock.json
```

The first invocation reached its fresh Lake copy but encountered an audit
container issue: Lean 4.22 resolves its executable through
`/proc/<getpid()>/exe`, while this PID namespace exposes the process only as
`/proc/self/exe`. That failed attempt is preserved.

I compiled the audit-authored `proc_exe_compat.c`, which redirects only
`readlink("/proc/*/exe", ...)` to `/proc/self/exe`. It does not alter any
mounted input, generated source, manifest, hash computation, or checker
logic. With that environment compatibility layer, the same unmodified trusted
check returned exit 0 with:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- trust declaration count `44`;
- designated sorry count `0`;
- `lake clean`: exit `0`, empty output;
- `lake build`: exit `0`, output SHA-256
  `7fa64f8af7e23352adb1a985e69b9090d0eb4cbd22ee6e03f44e42434ee78da8`.

The complete returned build output reports successful builds of Prelude,
Sorts, Inj, Lemmas, Func, Rewrite, and the root library, followed by
`Build completed successfully.` The returned evidence exactly matches the
previously recorded diagnostic hashes, but the audit verdict relies on the
fresh run and independent mathematical classification.

Evidence: `evidence/38_stage4_preflight_rerun.log`,
`evidence/proc_exe_compat.c`,
`evidence/79_proc_exe_compat_build.log`,
`evidence/80_proc_exe_compat_smoke_test.log`, and
`evidence/81_stage4_preflight_rerun_with_compat.log`.

## 7. Stage 5 applicability

Stage 5 is not selected. The launcher records null Lean invocation/workspace
paths and hashes, null `stage5_result`, and null target. `/candidate` is
absent. These facts are mutually consistent with `CLASSIFICATION_ONLY` and
with the genuinely empty independently classified domain set.

Consequently, no `Base` copy, candidate clean build, `Proof.final`,
`#print axioms`, target-parameter operational bridge, or candidate trust
audit is applicable. Running or inventing such a proof would contradict the
selected mode and the required no-target/no-candidate condition.

Evidence: `evidence/05_audit_input_raw.txt`,
`evidence/07_candidate_presence.txt`, and
`evidence/98_independent_stage3_stage4_full.log`.

## Final judgment

Stage 3 is complete, bijective, and correctly classifies all four rules as
definitions. The true domain-lemma set is empty. Stage 4’s empty obligation
map, zero obligation count, absent target, and `KLEAN_NO_OBLIGATIONS` status
therefore exactly match the frozen program and postcondition. All available
recorded source and tree hashes, including the immutable producer-source
binding, recompute successfully. The fresh trusted preflight passes. Stage 5
is correctly absent.

VERDICT: PASS
LEGITIMACY: LEGIT
