# Independent Stage 3/4/5 Audit — `41-car-race-collision`

## Scope and result

I independently audited condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed resolution in
`/audit-input.json` select `CLASSIFICATION_ONLY`. The resolution has no Stage 5
workspace, invocation, result, or target, and `/candidate` is absent. Therefore
the Stage 5 proof-only checks are inapplicable; a candidate in this mode would
have been an error.

The selected Stage 3 classification and Stage 4
`KLEAN_NO_OBLIGATIONS` result are legitimate. The decisive fact is not merely
that the manifests are self-consistent: the frozen verification-module closure
contains no local K rules at all, so its true domain-lemma set is empty.

## Input and producer integrity

I treated all mounted candidate/provenance prose as untrusted evidence and used
the trusted code under `/reference/tools` for inventories, tree hashes,
preflight, and final mechanical binding.

Before judging Stage 4, I hashed the exact mounted producer sources:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Those values exactly match both `generator-manifest.json` and
`source-manifest.json`. The immutable generator image ID is identically
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator manifest, source manifest, and the image-key component of the
producer-source path signed by `/audit-input.json`. The trusted bundle-tree hash
is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly the signed value. Thus there is no producer-source infrastructure
error.

The signed audit-input envelope validates to resolved-input digest
`e85ada1fc2ba5677055f9089b249b8c0815fa79bbb4f8276003bcf4cbd75853f`.
Independent recomputation matched all recorded non-null artifact hashes:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 selected artifact tree | `523d713b7bdf0dfda034c849acb229e3105ab3e92d484ab1dd0cb9dbf809e586` |
| Stage 1 exporter tree | `eb24378e0a824d7c09deb6b6658b049eb63ab819e35c427bdbda00a1e058bc0c` |
| Stage 2 selected audit tree | `605e9f7aca63b627504360576e3ad7ef4a37a69e1b6f5eb618d97e81a79e4305` |
| Stage 3 discovery file | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 4 selected generation tree | `ce54921c5ee71f1428629abc90d254ed2172f257485fa50a4cbc4362c8cdacc2` |
| Generated project | `1e8f632b959bba97cd04cab04622f40f913dcbd198577098eddaf4b17249391b` |

I also compared all 768 entries in the signed `stage1_source_hashes` map with
all 768 regular files in `/reference/k-proof`: there were no missing, extra,
mismatched, linked, or other non-regular entries. Raw producer and hash evidence
is in [00-producer-and-input.txt](evidence/00-producer-and-input.txt).

## Stage 3 inventory reconstruction

Frozen `verification.k` is exactly:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

The trusted `inventory_verification` implementation selected `VERIFICATION`
from the `prove.sh` main-module setting and reconstructed its local closure as
the single locally declared module `VERIFICATION`. `MPY` is supplied by the
separately required, frozen semantics; it is not a locally declared
proof-extension module in `verification.k`.

The reconstructed rule list is `[]`. Consequently there are no source spans,
normalized rule hashes, `source_rule_id` values, attributes, or duplicate
identities to account for. The canonical JSON hash of `[]` is
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
which exactly matches the inventory hash in `/reference/lemma-discovery.json`.
The protected manifest itself contains the same empty ordered list. The trusted
trust-boundary validator returned:

- definitions: 0;
- operational rules: 0;
- proved derived lemmas: 0;
- domain lemmas: 0; and
- unaccounted, omitted, duplicated, extra, or reordered rules: 0.

This is a bijective comparison even though it is empty: both sides have exactly
the same zero identities in the same order. Full reconstruction evidence is in
[01-inventory-and-classification.txt](evidence/01-inventory-and-classification.txt).

## Independent classification and mathematical judgment

There are no inventory entries to relabel. In particular, there is no local
summary/recurrence/macro/named proof term (`DEFINITION`), ordinary local
execution rule (`OPERATIONAL_RULE`), separately proved-and-later-used exact rule
(`PROVED_DERIVED_LEMMA`), or mathematical assertion (`DOMAIN_LEMMA`). There are
also no local `simplification` rules, so the simplification restriction is
satisfied without exception.

I separately checked that this empty classification is meaningful for the
frozen program rather than an evasion. The source function is
`return n * n`; the K claim loads that same body, calls it with symbolic integer
`N`, and requires `N *Int N`. The supplied semantics performs module loading,
function closure creation, name lookup, parameter binding, ordinary call/return
control, `BinOp` dispatch, and the exact equation
`applyBin("*", I1:Int, I2:Int) => I1 *Int I2`. No problem-local bridge or
summary replaces any of those steps. Relevant frozen source excerpts are in
[05-operational-semantics-source.txt](evidence/05-operational-semantics-source.txt).

As corroborating operational checks, rerunning the frozen K claim produced
`#Top` with exit code 0. A false postcondition `N *Int N +Int 1` was rejected
with a stuck implication and exit code 1. Changing the body to addition while
retaining the multiplication postcondition was also rejected with residual
`N +Int N = N *Int N` and exit code 1. These mutations demonstrate result and
body sensitivity; they are not used to manufacture the empty classification.
Complete outputs are in
[06-k-operational-checks.txt](evidence/06-k-operational-checks.txt).

## Stage 4 deterministic generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against exactly `/reference/k-proof`, `/reference/lemma-discovery.json`, and
`/reference/klean-generation`, using the pinned toolchain lock. Its returned
evidence is [preflight-rerun.json](evidence/preflight-rerun.json):

- status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: 0;
- target: `null`;
- designated sorry count: 0;
- `lake clean`: exit 0;
- `lake build`: exit 0; and
- generated tree and all Stage 1/3 bindings: exact hash matches.

The initial unshimmed run exposed an audit-shell infrastructure issue: the
command sandbox unshared PIDs while exposing the host `/proc`, preventing Lean
4.22 from locating `/proc/<namespace-pid>/exe`. I diagnosed this rather than
accepting the recorded preflight. The successful rerun used a narrow
`LD_PRELOAD` shim that changes only executable-path `readlink` requests from
`/proc/<digits>/exe` to `/proc/self/exe`. It does not change generated sources,
Lean declarations, proof terms, checker code, or manifests; the preflight's
before/after snapshots confirm that all immutable inputs remained unchanged.
Both failed attempts, the shim source/hash, pinned Lean/Lake versions, and the
complete successful result are recorded in
[03-preflight-rerun.txt](evidence/03-preflight-rerun.txt).

Independent of preflight, the canonical inventory IDs, Stage 3 classified IDs,
true domain IDs, obligation-map source IDs, and obligation IDs are all exactly
`[]`. `obligation-map.json` has empty `source_rules`, `obligations`, and
`trust_parameters`; its SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. With no conjuncts there is no opportunity for
an irrelevant, weakened, duplicated, vacuous, reordered, or omitted
obligation. The trusted expected-target constructor returned `None`, the
trusted parser found no generated target, `generator-manifest.json` and the
signed audit input both record `target: null`, and manual source search found no
target/final declaration. See
[02-stage4-bijection-and-target.txt](evidence/02-stage4-bijection-and-target.txt).

The trusted final gate was also run as a consistency check. It returned PASS,
`CLASSIFICATION_ONLY`, `KLEAN_NO_OBLIGATIONS`, target `null`, candidate
`null`, and no used axioms; exact evidence is in
[final-gate.json](evidence/final-gate.json). Its
`semantic_classification: NOT_EVALUATED` is expected because that gate is only
mechanical; the independent semantic classification is the analysis above.

## Stage 5 applicability and trust accounting

Stage 5 is intentionally absent in this audit mode. There is no generated
theorem to prove, no `Proof.final`, no candidate definitions, no target
parameters, and no candidate axiom list to reconcile. Running proof-mode
copy/build, `#print axioms Proof.final`, target-shadowing checks, or operational
bridge tests against a nonexistent candidate would contradict the signed
`CLASSIFICATION_ONLY` resolution. The generated project contains 41 allowlisted
executable trust declarations, but preflight confirms no proposition trust and,
critically, none supports a target because no target exists.

## Conclusion

The Stage 3 classification is complete and correct, the true domain set is
genuinely empty, and Stage 4 deterministically represents that fact with an
empty exact mapping and no target. The required absence of Stage 5 is also
satisfied. No proof-local domain assertion, operational bridge, omitted rule,
target change, weakened obligation, or trust escape was found.

VERDICT: PASS
LEGITIMACY: LEGIT
