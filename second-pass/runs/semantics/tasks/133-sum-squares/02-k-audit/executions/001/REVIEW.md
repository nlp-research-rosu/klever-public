# Independent adversarial review: 133-sum-squares

The two submitted reachability claims reconstruct cleanly and the
proof-specific loop acceleration is independently justified by a bridge-free
loop proof. The result is non-vacuous and the exact submitted function body is
executed by the entry claim as a direct closure. I judge the proof legitimate,
with concerns: the entry claim relies on an external syntactic/module-to-closure
pin rather than executing the submitted `Module` and resolving
`sum_squares`, and symbolic float ceiling remains a supplied opaque primitive.
Four requested provenance artifacts are also absent.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory exists, is a real directory, and
contains no symlinks, so the trusted mounts do not contradict the rendered
mode.

The independent manifest/type/hash check in
[`evidence/01-integrity.log`](evidence/01-integrity.log) found:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `c3e8935467740bb6def5ca00e35116e04dc22c240cc22df0f0efee1e5a493d57`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- The candidate supplied-semantics tree has exactly the same 25 entries
  (one subdirectory and 24 regular K files) as the trusted tree. There are no
  missing, additional, changed, mistyped, or symlinked entries.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files, not symlinks.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are missing. No structured generation trace is present.
  Consequently no generation metrics or narrative can be authenticated.

The candidate also contains auxiliary `prove.sh`, `concrete_tests.py`,
`concrete_tests.mpy`, and `__pycache__` entries. They are not part of the
trusted semantics comparison and were not trusted as proof evidence.
`PROOF.md` and a candidate vacuity spec are absent.

All execution sources were copied to
`/tmp/audit-work/133-sum-squares-audit`; the supplied semantics came from the
trusted reference tree, not a candidate cache. The exact copy command and
scratch manifest are in
[`evidence/03-scratch-copy.log`](evidence/03-scratch-copy.log).

Stage result: integrity of the program, translator, and supplied semantics
passes. Provenance completeness has a documented gap.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks for the sum of the squares of the ceilings of the
numbers in the input list. On the ordinary intended domain of finite Python
integers/floats:

```text
sum_squares([x1, ..., xn]) = ceil(x1)^2 + ... + ceil(xn)^2
sum_squares([]) = 0
```

The trusted canonical implementation initializes an accumulator to zero,
iterates left-to-right, adds `math.ceil(i) ** 2`, and returns the accumulator.
The submitted `solution.py` is the same algorithm with renamed local
variables. Source listings are preserved in
[`evidence/02-source-inspection.log`](evidence/02-source-inspection.log).

Python raises for non-finite floats such as NaN/infinity; these were tested for
exception parity but are not finite-real ceiling inputs. Unsupported
non-numeric values are outside the natural-language “numbers” domain.

### Trusted translation

The reviewer ran the trusted translator against the scratch copy of
`solution.py`. It exited 0, produced SHA-256
`7971e30fcd646c4fb2d73f9616ccf6303092865ac95c1ce4fe46501f8be97b25`,
and was byte-identical to submitted `solution.mpy`; see
[`evidence/04-regenerate.log`](evidence/04-regenerate.log) and
[`evidence/regenerate_solution.py`](evidence/regenerate_solution.py).

### Independent differential testing

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports `/reference/canonical.py` and the scratch `solution.py`. It does not
reuse K summary equations. Its complete deterministic scope was:

- all five documented examples;
- 17 empty, sign, integer-boundary, large-integer, boolean, NaN, and infinity
  cases;
- all 820 lists of lengths zero through three over a nine-value pool straddling
  positive and negative ceiling discontinuities;
- 200 generated lists of lengths zero through eight using random seed 133.

All 1,042 comparisons matched, including return values and exception
type/message for non-finite inputs. The complete inputs and per-case results are
in [`evidence/05-differential.log`](evidence/05-differential.log).

Stage result: pass.

## 3. Clean proof reconstruction

The installed tools were K `v7.1.337`. No candidate compiled definition or
cache was copied or used.

### Concrete definition

The trusted supplied semantics rebuilt with:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0
([`evidence/06-kompile-runtime.log`](evidence/06-kompile-runtime.log)).
Concrete execution of the actual submitted `solution.mpy` also exited 0 and
produced an environment-0 `sum_squares` closure whose body is the submitted
assignment/loop/return body
([`evidence/07-krun-solution.log`](evidence/07-krun-solution.log)).

The reviewer-authored concrete witness executes empty, integer, float,
negative, and ceiling-boundary assertions. Translation and `krun` both exited
0; the final configuration has `.K`, `NoExc`, and exit code 0
([`evidence/14-build-concrete-witness.log`](evidence/14-build-concrete-witness.log),
[`evidence/15-krun-concrete-witness.log`](evidence/15-krun-concrete-witness.log)).

### Positive claims

There are exactly two positive target claims.

1. The base proof definition was freshly built from `verification.k` with main
   module `SUM-SQUARES-VERIFICATION-BASE`. Build exit: 0
   ([`evidence/08-kompile-loop-proof.log`](evidence/08-kompile-loop-proof.log)).
   The bridge-free command

   ```bash
   kprove spec.k \
     --definition loop-verification-kompiled \
     --spec-module SUM-SQUARES-LOOP-SPEC \
     --claims SUM-SQUARES-LOOP-SPEC.loop-correct \
     --output pretty
   ```

   exited 0 and printed `#Top`
   ([`evidence/09-kprove-loop.log`](evidence/09-kprove-loop.log)).

2. The downstream definition was freshly built with main module
   `SUM-SQUARES-VERIFICATION`. Build exit: 0
   ([`evidence/10-kompile-function-proof.log`](evidence/10-kompile-function-proof.log)).
   The command

   ```bash
   kprove spec.k \
     --definition verification-kompiled \
     --spec-module SUM-SQUARES-SPEC \
     --claims SUM-SQUARES-SPEC.function-correct \
     --output pretty
   ```

   exited 0 and printed `#Top`
   ([`evidence/11-kprove-function.log`](evidence/11-kprove-function.log)).

Compiler warnings concerned unused variables and non-exhaustiveness of some
fixed total functions. They did not prevent either build or proof. The
`ceilF(cellsMark(...))` totality warning concerns a non-numeric internal value,
not an intended numeric input.

Stage result: pass. Both required success signals (exit 0 and `#Top`) are
present.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop-correct` starts with the exact `#loop` body from the submitted function,
an already evaluated `list(VS)`, environment location `L`, and a current scope
containing `lst`, `number = CURRENT`, and `result = ACC`. Its only explicit
condition is that `L` is not also a key of the framed `GLOBAL` map. It says the
loop reaches the arbitrary following continuation, changes `number` to the
last element when one exists, and changes `result` to
`sumSquaresFrom(ACC, VS)`. On an empty suffix it preserves `CURRENT` and
`ACC`.

`function-correct` has no `requires` clause. It starts from an exact direct call
of a `closureVal` with one parameter `lst`, the submitted function body,
defining environment 0, and argument `list(VS)`. It pins environment 0, the
two-scope global/builtin setup, fresh scope location 1, empty stack, and
`noRet`. It says the call returns `sumSquaresFrom(0, VS)` before the same
arbitrary continuation.

### Program identity

The entry claim does not execute `Module(...)` and does not resolve
`Name("sum_squares")`; it directly calls a closure. This is visible both in the
source and
[`evidence/33-check-embedded-body-original.log`](evidence/33-check-embedded-body-original.log).
That independent token-level check nevertheless establishes:

- the submitted `FuncDef` is named `sum_squares`;
- both the submitted function and closure use exactly parameter `lst`;
- the closure defining environment is 0; and
- the submitted function body and the embedded closure body have the identical
  token hash
  `e2740273e2b69d1218589c50da0450a144da2e7e24c274673df67846443ab820`.

The concrete module execution in stage 3 independently shows that loading the
actual ground module creates exactly this closure at environment 0. The
formal call omits the otherwise irrelevant global
`"sum_squares" |-> closureVal(...)` binding; the body uses only local
`lst/result/number`, and `math.ceil` is syntactically intercepted by the fixed
semantics. Static lookup/control review confirms the omitted self-binding
cannot affect this non-recursive body.

The body-sensitivity experiment regenerated a coherent source/MPY mutant that
returns 999. Python then returned 999 for `[1,2,3]`
([`evidence/27-regenerate-pinning-mutant.log`](evidence/27-regenerate-pinning-mutant.log),
[`evidence/28-run-pinning-mutant-python.log`](evidence/28-run-pinning-mutant-python.log)).
An isolated rebuild of the unchanged K spec still printed `#Top`
([`evidence/29-kompile-source-pinning-mutant.log`](evidence/29-kompile-source-pinning-mutant.log),
[`evidence/30-kprove-source-pinning-mutant.log`](evidence/30-kprove-source-pinning-mutant.log)),
showing that the K files do not mechanically depend on `solution.mpy`. Crucially,
the independent pinning check rejected that mutant with different body hashes
([`evidence/34-check-embedded-body-mutant.log`](evidence/34-check-embedded-body-mutant.log)).
Thus the original is pinned by a reproducible external syntax/module bridge,
not by the reachability claim alone. This is a concern, but it does not make the
theorem about the original exact body false.

### Real control flow and result constraint

The function initially has no `number` binding, while the loop lemma requires
one. Consequently the promoted lemma cannot bypass the first nonempty
iteration: fixed semantics evaluates `lst`, steps the iterator, binds
`number`, and executes the first body. The lemma can then summarize only the
remaining suffix. Empty input exits under fixed semantics. This matches the
actual control flow.

The returned value is not free. `sumSquaresFrom` has disjoint empty/cons
equations and recursively adds the fixed-semantics `ceilF(V) ^Int 2`.
`lastFrom` likewise has disjoint empty/cons equations. Both strictly descend on
the algebraic tail.

A satisfying function state is the pinned entry configuration with
`VS = [1.4,4.2,0]`. A reachable satisfying loop state after its first
iteration has `L=1`, `CURRENT=1.4`, `ACC=4`, remaining `VS=[4.2,0]`, and
global keys `{-1,0}`, so `1` is not in `GLOBAL`. Substitution yields:

```text
sumSquaresFrom(0, [1.4,4.2,0]) = 29
sumSquaresFrom(4, [4.2,0]) = 29
lastFrom(1.4, [4.2,0]) = 0
```

Both Python implementations return 29. The exact witness is in
[`evidence/16-ground-claim-witness.log`](evidence/16-ground-claim-witness.log).

The formal variable is `VS:ValSeq`, broader than the intended finite-number
domain. For non-numeric values the supplied total `ceilF` is an abstract value
rather than Python's type error. For NaN/infinity Python raises. These
over-broad formal cases are not used to claim correctness beyond the intended
finite numeric domain.

Stage result: adequate for the intended function, with a documented external
program-pinning limitation.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/13-exhaustive-rule-inventory.log`](evidence/13-exhaustive-rule-inventory.log)
enumerates the exact text, file, line span, attributes, and source class of all
1,225 top-level declarations:

```text
2 claims
1 configuration
5 contexts
29 modules / 29 endmodules
90 imports
140 requires/import guards
700 rules
229 syntax declarations
```

The inventory covers `semantics.k`, all 23 helper K files, `verification.k`,
and `spec.k`. A concise disposition for every file/rule and the complete
program/control mapping is in
[`evidence/rule-review.md`](evidence/rule-review.md). Special attributes and
all concrete/opaque/priority occurrences are indexed in
[`evidence/36-opaque-and-special-attributes.log`](evidence/36-opaque-and-special-attributes.log).
There are no `[simplification]` or `[functional]` declarations. The fixed
semantics accounts for 695 rules; the candidate adds five.

All syntax used by `solution.mpy` is declared: `Module`, `Import`, `FuncDef`,
`Params`, `Assign`, `For`, `Name`, `AugAssign`, `BinOp`, `Call`, `Attribute`,
`Int`, and `Return`. The relevant fixed rules implement:

```text
module load / function definition
  → direct closure call / frame allocation / parameter binding
  → result initialization
  → one-time list evaluation
  → left-to-right list iteration and target binding
  → local lookup and syntactic math.ceil interception
  → integer exponentiation and integer augmented addition
  → return, frame deletion, stack/env/scopeLoc restoration
```

The proof call uses an unboxed read-only `list(VS)`, so it allocates no input
heap object. The loop changes only `number` and `result`; it preserves `lst`,
the parent/global scopes, heap, allocation counters, stack, return state,
exception state, exit code, and the arbitrary continuation. The call creates
one scope and stack frame and restores both on return. With a local integer
target, evaluating the augmented-assignment RHS before reading `result` has no
observable difference from Python target evaluation.

### Candidate-local extensions

1. `sumSquaresFrom(Int, ValSeq) [function,total]` is a definitional left fold.
   Its empty and cons rules are exhaustive, non-overlapping, and descending.
2. `lastFrom(Val, ValSeq) [function,total]` is a definitional last-element
   summary. Its empty and cons rules are exhaustive, non-overlapping, and
   descending.
3. The priority-40 loop rule is an operational bridge, but not an oracle. Its
   normalized contract is exactly identical to the loop claim proved against
   `SUM-SQUARES-VERIFICATION-BASE`; priority is the only addition
   ([`evidence/35-check-promoted-loop-rule.log`](evidence/35-check-promoted-loop-rule.log)).
   That bridge-free claim quantifies over the same arbitrary continuation,
   bindings, guard, and framed cells. It is therefore a universal connection
   theorem over the bridge's complete match domain.

The operational-continuation sensitivity test used the ground list `[1,2]` and
placed `Assign(Name("after"), Int(7))` immediately after the loop. Both the
bridge-free base definition and bridge-enabled definition proved the same
state: `number=2`, `result=5`, and `after=7`, each with exit 0 and `#Top`
([`evidence/31-kprove-bridge-context-base.log`](evidence/31-kprove-bridge-context-base.log),
[`evidence/32-kprove-bridge-context-extended.log`](evidence/32-kprove-bridge-context-extended.log)).
The exact loop-body pattern also means a changed displaced body does not match
the bridge.

### Opaque/trusted semantics boundary

The result-bearing primitive `ceilF(Val)` is declared `[function,total,
symbol(ceilF)]` in the fixed supplied semantics. Its integer and float equations
are `[concrete]`; symbolic Haskell proof leaves `ceilF(V)` opaque. The program
execution and `sumSquaresFrom` use the same fixed symbol, so the proof is
interpretation-parametric in `ceilF`: it proves the program constructs the
specified fold, but does not independently prove that the opaque symbolic
function is mathematical ceiling.

This is not a candidate-created circular oracle. It is an explicit supplied
semantics boundary, concretely implemented by `Float2Int(ceilFloat(...))` for
LLVM execution. The K concrete witnesses and 1,042 Python differentials support
the finite numeric bridge but do not universally prove it.

The fixed priority-40 `math.ceil` rule syntactically intercepts that exact call
before name/attribute lookup, and `Import("math")` is a no-op. This would be
over-broad for programs that shadow `math`, but the submitted program does not;
on its actual path it evaluates the argument once and returns the same ceiling.
Duplicate mixed-float rules elsewhere in fixed `float.k` have identical
right-hand sides and are unreachable here.

No candidate-local rule is labeled unsound. Accordingly there is no claimed
unsound-rule witness to supply. The narrower evidence gaps are the external
module-to-closure pin and the supplied opaque-ceiling interpretation described
above.

Stage result: candidate-local rule soundness passes.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was available. The reviewer first tried symbolic
and function-level off-by-one mutations, but failed proof search wandered into
unrelated unsupported Haskell float hooks (`Int2Float`, then `minFloat`).
Those runs are preserved in
[`evidence/17-kprove-vacuity.log`](evidence/17-kprove-vacuity.log),
[`evidence/18-kprove-vacuity-ground.log`](evidence/18-kprove-vacuity-ground.log),
and [`evidence/19-kprove-vacuity-loop-ground.log`](evidence/19-kprove-vacuity-loop-ground.log);
they are explicitly not counted as non-vacuity evidence.

The valid fresh mutation is
[`evidence/spec-vacuity-loop-ground.k`](evidence/spec-vacuity-loop-ground.k).
It instantiates the proved loop claim with a satisfying empty-list state and
`CONT = .K`, then changes the result-bearing post-state from the true
`result=0` to false `result=1`.

It parsed and executed against the bridge-free base definition. Fixed semantics
reached `.K` with `result=0`; the target did not unify, `kore-exec` emitted
`WarnStuckClaimState`, and `kprove` exited 1 with the expected unmet result
obligation. There was no parser/import error, timeout, or unrelated backend
crash in this accepted run. Exact command and residual:
[`evidence/20-kprove-vacuity-loop-ground-exact-cont.log`](evidence/20-kprove-vacuity-loop-ground-exact-cont.log).

Stage result: pass; the result obligation is discriminating.

## 7. Proven versus assumed accounting

### Precisely proven

Under the fixed supplied `MPY` Haskell theory plus the four truthful
proof-local summary equations:

- The exact loop body, from every state satisfying `loop-correct`, reaches the
  same continuation, preserves all framed state, updates `number` to
  `lastFrom(CURRENT,VS)`, and updates `result` to
  `sumSquaresFrom(ACC,VS)`.
- From the exact direct-closure call configuration in `function-correct`, for
  every algebraic `VS:ValSeq` and arbitrary `CONT:K`, the exact submitted
  function body reaches `sumSquaresFrom(0,VS) ~> CONT` while restoring the
  pinned environment, scope allocation state, stack, and return state.
- The promoted loop rule is a previously proved execution summary, not an
  assumed task-answer rewrite.
- The false empty-loop result does not prove.

This is a reachability/partial-correctness theorem about the modeled direct
closure. It is not a universal theorem about CPython or every possible meaning
of “number.”

### Trust ledger and limitations

| Boundary | Influence | Accounting |
|---|---|---|
| Byte-identical supplied MPY semantics | All syntax, control, state, and calls | Selected trusted semantics. Candidate did not modify it. Relevant rules were statically traced. |
| K integer/map/list/boolean primitives and Haskell prover | Arithmetic, collections, rewriting, `#Top` | Standard K trust boundary. Fresh reconstruction used K v7.1.337. |
| `ceilF` and LLVM float hooks | Every float element and final result | Fixed supplied primitive. Symbolically opaque; concrete LLVM execution and Python differential evidence support, but do not prove, the mathematical-ceiling interpretation. |
| Other fixed opaque symbols (`sortVS`, `sortKeyVS`, `md5hexCodes`, other float helpers listed in evidence 36) | None | Imported but unreachable before either claim target; no theorem dependency. |
| Trusted translator | Source-to-`solution.mpy` identity | Actual output was byte-compared. This tests this source, not universal translator correctness. |
| Submitted module → direct closure | Real-program identity | Ground module execution plus exact token equality establishes the bridge externally. The K entry claim itself neither executes `Module` nor resolves `sum_squares`. A source mutant demonstrates that this external check is necessary and detects drift. |
| `sumSquaresFrom` → natural-language sum of squared ceilings | Human-facing intent | Definitionally exact conditional on `ceilF`; additionally supported by 1,042 independent Python comparisons and concrete K witnesses. Finite evidence is not a universal proof. |
| Missing run/metrics/Codex logs | Generation provenance only | Prevents auditing the generation narrative, but does not change the independently reconstructed K result. |

The formal precondition is broader than the intended finite-number domain.
Behavior for non-numeric values, NaN, infinity, Python import rebinding,
exceptions, and full CPython IEEE-754 edge semantics is not validated by the K
claim. Differential testing supports only the inputs recorded in evidence and
is not substituted for the reachability proof.

Gate A (proof-extension and modeled-body soundness): pass. Gate B (finite
numeric intent adequacy): pass with explicit excluded cases. Gate C (trust and
evidence): adequate but limited by symbolic `ceilF`, external module-to-closure
pinning, and missing provenance artifacts. Those limitations warrant
`CONCERNS`, but none makes a false result provable for the intended finite
numeric domain or disconnects the audited original body.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
