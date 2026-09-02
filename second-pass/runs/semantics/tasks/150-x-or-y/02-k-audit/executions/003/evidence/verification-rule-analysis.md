# Proof-local declaration and rule analysis

The complete mechanical inventory is `rule-inventory.tsv`. This file gives the
proof-local decision and justification for every declaration/rule in
`verification.k`.

| Location | Extension | Class and decision | Justification |
|---|---|---|---|
| 8 | `xOrYLoopBody` syntax macro | Definitional syntax; accepted | It introduces no runtime rewrite after macro expansion. Expanded KAST equals the translated inner `If` constructor. |
| 9–14 | `xOrYLoopBody => If(...)` | Definitional macro; accepted | Exact constructor identity; it executes `%`, `==`, and `Return` under the fixed semantics. |
| 16 | `xOrYBody` syntax macro | Definitional syntax; accepted | No opaque value or operational shortcut. |
| 17–23 | `xOrYBody => If ... For ... Return` | Definitional macro; accepted | Expanded KAST is byte-translation constructor-identical to the submitted function body. |
| 26 | `#xOrY(Int,Val,Val)` syntax macro | Definitional entry syntax; accepted | Restricts `n` to the intended integer domain and allows all supplied-semantics values for `x,y`. |
| 27–29 | `#xOrY => Call(closureVal(...))` | Definitional macro; accepted | Parameter list, body, defining module environment 0, and ground argument order were mechanically compared with the regenerated program. |
| 33 | `primeSelect` function declaration | Definitional mathematical summary; accepted | Not opaque and not declared total. Every occurrence has `D>=2`, where the equations below cover all cases. |
| 35–36 | `N<2 => Y` | Mathematical equation; accepted | Integers below 2 are not prime. Disjoint from all `N>=2` rules. |
| 38–39 | `N>=2, D>=N => X` | Mathematical equation; accepted | No candidate divisor remains in `[D,N)`. Disjoint from `D<N`. |
| 41–43 | `D<N, pyMod(N,D)=0 => Y` | Mathematical equation; accepted | A divisor in `[2,N)` witnesses compositeness. `D` is positive, so supplied `pyMod` equals Python `%`. |
| 45–49 | nondivisor recursion | Mathematical equation; accepted | Guard is the complement of the divisor rule on `D<N`; `D` increases by one and therefore reaches the base case for each finite integer `N`. |
| 52 | `scanLast` function declaration | Definitional state summary; accepted | Not opaque and not total. All uses satisfy `N>=2,D>=2`, where its equations cover every branch. |
| 54–55 | exhausted range keeps `OLD` | State equation; accepted | `#iterDone` performs no target binding. |
| 57–59 | divisor case yields `D` | State equation; accepted | The loop binds `divisor=D` before evaluating the body and returning. |
| 61–64 | nondivisor recursion | State equation; accepted | Target binding sets the local to `D`, then the range advances to `D+1`; recursion terminates as above. |
| 73–100 | loop summary priority rule | Operational bridge; accepted | It is exactly the independently closed `loop_correct` reachability claim, copied without broadening. Its domain includes the exact suffix `Return(x) ~> #endcall`, exact one-frame stack, plain local/module scopes, empty heap, fixed scope/heap locations, `NoExc`, and exit code 0. It changes precisely the same `<k>`, `divisor`, and `<ret>` fields and preserves every other cell. The valid body-sensitivity probe fails on reachable `n=9,D=3,OLD=2,x=1,y=2`. |

Guard overlap review: `primeSelect` and `scanLast` partition on `N<2` versus
`N>=2`, `D>=N` versus `D<N`, and zero versus nonzero modulus. No overlapping
right-hand sides disagree. Both recursions strictly increase `D` under
`D<N`. There are no proof-local `total`, `functional`, `simplification`,
`concrete`, `owise`, or opaque-symbol declarations. The sole priority
attribute is on the proven exact loop bridge.
