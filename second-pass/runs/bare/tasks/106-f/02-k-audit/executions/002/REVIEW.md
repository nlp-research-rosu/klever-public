# Independent adversarial review — HumanEval 106-f

The candidate contains a legitimate partial-correctness proof of the generated
program over the intended domain of nonnegative integer inputs. I rebuilt both
definitions from source, discharged the complete target claim set with a fresh
`kprove`, mechanically pinned the theorem term to trusted regeneration of
`solution.mpy`, reviewed every local K declaration/rule, and obtained the
expected failures from independent body and postcondition mutations.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS` in
`/audit-input.json`. This agrees with `/task.json`, `/run.json`, and the
generation records.

I read and checked:

- `/audit-input.json` and `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `legacy-metrics.json`, and `legacy-run-input.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- all 167 JSONL events in the one structured trace below
  `/generation-evidence/codex-trace/`.

These records were treated only as generation claims. The independently
generated event/tool summary is in
`evidence/generation-trace-summary.log`; a bounded index into the plaintext
generation log is in `evidence/codex-output-command-index.log`.

All required mounts and legacy-selected records are real regular files or real
directories. The candidate and trace trees contain no symlink or unsupported
entry. All required proof artifacts (`solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and `prove.sh`) are present as
regular files.

The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. The lock's actual SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the value recorded in `/audit-input.json`.

Every launcher-declared file hash checked in
`evidence/provenance_check.py` matches the mounted file. This includes the
canonical, trusted/candidate prompt, trusted/candidate translator, run/task
manifests, stage-1 result and invocation, metrics, usage, generation prompt,
generation last message, and generation output.

For recursive trees, independently applying the run pipeline's documented
content-and-path `sha256_tree` algorithm gives:

- candidate:
  `9446aa8469c786d57b74e526869d9e7b4b8607f32285e9da67fce8789b068cb3`,
  matching both `/generation-result.json` and
  `/generation-evidence/invocation.json`;
- trace:
  `85741d0e97232409e3c40a970ee8ec0184e6b8418d17699bacc9762e9495940c`,
  matching `/generation-evidence/usage.json`.

`/audit-input.json` also records separate launcher-level candidate/trace tree
values without naming their serialization algorithm. I did not incorrectly
compare those values to the pipeline algorithm; file-by-file hashes and the
generation-record pipeline digests establish that the mounted contents are the
recorded contents. Full paths, hashes, comparisons, and exit 0 are preserved
in `evidence/provenance.log`.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
`/reference/reference-semantics` is absent, as required for
`GENERATED_SEMANTICS`. There is no semantics-mode contradiction or other
audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For a nonnegative integer `n`, `f(n)` must return the length-`n` list indexed
from 1 in which the element for index `i` is:

- `i!` when `i` is even; and
- `1 + ... + i` when `i` is odd.

Thus `f(5)` must be `[1, 2, 6, 24, 15]`. The empty boundary `n=0`
requires `[]`.

The trusted canonical recomputes each factorial/triangular value with nested
`for` loops. The candidate uses one `while` loop and maintains a factorial
accumulator and a sum accumulator. This is a different but faithful algorithm:
both accumulators are updated through the current index before the parity
selection and append.

### Trusted regeneration

In scratch I ran the trusted translator on the copied `solution.py`:

```text
python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

The regenerated and submitted files are byte-identical, both with SHA-256
`c3b6b7a6b415641b7bb201cb69b8bfb18fdb92963412f8ea5063d0a08e2f08d7`.
The exact command, comparison, hashes, and exit 0 are in
`evidence/translator-byte-identity.log`.

### Independent differential

`evidence/differential.py` imports `/reference/canonical.py` and the copied
candidate through independent module loaders. It also uses a separately
implemented oracle based on `math.factorial(i)` and `i*(i+1)//2`.

The run covered:

- the documented example;
- negative observational checks `-3,-1`;
- empty and branch boundaries `0` through `10`;
- every integer `0` through `64`;
- 64 seeded draws from `0` through `120`;
- scale cases `100`, `120`, and `200`.

After deduplication there were 89 cases and zero mismatches among canonical,
candidate, and property oracle. Inputs, boundary outputs, record digest,
command, and exit 0 are in `evidence/python-differential.log`.

The formal theorem does not use the negative observations: its domain is
`N >= 0`, which is the material domain implied by a list of size `n`.
Non-integer inputs are likewise outside the canonical's `range`-based
contract.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/reconstruction`. The
candidate mount contains no compiled definition or cache, and none was reused.
The observed tools are K 7.1.293; see `evidence/tool-versions.log`.

### Concrete definition

Fresh build:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition audit-semantic-kompiled
```

This exited 0 (`evidence/kompile-semantic-llvm.log`).

`evidence/semantics_differential.py` then invoked that fresh definition for
`n = -1,0,1,2,3,4,5,8,10,12`. Every `krun` exited 0, reached
`<k> .K </k>` with `done(listVal(...))`, and matched both Python
implementations. This exercises zero iterations, the first odd branch, the
first even branch, repeated parity changes, and larger factorial values.
There were ten cases and zero mismatches; exact per-input commands and outputs
are in `evidence/generated-semantics-differential.log`.

### Proof definition and claims

Fresh build:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition audit-verification-kompiled
```

This exited 0 (`evidence/kompile-verification-haskell.log`).

The complete candidate target:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --output pretty
```

printed `#Top` and exited 0
(`evidence/kprove-all-claims.log`). An explicit selection of both positive
labels,
`SPEC.loop-invariant,SPEC.main-correct`, independently printed `#Top` and
exited 0 (`evidence/kprove-explicit-target-set.log`). The loop claim by itself
also printed `#Top` and exited 0
(`evidence/kprove-loop-invariant-only.log`).

The main claim relies on the loop claim as its circular loop lemma. As a
dependency diagnostic, selecting only `SPEC.main-correct` removes that lemma
from the proof set and timed out after 60 seconds
(`evidence/kprove-main-only.log`). That altered proof context is not the
candidate's positive target and is not evidence that the jointly discharged
main theorem failed. The explicit complete set is the relevant fresh proof:
both claims are obligations in that run, not an assumed claim.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop-invariant` starts with:

- the exact submitted loop followed by the exact final
  `Return(Name("result"))`;
- integer input/binding `N`;
- local bindings `factorial=F`, `i=I`, `n=N`, `result=L`, `total=T`;
- `noResult`; and
- precondition `N >= 0 and I >= 1`.

It says that completing this loop and return consumes the computation,
preserves `n`, leaves some final values for the three non-result accumulators,
and constrains both the environment's `result` and the observable result cell
to `expectedCompletion(I,N,F,T,L)`.

`main-correct` starts from the exact `solution` term, integer input `N`, empty
environment, `noResult`, and precondition `N >= 0`. It says execution consumes
the computation, produces exactly the five local bindings, and constrains both
result locations to `expected(N)`. The result is not a fresh variable,
tautology, implication in the wrong direction, or merely one of several
unconstrained outcomes.

### Program identity

The `solution` and `solutionLoop` symbols are syntax macros, not runtime
summaries. With macros expanded under the fresh proof definition, `kast` of
trusted-regenerated `solution.mpy` and `kast --expression solution` produce
byte-identical KORE. Both terms have SHA-256
`540c1642f3003eaf9d0dcff1aa11e5a9cae3c933d7158e7d17ed7ddb70d9f315`;
see `evidence/program-term-pinning.log`.

The expanded term includes the actual binding `FuncDef("f",Params("n"),...)`,
all initializations, the exact loop body in source order, and the final return.
No typing-only import or material operation was omitted.

### Satisfiable witnesses

`evidence/claim_witnesses.py` exhibits:

- main: `N=5`, empty environment, `noResult`;
- loop: the reachable state after iterations 1 and 2,
  `N=5,I=3,F=2,T=3,L=[1,2]`, with `noResult`.

Both satisfy their preconditions. Substitution into `expected(5)` and
`expectedCompletion(3,5,2,3,[1,2])` gives
`[1,2,6,24,15]`, exactly both Python implementations
(`evidence/claim-witnesses.log`).

### Body sensitivity

The independent mutation in
`evidence/verification-body-mutation.k` changes the executed factorial update
from multiplication to addition. Its expanded theorem term has SHA-256
`72b70c935fcf39e2c870b9172d35000eb85f25196631e3b2a4a98cc76dff6355`,
different from the real term
(`evidence/body-mutation-term-sensitivity.log`). At satisfying input `n=2`,
the mutated body returns `[1,4]` rather than `[1,2]`
(`evidence/body-mutation-witness.log`).

The mutation definition builds, but its proof exits 1 with
`WarnStuckClaimState`; the residual exposes the unmet equality between
completions using `F+I` and `F*I`
(`evidence/kompile-body-mutation.log`,
`evidence/kprove-body-mutation.log`). The theorem is therefore sensitive to a
material change in the program term it actually executes.

## 5. Rule-by-rule static soundness review

The exhaustive source-level inventory is
`evidence/rule-inventory.md`, supported by the mechanical declaration index
in `evidence/source-declaration-index.log`. It enumerates every local syntax
production, configuration/cell, function declaration, equation, macro,
ordinary semantic rule, and reachability claim.

### Inventory summary

`semantic.k` declares:

- constructor grammar for `Module`, statement/expression/parameter lists,
  the five used statements, the five used expressions, and `CmpOp`;
- integer/Boolean/list values and explicit `noResult`/`done` results;
- the `<k>`, `<input>`, `<env>`, and `<result>` cells;
- eleven explicit continuation forms; and
- 28 ordinary operational rules.

Those 28 rules cover module entry, statement sequencing, name assignment,
conditionals, loops, return, literals/lookups, empty and singleton lists,
left-to-right binary operations, integer `+/*/%`, list concatenation, and
integer `<=/==`.

`verification.k` declares five `[function]` symbols and ten guarded function
equations, plus two syntax macros and their two exact expansions. There are no
`[total]`, `[functional]`, opaque, priority, `simplification`, `anywhere`, or
proof-local operational rules. `spec.k` contains exactly the two inventoried
claims.

### Construct and state coverage

Every constructor in submitted `solution.mpy` maps to a declaration and rule
listed in the inventory. The candidate uses only:

- one function with one parameter;
- name assignments;
- `while`, `if`, and final `return`;
- integer/name/empty-list/singleton-list expressions;
- integer `+`, `*`, `%`, comparisons `<=`, `==`; and
- list concatenation.

No material construct is parsed and then fabricated or left unmodeled.
The explicit control frames enforce Python's left-to-right operand and
condition evaluation. Each loop iteration executes all four statements before
returning to the same loop head. Map updates model the only mutable state.
Because every list element is an integer and there is no alias, mutation,
identity test, exception handler, call stack, I/O, or heap operation, value
lists plus the four cells preserve every behavior observable by this program.

K integers and Python integers are both unbounded for the exercised
operations. The only modulo operation has positive loop index and divisor 2,
so any unused cross-language corner involving negative divisors is
irrelevant. All reads follow initialization and every used binary/comparison
rule has the required value types.

The semantic return rule discards its active computation suffix, as a Python
function return should. In the submitted control flow its concrete suffix is
the empty remaining statement sequence; there is no caller cleanup, exception,
or other observable continuation to lose.

### Proof-extension soundness

There is no operational proof bridge. The two macros disappear during
expansion and were shown mechanically equal to the submitted constructor
tree. No verification rule rewrites `exec`, `eval`, `While`, a function body,
or a returned value.

The loop claim is a reachability circularity over the exact real loop and exact
trailing return, complete environment, result cell, and input cell. It is
proved as an obligation in the successful complete target set; it is not a
trusted rewrite or unconstrained oracle.

The only result-bearing summary is `expected/expectedCompletion`. It never
replaces program execution: the operational rules independently compute the
list, and the claim requires equality with the summary. Its equations are
exhaustive and disjoint:

- `I>N` returns the accumulated list;
- for `I<=N`, `% 2 == 0` and `% 2 != 0` partition integers;
- both recursive cases increment `I`, update both accumulators, and append the
  correct parity-selected value.

Thus it is fully fixed over every claim use and terminates after finitely many
increments. It contains no fresh or opaque value. `expected(N)` is defined for
the entire formal domain `N>=0`.

`mathFactorial`, `mathTriangle`, and `expectedAt` have truthful, guarded,
descending equations on positive indices but are unused by both
postconditions. They neither help close the claims nor smuggle the intended
answer. Their intentionally partial negative cases have no `[total]`
declaration and are unreachable from any dependent claim because there are no
dependents.

The function guards are pairwise disjoint and cover every use; recursion
descends for factorial/triangle and advances toward the base case for
completion. No local equation overlap can yield inconsistent right-hand
sides.

I found no candidate-authored unsound rule on the intended domain. Therefore
there is no unsound-rule false-conclusion witness to report. The separate
body-mutation witness is sensitivity evidence, not an allegation that an
original rule is false.

### Summary-to-contract adequacy

Starting `expectedCompletion` at `I=1,F=1,T=0,L=[]` is a direct recursive
formalization of the requested list. By ordinary induction, immediately
before index `i`, `F` is the product through `i-1` and `T` is the sum through
`i-1`; after the two updates they are `i!` and `1+...+i`. The parity branch
then appends exactly the required one. This is a transparent mathematical
interpretation of fully defined equations, not an empirical or opaque
result-bearing bridge. The independent `math.factorial`/closed-form
differential provides additional finite corroboration but is not used as a
substitute for the K proof or the induction.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created the fresh
`evidence/spec-vacuity.k`, preserving the real loop claim but changing the
main result obligation to require one extra trailing zero:
`expected(N) ListItem(0)`.

This mutation is demonstrably false for the satisfying input `N=0`: both
Python implementations return `[]`, while the mutation demands `[0]`
(`evidence/vacuity-witness.log`).

The mutated spec first built successfully with:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run --output pretty
```

That command exited 0 (`evidence/kprove-vacuity-dry-run.log`). The actual proof
then exited 1 with `WarnStuckClaimState`. Its residual shows the precise unmet
equality between the real completion and that completion followed by
`ListItem(0)` (`evidence/kprove-vacuity-failure.log`). This is a reachable
result-constraint failure, not a parse error, missing import, timeout, or
unrelated crash.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the submitted generated semantics and imported K builtins, the
successful all-path reachability proof establishes:

1. For every K integer `N>=0`, executing the exact submitted `f` constructor
   body from the benchmark entry configuration has no terminating result
   other than `expected(N)`. On completion, both the `result` local and
   `<result>` cell contain that exact list.
2. More generally, for every `N>=0`, `I>=1`, and arbitrary integer
   accumulators `F,T` and list prefix `L`, executing the exact loop plus final
   return completes with
   `expectedCompletion(I,N,F,T,L)`.
3. `expected(N)` recursively contains exactly the required factorial values at
   even indices and triangular sums at odd indices, by the induction stated in
   Stage 5.

This is partial correctness. The reachability proof is not presented as a
separate termination theorem, although concrete execution and the
strictly-increasing loop counter make termination evident for each fixed
nonnegative integer input.

### Trust ledger

| Boundary | Effect/dependents | Assessment |
|---|---|---|
| K 7.1.293 front end, Haskell/LLVM backends, and reachability implementation | All builds/executions/proofs | Standard low-level proof-tool trust boundary; acceptable. Fresh builds avoid candidate binaries/caches. |
| Imported K `INT`, `BOOL`, `STRING`, `MAP`, and `LIST` hooks | Arithmetic, comparisons, environment, list values | Standard mathematical/runtime primitives; acceptable on the used domains. |
| `/reference/py2mpy.py` as trusted AST transliterator | Source-to-`solution.mpy` bridge | Launcher-designated trusted input. Byte identity was independently re-established. |
| Generated module-entry convention: execute the sole one-parameter function body with `<input>` bound to that parameter | Connects the constructor module to the HumanEval entry invocation | Acceptable and exact for the submitted `FuncDef("f",Params("n"),BODY)`. It executes rather than summarizes `BODY`. |
| Candidate-authored Python-subset semantics | Meaning of the real constructor program | Accepted after exhaustive static review and fresh boundary execution. It covers every used construct and stops outside many unused forms rather than fabricating them. |
| Recursive `expected` equations to English factorial/triangular contract | Intent interpretation | Acceptable ordinary induction over fully defined equations; no opaque symbol or assumed value. Finite property-oracle tests are corroboration only. |
| Python differential | Candidate/canonical equivalence on 89 inputs | Finite evidence only; it does not replace the K theorem. |

There is no candidate-local trusted primitive, opaque symbol, unconstrained
oracle, empirical rewrite, simplification lemma, or priority rule. The theorem
does not cover non-integer inputs or claim Python exception/alias behavior not
exercised by the program. It formally states `N>=0`; negative inputs were
tested observationally but are not needed by the source contract.

### Gate and decision summary

- Gate A, real-program soundness: PASS. Fresh `#Top`, exact program-term
  identity, complete result constraint, exhaustive extension audit, body
  sensitivity, and false-postcondition rejection all hold.
- Gate B, intent adequacy: PASS. The unrestricted nonnegative-integer source
  domain is covered; there is no fixed-size unrolling or example-only
  restriction.
- Gate C, trust/evidence auditability: PASS. All commands, statuses, scripts,
  mutations, witnesses, and bounded relevant outputs are preserved under
  `/audit-output/evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
