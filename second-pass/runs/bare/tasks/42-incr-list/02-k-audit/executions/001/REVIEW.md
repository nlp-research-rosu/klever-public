# Independent adversarial audit: 42-incr-list

This is a completed audit of the candidate in `GENERATED_SEMANTICS` mode. The
positive K claims can be reconstructed, and the submitted Python implementation
matches the trusted canonical implementation over extensive integer-list tests.
The proof is nevertheless not legitimate: a program-derived, result-bearing
`#incPrefix` abstraction is used both to replace loop computation and as the
postcondition, without a sound connection theorem. A ground input satisfying
the formal entry precondition demonstrates that this bridge can prove a normal
return even when fresh concrete K execution stops and both Python
implementations raise.

## 1. Input and provenance integrity

The trusted-mount boundary is consistent with the rendered mode:
`/reference/reference-semantics` is absent. The reference tree contains exactly
the three expected trusted files: `canonical.py`, `prompt.py`, and `py2mpy.py`.
Therefore there is no infrastructure breach and candidate verdict markers are
appropriate. See
[00-boundary-and-inventory.log](evidence/00-boundary-and-inventory.log).

All primary candidate artifacts are regular files, not symlinks:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, and `spec.k`. No required source artifact is missing or
mistyped. Candidate `prompt.py` and `py2mpy.py` are byte-identical to their
trusted versions:

- prompt SHA-256:
  `8b6d8ac13f22a485fb80312ee1b077ba1cc2653fbff4c36fb7e3d36ca1b8d609`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The type checks, comparisons, and hashes are in
[01-artifact-integrity.log](evidence/01-artifact-integrity.log).

The candidate also contains non-source extras:
`semantic-kompiled/`, `__pycache__/`, `kore-exec.tar.gz`, and generation logs.
They are not integrity failures in generated-semantics mode, but none was used
for reconstruction. The untrusted run metadata says this was the bare,
no-supplied-semantics condition and claims a successful generation run. The
untrusted final report claims one proof invocation covering both claims.
The structured trace is a regular 482-record JSONL file and contains the same
development claims. These were inspected only as claims:
[02-untrusted-generation-claims.log](evidence/02-untrusted-generation-claims.log)
and
[36-generation-trace-summary.log](evidence/36-generation-trace-summary.log).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: `incr_list(l)` returns a new list whose elements are
the corresponding input elements plus one. The two documented examples are
`[1, 2, 3] -> [2, 3, 4]` and
`[5, 3, 5, 2, 3, 3, 9, 0, 123] ->
[6, 4, 6, 3, 4, 4, 10, 1, 124]`. The canonical implementation is the list
comprehension `[(e + 1) for e in l]`; see
[prompt.py](/reference/prompt.py:3) and
[canonical.py](/reference/canonical.py:7).

The submitted implementation initializes a fresh list, loops over `l`, appends
`value + 1` by list concatenation, and returns the accumulator; see
[solution.py](/candidate/solution.py:1). On the intended integer-list domain it
is extensionally equivalent to the canonical implementation and does not
mutate its input.

A fresh trusted translation of `solution.py` is byte-identical to submitted
`solution.mpy`. Both hashes are
`973649ca065888e3e0d4180da89fc16cdb901ca5dee021a543b095f105ed2c50`;
see
[04-scratch-copy-and-translation.log](evidence/04-scratch-copy-and-translation.log).

The independent differential test imports the trusted canonical module and the
scratch-copied generated module by distinct paths. It covers both examples,
empty, one-iteration, two-iteration, negative/zero/positive boundaries, huge
Python integers, repeated values, all 3,906 lists of lengths 0 through 5 over
`[-2, 2]`, and 256 deterministic generated lists of lengths 0 through 20.
All 4,171 cases match and neither implementation mutates its input:

- test:
  [differential_test.py](evidence/differential_test.py)
- complete inputs:
  [differential-inputs.json](evidence/differential-inputs.json)
- complete per-case results:
  [differential-results.json](evidence/differential-results.json)
- command and summary:
  [05-differential.log](evidence/05-differential.log)

This is finite evidence about the implementation bridge, not a universal K
proof.

Stage 2 result: **PASS** on the intended integer-list domain.

## 3. Clean proof reconstruction

All source needed for execution was copied into
`/tmp/audit-work/reconstruction`; no candidate-built definition or cache was
copied. The audit used K `v7.1.293` and Python `3.10.12`; see
[06-toolchain.log](evidence/06-toolchain.log).

### Fresh builds and concrete execution

A fresh LLVM definition built from `semantic.k`. The compiler warned that
three declarations marked `[total]` are non-exhaustive:

- `#incPrefix(List, Int)`
- `#eval(Exp, Map, IterVal)`
- `#add(PyVal, PyVal)`

The warning-bearing builds are recorded in
[07-kompile-concrete.log](evidence/07-kompile-concrete.log) and
[14-kompile-concrete-search.log](evidence/14-kompile-concrete-search.log).
A separate fresh Haskell proof definition built from `verification.k` with
exit status 0:
[08-kompile-proof.log](evidence/08-kompile-proof.log).

After rebuilding LLVM with `--enable-search`, fresh concrete K executions
matched independent Python results for:

- `[1, 2, 3] -> [2, 3, 4]`:
  [15-krun-normal.log](evidence/15-krun-normal.log)
- `[] -> []`:
  [16-krun-empty.log](evidence/16-krun-empty.log)
- `[-1] -> [0]`:
  [17-krun-singleton-negative.log](evidence/17-krun-singleton-negative.log)
- `[-3, 0, 7] -> [-2, 1, 8]`:
  [19-krun-mixed-rerun.log](evidence/19-krun-mixed-rerun.log)

The corresponding Python oracle outputs are in
[09-python-concrete-oracle.log](evidence/09-python-concrete-oracle.log).
The preliminary pattern runs in logs 10–13 failed only because the first LLVM
build omitted `--enable-search`. One parallel mixed-input run in log 18
encountered a transient Java-detection error and passed when rerun sequentially
in log 19. These are reviewer-invocation issues, not candidate failures.

### Positive target claims

Each positive obligation was run against the fresh Haskell definition:

- `SPEC.for-invariant` alone printed `#Top` and exited 0:
  [20-kprove-for-invariant.log](evidence/20-kprove-for-invariant.log).
- The entry claim together with its declared invariant dependency printed
  `#Top` and exited 0:
  [22-kprove-entry-with-dependency.log](evidence/22-kprove-entry-with-dependency.log).
- The complete `SPEC` module printed `#Top` and exited 0:
  [23-kprove-all.log](evidence/23-kprove-all.log).

Selecting only `SPEC.incr-list-correct` filters out its circularity and fails at
the loop result; that diagnostic is
[21-kprove-entry.log](evidence/21-kprove-entry.log). It is not counted as the
positive entry run because the claim explicitly depends on `for-invariant`.

Thus the candidate's positive `#Top` claim is reproducible. This establishes
closure only under the candidate's theory; it does not validate that theory.

Stage 3 result: **PASS for reconstruction**, subject to the soundness failures
in Stages 4, 5, and 7.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim at [spec.k](/candidate/spec.k:8) says:

- Start at the exact submitted `for` loop at index `I`, followed by the exact
  submitted return.
- Require `0 <= I <= size(L)`.
- Bind `l` to `pyList(L)` and the current accumulator to
  `#incPrefix(L, I)`.
- Finish with an empty `<k>` cell, accumulator
  `#incPrefix(L, size(L))`, and returned value
  `#incPrefix(L, size(L))`.

The entry claim at [spec.k](/candidate/spec.k:36) says:

- For **any K `List` `L`**, start from the exact constructor term embedded in
  the claim, an empty environment, `noIter`, and `noResult`.
- Finish with an empty `<k>` cell and
  `result(#incPrefix(L, size(L)))`.
- Use the loop claim as a circularity.

Both preconditions are satisfiable. For the loop claim,
`L=.List`, `I=0`, `l=pyList(.List)`,
`result=pyList(.List)` (the base rule for `#incPrefix`), `noIter`, and
`noResult` is a witness. For the entry claim, `L=.List` in the initial
configuration is a witness. The nonempty witness
`L=[pyInt(1), pyInt(2), pyInt(3)]`, `I=0` is also realizable.

### Program identity

The theorem does not load `solution.mpy`; it embeds a program constructor term.
That term was independently re-rendered from the claim and parsed with the same
fresh definition. Its KORE is byte-identical to the parsed submitted
`solution.mpy`; both hashes are
`0e3ca1fd4be832edbd4df8f3e3fce0a4db346404d93a937010bbbe9945943020`.
See the reviewer term
[entry-program-from-spec.mpy](evidence/entry-program-from-spec.mpy) and
[28-entry-program-pinning-rerun.log](evidence/28-entry-program-pinning-rerun.log).
Together with the trusted translation identity in Stage 2, this pins the claim
to the real submitted program syntax.

### Concrete substitutions and result constraint

Fresh ground K claims prove the exact concrete list results for `[]` and
`[1,2,3]` by finite execution:
[ground-substitution.k](evidence/ground-substitution.k),
[29-ground-empty-proof.log](evidence/29-ground-empty-proof.log), and
[30-ground-three-proof.log](evidence/30-ground-three-proof.log).
Those results agree with both Python implementations.

The candidate's universal postcondition does **not** state those concrete
lists. It states the program-derived term
`#incPrefix(L, size(L))`. Only the zero case unfolds directly. For positive
indices the symbol is opaque, declared total despite non-exhaustive equations,
and is advanced by a special loop-update simplification. The same symbol is
then used in the invariant and final postcondition. There is no independent
universal claim connecting fixed execution to this value, nor a universal
theorem that it equals a `pyList` of the element-wise increments.

The postcondition is syntactically result-constraining and the fresh mutation
in Stage 6 rejects a wrong result. It is nevertheless circular as a statement
of the requested value: the proof-local abstraction that replaces the
property-bearing update is also the asserted answer.

Stage 4 result: **FAIL**. Program syntax is pinned, but the universal returned
value is not soundly connected to the intended result.

## 5. Rule-by-rule static soundness review

There are no candidate helper K source files beyond `semantic.k` and
`verification.k`. There are no local `functional`, `priority`, `owise`,
`concrete`, or macro declarations. The mechanically extracted inventory is in
[27-rule-inventory-extract.log](evidence/27-rule-inventory-extract.log), and
the complete line-numbered sources are in
[03-source-inspection.log](evidence/03-source-inspection.log).

### Local syntax, cells, functions, and opaque values

| Location | Declaration | Audit decision |
|---|---|---|
| `semantic.k:8-11` | `Program`, `Stmts`, `Params`, `Strings` | Minimal constructor grammar; matches the submitted module and one parameter. |
| `semantic.k:13-16` | `Stmt = FuncDef | Assign | For | Return` | Exactly covers all submitted statement forms. |
| `semantic.k:18-22` | `Exp = Name | Int | ListExpr | BinOp`; `Exps` | Exactly covers submitted expression syntax, although `BinOp` accepts arbitrary operator strings while behavior covers only `"+"`. |
| `semantic.k:33-36` | `PyVal = pyInt | pyList | #incPrefix`; `Result`; `IterVal` | `pyInt`/`pyList` are adequate for integer-list tests. `#incPrefix` is a proof-only program-derived value and is the material opaque abstraction. |
| `semantic.k:40-46` | `<k>`, `<env>`, `<iter>`, `<result>` | Sufficient for this program. No allocation or I/O is required. The separate iterator cell does not model Python's post-loop variable binding, but the submitted return cannot observe it. |
| `semantic.k:48-52` | `#init`, `#exec`, `#for`, `#bind`, `#return` | Internal control constructors are sufficient for the submitted flow. |
| `semantic.k:34` | `#incPrefix [function,total]` | Non-exhaustive and program-derived. Only index 0 has a direct defining equation. The compiler warns. **Illegitimate result-bearing abstraction.** |
| `semantic.k:91` | `#eval [function,total]` | Covers submitted expression shapes with bound names and `"+"`, but not every declared expression/operator/binding. The compiler warns. Sound only on the narrower reached subset. |
| `semantic.k:92` | `#add [function,total]` | Concrete rules cover int/int and list/list, not mixed values; the compiler warns. The unguarded summary case can erase an unresolved inner mixed addition. **Materially unsound in the claimed domain.** |
| `semantic.k:93` | `#at [function,total]` | Correct for in-bounds nonnegative indices but has no empty/out-of-bounds/negative equation despite `[total]`. Loop control makes target integer-list uses in bounds. |
| `semantic.k:94` | `#evalExps [function,total]` | Structurally complete for an `Exps` sequence, conditional on `#eval`. |
| `semantic.k:95` | `#asList [function]` | Defined only for `pyList`; the entry precondition supplies that outer value. |

The submitted constructs map completely: `Module`/`FuncDef`/`Params` to
`#init`; statement sequencing to `#exec`; `Assign` to the environment update;
`For` to `#for`/`#bind`; `Return` to `#return`; and
`Name`/`Int`/`ListExpr`/`BinOp("+")` to `#eval`, `#evalExps`, and `#add`.
There is no silently unmodeled syntax in `solution.mpy`.

### Every semantic and simplification rule

| Rule location | Role and decision |
|---|---|
| `semantic.k:56-58` | Initializes only the exact one-argument `incr_list` function and binds `l`. Sound and intentionally minimal for this program. |
| `semantic.k:60` | Consumes empty statement sequence. Sound. |
| `semantic.k:62-64` | Evaluates a pure RHS and updates a named environment binding before continuing. Sound for submitted assignments. |
| `semantic.k:66-69` | Evaluates the iterable once, converts it to a list, starts index 0, then continues with remaining statements. Correct order for the submitted `for`. |
| `semantic.k:71-73` | Converts a reached return statement to `#return` and ignores later statements in that `#exec`. Correct for return control. |
| `semantic.k:75-78` | For `I < size(L)`, bind element `I`, execute the body, increment `I`, and repeat. Correct for in-bounds target lists. |
| `semantic.k:80-81` | Ends the loop for `I >= size(L)`. Together with the step guard, exhaustive for integer `I`. |
| `semantic.k:83-84` | Stores the loop variable only in `<iter>`. This gives correct name resolution in the submitted body but does not preserve Python's loop variable after the loop; that variable is unobserved here. |
| `semantic.k:86-87` | Discards the active continuation and records a return value. Correct for the top-level submitted function; no call stack is modeled. |
| `semantic.k:97` | Iterator lookup. Correct on reached target states. |
| `semantic.k:98` | Environment lookup. It overlaps iterator lookup if the same name exists in both with different values; the submitted program never creates that state. This is a non-material subset ambiguity, not a witnessed target error. |
| `semantic.k:99` | Integer literal to `pyInt`. Sound. |
| `semantic.k:100` | List expression to a semantic list of evaluated expressions. Sound only if every element evaluation is defined. Its non-strict symbolic shape is involved in the bridge failure below. |
| `semantic.k:101-102` | Dispatches only binary `"+"` to `#add`. Sound for submitted syntax. |
| `semantic.k:104` | Empty expression list to empty K list. Sound. |
| `semantic.k:105-106` | Evaluates expression-list head then tail structurally. Sound conditional on `#eval`. |
| `semantic.k:108` | Integer addition. Sound over K mathematical integers. |
| `semantic.k:109` | List concatenation. Sound. |
| `semantic.k:110-114` | **Proof-specific simplification / operational bridge.** It replaces appending the current element's increment to `#incPrefix(L,I)` with the next opaque `#incPrefix`. It has no guard requiring an in-bounds integer element or a successfully evaluated inner `#add`. It directly advances the program-derived result used by the postcondition and is not backed by a fixed-execution connection theorem. This is the decisive unsound rule. |
| `semantic.k:116` | Extracts the underlying list from `pyList`. Sound on its match. |
| `semantic.k:117` | Index 0 returns the head `PyVal`. Sound on a nonempty list. |
| `semantic.k:118-119` | Positive index recurses on the tail and decrements. Sound when initially in bounds. |
| `semantic.k:121` | Empty-prefix base, `#incPrefix(L,0) = pyList(.List)`. Truthful for the intended prefix meaning. It does not define positive indices. |
| `verification.k:13-15` | Rewrites equality of two same-list `#incPrefix` values to equality of indices. It is essential to closure: removing it makes the invariant fail at the exit implication; see [verification-no-injectivity.k](evidence/verification-no-injectivity.k) and [25-no-injectivity-proof.log](evidence/25-no-injectivity-proof.log). It is unguarded and unproved. Under the prose meaning “first `I` elements,” the concrete witness `L=[pyInt(0)]`, `I=1`, `J=2` has equal truncated prefixes `[pyInt(1)]` but the rule concludes `1=2`; the missing guards `0 <= I,J <= size(L)` are therefore material to its asserted meaning. |
| `verification.k:17` | `0 <= size(L) => true`. Sound for K lists. |

### Concrete false-conclusion witness for the bridge

The entry claim has no element-type precondition; `L` may be
`ListItem(pyList(.List))`. Thus the ground argument `pyList([pyList([])])`
satisfies the formal entry precondition.

For that state:

1. Fresh LLVM execution stops with exit 113 at
   `#add(pyList(.List), pyInt(1))`:
   [31-krun-outside-int-domain.log](evidence/31-krun-outside-int-domain.log).
2. Both the trusted canonical Python and submitted Python raise `TypeError`
   rather than returning:
   [33-python-nested-list-witness.log](evidence/33-python-nested-list-witness.log).
3. A ground K claim with the candidate's invariant dependency nevertheless
   prints `#Top` and asserts the normal return
   `result(#incPrefix(ListItem(pyList(.List)),1))`:
   [bridge-unsound-witness.k](evidence/bridge-unsound-witness.k) and
   [32-bridge-unsound-witness-proof.log](evidence/32-bridge-unsound-witness-proof.log).
4. Selecting the same ground entry claim while filtering out the invariant
   fails. Its residual contains the unresolved mixed `#add` and cannot imply
   the `#incPrefix` postcondition:
   [37-bridge-witness-fixed-execution-proof.log](evidence/37-bridge-witness-fixed-execution-proof.log).

This is not merely missing coverage. Rule `semantic.k:110-114`, used through
the circular invariant, swallows a property-bearing unresolved computation and
fabricates the next result abstraction. It enables a false normal-return
conclusion on a state satisfying the formal theorem's entry precondition. The
natural examples suggest an integer-element intent, but the formal claim is
explicitly broader and the proof extension itself is not sound over its match
domain.

Stage 5 result: **FAIL**.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. A fresh reviewer mutation retained the
real program and invariant but replaced the entry result obligation with
`result(pyInt(0))`. This is demonstrably false for the satisfying witness
`L=.List`, for which both Python and fresh concrete K return an empty list.

The mutation source is
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k). `kprove --dry-run`
successfully parsed and built the proof input with exit 0:
[34-vacuity-dry-run.log](evidence/34-vacuity-dry-run.log). The actual proof
then exited 1 with a reached final configuration and the expected unmet
equality between `pyInt(0)` and `#incPrefix(L,size(L))`:
[35-vacuity-proof.log](evidence/35-vacuity-proof.log).

This is valid non-vacuity evidence: the original postcondition constrains the
result enough to reject this mutation. It does not repair the unsound value
bridge.

Stage 6 result: **PASS**.

## 7. Proven-versus-assumed accounting

What `#Top` establishes precisely is conditional:

> Under the candidate's constructor grammar, operational rules, incomplete
> total-function declarations, `#incPrefix` update simplification, unguarded
> `#incPrefix` injectivity simplification, and the loop circularity, the exact
> submitted constructor term reaches an empty `<k>` cell whose result is the
> candidate-defined term `#incPrefix(L,size(L))`.

It does not independently establish that this term is the real Python list
`[e + 1 for e in l]`.

| Boundary or assumption | Influence | Assessment |
|---|---|---|
| K built-in `INT`, `LIST`, `MAP`, `BOOL`, `K-EQUAL`, and `MAP-SYMBOLIC` | Integer arithmetic, list structure, maps, solver equalities | Acceptable low-level K trust boundary. |
| Trusted `py2mpy.py` | Source-to-constructor syntax | Acceptable mounted translator; fresh byte identity was checked. |
| Candidate minimal statement/control semantics | Evaluation order, environment, loop, return | Empirically supported and statically sound for the submitted integer-list path, with documented subset limitations. |
| `#incPrefix(List,Int) [function,total]` | Final value and loop invariant | Illegitimate program-derived opaque value. Non-exhaustive and not independently connected to fixed execution. |
| `semantic.k:110-114` summary simplification | Replaces every symbolic accumulator update; can erase unresolved element addition | Illegitimate operational bridge; the ground false-return witness demonstrates a match outside its justification. |
| `verification.k:13-15` injectivity | Needed to close the loop exit implication | Unproved, unguarded axiom; false under the stated ordinary prefix meaning outside valid prefix-length guards. |
| Integer-element assumption | Whether `value + 1` is defined | Missing from the formal entry precondition. Concrete semantics and Python disagree with the proved normal return on a satisfying non-integer K-list state. |
| Differential testing | Python implementation-to-canonical bridge for 4,171 integer lists | Strong finite evidence only; it cannot prove the universal K abstraction or validate proof rules. |
| Informal interpretation of `#incPrefix` as “incremented prefix” | Human-facing postcondition | Not machine-checked. The candidate's base and update rules do not form a safe, exhaustive fixed-execution connection over the formal precondition. |

Gate accounting:

- **Gate A — real-program soundness: FAIL.** The result-bearing operational
  bridge has no adequate universal connection theorem and admits the concrete
  false normal-return witness above.
- **Gate B — intent adequacy: FAIL.** The K entry domain is unrestricted over
  K-list contents while the modeled addition is not, exceptions are absent,
  and the stated result remains an opaque summary rather than the requested
  Python list.
- **Gate C — trust and auditability: FAIL for the candidate package.** It
  contains no trust ledger or validation report, marks incomplete functions
  total, and its `prove.sh`/generation report treats `#Top` as the end of the
  argument. The reviewer-authored evidence makes the failure reproducible but
  does not repair it.

The implementation itself appears correct on integer lists, the real program
syntax is pinned, the positive claims close, and the theorem is non-vacuous.
Those facts cannot compensate for a materially unsound, result-bearing proof
extension. The candidate therefore does not contain a legitimate
partial-correctness proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
