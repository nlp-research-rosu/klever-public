# Reviewer rule and declaration inventory

This inventory is reconstructed from the source copies in
`/tmp/audit-work/reconstruction`; candidate-compiled files were not used.

## Local syntax and configuration

| ID | Declaration | Use by submitted term or harness | Review |
|---|---|---|---|
| D1 | `Pgm ::= Module(Stmt)` | Root of `solution.mpy` | Exact for the one-definition submitted module. |
| D2 | `Stmt ::= FuncDef(String, Params, Stmt)` | Submitted function definition | Carries the name, one parameter, and body emitted by the trusted translator. |
| D3 | `Stmt ::= Return(Expr)` | Submitted body | Exact used statement form. |
| D4 | `Params ::= Params(String)` | Submitted one-parameter signature | Exact used parameter form. |
| D5 | `Expr ::= Value` | Evaluation results | Subsort used by the manual expression machine. |
| D6 | `Expr ::= Name(String)` | `Name("len")`, `Name("string")` | Exact used name form. |
| D7 | `Expr ::= Call(Expr, Expr)` | One-argument `len(string)` | Exact used call shape; the grammar does not model other Python call forms. |
| D8 | `Value ::= Str(String)` | Input wrapper | Models the submitted string argument. |
| D9 | `Value ::= Int(Int)` | Return wrapper | Models the integer result. |
| D10 | `KItem ::= invoke(String, Value)` | Initial harness continuation | Explicitly invokes `strlen` after module loading. |
| D11 | `KItem ::= callLen` | Internal call continuation | Receives the evaluated `len` argument. |
| D12 | `KItem ::= finishReturn` | Internal return continuation | Transfers a returned value to `<result>`. |
| D13 | `Function ::= function(String, Stmt)` | `<functions>` map value | Stores one formal and body. |
| D14 | `Result ::= noResult \| Value` | `<result>` cell | Initial marker and final value. |
| C1 | `<py>` with `<k>`, `<functions>`, `<locals>`, `<result>` | Complete proof state | Every cell is read or written. The harness fixes invocation of `strlen` with `Str($INPUT)`. |

There are no local priority declarations, `owise` rules, simplification rules,
`concrete` rules, `[functional]` declarations, or fresh/opaque value symbols.
`callLen` and `finishReturn` are control markers, not value oracles.

## Ordinary semantic rules

| ID | Source | Complete effect and matched context | Decision |
|---|---|---|---|
| R1 | `Module(S) => S ...` | Replaces the module term at the head of `<k>` and preserves its suffix and all other cells. | Sound for the used one-statement module. |
| R2 | `FuncDef(...) => .K ...`; update `<functions>` | Consumes the definition and installs `F |-> function(P,BODY)` in the current map. | Sound on the submitted initial empty map and used function form. |
| R3 | `invoke(F,V) => BODY ...`; map lookup; `<locals> _ => P |-> V` | Selects the stored function and replaces all locals with the sole parameter binding; preserves the arbitrary `<k>` suffix. | Sound on the entry claim's fresh, top-level, one-call state. It is broader than justified for nested calls because it has no call stack or restoration, but no submitted-input execution reaches such a context; this is a reuse limitation, not a second witnessed false result for the real program. |
| R4 | `Name(X) => V ...`; locals lookup | Resolves an evaluated name from `<locals>`, preserving state and continuation. | Sound for `Name("string")` in every reachable submitted execution. |
| R5 | `Call(Name("len"),E) => E ~> callLen ...` | Bypasses general name evaluation and evaluates the sole argument before `callLen`, preserving the suffix and cells. | Binding is correct for this exact program because it cannot shadow or reassign `len`; the minimal language has no such constructs. This is an operational bridge to the external primitive and depends on R6 for its value. |
| R6 | `Str(S) ~> callLen => Int(lengthString(S)) ...` | Replaces the evaluated `len` call with the imported K string length and preserves all state and suffix. | **Materially invalid as a model of Python `len(str)` over the intended `str` domain.** Witness: submitted execution with `S="😀"` returns K `Int(4)` under both freshly built backends, while trusted and candidate Python return `1`. For `S="é"`, K returns `3`, Python `2`. This rule enables the false conclusion specialized from the entry claim. |
| R7 | `Return(E) => E ~> finishReturn ...` | Evaluates the return expression before the marker, preserving cells and suffix. | Sound for the submitted function, whose body is exactly one return and has no later statement. |
| R8 | `V ~> finishReturn => .K ...`; `<result> _ => V` | Consumes the marker and writes the value, preserving any later suffix. | Sound in the exact submitted top-level invocation, where no later suffix exists. A general Python return stack is outside this minimal grammar. |

## Verification-local declarations and equations

| ID | Declaration/rule | Coverage and overlap | Decision |
|---|---|---|---|
| V1 | `strlenPost(Value,Value):Bool [function,total]` | The only equation covers `Str(S), Int(N)`. It has no overlap, but it does **not** cover `Str/Str`, `Int/Str`, or `Int/Int`, despite `[total]`. | The equation is a deterministic definition relative to K's `lengthString`, but `[total]` is unjustified. The ground `Str("x"),Str("y")` probe is stuck (exit 1), demonstrating the coverage gap. The symbol is unused by the entry claim, so the declaration did not close that proof. Its advertised Python-postcondition meaning also inherits R6's Unicode mismatch. |
| V1-rule | `strlenPost(Str(S),Int(N)) => N ==Int lengthString(S)` | Applies to the covered `Str/Int` domain only. | Mathematically truthful as a definition over the imported K primitive; not a theorem connecting that primitive to Python. It is not referenced by `spec.k`. |

## Imported/trusted operations actually used

| Primitive | Role | Boundary judgment |
|---|---|---|
| K sequencing `~>` and cell rewriting | Evaluation/control plumbing | Standard K operational substrate; acceptable. |
| `Map` lookup and update | Function and local bindings | Standard K map substrate; used on singleton maps; acceptable. |
| `Int`, `String`, and token parsing | Value representation | Standard K substrate, but K `String` is not shown equivalent to CPython's Unicode `str`. |
| `lengthString` | Result-bearing value used by R6 and by the postcondition | Illegitimate bridge for the requested theorem: it is both repeated circularly and concretely disagrees with Python on intended inputs. |
| `==Int` | Body of unused `strlenPost` | Standard integer equality; acceptable, but the containing helper is unused and incomplete as total. |

## Construct coverage

The submitted term's constructors map as follows:

`Module` → D1/R1; `FuncDef` → D2/R2; `Params` → D4/R2;
`Return` → D3/R7/R8; `Call` → D7/R5/R6; both `Name` nodes → D6
with `"string"` handled by R4 and `"len"` special-cased by R5. The harness uses
D8/D10 and the result uses D9/D14. Thus no used constructor is silently
unmodeled; the defect is the wrong value semantics assigned to a modeled used
operation.
