# Used-path static review

This is the reviewer’s manual mapping from the macro-expanded submitted AST to
the selected supplied semantics. The exhaustive source inventory is
`static-rule-inventory.md`.

| Program construct / phase | Declaration and rules | Static decision |
|---|---|---|
| `Module`, statement list, `FuncDef` | `syntax.k:53,56,61`; `core.k:49,124-127`; `functions.k:14-16` | Loads and executes the exact function definition in source order, binding the closure in module scope 0. |
| `Call(Name("hex_key"), str(CS))` | `call.k:19-21,69-74`; `core.k:130-154,185-191`; `functions.k:63-66` | Looks up the actual closure, evaluates the one argument left-to-right, allocates a local frame, and binds `num` to the supplied string. No call interception or summary rule exists. |
| `Assign(count, 0)` and `Assign(digit, "")` | `syntax.k:41`; strictness-generated RHS evaluation; `core.k:194`; `str.k:13-17`; `controls.k:9-11` | Produces integer 0 and the empty string, then updates only the current local scope. |
| `For(digit, num, body)` | `syntax.k:45`; `controls.k:65,69,71-74,85`; `iter.k:8`; `str.k:8-10`; `tuple.k:31-34` | Evaluates `num` once, iterates its code sequence in order, assigns each one-character string to `digit`, executes the body, and repeats on the suffix. Empty input takes the done rule. |
| `If(digit in "2357BD")` | `syntax.k:13,30,32,49`; `operators.k:15-17`; `str.k:14-17,29,32-41`; `core.k:199-203`; `controls.k:51-54` | Both operands evaluate, string `in` becomes singleton substring membership, and the Boolean chooses exactly one branch. Because the left string is one code, this is character membership in the six-code constant. |
| `count += 1` | `syntax.k:9,44`; `core.k:194,209`; `controls.k:20-23`; `int.k:9` | Reads the already-bound integer `count`, applies integer addition, and writes the result in the local scope. The ref/cell priority alternatives do not match this plain frame. |
| `Return(count)` | `syntax.k:50`; `core.k:130-134`; `functions.k:78-90` | Evaluates the local name, records that exact value, discards the remaining call continuation, restores module scope/environment, deletes the local frame, and returns the value to the caller. |

## Candidate-local extension decisions

| Extension | Class and complete-domain decision |
|---|---|
| `hexKeyLoopBody` macro (`verification.k:8-12`) | Syntax-only definitional expansion. KAST comparison proves it is the exact translated loop body. It replaces no operational execution. |
| `hexKeyBody` macro (`verification.k:14-19`) | Syntax-only definitional expansion. KAST comparison proves it is the exact translated function body. It replaces no operational execution. |
| `isPrimeHexCode(C)` (`verification.k:22-26`) | Total definitional summary with one unguarded equation. For every integer `C`, it tests whether singleton `[C]` occurs in `[50,51,53,55,66,68]`; this is exactly membership in the ASCII codes for `2357BD`. |
| `primeHexBit(C)` (`verification.k:28-30`) | Total definitional summary with one unguarded equation, returning 1 iff the preceding Boolean is true and 0 otherwise. |
| `hexCount` (`verification.k:32-35`) | Total structural recursion. Empty and `iCons` cases are disjoint and exhaustive; recursion strictly descends to `REST`. |
| `finalDigit` (`verification.k:39-42`) | Total structural recursion. Empty and `iCons` cases are disjoint and exhaustive; recursion strictly descends and records the last singleton string. It affects only the loop lemma’s local `digit`, not the entry result. |

There are no candidate-local priority, `owise`, simplification, concrete,
trusted, operational-bridge, or opaque-symbol rules. The two reachability
claims are inventoried separately. All candidate-local equations are covered,
non-overlapping, descending where recursive, and mathematically valid on their
complete sorts.
