# Used-construct and state-transition map

This map is the reviewer’s static trace from the submitted `solution.mpy` to the
recursively verified supplied semantics. Lines refer to the scratch copy under
`/tmp/audit-work/submitted/reference-semantics/semantics/`.

| Program construct | Declaration | Operational path | Static decision |
|---|---|---|---|
| `Module`, statement sequence | `syntax.k:56-61` | `core.k:124-127` loads and left-to-right sequences all statements | Sound for the source AST; no statements are skipped |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` binds the exact body as `closureVal(...,0)` | Sound; the defining scope is the module scope pinned by the claim |
| Function `Call` | `syntax.k:28` | `call.k:20-21,69-74`, `core.k:189-191`, `functions.k:63-66,80-90` evaluate callee/arguments, allocate a frame, bind `a,b`, execute the body, and restore caller state | Sound for two evaluated integer arguments; argument order and control suffix are preserved |
| Integer literal and name lookup | `syntax.k:9,12` | `core.k:131-154,194` | Sound; lookup walks the current frame then parent, and both parameters/result are in the callee frame |
| `Assign(Name("result"), ListExpr())` | `syntax.k:17,41` | `list.k:14-15`, `core.k:117-121,189-191`, `controls.k:9-11` | Sound; empty list allocates heap location 0 and its reference is assigned in the callee |
| Integer `<=` comparison | `syntax.k:30,32` | `operators.k:15-17`, `int.k:23` | Sound mathematical dispatch to K integer `<=Int`; both operands evaluate in order |
| `and`/`or` | `syntax.k:16` | `bool.k:16-25` | Sound short-circuit/value-returning behavior; all operands here are booleans from comparisons |
| Four `If` statements | `syntax.k:49` | `controls.k:51-54` | Sound truth test and branch choice; empty else branches are preserved |
| Attribute/call `result.append(D)` | `syntax.k:28-29,52` | `call.k:16,20-24`; `list.k:53-55`; `controls.k:48` | Sound receiver binding and in-place heap update; returns `noneV`, then expression statement discards it |
| `Return(Name("result"))` | `syntax.k:50` | `functions.k:78-90` | Sound abrupt return: sets `retV(ref(0))`, pops the exact call frame, preserves escaped heap object, and restores module scope |
| Final configuration | `core.k:49-60` | Entry/post cells in `spec.k` constrain `k`, scopes, allocator counters, heap, stack, return state, exception, and exit code | Complete for all observable cells in the supplied configuration |

The program does not use loops, comprehensions, floats, strings, dictionaries,
sets, sorting, slicing, imports, exceptions, or proof-local operational bridges.
Rules for those constructs remain in the fixed supplied semantics but are not
reachable from the target term.

## Proof-local declarations

| Extension | Class and domain | Coverage/overlap/termination | Decision |
|---|---|---|---|
| `generateIntegersBody`, `solutionModule`, `generateIntegersClosure` | Macros naming the submitted body/module/closure | Macro expansion terminates; `kast --expand-macros` produced byte-identical KORE for the parsed submitted module and `solutionModule` | Accept: exact program pin, not an operational bridge |
| `betweenEndpoints(A,B,D)` | Definitional `Bool` summary over all K integers | One unconditional total equation; exactly the inclusive either-or endpoint test | Accept: ordinary integer/Boolean mathematics |
| `keepDigit(B,D,REST)` | Definitional `ValSeq` constructor selector | `true` and `false` rules are disjoint and exhaustive; no recursion | Accept: ordinary sequence construction |
| `evenDigits(A,B)` | Definitional expected-result summary | One unconditional total equation; finite nesting through digits 2,4,6,8 and the exhaustive `keepDigit` function | Accept: result definition exactly matches the contract’s even decimal digits |

No proof-local priority, simplification, concrete, `owise`, opaque, or
operational rewrite exists. The three proof-local functions occur only in the
postcondition-side expected result; program execution reaches that value through
the supplied operational rules.
