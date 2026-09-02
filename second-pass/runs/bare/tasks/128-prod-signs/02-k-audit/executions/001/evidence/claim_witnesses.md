# Entry and auxiliary claim witnesses

All maps below use the cells and constructors of `semantic.k`.

| Candidate claim | Satisfying initial witness | Claimed observable result |
|---|---|---|
| `spec.k:7` empty entry | `<input> input(.Ints) </input>`, empty function/env/result cells | `result(contract(.Ints)) = result(none)` |
| `spec.k:16` nonempty initialization | `X = 1`, `IS = .Ints`, otherwise initial cells | reaches `loop("x", 1, .Ints, solutionLoopBody)` with `total=0`, `sign=1`, `x=0`; no return is claimed |
| `spec.k:32` negative step | `X=-1`, `IS=.Ints`, `RHO=.Map`, `_OLD=0`, `T=0`, `S=1` | next loop has `x=-1`, `total=1`, `sign=-1` |
| `spec.k:47` positive step | `X=1`, `IS=.Ints`, `RHO=.Map`, `_OLD=0`, `T=0`, `S=1` | next loop has `x=1`, `total=1`, `sign=1` |
| `spec.k:62` zero step | `X=0`, `IS=.Ints`, `RHO=.Map`, `_OLD=1`, `T=3`, `S=-1` | next loop has `x=0`, `total=3`, `sign=0` |
| `spec.k:77` exit | `T=9`, `S=-1`, `_RHO=.Map` | `result(-9)` |
| `spec.k:86` documented example | fixed input `[1,2,2,-4]` and initial cells | `result(contract(...)) = result(-9)` |
| `spec.k:98` zero example | fixed input `[0,1]` and initial cells | `result(contract(...)) = result(0)` |
| `spec.k:110` odd-negative example | fixed input `[-1,-2,-3]` and initial cells | `result(contract(...)) = result(-6)` |

The intended universal nonempty entry claim is absent. In particular,
`spec.k:16` has no returned-value postcondition and none of the three
one-step claims records the original list or states an inductive
entry-to-exit invariant.
