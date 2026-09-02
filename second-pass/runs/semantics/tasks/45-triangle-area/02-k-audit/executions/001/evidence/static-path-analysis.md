# Static path and rule assessment

This is the reviewer-authored assessment paired with `k-rule-inventory.md`.
Line references below use the immutable scratch snapshot copied from
`/candidate`; Stage 1 established byte identity of its supplied-semantics tree
with `/reference/reference-semantics`.

## Exhaustive-inventory disposition

`k-rule-inventory.md` enumerates all 1,102 top-level declarations in the 24
supplied-semantics K files, `verification.k`, and `spec.k`: 228 syntax
declarations, 696 rules, 147 function declarations, 108 declarations marked
`total`, 45 priority-bearing rules, 26 `owise` rules, 22
`no-evaluators` declarations, 36 concrete-only rules, five contexts, one
configuration, and one claim. There are no `functional` or `simplification`
attributes.

For this theorem, the initial configuration and exact constructor tree make
every operational rule outside the path listed below unreachable: there are no
lists, dictionaries, strings, sets, tuples, loops, conditionals,
comprehensions, imports, methods, builtins calls, assertions, user heap
objects, closure cells, or float operands in `solution.mpy`. Their sorts,
constructor heads, call targets, or continuation forms therefore do not unify
with any reachable redex. Those fixed supplied-semantics rules cannot affect
this claim. I found no overlap from an out-of-path rule onto a reachable redex.

Within the reachable path, the rules below are either the fixed semantics'
ordinary execution rules or the candidate's one exact program constant.
The candidate adds no priority rule, simplification, operational bridge,
auxiliary claim, or result oracle.

## Program syntax mapped to declarations and rules

| Submitted construct | Declaration | Reachable semantics | Assessment |
|---|---|---|---|
| `Module(...)` | `semantics/syntax.k:61` | `semantics/core.k:124-127` | Loads the exact statement list and sequences it left-to-right. |
| `FuncDef("triangle_area", ...)` | `semantics/syntax.k:53` | `semantics/functions.k:14-16` | Installs a closure containing the submitted parameters and body in module scope 0. |
| `Params("a","h")` | `semantics/syntax.k:57,60` | `semantics/functions.k:63-66` | Binds the two already-evaluated actual arguments, in order, in the fresh call scope. The closure-cell competitor at lines 68-75 is disabled because this plain frame has no `$cells`. |
| `Return(...)` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78-90` | Evaluates the expression, records the returned value, drops the remaining callee computation, restores the exact caller continuation/environment, removes the callee frame, and restores `scopeLoc`. |
| `BinOp("*",...)`, `BinOp("/",...)` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | `semantics/operators.k:12`; `semantics/int.k:14`; `semantics/float.k:30-32` | Left then right evaluation; integer multiplication is mathematical `*Int`; integer true division returns the supplied primitive `divII`. Heap-reference priority rules do not match integer operands. |
| `Name("a")`, `Name("h")` | `semantics/syntax.k:12` | `semantics/core.k:130-154` | Starts lookup at the fresh call scope and selects the bound integer. The cell-read priority rule is disabled by absence of `$cells`; parent traversal is unnecessary because both names are present. |
| `Int(2)` and call arguments `Int(A)`, `Int(H)` | `semantics/syntax.k:9` | `semantics/core.k:194` | Faithful injection of K integers. |
| `Call(Name("triangle_area"),...)` | `semantics/syntax.k:28` | `semantics/call.k:19-21,69-74`; `semantics/core.k:185-191,213-215` | Evaluates the actual binding, evaluates arguments left-to-right, selects the installed closure, allocates a fresh frame, saves the whole caller continuation, and later restores it. No builtin/method/math interception matches this callee. |

Configuration fields are declared at `semantics/core.k:49-60`. Along this
program path: the module binding is added and retained; one fresh call scope is
added then removed; `env` and `scopeLoc` return to 0 and 1; heap, heap location,
exception, and exit code never change; the saved stack frame is consumed; and
`ret` returns to `noRet`. These are exactly the cells constrained by `spec.k`.

## Candidate-local proof extension

`verification.k:7-11` declares the nullary function
`triangleAreaProgram` and its sole, unconditional equation. The right-hand
side is constructor-for-constructor identical to `solution.mpy`; the trusted
translator regeneration was byte-identical. The equation is a definitional
program constant, not an operational bridge or answer summary. It is
terminating, has no arguments, has no competing equation, and its sole rule
covers its complete domain. Its only dependent is the entry claim.

## Opaque and trusted symbols

The inventory contains 22 supplied `no-evaluators` primitives. Exactly one is
reachable here: `divII(Int,Int)` at `semantics/float.k:30`. The execution rule
at line 32 maps integer `/` to that same term; the concrete-only equation at
line 31 maps it to binary64 conversion and division for LLVM execution.

`divII` is result-bearing: it is the entire returned value and the entire
postcondition. The proof is interpretation-parametric in this supplied
primitive—it establishes that the program returns `divII(A*H,2)`, not a
standalone numerical theorem about its value. This is a low-level external
division boundary rather than a candidate-created oracle, but any claim that
it exactly models CPython for every unbounded integer requires separate
validation.

That bridge fails at two concrete boundaries:

- Let
  `N = (2**53 - 1) * 2**972`, written as one integer literal in the preserved
  test. The generated Python program's integer/integer true division returns
  the largest finite binary64 value, `1.7976931348623157e308`, but the supplied
  semantics fails an assertion demanding that value. Its concrete `divII`
  equation first converts the oversized numerator to binary64 and then divides,
  which does not model CPython's scaled integer/integer division. See
  `python-division-scaling-boundary.log` (exit 0) and
  `krun-division-scaling-boundary.log` (`AssertionError`, exit 1).
- With `A=10**400`, `H=1`, generated Python raises `OverflowError`, while fresh
  LLVM execution of the supplied semantics reaches `NoExc` and exit code 0.
  See `python-huge-boundary.log` and `krun-huge-boundary.log`.

Thus the supplied total/no-exception treatment of `divII` enables false
conclusions about both the returned value and normal completion on satisfying
formal inputs.

All other opaque symbols are unreachable from the exact syntax and values of
this program, so they have no dependent branch, state, exception, or
postcondition in this claim.

## Overlap, priority, totality, and simplification findings

- The reachable plain-name and plain-parameter rules have guarded,
  higher-priority closure-cell competitors; their guards are false in the
  freshly allocated plain frame.
- The generic call rule is `owise`; no special Attribute, builtin, method,
  math, or hash call has a matching head.
- Integer multiplication and integer division are sort- and operator-disjoint.
- `triangleAreaProgram` is total with one exact equation and no overlap.
- `builtinsScope`, `appendVal`, and the small recursive helpers used on this
  path have structurally descending, covering equations.
- No candidate-local or supplied rule used by the proof carries a
  `simplification` attribute.
- No reachable priority rule bypasses function-body execution.

The two concrete false-behavior witnesses above are on the formal integer
domain. I do not label unreachable baseline rules unsound without a witness
connecting them to an entry state of this theorem.
