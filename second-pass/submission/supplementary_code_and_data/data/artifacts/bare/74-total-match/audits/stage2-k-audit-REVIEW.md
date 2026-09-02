# Independent adversarial review: 74-total-match

The candidate's K commands reconstruct and its claims are non-vacuous, but the
proof is not a legitimate partial-correctness proof of the real generated
Python program over the source-contract domain. The generated semantics models
Python `len` with K's `lengthString`, which counts the UTF-8 bytes of K strings
rather than Python Unicode code points. For the valid input
`lst1 = ["😀"]`, `lst2 = ["ab"]`, both trusted Python implementations return
`lst1` because the totals are 1 and 2; the freshly rebuilt K semantics computes
the totals as 4 and 2 and returns `lst2`. This is a concrete false-conclusion
witness, not merely missing evidence.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. I used only the
paths in `container_paths`, not the host provenance paths. All layout-required
records are present as real regular files, and the candidate, generation trace,
and reference mounts contain no symlinks or unsupported nodes. The optional
`usage.json` is present and was inspected. Historical runtime metrics are not
required for this layout and were not reconstructed.

The complete JSON value of `/audit-campaign-lock.json` equals the
`audit_campaign` block in `/audit-input.json`. Its independently computed
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the launcher's recorded hash. The mounted run, task, result,
invocation, metrics, usage, prompt, last-message, output-log, canonical,
trusted-prompt, and translator file hashes all equal their recorded hashes.

An independent path/type/size/content tree digest of `/candidate` is
`eb87295adaa7db2486927e4602f9fd7484e5f333c9e9c1614e7ba51a465ec5e0`;
it equals both the stage result's `workspace_sha256` and the invocation's
`retained_workspace_sha256`. The corresponding trace-tree digest is
`a5f830d447d0dd1e8871bd4bad585bcc39aaee310a7897706f5a822efddd556e`;
it equals `usage.json`'s `source_trace_sha256`. These pipeline digests use a
different encoding from the additional launcher tree-digest fields in
`audit-input.json`; all individual trace artifacts also match the hashes in
`generation-result.json`.

The candidate's [prompt.py](/candidate/prompt.py) and
[py2mpy.py](/candidate/py2mpy.py) are byte-identical to the trusted mounts. As
required for generated semantics, `/reference/reference-semantics` does not
exist. There is therefore no trusted or hidden reference semantics in this
review.

I parsed every one of the structured trace's 177 JSONL records, including all
32 tool calls and 32 corresponding outputs. The generation transcript and its
reported `#Top` were treated only as untrusted historical claims.

Evidence:

- [launcher manifest and lock](evidence/01-input-manifest.log)
- [record, mount, and source inventory](evidence/02-provenance-records.log)
- [independent hashes and complete structured-trace parse](evidence/04-integrity-and-trace-passed.log)
- [integrity checker](evidence/integrity_check.py)

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for two finite lists of strings, sum the
number of Python characters in each list; return the list with the smaller
total, returning the first list on a tie. The trusted canonical implementation
does this with loops and Python `len`.

The submitted [solution.py](/candidate/solution.py) computes
`sum(map(len, list))` for both arguments and uses a conditional expression with
`<=`. This is equivalent to the canonical algorithm for the full ordinary
Python `list[str]` domain and preserves the first-list tie rule.

I regenerated `solution.mpy` from the scratch copy of `solution.py` using the
trusted `/reference/py2mpy.py`. `cmp` exited 0; both submitted and regenerated
files have SHA-256
`ac960b8284baa46acbba3e4283e333c889d6966fa5437803c59e000ab3e21766`.

The independent differential test imports the trusted canonical entry point
and the generated entry point separately. It covers the five documented
examples, 14 explicit boundary cases, and 4,000 deterministic generated pairs.
The explicit cases cover empty lists and strings, both strict comparison
branches, equal totals with different list shapes, combining and precomposed
Unicode, an astral code point, embedded NUL and control characters, and long
strings. Across 4,019 cases, the branch distribution was 1,973 first-strictly-
smaller, 114 ties, and 1,932 second-strictly-smaller, with zero mismatches and
correct returned-object identity.

Evidence:

- [trusted and submitted sources, plus exact regeneration](evidence/05-source-fidelity.log)
- [differential test](evidence/differential_test.py)
- [differential results](evidence/06-differential-test.log)

Thus the generated Python implementation itself is faithful; the later failure
is in its generated K language model.

## 3. Clean proof reconstruction

All execution occurred in `/tmp/audit-work/candidate`, populated only with
source copies. Candidate `__pycache__` files and any candidate-generated
definitions were not copied or used. `kup` is absent, but the independently
installed `kompile`, `krun`, and `kprove` are available at version v7.1.293,
which is the live-tooling path permitted by `using-kit`.

Fresh builds succeeded:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-concrete-kompiled
EXIT: 0

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
EXIT: 0
```

Fresh `krun` executions agree with Python on empty, ASCII strict-branch, and
ASCII tie cases. They disagree on the astral-Unicode boundary:

```text
K input:      args(pyList(pyStr("😀") :: .StrVals),
                   pyList(pyStr("ab") :: .StrVals))
K result:     pyList(pyStr("ab") :: .StrVals)
Python totals: (1, 2)
Python result: ["😀"]
```

The original `spec.k` run exits 0 and prints `#Top`. I also made a
semantically identical labeled scratch copy and ran all five target claims
separately; every run exits 0 and prints `#Top`. The two character-total claims
emit `WarnTrivialClaim`, accurately indicating that they close by function
unfolding rather than by an independent connection argument.

Evidence:

- [clean build commands and versions](evidence/08-clean-build-passed.log)
- [fresh concrete executions and Python comparisons](evidence/09-concrete-semantics.log)
- [original and per-claim proof runs](evidence/10-positive-claims.log)
- [per-claim runner](evidence/run_positive_claims.sh)

The candidate therefore has a reconstructible proof under its supplied theory.
`#Top` does not validate that theory as Python semantics.

## 4. Adequacy and real-program pinning

The five claims in [spec.k](/candidate/spec.k) mean:

| Claim | Precondition | Postcondition |
|---|---|---|
| character-total base | none | `totalChars(.StrVals)` rewrites to 0 |
| character-total step | any K string `S` and tail `REST` | total is `lengthString(S) + totalChars(REST)` |
| first/non-greater | K total of `LIST1` is `<=` K total of `LIST2` | execution returns `pyList(LIST1)` |
| second/strictly-smaller | K total of `LIST1` is `>` K total of `LIST2` | execution returns `pyList(LIST2)` |
| tie | the K totals are equal | execution returns `pyList(LIST1)` |

Every precondition is satisfiable. Concrete witnesses are respectively
`.StrVals`; `S = "a", REST = .StrVals`; `[]` versus `["a"]`; `["ab"]`
versus `["c"]`; and `["", "ab"]` versus `["a", "b"]`. The fresh K executions,
candidate Python, and canonical Python agree on those witnesses.

The claims do execute the submitted program term. I parsed both trusted-
regenerated `solution.mpy` and `solutionProgram` with the freshly built
definition, expanded macros, emitted JSON KAST, and compared them mechanically.
The files are byte-identical with SHA-256
`0649b584e57fa0fdde4000950e2e7a15d3b351e242047142824197dc72692e52`.
The term includes the same function name, parameters, `Return`, conditional,
comparison, call nesting, builtin names, and branch bodies. There are no loop
or helper-function control-flow claims.

A separate body-sensitivity test swapped the two return branches in the actual
constructor term while retaining the first-list postcondition. The mutation
compiled successfully, and `kprove` exited 1 with `WarnStuckClaimState` on the
satisfiable 0-versus-1 total boundary. This establishes sensitivity to the
executed body, not merely to an external source file.

The result is also genuinely constrained: the fresh false-postcondition test
in stage 6 is rejected. The adequacy failure is narrower and more concrete:
the formal total is not Python's character total for the full string domain.

Evidence:

- [mechanical constructor identity](evidence/11-program-pinning.log)
- [constructor comparison script](evidence/program_pinning.sh)
- [body-sensitivity mutation and expected failure](evidence/12-body-sensitivity.log)
- [body-sensitivity script](evidence/body_sensitivity.sh)

## 5. Rule-by-rule static soundness review

### Syntax, configuration, and attributes

There are no generated helper K files beyond `semantic.k` and
`verification.k`. The local syntax inventory is exhaustive:

| Lines | Declaration group | Review |
|---|---|---|
| `semantic.k:8` | `Program ::= Module(Stmt)` | Exact submitted module form; acceptable. |
| `semantic.k:10` | two-string `Params` | Exact arity used by the target; acceptable minimal coverage. |
| `semantic.k:12-13` | `FuncDef`, `Return` statements | Covers every submitted statement; acceptable. |
| `semantic.k:15-19` | `Name`, unary/binary `Call`, `IfExp`, `Compare` | Covers every submitted expression, with comma arity distinguishing calls; acceptable. |
| `semantic.k:21` | `CmpOp` | Covers the submitted constructor; unsupported operators stop visibly. |
| `semantic.k:31-45` | `PyString`, linked string/int values, `Value`, `Args`, `Env` | Finite list/value encoding adequate for target inputs, except for the string-length bridge below. |
| `semantic.k:49-55` | functions `eval`, `apply1`, `apply2`, `lessEqual`, `ifValue`, `mapLengths`, `sumInts` | All are partial `[function]` symbols. No unjustified `[total]` declaration is present. |
| `semantic.k:94` | `run(Program, Args)` | Explicit invocation wrapper; acceptable for this one module/function. |
| `semantic.k:100` | one `<k>` configuration | Sufficient for this pure target; no hidden state cell is omitted by a rule. |
| `verification.k:7` | `solutionProgram [macro]` | Exact program tree, mechanically checked. |
| `verification.k:21` | `totalChars [function]` | Definitional summary of the candidate evaluator's own `mapLengths`/`sumInts`. |

There are no local `total`, `functional`, `opaque`, `priority`,
`simplification`, `anywhere`, `owise`, `concrete`, `strict`, or `seqstrict`
attributes or rules. The sole macro is `solutionProgram`. The complete
machine-extracted declaration and attribute inventory is in
[14-static-inventory.log](evidence/14-static-inventory.log).

### Operational and equational rules

| ID | Rule | Classification and decision |
|---|---|---|
| R1 | `eval(Name("lst1"), env(V1,_)) => V1` | Sound positional lookup for the exact function binding. |
| R2 | `eval(Name("lst2"), env(_,V2)) => V2` | Sound positional lookup for the exact function binding. |
| R3 | `eval(Name("len"),_) => builtin("len")` | Sound for the submitted module under ordinary, unmodified Python builtin bindings. |
| R4 | `eval(Name("map"),_) => builtin("map")` | Same; acceptable target-specific binding. |
| R5 | `eval(Name("sum"),_) => builtin("sum")` | Same; acceptable target-specific binding. |
| R6 | unary `Call` to `apply1(eval(F),eval(A))` | Sound on the actual pure calls. |
| R7 | binary `Call` to `apply2(eval(F),eval(A),eval(B))` | Sound on the actual pure `map(len,list)` calls. |
| R8 | `Compare(...,"<=",...)` to `lessEqual` | Sound constructor dispatch. |
| R9 | `IfExp` to `ifValue(eval(C),eval(T),eval(E))` | Places both branch evaluation terms beneath `ifValue` instead of representing an explicit Python short-circuit context. Any extra normalization is inert here because both actual branches are total, side-effect-free parameter reads. |
| R10 | `apply1(builtin("len"),pyStr(S)) => pyInt(lengthString(S))` | **Unsound as Python `len` semantics on the intended domain.** Exact false witness below. |
| R11 | `sum(pyInts(IS)) => pyInt(sumInts(IS))` | Sound for the fully consumed mapped integer sequence. |
| R12 | `map(len,pyList(SS)) => pyInts(mapLengths(SS))` | Sound for finite exact strings conditional on a sound `len` bridge; inherits R10's defect. |
| R13 | `mapLengths(.StrVals) => .IntVals` | Sound base equation. |
| R14 | map-lengths cons equation | Structurally descending and sound conditional on R10's length meaning. |
| R15 | `sumInts(.IntVals) => 0` | Sound base equation. |
| R16 | sum-int cons equation | Structurally descending and ordinary integer arithmetic. |
| R17 | `lessEqual(I,J) => true` when `I <= J` | True over K mathematical integers. |
| R18 | `lessEqual(I,J) => true` when `I == J` | Redundant overlap with R17, but the overlap has the same RHS and is consistent. |
| R19 | `lessEqual(I,J) => false` when `I > J` | Disjoint from the true region and completes integer coverage. |
| R20 | `ifValue(true,T,_) => T` | Sound conditional selection. |
| R21 | `ifValue(false,_,E) => E` | Sound conditional selection. |
| R22 | exact `run(Module(FuncDef(...Return(BODY))),args(V1,V2))` to `eval(BODY,env(V1,V2))` | Target-specific operational rule, but it matches the exact binding, parameters, and return context; no module side effects or other cells exist. Acceptable for this program. |
| R23 | `solutionProgram` macro expansion | Definitional, exact, and mechanically connected to the regenerated program. |
| R24 | `totalChars(SS) => sumInts(mapLengths(SS))` | Truthful definition inside the candidate K theory; it does not replace program execution, but it inherits the wrong string metric. |

The source-construct mapping is complete: `Module`/`FuncDef`/`Params`/`Return`
are consumed by R22; `IfExp` by R9/R20/R21; `Compare`/`CmpOp("<=")` by
R8/R17-R19; calls and names by R1-R7; and `len`/`map`/`sum` by R10-R16. Every
material constructor in `solution.mpy` is modeled. Numeric addition and
comparison use unbounded K integers, matching Python integers here. The
functions descend on finite list tails; there is no hidden nontermination
assumption.

The semantics has no heap or object identity, so its returned list is a value
rather than an alias. That is a nonfatal abstraction for the stated
return-value contract and this nonmutating function, but it does not establish
post-return alias observations.

### Required false-conclusion witness for R10

The scratch program that invokes the candidate's own `len` rule on
`pyStr("😀")` returns:

```text
<k> pyInt(4) ~> .K </k>
```

CPython evaluates `len("😀")` to 1. This is recorded in
[13-unicode-len-witness.log](evidence/13-unicode-len-witness.log).

The defect enables a false result theorem on the source domain:

```text
lst1 = ["😀"]       Python total = 1; candidate K total = 4
lst2 = ["ab"]       Python total = 2; candidate K total = 2

Real generated Python and canonical Python: return lst1
Candidate K execution and its "second/strictly-smaller" claim: return lst2
```

The fresh full-program execution is in
[09-concrete-semantics.log](evidence/09-concrete-semantics.log). Therefore R10
is not merely underdocumented or overbroad: when used as the semantic bridge
for a construct the submitted program materially executes, it proves the wrong
branch and result for a valid intended input.

## 6. Fresh non-vacuity test

The candidate supplies no `spec-vacuity.k`. I created a fresh scratch claim
using the unchanged original program and semantics. Under the strict
precondition `totalChars(LIST1) < totalChars(LIST2)`, it deliberately demands
`pyList(LIST2)` instead of `pyList(LIST1)`.

The witness `LIST1 = .StrVals`,
`LIST2 = pyStr("a") :: .StrVals` satisfies the precondition (0 < 1), reaches
the result obligation, and makes the mutation false. `kprove --dry-run` exits 0,
showing that the mutated spec parses and builds. The actual proof exits 1 with
`WarnStuckClaimState`; the residual explicitly contains the unmet equality
between the selected `pyList(LIST1)` and demanded `pyList(LIST2)`. This is an
expected logical rejection, not a parser error, timeout, or unrelated crash.

Evidence:

- [fresh mutation](evidence/spec-vacuity-audit.k)
- [mutation script](evidence/nonvacuity_test.sh)
- [successful dry run and expected stuck proof](evidence/15-nonvacuity-test.log)

The proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting and decision

What the reconstructed reachability proof actually establishes is conditional
on the candidate K theory: for finite `StrVals`, where the "character count" is
K `lengthString`, the exact translated constructor tree returns the first
encoded list when that K metric is no greater and the second when it is
greater. It also establishes the first-list K-metric tie behavior.

Trust and assumption ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `py2mpy.py` translation | program identity | Acceptable and byte-checked; macro expansion is also KAST-identical. |
| K parser, compiler, LLVM/Haskell backends, and reachability prover | all machine results | Ordinary low-level trusted toolchain boundary; version and fresh commands recorded. |
| K unbounded `Int`, `+Int`, and integer comparisons | totals and branch conditions | Acceptable match for this use of Python integers. |
| Exact `run` wrapper and two-slot environment | call/return and argument binding | Acceptable for the exact one-function, side-effect-free module; constructor and body sensitivity were checked. |
| Hardwired ordinary builtin bindings for `len`, `map`, `sum` | all result claims | Acceptable only under normal HumanEval invocation without global monkey-patching. |
| K `lengthString` as Python `len` | all totals and every entry claim | **Illegitimate.** It is result-bearing, disagrees on a valid ground input, and has no bridge-free connection theorem to Python code-point length. |
| Source-level differential test | candidate Python versus canonical Python | Finite evidence only; it supports source fidelity and cannot repair the failed K semantic bridge. |
| Concrete K comparisons | generated semantics versus Python | Finite evidence; crucially, they expose rather than discharge the Unicode bridge failure. |

There are no local opaque symbols or unconstrained result oracles. The formal
claim closes and pins the real constructor tree, and the non-vacuity gate
passes. Nevertheless, Gate A real-program soundness fails at the result-bearing
`len` rule, and Gate B intent adequacy fails because the unqualified
`list[str]` source contract is materially narrowed to strings whose K byte
length happens to equal Python character length. The prompt's decision rule
requires such a material source-domain narrowing to be `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
