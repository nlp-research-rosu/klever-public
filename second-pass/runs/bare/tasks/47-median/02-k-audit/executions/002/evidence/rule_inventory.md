# Exhaustive local K inventory

Source line numbers refer to the immutable candidate copies:
`/candidate/semantic.k` and `/candidate/verification.k`.

## Local syntax, cells, and declarations

- `semantic.k:9-31`: constructor syntax for `Module`; K-list `Stmts`;
  `FuncDef`, `Assign`, `If`, `Return`; one-parameter `Params`; `Name`, `Int`,
  `Call`, `BinOp`, `Subscript`; and integer-list constructors `nil`/`cons`.
  These cover every constructor in `solution.mpy`. K's `List{Stmt,""}`
  generates the empty/list sequencing syntax used as `.Stmts` and juxtaposition.
- `semantic.k:39-47`: values `intVal`, result-bearing opaque pair
  `floatVal`, and `listVal`; persistent environments `.Env`/`bind`; execution
  results `next`/`returned`; result slot `noResult` or `Val`.
- `semantic.k:49`: `lookup` `[function]`, deliberately partial on `.Env`.
- `semantic.k:54`: `evalExpr` `[function]`, deliberately partial outside the
  submitted constructor subset.
- `semantic.k:66-70`: `[function]` declarations for `sortVal`, `lenVal`,
  `subscriptVal`, `binopVal`, and `ifVal`.
- `semantic.k:85-88`: `lenInts`, `nthInt`, `sortInts`, and `insertInt` are all
  declared `[function,total]`. `nthInt` is not actually exhaustive.
- `semantic.k:106-108`: `[function]` declarations for `evalBody`,
  `continueWith`, and `chooseBody`.
- `semantic.k:139-144`: configuration cells are `<k>`, immutable `<input>`,
  and `<result>`. There is no heap, output, exception, call-stack, or float
  state.
- `verification.k:7-8`: proof-local `[function]` declarations
  `promptMedian` and `promptMedianSorted`.
- There are no local `[functional]` declarations, simplification rules,
  priority attributes, explicit opaque-function attributes, or auxiliary
  reachability claims. The three reachability claims are in `spec.k`.

## Construct-to-rule map for `solution.mpy`

| Used constructor | Declaration | Behavior |
|---|---|---|
| `Module` | `semantic.k:9` | R36 selects the exact `median` binding |
| `FuncDef`, `Params` | `13-19` | R36 binds input to parameter `l` |
| statement sequence | `11` | R27-R31 execute statements |
| `Assign` | `15` | R28 prepends a binding |
| `If` | `16` | R30 fast path and R31-R35 general path |
| `Return` | `17` | R29/R30 create `returned`; R37 writes result |
| `Name` | `21` | R04 and R01-R02 perform lookup |
| `Int` | `22` | R03 creates `intVal` |
| `Call(sorted,...)` | `23` | R05, R09, R22-R26 |
| `Call(len,...)` | `23` | R06, R10, R18-R19 |
| `BinOp("//",...)` | `24` | R08, R13 |
| `BinOp("%",...)` | `24` | R08, R14 |
| `BinOp("+",...)` | `24` | R08, R12 |
| `BinOp("/",...)` | `24` | R08, R15 |
| `Subscript` | `26` | R07, R11, R20-R21 |

## Rule-by-rule decisions

| ID | Lines | Rule and decision |
|---|---:|---|
| R01 | 50 | Nearest matching environment binding is returned. Sound. |
| R02 | 51-52 | Lookup skips a different key under a disjoint string guard. Sound. |
| R03 | 55 | Integer AST literal becomes the same mathematical integer. Sound. |
| R04 | 56 | Name lookup delegates to R01-R02. Sound for bound names used here. |
| R05 | 57-58 | Textual `sorted` calls insertion sort. Binding is pinned rather than dynamically looked up, but the submitted module cannot rebind the builtin; sound in this exact program context. |
| R06 | 59-60 | Textual `len` calls list length. Same binding observation as R05; sound here. |
| R07 | 61-62 | Subscript evaluates receiver/index through R11. Sound only for modeled nonnegative in-range integer indexing. |
| R08 | 63-64 | Binary operations delegate to R12-R15. Pure recursive representation does not model Python exception/evaluation effects; source operands here are pure, but R15 remains materially wrong. |
| R09 | 72 | `sortVal(listVal(IS))` invokes insertion sort. Sound. |
| R10 | 73 | `lenVal(listVal(IS))` invokes structural length. Sound. |
| R11 | 74 | List indexing wraps `nthInt`. Sound in range; it silently lacks Python exception behavior out of range. |
| R12 | 76 | Integer addition uses `+Int`. Sound for Python integers. |
| R13 | 77 | Floor division is used only on nonnegative list lengths with divisor 2, where K `/Int` agrees with Python `//`. Sound on all submitted uses. |
| R14 | 78 | Remainder is used only on nonnegative list lengths with divisor 2. Sound on all submitted uses. |
| R15 | 80 | **Unsound Python bridge.** It claims every integer `/` returns an exact `floatVal(I,J)`, omitting IEEE-754 rounding and overflow. Witness: four `10**400` inputs satisfy the main precondition; Python raises `OverflowError`, while clean `krun` consumes `<k>` and returns `floatVal(2*10**400,2)` (`concrete_checks.log`). |
| R16 | 82 | Integer zero selects else. Sound for the used modulo condition. |
| R17 | 83 | Nonzero integer selects then under a disjoint guard. Sound. |
| R18 | 90 | Empty integer list has length zero. Sound. |
| R19 | 91 | Cons length is one plus tail length. Sound and descending. |
| R20 | 93 | Index zero returns head. Sound. |
| R21 | 94-95 | Positive index recurses on tail and decrements. Sound when an element exists, but has no rule when the tail becomes empty. |
| R22 | 98 | Sorting empty list returns empty. Sound. |
| R23 | 99 | Sorting cons inserts its head into sorted tail. Sound and descending. |
| R24 | 100 | Insert into empty list produces singleton. Sound. |
| R25 | 101-102 | Insert before a greater/equal head. Sound. |
| R26 | 103-104 | Insert after a smaller head and recurse. Sound; guard is disjoint from R25 and recursion descends. |
| R27 | 110 | Empty body returns the current environment. Sound. |
| R28 | 111-112 | Assignment evaluates the expression and prepends the new binding. Sound for name targets and pure expressions used here. |
| R29 | 113 | Return evaluates its expression and discards the remaining statements. Sound. |
| R30 | 118-126 | Fast path for an `if` whose two branches immediately return. It overlaps R31, but on supported pure expressions and integer truth values both paths converge to the same branch result and discard the same continuation. No false witness was found on the accepted match domain; sound for this program. |
| R31 | 129-130 | General `if` delegates to R32-R35. Sound for supported integer conditions. |
| R32 | 131-132 | Zero evaluates the else body then continuation. Sound. |
| R33 | 133-135 | Nonzero evaluates the then body under a disjoint guard. Sound. |
| R34 | 136 | A return discards the enclosing continuation. Sound. |
| R35 | 137 | Normal completion continues with remaining statements. Sound. |
| R36 | 146-149 | Exact module/function/parameter binding begins body evaluation on the input list. It matches the submitted singleton module and preserves input/result cells. Sound for the exact program. |
| R37 | 151-152 | A returned value consumes `<k>` and writes the previously empty result slot. Sound. |
| V01 | `verification.k:10` | Defines `promptMedian` by sorting. As a definition it is terminating, but it is not an independently proved bridge to the trusted canonical. |
| V02 | `verification.k:11-18` | Defines the proof result by the same odd branch and the same **wrong upper-pair even branch** as the submission. It is a well-formed definitional summary on the claim's restricted domain, but illegitimate as the source-contract reference. Witness `[1,2,3,4]`: V02/submission yield `floatVal(7,2)` / `3.5`; trusted canonical yields `2.5` (`precondition_witnesses.log`). |

## Totality and opaque-result findings

- `lenInts`, `sortInts`, and `insertInt` have complete, descending equations;
  their `[total]` attributes are justified.
- `nthInt` is declared `[total]` but has no equation for `nthInt(nil,N)` or
  negative indices. The clean LLVM build emits a non-exhaustive-match warning.
  Clean `krun` aborts at `nthInt(nil,0)` on empty and length-two inputs.
  Nevertheless, the Haskell prover closes the reviewer claim that the
  length-two program consumes `<k>` and returns
  `floatVal(10 +Int nthInt(nil,0),2)`. Python raises `IndexError`. This is a
  concrete false-normal-return conclusion enabled by exposing an uncovered,
  result-bearing functional term (`spec-oob-totality-witness.k` and
  `oob-totality-witness-kprove.log`).
- `floatVal(N,D)` is an uninterpreted, result-bearing constructor. No equation
  relates it to CPython float values, rounding, signed zero, infinity, or
  overflow. The proof's even result depends on this unproved and false-as-global
  "exact Python division" bridge.

## Overlap, order, state, and control

- Guard pairs for lookup, `ifVal`, insertion, and `chooseBody` are disjoint.
- R30 and R31 overlap. Their ground behavior is convergent for the modeled pure
  branch expressions; there are no expression-side state cells to distinguish
  evaluation order in this submitted program.
- Sorting and expression evaluation are represented as pure K functions. This
  is adequate for the exact integer operations that do not throw, but not for
  Python's float/overflow and exception behavior.
- The module has no mutable heap or external effects. Assignment state is
  represented by persistent environment shadowing. Return/control behavior is
  preserved for the submitted function.
