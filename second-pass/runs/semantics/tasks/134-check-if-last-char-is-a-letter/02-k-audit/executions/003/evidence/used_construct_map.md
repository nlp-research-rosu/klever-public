# Used-constructor and rule map

This map is the dependency slice for the regenerated `solution.mpy`. The
complete declaration/rule inventory, including unused supplied-semantics
constructs, is in `k_rule_inventory.tsv`.

| Submitted constructor/operation | Declaration and execution rules | Static result |
|---|---|---|
| `Module` | `semantics/syntax.k:63`; `semantics/core.k:124-127` (`#loadAll`, statement sequencing) | Module loading executes the sole `FuncDef`; the proof adapter omits this load but mechanically embeds the resulting capture-free closure. |
| `FuncDef`, `Params` | `semantics/syntax.k:53,58,60`; `semantics/functions.k:14-16` | Binds `closureVal(PNS,BODY,L)` in current scope. The adapter uses the same parameter/body and lexical scope `0`. |
| `Call` of user closure | `semantics/syntax.k:28`; `semantics/call.k:20-21,69-74`; `semantics/functions.k:63-90` | Callee and arguments evaluate left-to-right; a fresh frame is allocated, `txt` is bound, returns set `<ret>`, and `#pop` restores caller cells. No proof-local shortcut replaces body execution. |
| `Name("len")`, `Name("txt")` | `semantics/syntax.k:12`; `semantics/core.k:130-155,157-180` | Ordinary lexical lookup reaches local `txt` or the builtins scope. |
| `len(txt)` | `semantics/builtins.k:17-25`; generic call route in `call.k` | `len(str(IS))` reduces through `seqLen` to `isLen(IS)`. |
| `If` | `semantics/syntax.k:48`; strictness plus `semantics/controls.k:51-54` | Condition evaluates first, then exactly one branch executes. |
| `Return` | `semantics/syntax.k:49`; strictness plus `semantics/functions.k:78-90` | Evaluated value becomes `retV`, the remaining function continuation is discarded, and the frame is popped. |
| `Bool`, `Int`, `Str` | `semantics/syntax.k:9-13`; `semantics/core.k:195-197`; `semantics/str.k:12-17` | Bool/int literals are values. `" "` is an ASCII literal and becomes code point `32`. |
| `UnaryOp("not",...)` | `semantics/syntax.k:14`; `semantics/operators.k:10`; `semantics/bool.k:8`; truthiness in `core.k:199-205` | Boolean negation is faithful on the boolean returned by `isalpha`. |
| `UnaryOp("-", Int(1/2))` | same dispatch plus `semantics/int.k:6` | Produces `-1` or `-2`. |
| `Subscript(txt,-1/-2)` | `semantics/syntax.k:26`; `semantics/subscript.k:16-41` | `normIdx` adds string length and `intSeqAt` selects the indexed code. Claims avoid out-of-bounds use through the preceding length branches. |
| `Attribute(...,"isalpha")`, zero-argument method call | `semantics/syntax.k:29`; `semantics/call.k:16,20-24`; `semantics/methods.k:10,15,112-134` | Dispatch is operationally complete, but `isAlphaC` is ASCII-only. This disagrees with real Python `str.isalpha()` for Unicode letters such as U+00E9. |
| `Compare(...,"==",...)` | contexts and dispatch in `semantics/operators.k:15-17`; int cases `semantics/int.k:20-25`; string cases `semantics/str.k:24-26` | Length and penultimate-space comparisons reduce to booleans. |
| Statement list sequencing | `semantics/core.k:124-127` and strictness generated from syntax attributes | Early return prevents later statements from executing; otherwise statements run in source order. |

## Proof-local declarations

| Inventory IDs | Extension | Class and review |
|---|---|---|
| K0929-K0930 | `#checkIfLastChar` syntax and rewrite | Entry adapter. It constructs and calls the exact regenerated capture-free closure; it does not summarize the return value. It omits the module-level name binding, which is inert for this nonrecursive body but changes the otherwise-observable module scope. |
| K0931 | `isLen(seqConcat(P,[A,B])) => isLen(P)+2` | Derived sequence lemma. True by induction for finite constructor `IntSeq`; overlaps with fixed equations agree and recursion descends. A bridge-free symbolic `kprove` did not establish the unrestricted equation because the backend does not split abstract `P`. |
| K0932 | `intSeqAt(seqConcat(P,[A,B]),isLen(P)) => A` | Derived sequence/index lemma. True by induction for finite constructor `IntSeq`; fixed-rule overlaps agree. Same universal machine-check evidence gap. |
| K0933 | analogous index at `isLen(P)+1` returning `B` | Derived sequence/index lemma. Same review and evidence gap. |

No proof-local function, `total` declaration, opaque symbol, priority rule, or
task-answer oracle exists. The only proof-local attribute is `simplification`
on K0931-K0933. The 25 opaque/external functions in the supplied tree are
listed in the complete inventory and are unreachable from this program slice.
