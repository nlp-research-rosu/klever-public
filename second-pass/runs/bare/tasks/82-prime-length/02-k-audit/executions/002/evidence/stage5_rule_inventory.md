# Exhaustive local K inventory

Source line numbers refer to the immutable candidate files.

## Syntax and attributes

`semantic.k` / `MPY-SYNTAX`:

1. `Program ::= Module(Stmts)` (line 8).
2. `Stmts ::= List{Stmt,""}` (line 10).
3. `Stmt ::= FuncDef(...) | Assign(...) | Return(...)` (lines 11–13).
4. `Params ::= Params(Strings)` (line 15).
5. `CellVars ::= CellVars(Strings)` (line 16).
6. `FreeVars ::= FreeVars(Strings)` (line 17).
7. `Strings ::= List{String,","}` (line 18).
8. `Expr ::= Int | Bool | Str | Name | Call | BinOp | BoolOp | Compare |
   GenExp` with the constructor signatures shown on lines 20–28.
9. `Exprs ::= List{Expr,","}` (line 30).
10. `CmpOp ::= CmpOp(String,Expr)` (line 31).
11. `CmpOps ::= List{CmpOp,","}` (line 32).
12. `CompFor ::= CompFor(Expr,Expr,Exprs)` (line 33).
13. `CompFors ::= List{CompFor,""}` (line 34).
14. `Value ::= VInt(Int) | VBool(Bool) | VStr(String)` (lines 36–38).
15. `Result ::= noResult | Value` (line 40).
16. `KItem ::= run(Program,Value) | #exec(Stmts)` (lines 41–42).

`semantic.k` / `SEMANTIC`:

17. `eval(Expr,Map):Value [function,total]` (line 73).
18. `valueLength(Value):Int [function,total]` (line 83).
19. `asInt(Value):Int [function,total]` (line 89).
20. `asBool(Value):Bool [function,total]` (line 103).
21. `noDivisors(Int,Int,Int):Bool [function,total]` (line 127).

`verification.k` / `VERIFICATION`:

22. `solutionProgram:Program [macro]` (line 9).
23. `isPrime(Int):Bool [function,total]` (line 31).

There are no local `[functional]`, `[owise]`, priority, `anywhere`, or opaque
constructor declarations. The three `noDivisors` equations carry
`[concrete(...),simplification]`. The symbolic proof therefore treats
`noDivisors(lengthString(S),2,lengthString(S))` as an unreduced,
result-bearing term.

## Configuration

`semantic.k` lines 52–57 define one `<py>` cell containing:

- `<k>` initialized to `run($PGM:Program,$ARG:Value)`;
- `<env>` initialized to `.Map`;
- `<return>` initialized to `noResult`.

No heap, call stack, generator state, exception, or I/O cell exists. This is
enough only because the one submitted body is pure apart from local assignment
and is invoked directly by the specialized `run` rule.

## Rules and claim

| ID | Source | Declaration/rule | Classification and audit result |
|---|---|---|---|
| S1 | `semantic.k:61` | `run(Module(FuncDef(...)),ARG) => #exec(BODY)` and bind parameter | Specialized entry dispatch. It pins the function name, one argument, and exact one-function module shape. Ignoring cell/free variable metadata is inert for the submitted body. |
| S2 | `semantic.k:66` | execute `Assign(Name(X),E)` by pure `eval` and map update | Sound for the submitted assignment; the semantics does not model Python expression effects generally. |
| S3 | `semantic.k:69` | execute `Return(E)` and discard trailing statements | Correct Python return control for the submitted body; trailing statements are unreachable. |
| S4 | `semantic.k:74` | `eval(Int(I)) => VInt(I)` | Literal bridge; sound. |
| S5 | `semantic.k:75` | `eval(Bool(B)) => VBool(B)` | Literal bridge; sound. |
| S6 | `semantic.k:76` | `eval(Str(S)) => VStr(S)` | Literal bridge; not exercised by the submitted body. |
| S7 | `semantic.k:77` | guarded map lookup for `Name` | Sound on maps containing a `Value`; all target lookups satisfy the guard. |
| S8 | `semantic.k:80` | `len(E)` becomes `valueLength(eval(E))` | Structurally appropriate, but its dependent S9 does not implement Python Unicode length. |
| S9 | `semantic.k:84` | `valueLength(VStr(S)) => lengthString(S)` | **Materially unsound Python bridge.** Witnesses: Python `len("😀😀") = 2` and `len("你好") = 2`; fresh K execution produces `n = 8` and `n = 6`. Consequently both Python functions return `True` while K returns `False`. |
| S10 | `semantic.k:86` | integer `%` via `%Int` after `asInt` | Sound for target operands, which are nonnegative lengths and divisors at least 2. |
| S11 | `semantic.k:90` | `asInt(VInt(I)) => I` | Sound on the target; `[total]` over all `Value` is not justified. |
| S12 | `semantic.k:92` | integer `>=` | Sound for target operands. |
| S13 | `semantic.k:94` | integer `!=` | Sound for target operands. |
| S14 | `semantic.k:97` | eager Boolean `and` | Over-broad compared with Python short circuit. On the submitted body, the RHS is pure and defined even for lengths 0 and 1, so there is no false conclusion witness on the intended input domain from eagerness alone. |
| S15 | `semantic.k:104` | `asBool(VBool(B)) => B` | Sound on the target; `[total]` over all `Value` is not justified. |
| S16 | `semantic.k:109` | exact `all(n % i != 0 for i in range(lo,hi))` pattern becomes `noDivisors` | Result-bearing, task-specific direct semantics. Ground S17–S19 agree with the matched pure generator, but there is no independent general generator execution or bridge-free connection theorem. The final postcondition uses the identical `noDivisors` term, so symbolic closure itself does not validate this bridge. No false ground conclusion was found for the target pattern; this is an evidence/trust-boundary limitation rather than the concrete unsoundness witness used for S9. |
| S17 | `semantic.k:128` | `noDivisors(_,D,HI) => true` if `D >= HI` | Correct empty-range base case where used. |
| S18 | `semantic.k:131` | return false if current divisor divides | Correct where `D >= 2`. |
| S19 | `semantic.k:134` | increment divisor when it does not divide | Correct and descending toward the base case where `D >= 2`. |
| V1 | `verification.k:10` | macro expansion of `solutionProgram` | Exact constructor copy of regenerated `solution.mpy`; fresh expanded KORE comparison is byte-identical. |
| V2 | `verification.k:32` | `isPrime(N) => N >= 2 and noDivisors(N,2,N)` | Mathematically correct primality characterization for natural-number lengths, conditional on `noDivisors` having S17–S19's ground meaning. |
| C1 | `spec.k:9` | one all-`S:String` reachability claim | Result-constraining and satisfiable; executes V1. It proves the K-byte-string theorem, not the Python-Unicode theorem, because S9 changes the material result for valid Python inputs. |

## Function coverage and overlap

The fresh LLVM compiler warned that `eval`, `valueLength`, `asInt`, `asBool`,
and `noDivisors` are non-exhaustive despite `[total]`. On submitted executions:

- `eval` reaches only the listed matched forms;
- `valueLength` receives `VStr`;
- `asInt` receives `VInt`;
- `asBool` receives `VBool`;
- `noDivisors` starts at divisor 2, so division by zero is unreachable.

The three `noDivisors` guards are disjoint for the target domain: `D >= HI`,
`D < HI` with zero remainder, and `D < HI` with nonzero remainder. The recursive
case increases `D`, so it terminates for ground target inputs. Globally,
`[total]` is overclaimed (notably `noDivisors(N,0,HI)` can demand modulo zero),
but no target-domain false result follows from those unused cases.

## Construct coverage for `solution.mpy`

Every submitted constructor is declared and matched through the following
route:

`Module` → `FuncDef`/`Params`/`CellVars`/`FreeVars` → `Assign` →
`Name`/`Call(len)` → `Return` → `BoolOp(and)` → `Compare(>=)` and
`Call(all)` → `GenExp` → `Compare(!=)` → `BinOp(%)` →
`CompFor`/`Call(range)`/`Bool(true)`.

`Exprs`, `CmpOps`, `CompFors`, `Strings`, and `Stmts` provide the constructor
lists used at each layer. No submitted constructor is silently unmodeled.
