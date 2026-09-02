# Independent adversarial audit: 150-x-or-y

The candidate contains a legitimate, reconstructed partial-correctness proof
of the submitted generated program under its generated semantics. The proof is
result-constraining, unbounded over K integers, and executes the exact
constructor term regenerated from `solution.py`. I found no task-answer axiom,
opaque result oracle, substituted body, bounded unrolling, or materially
unsound semantic/proof rule.

I assign `CONCERNS / LEGIT`, rather than an unqualified pass, for two nonfatal
scope/evidence limitations: the generated K-to-Python semantics connection is
audited rule by rule and tested but is not itself a machine-checked CPython
refinement theorem; and the untyped prompt leaves boundary-domain ambiguity.
In particular, the trusted canonical returns `x` for `n <= 0` while the
generated program returns `y` (the latter agrees with the ordinary
prime/non-prime contract), and the formal theorem represents `x` and `y` only
as integers. These limitations do not make a false result provable on the
material integer HumanEval domain evidenced by the prompt and canonical.

## 1. Input and provenance integrity

`/audit-input.json` declares problem `150-x-or-y`, condition `bare`, record
layout `legacy-selected-stage1`, and `GENERATED_SEMANTICS`. I used its
`container_paths`, not its host provenance paths.

The required records were present as regular, non-symlink files:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the present optional `/generation-evidence/usage.json`; and
- one regular 194-line JSONL trace below
  `/generation-evidence/codex-trace/`.

Historical runtime metrics are not required for this layout. I did not
reconstruct them. Every trace line parsed as JSON. I inspected the generation
records, output signals, tail, and trace structure only as untrusted historical
claims; none is used to establish proof validity.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`. Its independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. All launcher-recorded hashes for the run/task/
result/invocation records, generation prompt/metrics/usage/output/last files,
and trusted canonical/prompt/translator match their mounted bytes.

I also independently reconstructed the pipeline tree digest. The mounted
candidate hashes to
`42d3b31838c3997c279f68ada08ae16a711a7833ca9b262b6041c8acab06670b`,
exactly the workspace digest in the authenticated result and invocation
records. The trace tree hashes to
`db7a246c474d2ca1bdfbebd2b24d71cf58a3d508e41a63d4e2ce045badb84ffc`,
matching the authenticated usage record; its sole file also matches the
per-file result hash. No symlink or unsupported node occurs in the candidate
or trace trees.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
`/reference/reference-semantics` is absent, as required in
`GENERATED_SEMANTICS`. There is therefore no semantics-mode contradiction or
audit infrastructure breach.

Evidence:

- `evidence/stage1/provenance_check.py`
- `evidence/stage1/provenance-check.log` (`FAILURE_COUNT=0`, exit 0)
- `evidence/stage1/mount-inventory.log`
- `evidence/stage1/record-hashes.log`
- `evidence/stage1/required-records.log`
- `evidence/stage1/trace-inventory.log`
- `evidence/stage1/generation-output-signals.log`

Stage result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt says that `x_or_y(n, x, y)` returns `x` when `n` is prime
and `y` otherwise. Its examples require:

- `x_or_y(7, 34, 12) == 34`;
- `x_or_y(15, 8, 5) == 5`.

The trusted canonical special-cases `n == 1`, searches every integer in
`range(2, n)`, returns `y` on the first divisor, and otherwise returns `x`.
The generated solution uses a standard square-root trial-division algorithm:
it returns `y` for `n < 2`, tests divisors from 2 while `divisor² <= n`, returns
`y` on a zero remainder, and returns `x` after exhausting candidates.

The generated algorithm is correct for the ordinary mathematical definition
of integer primality. It is also more direct than the canonical for `n <= 0`:
those integers are not prime, so it returns `y`; the canonical's empty range
causes it to return `x`. That discrepancy is recorded, not hidden.

### Trusted regeneration

I ran:

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/candidate-src/solution.regenerated.mpy
cmp -s /tmp/audit-work/candidate-src/solution.regenerated.mpy /tmp/audit-work/candidate-src/solution.mpy
```

Both commands exited 0. Both terms have SHA-256
`49abec0a167b6884ce55b00cf1ecdd07e8079ef83570b131580ed884535181d2`.
Thus submitted `solution.mpy` is byte-identical to fresh output from the trusted
translator.

### Independent differential testing

`evidence/stage2/differential_test.py` independently imports both Python entry
points and uses a separate `math.isqrt` trial-division oracle. It exercises the
two prompt examples; negative, zero, one, and two boundaries; zero-iteration
and multi-iteration loops; first-divisor and later-divisor composites; prime
and composite squares; and larger values. Its broader deterministic set
contains 5,001 cases (`n=-1000..2000` plus 2,000 seeded cases up to magnitude
100,000, with varied integer `x/y`).

Results:

```text
generated_contract_mismatch_count=0
canonical_contract_mismatch_count=2028
generated_canonical_mismatch_count=2028
positive_generated_canonical_mismatch_count=0
EXIT_STATUS: 0
```

Every candidate/canonical difference had `n <= 0`; there was no difference for
tested `n >= 1`. `n=0` supplies the required numeric empty/boundary analogue;
the function has no collection input.

Scope judgment: the examples, arithmetic on `n`, canonical implementation, and
HumanEval use support an integer argument domain, with positive `n` the
canonical's evident intended subdomain. The formal theorem actually covers all
K integer `n`. The prompt does not expressly type `x/y`; because the Python
implementations merely return them, arbitrary objects would work in CPython,
whereas the K theorem represents them as integers. I treat that as a
documented domain ambiguity rather than a material proved-domain failure,
because all trusted contract evidence presents numeric values. If arbitrary
Python objects were intended, the theorem would be sound but limited to the
integer subdomain.

Evidence:

- `evidence/stage2/source-listings.log`
- `evidence/stage2/translator-regenerate.log`
- `evidence/stage2/translator-byte-identity.log`
- `evidence/stage2/differential_test.py`
- `evidence/stage2/differential-test.log`

Stage result: PASS with the documented canonical/type scope concern.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/rebuild`. I did not copy or
use candidate-built definitions, caches, or proof logs. The installed tools
independently report K version `v7.1.293`.

### Concrete definition and execution

Exact build command:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition llvm-kompiled
```

It exited 0. I then ran fresh `krun` executions for:

```text
(-7,101,-303), (0,101,-303), (1,101,-303),
(2,101,-303), (3,101,-303), (4,101,-303),
(7,34,12), (15,8,5), (49,0,17),
(97,11,22), (121,11,22)
```

All 11 executions terminated with `.K` and the expected `intVal` result.
`evidence/stage3/check_krun_log.py` parsed those K results and independently
compared them to the generated Python function: 11/11 matched, exit 0.

### Proof definition and every positive target

Exact build command:

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. `spec.k` contains one claim in `LOOP-SPEC` and three entry claims
in `SPEC`. The module proof commands cover every one:

```text
kprove spec.k --definition verification-kompiled --spec-module LOOP-SPEC
# #Top
# exit 0

kprove spec.k --definition verification-kompiled --spec-module SPEC
# #Top
# exit 0
```

The second command covers the universal entry theorem and both fixed prompt
examples; the imported loop lemma was also independently proved by the first
command. No prior `#Top` or candidate definition contributed to these results.

Evidence:

- `evidence/stage3/tool-versions.log`
- `evidence/stage3/kompile-llvm.log`
- `evidence/stage3/krun-boundaries.log`
- `evidence/stage3/krun-python-comparison.log`
- `evidence/stage3/kompile-haskell.log`
- `evidence/stage3/kprove-loop-spec.log`
- `evidence/stage3/kprove-spec.log`

Stage result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `LOOP-SPEC` starts at the real loop-head computation, with local bindings
   `divisor=D`, `n=N`, `x=X`, `y=Y`, empty result, and `D >= 2`. If execution
   terminates, it consumes the computation and returns `X` exactly when no
   divisor from `D` through `floor(sqrt(N))` exists; otherwise it returns `Y`.
   The final local environment is existential, but the input cells and result
   are not.
2. The universal `SPEC` claim starts with the exact submitted function binding
   and body, empty environment/result, and arbitrary integer `N,X,Y`. If it
   terminates, it returns `X` exactly when `isPrime(N)` is true and `Y`
   otherwise.
3. The first example claim fixes `(N,X,Y)=(7,34,12)` and requires result 34.
4. The second fixes `(15,8,5)` and requires result 5.

There is no one-way implication standing in for equality: the result cell is
rewritten from `.K` to the specified `Val`, and `<k>` must be consumed.

### Program identity

`evidence/stage4/program_term_compare.py` extracts balanced `Module(...)`
terms and compares constructor tokens after only one demonstrated syntax
normalization: the translator's blank empty-list argument and K's `.Stmts`
denote the same `List{Stmt,""}` empty value. The fresh `solution.mpy` term and
each of the three entry-claim terms contain 157 constructor tokens and match
exactly.

The entry semantic rule also matches the exact singleton binding
`FuncDef("x_or_y", Params("n","x","y"), BODY)`, initializes arguments in the
same order, and then executes `BODY`; it does not replace the body with a
summary. The claim term therefore pins the submitted program despite not
reading the external file during proof.

### Satisfying and reachable witnesses

`evidence/stage4/claim_witnesses.py` records:

- loop claim: `D=2,N=7,X=34,Y=12`, satisfying `D>=2`, claimed/generated/
  canonical result 34;
- universal claim: `N=15,X=8,Y=5`, claimed/generated/canonical result 5;
- fixed examples: their required results agree with both Python functions.

For the loop witness, fresh concrete execution at depth 17 reaches the exact
claimed control point: the loop condition evaluation followed by
`whileBranch`, then `exec(Return(Name("x")))`, with the exact four-entry
environment and empty result. This shows the invariant is exercised by actual
control flow rather than proving an unreachable helper.

The universal theorem instantiated at `N=0,X=101,Y=-303` returns `-303`, as
does generated Python; canonical Python returns `101`, exposing the already
documented canonical boundary discrepancy.

### Body sensitivity

`evidence/stage4/spec-body-mutation.k` changes the actual program term in the
claim from final `Return(Name("x"))` to final `Return(Name("y"))` while retaining
the original prime-selection postcondition. It parses and executes far enough
to reach a final result. `kprove` exits 1 with `WarnStuckClaimState`; the
residual shows `intVal(Y)` on a prime path and the unmet `X == Y` requirement.
The satisfying counterexample is `n=7,x=34,y=12`. Thus proof closure is
sensitive to the executed body, not merely to an external source filename.

Evidence:

- `evidence/stage4/program_term_compare.py`
- `evidence/stage4/program-term-compare.log`
- `evidence/stage4/claim_witnesses.py`
- `evidence/stage4/claim-witnesses.log`
- `evidence/stage4/loop-head-depth-final.log`
- `evidence/stage4/spec-body-mutation.k`
- `evidence/stage4/body-sensitivity-kprove.log`

Stage result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule/claim inventory is
`evidence/stage5/rule-inventory.md`. The source scan is
`evidence/stage5/static-inventory-source-scan.log`.

### Inventory totals

`semantic.k` declares:

- `Program`, statement-list, five statement, identifier-list, four expression,
  comparison-list, and comparison-operator syntax;
- two internal value constructors and ten continuation/control constructors;
- one configuration containing `k`, local environment, three integer input
  cells, and result; and
- 25 ordinary operational rules.

The 25 rules are exhaustively inventoried as S1–S25 in the evidence. They cover
the exact entry binding; statement sequencing; `if`; `while`; name assignment;
return; true/false branch and loop outcomes; map update; abrupt return; integer
and name evaluation; left-to-right binary evaluation; `+`, `*`, `%`; and
left-to-right `<`, `<=`, `==` comparisons.

`verification.k` declares exactly three transparent `[function]` symbols:
`primeFrom`, `isPrime`, and `chooseVal`, with seven equations total. There are
no `[total]`, `[functional]`, `[simplification]`, `[concrete]`, priority,
`owise`, `anywhere`, macro, alias, opaque, fresh, or task-answer rules.
`spec.k` contains exactly the four claims described above.

### Operational fidelity

Every syntactic construct in `solution.mpy` maps to an inventoried declaration
and rule. Unsupported operators, chained comparisons, assignment targets, or
names stop visibly; no fallback fabricates a value. Missing behavior for those
unused constructs is acceptable in generated-semantics mode.

Evaluation is left to right. Assignment evaluates its right-hand side before
updating one environment binding. The while rules return to the loop-head shape
used by the invariant. Return evaluates its expression, writes the previously
empty result, and clears the active function computation. This program has no
caller, cleanup action, exception handler, I/O, heap, or other observable
state, so clearing the remaining function suffix is faithful. The `n=4`
concrete test demonstrates that an early loop return discards the increment and
final return, while retaining the correct result and divisor state.

K `Int` supplies arbitrary-precision arithmetic like Python integers. Every
reachable remainder has positive divisor `>=2`, so Python and K remainders
agree; the semantic `%` rule additionally excludes zero. There is no integer
overflow.

The exact module-entry rule is a call harness, not an execution bypass: it
checks function name, parameter order, singleton body, empty environment, and
integer argument cells, then runs that body. No rule rewrites an invocation or
program expression to `isPrime`, `primeFrom`, `chooseVal`, or another oracle.

### Proof-helper equations

On every proof use, `D >= 2`:

- `N < D²` is disjoint from `D² <= N`;
- under `D² <= N`, remainder zero and nonzero are disjoint and exhaustive;
- the recursive case increments `D`, eventually reaching `N < D²`;
- `N < 2` and `2 <= N` partition all integer `N`; and
- true/false selector equations partition `Bool`.

These equations mirror exactly the real loop: stop successfully after passing
the square root, return false on a divisor, or continue at `D+1`. The ordinary
mathematical bridge is the elementary divisor lemma: every composite
`N >= 2` has a factor no greater than `sqrt(N)`. Thus `isPrime` is a truthful
definition of the requested predicate, not an unconstrained interpretation.

I built a fresh LLVM helper harness and compared K evaluation with an
independent oracle. Fifteen `isPrime` cases and eight `primeFrom` cases,
including negative/0/1 boundaries, primes, composites, perfect squares, and
different starting divisors, all matched (`23/23`, exit 0).

Narrow evidence gap: `primeFrom` syntax permits a direct call with `D <= 0`,
while its intended remaining-divisor interpretation and every target use are
scoped to `D >= 2`. The function is not declared total, and no target claim can
create an off-scope call. I found no false conclusion it enables on the
intended target domain, so under the audit instruction I do not label this a
material unsoundness. A more reusable definition would encode the domain in a
sort or guard.

No inventoried rule admits a false target conclusion witness; consequently
there is no unsoundness claim requiring such a witness.

Evidence:

- `evidence/stage5/rule-inventory.md`
- `evidence/stage5/static-inventory-source-scan.log`
- `evidence/stage5/summary-harness.k`
- `evidence/stage5/kompile-summary-harness.log`
- `evidence/stage5/summary-ground-tests.log`
- `evidence/stage5/check_summary_log.py`
- `evidence/stage5/summary-oracle-comparison.log`

Stage result: PASS.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created a fresh independent
mutation at `evidence/stage6/spec-vacuity.k`. It retains the exact real program
and the satisfiable fixed inputs `n=7,x=34,y=12`, but changes the
result-constraining obligation from `intVal(34)` to the false `intVal(35)`.

First:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

This built/parsed the mutation successfully and exited 0. Then:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

This exited 1 with `WarnStuckClaimState`. The residual final configuration has
`.K` in the computation and `intVal(34)` in the result, which cannot unify with
the demanded `intVal(35)`. The failure is exactly the reachable unmet
postcondition—not a parser error, timeout, crash, or unrelated stuck term.

Evidence:

- `evidence/stage6/spec-vacuity.k`
- `evidence/stage6/vacuity-dry-run.log`
- `evidence/stage6/vacuity-kprove.log`

Stage result: PASS.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the freshly built `MPY` semantics and `MPY-VERIFICATION` equations:

> For every K integer `N`, `X`, and `Y`, starting with the exact regenerated
> `x_or_y` module, empty environment, and empty result, if execution terminates
> then it consumes the computation and returns `intVal(X)` when `isPrime(N)` is
> true and `intVal(Y)` otherwise.

It also proves the exact generalized loop theorem for every integer `N,X,Y`
and every `D >= 2`, plus the two prompt examples. The theorem is unbounded; it
is not finite-size testing or bounded unrolling. It is a partial-correctness
statement. Termination is not part of what `kprove` establishes, although the
strictly increasing divisor and square bound give a straightforward informal
termination argument for integer inputs.

### Trust ledger

| Boundary | Effect and dependents | Accounting |
|---|---|---|
| Trusted `/reference/py2mpy.py` | Connects CPython AST syntax to `solution.mpy`; every proof depends on program-term identity | Launcher hash and byte equality checked; fresh output is byte-identical. The translator's general correctness is trusted by the benchmark, not proved here. |
| Generated `semantic.k` | Defines all program execution, control, state, and result behavior | Not treated as candidate authority. All local declarations/rules were audited, all used constructs mapped, 11 concrete results compared with Python, and return/body sensitivity checked. This is a finite/static validation bridge, not a universal CPython refinement theorem. |
| Exact module-entry call harness S1 | Maps configuration integers into the exact function binding/body | Acceptable: exact name/arity/order/body and empty environment are checked; the body then executes. No result is summarized. |
| K standard `INT`, `BOOL`, `STRING`, `MAP`, parsing/list machinery, compiler, and Haskell/LLVM backends | Primitive arithmetic, booleans, state map, parsing, execution, and proof | Ordinary low-level trust boundary. Versions are recorded. No candidate rule changes these primitives. |
| `primeFrom`, `isPrime`, `chooseVal` | Determine the loop and entry postconditions | Transparent definitional summaries, not opaque primitives. Their equations are exhaustive/disjoint on all uses and statically justified by ordinary mathematics. Ground helper testing is corroboration only. |
| Elementary square-root divisor lemma | Connects trial division to the human word “prime” | Informal ordinary-mathematics bridge; no separate K theorem formalizes the English predicate. It does not import an oracle or permit an opposite result interpretation. |
| Python differential evidence | Supports implementation/canonical/semantics fidelity | Finite evidence only: 5,001 Python cases, 11 K/Python program cases, and 23 K-helper/oracle cases. It does not replace the universal reachability proof. |
| Integer sort for `n,x,y` | Formal theorem domain | Material benchmark examples and canonical operations are numeric. Untyped `x/y` could accept arbitrary CPython objects, which are outside this theorem; this is an explicit scope concern, not silently claimed coverage. |
| Trusted canonical at `n <= 0` | Candidate/canonical result comparison | The canonical returns `x`, while the prompt's prime/non-prime wording and generated program return `y`. The proof faithfully establishes generated-program behavior; it does not prove canonical equivalence on those boundary inputs. |

There are no opaque symbols, fresh result values, empirical result oracles,
unproved operational bridges replacing program-defined code, simplification
axioms, or trusted candidate proof traces.

### Gate and verdict accounting

- Gate A (real-program soundness): PASS. The exact body executes; state/control
  are preserved; transparent equations are sound on every use; witnesses,
  body sensitivity, and false-postcondition rejection all succeeded.
- Gate B (intent adequacy): PASS for the material integer HumanEval domain.
  The prompt/canonical ambiguity for `n<=0` and untyped `x/y` is explicitly
  limited rather than hidden.
- Gate C (trust/evidence): PASS. Every retained command, scope, oracle, exit
  status, and relevant output relied on by this verdict is preserved under
  `/audit-output/evidence/`.

The proof is therefore legitimate. The non-machine-checked generated-semantics
refinement boundary and the prompt/canonical type/boundary ambiguity are
nonfatal limitations, so the benchmark verdict is `CONCERNS / LEGIT`, not
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
