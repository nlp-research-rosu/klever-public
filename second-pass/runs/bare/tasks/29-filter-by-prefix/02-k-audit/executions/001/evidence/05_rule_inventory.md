# Exhaustive local K inventory and disposition

This inventory was reconstructed from the copied source, not from
`semantic-kompiled`. Line references are to `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`.

## Modules, imports, and configuration

- `MPY-SYNTAX` imports only `BOOL-SYNTAX` and `STRING-SYNTAX`.
- `MPY` imports `MPY-SYNTAX`, `BOOL`, `INT`, `STRING`, and `MAP-SYMBOLIC`.
- `SEMANTIC` imports `MPY` and `VERIFICATION`; the top-level source requirement
  makes `verification.k` available.
- `VERIFICATION` imports `MPY`; `SPEC` imports `SEMANTIC`.
- The sole configuration (semantic.k:48-56) is `<t>` containing `<k>`,
  `<env>`, `<functions>`, `<input>`, `<prefix>`, and `<output>`. Every
  non-`<k>` cell is read or changed by at least one used rule.

## Local syntax declarations

| ID | Declaration / productions | Attributes | Used role |
|---|---|---|---|
| S01 | `StrList ::= nil \| cons(String, StrList)` | none | Input and Python-list value representation |
| S02 | `Module ::= Module(Stmts)` | none | Translated file root |
| S03 | `Stmts ::= List{Stmt, ""}` | generated list syntax | Sequential bodies |
| S04 | `Strings ::= List{String, ","}` | generated list syntax | Imports and parameter names |
| S05 | `Params ::= Params(Strings)` | none | Function parameters |
| S06 | `Stmt ::= ImportFrom(String, Strings)` | none | Type-only import |
| S07 | `Stmt ::= FuncDef(String, Params, Stmts)` | none | Entry definition |
| S08 | `Stmt ::= Assign(Expr, Expr)` | none | `result = []` |
| S09 | `Stmt ::= For(Expr, Expr, Stmts)` | none | Source `for` |
| S10 | `Stmt ::= If(Expr, Stmts, Stmts)` | none | Prefix guard |
| S11 | `Stmt ::= Expr(Expr)` | none | Append call statement |
| S12 | `Stmt ::= Return(Expr)` | none | Return statement |
| S13 | `Expr ::= Val` | subsort | Evaluated values |
| S14 | `Expr ::= Name(String)` | none | Variable lookup |
| S15 | `Expr ::= ListExpr()` | none | Empty result allocation/value |
| S16 | `Expr ::= Attribute(Expr, String)` | none | `startswith` and `append` selection |
| S17 | `Expr ::= Call(Expr, Expr)` | none | One-argument calls |
| S18 | `Val ::= strVal(String)` | none | String runtime value |
| S19 | `Val ::= listVal(StrList)` | none | List runtime value |
| S20 | `Val ::= boolVal(Bool)` | none | Guard value |
| S21 | `Val ::= noneVal` | none | Append/fall-through result |
| S22 | `Val ::= boundString(String, String)` | none | Bound `startswith` receiver |
| S23 | `Val ::= boundRef(String, String)` | none | Bound append target for this program |
| S24 | `Function ::= function(Params, Stmts)` | none | Function table value |
| S25 | `Output ::= noOutput \| Val` | none | Observable return |
| S26-S36 | `KItem ::= launch`, `assignTo`, `startFor`, `loop`, `choose`, `discard`, `bindStartsWith`, `callArg`, `apply`, `doReturn`, `functionEnd` | none | Explicit evaluation/control continuations |
| S37 | `StrList ::= appendOne(StrList, String)` | `function` | Mathematical/pure list append-at-end |
| S38 | `Bool ::= startsWith(String, String)` | `function, total` | Prefix predicate |
| S39 | `StrList ::= filterAcc(StrList, String, StrList)` | `function` | Proof-side accumulator summary |
| S40 | `StrList ::= filterByPrefix(StrList, String)` | `function` | Proof-side result summary |
| S41 | `Stmts ::= loopBody()` | `function` | Exact syntax abbreviation |
| S42 | `Module ::= solutionProgram()` | `function` | Exact complete-program syntax abbreviation |

There are no local `functional`, `opaque`, `priority`, or `concrete`
declarations. The only `total` declaration is S38. The only local
`simplification` rules are R36 and R37 below.

## Rule-by-rule disposition

`Sound (scope)` means the rule is true for every match reachable in the
submitted, well-typed program. Some rules intentionally do not define general
Python; their broader limitations are called out without alleging a false
conclusion on the intended domain.

| ID | Source | Rule / effect | Class | Disposition and justification |
|---|---|---|---|---|
| R01 | semantic.k:71 | `appendOne(nil,S)=cons(S,nil)` | Function equation | Sound: base equation for stable append |
| R02 | semantic.k:72 | recurse over `cons(H,T)` | Function equation | Sound: preserves head and structurally descends |
| R03 | semantic.k:75-76 | prefix longer than string gives false | Function equation | Sound: Python string-prefix definition |
| R04 | semantic.k:77-78 | otherwise compare initial substring | Function equation | Sound: exact prefix definition; guard is complementary to R03 |
| R05 | semantic.k:81 | expose module statements, then `launch` | Operational | Sound (scope): module initialization order |
| R06 | semantic.k:82 | expose head statement before tail | Operational | Sound: left-to-right statement sequencing |
| R07 | semantic.k:83 | empty statement list disappears | Operational | Sound: sequencing identity |
| R08 | semantic.k:84 | ignore `ImportFrom` | Operational | Sound (scope): the sole import is type-only `typing.List`; over-broad for arbitrary imports but no bad intended-domain match |
| R09 | semantic.k:85-86 | register `FuncDef` body | Operational | Sound: stores the exact parameters/body under its name |
| R10 | semantic.k:89-93 | select entry body and bind two external arguments | Operational | Sound (scope): exact entry name/arity and parameter names are taken from the registered source definition |
| R11 | semantic.k:96-97 | `Name(X)` performs map lookup | Operational | Sound: all used names are bound before lookup |
| R12 | semantic.k:98 | `ListExpr()` becomes a fresh empty list value | Operational | Sound for observable behavior; identity/aliasing is not needed by this source |
| R13 | semantic.k:99-100 | evaluate named `startswith` receiver | Operational | Sound: receiver lookup precedes argument evaluation |
| R14 | semantic.k:101 | bind string receiver and method name | Operational | Sound for the used string method |
| R15 | semantic.k:102 | bind named append target | Operational | Sound (scope): no rebinding or alias-sensitive interleaving occurs between selection and application |
| R16 | semantic.k:103 | evaluate call target first | Operational | Sound: Python evaluation order for this call shape |
| R17 | semantic.k:104 | evaluate argument after target, then apply | Operational | Sound: preserves the used call order |
| R18 | semantic.k:105-106 | apply bound `startswith` | Operational | Sound, conditional on R03-R04 and imported String primitives |
| R19 | semantic.k:107-108 | append string to target list and return `None` | Operational | Sound for the sole append calls; changes only the target env binding |
| R20 | semantic.k:111 | evaluate assignment RHS first | Operational | Sound |
| R21 | semantic.k:112-113 | update assigned name with value | Operational | Sound |
| R22 | semantic.k:115 | evaluate iterable expression first | Operational | Sound |
| R23 | semantic.k:116 | turn evaluated list into loop state | Operational | Sound for `list[str]` inputs |
| R24 | semantic.k:117 | empty loop finishes | Operational | Sound: zero-iteration boundary |
| R25 | semantic.k:118-119 | bind next string, execute body, recur on tail | Operational | Sound (scope): stable order and one visit per element; source does not mutate the iterated input |
| R26 | semantic.k:121 | evaluate `If` condition before branch | Operational | Sound |
| R27 | semantic.k:122-123 | true Boolean chooses then-body | Operational | Sound |
| R28 | semantic.k:124-125 | false Boolean chooses else-body | Operational | Sound; guard is disjoint from and exhaustive with R27 for `Bool` |
| R29 | semantic.k:127 | evaluate expression statement then discard | Operational | Sound |
| R30 | semantic.k:128 | discard evaluated value | Operational | Sound |
| R31 | semantic.k:130 | evaluate return expression first | Operational | Sound |
| R32 | semantic.k:131-132 | set output and discard remaining function computation | Operational | Sound (scope): the source has one top-level invocation and this is Python return behavior. It is intentionally not a general nested-call stack rule. |
| R33 | semantic.k:133-134 | fall-through returns `None` | Operational | Sound though not reached because the submitted function explicitly returns |
| R34 | verification.k:9 | `filterByPrefix=filterAcc(...,nil)` | Definitional summary | Sound definition |
| R35 | verification.k:10 | empty input returns accumulator | Definitional summary | Sound base equation |
| R36 | verification.k:11-13 | matching head is appended to accumulator | Definitional summary + simplification | Sound under its true guard; structurally descends |
| R37 | verification.k:14-16 | nonmatching head is skipped | Definitional summary + simplification | Sound under its false guard; disjoint from R36 |
| R38 | verification.k:24-27 | expand `loopBody()` | Syntax abbreviation | Sound: byte-regenerated source has exactly this `If`/append body |
| R39 | verification.k:29-35 | expand `solutionProgram()` | Syntax abbreviation | Sound: exact constructor term modulo explicit empty list tails |

S38 totality is justified because, for integer string lengths, exactly one of
`length(P) > length(S)` and `length(P) <= length(S)` holds; the RHS substring
indices are valid in the latter branch. R36/R37 cover exactly `true`/`false`
after `startsWith` evaluates. R01/R02 and R35-R37 descend on a constructor list.
No equation pair has an overlapping guard with unequal right-hand sides.

## Claims and connection role

| Claim | Plain meaning | Connection assessment |
|---|---|---|
| `loop-correct` (spec.k:5-16) | Starting at the exact real loop head with accumulator `ACC`, remaining input `INPUT`, and the exact return continuation, termination returns `filterAcc(INPUT,PREFIX,ACC)`. | Universal execution connection for the proof summary. It fixes the exact continuation, preserves input/functions/prefix cells, and permits only the final env to be existential. The fresh body mutation made it fail. |
| `program-correct` (spec.k:19-26) | From empty env/functions and arbitrary `StrList`/`String` arguments, executing the exact program term terminates with `filterByPrefix(INPUT,PREFIX)` when it terminates. | Result-constraining end-to-end claim. `solutionProgram()` expands rather than bypasses execution; the loop claim supplies the execution-summary connection. |

## Construct coverage map for `solution.mpy`

| Submitted construct | Declaration | Operational rules |
|---|---|---|
| `Module` and statement lists | S02-S03 | R05-R07 |
| `ImportFrom("typing","List")` | S04, S06 | R08 |
| `FuncDef`, `Params` | S05, S07, S24 | R09-R10 |
| `Assign(Name("result"),ListExpr())` | S08, S14-S15 | R11-R12, R20-R21 |
| `For(Name("string"),Name("strings"),...)` | S09, S14 | R11, R22-R25 |
| `If(startswith-call, append-call, empty)` | S10 | R26-R28 |
| `Attribute`/`Call` for `startswith` | S16-S17, S18, S22 | R13-R14, R16-R18 |
| `Expr` plus `Attribute`/`Call` for `append` | S11, S16-S17, S19, S21, S23 | R15-R17, R19, R29-R30 |
| `Return(Name("result"))` | S12, S14, S25 | R11, R31-R32 |

Every constructor in the submitted term is covered. Unused Python constructs
remain unmodeled, which is allowed for generated minimal semantics.

## Narrow evidence gaps, not unsoundness findings

- The K String and Map builtins and K's reachability/circularity implementation
  are trusted primitives rather than candidate-defined conclusions.
- Equivalence of this deliberately small model to CPython for the used subset
  is assessed rule-by-rule and empirically, not proved inside K.
- R08, R15, R25, and R32 would be insufficient as a general Python semantics,
  but no satisfying intended-domain execution of this submitted source exposes
  the omitted import effects, rebinding/aliasing, list mutation during
  iteration, or nested call stack. No false-conclusion witness exists for the
  actual program and stated `List[str]`, `str` domain.

No local rule was classified as unsound, so no false-conclusion witness is
required for an unsoundness finding.
