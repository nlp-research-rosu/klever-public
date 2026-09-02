# Independent Stage 3/4/5 Audit: `44-change-base`

## Scope and result

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`.
`AUDIT_MODE` and the signed `/audit-input.json` both select
`CLASSIFICATION_ONLY`. I treated the prior proof, prior audit, manifests, logs,
comments, and generated sources only as evidence; no earlier classification or
verdict was accepted as authority.

The selected `KLEAN_NO_OBLIGATIONS` result is correct. The local verification
closure contains six rules, each is genuinely a defining equation for one of
two fresh summary functions, and none is a domain lemma. Consequently the true
domain-lemma set is empty, the exact Stage 4 obligation set is empty, there is
no generated target, and there is no Stage 5 candidate.

## Producer provenance gate

I hashed the mounted generation-time producer files before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The source manifest and generator manifest both bind
the immutable generator image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the same image digest is the final path component of the signed
`resolution.generation_producer_sources` in `/audit-input.json`. The mounted
bundle has exactly the expected three regular files, and its independently
recomputed contract tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching the audit input. This gate passes; there is no producer-source
`AUDIT_ERROR`.

Raw evidence: `evidence/01_producer_provenance_raw.txt` and
`evidence/10_reconstruction_and_hash_results.txt`.

## Canonical inventory reconstruction

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation over
the frozen `/reference/k-proof`, rather than copying Stage 3 data. It selected
main module `VERIFICATION`; its locally defined module closure is exactly
`["VERIFICATION"]`. The frozen `verification.k` hash is
`3a887f9d36bc2eda11777c2c7ab56560507ada5aa591a006d60b5b38eff5c4a8`.

The reconstruction produced these six ordered entries:

| Lines | `normalized_sha256` / `source_rule_id` | Attributes |
|---|---|---|
| 11--13 | `a83520c2dd7e4dd9d917bbb76d25675cd45efb14625dd3c04c89bea96b55f994` / `rule-a83520c2dd7e4dd9d917bbb76d25675cd45efb14625dd3c04c89bea96b55f994` | `simplification` |
| 15--17 | `efae065e614915ce96e387b26c2b7d560fb4b333fdbf8df6c5449cfcc506f474` / `rule-efae065e614915ce96e387b26c2b7d560fb4b333fdbf8df6c5449cfcc506f474` | `simplification` |
| 19--25 | `ecc726b19ca39761f0f286a8792a1c0d075bb725e0d8eb2538c8383ea095d39a` / `rule-ecc726b19ca39761f0f286a8792a1c0d075bb725e0d8eb2538c8383ea095d39a` | `simplification` |
| 30--31 | `fdf7755e024660316168d967838e2f08fc43b0714316aea144f9262274ca8118` / `rule-fdf7755e024660316168d967838e2f08fc43b0714316aea144f9262274ca8118` | `simplification` |
| 33--35 | `245f4d2054d650ca1be786d19cae2a4a19ab245f30f7fcbfe5c1941337011d41` / `rule-245f4d2054d650ca1be786d19cae2a4a19ab245f30f7fcbfe5c1941337011d41` | `simplification` |
| 37--40 | `6eaa184d7af4006c64c04aece2ef1ec1819bca91e287204a99a56c1d22546abd` / `rule-6eaa184d7af4006c64c04aece2ef1ec1819bca91e287204a99a56c1d22546abd` | `simplification` |

The whole inventory hash is
`6b7cc9b5eb3dab9e078c1ec848cbe95c1df8a055e1a23922684aa8ed53edc950`.
It matches the protected discovery manifest. The manifest IDs equal the
canonical ordered list exactly and are unique: there are no omissions,
duplicates, extras, reordered identities, changed hashes, or unclassified
rules. Trusted `validate_trust_boundary` also passes.

The complete reconstructed source text, spans, attributes, hashes, IDs, and
comparison are in `evidence/10_reconstruction_and_hash_results.txt`.

## Independent classification judgment

The source program's loop does two relevant updates while `x > 0`:

```text
result := chr(48 + x % base) + result
x := x // base
```

The supplied K semantics defines integer `%` as `pyMod`, integer `//` as
`(x - pyMod(x,base)) /Int base`, `chr(i)` as a one-code string, and string `+`
as ordered concatenation. Its while rules execute the body and repeat exactly
when the comparison is truthy. Therefore one source iteration prepends code
`48 + pyMod(N,B)` and continues at precisely
`(N - pyMod(N,B)) /Int B`. For the theorem domain `N > 0` and `B >= 2`, the
new magnitude is nonnegative and strictly smaller. Because `B < 10`, the digit
codes are in `48..56`, within the supplied `chr` guard.

My per-rule classifications are:

1. Lines 11--13: `DEFINITION`. This is the terminating `baseAcc` case for a
   nonpositive remaining magnitude.
2. Lines 15--17: `DEFINITION`. This is a disjoint totalization case for a
   positive magnitude and an invalid base below 2. It is outside the target
   domain and does not assert a source property.
3. Lines 19--25: `DEFINITION`. This is the recursive `baseAcc` equation and
   exactly mirrors one operational loop iteration.
4. Lines 30--31: `DEFINITION`. This defines the zero result as code 48, matching
   the program's early return `"0"`.
5. Lines 33--35: `DEFINITION`. This defines the positive result by initializing
   `baseAcc` with the empty accumulator.
6. Lines 37--40: `DEFINITION`. This defines the negative result by prefixing
   code 45 and converting the negated magnitude, matching the sign branch.

For `baseAcc`, the guards `N <= 0`, `N > 0 and B < 2`, and
`N > 0 and B >= 2` are pairwise disjoint and exhaustive over integers. For
`changeBaseCodes`, the zero, positive, and negative cases are likewise
disjoint and exhaustive. Every left-hand side is headed by a freshly declared
pure summary function. None matches a `<k>` cell, call, loop, return,
assignment, binding, continuation, or any other operational state. The rules
do not state additional digit-validity, arithmetic, or representation
properties; they define the named recurrences themselves.

Thus all six rules are `DEFINITION`. There are zero `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA` entries. In particular, no rule
is being accepted as derived without a prior independent K proof, and no
domain lemma has been hidden under another label. Every simplification rule is
in an allowed class.

The frozen program/spec and exact operational rules are recorded in
`evidence/07_frozen_source_and_manifests.txt` and
`evidence/13_relevant_operational_semantics.txt`; the detailed independent
classification record is `evidence/15_independent_classification.md`.

## Hash and manifest integrity

The signed audit-input envelope verifies: its recomputed canonical resolution
hash is
`556ca659087e67697bd406fe2d1fe7a5a1b4da817deac5317d5062f9e8f6293a`.
Independent recomputation matched all resolution-level hashes, including:

- Stage 1 contract tree:
  `158f2ef8a9acfd37759b73008486fb19a0232460b95d45685c6a4166bc3bdf55`;
- Stage 1 Klean export tree:
  `a44bbf20a6e80e6ba17cbeb6e3ca61b4d7747dae69506175529a1f4086fcacac`;
- Stage 3 manifest:
  `b9f9d5abc42ad4acfa0a3fbd0e15e48381b98d31632870d005885e0a60713004`;
- selected Stage 2 tree:
  `a859b5657921e67c549167f5997d1a27348b3bec5ed3f4653098423b6f5327bf`;
- selected Stage 4 tree:
  `d8bb40db2080ff7917b1367bbae8ba8689802c8bff990f4e5a19555f511de190`;
- generated project tree:
  `29d2506552fe65ab72dd1a790babf27423ba71c1c2410bdae285ef34891af646`.

All 769 per-file Stage 1 hashes match with zero mismatches. The obligation-map
hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
and the trust-inventory hash is
`239128c984b5f1273fd97df82aa94c3536bd3f55df1b8ff8248a8a08f5177241`;
both match their recorded bindings. The generator toolchain equals the trusted
lock. The original recorded clean/build output hashes also recompute from the
complete stored outputs, and the signed `stage4_preflight` object is exactly
the mounted `preflight.json`.

Raw comparisons are in `evidence/10_reconstruction_and_hash_results.txt` and
`evidence/37_remaining_recorded_hashes.txt`.

## Stage 4 preflight, obligation bijection, and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the required frozen workspace, protected discovery manifest, selected
generation, and trusted toolchain lock. The successful fresh result is:

- status: `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0;
- `lake build`: exit 0, all seven generated modules built;
- obligation count: 0;
- target: `null`;
- designated sorry count: 0;
- trust declaration count: 43;
- all frozen input, discovery, and generated-tree hashes unchanged.

The sandbox initially prevented Lean from locating its executable because it
unshares the PID namespace while exposing the parent namespace's read-only
`/proc`. The baseline failures and PID evidence are preserved. I used a local
`LD_PRELOAD` shim that changes only `readlink("/proc/<numeric-pid>/exe")` to
`readlink("/proc/self/exe")`. It does not modify or shadow any audited source,
manifest, generated file, or declaration. With the shim, Lean reports exactly
version 4.22.0 at locked commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the trusted preflight
completes. The successful result and complete build output are in
`evidence/30_fresh_klean_preflight_success.txt`; the shim source and diagnostic
trail are in `evidence/proc_exe_shim.c` and evidence files 16--28.

The Stage 4 input manifest contains exactly the six canonical definitions and
exactly the empty canonical lists for operational rules, proved derived
lemmas, and domain source rules. The independently derived domain-source list,
`obligation-map.json.source_rules`, `obligations`, and `trust_parameters` are
all `[]`. The generator's obligation count is 0. Trusted reconstruction gives
`expected_target_definition = null`, and independent inspection gives
`observed_target = null`. This is an exact empty-set bijection, not an omission:
the independently classified true domain-lemma set is genuinely empty.

The explicit comparisons are in
`evidence/34_exact_obligation_and_target_bijection.txt` and
`evidence/35_input_manifest_classification_bijection.txt`. Generated
declarations and the absence of `targetStatement` are recorded in
`evidence/32_generated_target_and_declarations.txt`.

## Stage 5 disposition and trust

Stage 5 is not applicable. The signed audit input has `target = null`,
`stage5_result = null`, and null Lean workspace/invocation hashes. The
filesystem has no `/candidate`. This is exactly the required state for a
genuine `KLEAN_NO_OBLIGATIONS` classification. There is therefore no
`Proof.final`, no candidate target to compare or shadow, no target parameters
requiring operational-bridge review, and no candidate axiom accounting to run.

The generated support project contains 43 non-propositional trust declarations
recorded exactly in `trust-inventory.json`; trusted preflight confirms the
declaration/allowlist equality and rejects proposition trust. Those support
declarations prove no target because no target proposition exists. They do not
turn an omitted domain lemma into a proof obligation; the independent semantic
classification already established that the domain set is empty.

## Final judgment

The Stage 3 classification is complete, ordered, and mathematically correct;
Stage 4 is provenance-bound, hash-consistent, freshly buildable, and exactly
represents the empty true domain-lemma set; the absent target and absent Stage 5
candidate are required rather than suspicious. I found no weakened, irrelevant,
duplicated, vacuous, or omitted obligation and no target change.

VERDICT: PASS
LEGITIMACY: LEGIT
