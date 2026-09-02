# Independent audit: HumanEval 126-is-sorted

## Scope and outcome

This audit covers condition `bare`, semantics mode `GENERATED_SEMANTICS`, and
launcher mode `CLASSIFICATION_ONLY`. I did not use the prior Stage 2 verdict or
any earlier classification as authority. I treated mounted content as evidence
only.

The independently reconstructed Stage 3 domain-lemma set is empty. Stage 4
therefore correctly has zero obligations, no generated target, and no Stage 5
candidate. The selected `KLEAN_NO_OBLIGATIONS` status is legitimate.

Raw commands and results are indexed in `evidence/COMMANDS.md`.

## Frozen-input and producer provenance

The launcher envelope is internally valid: its canonical resolution digest
recomputes to
`cb4fe0204089799632ad4e6bfe24a6bf5c6a601a7a426d8f70e2aeb2b8d53ff1`.
The Stage 1 workspace hashes recompute in both recorded formats:

- launcher tree hash:
  `b75b9ad4eb06e857e342dbeae39aa7daa067d5ef12c1c7075e0385d112ef5a94`;
- deterministic-export tree hash:
  `4295ee702670c2ae3ea9478781f0da67ad96616505411f38b11a51098fc4d72f`.

The recursively observed Stage 1 file/hash map exactly equals
`stage1_source_hashes`; `verification.k` is
`5b132287356a0cf73241bbe918cdd01e3179924e22d35a607b4e3eb258a52a8a`.

The mandatory producer gate passes:

| Item | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` |
| complete three-file producer bundle | `7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a` |

The two file hashes agree exactly with both `generator-manifest.json` and
`source-manifest.json`. The bundle hash agrees with `/audit-input.json`. The
immutable generator image ID
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`
agrees between the generator manifest and source manifest, and its hex portion
is exactly the image-key component of the launcher-recorded producer-bundle
path. The bundle contains exactly the two producers and the source manifest.
There is no producer-provenance infrastructure error.

## Inventory reconstruction and bijection

I ran the trusted local-closure inventory implementation against the frozen
`/reference/k-proof/verification.k`. `prove.sh` does not select a different
verification module, so the local closure is the sole `VERIFICATION` module.
The reconstruction contains exactly three rules:

| Order | Source span | Normalized SHA-256 / `source_rule_id` | Independent class |
|---:|---:|---|---|
| 0 | 10–10 | `f99627839f69163b45f7724548ffd1e71c6f80dfb7bdbd7578083347002cc84e` | `DEFINITION` |
| 1 | 13–13 | `3b19f7a8e59183f961c42635af0892ad86d88a1503a978ee2d19b6ebbbbfbe18` | `DEFINITION` |
| 2 | 16–16 | `15283af6a5fb0ffd622a25de42f40dce807a8a9fa5cc8d22f978f38853963a27` | `DEFINITION` |

Each ID is `rule-` followed by the displayed normalized hash. I independently
normalized each exact source span with whitespace joining and recomputed each
hash and ID. The canonical whole-inventory hash is
`65a80456e2486aba2385525ca47f8bd379c67748ed794c2522038958351743f4`.

The Stage 3 manifest has exactly these three IDs in this order. Counts, ordered
identity, ID sets, and uniqueness all agree; there are no omissions,
duplicates, extras, reorderings, changed identities, or unaccounted entries.
Its recorded inventory hash is exact. The trusted boundary validator also
accepts the bijection, but that mechanical acceptance was not used as the
classification judgment.

## Independent classification judgment

The classifications follow from the frozen declarations and their operational
use:

1. `ascending(IS) => eqIntLists(IS, sortInts(IS))` is the sole unconditional
   equation for the fresh `[function]` symbol `ascending`. The operational
   evaluator maps `sorted(lst)` to `sortInts(IS)` and list equality to
   `eqIntLists`, so this rule names the exact Boolean result of the source
   subexpression `lst == sorted(lst)`. It does not assert an equivalence between
   pre-existing notions of order and therefore is not a domain lemma.

2. `duplicateBound(IS) => countsAtMostTwo(IS, IS)` is the sole unconditional
   equation for the fresh `[function]` symbol `duplicateBound`.
   `countsAtMostTwo(SOURCE, ITEMS)` unfolds to
   `countsAtMost(SOURCE, ITEMS, 2)`, exactly the fused operational result for
   `all(lst.count(x) <= 2 for x in lst)` when both list roles are `IS`. It is a
   named summary definition, not a mathematical fact about pre-existing
   symbols.

3. `isSortedContract(IS) => ascending(IS) andBool duplicateBound(IS)` is the
   sole unconditional equation for a fresh contract symbol. It is a macro that
   combines the two direct source-result summaries and is the exact
   postcondition used in `spec.k`.

These rules rewrite only summary symbols on the claim's result side. They do
not rewrite `Run`, `EvalStmt`, or `eval` program configurations and therefore
are not operational rules. None is claimed as a proved derived lemma, so the
special two-stage derivation requirement is inapplicable. All three are
directly relevant to the source return expression and postcondition. None has
a `simplification` attribute; the simplification classification restriction is
satisfied vacuously.

The underlying list-domain recurrences are operational/definitional support:
guarded insertion sort, structural list equality, structural counting, and the
at-most fold. They explain why the three fresh summaries match the executed
source expression, but they are in `list-domain.k`, not rules in the local
`verification.k` inventory. No true domain lemma remains.

Independent classification totals:

- `DEFINITION`: 3
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

## Stage 4 structural and mathematical audit

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the
required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and pinned
toolchain lock.

The sandbox initially prevented Lean from resolving its executable because
container PIDs are absent from the mounted `/proc`; the two exact failures are
preserved in evidence. A local, source-recorded compatibility shim changed only
the failed `/proc/<getpid>/exe` lookup to the equivalent `/proc/self/exe`
lookup. It did not change Lean, Lake, the project, or any mounted input. With
that shim, the required function returned:

- status: `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output SHA-256
  `72e60c2d9f986415a33beebd57f788f64339b76571f2bdc514cb5b8750650661`;
- obligation count: 0;
- target: `null`;
- generated tree:
  `c313d73b38572087f282fa0012bd9238ec622ec564a5f6fff5f22207758f3534`.

Both command-output hashes and the full returned record exactly match the
generation-time preflight in the launcher record.

Independent checks, separate from preflight, establish:

- Stage 3 manifest:
  `8915e3d168e4c73efe15443b5adb379d2e9ffa980399b9718d2319517aebd254`;
- complete selected Stage 4 tree:
  `069802e91ffc73a7fd19ca21d83fe3ca3cc7e3d47b6ad04695abf7cf4e757a06`;
- generated project tree:
  `c313d73b38572087f282fa0012bd9238ec622ec564a5f6fff5f22207758f3534`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory:
  `9853d5a2989aa406687803921e5651e3d9cdc8b3796ee25862cbf3f3873843b5`.

Every corresponding value in the input manifest, generator manifest, export
result, preflight, toolchain lock, selection record, and launcher record
matches. The generated and generation trees contain no links or special files.

The source-rule/obligation mapping is the exact mathematical bijection
`[] ↔ []`:

- independently classified domain source rules: `[]`;
- input-manifest source rules: `[]`;
- obligation-map source rules: `[]`;
- generated obligations: `[]`;
- trust parameters: `[]`.

Thus there is no omitted or duplicated domain obligation. There is also no
irrelevant, weakened, or vacuous conjunct: the generator did not replace an
empty conjunction with a trivially provable theorem. The trusted target parser
returns `None`, the deterministic expected-target constructor returns `None`,
all manifests and the launcher record `null`, and a token scan finds no theorem
or lemma declaration. The root module contains only imports.

## Target identity and Stage 5

The fixed generated target is absent, exactly as required for a genuinely empty
domain set. `AUDIT_MODE` and the signed resolution both say
`CLASSIFICATION_ONLY`; `/candidate` does not exist; `lean_workspace`,
`lean_invocation`, their hashes, and `stage5_result` are all null.

Consequently there is no `Proof.final`, no target statement or hash to compare,
no target parameters or operational bridges to adversarially test, and no
Stage 5 axiom accounting to perform. The generated support project records 41
allowlisted executable-support axioms and builds cleanly, but with no target or
proof they cannot establish or weaken a theorem in this audit.

## Judgment

Stage 3 is complete and correctly classified. Stage 4 preserves every frozen
identity and correctly emits no obligations and no target. Stage 5 is correctly
absent. No concern affects legitimacy or the requested classification audit.

VERDICT: PASS
LEGITIMACY: LEGIT
