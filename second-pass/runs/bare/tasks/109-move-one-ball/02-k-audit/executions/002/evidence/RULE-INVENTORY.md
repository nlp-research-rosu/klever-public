# Reviewer rule inventory

This inventory covers every local declaration and rule in
`mpy-syntax.k`, `semantic.k`, and `verification.k`. Imported K built-ins are
listed separately as trust boundaries.

## Local syntax and attributes

- `mpy-syntax.k:7-8`: `Pgm ::= Module(Stmts)` and a zero-separator `Stmts`
  list.
- `mpy-syntax.k:9-14`: statement constructors `FuncDef`, `Return`, `Assign`,
  `If`, and `For`, plus one-string `Params`.
- `mpy-syntax.k:16-24`: expression constructors `Name`, `Int`, `Bool`,
  `UnaryOp`, `BinOp`, `Compare`, unary `Call`, `Subscript`, and `CmpOp`.
- `mpy-syntax.k:27-28`: finite integer-list input constructors `.IList` and
  `Int :: IList`.
- `mpy-syntax.k:31`: nullary `theSolution : Pgm`, `[function,total]`.
- `verification.k:9-14`: `length` (`function,total`), `last` (`function`,
  intentionally partial on empty), `dropBit` (`function,total`), `dropsFrom`
  (`function,total`), `cyclicDrops` (`function,total`), and
  `rotationSortable` (`function,total`).
- `semantic.k:9`: value wrappers `iVal`, `bVal`, and `listVal`.
- `semantic.k:11-20`: computation items `exec`, `execStmt`, `eval`, `branch`,
  `assignTo`, `addRight`, `addValues`, `compareRight`, `compareValues`,
  `getLength`, `getLast`, `isEmpty`, `startFor`, `loop`, `bind`, and
  `doReturn`.
- `semantic.k:22-25`: configuration cells `<k>`, `<input>`, and `<env>`.
- The only explicit priority attribute is `[priority(40)]` on the
  constructor-sensitive `len(E) == 0` rule at `semantic.k:97-99`.
- The only `owise` rule is generic nonempty loop iteration at
  `semantic.k:66-68`.
- There are no local `[simplification]`, `[anywhere]`, macro, opaque-symbol,
  or explicit `[functional]` declarations. K's function productions generate
  their normal function/functional machinery.

## Rules in `mpy-syntax.k` (1)

| ID | Location | Rule and classification | Review |
|---|---|---|---|
| M1 | 32-47 | `theSolution => Module(FuncDef(...))`; definitional program-term constant | Total and non-overlapping. Reviewer KAST comparison found its constructor RHS identical to trusted regeneration of `solution.mpy`. |

## Rules in `verification.k` (11)

| ID | Location | Rule | Review |
|---|---|---|---|
| V1 | 16 | `length(.IList) => 0` | True base equation. |
| V2 | 17 | `length(_I :: IS) => 1 +Int length(IS)` | True recursive equation; structurally descending and disjoint from V1. |
| V3 | 19 | `last(I :: .IList) => I` | True singleton equation. |
| V4 | 20 | `last(_I :: J :: IS) => last(J :: IS)` | True, structurally descending, and disjoint from V3. Empty input remains deliberately undefined. |
| V5 | 22 | `dropBit(I,J) => 1 requires I >Int J` | True guarded equation. |
| V6 | 23 | `dropBit(I,J) => 0 requires I <=Int J` | True; guard is disjoint from and exhaustive with V5 on mathematical integers. |
| V7 | 25 | `dropsFrom(_, .IList) => 0` | True fold base. |
| V8 | 26-27 | `dropsFrom(P,I::IS) => dropBit(P,I) +Int dropsFrom(I,IS)` | True fold step; structurally descending and disjoint from V7. |
| V9 | 29 | `cyclicDrops(.IList) => 0` | True empty base. |
| V10 | 30 | `cyclicDrops(I::IS) => dropsFrom(last(I::IS),I::IS)` | True definition of circular strict descents; `last` is defined on this guarded nonempty shape. |
| V11 | 34 | `rotationSortable(L) => cyclicDrops(L) <=Int 1` | Total definition, not itself a theorem that the name matches the HumanEval contract. The distinct-list equivalence is an informal intent bridge audited separately. |

## Rules in `semantic.k` (36)

| ID | Location | Rule or family member | Review |
|---|---|---|---|
| S1 | 28-30 | Start the sole unary function and bind its argument to `<input>` | Matches the submitted one-function module. It intentionally defines program launch rather than general Python module execution. |
| S2 | 32 | `exec(.Stmts) => .K` | Correct empty statement sequence. |
| S3 | 33 | Split a nonempty statement list into head execution then tail execution | Preserves left-to-right statement order. |
| S4 | 35 | Assignment evaluates RHS before assignment | Correct for the used name assignment. |
| S5 | 36-37 | Store an evaluated value with map update | Correct overwrite behavior; only `<env>` changes. |
| S6 | 39 | Evaluate an `If` guard before choosing a branch | Correct control order. |
| S7 | 40 | True guard executes `THEN` | Correct and disjoint from S8. |
| S8 | 41 | False guard executes `ELSE` | Correct and disjoint from S7. |
| S9 | 43-44 | Evaluate a `For` iterable before loop start | Correct for the used list iteration. |
| S10 | 45 | Convert a list value to `loop(X,L,BODY)` | Correct setup. |
| S11 | 46 | Empty loop completes | Correct zero-iteration boundary. |
| S12 | 51-63 | Exact-body nonempty-loop summary using `dropsFrom`, `last`, and map update | Operational bridge. Its input/body match, continuation framing, and state result agree with induction over S13/S14 plus the ordinary statement rules. It is result-bearing and shares `dropsFrom` with the postcondition. No candidate bridge-free universal theorem is supplied. Reviewer bridge-free concrete runs agreed; a broad symbolic connection attempt stuck on symbolic `Map REST`, and a reachable-shape attempt was interrupted after about 120 seconds. This is an evidence/trust-boundary limitation, not an identified false rule; no false-conclusion witness was found. |
| S13 | 66-68 | Generic nonempty iteration: bind head, execute body, recur on tail; `[owise]` | Correct structurally descending iteration. `owise` lets S12 preempt only its exact body/domain. |
| S14 | 69-70 | Bind loop variable in the environment | Correct overwrite semantics. |
| S15 | 72 | Evaluate a return expression before return control | Correct. |
| S16 | 73 | A returned value discards a nonempty remaining top-level statement continuation | Correct for the modeled single function; no call stack exists. It is broader than the submitted top-level context but does not create a false result for any used construct. |
| S17 | 74 | A returned value with no remaining continuation becomes the result | Correct. |
| S18 | 76 | Integer literal evaluation | Correct. |
| S19 | 77 | Boolean literal evaluation | Correct. |
| S20 | 78-79 | Name lookup from `<env>` | Correct; missing names visibly stick rather than fabricate values. |
| S21 | 81 | Used unary minus form on integer literals | Correct over mathematical integers. |
| S22 | 83-84 | Begin binary addition by evaluating the left operand | Correct left-to-right order. |
| S23 | 85 | Evaluate addition's right operand after preserving the left integer | Correct. |
| S24 | 86 | Add two evaluated integers | Correct. |
| S25 | 88-89 | Begin comparison by evaluating the left operand | Correct left-to-right order. |
| S26 | 90-91 | Evaluate comparison's right operand after preserving the left value | Correct. |
| S27 | 92 | Integer equality result | Correct operand orientation (symmetric). |
| S28 | 93 | Integer greater-than result | Correct: preserved left `I >Int` newly evaluated right `J`. |
| S29 | 94 | Integer less-than-or-equal result | Correct: preserved left `I <=Int` right `J`. |
| S30 | 97-99 | Specialized `len(E) == 0` to list emptiness, priority 40 | Equivalent to the generic length/equality path for list values and crucial for symbolic list case splitting. Non-list values stick rather than yield a fabricated result. |
| S31 | 100 | Empty list is empty | Correct. |
| S32 | 101 | Constructor-nonempty list is not empty | Correct and disjoint from S31. |
| S33 | 103 | Evaluate the argument of used `len` call | Correct. |
| S34 | 104 | List length via `length` | Correct, with V1/V2 fixing the result. |
| S35 | 106 | Evaluate the base of the used `[-1]` subscript | Correct for the only subscript form in the program. |
| S36 | 107 | Return `last(L)` | Correct for nonempty `L`; empty `L` visibly sticks because `last(.IList)` has no equation. The program's empty branch prevents this on all entry-claim executions. |

## Construct coverage

The submitted `solution.mpy` uses `Module`, `FuncDef`, `Params`, statement
lists, `If`, `Return`, `Assign`, `For`, `Name`, `Int`, `Bool`, `UnaryOp("-")`,
`BinOp("+")`, `Compare` with `==`, `>`, and `<=`, unary `Call(Name("len"),...)`,
and `Subscript(...,-1)`. M1 pins that exact tree. S1-S36 provide every material
launch, binding, evaluation, control, state, call, return, and result step used
by it. Unsupported unused Python constructs have no rules and therefore stop
visibly, which is acceptable for generated minimal semantics.

## Imported trust boundary

`INT`, `BOOL`, `MAP`, their syntax modules, K sequencing, finite K lists, and
the Haskell/LLVM backends are trusted primitives. No local rule is classified
as materially unsound, so there is no false-conclusion witness to report.
