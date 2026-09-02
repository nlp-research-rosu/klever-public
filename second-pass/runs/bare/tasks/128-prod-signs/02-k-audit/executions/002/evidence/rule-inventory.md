# Exhaustive local K inventory and static disposition

Source hashes and line numbers refer to the immutable candidate files. There
are no generated helper K files beyond `semantic.k`; `verification.k` is the
only proof-local definition imported by `spec.k`.

## Syntax and configuration inventory

`semantic.k:1-35` declares:

- `Pgm`: `Module(Stmts)`.
- List nonterminals: `Stmts` (empty separator), `Exprs`, `CmpOps`, `Strings`,
  and `Ints`.
- `Params(Strings)`.
- `Stmt`: `FuncDef`, `Return`, `Assign`, `If`, and `For`.
- `Expr`: `Name`, `Int`, `ListExpr`, `BinOp`, `UnaryOp`, `Compare`, and
  `NoneVal`.
- `CmpOp`.
- `Value`: the `Int` and `Bool` subsorts plus `none` and `listVal(Ints)`.
- `Input`: `input(Ints)`.

`semantic.k:44-69` declares:

- `Function`: `.Function` and `function(String, Stmts)`.
- `Result`: `noResult` and `result(Value)`.
- Configuration `<mpy>` with `<k>`, `<input>`, `<function>`, `<env>`, and
  `<result>` cells. Every non-`<k>` cell is read or written by at least one
  actual-program rule or claim.
- Fourteen internal `KItem` forms: `boot`, `exec`, `start`, `eval`, `store`,
  `bind`, `branch`, `binLeft`, `binRight`, `cmpLeft`, `cmpRight`, `forStart`,
  `loop`, and `returnK`.

`verification.k:7-11,32,42,53` declares:

- Five `[function, total]` result functions: `magnitude`, `integerSign`,
  `sumMagnitudes`, `productSigns`, and `contract`.
- Three zero-arity `[function]` program constants: `solutionLoopBody`,
  `solutionBody`, and `solutionProgram`.

There are no local `[functional]` declarations, opaque symbols, priorities,
`[simplification]` rules, or `[concrete]` rules.

## Construct coverage for `solution.mpy`

| Submitted construct | Declaration | Operational coverage |
|---|---|---|
| `Module`, one `FuncDef`, one parameter | `semantic.k:6,14,16` | S1, S4, S5 below |
| Statement sequencing and empty statement list | `semantic.k:8` | S2-S3 |
| `If` | `semantic.k:19` | S11-S13 |
| `Compare` with one `<` or `==` comparator | `semantic.k:27,30` | S31-S36 |
| `Name` lookup | `semantic.k:22` | S23 |
| Empty `ListExpr` | `semantic.k:24` | S22 |
| `Return` and `NoneVal` | `semantic.k:17,28` | S18-S21 |
| Assignment to a name | `semantic.k:18` | S6-S10 |
| Integer literals | `semantic.k:23` | S20 |
| `For` over the input integer list | `semantic.k:20` | S14-S17 |
| Binary `+`, `-`, `*` | `semantic.k:25` | S25-S29 |
| Unary `-` | `semantic.k:26` | S24, S27/S30 |

Every construct in the submitted term has both syntax and a terminating
operational path on list-of-integer inputs. Deliberately unsupported unused
forms (for example nonempty source `ListExpr` evaluation, multi-comparator
chains, other operators, other function names, and multiple parameters) stop
instead of fabricating a value.

## `semantic.k` rule inventory

All rules are ordinary operational rules. “Sound” means sound for the
individually generated language level and the actual program's intended
list-of-unbounded-integers domain.

| ID | Lines | Rule / role | Static disposition |
|---|---:|---|---|
| S1 | 71 | `boot(Module(SS)) => exec(SS) ~> start` | Sound: orders module definition before entry invocation. |
| S2 | 73 | `exec(.Stmts) => .K` | Sound list base case. |
| S3 | 74 | `exec(S SS) => S ~> exec(SS)` | Sound, left-to-right statement order. |
| S4 | 76-77 | matching `prod_signs` definition installs `function(P,BODY)` | Sound for the sole submitted one-parameter definition; other definitions visibly stop. |
| S5 | 79-82 | `start` installs the input list in a fresh local environment and executes the body | Sound entry-harness bridge for the submitted one-argument function. It resets the local environment and preserves input/function/result cells. |
| S6 | 84 | name assignment evaluates RHS before `store` | Sound evaluation order. |
| S7 | 85-86 | update an existing binding | Sound map update. |
| S8 | 87-89 | insert a missing binding | Sound; guard is disjoint from S7. |
| S9 | 91-92 | update an existing loop binding | Sound map update. |
| S10 | 93-95 | insert a missing loop binding | Sound; guard is disjoint from S9. |
| S11 | 97 | evaluate `If` guard before branching | Sound. |
| S12 | 98 | true branch | Sound. |
| S13 | 99 | false branch | Sound and disjoint from S12. |
| S14 | 101 | evaluate `For` iterable before iteration | Sound. |
| S15 | 102 | an integer-list value starts a loop | Sound for the input domain. |
| S16 | 103 | empty loop tail terminates | Sound base case. |
| S17 | 104 | bind head, execute body, then recur on tail | Sound list order and state flow. |
| S18 | 106 | evaluate a return expression before `returnK` | Sound. |
| S19 | 107-108 | consume the active continuation and set the result | Sound abrupt function return for this single-frame language. It is guarded by `noResult`; no call stack, cleanup, exceptions, heap, or output exist in the model. |
| S20 | 110 | integer literal evaluates to its K integer | Sound. |
| S21 | 111 | `NoneVal` evaluates to `none` | Sound. |
| S22 | 112 | empty source list evaluates to empty `listVal` | Sound and exactly the only submitted list literal. |
| S23 | 113-114 | name lookup from `<env>` | Sound. |
| S24 | 116 | unary operation evaluates its operand and stores left operand `0` | Sound for submitted unary `-`; unsupported unary strings stop. |
| S25 | 117 | binary operation evaluates left operand first | Sound. |
| S26 | 118 | then evaluates right operand with the left value saved | Sound. |
| S27 | 120 | integer addition | Sound unbounded-integer operation. |
| S28 | 121 | integer subtraction | Sound unbounded-integer operation. |
| S29 | 122 | integer multiplication | Sound unbounded-integer operation. |
| S30 | 123 | unary minus as `0 - I` | Sound; its overlap with S28 at saved left operand `0` has the identical RHS. |
| S31 | 125 | comparison evaluates its left expression first | Sound. |
| S32 | 126-127 | a single comparator evaluates its right expression with the left value saved | Sound for every submitted comparison; longer chains visibly stop. |
| S33 | 129 | integer `<` | Sound. |
| S34 | 130 | integer `==` | Sound. |
| S35 | 131 | empty list equals empty list | Sound. |
| S36 | 132 | a nonempty input list compared with the submitted empty literal is false | Sound in the `arr == []` evaluation orientation: current/right value is empty, saved/left value is nonempty. The semantics is intentionally incomplete, not falsely defined, for other list comparisons that the program does not use. |

No rule above replaces a program-defined calculation with an oracle or task
answer. S1-S36 execute all material operations. S5 is the only entry-harness
bridge; it maps `input(IS)` to a Python-like argument value `listVal(IS)`.

## `verification.k` rule inventory

| ID | Lines | Rule / role | Class and static disposition |
|---|---:|---|---|
| V1 | 13 | negative `magnitude(I) = 0-I` | Truthful definitional summary. |
| V2 | 14 | nonnegative `magnitude(I) = I` | Truthful; V1/V2 guards are disjoint and exhaustive. |
| V3 | 16 | negative `integerSign = -1` | Truthful definitional summary. |
| V4 | 17 | `integerSign(0) = 0` | Truthful. |
| V5 | 18 | positive `integerSign = 1` | Truthful; V3-V5 are pairwise disjoint and exhaustive. |
| V6 | 20 | empty `sumMagnitudes = 0` | Truthful recursive base. |
| V7 | 21 | head/tail magnitude sum | Truthful and structurally descending. |
| V8 | 23 | empty `productSigns = 1` | Truthful recursive base. |
| V9 | 24 | head/tail sign product | Truthful and structurally descending. |
| V10 | 26 | empty `contract = none` | Truthful prompt clause. |
| V11 | 27-28 | nonempty contract is magnitude sum times sign product | Truthful; disjoint from V10 and covers all `Ints`. |
| V12 | 33-40 | `solutionLoopBody` constructor constant | Sound definitional macro; it names but does not replace execution. |
| V13 | 43-51 | `solutionBody` constructor constant | Sound definitional macro. |
| V14 | 54-56 | `solutionProgram` constructor constant | Sound definitional macro. |

The `[total]` declarations V1-V11 have complete, non-overlapping coverage as
listed. V12-V14 each have exactly one zero-arity equation. Mechanical KAST
comparison in `10-program-term-compare.log` confirms their fully expanded
constructor term is identical to trusted-regenerated `solution.mpy`.

## Fixed-semantics and proof-local trust boundary

- Trusted built-ins: K `INT`, `BOOL`, `STRING`, and `MAP`, including unbounded
  integer arithmetic/comparisons, Booleans, string equality used for fixed
  constructor tags and names, finite map lookup/update, and list constructors.
- Entry representation: an external list of Python integers is represented as
  `input(IS)` and bound as `listVal(IS)`. This affects the argument value but
  does not insert a task result. Static structural review plus
  `06-k-semantics-differential.log` supports the bridge on 12 normal/boundary
  cases; those tests are finite evidence.
- Program constants V12-V14 are not opaque and do not bypass evaluation.
- There are no empirical or opaque result-bearing proof primitives.

No materially unsound local rule was found, so there is no false-conclusion
witness to report for a rule. The candidate's decisive defect is theorem
coverage, documented separately, rather than a false semantic equation.
