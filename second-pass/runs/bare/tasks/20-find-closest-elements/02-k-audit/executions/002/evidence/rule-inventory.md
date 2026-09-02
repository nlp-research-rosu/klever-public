# Exhaustive local K inventory

This inventory covers the scratch copies of candidate `semantic.k`,
`verification.k`, and `spec.k`. `rat.md` and the imported K `BOOL`, `INT`,
`RAT`, `MAP`, and `STRING` modules are toolchain primitives, not
candidate-local proof rules.

Decision codes:

- `S`: sound for the submitted program and the rule's used match domain.
- `P`: truthful partial operation; unsupported shapes stop rather than
  fabricate a value.
- `L`: truthful for the exact submitted program but deliberately limited or
  over-broad as reusable Python semantics. No false task-result witness exists
  on the submitted program/input matches, so these are not labeled unsound.

## Syntax and configuration inventory

| Location | Every production declared |
|---|---|
| `semantic.k:10-13` | `Program ::= Module(Stmts)`; `Stmts ::= List{Stmt,""}`; `Params ::= Params(String)`; `Strings ::= List{String,","}` |
| `semantic.k:15-20` | `Stmt ::= ImportFrom(String,Strings) \| FuncDef(String,Params,Stmts) \| Assign(Expr,Expr) \| If(Expr,Stmts,Stmts) \| While(Expr,Stmts) \| Return(Expr)` |
| `semantic.k:22-29` | `Expr ::= Name(String) \| Int(Int) \| Subscript(Expr,Expr) \| BinOp(String,Expr,Expr) \| Call(Expr,Expr) \| Compare(Expr,CmpOp) \| TupleExpr(Expr,Expr)`; `CmpOp ::= CmpOp(String,Expr)` |
| `semantic.k:33-38` | `Value ::= vint(Int) \| vnum(Rat) \| vbool(Bool) \| vnil \| vlist(Value,Value) \| vtuple(Value,Value)` |
| `semantic.k:40-41` | `Input ::= Program \| run(Program,Value)` |
| `semantic.k:51-52` | `Result ::= noResult \| Value`; `Function ::= function(Params,Stmts)` |
| `semantic.k:54-60` | Configuration `<mpy>` with `<k>`, `<env>`, `<functions>`, and `<result>` cells; initial values are input program, empty maps, and `noResult`. |
| `semantic.k:63-79` | `KItem ::= exec \| invoke \| bindAndExec \| eval \| assignTo \| binLeft \| binRight \| subscriptLeft \| subscriptRight \| compareLeft \| compareRight \| callOne \| tupleLeft \| tupleRight \| choose \| whileChoose \| finishReturn` with the exact argument sorts shown in the source. |
| `semantic.k:82-106` | Functional productions `valueLength`, `valueAt`, `valuePlus`, `valueMinus`, and `valueLess`. |
| `verification.k:8` | Functional `Program ::= solution`. |
| `verification.k:46-48` | Functional `Value ::= nums` at arities 2, 4, and 6. |

The submitted constructor program uses every source constructor in this list:
`Module`, `ImportFrom`, `FuncDef`, `Params`, `Assign`, `Name`, `Subscript`,
`Int`, `If`, `Compare`, `CmpOp("<",...)`, `BinOp("+",...)`,
`BinOp("-",...)`, `While`, `Call(Name("len"),...)`, `Return`, `TupleExpr`,
and `Stmts`. Each maps directly to the declaration above and to the rule family
below.

There are no candidate-local `[total]`, `[functional]`, `[simplification]`,
`[priority]`, `[owise]`, `[anywhere]`, strictness, heating/cooling, macro,
alias, or opaque-symbol declarations. The only local attribute is `[function]`
on the nine productions listed above. The list productions are standard K
syntax sugar.

## Rule-by-rule inventory

| ID | Location | Rule | Decision and check |
|---|---|---|---|
| S01 | `semantic.k:83` | `valueLength(vnil) => 0` | S: empty proper list length. |
| S02 | `semantic.k:84` | `valueLength(vlist(_,T)) => 1 + valueLength(T)` | P: structurally correct recursion; malformed tails stop. |
| S03 | `semantic.k:87` | `valueAt(vlist(H,_),0) => H` | S: zero-index lookup. |
| S04 | `semantic.k:88-89` | positive-index `valueAt` recurses on tail and `I-1` | P: guard is disjoint from S03 and descends; negative/out-of-range indices stop. |
| S05 | `semantic.k:93` | integer `valuePlus` | S: exact integer addition. |
| S06 | `semantic.k:94` | rational `valuePlus` | S: exact rational addition. |
| S07 | `semantic.k:95` | integer/rational `valuePlus` | S: exact injection and addition. |
| S08 | `semantic.k:96` | rational/integer `valuePlus` | S: exact injection and addition. |
| S09 | `semantic.k:97` | integer `valueMinus` | S: exact integer subtraction. |
| S10 | `semantic.k:98` | rational `valueMinus` | S: exact rational subtraction. |
| S11 | `semantic.k:99` | integer/rational `valueMinus` | S: exact injection and subtraction. |
| S12 | `semantic.k:100` | rational/integer `valueMinus` | S: exact injection and subtraction. |
| S13 | `semantic.k:103` | integer `valueLess` | S: exact integer comparison. |
| S14 | `semantic.k:104` | rational `valueLess` | S: exact rational comparison. |
| S15 | `semantic.k:105` | integer/rational `valueLess` | S: exact injected comparison. |
| S16 | `semantic.k:106` | rational/integer `valueLess` | S: exact injected comparison. |
| S17 | `semantic.k:109` | `Module(SS) => exec(SS)` | S: begins module statement execution. |
| S18 | `semantic.k:110` | `run(Module(SS),ARG)` executes module then invokes the named entry point | S: pins the actual module body and the required entry-point name. |
| S19 | `semantic.k:111` | empty `exec` consumes | S: list base case. |
| S20 | `semantic.k:112` | nonempty `exec` sequences head before tail | S: source statement order. |
| S21 | `semantic.k:114` | `ImportFrom(_,_)` consumes | L: the exact import is typing-only and annotations were omitted by the trusted translator; arbitrary runtime imports would require bindings. |
| S22 | `semantic.k:115-116` | `FuncDef` installs `function(P,BODY)` in `<functions>` | S for the submitted top-level definition. |
| S23 | `semantic.k:118-119` | `invoke` resolves the function map binding | S: lookup pins name, parameters, and exact stored body. |
| S24 | `semantic.k:120-121` | `bindAndExec` replaces environment with the one parameter binding | L: correct for this body, which uses no global/program bindings; not reusable for Python closures/globals. |
| S25 | `semantic.k:124` | assignment begins RHS evaluation | S: RHS evaluated before write. |
| S26 | `semantic.k:125-126` | assignment writes evaluated value by map update | S: exact local-variable update. |
| S27 | `semantic.k:128` | `If` evaluates guard before `choose` | S: correct evaluation order. |
| S28 | `semantic.k:129` | true `choose` executes yes branch | S. |
| S29 | `semantic.k:130` | false `choose` executes no branch | S; disjoint from S28. |
| S30 | `semantic.k:132` | `While` evaluates guard | S. |
| S31 | `semantic.k:133-134` | true while executes body then repeats the exact while term | S: stable loop-head recurrence and correct sequencing. |
| S32 | `semantic.k:135` | false while consumes | S; disjoint from S31. |
| S33 | `semantic.k:137` | `Return(E)` evaluates expression before `finishReturn` | S. |
| S34 | `semantic.k:138-141` | returned value discards continuation, clears internal maps, writes result | L: correct output/control for this top-level harness; clearing module/function maps is an internal abstraction, not full persistent Python module state. |
| S35 | `semantic.k:144-145` | name evaluation resolves `<env>` binding | S: exact value lookup. |
| S36 | `semantic.k:146` | integer literal becomes `vint` | S. |
| S37 | `semantic.k:148` | binary operation evaluates left first | S: Python left-to-right order. |
| S38 | `semantic.k:149` | after left value, evaluates right | S. |
| S39 | `semantic.k:150` | `"+"` applies `valuePlus(left,right)` | S. |
| S40 | `semantic.k:151` | `"-"` applies `valueMinus(left,right)` | S. |
| S41 | `semantic.k:153` | subscript evaluates container first | S. |
| S42 | `semantic.k:154` | subscript then evaluates index | S. |
| S43 | `semantic.k:155` | integer index applies `valueAt` | P: correct for all used, in-range indices; invalid indices visibly stop. |
| S44 | `semantic.k:157-158` | comparison evaluates left first | S. |
| S45 | `semantic.k:159-160` | comparison then evaluates right | S. |
| S46 | `semantic.k:161-162` | `"<"` returns `vbool(valueLess(left,right))` | S for all numeric combinations used. |
| S47 | `semantic.k:166` | syntactic `Call(Name("len"),ARG)` evaluates argument | L: exact program has no shadowing of `len`; reusable Python semantics would need normal binding resolution. |
| S48 | `semantic.k:167` | length call returns `vint(valueLength(V))` | S for proper lists. |
| S49 | `semantic.k:169` | tuple evaluates first element | S. |
| S50 | `semantic.k:170` | tuple then evaluates second element | S. |
| S51 | `semantic.k:171` | two values construct ordered `vtuple` | S. |
| V01 | `verification.k:9-43` | `solution => Module(...)` | S: definitional program constant. Trusted regeneration and independent KORE comparison show exact constructor identity. |
| V02 | `verification.k:49` | two-argument `nums` | S: exact proper list constructor. |
| V03 | `verification.k:50-51` | four-argument `nums` | S: exact proper list constructor. |
| V04 | `verification.k:52-54` | six-argument `nums` | S: exact proper list constructor. |

The helper equations have disjoint constructor/arity or guard cases, terminate
on every used proper-list/numeric input, and have no conflicting overlaps.
There are no proof-local operational bridges, loop-summary rules,
simplification axioms, or result-bearing opaque values.

## Claim inventory

`spec.k` contains six entry claims and no helper/loop claims:

1. the first length-six prompt example;
2. the duplicate-valued length-six prompt example;
3. all two-element rational inputs satisfying `A < B`;
4. all two-element rational inputs satisfying `B < A`;
5. all equal two-element rational inputs;
6. one fixed negative-valued length-four input.

Every claim executes `run(solution, nums(...))` from empty internal maps and
`noResult`, consumes `<k>`, restores the modeled maps to empty, and fixes an
explicit returned tuple. None states a theorem for arbitrary list length or
arbitrary list contents beyond length two.
