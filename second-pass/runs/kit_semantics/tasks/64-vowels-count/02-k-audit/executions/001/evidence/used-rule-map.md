# Material static rule map

The exhaustive inventory is in `rule-inventory.md`. This companion map gives
the dependency cone for the submitted constructor term and the proof-local
extensions. All omitted inventory rows have a top symbol that cannot arise
from this program or from either claim; constructor sorting and guards prevent
them from rewriting a reachable target state.

| Program construct / obligation | Fixed or proof rule | Static decision |
|---|---|---|
| `Module(...)` load and statement order | `semantics/core.k:124-127` | `#loadAll` exposes the module statement list; sequencing evaluates each statement left-to-right. |
| Function definition and binding | `semantics/functions.k:14-16` | Installs the exact `closureVal(params, body, defining-scope)` in module scope 0. |
| Name lookup | `semantics/core.k:130-154` | Looks in the current frame, then parents. All reachable names are concretely bound; the cell-specific priority rule is guard-false because this unannotated function has no `$cells`. |
| Call evaluation | `semantics/call.k:19-21`, `semantics/core.k:185-191` | Evaluates callee, then arguments left-to-right. No problem-local interception or builtin dispatch matches this closure call. |
| Closure application | `semantics/call.k:69-76` | Allocates callee scope 1, pushes the exact caller continuation/frame, binds arguments, executes the exact body, then `#endcall`. |
| Parameter binding | `semantics/functions.k:63-75` | Binds `s` to the supplied `str(INPUT)` value. The cell-specific priority alternative is guard-false. |
| Integer and string literals | `semantics/core.k:194`, `semantics/str.k:13-17` | Integer zero is exact. All body literals are ASCII and satisfy `strToCodes`’ ASCII guard, producing the listed code sequences. Input is already a `str(IntSeq)` and does not use literal conversion. |
| Simple assignments | `semantics/controls.k:9-17` | Writes `count`, `last`, and `char` in the current callee scope. Cell-priority alternative is guard-false. |
| `for char in s` | strict attribute in `semantics/syntax.k:45`; `semantics/controls.k:65-74`; `semantics/str.k:8-10`; `semantics/tuple.k:31-40` | Evaluates `s` once, yields one-character strings in order, binds `char`, executes `count += ...` then `last = char`, and resumes on the remaining string. |
| Comparisons | contexts and dispatch in `semantics/operators.k:15-17`; string cases in `semantics/str.k:25-41` | Left then right evaluation reaches constructor-disjoint `str/str` equality or membership. One-character membership is true exactly for a listed vowel code. |
| `count += Bool` | strict RHS attribute in `semantics/syntax.k:43`; update rule `semantics/controls.k:20-24`; arithmetic rule `semantics/int.k:11` | Converts `true/false` to `1/0` and adds it to the integer accumulator. The heap-ref priority alternative is guard-false. |
| Return and cleanup | `semantics/functions.k:78-91` | `Return` records the value, discards the rest of the callee continuation as an abrupt return, pops the exact frame, removes callee scope 1, restores caller env/scopeLoc, and leaves heap and caller state unchanged. |
| `vowelsTail` declaration | `verification.k:9` | Proof-local definitional summary, not an operational bridge. `[total]` is justified by exhaustive first-argument constructors. |
| `vowelsTail` base | `verification.k:11-13` | Adds exactly one for remembered final `y` or `Y`; the equalities cannot both be true. |
| `vowelsTail` step | `verification.k:15-28` | Counts the current character by truthful fixed `strContains`, replaces remembered last with that one character, and structurally descends on `REST`. |
| Loop circularity | `spec.k:6-55` | Matches the exact loop body, exact post-loop comparisons, exact return and `#endcall`, arbitrary caller continuation, complete live cells, and the exact four-key callee frame. It does not become an operational semantics rule outside proof use. |
| Entry theorem | `spec.k:57-130` | Loads the mechanically identical submitted `Module`, calls that closure with every `str(INPUT:IntSeq)`, and constrains the returned `<k>` value to `vowelsTail(INPUT,.IntSeq)` while pinning the final state. |

Overlap and totality conclusions:

- The two proof-local equations are constructor-disjoint (`.IntSeq` versus
  `iCons`) and the recursive call strictly descends.
- The proof adds no priority, `owise`, simplification, `[concrete]`,
  `[no-evaluators]`, or opaque symbol.
- The fixed theory contains 22 `no-evaluators` declarations and 35
  concrete-only equations, but all are outside the target dependency cone.
- Relevant priority overlaps are narrowed by concrete guards (`$cells` or
  heap-reference tests); every such special case is false on the target’s
  integer/string locals and empty heap.
- LLVM compilation warns about six non-exhaustive fixed-semantics helper
  functions. Their symbols (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
  `joinCodes`, `valSeqAt`) are unreachable from both target claims.

No static rule in the dependency cone enables a false conclusion witness.
Accordingly, no rule is labeled unsound; the remaining trust is the supplied
semantics and K’s builtin integer, Boolean, string, map/list, and equality
theories.
