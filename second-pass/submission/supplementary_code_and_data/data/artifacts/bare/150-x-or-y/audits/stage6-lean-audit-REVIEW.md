# Independent Stage 3–5 audit: `150-x-or-y`

## Scope and result

This audit covers condition `bare` in semantics mode
`GENERATED_SEMANTICS`. Both `/audit-input.json` and `AUDIT_MODE` record
`CLASSIFICATION_ONLY`. Stage 4 selected `KLEAN_NO_OBLIGATIONS`; `/candidate`
is absent, and the launcher records null Stage 5 workspace, invocation, result,
and target fields.

I treated the mounted candidate and provenance material as untrusted evidence.
I did not rely on the prior Stage 2 verdict or execute mounted Python source.
All executable semantic probes below use an independently written model of the
frozen program and K rules.

## Generation-producer authentication

The producer sources were authenticated before judging Stage 4:

| Producer | Observed SHA-256 | Generator/source manifests |
|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | exact match |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | exact match |

The source bundle contains exactly those two files plus
`source-manifest.json`. Its trusted tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`. The source manifest and generator manifest both
record immutable image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`;
the launcher-recorded producer-bundle path has the same image digest as its
final component. There is no producer-source infrastructure error.

The complete comparison is in
[17-complete-hash-ledger.txt](/audit-output/evidence/17-complete-hash-ledger.txt);
the raw manifest material is in
[04-producer-and-generator-manifests.txt](/audit-output/evidence/04-producer-and-generator-manifests.txt).

## Inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen `/reference/k-proof`. The selected local verification module is
`MPY-VERIFICATION`; its local import closure contains that module alone. The
reconstruction found seven rules in source order:

| Lines | `source_rule_id` / normalized SHA-256 | Independent class | Reason |
|---|---|---|---|
| 9–10 | `rule-3568314463b5f0cda0f318ebb08026d85632ffd161cd8c2d5ff1e4900f260969` | `DEFINITION` | Guarded base equation of the named `primeFrom` recurrence. |
| 11–12 | `rule-3cf9b4eaf0fc37f16b9c02bb86612432cff3badfb2761f79b078441bc26ec601` | `DEFINITION` | Divisible branch of that recurrence. |
| 13–14 | `rule-580860a84af419565613f03a6f4376674abe6fff2d2b519766ba75fb4f40e451` | `DEFINITION` | Recursive `D + 1` branch of that recurrence. |
| 17–18 | `rule-f8fc3c53a0505978f01db74728a727cd7869eda32ada9bd4865028c91fd75d91` | `DEFINITION` | Below-two branch of named summary `isPrime`. |
| 19–20 | `rule-9290ca5c6a6bfa55d5fce813d33d07aa7984f4656f33938a4e34fa11fa9d0655` | `DEFINITION` | Entry equation from `isPrime` to `primeFrom(N, 2)`. |
| 23 | `rule-430e599ca96d42aacd636f22618c18839f186b29b46581a108c51be2a8b03ef5` | `DEFINITION` | True branch of named result constructor `chooseVal`. |
| 24 | `rule-0cf2886c9720ca8500888e844b48dbcef4157496738d556f4340310b1c85ce00` | `DEFINITION` | False branch of named result constructor `chooseVal`. |

For every entry, the recomputed source span, normalized text hash, and
`source_rule_id` match. The ordered IDs are bijective with
`lemma-discovery.json`: seven observed, seven recorded, seven unique, with no
omission, extra rule, duplicate, or reordering. The reconstructed whole
inventory hash is
`bdc76b589c31174ad35d4f87c6970c4c9e6aa6b9be392e0dfd015630536ba6e2`,
exactly the protected value. The frozen `verification.k` hash is
`21e0be0014155fcc76212cc986fe183aa6bfbc12beea1583d8179789b54d689c`.

Raw reconstructed rule documents, normalized text, and comparisons are in
[03-reconstructed-inventory.txt](/audit-output/evidence/03-reconstructed-inventory.txt).

## Independent classification judgment

All seven entries are definitions, as Stage 3 records:

- `primeFrom` is explicitly declared as a function and its three rules are the
  base, divisible, and recursive equations of a named trial-division summary.
  Its guards split on `N < D*D` versus `D*D <= N`; the latter then splits on
  remainder zero versus nonzero. On the loop-invariant domain `D >= 2`, the
  recursive case advances exactly as the source loop and terminates by
  increasing `D`.
- `isPrime` is a named macro/summary. Its two guarded equations exhaust the
  integer domain at 2 and enter `primeFrom` at the source program's initial
  divisor.
- `chooseVal` is a named proof-result term. Its two Boolean equations select
  and wrap `X` or `Y`.

These terms occur in proof-result summaries; none matches or rewrites a source
execution construct such as `Module`, `eval`, `While`, `Return`, or a machine
cell. They therefore do not preempt operational K execution and are not
`OPERATIONAL_RULE`s. None asserts a standalone number-theory proposition, so
none is a `DOMAIN_LEMMA`. None is classified as `PROVED_DERIVED_LEMMA`; the
generalized loop invariant is a separate reachability claim in `spec.k`, not
one of these inventory rules.

No inventory rule has a `simplification` attribute, so the simplification
classification restriction is satisfied vacuously.

The definitions are relevant to both program and postcondition: the frozen
program performs trial division and returns `x` exactly when no divisor is
found; the universal postcondition selects between `x` and `y` with
`chooseVal(isPrime(N), X, Y)`. Independent probes included negative and
below-two inputs, the boundary primes 2 and 3, squares, composites, prompt
examples, a larger prime, and negative result values. All 14 operational and
summary results agreed. Counterfactual mutations to each kind of branch had
concrete distinguishing witnesses (`n=1`, `n=9`, and `n=7`).

The exact category-manifest reconstruction is in
[21-discovery-and-category-manifest-exactness-success.txt](/audit-output/evidence/21-discovery-and-category-manifest-exactness-success.txt);
the semantic probes and counterfactual witnesses are in
[19-independent-classification-bijection-target.txt](/audit-output/evidence/19-independent-classification-bijection-target.txt).

## Hash and manifest integrity

The trusted launcher-input verifier accepts `/audit-input.json`; its recomputed
resolved-input hash is
`d3a296689105c294563468c21b41cc02dc1ba6c522ed83475eabd69966a382e6`.
Every launcher-recorded artifact hash matches:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 workspace tree | `42d3b31838c3997c279f68ada08ae16a711a7833ca9b262b6041c8acab06670b` |
| Frozen Stage 1 export | `fd595b09f4aaace8009d92b0fd72b0fa4214b312453d47990b4cea2ad5cd9ba1` |
| Stage 3 discovery file | `a4703aa6ac115c99c80efdc39c6205c2932486868b674f0994fd0ed365fffd10` |
| Selected Stage 2 audit tree | `2116982f6e321484d76d217436bf7e627b2ff93eea63ecd5017b297b547511ac` |
| Selected Stage 4 generation tree | `dd03290a847e259669db68b12b214a443ebfd063c1a33200bb93e23c2b8910e1` |
| Producer-source bundle | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean tree | `41f11ac30a14507635b419c7dc8a71916828d38528d0e37286e00e41b0102d94` |

All nine per-file Stage 1 source hashes also match. The generator provenance,
input manifest, export result, original preflight, obligation-map hash,
trust-inventory hash, and pinned toolchain agree with these independently
recomputed values.

## Deterministic Stage 4 gate and target identity

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` against the three required mounted inputs and the
trusted toolchain lock. It returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `obligation_count: 0`;
- `target: null`;
- `lake clean` exit 0;
- `lake build` exit 0;
- generated tree hash
  `41f11ac30a14507635b419c7dc8a71916828d38528d0e37286e00e41b0102d94`;
  and
- 47 allowlisted generated trust declarations, with zero designated sorries.

The initial invocation exposed an audit-container issue: Lean's
`/proc/<getpid()>/exe` lookup used the nested PID against a host-PID `/proc`
mount. A minimal `LD_PRELOAD` shim made `getpid()` return the PID named by
`/proc/self`; it did not modify any mounted input, generated source, checker,
or theorem. With that environment repair, the unchanged trusted checker and
pinned Lean commit completed. The shim source, hash, and tool-version output
are preserved in
[15-hostpid-shim-build-and-test.txt](/audit-output/evidence/15-hostpid-shim-build-and-test.txt).
The failed diagnostic is retained in
[07-rerun-check-generation.txt](/audit-output/evidence/07-rerun-check-generation.txt),
and the successful returned evidence is in
[16-rerun-check-generation-success.txt](/audit-output/evidence/16-rerun-check-generation-success.txt).

The independent domain-lemma set is genuinely empty. It agrees exactly with:

- `input-manifest.json` `source_rules: []`;
- `obligation-map.json` `source_rules: []`;
- `obligation-map.json` `obligations: []`; and
- `obligation-map.json` `trust_parameters: []`.

Thus the source-rule/obligation correspondence is the exact empty bijection:
there are no omitted, duplicated, weakened, irrelevant, or vacuous conjuncts.
The trusted target constructor returns no expected definition, the trusted
target extractor returns null, and both `generator-manifest.json` and
`/audit-input.json` record null. `Lemmas.lean` has an empty namespace and no
target declaration. The fixed generated target is therefore exactly absent,
as required for `KLEAN_NO_OBLIGATIONS`.

## Stage 5

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`. No
`/candidate` exists, the launcher records no Lean workspace or invocation,
and there is no generated proposition for `Proof.final` to prove. This is the
required state for a legitimate zero-domain-obligation result.

## Judgment

Stage 3 is complete and correctly classified. Stage 4 is bound to authenticated
producer sources and immutable inputs, its generated project clean-builds, its
empty obligation set matches the independently empty domain-lemma set, and its
absent target is exact. The absence of Stage 5 is required rather than an
omission.

VERDICT: PASS
LEGITIMACY: LEGIT
