# Independent adversarial audit: 35-max-element

## Outcome

The candidate contains a legitimate, freshly reconstructable partial-correctness
proof for the exact submitted `solution.mpy`, under its generated semantics and
for the formal domain of finite, non-empty sequences of mathematical integers.
The proof is result-constraining, body-sensitive, and non-vacuous.

The decision is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
scope and trust reasons:

1. The prompt says “list” and does not explicitly restrict elements to integers,
   while the K theorem covers only non-empty integer sequences. The canonical
   implementation makes an empty input invalid but can also operate on other
   mutually comparable Python values.
2. The submitted Python implementation delegates the substantive operation to
   Python's external `max` builtin. The generated K semantics gives that builtin
   a truthful, exhaustive recursive definition, so this is not an unconstrained
   oracle or a false rule. Nevertheless, the reachability proof is conditional
   on that semantic bridge; it does not prove a universal connection theorem
   about the actual CPython implementation of `max`.

Neither limitation permits a false result for the fixed submitted program on
the stated K input domain.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, exactly as this mode requires.
There is therefore no supplied or hidden reference semantics to compare or use.
This check is recorded in
[`01-provenance-integrity.log`](/audit-output/evidence/01-provenance-integrity.log).
There is no infrastructure contradiction.

### Trusted-input comparison

The candidate prompt and translator are regular files, not symlinks, and are
byte-identical to the trusted mounts:

| Artifact | Trusted SHA-256 | Candidate SHA-256 | Result |
|---|---|---|---|
| `prompt.py` | `75ceb54ce0c4ea472f0613ef75a8b6bc8d5b530e6749df89eff0779faa70a96b` | same | exact |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | same | exact |

The recursive candidate-tree check found no symlinks. The required candidate
sources are present as regular files: `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. The generation
metadata requested by the audit is also present: `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, and one structured JSONL
trace. There are no candidate helper K files beyond `semantic.k`,
`verification.k`, and `spec.k`.

The candidate additionally contains `__pycache__`, `semantic-kompiled`, and
`verification-kompiled`. Those are extra generated products, not trusted source
artifacts. They were neither copied into the clean source set nor used for any
execution or proof.

### Untrusted generation claims

The small metadata files are transcribed in
[`01a-untrusted-metadata-claims.log`](/audit-output/evidence/01a-untrusted-metadata-claims.log).
They claim a bare/generated-semantics run, exit 0, two successful concrete
runs, and `#Top`. Those statements were treated only as claims.

The reviewer script
[`analyze-generation-trace.py`](/audit-output/evidence/analyze-generation-trace.py)
read all 121 JSONL records and all 4,425 lines of `codex-output.log`. Its digest
is in
[`02-generation-claims.log`](/audit-output/evidence/02-generation-claims.log).
The trace records prior build, `krun`, and `kprove` commands, but none of those
prior results is used as proof evidence below.

Stage 1 result: no provenance or mode-integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

[`prompt.py`](/reference/prompt.py:3) requires `max_element(l)` to return the
maximum element in the list and supplies examples returning `3` and `123`.
The trusted
[`canonical.py`](/reference/canonical.py:7) initializes `m = l[0]`, scans the
list, replaces `m` exactly when `e > m`, and returns `m`.

Consequently, the defined-result domain is a non-empty list whose elements
support the required comparisons. Empty input has no maximum and the canonical
implementation raises at `l[0]`. For non-empty Python integer lists, the
contract is simply to return the greatest integer, including for negative,
duplicate, and arbitrary-precision values.

### Submitted implementation and translation

[`solution.py`](/candidate/solution.py:1) is:

```python
def max_element(l: list):
    return max(l)
```

This is a different algorithmic presentation from the canonical loop but has
the same returned value on every non-empty list in the intended comparable
domain.

The trusted translator was run from `/reference/py2mpy.py` against the scratch
copy of `solution.py`. The regenerated file has SHA-256
`b040afa3d90d99cfcc4af2a4d930d009cfbf495e7de3998c1d24d2899e6b8791`,
identical to the submitted `solution.mpy`; `cmp` and `diff` both returned zero.
See
[`03-translator-regeneration.log`](/audit-output/evidence/03-translator-regeneration.log)
and the preserved
[`regenerated-solution.mpy`](/audit-output/evidence/regenerated-solution.mpy).

The exact translated AST is:

```text
Module(
  FuncDef("max_element", Params("l"),
    Return(Call(Name("max"), Name("l")))))
```

### Independent differential testing

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted entry point directly from `/reference/canonical.py` and the
submitted entry point from the isolated scratch copy. The full deterministic
input set is preserved in
[`differential-inputs.json`](/audit-output/evidence/differential-inputs.json).
It contains:

- both documented examples;
- singleton, all-negative, duplicate-maximum, very large integer, and
  maximum-first/middle/last cases;
- strict-greater, strict-less, and equality cases around the canonical branch;
- every list of lengths 1 through 4 over `{-2,-1,0,1,2}`: 780 inputs;
- 500 seeded generated lists of lengths 1 through 64 with elements in
  `[-10^12,10^12]`.

There were 1,292 in-domain comparisons and zero mismatches. The required empty
probe was also run: the canonical implementation raises `IndexError`, while
the submitted builtin-based version raises `ValueError`. This is an exact
exception-type divergence, but not a returned-value divergence on the
defined-result domain. The command, exit 0, and results are in
[`04-differential-python.log`](/audit-output/evidence/04-differential-python.log).

Stage 2 result: byte-exact translation and no material implementation divergence
on non-empty integer inputs. The broader comparable-value domain and exact
empty exception behavior remain outside the K theorem.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/candidate-src`.
No candidate-provided compiled definition, binary, cache, timestamp, or
`allRules.txt` was copied or referenced.

The installed tools report K version `v7.1.293`; see
[`00-toolchain.log`](/audit-output/evidence/00-toolchain.log).

### Fresh builds

| Purpose | Fresh command | Exit | Evidence |
|---|---|---:|---|
| Concrete semantics | `kompile semantic.k --backend llvm --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/semantic-llvm-kompiled` | 0 | [`05-build-concrete-llvm.log`](/audit-output/evidence/05-build-concrete-llvm.log) |
| Proof semantics | `kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/verification-haskell-kompiled` | 0 | [`06-build-proof-haskell.log`](/audit-output/evidence/06-build-proof-haskell.log) |

Both builds were from the copied source and produced new scratch definitions.

### Generated-semantics concrete execution

The fresh LLVM semantics executed the submitted `solution.mpy` on ten
in-domain inputs: both examples, positive and negative singletons, the
greater/less/equal comparison boundaries, maximum-first, maximum-last with all
negative numbers, and arbitrary-precision integers. Every run exited 0,
finished with `<k> .K </k>`, and produced the same integer as both Python
implementations.

The inputs are in
[`k-concrete-inputs.json`](/audit-output/evidence/k-concrete-inputs.json), the
reviewer is
[`k_concrete_compare.py`](/audit-output/evidence/k_concrete_compare.py), and all
commands/configurations are in
[`08-generated-semantics-comparison.log`](/audit-output/evidence/08-generated-semantics-comparison.log).
The minimum in-domain boundary is a singleton. An empty `IntSeq` was rejected
by the parser with exit 113, as the declared non-empty grammar requires.

One earlier reviewer run mis-parsed the pretty-printed result because its
regular expression was over-escaped. That harness failure is preserved in
[`08a-reviewer-harness-regex-failure.log`](/audit-output/evidence/08a-reviewer-harness-regex-failure.log);
the K executions in that log had already exited 0. The corrected harness is the
passing evidence above and did not alter candidate source or semantics.

### Positive proof claims

The unmodified submitted spec was first proved as a whole:

```text
kprove spec.k --definition /tmp/audit-work/verification-haskell-kompiled --spec-module SPEC
#Top
EXIT_STATUS: 0
```

See
[`09-kprove-original-all.log`](/audit-output/evidence/09-kprove-original-all.log).

Because the submitted claims are unlabeled, the reviewer then copied the same
three claim bodies into
[`spec-labelled.k`](/audit-output/evidence/spec-labelled.k), renaming the
container module and adding labels but changing no precondition, execution
term, state rewrite, or postcondition, and selected each target independently:

| Claim | Exit/output | Evidence |
|---|---|---|
| Universal non-empty `IntSeq` claim | 0, `#Top` | [`10-kprove-universal.log`](/audit-output/evidence/10-kprove-universal.log) |
| Prompt example `[1,2,3]` | 0, `#Top` | [`11-kprove-example1.log`](/audit-output/evidence/11-kprove-example1.log) |
| Prompt example ending in maximum `123` | 0, `#Top` | [`12-kprove-example2.log`](/audit-output/evidence/12-kprove-example2.log) |

Stage 3 result: both definitions rebuild cleanly, all positive targets close
independently, and the generated semantics agrees with independent Python
execution on the recorded normal and boundary inputs.

## 4. Adequacy and real-program pinning

### Plain-language claims

There are no explicit `requires` clauses in
[`spec.k`](/candidate/spec.k:8). Sorts and the exact initial cells supply the
preconditions.

1. **Universal entry claim.** For every syntactic `IS:IntSeq`—therefore every
   finite, non-empty sequence of K mathematical integers—start with the exact
   submitted program term followed by
   `invoke("max_element", IS)`, empty function and environment maps, and
   `noResult`. Execution must consume the entire computation, install exactly
   the submitted closure, bind exactly `"l" |-> IS`, and finish with
   `result(expectedMaximum(IS))`.
2. **First example.** The same exact initial state with `[1,2,3]` must finish
   with `result(3)` and the corresponding exact maps.
3. **Second example.** The same exact initial state with
   `[5,3,-5,2,-3,3,9,0,123,1,-10]` must finish with `result(123)` and the
   corresponding exact maps.

The destination does not contain a free result variable, existential result,
tautological `ensures`, or one-way condition. It fixes `<k>`, `<functions>`,
`<env>`, and `<result>` exactly.

### Pinning to the submitted program

The proof-local equation
[`solutionProgram`](/candidate/verification.k:8) expands to the exact AST bytes
shown in the regenerated `solution.mpy`: the module, function name, single
parameter, return, builtin name, and argument name all match. It is then
processed by the normal `Module`, statement, function-definition, invocation,
return, and expression rules. There is no rule in `verification.k` that
rewrites `invoke`, skips the function body, or directly installs a result.

As an additional dynamic check, the submitted AST file and the proof-local
`solutionProgram` term were executed with `[-4,8,8,1]` under the same fresh
proof definition. Their complete final configurations were byte-identical,
including `.K`, closure, environment, and `result(8)`; see
[`14-program-pinning.log`](/audit-output/evidence/14-program-pinning.log).
Parsing the proof-local literal requires `MPY-VERIFICATION`, whereas the public
runtime parser is intentionally `MPY-SYNTAX`; the reviewer parser used for this
check is preserved at
[`parse-verification-program.sh`](/audit-output/evidence/parse-verification-program.sh).
The initial attempt with the default syntax module, and its scanner error
before execution, is preserved separately in
[`14a-proof-alias-default-parser-failure.log`](/audit-output/evidence/14a-proof-alias-default-parser-failure.log).

### Satisfiable entry states and concrete substitution

Every entry precondition has an explicit witness:

| Entry | Satisfying input/state witness | Claimed result |
|---|---|---:|
| Universal | empty maps, `noResult`, exact program, `IS = [-4,8,8,1]` | 8 |
| Example 1 | its written initial configuration, `[1,2,3]` | 3 |
| Example 2 | its written initial configuration, the 11-element example | 123 |

The reviewer ground instance for `[-4,8,8,1]` is preserved in
[`spec-ground-witness.k`](/audit-output/evidence/spec-ground-witness.k). It
proved with `#Top`, exit 0:
[`13-kprove-ground-witness.log`](/audit-output/evidence/13-kprove-ground-witness.log).
Both trusted canonical Python and submitted Python returned `8` on that same
input:
[`15-ground-python-substitution.log`](/audit-output/evidence/15-ground-python-substitution.log).

There are no loop, helper, or circularity claims to match. The real submitted
body has no loop.

Stage 4 result: all entry states are realizable, the result is fixed, and the
proof executes the exact submitted program rather than a substituted body.

## 5. Rule-by-rule static soundness review

The complete numbered local sources and attribute search are preserved in
[`20-static-rule-inventory.log`](/audit-output/evidence/20-static-rule-inventory.log).
There are exactly three local K files and no generated helper K file.

### Local syntax and configuration inventory

[`semantic.k`](/candidate/semantic.k:3) declares:

| Sort/declaration | Productions and role |
|---|---|
| `Program` | `Module(Stmts)` |
| `Stmts` | K-generated list over `Stmt` with empty separator |
| `Stmt` | `FuncDef(String, Params, Stmts)` and `Return(Expr)` |
| `Params` | `Params(Strings)` |
| `Strings` | comma-separated K-generated list of `String` |
| `Expr` | `Name(String)` and `Call(Expr, Exprs)` |
| `Exprs` | comma-separated K-generated list of `Expr` |
| `IntSeq` | brackets around `NonEmptyInts` |
| `NonEmptyInts` | one `Int`, or a head `Int` and recursively non-empty tail |
| `Function` | `closure(Params, Stmts)` |
| `Result` | `noResult` or `result(Int)` |
| `KItem` | `exec`, `invoke`, `eval`, `intVal`, and `doReturn` |
| `Int` functions | `maxInts(IntSeq)` and `imax(Int,Int)`, both `[function,total]` |

The `List{...}` declarations also generate their standard empty and concatenation
constructors, such as `.Stmts`, `.Strings`, and `.Exprs`. There are no
hand-written rules hidden in separate helper files.

The configuration has exactly the state the fixed program needs:

- `<k>` starts with the parsed program and the selected entry invocation;
- `<functions>` stores the loaded function closure;
- `<env>` stores the one local binding;
- `<result>` stores either no result or the returned integer.

No heap, allocation, I/O, exception, or call-stack cell is omitted from a
behavior that this exact one-function, pure program exercises.

### Mathematical function equations

1. **`maxInts([I]) => I`** at
   [`semantic.k:45`](/candidate/semantic.k:45). A singleton's maximum is its
   sole integer.
2. **`maxInts([I, IS]) => imax(I,maxInts([IS]))`** at
   [`semantic.k:46`](/candidate/semantic.k:46). This is the standard head/tail
   maximum recurrence and structurally decreases the non-empty tail.
3. **`imax(I,J) => I requires I >=Int J`** at
   [`semantic.k:48`](/candidate/semantic.k:48).
4. **`imax(I,J) => J requires I <Int J`** at
   [`semantic.k:49`](/candidate/semantic.k:49).

The two `maxInts` shapes cover exactly all `IntSeq` grammar values and do not
overlap. The two `imax` guards are disjoint and exhaustive because K `Int` is
mathematically totally ordered. Their right-hand sides agree with integer
maximum. Recursion descends, so both `[total]` declarations are justified.
There is no opaque value, unconstrained choice, or missing branch.

### Operational rules

5. **Module:** `Module(SS) => exec(SS)` preserves the continuation and begins
   left-to-right module execution.
6. **Empty statement list:** `exec(.Stmts) => .K` consumes exactly an empty
   list.
7. **Non-empty statement list:** `exec(S REST) => S ~> exec(REST)` schedules
   the head before the tail. Rules 6 and 7 are disjoint and exhaustive for
   `Stmts`.
8. **Function definition:** the `FuncDef` rule consumes the statement and
   updates only `<functions>` with the parameter/body closure. The actual body
   has no free variables, so the intentionally minimal closure representation
   is sufficient.
9. **Invocation:** the `invoke` rule requires a matching named closure with
   exactly one parameter, schedules its real body, preserves the function map,
   and replaces `<env>` with the single parameter binding. The actual call is
   top-level, so no caller environment or return frame is required.
10. **Return scheduling:** `Return(E) => eval(E) ~> doReturn` evaluates the
    expression before installing a result.
11. **Name lookup:** `eval(Name(X)) => V` requires `X |-> V` in `<env>` and
    changes no state. This generic rule is not separately reached by the fixed
    body's atomic supported-call rule; if used with an unsupported result
    shape, the semantics stops visibly rather than fabricating a value.
12. **Builtin `max` call:** the rule at
    [`semantic.k:84`](/candidate/semantic.k:84) matches exactly a call of
    literal `"max"` to one named argument and requires that argument's
    environment value to be `IS:IntSeq`. It rewrites only the leading
    expression to `intVal(maxInts(IS))`, preserving every cell and the entire
    continuation. For this exact program, `"max"` is not rebound, `"l"` is
    bound by rule 9, inputs are integers, and non-emptiness excludes Python's
    empty-sequence exception.
13. **Return completion:** `intVal(I) ~> doReturn => .K` writes
    `noResult => result(I)` and preserves the remaining continuation. In the
    real body that remainder is only `exec(.Stmts)`, which rule 6 consumes.

These rules have no priority attributes. Their leading K constructors or
function guards are disjoint, so there is no priority-dependent overlap. State
updates are confined to the cells just enumerated. The concrete traces confirm
the evaluation order:

```text
Module
→ exec(FuncDef)
→ install closure
→ invoke selected closure and bind l
→ exec(Return)
→ eval(Call(max,l))
→ intVal(maxInts(IS)) ~> doReturn
→ result(maxInts(IS)), .K
```

The builtin-call rule is the only result-bearing semantic primitive. It is not
a proof-local bridge over program-defined code: the submitted program really
calls the external Python builtin. Its result is also not opaque—the four
equations above fix every value on the complete formal domain. The rule reads
the actual environment binding, preserves control and all state, and has no
exceptional path for non-empty integer sequences. Thus it is an acceptable
generated-language primitive, conditional on the explicitly recorded Python
builtin bridge, rather than a smuggled unconstrained answer.

### Proof-local declarations and equations

[`verification.k`](/candidate/verification.k:3) adds exactly two declarations:

1. `solutionProgram [function,total]` expands to the exact submitted AST. It is
   nullary, has one equation, terminates immediately, and has no overlap. This
   is a definitional program name, not an operational shortcut.
2. `expectedMaximum(IntSeq) [function,total] => maxInts(IS)` is a total,
   single-equation alias over the complete `IntSeq` domain. It is
   result-bearing, but its value is fixed by the exhaustive mathematical
   equations above.

There are no `[functional]` declarations distinct from `[function]`, no
`[simplification]` or `[concrete]` rules, no priority declarations, no
`[anywhere]` rules, no macros, no opaque symbols, no lemmas, and no ordinary
proof-local operational rewrite.

### Construct coverage and intentionally narrow scope

Every constructor in the submitted AST is mapped:

| Submitted construct | Declaration/rules |
|---|---|
| `Module` | `Program`; rule 5 |
| one-item module/body lists | `Stmts`; rules 6–7 |
| `FuncDef` | `Stmt`; rule 8 |
| `Params("l")` | `Params`/`Strings`; closure match in rule 9 |
| `Return` | `Stmt`; rules 7, 10, and 13 |
| `Call(Name("max"), Name("l"))` | `Expr`/`Exprs`; rule 12 |
| parameter binding `"l"` | `<env>` write in rule 9 and read in rule 12 |
| entry invocation | configuration plus rule 9 |
| non-empty integer argument/result | `IntSeq`, `maxInts`, `imax`, `intVal`, and `<result>` |

This is deliberately not a reusable full Python semantics. For alternate,
unsubmitted ASTs it does not model lexical closure capture, arbitrary calls,
multiple arguments, exceptions, or abrupt return past later body statements.
Those cases are outside the fixed program and formal input domain; unsupported
forms stop rather than silently producing the required answer. The
`GENERATED_SEMANTICS` boundary expressly permits minimal sound coverage of every
construct the submitted program actually uses. These limitations are therefore
an adequacy concern, not an unsoundness finding about the claimed theorem.

As a body-sensitivity check, the reviewer changed only the body argument from
bound `"l"` to unbound `"x"`. The mutated definition built successfully, but
the proof failed at the real residual
`eval(Call(Name("max"),Name("x")))` with `noResult`, rather than continuing to
the claimed maximum. Artifacts:
[`verification-body-mutation.k`](/audit-output/evidence/verification-body-mutation.k),
[`spec-body-mutation.k`](/audit-output/evidence/spec-body-mutation.k),
[`18-build-body-mutation.log`](/audit-output/evidence/18-build-body-mutation.log),
and
[`19-kprove-body-mutation.log`](/audit-output/evidence/19-kprove-body-mutation.log).
This independently shows that the proof does not bypass the submitted body.

No inventoried rule was found to enable a false conclusion for the fixed
submitted program on any non-empty `IntSeq`. Accordingly, this review makes no
material-unsoundness allegation requiring a false-conclusion witness; the
narrower gaps above are stated as scope limitations.

Stage 5 result: the local theory is internally consistent, exhaustive where
declared total, faithful to the real used control flow, and contains no
task-answer oracle or proof-local execution bypass.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted. The reviewer
created a fresh mutation,
[`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k), with the satisfiable
input `[1,2,3]`. It keeps the same real program, maps, and control obligation,
but changes the result-constraining destination from the true `result(3)` to
the false `result(4)`.

First, `kprove --dry-run` parsed and compiled the mutation to KORE and exited 0:
[`16-vacuity-dry-run.log`](/audit-output/evidence/16-vacuity-dry-run.log).
Thus the negative result is not a parser, import, or build failure.

The actual mutated proof then exited 1 with `WarnStuckClaimState`. Its residual
is the completed real configuration:

```text
<k> .K </k>
<env> "l" |-> [1,2,3] </env>
<result> result(3) </result>
```

This does not unify with the mutated `result(4)` destination. The exact command,
status, and residual are in
[`17-vacuity-false-result.log`](/audit-output/evidence/17-vacuity-false-result.log).

Stage 6 result: the proof discriminates a meaningful false returned value for
a reachable satisfying input.

## 7. Proven versus assumed accounting

### Precisely established by the successful K proof

Under the freshly compiled `MPY-SEMANTICS` plus the two truthful definitional
equations in `MPY-VERIFICATION`, the reachability proof establishes:

> For any finite non-empty `IntSeq` of K mathematical integers, starting from
> the exact translated submitted module with empty maps and `noResult`,
> execution loads the exact `max_element` closure, invokes its real
> `return max(l)` body with `l` bound to that sequence, consumes the
> computation, and finishes with `result(maxInts(IS))`.

The two prompt examples are additionally machine-checked ground instances.
This is a partial-correctness statement in the selected model. The recursive
equations also visibly descend on finite syntax, and all concrete runs
terminated, but the audit does not enlarge the requested result into a
universal theorem about CPython termination.

### Trust and assumption ledger

| Boundary | Effect/dependents | Assessment and evidence |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, and prover | All parsing, execution, and proof closure | Standard toolchain trust boundary; rebuilt independently and commands/statuses are preserved. |
| Imported `domains.md`: K `Int`, `String`, `Map`, list machinery, and `~>` sequencing | Integer order, map lookup/update, configuration execution | Acceptable low-level K primitives. No candidate redefinition or proof-local axiom alters them. |
| Trusted `py2mpy.py` | Connects `solution.py` to the AST proved | Byte identity is established. The translator itself is a trusted mounted input, and the simple resulting AST was independently inspected. |
| `solutionProgram` equation | Connects proof term to submitted `solution.mpy` | Exact definitional expansion; static AST equality, translator regeneration, and identical final configurations support the connection. |
| Python builtin `max` semantic rule | Determines the program's returned value | External fixed primitive, not program-defined code. Complete recursive equations fix its value. Ten fresh K/Python comparisons support the bridge, but do not universally prove CPython equivalence. |
| Mathematical reading of `maxInts` | Connects the formal returned recurrence to the phrase “maximum element” | Base/recursive and two ordered-choice equations are ordinary mathematics and exhaustive. No separate K theorem states member-and-upper-bound axioms, so the natural-language bridge remains an explicit informal derivation. |
| Canonical-versus-submitted Python differential evidence | Supports implementation-to-reference fidelity | Zero mismatches on 1,292 recorded non-empty integer inputs. Finite evidence only; it is not substituted for the K proof. |
| Domain interpretation | Determines theorem scope | Non-empty is justified by the absence of a maximum and canonical `l[0]`. Integer-only is consistent with all examples but not explicit in `prompt.py`; broader comparable Python values are excluded from the formal theorem. |

There are no opaque symbols, fresh result variables, empirical-only equations,
unproved loop invariants, proof-local simplifications, or hidden helper claims.

### Gate summary and decision rationale

- **Real-program soundness:** passes. Exact program identity, exact body
  execution, state/control fidelity, exhaustive result equations,
  body-sensitivity, and false-result rejection are all evidenced.
- **Intent adequacy:** legitimate but limited. On non-empty integer lists, the
  recursive formal result is the requested maximum. The theorem does not cover
  every Python value that might satisfy the prompt's unparameterized `list`
  annotation, nor exact empty-input exception behavior.
- **Trust and auditability:** passes with a documented primitive bridge. All
  reviewer artifacts, deterministic inputs, exact commands, statuses, and
  relevant bounded outputs are under `/audit-output/evidence`. The finite tests
  are described only as empirical support.

The limitations narrow what has been proved; they do not make a false claim
provable, leave the result unconstrained, or detach the proof from the submitted
program. They therefore warrant concerns while preserving legitimacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
