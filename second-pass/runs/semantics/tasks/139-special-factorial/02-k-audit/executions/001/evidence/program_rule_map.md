# Submitted-program construct-to-rule map

The target is the `FuncDef` inside `solution.mpy`, not the separate assertion
driver. Generated strictness/heat-cool rules come from attributes in
`semantics/syntax.k`; all listed source files are byte-identical to the trusted
supplied-semantics tree.

| Submitted construct / runtime action | Declaration and operational rules | Static decision |
|---|---|---|
| `Module(...)` and statement list | `syntax.k:60`; `core.k:122-125` (`#loadAll`, left-to-right statement sequencing, empty list) | Executes the whole submitted module; no bypass. |
| `FuncDef(... Params("n") ...)` | `syntax.k:53-59`; `functions.k:14-16` | Binds the exact body as a closure in the module scope. |
| `Assign(Name(...), rhs)` | `syntax.k:41` `[strict(2)]`; `controls.k:8-10` | Evaluates RHS then writes the current scope; target names here have no target-evaluation effects. |
| `Name(...)` | `syntax.k:12`; `core.k:128-155` | Starts at current environment and follows parents only if absent. Every local used in the loop is found in the callee frame. |
| `Int(...)` | `syntax.k:9`; `core.k:197` | Exact unbounded mathematical integer value. |
| `Call(Name("special_factorial"), Int(N))` | `syntax.k:28`; `call.k:19-21`; `core.k:186-194`; `call.k:69-74` | Looks up the submitted closure, evaluates one argument left-to-right, allocates a callee frame, binds `n`, and executes the stored body. |
| Parameter bind | `functions.k:63-66` | Maps the single formal `n` to the evaluated integer argument. |
| `While(condition, body)` | `syntax.k:46`; `controls.k:75-81`, `84` | Re-evaluates the condition each iteration; true executes the body then loops, false exits. The helper claim starts at this real `#while` control point. |
| `Compare(Name("i"), CmpOp("<=", Name("n")))` | `syntax.k:30-32`; `operators.k:14-17`; `int.k:22` | Contexts evaluate left then right; dispatch computes mathematical integer `<=`; the resulting Boolean is consumed by `truthy`. |
| Integer truth | `core.k:199-205` | The comparison already yields a Boolean, so `truthy(B)` is exactly `B`. |
| `AugAssign(..., "*", ...)` | `syntax.k:44` `[strict(3)]`; `controls.k:20-23`; `int.k:11` | RHS is evaluated, the current local is read, integer multiplication is applied, then the binding is updated. |
| `AugAssign(..., "+", Int(1))` | Same strictness and update rule; `int.k:6` | Updates `i` to `i+1`. |
| `Return(Name("result"))` | `syntax.k:50` `[strict]`; `functions.k:78-89` | Evaluates the local result, records it, pops exactly the current call frame, restores the caller, and resumes its captured continuation. |
| Final `answer` binding | The entry claim appends a real `Assign` after the exact submitted `FuncDef`; `controls.k:8-10` | Stores the actual returned value. Postcondition fixes it to `specialFactorial(N)`. |
| `factorial` proof summary | `verification.k:8-12` | Base/step guards are disjoint and exhaustive on `Int`; positive recursion strictly descends. This names ordinary factorial without rewriting program control. |
| `specialFactorial` proof summary | `verification.k:15-20` | Base/step guards are disjoint and exhaustive; positive recursion strictly descends and defines the product of factorials. It does not intercept a call or loop. |

No rule in `verification.k` matches a `<k>` cell, a program call, a loop, a
return, a frame, or state. There are no proof-local priorities,
`[simplification]` rules, `[concrete]` rules, opaque symbols, or operational
bridges. The only proof-local extensions are the two total summary declarations
and their four equations.
