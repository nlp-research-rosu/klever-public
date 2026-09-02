# Exhaustive local declaration and rule inventory

Scope: `/candidate/semantic.k` and `/candidate/verification.k`. The candidate
has no other helper K files. Line numbers below refer to those mounted files.

## Local syntax, configuration, and attributes

`semantic.k` declares:

- Lines 6-9: `Module`, one-string `Params`, juxtaposed `Stmts`, and
  comma-separated `Exprs`.
- Lines 11-16: the six statement constructors `FuncDef`, `Assign`,
  `AugAssign`, `For`, `If`, and `Return`.
- Lines 18-22: the six expression constructors `Name`, `Int`, `Str`,
  `Attribute`, and `Call` (five named alternatives; `Call` carries an `Exprs`
  list).
- Lines 31-41: the runtime constructors `vStr`, `vInt`, `vBool`, `vList`,
  `nil`, `cons`, `state`, `normal`, and `returned`.
- Lines 43-47: the complete four-cell configuration: `k`, `program`, `input`,
  and `result`.
- Line 49: control items `start` and `done`.
- Lines 56, 60, 64-66, 84, 88-89, 97, 102-103, 107, 111-115, 134-136,
  142-143, 151, 183-185, and 198: the local functions `runFunction`,
  `resultOf`, `evalStmts`, `evalStmt`, `evalRest`, `evalBranch`, `evalFor`,
  `evalForRest`, `lookup`, `setCount`, `setSentence`, `getCount`, `eval`,
  `replaceValue`, `splitValue`, `stripValue`, `startswithValue`, `asInt`,
  `asBool`, `asValues`, `splitDots`, `splitDotsAt`, `whiteSpace`, `strip`,
  `stripLeft`, `stripRight`, and `startsWith`.

`verification.k` declares the functions `solutionModule` (line 9),
`boredSpec`, `countBored`, and `boolInt` (lines 36-38).

There are no candidate-local `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, numeric-priority, claim, macro, anywhere, or opaque
declarations in these two files. All of the functions above have equations.
The only local priority-like attribute is `[owise]` on
`whiteSpace(_) => false` at semantic line 181.

## Constructor coverage for `solution.mpy`

| Submitted constructor | Declaration | Executing rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | semantic 6, 7, 11 | entry dispatch 51-54 |
| statement-list sequencing | semantic 8 | 68-72 |
| `Assign(Name("count"), Int(0))` | 12, 18, 19 | 74-75, 117, 137, 104 |
| `For(Name("sentence"), ...)` | 14 | 78-79, 90-94, 105 |
| `If(...)` | 15 | 80-81, 85-86 |
| `AugAssign(Name("count"), "+", Int(1))` | 13 | 76-77, 108, 117, 137, 104 |
| `Return(Name("count"))` | 16 | 82, 116, 99, 61 |
| `Name`, `Int`, `Str` | 18-20 | 116-118 |
| `Attribute`, `Call` for `replace` | 21-22 | 119-120, 128-129 |
| `Attribute`, `Call` for `split` | 21-22 | 121-122, 130, 142-149 |
| `Attribute`, zero-argument `Call` for `strip` | 21-22 | 123-124, 131, 151-196 |
| `Attribute`, `Call` for `startswith` | 21-22 | 125-126, 132, 198-201 |
| empty `Exprs` and `Stmts` tails | 8-9 | K list-unit constructors `.Exprs`, `.Stmts` |

Every constructor in the submitted term is declared and reaches a matching
rule. Missing rules for unused translator constructors are not counted as a
defect in generated-semantics mode.

## Rule-by-rule decisions: `semantic.k`

| Lines | Rule(s) | Class and decision |
|---|---|---|
| 51-54 | `start` dispatch | Operational entry bridge. It checks the exact function name and parameter and preserves all four cells except the intentional control/result updates. It admits any supported body and therefore inherits the over-broad initialization defect at 57-58 described below. |
| 57-58 | `runFunction(BODY, INPUT)` | Operational function-entry bridge. **Globally unsound as Python semantics:** it pre-binds `count` to `0` and `sentence` to `""` for every accepted body. The concrete witness `uninitialized-count.py`/`.mpy` returns `0` in K but Python raises `NameError` on input `"x"`; see logs 14a-14c. The exact submitted body overwrites `count` before reading it, so this false case does not explain the eight ground closures, but the rule is false over its declared match domain. |
| 61 | `resultOf(returned(vInt(N))) => N` | Partial projection, truthful on its constructor domain. Unsupported/non-integer outcomes remain visibly stuck. |
| 68 | empty `evalStmts` | Exact normal completion. |
| 69 | nonempty `evalStmts` | Exact left-to-right statement sequencing. |
| 71 | `evalRest(returned(V), _)` | Exact abrupt return propagation; remaining statements are discarded as in Python. |
| 72 | `evalRest(normal(ST), SS)` | Exact continuation after normal completion. |
| 74-75 | assignment to `count` | Exact for the submitted integer assignment; expression is evaluated before state update. |
| 76-77 | integer `count += E` | Exact for the submitted `+ Int(1)` path; the supported domain is integer-valued `E`. |
| 78-79 | `for sentence in E` | Exact dispatch to list iteration for the submitted list-of-strings expression. |
| 80-81 | `if E` | Exact dispatch for the submitted Boolean expression. |
| 82 | `return E` | Exact value evaluation and return construction. |
| 85 | true branch | Exact; only `THEN` executes. |
| 86 | false branch | Exact; only `ELSE` executes. |
| 90 | empty iteration | Exact normal loop completion. |
| 91-92 | string-list iteration step | Exact target assignment followed by body execution. |
| 93 | return from loop body | Exact abrupt return propagation. |
| 94 | normal loop continuation | Exact recursion on the remaining list. |
| 98 | lookup of parameter `S` | Exact for the initialized entry state. |
| 99 | lookup of `count` | Truthful for the abstract `state` value, but the state model has no unbound marker; the false program-level consequence originates at 57-58. |
| 100 | lookup of `sentence` | Same state-model limitation as line 99. It is sound on the submitted reachable path, where each split result is nonempty and the loop assigns `sentence`. |
| 104 | `setCount` | Exact functional update of only the count field. |
| 105 | `setSentence` | Exact functional update of only the sentence field. |
| 108 | `getCount` | Exact projection. |
| 116 | evaluate `Name` | Exact delegation to the modeled environment; inherits only the stated missing-unbound limitation. |
| 117 | evaluate `Int` | Exact. |
| 118 | evaluate `Str` | Exact. |
| 119-120 | two-argument string `replace` call | Exact for a string receiver and the submitted pure string arguments. Binding is fixed to `str.replace` by the source-contract string type. |
| 121-122 | one-argument string `split` call | Exact for the submitted separator `"."`. |
| 123-124 | zero-argument string `strip` call | Exact delegation to the local character-trimming definition. |
| 125-126 | one-argument string `startswith` call | Exact delegation for the submitted prefix `"I "`. |
| 128-129 | `replaceValue` | Exact on three strings, conditional on trusted K `replaceAll`. The used old strings are nonempty. |
| 130 | `splitValue(..., ".")` | Exact dispatch for the only submitted separator. |
| 131 | `stripValue` | Exact dispatch. |
| 132 | `startswithValue` | Exact dispatch. |
| 137 | `asInt(vInt(N))` | Exact checked projection; other values stay stuck. |
| 138 | `asBool(vBool(B))` | Exact checked projection; other values stay stuck. |
| 139 | `asValues(vList(VS))` | Exact checked projection; other values stay stuck. |
| 144 | find first dot | Exact first-split setup, conditional on trusted `findString`. |
| 145 | no-dot split base | Exact; Python `"s".split(".")` contains the one segment `"s"`, including when `s` is empty. |
| 146-149 | found-dot split step | Exact head/tail split and strict descent past one delimiter. The guard is disjoint from `-1`. |
| 152 | `" "` whitespace | True Python `str.strip` character. |
| 153 | `"\t"` whitespace | True Python `str.strip` character. |
| 154 | `"\n"` whitespace | True Python `str.strip` character. |
| 155 | `"\r"` whitespace | True Python `str.strip` character. |
| 156 | `"\f"` whitespace | True Python `str.strip` character. |
| 157 | U+000B whitespace | True Python `str.strip` character. |
| 158 | U+001C whitespace | True Python `str.strip` character. |
| 159 | U+001D whitespace | True Python `str.strip` character. |
| 160 | U+001E whitespace | True Python `str.strip` character. |
| 161 | U+001F whitespace | True Python `str.strip` character. |
| 162 | U+0085 whitespace | True Python `str.strip` character. |
| 163 | U+00A0 whitespace | True Python `str.strip` character. |
| 164 | U+1680 whitespace | True Python `str.strip` character. |
| 165 | U+2000 whitespace | True Python `str.strip` character. |
| 166 | U+2001 whitespace | True Python `str.strip` character. |
| 167 | U+2002 whitespace | True Python `str.strip` character. |
| 168 | U+2003 whitespace | True Python `str.strip` character. |
| 169 | U+2004 whitespace | True Python `str.strip` character. |
| 170 | U+2005 whitespace | True Python `str.strip` character. |
| 171 | U+2006 whitespace | True Python `str.strip` character. |
| 172 | U+2007 whitespace | True Python `str.strip` character. |
| 173 | U+2008 whitespace | True Python `str.strip` character. |
| 174 | U+2009 whitespace | True Python `str.strip` character. |
| 175 | U+200A whitespace | True Python `str.strip` character. |
| 176 | U+2028 whitespace | True Python `str.strip` character. |
| 177 | U+2029 whitespace | True Python `str.strip` character. |
| 178 | U+202F whitespace | True Python `str.strip` character. |
| 179 | U+205F whitespace | True Python `str.strip` character. |
| 180 | U+3000 whitespace | True Python `str.strip` character. |
| 181 | `whiteSpace(_) => false [owise]` | Priority fallback. It is disjoint from all preceding literal cases and exact for every other one-character string used by `strip`. |
| 186 | `strip => stripRight(stripLeft(...))` | Exact composition of left and right trimming. |
| 187 | empty `stripLeft` | Exact base case. |
| 188-189 | whitespace `stripLeft` step | Exact and strictly decreases string length. |
| 190-191 | non-whitespace `stripLeft` stop | Exact complement of the prior guard. |
| 192 | empty `stripRight` | Exact base case. |
| 193-194 | whitespace `stripRight` step | Exact and strictly decreases string length. |
| 195-196 | non-whitespace `stripRight` stop | Exact complement of the prior guard. |
| 199-201 | `startsWith` | Exact length guard plus prefix substring equality, conditional on trusted K string length/substrings. |

The only potentially overlapping strip base/generic rules are on `""`; the
explicit base yields `""`, while the non-whitespace stop, if its guard is
evaluable there, yields the same `""`. All other guarded pairs are disjoint.
The recursive rules decrease either a list, a delimiter count, or string
length.

## Rule-by-rule decisions: `verification.k`

| Lines | Rule | Class and decision |
|---|---|---|
| 10-32 | `solutionModule => Module(...)` | Definitional program constant. The trusted translator regeneration is byte-identical and the source-derived parsed-term pin claim closes. It does not replace the body: the operational semantics consumes this exact tree. |
| 39-40 | `boredSpec(S)` | Definitional summary of the submitted strip/split algorithm. It does not preempt program execution. The prose description “contract-level model” is materially inaccurate: for example `boredSpec("I ") = 0` while the trusted canonical is `1`. |
| 41 | `countBored(nil) => 0` | Exact base of that newly defined summary. |
| 42-43 | nonempty `countBored` | Exact recursive definition, decreasing on `REST`; disjoint from `nil`. |
| 44 | `boolInt(true) => 1` | Exact Boolean indicator. |
| 45 | `boolInt(false) => 0` | Exact Boolean indicator; disjoint from the prior rule. |

No rule in `verification.k` is an operational shortcut around
`evalStmts`. The summary is used only on the ground right-hand side of claim 8;
there is no universal connection claim relating program execution to
`boredSpec`.

## Imported trust boundary

The local theory relies on K's imported `STRING`, `INT`, and `BOOL`
primitives: `replaceAll`, `findString`, `substrString`, `lengthString`,
`==String`, integer addition/subtraction/comparison, and Boolean connectives.
These are fixed toolchain primitives rather than proof-local result oracles.
They affect the result, but no candidate rule changes their definitions.
The 16-case fresh K/Python comparison in log 12b supports their use on normal
and boundary values; it is finite evidence, not a universal theorem.
