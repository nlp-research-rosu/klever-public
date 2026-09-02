# Executed constructor-to-semantics map

This map is for the byte-identical regenerated `solution.mpy`. The complete
source inventory is in `rule-inventory.md`; entries below identify the material
rules on the submitted program's path.

| Program constructor/operation | Declaration and fixed rules | Review decision |
|---|---|---|
| `Module`, statement sequencing | `syntax.k:41-61`; `core.k:124-127` | Accept. `#loadAll` exposes the module statements and sequencing preserves source order. |
| `FuncDef("sort_even", Params("l"), BODY)` | `syntax.k:50-61`; `functions.k:14-16` | Accept. It binds exactly `closureVal("l", BODY, 0)` in module scope. |
| `Call`, callee lookup, argument evaluation | `call.k:17-21`; `core.k:130-153,188-205` | Accept. Callee then arguments evaluate left-to-right; name lookup follows the current scope and builtins parent. |
| User-function frame and parameter `l` | `call.k:69-76`; `functions.k:63-75` | Accept. A fresh local scope is created, the caller continuation is stored in one frame, and `l` is bound before the exact body runs. |
| `result = list(l)` | `builtins.k:32`; `core.k:104-122` | Accept. The external bare-list input is dereferenced as a value and a fresh heap list is allocated at location 0. |
| `l[::2]` | `subscript.k:27-32,44-69,72-114`; `core.k:223-239` | Accept for step 2 and `vsLen(VS) >= 0`. Bounds become `0`, `vsLen(VS)`, and `2`; `buildVS` selects exactly indices `0,2,...` and allocates heap location 1. |
| `sorted(...)` | `sort.k:18-37`; `call.k:24-32`; `core.k:157-180` | Accept as a supplied external primitive boundary. The call resolves the builtin binding, allocates location 2, and returns `sortVS(even-projection)`. `sortVS`'s ascending-permutation meaning is trusted/empirically checked rather than proved by the task theorem. |
| `len(l)` | `builtins.k:20-26` plus call/name rules | Accept. It reduces to `vsLen(VS)`. |
| integer `+`, `*`, and `//` | `operators.k:9-17`; `int.k:9-20` | Accept on this path. Divisor is the literal 2; `pyMod` implements Python floor division and cannot encounter zero here. |
| `range((len(l)+1)//2)` | `builtins.k:177-180`; `range.k:9-24` | Accept. It produces `rangeObj(0,C,1)` and yields each integer `0 <= i < C`. |
| `For` and target binding | `controls.k:65-74`; `tuple.k:31-41`; `range.k:20-24` | Accept. Each yield binds `i`, executes one body, then resumes the exact remaining range. |
| RHS `evens[i]` | `subscript.k:27-40`; `core.k:223-226` | Accept for reachable `0 <= i < C`, where `C` is the even-projection length. Heap ref 2 is read and `valSeqAt` selects the corresponding sorted value. |
| target index `2*i` | `operators.k:9-12`; `int.k:14` | Accept. Both operands are integers and the result is nonnegative for the reachable loop counter. |
| `result[2*i] = ...` | `dict.k:76-92`; `core.k:233-239` | Accept. Despite its file placement, these generic target rules evaluate the index after the RHS, recognize the local heap ref, normalize the nonnegative index, and update only heap list location 0 with `setVSAt`. |
| `return result` and frame cleanup | `functions.k:78-90`; lookup rules above | Accept. It sets `retV(ref(0))`, discards only the remaining function statements, restores environment 0, removes local scope 1, pops exactly one frame, and leaves heap allocations observable. |
| Proof-local body macros | `verification.k:8-9,27-49` | Accept. `program_identity.py` expands both macros and matches the trusted regenerated `FuncDef` body constructor-for-constructor. |
| `evenCount` | `verification.k:12,51-52` | Accept. Its single equation is algebraically identical to the fixed `// 2` rule; the entry only uses the nonnegative `vsLen`. |
| `fillEven` | `verification.k:15-16,54-63` | Accept. Guards `I >= STOP` and `I < STOP` are disjoint/exhaustive; the step mirrors one fixed body iteration and advances `I`. The bridge-free connection theorem universally validates the used operational meaning. |
| `sortEvenResult` | `verification.k:20,65-70` | Accept. It is a pure composition of the copied input, fixed even projection, supplied `sortVS`, exact count, and validated `fillEven`. |
| Exact loop bridge | `verification.k:85-134` | Accept. `bridge_context_check.py` proves textual identity of its complete cells/guard with `SPEC-CONNECTION.loop-connection`; the connection theorem imports only `VERIFICATION-NO-BRIDGE` and closes independently. |

The program does not use floats, strings, sets, tuples, dictionaries as data
structures, comprehensions, `while`, exceptions, imports, keyed sorting,
methods, or the concrete-only keyed-sort/deep-equality rules. Their declarations
and rules remain inventoried because they are imported by `MPY`; inspection
found no pattern capable of preempting the used terms except the explicit
fixed priorities listed above.
