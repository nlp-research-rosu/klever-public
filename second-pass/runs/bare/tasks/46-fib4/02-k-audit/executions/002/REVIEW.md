# Independent adversarial review: 46-fib4

The candidate is a legitimate but imperfect partial-correctness proof for the
natural, nonnegative index domain of the Fib4 sequence. Fresh reconstruction
closed every submitted claim, the program term is pinned to the trusted
translation, the semantics executes the real loop, and a false result mutation
is rejected. I assign `CONCERNS / LEGIT` rather than `PASS / LEGIT` because the
unbounded entry theorem is represented by two separately checked reachability
claims whose composition is not itself closed by one `kprove` invocation, the
rolling-summary-to-recurrence bridge is an ordinary mathematical induction
rather than a separate K theorem, and several `[total]` annotations overclaim
coverage outside the program's used subset.

## 1. Input and provenance integrity

The launcher declares:

- problem `46-fib4`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the required invocation and metrics
records, `usage.json`, both Codex text logs, `prompt.txt`, and all 336 JSONL
records in the structured trace. The trace has one regular JSONL file and all
336 lines parse as JSON. The generation claims and old `#Top` results were not
used as proof evidence.

The campaign-lock JSON is exactly equal to the `audit_campaign` object, and its
SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every layout-required mount and record is a real regular file or real directory;
there are no symlinked candidate, reference, or trace entries. All recorded
individual file hashes match. In particular:

- the candidate and trusted prompt are byte-identical;
- the candidate and trusted translator are byte-identical;
- the canonical, prompt, translator, run, task, result, invocation, metrics,
  usage, generation prompt, Codex logs, and trace-file digests all match their
  recorded values;
- recomputing the pipeline tree digest of `/candidate` gives
  `6a7e54aceb2cf83162b9564f3fab9bcb76a4ddfa7c6a15655fa9042ecba0b06c`,
  exactly the workspace digest in both the invocation and stage-1 result;
- recomputing the pipeline tree digest of the trace gives
  `43ecfc0b9fd2fe39065eeaed6979250a53f419c3996de11db902ee2827f8ab78`,
  exactly `usage.json`'s source-trace digest.

The aggregate `candidate_tree_sha256` and
`generation_codex_trace_sha256` values in `/audit-input.json` are respectively
`a42c...` and `28dd...`, not the values produced by the pipeline-v3
name/kind/size/bytes tree-digest algorithm. The audit record does not declare
the algorithm for those two aggregate fields. This is a provenance-format
limitation, not an absent or unreadable mount: file-by-file hashes and the
layout-native workspace/trace hashes independently pin the mounted content.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist, and neither does a candidate
`reference-semantics` tree. I therefore audited the candidate's `semantic.k` on
its own merits and did not infer a hidden baseline.

Evidence:

- `evidence/provenance_check.py`
- `evidence/stage1-provenance.log`
- `evidence/extract_generation_trace.py`
- `evidence/stage1-generation-trace-extract.log`

Stage result: PASS, with the documented aggregate-digest convention limitation.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt defines a sequence indexed from zero:

- `F(0) = 0`, `F(1) = 0`, `F(2) = 2`, `F(3) = 0`;
- for `n >= 4`,
  `F(n) = F(n-1) + F(n-2) + F(n-3) + F(n-4)`;
- compute the n-th element efficiently and without recursion.

The intended domain is the nonnegative sequence-index domain. The prompt does
not define negative sequence indices. The canonical implementation's Python
list indexing happens to return values for `-1..-4` and raises `IndexError` at
`-5`; those are implementation accidents, not a coherent negative-index Fib4
contract.

`/candidate/solution.py` implements the four bases explicitly, initializes
`(a,b,c,d) = (0,0,2,0)`, and iteratively shifts the four-value window from
index 4 through `n`. It is nonrecursive and uses unbounded Python integers.

### Trusted regeneration

Exact commands:

```text
python3 /reference/py2mpy.py /tmp/audit-work/46-fib4/solution.py > /tmp/audit-work/46-fib4/regenerated-solution.mpy
cmp -s /candidate/solution.mpy /tmp/audit-work/46-fib4/regenerated-solution.mpy
```

Both commands exited 0. Both files have SHA-256
`1c47bc669cedb3c4f2e69dbb62bf0976c4b82f699f7ff0155f4217062eefd498`;
the submitted translation is byte-identical to trusted regeneration.

### Independent differential test

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and `/candidate/solution.py`. It checks:

- documented inputs `5, 6, 7`;
- every explicit-return and loop boundary `0, 1, 2, 3, 4, 5`;
- every integer in `0..200`;
- 100 reproducibly generated values in `0..500`, seed `460046`.

There were 260 unique inputs and zero mismatches. Exploratory negative inputs
were recorded rather than hidden: the candidate diverges from incidental
canonical behavior at `-2` and `-5`, outside the stated sequence domain.

Evidence:

- `evidence/differential_test.py`
- `evidence/stage2-fidelity-and-differential.log`

Stage result: PASS for the material source-contract domain.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/46-fib4`, used no candidate
compiled definition or cache, and guarded against preexisting output
definitions. Fresh builds used:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module SEMANTIC-SYNTAX --output-definition concrete-kompiled
kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module SEMANTIC-SYNTAX --output-definition proof-kompiled
```

Both exited 0. LLVM compilation issued important non-exhaustive-match warnings
for `evalInt` and `evalBool`; those are reviewed in Stage 5.

Fresh LLVM `krun` executions for `n = 0,1,2,3,4,5,7,10,20` all exited 0 and
produced, respectively, `0,0,2,0,2,4,14,104,73552`. A separate automated
generated-semantics differential ran 36 boundary, dense, and reproducibly
generated nonnegative inputs. Every K result matched both Python
implementations.

I ran every submitted positive claim individually:

| Claim | Exit | Result |
|---|---:|---|
| `SPEC.fib4-spec-link` | 0 | `#Top` (with `WarnTrivialClaim`) |
| `SPEC.loop-correct` | 0 | `#Top` |
| `SPEC.fib4-inductive-init` | 0 | `#Top` |
| `SPEC.fib4-base-0` | 0 | `#Top` |
| `SPEC.fib4-base-1` | 0 | `#Top` |
| `SPEC.fib4-base-2` | 0 | `#Top` |
| `SPEC.fib4-base-3` | 0 | `#Top` |
| `SPEC.fib4-seven` | 0 | `#Top` |

The all-claims command also exited 0 and printed `#Top`:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

Evidence:

- `evidence/reconstruct.sh`
- `evidence/stage3-reconstruction-summary.log`
- `evidence/stage3-kompile-llvm.log`
- `evidence/stage3-kompile-haskell.log`
- the individual `evidence/stage3-kprove-*.log` files
- `evidence/stage3-kprove-all.log`
- `evidence/semantics_differential.py`
- `evidence/stage3-semantics-differential.log`

Stage result: PASS.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

1. `fib4-spec-link`: for any `N >= 4`, in an already finished configuration,
   `result(fib4Spec(N))` has the same definitional normal form as
   `result(advanceTo(0,0,2,0,4,N))`. This is a mathematical-link claim, not an
   entry execution claim. The backend correctly reports it as trivial because
   the `fib4Spec` equation already performs this reduction.
2. `loop-correct`: for `N >= 4`, `I >= 4`, and either `I <= N` or `I = N+1`,
   executing the exact submitted while-loop followed by `return d`, from any
   window `(A,B,C,D)`, returns
   `advanceTo(A,B,C,D,I,N)`. The final environment is existentially framed, but
   the result is not free.
3. `fib4-inductive-init`: for every `N >= 4`, executing `solutionProgram` from
   the initial configuration reaches the exact loop-head configuration with
   `n=N`, `(a,b,c,d)=(0,0,2,0)`, `e=0`, `i=4`, and `noResult`.
4. `fib4-base-0` through `fib4-base-3`: the actual submitted program returns
   `fib4Spec(0..3)` on the four fixed base inputs.
5. `fib4-seven`: the actual submitted program returns 14 at input 7.

Every precondition is satisfiable. Ground witnesses are preserved in
`evidence/stage4-claim-witnesses.log`; for example, `N=4`, `I=4`,
`(A,B,C,D,E)=(0,0,2,0,0)` satisfies the loop claim, and the result is 2.

### Exact composition for the unbounded branch

For arbitrary `N >= 4`, the post-state of `fib4-inductive-init` is
constructor-for-constructor the `loop-correct` pre-state under:

```text
A=0, B=0, C=2, D=0, E=0, I=4
```

The loop precondition then holds because `4 <= N`. Its postcondition is
`result(advanceTo(0,0,2,0,4,N))`, which is the guarded defining right-hand side
of `fib4Spec(N)`. Standard transitivity of reachability therefore composes the
two checked theorems into the unbounded entry property. Together with the four
base-entry claims, this covers every nonnegative integer.

The candidate does not contain a single all-`N >= 4` entry claim. I added a
reviewer-derived composed claim and tried it with the two already-proved claims
marked trusted. The bounded command made no progress and timed out after 30
seconds (exit 124). A timeout is not used as evidence against the candidate,
but the absence of a one-command machine check for the composition is a
nonfatal auditability concern. The exact intermediate-state match and
reachability transitivity—not the timeout or candidate prose—are the basis for
accepting the split proof.

### Program identity

Trusted regeneration pins `solution.mpy` to `solution.py`. The
`solutionProgram` equation expands to the exact translated `Module(FuncDef(...))`
constructor tree, including the `fib4` binding, parameter, four bases,
initialization, loop body, and final return. A mechanical runtime comparison
showed:

```text
krun solution.mpy ... --depth 1
krun solution-symbolic.mpy ... --depth 2
cmp -s concrete-expanded.out symbolic-expanded.out
```

All commands exited 0; the two complete configurations were byte-identical
with SHA-256
`9cfe2ea8c94d634619ac9e860041cd59ca98ccac9062c577f1cd8ab0a7b1be13`.
The extra symbolic depth is exactly the `solutionProgram` expansion step.

A body-sensitivity experiment changed the base-2 return inside the K term
actually executed by the claims from `Int(2)` to `Int(99)`. The definition
built successfully, but `SPEC.fib4-base-2` exited 1 with a stuck final state
containing `result(99)`. This rules out a theorem detached from its executed
body.

Evidence:

- `evidence/stage4-program-term-comparison.log`
- `evidence/stage4-claim-witnesses.log`
- `evidence/stage4-body-sensitivity.log`
- `evidence/spec-composed.k`
- `evidence/stage4-composed-entry-proof.log`

Stage result: PASS, with a nonfatal split-composition auditability concern.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

`semantic.k` declares:

- `Program`: `Module(Stmts)` and the named exact-term constant
  `solutionProgram`;
- list sort `Stmts`;
- `Stmt`: `FuncDef`, `Return`, `Assign`, `If`, `While`;
- `Params(String)`;
- `Exp`: `Int`, `Name`, `BinOp`, `Compare`;
- `CmpOp(String, Exp)`;
- `Result`: `noResult` and `result(Int)`;
- computation item `exec(Stmts)`;
- total function declarations `evalInt(Exp,Map)` and `evalBool(Exp,Map)`.

`verification.k` declares total functions
`advanceTo(Int,Int,Int,Int,Int,Int)` and `fib4Spec(Int)`.

There are no local `[functional]`, `[simplification]`, `[concrete]`,
`[anywhere]`, priority, or opaque declarations. The only special proof
attribute is `[circularity]` on `loop-correct`. The configuration has exactly
the needed `<k>`, `<arg>`, `<env>`, and `<result>` cells; no unused heap, I/O,
stack, or allocation cells are fabricated.

Every construct in `solution.mpy` is mapped:

| Submitted construct | Declaration/rules |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax plus module-entry rule |
| statement list | `Stmts` list plus `exec(.Stmts)` and head/rest rules |
| four `If`s and `==` comparisons | two disjoint equality-branch rules |
| `While` and `<=` comparison | two disjoint loop rules |
| `Assign`, `Name`, `Int`, `BinOp("+")` | assignment rule and three `evalInt` equations |
| `Return` | abrupt return/result rule |

`evalBool` is declared but is not used by any operational rule or submitted
term.

### Every local rule/equation

| Rule/equation | Review decision |
|---|---|
| `solutionProgram => Module(FuncDef(...))` | Exact definitional expansion, mechanically compared to trusted translation; it does not summarize or bypass execution. |
| module entry | Binds the sole parameter to `<arg>` and schedules the exact body. It is broader than a reusable Python semantics because it ignores the function-name string, but the actual term has the required `fib4` binding and one function. Sound on the submitted entry configuration. |
| `exec(.Stmts) => .K` | Correct sequential-computation base. |
| assignment | Evaluates the pure used expression in the pre-update map, then updates one binding. This preserves Python assignment order for the submitted expressions. |
| equality-`If`, true branch | Guard `I == J`; schedules then-body before the remaining statements. Correct and disjoint from the false rule. |
| equality-`If`, false branch | Guard `I =/= J`; schedules else-body before the remaining statements. Correct and exhaustive for mathematical integers. |
| `<=`-`While`, continue | Guard `I <= J`; schedules the body and then the same loop plus suffix. This is the real loop control flow. |
| `<=`-`While`, exit | Guard `I > J`; schedules the suffix. Disjoint and exhaustive with the continue rule. |
| return | Evaluates the return expression, sets the sole observable result, and discards remaining function computation. This is correct for the submitted single-frame entry execution, including early returns. No exception/finally/caller frame is present in the used subset. |
| `evalInt(Int(I),_) => I` | Exact. |
| `evalInt(Name(X),(X|->I) _M) => I` | Exact lookup for every submitted name use; all such names are bound before use. |
| `evalInt(BinOp("+",L,R),M)` | Exact unbounded integer addition; recursive operands are pure, so atomic evaluation introduces no order-visible difference. |
| `evalBool` equality | Mathematically correct but operationally unused. |
| `evalBool` less-or-equal | Mathematically correct but operationally unused. |
| `advanceTo`, `I > N` | Returns the current newest window value; correct loop-exit summary. |
| `advanceTo`, `I <= N` | Performs exactly one four-value sum, shift, and index increment. The guards are disjoint and exhaustive; `N-I+1` strictly decreases on the recursive branch. |
| `fib4Spec(0)`, `(1)`, `(2)`, `(3)` | Exact four contract bases. |
| `fib4Spec(N)`, `N >= 4` | Transparently invokes the rolling model from the base window and first update index. It does not rewrite any operational program term. |

The used program subset has deterministic, disjoint control rules. All material
state is visible in `<env>` and `<result>`. There is no heap, output,
allocation, exception, or mutation outside those cells in the submitted
program. Arithmetic uses K mathematical integers, matching Python's unbounded
integers for this program.

### Totality limitations

The source declares three functions total beyond their actual equation
coverage:

- `evalInt` has no equation for `Compare`, arbitrary binary-operator strings,
  or missing names;
- `evalBool` has no equation for non-comparisons or arbitrary comparison
  strings;
- `fib4Spec` has no equation for negative integers.

LLVM independently reports the first two declarations as non-exhaustive. These
are inaccurate global annotations and prevent calling the definition a sound
general semantics for every declared AST. They do not silently fabricate a
used operation: all `evalInt` calls reached by this program are covered,
`evalBool` is unreachable, and every intended `fib4Spec` argument is
nonnegative.

I also tested two concrete false equalities over the uncovered domains:
`fib4Spec(-1) = 0` and an unsupported comparison-valued `evalInt = 7`. Both
probe files built, both proofs exited 1 with the expected failed implication,
and neither false equality was admitted. Thus I do not label the totality
overclaims a material unsoundness capable of proving a false intended result;
they are a narrower trust/reuse limitation.

No rule encodes the task answer as an operational shortcut, introduces an
unconstrained result-bearing oracle, or preempts the real loop. `advanceTo` and
`fib4Spec` are transparent terminating equations used in postconditions, not
operational bridges. I found no concrete or symbolic false-conclusion witness
for any rule on the intended input domain.

Evidence:

- `evidence/stage5-source-and-rule-inventory.log`
- `evidence/spec-totality-probe.k`
- `evidence/stage5-totality-probes.log`
- LLVM warnings in `evidence/stage3-kompile-llvm.log`

Stage result: PASS on the submitted program, with nonfatal global-totality and
reuse concerns.

## 6. Fresh non-vacuity test

I created a fresh claim that executes the actual `solutionProgram` at the
satisfiable input 7 but requires `result(15)`. Both trusted canonical Python and
candidate Python return 14.

Commands:

```text
kprove spec-vacuity.k --definition /tmp/audit-work/46-fib4/proof-kompiled --spec-module SPEC-VACUITY --dry-run
kprove spec-vacuity.k --definition /tmp/audit-work/46-fib4/proof-kompiled --spec-module SPEC-VACUITY
```

The dry run exited 0, establishing that the mutation parses and builds. The
proof exited 1 with `WarnStuckClaimState`; the residual is the fully executed
program state with `result(14)`, directly exposing the unmet result obligation.
This is neither a parser error nor an unreachable mutation.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6-false-mutation.log`

Stage result: PASS.

## 7. Proven versus assumed accounting

### What is formally established

Under the generated semantics and K's built-in theories:

- on inputs 0, 1, 2, and 3, the actual pinned program returns the four stated
  base values;
- for every mathematical integer `N >= 4`, the actual pinned program reaches
  the exact initialized loop configuration;
- for every state in the loop theorem's precondition, executing the actual
  loop and return yields the transparent value
  `advanceTo(A,B,C,D,I,N)`;
- by exact state matching and reachability transitivity, the program on every
  `N >= 4` returns `advanceTo(0,0,2,0,4,N)`, which is the defining value of
  `fib4Spec(N)`;
- the result obligation is discriminating and depends on the executed body.

Combining the unbounded branch with the four bases covers every nonnegative
sequence index. This is a partial-correctness statement. The concrete program
also visibly terminates because `i` increases toward fixed `n`, but termination
is not needed for the requested partial-correctness classification.

### Trust and assumption ledger

| Boundary | Effect and judgment |
|---|---|
| K compiler, Haskell/LLVM backends, circularity mechanism | Foundational trusted toolchain. The audit rebuilt both definitions and did not trust candidate caches. |
| K `INT`, `MAP`, `BOOL`, `STRING` built-ins | Trusted primitives for unbounded integer arithmetic, finite-map lookup/update, booleans, and tokens. Appropriate for the used Python subset. |
| Trusted `py2mpy.py` | Empirical/syntactic bridge from Python AST to the submitted constructor term. Byte identity and runtime term comparison pin the artifact. |
| Generated entry bootstrap | Interprets the single translated function plus `<arg>` as entry invocation. Sound for this exact one-function module, but not a reusable full Python module/call semantics; documented concern. |
| `advanceTo` meaning | Not opaque: equations exactly expose one loop step and exit. The generic loop claim machine-checks execution against it. |
| Rolling summary versus the prose recurrence | Ordinary induction: before update `i`, the window is `(F(i-4),F(i-3),F(i-2),F(i-1))`; the sum/shift creates `F(i)` and preserves the invariant. This transparent argument is not packaged as a separate K theorem. Differential evidence supports 260 Python inputs and 36 K inputs but is finite. Nonfatal intent-bridge concern. |
| Split entry composition | Uses the standard transitivity metatheorem for two separately checked reachability claims with exact intermediate configurations. A reviewer-derived single composed claim timed out and is not claimed as a successful proof command. Nonfatal auditability concern. |
| `[total]` outside used domains | Overbroad declarations for unsupported expressions and negative `fib4Spec`; false-equality probes were rejected. Acceptable only because none can be reached by the submitted program on the intended domain. |
| Negative integers | Excluded because the prompt defines a zero-indexed sequence and supplies no negative-index contract. Canonical Python's negative list-index behavior is recorded but not elevated into the specification. |
| Differential tests | Reproducible finite evidence only; not a substitute for the K reachability proof or the mathematical induction. |
| Aggregate audit-input tree digests | Opaque digest-convention mismatch; layout-native and individual digests independently pin all mounted bytes. |

Gate A (real-program soundness and non-vacuity): PASS.  
Gate B (intent adequacy on the material sequence domain): PASS.  
Gate C (trust/evidence auditability): PASS with the limitations above.

The candidate is therefore legitimate. The limitations are material enough to
withhold an unqualified `PASS`, but none narrows the nonnegative HumanEval
domain, substitutes another program, makes the result free, or enables a false
conclusion on that domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
