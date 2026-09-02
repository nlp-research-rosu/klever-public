# Independent Stage 3–5 audit: 157-right-angle-triangle

## Scope and result

The launcher and environment both select:

- problem: `157-right-angle-triangle`
- condition: `bare`
- semantics mode: `GENERATED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

I treated the mounted Stage 1–5 artifacts, prior audit, manifests, logs,
comments, and rationales as untrusted evidence. I did not adopt the selected
Stage 2 verdict or the protected Stage 3 labels. The prior K audit was used
only as a tree whose launcher-recorded hash had to be checked.

The independent result is that the local verification-module closure contains
exactly two rules. Both are genuine definitions. There is no domain lemma, so
the empty Stage 4 obligation set, absent generated target, and absent Stage 5
candidate are correct.

## Producer provenance gate

I checked producer provenance before evaluating Stage 4. The observed hashes
are:

| Producer artifact | SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |
| producer-source bundle, using the launcher contract | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

Both file hashes equal the values in `source-manifest.json` and
`generator-manifest.json`. The bundle hash equals `/audit-input.json`. The
immutable image ID is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest and generator manifest, and is the image-key component
of the producer-source path recorded in `/audit-input.json`.

The complete check is in
`evidence/04d-producer-integrity-correct-contract.log`. An earlier diagnostic
in `evidence/04-producer-integrity.log` used the unrelated Stage 1 audit-tree
hash framing and is superseded; inspection of the launcher source established
that producer bundles use `tools.pipeline_contract.sha256_tree`, after which
every producer check passed.

## Frozen-input and manifest integrity

I recomputed every resolution tree/file hash, every listed Stage 1 source-file
hash, the resolved-input digest, the selected-artifact bindings, and the
relevant Stage 4 sidecar hashes. All comparisons passed. Important values
include:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 export tree | `8db7cccaf0b95cc092e258a2253f4a6bbd33472c41614be2efc5c742e42768da` |
| selected Stage 1 workspace tree | `cb3c8a89d5423cb96504d8b8e31c3741fbb0d3c8041c783c448c44c6f6e5ef1f` |
| `verification.k` | `f991f273eb7ffb565b8f0956150c1843ccccbe8a25bf61577e86d0b30d0f9836` |
| Stage 3 discovery manifest | `e1749edafdc600db7f40d9c5090f030f30afa149171d9cf12f7b96110602a97e` |
| generated Lean tree | `8736fb2c191115092ea856f59610ee40e7a14f31f4cd8e78203ac61a3f764f3d` |
| selected Stage 4 generation tree | `7b797bb246d45a6ab2c17f37368ff4d1d358c99aae464cf6959d73a595de970b` |
| obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| trust inventory | `432d50bc33d619d7ae08bd6dbff7ab3b11137a9664b65951f48fcf6f5178b3f6` |

The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`. The complete recomputation is in
`evidence/18-complete-recorded-hash-verification.log`.

## Independent rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` on the frozen
Stage 1 workspace and separately reconstructed its results from the two outer
`rule` sentences in `verification.k`. `prove.sh` selects `VERIFICATION`.
Within `verification.k`, its local module closure is only `VERIFICATION`;
`MPY` is supplied by the separately required `semantic.k` and was inspected
for operational meaning, not incorrectly added to the local
`verification.k` rule inventory.

The reconstructed inventory, in source order, is:

| Span | Normalized SHA-256 / source rule ID | Rule |
|---|---|---|
| lines 8–14 | `d1a23396f61dd26b11833b39066cbd64b498e0dfb07eaea1e6c090daaa0b0893` / `rule-d1a23396f61dd26b11833b39066cbd64b498e0dfb07eaea1e6c090daaa0b0893` | `rightTriangle(A, B, C) => ...` |
| lines 19–47 | `4fee0a7dc4c0172c3b675bff411434ca46c778b577d492797129b2328534b07a` / `rule-4fee0a7dc4c0172c3b675bff411434ca46c778b577d492797129b2328534b07a` | `solutionProgram => Module(...)` |

For each span I normalized with single whitespace between tokens and hashed the
normalized text. I then canonical-JSON-hashed the two complete rule records.
The resulting inventory hash is
`a884f8ef58b1e8a15f0626a1551c3d76fe8c2d4cbcb350700cbc4602131edab0`.

The protected Stage 3 manifest contains exactly those two IDs, once each, in
that order, and carries the same whole-inventory hash. There are no omissions,
duplicates, extra IDs, reordered identities, altered spans, or altered hashes.
Raw reconstruction is in `evidence/05-reconstructed-inventory.json`; the
manual span/hash and bijection checks are in
`evidence/10-inventory-bijection-and-classification.log`.

## Independent Stage 3 classification

### `rightTriangle`

Classification: `DEFINITION`.

Line 7 declares the total function
`rightTriangle(Int, Int, Int) : Bool`. The rule at lines 8–14 is its defining
equation: it unfolds the name to positivity of all three sides and the
disjunction of the three possible Pythagorean orientations. It defines the
mathematical postcondition summary used in `spec.k`; it does not state an
additional mathematical fact about a previously defined summary.

It is not an operational rule: `rightTriangle` does not occur in
`semantic.k` and does not replace `run`, binding, expression evaluation,
control, state, or result publication. It is not a proved-derived lemma:
there is no earlier proof of this rule against a module omitting it. It is not
a domain lemma because it is the direct defining equation for the named
summary.

### `solutionProgram`

Classification: `DEFINITION`.

Line 18 declares the nullary function `solutionProgram : Program`. The rule at
lines 19–47 expands that name to the exact `Module(FuncDef(...))` AST of the
frozen translated solution. Whitespace-normalized comparison confirms that its
right-hand side is exactly `solution.mpy`.

This equation names a proof/program term; it does not summarize or bypass
execution. After it unfolds, the fixed operational rule in `semantic.k`
matches the module and entry point, binds `a`, `b`, and `c`, evaluates the
complete body through `eval`, and publishes the resulting Boolean. It is
therefore neither an operational bridge nor an ordinary operational rule. No
earlier derivation makes it a proved-derived lemma, and it is not a domain
lemma.

Neither inventory rule has a `simplification` rule attribute. The `function`
and `total` annotations belong to the `rightTriangle` syntax declaration, not
to a simplification rule. Thus the requirement that every simplification rule
be a definition or domain lemma is satisfied vacuously.

The independently determined class counts are:

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

These independently determined labels match Stage 3 exactly.

## Program and operational-semantics judgment

The frozen Python function returns true exactly when all sides are positive and
one of the three squared-side equalities holds. The translated AST in
`solutionProgram` contains the same four-way conjunction and three-way
disjunction. The generated K semantics uses unbounded K integers for the
source integer operations and evaluates the pure arithmetic, comparisons, and
Boolean operands before publishing the Boolean result.

I parsed `solution.py` as data with Python's AST library and evaluated only an
explicit allowlist of integer, comparison, and Boolean AST nodes; I did not
execute the candidate source. Representative and adversarial inputs included
the three hypotenuse positions, non-triangles, zeros, negative sides, a scaled
triple, and values above 32-bit range. The source AST and `rightTriangle`
summary agreed on every case. Counterfactual mutations were discriminating:
removing positivity changes `(0,0,0)` and `(-3,4,5)`, while retaining only the
first Pythagorean orientation changes `(5,3,4)`.

These finite examples supplement, rather than replace, the structural
comparison of the exact source AST, defining equation, and operational K
rules. Full details are in
`evidence/16-definition-operational-semantics.log`.

## Deterministic Stage 4 generation

Because the independently classified domain set is genuinely empty, the exact
expected source-rule and obligation sequences are both empty. The immutable
Stage 4 artifacts contain:

- `input-manifest.json.source_rules = []`;
- `obligation-map.json.source_rules = []`;
- `obligation-map.json.obligations = []`;
- `obligation-map.json.trust_parameters = []`;
- generator, export, recorded-preflight, and audit obligation counts of zero.

The empty source/obligation mapping is bijective: there is no omitted,
duplicated, irrelevant, weakened, or reordered obligation. With no conjuncts,
there is also no vacuous conjunct masquerading as an obligation.

The fixed target is absent everywhere:

- `generator-manifest.json.target` is null;
- `preflight.json.target` is null;
- both target fields in `/audit-input.json` are null;
- `tools.klean_export.expected_target_definition` returns null;
- `tools.klean_export.target_statement` returns null;
- an independent scan finds no `def targetStatement` in any generated Lean
  source.

`Lemmas.lean` contains only its imports and empty namespace. `/candidate` is
absent. The exact empty-bijection and target checks are in
`evidence/14-zero-obligation-bijection-and-target.log`.

## Required preflight rerun

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required Stage 1 workspace, Stage 3 manifest,
Stage 4 generation, and trusted toolchain lock.

The first attempt reached the fresh-copy build gate but exposed an audit
sandbox compatibility issue: Lean 4.22 resolves its executable by reading
`/proc/<getpid()>/exe`, while this sandbox's mounted `/proc` uses the outer PID
namespace. This caused `IO.appPath` to fail before Lean read any generated
source. Evidence of the namespace mismatch and Lean implementation is in
`evidence/11u-proc-pid-diagnosis.log` and
`evidence/11s-lean-app-path-disassembly.log`.

I compiled an audit-local preload shim that redirects only numeric
`/proc/<pid>/exe` `readlink` requests to the equivalent `/proc/self/exe`.
Its complete source and build/test output are
`evidence/proc_self_exe_shim.c` and
`evidence/11w-proc-shim-build-and-test.log`. With that environment-only
compatibility correction, the unchanged trusted preflight returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0;
- build-output SHA-256
  `e6271e088825ceb9e0c91940a9ebc7d99b5c5e3571df2c10101f235048d9ab6c`;
- obligation count 0;
- target null;
- generated-tree SHA-256
  `8736fb2c191115092ea856f59610ee40e7a14f31f4cd8e78203ac61a3f764f3d`;
- designated sorry count 0.

The complete returned evidence is
`evidence/12-rerun-klean-preflight-with-proc-shim.log`. A second comparison run
confirmed that the returned object exactly equals both
`/audit-input.json`'s Stage 4 preflight and the immutable
`preflight.json`; see `evidence/15-preflight-exact-comparison.log`.

## Stage 5 disposition

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`. This is the
required mode for a legitimate `KLEAN_NO_OBLIGATIONS` result. The audit input
has no Lean workspace, Lean invocation, target, or Stage 5 result, and the
`/candidate` mount is absent. There are no target parameters and hence no Lean
operational-bridge definitions to audit. This review makes no claim that a
Stage 5 theorem was proved; correctly, no such theorem exists.

## Conclusion

The frozen rule inventory is complete and bijective with Stage 3. Both rules
are definitions under their actual semantic roles. The true domain-lemma set
is empty. Producer provenance, all relevant hashes, deterministic Stage 4
manifests, the empty obligation mapping, target absence, and the required
fresh preflight build all check out. The classification-only, no-obligation
result is legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
