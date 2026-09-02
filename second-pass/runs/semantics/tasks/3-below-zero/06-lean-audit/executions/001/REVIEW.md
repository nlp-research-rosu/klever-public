# Independent audit: HumanEval `3-below-zero`

## Scope and conclusion

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. I treated the
Stage 1 workspace, Stage 2 review, protected Stage 3 classification, Stage 4
generation, logs, comments, and manifests as untrusted evidence. I did not
adopt any prior verdict.

The independently reconstructed Stage 3 classification is correct. Its true
`DOMAIN_LEMMA` set is empty. Deterministic Stage 4 therefore correctly reports
`KLEAN_NO_OBLIGATIONS`, exports no obligations, fixes no Lean target, and has
no Stage 5 candidate. The classification and generation are legitimate.

## Producer and launcher provenance

The Stage 4 producer sources were hashed before judging generation:

| Producer | Recomputed SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | same in the source and generator manifests | match |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | same in the source and generator manifests | match |

The generator image identity is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the source manifest and generator manifest. The launcher-recorded producer
path ends in the identical digest. The complete producer-source tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`.

The trusted Stage 6 envelope verifier recomputed the canonical resolution hash
as
`6f67677c2841987aa1636d2c9a653d897b06aeba87a881b37a471a8920f01ebe`,
exactly the launcher-recorded `resolved_input_sha256`.

All 32 individually recorded Stage 1 source-file paths and hashes matched
bijectively. The principal tree and file bindings also matched:

| Binding | Recomputed value |
|---|---|
| Stage 1 pipeline tree | `ace8e1da81cad36f5d746a2704cf162744ea8ab760e0613bcb77fb772224c60a` |
| Stage 1 Klean-export tree | `21353f7e624f54e853bcb8df16c92569e4ece53f5b7920a8a3de8988a9da72a5` |
| selected Stage 2 tree | `b4de0fd83d771e205a9a0c58f9e6a25894bdb79903392ec66f45f662dc83866a` |
| Stage 3 manifest file | `572a94d033e4d6ef7c559a9000e6356ed8752149e46d581362a5f6aac37ca51e` |
| complete Stage 4 generation tree | `31a65a94b587d46a623bbb4a85c98b3528fdea9992364c36e8c342c78d76bb70` |
| generated Lean project tree | `76b950664ed6d87a5a4b4af9062a443a9e3f0bfda1512050a3eca6b9a46cdd4b` |

The final immutable-input snapshot still matched every launcher binding after
all checks.

## Canonical rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`, not against any earlier audit ledger.

The selected verification module is `MPY-VERIFICATION-LEMMA`. Its local
verification-file closure, in source order, is:

1. `BELOW-ZERO-COMMON`
2. `MPY-VERIFICATION-LEMMA`

The reconstructed `verification.k` hash is
`4da26ec06b74bc52e9dd464edc0e92b76104df16eda355a7d442c452f5e1f364`.
The canonical inventory has eight unique rules and whole-inventory hash
`995e881cff064ef9ab84cccbf1fdd83ccefea3f071f9508080fcb40a53cb605c`.
Every `source_rule_id` is exactly `rule-` followed by the normalized hash below.

| Source span | Normalized SHA-256 | Independent class |
|---|---|---|
| `BELOW-ZERO-COMMON:8-12` | `37490b390355d40b96a24fb6238d94c721dd106775648ef6adf702d0f018a945` | `DEFINITION` |
| `BELOW-ZERO-COMMON:15-19` | `7ad011f4ad8584143ada5134978d05f498d1696b3f046f0aafd22e1826e11e5d` | `DEFINITION` |
| `BELOW-ZERO-COMMON:22-25` | `f0df05e0e38700aa105eb11f7349ed86c708125ba2ed7016c90aeb1231ddfdc2` | `DEFINITION` |
| `BELOW-ZERO-COMMON:32` | `333fe6107e77ab191c2f76ba40e090e2476f94d001c790092147629f8518d311` | `OPERATIONAL_RULE` |
| `BELOW-ZERO-COMMON:33-34` | `8a249bc8e455d2bdc6fd578ff3452bd8220f754f9622c7679e0505ee4b9f4fd6` | `OPERATIONAL_RULE` |
| `BELOW-ZERO-COMMON:38` | `7ec387f9629680162121a42c4d6abab222bfc61592daa736e9caca2524fa4f39` | `DEFINITION` |
| `BELOW-ZERO-COMMON:39-43` | `2c07a06a5689cd1d706ba5a69e6209e1668dc73225ce9c4bbd9b06ff4f661a03` | `DEFINITION` |
| `MPY-VERIFICATION-LEMMA:55-80` | `f5db78ced6090ff9fb5c369808923c5e0a9d90c895bad6c69844f2b05f7c04e1` | `PROVED_DERIVED_LEMMA` |

The protected Stage 3 manifest contains these eight identities exactly once
and in the same order. There are no omitted, duplicated, extra, reordered, or
hash-changed rules. Its inventory hash is the independently reconstructed
hash. No inventory rule has a `simplification` attribute, so the additional
simplification-class restriction is satisfied vacuously.

## Independent classification judgment

The first three rules are macros naming exact constructor terms:
`belowZeroLoopBody`, `belowZeroFunctionBody`, and `solutionProgram`. They name
proof terms and do not assert domain facts, so they are `DEFINITION`s.
`solution.mpy` has the same translated function body: initialize balance and
operation to zero, iterate over operations, add each operation, return true on
a strict-negative balance, and otherwise return false.

The two iterator rules are ordinary operational observations for the
proof-local typed list carrier:

- the empty carrier produces `#iterDone`;
- a nonempty carrier produces `#iterYield(I, tail)`.

They mirror the supplied `MPY-LIST` rules for `.ValSeq` and `vCons`, while
retaining the head's `Int` sort for symbolic induction. They rewrite the
supplied iterator protocol in the `<k>` cell and are not mathematical domain
claims. `OPERATIONAL_RULE` is therefore the correct class.

The two `prefixBelow` rules form a complete structural recurrence:

- an empty suffix is false;
- a head is true exactly when the updated balance is below zero, otherwise the
  recurrence continues at that updated balance.

This is a named mathematical summary with a strictly smaller `IntVals`
argument, so both equations are `DEFINITION`s, not domain lemmas. Starting at
zero, it states exactly that some nonempty prefix sum is strictly negative,
which is the source postcondition. Independent witnesses covered empty,
zero-only, exact-zero, early-negative, later-negative, and large-integer
cases. Counterfactual `<= 0`, final-total-only, and skipped-head summaries were
distinguished by `[0]`, `[-1, 2]`, and `[-1]`, respectively.

The final rule is a valid `PROVED_DERIVED_LEMMA`:

- `AUX-SPEC` imports `MPY-VERIFICATION`, which imports only
  `BELOW-ZERO-COMMON` and does not contain the summary rule.
- The 25 semantic lines of the auxiliary claim and later rule are byte-for-byte
  identical after changing only the outer keyword `claim` to `rule`. The
  later `[priority(40)]` controls reuse and is not a changed premise,
  transition, guard, or state footprint.
- I independently compiled `MPY-VERIFICATION` and ran `AUX-SPEC`; both commands
  exited 0 and the prover returned `#Top`.
- Only afterward did I independently compile
  `MPY-VERIFICATION-LEMMA` and run `MAIN-SPEC`; both exited 0 and the prover
  returned `#Top`.

The derived rule matches the complete loop/call continuation and all relevant
configuration cells: environments, scopes, scope location, heap, heap
location, call stack, return state, exception state, and exit code. It
summarizes exactly the source loop and cleanup already established by the
auxiliary reachability proof.

Two sensitivity checks rejected convenient alternatives:

- Replacing the final result with `notBool prefixBelow(0, IS)` exited 1 with a
  stuck implication between the result and its negation.
- Mutating the source comparison from `< 0` to `<= 0` compiled but made the
  auxiliary proof exit 1 at the zero boundary.

Thus the summary is both result-sensitive and program-body-sensitive. The
independent classification counts are five `DEFINITION`s, two
`OPERATIONAL_RULE`s, one `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`s.
There is no relevant mathematical rule hidden under a non-domain label.

## Deterministic Stage 4 generation

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly these inputs:

```text
/reference/k-proof
/reference/lemma-discovery.json
/reference/klean-generation
/reference/klean-toolchain.lock.json
```

The first invocation exposed an audit-sandbox PID/proc incompatibility before
compilation: Lean 4.22 calls `readlink("/proc/<getpid()>/exe")`, while this
namespaced sandbox exposes the executable only through `/proc/self/exe`.
Evidence shows the numerical proc entry is absent and the Lean runtime's
corresponding call site. I used a narrow, audit-local preload shim that changes
only that exact self-executable readlink to `/proc/self/exe`. With the shim,
the compiler reported the pinned Lean version and commit:
`4.22.0`, `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.
No candidate, generated, manifest, or frozen source file was modified.

The rerun returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `obligation_count = 0`;
- `target = null`;
- `lake clean` exit 0 with empty output;
- `lake build` exit 0;
- build output SHA-256
  `882e1a85708a6f08f9f08dd7511cd843635b7a4db64989e72788d0226167b31a`,
  identical to the selected preflight record;
- zero designated sorries;
- 47 generated executable trust declarations.

I independently checked all Stage 4 bindings:

- The independent domain-rule set, input-manifest `source_rules`,
  obligation-map `source_rules`, obligation list, and trust-parameter list are
  all exactly `[]`.
- Counts and statuses agree across the generator manifest, export result,
  stored preflight, and launcher input.
- Stage 1, Stage 3, generated-tree, inventory, `verification.k`,
  obligation-map, and trust-inventory hashes all match their recorded bindings.
- `obligation-map.json` hashes to
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching the generator manifest.
- `trust-inventory.json` hashes to
  `cc916be76195f333a2e8b932e6b72b8e7ed47a9aa9aa18d23fc08bc7d2453e0c`,
  matching the export result.
- The 47 actual generated trust declarations match the allowlist bijectively.
  They are executable collection/K-symbol constants, not proposition or proof
  assumptions.

There are no conjuncts to weaken, duplicate, make vacuous, or detach from a
source rule. The empty export is mathematically justified because the
independent domain set is genuinely empty.

## Fixed target and Stage 5 applicability

The generator manifest, stored preflight, launcher preflight, and launcher
top-level target are all `null`. The obligation map has no obligations or
parameters. `Klean3BelowZero/Lemmas.lean` contains only imports and an empty
namespace; an independent scan found no generated theorem or lemma
declaration. Therefore there is no fixed generated target.

`AUDIT_MODE` is `CLASSIFICATION_ONLY`, and `/candidate` is absent. This is the
required state for a genuine `KLEAN_NO_OBLIGATIONS` result. Stage 5 clean
building, `Proof.final`, axiom printing, and operational-bridge parameter
checks are not applicable because no target or proof candidate exists.

## Evidence

Raw commands and complete outputs are under `/audit-output/evidence/`.
The principal records are:

- `00-mode-and-producer-provenance.log`
- `03-canonical-inventory-and-stage3.log`
- `04-recorded-hash-recomputation.log`
- `05-frozen-source-and-semantic-context.log`
- `07-operational-semantics-review.log`
- `09-independent-aux-proof.log`
- `10-independent-main-proof-and-lemma-identity.log`
- `11-check-generation-returned-evidence.log` (initial sandbox failure)
- `36-proc-pid-readlink-diagnostic.log`
- `38-lean-readlink-shim-build-and-test.log`
- `39-check-generation-returned-evidence-with-proc-shim.log`
- `40-stage4-sidecars-generated-source-and-candidate-absence.log`
- `41-independent-stage3-stage4-consistency-checks.log`
- `44-resolved-audit-input-verification.log`
- `45-mathematical-contract-witnesses.log`
- `46-false-postcondition-mutation.log`
- `47-loop-body-sensitivity-mutation.log`
- `48-final-immutable-snapshot-and-evidence-index.log`

VERDICT: PASS
LEGITIMACY: LEGIT
