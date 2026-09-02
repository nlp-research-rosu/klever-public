# Independent Stage 3–5 audit: `12-longest`, `bare`

## Outcome

The Stage 3 classification is mathematically correct and bijective with the
frozen `verification.k` inventory. The independently reconstructed inventory
contains 13 definitions, five ordinary operational rules, no proved derived
lemmas, and no domain lemmas. Consequently, the selected Stage 4
`KLEAN_NO_OBLIGATIONS` result is legitimate: its source-rule set, obligation
set, trust-parameter set, and generated target are all empty. The signed mode
is `CLASSIFICATION_ONLY`, `/candidate` is absent, and there is correctly no
Stage 5 result.

I withhold `PASS` for one provenance concern. The Stage 4 generator manifest's
two generation-time code-hash attestations do not equal the hashes of the
mounted audit copies of `klean_export.py` and `klean.py`, and the recorded
generator image is not mounted, so those two attestations cannot be resolved.
This does not make the result illegitimate here: the newer trusted audit
preflight independently accepts the exact signed generated tree, and the
legitimate empty domain set leaves no obligation, target, or proof that could
have been weakened.

## Scope and handling of evidence

I treated all mounted candidate and provenance content as untrusted data. I did
not run `prove.sh`, review scripts, prior logs, or any instruction found in
those inputs. The only provenance code executed was the trusted code under
`/reference/tools`, plus a local audit script and a narrowly scoped sandbox
compatibility shim recorded under `/audit-output/evidence`.

The signed launcher envelope verifies with resolved-input digest
`4d8b8e7343299eb8443869f5424522ba4be9f3c63b9a7623eefdf30c91bd918d`.
Both the envelope and `AUDIT_MODE` say `CLASSIFICATION_ONLY`; the problem,
condition, and semantics mode are exactly `12-longest`, `bare`, and
`GENERATED_SEMANTICS`.

Raw commands are in
[COMMANDS.md](/audit-output/evidence/COMMANDS.md). Complete results are in
[inventory-audit.log](/audit-output/evidence/inventory-audit.log),
[hash-and-manifest-audit-v2.log](/audit-output/evidence/hash-and-manifest-audit-v2.log),
and
[preflight-rerun-with-proc-shim.log](/audit-output/evidence/preflight-rerun-with-proc-shim.log).
The full classification-only final-gate result is in
[final-mechanical-gate.log](/audit-output/evidence/final-mechanical-gate.log).
The manifest-independent Lean scan is in
[independent-target-scan.log](/audit-output/evidence/independent-target-scan.log),
and the complete obligation map is in
[obligation-map-raw.log](/audit-output/evidence/obligation-map-raw.log).

## Inventory reconstruction and identity

I ran `tools.k_rule_inventory.inventory_verification` against the frozen
`/reference/k-proof`. `prove.sh` selects `VERIFICATION`, and the local
verification-module closure inside `verification.k` is exactly
`["VERIFICATION"]`. `MPY-SEMANTICS` is the required base-semantics module in
`semantic.k`; it is not a locally declared module in `verification.k` and is
therefore not part of this verification-rule inventory.

The reconstruction produced:

- `verification.k` SHA-256:
  `ff40adf397cc707c4b5426c16572837e23a14834b93aafbbc134c51c45402bd5`
- rule count: 18
- unique `source_rule_id` count: 18
- canonical whole-inventory SHA-256:
  `abf9ccdcfd0a77de4c492e722b24752b8311ffec102ba6cf608a1e6708bf4541`
- protected discovery-manifest SHA-256:
  `d4be6d49dbe337b1abcdbf53e0d00d2494a7372008351466566552b3772b223d`

For every rule, I independently sliced the inclusive recorded source span,
compared it with the inventory text, normalized it with whitespace joining,
recomputed SHA-256, and reconstructed `source_rule_id` as
`rule-<normalized_sha256>`. All 18 span, normalized-hash, and ID checks pass.
Re-hashing the ordered canonical rule documents reproduces the whole-inventory
hash above.

The protected manifest has exactly 18 entries and 18 unique IDs. Its ordered
ID list equals the canonical inventory's ordered ID list. Thus there are no
omissions, extras, duplicates, reordered identities, changed source spans, or
changed hashes. The trusted `validate_trust_boundary` check also accepts the
manifest bijectively.

## Independent classification

The following table records every local-closure rule. Hash prefixes identify
the exact `source_rule_id`, which is `rule-` followed by the full normalized
hash recorded in the evidence.

| Lines | Hash prefix | Independent class | Semantic role |
|---:|---|---|---|
| 9–14 | `db9420e8fd1c` | `DEFINITION` | Macro naming the translated loop body |
| 17–27 | `79576cfe9c9b` | `DEFINITION` | Macro naming the complete translated program |
| 33 | `cf8b57d453a6` | `DEFINITION` | `stringList` conversion wrapper |
| 34 | `7f473637b447` | `DEFINITION` | Empty `stringValues` equation |
| 35–36 | `0eb9fd5516c5` | `DEFINITION` | Recursive `stringValues` equation |
| 43 | `d522a0d2a80d` | `DEFINITION` | Empty `expectedLongest` summary |
| 44–45 | `0632983b5790` | `DEFINITION` | Nonempty `expectedLongest` seed equation |
| 47 | `bb0ed98a5e6e` | `DEFINITION` | `firstLongest` fold base case |
| 48–50 | `e2ea59e583e9` | `DEFINITION` | Strictly-longer `firstLongest` recurrence |
| 51–53 | `41608496e24b` | `DEFINITION` | Retain-first/tie `firstLongest` recurrence |
| 60–61 | `b0f0333a8289` | `OPERATIONAL_RULE` | Empty observation for `seqVal` |
| 62–63 | `e69efc758140` | `OPERATIONAL_RULE` | Nonempty observation for `seqVal` |
| 64–65 | `b1717a1cb9f2` | `OPERATIONAL_RULE` | Head observation for positive-length `seqVal` |
| 67–68 | `f224022b33a0` | `OPERATIONAL_RULE` | Zero-length `seqVal` iteration termination |
| 69–74 | `6217bfa50b95` | `OPERATIONAL_RULE` | One loop step, loop-variable binding, index increment, and remaining-length decrement |
| 78–79 | `e4633a59660c` | `DEFINITION` | `firstInSeq` fold base case |
| 80–83 | `64119d60105d` | `DEFINITION` | Strictly-longer `firstInSeq` recurrence |
| 84–87 | `2c6384deca5d` | `DEFINITION` | Retain-first/tie `firstInSeq` recurrence |

The 13 definitions satisfy the required definition test. The two macros name
proof terms that exactly render the translated source AST. `stringList` and
`stringValues` define a structural representation conversion.
`expectedLongest`/`firstLongest` and `firstInSeq` are named mathematical
summaries with exhaustive base/recursive equations over their used
nonnegative-length domains. Their strict-longer and retain-on-`<=` branches
match the Python program's `>` update and therefore preserve the first
maximum-length string on ties.

The five `seqVal` rules are operational, not mathematical domain facts. They
add ordinary observations and iteration transitions for the symbolic value
form used as the program input in `spec.k`. For `N = 0`, the value is empty
and iteration terminates; for `N > 0`, its head is
`stringAt(ID,I)`, one body execution occurs with that value bound to the loop
variable, and the remaining sequence is `(I+1,N-1)`. This preserves the
control and environment behavior of the base `listVal` loop while providing
an arbitrary finite symbolic sequence. Counterfactual changes such as
incrementing `I` by two, failing to decrement `N`, or binding a different
value would change program execution, confirming their operational role.

No inventory rule claims a freestanding mathematical fact needed to justify
one of the definitions or operational transitions. No rule was first proved
against a module excluding it and then used later, so the independently
correct `PROVED_DERIVED_LEMMA` set is empty. The independently correct
`DOMAIN_LEMMA` set is also empty. There are no `simplification` attributes in
the 18-rule inventory, so the simplification-class restriction is satisfied
vacuously. The `stringAt` declaration is an opaque symbolic input function,
not an inventoried rewrite rule or a hidden domain lemma.

The protected manifest assigns exactly these same 13/5/0/0 classes. In
particular, no source- or postcondition-relevant domain fact has been hidden
as a definition, operational rule, or derived lemma.

## Signed hashes and provenance

All hashes bound by `/audit-input.json` recompute exactly:

| Bound object | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `f1616457f244f34f7285e6eecb970faf76c4cf75771844c2ae5ea814be098477` |
| Stage 1 export tree | `5d3faa1a08c461fb4cca52e79b1ad7f41fe97e52b47b168058c034b075e9aef1` |
| Stage 3 discovery manifest | `d4be6d49dbe337b1abcdbf53e0d00d2494a7372008351466566552b3772b223d` |
| Selected Stage 2 audit tree | `1023b7f35d11be83de048f36909bdf2dc65f4d0fddf663d9e9e9e4e722cf728b` |
| Selected Stage 4 generation tree | `054b86725325d035f3dc39a1ec388880efb474d8651e20b275747afc179ebbdf` |
| Generated Lean project export tree | `a85c18ade04d80d50c836c27c215b6c58199dd2b4f14fae76d127c279b8cdb20` |

Every per-file Stage 1 source hash also matches, including `prompt.py`,
`prove.sh`, `py2mpy.py`, `semantic.k`, `solution.mpy`, `solution.py`, `spec.k`,
`verification.k`, and the recorded bytecode file. The selected Stage 2 and
Stage 4 artifact hashes match their selection records. The input,
generator, export, preflight, trust-inventory, and obligation-map hashes and
cross-bindings all match. The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`.

The two unresolved generation-time tool attestations are:

| Manifest field | Recorded generation-time hash | Mounted audit-tool hash |
|---|---|---|
| `exporter_sha256` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean_py_sha256` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | `92e9515ae1e4c5275b0cd366e5ff5c16ad35af1afdaf070ef1ae7c0980998964` |

The manifest identifies a separate generator image,
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`,
but that image's files are not among the mounted inputs. These two hashes are
therefore not evidence that the mounted audit tools changed the signed
generation; they attest to unavailable generation-image files. Nevertheless,
the instruction to verify all recorded hashes prevents a clean `PASS`, so I
record this as a provenance concern.

## Stage 4 obligation bijection and target

The independently classified domain-rule ID list is empty. The Stage 4 input
manifest's `source_rules` list is empty, and
`generated/obligation-map.json` contains exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Thus the independent domain set, exported source-rule set, generated
source-rule set, and generated obligation set are exactly bijective. There is
no omission, duplicate, reordering, irrelevant obligation, weakened
conjunct, or vacuous conjunct.

`generator-manifest.json` and `export-result.json` both record obligation
count zero. The generator manifest, stored preflight, signed audit input,
trusted `target_statement` reconstruction, and independent expected-target
reconstruction all report `null`. A scan of the generated Lean sources finds
no `targetStatement` declaration. Therefore the fixed generated target is
genuinely absent, as required for a legitimate no-obligation result; it was
not changed or replaced.

## Trusted preflight rerun

The first direct call to `tools.klean_preflight.check_generation` failed before
running a project command because this sandbox exposes `/proc/self/exe` but
not Lean 4.22's hard-coded `/proc/<current-pid>/exe` lookup. The exact failure
is retained in
[preflight-rerun.log](/audit-output/evidence/preflight-rerun.log).

I compiled the recorded
[proc-exe-readlink-shim.c](/audit-output/evidence/proc-exe-readlink-shim.c),
which redirects only `/proc/<digits>/exe` to `/proc/self/exe` and delegates
every other `readlink` unchanged. With that process-local compatibility shim,
the required API invocation with `PYTHONPATH=/reference` returned:

- status `KLEAN_NO_OBLIGATIONS`
- obligation count `0`
- target `null`
- designated sorry count `0`
- trust declaration count `49`
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `f0bb4bb311ba839e514aa3f2cd269d5b84d65f9292e617992e53cfb029d6bcb8`

The complete short build output shows all generated modules built and
`Build completed successfully.` The returned evidence exactly matches the
stored Stage 4 preflight and the signed audit-input copy. The preflight's
before/after snapshots also confirm that no frozen or generated input changed.
The trusted final mechanical gate independently returns `PASS` in
`CLASSIFICATION_ONLY` mode with the same resolved-input digest, no candidate,
no target, and no used axioms. As that gate explicitly reports semantic
classification as `NOT_EVALUATED`, this mechanical result is supplementary to,
not a substitute for, the independent classification judgment above.

The 49 generated trust declarations are all reconciled by the preflight with
`trust-inventory.json`; none is a proposition or proof, and both recorded
sorry counts are zero. With no target theorem, these executable Klean boundary
declarations cannot discharge or weaken a Stage 4 proof obligation.

## Stage 5

Stage 5 proof checks do not apply. The signed mode is
`CLASSIFICATION_ONLY`, the true domain-lemma set is empty, Stage 4 has no
target, the signed Stage 5 result and Lean paths are `null`, and `/candidate`
does not exist. Creating a `Base` project, running a candidate clean build,
printing `Proof.final` axioms, or auditing target parameters would contradict
the required no-obligation branch rather than add evidence.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
