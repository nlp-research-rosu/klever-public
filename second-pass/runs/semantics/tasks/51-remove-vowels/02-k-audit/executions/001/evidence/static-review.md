# Static soundness review evidence

## Inventory coverage

`k_inventory.py` enumerated every source declaration beginning with `syntax`,
`rule`, `claim`, `configuration`, `context`, or `alias` in the 24 supplied
semantics files plus `semantics.k`, `verification.k`, and `spec.k`. The complete
records, including full multiline source text, are in `k-inventory.json`; a
flattened index is in `k-inventory.tsv`.

- 949 declarations: 234 syntax, 705 rules, 5 contexts, 1 configuration, and 4
  claims.
- 928 belong to the byte-identical supplied semantics; 21 are candidate-local
  (17 in `verification.k`, 4 claims in `spec.k`).
- Attributes inventoried: 149 `function`, 110 `total`, 46 `priority`, 26
  `owise`, 35 `concrete`, 25 `symbol`, 8 `macro`, 1 `macro-rec`, 2 `strict`,
  and 1 `seqstrict`.
- There are no local `simplification` or `functional` declarations.

All 928 supplied declarations are accepted as the fixed semantics selected by
`SUPPLIED_SEMANTICS`, after recursive byte and type identity with the trusted
tree. Each was inspected for whether it can match the submitted program. No
false supplied rule was found in the execution-relevant slice. Unused partial
or intentionally opaque facilities do not match this program.

## Candidate-local declaration decisions

| Inventory IDs | Declaration(s) | Decision and basis |
|---|---|---|
| 929–930 | `vowelCodes` macro and equation | Sound. It is exactly the code sequence for `aeiouAEIOU`: 97,101,105,111,117,65,69,73,79,85. |
| 931–932 | total `isVowelCode(Int)` and equation | Sound and total. One unconditional Boolean disjunction covers every integer and is true exactly at those ten codes. |
| 933 | priority-40 `strContains(iCons(C,.IntSeq), vowelCodes)` specialization | Sound derived pure equation. It reads/writes no cells and has no control effect. The bridge-free exhaustive connection spec proves all ten matching integers and the complementary arbitrary-integer case. Opposite ground interpretations at 97 and 98 get stuck with `true`/`false` residuals. |
| 934–937 | total `removeVowelCodesAcc` and three equations | Sound definitional fold. Constructor cases cover `.IntSeq` and `iCons`; the latter guards are Boolean complements, so they are disjoint and exhaustive. Recursion strictly shortens the second sequence. The non-vowel case appends exactly the current code. |
| 938–939 | total `removeVowelCodes` and equation | Sound wrapper: it starts the accumulator fold at `.IntSeq`. |
| 940–941 | `removeVowelsLoopBody` macro and equation | Sound exact syntax abbreviation for the submitted loop body. |
| 942–943 | `removeVowelsBody` macro and equation | Sound exact syntax abbreviation for all four submitted body statements in order. |
| 944–945 | `removeVowelsProgram` macro and equation | Sound exact syntax abbreviation for the submitted module. Expanded KAST is byte-identical to the parsed submitted `solution.mpy`. |
| 946 | empty-loop claim | Sound base case. Empty string iteration yields `#iterDone`; no body executes, `result` and `char` are preserved. |
| 947 | vowel-head loop claim | Sound mutually inductive case. The yielded one-character string is assigned to `char`; the membership condition is true; the accumulator is unchanged; recursion processes `REST`. |
| 948 | non-vowel-head loop claim | Sound mutually inductive case. The condition is false; string `+` appends the one-character value to `result`; recursion processes `REST`. |
| 949 | entry claim | Sound and result-constraining. It loads the exact submitted module term, invokes its closure on `str(CODES)`, and returns exactly `str(removeVowelCodes(CODES))`, while pinning all initial/final cells. |

## Used-construct map

| Submitted construct | Supplied declaration/rules |
|---|---|
| `Module` / statement list | `syntax.k:56–61`; `core.k:124–127` (`#loadAll`, left-to-right statement sequencing). |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14–16` creates the closure in scope 0. |
| `Call(Name("remove_vowels"), str(CODES))` | `syntax.k:28`; `call.k:20–21` evaluates callee then arguments; `core.k:189–191` evaluates arguments left-to-right; `call.k:69–74` allocates/pushes the callee frame. |
| `Name` reads | `syntax.k:12`; `core.k:130–154` walks the scope chain. All relevant names are in the current plain frame, so no closure-cell priority rule applies. |
| `Assign` | `syntax.k:41` is strict in the RHS; `controls.k:9–11` updates the current plain scope. |
| `Str` literals | `syntax.k:13`; `str.k:13–17`. Every program literal is ASCII, within the rule guard. |
| `For` | `syntax.k:45` evaluates the iterable once; `controls.k:65–74` uses `#loop/#iterNext`; `str.k:8–10` yields one-character strings; `tuple.k:31–41` binds `char`. |
| `If` | `syntax.k:49` evaluates the guard; `controls.k:51–54` branches on `truthy`; Boolean values use `core.k:200`. |
| `Compare(...,"not in",...)` | `syntax.k:30,32`; `operators.k:15–17` evaluates left then right; `str.k:29–30` maps to `notBool strContains`; the reviewed specialization accelerates the fixed haystack. |
| `AugAssign(result,"+",char)` | `syntax.k:44` evaluates RHS first; `controls.k:20–23` reads/updates the current binding; `str.k:20–24` performs order-preserving concatenation. |
| `Return` | `syntax.k:50` evaluates the value; `functions.k:78–90` records it, discards the rest of the function body, pops the frame, restores the caller, and yields the value to the saved continuation. |

The execution-relevant rules preserve evaluation order, bindings, and control:
the module closure is defined in scope 0; the call creates scope 1 and binds
`text`; assignments initialize `result` and `char`; iteration overwrites
`char`, conditionally appends to `result`, and preserves order; return removes
scope 1 and restores every pinned cell. The program allocates no heap object and
raises no modeled exception.

## Priorities, overlaps, totality, and opaque symbols

- The proof-local priority rule (inventory 933) overlaps fixed
  `strContains` equations only with the same result; the bridge-free connection
  proof covers its complete match domain.
- The plain assignment/target-binding rules overlap closure-cell rules, but the
  latter require a `$cells` marker and have priority 40. This program uses a
  plain frame, so only the ordinary rules apply.
- Call routing is `[owise]`, allowing only more specific interceptors to preempt
  it. No imported interceptor matches `Call(Name("remove_vowels"), ...)`.
- The used total functions (`seqConcat`, `isVowelCode`,
  `removeVowelCodesAcc`, `removeVowelCodes`) have disjoint, exhaustive cases
  and structural descent.
- The supplied definition also imports 25 symbol/opaque facilities:
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
  `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
  `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  `sqrtF`, `md5hexCodes`, `sortVS`, and `sortKeyVS`. None occurs in the
  submitted term, any loop claim, the result summary, or any residual of the
  successful proof. They are therefore outside this proof's dependency cone.
- Fresh-build non-exhaustiveness warnings concerned `mapStrVS`, float
  conversion helpers, `joinCodes`, and `valSeqAt`; none is reachable here.
