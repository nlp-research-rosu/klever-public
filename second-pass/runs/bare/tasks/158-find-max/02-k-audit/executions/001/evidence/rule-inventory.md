# Reviewer rule inventory

Sources inventoried: the copied, hash-matched
`/tmp/audit-work/source/semantic.k`,
`/tmp/audit-work/source/verification.k`, and
`/tmp/audit-work/source/spec.k`. There are no other candidate K source/helper
files. Candidate-compiled rules were not used.

## Local syntax, attributes, and configuration

`MPY-SYNTAX` imports only K's `BOOL-SYNTAX`, `INT-SYNTAX`, and
`STRING-SYNTAX`.

| ID | Lines | Declaration | Attributes / assessment |
|---|---:|---|---|
| D01 | semantic.k:7-8 | `Pgm ::= AST \| runFindMax(AST, Words)` | Program start forms. `runFindMax` is unused by the submitted file. |
| D02 | 10 | `AST ::= Module(FuncDef)` | Used. |
| D03 | 11 | `FuncDef ::= FuncDef(String, Params, Stmts)` | Used. |
| D04 | 12 | `Params ::= Params(String)` | Used. |
| D05 | 15 | `Stmts ::= List{Stmt, ""}` | Used; matches translator juxtaposition. |
| D06 | 16-19 | `Stmt ::= Assign \| For \| If \| Return` | Exactly the submitted statement forms. |
| D07 | 21-26 | `Expr ::= Name \| Str \| Int \| UnaryOp \| Call \| Compare` | Exactly the submitted expression forms. |
| D08 | 27 | `CmpOp ::= CmpOp(String, Expr)` | Used for `>`, `==`, and `<`. |
| D09 | 30-31 | `Words ::= nil \| cons(String, Words)` | Transparent input list; every finite term is supported. |
| D10 | 40-43 | `Value ::= strVal \| intVal \| boolVal \| wordsVal` | Internal values. |
| D11 | 44 | `Result ::= noResult \| result(Value)` | Observable return state. |
| D12 | 46-56 | Eleven `KItem` continuations: `exec`, `eval`, `store`, `negate`, `callArg`, `cmpLeft`, `cmpRight`, `branch`, `startFor`, `loop`, `finishReturn` | Internal control syntax; no attributes or opaque control symbols. |
| D13 | 58-67 | `<mpy>` configuration with `<k>`, `<words>`, `<best>`, `<bestCount>`, `<word>`, `<count>`, `<result>` | Every non-`k` cell is read or written. Initial locals match `solution.py`; `<words>` is the external input. |
| D14 | 112 | `Value ::= setVal(String)` | Extensional set proxy. Sound only because the submitted program observes the set through `len`; its value is fixed by D15/S21/S37-S40. |
| D15 | 158 | `Int ::= distinctCount(String) [function, total]` | Result-bearing primitive/summary. Ground strings reduce through S37-S40. Symbolic strings intentionally remain opaque; fresh compilation warns “Non exhaustive match”. `[total]` does not prove the intended Python interpretation. |
| D16 | 159 | `Int ::= distinctCountFrom(String, Int) [function]` | Concrete recursive worker; not declared total. Used only from index 0. |
| D17 | verification.k:8 | `Stmts ::= solutionLoopBody [function]` | Definitional name; exact submitted body in V01. |
| D18 | 9 | `AST ::= solutionAST [function]` | Definitional name; exact submitted AST in V02. |
| D19 | 35 | `Candidate ::= candidate(String, Int)` | Contract accumulator constructor. |
| D20 | 36 | `Candidate ::= consider(String, Candidate) [function]` | Three guarded equations V03-V05. |
| D21 | 37 | `Candidate ::= maxCandidate(Words, Candidate) [function]` | Structural recursion V06-V07. |
| D22 | 38 | `String ::= candidateWord(Candidate) [function]` | Projection V08. |
| D23 | 39 | `String ::= findMaxSpec(Words) [function]` | Contract fold V09. |

There are no local `[functional]` declarations, priority rules/attributes,
`owise` rules, macros, anywhere rules, fresh-value declarations, or explicitly
opaque syntax. The only `[total]` declaration is D15. The only local
`[concrete]` rules are S37-S40. The only local `[simplification]` rules are
S37-S42 (S37-S40 also carry `concrete`).

## Operational and simplification rules in `semantic.k`

| ID | Lines | Rule role | Decision |
|---|---:|---|---|
| S01 | 70-71 | Exact `Module(FuncDef("find_max", Params("words"), BODY))` entry executes `BODY`. | Sound for the designated entry configuration. It executes the parsed body and does not synthesize a result. |
| S02 | 72-75 | `runFindMax` unwraps the same exact entry and replaces `<words>` with its argument. | Sound but unused. It is an auxiliary invocation form, not used by any target claim. |
| S03 | 78 | Empty statement-list execution terminates. | Sound. |
| S04 | 79 | Nonempty statement list schedules head before tail. | Sound left-to-right control. |
| S05 | 82 | Assignment evaluates RHS before a named store. | Sound for all submitted assignments. Unsupported targets would stop visibly. |
| S06 | 83-84 | Store string into `best`. | Sound and correctly typed. |
| S07 | 85-86 | Store integer into `best_count`. | Sound and correctly typed. |
| S08 | 87-88 | Store string into `word`. | Sound and correctly typed. |
| S09 | 89-90 | Store integer into `count`. | Sound and correctly typed. |
| S10 | 93 | String literal evaluation. | Sound. |
| S11 | 94 | Integer literal evaluation. | Sound. |
| S12 | 95-96 | Read `words`. | Sound. |
| S13 | 97-98 | Read `best`. | Sound. |
| S14 | 99-100 | Read `best_count`. | Sound. |
| S15 | 101-102 | Read `word`. | Sound. |
| S16 | 103-104 | Read `count`. | Sound. |
| S17 | 107 | Unary minus schedules operand before negation. | Sound for the submitted `-1`. |
| S18 | 108 | Integer negation as `0 -Int I`. | Sound. |
| S19 | 113 | A one-argument call evaluates its argument before dispatch by function name. | Sound on this program because `len`/`set` bindings cannot be rebound and function-name evaluation has no modeled side effects. Deliberately incomplete for unused Python calls. |
| S20 | 114 | `set(str)` becomes `setVal(str)`. | Sound as an extensional proxy only in combination with the sole supported observation, S21. |
| S21 | 115 | `len(setVal(S))` returns `distinctCount(S)`. | **Unsound bridge to real Python over the stated string domain.** S37-S40 operate on K string byte positions. Witness: on `S = "😀"`, K produces count 4 while Python `len(set("😀"))` is 1 (`unicode_single_emoji.log`). Observable false conclusion: on `["é", "é", "😀😀a"]`, the K program returns `"😀😀a"` while both Python implementations return `"é"` (`unicode_witness.log`, `concrete_execution.log`). |
| S22 | 118-119 | Comparison evaluates the left operand first. | Sound. |
| S23 | 120-121 | Saves left value, then evaluates right operand. | Sound and preserves Python order for the side-effect-free submitted operands. |
| S24 | 122-123 | Integer `>` with saved left and evaluated right. | Sound; operand orientation is correct (`I >Int J`). |
| S25 | 124-125 | Integer equality. | Sound. |
| S26 | 126-127 | String `<` with saved left and evaluated right. | Sound relative to K's string order; concrete tested cases agree with Python for ASCII. It does not repair S21's Unicode-count mismatch. |
| S27 | 130-131 | `If` schedules predicate and branch continuation. | Sound. |
| S28 | 132-133 | Execute then-branch when Bool is true. | Sound. |
| S29 | 134-135 | Execute else-branch when Bool is false. | Sound; guards are disjoint and exhaustive over Bool with S28. |
| S30 | 138-139 | `For` evaluates iterable before loop setup. | Sound for the submitted list iteration. |
| S31 | 140-141 | Snapshots `Words` into a loop term. | Sound because the program does not mutate the input list. |
| S32 | 142 | Empty loop terminates. | Sound. |
| S33 | 143-145 | Cons loop writes `word`, executes body, then recurs on tail. | Sound left-to-right iteration and state update. Only the used loop variable is supported; others stop. |
| S34 | 148 | Return evaluates its expression first. | Sound. |
| S35 | 149-150 | Return with a pending continuation records value and discards the continuation. | Sound abrupt function return for this single-frame semantics; result is constrained and written once from `noResult`. |
| S36 | 151-152 | Return without pending continuation records value. | Sound and disjoint in continuation shape from S35. |
| S37 | 160-161 | Concrete `distinctCount(S)` starts worker at byte index 0. | Internally consistent for K strings, but part of S21's inadequate Python bridge. It is not a bridge-free theorem about Python Unicode characters. |
| S38 | 162-163 | Worker returns 0 at/after `lengthString(S)`. | Internally sound termination base for K byte strings; guards do not overlap S39/S40. |
| S39 | 164-168 | If current byte occurs in the prior byte prefix, recurse without increment. | Internally sound byte-distinct counting; materially wrong if claimed as Python character counting. Same false-conclusion witness as S21. |
| S40 | 169-173 | If current byte is new, add one and recurse. | Internally sound byte-distinct counting; materially wrong if claimed as Python character counting. For `"😀"` it participates in deriving 4 rather than Python's 1. |
| S41 | 176 | `S <String S` simplifies to false. | Sound ordinary irreflexivity. |
| S42 | 177 | `distinctCount(S) >=Int 0` simplifies to true. | Sound for both the concrete byte-count implementation and intended set cardinality. It is an assumed mathematical lemma for symbolic S, not a proof of S21's value interpretation. |

For S38-S40's reachable worker domain, `I` starts at 0 and increases by one;
`I >= length` versus `I < length` is exhaustive, and within the latter domain
`findString(...) >= 0` versus `< 0` is exhaustive and disjoint. Negative or
otherwise arbitrary external uses of the worker are not used by the program or
proof.

## Definitional/contract rules in `verification.k`

| ID | Lines | Rule role | Decision |
|---|---:|---|---|
| V01 | 11-23 | Defines `solutionLoopBody`. | Sound exact definitional expansion; constructor-for-constructor identical to solution.mpy lines 6-17. No execution is bypassed. |
| V02 | 25-31 | Defines `solutionAST`. | Sound exact definitional expansion; matches the regenerated submitted AST byte-for-byte. |
| V03 | 41-43 | `consider`: strictly larger count replaces candidate. | Sound conditional equation. |
| V04 | 44-48 | Equal count and lexicographically smaller word replaces candidate. | Sound; guard entails equality despite redundant `<=`. |
| V05 | 49-52 | Smaller count, or equal count without a smaller word, retains candidate. | Sound. Guards V03-V05 are pairwise disjoint and exhaustive for integer counts and Boolean string comparison. |
| V06 | 54 | Empty fold returns accumulator. | Sound. |
| V07 | 55-56 | Cons fold considers head then structurally recurses. | Sound and terminating on finite `Words`. |
| V08 | 58 | Candidate-word projection. | Sound. |
| V09 | 59-60 | Initializes fold with `("", -1)`. | Sound as an algorithm over whatever nonnegative metric D15 denotes; it returns `""` on `nil`. It depends on the false S21 Python-value bridge for the natural-language “unique characters” meaning. |

V03-V09 are definitional summaries, not operational bridges: the operational
program body still executes under S01-S42. D15/S21 is the result-bearing
primitive shared by execution and the specification. The K proof is
interpretation-parametric over a nonnegative `distinctCount`, but the candidate
does not establish the required universal connection to Python
`len(set(word))`; its concrete equations refute that connection for non-ASCII
code points.

## Claims in `spec.k`

| ID | Lines | Plain-language obligation and static assessment |
|---|---:|---|
| C01 | 8-22 | From any accumulator `(BEST, BESTCOUNT)` and any finite remaining list, execute the real loop body and return the word in the contract fold. Result is constrained; final work cells are intentionally existential. |
| C02 | 27-38 | From exact initialized cells, executing `solutionAST` reaches the real loop head with the exact real body and return continuation. No result is fabricated. |
| C03 | 42-51 | From exact initialized cells and any finite `Words`, execute `solutionAST` to termination and constrain `<result>` to `findMaxSpec(WORDS)`. Final local cells are existential, but the observable return is not. |

All claims have no explicit `requires`; their displayed typed configurations
are satisfiable. The claims are about the literal program via V01/V02, but their
meaning as a Python correctness theorem fails at S21's language-semantic bridge.
