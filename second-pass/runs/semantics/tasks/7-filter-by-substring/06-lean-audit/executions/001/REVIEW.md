# Independent audit: `7-filter-by-substring` / `semantics`

## Result and scope

The launcher environment and `/audit-input.json` both select
`CLASSIFICATION_ONLY` with semantics mode `SUPPLIED_SEMANTICS`. I did not rely
on the selected Stage 2 review, any prior PASS, or any candidate/provenance
comment as authority. The selected Stage 2 tree was used only as a hash target.

The independent result is:

- the frozen Stage 1 local verification-module closure contains 17 rules;
- 11 are definitions and 6 are operational execution/observation rules;
- there are no `DOMAIN_LEMMA` or `PROVED_DERIVED_LEMMA` rules;
- the genuine domain-lemma set is therefore empty;
- Stage 4 maps that empty set bijectively to zero obligations, generates no
  target proposition, and has no Stage 5 proof candidate; and
- all producer, source, tree, manifest, obligation-map, and trust-inventory
  hashes checked below match.

Thus `KLEAN_NO_OBLIGATIONS` is legitimate for this classification-only audit.
This result does not claim that Stage 4 contains a Lean proof of the HumanEval
property: with a genuinely empty domain-lemma set, no Stage 5 theorem is
required or present.

## Inventory reconstruction

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation
directly on `/reference/k-proof`. The selected main module is
`FILTER-VERIFICATION`; its local closure in `verification.k` contains only that
module. `MPY` is supplied in external required files and was consulted for
operational meaning, but its rules are not proof-local rules in the frozen
`verification.k`.

The reconstruction produced:

- `verification.k` SHA-256:
  `afd06df9b0eaf53092c5a24aa52a0d06b5455932bc1aa260a0d1f1c1bfcc3d80`;
- rule count: 17; and
- canonical inventory SHA-256:
  `ec6635206f003e52afd47b526f0c4851bd55d2a3c9a9e67c810b17bc5b8c8605`.

For every rule, the trusted inventory recomputed the exact physical source
span, whitespace-normalized source SHA-256, and
`source_rule_id = "rule-" + normalized_sha256`. The complete reconstructed
documents are in `evidence/05-reconstructed-rule-inventory.json`.

The protected Stage 3 list has exactly the same 17 identities in exactly the
same order. There are no omitted, duplicated, or extra identities. Its
inventory hash is exact. The per-position comparison is recorded in
`evidence/07-stage3-bijection.json`; the enriched Stage 4 classification
buckets are also an exact one-to-one partition of the reconstructed inventory,
as recorded in `evidence/41-classification-generation-bijection.json`.

## Independent rule classification

I read the frozen `verification.k`, `solution.py`, `solution.mpy`, `spec.k`,
and the relevant supplied operational rules in `core.k`, `iter.k`, `list.k`,
`operators.k`, `str.k`, and `controls.k`. The independent classification is:

| Source lines | Rule ID prefix | Class | Independent basis |
|---|---|---|---|
| 13 | `rule-c68c2918…` | `DEFINITION` | Empty case of the named `strVals` structural representation |
| 14–15 | `rule-e676bec1…` | `DEFINITION` | Recursive `strVals` constructor equation |
| 18–20 | `rule-827a5136…` | `OPERATIONAL_RULE` | Dispatches the list iterator observation to an auxiliary iterator state |
| 21 | `rule-89be9027…` | `OPERATIONAL_RULE` | Empty auxiliary iterator execution step |
| 22–23 | `rule-be9d3af4…` | `OPERATIONAL_RULE` | Nonempty auxiliary iterator execution step |
| 27–29 | `rule-6a925c15…` | `OPERATIONAL_RULE` | Dispatches a string-membership comparison observation |
| 30–31 | `rule-9de7aaa8…` | `OPERATIONAL_RULE` | Positive containment execution branch |
| 32–33 | `rule-4bdddd2d…` | `OPERATIONAL_RULE` | Negative containment execution branch |
| 38 | `rule-01218437…` | `DEFINITION` | Base equation of the named filter accumulator recurrence |
| 39–43 | `rule-85795a93…` | `DEFINITION` | Recursive include case of the filter accumulator |
| 44–48 | `rule-63da1a3e…` | `DEFINITION` | Recursive exclude case of the filter accumulator |
| 51–52 | `rule-60d38087…` | `DEFINITION` | Named `filterStrings` summary wrapper |
| 55 | `rule-505dd923…` | `DEFINITION` | Base equation of the named `lastCodes` recurrence |
| 56–57 | `rule-be48bda4…` | `DEFINITION` | Recursive `lastCodes` equation |
| 61–64 | `rule-6e4d80c9…` | `DEFINITION` | Exact `filterLoopBody` macro expansion |
| 67–70 | `rule-087911b9…` | `DEFINITION` | Exact `filterBody` macro expansion |
| 73–76 | `rule-296f99ca…` | `DEFINITION` | Exact `filterProgram` macro expansion |

### Definitions

The `strVals` pair defines the proof-side encoding of a finite typed sequence
of strings as the supplied semantics' `ValSeq`. The three
`filterAccStrings` equations are a base case and two guarded recursive cases
for a named mathematical summary. Their guards are disjoint and exhaustive
because `strContains` is a total Boolean function, and recursion descends on
the `StrSeq` tail. `filterStrings` initializes the accumulator.

`lastCodes` is a named structural recurrence used by the loop invariant to
track the final loop-variable binding. The three macro rules name exact
translated AST terms. These all satisfy the requested definition criterion;
none asserts an independent domain fact.

The two rules carrying `[simplification]` are precisely the guarded
`filterAccStrings` include/exclude recurrence equations at lines 39–48. Both
are `DEFINITION`, so the simplification-class restriction is satisfied.

### Operational rules

The iterator rules are ordinary execution steps over the supplied iterator
protocol. They form the same one-step observations as the native list rules:

- `strVals(.StrSeq)` normalizes to `.ValSeq`, for which native list iteration
  produces `#iterDone`; the auxiliary empty rule produces the same result.
- `strVals(ssCons(S, SS))` normalizes to
  `vCons(str(S), strVals(SS))`, for which native list iteration yields
  `str(S)` and `list(strVals(SS))`; the auxiliary nonempty rule yields exactly
  that pair.

The comparison rules likewise preserve the supplied semantics. Native
execution takes
`Compare(str(P), CmpOp("in", str(S)))` through `applyCmp("in", ...)` to
`strContains(P, S)`. The local dispatch preserves the continuation and
branches to exactly `true` or `false` under equality with that same total
Boolean. These rules change no heap, binding, stack, return, exception, or
other state cell. They are operational observations, not mathematical domain
lemmas.

### Domain and derived lemmas

No local rule is a domain lemma. The only mathematical filter equations define
the named summary used by the postcondition; they do not state a separate
theorem about an already-defined operation. The operational rules directly
advance or observe `<k>` execution.

No rule meets the stricter `PROVED_DERIVED_LEMMA` criterion. Stage 1 does not
first prove any exact inventory rule in a module excluding that rule and then
use it later. The two claims in `spec.k` are the loop invariant and end-to-end
reachability claim, not proof-local rewrite rules in the inventory.

The summary is relevant to the source and postcondition: it preserves input
order and appends exactly those strings for which the supplied
`strContains(P, S)` is true, matching the source loop and the final heap
postcondition. Since there is no claimed domain lemma, there is no irrelevant
domain obligation hidden by the classification.

## Producer and immutable-image provenance

I hashed the mounted generation-time producer sources before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The producer-source tree recomputes to
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
matching `/audit-input.json`.

The generator image ID is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest, the source manifest, and the immutable
producer-source path recorded by `/audit-input.json`. All three producer
entries are regular, non-symlink files. The detailed comparison is
`evidence/12-producer-provenance-comparison.json`. There is no producer-source
infrastructure mismatch.

## Recorded hashes and manifest bindings

An independent pass recomputed every mounted input/tree hash recorded by the
launcher and every Stage 4 binding used by the decision. The principal values
are:

| Artifact | Recomputed SHA-256 |
|---|---|
| Signed resolved-input object | `855fbc2aa7358492a535dbedc35d905d22940d3ce69a890323adc0aa614c0912` |
| Mechanical-checker lock | `5f2476d09635fc2f32625592bd667dd87a374068cd5b6610d9513ee6dacc066f` |
| Stage 1 pipeline tree | `390e0b2cabf348ed1a1c9fb3d815a73656bc2c32d8002c1be9f5704845fdf059` |
| Stage 1 deterministic-export tree | `31def40ff0657cae78c4b2f069ebd6732b688b180c138b3982cd94e65d95ed87` |
| Selected Stage 2 tree | `df261dd1405ba587d5cd887c91ef904930b5fdbf00a2ad6f83b3698a8ecc9298` |
| Stage 3 manifest | `aea7b06d72b9c4f57de3dd5b1ffa2896223fc3ae165e8d1b78e0a5d0de761246` |
| Stage 4 generation tree | `b80810be245076e1f72dfca9c2d5643f688afe5b959fbccebedab2da8bb2bd50` |
| Generated Lean project | `d993fd46a6ce4767dbe4203e25e1023242e37f18d423e2842b43710eb9cc830d` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `a4a5b499ac3e65672a3b8ce8ad090b8e5668402634f842c2989ffceccfa528a8` |

The complete Stage 1 regular-file set equals the launcher's recorded set, and
every individual Stage 1 source hash matches. The input manifest, generator
provenance, export result, stored preflight, and audit input all bind to the
recomputed Stage 1, Stage 3, generated-tree, obligation-map, and
trust-inventory values. The canonical hash of the complete signed `resolution`
object equals `resolved_input_sha256`. The launcher-owned mechanical-checker
lock file has the recorded hash, and every `/reference/tools` file named in
that lock has its locked hash. The pinned toolchain object also exactly equals
the generator manifest's toolchain object. All checks in
`evidence/39-recorded-hash-verification.json` are true.

## Deterministic Stage 4 generation

I reran the required trusted call:

```text
PYTHONPATH=/reference python -c \
  '... tools.klean_preflight.check_generation(
       Path("/reference/k-proof"),
       Path("/reference/lemma-discovery.json"),
       Path("/reference/klean-generation"),
       toolchain_lock=Path("/reference/klean-toolchain.lock.json"))'
```

The audit container initially exposed a PID-namespace/toolchain issue:
Lean 4.22 used the inner result of `getpid()` to access
`/proc/<pid>/exe`, while the mounted `/proc` exposed host PIDs. This made the
first copied-project `lake clean` report that Lake could not detect its
installation. Evidence of the failed attempt and diagnosis is preserved in
`evidence/13-rerun-klean-preflight.log` and
`evidence/14-toolchain-diagnosis.log` through
`evidence/30-proc-self-symlink.txt`.

I used a narrow preload shim under `/tmp/audit-work` which changes only
`getpid()` to return the host-visible PID obtained from `/proc/self`. It does
not modify the trusted tools, generated project, Lean source, build arguments,
or mounted inputs. With the pinned Lean sysroot and Lake source location
declared, the trusted preflight still executed its literal `lake clean` and
`lake build` commands on its own fresh temporary copy.

The successful rerun returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output hash
  `5cc095edde1ecbc5d857f11f37297f34a8a59abc01b4e860f23d21157ef57152`;
- obligation count 0;
- target `null`;
- generated-tree hash `d993fd46…830d`; and
- 47 generated executable trust declarations and zero designated sorries.

The complete successful command and returned evidence are in
`evidence/32-rerun-klean-preflight-success.log`. Its diagnostic output hashes
are byte-for-byte the same as the stored Stage 4 preflight.

### Obligation bijection and fixed target

The generated `obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

The independently classified `DOMAIN_LEMMA` ID sequence is empty, the Stage 4
input-manifest `source_rules` sequence is empty, and the generated obligation
ID sequence is empty. This is an exact ordered bijection with no omissions,
duplicates, extras, weakened obligations, irrelevant obligations, vacuous
conjuncts, or unbound parameters.

The fixed generated target is therefore absence of a target. The generator
manifest, stored preflight, audit input, trusted target parser, and a direct
scan of the Lean files all agree: there is no generated proposition
declaration. `Lemmas.lean` contains only imports, a comment, and an empty
namespace. Generating a theorem such as `True` would have been an impermissible
vacuous target change; no such theorem exists.

The mechanical and independent checks are recorded in
`evidence/36-obligation-map-target-and-trust.txt`,
`evidence/37-generated-declarations-search.txt`, and
`evidence/41-classification-generation-bijection.json`.

## Stage 5

Stage 5 proof checks are not applicable. The launcher mode is
`CLASSIFICATION_ONLY`, `stage5_result`, `lean_workspace`, and all Lean
candidate hashes are null, and `/candidate` is absent. This is the required
state for a legitimate `KLEAN_NO_OBLIGATIONS` generation. No clean candidate
build, `#print axioms Proof.final`, target-shadowing check, or
`target.parameters` operational-bridge audit can or should be performed.

## Evidence index

The primary reproducible records are:

- `evidence/00-audit-context.txt`: launcher mode, paths, and trusted toolchain;
- `evidence/05-reconstructed-rule-inventory.json`: all reconstructed spans,
  normalized hashes, IDs, and inventory hash;
- `evidence/07-stage3-bijection.json`: ordered Stage 3 identity comparison;
- `evidence/09-relevant-operational-semantics-full.txt`: supplied iterator,
  list, comparison, string, value, and loop semantics used for classification;
- `evidence/12-producer-provenance-comparison.json`: producer hashes and image
  identity;
- `evidence/32-rerun-klean-preflight-success.log`: exact successful trusted
  preflight call and result;
- `evidence/38-verify-recorded-hashes.py` and
  `evidence/39-recorded-hash-verification.json`: comprehensive independent
  hash/binding check;
- `evidence/40-classification-generation-bijection.py` and
  `evidence/41-classification-generation-bijection.json`: classification
  partition, simplification policy, obligation bijection, and null target; and
- `evidence/42-k-toolchain-versions.log`: live K tools at pinned version
  7.1.293.

VERDICT: PASS
LEGITIMACY: LEGIT
