# Used-construct and rule map

This map covers every constructor in the trusted regenerated `solution.mpy`
and the extra `Call`/`#loadAll` terms used by the entry claim. Line numbers are
in the fresh scratch copy of the supplied semantics.

| Construct/operation | Declaration | Material rules | Static assessment |
|---|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:61-62`; `semantics/core.k:124` | `core.k:125-127` | `#loadAll` exposes the module statements and sequences them left-to-right, preserving the continuation. |
| `FuncDef`, `Params` | `syntax.k:50-57` | `functions.k:14-16` | Binds the exact body as `closureVal(PNS,BODY,L)` in the current module frame. No body summary or bypass occurs. |
| `Call(Name("count_upper"), str(S))` | `syntax.k:25`, `call.k:19` | `core.k:131-154`; `call.k:20-21,69-74`; `functions.k:63-66,78-90` | Resolves the actual module binding, evaluates the argument left-to-right, allocates a fresh call frame, binds `s`, executes `BODY`, and restores control/state on return. |
| `Assign` of `count`, `even`, `ch` | `syntax.k:39` | strictness generated from `[strict(2)]`; `controls.k:9-18` | Evaluates RHS before updating the current scope. The higher-priority cell case is inapplicable because this plain frame has no `$cells`. |
| `Int(0)`, `Bool(true)`, `Str("")`, `Str("AEIOU")` | `syntax.k:9-13` | `core.k:194-196`; `str.k:13-17` | Integer/Boolean literals reduce directly. Both used strings are ASCII, so the supplied ASCII literal rule covers them completely. |
| `For(Name("ch"), Name("s"), BODY)` | `syntax.k:42`; strictness on iterable | `controls.k:69-74`; `str.k:7-10`; tuple target rules used by `#bindTgt` | Evaluates `s` once; each `iCons` yields a one-character `str`, binds `ch`, executes the exact body, then recurs on the tail. Empty input terminates. |
| `AugAssign(Name("count"), "+", RHS)` | `syntax.k:41` | RHS strictness; `controls.k:20-31`; `int.k:7-10` | With `count:Int` and RHS `Bool`, updates `count` to `count + 1` for true and unchanged for false. Heap-ref priority case is inapplicable. |
| `BoolOp("and", even, membership)` | `syntax.k:15`; `bool.k:10-18` | Boolean short-circuit context/rules | If `even` is false, returns false without membership; if true, evaluates and returns the membership Boolean, matching Python value-returning `and`. |
| `Compare(ch, CmpOp("in", Str("AEIOU")))` | `syntax.k:26`; contexts in `operators.k:13-17` | `str.k:28-41` | Both operands are semantic strings. `applyCmp("in",str(P),str(X))` uses truthful structural prefix/substring recursion; here `P` is exactly one code. |
| `UnaryOp("not", even)` | `syntax.k:14` with strictness | `operators.k:9`; `bool.k:6`; `core.k:199-205` | `even` remains Boolean, so `truthy(even)=even` and the value toggles each iteration. |
| `Name` lookup | `syntax.k:12`; `core.k:130` | `core.k:131-154` | Finds the exact current-frame bindings for locals and the module binding for `count_upper`; no alternative binding is admitted by the exact maps in the entry claim. |
| `Return(Name("count"))` | `syntax.k:47` with strictness | `functions.k:78-90` | Evaluates the actual local count, records it in `<ret>`, drops the remaining function computation, pops precisely the saved call frame, and resumes the saved continuation with that value. |
| `countUpperFrom` | `verification.k:8` | `verification.k:10-16` | Proof-local definitional summary only; it does not rewrite any program constructor. Base is zero; the constructor rule adds exactly the current one-character contribution and recurses on the strict tail with toggled parity. Guards are constructor-disjoint and recursion structurally descends. |

No rule in `verification.k` matches `<k>`, `Module`, `FuncDef`, `Call`,
`For`, `#loop`, or any other operational constructor. Consequently there is
no proof-local operational bridge, priority override, state-changing rewrite,
or opaque program-derived oracle.
