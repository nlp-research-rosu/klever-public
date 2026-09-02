# Independent audit: HumanEval `9-rolling-max`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Outcome

The protected Stage 3 classification is complete and independently correct.
The deterministic Stage 4 generation is bound to the frozen inputs and
contains exactly the one genuine domain-lemma obligation. The Stage 5
candidate clean-builds, proves the exact immutable target without axioms, and
implements the generated target parameter with the frozen operational meaning.

## Input and producer provenance

I recomputed the launcher envelope digest and every hash having a corresponding
mounted input. All checks in `evidence/01_hash_provenance.log` pass:

| Artifact | Recomputed hash |
|---|---|
| Signed resolution | `f9f5e4ee65b990e5e2448f981e1e76db8c6068334b5c0f3f9a68188e42cdddbd` |
| Stage 1 workspace tree | `2f090d30c3678d752156ec1fd5495ec9e0100ea3865d0645d38ad70dd3bde8a3` |
| Stage 1 deterministic-export tree | `7a1b5a23be16310c39d73eebce7f4fadc7dec6a45b039a4cbff6a3a99afcd9dd` |
| Stage 3 manifest | `93c0b7a4a0691f75a40de634db54d8f57f5a2c1f7f25f65cf59594d002a3d671` |
| Selected Stage 2 audit tree | `9b3c9f775d0ab25b8be6406196cf6ec27a69fc36d62bb9964cd098ee8e0cbda5` |
| Selected Stage 4 generation tree | `b2ff7b84a33e7680952512875d5cbb51fb252e53a0c83e41619b754a34b86320` |
| Generated Lean project tree | `b6beacafc3c23d769d10af9ea05d0a63d2edbcaf5d04110cde914251d165d8bd` |
| Producer-source bundle tree | `d51304d7acd70db93e839359fc003780b85d84d8ab4fd36ac2ec2a8227f4437b` |
| Stage 5 candidate tree | `ec5da6da90b2fe3501cc01f8cfe71a9bcdf00ee06a9e38c74325b2c90ef45eee` |

The complete 34-entry Stage 1 per-file hash map also matches the signed audit
input. The historical Stage 5 invocation/evidence tree is not mounted, so its
recorded `lean_invocation_sha256` has no local tree to rehash; the mounted
Stage 5 workspace itself matches both the signed hash and
`stage5_result.outputs.workspace_sha256`.

Before judging generation, I hashed the two mounted producer sources:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `3a5a8be795d55a2bc01b73d47099f04795b9d64f6bbcf64494b57bcde8266582`

Each hash agrees with both `source-manifest.json` and
`generator-manifest.json`. Both manifests name immutable generator image
`sha256:db04cbaec4c5ee7b34348393f5a7742991e12d63480de3eab85fe97022f51657`,
and the final component of the producer-source path signed in
`/audit-input.json` is the same image key. The bundle has exactly the two
producer files and its source manifest. This provenance gate passes; there is
no `AUDIT_ERROR`.

## Inventory reconstruction and Stage 3 classification

Using the trusted `tools.k_rule_inventory.inventory_verification` code, I
reconstructed the local verification-module closure of frozen
`verification.k`. The selected module is `VERIFICATION`; it is the only module
in the local closure. The result contains 18 rules in source order, with:

- frozen `verification.k` SHA-256
  `cff7fa18bbc3131014865e83f3d8ab7fb295dbf5c309646b1cf45f6d7d6aae7f`;
- inventory SHA-256
  `0d5fe23d9dedd3ad555afbe0aa1bed145a5c21efee172628c5584122321912a3`.

For every entry, the reconstruction supplies its exact line span, normalized
source hash, and `rule-<normalized_sha256>` identity. The Stage 3 manifest has
the same 18 identities in exactly the same order. There are no omitted,
duplicated, extra, reordered, or hash-divergent rules. The complete
reconstruction is in `evidence/02_inventory_check.log`.

My independent classification is:

| Class | Count | Judgment |
|---|---:|---|
| `DEFINITION` | 15 | Three exact translated-body macros; two structural `intsVS` equations; and the base/recursive equations for `nextRolling`, `rollingAcc`, `firstAfter`, `maximumAfter`, and `numberAfter`. |
| `OPERATIONAL_RULE` | 2 | The empty and nonempty iterator observations, which respectively produce `#iterDone` and `#iterYield` in the active `<k>` cell. |
| `PROVED_DERIVED_LEMMA` | 0 | Stage 1 contains no qualifying prove-before-use rule. |
| `DOMAIN_LEMMA` | 1 | `firstAfter(_IS:IntSeq, false) => false` at line 65. |

The full per-rule assessment is in
`evidence/05_classification_assessment.md`. No inventory rule has an explicit
`simplification` attribute, so no simplification rule is misclassified.

The line-65 rule is correctly a `DOMAIN_LEMMA`, not a definition or a proved
derived lemma. The structural definition is supplied separately:

```k
rule firstAfter(.IntSeq, F:Bool) => F
rule firstAfter(iCons(_I:Int, _R:IntSeq), _F:Bool) => false
```

The sequence-independent false-flag rule follows by those two cases. However,
`prove.sh` compiles `verification.k` containing the rule and only then invokes
the sole `kprove`; Stage 1 never first proves the exact rule in a module that
omits it. It therefore cannot qualify as `PROVED_DERIVED_LEMMA`.

The domain lemma is true and relevant. The source initializes `first = True`,
sets it to `False` on the first iteration, and never restores it. The loop claim
tracks the final local binding as `firstAfter(INPUT,FIRST)`. After a symbolic
head, the recursive invariant needs exactly
`firstAfter(REST,false) = false`. It is therefore tied directly to the source
loop and the end-to-end correctness proof, not an unrelated mathematical fact.

## Deterministic Stage 4 generation

I reran the required function with `PYTHONPATH=/reference`:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

The returned evidence is `PASS`, has one obligation, has zero designated
sorries, reports 47 generated trust declarations, and exactly equals both the
recorded `preflight.json` and `resolution.stage4_preflight`. Its internal
`lake clean` and `lake build` both exit 0. See
`evidence/03_preflight.log`.

Independent manifest and sidecar checks in
`evidence/04_stage4_integrity.log` establish:

- frozen Stage 1, Stage 3, inventory, verification, generated-tree,
  trust-inventory, toolchain, and export-result hashes all agree;
- the sole independently classified domain rule is the sole source rule and
  sole generated obligation, in the same order and without duplication;
- its source span is exactly line 65 and all inventory/discovery/normalized
  hashes agree;
- `obligation-map.json` has SHA-256
  `27c31199967810f9b4dbbf568e892f7bb53a87f92468a72bd59731148c1a7784`;
- the Lean conjunct is exactly:

```lean
∀ (_IS : SortIntSeq),
  («firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» _IS false : SortBool)
    = (false : SortBool)
```

This is an exact translation of the frozen domain lemma. It is not weakened or
vacuous: `SortIntSeq` is inhabited by its empty constructor, and a parameter
returning `true` at flag `false` falsifies the proposition. The obligation
does not purport to characterize the parameter on all arguments; the separate
operational-bridge audit below checks that boundary.

The generated target is the exact one-conjunct definition, with no extra or
missing target:

- declaration: `Klean9RollingMax.Lemmas.targetStatement`;
- definition hash:
  `a2dc84673e2d014fbca47e43cf3d49c73bfc8818aa9e979e22435b64da93dcfb`;
- fixed statement:
  `Klean9RollingMax.Lemmas.targetStatement «firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool»`;
- statement hash:
  `d6f0a66e3f297a56c876e01bc1244f9603d129257224147f3a2d989a302d23c6`;
- parameter-binding hash:
  `184a865567ffa39decd72c890c4362864e7fb971165a476a790c1c86434ad6e0`.

The target, statement, hashes, KORE symbol, parameter type, and bound source ID
agree across the obligation map, generator manifest, recorded preflight, and
audit input.

## Stage 5 proof, identity, and trust

I created `/tmp/audit-work/stage5-fresh`, copied the generated project into it
as `Base`, and copied only the candidate source/dependency metadata into the
fresh root. Before execution:

- the fresh `Base` tree exactly matched the selected generated tree;
- all candidate entries were regular files or directories;
- the candidate source hashes matched the mounted candidate;
- the candidate did not define or shadow `targetStatement`;
- it defined the one required parameter exactly once and `Proof.final`
  exactly once;
- no candidate source contained `sorry`, `admit`, `unsafe`, a new `axiom`, or
  a new `opaque`.

The static record is `evidence/07_candidate_static.log`.

The required fresh commands both succeed:

```text
lake clean    # exit 0
lake build    # exit 0
```

After `lake clean`, the generated package's absolute build directory was
absent, confirming the build was not reusing its prior output. The complete
build output in `evidence/09_lake_build.log` ends with:

```text
✔ [3/8] Built Klean9RollingMax.Prelude
✔ [4/8] Built Klean9RollingMax.Sorts
✔ [5/8] Built Klean9RollingMax.Inj
✔ [6/8] Built Klean9RollingMax.Lemmas
✔ [7/8] Built Proof
Build completed successfully.
```

`#print Proof.final` confirms its type is exactly:

```lean
Klean9RollingMax.Lemmas.targetStatement
  Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool»
```

It is not a copied, weakened, or vacuous theorem. The printed declaration is in
`evidence/12_print_proof.log`.

Running Lean with the required command `#print axioms Proof.final` produces
exactly:

```text
'Proof.final' does not depend on any axioms
```

The generated project has 47 axiom/opaque trust declarations, and the
declaration set exactly equals the 47-entry `trust-inventory.json` allowlist.
None is reachable from `Proof.final`; `sorryAx` is absent, there are no
unrecorded dependencies, and the candidate adds no trust declaration.
See `evidence/10_print_axioms.log` and
`evidence/14_trust_reconciliation.log`.

The trusted end-to-end final mechanical gate independently repeats preflight,
fresh clean/build, exact-type checking, and axiom printing. It returns `PASS`,
the signed input hashes, the fixed target, and `used_axioms: []` in
`evidence/13_final_mechanical_gate.log`. Its
`semantic_classification: NOT_EVALUATED` is expected: the mathematical
classification and bridge judgments are the independent audit work documented
here.

## Operational bridge

The candidate's exact parameter definition is:

```lean
def «firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» :
    SortIntSeq → SortBool → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», flag => flag
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _, _ => false
```

This matches the two frozen structural `firstAfter` rules over the complete
`SortIntSeq × Bool` domain and matches the source loop's flag behavior. The
compiled adversarial audit proves universally, by cases on input and flag,
that the generated Option-valued K function returns `some` of the candidate's
value for every input.

The fixed target alone admits convenient bad implementations, so I tested
them explicitly:

- constant-false proves the target but disagrees with frozen empty/true;
- identity-on-flag proves the target but disagrees with frozen
  nonempty/true.

Both counterfactual target proofs and both disagreement witnesses compile.
The actual candidate passes empty/true, empty/false, singleton/true,
singleton/false, a multi-element witness, and the universal comparison. It is
therefore neither constant, identity, hard-coded, nor operationally vacuous.
The checked file and judgment are
`evidence/BridgeAudit.lean` and
`evidence/15_operational_bridge_assessment.md`.

## Reproduction note

The container exposes `/proc/self/exe` but its PID namespace does not reliably
expose Lean's `/proc/<getpid()>/exe`. The first raw preflight/build attempts
therefore failed before compilation with Lake application-path detection
errors. I used the auditable shim in
`evidence/proc_self_exe_shim.c`, which only maps numeric
`/proc/<pid>/exe` reads to `/proc/self/exe`, and copied the pinned Lean/Lake
launchers into an audit-local overlay. Hashes show those launchers are
byte-identical to the pinned toolchain. Lean then reports version 4.22.0,
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock and generator
manifest. Repeated preflight, clean builds, proof checks, and the trusted final
gate all succeed under that compatibility setup. The initial failures remain
preserved as raw evidence.

## Conclusion

The Stage 3 manifest is a bijective, correctly ordered classification of the
frozen verification-rule closure. Its one domain lemma is valid and relevant.
Stage 4 deterministically exports exactly that obligation and the fixed target
without weakening or omission. Stage 5 proves that target with an axiom-free
proof and supplies an operationally faithful total definition for its sole
parameter.

VERDICT: PASS
LEGITIMACY: LEGIT
