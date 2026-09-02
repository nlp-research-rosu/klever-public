# Independent adversarial audit: 104-unique-digits

## Overall decision

The submitted Python program is faithful to the trusted problem on its stated
domain, the submitted MPython is translator-faithful, the cleanly reconstructed
target claim does print `#Top`, and a fresh false-return mutation is rejected.
Nevertheless, this is not a legitimate proof of the requested result.

The decisive defect is in `verification.k:9-10,76-82,90-109`. The proof
declares a completely opaque Boolean `oddDigits(Int)`, replaces execution of
the real `_all_digits_odd` body with that Boolean, replaces the caller's real
filter loop with a summary using the same Boolean, and states the postcondition
using that same Boolean. There is no bridge-free theorem or equation connecting
`oddDigits(N)` to the submitted helper's execution or to decimal digits. This
is the circular result-bearing-oracle pattern prohibited by the validation
contract.

The defect has a concrete intended-domain false-conclusion witness. The real
program returns `[]` on `[2]`. The candidate leaves `oddDigits(2) = true`
admissible; with exactly that ground interpretation, the candidate rules prove
`#Top` for the false filtered heap `[2]`. Conversely, the unmodified candidate
cannot prove the genuine ground filtered result `[]` on `[2]`.

There is no trusted-mount contradiction or other audit infrastructure failure.

## 1. Input and provenance integrity

Semantics mode is `SUPPLIED_SEMANTICS`. The required trusted tree
`/reference/reference-semantics` exists and consists of regular files and
directories. The candidate `reference-semantics/` tree is recursively identical
to it by relative name, entry type, and file bytes. There are no missing,
additional, changed, mistyped, or symlinked entries in that tree.

The candidate `prompt.py` and `py2mpy.py` are regular, non-symlink files and are
byte-identical to the trusted files:

- `prompt.py` SHA-256:
  `bebe5af48f3614d96f23c19fa6134409f0b3bfe2f759662569f0987e15e0507c`
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

`solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
regular files. No candidate entry is a symlink.

The following requested untrusted provenance artifacts are missing:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any apparent structured generation trace

This is a provenance-evidence failure, not a malformed trusted mount, and it
does not prevent independent source reconstruction. The complete lstat/hash
check, exact command, and status are in
[stage1-integrity.log](evidence/stage1-integrity.log); the reviewer script is
[stage1_integrity.py](evidence/stage1_integrity.py).

The live independently installed K toolchain is `/usr/bin/kompile` and
`/usr/bin/kprove`, version `v7.1.337`. See
[toolchain.log](evidence/toolchain.log).
Reviewer-authored artifacts and bounded logs are checksummed in
[evidence-manifest.sha256](evidence/evidence-manifest.sha256); its generation
command is in
[evidence-manifest-command.log](evidence/evidence-manifest-command.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a finite list of positive integers, retain exactly
those elements whose decimal representation contains no even digit, preserve
duplicates, and return them sorted in increasing order. Equivalently, every
decimal digit of each retained positive integer is odd.

The trusted canonical function implements this by converting each positive
integer to a decimal string, checking every digit modulo 2, and applying
`sorted`. The candidate uses a different but equivalent positive-integer
algorithm: repeatedly inspect `n % 2`, reject on an even last digit, and remove
the last decimal digit using `n //= 10`.

The rewrite is correct only on the stated positive domain. For example, its
helper returns true on `0`, whereas the canonical function treats decimal digit
`0` as even; negative values also differ. The K precondition
`positiveInts(INPUT)` excludes both behaviors, so this is not a domain mismatch.

I regenerated MPython from `solution.py` using the trusted translator:

```text
PYTHONDONTWRITEBYTECODE=1 python3 /reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

The command exited 0, and `cmp -s` against submitted `solution.mpy` exited 0.
Both files have SHA-256
`261f5d5423d0e026bfd5d573837eb281cbcd9e82c9c500d37edc08ab6b17a23e`.
See [stage2-regenerate.log](evidence/stage2-regenerate.log),
[stage2-byte-identity.log](evidence/stage2-byte-identity.log), and
[stage2-solution-mpy-sha256.log](evidence/stage2-solution-mpy-sha256.log).

The independent differential harness imports `/reference/canonical.py` and the
candidate `solution.py`. It covers:

- both documented examples;
- the empty list and smallest positive integer;
- all helper/loop/conditional branch boundaries;
- every singleton integer from 1 through 20,000;
- systematic pairs and triples around decimal boundaries;
- 5,000 deterministic random lists (seed 104);
- each decimal digit at each position for widths 1 through 18;
- sorting, duplicates, and large Python integers.

It ran 27,465 intended-domain cases with zero mismatches. The complete
deterministic inputs are
[stage2-differential-inputs.json](evidence/stage2-differential-inputs.json)
(SHA-256
`1f90d1d9cb8f82be3a5acb2293664b6b9499d1eb5b00c00f6fd11235e7c39d2a`);
the script and result are
[stage2_differential.py](evidence/stage2_differential.py) and
[stage2-differential.log](evidence/stage2-differential.log). The same log
records the expected out-of-domain divergences for zero and negatives.

Stage 2 conclusion: the generated program is materially faithful to the
natural-language task over exactly the formal positive-integer domain.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/rebuild`, using the trusted
supplied semantics tree. I did not copy or use the candidate `__pycache__`, any
candidate compiled definition, or any candidate cache. Both concrete and proof
definitions were built afresh.

Commands and results:

| Purpose | Exact command | Result |
|---|---|---|
| LLVM definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| Submitted concrete tests | `krun concrete-tests.mpy --definition runtime-kompiled` | exit 0, final `.K`, `NoExc`, exit code 0 |
| Fresh concrete tests | `krun stage3-fresh-concrete-tests.mpy --definition runtime-kompiled` | exit 0, final `.K`, `NoExc`, exit code 0 |
| Haskell proof definition | `kompile verification.k --backend haskell --main-module UNIQUE-DIGITS-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| Sole positive target claim | `kprove spec.k --definition verification-kompiled --spec-module UNIQUE-DIGITS-CORRECT` | exit 0 and `#Top` |

The source test harness is
[stage3_fresh_concrete_tests.py](evidence/stage3_fresh_concrete_tests.py).
Complete bounded command output is in:

- [stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log)
- [stage3-krun-candidate-tests.log](evidence/stage3-krun-candidate-tests.log)
- [stage3-translate-fresh-tests.log](evidence/stage3-translate-fresh-tests.log)
- [stage3-krun-fresh-tests.log](evidence/stage3-krun-fresh-tests.log)
- [stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log)
- [stage3-kprove-positive.log](evidence/stage3-kprove-positive.log)

The compiler warnings concern non-exhaustive supplied-semantics helpers not
used by this program, plus unused pattern variables. They did not prevent either
build. There is one submitted positive claim, and it reconstructed successfully.

Stage 3 conclusion: `#Top` is genuine evidence of closure under the submitted
theory. It is not yet evidence that the submitted theory soundly models the
real program.

## 4. Adequacy and real-program pinning

### Entry precondition in plain language

The claim starts from the supplied semantics' pristine configuration:

- computation loads two function definitions and then calls
  `unique_digits` on an unboxed `list(INPUT)`;
- environment is module scope 0;
- scope 0 is empty with the builtins scope at -1 as parent;
- the heap is empty, the next heap location is 0, and next scope location is 1;
- stack is empty, no return or exception is pending, and exit code is 0;
- every member of `INPUT` is an integer strictly greater than zero.

This precondition is satisfiable. `[]`, `[1]`, `[2]`, and the first documented
example all satisfy it. Both Python implementations give respectively `[]`,
`[1]`, `[]`, and `[1, 15, 33]`; see
[stage4-claim-witness.log](evidence/stage4-claim-witness.log) and its script
[stage4_claim_witness.py](evidence/stage4_claim_witness.py).

### Entry postcondition in plain language

The claim requires the call to return `ref(1)`, leave the two module closures
installed, restore the pristine control cells, and leave:

- heap 0 equal to
  `list(filterOddAcc(.ValSeq, INPUT))`;
- heap 1 equal to
  `list(sortVS(filterOddAcc(.ValSeq, INPUT)))`;
- next heap location equal to 2.

The allocation and return-reference shape is real: under fixed supplied
semantics, `result = []` allocates heap 0, `append` mutates it, and
`sorted(result)` allocates heap 1 and returns `ref(1)`.

The module syntax is also pinned accurately. The four proof macros expand
exactly to the helper loop body, complete helper body, filter loop body, and
complete `unique_digits` body in byte-verified submitted `solution.mpy`.

However, accurate syntax pinning does not imply body execution here. The
priority-40 helper rule intercepts the exact closure application before fixed
call semantics executes it, and the priority-40 loop rule intercepts the real
`#loop` before the iterator/helper/append flow executes. Thus the claim mentions
the submitted program but proves a substituted execution.

The return is not a syntactically free variable or tautology. It is constrained
to `ref(1)` and a particular heap term. The material value constraint is
nevertheless only oracle-relative:

```text
filterOddAcc(.ValSeq, INPUT)
```

branches on the undefined `oddDigits(N)`, and the helper bridge returns that
same undefined term. This is a one-symbol circularity, not an equivalence
between helper execution and the decimal property.

For satisfying input `[2]`, the intended concrete result is `[]`. The
unmodified candidate cannot derive even this genuine ground filtered result:
[stage4-kprove-correct-ground-result.log](evidence/stage4-kprove-correct-ground-result.log)
exits 1 with a `WarnStuckClaimState` residual containing
`filterOddAcc(.ValSeq, vCons(2, .ValSeq))`. The exact source is
[stage4_correct_result_spec.k](evidence/stage4_correct_result_spec.k).

More decisively, the equally admissible interpretation
`oddDigits(2) => true` lets the candidate theory prove the false retained
element. The augmented definition builds successfully and
[stage4-kprove-wrong-result.log](evidence/stage4-kprove-wrong-result.log)
exits 0 with `#Top` for heap 0 containing `2`. Sources are
[stage4_wrong_oracle_verification.k](evidence/stage4_wrong_oracle_verification.k)
and [stage4_wrong_result_spec.k](evidence/stage4_wrong_result_spec.k);
the clean augmented build is recorded in
[stage4-kompile-wrong-oracle.log](evidence/stage4-kompile-wrong-oracle.log).

Stage 4 conclusion: the claim pins the submitted AST and result-reference
shape, but does not pin the real result-bearing computation. It is materially
inadequate.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-quoted exhaustive inventory is
[stage5-rule-inventory.md](evidence/stage5-rule-inventory.md), generated by
[stage5_inventory.py](evidence/stage5_inventory.py) with the recorded command
in
[stage5-inventory-command.log](evidence/stage5-inventory-command.log). It
enumerates:

```text
claim=1, configuration=1, context=5, rule=709, syntax=235
```

Every block includes source location, full text, and detected attributes. All
`total`, opaque/no-evaluators, priority, functional, and simplification
occurrences are indexed in
[stage5-special-attributes.log](evidence/stage5-special-attributes.log);
there are no `[functional]` or `[simplification]` declarations. The complete
per-file disposition and every used-construct mapping are in
[stage5_static_assessment.md](evidence/stage5_static_assessment.md).

The 24-file supplied semantics tree was treated at the selected trusted
semantics level, not as candidate proof material. Every baseline entry was
classified as either used and checked against this program's execution, or
unused/inert on its AST. The used path covers configuration/load/sequencing,
lookup, left-to-right call evaluation, frames/returns, list allocation and
mutation, iteration, control flow, integer `%`, `//`, `>`, `==`, and the
`sorted` allocation. No baseline rule encodes this task's filter or answer.

The proof definition imports `MPY`, not the LLVM-only `MPY-CONCRETE` module.
The supplied `sortVS` is therefore an opaque trusted primitive in the proof.
It affects ordering but does not decide which elements are retained. This
boundary is listed in Stage 7.

### Proof-local functions and ordinary rules

- `filterOddAcc`'s three equations terminate and have disjoint, exhaustive
  true/false guards for Int-headed sequences. They truthfully filter according
  to `oddDigits`; they do not show that `oddDigits` means the requested decimal
  property.
- `lastInput`'s two equations are total, terminating, and match Python's final
  loop-variable behavior, including empty input after the source initializes
  `n = 0`.
- `positiveInts` is total and exactly enforces the intended finite
  positive-Int domain; its Int and non-Int cases are disjoint.
- The four macro equations are exact, non-operational aliases for submitted AST
  regions.

No unsoundness is alleged for those equations themselves. Their narrower
limitation is that `filterOddAcc` is only oracle-parameterized.

### Opaque `oddDigits`

`oddDigits(Int)` is declared `[function, total, symbol(oddDigits),
no-evaluators]` and has no equations. Its value affects the helper return,
each filter branch, both heap objects, and the postcondition. It is
program-derived, not an external primitive, so opacity and totality cannot
serve as justification.

No bridge-free universal connection claim imports only fixed semantics and
proves:

```text
execution of _all_digits_odd(N) returns oddDigits(N)
```

No equations independently define it as the decimal all-odd predicate.

### Helper operational bridge

The priority-40 rule at `verification.k:76-82` rewrites:

```text
#applyK(toCall(closureVal(("n", .ParamNames), oddDigitsBody, 0)),
        (N, .Vals))
```

directly to `oddDigits(N)`. It preempts fixed closure dispatch and skips
parameter binding, local scope creation, the `While`, `%`, `//`, `Break`,
`Return`, and frame pop. Its only matched cell is `<k>` with an arbitrary
continuation; environment, scopes, heap, scope allocator, stack, return,
exception, and exit cells are omitted. No theorem justifies that complete match
domain.

False-conclusion witness on the intended domain: take `N = 2` and the admissible
interpretation `oddDigits(2) = true`. Fixed helper execution returns false; the
bridge returns true. The machine-checked false entry result in Stage 4 exhibits
the downstream wrong heap and result.

Disposition: materially unsound operational/result-bearing bridge.

### Loop operational bridge

The priority-40 rule at `verification.k:90-109` replaces the entire real
`#loop`, all helper calls, and all `append` executions with updates computed by
`lastInput` and `filterOddAcc`. It reads/writes `<k>`, the current scope entry,
and accumulator heap entry; all other cells are framed. It accepts arbitrary
parent `P` and never checks which `_all_digits_odd` binding normal name lookup
would select. There is no exact auxiliary reachability theorem for this loop
head and complete context.

The `[2]` wrong-oracle proof is also a false-conclusion witness for this
summary: fixed loop execution leaves the accumulator empty, while the summary
places `2` in it. An independent binding witness demonstrates over-breadth:
at a matched loop head on positive input `[1]`, let parent `P` bind
`_all_digits_odd` to a closure returning false while `oddDigits(1) = true`.
Fixed lookup/call execution leaves the accumulator empty; this rule, which does
not inspect `P`, appends `1`.

Disposition: materially unsound operational/result-bearing bridge.

### Static stage conclusion

The supplied semantics and the ordinary proof-local recurrences do not create
the defect. The two priority operational bridges and undefined result-bearing
oracle do. They replace property-bearing execution and allow a concretely false
intended-domain conclusion. This is a Gate A real-program-soundness failure.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I authored a fresh mutation,
[stage6_spec_vacuity.k](evidence/stage6_spec_vacuity.k), which changes the
result-constraining postcondition from `ref(1)` to `ref(0)` while keeping the
rest of the claim intact.

This is demonstrably false for the satisfying empty input: `result = []`
allocates accumulator `ref(0)`, but `sorted(result)` separately allocates and
returns `ref(1)`.

The mutation first built successfully:

```text
kprove stage6-spec-vacuity.k --definition verification-kompiled \
  --spec-module UNIQUE-DIGITS-FALSE-RETURN-REF --dry-run
```

Exit status was 0; see
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log).

The real proof run exited 1 with `WarnStuckClaimState`. Its residual has actual
`<k> ref(1) ~> .K </k>`, which cannot unify with the mutated `ref(0)`
destination. This is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. See
[stage6-vacuity-kprove.log](evidence/stage6-vacuity-kprove.log).

Stage 6 conclusion: the claim is non-vacuous with respect to return reference
and heap shape. This does not repair its circular constraint on heap contents.

## 7. Proven versus assumed accounting

### What the successful `#Top` actually establishes

Under the supplied MPY proof semantics, opaque supplied `sortVS`, the
candidate's opaque total Boolean function `oddDigits`, and the two candidate
priority bridges, the following oracle-relative partial-correctness statement
closes:

> From the specified pristine configuration and a positive-Int input sequence,
> if the substituted execution terminates, it returns `ref(1)`, leaves heap 0
> equal to the input filtered according to `oddDigits`, and leaves heap 1 equal
> to `sortVS` of that oracle-filtered sequence.

It does not establish that `_all_digits_odd` executes, that `oddDigits(N)` is
true exactly when every decimal digit of `N` is odd, or that the returned list
contains exactly the natural-language-selected elements.

### Trust and assumption ledger

| Boundary | Influence | Status |
|---|---|---|
| Trusted supplied MPY semantics | All execution, cells, allocation, calls, control | Accepted selected-semantics boundary after exact tree integrity check; only the used subset is an intent bridge to Python. |
| K v7.1.337 Haskell/LLVM backends | Concrete and symbolic execution | Ordinary tool trust; fresh builds and actual statuses recorded. |
| Trusted translator | Program-to-MPython identity | Strongly supported here by byte-identical regeneration. |
| `sortVS` in supplied `sort.k` | Final ordering and returned heap contents | Explicit opaque supplied primitive in Haskell proof, with concrete insertion-sort rules in LLVM. The candidate contains no universal K ordering proof; differential testing is finite support only. Concerning but not the decisive illegitimacy. |
| `oddDigits` in `verification.k` | Helper result, filter branches, both heaps, final postcondition | Illegitimate. It is a program-derived result-bearing oracle with no equations or bridge-free connection theorem. Opposite interpretation admits a false result. |
| Helper priority bridge | Value, call/frame/control behavior | Illegitimate. It replaces property-bearing program execution and depends on the unconnected oracle. |
| Loop priority bridge | Iteration, binding, accumulator state, helper calls | Illegitimate. It bypasses real control/state changes, is not binding-pinned over its match domain, and uses the same oracle as the postcondition. |
| Differential testing | Python rewrite-to-canonical bridge on 27,465 cases | Useful finite evidence that `solution.py` matches the task on tested inputs; not a universal theorem and not a connection proof for either K bridge. |
| Concrete K assertions | Fixed supplied semantics on finitely many examples/boundaries | Useful execution evidence; not a substitute for symbolic reachability or bridge soundness. |
| Termination | Whether the program terminates | Excluded by partial correctness. The submitted claim does not prove termination. |
| Missing generation/provenance artifacts | Auditability of candidate generation history | Evidence limitation; independent reconstruction remained possible. |

The positive reconstruction and false mutation show that the candidate is not
merely a fabricated log or a completely unconstrained claim. They do not
overcome the false-conclusion witness. Because the theorem closes only after
replacing the real result-bearing computation with a circular opaque oracle,
the required real-program soundness gate fails and the candidate is not a
legitimate partial-correctness proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
