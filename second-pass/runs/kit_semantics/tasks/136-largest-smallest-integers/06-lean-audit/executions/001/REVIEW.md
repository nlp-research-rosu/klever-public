# Independent Stage 3–4 audit: `136-largest-smallest-integers`

## Scope and result

The launcher-signed input and `AUDIT_MODE` both select `CLASSIFICATION_ONLY` for condition `kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. There is no Stage 5 workspace or invocation, and `/candidate` is absent. I therefore audited the frozen K rule classification and deterministic Klean generation; the Stage 5 proof-only checks are not applicable.

The independently reconstructed inventory contains one rule. That rule is legitimately a `PROVED_DERIVED_LEMMA`, so the true `DOMAIN_LEMMA` set is empty. The selected Stage 4 status `KLEAN_NO_OBLIGATIONS`, empty obligation map, absent generated target, and absent Stage 5 candidate are consequently correct.

## Producer provenance gate

I hashed the mounted generation-time producer sources before judging Stage 4:

| Producer | Observed and recorded SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values match `source-manifest.json` and `generator-manifest.json`. The immutable generator image ID is consistently `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` in the source manifest, generator manifest, and the image-keyed producer path signed into `/audit-input.json`. The producer bundle has exactly the two producer files plus its source manifest, and its independently recomputed tree hash is the launcher-recorded `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`. There is no producer-provenance infrastructure error.

Raw evidence: `evidence/01-producer-provenance-summary.log`, `evidence/02-producer-provenance-detail.log`, and `evidence/21-independent-hash-and-bijection-check.log`.

## Inventory reconstruction and bijection

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on `/reference/k-proof`, rather than copying the protected Stage 3 result. It reconstructed local verification-module closure `VERIFICATION`, with frozen `verification.k` SHA-256 `6e4825b68cf2c55b75971a9ff0019687ceb7e38975c74e7aa27d69bf93c3032d`.

The closure contains exactly this one rule:

| Field | Reconstructed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | `verification.k:10–31` |
| Attributes | `priority(40)` |
| Normalized SHA-256 | `163a865d82cdbf32cce773c75722becea55fcde50e42abef6f61661a7069c3a7` |
| `source_rule_id` | `rule-163a865d82cdbf32cce773c75722becea55fcde50e42abef6f61661a7069c3a7` |

The canonical whole-inventory hash is `6fdd0cbfc0fcd25cfdce05c3a734b3788c827b816a694cad314c9821edce6a7c`. The protected discovery document contains exactly one unique entry with that same ordered identity and whole-inventory hash. The trusted discovery validator also reconstructs the same source span, text, normalized hash, and identity. There are no omitted, duplicated, extra, reordered, or hash-changed rules, and every inventory entry has exactly one classification.

Raw evidence: `evidence/04-independent-rule-inventory.log`.

## Independent classification judgment

The rule summarizes execution of

`#loop(list(intVals(IS)), Name("value"), lsiLoopBody)`

in the exact function scope. Operationally, the supplied semantics converts a `For` to `#loop`, advances a list one element at a time with `#iterNext`, binds each element, runs `lsiLoopBody`, and resumes the residual loop. The frozen recurrence `scanNeg` updates only for a negative integer closer to zero, `scanPos` updates only for a smaller positive integer, and `lastValue` tracks the loop variable's final value. Thus the rule removes the completed loop while updating `largest_negative`, `smallest_positive`, and `value` to the exact fold summaries computed by that execution. This is directly relevant to the source implementation and its return postcondition.

The rule qualifies as `PROVED_DERIVED_LEMMA`, rather than an unproved operational bridge or a domain lemma, for all of the following independently checked reasons:

1. `loop-spec.k` states the identical configuration transition and identical guard. A whitespace-insensitive source comparison is equal after removing only the sentence-kind header and the installed rule's priority metadata. The arbitrary continuation and framed/omitted cells are the same on both sides.
2. `LOOP-SPEC` imports `VERIFICATION-CORE`, not `VERIFICATION`. `verification-core.k` contains the loop body and truthful recursive summaries but does not contain the installed loop-summary rule.
3. In a fresh directory, I compiled `verification-core.k` from frozen source and ran:

   ```text
   kprove loop-spec.k --definition verification-core-kompiled --spec-module LOOP-SPEC
   #Top
   EXIT_CODE: 0
   ```

4. Only after that bridge-free proof, I freshly compiled `verification.k` and ran the later entry proof:

   ```text
   kprove spec.k --definition verification-kompiled --spec-module SPEC
   #Top
   EXIT_CODE: 0
   ```

5. The frozen Stage 1 driver records the same order: compile/prove the core connection at lines 28–34, then compile `verification.k` and prove `spec.k` at lines 36–42. Priority changes rule selection but neither broadens the proved match domain nor changes the already-proved transition.
6. The guard is satisfiable, for example with `N = 0`, `P = 0`, `CURRENT = 0`, and an empty or finite integer sequence; this is not a vacuous implication.

The rule has no `simplification` attribute. Therefore the constraint that every simplification rule be a `DEFINITION` or `DOMAIN_LEMMA` is satisfied vacuously. No inventory entry is a material, unproved mathematical fact about largest negatives or smallest positives. My independent classification is exactly one `PROVED_DERIVED_LEMMA` and zero `DEFINITION`, `OPERATIONAL_RULE`, or `DOMAIN_LEMMA` entries.

Raw evidence: `evidence/05-frozen-proof-sources.log`, `evidence/06-fresh-loop-connection-proof.log`, `evidence/08-corrected-rule-claim-comparison.log`, and `evidence/09-fresh-later-stage1-proof.log`.

## Deterministic Stage 4 generation

The immutable producer constructs Stage 4 `source_rules` only from validated `domain_lemmas`, preserves their order and provenance, requires the generated obligation IDs to equal those source IDs bijectively, and defines a target only when the obligation list is nonempty.

Because the independently classified domain set is genuinely empty:

- `input-manifest.json` has `source_rules: []`;
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and `trust_parameters: []`;
- the expected target definition is `None`;
- independent `target_statement` extraction returns `None`;
- the generator manifest, recorded preflight, fresh preflight, and audit input all record `target: null` and obligation count zero; and
- the generated `Lemmas.lean` namespace contains no target proposition.

There are no conjuncts that could be irrelevant, weakened, duplicated, or vacuous. The exact source-rule/obligation bijection is the unique empty-to-empty bijection, and the fixed target identity is absence of a target. The generated tree hash is `a55ae26ba23aa915ec4008360e06e5ec8ce1498e4b83181472d54902071bccf0`; the obligation-map file hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.

I reran the required trusted call with `PYTHONPATH=/reference`. The sandbox initially denied Lean's `/proc/<pid>/exe` lookup, causing an environmental Lake configuration error. Disassembly localized the failure to that exact `readlink`. I used a narrow preload shim that returns the pinned `/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/{lean,lake}` path only for the current Lean/Lake process's self-executable lookup and delegates every other `readlink`. With it, Lean identified itself as version 4.22.0 at pinned commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unmodified trusted preflight ran normally:

```text
LD_PRELOAD=/tmp/audit-work/readlink_app_path_shim.so PYTHONPATH=/reference \
  python3 -c '... tools.klean_preflight.check_generation(...) ...'

status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
lake clean exit_code: 0
lake build exit_code: 0
lake build output_sha256: 830e27a137e8df217daf93ff10a991550ab4383fe6af8473b11dcc81c0846668
```

The complete fresh preflight result is object-equal to both `/reference/klean-generation/preflight.json` and the copy embedded in `/audit-input.json`. The shim did not modify or shadow any generated source or proof declaration.

Raw evidence: `evidence/19-lean-readlink-shim-validation.log`, `evidence/19a-readlink-shim-source.log`, `evidence/20-preflight-rerun-command.txt`, `evidence/20-preflight-return.json`, `evidence/22-deterministic-generation-and-candidate-absence.log`, and `evidence/23-preflight-object-and-final-scope-check.log`.

## Hash reconciliation

The signed audit-input envelope verifies with resolved-input SHA-256 `d4910f71d82e5c4bf6c9c4242bd0eee47b2514944c675d035b3fe084efdb280e`. I independently recomputed and matched the launcher hashes for the Stage 1 tree, Stage 1 export tree, Stage 2 audit tree, discovery document, complete Stage 4 generation tree, generated project tree, and producer-source tree. I also checked an exact path/hash bijection for all 826 entries in `stage1_source_hashes`, every producer and manifest cross-hash, the trust-inventory hash, pinned toolchain object, verification source hash, inventory hash, obligation-map hash, and every null Stage 5 field. All checks passed with exit code 0.

Raw evidence: `evidence/21-independent-hash-and-bijection-check.log`.

## Stage 5 applicability

`CLASSIFICATION_ONLY` requires no candidate proof. `/candidate` does not exist; the signed `lean_workspace`, `lean_invocation`, and `stage5_result` fields are all null. This is consistent with a legitimate `KLEAN_NO_OBLIGATIONS` generation. Accordingly, no `Base` copy, candidate clean build, `#print axioms Proof.final`, candidate token scan, proof identity check, or `target.parameters` operational-bridge audit applies. The immutable generated Stage 4 project itself was freshly cleaned and built by the required preflight.

## Final judgment

Stage 3 classifies the sole rule correctly as a bridge-free, previously proved derived lemma. The mathematical domain-lemma set is genuinely empty. Stage 4 deterministically and structurally preserves that empty set as zero obligations with no target, and all provenance, identity, hash, build, and mode checks reconcile. No concern remains that would affect legitimacy.

VERDICT: PASS
LEGITIMACY: LEGIT
