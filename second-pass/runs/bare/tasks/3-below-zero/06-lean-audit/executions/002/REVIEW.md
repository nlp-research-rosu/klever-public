# Independent Stage 3–5 Audit: `3-below-zero` / `bare`

## Scope and result

The launcher and environment both record `CLASSIFICATION_ONLY` under
`GENERATED_SEMANTICS`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`. I independently reconstructed and classified the
frozen Stage 1 rules, reran the trusted deterministic-generation preflight,
recomputed the mounted provenance bindings, and confirmed that a Lean proof
candidate is neither required nor present.

I treated the selected Stage 2 review, Stage 3 rationales, Stage 4 logs, and all
comments in the mounted inputs as untrusted evidence. No prior verdict was used
to reach this result.

## Rule inventory reconstruction

I invoked the trusted `/reference/tools/k_rule_inventory.py` implementation
against `/reference/k-proof`. `prove.sh` selects `VERIFICATION`, and the local
module closure inside `verification.k` is exactly `["VERIFICATION"]`. Imports
whose modules are defined in `semantic.k` or the K distribution are not local
modules in this file and therefore do not add local rules to this inventory.

The reconstructed `verification.k` SHA-256 is
`2bcf4b98c0ab283190e7f18d67ce40c4995229a5b61c9382dcceef818ea945c8`.
The canonical inventory has exactly these two ordered entries:

| Order | Span | `source_rule_id` / normalized SHA-256 | Reclassification |
|---|---:|---|---|
| 1 | 11–11 | `rule-fcdc37ffe1758064b9da7c725e0ad61a78f240a75ea058014581fdc375edabf6` | `DEFINITION` |
| 2 | 12–16 | `rule-8b7947851f91e86a240db6f33eb6cf303d12fbe3055e203d3b910d4df3445b39` | `DEFINITION` |

For each rule I independently normalized the exact extracted source text with
single whitespace separation, recomputed the SHA-256, and regenerated the
`rule-<sha256>` identity. Both identities match. Canonically hashing the
ordered rule documents gives
`d5def0ac85eed79dfa1a0f725d488b12243abe197cf40deeb8118eb10add9ab3`.

The protected Stage 3 manifest has the same count, ID set, order, individual
identities, and inventory hash. There are no duplicate, missing, extra, or
reordered entries. Exact reconstruction is in
`evidence/01_inventory_result.json`.

## Independent classification judgment

The declaration at `verification.k:9` introduces the total mathematical
summary `belowZeroFrom(Int, IntList) : Bool`.

The first inventoried rule is its base defining equation:

```k
belowZeroFrom(_, .IntList) => false
```

It defines the result for every starting balance on an empty list. It does not
match or replace an operational program configuration.

The second rule is its structurally recursive defining equation:

```k
belowZeroFrom(B, cons(I, IS))
  => #if B +Int I <Int 0
     #then true
     #else belowZeroFrom(B +Int I, IS)
     #fi
```

It consumes one `IntList` constructor, computes the updated balance, returns
true exactly when that balance is strictly negative, and otherwise recurs on
the tail with the updated balance. This is a recurrence defining the named
summary, not an ordinary execution rule and not a mathematical theorem added
to help a proof close.

The classification also agrees with the frozen source program and fixed K
semantics:

- `semantic.k:75–77` takes one list head and installs it as `current`.
- `semantic.k:69–71` changes `balance` from `B` to `B +Int I`.
- `semantic.k:100–102` tests the updated balance with strict `<Int 0`.
- The true branch executes the early `Return(true)`; `semantic.k:83–87`
  discards the remaining continuation and records the result.
- The false branch continues with the list tail.
- `semantic.k:74` ends an empty loop, after which the source's post-loop
  `Return(false)` executes.

Thus the two equations are precisely the base and step cases of the behavior
used in the `loop-correct` postcondition at `spec.k:54`. They are relevant to
the program and postcondition, but relevance does not turn defining equations
into domain lemmas.

Neither rule qualifies as `PROVED_DERIVED_LEMMA`: Stage 1 does not first prove
the exact rule against a module with that rule removed and only later use it.
Neither is an `OPERATIONAL_RULE`, because neither rewrites a `<k>` configuration
or observes execution state. There is no additional algebraic, ordering,
prefix-sum, or other domain theorem in the local closure. The independently
accepted `DOMAIN_LEMMA` set is genuinely empty.

The inventoried source attributes are empty. Even considering their role as
equations for a `[function, total]` symbol, their `DEFINITION` classification
satisfies the requirement that every simplifying rule be either a definition
or domain lemma. The two constructor cases are exhaustive for `IntList`, and
recursion descends on `IS`.

As finite adversarial support for this source-level judgment, I compared the
recurrence with an independent operational loop over every list of length
0 through 5 with elements from -3 through 3: 19,608 cases and zero mismatches.
Concrete witnesses reject constant-true, constant-false, final-balance-only,
non-strict-boundary, and head-ignoring mutations. These tests support, but do
not replace, the direct equation/semantics analysis. Results are in
`evidence/05_semantic_crosscheck_result.json`.

## Provenance and hash checks

The launcher resolution is internally bound by
`resolved_input_sha256 =
029adb4d8640f851cd078dd74fd5bb7f35ad43719bda3962cdf62676ce26a344`.
Independent recomputation matched:

- Stage 1 pipeline tree:
  `639f7233b9f8918bec0053d213458ef1f8a66a190c4488c1b19e0914a5bd2f91`
- Stage 1 deterministic-export tree:
  `35f8b4a7665b79e10c58099547dd158321a19689874d8c9c48f1404e6813fa42`
- Stage 2 selected audit tree:
  `f9f7ea334caeb7a209c1548fa0783979f556d6aa211f3eaab9ee5bf78da925b9`
- Stage 3 manifest:
  `fabd7fe1b139d97c12d50b5f3c99abdc197b5c295867fe6cec8f84d4eb320fdc`
- Stage 4 selected generation tree:
  `e1e4ced1a529bdde4d102a6e55e2114976406702c38112548934d17d3bbe0bf1`
- Generated project tree:
  `322f088531b9f1e7bddd6b3fa06f63af841d42455cea66d6f0608892a6437245`

The 240 recorded Stage 1 per-file paths and hashes match bijectively with the
mounted workspace; there are no path or digest mismatches. Both selected
artifact hashes also match their mounted trees.

I separately checked 31 mounted hash bindings across the launcher, Stage 3
manifest, input manifest, generator manifest, export result, recorded
preflight, obligation map, and trust inventory. All match. In particular:

- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
- trust inventory:
  `1680b9e90552c65805490ee7275c7e933168c24533f87e35c2c4f2340dbc3455`
- active audit-tool lock:
  `9cd22493bf7a2445bebb5c81b74bbe427a73a98d5c2a547db8b5c69b697ad56a`
- pinned toolchain lock:
  `a3dc0270ff7cab64550e91f605d8f2b5f6076b75f4ec49629a0e13894455fa9f`

Every tool file listed by the active mechanical-checker lock matches its
recorded digest. The reference and system toolchain locks are byte-identical.
Full results are in `evidence/02_hashes_result.json` and
`evidence/07_recorded_bindings_result.json`.

The generator manifest's `exporter_sha256`, `klean_py_sha256`, generator image
ID, and the launcher's audit image ID attest versions/images that are not
mounted as content-addressable artifact paths. I did not treat those labels as
evidence or compare them to the newer, separately locked audit-tool bundle.
All source/tree/file hashes that do have mounted referents were recomputed as
described above.

## Deterministic Stage 4 generation

I reran the required
`tools.klean_preflight.check_generation` call with `PYTHONPATH=/reference`,
using exactly:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The runner initially prevented Lean from locating itself because `getpid()`
returned an inner-namespace PID while mounted `/proc` exposed outer PIDs.
Lean 4.22 constructs `/proc/<getpid()>/exe`. I recorded that failure, then used
the small audited preload shim in `evidence/pid_namespace_shim.c` to return the
numeric `/proc/self` target. This changed no input or trusted checker code.
With the shim, Lean identified itself as version 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

The unchanged trusted preflight returned `KLEAN_NO_OBLIGATIONS`. Its returned
document is semantically identical to the recorded `preflight.json`:

- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `882e1a85708a6f08f9f08dd7511cd843635b7a4db64989e72788d0226167b31a`
- obligation count: 0
- target: `null`
- generated tree and all input hashes: exact matches

The exact failed attempt, shim build/test, successful returned evidence, and
command list are under `evidence/03c_preflight_failed_attempt.txt`,
`evidence/03b_pid_namespace_shim_build_and_test.txt`,
`evidence/03_preflight_result.json`, and `evidence/COMMANDS.md`.

## Obligation bijection and target identity

The independently accepted domain-rule ID list is empty. It exactly equals:

- `input-manifest.json.source_rules`
- `obligation-map.json.source_rules`
- the ordered list of `obligations[*].source_rule_id`

All three are empty and contain no duplicates. `trust_parameters` is also
empty. Generator, export-result, and preflight obligation counts are all zero.
There are therefore no omitted rules, duplicate obligations, weakened
conjuncts, irrelevant obligations, or vacuous conjuncts.

For an empty obligation map, the trusted generator's exact expected target
definition is `None`. Independent target extraction returns `None`; a raw scan
finds zero `def targetStatement` declarations. The generator manifest,
recorded preflight, and launcher all record `target: null`. Target identity is
therefore the required absence of a generated target, not a weakened theorem.
Detailed evidence is in `evidence/04_stage4_structure_result.json` and
`evidence/08_source_and_generated_excerpts.txt`.

The generated project contains translations of the two definitional equations
in `Klean3BelowZero/Func.lean`, but
`Klean3BelowZero/Lemmas.lean` declares no target proposition. The generated
Prelude's 41 recorded executable-hook axioms do not create a proposition or a
Stage 5 obligation, and no theorem depends on them because there is no target.

## Stage 5 applicability

`AUDIT_MODE` and the launcher both say `CLASSIFICATION_ONLY`.
`/candidate` does not exist, `lean_workspace` and `lean_invocation` are null,
and there is no generated target. This is exactly the required state for a
genuinely empty domain set. A Stage 5 copy/build, `Proof.final`, axiom print,
candidate declaration scan, and target-parameter operational-bridge audit are
not applicable and were not fabricated.

## Conclusion

Both Stage 3 entries are honest defining equations of the exact recursive
summary used by the frozen postcondition. No true domain lemma is hidden by
those classifications, so the true domain set is empty. Stage 4 preserves that
empty set bijectively, generates no target, and passes the trusted preflight
with all mounted content bindings intact. The absence of a Stage 5 candidate is
therefore correct.

VERDICT: PASS
LEGITIMACY: LEGIT
