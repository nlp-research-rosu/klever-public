# Independent adversarial review: 36-fizz-buzz

## Overall finding

The candidate contains a legitimate, result-constraining partial-correctness
proof of the real submitted program. I rebuilt both K definitions from source,
proved all claims with their prerequisite claims retained, mechanically pinned
the entry closure to the trusted regeneration of `solution.mpy`, and obtained
the expected rejection of a fresh false result mutation.

The non-fatal concern is that the machine-checked entry postcondition is stated
with the proof-local recurrence `fizzResult`, while the final identification of
that recurrence with the prompt's decimal-string counting description remains
an ordinary mathematical induction rather than a second machine-checked
equivalence theorem. The recurrence is truthful and fully connected to real
execution, so this is not an oracle, a domain restriction, or a soundness
failure. Broad differential evidence supports the bridge but does not prove it
universally. Under the benchmark decision boundary this warrants
`CONCERNS / LEGIT`, not `FAIL`.

## 1. Input and provenance integrity

### Launcher and record layout

`/audit-input.json` declares:

- problem `36-fizz-buzz`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `pipeline-v3`;
- mounted inputs through its `container_paths` map.

The rendered mode and trusted mounts agree: `/reference/reference-semantics`
exists as required. There is no infrastructure-mode contradiction.

I read and validated all required pipeline-v3 records:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the JSONL trace under `/generation-evidence/codex-trace/`

Every required record is a readable regular non-symlink. All JSON documents
parse, and all 690 structured trace lines parse. The structured trace contains
473 response items and 214 event messages; all 169 recorded tool calls have a
corresponding output. Its final message asserts `VALIDATED` and `#Top`, but I
treated those as untrusted claims. The complete independent trace summary is
in
[`generation_trace_summary.log`](evidence/generation_trace_summary.log), and
the script that read every trace record is
[`generation_trace_summary.py`](evidence/generation_trace_summary.py).

### Campaign lock and hashes

The JSON object in `/audit-campaign-lock.json` is exactly equal to the
`audit_campaign` block in `/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All launcher-declared file hashes and every evidence hash in
`/generation-result.json` match the independently read mounted bytes,
including the structured trace hash
`a1567f3401ae3744199d66ac93ef4ac6227f1b47c337192b060a8c267cdb0680`.
See
[`stage1_record_hashes.log`](evidence/stage1_record_hashes.log) and
[`stage1_integrity.log`](evidence/stage1_integrity.log).

### Candidate/trusted integrity

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The required proof artifacts
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md` are all readable regular non-symlinks.

For the supplied semantics boundary, I recursively compared entry types,
relative paths, and file hashes. The candidate and trusted trees each have the
same 25 entries, with no missing, additional, mistyped, changed, or symlinked
entry. `diff -r --no-dereference` exits 0, and independently generated typed
manifests are identical with SHA-256
`2b83397b8af132099b1f514f2f02ee49d148bf98cb76a7875250a0b3c0e6ddcb`.

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks `fizz_buzz(n: int)` to count occurrences of decimal
digit `7` among integers less than `n` that are divisible by 11 or 13. The
trusted canonical implementation realizes “integers less than `n`” as
`range(n)`, hence the candidates considered are exactly `0` through `n - 1`,
and the result is zero for `n <= 0`.

The submitted implementation uses the equivalent countdown:

1. set `i = n`;
2. while `i > 0`, decrement first, producing candidates `n - 1` down to `0`;
3. if the candidate is divisible by 11 or 13, repeatedly inspect its
   least-significant decimal digit and divide by 10;
4. add the Boolean digit comparison to the integer count.

Zero contributes no digit, matching the canonical string computation.

### Trusted regeneration

In the scratch directory I ran:

```text
python3 trusted/py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy candidate-source/solution.mpy
```

Both commands exit 0. Both files have SHA-256
`b5f6c66a030c31696fab572b0ee02f5ec93cddd71d27f5b1444f60c4a4f7ee77`.
Thus the submitted `solution.mpy` is byte-identical to trusted regeneration.
Exact commands, outputs, and statuses are in
[`stage2_fidelity.log`](evidence/stage2_fidelity.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and the scratch copy of the submitted Python entry point. It checks:

- prompt examples `50`, `78`, and `79`;
- negative, zero, and empty-loop boundaries;
- values immediately around multiples of 11, 13, and 143;
- values immediately around qualifying numbers containing digit 7;
- every integer from `-100` through `2000`;
- five larger values through `100000`;
- 2,000 deterministic generated values from `[-2000, 20000]`.

The resulting 3,825 unique inputs have zero value or return-type mismatches.
The exact scope and representative outputs are preserved in
[`stage2_fidelity.log`](evidence/stage2_fidelity.log). This is finite evidence,
not a substitute for the K proof.

## 3. Clean proof reconstruction

### Isolation and builds

I copied only source artifacts to `/tmp/audit-work/36-fizz-buzz`. The semantics
copy came from the trusted `/reference/reference-semantics` tree after the
integrity check. Candidate-provided `runtime-kompiled`,
`verification-kompiled`, caches, logs, and traces were not copied or used.

The independently observed tool version is K v7.1.293. The fresh commands
were:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun audit-concrete-tests.mpy \
  --definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Every build and concrete command exits 0. The concrete program contains the
constructor-identical submitted function plus 18 assertions over negative,
empty, prompt, branch, and digit boundaries through `1000`. `krun` terminates
with `.K`, caller environment 0, empty stack, `noRet`, `NoExc`, and exit code
0. The test source is
[`audit-concrete-tests.py`](evidence/audit-concrete-tests.py), with its trusted
translation in
[`audit-concrete-tests.mpy`](evidence/audit-concrete-tests.mpy).

The fixed supplied semantics emits warnings about unrelated total functions
whose equations do not cover internal `cellsMark` values, an abstract
out-of-bounds `valSeqAt`, and unused string-rule variables. None of those
symbols is constructible on this program's path. There is no positive-claim
error or warning indicating a stuck target state.

### Positive claims

The full target command is:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

It prints `#Top` and exits 0. I also ran dependency-closed selections:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.inner-loop

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.inner-loop,SPEC.outer-loop

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.fizz-buzz
```

All three print `#Top` and exit 0. This independently establishes the inner
claim, the outer claim with its inner prerequisite, and the entry claim with
both prerequisites.

For transparency, selecting `SPEC.outer-loop` alone fails because K's
`--claims` filter removes the `inner-loop` circularity that the outer theorem
uses. The resulting dependency diagnostic is preserved in
[`stage3_rebuild_isolated_filter_attempt.log`](evidence/stage3_rebuild_isolated_filter_attempt.log).
It is not a failure of the submitted proof set. The successful clean transcript
with every exact command and status is
[`stage3_rebuild.log`](evidence/stage3_rebuild.log); the runner is
[`stage3_rebuild.sh`](evidence/stage3_rebuild.sh).

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.inner-loop`:

- Precondition: `X >= 0`, the current local scope contains exactly integer
  locals `count=C`, `i=I`, `n=N`, and `x=X`, and the exact submitted inner
  `#while` is at the head of the computation.
- Postcondition: that loop is consumed, `count=digitResult(C,X)`, `x=0`, and
  the other locals, continuation, and framed cells are preserved.

`SPEC.outer-loop`:

- Precondition: `I >= 0`, locals are `count=C`, `i=I`, `n=N`, `x=0`, and the
  exact submitted outer `#while`, including its exact inner `While`, is at the
  computation head.
- Postcondition: that loop is consumed, `count=fizzResult(C,I)`, `i=0`,
  `x=0`, and `n` plus all framed state are preserved.

`SPEC.fizz-buzz`:

- Precondition: there is no restriction on `N:K Int`; the module scope binds
  `"fizz_buzz"` to the submitted closure, with builtins parent `-1`, empty
  heap/stack, no pending return or exception, and exit code 0.
- Postcondition: the call is consumed and produces an integer `R` satisfying
  `R == fizzResult(0,N)`, with all explicitly shown observable cells restored.

These domains cover every mathematical integer accepted by the stated source
contract. They are not a finite-size or example-only restriction.

### Satisfiable states and concrete substitutions

Concrete witnesses are:

- inner claim: `X=79`, `C=4`, `I=N=79`, `L=1`;
- outer claim: `I=79`, `C=0`, `N=79`, `L=1`, `x=0`;
- entry claim: `N=79` with exactly the module/builtins scopes and runtime cells
  shown in the claim.

The corresponding summary values are `digitResult(4,79)=5` and
`fizzResult(0,79)=3`. Fourteen concrete substitutions from `-5` through `777`
agree among the summary recurrence, trusted canonical, and submitted Python
implementation. See
[`claim_witnesses.py`](evidence/claim_witnesses.py) and
[`stage4_pinning.log`](evidence/stage4_pinning.log).

### Mechanical program pinning

[`constructor_identity.py`](evidence/constructor_identity.py) independently
parses balanced constructor calls rather than trusting candidate
`check_identity.py`. It establishes:

- the submitted module is exactly one
  `FuncDef("fizz_buzz", Params("n"), BODY)`;
- `spec.k` has exactly one `closureVal` entry binding;
- its parameter and defining environment are `"n"` and `0`;
- its body equals the regenerated function body constructor-for-constructor;
- the only normalization is one explicit `.Stmts` empty `If`-else list in the
  claim, corresponding to the list unit accepted implicitly by the submitted
  term;
- the fresh LLVM test executes the same function constructor;
- the entry call and all listed observable cells are present.

The fixed `FuncDef` rule would install exactly this closure in environment 0.
Therefore starting the theorem from its already-installed binding merely omits
semantically inert module-load setup; it does not substitute another program.
The actual submitted body, not an external source filename, is the term
executed by the claim.

The existential return is constrained by the equality in `ensures`; it is not
free, tautological, or protected only by a one-way implication.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule_inventory.tsv`](evidence/rule_inventory.tsv) contains every local
configuration, syntax declaration, context, rule, simplification, priority
attribute, function/total declaration, no-evaluator symbol, and claim in:

- the supplied `semantics.k` assembly and all 23 helper `.k` files;
- candidate `verification.k`;
- candidate `spec.k`.

The assembly file itself contains imports/modules but no local declaration or
rule. Across the 26 inventoried files there are 938 entries:

| Kind | Count |
|---|---:|
| Configuration | 1 |
| Syntax declarations | 228 |
| Contexts | 5 |
| Ordinary/simplification rules | 701 |
| Reachability claims | 3 |

Attribute counts include 149 function declarations, 110 total declarations,
52 priority-bearing entries, 30 `owise` entries, 55 concrete entries, six
proof-local simplifications, and 25 `symbol(...), no-evaluators` declarations.
There are no local `[functional]` declarations. Counts by file and audit
disposition are in
[`rule_inventory_summary.txt`](evidence/rule_inventory_summary.txt).

Every row is assigned one of four dispositions: proof-local manual review,
proof-claim manual review, supplied module containing the used path, or supplied
module unreachable from the submitted constructors. This preserves the full
rule-by-rule record rather than silently omitting unused imported theory.

### Used syntax and fixed-semantics execution

[`used_construct_map.md`](evidence/used_construct_map.md) maps every submitted
constructor to its declaration and reachable rules. The material chain is:

```text
Call
→ exact name lookup
→ left-to-right argument evaluation
→ exact closure dispatch/frame allocation
→ parameter binding
→ sequenced Assign/While/If/BoolOp/Compare/BinOp operations
→ strict Return
→ frame pop and caller-state restoration
```

The relevant fixed rules correctly preserve:

- local scope selection and parent binding;
- RHS-first assignment;
- left-to-right binary operands;
- left-to-right short-circuit `or`;
- integer truthiness and comparison;
- unbounded integer `+`, `-`, `%`, and `//`;
- conversion of Boolean digit equality to `0` or `1` under integer addition;
- while guard/body/control order;
- return value, frame removal, environment restoration, and exception/exit
  state.

All divisors reached by this program are positive constants 10, 11, or 13, so
the supplied `pyMod` and quotient equations coincide with CPython floor
division/modulo. Reference rules for cells, references, containers, floats,
imports, builtins, methods, exceptions, and other syntax are guard- or
constructor-unreachable here.

### Proof-local rule review

`verification.k` adds two `[function]` symbols, no `[total]` assertion, no
priority, no opaque/no-evaluator symbol, and no rule mentioning `<k>`, a call,
a loop, an assignment, a return, a closure, or any program AST constructor.
Consequently there is no operational bridge and no rule that can bypass fixed
execution.

| Rule | Class | Domain/overlap review | Soundness and value influence |
|---|---|---|---|
| `digitResult(C,N) => C` | Definitional base | `N <= 0`, disjoint from positive rules | A non-starting digit loop preserves the accumulator. |
| one-digit `digitResult` result | Derived base boundary | `N > 0` and quotient `<= 0`; overlaps the fold only where the fold reaches the base | For positive integers this is exactly one digit contribution. Both paths agree. |
| folded `digitResult(C+b(N),q(N)) => digitResult(C,N)` | Definitional recurrence | `N > 0`; normalized remainder is `0..9`; `0 <= q(N) < N` | Truthful decimal recurrence. It affects the final result but is universally connected to the exact inner loop by `SPEC.inner-loop`. |
| `fizzResult(C,N) => C` | Definitional base | `N <= 0`, disjoint from positive folds | Empty candidate range preserves the accumulator. |
| qualifying `fizzResult` fold | Definitional recurrence | `N > 0` and `(N-1)` divisible by 11 or 13 | Adds exactly `digitResult(C,N-1)` and descends to `N-1`. |
| non-qualifying `fizzResult` fold | Definitional recurrence | Exact Boolean complement of the qualifying guard | Preserves the accumulator and descends to `N-1`. |

The two outer guards are disjoint and exhaustive for every positive `N`. The
base and positive domains are also disjoint and exhaustive. The one intentional
inner boundary/fold overlap has equal consequences. No equation replaces a
program-derived value with an unconstrained symbol: the exact inner and outer
reachability claims connect fixed loop execution to the summaries over their
complete domains.

As supporting evidence, the independent guard/equation checker performs
40,404 digit recurrence checks, 36 boundary-overlap checks, and 40,404 outer
recurrence checks, with guard coverage, agreement, and descent all passing.
See
[`proof_equation_audit.py`](evidence/proof_equation_audit.py) and
[`stage5_static_checks.log`](evidence/stage5_static_checks.log). These finite
checks support, but do not replace, the manual universal arithmetic argument.

### Claim/circularity review

- `inner-loop` matches the exact internal `#while`, exact local names/values,
  and preserves an arbitrary continuation suffix and all omitted cells on both
  sides. It reads/writes only `count` and `x`.
- `outer-loop` matches the exact outer `#while` and inner surface `While`. It
  reads/writes `i`, `count`, and `x`; it preserves `n` and all framed state.
- `fizz-buzz` starts from exact lookup/call state and uses the loop claims only
  after fixed semantics reaches their real loop heads.

These are reachability circularities, not priority rewrites in the semantics.
The nested dependency closures were independently proved in Stage 3.

### Opaque and unused supplied theory

The supplied fixed semantics imports 25 no-evaluator symbols for float
arithmetic, sorting, and MD5. The exact list and reachability assessment are in
[`opaque_symbols.txt`](evidence/opaque_symbols.txt). No submitted constructor,
binding, verification equation, or claim can create any of them. They influence
neither control, state, result, nor postcondition here.

The compiler's non-exhaustive-totality warnings also concern unreachable
container/float helper inputs. I found no concrete or symbolic false conclusion
that any supplied or candidate rule can enable on this theorem's integer-only
domain. Accordingly I do not label a rule unsound; the required false-conclusion
witness obligation is not triggered. The unused imported theory remains part
of the broad supplied-semantics trust boundary and is one reason not to
overstate what was independently validated.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer mutation is
[`audit-spec-false.k`](evidence/audit-spec-false.k). It retains the exact
submitted closure, chooses the satisfiable witness `N == 79`, and changes the
result obligation to:

```text
R == fizzResult(0,N) + 2
```

At `N=79`, the submitted and trusted Python functions both return 3, so the
mutation demands the false result 5.

First:

```text
kprove audit-spec-false.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE \
  --dry-run
```

builds the claim successfully and exits 0. Then the same command without
`--dry-run` exits 1 with `WarnStuckClaimState`. Its residual includes:

```text
fizzResult(0,79) +Int 2 #Equals fizzResult(0,79)
```

and the prover reports that the reachable configuration cannot be rewritten
further. This is the expected unmet result obligation, not a parse error,
missing import, timeout, unrelated crash, or unreachable mutation. The exact
transcript is
[`stage6_false_mutation.log`](evidence/stage6_false_mutation.log), with the
complete prover output in
[`stage6_false_mutation_prover.log`](evidence/stage6_false_mutation_prover.log).

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied `MPY` semantics plus the six reviewed proof-local summary
equations, for every K integer `N`, if the exact submitted `fizz_buzz` call
terminates from the entry configuration, it reaches an integer `R` such that:

```text
R == fizzResult(0,N)
```

The theorem also establishes the two universal loop summaries used to reach
that result, consumes the call, and restores the explicitly pinned caller
environment, allocator, empty heap/stack, return state, exception state, and
exit code. This is a partial-correctness theorem; it is not a K liveness or
resource-bound theorem.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Supplied `reference-semantics` | Defines every program step, cell, value, and control effect in all claims | Required fixed semantics for this condition; candidate copy is byte/type/path identical. Material used rules were statically traced and concretely exercised. |
| K v7.1.293 parser/compiler, LLVM/Haskell backends, KORE executor, SMT and built-in Int/Bool/Map/List theories | Trusted computing base for builds, concrete runs, `#Top`, and mutation rejection | Conventional unavoidable proof TCB; independently rebuilt rather than reusing candidate output. |
| Trusted `py2mpy.py` | Connects `solution.py` to the constructor program | Accepted launcher-owned bridge; byte regeneration and independent constructor comparison pass. |
| `digitResult` and `fizzResult` equations | Name the result-bearing loop recurrences used by all claims | Not opaque primitives and not execution bridges. Guards, overlap, and descent are sound; exact loop claims universally connect them to real execution. |
| Recurrence-to-English property argument | Identifies the least-significant-digit recurrence with decimal digit count and the countdown recurrence with all qualifying integers below `n` | Straightforward well-founded induction, but not a separate machine-checked theorem. This is the principal non-fatal concern. |
| Trusted canonical and CPython differential tests | Support implementation intent, source/summary bridge, and examples | Empirical only: 3,825 tested inputs and 14 explicit summary substitutions cannot establish universal equivalence. |
| Imported float/sort/MD5 opaque symbols and unrelated total helpers | Present in the fixed definition but absent from every target path | No dependent target rule or claim; acceptable inert trust boundary for this theorem. |
| Termination argument | Outer positive `i` decreases by 1; inner positive `x` becomes `x // 10`, a smaller nonnegative integer | Informal and outside the requested partial-correctness theorem. It does not narrow the theorem's input domain. |

### Decision

Gate A passes: the real program executes, the summaries are sound and
connected, the result is constrained, all positive claims reconstruct, and the
fresh false mutation is rejected.

Intent adequacy covers the full integer source-contract domain, including
nonpositive inputs. There is no finite unrolling, fixed-size restriction,
substituted program, oracle, or execution-bypassing rule. The remaining
summary-to-English identification is a non-fatal informal intent bridge
supported by broad finite evidence. It prevents an unqualified `PASS` under
the benchmark's explicit concern category, but it does not undermine
legitimacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
