# Independent audit: HumanEval `46-fib4`

## Result

The Stage 3 classification is complete and mathematically appropriate, and the
selected deterministic Stage 4 result is an authentic
`KLEAN_NO_OBLIGATIONS`. The true domain-lemma set is empty. There is no fixed
generated theorem and, consistently, no Stage 5 candidate. I found no basis for
a concern or illegitimacy verdict.

This review did not rely on the selected Stage 2 verdict or any prior review.
Candidate and provenance text was treated as untrusted evidence and inspected
as data only.

## Scope and mode

- Problem: `46-fib4`
- Condition: `kit-semantics`
- Semantics mode: `SUPPLIED_SEMANTICS`
- `/audit-input.json` mode: `CLASSIFICATION_ONLY`
- `AUDIT_MODE`: `CLASSIFICATION_ONLY`
- `/candidate`: absent
- Stage 5 result, workspace, invocation, and hashes: all null/absent

The signed resolution envelope validated with
`resolved_input_sha256 = 1106cc4808cbfb23779d6d3dd14c99ae361d80f65a32e092b03a160d7e6dcfaf`.
The complete 771-file Stage 1 set was rehashed with no missing, extra, or
changed file. Both Stage 1 tree digests, the Stage 2 tree digest, Stage 3
manifest digest, Stage 4 generation digest, generated-project digest, and
producer-source digest all matched the signed resolution. The final rehash
after all checks produced the same results.

## Generation producer authentication

Authentication was completed before accepting any Stage 4 conclusion.

| Producer | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in `source-manifest.json` and `generator-manifest.json` |

The producer bundle contained exactly those two files plus
`source-manifest.json`. Its pipeline tree digest was
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`. The immutable image identity was
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the source manifest and generator manifest; the same identity is the final
component of the producer path recorded in the signed audit input. Producer
provenance is therefore authentic, so no infrastructure `AUDIT_ERROR` applies.

## Stage 3 inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace. The local verification-module closure is exactly
`VERIFICATION-SYNTAX` and `VERIFICATION`; only `VERIFICATION` contains rules.

- `verification.k` SHA-256:
  `398bf7d40f32e0f5c9be4eeb7085c35fc9a627e550d81e1b053808ba5d1b7585`
- Canonical inventory SHA-256:
  `551c2ad2e058ea51404c32413dec9df6da2982ef848827af03a8fbd7d13181d9`
- Canonical rule count: 5

For each entry, the `source_rule_id` is `rule-` followed by the normalized
source hash shown below.

| Order | Source span | Normalized SHA-256 | Attributes | Independent class |
|---:|---:|---|---|---|
| 0 | 15–16 | `293fdb8b1d4095ddc8eddd99c97d4c5b4818a9cdd792bb6b4caad600ddbaf296` | none | `DEFINITION` |
| 1 | 17–17 | `aefe9a8e0afe275fcdfc27000ccbac76a17a6ee88013c84c8f5f1b5213f62614` | none | `DEFINITION` |
| 2 | 18–18 | `b63d3b98fbeab97d51b6a9f210a585da08c78b0dba0660d7aa24fe8f9b52ac46` | none | `DEFINITION` |
| 3 | 19–19 | `ae0f386ab9647cf6bacccb9eec146bdadc0897e261591027a72b14b464abe92c` | none | `DEFINITION` |
| 4 | 20–23 | `d44d71dd060859619764bc0fe005a75f61253b9f2ffa46e35b48b4b028aaeca1` | none | `DEFINITION` |

Every exact source slice, whitespace-normalized hash, and derived rule ID was
recomputed independently. The protected manifest has the same inventory hash
and the same five IDs in exactly this order. There are no duplicate, omitted,
unknown, extra, or reordered identities. The trusted Stage 3 contract validator
also joined the manifest to the inventory successfully, yielding 5 definitions,
0 operational rules, 0 proved derived lemmas, and 0 domain lemmas.

## Independent classification judgment

`verification.k` introduces `fib4Spec : Int -> Int` as a fresh K symbol with
`[function, total]`. All five rules have `fib4Spec` at their left-hand side;
none rewrites a source-language `Call`, `While`, `Assign`, configuration cell,
or any other operational MPY term.

The equations are a genuine complete definition:

- `N <= 0` maps to 0, agreeing with the prompt at 0 and totalizing negative
  integers outside the stated `N >= 0` proof domain.
- The three singleton cases define indices 1, 2, and 3 as 0, 2, and 0.
- The `N >= 4` case defines the requested four-predecessor recurrence.

These five guards are pairwise disjoint and exhaustive over mathematical
integers. Every recursive call in the final rule strictly lowers `N`, and its
guard ensures the calls descend to the base cases. Thus the rules define the
named summary rather than assert an additional property of a pre-existing
function. No rule states positivity, a closed form, an equality to an execution
term, or the final program-correctness proposition. There are no
`simplification` attributes, so the special simplification classification gate
is satisfied trivially. There is also no candidate `PROVED_DERIVED_LEMMA` whose
two-stage proof history would need validation.

This classification matches the supplied operational semantics. Expression
strictness evaluates the integer operands, `applyBin("+", I1, I2)` uses K
integer addition, assignments update the active scope in source order, and the
while rules evaluate `i < n`, run the body when truthy, and re-enter the loop.
After `i` iterations the source variables satisfy
`a=fib4Spec(i)`, `b=fib4Spec(i+1)`, `c=fib4Spec(i+2)`, and
`d=fib4Spec(i+3)`; the ordered body shifts this tuple and computes the fourth
successor. The loop circularity in `spec.k` states that invariant, while the
separate `fib4-correct` claim connects the exact closure and complete body to
`fib4Spec(N)`. That connection is a claim proved over fixed semantics, not an
execution-bypassing rule in `verification.k`.

As finite adversarial support, an independent transition simulator agreed with
the recurrence for every integer from -8 through 30. Changing the source
initial value `c` from 2 to 3 changed the result at `n=2` from 2 to 3, while a
three-term recurrence mutation changed the value at `n=6` from 8 to 6. These
checks are supporting sensitivity evidence, not a substitute for the syntactic
and semantic classification above.

Conclusion: all five protected `DEFINITION` classifications are correct, and
the true domain-lemma set is genuinely empty.

## Deterministic Stage 4 audit

The authenticated generator binds the exact Stage 1 export digest
`2122f1b25ec38b26228f18a23211a94ede83b19f6b2a8330addc82684d348e38`,
Stage 3 digest
`578cb9129abc7c7290bce73311734e8271f8ea64b95e9638f5845af6d49c3994`,
inventory digest above, and generated-tree digest
`de97f2ce971ebd647dcd0d26ff0b82e9196ef26e83054c830a17cab05e04a1d3`.
The toolchain object exactly equals `/reference/klean-toolchain.lock.json`.

I reran `tools.klean_preflight.check_generation` directly with the required
three inputs and pinned lock. Its fresh copied project completed both
`lake clean` and `lake build` with exit code 0. The returned evidence is:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: 0
- target: null
- designated sorry count: 0
- trust declaration count: 43
- Stage 1, Stage 3, and generated-tree hashes: exact matches

The initial Lean launch exposed a sandbox-only PID namespace mismatch: Lean
looked up `/proc/<namespace-pid>/exe`, but `/proc` exposed host PIDs. A narrow
recorded compatibility shim retried only that missing numeric executable path
through `/proc/self/exe`; Lean then reported the pinned 4.22.0 commit and the
trusted API completed. The final build output SHA-256
`67006c676bd96e06a7814af9d2d73b026858333f6f7681ef0a0bca91416dad09`
also matches the recorded Stage 4 preflight. No candidate or reference artifact
was modified.

Independent of the preflight implementation, I compared each classification
partition in `input-manifest.json` to the reconstructed inventory. The exact
expected domain source-rule list is empty; `input-manifest.json` and
`obligation-map.json` both contain that exact empty list. The obligation list
and trust-parameter list are empty, the generator obligation count is zero,
and the obligation-map SHA-256
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
matches its manifest. Therefore there is no omission, duplicate, irrelevant or
weakened obligation, or vacuous conjunct.

`tools.klean_export.target_statement` returns null, and
`expected_target_definition` returns null. This matches the generator manifest,
preflight, export result, signed audit input, empty `Lemmas.lean` namespace, and
manual generated-source scan. The generated executable/model declarations in
the 43-entry trust inventory do not prove a proposition; preflight reconciled
them exactly and rejected proposition trust. With no obligation or target, they
cannot serve as a hidden Lean proof.

The selected `KLEAN_NO_OBLIGATIONS` status is consequently correct.

## Stage 5

Stage 5 is inapplicable. Both launcher sources select `CLASSIFICATION_ONLY`, the
fixed generated target is null, `/candidate` is absent, and the signed Stage 5
fields are null. Creating `Base`, rebuilding a candidate, printing axioms for
`Proof.final`, and auditing target parameters would be incorrect in this mode
because neither `Proof.final` nor any target parameter exists.

## Evidence

The exact command ledger is [evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md).
Key raw results are:

- [Inventory reconstruction](/audit-output/evidence/04-inventory-reconstruction.txt)
- [Producer and full provenance authentication](/audit-output/evidence/03-hash-and-producer-authentication.txt)
- [Trusted `check_generation` result](/audit-output/evidence/12-check-generation-success.txt)
- [Independent Stage 4 bijection and target check](/audit-output/evidence/14-stage4-bijection-and-target.txt)
- [Operational counterfactuals](/audit-output/evidence/15-stage3-semantic-counterfactuals.txt)
- [Final immutability rehash](/audit-output/evidence/17-final-immutability-rehash.txt)

VERDICT: PASS
LEGITIMACY: LEGIT
