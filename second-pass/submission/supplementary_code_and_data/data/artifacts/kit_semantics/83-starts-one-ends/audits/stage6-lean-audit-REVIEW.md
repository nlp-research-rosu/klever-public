# Independent audit: `83-starts-one-ends` / `kit-semantics`

## Result

The selected `KLEAN_NO_OBLIGATIONS` result is legitimate. The frozen Stage 1
verification module has no local rules, so the independently reconstructed
Stage 3 domain-lemma set is genuinely empty. Stage 4 preserves that empty set
bijectively, emits no obligation and no target proposition, and the launcher
correctly selected `CLASSIFICATION_ONLY` with no Stage 5 candidate.

This review does not rely on the earlier Stage 2 verdict or the protected Stage
3 classification as authority. It reconstructs the relevant facts from the
frozen source and trusted tools. Raw commands and results are under
`/audit-output/evidence/`; the concise command index is
`evidence/COMMANDS.md`.

## Scope and launcher mode

`AUDIT_MODE` and `/audit-input.json` both record `CLASSIFICATION_ONLY`.
`semantics_mode` is `SUPPLIED_SEMANTICS`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; the audit input has null Stage 5 workspace, invocation,
result, and hashes. `/candidate` is absent. Evidence:
`00-audit-mode.txt`, `01b-audit-input.txt`, `50-comprehensive-integrity-check.txt`,
and `55-no-candidate-check.txt`.

## Input and producer integrity

Before assessing Stage 4, I hashed the exact mounted producer sources. The
observed hashes are:

| Producer input | SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |
| Complete producer bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

The two file hashes match both `generator-manifest.json` and
`source-manifest.json`. The producer bundle contains exactly those two files
plus `source-manifest.json`. The image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in both manifests, and it matches the content-addressed producer path recorded
by `/audit-input.json`. Producer provenance is therefore present and
consistent; there is no infrastructure `AUDIT_ERROR`. Evidence:
`17-producer-source-manifest.txt`, `18-direct-sha256.txt`,
`19-producer-provenance-crossrefs.txt`, and
`50-comprehensive-integrity-check.txt`.

I also independently recomputed every top-level tree hash recorded by the
launcher:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace tree | `6af3781781c45f2f6b47c63668ad8e31ffa5263efffde8d993911bb1dfb667f7` |
| Stage 1 deterministic-export tree | `761719d9d41c7ef5e6804c14eda8f1d75ffed34c46596244bb1584cf66db4135` |
| Stage 3 discovery manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Selected Stage 2 audit tree | `816cb2fd1e431c153a72fe846120f8a43c51057c1a1a77b0a95b67e22dad9c22` |
| Selected Stage 4 generation tree | `7e19c1510462ac2dc7c2eae7019f3e1a18ff68a1fb3578520494d92de03b95f9` |
| Producer-source bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| Generated Lean tree | `18cd73dfa2f9ed027ed536ea33074fa7c677fe787b22dc87a0cb977635e122cb` |

All match `/audit-input.json`, the selection artifact hashes, and the relevant
Stage 4 sidecars. I additionally recomputed the complete bijective set of 770
Stage 1 per-file hashes: there are no missing, extra, or mismatched paths.
Evidence: `50-comprehensive-integrity-check.txt`.

## Stage 3 inventory reconstruction

The trusted `tools.k_rule_inventory.inventory_verification` was run directly
with `PYTHONPATH=/reference` against `/reference/k-proof`. It reconstructed:

- verification file SHA-256:
  `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`;
- selected verification module: `VERIFICATION`;
- local verification-module closure: exactly `["VERIFICATION"]`;
- rules: `[]`; and
- canonical inventory SHA-256:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

The source itself corroborates the result: `verification.k` consists only of a
`requires` line, module `VERIFICATION`, `imports MPY`, and `endmodule`. It has no
`rule` sentence. The imported `MPY` modules live in the frozen supplied
semantics; they are not proof-local additions declared in `verification.k` and
are not members of the trusted inventory tool's local source closure.

The reconstructed rule sequence and inventory hash equal
`/reference/lemma-discovery.json` exactly. Because both sequences are empty,
there are no source spans, normalized rule hashes, `source_rule_id` values, or
classifications that could have been omitted, duplicated, reordered, changed,
or left unaccounted. The trusted Stage 3 boundary validator independently
accepted the same document. Evidence: `04-verification-k.txt`,
`08-lemma-discovery.txt`, `20-reconstructed-rule-inventory.json.txt`,
`21-independent-verification-lexical-check.txt`, and
`50-comprehensive-integrity-check.txt`.

## Independent classification and mathematical judgment

The independent classification counts are all zero:

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0
- rules bearing `simplification`: 0

Thus there is no rule whose behavioral category is disputed, no purported
derived lemma requiring an earlier bridge-free proof, and no simplification
that can conceal a domain lemma.

The empty domain set is also consistent with the frozen program and operational
K proof. The source function is exactly:

```python
return 1 if n == 1 else 18 * 10 ** (n - 2)
```

The two K claims reproduce that exact translated body and partition the stated
positive-integer domain into `N ==Int 1` and `N >Int 1`. Under the supplied
semantics, `Call` resolves the module closure and evaluates/binds the argument;
`Compare` dispatches integer equality; `IfExp` selects the corresponding
branch; integer subtraction, multiplication, and nonnegative exponentiation
evaluate through `applyBin`; and `Return` produces the value and pops the call
frame. For `N > 1`, the exponent `N - 2` is nonnegative, so the supplied integer
power rule applies. No proof-local rewrite or mathematical oracle is needed.

The formula is relevant to the prompt as well: for one digit only `1` counts;
for more digits, inclusion-exclusion gives
`10^(n-1) + 9*10^(n-2) - 10^(n-2) = 18*10^(n-2)`. This calculation is not
installed as a K simplification or hidden assumption—the program already
returns that expression, and the Stage 1 reachability claims establish the
program's operational return value. Evidence: `05-spec-k.txt`,
`06-solution-py.txt`, `07-solution-mpy.txt`, `24-operational-semantics-relevant-rules.txt`,
and `25-problem-prompt.txt`.

## Deterministic Stage 4 audit

I invoked the required trusted function
`tools.klean_preflight.check_generation` with:

- frozen input `/reference/k-proof`;
- discovery manifest `/reference/lemma-discovery.json`;
- generation `/reference/klean-generation`; and
- toolchain lock `/reference/klean-toolchain.lock.json`.

The first attempt exposed a sandbox-only Lean launcher problem: this audit
environment hides `/proc/<pid>/exe`, so Lake/Lean could not locate their own
installation. The failure is preserved in `32-rerun-klean-preflight.txt`. I
compiled a narrow, recorded interposer which substitutes only that executable
location using the process's absolute invocation name; it does not alter Lean
sources, generated artifacts, imports, or theorem checking. Its source and
hash are in `lean_proc_self_exe_interposer.c` and
`51-local-audit-helper-hashes.txt`, and the successful Lean version probe is in
`48-interposed-lean-version.txt`.

With the pinned Lean paths and that location-only workaround, the unmodified
trusted `check_generation` completed successfully. It independently copied and
clean-built the generated project, re-snapshotted all immutable inputs, and
returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- `lake clean` exit `0` with empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit `0` with output hash
  `692ba8a74b2c0fcbbbfd12bdd267bce61152521cf940c3920562187e38ae957b`;
  and
- the same frozen-input, discovery, and generated-tree hashes listed above.

The build output hash and complete returned evidence exactly match the recorded
Stage 4 preflight. Evidence: `49-rerun-klean-preflight-success.txt`.

Independent sidecar checks reached the same result. `input-manifest.json` has
`source_rules: []`; `obligation-map.json` has `source_rules: []`,
`obligations: []`, and `trust_parameters: []`; all three recorded obligation
counts are zero. The obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
and matches the generator manifest. Therefore the source-rule/obligation
bijection is exact and empty—there are no omitted or duplicated obligations,
no irrelevant or weakened statements, and no vacuous conjuncts.

The deterministic expected target is `None`. The observed generated target is
also `None`; `generator-manifest.json` and `/audit-input.json` both record
`target: null`. The top-level generated module contains imports only, and the
generated `Lemmas` namespace has no proposition declaration. The 41 generated
trust declarations are executable collection-hook parameters recorded exactly
in `trust-inventory.json`; the trusted preflight finds no proposition trust and
no proof hole. Evidence: `09-generator-manifest.txt`, `10-input-manifest.txt`,
`13-obligation-map.txt`, `14-export-result.txt`, `16-generated-target-module.txt`,
`22-stage4-file-sha256.txt`, `31-stage4-trust-inventory.txt`,
`52-generated-lemmas.txt`, `53-generated-rewrite.txt`, and
`54-generated-trust-and-target-scan.txt`.

## Stage 5 disposition

Stage 5 is not applicable. A genuinely empty independently classified domain
set requires no generated theorem and no proof candidate. Both conditions hold:
the fixed Stage 4 target is absent and `/candidate` is absent. Accordingly no
Lean `Proof.final`, axiom printout, candidate definition, or operational-bridge
parameter exists to audit.

## Conclusion

All provenance, inventory, classification, bijection, and target-identity
checks pass. The selected no-obligation outcome is mathematically consistent
with the frozen source and supplied operational semantics, not merely
self-consistent at the manifest level.

VERDICT: PASS
LEGITIMACY: LEGIT
