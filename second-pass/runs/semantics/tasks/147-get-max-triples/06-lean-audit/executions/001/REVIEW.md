# Independent Stage 3–5 Audit: `147-get-max-triples`

## Scope and audit mode

This is an independent audit of condition `semantics` in
`SUPPLIED_SEMANTICS` mode. I treated the selected Stage 2 review, all prior
logs, comments, manifests, generated sources, and any purported verdict as
untrusted evidence. I did not use the earlier review to reach this result and
did not execute the generation-time producer sources.

Both `AUDIT_MODE` and the signed resolution in `/audit-input.json` say
`CLASSIFICATION_ONLY`. The signed resolution digest recomputes to
`44fb41090deac3d8a0196e746fff9c9062176c00cd4a45603ac89ce43311af69`.
The resolution has no Lean workspace, Lean invocation, Stage 5 result, or
target, and `/candidate` is absent. Consequently the Stage 5 clean-copy build,
`Proof.final`, `#print axioms`, and target-parameter operational-bridge checks
are not applicable. Their absence is required by the selected
`KLEAN_NO_OBLIGATIONS` status.

## Input and producer integrity

I independently rehashed all material signed inputs and manifest bindings.
The complete machine-readable results are in
`evidence/17_independent_consistency_checks.json`; every recorded check passed.

| Artifact or binding | Recomputed SHA-256 | Judgment |
|---|---|---|
| Stage 1 selected workspace, pipeline tree hash | `b852c9d3f64f0d8a1278a427af882107587934654cb232d910efc1a1cd95a933` | Matches audit input |
| Frozen Stage 1 export, Klean tree hash | `bc01df1cea61c8c64650ac8cd1492a62594f84c106027eb72d9e31f340756cd6` | Matches audit input and all Stage 4 provenance |
| Stage 2 selected audit, pipeline tree hash | `d39555c508e5240587b6c8accca5d504a7a98a4a28957ceeae9b4fbc2f4a8cb2` | Matches audit input; contents were not trusted |
| Stage 3 manifest file | `0bca966e85ff7dafbf32bc3c07bc221908ebcdce3fed3e17c7f04ff7f06205d2` | Matches audit input and Stage 4 provenance |
| Stage 4 generation, pipeline tree hash | `aa111498f2ab3f33ea5c974d29f1db77fcaafaaee666e963edcc19a1021f8721` | Matches audit input |
| Generated project, Klean tree hash | `604124a0567019182e142d6df023f09be0cbd093ca481a0ebed4248d48300a5f` | Matches audit input, generator manifest, and export result |
| Producer-source bundle, pipeline tree hash | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` | Matches audit input |
| Generated obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` | Matches generator manifest |
| Trust inventory | `c48fd18d7bdf35cfc66c7f452c833830c07587e2a3d14b8c33a9094c00dd09b2` | Matches export result |

The audit input lists 34 Stage 1 source files. I found exactly those 34
regular files, with no missing, extra, or hash-mismatched entry.

Before judging Stage 4, I hashed the two preserved generation-time producer
files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes exactly match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The bundle contains exactly those
two sources and the source manifest. The immutable generator image identity is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest and source manifest, and the same digest is bound by
the terminal component of the signed producer-source path in the audit input.
There is therefore no producer-source infrastructure error.

## Canonical inventory reconstruction

I ran the trusted inventory implementation directly on the frozen Stage 1
workspace. `prove.sh` selects `VERIFICATION`; its local, same-file module
closure is exactly `["VERIFICATION"]`. The imported `MPY` module is supplied
from the frozen semantics but is not a module declared locally in
`verification.k`, so it does not enlarge this local inventory.

The reconstruction found exactly four rules. For each one I separately sliced
the recorded physical source lines, compared the text byte-for-byte, normalized
it with whitespace joining, recomputed its SHA-256, and rebuilt
`source_rule_id` as `rule-<normalized SHA-256>`.

| Source span | Recomputed normalized SHA-256 | Attributes |
|---|---|---|
| `verification.k:9–41` | `c93f82157c0edf66f39013c6c43f9942de4d4fdb03a65233bc92f11b525c2c62` | none |
| `verification.k:46–48` | `6e1a3f1a867ffa5aac98437215b212d2acc24e46fb6c160c7eef1d20a27d3da2` | none |
| `verification.k:52–53` | `ed9df131f37e783d697605c42deebd79589fdb258ea41d40595b1e3bc625bc2e` | none |
| `verification.k:56–58` | `54b144e14a69f0c5714e7e1621ac7fbbcf27e44642f7d6a540aa852db23a3ef0` | none |

All spans, text, hashes, and IDs match the canonical inventory. Its whole
canonical inventory hash recomputes to
`50b8fc17588e9a70110064bc0f0e52b0922b9ce7723689693ff446b7a2d52d25`.

The Stage 3 manifest has exactly these four IDs, exactly once each, in the same
order. The trusted Stage 3 boundary validator also accepts the manifest.
Therefore there are no omissions, duplicates, extras, reordered identities,
changed hashes, or unaccounted entries.

The three residue declarations at `spec.k:7–26` are reachability `claim`
sentences, not `rule` sentences in the local verification-module closure. They
are separate Stage 1 claims and are not silently present in this rule
inventory.

## Independent classification judgment

I classified by the rule's actual semantic role, not its name or Stage 3
rationale:

| Rule | Independent class | Reason |
|---|---|---|
| `getMaxTriplesBody` | `DEFINITION` | It is a named proof-term/macro expanding to the exact translated sequence of four assignments and a return from `solution.mpy`. It does not return a summarized value or preempt call execution. After expansion, the ordinary semantics performs name lookup, expression evaluation, assignments, return, frame restoration, and all state changes. |
| `chooseThree(C)` | `DEFINITION` | It introduces a fresh mathematical summary symbol and gives its single unconditional equation. It does not rewrite an existing Python or K operation. For the nonnegative population counts used by the theorem, the expression is the usual `C choose 3`; as a K rule it is definitional even outside that intended interpretation. |
| `zeroResidues(N)` | `DEFINITION` | It introduces a fresh summary name for the floor expression `(N+1)//3`. It does not itself assert a cardinality theorem about an existing set or sequence. |
| `tripleCount(N)` | `DEFINITION` | It introduces a composite summary by applying the two preceding summaries. It asserts no new fact about an existing symbol. |

The supplied semantics confirms this behavioral classification:

- `Call` evaluates the callee and arguments, dispatches a `closureVal`, binds
  the parameter, pushes a frame, and runs the body.
- statement sequencing exposes each statement;
- assignment evaluates its right-hand side and updates the current scope;
- `Name` performs scope lookup;
- `BinOp` evaluates operands and dispatches ordinary integer operations;
- Python `//` is implemented as `(I1 - pyMod(I1,I2)) /Int I2`;
- `Return` records the value and pops/restores the frame.

Thus `getMaxTriplesBody` is a syntax macro, not an operational bridge. The
other three rules only define fresh summaries. None matches a configuration
cell, skips a source-language operation, establishes a pre-existing algebraic
identity, or has a prior-proof/later-use history. There are no
`OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA` entries. No rule
has a `simplification` attribute, so the simplification-class restriction is
also satisfied.

The classification is mathematically relevant to the frozen program and
postcondition. For `i mod 3` equal to `0, 1, 2`,
`i²-i+1 mod 3` is respectively `1, 1, 0`. Among `1..n`, the zero-residue
population is therefore `floor((n+1)/3)` and the remaining values have residue
one. A triple sums to zero modulo three exactly when it uses three zero
residues or three one residues, yielding the `tripleCount` expression. An
independent brute-force check for every positive `n` from 1 through 60 found
zero mismatches with both the frozen source formula and the summary formula.
A counterfactual `n//3` population formula first fails at `n=5` (`4` versus
the correct `1`), and a `+1` result mutation also fails there. These finite
tests support relevance and sensitivity; the classification itself follows
from the rule forms and operational semantics.

## Stage 4 generation and obligation judgment

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4
generation, and pinned toolchain lock.

The first invocation exposed an audit-sandbox runtime defect: Lean attempted
to resolve `/proc/<process-id>/exe`, but the sandbox's process namespace does
not expose that numeric path. Consequently `lake clean` initially reported
that it could not detect the Lake installation. A readlink trace demonstrated
the exact failing call. I used a minimal, recorded preload shim that only
retries a failed `/proc/<pid>/exe` lookup as `/proc/self/exe`; this made the
same installed binary report Lean `4.22.0`, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. It does not alter any input,
Lean source, checker decision, or generated project. The shim source and both
the failed and successful runs are preserved under `evidence/`.

The rerun of the unmodified trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1 hash
  `bc01df1cea61c8c64650ac8cd1492a62594f84c106027eb72d9e31f340756cd6`;
- Stage 3 hash
  `0bca966e85ff7dafbf32bc3c07bc221908ebcdce3fed3e17c7f04ff7f06205d2`;
- generated tree hash
  `604124a0567019182e142d6df023f09be0cbd093ca481a0ebed4248d48300a5f`;
- zero obligations;
- `target: null`;
- zero designated sorries;
- 48 allowlisted non-proposition trust declarations; and
- successful `lake clean` and `lake build`.

The regenerated diagnostic hashes differ from the historical diagnostic
hashes only because the preload shim writes executable-path trace lines to
stderr. The build result and every immutable input/tree hash match.

Independently of preflight, I compared the classification partition to
`input-manifest.json` and `obligation-map.json`. The true domain-lemma ID list,
the Stage 4 `source_rules` list, and the generated obligation ID list are all
exactly empty. There is no duplicate, omission, weakened obligation,
irrelevant conjunct, or vacuous conjunct because there is no conjunct at all.
The obligation count is zero in the generator manifest, export result,
historical preflight, fresh preflight, and signed audit input.

I also invoked the trusted generated-target parser directly. It returns
`null`; `generator-manifest.json` and the signed audit input also record
`target: null`, and `Lemmas.lean` contains no proposition declaration. This
is the exact fixed generated target required for a genuine empty domain set.
No Stage 5 proof candidate exists.

## Evidence index

- `evidence/01_inputs_and_producer_hashes.txt`: initial producer hashes and
  manifests.
- `evidence/02_inventory_source_and_contract.txt`: frozen source, canonical
  inventory, and Stage 3 boundary-validation output.
- `evidence/03_required_preflight.txt`: preserved initial environment failure.
- `evidence/04_lean_toolchain_diagnosis.txt` through
  `evidence/12_lean_proc_workaround_test.txt`: toolchain identity and isolated
  `/proc` diagnosis.
- `evidence/13_required_preflight_success.txt`: successful required preflight
  and complete returned evidence.
- `evidence/14_primary_hash_recomputation.txt` and
  `evidence/15_pipeline_tree_hash_recomputation.txt`: raw hash recomputations.
- `evidence/16_generated_project_and_manifests.txt`: obligation map, generated
  target module, trust inventory, and token scan.
- `evidence/17_independent_consistency_checks.json` with
  `evidence/audit_consistency.py`: all signed hash, source, inventory,
  bijection, status, target, and Stage 5-absence checks.
- `evidence/18_operational_semantics_relevant_rules.txt`: relevant frozen
  operational rules.
- `evidence/19_mathematical_relevance_and_sensitivity.txt` with
  `evidence/math_sensitivity.py`: independent contract and mutation checks.
- `evidence/readlink_proc_workaround.c`: exact sandbox-only workaround source.

## Conclusion

The Stage 3 manifest is a bijective, hash-exact classification of the complete
local rule inventory. All four rules are genuinely definitional; the
independently determined domain-lemma set is empty. Stage 4 faithfully and
deterministically records that empty set as zero obligations with no generated
target, and all producer, source, tree, obligation-map, toolchain, and signed
resolution bindings hold. The classification-only mode correctly has no Stage
5 candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
