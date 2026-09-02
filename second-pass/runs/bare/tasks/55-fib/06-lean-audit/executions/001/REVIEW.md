# Independent audit of `55-fib`

## Scope and audit mode

This review covers Stage 3 lemma classification and deterministic Stage 4
generation for HumanEval `55-fib`, condition `bare`, semantics mode
`GENERATED_SEMANTICS`. Both `/audit-input.json` and `AUDIT_MODE` record
`CLASSIFICATION_ONLY`. Accordingly, a Stage 5 proof project is neither
required nor permitted for this selected no-obligation result.

All mounted candidate and provenance material was treated as untrusted,
read-only evidence. No mounted shell script or claimed prior verdict was
executed or accepted as authoritative.

## Producer-source gate

Before evaluating Stage 4, I hashed the exact mounted producer sources:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`
- producer-bundle pipeline tree:
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`

The individual hashes agree with both
`generation-tools/source-manifest.json` and `generator-manifest.json`. The
bundle tree agrees with `/audit-input.json`. The bundle contains exactly the
two producers and its source manifest. The immutable image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest, generator manifest, and the image-key component of
the launcher-recorded producer path. The producer-source infrastructure gate
therefore passes.

## Canonical rule inventory

I reconstructed the local verification-module closure of the frozen
`verification.k` with the trusted `tools.k_rule_inventory` implementation.
The selected module is `VERIFICATION`; its local closure contains only that
module. The frozen file hash is
`06e04903013a3b9a4da09f4cb49d2c3de45a8721fed3408054c67c80f82b5702`.

The canonical inventory contains exactly two rules:

| Span | `source_rule_id` | Independent classification |
|---|---|---|
| lines 8–9 | `rule-84a0db9c987c24ad93dcfb91a4deaa38c9077791aa141b3417212a69f3dcf48c` | `DEFINITION` |
| lines 10–11 | `rule-da5d86dd353aec918d6e03a13c4d58e6661da94353a37d075cd57cb69d879e4d` | `DEFINITION` |

For each entry, I independently sliced the recorded source span, normalized it
with whitespace joining, recomputed its SHA-256, and derived
`source_rule_id = "rule-" + normalized_sha256`. All spans, text, hashes, and
IDs match. Canonical JSON hashing of the ordered rule list gives inventory
hash
`3e4c5d2b2da95d9e54f053fc301561c4c00a34a43604fea5997a3fae14b4acd3`.

The protected Stage 3 manifest has exactly the same two identities in the
same order and the same inventory hash. There are no omissions, duplicates,
extras, reordered identities, or changed hashes.

## Independent classification judgment

`verification.k` declares the named function `fibMath : Int → Int`, followed
by:

1. the guarded base equation `fibMath(N) => N` for `0 ≤ N ≤ 1`; and
2. the guarded recurrence
   `fibMath(N) => fibMath(N - 1) + fibMath(N - 2)` for `N > 1`.

These are the defining equations of the proof summary, not ordinary
execution/observation rules and not algebraic facts about an already defined
function. They directly mirror the frozen program's `n <= 1` return branch
and its two recursive calls. The postcondition names `fibMath(N)` under
`N >= 0`, so the two guarded equations cover the entire claimed input domain.
Their lack of behavior for negative integers is immaterial because those
inputs are excluded by the claim precondition.

Neither rule is a `PROVED_DERIVED_LEMMA`: there is no earlier proof of either
exact rule against a module omitting it followed by later use. Neither is a
`DOMAIN_LEMMA`: each rule constitutes the definition of the named summary
itself rather than an additional fact needed to reason about that summary.
Neither carries a `simplification` attribute; in any event, both are
classified in an allowed category.

As an operational cross-check, I freshly compiled only the frozen
`semantic.k` with K 7.1.293 and interpreted the frozen constructor term.
Inputs `0, 1, 2, 3, 5, 8` produced `0, 1, 1, 2, 5, 21`, exactly the sequence
defined by the two equations. Constant-zero, identity, wrong-base, and
duplicated-recursion counterfactuals all disagree with these observations.

The independently determined category counts are therefore:

- definitions: 2
- operational rules in the verification closure: 0
- proved derived lemmas: 0
- domain lemmas: 0

The Stage 3 classification is mathematically appropriate and its genuine
domain-lemma set is empty.

## Deterministic Stage 4 integrity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The first attempt exposed a sandbox-only PID/procfs mismatch that prevented
Lean from locating its executable. An audit-local preload shim made
`getpid()` return the host-visible `/proc/self` PID for Lean subprocesses; it
did not alter any mounted input or generated source. With that environment
correction, the required function returned `KLEAN_NO_OBLIGATIONS`, and its
complete returned JSON is exactly equal to both the selected
`preflight.json` and the launcher-embedded Stage 4 preflight.

The isolated preflight commands both succeed:

- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `2ad1f300453b8ad743138bc9489a91c61346b75d26d0cb6ee0f3bff092862f8d`

Independent hash reconciliation also passes for:

- launcher envelope digest:
  `b5d60870bf63e5f58d55eaade2c287989da3063bd9b0b543ba7e1f8d7011151f`
- Stage 1 pipeline tree:
  `2e10edca497d0e4ab9fc79a0f758565f3c0e409c3b2dcceee15b1c5d63ae2af6`
- Stage 1 export tree:
  `c9652339cbd422070709174c6f48e7b7788c1206ddd5932e906f583ec6d3f87b`
- Stage 2 audit tree:
  `5eaa19e44e4770e5b85cd1b8e9e784bfcde52fa1ea5659fd749acdd2cafb1e46`
- Stage 3 manifest:
  `f6b779823bad739b55d9bd4d827bf2d3ec761fc49853e017218e06bddedc6cfb`
- Stage 4 generation tree:
  `62ea59969a7ef4303b001016600f9747629f5679841ca07b3e566c6b981377e3`
- generated Lean tree:
  `2fbfff7fb947f2da9130f5ad883d803fcf5bb6f7eba406e829e4e50a4ca7ade3`
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
- trust inventory:
  `630dd3eec9a4c9e34e2c638f50fd4b714213ea0ec9293dfe9fa1d3ade43de6e0`

All 18 launcher-recorded Stage 1 per-file hashes also match. The generator
toolchain object exactly equals the pinned toolchain lock, and the Stage 1,
Stage 3, inventory, generated-tree, obligation-map, and trust-inventory hashes
reconcile across the input manifest, generator manifest, export result,
preflight, selection records, and audit input.

## Obligation bijection and fixed target

The independently classified domain set is empty. The deterministic
obligation map correspondingly contains:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

Thus the source-rule/obligation mapping is an exact empty bijection, not an
omission. No irrelevant, weakened, duplicated, or vacuous conjunct exists.
The exporter-computed expected target is `null`; a scan of every generated
Lean source finds zero `targetStatement` declarations. The generator
manifest, selected preflight, and audit input all also record `target: null`.
Consequently, there is no generated target whose declaration, statement, or
hash could have changed.

The generated trust inventory records 46 executable K boundary declarations,
and preflight finds no generated `sorry`, `admit`, `unsafe`, or proposition
trust declaration. These declarations do not manufacture a theorem: the
generated lemma namespace is empty and there is no target proposition.

## Stage 5 applicability

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`. `/candidate`
is absent; `lean_workspace`, `lean_invocation`, their hashes, `stage5_result`,
and `target` are all null. This is exactly the required state for a legitimate
`KLEAN_NO_OBLIGATIONS` result. No `Proof.final` or target parameters exist, so
candidate clean-build, axiom-printing, proof-identity, and operational-bridge
checks have no object to inspect.

## Evidence

Raw transcripts, returned JSON, source excerpts, and the auditor-authored
checking scripts are under `evidence/`. `evidence/COMMANDS.md` records the
exact commands. The decisive artifacts are:

- `02-producer-check.txt`
- `inventory-reconstructed.json`
- `05-inventory-bijection.txt`
- `07-preflight-command-with-pid-shim.txt`
- `preflight-rerun.json`
- `08-stage4-integrity.txt`
- `09-fresh-operational-k.txt`
- `10-source-and-target-evidence.txt`
- `11-operational-comparison.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
