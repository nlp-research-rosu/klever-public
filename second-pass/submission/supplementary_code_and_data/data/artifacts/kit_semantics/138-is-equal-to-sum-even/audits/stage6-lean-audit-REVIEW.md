# Independent Stage 3/4 Audit: HumanEval 138

Audit scope: problem `138-is-equal-to-sum-even`, condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. The launcher and `AUDIT_MODE` both select `CLASSIFICATION_ONLY`. I treated the candidate, prior audit, comments, logs, and manifests as untrusted evidence; no prior PASS or classification was used as the basis for this judgment.

## Producer provenance gate

I hashed the two mounted generation-time producer sources before judging Stage 4:

| Source | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values exactly match the file map in `source-manifest.json` and the `exporter_sha256`/`klean_py_sha256` fields in `generator-manifest.json`. The immutable image ID is consistently `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` in the source manifest, generator provenance, and the image-key component of the producer-source path signed into `/audit-input.json`. The producer bundle contains exactly the two producer files and `source-manifest.json`; its independently recomputed tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, matching the audit input. The infrastructure provenance gate therefore passes.

## Inventory reconstruction and Stage 3 classification

Using the trusted `/reference/tools/k_rule_inventory.py`, I reconstructed the local verification-module closure directly from the frozen `/reference/k-proof/verification.k`. `prove.sh` selects `VERIFICATION`; the local closure is exactly `VERIFICATION`. The module only imports fixed supplied-semantics module `MPY` and contains no rule sentence at all:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

Consequently there are no source spans, normalized rule hashes, or `source_rule_id` values to classify. The canonical ordered rule document is `[]`, whose inventory SHA-256 is `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`. The verification source SHA-256 is `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`.

The protected Stage 3 manifest has the same inventory hash and exactly the same ordered empty list. Trusted boundary validation reports zero definitions, zero operational rules, zero proved derived lemmas, and zero domain lemmas. The comparison is bijective: there are no omitted, duplicated, extra, reordered, or hash-changed rules. The restrictions on simplification rules and proved-derived-lemma chronology are vacuously satisfied because the closure contains no rules.

I also checked that the empty domain set is mathematically genuine for this frozen program, rather than a manifest artifact. The source body is:

```python
return n >= 8 and n % 2 == 0
```

The frozen MPY translation is the corresponding short-circuit `BoolOp` over integer `>=`, `%`, and `==`. The supplied operational semantics evaluates calls and returns normally, dispatches integer `%` to `pyMod`, dispatches `>=` and `==` to the integer hooks, and implements value-returning short-circuit `and`. The Stage 1 claim's result is exactly `N >=Int 8 andBool pyMod(N, 2) ==Int 0`; no proof-local summary, bridge, recurrence, or mathematical simplification is inserted. As an intent cross-check, an integer is a sum of four positive even integers only if it is even and at least 8; conversely, any even `n >= 8` is `2 + 2 + 2 + (n - 6)`, with the last term positive and even. This fact explains the source implementation but is not a hidden rule in the verification closure. There is no true inventory domain lemma that Stage 3 failed to expose.

## Signed hashes and immutable inputs

I independently recomputed every signed tree/hash category in the audit input. The Stage 1 artifact tree (`427cd189…`), Stage 1 exporter tree (`c7c0e79e…`), discovery file (`e13c012…`), Stage 2 artifact (`5104cc0c…`), Stage 4 artifact (`a81439ee…`), producer tree (`388cac39…`), and generated tree (`41ab6221…`) all match. The 772-entry Stage 1 source-file hash map has no missing, extra, or mismatched paths. Both Lean workspace/invocation hashes are correctly null. The canonical signed-resolution digest recomputes to `87077655a4322ebd93a8ab5ace2eaff1001ebe08de8d3f2231cfff92b83e8623`, exactly the envelope value.

These checks establish provenance only; the classification and mathematical judgments above were made independently of the selected Stage 2 report.

## Stage 4 source/obligation bijection and target identity

The independently classified domain-rule IDs, Stage 4 input `source_rules`, obligation-map `source_rules`, and generated obligation IDs are all exactly `[]`. The obligation map also has no trust parameters. Thus the source-rule/obligation correspondence is an exact empty bijection, not an omission or duplicate.

The generator manifest and export result both record obligation count zero. The obligation-map SHA-256 recomputes to `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching the generator manifest. The toolchain record exactly equals `/reference/klean-toolchain.lock.json`. The independent inventory hash and verification hash match the Stage 4 input manifest and generator provenance.

There is no conjunct to weaken, make vacuous, duplicate, or omit. Trusted `target_statement` inspection returns `None`, deterministic expected-target construction returns `None`, and the generator manifest and audit input both record `target: null`. `Lemmas.lean` contains no `def`, theorem, axiom, or opaque declaration, and no `Proof.lean` is present. The selected status `KLEAN_NO_OBLIGATIONS` is therefore correct for a genuinely empty independently classified domain set.

## Mechanical preflight

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the mandated Stage 1, Stage 3, Stage 4, and toolchain-lock paths. The managed sandbox initially exposed an outer `/proc` with namespace-local process IDs, causing Lean's `IO.appPath` to fail before project evaluation. I diagnosed this directly and used the recorded, narrowly scoped `LD_PRELOAD` shim in `evidence/lean-pid-shim.c` to translate `getpid()` through `/proc/*/status` `NSpid`. It changes no frozen or generated input and was applied only to the Lean/Lake subprocess environment.

With that environment repair, the actual trusted preflight completed successfully. Its temporary-project `lake clean` exited 0 with empty output; `lake build` exited 0 and built all generated modules. The returned evidence reports:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target `null`;
- designated sorry count 0;
- Stage 1 exporter hash `c7c0e79e…`;
- Stage 3 manifest hash `e13c012…`; and
- generated tree hash `41ab6221…`.

The 41 declarations in the generated generic hook prelude are exactly reconciled by preflight with `trust-inventory.json`; preflight also rejects proposition trust, imports outside policy, and proof holes. They support no target here because no target or obligation exists.

## Stage 5 applicability

Stage 5 is not applicable in `CLASSIFICATION_ONLY`. `/candidate` is absent, the signed Lean workspace and invocation fields are null, and there is no generated target to prove. Therefore a `Base` copy, candidate clean build, `#print axioms Proof.final`, target-parameter bridge audit, and candidate trust-token scan would be inappropriate: each is conditional on `CLASSIFICATION_AND_PROOF`. Their absence is required and confirmed.

## Evidence

- `evidence/00-mode-and-source.log`: launcher mode, frozen verification module, source, and MPY translation.
- `evidence/reconstruct_and_hash.py` and `evidence/01-reconstruct-and-hash.log`: reproducible inventory, producer, complete hash-ledger, bijection, and target checks.
- `evidence/run_preflight.py`, `evidence/02-preflight-initial-error.log`, `evidence/lean-pid-shim.c`, and `evidence/03-preflight.log`: exact preflight invocation, sandbox diagnosis, environment repair, and returned clean-build evidence.
- `evidence/04-target-and-candidate-absence.log`: direct absence checks.
- `evidence/05-operational-semantics.log`: frozen operational rules used in the independent mathematical judgment.

VERDICT: PASS
LEGITIMACY: LEGIT
