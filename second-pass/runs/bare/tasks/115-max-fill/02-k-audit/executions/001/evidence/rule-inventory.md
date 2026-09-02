# Reviewer rule and syntax inventory

Scope: fresh source copies of `semantic.k`, `solution-program.k`,
`verification.k`, and `spec.k` under `/tmp/audit-work/rebuild`. Line numbers
below refer to those byte-identical candidate-source copies.

## Attribute and opaque-symbol census

- Local `[function]` symbols (13): `solutionProgram`, `collectFunctions`,
  `fromVals`, `appendArg`, `argValsToVals`, `bindParams`, `arithmetic`,
  `getItem`, `dropItems`, `water`, `requiredBuckets`, `solutionFunctions`, and
  `functionsOf`.
- Local `[total]`, `[functional]`, `[simplification]`, priority, `owise`,
  `anywhere`, and macro declarations: none.
- Opaque local symbols: none. Every local function has equations on every
  domain used by the submitted program and claims. Some functions are
  intentionally partial outside those used domains and are not marked
  `[total]`.
- Ordinary local rules: 58 in `semantic.k`, one in `solution-program.k`, and
  six in `verification.k`.
- Reachability claims: three in `spec.k`.

## Local syntax declarations

`MPY-SYNTAX`:

- `Module`: `Module(Stmts)` and the proof constant `solutionProgram`
  (`[function]`).
- `Stmts`: zero or more `Stmt` values, juxtaposed.
- `Stmt`: `FuncDef(String, Params, Stmts)` and `Return(Expr)`.
- `Params`: `Params(ParamList)`; `ParamList` is a comma-separated list of
  `String`.
- `Expr`: `Int(Int)`, `Name(String)`, `ListExpr(ExprList)`,
  `BinOp(String,Expr,Expr)`, `Compare(Expr,CmpOps)`,
  `IfExp(Expr,Expr,Expr)`, `Subscript(Expr,Index)`, and
  `Call(Expr,ExprList)`.
- `ExprList`: comma-separated `Expr`; `CmpOp`: `CmpOp(String,Expr)`;
  `CmpOps`: comma-separated `CmpOp`.
- `Index`: either `Expr` or `Slice`; `Slice`:
  `Slice(Bound,Bound,Bound)`; `Bound`: either `Expr` or `NoBound`.

`MPY` runtime and internal syntax:

- `Val`: `intVal(Int)`, `boolVal(Bool)`, `listVal(Vals)`, any `Row`,
  `gridVal(Rows)`, and `noneVal`.
- `Vals`: comma-separated `Val`; `Ints`: comma-separated `Int`;
  `Row`: `rowVal(Ints)`; `Rows`: comma-separated `Row`.
- `Function`: `function(Params,Stmts)`; `Exprs`: `exprs(ExprList)`;
  `Values`: `values(Vals)` (declared but unused); `ArgVals`: `noArgs` or
  `arg(Val,ArgVals)`.
- Function-result syntax: `collectFunctions(Stmts):Map`,
  `fromVals(Vals):ArgVals`, `appendArg(ArgVals,Val):ArgVals`,
  `argValsToVals(ArgVals):Vals`, `bindParams(Params,ArgVals):Map`,
  `arithmetic(String,Val,Val):Val`, `getItem(Val,Val):Val`, and
  `dropItems(Int,Val):Val`.
- Continuation `KItem` constructors: `invoke`, `restoreEnv`, `binRight`,
  `binApply`, `chooseBranch`, `compareEmpty`, `subscriptIndex`,
  `subscriptApply`, `sliceFrom`, `evalCallArgs`, `collectCallArg`,
  `evalListItems`, and `collectListItem`.
- Configuration: `<max-fill>` contains `<k>`, immutable input `<args>`, function
  table `<functions>`, local bindings `<env>`, and observable `<result>`.

`VERIFICATION`:

- `water(Ints):Int`, `requiredBuckets(Rows,Int):Int`,
  `solutionFunctions:Map`, and `functionsOf(Module):Map`, all `[function]`.

## Exhaustive rule decisions

The IDs S01–S58 follow source order in `semantic.k`.

- **S01–S02 (lines 81–83), `collectFunctions`: sound on its domain.** Empty
  statements produce an empty map; a leading function definition adds exactly
  its name, parameter list, and body and structurally recurses. The submitted
  program has three distinct function names, so no map-key conflict arises.
- **S03–S04 (lines 86–87), `fromVals`: sound.** It preserves value order while
  changing only the list representation.
- **S05–S06 (lines 90–91), `appendArg`: sound.** It structurally appends one
  value at the tail and terminates.
- **S07–S08 (lines 94–95), `argValsToVals`: sound.** It is the ordered inverse
  representation conversion used for list literals.
- **S09–S10 (lines 98–100), `bindParams`: sound for exact arity.** It pairs
  parameters and evaluated arguments left-to-right. Arity mismatches get
  stuck rather than fabricating bindings; all actual calls have exact arity.
- **S11 (line 103), integer addition: sound.** It maps Python integer `+` to
  unbounded K integer addition.
- **S12 (line 104), integer subtraction: sound.** It maps Python integer `-` to
  K integer subtraction.
- **S13 (lines 105–106), floor division: sound on the intended domain but
  over-broad as a Python rule.** It maps `//` to K `/Int`, which truncates
  toward zero. On every intended execution, the divisor is positive and the
  dividend `water + capacity - 1` is nonnegative, so truncation equals Python
  floor division. Off-domain witness: `grid=[[-4]], capacity=2` makes both
  Python implementations return `-2`, while K returns `-1`; see
  `stage5-off-domain-division-witness.log`. Because `-4` violates the prompt's
  `0 | 1` cell restriction, this is recorded as a narrowed adequacy/formal-
  scope concern, not an unsoundness witness on the intended domain.
- **S14–S15 (lines 109–112), `listVal` indexing: sound for used indices.**
  Index zero returns the head; a positive index drops one head and decreases.
  Guards are disjoint. Negative and out-of-range cases stop visibly.
- **S16–S17 (lines 113–116), `rowVal` indexing: sound.** These are the typed-row
  counterparts of S14–S15; results are wrapped as `intVal`.
- **S18–S19 (lines 117–120), `gridVal` indexing: sound.** These are the
  typed-grid counterparts; row values are returned without alteration.
- **S20–S21 (lines 123–125), `listVal` slicing from an integer: sound for used
  starts.** Start zero is identity; a positive start structurally drops items.
- **S22–S23 (lines 126–128), `rowVal` slicing: sound.** Same operation on the
  typed-row representation.
- **S24–S25 (lines 129–131), `gridVal` slicing: sound.** Same operation on the
  typed-grid representation.
- **S26 (lines 151–154), module initialization: sound for the configured entry
  state.** It collects the actual module's function definitions, preserves
  supplied arguments, and invokes `max_fill`. It applies only while the
  function table is empty.
- **S27 (lines 156–160), invocation: sound for the submitted pure functions.**
  The selected body and parameters come from the function map, arguments are
  already evaluated, the caller environment is saved, and a restoration frame
  is installed. It changes only `<k>` and `<env>`.
- **S28 (line 161), `Return`: sound for the submitted singleton bodies.** The
  literal `.Stmts` requires that `Return` is the sole remaining statement; all
  three real bodies have that form.
- **S29 (lines 162–164), environment restoration: sound.** Once a callee value
  is produced, the old environment is restored without changing the value or
  continuation.
- **S30 (line 166), integer literal: sound.**
- **S31 (line 167), name lookup: sound for the actual bindings.** It returns
  the map-bound value and changes no state.
- **S32–S34 (lines 169–171), binary evaluation: sound.** The frames force
  left-before-right evaluation and pass operands to `arithmetic` in source
  order.
- **S35–S37 (lines 173–175), conditional expression: sound.** The condition is
  evaluated first and exactly one branch is selected from a Boolean result.
- **S38 (lines 179–180), `== []` dispatch: sound for the only comparison form
  used by `solution.mpy`.**
- **S39–S44 (lines 181–186), empty-list tests: sound.** Empty/nonempty cases for
  `listVal`, `rowVal`, and `gridVal` are constructor-disjoint and return the
  corresponding Boolean.
- **S45–S47 (lines 188–192), ordinary subscripting: sound.** Base precedes
  index evaluation and `getItem` receives the evaluated base and index.
- **S48–S49 (lines 193–195), `[START:]` slicing: sound for the only slice shape
  used by the submitted AST.** The base is evaluated before `dropItems`.
- **S50–S53 (lines 197–203), calls: sound for direct named calls in this
  program.** Arguments are evaluated left-to-right, appended in order, and
  then passed to `invoke`. Direct name-to-function-table dispatch is narrower
  than general Python call binding, but every real call target is one of the
  three immutable top-level definitions and no program assignment can shadow
  it.
- **S54–S57 (lines 205–212), list literals: sound.** Items are evaluated
  left-to-right and converted to a `listVal`; the submitted program only uses
  the empty literal as the right operand of its special comparison rule.
- **S58 (lines 214–216), finalization: sound.** It applies only to a lone final
  value and initial `noneVal`, consumes the computation, and puts that exact
  value in the observable result cell. It cannot bypass a continuation.

`solution-program.k`:

- **SP01 (lines 8–43), `solutionProgram`: sound definitional program
  constant.** The rule contains the complete translated AST. A fresh trusted
  translation is byte-identical to `solution.mpy`, and depth-one normalized
  KORE states for the file and constant are identical
  (`stage2-translation.log`, `stage4-program-pinning.log`). It contains no
  task answer and still executes through S26–S58.

`verification.k`:

- **V01 (line 11), empty `water`: sound.** Empty integer list sums to zero.
- **V02 (line 12), nonempty `water`: sound.** Head plus recursive tail is the
  mathematical integer sum; structural descent terminates.
- **V03 (line 15), empty `requiredBuckets`: sound on every capacity.** No rows
  require zero bucket lowerings.
- **V04 (lines 16–19), nonempty `requiredBuckets`: sound under its `C > 0`
  guard and on the intended cell domain.** It adds the integer ceiling formula
  for the head row and structurally recurses. Its use of K `/Int` has the same
  off-domain negative-value limitation recorded for S13.
- **V05 (line 23), `functionsOf`: sound.** It delegates a concrete module's
  statements to S01–S02.
- **V06 (line 24), `solutionFunctions`: sound.** It names the function table of
  SP01 and does not replace any function execution.

`spec.k` claims:

- **C01 (lines 7–17):** connection theorem from exact `_water_in` invocation
  to `intVal(water(ROW))`, preserving arbitrary continuation and every framed
  cell.
- **C02 (lines 20–33):** connection theorem from exact `_buckets_for`
  invocation to `intVal(requiredBuckets(GRID,C))` for `C > 0`, likewise
  preserving all framed state.
- **C03 (lines 36–46):** end-to-end execution of SP01 from initial cells to
  empty `<k>` and the constrained `requiredBuckets` result for `C > 0`.

## Construct coverage and overlap review

Every constructor counted in the fresh translator output is declared and
executed: `Module`/`FuncDef`/`Params` are handled by S01–S02 and S26;
`Return` by S28; `Int` and `Name` by S30–S31; `BinOp` by S32–S34 and
S11–S13; `IfExp` by S35–S37; `Compare`/`CmpOp`/empty `ListExpr` by S38–S44;
the two `Subscript` forms and `Slice` by S45–S49 and S14–S25; and `Call` by
S50–S53, S27, and S29. User-list declarations cover all emitted statement,
parameter, expression, and comparison sequences.

All potentially overlapping local cases are disjoint by empty/nonempty
constructor, literal operator, runtime-value constructor, expression-versus-
slice sort, or a `0` versus `> 0` guard. No local priority is needed. The
configuration has no heap, output, allocation, exception, or mutation cell
because the submitted program performs none of those operations. Calls save
and restore the only mutable interpreter state (`<env>`); `<args>`,
`<functions>`, and `<result>` are preserved until finalization.
