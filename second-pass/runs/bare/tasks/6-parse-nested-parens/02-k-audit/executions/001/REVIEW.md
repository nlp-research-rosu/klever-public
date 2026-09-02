# Independent adversarial audit: 6-parse-nested-parens

The candidate cleanly proves three concrete executions of its submitted
program, but it does not prove the task's general partial-correctness contract.
Worse, the submitted Python program is observably different from the trusted
canonical program on empty split fields. The generated K semantics faithfully
reproduces that implementation bug. This is therefore not a legitimate proof
of the requested task.

All candidate prose, traces, compiled definitions, and caches were treated as
untrusted. Every executable source used below was copied to
`/tmp/audit-work/6-parse-nested-parens`; candidate-provided kompiled
definitions were never used.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, including as a symlink, as required.
There is no infrastructure contradiction. The installed tools are K
v7.1.293 (`kompile`, `krun`, and `kprove` all resolve under `/usr/bin`).
The exact checks and versions are in
[`00_environment.log`](evidence/00_environment.log).

### Artifacts and types

The candidate has regular-file copies of every generation deliverable:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. It also has the requested provenance artifacts
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and one
structured JSONL trace. No entry anywhere under `/candidate` is a symlink.
The full type/size inventory is
[`01_artifact_inventory.log`](evidence/01_artifact_inventory.log).

The candidate also contains extra, non-source material:

- candidate-built `semantic-kompiled/` and `verification-kompiled/`;
- `__pycache__/`;
- the optional negative probe `mutation-spec.k`;
- generation logs and trace data.

The compiled directories and cache were deliberately excluded from the
scratch reconstruction. No `PROOF.md` is present; it was not a required
generation deliverable and its absence is not itself an integrity failure.

### Trusted prompt and translator

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
SHA-256 values are respectively
`39b4ae7cbb22820ff04ffe8a3cbe4bd4332d16046130335d78f36d75a5c3cf4c`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
See [`03_provenance_compare.log`](evidence/03_provenance_compare.log).

`run-input.json` claims the bare/generated-semantics condition and the same two
hashes. `metrics.json` claims generation exit 0. `codex-last.txt`,
`codex-output.log`, and the trace claim that all three positive claims produced
`#Top` and that a candidate-authored mutation failed. These are claims only.
The source/prose extraction is in
[`04_source_listing.log`](evidence/04_source_listing.log) and
[`05_generation_claims.log`](evidence/05_generation_claims.log). The entire
248-record structured trace parses as JSON with no malformed record; its
untrusted proof claims are summarized by the reviewer-authored
[`trace_summary.py`](evidence/trace_summary.py) and
[`05a_structured_trace_summary.log`](evidence/05a_structured_trace_summary.log).

Stage 1 result: provenance and mode integrity pass. Extra compiled/cache
artifacts were present but isolated and ignored.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py` and `/reference/canonical.py`, the entry point
accepts a string containing space-separated groups of nested parentheses and
returns, for every nonempty group, its maximum nesting depth. The canonical
implementation makes the empty-field behavior explicit:

`[parse_paren_group(x) for x in paren_string.split(' ') if x]`.

Thus empty fields caused by the empty string, repeated spaces, or
leading/trailing spaces do not contribute output elements.

### Submitted implementation

`/candidate/solution.py:5-17` computes the right maximum for every nonempty
group, using `depth` and `maximum`. Its outer loop, however, appends one result
for every value returned by `paren_string.split(" ")` without `if group`.
An empty group executes zero inner iterations and contributes `0`.

The submitted `solution.mpy` is not stale or substituted. Regeneration with
the trusted translator produced a byte-identical file with SHA-256
`4cc43e4ecb2ef1adeb7d7014acb39c8811a7a42a77a48b44ea96974e66ae43e7`.
The exact command and `cmp` result are in
[`06_translation_identity.log`](evidence/06_translation_identity.log).

### Independent differential

The reviewer-authored
[`differential.py`](evidence/differential.py) imports the trusted canonical
entry point and the copied candidate entry point by absolute scratch paths. It
tests:

- the documented example;
- empty, one-space, two-space, leading-space, trailing-space, and repeated
  separator boundaries;
- every balanced parenthesis group through four pairs;
- all ordered pairs of those generated groups;
- representative generated pairs with repeated separators.

All 621 inputs and both results are preserved in
[`07_differential.log`](evidence/07_differential.log). The script exited 1
after reporting 112 mismatches. Representative concrete witnesses are:

| Input | Trusted canonical | Candidate |
|---|---:|---:|
| `""` | `[]` | `[0]` |
| `" "` | `[]` | `[0, 0]` |
| `"()  ()"` | `[1, 1]` | `[1, 0, 1]` |
| `" ()"` | `[1]` | `[0, 1]` |
| `"() "` | `[1]` | `[1, 0]` |

The nonempty, single-separated generated cases agree. The documented example
also agrees. The mismatch is nevertheless material: the trusted canonical
defines empty-field behavior, and the audit explicitly requires empty and
boundary cases.

Stage 2 result: **fail**. The real generated program is not faithful to the
trusted task on empty split fields.

## 3. Clean proof reconstruction

### Fresh generated-semantics build and concrete execution

Only copied source files were present in the build directory before
kompilation. The generated semantics compiled from `semantic.k` with the LLVM
backend:

```text
kompile semantic.k --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition audit-semantic-kompiled
```

It exited 0; see
[`08_build_semantics_llvm.log`](evidence/08_build_semantics_llvm.log).

Five concrete runs then terminated at `.K` with these result cells:

| Input | Fresh K result | Candidate Python | Canonical Python |
|---|---:|---:|---:|
| `"(()()) ((())) () ((())()())"` | `[2,3,1,3]` | `[2,3,1,3]` | `[2,3,1,3]` |
| `""` | `[0]` | `[0]` | `[]` |
| `"()"` | `[1]` | `[1]` | `[1]` |
| `"()  ()"` | `[1,0,1]` | `[1,0,1]` | `[1,1]` |
| `" (()) "` | `[0,2,0]` | `[0,2,0]` | `[2]` |

The successful K outputs are
[`09a_krun_example_corrected.log`](evidence/09a_krun_example_corrected.log),
[`10a_krun_empty_corrected.log`](evidence/10a_krun_empty_corrected.log),
[`11a_krun_single_corrected.log`](evidence/11a_krun_single_corrected.log),
[`12a_krun_double_separator_corrected.log`](evidence/12a_krun_double_separator_corrected.log),
and
[`13a_krun_leading_trailing_corrected.log`](evidence/13a_krun_leading_trailing_corrected.log).
The Python comparisons appear in the complete differential log.

For transparency, the reviewer first passed `-cINPUT` and its value as two
arguments, which this `krun` version rejects. Those five usage errors are
preserved in logs `09_krun_example.log` through
`13_krun_leading_trailing.log`. The corrected one-argument
`-cINPUT=...` commands above are the executions used for the audit. This was a
reviewer invocation error, not an infrastructure or candidate failure.

The concrete evidence shows that the generated semantics models the submitted
implementation's empty-field behavior; it does not repair or conceal it.

### Fresh proof build and positive claims

The proof definition compiled from copied `verification.k` and `semantic.k`
with the Haskell backend:

```text
kompile verification.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION --backend haskell \
  --output-definition audit-verification-kompiled
```

The command exited 0; see
[`14_build_verification_haskell.log`](evidence/14_build_verification_haskell.log).

The original three-claim module produced `#Top` and exit 0 in
[`15_kprove_all_original.log`](evidence/15_kprove_all_original.log).
Because the candidate left the claims unlabeled, the reviewer also copied each
claim unchanged into a separate module and ran it independently:

| Claim | Reviewer artifact | Result |
|---|---|---|
| 1 | [`audit-spec-claim-1.k`](evidence/audit-spec-claim-1.k) | `#Top`, exit 0 in [`16_kprove_claim_1.log`](evidence/16_kprove_claim_1.log) |
| 2 | [`audit-spec-claim-2.k`](evidence/audit-spec-claim-2.k) | `#Top`, exit 0 in [`17_kprove_claim_2.log`](evidence/17_kprove_claim_2.log) |
| 3 | [`audit-spec-claim-3.k`](evidence/audit-spec-claim-3.k) | `#Top`, exit 0 in [`18_kprove_claim_3.log`](evidence/18_kprove_claim_3.log) |

Stage 3 result: the clean build and all submitted positive claims pass. This
establishes only that those particular claims close under the candidate
semantics; it does not cure the Stage 2 fidelity failure or the adequacy defect
below.

## 4. Adequacy and real-program pinning

### Plain-language claims

There are no symbolic inputs and no `requires` or `ensures` clauses. Each
claim's precondition is the fully concrete initial configuration:
`<k>` contains `solutionProgram`, `<input>` contains one literal string,
`<env>` and `<functions>` are empty, and `<result>` is `noResult`.

| Claim | Concrete precondition input | Postcondition |
|---|---|---|
| 1 | `"(()()) ((())) () ((())()())"` | computation is `.K`, environment/function maps are empty, result is exactly `[2,3,1,3]` |
| 2 | `"() (()) ((())) (((())))"` | computation is `.K`, maps are empty, result is exactly `[1,2,3,4]` |
| 3 | `"(()(())((())))"` | computation is `.K`, maps are empty, result is exactly `[4]` |

These preconditions are satisfiable: they are ordinary initial configurations
created by the candidate configuration with the shown `$PGM` and `$INPUT`.
The reviewer substituted all three ground inputs into both Python
implementations. Both implementations equal the claimed list on every one.
The script and output are
[`claim_adequacy.py`](evidence/claim_adequacy.py) and
[`19_claim_adequacy.log`](evidence/19_claim_adequacy.log).

### Real-program pinning

`verification.k` has one proof-facing constant, `solutionProgram`, whose only
equation expands to a full `Module(...)` constructor tree. It does not return a
task answer or bypass execution.

The reviewer transcribed that equation's RHS into concrete MPY surface syntax,
parsed both it and the submitted `solution.mpy` with the fresh proof
definition, and compared normalized KAST JSON. Both KAST files have SHA-256
`cf651ba5454f0216f0a3b475ff5a55c4e7b6de69b046d31f83e6a6718429274e`
and are byte-identical. Evidence:
[`verification-rhs.mpy`](evidence/verification-rhs.mpy),
[`submitted-program.kast.json`](evidence/submitted-program.kast.json),
[`verification-rhs.kast.json`](evidence/verification-rhs.kast.json), and
[`22a_program_tree_identity_corrected.log`](evidence/22a_program_tree_identity_corrected.log).
An initial attempt used internal `.Exprs`/`.Stmts` notation in a program file;
the parser rejected it. That failed attempt is preserved in
`21_kast_verification_rhs.log`; the corrected surface spelling parsed and is
recorded in
[`21a_kast_verification_rhs_corrected.log`](evidence/21a_kast_verification_rhs_corrected.log).

There are no helper or loop claims. Both nested `For` constructs are the actual
translated control flow and are concretely unrolled for the three literal
inputs. The exact result constructor in every destination constrains the return
value; there is no fresh or free result variable, tautological implication, or
one-way summary.

### Material adequacy gap

The result is constrained, but the theorem is only three test cases. It says
nothing about an arbitrary input string, no claim relates output positions to
nonempty groups, and no invariant or universal summary states the maximum-depth
property. In particular, none of the claims reaches the empty-field inputs that
falsify fidelity. Three ground executions are not a partial-correctness proof
of the universally stated function contract.

Stage 4 result: real-program pinning and non-vacuous result constraint pass for
the three ground claims; task-level adequacy fails materially.

## 5. Rule-by-rule static soundness review

The authoritative local declaration extraction is
[`23_static_declaration_inventory.log`](evidence/23_static_declaration_inventory.log).
There are 42 rules in `semantic.k`, one rule in `verification.k`, and three
claims in `spec.k`. There are no helper K files. No local declaration uses
`total`, `functional`, `simplification`, `concrete`, `owise`, priority, or an
opaque attribute. The word “macro” occurs only in a comment; `solutionProgram`
is a normal K function.

### Local syntax and configuration inventory

| Declaration | Productions / role | Review |
|---|---|---|
| `Program` | `Module(Stmts)` | Exact outer constructor emitted by the translator. |
| `Stmts` | separator-free `List{Stmt,""}` | Represents translator statement sequences, including empty sequences. |
| `Strs` | comma-separated strings | Used by `Params` and `ImportFrom`. |
| `Exprs` | comma-separated expressions | Used by empty `ListExpr` and call arguments. |
| `CmpOps` | comma-separated comparison operations | Actual program uses one operation per comparison. |
| `Params` | `Params(Strs)` | Actual function has one parameter. |
| `Stmt` | `ImportFrom`, `FuncDef`, `Assign`, `AugAssign`, `For`, `If`, `Expr`, `Return` | Enumerates every statement constructor in `solution.mpy`; no used statement is missing. |
| `Expr` | `Name`, `Int`, `Str`, `ListExpr`, `Attribute`, `Call`, `Compare` | Enumerates every expression constructor in `solution.mpy`; evaluation is deliberately pattern-specific. |
| `CmpOp` | `CmpOp(String,Expr)` | Covers `==` and `>` instances in the program. |
| `PyVal` | `pyInt`, `pyStr`, `pyBool`, `pyList` | Sufficient runtime value universe for this program. |
| `PyVals` | empty or head/tail list | Immutable value representation; sound here because the program has no observable list alias. |
| `Result` | `noResult` or `result(PyVal)` | Explicit return cell. |
| `Function` | `function(Params,Stmts)` | Stores the translated entry body. |
| `KItem` extensions | `start`, `invoke`, `forValues`, `choose` | Internal control items; each has operational rules below. |
| Configuration | `<k>`, `<input>`, `<env>`, `<functions>`, `<result>` under `<mpy>` | Every cell is read or written. No heap, stack, output, or exception cell is needed by the actual program and intended valid-string domain. |
| `eval` `[function]` | expression plus environment | Seven partial equations; every expression shape used as an rvalue is covered. |
| `lookupPy` `[function]` | name plus environment | One map-membership equation; all actual lookups are bound. |
| `stringOf` `[function]` | `pyStr` projection | Used only after evaluating the string parameter. |
| `truth` `[function]` | `pyBool` projection | Unused; truthful where defined. |
| `eqPy` `[function]` | string and integer equality | String case used; both equations are truthful and disjoint by constructor. |
| `gtPy` `[function]` | integer greater-than | Used for `depth > maximum`. |
| `addPy`, `subPy` `[function]` | integer arithmetic | Used by the two augmented assignments. |
| `appendPy` `[function]` | append to `pyList` | Used only for `result.append(maximum)`. |
| `appendVals` `[function]` | recursive list append | Two disjoint, structurally decreasing equations. |
| `iterable` `[function]` | list or string elements | Both cases used: groups list and characters string. |
| `chars` `[function]` | string-to-character values | Empty and positive-length cases are disjoint and cover K strings. |
| `splitSpaces` `[function]` | explicit ASCII-space split | Two disjoint cases based on `findString`; recursion consumes through the found space. |
| `solutionProgram` `[function]` | constant program tree | Its only equation is KAST-identical to submitted `solution.mpy`; it carries no answer. |

All function declarations are intentionally partial outside their modeled
construct/type combinations. Because none is declared `total`, an unsupported
combination becomes stuck rather than an unconstrained oracle. Minimal coverage
is acceptable in generated-semantics mode, and every actual call falls in a
covered equation.

### Exhaustive semantic and verification rule inventory

The following table decides every local rule. “Used-scope valid” means the rule
matches actual control flow and agrees with Python on the submitted program and
the intended valid parenthesis-string domain. It does not claim a reusable
semantics for arbitrary Python programs.

| ID / source line | Rule effect | Decision |
|---|---|---|
| S1 `semantic.k:68` | `Module(SS)` schedules statements then `start`. | Used-scope valid; module declarations run before entry invocation. |
| S2 `:69` | Nonempty `Stmts` schedules head then tail. | Valid left-to-right statement order. |
| S3 `:70` | Empty `Stmts` becomes `.K`. | Valid sequence base case. |
| S4 `:72` | Ignores `ImportFrom`. | Valid for actual `from typing import List`, which has no runtime influence on this body. Over-broad for arbitrary imports, but no false conclusion arises on the submitted program/domain. |
| S5 `:73-74` | Registers `FuncDef` in `<functions>`. | Used-scope valid; preserves exact parameters/body and updates the only function binding. |
| S6 `:76-77` | `start` invokes the named entry on input as `pyStr`. | Valid entry-point bridge fixed by the task and configuration. |
| S7 `:79-81` | Looks up one-parameter function, replaces environment with parameter binding, executes body. | Valid for the sole top-level entry invocation; no caller locals or nested calls exist. Partial outside this scope rather than result-fabricating. |
| S8 `:84-85` | Assignment evaluates in old environment then updates binding. | Valid; all actual rvalues are pure under this model. |
| S9 `:87-88` | Integer `+=`. | Valid for bound `pyInt depth` and literal 1. |
| S10 `:90-91` | Integer `-=`. | Valid for bound `pyInt depth` and literal 1. |
| S11 `:93-94` | Evaluates `If` condition and creates `choose`. | Valid evaluation before branch; actual condition evaluation is pure. |
| S12 `:95` | `choose(true)` schedules then-branch. | Valid and disjoint from S13. |
| S13 `:96` | `choose(false)` schedules else-branch. | Valid and disjoint from S12. |
| S14 `:98-99` | Evaluates `For` iterable once and creates `forValues`. | Matches Python's one-time iterable evaluation for the pure actual expressions. |
| S15 `:100` | Empty `forValues` terminates the loop. | Valid zero-iteration boundary. |
| S16 `:101-102` | Binds next value, runs body, then remaining values. | Valid iteration order and loop-variable update. |
| S17 `:104-105` | Models `X.append(E)` by rebinding `X` to a list with the value appended. | Used-scope valid because `result` has no alias and `E` is pure; no general claim about Python aliasing is made. |
| S18 `:107-110` | Top-level return evaluates value, terminates continuation, clears local/function maps, and sets result. | Valid for the actual entry return, which is the final function statement and has no caller. The pattern is too broad for nested-call Python, but that construct is unused; no false intended-domain witness exists, so this is a scope limitation rather than a labeled unsound rule. |
| S19 `:115` | `lookupPy` returns the value at matching map key. | True Map lookup equation on all matches. |
| S20 `:117` | `eval(Int(I)) = pyInt(I)`. | True constructor interpretation. |
| S21 `:118` | `eval(Str(S)) = pyStr(S)`. | True constructor interpretation. |
| S22 `:119` | `eval(Name(X),ENV)` delegates to lookup. | Valid for all bound names used by the program. |
| S23 `:120` | Empty `ListExpr` evaluates to empty `pyList`. | Exact actual list literal; nonempty literals are deliberately unmodeled. |
| S24 `:121-122` | Explicit `" "` split evaluates through `splitSpaces`. | Matches submitted source's `str.split(" ")`; concrete boundary runs confirm preservation of empty fields. |
| S25 `:123-124` | `==` comparison delegates to `eqPy`. | Valid for actual string operands. |
| S26 `:125-126` | `>` comparison delegates to `gtPy`. | Valid for actual integer operands. |
| S27 `:129` | Projects K string from `pyStr`. | True constructor equation. |
| S28 `:132` | Projects K boolean from `pyBool`. | True but unused. |
| S29 `:135` | String equality maps to `==String`. | Ordinary equality, truthful. |
| S30 `:136` | Integer equality maps to `==Int`. | Ordinary equality, truthful; unused by the program. |
| S31 `:139` | Integer greater-than maps to `>Int`. | Ordinary integer order, truthful. |
| S32 `:142` | `addPy` maps to unbounded K integer addition. | Truthful for Python integers on this domain. |
| S33 `:145` | `subPy` maps to unbounded K integer subtraction. | Truthful for Python integers on this domain. |
| S34 `:148` | `appendPy` delegates to value-list append. | Truthful immutable representation of the no-alias actual append. |
| S35 `:151` | Append to empty list produces singleton. | True list base equation. |
| S36 `:152` | Append through a head recurses on tail. | True list equation; structurally decreasing. |
| S37 `:155` | A `pyList` iterates as its values. | True for the modeled immutable list. |
| S38 `:156` | A `pyStr` iterates via `chars`. | True for intended ASCII parentheses/spaces. |
| S39 `:159` | `chars("")` is empty. | True base equation. |
| S40 `:160-162` | Positive-length string yields first character plus recursion on suffix. | True for intended ASCII strings; guard excludes overlap with S39 and length decreases by one. |
| S41 `:166-167` | No-space string splits to one field, including `""`. | Exactly Python explicit-separator behavior; guard is disjoint from S42. |
| S42 `:168-172` | Found-space string emits prefix and recurses after that space. | Exactly Python explicit-separator behavior; suffix is shorter and guard is disjoint from S41. |
| V1 `verification.k:10-29` | `solutionProgram` rewrites to the translated program tree. | Definitional summary only; normalized KAST identity proves it neither substitutes nor changes the program. |

### Used-construct coverage and control/state review

Every constructor in `solution.mpy` maps to both a declaration and the
following behavior:

| Submitted construct | Rules |
|---|---|
| `Module`, statement lists | S1-S3 |
| `ImportFrom`, `FuncDef`, entry invocation | S4-S7 |
| `Assign`, empty `ListExpr`, names/literals | S8, S19-S24 |
| outer and inner `For` | S14-S16, S37-S40 |
| `If`, `==`, `>` | S11-S13, S25-S31 |
| `AugAssign +` / `-` | S9-S10, S32-S33 |
| `result.append(maximum)` | S17, S34-S36 |
| `Return` | S18 |

Statements and loop elements execute left-to-right. Assignment and augmented
assignment evaluate against the old environment before update. The loop
variable is rebound before each body. The only modeled mutation, list append,
is represented as rebinding; this preserves the actual program because no
alias observes the old list. Calls are limited to the configured entry,
`split(" ")`, and `append`; all are covered. There is no allocation identity,
exception, output, or external state used by this program. K integers avoid
overflow just as Python integers do.

The generated semantics is not a general Python semantics: arbitrary imports,
nonempty list literals, aliases, nested calls/returns, exceptions, and many
types are outside it. Under `GENERATED_SEMANTICS`, those unused omissions are
not defects. The broad S4 and S18 rules would be concerning for reuse, but
there is no concrete or symbolic witness on this submitted program's intended
input domain that makes either produce a false conclusion. Accordingly, this
review does **not** label a local K rule unsound. The witnessed false task
conclusion instead comes from `solution.py` omitting the canonical empty-field
filter and from `spec.k` failing to state the general contract.

Stage 5 result: the local K rules are sound for the actual three executions and
the used program path. They do not encode the answer, introduce an oracle,
bypass the body, or fabricate an unmodeled used construct. Static soundness
does not compensate for the source fidelity and theorem adequacy failures.

## 6. Fresh non-vacuity test

The candidate's `mutation-spec.k` was inspected only as untrusted evidence and
was not reused.

The reviewer created
[`audit-vacuity.k`](evidence/audit-vacuity.k), starting from the second
positive claim and changing only the result-bearing second element from the
true `2` to `9`. The exact initial state is satisfiable, and both Python
implementations return `[1,2,3,4]` on that input.

First, `kprove --dry-run` parsed and built the mutation successfully with exit
0; see [`24_vacuity_dry_run.log`](evidence/24_vacuity_dry_run.log). The real
proof then exited 1 with `WarnStuckClaimState`. Its residual is a fully
terminated `.K` configuration containing `[1,2,3,4]`, which does not unify with
the mutated destination `[1,9,3,4]`. See
[`25_vacuity_proof_expected_failure.log`](evidence/25_vacuity_proof_expected_failure.log).

This is a meaningful unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash.

Stage 6 result: pass. The three ground claims discriminate their exact results.

## 7. Proven versus assumed accounting

### What is actually proven

Conditional on the candidate-generated semantics and the trusted K runtime,
the successful reachability proofs establish:

1. Starting from the exact submitted program tree, literal input
   `"(()()) ((())) () ((())()())"`, empty maps, and `noResult`, execution
   terminates at `.K` with result `[2,3,1,3]`.
2. The analogous execution on `"() (()) ((())) (((())))"` terminates with
   `[1,2,3,4]`.
3. The analogous execution on `"(()(())((())))"` terminates with `[4]`.

They also establish the explicitly claimed clearing of `<env>` and
`<functions>` on those paths. Because the inputs are ground, this proof is
essentially machine-checked execution of three examples. It establishes no
universal relationship between input groups and returned maxima.

### Trust and assumption ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell prover, LLVM executor, and reachability logic | All K build/run/proof results | Ordinary unavoidable toolchain trust boundary; rebuilt independently and outputs preserved. |
| Imported K `INT`, `STRING`, `BOOL`, and `MAP` primitives, including `+Int`, `-Int`, comparisons, `lengthString`, `substrString`, `findString`, map lookup/update, and K sequencing | S2-S3, S8-S17, S19-S42 | Acceptable low-level primitive boundary. None states the task answer. |
| Trusted `/reference/py2mpy.py` as the Python-AST-to-MPY bridge | Identity of source and submitted program | The submitted MPY is byte-identical to fresh trusted translation. This proves translation identity, while the translator itself remains a trusted mounted component. |
| Candidate `semantic.k` as a model of the used Python subset | Meaning of all three K executions | Audited rule by rule. Five concrete normal/boundary runs agree with candidate Python, including its bug. There is no universal mechanized CPython-equivalence theorem; the bridge is informal plus finite evidence. This limitation is not what causes the verdict because the source-level counterexamples are direct. |
| `solutionProgram` constant | All three claims | Acceptable definitional summary: its normalized KAST is identical to the submitted program, and the body executes under ordinary semantics. |
| Candidate-Python to trusted task intent/canonical behavior | Claim that the task was implemented correctly | Illegitimate as a correctness bridge: 112/621 independent cases diverge, with `""` giving `[0]` instead of `[]`. |
| Three ground claims as evidence for a universal function contract | Claim that the task was proved correct | Illegitimate substitution of examples for the required general theorem. No symbolic input, invariant, or universal postcondition exists. |

There are no local opaque symbols, result-bearing oracles, proof-local
simplifications, assumed lemmas, operational proof bridges, or circular
summaries. Differential testing is used only to assess the Python/canonical and
K/Python bridges; it is not treated as a substitute for a K theorem.

### Decision

The reconstructed K executions are honest and non-vacuous for their three
literal inputs, and they pin the actual translated body. Nonetheless, the
candidate does not contain a partial-correctness proof of the task contract:
the formal theorem consists only of three examples, and the real submitted
program is false against the trusted canonical contract on empty split fields.
These are material fidelity and adequacy failures, not thin evidence or an
infrastructure uncertainty. Under the required decision boundary, the result
is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
