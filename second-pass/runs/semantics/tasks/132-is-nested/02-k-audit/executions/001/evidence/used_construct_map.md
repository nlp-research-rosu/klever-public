# Used-program construct and state-footprint map

This map is based on the byte-identical trusted translation recorded in
`stage2_fidelity.log`.  Line references below are relative to the clean scratch
copy under `/tmp/audit-work/132-is-nested/source`.

| Submitted construct | Declaration | Execution path in supplied semantics | Observable effect |
|---|---|---|---|
| `Module` | `reference-semantics/semantics/syntax.k:61` | `core.k:124-127` loads and sequences statements | Initializes module definitions in scope 0 |
| `FuncDef("is_nested", ...)` / `Params` | `syntax.k:53,57` | `functions.k:14-16` creates `closureVal`; the claims instead install the exact factored closure `isNestedClosure` | Adds `is_nested` to module scope |
| `Assign(Name(...), ...)` | `syntax.k:41` | strict RHS, then `controls.k:9-18` | Writes `state` and `char` in callee scope 1 |
| `Name` | `syntax.k:12` | `core.k:130-154` follows scope parents | Reads locals first, then module scope, then builtins |
| `Int` | `syntax.k:9` | `core.k:194` | Produces mathematical integers |
| `Str` | `syntax.k:13` | `str.k:13-17` | Produces an ASCII code sequence |
| `For` | `syntax.k:45` | strict iterable evaluation, then `controls.k:65-74` | Iterates in order, binds `char`, runs body, retains remaining iterable |
| Loop-target `Name("char")` | `tuple.k:31` | `tuple.k:32-41` | Updates `char` in scope 1 on each yield |
| `If` | `syntax.k:49` | strict condition plus `controls.k:51-54` | Executes exactly one branch |
| `Compare` / `CmpOp` | `syntax.k:30,32` | left-to-right contexts and `operators.k:14-17`; integer cases in `int.k:22-27` | Produces the boolean guards used by the automaton |
| `Call(Name("ord"), ...)` | `syntax.k:28` | `call.k:18-32`; lookup in `core.k:130-181`; arguments in `core.k:183-191`; `builtins.k:142-145` | For the intended scope, maps the one-character string to 91 or 93 |
| `AugAssign` | `syntax.k:44` | strict RHS plus `controls.k:20-31`; integer addition in `int.k:9` | Increments `state` in scope 1 |
| `Return` | `syntax.k:50` | strict expression and `functions.k:77-90` | Sets return value, restores caller environment, removes callee scope and stack frame |

## Configuration and evaluation order

The supplied configuration (`core.k:49-60`) contains `k`, `env`, `scopes`,
`scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, and `exit-code`.  The
ordinary call rule (`call.k:69-74`) allocates scope 1, changes `env` from 0 to 1,
and pushes the complete continuation.  Parameter binding and statement
sequencing are left-to-right.  The program allocates no heap objects, raises no
modeled exception on the claimed domain, and does not change `heap`, `heapLoc`,
or `exit-code`.  Return/pop restores `env`, removes scope 1, rewinds `scopeLoc`,
empties `stack`, and resets `ret`.

The proof-side `bCodes` iterator rules yield exactly one-character strings with
code 91 for `bOpen` and code 93 for `bClose`; they modify only the `k` cell and
frame every other cell.  They form a conservative lazy input encoding for the
only operation performed on the input (iteration), but no bridge-free universal
K connection theorem to native `iCons` strings is supplied.  The structural
equations are truthful; this is an evidence/intent bridge, not the identified
false rule.

## Candidate proof-extension classification

| Extension | Class | Domain and state footprint | Review |
|---|---|---|---|
| `scanBody`, `isNestedBody`, `isNestedClosure` | Definitional summaries | Exact submitted function AST and module-scope closure | Accepted after byte-level translation check and source comparison |
| `BSeq`, `bCodes`, three `#iterNext` rules | Proof input encoding / operational extension | Finite `bOpen`/`bClose` trees; rewrites only `k` | Equations match 91/93 iteration. No false witness found; universal native-string connection is informal/structural |
| `openStep`, `closeStep`, `scanState`, `nested` | Definitional mathematical summary | All `Int` inputs for step functions and all finite `BSeq` values; no cells | Accepted: guarded arithmetic is exact, recursion descends structurally, equations cover constructors without harmful overlap |
| `proved-scan-loop` | Operational bridge | Entire loop, return, call-pop, and listed cells; `_REST:Map` accepts arbitrary remaining scopes | Rejected: the proving claim fixed scopes 0 and -1, but the installed rule accepts altered name bindings. `bridge-witness.k` shows a valid bracket input where fixed semantics returns `false` and this rule proves `true` |

The complete 953-item inventory, including all function/total declarations,
opaque symbols, priority rules, ordinary rules, contexts, and the absence of
local simplification rules, is in `rule_inventory.md`.
