# Independent Stage 3–5 audit: `151-double-the-difference`

## Scope and result

The launcher envelope is internally valid and records:

- condition `bare`;
- semantics mode `GENERATED_SEMANTICS`;
- audit mode `CLASSIFICATION_ONLY`; and
- selected Stage 4 status `KLEAN_NO_OBLIGATIONS`.

I independently reconstructed the Stage 3 inventory and classification, then
audited the deterministic Stage 4 generation. Stage 5 is correctly absent in
this mode: the audit input has null Lean workspace, invocation, result, and
target fields, and `/candidate` is not mounted.

The classification is correct. The genuine domain-lemma set is empty, so the
zero-obligation Stage 4 result is legitimate.

## Producer provenance gate

I hashed the two mounted generation-time producer sources before judging the
generation:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

These hashes exactly match both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
sources plus the source manifest. The generator image ID is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest and generator manifest, and its digest component is the
bundle identity in the launcher-recorded producer path. The producer bundle
tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`. There is no producer-provenance infrastructure
error.

The signed launcher resolution also recomputes to
`6d86342e826c0bdd8178d7e390ac5f1dd66bfa5ddd055436f9275047f25793ca`.
Every recorded input hash matched independently:

| Input | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `3c153940251af71a81e568dd1f20dcf6b2d42de1de92ab47c7ee7b454e6e6c94` |
| Stage 1 export tree | `b5249f4aa17d496511c80d28999bd4ce2259e20c312c986d1a94b59106277e6e` |
| Stage 3 discovery manifest | `0b9e1d917a2c49c70d8acabd4c04c76dbb37618f7ae45b4e0177132c97c72692` |
| Selected Stage 2 tree | `5e5c918d129e88cd3ab50cf9264a01bb666a8afe22f1f99cdaecefcdf7ea8c42` |
| Selected Stage 4 tree | `e3442e8145679cfdd77aa251907520bc200e4e90b0ddd6f61a34330d41ebd0d1` |
| Generated project tree | `63c14522fca63883ad0e70dc8d0ebf4642c9aea740bdcbbf9f4cd048df3051a8` |

All 41 launcher-recorded per-file Stage 1 source hashes also match.

Raw result:
`evidence/01-provenance-inventory-rerun.log`.

## Canonical inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` code against
the frozen `/reference/k-proof`, I resolved the proof-selected main module to
`VERIFICATION`. Its local closure inside `verification.k` contains only that
module; imported `MPY` is defined in the required `semantic.k`, not as another
local module in `verification.k`.

The reconstructed `verification.k` hash is
`d967476540ac1ef2dba63f2126ff7641aad9b6988d07f698494806ebcebb2bc4`.
The canonical inventory has ten rules and hash
`947d99fd15d1308651c2cc9e54a4d58890f51308992f804a352683a5136451e7`.
For every entry, I independently confirmed that:

- the recorded span extracts exactly the rule text from frozen source;
- SHA-256 of whitespace-normalized text equals `normalized_sha256`;
- `source_rule_id` is exactly `rule-<normalized_sha256>`; and
- the Stage 3 identity occurs exactly once and at the same ordinal position.

The bijection has no omissions, duplicates, extras, reordering, or changed
hashes. The whole-inventory hash also agrees across the Stage 3 manifest, input
manifest, and generator provenance.

## Independent rule classification

Every rule has an empty rule-attribute list, so there is no
`simplification`-attributed rule to satisfy separately. I reclassified each
rule from the frozen source rather than accepting its rationale:

| Position and span | `source_rule_id` | Judgment |
|---|---|---|
| 0, lines 10–20 | `rule-844231156e8298b2f3f1f0d2760dbd2dbfb000083c6677f15629b7ed13bd6a65` | `DEFINITION`: `loopBody` is a named proof term expanding to the exact translated loop-body constructor tree. |
| 1, lines 23–28 | `rule-e0ae7f562a5a11b10584f0fb0c6d0b749dfc727a5985bfecd6b7a36f2f96f9ad` | `DEFINITION`: `solutionProgram` is the exact module/function constructor macro, using `loopBody`. |
| 2, lines 37–38 | `rule-8454b752a76f90d1a39baf4e33b2d9e2f834614960822c927d2511cd5aa2b08e` | `DEFINITION`: selected nonnegative odd integer case of fresh summary `selectedSquare`. |
| 3, lines 39–40 | `rule-44a20257cb460498a6716cd704123f476069138be2df34c2c6af991d309f58d7` | `DEFINITION`: complementary unselected case of `selectedSquare`. |
| 4, line 42 | `rule-c14a0f369e43a8ec59130209c3f14aa51ea94251a1f7e613c750f61abdecb12b` | `DEFINITION`: empty-list base case of fresh recurrence `oddSquareFold`. |
| 5, lines 43–44 | `rule-679ba6aca8f5cb4617e8b1cc5ddee8d34d027eb30d0ab793315ae4c7df5a6fe3` | `DEFINITION`: integer-head recurrence using `selectedSquare`. |
| 6, lines 45–46 | `rule-5e4a4cb86f56fc30db7ddbf3c6f8b5aa8ced3783ec154620a4d07e50d309dd22` | `DEFINITION`: float-head recurrence with zero contribution. |
| 7, lines 47–48 | `rule-f584191e2346e78c94bf076ce12c59b19e092b1855804ed825d3a4e72ecf99b8` | `DEFINITION`: true-boolean recurrence with contribution one. |
| 8, lines 49–50 | `rule-f0a3752efa56c973f2eddf6d2933848ce052ed1be1c2cc6354b9789a36ae50e2` | `DEFINITION`: false-boolean recurrence with zero contribution. |
| 9, lines 51–52 | `rule-da8dfd435ecea940ae65a4759b362315e9c5ff5e381d41b97e3051b3cab07ef5` | `DEFINITION`: nested-list-head recurrence with zero contribution. |

The first two rules introduce exact constructor abbreviations. They do not
assert a mathematical fact or replace the body with an opaque result. The
remaining eight are equations whose left sides contain the newly defined
summary symbols. They define those summaries; they are not free-standing
facts about existing domain operations.

No rule is an ordinary execution/observation rule over the operational cells,
so the `OPERATIONAL_RULE` set is empty. No rule is claimed as
`PROVED_DERIVED_LEMMA`, and therefore no unsupported “proved first, used
later” claim is present. No rule remains as a `DOMAIN_LEMMA`.

### Operational-semantic check

The classification and empty domain set also agree mathematically with the
frozen program and K semantics:

- `loopBody` and `solutionProgram` reproduce the constructor program in
  `solution.mpy`, including initialization, iteration, the three nested tests,
  conditional square accumulation, and return.
- For an integer head, fixed semantics makes `isIntVal` true, evaluates the
  same `I >= 0` and `I % 2 == 1` conditions, and adds `I * I` exactly when both
  hold. The two `selectedSquare` guards are `P` and `notBool P`, hence disjoint
  and exhaustive over integers.
- A float or nested-list value makes `isIntVal` false and leaves the
  accumulator unchanged, as its fold equation specifies.
- The semantics intentionally models CPython `bool` as an `int` subclass:
  `asInt(true) = 1` and `asInt(false) = 0`. Thus true contributes one and false
  contributes zero, exactly as the two boolean recurrences specify.
- The `Vals` domain is exhausted by `nil`, `intCons`, `floatCons`, `boolCons`,
  and `listCons`; the fold rules cover all of them and recurse on the tail.
  This is precisely the loop invariant and the end-to-end postcondition in
  `spec.k`, so the definitions are relevant rather than decorative.

Finite adversarial corroboration covered negative/zero/positive parity
boundaries, very large positive and negative integers, both booleans, floats,
and nested lists. It found no mismatch and detected constant-zero, identity,
square-every-integer, and exclude-boolean counterfactuals. This finite check is
supplemental; the universal judgment above follows from the exhaustive K
constructor and guard analysis.

Raw results:
`evidence/01-provenance-inventory-rerun.log` and
`evidence/05-semantic-cases.log`.

## Deterministic Stage 4 audit

I reran exactly `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and these immutable inputs:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`; and
- `/reference/klean-toolchain.lock.json`.

The command sandbox exposes `/proc` from an outer PID namespace while
`getpid()` reports an inner PID. Lean 4.22 initially failed to find
`/proc/<inner-pid>/exe`. I preserved that failed run, documented the mismatch,
and used a minimal `LD_PRELOAD` compatibility shim that changes only `getpid()`
to the numeric PID represented by `/proc/self`. With the pinned toolchain then
resolvable, the trusted preflight function itself ran unchanged.

The successful return was:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- trust declaration count `42`;
- designated sorry count `0`;
- `lake clean`: exit `0`, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit `0`, output SHA-256
  `208db0a3f72247a2982c8523fe0a21a218e5be75b16144851ea58b88d7ed666f`;
  and
- frozen input, discovery, and generated-project hashes equal to the values
  independently listed above.

The build-output hash exactly matches the selected Stage 4 preflight record.
The shim does not edit the checker, source, project, or toolchain; the
preflight's before/after immutable snapshots remained equal.

Raw environment diagnosis and returned evidence:
`evidence/02-toolchain-environment.log`,
`evidence/03-preflight.log`, and
`evidence/03-preflight-rerun.log`.

## Obligation bijection and fixed target

My independent classification yields zero domain source rules. The following
are all exactly `[]`, in the same order:

- independently derived domain source rules;
- `input-manifest.json` source rules;
- `obligation-map.json` source rules;
- generated obligations; and
- generated trust parameters.

The source-rule/obligation mapping is therefore a genuine empty-set bijection,
not an omission. The obligation-map SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
and matches the generator manifest. All generator, export-result, recorded
preflight, and independently counted obligation counts are zero.

Because there are no conjuncts, there is no irrelevant, weakened, duplicated,
or vacuous generated obligation. The deterministic expected target is null.
Trusted target parsing returns null; `targetStatement` occurs zero times in
the generated Lean tree; and the generator manifest, recorded preflight, and
audit input all bind the same null target. `Lemmas.lean` contains only imports,
comments, and an empty namespace. Thus there is no changed generated target.

The selected status is consistently `KLEAN_NO_OBLIGATIONS` across the export
result, recorded preflight, and launcher selection. Since the true domain set
is empty, this status is substantively correct, not merely self-consistent.
The required absence of a Stage 5 candidate is also confirmed.

Raw result: `evidence/04-stage4-bijection.log`.

## Final judgment

Stage 3 is bijective and correctly classifies all ten local verification rules
as definitions. Stage 4 faithfully produces no obligations and no theorem
target from the genuinely empty domain-lemma set. The provenance gate, all
recorded hashes, clean preflight build, empty obligation bijection, fixed null
target, and absence of Stage 5 all pass.

VERDICT: PASS
LEGITIMACY: LEGIT
