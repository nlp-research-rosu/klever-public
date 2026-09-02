# Independent Stage 3–4 audit: `94-skjkasdkd`

## Result and scope

I independently audited HumanEval `94-skjkasdkd`, condition `bare`, semantics
mode `GENERATED_SEMANTICS`. Both `AUDIT_MODE` and the signed launcher input
select `CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate`, a Stage 5 result, Lean workspace hashes,
and a fixed target are all absent. Therefore the Stage 5 proof, candidate
bridge, `Proof.final`, and axiom-accounting procedures do not apply.

I treated every mounted candidate/provenance statement as untrusted evidence.
I did not rely on the prior Stage 2 review or any earlier PASS/classification.
The final judgment comes from the frozen K source, the trusted rule inventory,
the trusted preflight, the producer sources and manifests, and independent
hash/bijection checks recorded in `evidence/`.

## Producer-source infrastructure gate

This gate passes:

- `/reference/generation-tools/klean_export.py` hashes to
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`.
- `/reference/generation-tools/klean.py` hashes to
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`.
- Those exact values occur in both `generator-manifest.json` and
  `source-manifest.json`.
- Both manifests name generator image
  `sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
  The launcher's immutable producer-bundle path ends in the same image digest.
- The trusted pipeline tree digest of the three-file producer bundle is
  `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
  exactly the value in `/audit-input.json`.

The raw producer hashes are in `evidence/01-producer-sha256.txt` and
`evidence/03-producer-pipeline-tree-sha256.txt`.

## Inventory reconstruction and manifest bijection

I ran `tools.k_rule_inventory.inventory_verification` from `/reference` against
the frozen `/reference/k-proof`. The selected main module is `VERIFICATION`.
Its local verification-file closure contains only that module: `SEMANTIC` is
required from `semantic.k`, not a module declared in `verification.k`, so its
ordinary execution rules are outside this local inventory.

The canonical reconstruction found 15 rules. It recomputed every source span,
normalized source hash, and `source_rule_id`. The reconstructed
`verification.k` hash is
`2104440e5a6df97da9a6a8405876b8a2fd2ef55a1209ff365b6b8b90324d6917`;
the canonical whole-inventory hash is
`3e46f41fca2b599e817e692c7ef1252c24ce1b5baf274b23def3e831810479fe`.

The 15 protected Stage 3 IDs are in exactly the same order as the canonical
inventory. There are no omissions, duplicates, unknown/extra IDs, or reordered
identities. Every ID is exactly `rule-` followed by its reconstructed
normalized SHA-256. Stage 4's input manifest additionally preserves the full
15 reconstructed records—including text, module, span, attributes, normalized
hash, ID, classification, and rationale—without change. The complete canonical
records are in `evidence/04-reconstructed-inventory.txt`; the programmatic
bijection check is in `evidence/15-complete-hashes-and-bijections.txt`.

## Independent classification judgment

All 15 entries are genuinely `DEFINITION`. None is a domain lemma, ordinary
operational rule, or proved-derived lemma.

| Frozen lines | Defined term | Independent classification and reason |
|---:|---|---|
| 9–44 | `solutionProgram` | `DEFINITION`: macro/named proof term giving the exact translated program AST. |
| 48 | `programDefs` | `DEFINITION`: structural summary extracting the definition map via `collectDefs`. |
| 49 | `solutionDefs` | `DEFINITION`: named macro/proof term for the definition map of `solutionProgram`. |
| 54–55 | `refPrimeFrom`, square bound | `DEFINITION`: base equation of the primality-search recurrence. |
| 56–57 | `refPrimeFrom`, divisible | `DEFINITION`: divisibility branch of the same recurrence. |
| 58–59 | `refPrimeFrom`, advance | `DEFINITION`: recursive `D + 1` branch of the same recurrence. |
| 60 | `refPrime`, below two | `DEFINITION`: base equation matching the source helper. |
| 61 | `refPrime`, entry | `DEFINITION`: recurrence entry at divisor two. |
| 67–68 | `refChoose`, replace best | `DEFINITION`: true branch of the prime/greater-than selection summary. |
| 69–70 | `refChoose`, retain best | `DEFINITION`: complementary false branch of that summary. |
| 71–72 | `refLargest`, empty | `DEFINITION`: empty-list base equation returning zero. |
| 73–74 | `refLargest`, nonempty | `DEFINITION`: tail-recursive list summary followed by `refChoose` on the head. |
| 75 | `refDigitSum`, one digit | `DEFINITION`: base equation for values below ten. |
| 76–77 | `refDigitSum`, decimal recurrence | `DEFINITION`: last digit plus the summary of the quotient by ten. |
| 78 | `refAnswer` | `DEFINITION`: top-level composition `refDigitSum(refLargest(VS))`. |

This classification follows behavior, not names:

- The first three rules define macros or named proof terms and do not rewrite
  a running `<k>` configuration.
- The remaining twelve are guarded base/recursive equations for the exact
  summaries used by the six reachability claims in `spec.k`.
- No rule asserts an algebraic, number-theoretic, induction, or other
  mathematical fact about already-defined operations. Thus no rule is a
  `DOMAIN_LEMMA`.
- No inventory rule is an ordinary execution/observation rule: none rewrites a
  `<k>`, `<result>`, environment, continuation, or control cell. The operational
  rules that do so are in the separately required `semantic.k`.
- No rule is a `PROVED_DERIVED_LEMMA`. Stage 1 performs one later `kprove`
  against `VERIFICATION`, which already contains all 15 rules; there is no
  earlier proof of any exact inventory rule against a module with that rule
  removed.
- The canonical inventory reports an empty attribute list for every entry, so
  there are no `simplification` rules to account for.

## Source-program and operational-semantic relevance

The classification is also mathematically relevant to the frozen program and
postcondition:

- `solutionProgram` reproduces the six source functions and their binding,
  argument order, branches, recursion, list indexing/slicing, and top-level
  composition.
- In `semantic.k`, `invoke` resolves the selected definition map, `invokeDef`
  binds parameters to evaluated arguments, and `execStmts`/`eval` implement
  returns, conditionals, left-to-right expression evaluation, calls, list
  length, head/tail slicing, integer arithmetic/comparison, and final result
  storage.
- `refPrimeFrom` mirrors `is_prime_from`: stop true when `D² > N`, stop false
  on divisibility, otherwise advance `D`. The proof-use domain has `N ≥ 2` and
  `D ≥ 2`; the `refPrime` entry uses `D = 2`, so the recurrence descends toward
  the square bound over every relevant call.
- `refPrime`, `refChoose`, `refLargest`, and `refDigitSum` match the source
  branches exactly. For the final source domain, `refLargest` returns zero or
  a prime, so `refDigitSum` receives a nonnegative value and its division-by-ten
  recurrence descends.
- `refAnswer` is exactly the postcondition used by the final claim:
  the digit sum of the largest prime selected from the input list.

Counterfactual changes are discriminating: changing any primality branch,
the `N > BEST` test, the empty-list value, head/tail recursion, decimal base,
`% 10`, `/ 10`, or final composition would change the corresponding summary
equation and break its exact match to the source execution claims. Constant,
identity, hard-coded-example, vacuous, and unrelated summaries are not present.

Consequently the true independently classified domain-lemma set is genuinely
empty. This is not a case where a necessary source/postcondition fact was
hidden under `DEFINITION`.

## Deterministic Stage 4 generation

The required trusted call to
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation)` passes with the
pinned lock. Its returned evidence is:

- status `KLEAN_NO_OBLIGATIONS`;
- frozen/Stage 1 digest
  `f8e6c8a40dd84c14bcb8f84579488c2c24eaf4d47fdb7da104955cd3b982bb77`;
- Stage 3 manifest digest
  `2931c4e6ea7395df875eb2d8765506a33a3fc4708a8d6235b6a86bd046e26b28`;
- generated tree digest
  `cabb68075ffc40033f95e15648b2879574a9df55d1c0a8d4c8193ea9e2af2f88`;
- obligation count zero, target `null`, designated sorry count zero;
- `lake clean` exit 0 and `lake build` exit 0 with output hash
  `74c12b41b87a2ab536b40cf9bc8f82a00516efcb072638e9fdf4ab579f74c1c0`.

The first preflight attempt exposed a sandbox infrastructure quirk: Lean
4.22's `IO.appPath` asks for `/proc/<getpid()>/exe`, while this container's
namespace-local PID does not occur in its mounted `/proc`. I recorded that
failure, then used the source-recorded preload shim that redirects only this
exact readlink shape to `/proc/self/exe`. The shim does not alter Lean source,
imports, elaboration, build output, manifests, or project files. With it, the
actual pinned Lean reports commit `ba2cbbf...`, and the required trusted
preflight returns byte-for-byte the same diagnostics and hashes as the selected
preflight. See `evidence/11-rerun-check-generation.txt`,
`evidence/proc-self-readlink.c`,
`evidence/16-proc-shim-build-and-toolchain.txt`, and
`evidence/13-rerun-check-generation-success.txt`.

I separately recomputed every recorded launcher and Stage 4 file/tree hash,
the signed audit-envelope digest, the mechanical-checker lock, selection
artifact hashes, producer hashes, toolchain lock, input/generator/export
provenance, obligation-map hash, and trust-inventory hash. All comparisons pass.

The independently classified domain set, Stage 4 `source_rules`, obligation-map
`source_rules`, obligation list, and trust-parameter list are all exactly empty.
This is an exact empty-to-empty source-rule/obligation bijection: no omission,
duplicate, weakened/irrelevant obligation, or vacuous conjunct exists.
`generator-manifest.json`, the launcher input, selected preflight, and the
generated project itself all have no target. The generated root module contains
imports only; it does not substitute `True` or another target. No Stage 5
candidate/result exists.

## Conclusion

Stage 3's all-definition classification is correct for every canonical local
rule. The true domain-lemma set is empty. Deterministic Stage 4 faithfully
preserves the frozen inputs and correctly emits no obligation and no target.
The selected `KLEAN_NO_OBLIGATIONS` status is legitimate, and proof-mode checks
are correctly inapplicable.

VERDICT: PASS
LEGITIMACY: LEGIT
