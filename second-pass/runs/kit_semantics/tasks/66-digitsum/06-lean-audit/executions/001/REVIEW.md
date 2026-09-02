# Independent Stage 3–4 Audit: HumanEval 66-digitsum

## Scope and result

The launcher and `AUDIT_MODE` both record `CLASSIFICATION_ONLY` for problem
`66-digitsum`, condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`. There is no `/candidate`, no Stage 5 result, no Lean
workspace or invocation path, and both Stage 5 hashes are null. Accordingly,
this audit covers the independent Stage 3 classification and deterministic
Stage 4 generation; the optional Stage 5 proof checks do not apply.

I did not rely on the selected Stage 2 review, the Stage 1 `PROOF.md`, prior
logs, comments, or prior PASS/classification conclusions. Mounted artifact
content was treated as evidence. Only the trusted `/reference/tools` code was
executed for inventory, hashing, preflight, and the final mechanical gate.

The result is PASS/LEGIT. The frozen verification closure contains two genuine
definition equations and no domain lemmas. Therefore the empty Stage 4
obligation set and null target are mathematically appropriate, not merely
self-consistent.

## Producer provenance gate

The required producer-source check was completed before substantive Stage 4
judgment:

| Producer | Observed SHA-256 | Generator/source manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | identical |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | identical |

The complete producer-bundle tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
identical to `/audit-input.json`. The immutable generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator manifest and source manifest; the launcher-recorded producer
path ends in the same image digest. The source bundle contains exactly the two
producer files and `source-manifest.json`. This clears the infrastructure
provenance gate.

## Frozen-input and envelope integrity

All 795 entries in `resolution.stage1_source_hashes` were independently
rehashed. Every entry exists as a regular file and matches; the actual frozen
tree also has exactly 795 regular files, with no unrecorded files, symlinks, or
special entries. The independently recomputed resolution hashes all match:

| Binding | SHA-256 |
|---|---|
| Stage 1 workspace tree | `66e75438c4cec75e1a0db79ff447bb20357f98f6455c0ee5fb88dd06184087a2` |
| Stage 1 export tree | `b9b461fcdcd051c01a4b94fe94104a73cece2f0a54da02259fb1c4b61e8b9260` |
| Stage 3 discovery file | `4dd61b24f1888c72385c3384749573aa72ef66c35387837bbcbf3310586e9e48` |
| Selected Stage 2 tree | `294d6ad0ae3a68c131ff782c71b5efb2dd8b3da471f1e4cb03b826bdd255f84a` |
| Selected Stage 4 tree | `019af2796e45433532c0be84a05d127872b947f4e2f9cdaf22ba1fe6ed77229e` |
| Generated project tree | `365302f36a0b09b49e686cbf56adae0eff4246631273848941ae7d05afa33cee` |
| Producer source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

The trusted Stage 6 envelope verifier recomputed the signed resolution digest
as `f21da657907f005bd9385920bf75a1ca14a0076b77ae81205b1e79ea840409f0`,
identical to `resolved_input_sha256`. The embedded Stage 4 preflight record is
data-identical to the selected preflight JSON, and both selection
artifact hashes match their resolution tree hashes.

## Inventory reconstruction and bijection

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` on the frozen Stage 1 workspace. `prove.sh` selects
`VERIFICATION`, and the local module closure inside `verification.k` is exactly
`["VERIFICATION"]`. The frozen file SHA-256 is
`fadba8c0b8a573ce51fe04d84d5faa72180d32067f6a879fe8f68094748b744b`.

The reconstructed inventory is:

| Order | Source span | `source_rule_id` / normalized SHA-256 | Attributes |
|---:|---|---|---|
| 1 | `VERIFICATION:10-10` | `rule-e470dad5bcaab0cce73635a8c1bc13a406d112c55527ad14e4ae9317461108c4` | none |
| 2 | `VERIFICATION:11-16` | `rule-b3786e0b561f5d76d2d73d69b0306d78d399d738da6b14efa48ef6eb76a56060` | none |

The canonical whole-inventory hash is
`a4e81b7526afaf06451faab8a91e569389fec6f0afd1a15ea730072963212557`.
The protected discovery manifest has exactly two entries with those identities
in that order and the same inventory hash. Neither side contains duplicate
IDs; there are no omissions, extras, reordered identities, changed normalized
hashes, or unaccounted rules. The Stage 4 input manifest reproduces both full
definition records—including spans, texts, classifications, and rationales—
exactly.

## Independent classification judgment

The two rules are independently classified as follows:

1. `rule-e470...1108c4` is a `DEFINITION`. It is the empty-constructor equation
   `digitSumIS(.IntSeq) => 0` for the newly declared total summary function
   `digitSumIS(IntSeq)`.
2. `rule-b378...56060` is a `DEFINITION`. It is the nonempty-constructor
   recurrence. It chooses `C` exactly when
   `isUpperC(C) andBool notBool isLowerC(C)`, otherwise zero, then adds the
   structurally smaller `digitSumIS(REST)`.

These rules match only applications of a new named summary function. They do
not match a program term, configuration cell, call, loop, continuation, frame,
binding, or state transition, so they are not operational rules or operational
bridges. They do not assert a separate aggregate property such as a final sum
equality, so they are not domain lemmas. They were not first proved in a module
without themselves and later reused, so they are not claimed as proved derived
lemmas. Neither rule has a `simplification` attribute.

The recurrence is relevant and exact for the frozen source program. Under the
supplied semantics:

- string iteration on `iCons(C, REST)` yields the singleton string containing
  `C` and recurs on `REST`;
- `isupper` on that singleton reduces to
  `hasUpper(iCons(C,.IntSeq)) andBool notBool hasLower(iCons(C,.IntSeq))`,
  which reduces exactly to the recurrence condition;
- `ord(str(iCons(C,.IntSeq)))` reduces to `C`; and
- empty iteration contributes zero.

Thus the summary step is syntactically the same value computation as one
operational loop step, not an assumed human-facing result fact. This remains
true for every integer code represented by the symbolic `IntSeq`, not only
ASCII-literal examples. Boundary checks included negative codes, 64/65,
89/90/91, 96/97/122/123, 127/128, and 1000. Constant-zero, identity, `< 90`,
and lowercase-summing counterfactuals were each distinguished by concrete
witnesses. The universal conclusion comes from the source-rule reduction
above; the finite checks are only adversarial corroboration.

The independently classified sets are therefore:

- `DEFINITION`: the two reconstructed rules;
- `OPERATIONAL_RULE`: empty;
- `PROVED_DERIVED_LEMMA`: empty;
- `DOMAIN_LEMMA`: empty; and
- `simplification`: empty.

## Stage 4 obligation and target audit

The exact producer-source routing was inspected but not executed. It derives
Stage 4 source rules exclusively from validated `domain_lemmas`, checks an
ordered source-rule/obligation bijection, emits a target only for a nonempty
obligation list, and derives `KLEAN_NO_OBLIGATIONS` from an empty list. This is
the correct routing for the independently determined classification above.

The observed Stage 4 records agree:

- `input-manifest.json` has the two exact definitions and empty
  `source_rules`, `operational_rules`, and `proved_derived_lemmas` lists;
- `obligation-map.json` has empty `source_rules`, `obligations`, and
  `trust_parameters` lists;
- the obligation-map SHA-256 is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching the generator manifest;
- the generator manifest records `obligation_count: 0` and `target: null`;
- `export-result.json` records `KLEAN_NO_OBLIGATIONS` and zero obligations;
- the launcher records the same status and null target; and
- trusted `klean_export.target_statement` independently returns `None`.

There can be no omitted, duplicated, reordered, irrelevant, weakened, or
vacuous domain obligation because the true domain set is empty and every one of
the two inventory entries is accounted for as a definition. There is no target
conjunct to weaken or make vacuous. A scan of all 1,310 generated Lean source
lines found no `targetStatement`, theorem, lemma, example, proof hole, or final
proof declaration. The generated `Func.lean` implements the same empty and
structural recurrence equations. `Rewrite.lean` contains an export constructor
for executing that generated definition, but it is not a proposition or target.

The generated generic collection scaffolding contains 41 axioms, all exactly
recorded in `trust-inventory.json`; its SHA-256
`12bc03781c94328e0f5746b27cff0e9ea555ffe5f216b876c7cdbb9a02ca7560`
matches `export-result.json`. With no theorem target or Stage 5 proof, those
scaffolding declarations cannot serve as a proof escape for this no-obligation
result. The trusted preflight also found zero designated or other sorries.

## Mechanical preflight and gate

The first direct `check_generation` call reached the required clean-build step
but failed because this audit sandbox exposes host PIDs in `/proc` while Lean's
`getpid()` returns an inner namespace PID. Lean consequently could not resolve
`/proc/<inner-pid>/exe`. This was an environment issue, not an artifact or proof
failure. I recorded the exact failure and used a narrow preload shim that only
returns the host PID from `/proc/self/status` and redirects numeric proc-exe
realpath lookups to `/proc/self/exe`. It was inherited only by Lean/Lake child
processes; no mounted input, trusted Python tool, generated source, or toolchain
binary was modified.

With that environment repair, the required call to
`tools.klean_preflight.check_generation` returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- zero designated sorries;
- `lake clean` exit `0`; and
- `lake build` exit `0`, ending in `Build completed successfully.`

The trusted final mechanical gate independently repeated preflight, verified
the signed bindings before and after execution, and returned PASS in
`CLASSIFICATION_ONLY` mode with null target, null candidate hash, and no used
axioms. As designed, that gate labels semantic classification
`NOT_EVALUATED`; the semantic judgment in the preceding sections is independent
and is the basis for legitimacy.

## Stage 5 applicability

Stage 5 checks are not skipped despite a proof-bearing mode; they are genuinely
inapplicable. `AUDIT_MODE`, the signed resolution, and the selected Stage 4
status all establish `CLASSIFICATION_ONLY`. The true domain-lemma set is empty,
the generated target is null, `/candidate` is absent, `stage5_result` is null,
and the Lean workspace/invocation paths and hashes are null. Creating a Base
copy, checking `Proof.final`, printing its axioms, or validating target
parameters would invent a Stage 5 artifact forbidden by the no-obligations
contract.

## Evidence index

- `evidence/00-mode-and-producer-provenance.txt`: mode, producer hashes, image
  identity, and top-level tree bindings.
- `evidence/01-reconstructed-rule-inventory.json`: complete trusted inventory.
- `evidence/02-stage3-bijection.txt`: exact ordered-bijection result.
- `evidence/03-preflight-initial-environment-failure.txt`: exact initial
  environment failure and workaround diagnosis.
- `evidence/04-check-generation.json`: required preflight return value.
- `evidence/05-independent-hash-and-manifest-checks.txt`: all Stage 1 file
  checks, resolution hashes, sidecars, obligations, target, and candidate
  absence.
- `evidence/06-generated-source-target-scan.txt`: generated-source declaration
  and target scan.
- `evidence/07-producer-obligation-routing.txt`: inspected deterministic
  obligation routing.
- `evidence/08-independent-semantic-classification.txt`: operational semantic
  reduction and counterfactual witnesses.
- `evidence/09-audit-envelope-binding.txt`: signed resolution verification.
- `evidence/10-final-mechanical-gate.json`: final trusted gate output.
- `evidence/scripts/`: reproducible independent comparison and adversarial
  scripts plus the proc/PID workaround source.

VERDICT: PASS
LEGITIMACY: LEGIT
