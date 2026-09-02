# Exhaustive local K inventory

The reviewed source set contains only `semantic.k`, `verification.k`, and
`spec.k`; there are no generated helper K files. There are no local
`priority`, `simplification`, or `functional` attributes and no unequated
opaque result symbols.

## Syntax and state

- `MPY-SYNTAX`: `Program` (`Module`); `Stmts` (empty-separated `Stmt` list);
  `Stmt` (`FuncDef`, `Assign`, `For`, `If`, `Return`); `Params`; comma lists
  `Exprs` and `CmpOps`; `Value` (`Str`, `Int`, `Bool`, `NoneVal`); `Expr`
  (`Value`, `Name`, `Attribute`, `Call`, `Compare`, `ListExpr`, `BinOp`); and
  `CmpOp`.
- `MPY-SEMANTIC`: `WordSeq` (`WNil`, `WCons`); stored `function`; computation
  items `load`, `invoke`, `exec`, `execStmt`, `loop`, `put`, and `choose`.
- Configuration: `<mpy>` contains `<k>`, `<functions>`, `<env>`, and `<result>`.
  The initializer loads `$PGM`, invokes `words_in_sentence` on string
  `$SENTENCE`, starts with empty maps, and starts with `NoneVal`.
- `MPY-VERIFICATION`: nullary syntax functions `solutionPrimes`,
  `solutionLoopBody`, `solutionBody`, `solutionProgram`, and `contractPrimes`;
  value functions `primeLength`, `appendSelected`, `selectedWords`, `loopEnv`,
  `wordEnv`, `wellFormedWords`, and `renderWords`; and computation marker
  `finishProgram`.

All constructors in `solution.mpy` map to those declarations. `Bool` and
`NoneVal` are not source constructors in this program (`NoneVal` is the initial
result); all other listed source constructors occur.

## Functions and totality

| ID | Declaration | Attributes | Static disposition |
|---|---|---|---|
| F1 | `splitWords(String):WordSeq` | `function,total` | Two disjoint guards (`findString == -1` and `>= 0`) cover K strings; recursion removes the first delimiter and prefix. Models Python `split(" ")`, including empty tokens. |
| F2 | `memberInt(Int,Exprs):Bool` | `function` | Empty and integer-head equations are disjoint and recursive. It is intentionally partial for non-`Int` heads; every actual use supplies only `Int` constructors. |
| F3 | `conditionalAppend(Bool,String,String):String` | `function,total` | Exhaustive Boolean conditional; exactly implements “keep accumulator or append word with one separator.” |
| F4–F7 | `solutionPrimes`, `solutionLoopBody`, `solutionBody`, `solutionProgram` | `function` | Single nullary equations. Mechanical KAST comparison pins F7’s normal form to trusted-regenerated `solution.mpy`. |
| F8 | `contractPrimes` | `function` | Single finite list equation; independently checked as exactly the primes through 100. |
| F9 | `primeLength(Int):Bool` | `function,total` | Delegates to F2 over F8’s concrete integer list; exhaustive for `Int`. |
| F10 | `appendSelected(String,String):String` | `function,total` | Delegates to F3/F9; exhaustive. |
| F11 | `selectedWords(WordSeq,String):String` | `function,total` | Disjoint `WNil`/`WCons` equations with structural descent. |
| F12 | `loopEnv(WordSeq,Map):Map` | `function` | One guarded equation, used only when the map has one separated string `result` binding. |
| F13 | `wordEnv(WordSeq,Map):Map` | `function,total` | Equations are correct on the proof domain (a separated string `word` binding), but `[total]` is broader than their coverage: `wordEnv(WCons("x",WNil),.Map)` has no defining equation. This is an off-domain totality evidence gap, not a witnessed false return equality on an entry state. |
| F14 | `wellFormedWords(WordSeq):Bool` | `function` | Disjoint structurally recursive equations; unused by all claims. |
| F15 | `renderWords(WordSeq):String` | `function` | Disjoint empty/singleton/two-or-more equations with descent; unused by all claims. |

## Semantic rules (`semantic.k`)

| ID | Lines | Rule and disposition |
|---|---:|---|
| S1–S2 | 45–51 | `splitWords`: no-space base and first-space recursion. Guards are disjoint; behavior and descent are correct. |
| S3–S4 | 70–73 | Empty-module termination and left-to-right `FuncDef` loading. Exact for the one submitted binding; map update preserves later-definition overwrite behavior. |
| S5 | 75–77 | `invoke`: looks up the selected binding, starts its exact body, and resets the local environment to the one parameter. Correct for the submitted top-level call. |
| S6–S7 | 79–80 | Empty and cons statement execution, preserving sequential order with `~>`. |
| S8 | 82–83 | String-literal assignment by map update. |
| S9 | 85–89 | Exact `sentence.split(" ")` `For` form; reads the named string binding and creates F1’s sequence. |
| S10–S12 | 91–95 | Loop termination, one iteration (`put ~> body ~> rest`), and existing-target update. The submitted body initializes `word`, satisfying S12’s match. |
| S13–S14 | 98–100 | Integer membership base/step; correct on the submitted literal list. |
| S15 | 104–108 | Conditional accumulation; correct and exhaustive. |
| S16 | 113–126 | Atomic semantics for the exact nested source `If`. It preserves the continuation and all framed state, reads the actual `result`/`word` bindings, and computes the same membership and concatenation for ASCII source inputs. It is task-shaped but not an unconstrained oracle: `NUMS` comes from the executed AST and the proof separately expands the contract list. The use of K `lengthString`, however, is not faithful to Python `len` for every Unicode letter. Witness: input `λλλ` makes S16/K return `""`, while both Python implementations return `"λλλ"`. |
| S17–S19 | 128–134 | Generic string-equality `If` and disjoint `choose(true/false)` rules. Correct; S16 preempts them for the submitted outer/nested pair. |
| S20 | 136–137 | Name-to-name assignment. Correct when the source binding exists, as it does in the submitted branch. |
| S21 | 139–143 | Exact nested string concatenation. Haskell side-condition unification uniquely binds `SY`/`SZ` on covered string maps. LLVM rejects these RHS-only variables, a portability gap; S16 preempts S21 on the submitted program. |
| S22 | 145–147 | Return reads the named value and writes only `<result>`, preserving continuation and other cells. |

There are no rule priorities. S16 and S17 are syntactically disjoint; the
literal/name/binop assignment rules are disjoint; `choose` guards are
constructor-disjoint; and the split guards do not overlap.

## Verification rules (`verification.k`)

| ID | Lines | Rule and disposition |
|---|---:|---|
| V1–V4 | 8–36 | Equations expanding the exact implementation list, loop body, function body, and module. Trusted regeneration plus normalized KAST comparison establishes constructor identity. |
| V5–V9 | 43–59 | Contract list, primality membership, append summary, and `selectedWords` base/step. The two lists expand independently but identically; trial division confirms V5 on the bounded contract. Structural recursion descends. |
| V10–V12 | 66–72 | `wordEnv` base/step and `loopEnv`. Equations correctly summarize the result/word map transformation under the claim guards. F13’s over-broad total declaration remains the limitation noted above. |
| V13 | 75–77 | `finishProgram` removes the fresh marker and clears internal function/environment maps without changing `<result>`. It is a proof-harness cleanup primitive, not a program step. It does not affect the source-contract return value, but its empty-map postconditions are conclusions about program-plus-cleanup, not the raw Python final locals. |
| V14–V15 | 81–84 | `wellFormedWords`; true structural characterization, unused. |
| V16–V18 | 87–90 | `renderWords`; true structural renderer, unused. |

## Claims

- C1 `loop-invariant`: derived helper theorem over every finite `WordSeq`,
  string accumulator/old word, and separated residual map.
- C2 `symbolic-contract`: entry theorem for every K `String`; executes
  `load(solutionProgram)` and the exact invocation, followed by V13, and
  constrains `<result>` to `selectedWords(splitWords(S),"")`.
- C3–C6: exact ground examples/boundaries. Each executes the same pinned
  program and constrains a concrete result string.
