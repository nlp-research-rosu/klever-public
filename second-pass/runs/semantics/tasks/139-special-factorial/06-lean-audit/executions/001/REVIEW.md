# Independent Stage 3–5 Audit: `139-special-factorial`

## Result

The selected Stage 3 classification is complete and mathematically correct. The
true `DOMAIN_LEMMA` set is empty. The selected deterministic Stage 4 result is
therefore correctly `KLEAN_NO_OBLIGATIONS`: its source-rule map and obligation
map are both empty, it generated no target, and no Stage 5 candidate exists.

The launcher-recorded mode is `CLASSIFICATION_ONLY`, condition `semantics`, with
semantics mode `SUPPLIED_SEMANTICS`. Stage 5 proof checks are consequently not
applicable.

## Immutable-input and producer authentication

I verified the signed `/audit-input.json` envelope with the trusted
`stage6_resolution_contract` code. Its canonical resolved-input digest is
`3799c1bc9816fa191349f4c7f11bcf56c6ad62e69c6e11c8a688d0fecd008498`.
`AUDIT_MODE` exactly matches the signed mode.

Before judging Stage 4, I hashed the mounted generation-time producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Those values exactly match both `generator-manifest.json` and
`source-manifest.json`. The producer bundle contains exactly those two source
files plus `source-manifest.json`. Its pipeline tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`.

The immutable generator image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
It agrees among the generator manifest, source manifest, and the terminal
component of the producer-source path signed in `/audit-input.json`. The
generator toolchain object also exactly matches
`/reference/klean-toolchain.lock.json`.

All other recorded hashes were independently recomputed:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `731d79e06972ff8deb641b049287af52ba1182b00b956306ede2638ad3b9deaa` |
| Stage 1 export tree | `99391a80a8cb8964dbd32cc716431224ebaafda1958a4d62a29e359cf9e37eed` |
| Selected Stage 2 tree | `b1383e873b1f80c83f22585d550d75d1ff47c076f7d4c65cae80125927868ef7` |
| Stage 3 manifest | `1ed7b378bc5ef79397d9813d064c5489f7d8c7e9fb21d9f07997949a2e03d695` |
| Selected Stage 4 tree | `d974a53fc3976f8dda4e410c71cf4f0446afa238f0bc7a77599e6ff1a0ff5af8` |
| Generated-project export tree | `c76e926be7fc095abdb4ab4e31d956c7deb4a2ba90b735434499ef8b66ce479e` |

The complete Stage 1 per-file hash map, including its exact file set, also
matches the signed map. Both Lean workspace/invocation hashes are correctly
null. The selected Stage 2 and Stage 4 artifact hashes match their mounted
trees. See
[`21-independent-integrity-checks.txt`](evidence/21-independent-integrity-checks.txt).

## Rule-inventory reconstruction and bijection

I reconstructed the inventory directly from the frozen
`/reference/k-proof/verification.k` using the trusted
`tools.k_rule_inventory.inventory_verification` implementation.
`prove.sh` selects `VERIFICATION` as the main module. The local module closure
inside `verification.k` is exactly `[VERIFICATION]`; its import of `MPY` is
provided by the separate frozen supplied-semantics files.

The reconstructed `verification.k` hash is
`f01384534c27f04055c3b36580287a0a9db61c9236d5d08cfe676fbf3701cf52`.
The whole ordered rule-inventory hash is
`78ca969c32c7408012b3c0945044b8cdfba4503f693170d0585f82d2f07c9421`.

For every rule, I independently compared the reported span with the exact
physical source slice, normalized whitespace with `" ".join(text.split())`,
recomputed the normalized SHA-256, and rebuilt `source_rule_id` as
`rule-<normalized-sha256>`:

| Span | Head/role | Normalized SHA-256 and `source_rule_id` |
|---|---|---|
| 9–10 | `factorial(N) = 1` for `N <= 0`; `DEFINITION` | `061c723304f7123e51ae42344edc69b86c8037ca6606ef3145658939fb695c6b` |
| 11–12 | `factorial(N) = factorial(N-1) * N` for `N > 0`; `DEFINITION` | `458409c7bc07693a15b8bbc9bc5f73e395714f67d4b55f228b0496515b94136f` |
| 16–17 | `specialFactorial(N) = 1` for `N <= 0`; `DEFINITION` | `edc55d2e0a1a07541a0d8f6c1255456689844a9679ab6259bceb68f8c6465dbe` |
| 18–20 | `specialFactorial(N) = specialFactorial(N-1) * factorial(N)` for `N > 0`; `DEFINITION` | `0e4e7b60244adfbc0ed7ab152432bbfd95134e586f60ecb865844be14801286a` |

Each full rule ID is the corresponding hash in the last column prefixed with
`rule-`.

The protected Stage 3 manifest contains exactly those four IDs, exactly once,
in exactly the same order. Its inventory hash matches. There are no missing,
extra, duplicate, reordered, or unclassified identities. The trusted Stage 3
contract validation also succeeds. Raw reconstructions are in
[`12-reconstructed-rule-inventory.json`](evidence/12-reconstructed-rule-inventory.json)
and
[`13-stage3-trust-boundary-validation.json`](evidence/13-stage3-trust-boundary-validation.json).

## Independent classification judgment

All four entries are genuinely `DEFINITION`:

- `factorial` is a fresh named mathematical summary. Its two equations have
  disjoint and exhaustive integer guards. The positive branch decreases the
  argument by one; the non-positive branch supplies the total base value.
- `specialFactorial` is a second fresh named mathematical summary. Its two
  equations likewise have disjoint/exhaustive guards and positive-argument
  descent. They define the product `1! * ... * N!`.
- None of the four rules matches a `<k>` cell, source AST constructor, call,
  continuation, binding, store, stack, return, or other operational state.
  Thus none replaces or observes ordinary execution and none is an
  `OPERATIONAL_RULE`.
- Each rule has one of the newly declared summary symbols at its head and
  contributes a defining equation for that symbol. None states an independent
  fact over previously defined symbols, so none is a `DOMAIN_LEMMA`.
- There is no `PROVED_DERIVED_LEMMA` claim. Therefore no entry depends on the
  special two-phase “prove without the rule, then use later” exception.
- The inventory reports an empty attribute list for every rule. In particular,
  there are no `[simplification]` rules requiring further classification. The
  separate syntax declarations use `[function, total]`; those are not rule
  simplification attributes.

This judgment was made against the frozen source and supplied operational
semantics. The source function executes through ordinary module loading,
closure/call and parameter binding, assignments, `while` control, integer
comparison/multiplication/addition, lookup, return, and frame pop. The new
summary symbols appear in the proof claim’s invariant and postcondition, not
as execution interceptors. Relevant frozen semantics excerpts are preserved in
[`44-operational-semantics-excerpts.txt`](evidence/44-operational-semantics-excerpts.txt).

As an additional finite sensitivity check, I evaluated the source loop and the
two recurrences for integers `-3` through `10`; all results agree. For input
`4`, independently mutating each base or recursive defining case changes the
expected result `288`, showing that each equation materially contributes to
the summary rather than acting as an irrelevant fact. This finite check
supports, but is not substituted for, the structural and mathematical
classification above. See
[`47-semantic-recurrence-and-mutations.txt`](evidence/47-semantic-recurrence-and-mutations.txt).

The resulting independently classified sets are:

- `DEFINITION`: 4
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

Thus the true domain-lemma set is genuinely empty.

## Deterministic Stage 4 and target identity

I independently compared Stage 4’s input manifest with the reconstructed,
ordered Stage 3 inventory:

- `definitions` is exactly the four classified rules in canonical order.
- `operational_rules`, `proved_derived_lemmas`, and `source_rules` are all
  empty, as required by the independent classification.
- `obligation-map.json` has exactly empty `source_rules`, `obligations`, and
  `trust_parameters` arrays.
- The obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching the generator manifest.
- Generator, export-result, recorded preflight, and signed audit input all
  report obligation count zero.

There is consequently no source-rule/obligation omission, duplicate, reordering,
weakening, irrelevant obligation, or vacuous conjunct. There is no conjunction
at all.

Target identity is consistently null in the generator manifest, recorded
preflight, and `/audit-input.json`. The trusted
`klean_export.target_statement` detector also returns null. The generated
`Lemmas.lean` contains only imports, a namespace declaration, and its closing
`end`; it contains no target declaration. See
[`45-generated-target-files.txt`](evidence/45-generated-target-files.txt).

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the required frozen Stage 1 workspace, protected Stage 3 manifest, selected
Stage 4 generation, and trusted toolchain lock. Its fresh temporary copy passed
both `lake clean` and `lake build`. The returned result is:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: `0`
- target: null
- designated sorry count: `0`
- trust declaration count: `51`
- clean exit: `0`
- build exit: `0`
- build-output SHA-256:
  `d5eb4147211a1d23bc3d864380d1505e64d582f543d796d2a929297edce00c15`

The complete returned evidence is
[`43-fresh-check-generation-success.json`](evidence/43-fresh-check-generation-success.json).

The ambient Lean runtime initially failed because it attempted to resolve
`/proc/<namespace-pid>/exe`, which is absent under this audit container’s PID
namespace. The diagnosis captured `readlink("/proc/8/exe") = ENOENT`.
I used a narrow `LD_PRELOAD` shim that redirects only `/proc/*/exe` readlink
requests to `/proc/self/exe`; this restored the pinned Lean
`4.22.0`/commit `ba2cbbf...` without changing the trusted preflight or any
input. The shim source, binary hashes, failed attempts, diagnosis, and
successful rerun are all retained in evidence files 22–43.

## Stage 5 applicability

Stage 5 is correctly absent:

- signed audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`
- true domain-lemma set: empty
- generated target: absent
- `/candidate`: absent
- signed Lean workspace and invocation hashes: null
- signed Stage 5 result: null

Accordingly, a candidate clean build, `#print axioms Proof.final`, proof-target
identity audit, and `target.parameters` operational-bridge audit are not
applicable. Performing or inventing a Stage 5 proof in this mode would violate
the no-obligation contract.

## Evidence summary

Raw commands, stdout/stderr, and exit codes are under `evidence/`. The first
`jq` formatting attempts are intentionally retained as failed commands because
`jq` was unavailable; subsequent JSON formatting used Python’s passive
`json.tool`. The substantive integrity checker, trusted preflight, and semantic
sensitivity checks all exit zero.

VERDICT: PASS
LEGITIMACY: LEGIT
