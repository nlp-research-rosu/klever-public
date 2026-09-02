# Independent adversarial review: 31-is-prime

The candidate reconstructs to `#Top`, constrains the result, and mechanically
pins the submitted `solution.mpy`. It is nevertheless not a legitimate proof of
the real generated Python program. The generated semantics implements recursive
tail calls as constant-space jumps and has no Python call-stack or exception
state. On the valid, unrestricted integer input `1000003`, the K semantics
returns `Bool(true)` and the target claim concludes normal return, while the
submitted `solution.py` raises `RecursionError`; the trusted canonical returns
`True`. This is a concrete false normal-execution conclusion enabled by the
used call rules, not an unused-language coverage gap.

## 1. Input and provenance integrity

I first read `/audit-input.json`. It declares:

- problem `31-is-prime`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- candidate, trusted prompt/translator/canonical, generation records, and
  manifests at the mounted paths in `container_paths`.

The campaign object in `/audit-campaign-lock.json` is JSON-equal to
`audit_input.audit_campaign`. Its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

I read and parsed every required `legacy-selected-stage1` record:
`/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and all 164 JSONL events in the structured
trace. `usage.json` is present and was also inspected. Historical
`runtime-metrics.json` is absent, which is permitted for this layout. The
generation log and trace are treated only as untrusted historical claims; among
other things, they claim prior `#Top`.

All required mounts and entries are real regular files or real directories.
There are no symlinks or unsupported entries in the candidate or generation
trees. The candidate prompt and translator are byte-identical to their trusted
mounts. All individually recorded hashes for the campaign lock, canonical,
prompts, translators, run/task/result/invocation/metrics/usage records, prompt,
last message, output log, and trace JSONL file match.

An independently recomputed pipeline content-tree digest is
`1f332e78f0b2c9e8c1935db7c87f9298d4274eeeff701efd043148243bddcde9`
for `/candidate`; it matches both the generation result's workspace digest and
the invocation's retained-workspace digest. The trace digest is
`663592467847ad2f4abe652f0fd614dbf22d1e3ac9a3fad47167b78d46a1296a`
and matches `usage.json`. `audit-input.json` also contains launcher aggregate
digests under `candidate_tree_sha256` and
`generation_codex_trace_sha256`; their aggregate serialization is not declared
there, so I did not equate them with the pipeline digest. The manifest-linked
tree digests and every declared per-file digest independently bind the mounted
bytes.

No `/reference/reference-semantics` exists, as required in
`GENERATED_SEMANTICS` mode. I did not seek or use a hidden semantics. There is
no audit-infrastructure breach.

Reproduction: [provenance checker](evidence/provenance_check.py),
[complete log](evidence/stage1-complete.log). The earlier
`stage1.log` preserves a reviewer-script assertion that was corrected from
whole-object equality to the actual task-manifest subset relation; it was not
an input failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` requires `is_prime(n)` to return true exactly when the
given number is prime and false otherwise. The examples include primes,
composites, and `1`. The trusted `/reference/canonical.py` makes the intended
scalar domain concrete as Python integers: it returns false below `2`, searches
integer divisors from `2` through `n-2`, returns false on a divisor, and
otherwise returns true. No input bound is stated.

The submitted implementation uses a different but mathematically standard
algorithm: after rejecting `n < 2`, recursive helper `no_divisor(n,d)` tests
divisors from `2` until `d*d > n`. This is result-equivalent while it returns,
but CPython recursion depth is observable for sufficiently large primes.

### Translation fidelity

I regenerated the constructor term with the trusted translator:

```text
python3 /tmp/audit-work/review-31/reference/py2mpy.py \
  /tmp/audit-work/review-31/candidate/solution.py \
  > /tmp/audit-work/review-31/regenerated.mpy
```

The command exited 0 and `cmp -s` against the submitted `solution.mpy` exited
0. Thus the proof target is not based on a mistranslation.

### Independent differential

The reviewer-authored differential imported the trusted canonical and submitted
entry points independently. It ran:

- all seven documented examples;
- 20 outer-condition, square, divisor, and recursion branch boundaries;
- every integer from `-25` through `500`;
- 250 seeded representative integers in `[-1000,100000]`;
- recursion-boundary probes `9973`, `99991`, and `1000003`.

Of 806 executions, 805 matched. The one mismatch is material:

```text
n=1000003
canonical=('return', True)
generated=('raise', 'RecursionError',
           'maximum recursion depth exceeded in comparison')
```

`factor 1000003` independently reports `1000003: 1000003`. The input is a
prime integer in the unrestricted source-contract domain, not a malformed or
out-of-domain case.

Reproduction: [differential.py](evidence/differential.py),
[runner](evidence/run_stage2.sh), [log](evidence/stage2.log).

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/review-31` and ignored the
candidate `__pycache__`. No candidate-built definition or cache was used. The
installed tools report K `v7.1.293`, matching the campaign lock.

I built two fresh definitions:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/review-31/semantic-concrete-kompiled

kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/review-31/verification-proof-kompiled
```

Both exited 0.

Fresh `krun` executions covered negative/zero/one, the `2` boundary, prime and
composite branches, examples, and the recursion witness. They matched both
Python implementations on the ordinary cases. On `1000003`, the discrepancy
was:

```text
K generated semantics: <result> Bool ( true ) </result>   (exit 0)
trusted canonical:      return True
submitted solution.py:  raise RecursionError
```

The helper claim selected by label closed independently:

```text
kprove spec.k --definition .../verification-proof-kompiled \
  --spec-module SPEC --claims helper-correct
#Top
EXIT: 0
```

The actual positive target set, explicitly selecting both labels, also closed:

```text
kprove spec.k --definition .../verification-proof-kompiled \
  --spec-module SPEC --claims helper-correct,is-prime-correct
#Top
EXIT: 0
```

The unfiltered full-spec command likewise printed exactly `#Top` and exited 0.
For completeness, I also ran `--claims is-prime-correct` alone. It failed after
symbolic unrolling because that filter removes the helper circularity on which
the entry theorem explicitly depends. This is a useful dependency diagnostic,
not a failure of the full two-claim proof: the helper closes alone and the
claim set containing it closes. The failure is preserved in `stage3.log`.

Reproduction: [stage-3 runner](evidence/run_stage3.sh),
[build/concrete/diagnostic log](evidence/stage3.log),
[full-spec closure](evidence/stage3-all-claims.log), and
[explicit two-label closure](evidence/stage3-both-labels.log).

Dynamic reconstruction therefore passes under the candidate theory. It does not
validate that theory as Python semantics.

## 4. Adequacy and real-program pinning

### Claims in plain language

`helper-correct` says: for any K integers `N >= 2` and `D >= 2`, with
`"no_divisor"` bound to the exact helper body, invoking it consumes the
computation and changes the result to `Bool(noDivisor(N,D))`. The surrounding
function map is framed; final environment is existential because invocation
replaces it.

`is-prime-correct` says: for every K integer `N` (there is no precondition),
load `solutionProgram()`, invoke `"is_prime"` on `N`, consume the computation,
and change `Bool(false)` to `Bool(prime(N))`. The final environment alone is
existential. The result is fixed by `prime(N)` and is neither a free variable,
tautology, nor one-way implication.

Both sources are satisfiable. For example:

- helper: `N=2`, `D=2`, exact helper binding, `.Map` environment, and
  `Bool(false)` initial result;
- entry: `N=2`, empty initial maps, and `Bool(false)` initial result.

### Constructor-level identity and body sensitivity

I extracted the literal RHS of the `solutionProgram()` equation from
`verification.k`. The only normalization was converting explicit K list units
`.Stmts` in rule syntax to the external parser's omitted empty blocks. Parsing
both that RHS and the submitted `solution.mpy` with `kast --module VERIFICATION
--sort Program --output kore` produced byte-identical KORE:

```text
ce58457a17793e86173e7cc8d36972b11c30a418a5b5b3774e6fb36d57419726
```

A body-sensitivity mutant changed the helper increment from `d+1` to `d+2`.
It parsed successfully and produced a different KORE digest,
`f5bf175c57c4ab6e81e5f500154383d69baf7148fd02ed07da5efbe83c5637ff`;
`cmp` exited 1 as expected. The claim term therefore pins the immutable
submitted constructor body, not merely an external filename.

Reproduction: [extractor](evidence/extract_solution_program.py),
[runner](evidence/run_stage4.sh), and
[successful normalized comparison](evidence/stage4-normalized.log).
`stage4.log` preserves the preliminary parse failure that motivated the
explicit `.Stmts` normalization.

### Concrete substitutions

| `N` | Formal/K result | Trusted canonical | Submitted Python |
|---:|---|---|---|
| `-5` | `false` | `False` | `False` |
| `2` | `true` | `True` | `True` |
| `4` | `false` | `False` | `False` |
| `101` | `true` | `True` | `True` |
| `1000003` | `true` | `True` | `RecursionError` |

The helper claim matches actual helper control flow: test `d*d>n`, then
divisibility, then recurse at `d+1`. The entry claim executes the actual
submitted module and binding. Real-program pinning at the constructor level
passes; operational adequacy to Python fails at the final row.

## 5. Rule-by-rule static soundness review

The complete inventory, including every local syntax production, function
attribute, configuration cell, operational rule, equation, priority, and both
claims, is [rule-inventory.md](evidence/rule-inventory.md). The IDs below cover
that inventory exhaustively.

### Construct and declaration coverage

- D01–D15 declare exactly the submitted `Module`, statement-list,
  `FuncDef`, `Return`, `If`, parameter/list, `Int`, `Bool`, `Name`, `BinOp`,
  `Compare`, `Call`, comparison, and argument-list constructors.
- D16–D25 declare the internal function/control/evaluation/binding symbols.
  `#eval`, `#lookup`, `#bin`, `#cmp`, `#evalArgs`, and `#bind` are
  `[function]` but not `[total]`; their equations cover every actual use.
- D26–D30 declare the mathematical `noDivisor`/`prime` functions and exact
  body/program abbreviations.
- There are no local `[total]`, `[functional]`, `[simplification]`,
  `[concrete]`, or opaque declarations. The only priority is S09
  `[priority(40)]`.

The used-constructor mapping is complete:

| Submitted construct | Declaration | Behavior |
|---|---|---|
| module and statement sequence | D01–D02 | S01–S03 |
| function definitions | D03 | S04 |
| invocation/calls/names/arguments | D13, D17, D21, D24–D25 | S05, S09, S12, S15, S24–S27 |
| conditionals | D05, D18 | S06–S08 |
| returns/final result | D04, D19 | S09–S11 |
| integer/boolean literals | D08–D09 | S13–S14 |
| `+`, `*`, `%` | D11, D22 | S16, S18–S20 |
| `<`, `>`, `==` | D12, D14, D23 | S17, S21–S23 |

The `<functions>`, `<env>`, and `<result>` cells are all read or written.
There is no heap or I/O because the submitted program uses neither. There is,
however, no call-stack/frame cell and no exception cell even though recursive
Python calls are material.

### Operational rules S01–S27

S01–S04 soundly flatten the submitted module/list and install the two exact
capture-free definitions. S06–S08 soundly evaluate and select pure Boolean
guards. S12–S27 soundly implement the used map lookup, pure expression
evaluation, unbounded integer arithmetic/comparisons, one-/two-argument
evaluation, and one-/two-parameter binding. The `%` rule is guarded by nonzero
denominator, and actual `D >= 2`.

S05 and prioritized S09 are materially unsound as semantics of the real Python
program:

```k
rule <k> #invoke(F, VS) => B ... </k>
     <functions> ... F |-> function(P, B) ... </functions>
     <env> _ => #bind(P, VS) </env>

rule <k> Return(Call(Name(F), ES)) ~> _
      => #invoke(F, #evalArgs(ES, RHO)) </k>
     <env> RHO </env> [priority(40)]
```

They replace each Python call with the callee body and overwrite the current
environment without allocating or retaining a call frame. The recursive helper
is therefore tail-call optimized even though CPython does not perform tail-call
elimination. S10–S11 then turn a base return directly into the top-level result.
S10–S11 are value-correct for this all-tail-position program below the resource
boundary, although their context scope would be too broad for general Python
calls.

The required false-conclusion witness is concrete and in-domain:

1. `1000003` is prime, so the helper finds no divisor before crossing its
   square-root boundary.
2. CPython's observed recursion limit is `1000`.
3. The submitted Python raises `RecursionError`.
4. The generated K semantics performs constant-space jumps and exits 0 with
   `Bool(true)`.
5. `is-prime-correct` has no precondition excluding this `N` and concludes the
   normal result `Bool(prime(1000003)) = Bool(true)`.

This is evidence from the actual submitted body, not a hypothetical unused
construct. Rule priority makes S09 preempt the generic return rule; it does not
justify equivalence. The focused commands and outputs are in
[stage5-witness.log](evidence/stage5-witness.log), generated by
[run_stage5_witness.sh](evidence/run_stage5_witness.sh).

### Verification equations V01–V08 and claims C01–C02

V01–V03 define the finite divisor search. On the claim domain `N>=2,D>=2`,
the guards `D*D>N`, `D*D<=N && D divides N`, and
`D*D<=N && not(D divides N)` are exhaustive and pairwise disjoint; recursion
increments `D`. V04–V05 split all integers at `2`. K's imported
`dividesInt` reduces to integer remainder equality. These equations are
truthful mathematical definitions, not unconstrained oracles.

V06–V08 are exact constructor abbreviations for the two function bodies and
submitted module. They do not preempt actual `Module`, `If`, arithmetic, call,
or return execution. The mechanical comparison establishes their value.

C01 is a progressive circular helper invariant: concrete evaluation precedes
any recursive reuse at `D+1`. C02 depends on C01 and constrains the final
result. The proof therefore has no task-answer rewrite or execution bypass.
The ordinary theorem that a composite positive integer has a divisor no larger
than its square root is the informal bridge from V05's algorithmic predicate to
the word “prime”; it is standard mathematics but is not a separate K theorem.

Static review thus finds one material used-semantics defect: call/frame and
exception behavior. The exact witness above is the false conclusion that defect
enables.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. I wrote the fresh ground claim
[spec-audit-vacuity.k](evidence/spec-audit-vacuity.k). Its source state is the
real entry program at satisfiable input `N=2`; it deliberately requires final
`Bool(false)` although both the submitted K body and trusted canonical produce
true.

First, `kprove --dry-run` parsed and built the mutation successfully (exit 0).
The real proof command then exited 1 with `WarnStuckClaimState`. The residual
had empty `<k>`, exact loaded functions, `n |-> Int(2)`, `d |-> Int(2)`, and:

```text
<result>
  Bool ( true )
</result>
```

which could not unify with the false destination. This is the expected unmet
result obligation, not a parser error, timeout, or unrelated crash.

Reproduction: [runner](evidence/run_stage6.sh) and
[bounded log](evidence/stage6.log). Non-vacuity passes.

## 7. Proven versus assumed accounting and verdict

### What the successful reachability proof establishes

Under the candidate's abstract K theory:

- K values are unbounded integers and booleans with the imported arithmetic,
  comparison, remainder, Boolean, and map behavior;
- function invocation and recursive tail calls are constant-space body/env
  replacement transitions;
- the exact submitted `solution.mpy` is loaded;
- if the helper execution is considered under reachability/circularity from
  `N>=2,D>=2`, its final result is the algorithmic `noDivisor(N,D)`;
- for every K integer `N`, the entry execution reaches
  `Bool(prime(N))`.

That is a discriminating theorem about the exact constructor body under the
candidate semantics. It is not a theorem that the real Python call/exception
execution has that normal result for every source-contract input.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `Int`, `Bool`, `%Int`, `dividesInt`, comparison, and `Map` hooks/backends | all execution and summary equations | Acceptable low-level K trust boundary; exact tool version recorded. |
| Trusted CPython-AST translator | source-to-`solution.mpy` bridge | Acceptable and byte-checked; regeneration is identical. |
| `solutionProgram()`/body abbreviations | both claims | Acceptable; constructor-level KORE equality and sensitivity mutant recorded. |
| C01 circular helper invariant | C02 | Formally checked under the candidate theory; helper closes and progresses at `D+1`. |
| Divisor-below-square-root theorem | human meaning of `prime` | Standard but informal; finite differential supports, not proves, the intent bridge. |
| Differential against trusted canonical | implementation/intent and semantics evidence on 806 executions | Finite empirical evidence only. It exposes one material mismatch. |
| Generated call semantics as a model of Python frames/exceptions | the entry theorem's real-program interpretation | Illegitimate: contradicted by the concrete `N=1000003` witness. |
| Unbounded resource abstraction / no recursion exception | normal-result conclusion for large primes | Illegitimate here because unrestricted used calls are material and the theorem has no guard or conditional contract naming this abstraction. |

`PROOF.md`, generation traces, prior `#Top`, and differential testing were not
used as substitutes for the K proof.

### Gate and benchmark decision

- Dynamic reconstruction: pass under the submitted theory.
- Gate A, real-program soundness: fail. S05/S09 change used Python call behavior
  and enable the witnessed false normal-return conclusion.
- Gate B, intent/domain adequacy: fail. The unrestricted integer contract
  includes the witness; the semantics silently omits the material frame/exception
  behavior instead of stating a bounded or abstract-machine domain.
- Gate C, reproducibility/trust accounting: the audit evidence is reproducible,
  but it cannot repair Gate A.
- Non-vacuity and immutable body pinning: pass; neither cures unsound semantics.

Under the benchmark decision boundary, a clean `#Top` obtained for a
result-constraining, body-pinned claim is still not legitimate when materially
unsound generated semantics makes a false real-program conclusion provable.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
