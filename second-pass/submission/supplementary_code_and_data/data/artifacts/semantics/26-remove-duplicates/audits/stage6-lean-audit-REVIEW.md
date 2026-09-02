# Independent Stage 3–5 audit: `26-remove-duplicates`

## Result

The selected Stage 3 classification and deterministic Stage 4
`KLEAN_NO_OBLIGATIONS` result are legitimate. The independently reconstructed
verification-module inventory contains seven definitions and no domain lemmas.
Consequently, the empty Stage 4 obligation set, absent generated target, and
absence of a Stage 5 candidate are exactly the required outcome.

The launcher-bound mode is `CLASSIFICATION_ONLY`, condition `semantics`, with
`SUPPLIED_SEMANTICS`. The canonical signed-resolution digest recomputes to
`4fd9d01694b047e7bee697f9cd17fce056f2d755452ee6a53b4eadb6e7466955`.
No Stage 5 proof audit is applicable in this mode.

All mounted candidate, review, log, comment, and provenance content was treated
as untrusted evidence. Conclusions below come from the frozen source, trusted
inventory/checking code, operational-semantics inspection, recomputed hashes,
and fresh mechanical runs.

## Producer-source infrastructure gate

The required Stage 4 producer sources are present and regular. Their observed
SHA-256 hashes are:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
files plus `source-manifest.json`; its recomputed launcher tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`.

The immutable image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
It agrees among the source manifest, generator-manifest provenance, and the
image-addressed producer-source path recorded in `/audit-input.json`. There is
therefore no producer-source infrastructure error.

## Inventory reconstruction and bijection

I ran `tools.k_rule_inventory.inventory_verification` from the trusted
`/reference` code on the frozen `/reference/k-proof` workspace. The selected
module and its local closure are both exactly
`REMOVE-DUPLICATES-VERIFICATION`; no other local module enters the closure.

The frozen `verification.k` hash recomputes to
`7b45d64e2dd9fd46d5a4f3c02b75913141848cdd49e73932004f6dd01457aace`.
The whole canonical rule-inventory hash recomputes to
`e61b7f5b49ab5bec69842b8e4207e5a8cc2bbf1000bbeba3eee1fce538740999`.
Both match the Stage 3 and Stage 4 records.

For each rule, I recomputed the exact source span, whitespace-normalized
source hash, and `source_rule_id = "rule-" + normalized_sha256`:

| Lines | Normalized SHA-256 | Independent class | Reason |
|---|---|---|---|
| 9–9 | `8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Base equation for the newly declared `allInts` predicate. |
| 10–11 | `4b7d8a3dd89930bb1f991f9d000323aad3d585fbda5fd4d1848373fe82de4ec3` | `DEFINITION` | Structural recurrence for `allInts` over a `ValSeq`. |
| 16–17 | `45d546041e07c693a02ce0e4998fc5dd461eeaae328b3591a97828211cae17bd` | `DEFINITION` | Empty-input base equation for the newly declared accumulator summary `keepSinglesAcc`. |
| 18–26 | `f182c17eceebcd68e6c4d08bf4b41078be53cda610c80ce60798a366c6efea7e` | `DEFINITION` | Recursive retain-head equation for `keepSinglesAcc`. |
| 27–32 | `85709daa813b144f2a9305803f8c34a89fc45b5a3840fd340b8b6aa009594317` | `DEFINITION` | Recursive discard-head equation for `keepSinglesAcc`. |
| 36–49 | `442613f43787a483184b024d9daa6f57fe06416478d0dc9655232ec3c4d92fb5` | `DEFINITION` | Expansion of the newly declared `#removeDuplicatesBody` macro to the exact translated loop body. |
| 53–63 | `acbb93cb727d3a609e3ca238b000272a949fbd1c144b42dd558c237dc078cc11` | `DEFINITION` | Expansion of the newly declared `#removeDuplicatesClosure` macro to the exact translated function closure. |

The protected Stage 3 manifest has exactly these seven IDs, once each, in this
order. There are no omitted, duplicated, extra, or reordered identities. Its
classification for every ID is `DEFINITION`, agreeing with the independent
classification. The Stage 4 input manifest preserves the same seven definition
records in the same order.

The three `[simplification]` rules are precisely the base, retain, and discard
equations of the newly declared `keepSinglesAcc` function. They are definitions,
not free-standing algebraic facts. Thus every simplification rule satisfies the
required `DEFINITION`-or-`DOMAIN_LEMMA` restriction.

No inventory entry is an ordinary execution/observation rule: none rewrites a
runtime configuration or preempts the supplied operational semantics. No
inventory entry is a proved-derived lemma. Stage 1 does separately prove the
`loop-invariant` claim before later passing that claim as trusted, but that
claim is in `spec.k` and is not one of the reconstructed `verification.k`
rules. It does not justify or alter any Stage 3 rule classification.

## Mathematical and operational classification judgment

The classifications agree with the frozen program and supplied semantics:

- `allInts` structurally recognizes precisely sequences of K `Int` values.
  Supplied `isIntV` is true on `Int` and false on other `Val` constructors.
- The supplied `For` semantics evaluates/dereferences the iterable once and
  iterates the resulting list snapshot using `#iterNext`.
- `numbers.count(number)` resolves through the non-mutating method path to
  `cntOccVS(ALL, V)`, whose equations count occurrences in the original
  `numbers` sequence.
- `result.append(number)` is the mutating list method whose heap rule appends
  `vCons(number, .ValSeq)` using `valSeqConcat`.
- `keepSinglesAcc(ACC, REST, ALL)` keeps `ALL` fixed, consumes one element of
  `REST` per recursive step, appends the head exactly when
  `cntOccVS(ALL, head) == 1`, and returns `ACC` at the empty tail. This is the
  direct mathematical recurrence for the frozen loop and is not an independent
  domain theorem.
- The two macro expansions match the translated `solution.mpy`: empty result
  allocation, iteration over `numbers`, the exact count comparison, conditional
  append, and return of `result`.

As finite adversarial support for that source-level analysis, an independent
executable model compared the frozen source behavior with the recurrence on all
364 lists of length 0 through 5 over `{-1, 0, 1}` and found zero mismatches.
Counterfactuals were discriminating: changing the fixed original count to a
moving remaining-list count changes `(1, 2, 1)` from `(2,)` to `(2, 1)`;
prepending reverses `(1, 2, 3)`; and a constant-empty summary fails on `(7,)`.
These tests support, but do not replace, the operational-semantic comparison.

There is no true domain lemma. Therefore there is also no irrelevant domain
lemma hidden under another category, and the independently determined domain
set is genuinely empty.

## Recorded hashes and deterministic Stage 4

Every launcher-recorded input hash was recomputed:

| Binding | Recomputed value |
|---|---|
| Stage 1 workspace tree | `930f922364fa1e3b2a0c5a18d8be66c26f22624b4ab3820abccab1cb20ce05f9` |
| Stage 1 export/frozen input | `ed23213559a98770c1d7a93b8bcfb618f28f22f53a270d49669438be36225978` |
| Stage 3 manifest | `44fe7430f8c97c79329bc978eeedeee2a0a19923df04770c7ad440476adbaea6` |
| Selected Stage 2 artifact | `912bb0f084ee713974eccc0deb0c95ad148c5c606fe383f0daa8fead8e968f45` |
| Selected Stage 4 artifact | `0dcc6a40bc639893e681998ad5db7839f9ac62e696456ee4e0eb9182c505fd3c` |
| Producer-source bundle | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |
| Generated project tree | `81a74941e71fc56721d2e72e54541089804faefb417714da46c08110e33150b9` |

The complete 33-file Stage 1 source-hash map also exactly matches
`/audit-input.json`. The Lean workspace and invocation hashes are correctly
null in classification-only mode.

The independently classified domain IDs, Stage 4 input-manifest `source_rules`,
generated obligation-map `source_rules`, and generated obligation IDs are all
the same empty ordered list. The obligation map is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Its SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching `generator-manifest.json`. Obligation counts are zero in the generator
manifest, export result, preflight, and audit input. With no source rules or
conjuncts, there can be no omission, duplication, weakened obligation, irrelevant
obligation, or vacuous conjunct.

The trusted target parser returns `None`. The generator manifest, recorded
preflight, and audit input all record `target: null`, and the generated
`Lemmas.lean` namespace contains no target declaration. Thus the fixed
generated target is genuinely absent, as required for a legitimate
`KLEAN_NO_OBLIGATIONS` result. The generator toolchain record also exactly
matches `/reference/klean-toolchain.lock.json`.

## Fresh preflight and mechanical gate

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the required Stage 1 workspace, Stage 3 manifest, and selected Stage 4
generation. The audit sandbox initially hid `/proc/<getpid>/exe`, while Lean
4.22 uses that path to locate its application. This produced the recorded
infrastructure-only initial failure before any source judgment.

I compiled a narrowly scoped compatibility preload that redirects only
`readlink("/proc/<digits>/exe", ...)` to `/proc/self/exe`. With that sandbox
compatibility in place, the unchanged trusted preflight completed:

- status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: `0`;
- target: `null`;
- trust declaration count: `48`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0;
- build-output SHA-256:
  `2f9c80f1bc7a8413aea4f518ef8d8e2fb74f7427b98a4dd72407d1822d00d994`.

The clean build output hash exactly reproduces the generation-time recorded
output. The preflight also independently revalidated the immutable inputs,
generated tree, source/obligation bijection, target absence, imports, trust
allowlist, absence of generated proof holes, and absence of proposition trust.

I additionally ran the trusted classification-only
`tools.klean_final_gate.check_final`. It returned `status: PASS`,
`mode: CLASSIFICATION_ONLY`, `target: null`, `candidate_sha256: null`, and
`used_axioms: []`. Its `semantic_classification: NOT_EVALUATED` field is
expected: the mechanical gate deliberately does not own the semantic
classification; that judgment is supplied independently above.

## Stage 5 applicability and trust

`AUDIT_MODE` and `/audit-input.json` both select `CLASSIFICATION_ONLY`.
`stage5_result`, `lean_workspace`, and `lean_invocation` are null, `/candidate`
is absent, and there is no generated theorem to prove. Therefore a Stage 5
clean build, `Proof.final`, `#print axioms`, theorem-identity audit, and
operational-bridge parameter audit are not applicable. Attempting to introduce
a Stage 5 candidate in this mode would itself violate the contract.

The 48 allowlisted declarations in the generic generated Klean project are
executable-data boundary declarations checked by preflight, not propositions
used by a Stage 5 proof. With no target and no proof, no axiom supports an audit
theorem.

## Evidence

Exact commands are indexed in `evidence/COMMANDS.md`. Principal raw evidence:

- `evidence/01_generator_provenance.txt`
- `evidence/04_reconstructed_inventory.txt`
- `evidence/05_frozen_program_spec_verification.txt`
- `evidence/07_operational_semantics_snippets.txt`
- `evidence/08_generation_artifacts.txt`
- `evidence/26_proc_exe_compat_build_and_test.txt`
- `evidence/27_preflight_rerun_success.txt`
- `evidence/28_independent_structural_hash_checks.txt`
- `evidence/29_final_mechanical_gate.txt`
- `evidence/30_semantic_recurrence_adversarial_checks.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
