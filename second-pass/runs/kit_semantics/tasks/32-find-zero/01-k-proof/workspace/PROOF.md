VALIDATED

# Proof result

Gate A: **PASS**. Gate B: **PASS**. Gate C: **PASS**.

For every symbolic `NumSeq NS` satisfying `validCoeffs(NS)`—at least two
coefficients, even length, and a nonzero final coefficient—the claims prove the
execution of:

```text
#loadAll(solutionModule)
~> find_zero(list(numVals(NS)))
```

under the supplied MPY semantics. By transitivity of the exact intermediate
configurations, the returned value is

```text
solveFrom(NS, B0, E0)
```

where `B0` and `E0` are the two values produced by the source's `len(xs) /
-len(xs)` and `len(xs) / len(xs)` expressions. `solveFrom` is definitionally:

```text
bisectFrom(NS, bracketBegin(NS, B0, E0), bracketEnd(NS, B0, E0))
```

The proof also establishes the source frame pop, restoration of environment 0,
preservation of the heap and heap counter, `NoExc`, and exit code 0 at the
return boundary. The theorem is symbolic in list length and coefficient values;
it is not a bounded unrolling or a finite-size theorem.

The positive proof is modular:

1. `SPEC.find-load` executes module loading, lookup, argument evaluation, and
   selects the exact `find_zero` closure.
2. `SPEC.find-init` executes closure application, parameter binding, all three
   initial assignments, and reaches the first fixed-semantics loop head.
3. The three `poly-loop-*` claims form a constructor-split induction over every
   finite mixed `Int`/`Float` coefficient list.
4. `expand-loop` proves the unbounded bracketing loop and its endpoint
   projections.
5. `bisect-head` proves the fixed semantics' statement-tail staging step.
6. `bisect-loop` proves the unbounded bisection loop, return, and frame pop.

Every claim in `spec.k` is covered by a positive command in `prove.sh`. Each of
the five positive `kprove` invocations printed `#Top` and exited 0 in the final
run.

# Gate A — real-program soundness

## A1–A3: identity, execution, state, binding, and control

PASS.

`solution.mpy` is regenerated from `solution.py` by the unmodified translator.
The workflow then loads both `solution.mpy` and `verification-program.mpy`
(whose term is `solutionModule`) through the same compiled semantics and
requires identical final closure configurations. This mechanically checks that
the bodies, parameters, and bindings used by the proof are the generated
program bodies.

All program-defined operations execute under the supplied rules. There is no
operational bridge in `verification.k`: no rule replaces `Call`, `#applyK`,
`For`, `#loop`, `While`, `#while`, `Return`, or a program-defined `poly`
invocation. The exact continuations, environments, scope maps, stack frames,
heap cells, return cell, exception cell, and exit code are present in the
connection claims.

The material mutation in `solution-body-mutation.py` changes the source update
from `power * x` to `power + x`. Its generated module is rejected by the
source/proof identity comparison (expected `diff` exit 1).

## A4: equations and logical consistency

PASS.

- `NumSeq`, `numVals`, `numLen`, `lastNonZero`, `validCoeffs`, `polyAcc`,
  `polyPower`, and `polyLast` recurse structurally.
- The `Int` and `Float` constructors are disjoint. The four logical
  injectivity simplifications are no-confusion consequences of the three
  `numVals` equations.
- The two expansion clauses split on `G` versus `notBool G`.
- The bisection clauses split first on the while guard and then on the source
  `if` guard. Their guards are exhaustive and pairwise disjoint.
- The recursively defined loop summaries make exactly the same recursive
  transition as their source loops. Thus they characterize partial-correctness
  execution even where an arithmetic interpretation makes a loop diverge;
  termination under the intended numeric interpretation is recorded below as
  a trust-boundary obligation.
- No equation directly asserts the requested root property.

## A5: constraint and non-vacuity

PASS.

The prompt examples are realizable witnesses and execute concretely. The
deliberately false `spec-mutation.k` claim changes the empty polynomial fold's
post-state from `A` to `addF(A, 1.0)`. `kprove` exits 1 with
`WarnStuckClaimState` and the failed obligation
`A #Equals addF(A, 1.0)`. This is a clean result-sensitivity failure, not a
timeout or unsupported-hook failure.

# Gate B — intent adequacy

PASS.

## B1: input domain

`NumSeq` denotes every finite list containing any mixture of MPY `Int` and
`Float` coefficients. `validCoeffs` imposes exactly the material prompt
conditions: a nonempty even coefficient count (therefore at least two) and a
nonzero highest coefficient. There is no maximum length, coefficient bound,
fixed shape, or example-only restriction.

## B2: language model

The formal theorem is about the supplied MPY semantics, as required by the
task. Its numeric values and opaque symbolic float operations are not a full
model of every CPython numeric corner case. In particular, NaN/infinity,
overflow/conversion exceptions, and arbitrary non-`Int`/`Float` Python numeric
objects are not given a complete CPython model here. These differences are not
silently promoted to claims about CPython.

For ordinary finite real-valued polynomial coefficients—the material HumanEval
domain—the structural theorem covers arbitrary finite input length. Supplied
primitive value opacity is a named trust boundary, not a finite-domain
restriction.

## B3–B4: summary and intended property

The execution-to-summary connection is formally proved. The
summary-to-root interpretation is conditional on the ordinary ordered
arithmetic contracts of the supplied primitive symbols and the standard
odd-degree/bisection argument:

- an even number of coefficients with nonzero last coefficient gives odd
  degree;
- an odd-degree real polynomial has opposite limiting signs;
- doubling symmetric endpoints eventually finds a non-positive endpoint
  product;
- each bisection step preserves a sign-changing bracket;
- the exit guard gives bracket width at most `1e-10`, and the source returns
  its lower endpoint.

Accordingly, the implementation returns a floating approximation, not an
algebraically exact representable zero in every case. That interpretation
matches the prompt's rounded examples. It is independently supported, but the
real-analysis bridge is not claimed as a K theorem.

# Gate C — trust and evidence audit

PASS.

## Trust ledger

| Unproved component | Exact boundary and influence | Dependents | Evidence |
|---|---|---|---|
| Supplied arithmetic primitives | `intToF`, `divII`, `addF`, `subF`, `mulF`, `divF`, `gtF`, and `eqF`; they affect accumulated polynomial values, branch guards, returned values, and termination | `poly-loop-*`, `find-init`, `expand-loop`, `bisect-loop` | They are fixed symbols from `reference-semantics/`; LLVM execution passes both prompt examples |
| Odd-degree and bisection mathematics | Interprets `bracketBegin`, `bracketEnd`, and `bisectFrom` as a root approximation and supplies termination for ordinary finite ordered arithmetic | Human-facing root conclusion only; not the execution theorem | Prompt examples plus 500 deterministic randomized odd-degree cases against an independent direct-power polynomial oracle |
| MPY versus full CPython | The supplied language omits or abstracts some exceptional numeric behavior and nonstandard numeric objects | Any extrapolation beyond MPY | Scope is stated explicitly; no such extrapolation is made |

## Proof-extension record

| Extension | Class and semantic role | Domain and matched context | State/value influence | Justification, dependents, and validation |
|---|---|---|---|---|
| `NumSeq`, `numVals`, `numLen`, `lastNonZero`, `validCoeffs` and their equations | Definitional summaries; encode the symbolic input and precondition | All finite `Int`/`Float` sequences; these functions match only proof-domain terms | Selects input structure and validity; does not replace program execution | Structural definitions. Used by every claim. Constructor coverage is exhaustive |
| `polyStep`, `polyBody`, `expandCond`, `expandBody`, `bisectCond`, `bisectBody`, `findZeroBody`, `solutionModule` | Definitional syntax abbreviations; expose the exact translated AST | Exact terms named in `verification.k`; they unfold to MPY syntax without changing cells or control | Determines the program body and therefore all behavior | Compared mechanically with the generated module by fixed-semantics loading; the material body mutation is rejected |
| Four `numVals` equality simplifications | Derived lemmas; logical constructor no-confusion only | Equality patterns for empty, embedded, `Int`-head, and `Float`-head sequences | Enables symbolic constructor splitting; no operational state effect | Consequences of the disjoint `ValSeq`/`NumSeq` constructors. Used by unbounded list induction |
| `polyAcc`, `polyValue`, `polyPower`, `polyLast` equations | Definitional summaries of polynomial-loop state | Every finite `NumSeq`, arbitrary symbolic `x`, accumulator, power, and last coefficient | Characterizes `value`, `power`, and `coeff` after the loop | Universally connected to fixed execution by the three `poly-loop-*` circularities; false-result mutation is rejected |
| `bracketBegin`, `bracketEnd` equations | Definitional summaries of expansion-loop endpoints | Any symbolic sequence and endpoints; exact source guard or its negation | Affects the endpoints passed to bisection | Universally connected over the exact closure, frame, continuation, and cells by `expand-loop` |
| `bisectFrom` and `solveFrom` equations | Definitional summaries of the bisection result and composition | Any symbolic sequence/endpoints; exact while/if guard partition | Determines the final returned value | `bisect-loop` proves the connection while executing all `poly` calls; `solveFrom` only composes already-connected summaries |
| `find-load`, `find-init`, `poly-loop-*`, `expand-loop`, `bisect-head`, `bisect-loop` | Derived reachability claims/circularities; prove rather than replace execution | The complete configurations in `spec.k`; `poly-loop-*` preserve arbitrary framed state, while root-loop claims use the exact active closure, continuation, and stack | Covers binding, control, all local updates, return, scope/frame cleanup, exceptions, and exit code | All print `#Top`; exact post/pre configurations compose transitively. `bisect-head` is a fixed-semantics staging theorem with no summary |

There are no operational bridges to inventory. Summary symbols occur only in
proof states/postconditions and never preempt a fixed program transition.
Context containment is therefore exact for the root-loop claims and universal
for the explicitly framed coefficient-loop and staging claims. Control
validation consists of the exact fixed-semantics connection claims, concrete
LLVM execution, the source-body identity mutation, and the false-postcondition
mutation.

## Reproducible evidence

Run:

```bash
./prove.sh
```

`prove.sh` contains the exact translator, LLVM compilation, `krun`, identity,
positive proof, randomized validation, and negative mutation commands. The
final run used K `v7.1.293` and Python `3.10.12` and produced:

- concrete `krun`: `.K`, `NoExc`, exit code 0 for both prompt examples;
- identity comparison: generated module equals the module used by the proof;
- source-body mutation: expected identity rejection;
- five positive `kprove` invocations: `#Top`, exit 0;
- `validate.py`: 500/500 seeded cases with normalized residual below `1e-8`;
- false-postcondition mutation: expected `WarnStuckClaimState`, exit 1;
- overall `prove.sh`: exit 0.

Finite tests support the arithmetic/intent bridge; they are not presented as a
universal proof. The universal result is the symbolic fixed-semantics execution
theorem above.
