# Stage 5 rule-by-rule review

The exhaustive machine inventory is `k-rule-inventory.tsv` (1,100 entries
after the header): 231 syntax declarations, 717 rules, five contexts, one
configuration, two claims, and module/import/require records.  Of these, 38
entries are proof-local (`verification.k` and `spec.k`); the remaining 1,062
are the byte-identical supplied semantics.

## Disposition of the supplied inventory

Every supplied entry is fixed by the benchmark's `SUPPLIED_SEMANTICS` boundary.
The inventory was nevertheless scanned for task-specific rules, claims,
proof-local imports, operational shortcuts, priorities, and opaque functions.
There are no task-specific tokens or claims in the supplied tree.  The 22
`no-evaluators` declarations are confined to MD5, floats, and sorting and no
such symbol occurs in `solution.mpy`, `verification.k`, or `spec.k`.  The 35
`[concrete]` rules are in concrete-only support and are not imported by the
proof's `MPY` module.  Every other non-reachable supplied rule has an LHS root
symbol or sort that the submitted program never constructs.  Its disposition
for this theorem is `FIXED/NOT-REACHED`: it does not contribute a rewrite,
result, side condition, or inconsistency to either claim.

The fixed rules that are reachable are individually mapped below.  They have
the expected Python-subset behavior on the theorem's typed input domain:

| Construct / effect | Declaration and rules | Review |
|---|---|---|
| Module and statement sequence | `syntax.k:41-61`; `core.k:124-127` | `#loadAll` exposes the module statements in order; sequencing preserves the continuation. |
| Values and initial state | `core.k:13-60` | Strings are finite `IntSeq`s; lists are heap values; the initial module/builtin scopes, counters, stack, return, exception, and exit cells match the entry claim. |
| Function definition | `functions.k:14-16` | Binds the exact parameter list and exact body in module scope 0; no body is summarized. |
| Name lookup | `core.k:130-154` | Walks the current scope and parents. The relevant frames are ordinary non-cell frames, so cell-priority rules are inapplicable. |
| Call evaluation and dispatch | `call.k:15-24,69-75`; `core.k:183-191` | Callee then arguments evaluate left-to-right; closure dispatch allocates a local frame, pushes the complete continuation, and runs parameter binding, body, and `#endcall`. |
| Parameter binding and return | `functions.k:62-90` | `s` and `n` bind in order; `Return` sets `retV`, discards only the remaining function-body computation, and `#pop` restores the saved continuation/environment and removes the local frame. |
| Literals and assignment | `core.k:117-121,193-196`; `controls.k:8-18`; `list.k:12-20`; `str.k:12-22` | The result list allocates once at heap location 0; integer/string values are exact; ordinary local assignment updates only the current scope; string/list concatenation preserves order. |
| `for` over string | `controls.k:62-74,84-91`; `str.k:7-10`; `tuple.k:31-41` | The string evaluates once. Each step yields the next one-character string, binds `ch`, executes the exact body, then resumes the remaining suffix. Empty suffix ends without a body step. |
| `if` and `and` | `controls.k:50-54`; `bool.k:13-25`; `core.k:198-205` | Conditions are evaluated before branch selection; `and` short-circuits and returns a Boolean here. No skipped side effect occurs because both operands are comparisons. |
| Comparison and membership | `operators.k:10-20`; `int.k:22-27`; `str.k:24-41` | Integer and string equality are structural. One-character `ch not in "aeiouAEIOU"` becomes the negation of contiguous membership in the literal's exact ASCII codes. |
| Arithmetic and concatenation | `operators.k:10-17`; `int.k:9`; `str.k:20-24` | `count + 1` is integer addition; `word + ch` is order-preserving code-sequence concatenation. |
| Attribute/call/append | `call.k:15-24,52-67`; `list.k:52-55`; `controls.k:46-48` | `result.append(word)` retains the heap reference, appends exactly one string in place, returns `noneV`, and the expression statement discards that value. |

The priorities reached on this path only select the more specific list-mutator,
heap dereference, or ordinary non-cell alternatives.  Their guards are
disjoint from the generic alternatives where required; none changes the task's
computed value.

## Proof-local declarations and rules

There are no proof-local `<k>`/cell rules, priority rules, macros, opaque
symbols, `functional` declarations, or trusted primitives.  Thus there is no
operational bridge to validate.  All proof-local rules are equations over
syntax names or mathematical summaries.

| Inventory ID / lines | Extension | Classification and rule-by-rule decision |
|---|---|---|
| K1067, `verification.k:9-11` | `charLoopBody`, `afterCharLoop`, `selectWordsBody` (`function,total`) | Complete: each nullary syntax function has exactly one unconditional equation (K1074-K1076). They are AST names, not result or operational oracles. |
| K1068, `verification.k:15-20` | `selectScan`, `scanAccum`, `flushSelected` (`function,total`) | Complete over constructor `IntSeq`, arbitrary integers, and `ValSeq`; coverage is supplied by K1077-K1086. |
| K1069, `verification.k:22-23` | `wordAfter`, `charAfter` (`function,total`) | Complete over empty/cons `IntSeq`; coverage is K1087-K1089 and K1094-K1095. |
| K1070, `verification.k:24` | `countAfter` (`function,total`) | Complete over empty/cons `IntSeq`; coverage is K1090-K1093. |
| K1074, `verification.k:31-49` | `charLoopBody` equation | Sound exact constructor abbreviation. The branch, nested conditional append, reset, concatenate, and conditional increment match regenerated `solution.mpy`. |
| K1075, `verification.k:51-59` | `afterCharLoop` equation | Sound exact constructor abbreviation for final nonempty/equal-count flush and return. |
| K1076, `verification.k:61-67` | `selectWordsBody` equation | Sound exact constructor abbreviation for all four initializations, the real `For`, and the exact final fragment. |
| K1077, `verification.k:70-72` | `flushSelected`, `COUNT != N` | Sound: a nonmatching count does not append, regardless of the word. |
| K1078, `verification.k:73-75` | `flushSelected`, equal count and empty word | Sound: empty runs are not emitted, including `N = 0`. |
| K1079, `verification.k:76-79` | `flushSelected`, equal count and nonempty word | Sound: appends exactly that word to the accumulator. Disjoint from K1078 by structural emptiness. |
| K1080, `verification.k:81-87` | `selectScan` | Sound definitional composition: scan all characters, then flush the separately computed final word/count. It never rewrites an MPY term. |
| K1081, `verification.k:90-92` | `scanAccum` empty suffix | Sound base case: no more separators have been seen, so the completed-word accumulator is unchanged. |
| K1082, `verification.k:93-97` | space, unequal count | Sound: do not append; reset word/count; consume one constructor. |
| K1083, `verification.k:98-102` | space, equal count, empty word | Sound: do not append an empty token; reset and consume one constructor. |
| K1084, `verification.k:103-111` | space, equal count, nonempty word | Sound: append once in encounter order, reset, and consume one constructor. Its guard is disjoint from K1083. |
| K1085, `verification.k:115-122` | nonspace vowel | Sound: extend the word without changing count; the membership predicate is the exact fixed-semantics predicate used by the program. |
| K1086, `verification.k:123-131` | nonspace nonvowel | Sound: extend the word and increment count. The guard is the Boolean complement of K1085. |
| K1087, `verification.k:135-136` | `wordAfter` empty suffix | Sound base case. |
| K1088, `verification.k:137-140` | `wordAfter` space | Sound reset and structural descent. |
| K1089, `verification.k:141-144` | `wordAfter` nonspace | Sound concatenation and structural descent; disjoint from K1088. |
| K1090, `verification.k:146-147` | `countAfter` empty suffix | Sound base case. |
| K1091, `verification.k:148-151` | `countAfter` space | Sound reset and structural descent. |
| K1092, `verification.k:152-157` | `countAfter` nonspace vowel | Sound unchanged count and structural descent. |
| K1093, `verification.k:158-163` | `countAfter` nonspace nonvowel | Sound increment and structural descent; guard complements K1092. |
| K1094, `verification.k:165-166` | `charAfter` empty suffix | Sound: an empty loop preserves the old target value. |
| K1095, `verification.k:167-169` | `charAfter` cons suffix | Sound: records the current character and structurally recurses, leaving the last character for nonempty input. |
| K1099, `spec.k:8-42` | loop reachability claim | Sound auxiliary circularity. It tracks the exact ordinary local frame and result-list heap entry. The exact body contains no return, break, continue, exception, allocation, or output, so the arbitrary trailing continuation and all framed cells are preserved. |
| K1100, `spec.k:47-77` | whole-program reachability claim | Result-constraining entry theorem. It loads and calls the submitted binding/body and constrains the returned reference, heap list, binding, allocation counters, stack, return, exception, and exit cells. |

For every recursive proof-local equation, the first `IntSeq` argument loses one
`iCons` on each recursive call.  `flushSelected` is nonrecursive and
`selectScan` expands once.  The equality/non-equality, space/nonspace,
empty/nonempty, and vowel/nonvowel guard partitions are exhaustive and
pairwise compatible.  No false-rule witness exists because no reviewed
proof-local rule has a false conclusion on its match domain.
