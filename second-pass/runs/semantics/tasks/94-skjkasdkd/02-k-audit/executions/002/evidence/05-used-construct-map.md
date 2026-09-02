# Material constructor-to-rule map

The complete 1,160-sentence inventory is in `05-rule-inventory.md` and
`05-rule-inventory.json`.  This file maps every constructor occurring in the
submitted `solution.mpy` to the material rules that execute it.

| Submitted constructor/operation | Declaration | Material execution |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `semantics/syntax.k:53,57,61`; `semantics/core.k:124-127` | `#loadAll` exposes statements; `semantics/functions.k:14-16` binds the exact closure |
| Function `Call` | `semantics/syntax.k:28`; `semantics/call.k:19-21,69-74` | Candidate `verification.k:142-164` is an exact binding/evaluation specialization; `verification.k:307-339` summarizes only frame allocation, parameter binding, five literal initializations, and one-time `For` iterable evaluation |
| `Assign(Name, Int/Bool/Name/Compare)` | `semantics/syntax.k:41`; `semantics/controls.k:9-18` | `verification.k:31-53,119-125,166-176` preserves RHS evaluation and performs the same current-frame map update |
| `Name` | `semantics/syntax.k:12`; `semantics/core.k:130-154` | `verification.k:18-29` specializes lookup to the already-pinned current plain frame; `$cells` guards exclude closure-cell behavior |
| `For` and list iteration | `semantics/syntax.k:45`; `semantics/controls.k:62-74`; `semantics/list.k:9-10` | `verification.k:134-140` specializes iterable lookup; `verification.k:186-190` gives empty/cons iterator behavior for the unbounded proof input representation `asVals(IntList)` |
| `If` and branch | `semantics/syntax.k:49`; `semantics/controls.k:50-54` | Fixed rules after comparison evaluation; `verification.k:111-117` directly specializes `If(Name(...))` |
| `While` | `semantics/syntax.k:46`; `semantics/controls.k:76-82` | Fixed `#while/#whileCond/#loopLbl` control. `prime-loop` and `digit-loop` are circularities at the real `#while` loop head |
| `BoolOp("and",...)` | `semantics/syntax.k:16`; `semantics/bool.k:16-25` | Fixed left-to-right short circuit, preserving the source guard's avoidance of modulo after `prime` becomes false |
| `Compare`, `CmpOp` | `semantics/syntax.k:30,32`; `semantics/operators.k:14-20`; `semantics/int.k:22-27` | `verification.k:91-109` specializes Name/Name and Name/Int cases; compound arithmetic operands use fixed evaluation contexts then integer comparison |
| `BinOp("*","%")` | `semantics/syntax.k:15`; `semantics/operators.k:12`; `semantics/int.k:14-15,19-20` | Left-to-right strict evaluation, unbounded integer multiplication, and Python-style modulo; reachable divisors are at least 2 |
| `AugAssign("+","//")` | `semantics/syntax.k:44`; `semantics/controls.k:20-31`; `semantics/int.k:9,16` | `verification.k:55-73` is the same plain-frame update. Used floor divisors are positive (`10` and divisor increment), matching Python |
| `Return` and frame pop | `semantics/syntax.k:50`; `semantics/functions.k:77-90` | `verification.k:127-132` specializes only Name evaluation; fixed `Return/#pop` restores caller env, removes the callee scope, resets `scopeLoc`, and preserves heap allocation state |

## Configuration, order, and state

- The `main-correct` claim fixes every supplied configuration cell.  The
  function is read-only on its argument and allocates no heap object because
  the supplied semantics explicitly permits bare read-only `list(ValSeq)`
  inputs in claims.
- Argument order and expression order are supplied `strict`/`seqstrict`
  order.  Every candidate shortcut requires already-resolved values in the
  current frame and performs the same update, so it does not reorder a
  side-effecting expression.
- The call bridge's LHS has no continuation suffix and an empty stack.  Its
  fixed counterpart therefore pushes `frame(.K,0,1)`.  It changes exactly
  `<env>`, `<scopes>`, `<scopeLoc>`, and `<stack>`; all other cells are framed
  and unchanged.
- The proof imports `MPY`, not `MPY-CONCRETE`; the 24 concrete-only local
  sentences are not in the proof theory.

## Candidate-local decision summary

- Twenty map/name/assignment/control/call rules are guarded specializations of
  fixed supplied rules.  Their complete LHS/RHS/guard text and individual
  decisions appear in the inventory.
- Two iterator rules are constructor-complete for `.IntList`/`intCons`; they
  define an input representation, not a result oracle.
- Nineteen declarations/rules define `trialPrime`, `trialDivisor`, `isPrime`,
  `largestPrime`, `digitAcc`, and `digitSum`.  Guards are disjoint on the
  reachable domain; recursions advance the divisor, shrink the list, or divide
  a positive integer by 10.
- Fourteen macro declarations/rules are AST constructors.  `04-kast-compare.log`
  establishes exact expansion of the full submitted module.
- One operational prefix bridge (`verification.k:307-339`) has no candidate
  bridge-free universal connection theorem.  Static composition and the
  bridge-free ground outcomes `1 -> 0`, `2 -> 2`, and `13 -> 4` support it,
  but finite cases do not replace that missing theorem.

## Narrow totality limitation

`trialPrime` and `trialDivisor` are declared `[total]` for all integer
divisors, but their modulo branch is not Python-defined at `D = 0`.
Every claim-reachable call has `D >= 2`, so this cannot affect the target
theorem.  The ground probes in `05-totality-*.log` document the over-broad
declarations: the theory reduces `trialPrime(0,0,true)` to `true` and
`trialDivisor(0,0,true)` to `1`; neither case is reachable from the submitted
program on any integer-list input.
