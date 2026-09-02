# Independent Stage 3–5 audit: HumanEval `129-minPath`

## Result

I independently audited the Stage 3 classification, deterministic Stage 4 generation, and Stage 5 Lean proof for condition `kit-semantics` with `SUPPLIED_SEMANTICS`. The launcher and environment both report `CLASSIFICATION_AND_PROOF`.

The protected classification is complete and correct: the frozen local verification-module closure has 71 rules, comprising 64 definitions and seven genuine, relevant domain lemmas. Stage 4 generates exactly one obligation for each domain lemma and exactly the fixed seven-conjunct target. The Stage 5 candidate clean-builds against a fresh copy of that target, states it exactly, introduces no forbidden trust declarations, and uses honest operational models for all 18 target parameters. `Proof.final` depends only on the three standard Lean axioms accepted by the trusted gate and on none of the 50 generated allowlisted axioms.

## Evidence and runtime qualification

Raw command transcripts, reconstructed rules, source excerpts, complete build output, and test results are under `evidence/`. `evidence/19_evidence_index_and_hashes.txt` indexes their SHA-256 hashes. The principal records are:

- `02_inventory_reconstruction_and_bijection.txt`: all reconstructed rule spans, texts, normalized hashes, IDs, and ordered-bijection checks.
- `06_rerun_klean_preflight_check_generation.txt`: required Stage 4 preflight result.
- `09_independent_hash_obligation_target_checks.txt`: independent mounted-input hashes, obligation bijection, and target reconstruction.
- `11_fresh_stage5_lake_clean_build.txt`: complete `lake clean` and `lake build` transcript.
- `12_trusted_stage5_mechanical_check.txt`: independent trusted Stage 5 checker result.
- `13_exact_print_axioms_proof_final.txt`: exact requested `#print axioms Proof.final` output.
- `15_candidate_proof_full_numbered.txt`: complete numbered candidate source.
- `18_operational_bridge_judgment.txt`: per-parameter bridge comparison.

The pinned Lean executable initially failed before reading any project because the sandbox's namespaced `getpid()` value did not exist as `/proc/<pid>` in the visible host procfs. This was isolated in `05_lean_toolchain_diagnosis.txt` through `05g_repaired_pinned_lean_launcher_test.txt`. I used the source-recorded compatibility shim in `05h_proc_namespace_compatibility_shim_source.c`; it changes only `readlink("/proc/<pid>/exe")` to `readlink("/proc/self/exe")`. It neither rewrites Lean input nor changes compiler behavior. With it, the frozen gate reported K 7.1.293, pyk/Klean 7.1.293, Lean 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and Codex 0.144.6. All authoritative Lean runs below use those binaries. The earlier failed preflight in evidence 04 is superseded by the successful identical preflight in evidence 06.

## Producer and input authentication

Before judging Stage 4, I hashed the two mounted generation-time producers:

| Source | Recomputed SHA-256 | Result |
|---|---|---|
| `klean_export.py` | `f1a7004c0ec7b8be2646f9fdedbc9a9975903f9797e34cdf8b3e4ecb1df3ed59` | Matches the source manifest and `generator-manifest.json` |
| `klean.py` | `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91` | Matches the source manifest and `generator-manifest.json` |

The trusted pipeline tree hash of `/reference/generation-tools` is `3141041ba4f4427b633483489102d026b053f5f382041e7ae1d1041689619478`, exactly the audit-input digest. The source manifest and generator manifest both identify immutable generator image `sha256:853cc3153c8c3a393e12a3bbc09f51f7f1384695616f4490f55b252c156a3d0e`; the same ID is the basename of the launcher-recorded producer-source path. Thus the producer source is present and authenticated, with no infrastructure error. Evidence 03 used the wrong tree-digest convention during diagnosis; evidence 03b is the corrected trusted pipeline-tree calculation and is the result relied upon.

I independently recomputed every hash whose object the launcher mounted. All matched:

- K workspace pipeline tree: `6579796facb7cb2ec175151b01b0f0e0c0386918f3b2ba4a400594fb28869882`.
- Stage 1 export tree: `348dce5dc4d8752ff98fd445064385e8fa1dea916a081e609b2ea16ab4fe5256`.
- Stage 2 audit tree: `615f43026ef6682568735eeaf71130b8e430bc3aeb9c1c98bac0b9fdb0684f9e`.
- Stage 3 manifest file: `d021c40e31d42f3e583a14daef7e41bbed5939b3928fc963569df326bd631ce0`.
- Stage 4 generation pipeline tree: `19e379bd862003a64fb7d053c37b80129b355f514109938232e3ba588a9e686f`.
- Generated Lean tree: `35197789ca46f7f8d7eeec631e18b1e30af607c328967d86d1a27ffa2ffb502b`.
- Stage 5 candidate pipeline tree: `fa6a26e89061ed552288ee48269609a052c0e0c5715fff0c80f0ac6ab7288ba6`.
- All 770 individually recorded Stage 1 source hashes, with no missing, mismatched, or unrecorded mounted files.

The audit input also records a Stage 5 invocation-directory digest, but the launcher intentionally did not mount that directory among the declared inputs, so that one historical-directory digest cannot be recalculated. It is not used as proof evidence: the mounted candidate tree matched its own recorded digest and I regenerated the clean build, exact-type check, and axiom output from scratch.

## Inventory reconstruction and Stage 3 classification

Using `tools.k_rule_inventory.inventory_verification` with `PYTHONPATH=/reference`, I reconstructed the local closure rooted at frozen `verification.k`. It contains only local module `VERIFICATION` and exactly 71 rule entries. The reconstruction produced:

- frozen `verification.k` SHA-256 `2834fcdd963685cbed1873b2aa802b5f508d1028eeee72007f4e7001c223fb76`;
- inventory SHA-256 `2f34de6086439b274fa066f73caa7594f022eb8812c6d5ff00eb4b9566898f3e`;
- 71 unique source spans, normalized hashes, and `source_rule_id` values.

The protected Stage 3 manifest also has exactly 71 unique entries. Its ordered ID sequence is identical to the reconstruction: no omission, duplicate, extra rule, reordered identity, changed source span, or changed normalized hash exists. The full per-rule comparison is in evidence 02, and the independent category decision for every entry is in evidence 08.

My classification is 64 `DEFINITION`, zero `OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and seven `DOMAIN_LEMMA`, exactly matching Stage 3:

- Rules 1–26 define membership, range, uniqueness, valid permutations, total flat access, row construction, grid construction, and location-of-one summaries by base/step or guarded equations.
- Rules 32–46 and 48–51 and 53–57 define the minimum, append, pair/odd completion, finish, and path summaries. The special `snocVS` equations remain defining equations for that named recurrence.
- Rules 58–71 are exact named AST macros for contiguous constructs in `solution.py`, which the requested taxonomy expressly treats as definitions.
- No rule rewrites an MPY execution configuration; execution-state claims are in `spec.k`, outside this rule inventory. Therefore none is an operational rule.
- No theorem-like rule is first proved against a module excluding that exact rule and then imported for a later proof. All seven theorem-like rules are present in `VERIFICATION` from the start, so none qualifies as a proved derived lemma.

The seven independently identified domain lemmas are:

| Frozen span and source-rule ID | Mathematical judgment and relevance |
|---|---|
| 105–107, `rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70` | `gridRows` has length `N` for a valid `N²` permutation. This connects source `len(grid)` and the nested scan bound. |
| 109–113, `rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149` | In-bounds lookup of `gridRows` returns the matching constructed row. This is the outer subscript bridge for `grid[i][j]`. |
| 115–120, `rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b` | In-bounds lookup of a constructed row equals row-major `gridAt`. This is the inner subscript bridge. |
| 122–127, `rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1` | Under permutation and bounds, a cell is 1 iff its coordinates are the unique `oneRow`/`oneCol`. This justifies the source scan's location result. |
| 129–134, `rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987` | Every valid cell is below `N²+1`. This connects the source's initial neighbor sentinel to the conditional minimum updates. |
| 212–213, `rule-79cc3308597d2aedf94188a46aa45b9302edb4bd5dc309fcd4bc218ec8dc5894` | Operational list concatenation with a singleton equals the verification `snocVS` summary. This is required for each `result.append`. |
| 239–242, `rule-9b8ee50fdbbf692e2fa2c6bc4aa68e73f5759ff24a19c85fc3e0de3519dd9348` | For nonnegative pair count, adding the final 1 turns `oddDone` into `pairDone`. This is precisely the odd-`k` tail of the postcondition. |

All seven are true over the supplied constructor/list/integer semantics and are directly relevant to the frozen program or full postcondition. Independent finite/adversarial checks exercised 46,648 cases, including all 24 permutations for `N=2`, diverse `N=3` locations, negative and invalid permutation inputs, sequence append cases, and pair counts 0–6. Five direct executions of frozen `solution.py` covered corner, edge, center, odd-`k`, and even-`k` cases. All passed. Every one of the 19 `[simplification]` rules is either one of these seven domain lemmas or a defining summary equation; there is no forbidden simplification classification.

## Stage 4 generation and mathematical target audit

I reran the required check with the trusted module and exact mounted inputs:

```text
PYTHONPATH=/reference tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

The result is `PASS`: seven obligations, zero designated sorries, generated tree `35197789ca46f7f8d7eeec631e18b1e30af607c328967d86d1a27ffa2ffb502b`, and 50 recorded generated trust declarations. Its internal fresh `lake clean` and `lake build` both exited 0.

I separately reconstructed the obligation map rather than treating preflight as mathematical evidence. The ordered domain-lemma ID list, `source_rules` list, and `obligations` list are the same seven-element sequence with seven unique IDs. For every entry, the frozen span, normalized source hash, inventory hash, discovery-manifest hash, and independently recomputed Lean-conjunct hash agree. There are no omissions, duplicates, or surplus obligations.

Each conjunct is the direct equation represented by its K rule: guards are retained exactly for the first five; the unguarded singleton append equation remains universal; and the odd/pair equation retains `R >= 0`. The valid-grid guards have concrete witnesses and the candidate's `validPerm` is not constant false. The cell-location equation was exercised at both the 1-cell and non-1 cells. The final two equations quantify over arbitrary sequences. Thus no conjunct is vacuous under the actual bridge. The target neither weakens nor changes any conclusion.

Trusted reconstruction of `targetStatement` from the obligation map occurs exactly once in `Klean129Minpath/Lemmas.lean`. Its fixed identity is:

- declaration: `Klean129Minpath.Lemmas.targetStatement`;
- definition SHA-256: `f0f7fa1540eb7f59d6d7de4a086b86041e0a33844ed07278be70f46d3b14128d`;
- applied-statement SHA-256: `26eb2d37e8fa8f1eeffa43885ca21c5d35c9978b564b5f092510651f4257e1fc`.

The reconstructed target metadata equals `generator-manifest.json`, the successful preflight, and `/audit-input.json` byte-for-byte as structured data. This is correctly a nonempty-obligation generation, not `KLEAN_NO_OBLIGATIONS`.

## Stage 5 proof, target identity, and trust

I created fresh project `/tmp/audit-work/stage5-proof-audit.0I7s5N`, copied `/reference/klean-generation/generated` into it as `Base`, and copied only the four candidate project files. The fresh `Base` non-build files are byte-identical to the selected generated project. I then ran both required commands:

```text
lake clean   # exit 0
lake build   # exit 0, Build completed successfully
```

The complete output is in evidence 11. The trusted Stage 5 mechanical checker independently repeated clean/build and the exact-type/axiom check and returned `PASS` in evidence 12.

Static inspection found no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque` token in any candidate Lean source. Each of the 18 exact target parameters has exactly one candidate `def`; `Proof.lean` defines no `targetStatement`, contains exactly one theorem named `final`, and cannot shadow the generated namespace. The normalized theorem type is exactly the fixed applied statement above, not a copy, weakening, or alternate proposition.

The exact requested Lean output was:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. `propext`, `Classical.choice`, and `Quot.sound` are the three standard Lean kernel axioms explicitly admitted by the trusted gate in addition to names recorded in `trust-inventory.json`. None of the 50 generated allowlisted axioms is actually a dependency of `Proof.final`, and there is no unexpected or unrecorded axiom dependency.

## Operational bridge audit

I compared every parameter declaration to its bound KORE symbol, all recorded source-rule IDs, the corresponding frozen verification equations, imported operational semantics, and `solution.py`. The result is:

| Parameters | Candidate implementation | Judgment |
|---|---|---|
| `_andBool_`, `«_>=Int_»`, `«_<Int_»`, `«_==Int_»`, `«_+Int_»`, `«_*Int_»` | Lean Bool conjunction and decidable mathematical-Int comparison/equality/addition/multiplication | Exact hook meanings |
| `gridAt` | Total flat access at `i*n+j`, using the frozen `pAtTotal` zero default | Exact |
| `gridRow`, `gridRows` | Constructor-preserving ranges over columns and rows, with empty behavior for nonpositive `n` | Exact frozen recurrences |
| `oneRow`, `oneCol` | First index of 1, K `INT.tdiv` row quotient, normalized K/Python modulus column, and the frozen nonpositive-`n` cases | Exact |
| `validPerm` | `m >= 0` and permutation of `[1..m]` | Equivalent to frozen length/range/uniqueness definition, including `m <= 0` edge cases |
| `vsLen` | Constructor count converted to Int | Exact imported recurrence |
| `valSeqAt` | Constructor indexing for every specified in-bounds case | Exact on all guarded/reachable cases; `noneV` is a harmless total realization only where imported `[total]` intentionally leaves OOB/opaque access abstract |
| `valSeqConcat` | Constructor-preserving list append | Exact operational list concatenation |
| `snocVS` | Constructor-preserving append of one value | Exact frozen base/step recurrence |
| `pairDone`, `oddDone` | Repeated append of `[1,m]`, with the exact equality base cases and final odd 1; negative `r` maps to the `r <= 0` base | Exact frozen recurrences |

Actual Lean evaluation produced the expected values for normal and adversarial inputs: row-major cells 1 and 4, negative flat index default 0, location `(1,0)` for permutation `[4,2,1,3]`, `validPerm` true for `[1,2,3,4]`, false for a duplicate and for negative size, and two generated rows. Constructor-valued indexing, snoc, and concatenation examples reduced by reflexivity. The independent oracle additionally compared K-style and candidate-style `validPerm` on invalid, empty, duplicate, out-of-range, and valid inputs with no mismatch.

Counterfactual checks show why the operational inspection matters. A constant-false `validPerm` would vacuate the first five conjuncts, and identical constant `oddDone`/`pairDone` functions would trivialize the seventh; the actual definitions are neither. Replacing the actual `gridAt` definition by constant zero made Lean fail with the concrete unsolved goal `gridAtModel P N I J = 0`. Replacing `snocVS` by identity made the singleton-concatenation and odd-tail obligations fail. The authoritative sequential transcripts are evidence 16c and 16d. Preliminary parallel attempts in 16a/16b are not relied upon because the generated Lake package uses a shared fixed `/tmp/klean-generated-build` directory, causing those two experiments to interfere.

The successful build is therefore not merely an equation solved by convenient parameter choices: all parameter bridges implement the frozen operational meanings used by the source and postcondition.

VERDICT: PASS
LEGITIMACY: LEGIT
