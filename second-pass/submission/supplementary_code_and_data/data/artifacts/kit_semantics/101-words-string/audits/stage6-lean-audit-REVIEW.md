# Independent audit: `101-words-string`, `kit-semantics`

## Audit result

The protected Stage 3 classification is complete and correct, and the selected Stage 4 status `KLEAN_NO_OBLIGATIONS` is legitimate. The frozen local verification-module closure contains no rules at all, so the independently classified domain-lemma set is genuinely empty. Stage 4 maps the empty source-rule list bijectively to an empty obligation list, emits no target, and has no Stage 5 candidate.

I treated the candidate/provenance files and all earlier reviews and logs as untrusted evidence. I did not use the prior Stage 2 verdict or Stage 1 narrative as authority. Trusted code from `/reference/tools` was used for inventory reconstruction and the required mechanical preflight; the classification and mathematical relevance judgment below are independent.

## Scope and mode

- `AUDIT_MODE`: `CLASSIFICATION_ONLY`
- Launcher mode: `CLASSIFICATION_ONLY`
- Problem: `101-words-string`
- Condition: `kit-semantics`
- Semantics mode: `SUPPLIED_SEMANTICS`
- `/candidate`: absent
- Launcher `lean_workspace`, `lean_invocation`, and `target`: all `null`

The Stage 5 proof-only checks—copying a candidate as `Base`, candidate clean build, prohibited-token scan, `#print axioms Proof.final`, proof identity, and candidate parameter bridge testing—are therefore not applicable. Running them would contradict the no-obligation mode, which requires that no Stage 5 candidate exist.

## Stage 4 producer-source provenance gate

I performed this gate before judging the generated result. Direct SHA-256 recomputation gave:

| Producer | Observed SHA-256 | Generator/source manifests |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | exact match |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | exact match |

The source bundle contains exactly those two files plus `source-manifest.json`. Its independently recomputed pipeline tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, exactly the launcher-recorded value. The immutable image ID is `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` in both the generator manifest and source manifest; the launcher-recorded producer path has the same digest as its final path component. Producer provenance therefore passes and does not trigger `AUDIT_ERROR`.

Raw evidence: `evidence/01-producer-auth.log` and `evidence/08-stage4-integrity.log`.

## Inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` directly on `/reference/k-proof` and separately inspected the numbered source.

| Field | Independently reconstructed value |
|---|---|
| `verification.k` SHA-256 | `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4` |
| Selected verification module | `VERIFICATION` |
| Local verification-module closure | `VERIFICATION` |
| Rule count | `0` |
| Canonical inventory SHA-256 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |

The entire frozen file is:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

`MPY` is supplied by the required frozen semantics, not defined as another local module in `verification.k`; the trusted local-closure algorithm therefore correctly reports only `VERIFICATION`. There is no `rule` sentence in that closure. Consequently there are no source spans, normalized rule hashes, `source_rule_id` values, rule attributes, or rule identities to omit, duplicate, reorder, or alter.

The protected `/reference/lemma-discovery.json` is exactly schema 2, the same inventory hash, and the same ordered rule array `[]`. The comparison is a bijection, including uniqueness checks, with no extra or unaccounted entry.

Raw evidence: `evidence/02-rule-inventory.log`.

## Independent classification judgment

The independent category counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |
| Rules carrying `simplification` | 0 |

This is not an empty classification hiding a source-level fact. The frozen solution is:

```python
def words_string(s):
    return s.replace(",", " ").split()
```

The supplied operational semantics rewrites the `replace` method to `replaceC(CS, A, B)`, whose exhaustive recursive equations substitute character `A` with `B`. It rewrites no-argument `split` to an allocated list containing `splitWS(CS, .IntSeq, .ValSeq)`, whose exhaustive equations split on the supplied semantics' whitespace predicate and drop empty tokens. The frozen K postcondition is exactly:

```k
0 |-> list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))
```

Thus the postcondition records the direct operational result of comma code point `44` being replaced by space code point `32` and then split. `replaceC`, `splitWS`, `flushTok`, and `isWSC` are definitions/operational machinery in the fixed supplied `MPY` semantics; they are not proof-local extensions installed by Stage 1 and are not concealed domain lemmas. The postcondition asserts no additional aggregate, ordering, membership, or other human-facing domain fact about the returned list. No derived rule was used before being proved, and no domain lemma—relevant or irrelevant—exists in the local inventory.

Accordingly, the true Stage 3 domain-lemma set is `[]`. The rule that every `simplification` entry must be a `DEFINITION` or `DOMAIN_LEMMA` holds vacuously because there are no local simplification rules.

Raw evidence: `evidence/03-operational-classification.log`.

## Stage 4 preflight and independent integrity checks

I reran the required function with the exact immutable arguments:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The audit container initially prevented Lean from locating itself: namespace-local PIDs have no corresponding `/proc/<pid>/exe` entry. The two initial attempts failed before elaboration and are preserved in `evidence/04-check-generation.log` and `evidence/05-check-generation-elan.log`. I diagnosed this rather than treating it as a verdict. The source and hash of a narrow `LD_PRELOAD` shim are recorded in `evidence/pidns_readlink_shim.c` and `evidence/06-pidns-shim.log`; it changes only `/proc/<pid>/exe` reads to the equivalent `/proc/self/exe`. It does not modify any frozen input, generated source, target, or Lean declaration.

With that container-only path repair, the unchanged trusted `check_generation` returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- `lake clean` exit `0`;
- `lake build` exit `0`, ending in `Build completed successfully.`;
- generated-tree hash `5c48dd393f77ec9ae9cd5d18518beb7f5572bc43d07a3177cc829f21e512fd6f`;
- frozen Stage 1 tree hash `5507aa9a85398bacfc4d0486561a31a5d25e16ccb514bcb3c8ca176bcf3f16fc`; and
- protected Stage 3 manifest hash `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`.

The returned JSON is preserved exactly in `evidence/07-check-generation-success.log`.

I then independently recomputed every launcher resolution hash, both Stage 4 producer hashes, all 769 launcher-recorded Stage 1 per-file hashes, the Stage 1 export digest, selected Stage 2 and Stage 4 artifact tree hashes, discovery hash, generated-project digest, obligation-map hash, trust-inventory hash, and every cross-manifest provenance binding. There were zero missing files, extra files, or mismatches. The generator toolchain object exactly equals `/reference/klean-toolchain.lock.json`.

The source-rule/obligation identity is the exact ordered bijection:

```text
independently classified DOMAIN_LEMMA rules = []
input-manifest source_rules               = []
obligation-map source_rules               = []
obligation-map obligations                = []
obligation-map trust_parameters           = []
```

There are no conjuncts that could be irrelevant, weakened, duplicated, or vacuous, and no omission because the independently determined eligible set is empty. The trusted target parser returns `None`, the deterministic expected-target constructor returns `None`, both manifests record `target: null`, and the generated `Lemmas.lean` namespace contains no target declaration. The generated base project has 41 trust declarations exactly reconciled by the trusted preflight with `trust-inventory.json`; its independent proposition-trust check accepts none as a target proposition or proof. Since there is no target theorem, those generated representation declarations are not a Stage 5 proof or a substitute target.

Raw evidence: `evidence/07-check-generation-success.log`, `evidence/08-stage4-integrity.log`, and `evidence/09-target-and-candidate.log`. The verification script itself is `evidence/verify_stage4_integrity.py`.

## Conclusion

The Stage 3 inventory is exactly and genuinely empty, its protected classification is bijective with the frozen local verification closure, and the operational source/postcondition requires no domain lemma. The authenticated Stage 4 producer deterministically preserves that empty set as zero obligations and no target. `KLEAN_NO_OBLIGATIONS` is therefore the correct status, and the absence of a Stage 5 candidate is required rather than missing work.

VERDICT: PASS
LEGITIMACY: LEGIT
