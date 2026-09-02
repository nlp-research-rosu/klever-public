# Reviewer rule and declaration assessment

The canonical lexical inventory is in `k_source_inventory.log`. IDs below are
the per-file IDs from that log. Source line numbers refer to the clean scratch
copies, which are byte copies of the immutable candidate sources.

## Declarations and attributes

`semantic.k` has 31 local `syntax` sentences. They declare:

- AST/container constructors: `Module`; `FuncDef`, `Return`, `If`; `Params`;
  `Name`, `Int`, `Str`, `ListExpr`, `BinOp`, `BoolOp`, `Compare`, `Call`,
  `Subscript`, `ValueExpr`, `ListComp`, `Lambda`, `TupleExpr`, `KwArg`;
  `CmpOp`, `Slice`, `NoBound`, `CompFor`, `CellVars`, and `FreeVars`.
- Runtime constructors: `VInt`, `VStr`, `VBool`, `VList`, `VNone`, `Run`,
  `Result`, `Function`, `Normal`, and `Returned`, plus the list sorts `Stmts`,
  `Strings`, `Exprs`, `CmpOps`, `CompFors`, `Words`, and `Values`.
- Twenty-four `[function]` symbols: `evalExpr`, `evalExprs`, `evalBinOp`,
  `evalCompare`, `evalBoolOp`, `evalSubscript`, `callFunction`,
  `returnedValue`, `makeList`, `valueLength`, `valueWords`, `filterEven`,
  `filterEvenDecision`, `sortByKey`, `insertBySemanticKey`,
  `insertBySemanticDecision`, `semanticKeyLess`, `findFunction`,
  `programStmts`, `bindParams`, `execStmts`, `continueWith`, `chooseBranch`,
  and `prependWord`.

`solution-program.k` adds the zero-argument `[function]` `solutionProgram`.
`verification.k` adds six `[function]` symbols: `evenSorted`, `insertByKey`,
`insertAfterDecision`, `keepAfterDecision`, `sortedListSumSpec`, and
`keyLess`.

There are no `[total]`, `[functional]`, `[simplification]`, `[concrete]`, or
priority declarations; no `context` or `alias` sentences; no proof-local
claims in `verification.k`; and no fresh or unconstrained result-bearing
symbols. Zero-argument `[symbol]` attributes on constructors cause compiler
warnings but do not add equations. The sole configuration is
`<k> $PGM:Run </k>`; no state, heap, output, exception, or call-stack cell is
modeled.

## Construct coverage of `solution.mpy`

The submitted term uses `Module`, `FuncDef`, `Params`, `Return`, `Call`,
`Name`, `ListComp`, `CompFor`, `Compare`, `BinOp`, `Int`, `CmpOp`, `KwArg`,
`Lambda`, `CellVars`, `FreeVars`, and `TupleExpr`. Function lookup/calling and
return use semantic rules R02-R06, R31-R33, and R53. The comprehension and all
of its material per-element operations are replaced as one unit by R29. The
`sorted` call and its key lambda/tuple are replaced as one unit by R30.
Runtime `ValueExpr(VList(...))` inputs use R07; ground example lists use
R09 and R11-R18. Filtering and sorting then use R34 and R37-R48.

Thus the term parses and every used path has a rule, but R29/R30 are
task-specific result-bearing big-step bridges rather than reusable semantics
for comprehension iteration, lambda calls, tuple comparison, and `sorted`.
Their result is reused by the universal postcondition.

## `semantic.k` rules R01-R58

| Rule | Assessment |
|---|---|
| R01 | `Run` evaluates the supplied expression in an empty environment and wraps the value. Sound for the pure supported subset. |
| R02 | Extracts module statements. Sound. |
| R03 | Selects a matching function definition. Sound for the actual one-definition module. |
| R04 | Skips a nonmatching definition under `F =/=String G`. Disjoint from R03 and sound for the actual module. It would select the first duplicate definition rather than Python's last binding, but duplicate definitions are absent, so this is an unused coverage gap rather than a false conclusion witness for this program. |
| R05 | Empty parameter/value binding gives `.Map`. Sound. |
| R06 | Recursively binds one parameter to one value. Sound for the actual unique single parameter. |
| R07 | Injected `ValueExpr(V)` evaluates to `V`. Sound test/spec boundary. |
| R08 | Python integer AST constructor to `VInt`. Sound for modeled integers. |
| R09 | Python string AST constructor to `VStr`. Syntactic injection is sound; interpretation of length later is not. |
| R10 | Name lookup from the environment. Sound when bound; missing names visibly stick. |
| R11 | Empty expression list evaluates to empty values. Sound. |
| R12 | Singleton expression list evaluates to a singleton value. Sound. |
| R13 | Recursive expression-list evaluation. Its singleton overlap with R12 normalizes to the same result; all used arguments are pure. |
| R14 | List literal delegates to expression-list evaluation and construction. Sound for string elements. |
| R15 | Empty values make an empty list. Sound. |
| R16 | Singleton string value makes a singleton list. Sound. |
| R17 | Recursive string-list construction. Its singleton overlap with R16 agrees after R15/R18. |
| R18 | Prepends a string to a `VList`. Sound. |
| R19 | Delegates a binary expression to operand evaluation and `evalBinOp`. Sound on the pure supported operators. |
| R20 | `%` on `VInt` uses `%Int`. It agrees on the used nonnegative string length and divisor 2. Other error cases are partial and unused. |
| R21 | `+` concatenates two string lists. Sound but unused. |
| R22 | Delegates a single comparison. Sound for the pure supported operands. |
| R23 | Integer equality uses `==Int`. Sound. |
| R24 | Integer less-than uses `<Int`. Sound. |
| R25 | String less-than uses `<String`. No ordering counterexample was found for valid Unicode scalar strings; the task failure comes from byte length, not this rule alone. |
| R26 | Evaluates all Boolean operands before dispatch. This does not model Python short-circuiting and only R27's two-operand case is covered. It is unused by the submitted term; with the modeled pure Boolean operands it does not furnish a false result witness, so this is an unused evidence/coverage gap rather than labeled unsoundness. |
| R27 | Two Boolean operands with `"and"` use `andBool`. The truth table is sound; arities other than two are unsupported and unused. |
| R28 | `len` delegates to `valueLength`. Structurally sound, but inherits the false string-length rule R34. |
| R29 | Exact, task-specific comprehension bridge. It replaces binder iteration, `len`, `%`, and comparison with `filterEven`. It is result-bearing and is false for Python Unicode: for input `["😀"]`, the rule reaches `filterEven` using byte length 4 and keeps the word, while both Python implementations use code-point length 1 and return `[]`. |
| R30 | Exact, task-specific `sorted(..., key=lambda word: (len(word), word))` bridge. Its recursive sort is deterministic, but its key uses the false byte-length bridge. Witness: on `["😀😀", "aaaa"]`, Python lengths are 2 and 4 and Python returns `["😀😀", "aaaa"]`; this rule's K execution orders byte lengths 8 and 4 and returns `["aaaa", "😀😀"]`. |
| R31 | Generic non-`len`/non-`sorted` named call: evaluates arguments and finds a program function. Guards are disjoint from the two built-ins. Sound for the actual binding and pure argument. |
| R32 | Calls the found body under parameter bindings. Sound for the actual pure, single-frame function; the evaluator does not model a general Python call stack. |
| R33 | Extracts a returned value. Sound. |
| R34 | **Unsound Python bridge.** `valueLength(VStr(S)) => lengthString(S)` treats K's UTF-8 byte count as Python `len(str)`. Concrete witness `S = "😀"` gives K length 4 and Python length 1, enabling the false parity result above. |
| R35 | Empty list length is zero. Sound. |
| R36 | Nonempty list length is one plus tail length. Sound. |
| R37 | Extracts the word sequence from a list. Sound. |
| R38 | Empty input filters to empty. Sound. |
| R39 | Recursive filter directly tests `lengthString(S)`. **Unsound relative to Python** by the same `"😀"` witness; it selects the wrong branch. |
| R40 | True filter decision keeps the word. Sound conditional on its Boolean, but R39 can supply the wrong Boolean. |
| R41 | False filter decision drops the word. Sound conditional on its Boolean, but R39 can supply the wrong Boolean. Guards R40/R41 are disjoint and exhaustive for `Bool`. |
| R42 | Empty list sorts to empty. Sound. |
| R43 | Recursive insertion sort. It descends on the tail and is mathematically sound given a correct key relation. |
| R44 | Insert into empty gives the singleton. Sound. |
| R45 | Nonempty insertion delegates to a Boolean key decision. Sound given R46. |
| R46 | **Unsound Python key bridge** because tuple key length is computed with `lengthString`. Witness `S = "😀😀"`, `T = "aaaa"`: Python compares code-point lengths `2 < 4`; K compares UTF-8 byte lengths `8 < 4`, reversing the intended order. |
| R47 | True insertion decision places `S` first. Sound conditional on R46. |
| R48 | False insertion decision keeps `T` and recurses. Sound conditional on R46. R47/R48 guards are disjoint and exhaustive. |
| R49 | Subscript dispatch evaluates the receiver but passes the index syntax to the partial subscript evaluator. Unsupported dynamic indices stick; unused. |
| R50 | Index zero of a nonempty modeled list returns the first string. Sound. |
| R51 | Slice `[1:]` of a nonempty modeled list returns the tail. Sound. |
| R52 | Empty statement sequence terminates normally. Sound. |
| R53 | `Return` evaluates its expression and discards following statements. This is Python's abrupt return behavior and is sound for the actual body. |
| R54 | `If` evaluates the condition then delegates. Sound for Boolean conditions, though unused. |
| R55 | True branch executes, then continues with the suffix unless it returned. Sound. |
| R56 | False branch analog. Sound; R55/R56 guards are disjoint and exhaustive. |
| R57 | A return propagates and ignores the suffix. Sound. |
| R58 | Normal completion executes the suffix. Sound. |

All semantic recursive equations used by the target descend structurally. The
only material false conclusions are not attributed to an overlap or
nontermination: they arise from the explicit string-length bridge and flow
through the two task-specific operational summaries.

## `solution-program.k` rule R01

R01 defines `solutionProgram` as the exact `Module(FuncDef(...))` constructor
term. Trusted regeneration and an independent normalization comparison prove
constructor-level equality; the only normalizations spell empty `CellVars` and
`FreeVars` list units explicitly. This rule is sound for the immutable
candidate. A body mutation that removed `sorted` changed this RHS and made the
universal proof stick on the resulting unsorted `filterEven(INPUT)`.

## `verification.k` rules R01-R10

| Rule | Assessment |
|---|---|
| R01 | `keyLess` repeats the semantic length/text key. Its Boolean is false relative to Python for the `("😀😀", "aaaa")` witness above. |
| R02 | Defines `sortedListSumSpec(WS)` by the *same* semantic helpers `sortByKey(filterEven(WS))` returned by R29/R30. This equation is internally consistent, but it is not an independent connection from execution to the source contract; it makes the universal claim definitionally circular. |
| R03 | `evenSorted` empty base. Sound. |
| R04 | Recursive independent-looking filter/sort specification, but it also uses `lengthString`; it therefore includes `"😀"` contrary to Python. |
| R05 | True keep decision inserts the word. Sound conditional on R04. |
| R06 | False keep decision drops it. Sound conditional on R04; R05/R06 are disjoint/exhaustive. |
| R07 | Insert into empty. Sound. |
| R08 | Recursive insertion delegates to `keyLess`. Structurally descending and sound conditional on R01. |
| R09 | True insertion branch. Sound conditional on R01. |
| R10 | False insertion branch. Sound conditional on R01; R09/R10 are disjoint/exhaustive. |

The auxiliary `evenSorted` equations do not repair R02's circularity: there is
no universal claim connecting `sortByKey(filterEven(WS))` to `evenSorted(WS)`,
and both use the same incorrect K byte-length interpretation anyway.

## `spec.k` claims C01-C07

There are seven positive claims and no hidden helper claims. C01 is unrestricted
over finite K `Words`; C02 is the empty ground case; C03/C04 constrain two
strings to K byte length 2 and opposite K lexical branches; C05 constrains K
byte lengths 4/2/3; C06/C07 are the prompt examples. Every `<k>` starts with
`Run(solutionProgram, Call(Name("sorted_list_sum"), ...))`, consumes the
program call, and fixes an exact `Result(VList(...))`; no right-only/free
result variable occurs.
