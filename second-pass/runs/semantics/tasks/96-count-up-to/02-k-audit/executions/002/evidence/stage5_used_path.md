# Used-path semantics map

This map is based on the byte-identical regenerated `solution.mpy`. The full
declaration/rule inventory is `stage5_rule_inventory.tsv`; entries outside this
map were checked for constructor/operator overlap and cannot fire on this
program's proof path.

| Submitted construct/effect | Declaration | Operational rules | Audit result |
|---|---|---|---|
| `Module`, `FuncDef`, `Params`, statement sequencing | `syntax.k:53,57,61`; `core.k:124-127`; `functions.k:14-16` | Module loading binds `count_up_to` to its exact translated body; sequencing is left-to-right. | Sound; the proof starts at the mechanically identical body in a call frame. |
| Integer and Boolean literals | `syntax.k:9,11`; `core.k:193-196` | Constructors reduce to K `Int`/`Bool`. | Sound. |
| Name lookup and local assignment | `syntax.k:12,41`; `core.k:129-154`; `controls.k:9-18` | Lookup walks the pinned local scope; assignments update that scope. Cell cases cannot match the plain frame. | Sound and binding-pinned. |
| Empty list construction/allocation | `syntax.k:17`; `list.k:13-15`; `core.k:117-121,183-191,217-219` | Elements evaluate left-to-right, `list(.ValSeq)` is allocated at fresh heap location 0, and `heapLoc` advances. | Sound; freshness follows from the empty initial heap. |
| `while` and loop continuation | `syntax.k:46`; `controls.k:65-82,85` | Condition is evaluated on every iteration; truthiness selects body/exit; loop label resumes. | Sound. Both candidate summaries were independently reproved over their complete rule match domains. |
| `<` and `==` comparisons | `syntax.k:30,32`; `operators.k:14-17`; `int.k:22-27` | Left then right evaluation, followed by integer comparison. | Sound. Reference dereference cases cannot match integer operands. |
| `%` and `+` arithmetic | `syntax.k:15`; `operators.k:10-12`; `int.k:9-20` | Integer modulo uses `pyMod`; addition is unbounded integer addition. Divisors on the used path satisfy `D >= 2`, avoiding zero. | Sound on the full formal domain. |
| `if` and Boolean truthiness | `syntax.k:49`; `controls.k:50-54`; `core.k:198-205` | The strict guard reduces to Boolean truthiness and selects exactly one branch. | Sound. |
| `AugAssign` | `syntax.k:44`; `controls.k:20-31` | Reads the existing integer binding, applies integer `+`, and writes the result. The reference-valued priority case cannot match. | Sound. |
| `result.append(candidate)` | `syntax.k:28-29,52`; `call.k:15-24,52-74`; `list.k:18-20,52-55`; `controls.k:46-48` | Receiver and argument evaluate left-to-right; the exact `append` bound method mutates the referenced heap list; its `noneV` result is discarded. | Sound; only heap cell 0 changes. |
| Function return/frame pop | `syntax.k:50`; `functions.k:77-90` | The result name evaluates to `ref(0)`, `Return` discards the exact trailing `#endcall`, and `#pop` restores env/scope/stack while preserving the heap. | Sound; the entry claims pin every affected cell. |

## Candidate proof extensions

| Extension | Class and domain | State/value effect | Independent validation |
|---|---|---|---|
| `noDivisor(C,D,HI)` (`verification.k:9-17`) | Definitional summary. On every proof use, `2 <= D <= HI`; three guards are exhaustive and disjoint. Recursion strictly increases `D` until `HI`. | Boolean only. It is false iff a divisor in `[D,HI)` has zero `pyMod`. | Ordinary integer mathematics plus the inner-loop proof. |
| `appendIfPrime(VS,I,B)` (`verification.k:20-24`) | Definitional summary; two Boolean constructor cases are exhaustive and disjoint. | Appends exactly `I` iff `B=true`. | Direct equations. |
| `primesAcc(VS,I,N)` (`verification.k:29-38`) | Definitional summary; `I>=N` and `I<N` are exhaustive/disjoint. On recursive use, `I` increases by one. | Exact ordered accumulation of values passing `noDivisor(I,2,I)`. | Direct equations plus outer-loop proof. |
| Inner loop summary (`verification.k:46-73`) | Operational bridge for `2 <= D <= C`; exact loop syntax, env, scope maps, locals, and heap; arbitrary continuation and omitted cells are framed. | Sets `divisor=C` and `is_prime=B and noDivisor(C,D,C)`; preserves all other cells. | `stage5_bridge_connections.k`, module `AUDIT-FULL-INNER-BRIDGE-SPEC`, proves `#Top` against `COUNT-UP-TO-BASE`, with no inner summary imported. |
| Outer loop summary (`verification.k:82-122`) | Operational bridge for `2 <= I <= N`; exact loop syntax and state; arbitrary continuation and omitted cells are framed. | Sets `candidate=N` and replaces the result sequence by `primesAcc(VS,I,N)`; preserves all other cells. | `stage5_bridge_connections.k`, module `AUDIT-FULL-OUTER-BRIDGE-SPEC`, proves `#Top` without importing the outer summary; it uses only the separately validated inner theorem. |

There are no `[simplification]` or `[functional]` declarations in the audited
sources. Proof-local priority rules are only the two derived loop summaries;
their priority makes them preempt ordinary unrolling but does not change their
independently checked transition. Proof-local `symbol`/`no-evaluators`
attributes do not introduce opaque results because every used constructor has
complete defining equations on its use domain.
