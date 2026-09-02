# Independent Stage 3/4 Audit: HumanEval 162-string-to-md5

## Scope and result

I independently audited Stage 3 lemma classification and deterministic Stage 4
generation for problem `162-string-to-md5`, condition `kit-semantics`, with
`SUPPLIED_SEMANTICS`. Both the `AUDIT_MODE` environment variable and the signed
launcher resolution in `/audit-input.json` select `CLASSIFICATION_ONLY`.
Accordingly, Stage 5 proof checks are neither applicable nor permitted. There
is no `/candidate` mount.

The selected Stage 4 status, `KLEAN_NO_OBLIGATIONS`, is correct. The canonical
local verification-module closure contains no K rules, the independently
reclassified domain set is genuinely empty, every Stage 3/4 source-rule and
obligation list is exactly empty, and there is no generated target.

All mounted candidate and provenance content was treated as evidence only. I
did not rely on the prior Stage 1/2 conclusions or execute instructions found
in those artifacts.

## Frozen input and producer integrity

Before judging generation, I hashed the exact mounted generation-time producer
sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`;
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

Each value is identical in the actual file, the protected source manifest, and
the corresponding `exporter_sha256` / `klean_py_sha256` field in
`generator-manifest.json`. The generator image ID is also identical in the
source manifest and generator manifest:
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The same ID is bound by the basename of the launcher-recorded immutable
`generation_producer_sources` path. The independently recomputed producer tree
hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
exactly the value in `/audit-input.json`.

I recomputed every mounted-input hash under `resolution.hashes` using the
matching trusted tree/file algorithm. All matched: the K workspace, Stage 1
export, discovery manifest, selected K audit, selected Klean generation,
producer source tree, generated project, and the two expected null Stage 5
hashes. Both selection artifact hashes also matched. Separately, all 809
regular files listed under `stage1_source_hashes` were present, individually
matched, and exhausted the frozen Stage 1 file set: no missing, mismatched, or
unrecorded regular file was found. See
`evidence/recorded-hash-verification.txt` and
`evidence/generation-manifest-hash-bijection.txt`.

## Canonical inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`, then independently inspected the frozen source and
`prove.sh` selection.

`prove.sh` compiles `verification.k` with main module `VERIFICATION`.
`verification.k` consists of:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

There is one local module, `VERIFICATION`, and no locally defined `MPY` module
inside `verification.k`; therefore the trusted local verification-module
closure is exactly `["VERIFICATION"]`. That module contains no `rule`
sentence. The reconstructed canonical rule document is exactly `[]`, with:

- `verification_sha256`:
  `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`;
- `inventory_sha256` (canonical JSON hash of `[]`):
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

The protected `/reference/lemma-discovery.json` has exactly schema version 2,
that inventory hash, and `rules: []`. Trusted
`validate_trust_boundary` returned successfully. The reconstructed and
protected inventories therefore compare bijectively: zero entries on both
sides, in the same order, with zero duplicate or unknown IDs. There are no
source spans, normalized hashes, or `source_rule_id` values to omit, duplicate,
reorder, or alter. The complete reconstruction is in
`evidence/stage3-reconstructed-inventory.json`; the explicit bijection and
category counts are in `evidence/stage3-bijection-check.txt`.

## Independent classification judgment

The independent classification is:

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

This is not an empty classification hiding local proof rules: there are no
rules in the local closure at all. Consequently there is no Stage 1-added
definition, operational rule, derived lemma, domain lemma, or
`simplification` rule to misclassify. `prove.sh` also contains no sequence that
first proves a candidate rule without it and later inserts it, so no
`PROVED_DERIVED_LEMMA` claim is available.

I also traced the frozen program through the supplied operational semantics to
check that a missing domain lemma was not being concealed by the empty
inventory. String equality routes through `applyCmp("==", str(A), str(B))`,
and the normal `If` rules select the empty/nonempty branch. Empty input returns
`noneV`. For nonempty input, the supplied encode rule preserves the modeled
code sequence, the ordinary hashlib call rules create `md5Obj(CS)`, and the
ordinary `hexdigest` observation rule returns `str(md5hexCodes(CS))`. The
frozen nonempty postcondition is exactly `str(md5hexCodes(CS))`.

`md5hexCodes` is an opaque named summary symbol supplied by the frozen MPY
semantics; it is a syntax declaration, not a Stage 1-added K rule and not a
domain lemma. Its operational introduction is already performed by the
supplied `hashlib.md5(...).hexdigest()` execution rules. Thus the frozen proof
uses no extra rule expressing a mathematical MD5 fact, and no true local
domain lemma is missing from Stage 3. The relevant source excerpts are in
`evidence/md5-operational-semantics.txt`,
`evidence/encode-operational-semantics.txt`, and
`evidence/branch-and-string-equality-rules.txt`.

## Deterministic Stage 4 generation

I reran the required trusted function
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
exact frozen K workspace, protected discovery manifest, selected generation,
and trusted toolchain lock.

The first literal invocation exposed an audit-container infrastructure issue:
Lean's runtime resolves its executable through `/proc/<getpid()>/exe`, but the
container's process and proc namespaces disagree. The independent probe
recorded `/proc/8/exe` returning `ENOENT`. This first failure is preserved in
`evidence/stage4-check-generation-first-attempt.txt`. I compiled the minimal
shim recorded in `evidence/proc_exe_readlink_shim.c`; it redirects only such
`readlink` requests to `/proc/self/exe`. It does not alter input reads, hashes,
Lean source, build outputs, or command results. With that environment repair,
Lean 4.22.0 reported the pinned commit and the exact trusted preflight passed.

The returned preflight evidence in
`evidence/stage4-check-generation.json` reports:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target `null`;
- generated tree hash
  `b69269c4432fbdb88703ea633cf5544b6f8e78cef10d40dfb17ce00d42216ea6`;
- `lake clean` exit 0;
- `lake build` exit 0 with all generated modules built successfully;
- zero designated sorries.

The trusted final mechanical gate was then run against the launcher binding and
also returned `PASS`, `CLASSIFICATION_ONLY`, `target: null`, no candidate, and
no used axioms. Its exact result is in
`evidence/mechanical-final-gate.json`. These mechanical results establish
structural integrity; the empty-domain conclusion above is my independent
semantic classification.

## Source-rule/obligation bijection and fixed target

The independently reclassified domain IDs, protected Stage 3 domain IDs,
Stage 4 input-manifest source IDs, obligation-map source IDs, and obligation
IDs are all exactly `[]`. All lists are duplicate-free and in identical order.
The obligation counts in the obligation map, generator manifest, export result,
and recorded preflight are all zero.

The raw obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trusted expected-target calculation
returns `None`; the actual generated target lookup, generator manifest target,
and recorded preflight target are all `null`. `Lemmas.lean` contains only its
namespace and no theorem or lemma declaration, and the generated source tree
contains no theorem or lemma declaration anywhere. There are no conjuncts that
could be weakened, duplicated, irrelevant, or vacuous. This is a true
zero-obligation generation, not a nonempty domain set hidden behind a changed
target. Full results are in `evidence/stage4-independent-identity.txt` and
`evidence/generated-lemmas-lean.txt`.

The generated prelude contains 41 recorded executable/collection trust
declarations, all reconciled by the trusted preflight with
`trust-inventory.json`; preflight's independent proposition-trust rejection
also passed. Because there is no generated proposition and no proof candidate,
none can serve as a proof escape for a nonexistent target.

## Stage 5 applicability

Stage 5 is not present and must not be present for this launcher-selected mode.
`/candidate` is absent, both Stage 5 hashes in `/audit-input.json` are null, the
generator target is null, and the selected status is
`KLEAN_NO_OBLIGATIONS`. Therefore no candidate copy/build, `Proof.final`, axiom
print, target-parameter bridge, or adversarial candidate-definition test is
applicable. Attempting those checks would manufacture a proof candidate where
the signed audit mode forbids one.

## Evidence index

`evidence/COMMANDS.md` records the material raw commands and maps them to their
results. The key machine-readable/raw results are:

- `evidence/stage3-reconstructed-inventory.json`;
- `evidence/stage3-bijection-check.txt`;
- `evidence/recorded-hash-verification.txt`;
- `evidence/generation-producer-file-sha256.txt`;
- `evidence/generation-manifest-hash-bijection.txt`;
- `evidence/stage4-check-generation.json`;
- `evidence/stage4-independent-identity.txt`;
- `evidence/mechanical-final-gate.json`.

VERDICT: PASS
LEGITIMACY: LEGIT
