# Independent adversarial audit: 129-minPath

## Executive decision

The candidate contains a sound, non-vacuous K reachability proof of four
specific executions of the real submitted `solution.mpy`. It does **not**
contain a universal partial-correctness proof for every valid square
permutation grid and every positive `k`. The proof is therefore legitimate
within its explicitly ground scope, but it has a material intent-adequacy
limitation and cannot receive `PASS`.

This is `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`, because fresh reconstruction
closed the only positive claim, the claim is result-constraining, the exact
submitted program is pinned by parsed KAST identity, no candidate rule bypasses
execution, and a fresh false-result mutation is rejected for the expected
reason. The limitation is theorem scope, not a false conclusion or an unsound
proof rule.

The complete reviewer evidence index is
[`evidence/README.md`](/audit-output/evidence/README.md).

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory is present, so there is no
mode/mount contradiction and no infrastructure breach.

The reviewer checked the candidate tree without following symlinks:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`, and
  `verification.k` are regular files.
- One regular structured trace is present under `codex-trace/`.
- No symlink occurs in the candidate source tree after pruning the
  candidate-built compiled directories and `__pycache__`.
- `cmp` reports identity for candidate versus trusted `prompt.py` and
  `py2mpy.py`.
- `diff --no-dereference -r` reports exact recursive identity between the
  candidate and trusted `reference-semantics/` trees. There are no missing,
  additional, changed, mistyped, or symlinked semantics entries.
- Candidate-built `runtime-kompiled/`, `verification-kompiled/`, bytecode, and
  caches were not copied or used.

The exact checks, hashes, and exit statuses are in
[`stage1-integrity.log`](/audit-output/evidence/stage1-integrity.log). The
candidate metadata, final report, 1.48 MB generation log, and 817 KB structured
trace were treated only as untrusted claims. Their bounded extraction records
that the generator itself ultimately claimed `#Top`, 869 differential cases,
and `SOUND-BUT-LIMITED`; none of those claims was used as proof evidence. See
[`stage1-untrusted-claims.log`](/audit-output/evidence/stage1-untrusted-claims.log).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and canonical behavior

The trusted prompt requires, for a square `N x N` grid with `N >= 2` containing
each integer `1..N²` exactly once and for positive `k`, the lexicographically
least sequence of values along any legal edge-adjacent walk visiting exactly
`k` cells. Cells may be revisited and the result is guaranteed unique.

The trusted canonical implementation finds the unique cell containing `1`,
finds its least-valued orthogonal neighbor, then returns the length-`k`
alternation `1, neighbor, 1, neighbor, ...`. This follows from the
lexicographic objective: the first value must be the globally least value `1`;
the second must be the least legal neighbor; from that neighbor the globally
least value `1` is again legal, and the argument repeats.

`solution.py` implements the same algorithm using `while` loops. It scans the
whole grid for `1`, conditionally considers the four in-bounds neighbors, and
constructs the alternating list.

### Trusted translation

From the scratch copy, the exact command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

used the trusted translator. It exited 0. `cmp -s` between the regenerated and
submitted `solution.mpy` exited 0; both have SHA-256
`35f9a35abbdbe5b2bea4bb8dd7579c48ccef9931f9db72dbd8b1c63e2d6700a3`.
See [`stage2-fidelity.log`](/audit-output/evidence/stage2-fidelity.log).

### Independent differential test

The reviewer-authored
[`stage2_differential.py`](/audit-output/evidence/stage2_differential.py)
imports `/reference/canonical.py` and the scratch copy of `solution.py`.
It also uses an independent oracle that enumerates every legal length-`k`
walk and takes the lexicographic minimum. Its exact inputs are preserved in
[`stage2-inputs.json`](/audit-output/evidence/stage2-inputs.json).

The valid-input scope was 897 cases:

- both documented examples;
- all 24 permutations of a `2 x 2` grid for `k = 1..7`;
- a `3 x 3` grid with `1` in each of all nine positions for `k = 1..8`,
  exercising the true and false boundaries of all four neighbor guards;
- 50 deterministic random `3 x 3` grids for `k = 1..8`;
- 30 deterministic random `4 x 4` grids for `k = 1..6`; and
- 15 deterministic random `5 x 5` grids for `k = 1..5`.

There were zero generated-versus-canonical mismatches and zero oracle
mismatches. The input serialization SHA-256 is
`00f3a1ac0371754a3a3f30dc4e03862fb34f4e91670c1132757dda941f7e3cd1`.
Empty-grid, zero-`k`, negative-`k`, and `N=1` characterization cases were also
run. The implementations differ at `N=1`: canonical raises `ValueError` while
the candidate returns `[1]`. That case is outside the stated `N >= 2` domain
and does not undermine intended-domain fidelity.

Stage 2 result: **PASS**, with the ordinary limitation that finite testing is
not a universal proof.

## 3. Clean proof reconstruction

All reconstruction occurred under `/tmp/audit-work/reconstruction`. The
reviewer copied the candidate source proof files, the trusted translator and
canonical source, and the trusted supplied semantics. No candidate-compiled
definition was reused. The installed tools are K `v7.1.293`; command paths and
versions are in [`toolchain.log`](/audit-output/evidence/toolchain.log).

Claim discovery found exactly one positive claim:
`SPEC.target-examples`. There are no claims in `verification.k`; see
[`stage3-claim-inventory.log`](/audit-output/evidence/stage3-claim-inventory.log).

The fresh commands and outcomes were:

| Purpose | Exact command | Result |
|---|---|---|
| LLVM definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0 |
| Concrete run | `krun stage3_concrete.mpy --definition audit-runtime-kompiled` | exit 0; `.K`, `NoExc`, exit code `0` |
| Haskell definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX --output-definition audit-verification-kompiled` | exit 0 |
| Positive proof | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.target-examples` | exit 0; `#Top` |

The concrete harness was independently translated with the trusted translator
and exercised six valid cases covering corners, edges, an interior `1`, and
`k=1`. Full bounded outputs are
[`stage3-runtime-build.log`](/audit-output/evidence/stage3-runtime-build.log),
[`stage3-concrete-run.log`](/audit-output/evidence/stage3-concrete-run.log),
[`stage3-proof-build.log`](/audit-output/evidence/stage3-proof-build.log), and
[`stage3-positive-target-examples.log`](/audit-output/evidence/stage3-positive-target-examples.log).

The LLVM compiler reported supplied-semantics non-exhaustiveness warnings
discussed in Stage 5. They are not build or proof failures.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

`SPEC.target-examples` has no symbolic input and no `requires` clause. Its
precondition is one exact, realizable initial MPY configuration:

- `<k>` loads a module containing `MinPathDefinition` followed by four ground
  assertion statements;
- environment `0`;
- the standard empty module scope with the supplied builtins parent;
- empty heap and stack, allocation counters at their initial values;
- `noRet`, `NoExc`, and exit code `0`.

Its postcondition requires all computation to be consumed (`<k> .K </k>`),
environment `0`, empty stack, `noRet`, `NoExc`, and exit code `0`. The final
scopes, heap, and heap counter are existential. This existential framing does
not free the function result: every returned list is immediately compared with
a concrete expected list by `Assert`. A false assertion sets
`AssertionError` and exit code `1`, which cannot satisfy the destination.

The four formal inputs and constrained results are:

| Grid | `k` | Required result |
|---|---:|---|
| `[[1,2,3],[4,5,6],[7,8,9]]` | 3 | `[1,2,1]` |
| `[[5,9,3],[4,1,6],[7,8,2]]` | 1 | `[1]` |
| `[[5,9,3],[4,1,6],[7,8,2]]` | 6 | `[1,4,1,4,1,4]` |
| `[[4,3],[2,1]]` | 5 | `[1,2,1,2,1]` |

Both Python implementations produce exactly those values. The complete
witness record is
[`stage4-adequacy.log`](/audit-output/evidence/stage4-adequacy.log).

### Program identity and control flow

The `<k>` cell does not read `solution.mpy` directly; it uses a syntax macro
whose right-hand side duplicates the translated `FuncDef`. The reviewer
therefore extracted that RHS independently, parsed both it and submitted
`solution.mpy` with `kast` against the fresh definition, and compared their
KASTs. They are equal. Changing the even-step appended value from `1` to `9`
produces a different KAST, so the identity check is body-sensitive.

The program body executes under the supplied semantics: function definition,
name lookup, argument evaluation and binding, both search loops, four guarded
neighbor reads, arithmetic, `len`, `min`, list allocation, `append`, the result
loop, return-frame handling, list comparison, and assertions. There is no
helper claim or summary replacing any loop or call.

### Adequacy limitation

No K variable represents an arbitrary grid or arbitrary positive `k`. The
claim proves only the four rows in the table. It therefore does not prove the
prompt contract over the intended domain, does not establish a loop invariant,
and does not establish universal termination or result correctness. The
mathematical alternating-path argument and the differential evidence support
the implementation-to-intent bridge, but neither is part of the K theorem.

Stage 4 result: **sound and pinned, but materially under-scoped**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory covers all 24 supplied K files plus
`verification.k` and `spec.k`, records source hashes, and contains every local
entry with its complete multi-line block and attributes. It enumerates:

- 696 rules;
- 228 syntax declarations;
- five contexts;
- one configuration; and
- one positive claim.

Each of the 931 records is classified in
[`stage5-rule-inventory.tsv`](/audit-output/evidence/stage5-rule-inventory.tsv).
The separate attribute audit enumerates every opaque/symbol declaration,
priority rule, and `total` declaration, and confirms there are no
`simplification` rules and no `functional` declarations:
[`stage5-attribute-audit.log`](/audit-output/evidence/stage5-attribute-audit.log).

For the supplied tree, the inventory decision is “fixed supplied rule or
declaration, unchanged by the candidate; no false witness found,” with opaque
and concrete-only boundaries called out separately. This is not a claim that
all 696 rules are a complete semantics of CPython. It records that they are the
selected trusted MPY semantics, that the candidate did not alter them, and
that no inventoried rule enables a false conclusion for this theorem.

### Candidate-local extensions

There are exactly two candidate-local K entries:

1. `syntax Stmt ::= "MinPathDefinition" [macro]`.
2. Its macro expansion rule to the full `FuncDef`.

The pair is a compile-time program abbreviation, not an operational bridge,
equational oracle, trusted primitive, loop summary, or result rule. Parsed-KAST
identity establishes its complete justification scope. It reads/writes no
runtime cell, has no guard or overlap, and is not broader than the actual
program term. There are no candidate functions, `total`/`functional`
declarations, opaque symbols, priorities, ordinary semantic rules,
simplifications, or auxiliary claims.

### Used-construct coverage

Every syntax construct in `solution.mpy` is declared in
`semantics/syntax.k`: `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Call`,
`Int`, `While`, `Compare`, `CmpOp`, `Subscript`, `If`, `BinOp`, `ListExpr`,
`Expr`, `Attribute`, and `Return`. The spec additionally uses `Assert`.

The execution path is covered as follows:

| Behavior | Supplied source and rule family | Audit conclusion |
|---|---|---|
| Configuration, module load, sequencing, literals, name lookup, argument-list evaluation, allocation | `core.k` | Initial cells match the claim; lookup follows the scope chain; arguments and list elements evaluate left-to-right; allocation updates heap and `heapLoc`. |
| Function creation, calls, binding, returns | `functions.k`, `call.k` | The real closure body is stored, arguments are bound in a fresh frame, the caller continuation is preserved on the stack, and `Return` reaches `#pop`, which restores the caller. |
| Assignment, expression statements, conditionals, loops | `controls.k` | Strict RHS/condition evaluation and repeated `#while` condition evaluation match the program; loop control is not bypassed. |
| Arithmetic and comparison | `operators.k`, `int.k` | Integer `+`, `-`, `*`, `%`, `<`, `>`, and `==` are the used cases. `pyMod` is used only with divisor `2`; no division-by-zero case is reachable. |
| List literals, append, list equality | `list.k` | Literals allocate fresh heap objects; `append` mutates the referenced list; comparison dereferences operands and compares the integer sequences structurally. |
| Nested indexing | `subscript.k` | Object then index evaluation, heap dereference, index normalization, and `valSeqAt` cover all ground in-bounds reads. Neighbor guards prevent off-grid indices. |
| `len` and two-argument `min` | `builtins.k`, `call.k` | Builtin binding is resolved through the real builtins scope; list `len` uses `vsLen`; variadic integer `min` folds with `minInt`. |
| Result assertions | `assert.k` | True assertions consume normally; false assertions set `AssertionError` and exit `1`. The fresh mutation confirms the failure rule is reachable. |

### Configuration, overlaps, priorities, totality, and opacity

- The only cells affected by the used program are `<k>`, `<env>`, `<scopes>`,
  `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
  `<exit-code>`. The claim includes all of them. Heap and scope post-state are
  intentionally existential, but result comparisons occur before that final
  framing.
- Priority rules on the used path select heap-reference dereference,
  list-append mutation, cell-aware binding where applicable, and assertion
  dereference ahead of generic dispatch. Their guards are disjoint from or
  more specific than the fallback rules. No candidate priority exists.
- Recursive helpers used here (`appendVal`, `vals2valSeq`, `vsLen`,
  `valSeqConcat`, `minVals`, and in-bounds `valSeqAt`) descend structurally or
  on a decreasing positive index. Guard overlaps do not yield different
  right-hand sides on the used domain.
- The LLVM compiler identifies six narrow non-exhaustiveness gaps in supplied
  `total` functions: `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
  `valSeqAt`. The first five are unreachable because this program has no map,
  float, or string-join operation. `valSeqAt` is intentionally underspecified
  for empty/out-of-bounds access; every index in the four ground executions is
  in bounds. This is an evidence gap in the broad supplied language model, not
  an unsoundness witness for the intended inputs or this theorem.
- The 25 supplied opaque/symbol declarations implement float operations,
  sorting/key sorting, and MD5. None occurs in `solution.mpy`, the claim, or
  its proof path. `MPY-CONCRETE` is present only in the LLVM execution module;
  the Haskell proof imports `MPY`, not its concrete-only extensions.
- There is no rule that encodes the min-path answer, replaces the program with
  an unconstrained oracle, fabricates a result, or discards a successful
  continuation. No unsoundness is alleged, so there is no false-conclusion
  witness to report.

Stage 5 result: **PASS for real-program soundness**. The fixed-semantics
coverage warnings are documented trust limitations, not candidate proof
extensions and not theorem-critical here.

## 6. Fresh non-vacuity test

The candidate `spec-vacuity.k` was inspected only as untrusted evidence and was
not reused. The reviewer created the preserved
[`audit-spec-vacuity.k`](/audit-output/evidence/audit-spec-vacuity.k), changing
the last value for the valid input `[[4,3],[2,1]], k=5` from the true `1` to
false `2`.

Both trusted canonical and generated Python return `[1,2,1,2,1]`, not the
mutated `[1,2,1,2,2]`; see
[`stage6-false-witness.log`](/audit-output/evidence/stage6-false-witness.log).

The mutation first built successfully:

```text
kprove audit-spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --claims AUDIT-SPEC-VACUITY.false-ground-result --dry-run
```

Exit status was 0. The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual contains `.K`, the actual heap list
`[1,2,1,2,1]`, the false expected heap list `[1,2,1,2,2]`,
`AssertionError`, and exit code `1`. This is the expected unmet obligation,
not a parser error, timeout, unrelated crash, or unreachable mutation.
See [`stage6-dry-run.log`](/audit-output/evidence/stage6-dry-run.log) and
[`stage6-false-proof.log`](/audit-output/evidence/stage6-false-proof.log).

Stage 6 result: **PASS**. The proof discriminates the asserted ground result.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on the supplied MPY semantics and K toolchain, the successful
reachability proof establishes that starting from the standard empty MPY
configuration, loading the exact submitted `minPath` function and executing
the four listed calls reaches normal completion and all four concrete list
equalities hold. The final stack is empty, return state is `noRet`, exception
state is `NoExc`, and exit code is `0`.

It does **not** establish:

- correctness for an arbitrary valid grid;
- correctness for arbitrary positive `k`;
- a symbolic characterization of the returned list;
- a loop invariant or universal termination argument; or
- behavior on invalid grids, duplicate/missing values, `N < 2`, or
  non-positive `k`.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied `reference-semantics/` | Concrete run and K proof | Acceptable mandated semantics boundary; recursively identical to the trusted mount. It models the MPY subset, not all of CPython. |
| Trusted `py2mpy.py` | Link from Python source to `solution.mpy` | Acceptable mounted translator boundary; fresh translation is byte-identical. |
| Manual `MinPathDefinition` macro | Entry claim's program term | Not merely assumed: independently parsed KAST equals submitted `solution.mpy`; a body mutation is detected. |
| K parser/compiler, builtin K theories, LLVM/Haskell backends, and prover | All machine-checked evidence | Standard toolchain trust boundary; K version and exact commands are recorded. |
| Supplied opaque float/sort/MD5 symbols | None for this theorem | Acceptable but unused. They have no control, state, or result influence here. |
| Supplied `valSeqAt` totality outside in-bounds sequences | Broad language behavior | Concerning in the abstract semantics, but no bad case is reached by the four claims and no false theorem witness was found. |
| CPython, trusted canonical implementation, and exhaustive-path oracle | Differential and intent evidence only | Finite empirical support, not a K axiom and not a replacement for the reachability proof. |
| Alternating-path mathematical argument | Bridge from implementation behavior to prompt intent | Informal universal argument only; it is not encoded or proved in K. |

### Final rationale

Gate A (real-program soundness and non-vacuity) passes. Gate B (full intent
adequacy) fails because the formal domain is four ground cases rather than the
prompt's valid-input domain. Gate C (auditability) passes: source identities,
commands, inputs, statuses, proof output, mutation residual, and the complete
rule inventory are preserved. The appropriate completed-audit classification
is therefore a legitimate but materially limited proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
