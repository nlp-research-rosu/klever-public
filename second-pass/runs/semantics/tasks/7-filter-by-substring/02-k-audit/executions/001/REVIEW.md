# Independent adversarial review: 7-filter-by-substring

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program under the supplied MPY semantics. The proof
reconstructs cleanly, the program macro is the exact parsed submitted program,
the loop body executes rather than being replaced by an answer oracle, and a
fresh false result obligation is rejected after reaching the correct concrete
final heap.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
candidate is missing all four requested provenance records and did not supply
its own bridge-free connection theorem for its two operational proof bridges.
The latter gap was independently investigated: a bridge-free theorem using the
same exhaustive algebraic representation equations closes with `#Top`, and
opposite ground interpretations are rejected. Thus this is an auditability
limitation, not a demonstrated semantic unsoundness.

All candidate content was treated as untrusted. `/candidate` was never used as
a build directory. Fresh definitions and experiments were made under
`/tmp/audit-work`; reviewer artifacts and bounded logs are under
[`evidence/`](evidence/).

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so there is no mode/mount
contradiction and no infrastructure breach.

The candidate `reference-semantics/` tree and the trusted tree contain the same
root `semantics.k` and 23 helper `.k` files. Every entry is an ordinary file or
directory; there are no symlinks. Recursive `diff -qr --no-dereference` exited
0 with no output. See
[`stage1-artifact-types.log`](evidence/stage1-artifact-types.log) and
[`stage1-semantics-compare.log`](evidence/stage1-semantics-compare.log).

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`; both `cmp`
commands exited 0. Hashes and commands are in
[`stage1-source-hashes.log`](evidence/stage1-source-hashes.log),
[`stage1-prompt-compare.log`](evidence/stage1-prompt-compare.log), and
[`stage1-translator-compare.log`](evidence/stage1-translator-compare.log).

### Missing and additional artifacts

The following requested candidate records are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace (`*trace*` or `*.jsonl`) is present. This is
recorded in
[`stage1-required-artifacts.log`](evidence/stage1-required-artifacts.log).
Because these files are provenance evidence rather than proof sources, their
absence does not invalidate the independently rebuilt theorem, but it prevents
a complete generation-history audit.

The candidate additionally contains `concrete_tests.py`,
`concrete_tests.mpy`, `prove.sh`, and a Python `__pycache__`. The tests and
script were inspected only as untrusted suggestions. The bytecode cache was
ignored and never copied into the build. There are no candidate-provided K
kompiled directories or K caches.

The exact scratch-copy command and post-copy hashes are preserved in
[`scratch-copy.log`](evidence/scratch-copy.log) and
[`scratch-copy-hashes.log`](evidence/scratch-copy-hashes.log).

**Stage 1 finding:** integrity of every proof/source input is established;
provenance metadata is incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, the function accepts a
finite `List[str]` and a `str`, constructs a new list, and retains exactly those
input elements for which Python's `substring in element` is true. Input order
and duplicate occurrences are preserved. The empty list returns empty; the
empty substring matches every string, including the empty string.

`solution.py` implements the same contract with an explicit accumulator and
loop:

1. allocate `result = []`;
2. visit each input string once;
3. append that same string exactly when `substring in string`;
4. return `result`.

It neither mutates the input list nor changes element identity/content.

### Trusted translation

The trusted `/reference/py2mpy.py` regenerated
[`solution.regenerated.mpy`](evidence/solution.regenerated.mpy) from the scratch
copy of `solution.py`. `cmp -l` against the submitted `solution.mpy` exited 0,
and both files have SHA-256
`78e9c004ec76138d1019cc2f83c68fa31f8e86289c2098228d7975b141981d7e`.
See [`stage2-translate.log`](evidence/stage2-translate.log) and
[`stage2-mpy-byte-identity.log`](evidence/stage2-mpy-byte-identity.log).

### Independent differential testing

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry point and the scratch generated entry point. Its
complete 26,324 inputs are preserved in
[`differential-inputs.jsonl`](evidence/differential-inputs.jsonl). The scope was:

- both documented examples;
- empty list, empty string, and empty substring;
- prefix, middle, suffix, exact, longer-than-string, and no-match boundaries;
- duplicates and order preservation;
- Unicode examples;
- all 25,312 combinations of lists of length 0–3 over strings of length 0–3
  from `{a,b}`, with substrings of length 0–2;
- 1,000 deterministic seeded random cases with list length up to 8, string
  length up to 12, and ASCII/space/Unicode characters.

The run exited 0 with `mismatches=0`; neither implementation mutated an input
list. See [`stage2-differential.log`](evidence/stage2-differential.log) and the
input count/hash in
[`stage2-input-count-hash.log`](evidence/stage2-input-count-hash.log).

An optional `py_compile` diagnostic attempted to write
`/reference/__pycache__` and exited 1 because the trusted mount is read-only.
That check is not used as evidence. The differential script successfully
imported and executed both files without writing the trusted mount.

**Stage 2 finding:** the submitted Python program matches the trusted canonical
implementation on the intended domain, and the submitted MPY is exactly its
trusted translation.

## 3. Clean proof reconstruction

K v7.1.337 was independently available. Versions are recorded in
[`stage3-toolchain.log`](evidence/stage3-toolchain.log).

### Concrete definition

From the copied source tree, with no candidate cache:

```text
timeout 600 kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The command exited 0. The compiler emitted supplied-baseline warnings about
several non-exhaustive or unused declarations, none on the program path.
[`stage3-runtime-build.log`](evidence/stage3-runtime-build.log) contains the
exact command, warnings, and status.

The translated candidate function plus five normal/boundary assertions ran
with:

```text
timeout 180 krun concrete_tests.mpy --definition runtime-kompiled
```

It exited 0 with `.K`, `NoExc`, and exit code 0. The final heap shows the
expected empty, documented, empty-substring, exact-substring, and no-match
results. See
[`stage3-concrete-tests.log`](evidence/stage3-concrete-tests.log).

### Proof definition and positive targets

The proof definition was freshly built:

```text
timeout 600 kompile verification.k --backend haskell \
  --main-module FILTER-VERIFICATION \
  --syntax-module FILTER-VERIFICATION \
  --output-definition verification-kompiled
```

It exited 0; see
[`stage3-proof-build.log`](evidence/stage3-proof-build.log).

The original two-claim candidate spec was then run exactly:

```text
timeout 600 kprove spec.k --definition verification-kompiled \
  --spec-module FILTER-SPEC --output pretty
```

It exited 0 and printed `#Top`; see
[`stage3-proof-all.log`](evidence/stage3-proof-all.log).

Because the two source claims are unlabeled, scratch-only labeled copies were
also used to audit them separately:

- The loop claim alone exited 0 with `#Top`:
  [`spec-loop-only.k`](evidence/spec-loop-only.k) and
  [`stage3-proof-loop-only.log`](evidence/stage3-proof-loop-only.log).
- The entry claim was run with the separately proved loop target marked
  trusted for that composition. It exited 0 with `#Top`:
  [`spec-labeled.k`](evidence/spec-labeled.k) and
  [`stage3-proof-entry-with-proved-helper.log`](evidence/stage3-proof-entry-with-proved-helper.log).

As a diagnostic, deleting the helper claim and running the entry claim alone
timed out at the audit's 30-second bound
([`stage3-entry-without-helper-diagnostic.log`](evidence/stage3-entry-without-helper-diagnostic.log)).
That is not a candidate target configuration: the submitted spec includes the
loop circularity, and the complete submitted spec closes quickly.

**Stage 3 finding:** both positive claims close in a clean reconstruction, and
the entry proof composes with an independently closed loop claim.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim has no textual `requires`; its sort and cell patterns are its
precondition. It starts at a real MPY loop head over a finite typed suffix
`SS`, with:

- local bindings for the original input, substring `P`, result reference `H`,
  and current loop string `CUR`;
- heap location `H` containing accumulator `ACC`;
- the exact translated loop body and an arbitrary continuation `CONT`.

It states that consuming the remaining loop preserves `CONT`, changes the
result heap value to `filterAccStrings(ACC,P,SS)`, and leaves the loop variable
equal to `CUR` for an empty suffix or to the last visited suffix element
otherwise (`lastCodes(CUR,SS)`). All omitted configuration cells are framed.

The entry claim also has no textual `requires`. It starts from the exact empty
module configuration: environment 0, empty module scope over the supplied
builtins scope, `scopeLoc=1`, empty heap with `heapLoc=0`, empty stack,
`noRet`, `NoExc`, and exit code 0. Its `<k>` cell loads `filterProgram` and
calls `filter_by_substring` with a finite `StrSeq` list and `IntSeq` substring.

It states that execution returns exactly `ref(0)`, the module scope contains
the exact function closure, heap location 0 contains
`list(filterStrings(P,SS))`, `heapLoc` is 1, and all control/exception cells
are clean. The return is not a free variable: `filterStrings` is a total,
terminating recursive function with exhaustive equations.

### Exact submitted-program identity

`filterProgram` and `solution.mpy` were independently parsed with macro
expansion using the fresh proof definition. Their JSON KAST files are byte
identical with SHA-256
`88a17fd37cf42e25207c2cb9899c8b53a205b285982bf5f444434a33527db09e`.
See [`solution.kast.json`](evidence/solution.kast.json),
[`filterProgram.kast.json`](evidence/filterProgram.kast.json), and
[`stage4-program-ast-identity.log`](evidence/stage4-program-ast-identity.log).
Thus the entry claim does not load a substituted program.

The helper matches actual control flow. The initial `For` head has no
`string` binding; fixed semantics unrolls one iteration, binds `string`,
executes the body, and returns to `#loop`, where the helper circularity applies.
Empty input finishes without needing the helper. One-element input reaches the
helper with an empty suffix.

### Satisfiable witnesses and substitution

One concrete entry witness is:

```text
strings = ["abc", "bacd", "cde", "array"]
substring = "a"
SS = ssCons(codes("abc"), ssCons(codes("bacd"),
     ssCons(codes("cde"), ssCons(codes("array"), .StrSeq))))
P = iCons(97, .IntSeq)
```

The trusted canonical function and generated function both return
`["abc","bacd","array"]`. The exact code-sequence substitution and claimed
`ValSeq` normal form are printed in
[`stage4-ground-python.log`](evidence/stage4-ground-python.log).

The result-specific K claim in
[`spec-ground-witness.k`](evidence/spec-ground-witness.k) uses that exact
initial entry configuration and exact three-element final heap. It exits 0
with `#Top`; see
[`stage4-ground-kprove-corrected.log`](evidence/stage4-ground-kprove-corrected.log).

A realizable loop witness after visiting `"abc"` and `"bacd"` uses
`L=1`, `H=0`, `CUR=codes("bacd")`, `ACC=["abc","bacd"]`, remaining
`SS=["cde","array"]`, and continuation
`Return(Name("result")) ~> #endcall`, with the function frame, heap, stack,
and counters produced by the fixed call rules. It satisfies every loop-cell
pattern and corresponds to a reachable state of the documented entry witness.

**Stage 4 finding:** both claims are satisfiable, result-constraining, and
pinned to the real submitted MPY program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`static-inventory.md`](evidence/static-inventory.md) and
[`static-inventory.json`](evidence/static-inventory.json) enumerate the complete
source block, file, and line range for every local declaration in the supplied
semantics tree, `verification.k`, and `spec.k`. The reviewer-authored generator
is [`static_inventory.py`](evidence/static_inventory.py). It found 957
declarations:

- 237 syntax declarations;
- 149 function declarations, of which 110 are marked `total`;
- no distinct `[functional]` declarations;
- 25 explicit `symbol(...)` declarations, 22 also marked
  `no-evaluators`;
- 712 rules: 710 ordinary and 2 simplification rules;
- 47 priority rules, 35 concrete rules, and 26 `owise` rules;
- 5 contexts, 1 configuration, and 2 reachability claims.

This is the exhaustive inventory; the tables below give the soundness
disposition rather than duplicating 957 full source blocks in this report.

All baseline records D0001–D0928 are byte-identical supplied semantics and are
accounted as the selected fixed-semantics trust boundary, not candidate proof
extensions. The relevant execution slice was still traced rule by rule:

| Submitted construct | Declaration and fixed execution path |
|---|---|
| `Module`, `ImportFrom`, `FuncDef` | `syntax.k`; `core.k` `#loadAll`/statement sequencing; `controls.k` import no-op; `functions.k` closure creation |
| `Call`, `Name`, `Params` | `core.k` lookup and left-to-right argument evaluation; `call.k` closure dispatch/frame push; `functions.k` parameter binding |
| `Assign`, `ListExpr` | RHS strictness; `list.k` argument collection and `#alloc`; `controls.k` local-scope write |
| `For` | iterable evaluated once; `controls.k` `#loop/#loopStep`; list iterator head/tail rules plus the reviewed symbolic iterator bridge |
| `If`, `Compare(...,"in",...)` | left/right comparison contexts; `str.k` `applyCmp`, `strPrefix`, and `strContains`; proof bridge; `controls.k` truth/branch rules |
| `Attribute`, `Call(...append...)`, `Expr` | receiver and argument evaluation; bound-method dispatch; `list.k` in-place append at the result heap location; expression-result discard |
| `Return` | strict result evaluation, `retV`, frame pop, environment restoration, scope deallocation, and returned reference |

This trace accounts for evaluation order, binding, calls/returns, allocation,
heap mutation, control, and every configuration cell in the entry poststate.
Other supplied modules and rules cannot match any submitted AST or reachable
value on this path. The 25 baseline symbols are:

`md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`; and `sortVS`, `sortKeyVS`.

None occurs in `solution.mpy`, `verification.k`, either claim, or a reachable
term in the reconstructed proof. They therefore have no value, branch,
control, state, or postcondition influence here. `strContains` is not opaque:
its supplied equations are exhaustive recursion over `IntSeq`.

### Candidate proof-extension inventory and decisions

The 27 `verification.k` records are D0929–D0955 in the exhaustive inventory:
10 syntax declarations and 17 rules. Every one is disposed below.

| Records | Class and complete domain | Decision |
|---|---|---|
| D0929–D0932 | `StrSeq` algebra and `strVals` empty/cons equations | Accepted definitional representation. Constructors are disjoint and exhaustive; recursion strictly shortens the sequence. |
| D0933–D0936 | `#strIterNext`; priority-40 bridge for any `SS:StrSeq`; empty and cons outcomes | Accepted operational bridge. It preserves arbitrary continuation and all cells and gives exactly the fixed list iterator's done/head/tail behavior. |
| D0937–D0940 | `#strContainsBool`; priority-40 bridge for all `P,S:IntSeq`; true/false guarded outcomes | Accepted operational bridge. Operands are already values; the bridge preserves continuation/cells and returns exactly supplied `strContains(P,S)`. Guards are disjoint and exhaustive over `Bool`. |
| D0941–D0944 | total `filterAccStrings`; empty, contains, and non-contains equations; two simplification rules | Accepted definitional summary. It is not an execution rewrite. Equations are exhaustive, disjoint, terminating, preserve order/duplicates, and append exactly on the same `strContains` predicate used by execution. |
| D0945–D0946 | total `filterStrings` wrapper | Accepted: a single total equation fixes the final value to `filterAccStrings(.ValSeq,P,SS)`. |
| D0947–D0949 | total `lastCodes`; empty and cons equations | Accepted auxiliary summary. Constructors are exhaustive/disjoint and recursion shortens `SS`. It tracks the final target binding and does not determine the returned list. |
| D0950–D0955 | three macro syntax declarations and their expansion rules | Accepted program pinning, not an oracle. Expanded `filterLoopBody`, `filterBody`, and `filterProgram` are exactly the parsed submitted AST, as the byte-identical KAST test establishes. |

No proof-local opaque or fresh result symbol exists. No `total` declaration has
an uncovered constructor case. The two simplification rules have complementary
true/false guards and true equations. The two priority rules preempt fixed
steps but do not broaden their value or state effect.

### Operational-bridge validation

The candidate did not include a universal bridge-connection theorem. The audit
therefore built one without importing D0933–D0940:

- [`bridge-base-total.k`](evidence/bridge-base-total.k) imports only the fixed
  `MPY` semantics and gives `strVals` the same two exhaustive equations as a
  total mathematical function.
- [`bridge-connection-spec.k`](evidence/bridge-connection-spec.k) proves both
  iterator constructors and both containment truth outcomes, each with an
  arbitrary `CONT:K`.

The bridge-free definition built with exit 0 and all four claims produced
`#Top` with exit 0. See
[`stage5-bridgefree-build-total-representation.log`](evidence/stage5-bridgefree-build-total-representation.log)
and
[`stage5-bridge-connection-proof-total-representation.log`](evidence/stage5-bridge-connection-proof-total-representation.log).
Quantifying `CONT` establishes context containment, while omitted cells are
universally framed; neither bridge introduces return, exception, allocation,
or state mutation.

The first diagnostic used the candidate's ordinary, non-functional
`strVals` declaration verbatim. It got stuck because fixed semantics does not
evaluate that representation underneath `list(...)`; see
[`bridge-base-ordinary-failed.k`](evidence/bridge-base-ordinary-failed.k) and
[`stage5-bridge-connection-proof.log`](evidence/stage5-bridge-connection-proof.log).
This explains the need for a symbolic iterator bridge. The successful theorem
adds only congruent evaluation of the same exhaustive representation equations,
not the candidate bridge or a task-answer equation.

Opposite ground interpretations were also rejected:

- claiming `"a" in "abc"` is false reaches `true` and exits 1;
- claiming the head of `["a"]` is `"b"` reaches a yield of `"a"` and exits 1.

See
[`stage5-opposite-containment-proof.log`](evidence/stage5-opposite-containment-proof.log)
and
[`stage5-opposite-iterator-proof.log`](evidence/stage5-opposite-iterator-proof.log).

Finally, deleting the real append-bearing loop body from a scratch verification
copy did not leave the proof intact. The mutated definition built successfully,
but `kprove` exited 1 with a stuck accumulator equality. See
[`verification-body-deleted.k`](evidence/verification-body-deleted.k),
[`stage5-body-mutation-build.log`](evidence/stage5-body-mutation-build.log), and
[`stage5-body-mutation-proof.log`](evidence/stage5-body-mutation-proof.log).
This demonstrates program-body sensitivity independently of the Stage 6
postcondition mutation.

No inventoried rule was labeled unsound: the audit found no rule capable of a
false conclusion on the intended input domain. The narrower evidence gap is
that the candidate itself omitted the bridge-free theorem later reconstructed
by this audit.

**Stage 5 finding:** the fixed execution path and every proof extension are
sound for the theorem; no answer oracle, execution bypass, guard overlap, or
unconstrained result exists.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so no candidate mutation was
trusted or reused.

The fresh mutation
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) keeps the documented
satisfying input
`(["abc","bacd","cde","array"], "a")` but falsely constrains the result heap to
`["abc","bacd"]`, omitting `"array"`.

First, `kprove --dry-run` compiled the mutated spec successfully and exited 0;
see [`stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log). The
actual proof then exited 1 with `WarnStuckClaimState`. Its residual is the
fully terminated configuration with `ref(0)` and the actual heap value
`["abc","bacd","array"]`, so failure is caused by the deliberately unmet result
obligation—not parsing, imports, timeout, crash, or unreachable code. See
[`stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log).

**Stage 6 finding:** the proof is non-vacuous and discriminates a reachable
false result.

## 7. Proven versus assumed accounting

### What is formally proved

Under the freshly compiled supplied MPY semantics plus the audited
`verification.k` definitions, for every finite `StrSeq SS` and every finite
`IntSeq P`, execution from the exact entry configuration of the exact submitted
program satisfies partial correctness:

- the function returns `ref(0)`;
- heap 0 contains `list(filterStrings(P,SS))`;
- `filterStrings` retains each source string in order exactly when the supplied
  total `strContains(P,S)` predicate is true;
- duplicates are preserved;
- the result list is freshly allocated from the initially empty heap;
- module/function scope, counters, stack, return state, exception state, and
  exit code have the claimed final values.

The loop claim formally establishes the accumulator transformation and final
loop-target binding for any typed remaining suffix. The theorem is partial
correctness in the Kit sense; it is not a claim about arbitrary CPython
programs or arbitrary dynamic argument types.

### Trust ledger

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| K v7.1.337 parser, compiler, Haskell prover, and LLVM runner | Entire machine-checking result | Standard toolchain trust boundary; fresh commands and actual statuses are logged. |
| Exact supplied `reference-semantics` tree | All MPY execution steps | Authorized fixed-semantics boundary; candidate tree is recursively identical. Used-path control/state rules were traced above. |
| K built-in integer, Boolean, string, map, list, equality, and rewriting hooks | Algebra and configuration machinery | Ordinary K foundation assumed by the supplied semantics. |
| Proof `StrSeq`/`strVals` representation | Symbolic list-of-strings domain and iterator bridge | Exhaustive algebraic equations; bridge-free four-case connection proof, arbitrary-continuation coverage, and rejected opposite witnesses. |
| `IntSeq` as the model of Python string code points; `strContains` as Python substring membership | Bridge from formal result to natural-language/Python intent | Direct sequence definition in supplied `str.k`; exhaustive Python differential evidence includes boundaries and Unicode. This is not a separate K theorem about CPython internals. |
| Trusted translator | Identity of Python and submitted MPY AST | Candidate translator equals trusted translator; fresh output is byte-identical; expanded program KAST is identical. |
| Trusted canonical Python function | Differential oracle only | Supports the implementation-to-intent bridge over 26,324 cases; it is not used to close the K proof. |
| 25 supplied opaque/concrete-only symbols listed in Stage 5 | Potentially values in unrelated tasks | None is reachable or referenced here, so none influences this theorem. |

The formal entry represents read-only input lists as bare `list(ValSeq)` values
rather than heap references. This is sound for the stated function because it
never mutates or returns the input object; all observable result content and
the fresh result allocation are constrained. Inputs outside `List[str] × str`,
CPython exception behavior outside this path, identity observations not in the
contract, and unused MPY language constructs are excluded.

### Gate and verdict rationale

- Real-program soundness: pass. Exact AST pinning, bridge connection,
  body-sensitivity, positive `#Top`, and false-result rejection all hold.
- Intent adequacy: pass. The formal recursive result is exactly stable
  substring filtering over the intended typed finite domain; Python
  differential evidence has zero mismatches.
- Evidence/auditability: concern. Four requested provenance files are missing,
  and the bridge-connection theorem had to be reconstructed by the auditor
  rather than inspected as a candidate artifact.

Those concerns do not make a false conclusion provable and do not create a
material adequacy gap. They therefore justify `CONCERNS / LEGIT`, not
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
