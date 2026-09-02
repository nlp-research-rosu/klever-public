# Exhaustive local K declaration and rule inventory

Scope: untrusted candidate sources `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`. There are no generated
helper `.k` files. Candidate SHA-256 values are recorded in
`01-provenance.log`.

## Local declarations

| ID | Source | Declaration |
|---|---|---|
| D01 | `semantic.k:8-17` | Sorts `Module`, `Stmt`, `Expr`, `CmpOp`, `CompFor`; list sorts `Stmts`, `Exprs`, `Strings`, `CmpOps`, `CompFors`. |
| D02 | `semantic.k:19` | `Module(Stmts)`. |
| D03 | `semantic.k:21-30` | `Stmt` constructors: ordinary `FuncDef`, closure-annotated `FuncDef`, `Return`, and expression statement `Expr`. |
| D04 | `semantic.k:32-38` | `Expr` constructors: `Name`, `Str`, `Int`, `Attribute`, `Call`, `ListComp`, and `Compare`. |
| D05 | `semantic.k:40-41` | `CmpOp(String, Expr)` and `CompFor(Expr, Expr, Exprs)`. |
| D06 | `semantic.k:52-53` | Word sequence `.Words` / `WCons(String, Words)`. |
| D07 | `semantic.k:54-55` | Observable `pyList(Words)` and result alternatives `noResult` / `PyValue`. |
| D08 | `semantic.k:57-59` | Control terms `exec(Stmts)`, `eval(Expr,String,Int)`, and `finish`. |
| D09 | `semantic.k:61` | Function `words(String):Words`. |
| D10 | `semantic.k:62` | Function `scanWords(String,String,Words):Words`. |
| D11 | `semantic.k:63` | Function `appendWord(Words,String):Words`. |
| D12 | `semantic.k:64` | Function `filterWords(Words,Int):Words`. |
| D13 | `semantic.k:65` | Function `countConsonants(String):Int`. |
| D14 | `semantic.k:67-73` | Configuration with `<k>`, immutable input cells `<inputS>` / `<inputN>`, and observable `<result>`. |
| D15 | `verification.k:10` | Function `selectWordsSpec(String,Int):PyValue`. |

There are six local `[function]` declarations. There are no local `[total]`,
`[functional]`, `[simplification]`, `[owise]`, priority, macro, alias, context,
or opaque declarations. There are no proof-local imported helper modules.
`DOMAINS-SYNTAX`, `BOOL`, `INT`, and `STRING` are imported K libraries rather
than local declarations.

## Ordinary and function rules

| ID | Source | Complete role/domain | Classification and audit |
|---|---|---|---|
| R01 | `semantic.k:77-78` | Load an ordinary function named `select_words` with exactly parameters `s,n`; preserve all framed cells. | Operational semantics. Unused by the submitted closure-annotated term; harmless on its match domain. |
| R02 | `semantic.k:79-81` | Load the closure-annotated `select_words(s,n)` while accepting arbitrary cell/free-variable lists. | Operational semantics. Matches the submitted term. Ignoring those annotations is sound for this body because variable values are supplied by the two explicit input cells. |
| R03 | `semantic.k:84` | Drop a leading string expression from `exec`; preserve continuation and all cells. | Operational semantics for the actual docstring. Sound for a leading Python docstring. |
| R04 | `semantic.k:86-89` | Replace `Return(E)` by `eval(E,S,N) ~> finish`, reading both input cells. | Operational semantics. Sound for the actual pure body and exact inputs; no exception/state behavior is modeled. |
| R05 | `semantic.k:91-92` | Consume `V:PyValue ~> finish`, set `<result>` to `V`, and leave `.K`. | Operational semantics. Sound for the modeled return path. |
| R06 | `semantic.k:102-121` | Match the one exact nested-comprehension AST for this task for every K `String S` and `Int N`, and replace it atomically by `pyList(filterWords(words(S),N))`. | **Result-bearing operational bridge / task-answer encoding.** It is the only rule giving `ListComp`, `Call`, `Attribute`, `Compare`, `CmpOp`, or `CompFor` behavior. Its RHS is textually the same summary used by V01. There is no bridge-free generic execution semantics or connection claim. Removing only R06 leaves `eval(the submitted ListComp,...) ~> finish` stuck (`05-static-probes-final.log`). It is also false as a Python denotation on a stated-domain witness: `S="é", N=1` makes trusted and submitted Python return `["é"]`, while R06 plus R07-R20 returns `[]`, because the K string recurrences process the UTF-8 bytes. |
| R07 | `semantic.k:125` | Start `words(S)` as `scanWords(S,"",.Words)` for every K string. | Definitional recursion. |
| R08 | `semantic.k:127` | Finish scanning empty input with empty current word. | Definitional base case; disjoint from R09. |
| R09 | `semantic.k:128-129` | Finish scanning empty input with a nonempty current word by appending it. | Definitional base case; disjoint from R08. |
| R10 | `semantic.k:131-138` | On a literal space with empty current word, consume one K string unit and discard the empty field. | Definitional scan branch. Correct for U+0020 and the candidate's intended ASCII sample, but tied to K's byte-oriented `String` operations. |
| R11 | `semantic.k:140-147` | On a literal space with nonempty current word, consume it and append the word. | Definitional scan branch; guard-disjoint from R10/R12. |
| R12 | `semantic.k:149-155` | On a non-space unit, append that unit to the current word and recurse. | Definitional scan branch; guard-disjoint from R10/R11. Reconstructs UTF-8 bytes but does not implement Python character iteration. |
| R13 | `semantic.k:157` | Append to an empty `Words`. | Definitional base case; disjoint from R14. |
| R14 | `semantic.k:158-159` | Recurse through a nonempty `Words` and append at the end. | Definitional recursion; strictly descends through `Words`. |
| R15 | `semantic.k:163` | Empty K string has zero consonants. | Definitional base case. |
| R16 | `semantic.k:164-168` | If the first K string unit is found in ASCII `aeiouAEIOU`, consume it without incrementing. | Definitional recursion. The ASCII vowel test agrees with Python on individual Unicode code points, but K's `substrString` here exposes UTF-8 bytes rather than Python characters. |
| R17 | `semantic.k:169-174` | If the first K string unit is not found in ASCII vowels, consume it and increment. | Definitional recursion. Together with R15-R16 it is not a valid implementation of the source loop over Unicode letters. Concrete false witness: `"é"` is one Python character/consonant but two K units, so this rule fires twice and yields 2. |
| R18 | `semantic.k:176` | Filtering an empty word sequence returns empty. | Definitional base case. |
| R19 | `semantic.k:177-179` | Preserve a head word when its modeled consonant count equals `N`. | Definitional branch; disjoint from R20. Correct relative to `countConsonants`, but inherits R15-R17's Python-model error. |
| R20 | `semantic.k:180-182` | Drop a head word when its modeled consonant count differs from `N`. | Definitional branch; disjoint from R19. Correct relative to `countConsonants`, but inherits R15-R17's Python-model error. |
| V01 | `verification.k:12-13` | Define `selectWordsSpec(S,N)` as exactly `pyList(filterWords(words(S),N))` for all K strings/ints. | Definitional summary, but not independent of R06: the execution bridge and postcondition reduce to the same term. It also inherits the Unicode mismatch. |

R08/R09, R10/R11/R12, R13/R14, R15/R16/R17, and R18/R19/R20
have pairwise disjoint patterns or complementary guards. Their recursions
descend through the string/list argument on the concrete ASCII domain. No
priority rule preempts one branch, and no overlap was found that yields
different right-hand sides.

## Construct coverage map for `solution.mpy`

| Submitted construct | Declaration | Rules actually used |
|---|---|---|
| `Module` | D02 | R02 |
| Closure `FuncDef`, `Params`, `CellVars`, `FreeVars` | D03 | R02 |
| Leading `Expr(Str(...))` | D03/D04 | R03 |
| `Return` | D03 | R04/R05 |
| `ListComp`, `Name`, `CompFor`, `Call`, `Attribute`, `Compare`, `CmpOp` | D04/D05 | Only the single composite bridge R06; none has independent evaluation rules. |
| Empty `Strings`, `Exprs`, `CmpOps`, `CompFors` list syntax | D01 | Parsed collection units only. |
| Splitting, counting, filtering, list construction | D06/D09-D13 | R07-R20, reached only through R06. |

Thus syntax coverage exists, but operational coverage of every material source
operation is replaced by one exact whole-expression rule. The bridge-free
probe proves that the declared component constructs do not execute
independently.

## Reachability claims

`spec.k` has seven positive claims and no helper/circularity claims:

1. `spec.k:9-39`: symbolic `S:String`, `N:Int`, precondition `N >=Int 0`,
   exact submitted program term, result `selectWordsSpec(S,N)`.
2. `spec.k:43-56`: first prompt example.
3. `spec.k:58-72`: second prompt example.
4. `spec.k:74-87`: third prompt example.
5. `spec.k:89-102`: fourth prompt example.
6. `spec.k:104-117`: fifth prompt example.
7. `spec.k:119-132`: empty input.

All seven execute the same submitted constructor tree; the concrete claims
replace the summary postcondition with fixed expected lists.
