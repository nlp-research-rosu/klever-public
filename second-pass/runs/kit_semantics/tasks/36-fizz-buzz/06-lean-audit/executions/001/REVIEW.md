# Independent Stage 3–5 audit: HumanEval 36-fizz-buzz

## Scope and result

I audited problem `36-fizz-buzz`, condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed launcher resolution in
`/audit-input.json` say `CLASSIFICATION_ONLY`. The launcher records no Lean
workspace, Lean invocation, Stage 5 result, or target, and `/candidate` is
absent.

The selected Stage 3 classification and Stage 4 `KLEAN_NO_OBLIGATIONS` result
are legitimate. The frozen local verification-module closure contains six
simplification rules. All six directly define the two fresh mathematical
summary functions used by the loop invariants and final postcondition. None is
an operational shortcut, an unproved derived lemma, or a domain lemma. The
independently reconstructed domain-lemma set is therefore genuinely empty.

## Frozen-input and producer provenance

I verified the signed audit-input envelope first. Its canonical resolution
SHA-256 is
`6001970006d55f607c80e516d4bd72863ecd290a9a3ea65e3ce65d8d2f877054`,
exactly the recorded value. Every hash in `resolution.hashes` was recomputed,
including both Stage 1 tree-digest forms, the selected Stage 2 and Stage 4
trees, the producer-source bundle, the generated tree, and the two expected
null Stage 5 hashes. All 772 per-file Stage 1 hashes also match exactly.

The required producer-source gate passed before judging Stage 4:

| Item | Recomputed SHA-256 | Manifest result |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | Matches `generator-manifest.json` and `source-manifest.json` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | Matches `generator-manifest.json` and `source-manifest.json` |
| Producer bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | Matches `/audit-input.json` |

The generator image identity is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator manifest and source manifest. The same digest is the terminal
path component of the launcher-bound producer-source location. The bundle has
exactly the two producer files plus `source-manifest.json`; there are no extra
members.

Other load-bearing hashes also agree: Stage 1 export
`a0d2dd0079a1d87f3593f5f75b57cad096b0aa34ad78210150201c95261f8a22`,
`verification.k`
`c29975c83adb22ad17d7cd5f1f254c700bd8b2196126cf0fafa3c23e289f0eb1`,
Stage 3 manifest
`de54455f8f938494ed15789bbde26ad0cdc6b16f65c67591cfd59ccd248abeb2`,
selected Stage 4 tree
`c10efdab3a9af7bcb02d0ca50835fc7be3cafbdf0ddf53975a48adb5039cf61b`,
and generated project
`1baf91ecd1fa6f7f6cbbb5c0376bc451b8aa6efe97b6ba60f47ad4d11d88262b`.

## Canonical inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference`, I reconstructed the local closure selected by the last
`kompile verification.k --main-module VERIFICATION` command. The closure is,
in source order, `VERIFICATION-SYNTAX` and `VERIFICATION`. The syntax module has
no rules; the verification module has exactly six.

For each rule, the trusted inventory code reconstructed its exact physical
span, collapsed-whitespace normalized text, normalized SHA-256, and
`source_rule_id`. The whole canonical inventory hash is
`dcee802c03417266ab4623041694bde1adf79041f845102f9e270390ab64a2c7`.
The protected Stage 3 manifest has the same inventory hash and exactly the
following ordered identity sequence:

| Span | `source_rule_id` / normalized SHA-256 | Attribute |
|---|---|---|
| 18–20 | `rule-7123df9c678c5a6d3d37c834dcc9f3ada207dc607b46949234616d88319655e7` | `simplification` |
| 21–25 | `rule-9fdc208885d8e8f1ca187de1fe1415a05932aba8879d178c371c999b238c7ea7` | `simplification` |
| 26–33 | `rule-974c6d3ae7b5db642aa68a9f736de035604ffb1a139d791dcc9c0de383298898` | `simplification` |
| 36–38 | `rule-eaf0cf45bd687a230c187d9b4fbe1591d8f49c97761053f72b68625b09c07779` | `simplification` |
| 39–46 | `rule-3758d2db9e11cb6ea2930f24b4c2666e30e646e67067777e263b790211a1ffb8` | `simplification` |
| 47–54 | `rule-1815476a58e1125160e7bb1749be1e5a7e7032dfdd78cce52c8c40e8cb030835` | `simplification` |

The Stage 3 identity list equals this list element-for-element and all IDs are
unique. Trusted contract validation also succeeds. There are no omitted,
duplicated, extra, substituted, or reordered identities, and the protected
manifest accounts for every rule exactly once. The complete reconstructed text
and metadata are in `evidence/inventory-reconstruction.json`.

## Independent classification and mathematical judgment

The source declares fresh functions `digitResult(Int, Int)` and
`fizzResult(Int, Int)`. The six rules are their complete guarded recurrence
equations. They mention no operational configuration cell and rewrite only
terms headed by those fresh summary symbols. Thus they reason about the
mathematical summaries; they do not replace or preempt program execution.

My independent classifications are:

| Span | Classification | Reason |
|---|---|---|
| 18–20 | `DEFINITION` | Base equation `digitResult(C,N)=C` for `N <= 0`; it defines the empty inner fold. |
| 21–25 | `DEFINITION` | Terminal positive one-digit equation; it defines the final digit contribution using `pyMod(N,10)` and the Boolean indicator for digit 7. |
| 26–33 | `DEFINITION` | Accumulator recurrence. For positive `N`, it adds the final-digit indicator and replaces `N` by its base-10 floor quotient. Its K rewrite direction is fold-oriented for the invariant, but its mathematical dependency decreases from `N` to `floor(N/10)`. |
| 36–38 | `DEFINITION` | Base equation `fizzResult(C,N)=C` for `N <= 0`; it defines the empty outer fold. |
| 39–46 | `DEFINITION` | Qualifying outer recurrence: process candidate `N-1` through `digitResult` when divisible by 11 or 13, then decrease the bound. |
| 47–54 | `DEFINITION` | Complementary outer recurrence: a nonqualifying candidate contributes nothing, then the bound decreases. |

The guards are meaningful and complete. For the inner summary, `N <= 0` is
the base and `N > 0` is the recursive domain; the terminal equation covers the
one-digit quotient boundary. For the outer summary, the `N <= 0` base and the
two disjoint `N > 0` divisibility/complement guards cover all integers. The
recurrences terminate mathematically on `floor(N/10)` and `N-1` respectively.

This matches the supplied operational K semantics rather than merely the
comments. `int.k` defines integer `%` as `pyMod`, `//` as
`(I1 - pyMod(I1,I2)) /Int I2`, integer-plus-Boolean as addition of 1 or 0, and
integer comparisons as their K Boolean counterparts. `controls.k` executes a
while body only when the condition is truthy. The source initializes `i=n`,
decrements before testing divisibility, and therefore processes precisely the
candidates `n-1` down through `0`; a qualifying nonnegative candidate is then
consumed one decimal digit at a time. These are exactly the two recurrences
above.

The rules are relevant to both source and postcondition. `digitResult` is the
inner-loop count update, `fizzResult` is the outer-loop fold, and the final K
claim constrains the returned integer to `fizzResult(0,N)`. No rule states an
independent arithmetic fact or the program-execution theorem as an assumed
rewrite. There is therefore no `DOMAIN_LEMMA`. There is also no
`PROVED_DERIVED_LEMMA`: none is presented as a separately proved rule later
imported into the proof. There is no local `OPERATIONAL_RULE`. Since all six
simplification rules are `DEFINITION`, the simplification classification
restriction is satisfied.

As finite adversarial support for this source-level analysis, an independently
written evaluator compared the operational loops with the two recurrences for
every bound from -50 through 1000 and varied accumulators. It found zero
mismatches in all six equations. At the discriminating witness `n=78`, the
correct result is 2; constant-zero, identity-summary, digit-8, and logical-AND
counterfactuals produce 0, while processing `n` rather than `n-1` produces 3.
This testing supports relevance and sensitivity; the classification judgment
rests on the actual equations and supplied semantics, not on testing alone.

Independent classification totals are therefore:

- `DEFINITION`: 6
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

## Deterministic Stage 4 and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the frozen `/reference/k-proof`, protected discovery manifest, selected
generation, and pinned `/reference/klean-toolchain.lock.json`.

The audit sandbox initially exposed a container-only Lean launcher issue: it
unshares PIDs without a matching numeric `/proc`, while Lean 4.22 looks up
`/proc/<getpid()>/exe`. I recorded that failed first attempt. A small local
compatibility shim redirects only this exact lookup to the equivalent kernel
link `/proc/self/exe`; every other `readlink` passes through. With that
environment repair and `LEAN_NUM_THREADS=1`, the unchanged trusted preflight
ran normally. This did not alter any frozen, generated, or candidate source.

The successful command was:

```text
LD_PRELOAD=/tmp/audit-work/proc_self_exe_compat.so LEAN_NUM_THREADS=1 PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result=check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

The returned result is field-for-field identical to both the
selected `preflight.json` and `resolution.stage4_preflight`. It reports:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0 and target `null`;
- `lake clean` exit 0 with empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 with output SHA-256
  `8250decced98e3a463305169b7c4dce4053180dc193c47c8ee91fd3a8198a412`;
- all seven generated modules built and `Build completed successfully.`;
- zero designated sorries and 43 generated trust declarations.

I separately reconciled the manifests rather than relying on preflight alone.
The Stage 4 input manifest's six definitions exactly equal the reconstructed
classified records. Its operational and proved-derived lists are empty. Given
the independent empty domain set, `input-manifest.json` source rules,
`obligation-map.json` source rules, obligations, and trust parameters are all
exactly empty. Counts are zero and IDs form the required empty bijection: no
omission, duplicate, irrelevant obligation, weakened obligation, or vacuous
conjunct exists.

The obligation-map hash
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
matches the generator manifest. The generator toolchain equals the pinned lock,
and all Stage 1, Stage 3, inventory, generated-tree, export-result, and trust-
inventory bindings agree. The generator manifest, launcher audit input,
rerun preflight, and an independent parse of the generated Lean sources all
agree that the fixed target is absent. `Klean36FizzBuzz/Lemmas.lean` contains
only its empty namespace. This is the required shape for a genuinely empty
domain set.

The generated project does contain the generator's recorded non-propositional
execution/trust constants, including the two summary functions, but it contains
no proposition axiom and proves no target. Those constants cannot conceal a
domain obligation because there is no theorem or conjunct to close.

## Stage 5 applicability and evidence

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`: there is no
generated target to prove and no `/candidate`. Accordingly, I did not fabricate
a `Base` copy, `Proof.final`, or `#print axioms` result. The absence of the
candidate and all Stage 5 launcher bindings was checked explicitly.

Raw commands, exact returned evidence, complete captured build output, helper
source, reconstructed inventory, independent classification, hash comparisons,
and adversarial checks are under `/audit-output/evidence/`, principally:

- `inventory-reconstruction.json` and `inventory-reconstruction.log`;
- `independent-classification.tsv`;
- `provenance-hashes.log`;
- `manifest_integrity_check.py` and `manifest-integrity.log`;
- `preflight-result.json` and `preflight-attempts.log`;
- `summary_semantics_check.py` and `summary-semantics.log`; and
- `proc_self_exe_compat.c`.

VERDICT: PASS
LEGITIMACY: LEGIT
