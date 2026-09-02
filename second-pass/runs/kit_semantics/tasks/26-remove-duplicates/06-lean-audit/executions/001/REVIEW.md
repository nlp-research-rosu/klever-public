# Independent Stage 3–5 audit: 26-remove-duplicates

## Scope and result

This audit covers HumanEval `26-remove-duplicates`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`.

The signed launcher resolution and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY`. Stage 4 is recorded as `KLEAN_NO_OBLIGATIONS`;
the Stage 5 paths are null and `/candidate` is absent. Consequently no
candidate `Proof.final`, operational parameter definition, or Stage 5 axiom
accounting exists to audit.

I independently find that all four local verification rules are genuine
definitions and that the true `DOMAIN_LEMMA` set is empty. The deterministic
Stage 4 output therefore correctly contains zero obligations and no generated
target. The selected classification-only outcome is legitimate.

## Input and producer authentication

I verified the signed Stage 6 resolution envelope before using its paths or
hashes. Its signed resolution digest is
`3228524ce4663b43e9b9fca4b28e23cd509b64cacb89977782d57f44b4d25f02`.

The full independent hash ledger passed:

- Stage 1 complete tree:
  `4fde0cb30e3cf3a04c11d1de21f65306b4c6278929b1b8c3095eaf9d36e95cc8`.
- Stage 1 deterministic-export tree:
  `43e17dd455ddaa97c5a8e57e7c0f34364c0583f9649a9191df4b6da8c6802df3`.
- Every one of the 777 recorded Stage 1 regular-file paths and hashes matched.
- Stage 2 selected audit tree:
  `af258d689a468df3208350ed943987a71c068ca35c9de556402c1792f5de781e`.
- Stage 3 discovery file:
  `e6968140f6621cd53ff461b4697124372c375660619110992b9f8800483af358`.
- Stage 4 selected generation tree:
  `03120ee59221b4e8887ab7cbd6705f35808b9f2e5bbe86f29b088f1e50805d7f`.
- Generated project tree:
  `19e83d8a828745c726a36c7c5f711b13ca062113b0c4c5cee0c3d6ee46651f78`.
- Generation-time producer bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

Before judging Stage 4, I directly hashed the two mounted generation-time
producer sources:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

These values exactly match both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
files plus `source-manifest.json`. Both manifests record generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`,
and the immutable producer path in `/audit-input.json` ends in the same image
digest. The launcher-recorded bundle tree hash also matches. There is no
producer-source infrastructure error.

Evidence:
[`06_recorded_hashes_and_producer_provenance.txt`](evidence/06_recorded_hashes_and_producer_provenance.txt),
[`verify_recorded_hashes.py`](evidence/verify_recorded_hashes.py).

## Canonical inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py` with
`PYTHONPATH=/reference`, I reconstructed the local closure selected by
`prove.sh`:

- selected verification module: `VERIFICATION`;
- local module closure: exactly `VERIFICATION`;
- frozen `verification.k` SHA-256:
  `2ebd91be3260fa3cba17758d13378ea24b6a0ef9af9871d92cb84f352ffec089`;
- canonical whole-inventory SHA-256:
  `999a94a14a4ee59a8507f036df83415964d63647ddc55c2c8a288c2eb762ccd2`.

The reconstructed inventory is:

| Order | Source span | `source_rule_id` / normalized source SHA-256 | Attributes |
|---:|---:|---|---|
| 1 | 8–8 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | none |
| 2 | 9–9 | `rule-bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | none |
| 3 | 14–14 | `rule-6c55d502b263cd9488fb4d13c18990fa8865f154bf5db922ef461ae84c961308` | none |
| 4 | 15–19 | `rule-7614bf9bc54b61933d1cbd1d534bb404043cb2a80c42f36e07b6cf7486cf642d` | none |

For each entry, the suffix after `rule-` equals the independently recomputed
normalized rule SHA-256. The Stage 3 file has exactly four entries, four
unique IDs, the same order, the same inventory hash, and no missing, extra,
or duplicated identity. The trusted Stage 3 contract validator also passes.

Evidence:
[`03_inventory_reconstruction.json`](evidence/03_inventory_reconstruction.json),
[`04_inventory_bijection.txt`](evidence/04_inventory_bijection.txt).

## Independent classification judgment

I reclassified every rule from its text, the source solution, the Stage 1
claims, and the supplied operational semantics:

1. `allInts(.ValSeq) => true` is `DEFINITION`. It is the base equation of the
   named input-domain predicate used by both Stage 1 claims.
2. `allInts(vCons(V,R)) => isInt(V) andBool allInts(R)` is `DEFINITION`. It is
   the structurally recursive step of that predicate.
3. `rdAcc(ACC,.ValSeq,ALL) => ACC` is `DEFINITION`. It is the base equation of
   the named output summary.
4. The nonempty `rdAcc` rule is `DEFINITION`. It recursively consumes the
   remaining list, appends the head exactly when `cntOccVS(ALL,V) == 1`, and
   otherwise retains the accumulator.

The fourth rule is not a disguised domain theorem. It defines the value of a
fresh summary symbol by structural recursion on `REST`; it does not state a
uniqueness, ordering, membership, or postcondition property about an already
computed result. It also does not rewrite a `<k>` configuration or preempt
program execution.

This recurrence is operationally faithful:

- the supplied for-loop semantics consumes the list from head to tail;
- `list.count(V)` reduces to `cntOccVS`, whose equations count K-equal
  occurrences in the complete list;
- `result.append(V)` updates the result heap cell with
  `valSeqConcat(..., vCons(V,.ValSeq))`;
- the Stage 1 loop claim threads exactly `rdAcc(ACC,REST,ALL)`;
- the final claim uses `rdAcc(.ValSeq,INPUT,INPUT)`.

Thus `rdAcc` is directly relevant to the source program and exact
post-state. `allInts` is directly relevant to the `List[int]` input contract.
There are no `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`
entries. No rule has a `simplification` attribute, so the simplification
classification restriction is also satisfied.

As finite adversarial support, an independently implemented frequency oracle
matched the `rdAcc` recurrence on 1,097 lists, including empty, repeated,
negative, large, and mixed-order cases. On `(1,2,1,3)`, the recurrence and
oracle return `(2,3)`, while “keep all” and “keep repeated” counterfactuals
return different results. This finite check supports, but does not replace,
the source-level recurrence argument above.

Evidence:
[`15_operational_semantics_bridge.txt`](evidence/15_operational_semantics_bridge.txt),
[`17_semantic_recurrence_check.txt`](evidence/17_semantic_recurrence_check.txt).

## Deterministic Stage 4 audit

I reran the required trusted call:

```text
PYTHONPATH=/reference python3 -c '... tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json) ...'
```

The audit sandbox virtualizes `getpid()` without exposing the corresponding
`/proc/<pid>/exe`; Lean 4.22 uses that path to locate its installation. The
first preflight attempt consequently failed at `lake clean` before a build or
verdict. I diagnosed this and used a local preload shim that changes only
absolute `/proc/<decimal-pid>/exe` `readlink` calls to `/proc/self/exe`. The
shim neither reads nor changes the generated project. Its probe reported the
pinned Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and matching Lake.

With that environment compatibility fix, the unchanged trusted checker
returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- trust declaration count `42`;
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output SHA-256
  `e6d8a13d3c93f12dae63c4f1c7566e53c519534399457dde82fb44f487a2e272`.

The complete returned object is byte-for-byte equivalent as parsed JSON to
the selected Stage 4 `preflight.json`, including both diagnostics. The
checker also re-snapshotted the frozen inputs, generated tree, and sidecars
after the clean build.

I separately verified the mathematical and manifest mapping:

- independent true domain IDs: `[]`;
- `input-manifest.json.source_rules`: `[]`;
- `obligation-map.json.source_rules`: `[]`;
- `obligation-map.json.obligations`: `[]`;
- `obligation-map.json.trust_parameters`: `[]`;
- obligation-map SHA-256 matches the generator manifest;
- no duplicated obligations and no vacuous conjuncts exist;
- generator obligation count is exactly zero;
- `generator-manifest.json`, both preflight results, and the signed audit
  input all record target `null`;
- no Lean source contains a `def targetStatement` declaration;
- `export-result.json`, both preflights, and the selected Stage 4 status all
  agree on `KLEAN_NO_OBLIGATIONS`;
- the toolchain object exactly matches
  `/reference/klean-toolchain.lock.json`;
- the trust-inventory file hash matches `export-result.json`.

The generated project contains Klean translation scaffolding and 42
allowlisted executable-symbol trust declarations, but it contains no target
proposition. They therefore cannot serve as a proof of a weakened or vacuous
target in this classification-only outcome.

Evidence:
[`07_preflight_command.txt`](evidence/07_preflight_command.txt),
[`13_proc_exe_compat_successful_probe.txt`](evidence/13_proc_exe_compat_successful_probe.txt),
[`14_preflight_returned_evidence.json`](evidence/14_preflight_returned_evidence.json),
[`16_independent_stage4_audit.txt`](evidence/16_independent_stage4_audit.txt).

## Stage 5 disposition

Stage 5 is correctly absent. Because the independently classified domain set
is genuinely empty, the required state is classification-only: no generated
target, null Stage 5 paths, and no `/candidate`. Running a candidate clean
build, `#print axioms Proof.final`, target-identity check, or operational
parameter bridge audit would invent a proof stage that the signed resolution
does not contain.

## Conclusion

The protected Stage 3 classification is complete, ordered, bijective, and
mathematically correct. The authenticated Stage 4 producer provenance and
all recorded content hashes match. The trusted preflight reproduces the
selected output, and the independent semantic audit confirms that zero
obligations is warranted rather than an omission. No target or Stage 5 proof
candidate exists.

The raw command ledger is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

VERDICT: PASS
LEGITIMACY: LEGIT
