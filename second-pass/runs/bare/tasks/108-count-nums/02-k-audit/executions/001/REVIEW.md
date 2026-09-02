# Independent adversarial audit: 108-count-nums

## Audit outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof under its generated K semantics. Fresh builds close the submitted proof,
the proof executes a macro whose fully expanded KORE is byte-identical to the
fresh parse of the submitted `solution.mpy`, and a meaningful false-result
mutation is rejected at the expected value mismatch.

The result is `CONCERNS / LEGIT`, rather than `PASS`, because the generated
semantics is an idealized subset rather than a complete CPython model. In
particular, it omits recursion/resource exceptions that are observable for
large valid Python inputs, and its general `%`/`//` rules disagree with Python
on negative dividends even though those cases are unreachable in this fixed
program. Neither limitation enables a false returned result on any reachable
normal execution of the submitted program, so they do not make the K proof
illegitimate.

All candidate prose, prior logs, traces, and candidate-compiled definitions
were treated only as untrusted claims. Builds and experiments used source
copies in `/tmp/audit-work`; reviewer artifacts and bounded logs are under
`/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` is absent, exactly as this mode requires.
There is therefore no infrastructure breach and no hidden or inferred
reference semantics was used.

The required candidate artifacts are regular files, not symlinks:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. There are no missing, mistyped, or
symlinked required artifacts. The candidate also contains untrusted generated
build products (`semantic-kompiled/`, `verification-kompiled/`, and
`__pycache__/`); these are extra caches, not source deliverables, and were
deliberately neither copied nor used. There are no additional helper K source
files.

Fresh hashes and comparisons establish:

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`c2e8f3...5981`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485...db16`).
- No symlink exists anywhere beneath `/candidate` or `/reference`.

The exact checks and exit statuses are in
`evidence/provenance/integrity.log` (exit 0), and the complete candidate tree is
in `evidence/provenance/candidate-tree.txt`.

The metadata was read only as untrusted history. `run-input.json` claims
problem `108-count-nums`, condition `bare`, and no supplied semantics;
`metrics.json` claims a generation exit of 0 without timeout;
`codex-last.txt` and `codex-output.log` claim one aggregate `#Top` for seven
claims. The structured trace was fully parsed: 198 valid JSONL records, zero
malformed records, 30 custom tool calls, and 30 corresponding outputs. Its
claims and intermediate failures are summarized in
`evidence/provenance/trace-summary.log`; the original untrusted inputs are
preserved in `evidence/provenance/`. None was accepted as proof evidence.

The independently observed toolchain is K v7.1.293 and Python 3.10.12
(`evidence/provenance/tool-versions.log`).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a list of integers, return the count of elements whose decimal digit sum is
strictly positive. For a negative integer, only its most-significant decimal
digit is signed negative: for example, `-123` has digit sum
`-1 + 2 + 3 = 4`. The documented examples require:

- `[] -> 0`
- `[-1, 11, -11] -> 1`
- `[1, 1, 2] -> 3`

The trusted canonical implementation converts the absolute decimal spelling to
digits, negates the first digit for a negative number, and counts positive
sums. The candidate implements an equivalent recursive `digit_sum` and then
recurses structurally over the input list.

### Translation identity

The trusted command

`python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py`

regenerated an artifact with SHA-256
`466756...1937`, byte-identical to the submitted `solution.mpy`. Both translator
and `cmp` exited 0. See
`evidence/differential/translation-regeneration.log`.

### Independent differential testing

The reviewer-authored corpus generator and test are:

- `evidence/differential/generate_inputs.py`
- `evidence/differential/differential.py`
- `evidence/differential/inputs.json`

The corpus preserves 5,391 distinct inputs. It includes all three examples;
the `-10/-9` and `9/10` helper branch boundaries; values with negative, zero,
and positive signed digit sums; all pairs drawn from 27 branch-focused values;
all lists of lengths 0 through 3 over a nine-value boundary set; every
singleton integer from -1000 through 1000; and 2,000 deterministic random lists
of lengths 0 through 25 with integers in `[-10^18, 10^18]` (seed 108).

The test imports both `/reference/canonical.py` and the candidate
`solution.py`, and uses a third independently written string-based signed digit
oracle. Result: 5,391 cases, zero canonical mismatches, zero candidate
mismatches, and zero direct `digit_sum` boundary mismatches. Command, scope,
examples, and exit 0 are in `evidence/differential/differential.log`.

An explicit resource-boundary probe found two observable CPython differences:

- `[1] * 1500`: canonical returns 1500; candidate raises `RecursionError`.
- A singleton list containing a 1,050-digit positive integer: canonical
  returns 1; candidate raises `RecursionError`.

The probe intentionally exits 1 and is preserved in
`evidence/differential/resource-boundaries.log`. These are
termination/exception differences, not wrong returned values. They matter to
the Python-language adequacy bridge, but partial correctness does not assert a
postcondition when the candidate fails to return normally.

## 3. Clean proof reconstruction

Only the source files were copied to `/tmp/audit-work/candidate-src`. Neither
candidate `*-kompiled` directory nor any candidate cache was reused.

### Fresh generated-semantics build and execution

The LLVM definition was built with:

`kompile semantic.k --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX --backend llvm --output-definition /tmp/audit-work/semantic-kompiled`

It exited 0 with no diagnostic
(`evidence/build/kompile-semantic-llvm.log`). Ten fresh `krun` executions then
covered empty, documented, sign, digit-boundary, and exact entry-witness cases.
Every `krun` exited 0 and matched both Python implementations:

| Input | K | candidate Python | canonical Python |
|---|---:|---:|---:|
| `[]` | 0 | 0 | 0 |
| `[-1,11,-11]` | 1 | 1 | 1 |
| `[11,-11]` | 1 | 1 | 1 |
| `[-11,11]` | 1 | 1 | 1 |
| `[1,1,2]` | 3 | 3 | 3 |
| `[-123,-100,-99,0,10]` | 2 | 2 | 2 |
| `[-10,-9,9,10]` | 2 | 2 | 2 |
| `[-99,-98,99,100]` | 2 | 2 | 2 |
| `[-1000,0,1000]` | 1 | 1 | 1 |
| `[-101,-100,-20,-19,-11]` | 1 | 1 | 1 |

The reviewer script prints every exact `krun` argv, result, comparison, and
exit status in `evidence/concrete/krun-python-comparison.log`.

### Fresh proof build and positive claims

The Haskell definition was built with:

`kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/verification-kompiled`

It exited 0 with no diagnostic
(`evidence/build/kompile-verification-haskell.log`).

The exact submitted positive command,

`kprove spec.k --definition /tmp/audit-work/verification-kompiled --spec-module SPEC`

exited 0 and printed exactly `#Top`
(`evidence/proofs/submitted-aggregate.log`).

Because the submitted claims are unlabeled and claims 1–4 form a mutually
supporting induction, the audit also reconstructed explicit modules:

| Reconstructed target | Dependencies retained | Result |
|---|---|---|
| digit-sum helper claim | none | `#Top`, exit 0 |
| empty count helper claim | none | `#Top`, exit 0 |
| positive/nonpositive count induction | all four helper cases | `#Top`, exit 0 |
| empty entry claim | common helper layer | `#Top`, exit 0 |
| positive-head entry claim | common helper layer | `#Top`, exit 0 |
| nonpositive-head entry claim | common helper layer | `#Top`, exit 0 |

The reconstructed source is
`evidence/proofs/audit-spec-dependencies.k`; the corresponding logs are
`claim-1-digit-sum.log`, `claim-2-count-empty.log`,
`helper-induction-group.log`, and the three `entry-*-with-helpers.log` files.
Thus every original obligation was freshly run, and each end-to-end target was
run separately with only its legitimate induction layer.

For transparency, stripping the required helper/induction claims caused the
positive and nonpositive recursive cases to stick, and the stripped
nonpositive entry diagnostic was interrupted after more than three minutes.
Those diagnostics are preserved as `claim-3-*`, `claim-4-*`,
`claim-6-*`, and `claim-7-*` logs. They are not failures of the submitted
aggregate theory: removing a mutually recursive circularity removes the
induction hypothesis needed for the recursive call.

## 4. Adequacy and real-program pinning

### Plain-language meaning of all seven claims

1. For any mathematical integer `N`, calling the actual loaded `digit_sum`
   body returns `signedDigitSum(N)`, restores the caller environment/stack, and
   preserves an arbitrary continuation.
2. Calling the actual loaded `count_nums` body on the empty K list returns 0.
3. On a nonempty list whose head has positive signed digit sum, actual
   `count_nums` execution returns `countPositive` of the complete input.
4. The same result holds in the complementary nonpositive-head case. Claims
   2–4 exhaust every finite `VList`.
5. From clean state, loading the exact program and invoking `count_nums([])`
   returns 0 and leaves the exact loaded function map.
6. From clean state, every nonempty positive-head input returns
   `countPositive` of that input.
7. From clean state, every nonempty nonpositive-head input returns the same
   exact summary. Claims 5–7 exhaust every finite integer list.

Claims 1, 2, and 5 have no logical precondition beyond the well-sorted
configuration. Claims 3 and 6 require `signedDigitSum(I) > 0`; claims 4 and 7
require `signedDigitSum(I) <= 0`. The positive and nonpositive guards are
disjoint and exhaustive over integers.

### Actual submitted program, not a substitute

The entry `<k>` uses `solutionProgram`, a macro in `verification.k`. The audit
freshly parsed submitted `solution.mpy`, separately parsed `solutionProgram` in
module `VERIFICATION`, expanded all macros, emitted KORE for both, and compared
the outputs byte-for-byte. Both KORE files have SHA-256
`a0dace...6ee1`; `cmp` exited 0. Exact commands and statuses are in
`evidence/static/program-pinning-kast.log`.

The macro therefore denotes exactly the submitted translated constructor tree.
The operational `Module` and `FuncDef` rules then execute and produce
`solutionFuns`; concrete final configurations also show the exact two loaded
bodies. No proof rule rewrites a call directly to `countPositive` or
`signedDigitSum`.

The postconditions are result-constraining. The entry right-hand sides are
`IntV(0)` or `IntV(countPositive(the same input))`; there is no fresh result
variable, existential output, tautological equality, or one-way implication.
`countPositive`, `signedDigitSum`, and `boolToInt` are fully defined functions.

### Satisfiable entry witnesses

| Entry claim | Satisfying clean state/input | Guard | Formal result | K / candidate / canonical |
|---|---|---|---:|---:|
| 5 | empty maps/lists, `[]` | none | 0 | 0 / 0 / 0 |
| 6 | empty maps/lists, `[11,-11]` | `signedDigitSum(11)=2 > 0` | 1 | 1 / 1 / 1 |
| 7 | empty maps/lists, `[-11,11]` | `signedDigitSum(-11)=0 <= 0` | 1 | 1 / 1 / 1 |

These are present in the concrete comparison log and differential corpus.
They also witness that no entry precondition is contradictory.

## 5. Rule-by-rule static soundness review

The exhaustive declaration, attribute, rule, claim, and construct-coverage
inventory is `evidence/static/rule-inventory.md`. The mechanical declaration
scan with source line numbers is `evidence/static/declaration-scan.log`.

In total, `semantic.k` contains 39 local rules: six exact `list(...)` macro
expansions and 33 operational rules. `verification.k` contains 11 rules: four
compile-time program/body/map macros and seven equations for three total
mathematical functions. There are no generated helper K files.

The inventory enumerates every local:

- syntax sort and constructor (`Module`, statements, expressions, comparison,
  index/slice, values, function/frame, and all 12 continuation items);
- configuration cell;
- macro and macro-expansion rule;
- operational rule;
- `function`, `total`, `symbol`, and SMT-hook declaration;
- proof claim.

There are no local `functional`, simplification, priority, `owise`, fresh,
unconstrained opaque, or result-oracle declarations.

### Operational semantics

The four-cell configuration is minimal and read: `<k>`, `<funs>`, `<env>`, and
`<stack>`. Module loading preserves exact bodies. Calls evaluate the actual
argument, resolve one of the two unshadowed global functions, push the caller
environment, install the one parameter binding, execute the body, and restore
the caller on return. All submitted returns are the sole statement in their
selected branch.

Evaluation order is explicit and Python-compatible on the used subset:
condition before branch; left before right for binary operators and
comparisons; base before integer index; argument before the called body. The
rules cover every used literal, name, empty list, unary minus, `+`, `%`, `//`,
`<`, `>`, empty-list equality, call, index 0, and exact `[1:]` slice. The index
is reached only after a nonempty test. Unsupported forms remain stuck instead
of fabricating a value.

List slicing is represented by the immutable tail and does not model Python
allocation identity. The program performs no mutation or identity test, so
that omitted allocation is observationally irrelevant here. No heap, I/O,
exception, concurrency, or resource-limit behavior is modeled.

### Proof-local definitions

`solutionProgram`, `digitBody`, `countBody`, and `solutionFuns` are only exact
macros; they do not preempt or summarize operational execution. The body
sensitivity experiment changed only the empty branch from `Return(Int(0))` to
`Return(Int(1))`. The altered definition built successfully, but the aggregate
proof exited 1 and stuck at actual `IntV(1)` against the required `IntV(0)`.
See `evidence/static/body-mutation-diff.log`,
`body-mutation-build.log`, and `body-mutation-proof.log`.

`signedDigitSum` has three pairwise-disjoint, exhaustive integer guards:
`N < -9`, `N > 9`, and `-9 <= N <= 9`; recursive calls strictly decrease
absolute decimal magnitude. `countPositive` has exhaustive `VNil`/`VCons`
equations and structurally decreases the list. `boolToInt` covers the two Bool
constructors, and its `ite` SMT hook agrees with `true -> 1` and `false -> 0`.
Thus all three `total` declarations have covered, consistent equations.

These summaries do not replace program execution. The universal helper claims
machine-connect actual `digit_sum` execution to `signedDigitSum`, and the
three exhaustive list claims machine-connect actual `count_nums` execution to
`countPositive`. Reusing those claims only after semantic progress is the
ordinary circularity/induction mechanism, not an opaque oracle.

### Narrow semantic limitations

K `/Int` and `%Int` use truncation toward zero. Python `//` and `%` differ on a
negative dividend with a positive divisor. A concrete off-path witness is:

- K: `-11 /Int 10 = -1`, `-11 %Int 10 = -1`
- Python: `-11 // 10 = -2`, `-11 % 10 = 9`

The fresh probe is in `evidence/static/negative-*-krun-module-int.log` and
`python-negative-arithmetic.log`. This does not witness a false conclusion on
the submitted program's intended input domain: the negative-number branch
first evaluates `-num > 0` before division/modulo, and the positive branch has
`num > 9`. Every reachable dividend is positive. The rules are therefore
over-broad relative to full Python but sound on every reachable use here.

Likewise, general Python return-after-trailing-statements and locally shadowed
callables are outside this deliberately small semantics, but neither situation
occurs in the exact program. I found no rule that can enable a false returned
result for a satisfying intended input, so I do not label any local rule
materially unsound. These narrower coverage/bridge limitations support a
`CONCERNS` verdict, not `FAIL`.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation evidence was
trusted. The audit created
`evidence/vacuity/audit-spec-vacuity.k`.

The mutation uses the fully satisfying positive-head input `[11]` but changes
the exact normal-result obligation from 1 to 0. It is meaningful and reachable:
`signedDigitSum(11)=2 > 0`, and both Python implementations return 1.

First,

`kprove audit-spec-vacuity.k --definition /tmp/audit-work/verification-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run`

exited 0 and emitted the `kore-exec` invocation, proving the mutation parses
and builds (`evidence/vacuity/vacuity-dry-run.log`). The actual proof command
then exited 1 with `WarnStuckClaimState`. Its residual is the complete clean
final configuration with `IntV(1) ~> .K`, which cannot unify with mutated
`IntV(0)`. See `evidence/vacuity/vacuity-proof.log`. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What is machine-proven

Under the freshly built generated semantics and its imported K builtins, the
seven reachability claims establish partial correctness for every finite
`VList` of mathematical integers:

- the exact submitted program tree loads the exact two function bodies;
- actual recursive execution of `digit_sum(N)` returns the fully defined
  `signedDigitSum(N)`;
- actual recursive execution of `count_nums(INPUT)` returns the fully defined
  number of elements whose `signedDigitSum` is positive;
- clean entry execution returns that exact constrained integer and restores the
  modeled environment/stack state.

This is a reachability/partial-correctness theorem. It does not assert CPython
termination, absence of resource exceptions, or behavior for values outside
the modeled finite integer-list domain.

### Trust and assumption ledger

| Boundary | Influence | Evidence and assessment |
|---|---|---|
| K compiler, Haskell/LLVM backends, `kore-exec`, SMT integration | Parsing, execution, and proof closure | Standard low-level trusted computing base; versions recorded and all builds fresh. Acceptable. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, `LIST` builtins | Arithmetic, guards, environments, frames | Standard fixed K primitives. Accepted, with the explicitly bounded Python-vs-K division concern above. |
| `boolToInt` SMT hook | Normalizes symbolic branch count | Exact `ite(true,1,0)`/`ite(false,1,0)` equations; exhaustive and nonopaque. Acceptable. |
| Trusted translator `/reference/py2mpy.py` | Python AST-to-constructor provenance | Candidate translator matches trusted bytes; regenerated `solution.mpy` matches submitted bytes. Acceptable provenance bridge. |
| `solutionProgram` macro | Chooses the executed program | Fresh expanded-KORE byte identity with submitted `solution.mpy`; body mutation invalidates proof. Strong, acceptable pinning. |
| Generated semantics to Python behavior | Meaning of the translated constructors | Exhaustive static review on every used construct plus ten concrete K/Python comparisons. No mechanized CPython correspondence; resource exceptions omitted. Legitimate but concerning boundary. |
| `signedDigitSum` means the prompt's signed decimal digit sum | Natural-language intent | Equations implement decimal right-peeling with a signed leading base digit; universal K claim connects the program helper to them. Human mathematical interpretation plus finite tests, not a separate decimal-string theorem. Acceptable with concern. |
| Candidate versus trusted canonical behavior | Implementation-to-intent bridge | Independent 5,391-case differential has zero normal-result mismatches; finite evidence only. Resource probe exposes two recursion exceptions. Supports, but does not replace, the K proof. |

There are no opaque result symbols, empirical operational bridges, trusted
program-defined helpers, or assumptions imported from `PROOF.md`, generation
traces, prior `#Top` output, or candidate compiled artifacts.

### Validation gates and decision

- Gate A, real-program soundness: **PASS**. Exact program pinning, full body
  execution, universal connection claims, satisfiable states, body sensitivity,
  and result mutation all pass.
- Gate B, intent/language adequacy: **LIMITED**. Normal returned values align,
  but the semantics omits CPython recursion/resource exceptions and contains
  broader off-path arithmetic rules. This is `SOUND-BUT-LIMITED`, not an
  internal proof unsoundness.
- Gate C, trust/evidence auditability: **PASS**. Exact sources, commands,
  statuses, bounded outputs, corpus, mutations, and reviewer scripts are
  preserved.

The proof is therefore legitimate and result-constraining, but the bridge from
the idealized K machine to all observable CPython executions has documented
limitations. The appropriate decision is `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
