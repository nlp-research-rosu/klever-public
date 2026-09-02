# Executed-construct dependency map

The constructor term is the byte-identical expansion recorded in
`04-program-term-identity.log`. Line references below are to the scratch copy
of the trusted supplied semantics.

| Program constructor/operation | Declaration | Execution rules used |
|---|---|---|
| `Module`, `Stmts` | `reference-semantics/semantics/syntax.k:56-61` | `core.k:124-127` loads the module and sequences statements. |
| `FuncDef`, `Params`, `ParamNames` | `syntax.k:52,57,60` | `functions.k:14-16` binds the closure in scope 0. The entry claim supplies that same binding directly. |
| `Call(Name("file_name_check"), ...)` | `syntax.k:28,37` | `core.k:131-153` performs scope-chain lookup; `call.k:20-21` evaluates callee then arguments left-to-right; `call.k:69-76` allocates the call frame and executes its body. |
| Parameter binding and return | `functions.k:7-10` | `functions.k:63-75` binds `file_name`; `functions.k:78-91` performs abrupt return, restores the caller, removes the callee scope, and restores `ret`, stack, and `scopeLoc`. |
| `Name`, `Int`, `Str` | `syntax.k:9-13` | `core.k:131-153,194`; `str.k:13-17`. Every literal in the program/proof is ASCII, inside `strToCodes`'s explicit domain. |
| `Attribute(...,"count")`, method calls | `syntax.k:28-29` | `call.k:16,20-24` constructs and dispatches a bound method; `methods.k:34-44` implements non-overlapping `str.count`. All program patterns are nonempty one-character strings. |
| `If` and truthiness | `syntax.k:47` | strictness evaluates the guard; `controls.k:51-54` chooses exactly one branch; `core.k:199-205` supplies truthiness. Guards here are `Bool`. |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:15-17`; integer cases in `int.k:21-27`; string equality and membership in `str.k:25-40`. |
| `UnaryOp("not",...)` | `syntax.k:14` | `operators.k:10`; `bool.k:8`. |
| `UnaryOp("-",Int(4))` | `syntax.k:14` | `operators.k:10`; `int.k:7`. |
| `BoolOp("or",...)` | `syntax.k:15` | `bool.k:16-25` evaluates the head and short-circuits left-to-right. |
| `BinOp("+",...)` | `syntax.k:15` with `seqstrict(2,3)` | `operators.k:12`; `int.k:9` for each left-associated count sum. |
| `Subscript(s,0)` | `syntax.k:38` | `subscript.k:27-41`; `normIdx` and `intSeqAt` implement string indexing. The only path reaching this operation has a nonempty sequence because its dot count is one. |
| `Subscript(s,Slice(-4,None,None))` | `syntax.k:38-39` | `subscript.k:47-69,72-121`; bound evaluation, negative-index adjustment, and `buildIS` implement Python's step-1 suffix slice for every sequence length. |
| `Return` | `syntax.k:49` | strict expression evaluation plus `functions.k:78-91`; it discards the remaining function-body continuation and pops exactly the active call frame. |

## Proof-local declarations and rules

| Extension | Classification and review |
|---|---|
| `fileNameCheckBody` macro (`verification.k:8-99`) | Parse-time syntactic alias. It has no runtime symbol after macro expansion. Its expanded `Module` term is byte-identical to regenerated `solution.mpy`; changing its final return changes the actually executed claim body and makes `valid-name-txt` stick. |
| `decimalDigitCount` (`verification.k:102-113`) | Exhaustive single-equation definitional summary used only in claim preconditions. Its right side is exactly the ten left-associated singleton `cntSub` terms executed by the body. |
| `fileExtensionIs` (`verification.k:115-120`) | Exhaustive single-equation definitional summary used only in preconditions. It is the fixed `doSlice(...,-4,None,None)` followed by fixed string equality. |
| `allowedFileExtension` (`verification.k:122-126`) | Exhaustive single-equation Boolean disjunction of the three allowed four-code suffixes, used only in `bad-extension`'s precondition. |
| `N >Int 3 => false requires N <=Int 3` (`verification.k:128-130`) | Globally true guarded integer simplification. It has one equation, no overlap, and a bridge-free MPY-only reachability proof (`03-kprove-lemma.log`). |

There are no proof-local operational bridges, opaque result-bearing symbols,
priority rules, circularities, or helper claims.
