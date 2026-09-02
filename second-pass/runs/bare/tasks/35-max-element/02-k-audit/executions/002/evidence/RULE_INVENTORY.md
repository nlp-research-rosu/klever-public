# Local declaration and rule inventory

Line references are to the fresh source copies under
`/tmp/audit-work/35-max-element`.

## Syntax productions

| ID | File:line | Production | Used by the submitted program? | Review |
|---|---|---|---|---|
| S1 | semantic.k:8 | `Program ::= Module(Stmts)` | Yes | Exact outer translator constructor. |
| S2 | semantic.k:9 | `Stmts ::= List{Stmt,""}` | Yes | Holds the module and function-body statement lists. |
| S3 | semantic.k:10 | `Stmt ::= FuncDef(String,Params,Stmts)` | Yes | Exact translated function binding. |
| S4 | semantic.k:11 | `Stmt ::= Return(Expr)` | Yes | Exact sole body statement. |
| S5 | semantic.k:13 | `Params ::= Params(Strings)` | Yes | Exact parameter constructor. |
| S6 | semantic.k:14 | `Strings ::= List{String,","}` | Yes | One parameter, `l`. |
| S7 | semantic.k:16 | `Expr ::= Name(String)` | Yes | Represents both `max` and `l`. |
| S8 | semantic.k:17 | `Expr ::= Call(Expr,Exprs)` | Yes | Represents `max(l)`. |
| S9 | semantic.k:18 | `Exprs ::= List{Expr,","}` | Yes | Represents the one positional argument. |
| S10 | semantic.k:22 | `IntSeq ::= [ NonEmptyInts ]` | Runtime input | Deliberately excludes `[]`. |
| S11 | semantic.k:23 | `NonEmptyInts ::= Int` | Runtime input | Singleton/base input form. |
| S12 | semantic.k:24 | `NonEmptyInts ::= Int , NonEmptyInts` | Runtime input | Recursive non-empty input form. |
| S13 | semantic.k:32 | `Function ::= closure(Params,Stmts)` | Runtime | Stores the submitted binding and body. |
| S14 | semantic.k:33 | `Result ::= noResult` | Runtime | Initial result state. |
| S15 | semantic.k:33 | `Result ::= result(Int)` | Runtime | Final observable result. |
| S16 | semantic.k:35 | `KItem ::= exec(Stmts)` | Runtime | Statement-list control. |
| S17 | semantic.k:36 | `KItem ::= invoke(String,IntSeq)` | Runtime | Entrypoint invocation. |
| S18 | semantic.k:37 | `KItem ::= eval(Expr)` | Runtime | Return-expression evaluation. |
| S19 | semantic.k:38 | `KItem ::= intVal(Int)` | Runtime | Tags the builtin result. |
| S20 | semantic.k:39 | `KItem ::= doReturn` | Runtime | Transfers the tagged result to `<result>`. |
| S21 | semantic.k:42 | `Int ::= maxInts(IntSeq) [function,total]` | Runtime and postcondition | Recursive, fully equated integer-list maximum. |
| S22 | semantic.k:43 | `Int ::= imax(Int,Int) [function,total]` | Runtime and postcondition | Two-integer maximum. |
| S23 | verification.k:8 | `Program ::= solutionProgram [function,total]` | Claim entry | Nullary name for the exact submitted constructor term. |
| S24 | verification.k:17 | `Int ::= expectedMaximum(IntSeq) [function,total]` | Claim result | Contract-facing alias of `maxInts`. |

The imported `Int`, `String`, `Map`, list, and K-sequence productions are
toolchain primitives, not candidate-local declarations.

## Configuration

`semantic.k:51-57` declares exactly four cells: `<k>` for control,
`<functions>` for module bindings, `<env>` for the active local binding, and
`<result>` for the observable return. The default computation loads `$PGM`
then invokes `max_element` with `$ARGS`. There is no heap, I/O, exception,
allocation, or call-stack cell.

## Functions and rules

| ID | File:line | Declaration/rule | Class and domain | Assessment |
|---|---|---|---|---|
| R1 | semantic.k:45 | singleton `maxInts` | Definitional equation; one-element `IntSeq` | True base equation. |
| R2 | semantic.k:46 | recursive `maxInts` | Definitional equation; length at least two | Structurally decreases and folds with `imax`; disjoint from R1. |
| R3 | semantic.k:48 | `imax(I,J) => I` if `I >= J` | Definitional equation | True on its guard. |
| R4 | semantic.k:49 | `imax(I,J) => J` if `I < J` | Definitional equation | True on its guard; R3/R4 are disjoint and exhaustive over K integers. |
| R5 | semantic.k:60 | `Module(SS) => exec(SS)` | Ordinary operational rule | Preserves continuation and begins module execution. |
| R6 | semantic.k:61 | `exec(.Stmts) => .K` | Ordinary operational rule | Correct empty-list base. |
| R7 | semantic.k:62 | split statement head/tail | Ordinary operational rule | Left-to-right sequencing; disjoint from R6. |
| R8 | semantic.k:66-67 | install `FuncDef` closure | Ordinary operational rule | Correct for this capture-free module function; updates only `<functions>`. |
| R9 | semantic.k:71-75 | invoke one-argument closure | Ordinary operational rule | The lookup pins the installed binding; resets `<env>` to the one parameter. Exact for the submitted capture-free function. |
| R10 | semantic.k:77 | `Return(E) => eval(E) ~> doReturn` | Ordinary operational rule | Correct along the submitted body, whose return is the sole statement. It does not implement general early-return unwinding. |
| R11 | semantic.k:81-82 | name lookup | Ordinary operational rule | Truthful map lookup; unused by the specialized actual `max(l)` path. |
| R12 | semantic.k:84-88 | `max(Name(X)) => maxInts(IS)` | Trusted external-primitive bridge | Directly models Python's builtin `max` for a bound non-empty integer sequence. `maxInts` is not opaque: R1-R4 fix its value. The rule is over-broad because it does not check that `max` is unshadowed. |
| R13 | semantic.k:90-91 | `intVal(I) ~> doReturn` writes result | Ordinary operational rule | Correct on the submitted single-return suffix and modifies only `<result>`. It is not a general return/unwind mechanism. |
| R14 | verification.k:9-12 | `solutionProgram` equation | Definitional summary | Exact constructor equality, independently parsed and hashed. |
| R15 | verification.k:18 | `expectedMaximum(IS) => maxInts(IS)` | Definitional summary | Truthful alias, but the natural-language “is a maximum” bridge remains the elementary induction on R1-R4. |

There are exactly four local `[function,total]` declarations (S21-S24).
There are no local `[functional]`, opaque, macro, priority, anywhere,
simplification, or concrete declarations/rules. There are no helper K files.
`spec.k` contains exactly three reachability claims and no rules.

## Construct-to-execution map

The submitted term uses `Module`, `FuncDef`, `Params`, `Return`, `Call`, and
`Name`. R5-R9 load and invoke its exact binding/body. R7 and R10 schedule the
sole return. R12 handles both syntactic names in `max(l)` in one specialized
step; R1-R4 compute the value; R13 records it. R6 consumes the empty body tail.
Every material operation of this program is therefore executed, although R12
is a direct builtin semantic primitive rather than a model of Python's general
name/call machinery.

## Rule-domain witnesses for limitations

- R12 is false as a general Python call rule when the local name `max` is
  shadowed. `shadow-max.mpy` binds the sole parameter as `"max"` and calls it.
  With `[1,2]`, this generated K semantics returns `result(2)`; the analogous
  Python function raises `TypeError` because the list is not callable.
- R10/R13 do not implement general early return. `trailing-return.mpy` has two
  consecutive returns. Python returns after the first. K reaches the second
  return and becomes stuck because `<result>` is already populated.

Neither witness is the submitted immutable program: its parameter is `l`, the
builtin name is unshadowed, and its return is the only body statement. These
are therefore over-broad/incomplete generated-semantics boundaries, not a
false conclusion witness for any satisfying input to the actual entry claim.
