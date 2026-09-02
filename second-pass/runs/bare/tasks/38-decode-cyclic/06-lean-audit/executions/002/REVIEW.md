# Independent Stage 3–5 audit: `38-decode-cyclic`

## Result

The Stage 3 classification and the structural Stage 4 export are internally
consistent and mathematically correspond to the three frozen proof-only
simplifiers. The Lean project also clean-builds, proves exactly the immutable
target, and has a clean accounted axiom list.

The proof is nevertheless not legitimate. Two candidate definitions do not
implement their bound KORE symbols: frozen K v7.1.293 indexes strings by UTF-8
bytes, while the candidate indexes Lean strings by Unicode scalar values. This
changes both `lengthString` and `substrString` on ordinary non-ASCII source
inputs and is an operational-bridge failure under the requested decision rule.

## Scope and input integrity

`AUDIT_MODE` and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF`, condition `bare`, and semantics mode
`GENERATED_SEMANTICS`. The resolved-input digest recomputes to
`606dfaee1e3b5cdadaef09a9a374743d11c62c29cf616c4a94bcd81e9a22d86a`.

Every launcher-bound hash whose artifact is mounted recomputes exactly:

- Stage 1 pipeline tree:
  `f600725fab73470246ba886f9bf3af31bb1d72edca63918399cd60d871f1bc73`;
- Stage 1 export tree:
  `2db69dd3a57605c6a212cedbe401470040ad29a65b7c00f27b9d286bb5ff3dff`;
- Stage 2 audit tree:
  `a257592abdcfea9cecf9efce51a1e29a1d4b0b62342fc318f65a57761a25e6b2`;
- Stage 3 manifest:
  `b5ecfd0e5ad951679b77e881ccf86470d4328205da3f2ef238dd9e8061ae5fb8`;
- Stage 4 generation tree:
  `b2d2ee67e50006a244f35eb09575bb7d232056e23540da53b9692b35bbb93ae3`;
- generated project:
  `9a729bf9e6da030fc7c4fe7790160f24365d0a04642cc6ab149786aecce5bd8d`;
- Stage 5 workspace:
  `a929657b8239498ed485be3c9e954f9a039afb0ed52126cda7d71f68f6c0038e`.

All ten recorded Stage 1 source-file hashes match. The obligation-map and trust
inventory hashes also match their manifests. The Stage 5 invocation tree is
not mounted, so its launcher-recorded digest cannot be independently
recomputed; this does not affect the mounted candidate-tree check.

There is a separate provenance shortfall: the generation-time producer
fingerprints recorded in `generator-manifest.json` do not identify the mounted
current tools. The recorded/observed pairs are:

- `exporter_sha256`:
  `4fa919ac...` / `0c18ea79...`;
- `klean_py_sha256`:
  `b8bcddc0...` / `92e9515a...`.

No mounted file has either recorded producer digest. This does not change the
successfully verified generated-tree and sidecar identities, but those two
recorded generation-time code hashes are not independently accountable from
the supplied mounts. Full details are in
`evidence/13-hashes-and-target.json`.

## Inventory reconstruction and Stage 3 classification

The trusted inventory code selects `VERIFICATION` from `prove.sh`. Its local
module closure inside frozen `verification.k` is exactly `["VERIFICATION"]`.
It reconstructs exactly three rules, in physical order:

| Span | Source rule | Independent classification | Reason and relevance |
|---|---|---|---|
| 9–11 | `rule-ef7d5d...` | `DOMAIN_LEMMA` | Cancellation/injectivity of equal updates at one map key. It defines no summary and is not an execution rule. The program's assignment rule updates `<env>` with this very map operation, so it is relevant to symbolic execution. |
| 13 | `rule-aa08fc7a...` | `DOMAIN_LEMMA` | Nonnegativity of the K string-length hook. It defines no named term and is used by the loop guard and invariant bounds. |
| 14 | `rule-6a69a835...` | `DOMAIN_LEMMA` | Full-range substring identity. It defines no named term and is relevant to the decoder's slice/tail rules and base case. |

All three carry `[simplification]`, so the allowed classifications are
`DEFINITION` or `DOMAIN_LEMMA`. None is a definition: no rule introduces a
summary, recurrence, macro, or named proof term. None is operational: no rule
steps the `<k>`, `<env>`, or `<result>` cells. None is
`PROVED_DERIVED_LEMMA`: Stage 1 has one later `kprove` call and contains no
earlier proof of any exact rule against a module omitting it.

For each rule, the physical source span exactly reproduces the inventoried
text, SHA-256 of whitespace-normalized text equals the recorded normalized
hash, and `source_rule_id` is exactly `rule-` plus that hash. The whole
canonical inventory hash is
`d2db99b7bfbb6f10173dc29736d6dd1020fae34b484b232cc0ed4a77b679becb`.
The Stage 3 manifest has the same three identities in the same order, with no
duplicates, omissions, extras, or unaccounted classifications. See
`evidence/01-reconstructed-inventory.json` and
`evidence/03-inventory-bijection.json`.

## Deterministic Stage 4 generation

The first required preflight attempt exposed a sandbox-only toolchain issue:
the sandbox virtualizes `getpid()` but `/proc` exposes a different PID
namespace, while Lean 4.22 implements `IO.appPath` as
`/proc/<getpid()>/exe`. A local preload shim made `getpid()` return the
identifier exposed by `/proc/self`; it changed no source, target, proof, or
hash. With that environment repair, the exact required call to
`tools.klean_preflight.check_generation` returned `PASS`, built the immutable
generated project, and reported three obligations.

The obligation bijection is exact and ordered:

1. map-update cancellation becomes the substantive forward implication plus
   its trivial converse, expressed as one `↔`;
2. `0 <=Int lengthString(S) => true` becomes equality with Lean `true`;
3. the full-range substring rewrite becomes equality with `S`.

The three conjuncts are universally quantified, nonempty, and contain the
expected symbols. There is no omitted rule, duplicate obligation, irrelevant
new obligation, changed guard, weakened conclusion, `True` placeholder, or
generated target substitution. The domain set is genuinely nonempty, so the
no-obligation path does not apply.

The unique target recovered from generated source is:

- declaration:
  `Klean38DecodeCyclic.Lemmas.targetStatement`;
- definition hash:
  `7bba40a4a2892d50612192343a8e7d8226c3ab93278ca4a4d062e68a5dc1b835`;
- applied statement hash:
  `32a2ae8e9350f6d65d01c27776f3613cdd40397f360a1a8e886b85a2cf20fd80`.

It equals the generator manifest, Stage 4 preflight record, audit input, and
the exact conjunction reconstructed from `obligation-map.json`. The four
parameter binding hashes also recompute. Mechanical evidence is in
`evidence/04b-check-generation.json` and
`evidence/13-hashes-and-target.json`.

## Stage 5 proof identity and trust

A fresh project was made below `/tmp/audit-work`; the generated project was
copied into it as `Base`. From that project:

```text
$ lake clean
EXIT_CODE=0
$ lake build
...
Built Proof
Build completed successfully.
EXIT_CODE=0
```

The full output is `evidence/06b-stage5-clean-build.log`. The candidate
contains exactly one definition for each required parameter, does not define
or shadow `Klean38DecodeCyclic.Lemmas.targetStatement`, and contains no
`sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. `Proof.final` states
the manifest's applied target exactly; it is not a duplicate or weakened
variant.

The exact Lean output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`sorryAx` is absent. None of the 44 generated declarations in
`trust-inventory.json` is used. The three reported names are the standard Lean
core principles explicitly permitted by the trusted final-gate policy, and
there is no unrecorded or candidate-added proof escape. See
`evidence/08-print-axioms.log` and
`evidence/15-axiom-reconciliation.json`.

## Operational-bridge audit

The candidate definitions were compared with their bound KORE symbols, frozen
rules, source operations, and executable K hooks.

`Proof.«_<=Int_»` uses Lean integer order and agrees with K on negative,
equal, and false cases (`-2 <= -1`, `3 <= 3`, and not `3 <= 2`).

`Proof.«Map:update»` removes prior entries at the key, prepends the replacement,
and preserves other bindings. On valid no-duplicate K maps it agrees with K
for empty insertion, replacement, and replacement while preserving another
key. The candidate representation is order-sensitive, unlike abstract K map
equality, but no counterexample was found on the valid generated
`SortMap` representation used by these obligations.

The two string bindings fail:

| Probe | Frozen K hook | Candidate Lean definition |
|---|---|---|
| length of `"😀"` | `4` UTF-8 bytes | `1` Unicode scalar |
| length of `"é"` | `3` UTF-8 bytes | `2` Unicode scalars |
| substring of `"a😀b"` at `[1,2)` | `"\xf0"` (first UTF-8 byte) | `"😀"` |
| substring of `"a😀b"` at `[0,3)` | `"a\xf0\x9f"` | `"a😀b"` |

These are direct executions of a fresh K module importing the same `INT`,
`STRING`, and `MAP` domains, compared with direct evaluation of the exact
candidate definitions. Complete output is in
`evidence/10-k-hook-probe-results.log` and
`evidence/11d-lean-all-bridge-probe-results.log`.

The mismatch is material to the frozen program, not an unused totalization
choice. The source loop tests `i + 2 < len(s)` and then indexes and slices the
same string. For a one-scalar, four-byte emoji, byte length makes the frozen K
loop enter while the candidate length is `1`; the substring meanings then
also diverge. Thus the candidate's convenient Unicode-scalar definitions
prove the equations without implementing the frozen operational meaning.

As an additional sensitivity test, deliberately dishonest definitions—
always-true integer comparison, map update that discards the rest of the map,
constant-zero length, and identity substring—also prove the fixed target.
That successful counterfactual (`evidence/12-counterfactual-target.log`) does
not criticize the exact Stage 4 translation; it confirms why the required
Stage 5 operational bridge is essential and why a clean theorem alone is
insufficient.

## Judgment

Stage 3's three `DOMAIN_LEMMA` classifications are accepted. Stage 4's
source-rule/obligation bijection and fixed target are accepted structurally
and mathematically, subject to the unaccounted generation-time producer
fingerprints noted above. The Stage 5 proof is syntactically exact, cleanly
built, and axiom-accounted, but it fails the mandatory operational bridge for
both K string parameters. Under the explicit audit rule, that failure requires
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
