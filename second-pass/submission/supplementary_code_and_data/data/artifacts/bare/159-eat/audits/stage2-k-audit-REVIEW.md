# Independent adversarial audit: HumanEval 159 `eat`

## Overall decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the trusted-regenerated `solution.mpy` over the complete documented
input domain. I rebuilt both definitions from source, proved all six positive
claims together and independently, mechanically pinned the claim’s
`solutionProgram` term to the submitted constructor tree, checked concrete
execution against both Python implementations, changed the executed body, and
ran a fresh false-postcondition mutation.

The qualification is in the generated language definition: ten declarations
marked `[total]` are not globally exhaustive over the broad sorts the candidate
declares. Fresh LLVM compilation reports this directly. Every invocation
reachable from the exact submitted program is covered, and I found no concrete
or symbolic witness by which those off-path gaps enable a false conclusion on
the intended input domain. Under the benchmark’s explicit boundary, this is an
over-broad-but-sound-on-the-intended-program limitation, so the result is
`CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

All candidate material and historical generation output was treated as
untrusted. Commands were executed only against source copied to
`/tmp/audit-work/159-eat-audit/rebuild`; no candidate-provided compiled
definition or cache was available or reused. Reviewer scripts, mutations,
inputs, and bounded logs are under `/audit-output/evidence/`.

## 1. Input and provenance integrity

### Declared layout and mounts

`/audit-input.json` declares:

- problem `159-eat`;
- condition `bare`;
- semantics mode `GENERATED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The required `/reference/reference-semantics` tree is absent, as it must be for
`GENERATED_SEMANTICS`; I did not search for or infer any hidden reference
semantics. The candidate, generation trace, and every required launcher record
are real regular files/directories, with no symlinked or special entries.

I read and parsed `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/usage.json` (present),
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and the complete structured trace. Historical
`runtime-metrics.json` is not present and was not reconstructed; it is not
required for this legacy-selected layout.

### Independent integrity results

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` exactly. Independently recomputed SHA-256 values
match every launcher-recorded file hash, including the lock, run/task/result
records, invocation, metrics, usage, prompt, final message, complete output log,
trusted canonical, trusted/candidate prompt, and trusted/candidate translator.
Every evidence file named by both `generation-result.json` and
`invocation.json` is present as a regular file and matches its recorded digest.

The candidate prompt is byte-identical to `/reference/prompt.py`; the candidate
translator is byte-identical to `/reference/py2mpy.py`. The independently
computed pipeline-contract tree digest of `/candidate` is
`8e2b81ca8c45c781f6b1f62dff963f2b505a92bdfa72f7bd94852f4e7818e281`,
exactly the workspace digest recorded by the generation result. The equivalent
trace-tree digest is
`bc12a979db47584b4f8652fcf56ffe7dcbcc4e178594091d56f7246b4e8588ab`,
exactly `usage.json`’s source-trace digest. The audit manifest’s two aggregate
tree fields use a different, unspecified serialization; I recorded those
values separately rather than incorrectly comparing unlike serializations.
All constituent file hashes and the independently documented tree digests
match their corresponding pins.

The corrected integrity run has 68 checks and zero failures:
[01-provenance-check.log](/audit-output/evidence/01-provenance-check.log).
The retained
[initial log](/audit-output/evidence/01-provenance-check-initial-algorithm-mismatch.log)
shows the reviewer’s rejected attempt to compare the audit-specific aggregate
against the different pipeline-contract serialization; it is not a mounted-file
mismatch.

The structured trace contains one JSONL file, 367 valid records, zero malformed
records, and zero error events. It includes historical claims of ten `#Top`
strings and six earlier stuck states; none was used as verification evidence.
See
[01-generation-record-summary.log](/audit-output/evidence/01-generation-record-summary.log)
and the extracted
[tool calls](/audit-output/evidence/generation_trace_tool_calls.txt).

There is no infrastructure contradiction or breach, so a candidate verdict is
appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For integer inputs satisfying
`0 <= number, need, remaining <= 1000`, the rabbit eats
`min(need, remaining)` additional carrots. The function must return:

```text
[number + min(need, remaining), remaining - min(need, remaining)]
```

Equivalently:

- if `need <= remaining`, return
  `[number + need, remaining - need]`;
- otherwise return `[number + remaining, 0]`.

That is the behavior of `/reference/canonical.py`. The candidate
`solution.py` implements the same two branches, with the second return placed
after the `if` rather than in an explicit `else`; early return makes the forms
equivalent.

### Trusted regeneration

From scratch I ran:

```text
python3 /tmp/audit-work/159-eat-audit/trusted/py2mpy.py solution.py > regenerated.mpy
cmp -s regenerated.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`49f9697d0fa8809c3144fc5b812d49e68db0cdbb56b74617e8c089e0a8c6e78a`.
See
[02-mpy-regeneration.log](/audit-output/evidence/02-mpy-regeneration.log).

### Independent differential execution

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical entry point and the copied candidate entry point under
different module names. It also evaluates a separately written `min`-based
contract oracle. Its deterministic scope includes:

- all four documented examples;
- lower/upper and representative Cartesian boundaries;
- every triple in the dense cube `0..20`;
- both sides and equality at every `need`/`remaining` boundary for four
  low/high `number` values;
- 10,000 seeded samples across the full `0..1000` cube.

The exact 31,542 inputs are preserved in
[differential_inputs.json](/audit-output/evidence/differential_inputs.json),
SHA-256
`980e8f1158c2cdd51bb4dd56d990f086aab24c60248b8ec211c327205519d82d`.
There were 17,996 enough-stock cases, 13,546 insufficient-stock cases, and zero
mismatches:
[02-differential-test.log](/audit-output/evidence/02-differential-test.log).
This is finite bridge evidence, not a substitute for the symbolic K proof.

## 3. Clean proof reconstruction

### Toolchain and scratch isolation

`kompile`, `krun`, and `kprove` resolve to `/usr/bin`. `kompile --version` and
`kprove --version` both report K `v7.1.293`, matching the campaign lock:
[00-toolchain.log](/audit-output/evidence/00-toolchain.log).

Only the candidate source files and trusted reference inputs were copied to
`/tmp/audit-work/159-eat-audit`. The mounted candidate contains no compiled
definition. Fresh definitions were written under the scratch tree.

### Concrete definition and executions

The exact build command was:

```text
kompile semantic.k --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

It exited 0. Its non-exhaustive `[total]` warnings are analyzed in stage 5; see
[03-kompile-concrete.log](/audit-output/evidence/03-kompile-concrete.log).

[concrete_semantics_compare.py](/audit-output/evidence/concrete_semantics_compare.py)
then ran fresh `krun solution.mpy --definition concrete-kompiled` executions
on nine normal, lower/upper, equality, and adjacent-branch-boundary inputs.
Every `krun` exited 0 and its parsed `result(A,B)` equaled both Python
implementations. The cases include `(0,0,0)`, `(1000,1000,1000)`,
`(1000,1000,0)`, and the three adjacent cases around
`need = remaining = 500`. See
[03-concrete-semantics-comparison.log](/audit-output/evidence/03-concrete-semantics-comparison.log).
The retained earlier log is explicitly a reviewer regex-parsing mistake after
successful K executions, not a candidate failure.

### Proof definition and positive targets

The exact proof build was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

It exited 0:
[03-kompile-proof.log](/audit-output/evidence/03-kompile-proof.log).

The candidate suite was then run unchanged:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`:
[03-kprove-all-claims.log](/audit-output/evidence/03-kprove-all-claims.log).

Because the six candidate claims are unlabeled, I also extracted each,
unchanged, into a separate reviewer spec module and ran six independent
commands. Every command exited 0 and printed `#Top`:
[03-kprove-individual-claims.log](/audit-output/evidence/03-kprove-individual-claims.log).
The exact extracted claims are under
[individual-specs](/audit-output/evidence/individual-specs/).

The clean dynamic reconstruction gate therefore passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

The first symbolic entry claim assumes all three integers are within
`0..1000` and `need <= remaining`. It proves that execution returns
`result(number + need, remaining - need)`.

The second assumes the same documented bounds and `remaining < need`. It
proves that execution returns `result(number + remaining, 0)`.

Those guards are disjoint and exhaustive over the documented domain. The four
remaining claims prove the four prompt examples directly. There are no helper,
loop, circularity, or invariant claims.

### Program identity

The `<k>` term in both symbolic claims is:

```text
run(solutionProgram, args(NUMBER, NEED, REMAINING))
```

`solutionProgram` has one equation whose right-hand side is a full
`Module(FuncDef("eat",...))` constructor term. It is not a result summary. The
semantic `run` rule checks the exact function name, parameter count/order, and
names; binds the three supplied integer arguments; then evaluates `BODY`.

[program_pinning_check.py](/audit-output/evidence/program_pinning_check.py)
mechanically extracts the `solutionProgram` RHS from the copied
`verification.k`, parses both it and trusted-regenerated `solution.mpy` with
the fresh definition, and compares their constructor JSON. The only
normalization is replacing rule syntax’s `.Stmts` identity with the concrete
grammar’s zero-item statement sequence. Both parsed terms have identical
SHA-256
`00671562d0e02dac111dc8a2d00ce16bc20bc36720319b70ff46dace81229fcf`.
See [04-program-pinning.log](/audit-output/evidence/04-program-pinning.log).
Thus the claim executes the actual submitted program body, not a substituted
algorithm.

### Result constraint and satisfying states

The destination contains no free or existential result variable. Each branch’s
`carrotContract` reduces to an exact `result(Int,Int)` under that branch’s
guard. It is an equality-style result constraint, not a one-way implication or
tautology.

Concrete satisfying substitutions include:

- symbolic enough-stock claim: `(5,6,10)` satisfies the bounds and
  `6 <= 10`; the destination is `result(11,4)`;
- symbolic insufficient-stock claim: `(2,11,5)` satisfies the bounds and
  `5 < 11`; the destination is `result(7,0)`.

Both Python implementations and fresh K execution agree on these values. All
four ground entry claims likewise agree. Full output is in
[04-entry-witnesses.log](/audit-output/evidence/04-entry-witnesses.log).

### Body sensitivity

I copied the proof source and changed the constructor actually bound by
`solutionProgram`: the first returned total uses `number - need` instead of
`number + need`. I did not merely edit external `solution.py`. The mutated
definition built successfully. At satisfying input `(5,6,10)`, `kprove`
stopped at `result(-1,4)` while the unchanged destination required
`result(11,4)`; it emitted `WarnStuckClaimState` and exited 1.

The mutation and log are
[body-sensitivity](/audit-output/evidence/body-sensitivity/) and
[04-body-sensitivity.log](/audit-output/evidence/04-body-sensitivity.log).
This confirms that the positive theorem depends on the executed body.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[05-rule-inventory.md](/audit-output/evidence/05-rule-inventory.md); the raw
declaration scan is
[05-static-declaration-scan.log](/audit-output/evidence/05-static-declaration-scan.log).
It covers all 23 local syntax declarations, 13 function symbols, 21
`semantic.k` rules, four `verification.k` equations, the configuration, and all
six reachability claims. There are no other candidate K helper files.

There are no local opaque symbols, `functional` declarations, simplification
rules, concrete rules, `owise` rules, `anywhere` rules, priority rules, or
priority declarations.

### Construct and control coverage

Every constructor in `solution.mpy` has a declaration and applicable rule:

- `Module`, the exact `FuncDef`, `Params`, and argument binding are handled by
  `run`;
- statement-list identity/cons, `If`, `Return`, normal continuation, and
  abrupt `returned` propagation model both control paths;
- `Name`, `Int`, `BinOp("+")`, `BinOp("-")`, single `<=` comparison, and the
  two-element `ListExpr` are evaluated structurally;
- K integer addition, subtraction, and comparison compute the values;
- `resultOf` preserves both integers from the returned list.

The true branch’s return propagates through `continueWith(returned(...))` and
skips the following return. The false branch evaluates the empty `else`,
continues normally, and reaches the following return. This matches the real
source control flow.

There are no source assignments, heap effects, I/O, exceptions on documented
inputs, calls from expressions, loops, or recursion. Hence the one-cell
configuration omits no observable state used by this program. K `Int` matches
Python’s arbitrary-precision integer behavior for these operations, and the
program’s only observable collection behavior is the two returned elements.

All recursive evaluator equations descend structurally. The guards for
`leVals` and `carrotContract` are pairwise disjoint and exhaustive over
integers. Constructor-specific equations do not overlap. The parameter map has
three distinct literal keys, so every reachable `lookup` is bound.

### No execution-bypassing proof rule

`carrotContract` is a truthful, piecewise mathematical destination summary. No
semantic rule rewrites any `run`, statement, expression, or returned value to
`carrotContract`. The program instead reduces through the generic interpreter
to arithmetic `result` terms, while the destination summary reduces
independently. There is no fresh result-bearing oracle shared between execution
and postcondition, no operational bridge, and no circular value
justification.

`solutionProgram` is a definitional name for the mechanically identical
constructor tree. It does not replace an executed operation with an answer.
The body-sensitivity mutation independently confirms this.

### Non-fatal totality limitation

Fresh LLVM compilation reports non-exhaustive matches for ten declarations
marked `[total]`: `carrotContract` and `validInput` before their proof-layer
equations are imported, plus partial broad-sort declarations such as `lookup`,
`evalExpr`, `addVals`, `subVals`, `leVals`, `evalStmt`, `chooseBranch`, and
`resultOf`.

Concrete out-of-scope gaps include `lookup("missing", .Map)`, an expression
with an unsupported operator string, arithmetic on `listVal`, direct
`evalStmt(FuncDef(...))`, a non-Boolean branch value, or `resultOf(normal)`.
Those annotations are broader than the generated semantics actually defines
and should have been omitted or assigned narrower sorts. In the proof
definition, the two proof-layer functions do become exhaustive.

For the exact submitted term and documented integer arguments, every reachable
invocation has a covered shape; the constructor mapping above is exhaustive,
both symbolic branches close, all ground executions terminate, and the two
negative mutations are rejected. I therefore do not call any rule unsound:
there is no required intended-domain false-conclusion witness. The narrower
finding is a global declaration/coverage gap outside the fixed program path,
which is why the verdict is `CONCERNS` rather than unqualified `PASS`.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created a fresh mutation at
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k). It keeps
symbolic claim 1’s satisfiable documented precondition but changes its first
result component from `NUMBER + NEED` to
`NUMBER + NEED + 1`. Witness `(5,6,10)` requires `result(12,4)`, while the
program returns `result(11,4)`.

The exact checks were:

```text
kprove spec-vacuity-audit.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run

kprove spec-vacuity-audit.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

The dry run exited 0, establishing successful parsing and claim build. The real
proof exited 1 with `WarnStuckClaimState`. Its residual shows the expected
failed implication:

```text
NUMBER +Int NEED +Int 1 #Equals NUMBER +Int NEED
```

This is the intended unmet result obligation, not a parser error, missing
import, timeout, or unrelated backend failure. Full evidence:
[06-non-vacuity.log](/audit-output/evidence/06-non-vacuity.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Let `P` be the constructor term parsed from trusted-regenerated
`solution.mpy`. Under the audited generated semantics, the successful symbolic
claims establish:

```text
For all K integers number, need, remaining:
  if each is in [0,1000] and need <= remaining,
  run(P,args(number,need,remaining))
    reaches result(number+need, remaining-need).

  if each is in [0,1000] and remaining < need,
  run(P,args(number,need,remaining))
    reaches result(number+remaining, 0).
```

Together the branches cover the complete HumanEval source-contract domain.
The four example claims establish the four corresponding ground instances.
This is a partial-correctness result. Structural inspection and concrete runs
show this finite program terminates, but termination is not needed to
overstate the reachability theorem as a separate total-correctness proof.

### Trust and assumption ledger

| Boundary | Effect on theorem | Evidence and judgment |
|---|---|---|
| K v7.1.293 compiler, Haskell prover/backend, LLVM concrete backend | Foundation for parsing, rewriting, and `#Top` | Campaign-pinned and freshly version-checked. Ordinary accepted toolchain trust. |
| K built-in `Int`, `Bool`, `String`, `Map`, and generated list constructors | Arithmetic, guards, bindings, and AST/value sequences | Standard fixed primitives. Their use is low-level and does not encode the task answer. |
| Trusted `/reference/py2mpy.py` | Python source to constructor-tree bridge | Candidate copy is byte-identical; trusted regeneration is byte-identical to submitted `solution.mpy`; constructor-level claim pinning is exact. Translator implementation is trusted input, not a proof-local oracle. |
| Candidate-generated `semantic.k` correspondence to this Python subset | Meaning of the K theorem as a theorem about `solution.py` | Audited rule by rule, exercised on every used construct, checked on normal/boundary cases, and supported by 31,542 differential inputs. There is no hidden reference semantics in this mode. |
| Proof-local `carrotContract` and `validInput` | Formal domain and destination value | Exhaustive, disjoint/truthful equations; neither replaces execution. Acceptable definitional mathematics. |
| Proof-local `solutionProgram` | Name for the executed body | Mechanically identical AST and body-sensitive. Acceptable definitional abbreviation. |
| Python canonical/runtime differential oracle | Finite source-intent evidence | Supports implementation/semantics alignment only on recorded cases; not used as a universal proof. |
| Over-broad `[total]` declarations | Global reuse/coverage confidence outside the submitted term | Non-fatal concern. Fresh compiler warnings and concrete uncovered shapes are documented; no intended-domain false-conclusion witness exists. |

There is no candidate opaque symbol, externally supplied result oracle,
empirical value substituted into the K proof, unproved helper claim, or
operational bridge. Historical `PROOF.md`/trace claims (there is no candidate
`PROOF.md`) and prior `#Top` output play no role in this conclusion.

### Gate summary

- Clean verification: pass — all positive targets independently exit 0 with
  `#Top`.
- Real-program soundness and non-vacuity: pass on the pinned submitted program.
- Intent adequacy: pass — no domain narrowing; both branches cover all
  documented integers in `0..1000`.
- Reproducibility/evidence: pass.
- Qualification: globally over-broad `[total]` annotations in the generated
  semantics, soundly avoided by the fixed submitted term.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
