# Independent Stage 3–4 audit: `163-generate-integers`

## Scope and result

I audited HumanEval problem `163-generate-integers`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and
the signed launcher input select `CLASSIFICATION_ONLY`. The selected Stage 4
status is `KLEAN_NO_OBLIGATIONS`. Accordingly, there is no Stage 5 proof to
audit: `/candidate` is absent, the signed Lean workspace/invocation fields are
null, and the Stage 5 result is null.

I treated all mounted workspaces, reports, manifests, comments, and logs as
untrusted evidence. I did not execute any mounted provenance script. The only
executed project operation was the clean-build performed on a temporary copy
inside the trusted `tools.klean_preflight.check_generation` procedure.

Result: the four local K rules are genuinely definitions; the true
`DOMAIN_LEMMA` set is empty; Stage 4 correctly generated no obligations and no
target; all reconstructed identities and recorded hashes agree.

## Producer provenance gate

This gate passed before judging generation.

| Item | Recomputed value | Comparison |
|---|---|---|
| `generation-tools/klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | Matches `generator-manifest.json` and `source-manifest.json` |
| `generation-tools/klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | Matches both manifests |
| Producer bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | Matches `/audit-input.json` |
| Generator image | `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` | Matches generator provenance, the source manifest, and the image-addressed producer path in `/audit-input.json` |

The signed-resolution envelope hash also recomputes exactly. The independent
hash gate checked every Stage 1 per-file hash and exact file-name set, both
recorded Stage 1 tree formats, the selected Stage 2 tree, Stage 3 manifest,
selected Stage 4 tree, selection artifact hashes, generated tree, and producer
tree: 30 checks, zero
failures. See `evidence/09-producer-sha256.txt` and
`evidence/31-verify-recorded-hashes.log`.

## Canonical local-rule inventory

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. The selected main module is `VERIFICATION`; its local
verification-module closure contains only `VERIFICATION`. The external `MPY`
import is supplied semantics, not another local module in `verification.k`.

The reconstruction found exactly four source rules in source order:

| # | Span | Normalized SHA-256 / `source_rule_id` | Independent class |
|---|---|---|---|
| 1 | 9–11 | `e485812b492df1e2d627d73dd057ca7d00d04af511b2dc7bdd89e5e026812d48` / `rule-e485812b492df1e2d627d73dd057ca7d00d04af511b2dc7bdd89e5e026812d48` | `DEFINITION` |
| 2 | 14 | `8e0942964d5eb30f25988841f3b2b7d776f3c0a617ec8af6602e2863e4e471e1` / `rule-8e0942964d5eb30f25988841f3b2b7d776f3c0a617ec8af6602e2863e4e471e1` | `DEFINITION` |
| 3 | 15 | `1ca5229dc152dfa3dcd21aa4974e7959fd9ec785342863588027006c39579132` / `rule-1ca5229dc152dfa3dcd21aa4974e7959fd9ec785342863588027006c39579132` | `DEFINITION` |
| 4 | 18–22 | `1d4a13583c5d0924f771db5d1584f01d12bfcbce0077644a396fa7bf3d6fa6e8` / `rule-1d4a13583c5d0924f771db5d1584f01d12bfcbce0077644a396fa7bf3d6fa6e8` | `DEFINITION` |

The canonical whole-inventory hash is
`3d466cb6625fb9c3bf00b56d4b753370f1ae5da4550698bf12d5415a2784b6ea`.
It matches Stage 3, the Stage 4 input manifest, and generator provenance.

Comparison with `/reference/lemma-discovery.json` is bijective and
order-exact: four canonical IDs, four distinct manifest IDs, identical ordered
lists, no omissions, duplicates, extras, changed hashes, or unaccounted
classifications. The trusted Stage 3 contract also passes. Full reconstructed
text, spans, attributes, and hashes are in
`evidence/21-reconstructed-inventory.json`; the independent order/bijection
results are in `evidence/22-stage3-contract-and-order-check.txt`.

## Independent classification and mathematical adequacy

All four rules have fresh summary-function symbols at the head of their left
sides. None matches a `<k>` computation, an existing operational symbol, or
any configuration cell. Thus none preempts binding, evaluation, branching,
allocation, mutation, return, control, or state. None has a `simplification`
attribute.

1. `inClosedSpan(A,B,D)` is a total named Boolean summary. Its single equation
   defines it as `(A ≤ D ≤ B) ∨ (B ≤ D ≤ A)` for all K integers. It is a
   definition, not an algebraic fact asserted about a pre-existing symbol.
2. The two `keepDigit` rules define a fresh total helper by the disjoint and
   exhaustive Boolean constructors. `true` prepends `D`; `false` preserves the
   tail. Neither rule recurses or overlaps the other.
3. `expectedDigits(A,B)` is a finite, unconditional definition of a named
   postcondition value. Its nesting preserves the order 2, 4, 6, 8. It does
   not assert that the source program computes this value; the Stage 1 reachability
   claim is what connects ordinary execution to this separately defined term.

There is no `OPERATIONAL_RULE`: no local rule rewrites or observes an ordinary
program configuration. There is no `PROVED_DERIVED_LEMMA`: Stage 1 contains no
earlier proof of any one of these exact rules against a module omitting it and
no later proof that uses such a separately established rule. There is no
`DOMAIN_LEMMA`: every rule is an equation defining one of the three fresh
summary functions, rather than a mathematical property assumed about existing
symbols.

This classification is also faithful to the frozen program. The source starts
with an empty list, tests the four digits in ascending order, and appends each
digit exactly when
`(a <= d and d <= b) or (b <= d and d <= a)`. Under the supplied semantics,
`Compare` dispatches integer `<=` to `<=Int`; `BoolOp` implements the same
short-circuit Boolean predicate; `If` chooses the corresponding branch;
`ListExpr` allocates the empty list; `append` extends the `ValSeq` at its end;
and `Return` returns the resulting reference through the ordinary call frame.
Therefore, for each `d` in 2, 4, 6, 8, the source inclusion condition is
definitionally the `inClosedSpan` condition, and sequential append yields
exactly the `expectedDigits` sequence.

Focused frozen rules are recorded in `evidence/93-list-semantics-focused.txt`
through `evidence/99-return-semantics-focused.txt`. An independent finite
sensitivity check covered 289 endpoint pairs with zero source/summary
mismatches. Witnesses include reversed endpoints, inclusivity, singleton,
partial, full, and empty results. Hard-coded empty/all, one-direction-only,
exclusive-endpoint, missing-8, and reversed-output counterfactuals each fail on
a stated witness. This is finite supporting evidence; the universal judgment
above follows directly from the four identical per-digit predicates and the
append order. See `evidence/92-classification-witnesses.log`.

The generated Lean definitions preserve these equations: the translated
`inClosedSpan` computes the same six comparisons/Boolean combinations,
`keepDigit` has the two exact constructor cases, and `expectedDigits` builds
8, 6, 4, then 2 by nesting so the resulting sequence is ascending. See
`evidence/100-generated-summary-functions.txt`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and
pinned toolchain lock.

The sandbox hides `/proc/<own-pid>/exe`, which Lean 4.22 uses to locate its
application, while exposing the equivalent `/proc/self/exe`. The first run
therefore failed before theorem elaboration; an explicit toolchain root let
Lake start but left the child Lean lookup failure. I recorded both failures.
For the final run I used the recorded, narrowly scoped preload shim in
`evidence/79-lean-app-path-shim-source.txt`, which redirects only the exact
self-PID executable lookup to `/proc/self/exe`. It does not alter any Lean/K
source, declaration, proposition, hash input, or elaboration result.

The unchanged trusted checker then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- zero obligations;
- target `null`;
- `lake clean` exit 0 with empty output;
- `lake build` exit 0;
- build-output SHA-256
  `50ee102a6d4b07ce056fc793fb9e10c02a3ff0173b636b7142448ddb9918e7a4`,
  exactly matching the generation-time preflight;
- generated tree
  `572f79f06b7e1fc0b880d9e7b97c699d3b2cf63d8434565824838ad2b8a1dbdf`;
  and
- zero designated sorries.

Complete returned evidence is in `evidence/81-check-generation-final.log`.
Exact commands and the resolved sandbox setup are in
`evidence/COMMANDS.md`.

I separately checked the Stage 4 bindings rather than relying on the preflight
result. The independently classified domain set is `[]`; the input-manifest
`source_rules` is `[]`; obligation-map `source_rules` and `obligations` are
both `[]`; trust parameters are `[]`; the obligation count is zero; and there
are no conjuncts, hence no omitted, duplicated, weakened, irrelevant, or
vacuous conjunct. The obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
and matches the generator manifest.

The trusted expected-target reconstruction returns `None`, the independent
generated-target parser returns `None`, and both the generator manifest and
signed audit input record target `null`. The generated root module contains no
target declaration. Thus the fixed generated target is exactly the required
absence of a target, not a changed or weakened theorem. All 35 independent
Stage 4 sidecar, hash, source-rule/obligation, status, and target checks pass;
see `evidence/91-independent-stage4-gate.log`.

The generated library contains 41 generic collection-hook trust declarations,
all exactly inventoried by `trust-inventory.json`; preflight independently
rejects proposition trust. With no target or obligation, these declarations do
not establish any theorem. They do not convert an omitted domain lemma into a
no-obligation result because the independent domain set is genuinely empty.

## Stage 5 applicability

Stage 5 proof checks are intentionally not run in `CLASSIFICATION_ONLY` mode.
There is no generated theorem to prove, no `target.parameters`, no candidate
`Proof.final`, and no candidate project. Consequently clean candidate build,
target-shadowing checks, `#print axioms Proof.final`, proof identity, axiom
accounting, and operational-bridge parameter definitions are not applicable.
Their absence is consistent with `KLEAN_NO_OBLIGATIONS` and with the signed
launcher input.

VERDICT: PASS
LEGITIMACY: LEGIT
