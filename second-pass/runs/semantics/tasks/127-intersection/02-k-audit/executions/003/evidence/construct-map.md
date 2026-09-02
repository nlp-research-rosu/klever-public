# Submitted constructors to supplied semantics

The regenerated `solution.mpy` uses only the constructors below. Line references
are to the trusted `/reference/reference-semantics` tree.

| Submitted constructor or runtime form | Declaration | Material rules |
|---|---|---|
| `Module`, `Stmts` sequence | `semantics/syntax.k:56-61` | `semantics/core.k:124-127` (module loading/sequencing; the entry claim starts after module loading) |
| `FuncDef` / `closureVal` | `semantics/syntax.k:53`; `semantics/core.k:31` | `semantics/functions.k:14-16`; the entry claim supplies exactly this resulting closure |
| `Call` | `semantics/syntax.k:28` | `semantics/call.k:20-21,31-32,69-74`; `semantics/core.k:189-191` |
| `Name` lookup | `semantics/syntax.k:12` | `semantics/core.k:131-154`; builtins frame at `157-181` |
| `TupleExpr` arguments | `semantics/syntax.k:21` | `semantics/tuple.k:14-16` |
| `Int` and `Str` literals | `semantics/syntax.k:9,13` | `semantics/core.k:194`; `semantics/str.k:13-17` |
| `Subscript(..., Int(0/1))` | `semantics/syntax.k:22,38` | contexts and lookup at `semantics/subscript.k:27-41` |
| `max(x,y)` and `min(x,y)` | builtin registrations `semantics/core.k:163-164` | call dispatch `semantics/call.k:31`; variadic folds `semantics/builtins.k:97-105` |
| `Assign(Name(...), value)` | `semantics/syntax.k:41` | `semantics/controls.k:9-18` (plain-frame branch is used) |
| integer subtraction and modulo | `semantics/syntax.k:15`; dispatch `semantics/operators.k:12` | `semantics/int.k:13,15,19-20` |
| integer `<=` and `==` comparisons | `semantics/syntax.k:30,32`; contexts/dispatch `semantics/operators.k:15-17` | `semantics/int.k:23,26` |
| `If` | `semantics/syntax.k:49` | `semantics/controls.k:51-54`; integer truthiness `semantics/core.k:199-205` |
| `range(2,length)` | builtin registration `semantics/core.k:167` | `semantics/builtins.k:177-180`; range iteration `semantics/range.k:9-24` |
| `For` / internal `#loop` | `semantics/syntax.k:45` | `semantics/controls.k:65-74,85`; iterator declaration `semantics/iter.k:8` |
| loop-target binding | `semantics/tuple.k:31-41` | plain-frame `#bindTgt(Name,Val)` branch |
| `Return` / call-frame pop | `semantics/syntax.k:50` | `semantics/functions.k:78-90` |

The program never reaches lists, dictionaries, sets, comprehensions, sorting,
methods, float operations, slicing, imports, assertions, lambdas, closures with
cells, `while`, `break`, or `continue`. Their declarations and rules remain in
the exhaustive `rule-inventory.tsv`; none can rewrite a constructor in this
program's reachable configurations.

# Proof-local extension assessment

| Source | Class | Assessment |
|---|---|---|
| `verification.k:9-10` map deletion normalization | Derived low-level map lemma | For a map consisting of key `1` plus a remainder disjoint from `1`, deleting key `1` yields that remainder. It changes no program value and only normalizes the symbolic frame deletion performed by fixed `#pop`. |
| `verification.k:15-43` `intersectionBody`, `divisorBody` | Definitional summaries | Exact aliases for the trusted translator's constructor body. `constructor-pinning.k` mechanically checks the equality after parsing/normalization. |
| `verification.k:46-49` `yesV`, `noV` | Definitional summaries | Exact ASCII `str(IntSeq)` encodings of `"YES"` and `"NO"`. |
| `verification.k:53-65` `primeFrom`, `primeResult` | Definitional mathematical summary | Guards are disjoint and cover every used state (`N>1`, `2<=D<=N`); recursion increases `D`; equations are exhaustive divisor search and agree with the program's `%` operation. They do not replace program execution. |
| `verification.k:67-69` `overlapLength` | Definitional mathematical summary | Exactly `min(B,D)-max(A,C)`, matching both implementations. |
| `verification.k:78-106` loop rule | Operational bridge / installed proved lemma | Its complete domain is the `LOOP-SPEC` claim proved bridge-free under `VERIFICATION-BASE`: same loop/body/trailing return and `#endcall`, arbitrary `KONT`, same binding/frame cells and guard. It reads the loop state and performs the exact return/frame-pop footprint established by that claim. |

No candidate-local symbol is opaque, `total`, `functional`, `simplification`,
`anywhere`, or `no-evaluators`. The sole candidate-local priority rule is the
installed loop theorem at priority 40.
