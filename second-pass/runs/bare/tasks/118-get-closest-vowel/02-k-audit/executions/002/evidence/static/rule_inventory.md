# Reviewer rule and declaration inventory

This inventory covers the immutable candidate sources copied to
`/tmp/audit-work/118-get-closest-vowel/candidate-src`. The raw declaration
listing is in `raw-rule-inventory.log`.

## Local syntax and configuration declarations

| ID | File:line(s) | Declaration |
|---|---|---|
| D01 | `semantic.k:10` | `Module ::= Module(Stmts)` |
| D02 | `semantic.k:11` | empty-separated `Stmts` list |
| D03 | `semantic.k:12-15` | `Stmt`: `FuncDef`, `Assign`, `If`, `Return` |
| D04 | `semantic.k:16` | `Params(ParamNames)` |
| D05 | `semantic.k:17` | comma-separated `ParamNames` |
| D06 | `semantic.k:19-26` | `Expr`: `Name`, `Str`, `Int`, `Call`, `Compare`, `CmpOp`, `UnaryOp`, `Subscript` |
| D07 | `semantic.k:27` | comma-separated `Exprs` |
| D08 | `semantic.k:28` | comma-separated `CmpOps` |
| D09 | `semantic.k:29` | `Index ::= Expr \| Slice` |
| D10 | `semantic.k:30` | `Slice(Bound, Bound, Bound)` |
| D11 | `semantic.k:31` | `Bound ::= Expr \| NoBound` |
| D12 | `semantic.k:35-36` | ten case-sensitive `Vowel` constructors |
| D13 | `semantic.k:37` | `Char ::= vow(Vowel) \| con(String)` |
| D14 | `semantic.k:38` | snoc-list `Chars` |
| D15 | `semantic.k:39` | Peano `Nat` |
| D16 | `semantic.k:40-45` | `Val`: `pyStr`, `pyNat`, `pyNeg`, `pyBool`, `vowelSet`, and input wrapper `word` |
| D17 | `semantic.k:56-62` | configuration `<T>` with `<k>`, `<program>`, `<env>`, and `<stack>` |
| D18 | `semantic.k:64-74` | machine `KItem`s: start/invoke/execution/branch/return protocol |
| D19 | `semantic.k:75` | saved `frame(K, Map)` |
| D20 | `semantic.k:76` | `Frames` stack |
| D21 | `semantic.k:77` | `Frame` subsorted into `KItem` |
| D22 | `semantic.k:78` | big-step `ExecResult`: normal/returned |
| D23 | `semantic.k:80` | function `normalize` |
| D24 | `semantic.k:144` | function `call` |
| D25 | `semantic.k:149` | function `functionBody` |
| D26 | `semantic.k:153` | function `functionEnv` |
| D27 | `semantic.k:157` | function `returnValue` |
| D28 | `semantic.k:160-163` | functions `exec`, `execRest`, `execStmt`, `choose` |
| D29 | `semantic.k:179-184` | functions `eval`, `evalCompare`, `evalUnary`, `evalIndex`, `evalSliceLast`, `asBool` |
| D30 | `semantic.k:186` | function `lookupVal` |
| D31 | `semantic.k:217` | function `litChars` |
| D32 | `semantic.k:218` | function `litChar` |
| D33 | `semantic.k:237` | function `intNat` |
| D34 | `semantic.k:238` | function `lenChars` |
| D35 | `semantic.k:247` | function `asChars` |
| D36 | `semantic.k:250` | function `natLt` |
| D37 | `semantic.k:255` | function `fromEnd` |
| D38 | `semantic.k:259` | function `isVowelChar` |
| D39 | `program.k:3` | function constant `solutionProgram` |
| D40 | `verification.k:13` | result-bearing specification function `closestSpec` |

There are no local `[total]`, `[functional]`, `[simplification]`, or explicit
numeric-priority declarations and no opaque/uninterpreted local symbols.
The four local `[owise]` priority cases are S02, S21, S26, and S70 below.
Constructor declarations marked `[symbol]` are D01, D03, D04, D06, D10, and
D11; this attribute supplies KORE symbols, not equations.

## `semantic.k` rules

| IDs | Lines | Rule meaning and audit result |
|---|---|---|
| S01-S02 | 81-82 | Convert `word(S)` through `litChars`; otherwise preserve a `Val`. Disjoint through `owise`; sound. |
| S03 | 84 | Start the submitted entry point and append `unwrap`; sound wrapper. |
| S04 | 88-91 | Invoke the selected function body, install its parameter environment, and save the exact continuation/environment frame; sound for the one-function subset. |
| S05 | 93-95 | Restore the saved continuation and environment when a value is produced. The same `K` occurs in the active continuation and frame; sound. |
| S06-S07 | 96-97 | Consume `tailReturn` or `unwrap`; sound protocol rules. |
| S08-S09 | 99-100 | Empty/nonempty statement-machine sequencing; sound. |
| S10 | 101-103 | Evaluate an assignment RHS and update the named map entry; sound for the used assignment. |
| S11 | 104-107 | Fast path for `len(Name(X)) < 3`, reading the actual `X` binding. It is an operational bridge but agrees with S45/S51 over its matched `pyStr` domain. |
| S12-S15 | 108-112 | Length branches for 0, 1, 2, and at least 3 snoc elements; exhaustive/disjoint and sound. |
| S16 | 113-117 | Fast path for a comparison whose RHS is textually `Name("vowels")`. **Unsound operational bridge:** it does not read or guard the `vowels` binding and sends only the left value to `memberBranch`. |
| S17-S20 | 118-125 | Choose `in`/`not in` results solely from the `vow`/`con` constructor. Internally disjoint, but together with S16 they fabricate membership when the actual binding differs. The material-body witness is recorded in `body-sensitivity.log`. |
| S21 | 126-129 | Generic `If` evaluates the condition; `owise` makes it secondary to S11/S16. Sound where `eval` is defined. |
| S22-S23 | 130-131 | Boolean branch selection; sound/disjoint. |
| S24 | 132 | A return discards the remaining function-local computation. Caller continuations are on `<stack>`; sound for reachable machine states. |
| S25 | 133-136 | Tail-return call evaluates its argument then invokes the real function body; it does not summarize/skip that body. Sound for the used one-argument call. |
| S26 | 137-139 | Other returned expressions evaluate normally; `owise` is disjoint from S25. |
| S27 | 145-147 | Big-step call evaluates the selected body with its function environment. Partial outside the one-function subset; sound where defined. |
| S28 | 150-151 | Extract the body of the matching one-function module; sound/partial. |
| S29 | 154-155 | Bind the sole formal parameter to the argument; sound/partial. |
| S30 | 158 | Extract a returned value; sound/partial. |
| S31-S32 | 164-166 | Big-step execution of empty/nonempty statement lists; sound. |
| S33-S34 | 167-168 | Continue after normal execution or propagate return; sound/disjoint. |
| S35-S37 | 170-174 | Big-step assignment, conditional, and return; sound where expression evaluation is defined. |
| S38-S39 | 175-176 | Big-step Boolean branch choice; sound/disjoint. |
| S40 | 187 | Map lookup for the matching key; sound. |
| S41 | 188 | Evaluate a name through S40; sound where bound. |
| S42-S43 | 189-191 | Map the exact vowel literal to `vowelSet`, all other strings to `pyStr(litChars(S))`; guards are disjoint and cover strings. This is task-specific but truthful for the literal. |
| S44 | 192 | Nonnegative integer literal to Peano natural; sound/partial for the used nonnegative integers. |
| S45-S46 | 193-196 | Builtin `len` versus other one-argument calls; guards are disjoint. Sound for the submitted bindings. |
| S47-S50 | 197-203 | Evaluate single comparisons, unary expressions, ordinary indices, and the exact `[:-1]` slice; patterns cover every such form used by the program. |
| S51 | 205 | Peano less-than result; sound. |
| S52-S53 | 206-209 | Membership/nonmembership of a one-character string in the fixed `vowelSet`; sound and complementary. |
| S54 | 210 | Unary minus of a natural; sound for used negative indices. |
| S55 | 211 | Negative string indexing via `fromEnd`; sound when in range. |
| S56 | 212 | Remove the last character of a nonempty string; sound. |
| S57 | 213 | Extract a Boolean; sound. |
| S58-S59 | 219-224 | Convert empty/nonempty host strings to a snoc list by removing the last one-character substring; descends on host-string length and is sound for English-letter input. |
| S60-S69 | 225-234 | `litChar` equations for `a,e,i,o,u,A,E,I,O,U`, respectively; truthful and pairwise disjoint. |
| S70 | 235 | Every other one-character English input becomes `con(S)`; `owise` excludes S60-S69, so sound on the intended alphabet. |
| S71-S75 | 239-243 | `intNat` at 0/1/2/3 and positive recursive case. The recursive rule overlaps 1/2/3 but produces the same normal form and descends. |
| S76-S77 | 244-245 | Length of empty/snoc `Chars`; sound/disjoint. |
| S78 | 248 | Extract `Chars` from `pyStr`; sound/partial. |
| S79-S81 | 251-253 | Peano less-than for RHS zero, zero/successor, successor/successor; exhaustive/disjoint and descending. |
| S82-S83 | 256-257 | One-based indexing from the end at 1 and at least 2; disjoint and descending, sound when in range. |
| S84-S85 | 260-261 | `vow` is a vowel and `con` is not; disjoint/exhaustive over `Char`. |

S16-S20 have no bridge-free connection theorem or binding guard. A concrete
false-conclusion witness uses input `"bab"` and a translated program whose
material assignment is changed from `vowels = "aeiouAEIOU"` to `vowels = ""`.
Python returns `""`; S16-S20 still select the `vow(v_a)` branch, K returns
`"a"`, and all original postcondition claims still close. The mutation changes
the `solutionProgram` constructor hash, so this is not a source-only mutation.

Separately, the configuration/rules have no Python recursion-depth or exception
state. For the actual submitted program and intended English input `"b"*1000`,
CPython raises `RecursionError`, while this semantics returns `""`.

## `program.k` and `verification.k` rules

| ID | Lines | Meaning and audit result |
|---|---|---|
| P01 | `program.k:4-29` | `solutionProgram` expands to the submitted translated module. Independent token comparison proves identity after explicit empty-`Stmts` units. |
| V01 | `verification.k:14` | `closestSpec([]) = ""`; truthful. |
| V02 | `verification.k:15` | one-character result is empty; truthful. |
| V03 | `verification.k:16` | two-character result is empty; truthful. |
| V04 | `verification.k:17-18` | a rightmost consonant-vowel-consonant triple returns that vowel; truthful. |
| V05 | `verification.k:19-20` | middle consonant: remove the last character and recurse; truthful. |
| V06 | `verification.k:21-22` | left and middle vowels: remove the last character and recurse; truthful. |
| V07 | `verification.k:23-24` | consonant-vowel-vowel: remove the last character and recurse; truthful. |

V01-V07 are pairwise disjoint by list length and the `vow`/`con` constructor
partition, cover every `Chars` value, and every recursive RHS is one element
shorter. `closestSpec` is not an oracle in execution: it occurs only in claim
destinations, and the reachability claims connect actual machine execution to
it. There are no ordinary or simplification rules in `spec.k`.

## Reachability claims

`spec.k` has 13 unlabeled claims and no `requires`/`ensures` clauses. Each
quantifies arbitrary caller continuation `KREST`, environment `ENV`, and stack
`STACK`, while fixing `<program>` to `solutionProgram`.

| Claim | Lines | Entry shape and destination |
|---|---|---|
| C01 | 10-15 | empty input -> empty |
| C02 | 17-22 | length 1 -> empty |
| C03 | 24-30 | length 2 -> empty |
| C04 | 33-40 | terminal consonant-vowel-consonant -> that vowel |
| C05 | 44-51 | length-3, middle consonant -> empty |
| C06 | 53-60 | longer, predecessor ending consonant-consonant -> `closestSpec(predecessor)` |
| C07 | 62-69 | longer, predecessor ending vowel-vowel-consonant -> `closestSpec(predecessor)` |
| C08 | 71-78 | longer, predecessor ending consonant-vowel-consonant -> `closestSpec(predecessor)` |
| C09 | 81-88 | length-3, first two vowels -> empty |
| C10 | 90-97 | longer, predecessor ending vowel-vowel-vowel -> `closestSpec(predecessor)` |
| C11 | 99-106 | longer, predecessor ending consonant-vowel-vowel -> `closestSpec(predecessor)` |
| C12 | 110-117 | length-3 consonant-vowel-vowel -> empty |
| C13 | 119-126 | longer predecessor ending arbitrary-consonant-vowel -> `closestSpec(predecessor)` |

The shapes jointly cover all finite `Chars`: lengths 0/1/2; success at length
at least 3; and the three exhaustive failure shapes (middle consonant,
left+middle vowels, consonant+middle vowel+right vowel), with predecessor
subcases supplying the structural circularities. All destinations constrain
the returned `callResult`; none contains a fresh/free result variable.
