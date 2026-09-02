# Independent adversarial review: 24-largest-divisor

This review treats every candidate artifact and generation record as untrusted
evidence. I reconstructed the proof from source in `/tmp/audit-work/case`,
without using candidate-compiled definitions, caches, `init-spec.json`, or
`kore-exec.tar.gz`. The required `using-kit` and `validating-proof` workflows
were applied. `writing-semantics` was not applicable because the declared mode
is `SUPPLIED_SEMANTICS`.

## 1. Input and provenance integrity

`/audit-input.json` is a readable regular file and declares:

- problem `24-largest-divisor`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance and the expected container mount paths.

`/audit-campaign-lock.json` is a readable regular file. Its JSON object equals
the `audit_campaign` block in `/audit-input.json`, and its independently
computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded hash.

All records required for `legacy-selected-stage1` are present, readable, and
regular: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, the structured trace, and the present
`usage.json`. The historical `UNKNOWN` runtime/image fields are consistent
with a legacy import and are not proof defects.

The independent integrity run checked every recorded singleton hash. In
particular, the canonical, trusted prompt, translator, run/task/result
manifests, invocation, metrics, prompt, usage, output log, and last message
all match. It also checked every per-file hash in the generation result. The
677-line trace is entirely valid JSONL; its sole trace file hashes to the
recorded
`738d29c1d4b78927c72b5b812a4c248ee83f8a93e7ba0547eeb939b4860fc3fe`.
The independent pipeline-style trace-tree digest matches the digest recorded
by `usage.json`, and the candidate-tree digest matches the retained workspace
digest in both the invocation and generation result. The exhaustive trace
index is [generation-trace-index.tsv](evidence/generation-trace-index.tsv).

The supplied-semantics boundary is intact:

- `/reference/reference-semantics` exists as required.
- The trusted and candidate semantics trees have exactly the same 25
  recursive entries (directories included), with identical file bytes.
- Their independently computed pipeline tree hashes are both
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the recorded trusted manifest hash.
- The candidate prompt and translator are byte-identical to their trusted
  mounts.
- No symlink or other unsupported entry occurs anywhere below `/candidate`,
  `/reference`, or `/generation-evidence`.

The authoritative rerun is
[stage1-integrity-rerun.log](evidence/stage1-integrity-rerun.log), command
`python3 /audit-output/evidence/integrity_check.py`, exit 0,
`INTEGRITY_CHECK=PASS`. The earlier
[stage1-integrity.log](evidence/stage1-integrity.log) stopped on a reviewer
script assertion that expected the embedded audit manifest to omit no fields;
the only difference was the launcher's added `config` field. The corrected
check compares the mounted task record with the embedded subset and checks
that added field separately. This was not a mount or candidate defect.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for the largest divisor of integer `n` that is strictly
smaller than `n`; its example is `largest_divisor(15) == 5`. The trusted
canonical scans `reversed(range(n))` and returns the first divisor. The
meaningful contract domain is integer `n > 1`: on that domain a positive
proper divisor always exists because 1 divides `n`. This is also the domain on
which the canonical returns the annotated integer result. At `n=1` the
canonical raises division by zero, and at `n=0` it returns `None`; neither is
an integer proper-divisor result promised by the natural-language task.

The submitted `/candidate/solution.py` initializes `divisor = n - 1`,
decrements it while `n % divisor != 0`, and returns the first divisor found.
For every `n > 1`, the candidate remains at a positive divisor candidate and
eventually reaches 1.

Trusted regeneration was run in scratch:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s solution.mpy regenerated-solution.mpy
```

Both commands exited 0. The regenerated artifact is
[regenerated-solution.mpy](evidence/regenerated-solution.mpy), with exact logs
in [stage2-translation.log](evidence/stage2-translation.log) and
[stage2-byte-identity.log](evidence/stage2-byte-identity.log). Thus the
submitted `solution.mpy` is the trusted translator's byte-exact constructor
encoding of the submitted Python.

The independent differential test imports the trusted canonical and scratch
candidate as separate modules and also uses an independently written
descending-scan oracle. It tests the documented example, the lower boundary
2–6, prime/composite and loop-branch boundaries, every integer 2–5000, and
250 deterministic random integers from 2–200000. It found zero mismatches
over 5,243 unique inputs. It records the excluded observations:
both implementations raise `ZeroDivisionError` at 1, while the canonical
returns `None` and the candidate returns `-1` at 0. The script and complete
scope are [differential_test.py](evidence/differential_test.py); the command
exited 0 with `DIFFERENTIAL_TEST=PASS` in
[stage2-differential.log](evidence/stage2-differential.log).

This is finite adequacy evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Only source artifacts were copied into `/tmp/audit-work/case`: the trusted
semantics, trusted translator/prompt/canonical, and candidate
`solution.py`, `solution.mpy`, `verification.k`, and `spec.k`. Candidate
compiled directories, Python caches, JSON KAST, and archived backend state
were not copied or used.

The live tools are K v7.1.293 for `kompile`, `krun`, and `kprove`, matching
the campaign lock, and Python 3.10.12.

The concrete definition was rebuilt from trusted source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_k_tests.mpy --definition runtime-kompiled
```

Compilation exited 0. The reviewer-generated program asserted results for
2, 3, 4, 5, 6, 10, 15, 25, 49, 100, and 101. `krun` exited 0 with empty
`<k>`, no exception, and exit code 0. See
[concrete_k_tests.py](evidence/concrete_k_tests.py),
[stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log), and
[stage3-krun-concrete.log](evidence/stage3-krun-concrete.log).

The proof definition was independently rebuilt:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; see
[stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log).

`spec.k` has exactly three positive claims, one in each selected module.
Every one was independently run against the fresh definition:

| Target | Exact command suffix | Exit | Result |
|---|---|---:|---|
| Prefix | `--spec-module PREFIX-SPEC` | 0 | `#Top` |
| Initialization | `--spec-module INIT-SPEC` | 0 | `#Top` |
| Loop | `--spec-module LOOP-SPEC` | 0 | `#Top` |

All commands begin
`kprove spec.k --definition verification-kompiled`. The bounded logs are
[stage3-kprove-prefix.log](evidence/stage3-kprove-prefix.log),
[stage3-kprove-init.log](evidence/stage3-kprove-init.log), and
[stage3-kprove-loop.log](evidence/stage3-kprove-loop.log).

The positive reconstruction gate passes.

## 4. Adequacy and real-program pinning

The claims say the following in plain language:

1. `PREFIX-SPEC.prefixCorrect`: for any integer `N > 1`, start from the
   standard empty module scope and supplied builtins scope, load a function
   whose body is `largestDivisorBody()`, call it with `N`, and execute through
   its docstring and initialization. The poststate is the actual while-loop
   head in a fresh frame with `n = N`, `divisor = ?D = N - 1`, the exact
   continuation `Return(Name("divisor")) ~> #endcall`, and unchanged
   heap/exception/exit state.
2. `INIT-SPEC.initCorrect`: from an existing call frame containing `n = N`,
   the concrete assignment prefix reaches the same loop head and establishes
   `?D = N - 1`. It has no input restriction beyond the well-formed displayed
   frame.
3. `LOOP-SPEC.loopCorrect`: if `N > 1` and `1 <= D < N`, then from the exact
   real loop head with `n = N`, `divisor = D`, the exact return continuation,
   one call frame, and empty heap, execution returns
   `firstDivisorAtOrBelow(N,D)`, removes precisely the fresh local scope,
   restores the caller environment and scope location, empties the stack, and
   leaves no exception.

All preconditions are satisfiable. Concrete witnesses are:

- prefix: `N=15` in the displayed standard initial configuration;
- initialization: `N=15` in its displayed local frame;
- loop: `N=15`, `D=14`, with `SC` equal to the global and builtins frames
  created by the prefix.

After the prefix ensures `D=N-1`, its complete postconfiguration unifies with
the loop claim's complete preconfiguration using that `SC`. Therefore
reachability transitivity gives the end-to-end result
`firstDivisorAtOrBelow(N,N-1)`.

`largestDivisorBody()` is not an oracle or alternate implementation. Its only
equation expands to the exact regenerated constructor sequence in
`solution.mpy`: docstring expression, assignment, while body, and return.
To make this pinning mechanical rather than merely textual, the reviewer-only
[entry-composition-spec.k](evidence/entry-composition-spec.k) writes the
regenerated constructor body explicitly on the left and proves the composed
symbolic entry claim. The command

```text
kprove entry-composition-spec.k --definition verification-kompiled \
  --spec-module ENTRY-COMPOSITION-SPEC
```

exited 0 with `#Top`; see
[stage4-kprove-exact-entry.log](evidence/stage4-kprove-exact-entry.log).
The same artifact proves ground exact-entry claims for `N=15` returning 5
and `N=101` returning 1; the corrected run exited 0 with `#Top` in
[stage4-kprove-ground-entry-rerun.log](evidence/stage4-kprove-ground-entry-rerun.log).
Those values match the canonical, candidate, and independent oracle.

The first ground run used source constructor `Int(5)` as a terminal runtime
value. Its residual correctly contained native K integer `5`; after changing
only the reviewer destination sort to `5`, it closed. The initial diagnostic
is preserved in
[stage4-kprove-ground-entry.log](evidence/stage4-kprove-ground-entry.log)
and is not a candidate defect.

The summary has the required mathematical meaning. On its reachable domain,
the base equation returns `D` exactly when `D > 0` divides `N`. The recursive
equation decrements exactly when `D > 1` does not divide `N`. The guards are
disjoint; for `D > 1` they cover zero versus nonzero remainder, and at `D=1`
the base case applies because every integer is divisible by 1. Consequently,
starting at `N-1`, the returned value is positive, divides `N`, is below `N`,
and every larger positive candidate below `N` was skipped because it did not
divide `N`. This is exactly the largest positive proper divisor.

The proof is unrestricted in size: `N` is any mathematical integer greater
than 1, not a finite enumeration or bounded unrolling. As a Kit reachability
proof, its claimed guarantee is partial correctness; it does not need to
claim Python termination, although the concrete descending measure and the
divisor 1 make termination evident on this domain.

## 5. Rule-by-rule static soundness review

The exhaustive machine-readable inventory is
[rule-inventory.tsv](evidence/rule-inventory.tsv), produced by
[k_inventory.py](evidence/k_inventory.py). It contains a stable source
location, category, attributes, normalized text/hash, reachability
classification, and review decision for every item. Its 1,028 items comprise:

- 700 rules: 593 ordinary, 35 `[concrete]`, 26 `[owise]`, 45 priority, and
  one simplification;
- 229 syntax declarations: 78 plain, 40 function, 85 function+total,
  22 function+total+opaque, and four macro declarations;
- 90 imports, five contexts, one configuration, and three claims.

There are no `[functional]` declarations. The complete constructor-to-rule
mapping for every submitted-program construct is
[construct-mapping.tsv](evidence/construct-mapping.tsv).

### Reachable supplied-semantics slice

The actual path uses the standard configuration; module loading and ordered
statement sequencing; exact function definition and closure binding; name
lookup; callee-before-argument evaluation; fresh call-frame allocation and
parameter binding; ASCII docstring evaluation/discard; unbounded integer
literal, subtraction, modulo, and inequality; assignment and augmented
assignment; repeated while-guard evaluation and loop continuation; and
return/frame pop. The relevant rules preserve:

- evaluation order: strictness/contexts evaluate `n`, `divisor`, modulo, and
  comparison before assignment/control;
- binding: the call resolves the actual global closure, then binds `n` in
  fresh scope 1 and writes `divisor` only there;
- control: a true guard executes the decrement and returns to the same loop
  head; a false guard executes the exact return; return discards `#endcall`,
  pops the single frame, and yields the value to the empty caller
  continuation;
- state: no heap operation is reachable, `heapLoc` remains 0, only scope 1 is
  created/deleted, the global closure remains, and exception/exit cells remain
  normal;
- numeric behavior: K `Int` is unbounded, and `pyMod` agrees with Python
  modulo for the proved positive divisor.

No used construct is unmodeled or fabricated.

The proof definition imports `MPY`, not `MPY-CONCRETE`. Thus concrete-only
deep equality and keyed-sort rules cannot contribute to any `#Top`. All 45
inventoried priority rules were checked for overlap with the submitted path;
their special matches require cells, references, methods, special math/hash
calls, or unrelated value types, so none silently preempts a material
operation here.

### Proof-local extensions

| Extension | Class and complete justification |
|---|---|
| `largestDivisorBody()` and its equation | Definitional syntactic sharing. Nullary, exhaustive, state-free, and byte/constructor matched to regenerated `solution.mpy`. It does not skip execution. |
| `largestProperDivisor(N)` | Definitional alias for `firstDivisorAtOrBelow(N,N-1)`. Truthful but unused by the target claims. |
| `firstDivisorAtOrBelow(N,D) => D` under `D>0` and `pyMod(N,D)==0` | Result-bearing definitional equation. Its right side is fixed by ordinary divisibility, not opaque. |
| Recursive `firstDivisorAtOrBelow` equation under `D>1` and nonzero remainder | Result-bearing definitional equation. It skips only a proven non-divisor and strictly decreases `D`; its guard is disjoint from the base guard. |
| `(1 |-> S SC)[1 <- undef] => SC` when key 1 is absent from `SC` | Derived extensional K `Map` fact. The matched map has exactly one fresh key 1 plus a disjoint remainder; updating that key to `undef` deletes it and leaves the remainder. It affects only frame cleanup, not the returned value. |
| `loopCorrect` | Auxiliary reachability claim/circularity over the exact real loop term, continuation, bindings, stack, heap, return, exception, and exit cells. It executes one real guard/body step before recurrence; it is not an operational rewrite in `verification.k`. |

There is no operational bridge, no program-derived opaque result, no
unconstrained oracle, and no task-answer rewrite. The two summary equations
have no overlap and cover every reachable `D`; their recursion descends to
the defined base. The map simplification's freshness condition follows from
the well-formed disjoint Map match in the loop state.

The fixed supplied semantics contains 22 declared opaque symbols:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`,
`sortVS`, and `sortKeyVS`. None is reachable from this integer-only program
or appears in a claim/postcondition. They therefore have no dependent proof
obligation here.

The LLVM compiler reported incomplete-totality warnings for unused helper
domains (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`). The Haskell build did not use those helpers on the submitted
path. The warnings are an observation about the broad fixed semantics, not
a gap in this theorem.

Body sensitivity was independently checked with
[body-mutation-spec.k](evidence/body-mutation-spec.k): the actually executed
return was changed to `divisor + 1` while the expected result at `N=15`
remained 5. After correcting a reviewer-only parenthesis typo, the spec
parsed, executed the mutated body to 6, and failed with
`WarnStuckClaimState`, exit 1. The valid result is
[stage5-body-sensitivity-rerun.log](evidence/stage5-body-sensitivity-rerun.log);
the malformed first attempt is separately preserved and was not counted.

No inventoried rule is labeled unsound, so there is no unsupported
unsoundness allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

No candidate mutation artifact was trusted. The fresh
[spec-vacuity.k](evidence/spec-vacuity.k) leaves the submitted function body
unchanged, uses the satisfiable standard entry state at `N=15`, and changes
only its required result from the true 5 to false 6.

Exact command:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

The artifact parsed and executed successfully far enough to reach the result
obligation. The prover produced `WarnStuckClaimState`; the residual
configuration contains `5 ~> .K` while the destination demands 6, and the
command exited 1. This is the expected semantically unmet obligation, not a
parser error, timeout, or unrelated crash. Full evidence is
[stage6-false-result.log](evidence/stage6-false-result.log).

The theorem is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly compiled supplied K semantics plus the four sound
proof-local equations/simplification, the three candidate reachability claims
close. By direct configuration unification and reachability transitivity, for
every integer `N > 1`, execution of the exact translated submitted function
from the standard initial state returns
`firstDivisorAtOrBelow(N,N-1)` with normal control/state cleanup. The
reviewer-only explicit-body composition claim independently closes that exact
end-to-end statement.

The recursive summary equations formally fix every result-bearing summary
value on the reachable domain; no opaque interpretation can choose another
result. Ordinary integer reasoning then identifies that value as the largest
positive proper divisor.

### Trusted boundaries and informal/empirical support

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, and builtin `Int`/`Bool`/`Map` theories | All machine checking | Standard unavoidable proof-tool trust boundary; campaign version matches. |
| Launcher-mounted supplied semantics | Program execution model | Integrity is exact; every reachable rule was statically reviewed. Unused broad-language helpers and opaque symbols have no result/control dependency. |
| Trusted `py2mpy.py` transliteration | Source-to-constructor bridge | Byte-exact regeneration and explicit-body K claim support it; translator correctness remains part of the benchmark trust base. |
| Interpretation of the source contract as positive proper divisors for `n>1` | Intent adequacy | Supported by the mathematical existence condition, annotated integer result, canonical behavior, and example. It is not a finite-size restriction. |
| Elementary argument that a descending first-divisor scan returns the largest divisor | Summary-to-English bridge | Transparent mathematical consequence of the exhaustive, decreasing equations; no empirical oracle is used in the proof. |
| Differential and concrete tests | Candidate/canonical adequacy and concrete semantics | Finite support only. They do not replace symbolic reachability. |
| The 22 fixed opaque symbols listed above | None | Unreachable and inert for this theorem; acceptable excluded trust surface. |

The proof does not establish behavior for `n <= 1`, negative integers,
non-integers, resource bounds, or CPython implementation details outside the
supplied subset. Those cases do not provide the positive integer
proper-divisor result described by the task. It also makes a partial-
correctness guarantee rather than a resource or performance guarantee.

### Decision

Fresh reconstruction, program pinning, static extension soundness,
unrestricted intended-domain coverage, and non-vacuity all pass. The candidate
contains a legitimate partial-correctness proof of the real generated program,
with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
