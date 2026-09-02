# Exhaustive local K inventory

This inventory covers every local declaration in `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`. Imported K built-ins are
listed separately in the trust ledger; they are not re-enumerated here.

## Syntax declarations

### `semantic.k`

| Lines | Sort / symbol | Productions and attributes |
|---|---|---|
| 6 | `Program` | `Module(Stmts)` |
| 7 | `Stmts` | empty-separator `List{Stmt,""}` |
| 9–13 | `Stmt` | `FuncDef`, `Assign`, `For`, `If`, `Return` |
| 15 | `Params` | one string parameter |
| 16 | `Exprs` | comma-separated expression list |
| 17 | `CmpOps` | comma-separated comparison-operation list |
| 19–22 | `Value` | `Str`, `Int`, `Bool`, `NoneVal` |
| 23–29 | `Expr` | `Value`, `Name`, `Attribute`, `Call`, `Compare`, `ListExpr`, `BinOp` |
| 30 | `CmpOp` | operator string plus comparator expression |
| 42 | `WordSeq` | `WNil`, `WCons(String,WordSeq)` |
| 43 | `splitWords` | `String -> WordSeq`; `[function,total]` |
| 53 | `Function` | stored function parameter/body pair |
| 54–60 | `KItem` | `load`, `invoke`, `exec`, `execStmt`, `loop`, `put`, `choose` |
| 97 | `memberInt` | `Int × Exprs -> Bool`; `[function]` |
| 102–103 | `conditionalAppend` | `Bool × String × String -> String`; `[function,total]` |

The configuration at lines 62–68 has one computation cell and three state
cells: `<k>`, `<functions>`, `<env>`, and `<result>`.

### `verification.k`

| Lines | Sort / symbol | Attributes |
|---|---|---|
| 7 | `solutionPrimes : Exprs` | `[function]` |
| 14 | `solutionLoopBody : Stmts` | `[function]` |
| 25 | `solutionBody : Stmts` | `[function]` |
| 34 | `solutionProgram : Program` | `[function]` |
| 42 | `contractPrimes : Exprs` | `[function]` |
| 49 | `primeLength(Int) : Bool` | `[function,total]` |
| 52 | `appendSelected(String,String) : String` | `[function,total]` |
| 56 | `selectedWords(WordSeq,String) : String` | `[function,total]` |
| 64 | `loopEnv(WordSeq,Map) : Map` | `[function]` |
| 65 | `wordEnv(WordSeq,Map) : Map` | `[function,total]` |
| 74 | `finishProgram : KItem` | ordinary constructor |
| 80 | `wellFormedWords(WordSeq) : Bool` | `[function]` |
| 86 | `renderWords(WordSeq) : String` | `[function]` |

There are no local syntax declarations in `spec.k`.

## Rules in `semantic.k`

| ID / lines | Rule | Class and audit decision |
|---|---|---|
| S1 / 45–46 | `splitWords` no-separator case | Definitional. Guard is disjoint from S2 and yields the one Python `split(" ")` segment. Valid. |
| S2 / 47–51 | `splitWords` separator case | Definitional. Removes the first separator, so recursion descends; preserves empty segments. Valid for all K strings assuming trusted `findString`/`substrString` contracts. |
| S3 / 70 | empty module load | Operational. Consumes an empty module. Valid. |
| S4 / 71–73 | load a function definition | Operational. Stores the exact parameter/body and continues with remaining definitions. Valid for the submitted one-definition module. |
| S5 / 75–77 | invoke | Operational. Looks up the stored body and replaces locals by the parameter binding. Valid for the submitted direct call. No exception/global model is claimed. |
| S6 / 79 | execute empty statement list | Operational. Valid. |
| S7 / 80 | execute head then tail | Operational. Establishes source statement order. Valid. |
| S8 / 82–83 | assign a string literal | Operational. Map update matches the used assignments. Valid. |
| S9 / 85–89 | exact `for x in y.split(" ")` | Operational. Reads `y`, builds `splitWords`, and enters the loop. Valid for the submitted iterator expression. |
| S10 / 91 | empty sequence loop | Operational. Valid. |
| S11 / 92–93 | nonempty sequence loop | Operational. Assigns the loop variable, executes the body, then recurs. Valid evaluation/control order. |
| S12 / 94–95 | update loop variable | Operational. Valid on the reachable state because `word` is initialized before the loop. It intentionally does not model allocating an absent target. |
| S13 / 98 | membership empty list | Definitional. Valid. |
| S14 / 99–100 | membership integer head | Definitional. Valid and descending for the all-`Int` submitted list. `memberInt` is intentionally partial for non-`Int` AST elements, which are not used. |
| S15 / 104–108 | conditional append | Definitional. Exhaustive over `Bool`, with the exact accumulator behavior. Valid and total. |
| S16 / 113–126 | exact outer/nested `If` store transformer | Program-specialized operational rule. It reads the literal membership list from the AST, not a prime oracle, and performs exactly the nested branch's sole observable update on reachable states. No generic-language connection theorem exists; body sensitivity and concrete/differential evidence support the intended reachable domain. No intended-domain false conclusion witness was found. |
| S17 / 128–131 | string-equality `If` | Operational. Valid lookup/comparison and preserves branch order. Dynamically preempted by S16 for the submitted nested conditional. |
| S18 / 133 | choose true | Operational. Valid. |
| S19 / 134 | choose false | Operational. Valid. |
| S20 / 136–137 | name-to-name assignment | Operational. Valid when the source binding exists; that condition holds in the submitted nested branch. Dynamically bypassed by S16. |
| S21 / 139–143 | exact nested string concatenation assignment | Operational. Guard fixes both operands to strings; left-associated concatenation matches the AST. Valid. Dynamically bypassed by S16. |
| S22 / 145–147 | return a named value | Operational. Sets `<result>`. It does not implement abrupt unwinding for arbitrary non-tail returns, but the only submitted `Return` is the final statement, so no satisfying intended input reaches a divergent context. This is a language-coverage limitation, not an intended-domain unsoundness witness. |

## Rules in `verification.k`

| ID / lines | Rule | Class and audit decision |
|---|---|---|
| V1 / 8–12 | `solutionPrimes` | Definitional AST constant. Matches the regenerated file. Valid. |
| V2 / 15–23 | `solutionLoopBody` | Definitional AST constant. Matches the regenerated file. Valid. |
| V3 / 26–32 | `solutionBody` | Definitional AST constant. Matches the regenerated file. Valid. |
| V4 / 35–36 | `solutionProgram` | Definitional AST constant. The independent identity claim closes and its `2 -> 4` mutation fails. Valid pinning bridge. |
| V5 / 43–47 | `contractPrimes` | Definitional specification table. Independent trial division confirms it is exactly the primes in `[0,100]`. Valid on the intended length domain. |
| V6 / 50 | `primeLength` | Definitional wrapper around V5/S13–S14. Unconditional and total for every `Int` because the fixed list contains only `Int` constructors. Valid. |
| V7 / 53–54 | `appendSelected` | Definitional wrapper around S15/V6. Valid and total. |
| V8 / 57 | `selectedWords` empty | Definitional base case. Valid. |
| V9 / 58–59 | `selectedWords` cons | Definitional descending recursion. Valid. |
| V10 / 66 | `wordEnv` empty | Definitional base case. Valid. |
| V11 / 67–69 | `wordEnv` cons | Definitional update of the existing string-valued `word` binding. Valid on every claim/reachable use. Its `[total]` attribute is broader than its equations: for example `wordEnv(WCons("x",WNil), .Map)` has no equation. That is a totality-coverage gap outside all entry/loop preconditions; it supplies no false result equality on the intended domain. |
| V12 / 70–72 | `loopEnv` | Definitional store summary guarded against duplicate `result`. Exact on the loop claim's map shape. Valid. |
| V13 / 75–77 | `finishProgram` | Proof-harness operational rule. It clears function/local maps but preserves `<result>`. All entry claims place it after invocation. It cannot fabricate the returned value; it deliberately makes the theorem insensitive to final local/function maps. Acceptable for a return-value contract, but not a theorem about those maps. |
| V14 / 81 | `wellFormedWords` empty | Definitional. Valid; unused by all claims. |
| V15 / 82–84 | `wellFormedWords` cons | Definitional descending recursion. Valid; unused by all claims. |
| V16 / 87 | `renderWords` empty | Definitional. Valid; unused. |
| V17 / 88 | `renderWords` singleton | Definitional. Disjoint from V18. Valid; unused. |
| V18 / 89–90 | `renderWords` two-or-more | Definitional descending recursion. Valid; unused. |

## Claims in `spec.k`

| ID / lines | Claim and role |
|---|---|
| C1 / 8–18 | `loop-invariant`: all `WordSeq`, accumulator, old loop word, disjoint remainder map, arbitrary functions/result/continuation; consumes the real loop and produces `loopEnv`. |
| C2 / 22–32 | `symbolic-contract`: all K strings from empty stores; executes `solutionProgram`, invokes it, runs the harness, and returns `selectedWords(splitWords(S),"")`. |
| C3 / 34–43 | first prompt example. |
| C4 / 45–54 | second prompt example. |
| C5 / 58–69 | 100-character `2 + space + 97` boundary. |
| C6 / 71–81 | composite length-100 word boundary. |

## Attributes and extension categories

- `[total]`: `splitWords`, `conditionalAppend`, `primeLength`,
  `appendSelected`, `selectedWords`, and `wordEnv`. All are covered on every
  theorem use; only `wordEnv` is not globally covered over its declared full
  `Map` sort.
- `[function]` without `[total]`: `memberInt`, the four `solution*`/prime
  constants, `loopEnv`, `wellFormedWords`, and `renderWords`. Their equations
  cover all actual/claim uses.
- No local `[functional]`, `[simplification]`, `[concrete]`, `[owise]`,
  priority, macro, anywhere, fresh/existential, or explicitly opaque
  declarations occur.
- No separate generated helper K files exist. `verification.k` is the only
  proof-local extension module, and `spec.k` contains the six claims only.

## Submitted-construct coverage

| Submitted `.mpy` construct | Declaration and execution rule |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax lines 6, 9, 15; S3–S5 |
| statement sequencing | `Stmts` line 7; S6–S7 |
| literal/name assignment | syntax lines 10, 19, 24; S8 (and S20 for the nested branch) |
| `For(Name, Call(Attribute(Name,"split"), Str(" ")), body)` | syntax lines 11, 24–26; S1–S2 and S9–S12 |
| outer `If`, `Compare`, `CmpOp("in")`, `ListExpr`, `len`, integer literals | syntax lines 12, 20, 26–30; S13–S16 |
| nested equality `If`, name assignment, `BinOp("+",...)` | syntax lines 12, 24, 29; atomically S16, with S17–S21 as unused narrow rules |
| tail `Return(Name("result"))` | syntax line 13; S22 |

All used constructs are either stepped explicitly or included in the exact,
result-sensitive S16 pattern. Unsupported variants stop with residual syntax
rather than being assigned fabricated behavior.
