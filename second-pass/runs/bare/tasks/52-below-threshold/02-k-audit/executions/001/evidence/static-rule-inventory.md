# Reviewer static inventory

This inventory was reconstructed from the copied source in
`/tmp/audit-work/reconstruction`, whose hashes are recorded in
`stage2-prepare-and-translator.log`. Candidate-compiled rules were not used.

## Local syntax and configuration

| ID | Source | Declaration / alternatives | Used role | Review |
|---|---|---|---|---|
| SY1 | `semantic.k:7` | `Pgm ::= Module(Stmts)` | submitted module root | Exact constructor transliteration. |
| SY2 | `semantic.k:8` | `Stmts ::= List{Stmt,""}` | empty and sequential statement bodies | Generated list syntax supplies `.Stmts` and juxtaposition. |
| SY3 | `semantic.k:9-12` | `Stmt ::= FuncDef(String,Params,Stmts) \| For(Expr,Expr,Stmts) \| If(Expr,Stmts,Stmts) \| Return(Expr)` | every statement constructor in `solution.mpy` | Minimal statement subset; no used constructor is absent. |
| SY4 | `semantic.k:13` | `ParamItems ::= List{String, ","}` | two entry parameters | Generated list syntax covers the submitted parameter list. |
| SY5 | `semantic.k:14` | `Params ::= Params(ParamItems)` | function parameter constructor | Exact constructor transliteration. |
| SY6 | `semantic.k:15-17` | `Expr ::= Name(String) \| Bool(Bool) \| Compare(Expr,CmpOp)` | names, Boolean returns, loop guard | Every expression in the submitted term is covered. |
| SY7 | `semantic.k:18` | `CmpOp ::= CmpOp(String,Expr)` | `">="` guard constructor | Operational rules deliberately recognize only the used `">="` spelling. |
| SY8 | `semantic.k:21-22` | `IntSeq ::= nil \| cons(Int,IntSeq)` | formal representation of integer lists | Finite recursive input domain. |
| SY9 | `semantic.k:30` | `Value ::= VInt(Int) \| VBool(Bool) \| VList(IntSeq)` | runtime values used by the program | Minimal and typed. |
| SY10 | `semantic.k:31` | `Slot ::= unbound \| slot(Value)` | `l`, `t`, `x` cells | Makes initialization explicit. |
| SY11 | `semantic.k:32` | `Result ::= noResult \| result(Bool)` | observable return | Restricts the modeled entry to Boolean results, exactly as used. |
| SY12 | `semantic.k:34-42` | `KItem ::= boot \| exec(Stmts) \| eval(Expr) \| ifK(Stmts,Stmts) \| forK(Expr,Stmts) \| loop(Expr,IntSeq,Stmts) \| cmpRight(Expr) \| cmpValues(Value,String) \| returnK` | evaluator control terms | Each term is consumed by the rules inventoried below; none is opaque. |
| CFG | `semantic.k:44-54` | `<bt>` with `<k>`, `<program>`, `<input>`, `<threshold>`, `<l>`, `<t>`, `<x>`, `<result>` | complete modeled state | Every non-`k` cell is read or written. There is intentionally no heap, I/O, exception, or call-stack cell because the submitted program uses none. |
| SY13 | `verification.k:7` | `Bool ::= allBelow(IntSeq,Int) [function,total]` | mathematical postcondition | Totality and equations reviewed under V1-V2. |
| SY14 | `verification.k:13` | `Pgm ::= solutionProgram [macro]` | exact theorem program term | Expansion identity was machine-checked in `stage4-kast-program-identity.log`. |

There are no other local syntax declarations or generated helper K source
files. There are no local `[functional]`, `[simplification]`, `[concrete]`,
priority, or opaque declarations.

## Operational and definitional rule inventory

| ID | Source | Rule effect | Cells / control | Soundness decision |
|---|---|---|---|---|
| R1 | `semantic.k:57-64` | `boot` selects exactly `Module(FuncDef("below_threshold", Params("l","t"), BODY))`, executes `BODY`, and binds formal inputs. | Reads `program,input,threshold,l,t`; writes `k,l,t`; preserves `x,result`. | Sound entry-driver bridge for this theorem. It does not summarize or replace `BODY`; it places the actual body in `<k>`. Its accepted module/name/arity are exact. |
| R2 | `semantic.k:67` | `exec(.Stmts) => .K` | `k` only | Sound empty-sequence identity. |
| R3 | `semantic.k:68` | `exec(S SS) => S ~> exec(SS)` | `k` only | Sound left-to-right statement sequencing. |
| R4 | `semantic.k:71` | `eval(Bool(B)) => VBool(B)` | `k` only | Exact Boolean literal evaluation. |
| R5 | `semantic.k:72-73` | lookup `Name("l")` | Reads `l`; rewrites `k`. | Sound under the required initialized slot. |
| R6 | `semantic.k:74-75` | lookup `Name("t")` | Reads `t`; rewrites `k`. | Sound under the required initialized slot. |
| R7 | `semantic.k:76-77` | lookup `Name("x")` | Reads `x`; rewrites `k`. | Sound after the loop rule binds `x`. |
| R8 | `semantic.k:80-81` | start `>=` comparison by evaluating the left expression | `k` only | Sound first step of left-to-right comparison evaluation. |
| R9 | `semantic.k:82-83` | preserve left value, then evaluate the right expression | `k` only | Sound evaluation-order continuation. |
| R10 | `semantic.k:84-85` | `VInt(I1) >= VInt(I2)` becomes `VBool(I1 >=Int I2)` | `k` only | Truthful use of K's unbounded integer comparison; equality/less/greater witnesses were executed. |
| R11 | `semantic.k:88-89` | evaluate an `If` condition before choosing a branch | `k` only | Sound condition-first control. |
| R12 | `semantic.k:90-91` | true condition executes only `THEN` | `k` only | Sound and disjoint from R13. |
| R13 | `semantic.k:92-93` | false condition executes only `ELSE` | `k` only | Sound and disjoint from R12. |
| R14 | `semantic.k:96-97` | evaluate the `For` iterable before loop entry | `k` only | Sound for the used iterable. |
| R15 | `semantic.k:98-99` | a `VList(XS)` becomes a loop over `XS` | `k` only | Sound list-iteration bridge for immutable `IntSeq`; no list mutation occurs. |
| R16 | `semantic.k:100` | empty loop terminates | `k` only | Sound base case, disjoint from R17. |
| R17 | `semantic.k:101-103` | bind head integer to `x`, execute body, recurse on tail | Writes `k,x`; other cells preserved. | Sound left-to-right iteration. Recursive argument is the strict tail. |
| R18 | `semantic.k:106` | `Return(E)` discards the remaining function computation, then evaluates `E` and enters `returnK` | Replaces the entire `k` continuation; all state cells preserved during expression evaluation. | Sound for the one-function/no-call-stack modeled language. The submitted false case exercises discarding the remaining loop and final `Return(true)`. |
| R19 | `semantic.k:107-108` | a Boolean return empties `<k>` and writes the observable result | Writes `k,result`; requires `noResult`. | Sound and result-constraining. |
| V1 | `verification.k:8` | `allBelow(nil,T) => true` | Pure function | Truthful empty-list base case. |
| V2 | `verification.k:9-10` | `allBelow(cons(I,XS),T) => (I <Int T) andBool allBelow(XS,T)` | Pure function | Truthful definition of universal strict inequality; constructor cases are disjoint, cover all `IntSeq`, and recurse structurally. |
| V3 | `verification.k:14-21` | expand `solutionProgram` to the complete submitted constructor term | Parse-time macro | Exact definitional spelling, not an operational shortcut. Parsed/expanded KAST is byte-identical to the submitted term. |

No pair of local operational rules overlaps on a common fully typed head
except where their constructors/Boolean literals make the guards disjoint.
There are no local priority rules. No rule introduces a fresh, opaque, or
unconstrained result-bearing symbol.

## Claim inventory

| ID | Source | Domain and exact context | Result / role | Review |
|---|---|---|---|---|
| C1 | `spec.k:8-25` | Any remaining `XS:IntSeq`, threshold `T:Int`, any full `INPUT:IntSeq`, exact loop body and exact trailing `exec(Return(true))`, initialized `l,t`, arbitrary initial `x`, `noResult`. | Consumes the exact loop continuation and returns `allBelow(XS,T)`; final `x` is existential. | Valid auxiliary circularity. It matches the real recurring loop state after progress; its exact continuation prevents use in unrelated frames. Independently proved in `stage3-kprove-loop-invariant.log`. |
| C2 | `spec.k:27-37` | Any `XS:IntSeq,T:Int`; exact boot state, exact program macro, and unbound `l,t,x` with `noResult`. | Terminates at `.K` with `result(allBelow(XS,T))`; `l,t` hold formal inputs and final `x` is existential. | Exact universal entry theorem. It is neither tautological nor one-way: the result cell is rewritten to one Boolean term. |

## Used-constructor coverage

| Submitted construct | Declaration | Executing rules / evidence |
|---|---|---|
| `Module`, `FuncDef`, `Params("l","t")` | SY1, SY3, SY4, SY5 | R1; every `krun` log |
| statement sequence and `.Stmts` | SY2 | R2-R3; empty and nonempty cases |
| `For(Name("x"),Name("l"),BODY)` | SY3, SY6 | R5, R7, R14-R17; empty and nonempty `krun` logs |
| `If(COMPARE,Return(false),.Stmts)` | SY3 | R11-R13; prompt-true and prompt-false logs cover both branches |
| `Compare(Name("x"),CmpOp(">=",Name("t")))` | SY6-SY7 | R6-R10; less/equal/greater cases in Stages 2-3 |
| `Return(Bool(false))`, `Return(Bool(true))` | SY3, SY6 | R4, R18-R19; both result values executed |

## Trust conclusion from the inventory

The imported K `INT`, `BOOL`, `STRING` syntax/operations, generated list
syntax, K sequencing, matching, and reachability engine remain the low-level
toolchain trust boundary. Locally, R1 is an intentionally narrow invocation
bridge and R15 is the representation bridge from `IntSeq` to immutable list
iteration. Neither computes the task answer or replaces the submitted body.
The only result summary, `allBelow`, is both truthfully defined and connected
to real execution by C1/C2. No unsound local rule was identified, so there is
no unsoundness allegation requiring a false-conclusion witness.
