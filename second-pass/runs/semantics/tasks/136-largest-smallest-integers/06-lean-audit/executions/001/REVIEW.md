# Independent Stage 3–5 Audit: 136-largest-smallest-integers

## Scope and audit mode

This audit covers HumanEval problem `136-largest-smallest-integers`, condition
`semantics`, semantics mode `SUPPLIED_SEMANTICS`.

Both `AUDIT_MODE` and `/audit-input.json` record `CLASSIFICATION_ONLY`.
Accordingly, the mounted Stage 4 selection is `KLEAN_NO_OBLIGATIONS`,
`/candidate` is absent, all launcher Stage 5 fields and hashes are null, and
there is no Stage 5 proof to validate. I treated every mounted candidate,
review, log, comment, and rationale as untrusted evidence and did not rely on
the prior Stage 2 verdict or Stage 3 rationales.

## Producer-source and provenance authentication

I authenticated the immutable generation-time sources before accepting any
Stage 4 result:

- `/reference/generation-tools/klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`.
- `/reference/generation-tools/klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`.
- Both hashes exactly match `source-manifest.json` and
  `generator-manifest.json`.
- The generator image is
  `sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
  in both manifests. `/audit-input.json` binds the producer-source directory
  whose basename is exactly that image digest. (Its separate `audit.image_id`
  identifies the auditor image, not the Stage 4 generator.)
- The producer-source tree hash is
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
  exactly the launcher-recorded value.

The broader independent hash check performed 39 comparisons with zero
mismatches. It checked all 765 launcher-recorded Stage 1 per-file hashes and
the Stage 1, Stage 2, Stage 3, Stage 4, generated-project, obligation-map,
trust-inventory, and toolchain bindings. Notable matching values are:

- Stage 1 pipeline tree:
  `752500f37c14d74b4bb9dceddfc0dbc2084f3225211d4db153be4a9cd290227e`.
- Stage 1 deterministic-export tree:
  `122c8955f5188979a6fb76ebb9b753759577d3c9c46f2e81dee1d81229d16a2d`.
- Stage 3 manifest:
  `b63332c10f6c686d93eb9a8a4e17ba0d4c8860d26a2c8ffd83a7d319501b821e`.
- Selected Stage 4 tree:
  `d1a6096dbad0862489a27101f8aa73bc3296e2ba762ef1665791ef92de2876a7`.
- Generated project tree:
  `e6c5d7c3dbc47b4461f9c99a9079dfd5a5fa071933f45d6040710e66e59c386c`.

Full results are in
[recorded-hash-verification.json](/audit-output/evidence/recorded-hash-verification.json)
and the executable audit logic is retained in
[verify_recorded_hashes.py](/audit-output/evidence/verify_recorded_hashes.py).

## Canonical inventory reconstruction

The trusted rule-inventory code reads the final `kompile verification.k`
command in `prove.sh`, selects `VERIFICATION`, and computes its local
verification-file import closure. The closure contains only the local module
`VERIFICATION`; `MPY` is supplied by the required semantics outside the local
file.

Independent reconstruction produced:

- `verification.k` SHA-256:
  `feac1a9aaf95141a45c785cb0b6e8361a5c889bea6af88c1babc1617aa46b99f`.
- 26 canonical rules.
- Inventory SHA-256:
  `c546cc66576bdf88dd066e086ead92df73aa01251b15271d8bc4c78b5a3b2273`.

For every rule I recomputed the source span, normalized source hash, and
`source_rule_id`; every ID is exactly `rule-<normalized_sha256>`, and every
reported text equals the corresponding frozen line slice. Comparison with
`/reference/lemma-discovery.json` was bijective and order-sensitive: there are
no omitted, duplicate, extra, reordered, changed-hash, malformed-ID, or
source-span entries. The manifest inventory hash equals the independently
recomputed whole-inventory hash.

The complete reconstructed records are in
[reconstructed-inventory.json](/audit-output/evidence/reconstructed-inventory.json);
the comparison is in
[inventory-comparison.json](/audit-output/evidence/inventory-comparison.json).

## Independent rule classification

My classification totals are:

| Class | Count |
|---|---:|
| `DEFINITION` | 25 |
| `OPERATIONAL_RULE` | 1 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All 25 definitions have a fresh proof-local head symbol and genuinely define a
macro, named proof term, summary function, structural recurrence, input
predicate, or sentinel conversion:

- `scanBody`, `finishBody`, `solutionBody`, and `largestSmallestModule`
  reconstruct the exact translated program in `solution.mpy`.
- `negStep`/`posStep` and `negFold`/`posFold` define the extrema summaries used
  by the entry-point postcondition.
- `finalValue` defines the loop-variable summary used by the loop claim.
- `allInts` defines the formal input predicate.
- `optionalNeg` and `optionalPos` define the final zero-to-`None` conversion.
- `intValue` defines the integer projection used under integer-sort evidence.

These are equations defining newly introduced symbols, not mathematical facts
about pre-existing symbols, so none is a hidden domain lemma. Each is relevant
to the frozen program, loop claim, precondition, or postcondition.

The sole operational entry is the rule at `verification.k:12–15`:

```k
rule <k> #iterNext(list(vCons(V:Val, REST:ValSeq)))
      => #iterYield(intValue(V), list(REST)) ... </k>
  requires isInt(V)
  [priority(40)]
```

The supplied semantics rule at `semantics/list.k:10` has the same nonempty-list
match and continuation but yields `V` directly. On the specialized rule's
strictly narrower match domain, `isInt(V)` and the definition
`intValue(I:Int) => I` make the yielded value identical. The rule preserves
the remainder, arbitrary continuation, control, and every non-`k` cell; it
introduces no return, exception, frame change, or state effect. Heads `-3`,
`0`, and `5` discriminate the identity, while `noneV` fails the specialized
guard and stays with the supplied rule. Thus this is an ordinary operational
sort refinement, not a domain lemma and not an unproved derived lemma.

No rule in the inventory has the `simplification` attribute. No rule is claimed
as `PROVED_DERIVED_LEMMA`, so there is no unsupported “proved first, used
later” assertion. The exact per-rule judgments are in
[classification-judgment.md](/audit-output/evidence/classification-judgment.md).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against exactly:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`; and
- `/reference/klean-toolchain.lock.json`.

The first attempt exposed an audit-container infrastructure defect before any
Lean checking: Lean 4.22 resolves its executable with
`/proc/<getpid()>/exe`, while this PID namespace's `/proc` mount exposes only
the equivalent `/proc/self/exe`. I preserved the failure, diagnosed it, and
used a narrow audit-local `readlink` shim that changes only
`/proc/<digits>/exe` to `/proc/self/exe`. It does not alter source, generated
artifacts, Lean terms, or compiler results. The shim source and environment
evidence are retained under `evidence/`.

With that compatibility fix, the unchanged trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0;
- `lake build` exit 0;
- zero designated sorries;
- zero obligations;
- target `null`; and
- the same frozen-input, discovery-manifest, and generated-tree hashes listed
  above.

The exact returned object, including complete build output (the output is under
the checker's 4,000-character retention bound), is in
[preflight-check-generation.json](/audit-output/evidence/preflight-check-generation.json).
The initial failure is in
[preflight-first-attempt.txt](/audit-output/evidence/preflight-first-attempt.txt),
and all principal commands are collected in
[COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## Obligation bijection and fixed target

The independently classified true domain-lemma set is empty. The entire
deterministic mapping is therefore the unique empty bijection:

```text
independent DOMAIN_LEMMA source IDs = []
input-manifest source_rules          = []
obligation-map source_rules          = []
obligation-map obligations           = []
obligation-map trust_parameters      = []
```

The generator manifest and export result both record obligation count 0.
`obligation-map.json` has no conjunct, so there is no irrelevant, weakened,
duplicated, omitted, or vacuous conjunct. The expected generated target is
therefore absent. Independent target parsing returns `None`;
`Lemmas.lean` contains no target declaration; and the generator manifest,
recorded preflight, fresh preflight, and `/audit-input.json` all record target
`null`. There is no target change or shadow.

The 20 independent structure checks, including exact categorized Stage 3 lists,
the empty source-rule/obligation bijection, all target identities, selected
status, and Stage 5 absence, have zero mismatches in
[stage4-structure-verification.json](/audit-output/evidence/stage4-structure-verification.json).

## Stage 5 disposition

Stage 5 checks are conditional on `CLASSIFICATION_AND_PROOF`; this launch is
`CLASSIFICATION_ONLY`. Consistent with the genuine empty domain set:

- there is no generated target;
- `/candidate` does not exist;
- `stage5_result`, `lean_workspace`, and `lean_invocation` are null; and
- both Lean workspace/invocation hashes are null.

Therefore no `Proof.final`, candidate parameter definitions, candidate clean
build, or `#print axioms Proof.final` exists or is required. The absence is
the required Stage 5 state for a legitimate `KLEAN_NO_OBLIGATIONS` selection.

## Judgment

The Stage 3 classification is complete and mathematically appropriate; the
true domain-lemma set is empty. The authenticated deterministic Stage 4 output
is exactly the required no-obligation artifact with no target, and the
classification-only launcher correctly supplies no Stage 5 candidate. All
structural, provenance, hash, build, bijection, and target-identity checks
pass.

VERDICT: PASS
LEGITIMACY: LEGIT
