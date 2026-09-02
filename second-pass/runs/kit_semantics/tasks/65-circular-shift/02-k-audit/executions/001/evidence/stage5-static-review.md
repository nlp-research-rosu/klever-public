# Stage 5 static soundness review

## Inventory scope and per-entry disposition

`stage5-rule-inventory.json` and `stage5-rule-inventory.md` exhaustively
inventory all 25 K source files used by the fresh build: the supplied
`semantics.k`, its 23 helper files, and proof-local `verification.k`. The 1,074
outer sentences comprise 147 function declarations, 109 declarations carrying
`total`, no `functional` declarations, 82 other syntax declarations, one
configuration, five contexts, 654 ordinary rules, 45 priority rules, one
simplification rule, and structural module/import sentences. Every entry has a
stable source range/hash, full normalized text, and one of these explicit
decisions:

- 157 entries are `USED_FIXED_SEMANTICS_REVIEWED`. These conservatively
  over-approximate the submitted program's execution path. The inventory's
  used-path matrix checks their configuration, evaluation order, binding,
  frame/state effects, arithmetic, string, and slicing roles.
- 907 entries are `UNUSED_TRUSTED_FIXED_SEMANTICS`. They are byte-identical to
  the launcher-supplied fixed semantics and unreachable from this submitted
  constructor/call path. They supply no candidate proof extension and cannot
  rewrite a state reached by this theorem.
- The ten proof-module entries receive individual decisions: three structural
  module sentences, two exact closure-definition sentences, four
  result-definition sentences, and one hook-definedness simplification.

This is a per-entry decision, not an assumption that arbitrary candidate rules
are safe. The recursive integrity check establishes that the 1,064
non-proof-local entries are exactly the selected supplied semantics. The
proof-local entries are audited below.

## Submitted constructors and fixed execution path

The submitted `solution.mpy` contains exactly:

`Assign`, `BinOp`, `Call`, `CmpOp`, `Compare`, `FuncDef`, `IfExp`, `Int`,
`Module`, `Name`, `NoBound`, `Params`, `Return`, `Slice`, `Subscript`, and
`UnaryOp`.

The inventory maps every constructor to declarations and rules. In summary:

- `core.k` initializes the complete configuration, loads the module, sequences
  statements left-to-right, performs lexical lookup, evaluates call arguments
  left-to-right, and defines exact sequence lengths.
- `functions.k` binds the translated body into environment 0, binds both
  parameters in order, records the return value, pops/deallocates the local
  frame, and restores the caller environment and scope allocator.
- `call.k` evaluates the callee before arguments, selects the pinned global
  closure or fixed `str`/`len` builtin, allocates a real user-function frame,
  and schedules the actual body. No call interception or operational summary
  applies.
- `controls.k` evaluates the assignment RHS before the local update and selects
  only one `IfExp` branch.
- `operators.k` plus `int.k` implement exact unbounded integer negation,
  subtraction, multiplication, and `<`/`>`; `str.k` implements structural
  concatenation; `subscript.k` evaluates slice bounds in Python order and uses
  CPython-style defaults/clamps followed by structural `buildIS`.

The initial and final claims pin all active cells. The function is pure on this
domain: its temporary local `s` lives only in the allocated call frame; the
heap remains empty; frame pop restores `<env>`, `<scopes>`, `<scopeLoc>`,
`<stack>`, and `<ret>`; no exception or exit-code transition occurs.

## Proof-local declaration/rule review

| Source | Class | Static decision |
|---|---|---|
| `verification.k:9` `#Ceil(strToCodes(Int2String(X))) => #Top [simplification]` | Trusted-primitive definedness fact | Sound. K declares `Int2String` total and documents a nonempty decimal digit string with an optional minus sign; the implementation is `BigInteger.toString()`. Every resulting character is ASCII, so the guarded `strToCodes` recursion is defined. It adds no value equation. A clean definition with this rule removed still proves all three claims together (`stage5-no-ceil-kprove-all.log`), so target closure does not depend on it. |
| `verification.k:14-46` `circularShiftClosure` | Exact definitional name | One unguarded equation covers the nullary total symbol. It rewrites only the name, never a `Call` or body step. The generated constructor-equality claim is `#Top`; mutating the closure bound in the executed state to `return s` is rejected with the concrete residual `"12"`. |
| `verification.k:50` `circularShiftResult` declaration | Result definition | A result-constraining postcondition symbol, not an operational bridge. It never appears in an execution rule LHS or source-program binding. |
| `verification.k:52-58` reverse equation | Definitional summary | Guard is `shift > n`. With nonempty decimal code sequence length `n`, `buildIS(codes,n-1,-1,-1)` visits exactly `n-1,...,0`, hence is the reverse. |
| `verification.k:60-64` negative equation | Definitional summary | Guard is `not(shift > n) and shift < 0`. Python slice saturation makes the canonical `s[n-shift:] + s[:n-shift]` equal `"" + s`; the candidate's explicit `s` branch is equivalent. |
| `verification.k:66-86` rotation equation | Definitional summary | Guard is `not(shift > n) and not(shift < 0)`, hence `0 <= shift <= n`. On doubled sequence length `2n`, adjusted bounds are `n-shift` and `2n-shift`; `buildIS` returns exactly `n` characters, the suffix followed by the prefix. |

Let `B` mean `shift > n` and `C` mean `shift < 0`. The guards are `B`,
`not B and C`, and `not B and not C`: pairwise disjoint and exhaustive. Thus
the `total` result declaration has exactly one applicable equation for every
integer pair once `strToCodes(Int2String(X))` is defined. The closure constant
also has exactly one equation. Recursive fixed functions used in each RHS
descend over a finite code sequence or move the slice index monotonically
toward its stop.

## Opaque symbols, priority, totality, and overlap

The inventory enumerates 22 explicit `[no-evaluators]` symbols in the supplied
semantics: the MD5 summary; nineteen float/conversion summaries; and two sort
summaries. None occurs in `solution.mpy`, `verification.k`'s result equations,
or a reachable call path. There is no proof-local opaque symbol.

All 45 priority rules belong to the supplied semantics. They disambiguate heap
reference/cell/method or concrete-only behavior. The submitted execution uses
integer/string values with an empty heap and plain closure frame, so no
proof-local priority or task-specific preemption exists. There is one
proof-local simplification rule, reviewed above, and no proof-local `owise`,
`macro`, operational bridge, auxiliary circularity, or call interception.

Fresh compiler warnings identify non-exhaustive `total` functions
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is on
this program's path (string slicing uses `buildIS`/`intSeqAt`, not
`valSeqAt`). The used total functions have constructor or complementary-guard
coverage on their actual domains. `strToCodes` is intentionally partial for
arbitrary Unicode strings, but this theorem feeds it only the fixed decimal
`Int2String` result described above.

## Soundness conclusion

No inventoried candidate rule encodes an execution result, replaces a
property-bearing source computation with an oracle, bypasses the real body, or
fabricates state/control. `circularShiftResult` states the postcondition, while
fixed semantics independently executes the same primitive operations to reach
it. No rule was classified as unsound, so there is no false-conclusion witness
to report. The only non-source rule involving a primitive is a true,
value-free, and empirically unnecessary definedness fact.
