# Independent audit: `54-same-chars`

## Scope and result

This audit covers HumanEval problem `54-same-chars`, condition `semantics`,
semantics mode `SUPPLIED_SEMANTICS`. Both `/audit-input.json` and
`AUDIT_MODE` select `CLASSIFICATION_ONLY`. The signed resolution envelope
recomputes to its recorded digest, and the environment mode agrees with it.

I treated the mounted Stage 1–4 artifacts, previous audit, logs, comments, and
classifications as untrusted evidence. I used the trusted inventory and
preflight implementations under `/reference/tools` and made the semantic
classification directly from the frozen program and supplied K semantics.

The result is legitimate. The local verification closure contains one rule,
that rule is an honest definition of a fresh named proof term, and the true
domain-lemma set is empty. Consequently, `KLEAN_NO_OBLIGATIONS`, a null
generated target, and the absence of a Stage 5 candidate are all correct.

## Inventory reconstruction and Stage 3 bijection

I reconstructed the inventory with
`tools.k_rule_inventory.inventory_verification` using the frozen
`/reference/k-proof` workspace. `prove.sh` selects
`SAME-CHARS-VERIFICATION` as the main module. The local module closure inside
`verification.k` is exactly:

- `SAME-CHARS-VERIFICATION`

The reconstruction contains exactly one rule:

- Source span: `verification.k` lines 10–23
- Module: `SAME-CHARS-VERIFICATION`
- Attributes: none
- Normalized SHA-256:
  `64ab866119ef68aee7112f09de97735afd57399d3ba18fb6463d8b22a673c966`
- Source rule ID:
  `rule-64ab866119ef68aee7112f09de97735afd57399d3ba18fb6463d8b22a673c966`

The extracted line span exactly equals the inventory text. Independently
normalizing whitespace and hashing that span reproduces both the normalized
hash and the hash-bearing source rule ID. The complete ordered-rule inventory
hash is:

`c1534c6113c88c0bb5b2530edcf8c3dbb61b692426c714be2d9eb96085fc2610`

The Stage 3 manifest has exactly that inventory hash and exactly that one
source rule ID in the same order. The identity is unique. There are no omitted,
duplicated, extra, reordered, or hash-changed rules. The trusted Stage 3
contract also validates the manifest and partitions it as one `DEFINITION`,
zero `OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and zero
`DOMAIN_LEMMA`.

Raw reconstruction and comparison are in
[`evidence/01_inventory_reconstruction.log`](evidence/01_inventory_reconstruction.log);
the independently written checking program is
[`evidence/inventory_audit.py`](evidence/inventory_audit.py).

## Independent rule classification

The sole rule rewrites the fresh syntax
`#sameChars(S0:IntSeq, S1:IntSeq)` to a call of a closure with:

- parameters `s0` and `s1`;
- lexical parent scope `0`;
- arguments `str(S0)` and `str(S1)`; and
- body `return set(s0) == set(s1)`.

This is exactly the constructor-level content of the frozen `solution.mpy`,
which in turn matches the frozen source:

`def same_chars(s0, s1): return set(s0) == set(s1)`.

The rule is a `DEFINITION`, specifically a macro-like definition of a named
proof entry term. Its left side is newly declared in `verification.k`; it is
not an existing source-program `Call`, name lookup, comparison, or semantic
operation that the rule preempts.

After this one expansion, the supplied operational semantics still performs
all program behavior:

1. `Call` evaluates the closure and arguments.
2. Closure application creates a frame and binds `s0` and `s1`.
3. `Name("set")` resolves through the lexical parent to the builtins scope.
4. Each set call executes
   `applyBuiltin("set", str(CS), .Vals) => setV(dedupCodes(CS))`.
5. `Compare` dispatches to `applyCmp`.
6. Set equality executes
   `applyCmp("==", setV(A), setV(B)) => sameSet(A, B)`.
7. `Return` stores the value, pops the frame, restores the caller
   environment, and resumes the continuation.

Thus the local rule neither states a mathematical domain fact nor replaces an
operational result with a convenient summary. It is not an ordinary
observation/execution rule, and Stage 1 does not claim it as a separately
proved derived lemma. It has no `simplification` attribute. The Stage 3
classification is therefore correct under all category constraints.

The `dedupCodes`, `subsetCodes`, and `sameSet` equations are part of the frozen
supplied semantics, not local proof extensions in the verification-module
inventory. There is no local domain lemma relevant to export. Source and
semantic excerpts are preserved in
[`evidence/02_classification_sources.log`](evidence/02_classification_sources.log).

## Generation-time producer provenance

Before judging Stage 4, I hashed the mounted generation-time sources:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Both hashes exactly match `generator-manifest.json` and
`source-manifest.json`. The source manifest contains exactly those two
producer files, plus the manifest itself, with no linked or unsupported
entries. Its generator image ID is:

`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`

That ID agrees with the generator manifest and with the image-key directory
recorded in `/audit-input.json`. The producer-bundle tree hash is:

`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`

It exactly matches the audit input. There is no producer-provenance
infrastructure error. See
[`evidence/03_producer_provenance.log`](evidence/03_producer_provenance.log)
and
[`evidence/producer_provenance_audit.py`](evidence/producer_provenance_audit.py).

The hash-verified generation-time code selects only validated
`domain_lemmas` as source rules, checks their ordered bijection with emitted
KORE/Lean obligations, emits `targetStatement` only when propositions are
nonempty, and selects `KLEAN_NO_OBLIGATIONS` exactly when the obligation list
is empty. Relevant producer and generated excerpts are in
[`evidence/07_generation_zero_domain_path.log`](evidence/07_generation_zero_domain_path.log).

## Stage 4 hashes, obligations, and fixed target

I independently recomputed all resolution artifact hashes using their
recorded hash schemes:

- Stage 1 workspace tree:
  `2f292394c89b1fd17ad12ae6b59fb8644646b7591a19815b7be7e006b2d8e0ed`
- Stage 1 export/frozen-input tree:
  `6911a8d77c9e982ca8633dc88f88d64c507f1ebd7aef999b65e7c48b33acb3eb`
- Selected Stage 2 audit tree:
  `fcf1093996ab53d9ff7826dabf4938fb39be1b2bf84cbe7af14b6f1050e6065b`
- Stage 3 manifest:
  `e63889f1ad8996794b994e5fa5adbc24fa4ef8aa4048b3502738d7110283d4e4`
- Selected Stage 4 generation tree:
  `88b8849403de19994754238af22d717f3fead23fee10b0684c7c84a880ab419f`
- Generated Lean project tree:
  `a69c207c67dbcf1070c28a0b357a4a391fbc1246f4d9d5fe401ee6d01a13eea5`

All 34 individually recorded Stage 1 source-file hashes also match exactly.
The generator/input/export manifests bind the same frozen input, Stage 3
manifest, inventory, `verification.k`, generated tree, obligation map, and
trust inventory. The preflight document mounted with Stage 4 is byte-content
equivalent to the copy signed into the audit input; each stored command-output
hash reproduces from its complete stored output.

The independently classified domain set, Stage 4 input source rules, generated
source rules, and generated obligations are all the same empty ordered list.
There are no duplicate obligations, trust parameters, conjuncts, omissions,
weakenings, or irrelevant additions. Apart from its schema version, the
obligation map's substantive lists are exactly:

`{"source_rules": [], "obligations": [], "trust_parameters": []}`

The generator manifest, preflight, export result, and signed audit input all
record zero obligations and `KLEAN_NO_OBLIGATIONS`. Independent target
extraction returns `null`; expected target generation returns `null`; the
generated Lean tree contains zero `def targetStatement` declarations.
Therefore the fixed generated target is correctly absent rather than changed,
weakened, duplicated, or made vacuous.

The complete checks are in
[`evidence/06_stage4_integrity.log`](evidence/06_stage4_integrity.log);
the audit program is
[`evidence/stage4_integrity_audit.py`](evidence/stage4_integrity_audit.py).

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required Stage 1, Stage 3, Stage 4, and
toolchain-lock paths.

The first invocation reached the build gate but exposed an audit-runner PID
namespace issue: Lean 4.22 asks for `/proc/<getpid()>/exe`, while this runner
mounts `/proc` from another namespace. The failed raw attempt is retained in
[`evidence/04_preflight_rerun.log`](evidence/04_preflight_rerun.log).

I used the narrow compatibility shim in
[`evidence/proc_exe_compat.c`](evidence/proc_exe_compat.c), which redirects
only `/proc/<pid>/exe` reads to the equivalent `/proc/self/exe`. It does not
alter the generated project, Lean source, proof terms, imports, or checker
logic. With that environment correction, the trusted preflight returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, all generated modules built successfully;
- obligation count 0;
- target `null`;
- designated sorry count 0; and
- the expected frozen-input, discovery, and generated-tree hashes.

The successful returned evidence is
[`evidence/05_preflight_rerun_with_proc_compat.log`](evidence/05_preflight_rerun_with_proc_compat.log).
The rerun build-output hash differs from the earlier stored run only because
the independent `Func` and `Lemmas` modules completed in the opposite order;
the generated tree and every structural binding are unchanged.

## Stage 5 applicability

Stage 5 is correctly absent. `/candidate` does not exist, the signed Lean
workspace and invocation hashes are null, the Stage 5 result is null, and
there is no generated target to prove. Clean candidate build, `Proof.final`,
axiom accounting, and operational-bridge parameter checks are therefore not
applicable in this `CLASSIFICATION_ONLY` audit. Their absence is required by
the genuine empty domain set and is not missing proof evidence.

## Evidence index

- Exact supporting commands:
  [`evidence/COMMANDS.md`](evidence/COMMANDS.md)
- Initial mode and independent hashes:
  [`evidence/00_context_and_producer_hashes.log`](evidence/00_context_and_producer_hashes.log)
- Inventory reconstruction:
  [`evidence/01_inventory_reconstruction.log`](evidence/01_inventory_reconstruction.log)
- Frozen source and operational semantics:
  [`evidence/02_classification_sources.log`](evidence/02_classification_sources.log)
- Producer provenance:
  [`evidence/03_producer_provenance.log`](evidence/03_producer_provenance.log)
- Initial environment-failed preflight:
  [`evidence/04_preflight_rerun.log`](evidence/04_preflight_rerun.log)
- Successful trusted preflight:
  [`evidence/05_preflight_rerun_with_proc_compat.log`](evidence/05_preflight_rerun_with_proc_compat.log)
- Independent hash, bijection, and target audit:
  [`evidence/06_stage4_integrity.log`](evidence/06_stage4_integrity.log)
- Generation-time zero-domain path:
  [`evidence/07_generation_zero_domain_path.log`](evidence/07_generation_zero_domain_path.log)

VERDICT: PASS
LEGITIMACY: LEGIT
