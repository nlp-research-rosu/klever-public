# Independent Stage 3–5 audit: `14-all-prefixes`

## Scope and outcome

The launcher and signed audit input both select:

- problem: `14-all-prefixes`
- condition: `semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

`/candidate` is absent, the recorded Stage 5 result is null, and both recorded
Lean workspace hashes are null. Consequently, the Stage 5 proof, axiom,
operational-bridge, and `Proof.final` checks are not applicable. Their absence
is correct for this audit mode and for a genuine zero-domain-lemma result.

I treated the mounted Stage 1–4 artifacts and prior reviews as untrusted
evidence. The inventory, classifications, source hashes, producer provenance,
obligation mapping, and target status were reconstructed independently with the
trusted tools under `/reference/tools`.

## Launcher and hash reconciliation

The trusted audit-input verifier accepted the signed resolution. Its canonical
digest is
`ea769d2a6682357766ec6dc8756867c9c3ec0a65f6c9800f245493d4bc6fb7cc`.

Independent recomputation matched every relevant recorded hash:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 pipeline tree | `52c454781d34ae87a19ce4d39c210d317c2aa90cd6bb19432ca76f3f562e354c` |
| Stage 1 deterministic-export tree | `7a130c32545c74c27cb4e3b08b0c83e353d27cfbb4eea78e7062a601dde65c10` |
| Frozen `verification.k` | `700579025a7e4d307ef6f729d7344deb55d68e848ae1bf528a07ce2ee6be0147` |
| Selected Stage 2 audit tree | `4e51ca1c3ea1df119a68bdb72df0c18f140b2f4e065f18c382867810d0b1b3c6` |
| Protected Stage 3 manifest | `55a2e661d5c746338dc99d450fc92945b77106a8ccbfce556bfae808b2630683` |
| Selected Stage 4 generation tree | `341b7dd19f88f36b294570857513584a31a6e9785e4e943e2bebc9cd1f2f4121` |
| Generated Lean-project tree | `2319960ffacd5a97608490d5f560c47ba36834eae7abf0bb527cfe3b38744fe2` |
| Producer-source bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

The complete Stage 1 per-file hash map also matches `/audit-input.json`
bijectively. Hashes remained unchanged after the independent preflight.

The raw reconstruction and comparisons are in
[`03-reconstruction-and-hashes.log`](/audit-output/evidence/03-reconstruction-and-hashes.log)
and
[`13-post-preflight-hashes.log`](/audit-output/evidence/13-post-preflight-hashes.log).
Mode and candidate-absence evidence is in
[`14-mode-and-stage5-absence.log`](/audit-output/evidence/14-mode-and-stage5-absence.log).

## Stage 3 inventory reconstruction

Using `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference`, I reconstructed the local verification-module closure
of the frozen `verification.k`. `prove.sh` fixes `VERIFICATION` as the main
module; the local closure is exactly `["VERIFICATION"]`.

The canonical inventory contains exactly seven rules. Its whole-inventory hash
is
`40e9769bf470a35269735642ec44dc37c797d993482694c8a07eac9ce74bc559`.
For every rule, I independently re-extracted the physical source span,
normalized whitespace, recomputed SHA-256, and confirmed that
`source_rule_id = "rule-" + normalized_sha256`.

| Lines | Normalized SHA-256 / source-rule suffix | Independent class |
|---|---|---|
| 11–19 | `304d2987c766d8fd47b4acd75d897a4990ad3f33be34064740db13cb12cd7973` | `DEFINITION` |
| 20–21 | `a73447fc9c4a07cb4db21f913f63ec0a12d22016eaa29d60d69da2c2c09b3343` | `DEFINITION` |
| 24–25 | `b463ecc1fcafb4659695aa4718142d96b6f1fb9af4b47865ad8c2e1c23aa465d` | `DEFINITION` |
| 30–36 | `4b8d3d3d4f7336421c9303880f0fb545ba0266b6523b5a08d9004f09ac25eb6c` | `DEFINITION` |
| 39–50 | `7c22c576e8210ec39056f4e4da36810495c640312df98f28d9c8d2bbd7ce68a6` | `DEFINITION` |
| 53–54 | `8e477bcfeff61e45ce366cc0bc9c0d31da737fcc36a3d3245a97fe3999a4b623` | `DEFINITION` |
| 57–58 | `eca51dfe7c73830a4d8f1299f6714500181d4e7011cddec0c87182f65d948a14` | `DEFINITION` |

The protected Stage 3 manifest contains these same seven identities exactly
once and in this exact order. There are no omitted, duplicated, extra, or
reordered identities. The protected inventory hash matches the reconstructed
hash.

All seven rule-level attribute lists are empty. In particular, there is no
`simplification` rule. The `[function]` and `[function, total]` annotations are
syntax-symbol attributes, not hidden rule-level simplification attributes.

## Independent classification judgment

The first two rules are the two guarded equations defining
`prefixesAcc(S, END, STOP, ACC)`:

- when `END < STOP`, the recurrence increments `END` and appends the supplied
  semantics' slice `S[:END]` to `ACC`;
- when `END >= STOP`, it returns `ACC`.

The guards are disjoint and exhaustive over K integers. In the recursive case,
`STOP - END` decreases by one, so the recurrence reaches the base case. These
rules stipulate the meaning of a fresh summary symbol; they do not assert an
algebraic fact about an independently defined symbol and do not replace a
program step. They are definitions, not domain lemmas.

The third rule defines `allPrefixes(S)` as the recurrence starting at bound 1,
ending at `isLen(S) + 1`, with an empty accumulator. This is a named
mathematical summary. It is relevant to the source contract and is not itself a
claim that the program implements the summary.

The last four rules define named AST/proof terms:

- `allPrefixesLoopBody()` expands to the exact append-of-slice source loop body;
- `allPrefixesBody()` expands to the docstring, empty-list initialization,
  range loop, and return from the translated source;
- `allPrefixesDef()` expands to the translated function definition;
- `solutionModule()` expands to the translated import plus function.

These equations expose exact constructor syntax before ordinary supplied
semantics execute it. They do not skip lookup, slicing, mutation, looping,
return, heap, or control behavior, so they are definitions/macros rather than
operational bridges.

The supplied semantics confirms the operational alignment:

- `len(str(S))` reduces to `isLen(S)`;
- `range(1, len(S)+1)` creates `rangeObj(1, isLen(S)+1, 1)` and yields exactly
  those successive end indices;
- string `Subscript` with `Slice(NoBound, end, NoBound)` reduces through
  `doSlice(str(S), noB, someB(end), noB)`;
- `prefixes.append(v)` updates the referenced heap list with
  `valSeqConcat`;
- the fixed `For` rules drive `#loop` through iterator yield and completion.

Thus the summary yields `[]` for an empty string, `[S[:1]]` for a one-character
string, and one additional prefix per range step for longer strings. The loop
reachability claim in `spec.k` connects fixed execution to the recurrence; it is
not one of the inventoried `verification.k` rules and does not turn any
definition into a derived or domain lemma.

My independent classification counts are therefore:

- `DEFINITION`: 7
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The frozen source, claim, and solution are captured in
[`01-frozen-program-and-proof.log`](/audit-output/evidence/01-frozen-program-and-proof.log).
The relevant fixed operational rules are captured in
[`04b-operational-semantics-trace.log`](/audit-output/evidence/04b-operational-semantics-trace.log).

## Stage 4 producer authentication

Producer authentication was completed before judging the generated output:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The immutable generator image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
it matches the generator manifest, source manifest, and the image-key component
of the producer-source path recorded in `/audit-input.json`. The complete
producer bundle tree also matches the audit-input hash.

Raw producer and manifest evidence is in
[`02-producer-and-generation-records.log`](/audit-output/evidence/02-producer-and-generation-records.log).
The authenticated producer's obligation and target logic is recorded in
[`17-producer-obligation-logic.log`](/audit-output/evidence/17-producer-obligation-logic.log).

## Stage 4 preflight, bijection, and target identity

I invoked the required trusted function:

```text
PYTHONPATH=/reference python3 /audit-output/evidence/run_check_generation.py
```

The sandbox initially prevented Lean and Lake from finding their executables:
it remaps `getpid()` while exposing host PIDs in `/proc`. I diagnosed this
independently and used an audit-local `LD_PRELOAD` shim that redirects only
`/proc/*/exe` `readlink` calls to `/proc/self/exe`. With that environment-only
repair, Lean reports the pinned version and commit from the toolchain lock. The
trusted check was then rerun unchanged as:

```text
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
PYTHONPATH=/reference \
python3 /audit-output/evidence/run_check_generation.py
```

The returned evidence is:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: `0`
- target: null
- designated sorry count: `0`
- trust declaration count: `53`
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `07123ee4dd17259c5af19a5baba33b5de61399f850e49b6eca721321cbb34093`

Those diagnostics exactly match the generation-time preflight embedded in the
signed audit input. The shim changes neither source inputs nor Lean semantics;
post-check hashes confirm all mounted artifacts remained unchanged.

The initial infrastructure failure is preserved in
[`05-check-generation.log`](/audit-output/evidence/05-check-generation.log).
The diagnosis and narrow repair are in
[`06-lean-toolchain-diagnosis.log`](/audit-output/evidence/06-lean-toolchain-diagnosis.log),
[`11-lean-loader-shim.log`](/audit-output/evidence/11-lean-loader-shim.log), and
[`proc_exe_readlink_shim.c`](/audit-output/evidence/proc_exe_readlink_shim.c).
The successful trusted return is in
[`12-check-generation-rerun.log`](/audit-output/evidence/12-check-generation-rerun.log).

The exact Stage 4 mapping is:

| Set or declaration | Observed value |
|---|---|
| independently classified true domain-lemma set | `[]` |
| `input-manifest.source_rules` | `[]` |
| `obligation-map.source_rules` | `[]` |
| `obligation-map.obligations` | `[]` |
| `obligation-map.trust_parameters` | `[]` |
| generated `targetStatement` | absent |
| generator-manifest target | null |
| audit-input target | null |

This is an exact empty-set source-rule/obligation bijection. There are no
omissions, duplicates, irrelevant or weakened obligations, vacuous conjuncts,
or target changes. `Lemmas.lean` contains only imports and an empty namespace;
the authenticated producer and trusted checker both require a null target when
the obligation list is empty. Because the independently classified domain set
is genuinely empty, `KLEAN_NO_OBLIGATIONS` is mathematically appropriate rather
than merely self-consistent.

## Final judgment

Stage 3 is complete and correctly classified. Stage 4 is authenticated,
structurally bijective, deterministic with respect to the recorded inputs, and
mathematically faithful to the independently reconstructed empty domain-lemma
set. The required absence of a generated target and Stage 5 candidate is
confirmed.

VERDICT: PASS
LEGITIMACY: LEGIT
