# Adversarial audit: 114-minSubArraySum

## Audit result

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied semantics.  Clean reconstruction succeeds, the
claims constrain the result, the executed constructor term is mechanically the
regenerated program, and the sole operational bridge has first been proved
against a bridge-free definition over the bridge's complete context.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for one non-fatal
formalization limitation: the K postcondition defines the exact Kadane
recurrence, while the lemma equating that recurrence with the extensional
minimum over all non-empty contiguous index intervals is an ordinary
mathematical argument supported by extensive differential testing, not a
separate K theorem.  This does not narrow the HumanEval domain and does not
enable any false program result.

All build, mutation, and execution commands ran from copied sources in
`/tmp/audit-work/114-minSubArraySum`; no candidate compiled definition or cache
was reused.  Reviewer scripts, mutations, and bounded transcripts are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `114-minSubArraySum`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The trusted `/reference/reference-semantics` mount exists, so the rendered mode
and mounts agree.  There is no infrastructure breach.

I independently checked the launcher records as follows:

- `/audit-campaign-lock.json` is byte-hashed to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash in `/audit-input.json`, and its parsed JSON is exactly equal
  to the `audit_campaign` block.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt` are regular, readable, non-symlink
  files.  Every launcher-recorded single-file SHA-256 matches.
- `runtime-metrics.json` is absent.  That record is not required for
  `legacy-selected-stage1`; historical runtime observations must not be
  reconstructed.  The optional `usage.json` is present, inspected, and matches
  its recorded hash.
- The present legacy records `legacy-run-input.json` and
  `legacy-metrics.json` were also inspected and match the hashes recorded by
  `generation-result.json`.
- The structured trace consists of one regular JSONL file, whose recorded
  SHA-256 matches.  All 541 lines parse as JSON.  The parser found 103 function
  calls, 116 reasoning records, and eight agent messages.  The complete
  1,305,074-byte text transcript is valid UTF-8 with no NUL bytes.  These
  generation records were treated only as untrusted history.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts, with SHA-256 values
  `4bdb0afd53bc0e28529bafba0538d6b3a566ad5f476fb7f1016cfabe823f1c3f`
  and
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- Recursive, no-dereference comparison of candidate and trusted supplied
  semantics exits zero.  Both trees have exactly one directory and 24 regular
  files below the root, with the same paths and bytes; neither contains a
  symlink, special entry, missing entry, or extra entry.
- All required candidate proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh`) are regular non-symlink files.

Evidence: `evidence/stage1_integrity.sh`,
`evidence/stage1_integrity.log`, `evidence/trace_inventory.py`, and
`evidence/trace_inventory.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks `minSubArraySum(nums)` to return the minimum sum among
all non-empty contiguous subarrays of an integer array.  Its examples require:

- `[2,3,4,1,2,4] -> 1`;
- `[-1,-2,-3] -> -6`.

A meaningful result therefore requires a non-empty input.  This is also the
domain on which the trusted canonical implementation is defined: on `[]`,
canonical Python raises `ValueError` while the candidate raises `IndexError`.
There is no non-empty subarray on that boundary, so the differing exception
class does not remove a contract result.

The canonical code computes the negative of the maximum subarray sum after
negating elements.  The submitted code uses the equivalent Kadane recurrence:

```text
current  := min(value, current + value)
smallest := min(current, smallest)
```

It initializes `smallest` from `nums[0]` and folds the complete input.  This is
a different but correct algorithm.

### Trusted regeneration

Exact command:

```bash
python3 py2mpy.py solution.py > regenerated.mpy
cmp -s regenerated.mpy solution.mpy
```

Both commands exit zero.  Submitted and regenerated terms have the same
SHA-256:

```text
f1476cc2c62686c10e41dbc7811275b5f0340b82321e7d5188a356b1d8b8838d
```

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and submitted generated entry point, and also uses a separate
quadratic enumeration of all contiguous subarrays as a second oracle.  It
checks:

- both documented examples;
- 14 singleton, zero, sign-transition, tie, large-integer, and mixed boundary
  cases;
- every one of the 137,256 lists of lengths 1 through 6 over `[-3,3]`;
- 5,000 deterministic random lists of lengths 1 through 30 with elements in
  `[-10^12,10^12]`.

All 142,272 non-empty cases agree, with zero mismatches.  The generated corpus
exercises less-than, equality, and greater-than outcomes for both comparisons
in the submitted loop.  Exact command:

```bash
python3 /audit-output/evidence/differential_test.py
```

Exit status is zero.  Evidence: `evidence/stage2_fidelity.sh` and
`evidence/stage2_fidelity.log`.

## 3. Clean proof reconstruction

K `v7.1.293` and Python `3.10.12` were used (see
`evidence/toolchain.log`).  Only source files were copied to scratch.  There
were no `*-kompiled` directories before reconstruction.

| Purpose | Exact command | Fresh result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| Concrete harness | `krun concrete-tests.mpy --definition runtime-kompiled --output pretty` | exit 0; terminal `.K`, `NoExc`, exit code 0 |
| Bridge-free proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition verification-base-kompiled` | exit 0 |
| Loop theorem | `kprove spec.k --definition verification-base-kompiled --spec-module LOOP-SPEC --output pretty` | exit 0; `#Top` |
| Definition-loading theorem | `kprove spec.k --definition verification-base-kompiled --spec-module LOAD-SPEC --output pretty` | exit 0; `#Top` |
| Bridge-enabled definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| Function theorem | `kprove spec.k --definition verification-kompiled --spec-module FUNCTION-SPEC --output pretty` | exit 0; `#Top` |

The base definition contains 845 compiled rule-source entries and the full
definition 846; the additional entry is the loop bridge at
`verification.k:119`.  Thus `LOOP-SPEC` is not proved using the rule it is
intended to justify.

The compiler emitted warnings about non-exhaustive total functions in unused
string/float/builtin/out-of-bounds cases.  None of those symbols occurs in the
submitted term, claims, summaries, or residuals.

Evidence: all `evidence/stage3_*.log` files.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `LOOP-SPEC`: for any non-empty remaining integer sequence, any integer
   `current` and `smallest`, and an exact plain local frame containing
   `nums/smallest/current/value`, executing the real emitted loop body consumes
   the loop and leaves:
   - `current` equal to the `nextCurrent` fold;
   - `smallest` equal to the `kadaneSmallest` fold;
   - `value` equal to the last iterated integer;
   - `nums`, arbitrary surrounding scope entries, arbitrary continuation, and
     omitted cells unchanged.

2. `LOAD-SPEC`: from the initial module configuration, loading
   `Module(minSubArraySumDef)` installs the exact generated closure under the
   exact name `minSubArraySum`, while heap, stack, exception, return, and exit
   state remain clean.

3. `FUNCTION-SPEC`: for arbitrary `H:Int` and `T:IntSeq`, directly invoking the
   exact closure on `list(intVals(iCons(H,T)))` returns the exact integer
   `minSubArraySumSpec(iCons(H,T))` and restores the full initial configuration.
   The postcondition is an equality to that term, not an implication, free
   variable, or tautology.

The entry precondition is satisfiable, for example with `H=5`,
`T=.IntSeq`, the explicit empty global scope plus builtins, empty heap/stack,
`NoExc`, and exit code zero.

### Constructor-level program identity

The claim need not read a file at run time because it pins the closure
constructor directly.  I parsed both regenerated `solution.mpy` and
`Module(minSubArraySumDef)` with the fresh base definition and
`--expand-macros --output kore`.  `cmp` exits zero; both expanded files have
SHA-256:

```text
5d2ddbcad87c5128676acf9d66d57b8f73ff6bf0371f2e28edd605abd857ec45
```

The exact commands are recorded in `evidence/stage4_pinning.sh` and
`evidence/stage4_pinning.log`.

Three ground substitutions of the function theorem (`[5]`,
`[-1,-2,-3]`, and `[2,3,4,1,2,4]`) jointly produce `#Top`; their required
results `5`, `-6`, and `1` equal both Python implementations.

The formal domain is every finite non-empty list of mathematical integers.  It
has no fixed length, magnitude bound, bounded unrolling, or example-only
restriction.  K mathematical integers align with Python's unbounded integer
values for the used operations.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.py` enumerates every source-level declaration and
rule from the trusted supplied tree, candidate `verification.k`, and
`spec.k`.  Its output, `evidence/rule_inventory.log`, contains:

- 238 syntax declarations;
- 715 rules (474 equational and 241 operational);
- five contexts;
- one configuration;
- three claims;
- all 112 `total`, 48 priority, 35 concrete-only, 26 `owise`, 22
  no-evaluator/opaque, eight macro/macro-rec, and one simplification
  declaration/rule occurrences.

`evidence/static_assessment.md` gives the decision for every fixed-semantics
module, maps every constructor used by `solution.mpy` to its evaluation path,
and assesses all proof-local declarations/rules.  Important conclusions are:

- Used fixed rules preserve RHS-first assignment, left-to-right
  addition/comparison, one-time iterable evaluation, local binding, branch
  selection, frame creation/restoration, and exact integer behavior.
- The input is a bare read-only `list(intVals(...))`; no heap mutation,
  allocation, I/O, exception, builtin call, float, sort, digest, dict, set,
  range, or external state can influence the proof.
- `intVals` and the iterator priority rules are truthful structural
  specializations.  The `valSeqAt` simplification is exact head access at index
  zero.  Overlaps with fixed rules have identical results.
- `chooseSmaller` has disjoint/exhaustive integer guards.  All recursive
  summaries structurally descend.  `minSubArraySumSpec` is defined on exactly
  its used non-empty domain.
- The four macros are pure syntax expansions and mechanically match the
  generated constructor term.
- There are no proof-local opaque symbols or unconstrained result-bearing
  values.

### Operational bridge

The sole operational extension is the priority-30 loop summary.  Its
bridge-free connection theorem is `LOOP-SPEC`, whose LHS, guards, arbitrary
continuation, environment, exact local frame, framed scopes, omitted cells, and
RHS are identical to the rule's complete match domain.  It imports only
`VERIFICATION-BASE`, where that bridge is absent.

Its state footprint is limited to consuming the loop and updating the three
loop locals.  `nums`, additional scopes, continuation, heap, allocation
counters, stack, return state, exception, and exit code are preserved.

Two fresh sensitivity checks support the universal theorem:

- A continuation immediately following the loop assigns an observable
  `after=99`.  Both the bridge-free and bridge-enabled claims close with
  `#Top`, requiring the same final `smallest=-2`, `current=-2`, `value=-2`,
  and `after=99` for `[1,-2]`.
- A body mutation changed the executed macro from addition to subtraction.
  Its expanded term changed SHA-256 from `5d2d...ec45` to `6c13...b31b`.
  The bridge-free universal connection proof then exits 1 with
  `WarnStuckClaimState`.  The satisfying ground witness `[1]`, `current=0`,
  `smallest=1` reaches `current=-1, smallest=-1`, while the original summary
  requires `1,1`; that ground proof also exits 1 with the expected terminal
  mismatch.

Evidence: `evidence/continuation-sensitivity-spec.k`,
`evidence/stage5_continuation_*.log`,
`evidence/verification-body-mutation.k`,
`evidence/spec-body-mutation.k`,
`evidence/ground-body-mutation-spec.k`, and
`evidence/stage5_body_mutation_*.log`.

No unsound candidate rule was found.  Consequently there is no false
conclusion witness against a candidate rule; the body-mutation witness instead
demonstrates that the valid bridge is sensitive to the real body.

### Intent bridge

The theorem formally establishes the Kadane recurrence.  The standard
induction is:

- after an element `I`, every minimum-sum non-empty subarray ending at `I` is
  either `[I]` or extends the minimum ending at the previous element, hence
  `min(I,C+I)`;
- the minimum seen anywhere is the minimum of the previous best and that new
  ending minimum;
- seeding from the first element and folding the tail therefore equals the
  minimum over all non-empty contiguous subarrays.

This argument is sound ordinary integer mathematics, and the independent
canonical/brute-force results strongly support it.  However, the candidate
does not encode index intervals and prove this equivalence as a second K
claim.  That is the documented non-fatal concern.

## 6. Fresh non-vacuity test

I authored `evidence/spec-vacuity.k`, changing the function result obligation
to:

```k
minSubArraySumSpec(iCons(H, T)) +Int 1
```

This is false for the satisfying input `H=5`, `T=.IntSeq`: the actual and
originally claimed result is 5, while the mutation requires 6.

Build/parse command:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run --output pretty
```

It exits zero and emits a valid `kore-exec ... --prove ...` command, so the
negative result is not a parser/import/build failure.

Proof command:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --output pretty
```

It exits 1 with `WarnStuckClaimState` and the expected unmet equality:

```text
kadaneSmallest(T,H,H) +Int 1 #Equals kadaneSmallest(T,H,H)
```

The terminal configuration otherwise contains the original exact result and
restored cells.  This is meaningful non-vacuity evidence.  See
`evidence/stage6_vacuity_dry_run.log` and
`evidence/stage6_vacuity_kprove.log`.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied K semantics, for every finite non-empty `IntSeq`, the exact
submitted closure, when invoked from the specified clean configuration,
partially correctly returns the structurally defined Kadane fold and restores
caller-visible configuration state.  The loop summary itself is established
by symbolic execution of the exact emitted loop body without that summary
rule.  The exact module constructor also installs the exact closure.

This remains a partial-correctness result: it is not presented as a separate
termination theorem.

### Trust and evidence ledger

| Boundary | Effect on theorem | Assessment |
|---|---|---|
| K compiler, Haskell prover, LLVM runtime, and K builtin mathematical domains | Foundation of parsing, rewriting, and `#Top` | Standard unavoidable toolchain trust; exact version recorded. |
| Trusted supplied semantics | Defines the Python subset | Required benchmark boundary.  Candidate tree is exactly identical; every materially used rule was statically checked. |
| Trusted `py2mpy.py` | Bridges `solution.py` to constructor syntax | Acceptable: candidate translator is identical, regeneration is byte-identical, and expanded claim/program terms are identical. |
| K `Int`, `+Int`, and `<Int` | Numeric result and branches | Acceptable exact mathematical integers; matches used Python integer behavior. |
| Candidate recursive summaries | Affect loop locals and final result | Not opaque or assumed: terminating equations plus bridge-free `LOOP-SPEC` fix their execution values. |
| Recurrence equals extensional minimum contiguous-subarray sum | Connects formal result to human contract | Sound informal induction, not separately machine-checked; finite evidence is 142,272 zero-mismatch cases.  This is the reason for `CONCERNS`. |
| Trusted `canonical.py` and independent brute-force oracle | Empirical implementation/intent bridge | Finite evidence only, explicitly not a replacement for the K proof. |
| Unused opaque float, sort, and digest symbols in the supplied semantics | None | Inert: absent from every reachable term and postcondition. |

### Excluded behavior

- Empty input has no contract result and both Python implementations reject it;
  exception-class equivalence is not proved.
- Non-integer elements and non-list inputs are outside the HumanEval integer
  array domain and the K precondition.
- The supplied semantics is not a complete CPython semantics, but every
  material construct of this program is modeled and executed.

### Decision

The proof is sound, discriminating, body-sensitive, result-constraining, and
pins the real generated program over the full meaningful source-contract
domain.  It is therefore legitimate.  The informal recurrence-to-extensional
specification bridge is a documented non-fatal limitation under the benchmark
decision boundary, so the appropriate pairing is `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
