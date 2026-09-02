# Independent Stage 3/4/5 audit: HumanEval `84-solve`, `bare`

## Result

The protected Stage 3 classification is correct, the selected Stage 4
`KLEAN_NO_OBLIGATIONS` generation is structurally intact and mathematically
appropriate, and Stage 5 is correctly absent because the launcher-selected
mode is `CLASSIFICATION_ONLY`.

I treated the mounted workspaces, manifests, logs, and prior review as
untrusted evidence. The conclusions below come from a new canonical inventory,
direct inspection and fresh execution of the frozen K sources, fresh hash
reconstruction, and a new call to the trusted preflight.

## Audit mode and immutable producer provenance

Both `AUDIT_MODE` and `/audit-input.json` say `CLASSIFICATION_ONLY`.
`/candidate` does not exist. The Stage 5 workspace/invocation hashes, Stage 5
result, target, and Lean paths in the audit input are all null, as required.

The generation-time producer check passed before any Stage 4 judgment:

| Item | Observed SHA-256 |
|---|---|
| `generation-tools/klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `generation-tools/klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` |
| producer bundle tree | `7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a` |

The two file hashes exactly match both `source-manifest.json` and
`generator-manifest.json`. The source manifest and generator manifest also
agree on immutable generator image
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`;
the same image digest is the basename of the producer-source path recorded in
the audit input. The bundle tree hash matches the audit input. There are no
unexpected files in the producer bundle.

The signed resolution digest recomputes to
`4c2989d00cfdcf484cd876d0e3a62143ad40c596bdc559e0eb5067302f8327d7`,
exactly the recorded `resolved_input_sha256`. All 24 recorded Stage 1
per-file hashes match. The independently recomputed tree hashes also match:

| Tree/hash convention | Observed and recorded value |
|---|---|
| Stage 1 pipeline tree | `0fd0b2738f0c86928b937d37518429e0060c8192300a3b92b08c3b91c9c578a9` |
| Stage 1 Klean frozen-input tree | `ff78a98fa909e6600d3495fe29c020936e5484a2d060da69c15c66c837e49bcb` |
| selected Stage 2 audit tree | `8dcaff2c87dcbaf0a1181b6000500c32e95befe14013765da2af4517bb6a5088` |
| selected Stage 4 generation tree | `675b9bf3e8b2b6240787d2f605d38d1056fd1ee868c905ee0a2a11fcd6e0a5c7` |
| generated Lean project tree | `fa75730ca4358bca90dcd37aebd2ac44e62883c55672a7c5bb75c25261fc183c` |

The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`.

## Canonical inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace produced:

- verification file SHA-256
  `e216d7d709f2101492f0dcf051c4228248e9619b38719e62d24d514fa5655cd7`;
- selected verification module `VERIFICATION`;
- local verification-file module closure `["VERIFICATION"]`;
- 13 rules; and
- whole inventory SHA-256
  `64981393230dd7f9e3ca36660db17e1ce1dc367753e244d73a67ec75c7bf2714`.

For every rule I independently sliced the recorded physical source span,
normalized its exact text with whitespace joining, recomputed the normalized
SHA-256, and reconstructed `source_rule_id` as `rule-<normalized SHA-256>`.
Every source slice, line endpoint, normalized hash, and identity matched the
trusted inventory. The 13 identities are unique.

The protected manifest also contains exactly 13 unique identities. Its
identity sequence is exactly the canonical source order; there are no missing,
extra, duplicated, or reordered entries. Its whole inventory hash is the same
canonical value above. The trusted Stage 3 boundary validator independently
accepts the same 13-rule bijection.

## Independent rule classification

All 13 rules are `DEFINITION`. This is not based on their prior rationales:
the frozen declarations mark the relevant symbols as functions or the
`solutionProgram` macro, and each rule supplies a macro expansion, defining
equation, descending recurrence, structural helper, or named proof term.

| Source span | Rule head | Independent classification and reason |
|---:|---|---|
| 18-67 | `solutionProgram` | `DEFINITION`: exact macro expansion naming the translated source-program AST. |
| 69-70 | `oracleDigitSum(N)` | `DEFINITION`: guarded base equation for the decimal digit-sum summary. |
| 71-72 | `oracleDigitSum(N)` | `DEFINITION`: quotient-by-ten recurrence, descending on its `N >= 10` guard. |
| 74 | `oracleBinary(0)` | `DEFINITION`: zero base equation for the binary-string summary. |
| 75-76 | `oracleBinary(N)` | `DEFINITION`: positive-case dispatch to the positive recurrence. |
| 77 | `oracleBinaryPositive(1)` | `DEFINITION`: base equation for positive binary conversion. |
| 78-80 | `oracleBinaryPositive(N)` | `DEFINITION`: quotient-by-two recurrence, descending on `N > 1`. |
| 81 | `appendOracleBit(VStr(S), 0)` | `DEFINITION`: structural helper equation appending bit zero. |
| 82 | `appendOracleBit(VStr(S), 1)` | `DEFINITION`: structural helper equation appending bit one. |
| 84 | `sameValue(VStr(S1), VStr(S2))` | `DEFINITION`: equation for a named Boolean proof helper, not a source-language execution rule. |
| 85-86 | `checkInput(N)` | `DEFINITION`: named per-input proof term; it invokes rather than replaces `runProgram`. |
| 87 | `checkRange(LIMIT, LIMIT)` | `DEFINITION`: empty half-open-range base equation. |
| 88-89 | `checkRange(N, LIMIT)` | `DEFINITION`: recurrence naming the range-wide conjunction. |

Thus the independent totals are:

- `DEFINITION`: 13;
- `OPERATIONAL_RULE`: 0;
- `PROVED_DERIVED_LEMMA`: 0; and
- `DOMAIN_LEMMA`: 0.

None of these rules has an execution-configuration LHS or defines/preempts the
source-language `evalExpr` or `runProgram` relation. Conversely, none states a
fact about a separately defined arithmetic or string symbol: every one defines
its own LHS head. No rule was first proved against a module omitting it and
then used later, so none qualifies as `PROVED_DERIVED_LEMMA`. The Stage 1
reachability claims in `spec.k` are goals, not inventory rules.

The reconstructed textual attribute list is empty for every rule, so there
are no `simplification`-attributed rules to classify. In particular, no
domain lemma is hidden under another label. The true domain-lemma set is
genuinely empty.

### Operational and source-program checks

I compiled `semantic.k` and `verification.k` afresh in `/tmp/audit-work`,
without using the mounted compiled backend. Independently parsing
`solution.mpy` and expanding `solutionProgram` produced byte-identical KAST
JSON files, both with SHA-256
`3309d2a7ad317251d807b41f215e09229e5751334e453412aceba72d2e1301ca`.
This confirms that the macro classified as a definition binds the exact
translated source program.

Fresh operational witnesses returned:

| `N` | K result string |
|---:|---|
| 0 | `"0"` |
| 9 | `"1001"` |
| 10 | `"1"` |
| 36 | `"1001"` |
| 99 | `"10010"` |
| 147 | `"1100"` |
| 9999 | `"100100"` |
| 10000 | `"1"` |

These cover zero, recurrence boundaries, a prompt example, the maximum
four-digit sum, and the upper input boundary. They are finite operational
evidence, not the basis for relabeling a rule as a lemma.

## Stage 4 manifest, obligation, and target identity

The Stage 3 discovery file SHA-256 recomputes to
`5eaf24c1e68b57ce146993c4105db0b7d9658741bb45c73ef6cd3768dcd8349c`
and matches the audit input, input manifest, generator provenance, and export
result.

The Stage 4 input manifest reproduces the independently validated categories
exactly: all 13 definition records, no operational rules, no proved-derived
lemmas, and no domain source rules. The category partition covers every
canonical rule once.

The generated `obligation-map.json` has SHA-256
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest, and contains exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

This is the exact source-rule/obligation bijection for the independently empty
domain set. There are no omissions, duplicates, weakened obligations, or
vacuous `True` conjuncts; there are no conjuncts at all.

The generator's expected-target function returns null. Independent target
detection returns null. `generator-manifest.json`, the recorded and rerun
preflights, and `/audit-input.json` all record a null target.
`Klean84Solve/Lemmas.lean` contains no `def`, `theorem`, `lemma`, `axiom`, or
`opaque` declaration. Therefore no generated theorem was changed, shadowed,
weakened, duplicated, or replaced by a vacuous variant: no generated theorem
exists in this legitimate zero-obligation case.

The trust-inventory file hash is
`2287f1a043dfe2f8b672e76f013f4361fd8034338931ebfb8d068fd79d3670a1`,
matching the export result. The generated semantics project contains 50
allowlisted executable trust declarations, which the preflight accounts for,
but there is no target proposition or proof that could consume them.

## Fresh Stage 4 preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the exact three requested inputs plus the pinned
toolchain lock.

The first call exposed a container-only PID namespace issue: Lean 4.22 looked
for `/proc/<getpid()>/exe`, while this container exposes only
`/proc/self/exe`. The failure is preserved in
`evidence/stage4-preflight-rerun.log`. I used a narrow `LD_PRELOAD` shim that
redirects only `/proc/<digits>/exe` reads to `/proc/self/exe`; its source and
validation are preserved. This changes installation-path discovery only, not
the generated files or Lean elaboration.

The rerun returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- designated sorry count 0;
- trust declaration count 50;
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
  and
- `lake build`: exit 0, output SHA-256
  `fbe18cce2bdbdd9bd0127f49f01ca6e95331b4aed97b6d4a6cea83eb0edf10ed`.

The two command output hashes and all returned fields exactly match the
generation-time preflight recorded in both the generation and audit input.
The preflight also rechecked that its read-only inputs did not change.

The trusted model-free `tools.klean_final_gate` also returned `PASS` in
`CLASSIFICATION_ONLY` mode, with candidate null, target null, zero obligations,
the same bound input hashes, the same clean-build diagnostics, and no used
axioms. As the gate itself reports, semantic classification is
`NOT_EVALUATED`; the independent rule analysis above supplies that required
mathematical judgment.

## Stage 5

Stage 5 proof auditing is inapplicable. The launcher did not select
`CLASSIFICATION_AND_PROOF`, there is no fixed generated theorem to prove, and
there is no `/candidate`. Creating a `Base` copy, inspecting `Proof.final`,
running `#print axioms Proof.final`, or checking candidate parameter bridges
would invent a proof-stage input that the signed resolution explicitly says
does not exist.

## Evidence index

- `evidence/COMMANDS.md`: exact commands and corresponding result logs.
- `evidence/producer-provenance.log`: producer hashes, manifests, and image ID.
- `evidence/tree-hashes.log`: recomputed mounted tree hashes.
- `evidence/reconstruct_inventory.py` and
  `evidence/inventory-reconstruction.log`: strict source-span, per-rule hash,
  identity-order, and inventory reconstruction.
- `evidence/classification-judgment.md`: full rule IDs and rule-by-rule
  independent classification.
- `evidence/frozen-source-and-manifests.log`: line-numbered frozen sources and
  relevant manifests.
- `evidence/fresh-k-operational-witnesses.log`: fresh K compilation, exact
  macro/program KAST comparison, and boundary witnesses.
- `evidence/independent_stage4_checks.py` and
  `evidence/independent-stage4-checks.log`: all recorded hash, category,
  obligation, status, and target cross-checks.
- `evidence/stage4-preflight-rerun.log`: initial environment failure.
- `evidence/lean-pid-namespace-workaround.log`: diagnosed PID namespace
  condition and narrow Lean path-discovery workaround.
- `evidence/stage4-preflight-rerun-with-pid-shim.log`: successful trusted
  preflight return, including clean-build diagnostics.
- `evidence/mechanical-final-gate.log` and
  `evidence/mechanical-final-gate.json`: trusted model-free signed-input gate,
  status `PASS`.

VERDICT: PASS
LEGITIMACY: LEGIT
