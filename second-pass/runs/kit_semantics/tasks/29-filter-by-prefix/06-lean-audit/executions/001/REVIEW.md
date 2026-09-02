# Independent audit: 29-filter-by-prefix

## Scope and result

This audit covers HumanEval `29-filter-by-prefix`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and
the canonically verified `/audit-input.json` select `CLASSIFICATION_ONLY`.
Stage 4 is selected as `KLEAN_NO_OBLIGATIONS`.

I treated all mounted candidate, provenance, report, log, comment, and
instruction content as untrusted evidence. The rule inventory, hashes, K
proofs, and Stage 4 preflight were independently reconstructed or rerun with
the trusted tools.

The classification and no-obligation generation are legitimate. There is no
Stage 5 candidate or generated target to audit in this mode.

## Producer provenance gate

I authenticated the producer sources before judging Stage 4.

- `/reference/generation-tools/klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `/reference/generation-tools/klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- Immutable generator image:
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
- Producer bundle tree hash, using
  `tools.pipeline_contract.sha256_tree`:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`

The two file hashes match `source-manifest.json` and the corresponding
`exporter_sha256`/`klean_py_sha256` fields in `generator-manifest.json`. The
image ID matches the source manifest, generator provenance, and the image-key
component of the producer-source path recorded in `/audit-input.json`. The
bundle tree hash matches the audit input. This gate passes; there is no
producer-source `AUDIT_ERROR`.

The verified audit-input digest is
`5084f582608482b1a3a22da6e725c74f7114e0b9f97a8283bce0258b75024cf5`.

## Rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof` workspace.

The reconstructed local verification-module closure is exactly
`["VERIFICATION"]`. It contains one rule:

- Source span: `verification.k:10-43`
- Module: `VERIFICATION`
- Attributes: `[priority(40)]`
- Normalized source SHA-256:
  `d4a0ca7c71bd8004730d058283a2e7c70fe73c82b0044f80eda2cfa19e148b41`
- Source rule ID:
  `rule-d4a0ca7c71bd8004730d058283a2e7c70fe73c82b0044f80eda2cfa19e148b41`
- Whole inventory SHA-256:
  `8562989cb1139eab0ae6201ecdb15f1af6a793bb508e807029a8c1e23f45801e`
- Frozen `verification.k` SHA-256:
  `77b71c835c3b86535d9cf21e4aafb4859fb55fe0039eba8361f685271773c5a7`

I separately re-extracted lines 10-43, normalized their whitespace, recomputed
the normalized hash and `source_rule_id`, and recomputed the canonical whole
inventory hash. All values agree.

`/reference/lemma-discovery.json` contains exactly that one identity, once, in
the same order, and records the same inventory hash. There are no omitted,
duplicated, extra, reordered, or hash-changed entries.

The trusted inventory contract is intentionally local to the modules declared
inside `verification.k`; required/imported files are proof dependencies rather
than additional Stage 3 inventory entries. I nevertheless inspected and
reproved the load-bearing proof-local bridge in that dependency closure as
described below.

## Independent classification judgment

The sole rule rewrites an exact operational configuration:

- It starts at the program's `#loop` over `list(INPUT)`, with the exact loop
  variable and `filterLoopBody`.
- It includes the exact `Return(Name("result")) ~> #endcall` continuation,
  environment, scopes, heap, allocator, stack frame, return cell, exception
  cell, and `allStrings(INPUT)` guard.
- It returns `ref(H)` and updates the list at `H` from `ACC` to
  `filterPrefixAcc(ACC, INPUT, P)`, while performing the specified frame and
  scope cleanup.

This is not a `DEFINITION`: it summarizes an operational execution rather than
defining a summary symbol. It is not an ordinary `OPERATIONAL_RULE`: the exact
whole-loop execution statement is separately proved before being installed.
It is not a `DOMAIN_LEMMA`: it is an exact reachability result over the program
configuration, not an unproved mathematical property added to close the
postcondition. It has no `simplification` attribute.

The correct independent classification is therefore
`PROVED_DERIVED_LEMMA`, for these independently checked reasons:

1. `loop-connection-spec.k` contains the exact same configuration,
   rewrite, guard, and result as the rule (after removing only the `claim`
   label and the later operational priority attribute).
2. Its proof definition is freshly compiled from `verification-core.k`.
   The recursive required-file closure contains `verification-core.k`,
   `domain.k`, and the supplied reference semantics, but does not contain
   `verification.k` or the classified rule.
3. A fresh `kompile` of that bridge-free closure succeeded, and a fresh
   `kprove loop-connection-spec.k` returned `#Top` with exit 0.
4. The frozen Stage 1 source orders this auxiliary proof before compiling
   `verification.k`; only afterward does it prove `spec.k`. I reenacted that
   sequence in a clean temporary workspace. The fresh later proof also
   returned `#Top` with exit 0.

The auxiliary loop proof imports one proof-local iterator bridge. I audited
that dependency rather than accepting it transitively. The bridge replaces
fixed list iteration's yielded value `V` with
`str(stringCodes(V))` under `isStringVal(V)`. The guard states exactly that
those values are equal. Its universal connection claim quantifies over an
arbitrary continuation `CONT`, and was freshly proved with `#Top` against
`domain.k`, whose closure contains fixed semantics but not the bridge.

The operational meaning also matches the frozen program. Supplied semantics
iterate list elements in order, implement `startswith` through
`startsWith(prefix, string)`, and implement `append` as an in-place append to
the result list. `filterPrefixAcc` performs exactly that stable selection,
preserving the initial accumulator, taking the matching branch when
`startsWith` is true and dropping the element otherwise. The `allStrings`
guard makes `stringCodes` exact on every iterated value. Empty input, empty
prefix, no-match input, repeated strings, and mixed matching/nonmatching order
all follow those same complementary recursive branches.

Finally, I reran the concrete false-result mutation for input `["abc"]` and
prefix `"a"`. The mutation demands an empty output. `kprove` exited 1 with
`WarnStuckClaimState`, exposing the actual nonempty heap result. The proof is
therefore result-constraining rather than vacuous.

The independently reconstructed Stage 3 domain-lemma set is genuinely empty.
The protected classification's sole `PROVED_DERIVED_LEMMA` entry is accepted.

## Recorded hashes and manifest chain

I independently recomputed every resolution hash recorded in the audit input:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 3 discovery manifest | `2c7abbfa89a86ee7de1e664512b58e6b01f403793a15583a1262a24b4775264d` |
| Generated project tree | `4c0a73a71e8274ab2f86fd414b24e97d07838694c0fcb7623114f1eb4f14f10b` |
| Producer-source bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| Selected Stage 2 K audit tree | `3d33e75f3554bb09a104738bcd7ba63f0991d9b6b94eb922490edfe066a2ed3a` |
| Stage 1 workspace tree | `f8a9295f1f12ff25366a0c3eba30f6a8cf0865d89e46560b854375f4708c04b6` |
| Selected Stage 4 generation tree | `fe4cb65537457b7f6ecaf4d1e643be373fb96c071ed5c03af58a02c57dee29de` |
| Stage 1 deterministic-export tree | `a43eb55faa420b68e760f7991f7320f54545f52c8c02720046b77e22f189cbbe` |

The selected Stage 2 and Stage 4 artifact hashes agree with their selection
records. All 835 individual `stage1_source_hashes` entries were recomputed;
there are no missing, extra, or mismatched paths. The input manifest,
generator provenance, export result, stored preflight, trust-inventory hash,
obligation-map hash, verification-source hash, and pinned toolchain object all
agree with the recomputed inputs.

## Stage 4 obligation and target audit

The independently accepted domain set is empty. Stage 4 consistently records:

- `input-manifest.json` domain `source_rules`: empty
- Generated `obligation-map.json` source rules: empty
- Generated obligations: empty
- Generated trust parameters: empty
- Generator `obligation_count`: `0`
- Export result `obligation_count`: `0`
- Generator target: `null`
- Stored preflight target: `null`
- Audit-input target: `null`

The obligation-map SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trusted target extractor independently
returns `null`, and a source scan finds no `targetStatement`. Thus the
source-rule/obligation relation is an exact empty bijection. There are no
omissions, duplicates, irrelevant or weakened obligations, vacuous conjuncts,
or target changes.

Because the true domain set is empty, `KLEAN_NO_OBLIGATIONS` is the correct
Stage 4 status rather than an evasion of a material Lean obligation.

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly these logical inputs:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The trusted preflight returned:

- Status: `KLEAN_NO_OBLIGATIONS`
- Obligation count: `0`
- Target: `null`
- Trust declaration count: `41`
- Designated sorry count: `0`
- Fresh `lake clean`: exit `0`
- Fresh `lake build`: exit `0`
- Generated tree:
  `4c0a73a71e8274ab2f86fd414b24e97d07838694c0fcb7623114f1eb4f14f10b`

The 41 declarations are generated collection-hook executable boundaries in a
project with no target proposition; the preflight independently rejected
proposition trust and reconciled the declarations with
`trust-inventory.json`.

The first clean-build attempts exposed an audit-container infrastructure
quirk: Lean queried `/proc/<namespace-pid>/exe`, while the mounted host `/proc`
could make that PID absent or point at an unrelated host process. The pinned
Lean executable therefore initially failed before elaboration. The raw
failures are preserved. A minimal `LD_PRELOAD` shim redirected only those
`/proc/<pid>/exe` reads to `/proc/self/exe`; the real pinned Lean 4.22.0 and
Lake executables then ran successfully. The trusted preflight still copied the
immutable generated tree to its own fresh directory, performed both build
commands, and verified unchanged input snapshots afterward. This environment
repair does not alter candidate or provenance content and does not weaken any
preflight gate.

## Stage 5 applicability

This is not proof mode. `/candidate` is absent, the audit input records null
Stage 5 hashes and result, and Stage 4 has no generated target. Running
`Proof.final`, auditing its axioms, or checking operational target parameters
would invent a Stage 5 artifact forbidden by the selected
`CLASSIFICATION_ONLY` mode. No Stage 5 proof verdict is needed.

## Evidence

The exact command record is in
`/audit-output/evidence/COMMANDS.md`. Principal raw results are:

- `stage1-rule-inventory.json`
- `stage3-classification-verification.json`
- `fresh-iterator-connection-kompile.log`
- `fresh-iterator-connection-kprove.log`
- `fresh-loop-connection-kompile.log`
- `fresh-loop-connection-kprove.log`
- `fresh-final-kompile.log`
- `fresh-final-kprove.log`
- `fresh-vacuity-mutation-kprove.log`
- `generation-producer-authentication.json`
- `recorded-hash-verification.json`
- `klean-preflight-rerun.json`
- `tool-versions.log`

VERDICT: PASS
LEGITIMACY: LEGIT
