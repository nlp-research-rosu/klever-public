# Independent Stage 3/4 audit: HumanEval 51-remove-vowels

## Scope and result

The launcher and `/audit-input.json` agree on `AUDIT_MODE=CLASSIFICATION_ONLY`,
condition `kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. The selected
Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent and the recorded
Stage 5 workspace, invocation, and result are all null.

I independently reconstructed and classified the local verification-module
rule closure, authenticated the generation-time producer sources, checked all
mounted provenance hashes and Stage 4 bindings, reran the trusted preflight on
fresh build state, and inspected the generated target and obligation map. The
true domain-lemma set is empty, so the selected no-obligation result is correct.

## Frozen-input and producer integrity

The trusted `tools.k_rule_inventory.inventory_verification` reconstruction
selected `VERIFICATION`, the main module named by `prove.sh`. Its local closure
inside `verification.k` is exactly `[VERIFICATION]`; `MPY` is supplied by the
separately required frozen semantics and is not another module defined in
`verification.k`. The supplied semantics was inspected separately for the
operational judgment below.

The following observed values all equal their recorded values. The full
per-file Stage 1 hash map also matched bijectively, including the compiled
artifacts; there were no missing or extra regular files.

| Binding | Verified SHA-256 |
|---|---|
| launcher resolved input | `7da7575775b6100e3f943a7d12b494cfdd21b52e18bc80d422d53341855b6cdd` |
| Stage 1 pipeline tree | `3c12de6ed8adaaae7f791c62ed020f965cf961450a8834a6fc8e2f4d30f0d1a5` |
| Stage 1 deterministic-export tree | `8a765c5be454e951ed67d184a0653f0dc41e91681780a81dda1989a9978284e0` |
| frozen `verification.k` | `db37d727ca7490b770b04e5662bc82132e2c167772e968304b81b349891cea19` |
| selected Stage 2 tree | `7d6e938bd6c71a3004bc448012142ad2f69afb91d3f49966bc13bed6cf108b9d` |
| Stage 3 manifest | `766805ab230e7c79c82f08de3d0ff6a922285fbf53f32440e355003c1b665096` |
| Stage 4 producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| selected Stage 4 generation tree | `3b2b01b6f83ea6e4b95570f38c49e7615591d74306049011cf6977031380592f` |
| generated project export tree | `b34ce1885a4ffbe21b1b3060ddcb33402d2a2159b504698fca61ae00c2e821c5` |
| obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| trust inventory | `c88c13079167837c647aaaaf4dd251ca3797f6688d5b3e8c9eb55c0a29fe0c16` |

Before any Stage 4 judgment, I directly hashed the immutable producer bundle:

- `klean_export.py` is
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `klean.py` is
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

Both hashes exactly match `generator-manifest.json` and
`source-manifest.json`. Both manifests name generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the basename of the producer path recorded in `/audit-input.json` is the same
digest, and the mounted three-file bundle has the exact recorded tree hash.
There is therefore no producer-source infrastructure error.

Evidence: `03-producer-authentication.txt`,
`04-integrity-and-inventory-results.txt`, and
`09-stage4-sidecar-and-target-results.txt`.

## Inventory reconstruction and Stage 3 bijection

The trusted inventory found exactly three rules, in this source order:

| Index | Source span | Normalized hash / `source_rule_id` suffix | Attributes | Independent class |
|---:|---:|---|---|---|
| 0 | 10-10 | `57b0cde04709c6e7a00dfe8653eab54893af58910849881dee897171eda75743` | none | `DEFINITION` |
| 1 | 12-26 | `4a0f30aa2efa0ab7a661101ca8c4d5b92435f1906adced2f965cb6025ae9176f` | `simplification` | `DEFINITION` |
| 2 | 28-44 | `b4fa0061a0832f9024dfe53cedb6eccc549392fe39607aaacbe4eb2194cb1686` | `simplification` | `DEFINITION` |

For every entry I independently sliced the inclusive source lines, compared
the exact text, normalized it as a whitespace-joined sentence, recomputed its
SHA-256, and reconstructed `source_rule_id` as `rule-<normalized hash>`. The
whole canonical rule-list hash recomputes to
`66a4d5e793d791fbdda316eb554e724dae0c3c9a8c8e7a0b4c19a947953aa0c4`.

The raw Stage 3 rule-ID list is exactly equal to the canonical ordered list.
Its cardinality and set cardinality are both three. Thus there are no omitted,
duplicated, extra, reordered, or hash-changed rules. The trusted
`lemma_discovery_contract.validate_trust_boundary` also accepted the exact
manifest. Evidence: `04-integrity-and-inventory-results.txt`.

## Independent classification judgment

All three rules define the fresh named function
`removeVowelsFrom(IntSeq, IntSeq)`, declared `[function, total]` in the
verification module:

1. On empty remaining input, the result is the accumulator.
2. When the head code is in `aeiouAEIOU`, the recurrence drops that head and
   recurses on `REST` with the same accumulator.
3. Under the complementary `notBool` guard, it appends the head to the
   accumulator with `seqConcat` and recurses on `REST`.

These are defining equations, not domain facts. Their left-hand sides contain
only the newly named summary symbol; they contain no `<k>` cell, program AST,
invocation, continuation, scope, heap, or other operational configuration.
Consequently they cannot preempt or replace ordinary execution. Each recursive
case strictly decreases the first `IntSeq` argument. The empty/constructor
patterns cover the datatype, and the two constructor guards are exact Boolean
complements, so they do not overlap and cover every head code. Both rules
carrying `simplification` are therefore correctly classified as `DEFINITION`.

The classification also agrees with the frozen operational semantics, rather
than merely with the symbol's name:

- `str.k` represents a string as `str(IntSeq)`, iterates it one code at a time,
  and defines `Compare(..., "not in", ...)` as `notBool strContains`.
- For a one-code pattern, `strContains` scans the target sequence with
  `strPrefix`, so the guard is true exactly for the ten explicit vowel codes.
- String `+` uses `seqConcat`.
- `controls.k` lowers `For` to `#loop`, binds each yielded one-character
  string, and implements `AugAssign` through the same string concatenation.

Thus, by induction on the remaining `IntSeq`, `removeVowelsFrom(REST, ACC)` is
exactly the accumulator followed by the non-vowel codes of `REST`, in order.
That is the frozen source loop's transition and its final result. The summary
is load-bearing and relevant: the loop invariant updates `result` to
`str(removeVowelsFrom(REST, ACC))`, and the final postcondition is
`str(removeVowelsFrom(TEXT, .IntSeq))`.

No rule is a `DOMAIN_LEMMA`, `OPERATIONAL_RULE`, or
`PROVED_DERIVED_LEMMA`. In particular, there is no purported derived lemma for
which an earlier bridge-free proof would need to be located, and no
human-facing property has been hidden as a definitional simplifier.

As finite supporting evidence, an independent recurrence/loop comparison
covered 4,681 sequences of length zero through four over vowel, consonant,
punctuation, zero, and non-ASCII code points with zero mismatches. Constant,
identity, swapped-guard, and missing-uppercase-vowel counterfactuals all failed
on explicit witnesses. This finite run supports, but does not replace, the
structural argument above. Evidence: `07-operational-semantics-symbol-trace.txt`
and `08-classification-witness-results.txt`.

## Stage 4 obligation and target audit

The independently classified domain set is genuinely empty. The Stage 4
bindings are consequently the unique correct empty bijection:

- `input-manifest.json.source_rules = []`;
- `obligation-map.json.source_rules = []`;
- `obligation-map.json.obligations = []`;
- `obligation-map.json.trust_parameters = []`; and
- `generator-manifest.json.obligation_count = 0`.

There are no omitted or duplicated source rules, irrelevant or weakened
obligations, or vacuous conjuncts because there are no eligible source rules or
conjuncts. The obligation-map hash and every source, inventory, discovery,
toolchain, generated-tree, export-result, trust-inventory, and diagnostic-output
hash binding recomputed correctly.

The fixed target is absent in every independent view:

- the generator manifest target is null;
- the launcher-resolved target is null;
- trusted `klean_export.target_statement(generated)` returns null;
- `Lemmas.lean` has an empty namespace and no target declaration; and
- a generated-source search finds no `KleanTarget` or target declaration.

The generated project has no `sorry`, `admit`, or `unsafe`, and `Lemmas.lean`
has no axiom or opaque declaration. The 41 generated executable collection-hook
axioms in `Prelude.lean` match the trust inventory exactly under trusted
preflight and none is proposition trust. Since there is no target theorem,
none can disguise a proof obligation.

## Trusted preflight rerun

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required frozen Stage 1 workspace, Stage 3
manifest, Stage 4 generation, and pinned toolchain lock. The audit container's
initial Lean invocation exposed an infrastructure quirk: Lean queried
`/proc/<getpid>/exe`, but the mounted `/proc` PID view did not contain that PID,
and `readlink` returned `ENOENT`. A tracing library recorded the exact failing
path. A retained compatibility shim redirects only paths matching
`/proc/[digits]+/exe` to the equivalent `/proc/self/exe`; it does not alter Lean
source, generated files, imports, declarations, or proof behavior. With this
shim, Lean reports version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

The unchanged trusted preflight then copied the generated project to its own
fresh temporary directory and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- designated sorry count 0;
- trust declaration count 41;
- `lake clean` exit 0; and
- `lake build` exit 0, `Build completed successfully.`

One successful rerun reproduced the recorded diagnostic output hash exactly.
Another repeated build scheduled the independent `Func` and `Lemmas` modules
in the opposite order, changing only the raw parallel-build log hash; all
immutable fields and normalized diagnostic lines remained identical. This does
not change the deterministic generated tree, obligation mapping, target, or
build result. The initial failure, root-cause evidence, shim source, successful
raw returned documents, and repeated comparison are all retained in
`05-rerun-klean-preflight.txt` through
`06d-proc-shim-validation.txt` and
`11-rerun-preflight-exact-comparison.txt` through
`11c-rerun-preflight-normalized-comparison-success.txt`.

## Stage 5 applicability

Stage 5 proof auditing is not applicable in this launcher mode. The generated
target is absent, `/candidate` is absent, and the launcher records no Stage 5
result, workspace, or invocation. Creating `Base`, auditing `Proof.final`,
running `#print axioms Proof.final`, or checking target parameters would invent
a proof candidate contrary to the required `KLEAN_NO_OBLIGATIONS` invariant.
Their absence is therefore a passed mode check, not an omitted proof check.

## Evidence index

`evidence/COMMANDS.md` records the exact commands. Raw outputs, including failed
infrastructure attempts, are retained under `evidence/`. The principal results
are:

- `04-integrity-and-inventory-results.txt`: canonical inventory, exact ordered
  Stage 3 bijection, producer authentication, tree hashes, and the complete
  per-file Stage 1 hash comparison.
- `05c-rerun-klean-preflight-success.txt`: required trusted preflight return.
- `07-operational-semantics-symbol-trace.txt`: frozen operational rules used in
  the mathematical classification.
- `08-classification-witness-results.txt`: adversarial finite witnesses.
- `09-stage4-sidecar-and-target-results.txt`: launcher, export, sidecar,
  diagnostic, target, and mode checks.
- `10-generated-source-and-mode-inspection.txt`: direct generated-source and
  candidate-absence inspection.
- `11c-rerun-preflight-normalized-comparison-success.txt`: repeated fresh
  preflight comparison.

VERDICT: PASS
LEGITIMACY: LEGIT
