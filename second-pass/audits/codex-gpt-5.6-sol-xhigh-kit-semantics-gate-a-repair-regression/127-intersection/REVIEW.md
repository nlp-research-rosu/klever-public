# Independent adversarial audit: 127-intersection

This audit used the required `using-kit` and `validating-proof` procedures. It
treated every candidate artifact, prior trace, log, compiled definition, and
`PROOF.md` as an untrusted claim. All executions used source copied to
`/tmp/audit-work/127-intersection`; candidate-provided kompiled definitions and
caches were not reused.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The required trusted mount
`/reference/reference-semantics` exists as a real directory, so there is no
mode/mount contradiction and no infrastructure breach.

The recursive integrity check found:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- All 24 K source files in `/candidate/reference-semantics` have exactly the
  same paths, types, and bytes as `/reference/reference-semantics`. There are
  no missing, additional, changed, mistyped, or symlinked entries in that tree.
- All required top-level candidate source/evidence artifacts checked by the
  audit are regular files. `find -P /candidate -type l` found no symlink
  anywhere under the candidate.

The exact comparisons, types, and per-file hashes are in
`evidence/01_integrity.sh` and `evidence/01_integrity.log`; the script exited
0. Candidate-produced `runtime-kompiled`, `verification-kompiled`,
`__pycache__`, logs, traces, and negative probes were present but were not
trusted or reused as proof evidence.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the 358-line structured JSONL trace only as untrusted
generation claims. The trace is valid JSONL and claims a successful generation,
two `#Top` results, 8,281 differential cases, and expected negative failures.
Those claims were not used to establish the verdict. Their hashes, bounded
summaries, event counts, and final claims are preserved in
`evidence/01_provenance_summary.py` and
`evidence/01_provenance_claims.log`.

Stage result: **PASS**. No provenance or semantics-integrity failure was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two closed integer intervals `(a0,a1)` and `(b0,b1)`, with
`a0 <= a1` and `b0 <= b1`, define

```text
L = min(a1,b1) - max(a0,b0).
```

The trusted prompt and canonical implementation use geometric coordinate
length, not the number of contained integer points: for example `[2,3]` has
length 1. The required result is `"YES"` exactly when `L` is a prime integer;
touching, disjoint, length-0, and length-1 intersections return `"NO"`.

### Source behavior

`solution.py` computes the same `L`. It returns `"NO"` for `L < 2`; otherwise
it tests every divisor from 2 through `L-1`. It does not break after finding a
divisor, but `is_prime` is only changed from `True` to `False`, so the extra
iterations do not change the result. Every source branch is consistent with
the trusted canonical implementation on the intended domain.

Using the trusted translator from the scratch copy:

```text
python3 /tmp/audit-work/127-intersection/trusted/py2mpy.py \
  /tmp/audit-work/127-intersection/candidate-src/solution.py \
  > /tmp/audit-work/127-intersection/regenerated-solution.mpy
```

exited 0. `cmp -l` against the submitted `solution.mpy` exited 0, and both
files have SHA-256
`73f08111bfe441025922cb117f0c97d61442edfed477d93bbcd6b9464a368cde`.
See `evidence/02_translation_identity.log`.

The independent differential script imports the trusted canonical and
candidate entry points from separate files. It tests:

- all three prompt examples;
- degenerate, touching, disjoint, and lengths 0, 1, 2, 3, 4, 5, and 6;
- both choices of `max` and `min`, nested intervals, negative endpoints, and
  large positive/negative integers;
- all 23,409 pairs of ordered intervals whose endpoints lie in `[-8,8]`; and
- 2,000 deterministic generated cases using seed 127 and endpoints in
  `[-100,100]`.

All 25,428 comparisons agreed: 0 mismatches, 6,509 `"YES"` results, and 18,919
`"NO"` results. The deterministic input description, script, command, digest,
and output are in `evidence/02_differential_inputs.json`,
`evidence/02_differential.py`, and `evidence/02_differential.log`.

Stage result: **PASS**.

## 3. Clean proof reconstruction

Only candidate source files and the recursively verified source semantics were
copied to `/tmp/audit-work/127-intersection/candidate-src`. Fresh output
definitions were created below `/tmp/audit-work/127-intersection/build`.
The tool versions are K `v7.1.293` and Python `3.10.12`
(`evidence/00_environment.log`).

### Concrete definition

The supplied semantics was freshly compiled:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/127-intersection/build/runtime-kompiled
```

This exited 0 (`evidence/03_runtime_build.log`). A reviewer-authored smoke
program contains an AST-identical copy of the submitted function plus eight
normal/boundary assertions. Python execution and translation both exited 0.
Fresh `krun` execution ended with `.K`, `NoExc`, `<exit-code> 0`, empty heap,
empty stack, and restored module environment. See
`evidence/03_concrete_prepare.log` and
`evidence/03_concrete_krun.log`.

### Proof definition and claims

The proof theory was freshly compiled:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/127-intersection/build/verification-kompiled
```

It exited 0 (`evidence/03_verification_build.log`).

The loop target was then run independently:

```text
kprove spec.k \
  --definition /tmp/audit-work/127-intersection/build/verification-kompiled \
  --spec-module SPEC --claims SPEC.divisor-loop
```

It printed `#Top` and exited 0
(`evidence/03_kprove_divisor_loop.log`).

Finally, the complete specification was run with both the loop circularity and
entry claim present:

```text
kprove spec.k \
  --definition /tmp/audit-work/127-intersection/build/verification-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0
(`evidence/03_kprove_complete_spec.log`). Thus every positive claim was
included in a fresh successful target run, and the auxiliary loop claim also
closed in its own focused run.

The only warnings in the positive proof logs are unused variables in the
trusted `strLt` equations and unused preserved loop-frame values in `spec.k`;
they do not indicate a stuck or incomplete claim.

Stage result: **PASS**.

## 4. Adequacy and real-program pinning

### `SPEC.divisor-loop`

Plain-language precondition: execution is at the real recurring `#while` head;
the current divisor is integer `I`, the saved intersection length is integer
`N`, the Boolean flag is `P`, and `2 <= I <= N`. The local frame has exactly
the function’s seven real variables.

Plain-language postcondition: the loop and its loop-control marker are
consumed, `divisor` is `N`, and `is_prime` is
`P andBool noDivisors(N,I)`. Parameters, endpoints, length, enclosing scopes,
the arbitrary continuation, and omitted configuration cells are framed.

The precondition is satisfiable. For example, `N=5`, `I=2`, `P=true`, with
any two tuple parameters and consistent stored endpoint variables, is a real
loop-head state. One iteration preserves the invariant because it changes the
flag precisely when `pyMod(N,I) == 0` and then increments `I`; this is exactly
the recursive `noDivisors` equation. At `I=N`, the loop guard is false and
`noDivisors(N,N)=true`.

### `SPEC.intersection`

Plain-language precondition: the two arguments are exactly two-element integer
tuples; both endpoint pairs are ordered; the current module scope binds
`"intersection"` to a plain closure with parameters
`("interval1","interval2")`, exact submitted body, and parent module scope 0;
the builtins scope and every state cell needed by calls are fixed.

Plain-language postcondition: after actual fixed-semantics call, lookup,
argument evaluation, assignment, looping, return, and frame-pop execution, the
result is

```text
primeResult(minInt(A1,B1) -Int maxInt(A0,B0)).
```

All explicitly written caller cells are restored. `primeResult` is an
exhaustively defined total function producing one of the two concrete strings;
the destination is not a free variable, tautology, opaque result, or one-way
implication.

The trusted regenerated `solution.mpy` body and the `intersectionBody`
equation are constructor-for-constructor identical after only normalizing the
two surface spellings of the empty `.Stmts` unit: both normalized bodies have
693 characters. The independent checker is
`evidence/04_body_pinning.py`; its result is in
`evidence/04_pinning_and_witnesses.log`. The abbreviation only supplies the
closure body and does not replace its execution.

Ground satisfying substitutions were checked against the formal result and
both Python implementations:

- `(-3,-1),(-5,5)`: `L=2`, all return `"YES"`;
- `(0,4),(-2,8)`: `L=4`, all return `"NO"`; and
- `(8,10),(-4,3)`: `L=-5`, all return `"NO"`.

The same evidence file contains three satisfying loop states with the expected
final divisor and flag.

As an additional body-sensitivity check, the candidate-provided mutation was
inspected and then rerun independently against the fresh definition. Binding
the closure to `return "NO"` made the prime `"YES"` obligation fail with exit
1 and a residual containing `"NO"`; see
`evidence/04_body_mutation_check.log`. This probe is supporting evidence, not
a substitute for the constructor identity or positive K proof.

Stage result: **PASS**.

## 5. Rule-by-rule static soundness review

The exhaustive artifacts are:

- `evidence/05_numbered_k_sources.txt`: every line of all 24 supplied K files,
  `verification.k`, and `spec.k`;
- `evidence/05_rule_inventory.tsv`: every top-level configuration, syntax,
  context, rule, claim, relevant attribute, and opaque/symbol occurrence with
  file and line; and
- `evidence/05_static_assessment.md`: the reviewer’s per-class decision record
  and used-construct mapping.

The inventory contains 1 supplied configuration, 227 supplied syntax
declaration starts, 5 supplied contexts, 695 supplied rule starts, 3
candidate-local declarations, 6 candidate-local equations, and 2 claims.

### Supplied semantics

Every supplied entry is classified `TRUSTED_SUPPLIED_BASELINE`: recursive
comparison proves it is exactly the semantics selected by the rendered
`SUPPLIED_SEMANTICS` condition. This is the condition-defined semantics level,
not a claim that all 2,211 baseline lines implement all of CPython. No supplied
file contains any task-specific answer term.

The target’s complete used path was reviewed directly:

- syntax and sequencing for `Module`, `FuncDef`, `Params`, assignments,
  literals, calls, subscripts, comparisons, `If`, `While`, and `Return`;
- scope-chain lookup and the real builtins binding;
- callee-first then left-to-right argument evaluation;
- exact plain-frame allocation, parameter binding, return state, frame pop,
  environment restoration, and scope deallocation;
- in-bounds tuple indexing at 0 and 1;
- variadic integer `max` and `min`;
- integer subtraction, addition, comparison, and Python-style modulo with a
  positive divisor;
- Boolean truth, branch selection, while control, and loop continuation; and
- ASCII construction of `"YES"` and `"NO"`.

The configuration explicitly accounts for computation, current environment,
scopes and allocator, heap and allocator, stack, return state, exception state,
and exit code. The used rules preserve evaluation order and the state footprint
required by the claims.

The baseline has 50 priority annotations, but none can substitute a
task-specific operation: they govern cell/ref handling, allocation/mutation,
special float/math/hash/sort calls, and concrete collection legs. This target
uses plain frames, bare tuple values, integers, and generic calls.

The 25 explicit baseline opaque symbols are `sortVS`, `sortKeyVS`,
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`. None occurs in the program, candidate-local
helpers, proof claims, or their result path.

Fresh LLVM compilation warned that several trusted total helpers are
non-exhaustive. `mapStrVS`, float helpers, and `joinCodes` are unreachable.
`valSeqAt` is reached, but only for indices 0 and 1 of explicitly
two-element tuples, so its ordinary in-bounds equations determine the values;
the supplied out-of-bounds/opaque totality boundary is not exposed.

### Candidate-local extensions and claims

There are no candidate-local priority, `owise`, `concrete`,
`simplification`, `functional`, `symbol`, `no-evaluators`, or opaque
declarations.

- `intersectionBody` is a zero-argument total definitional abbreviation with
  one unconditional equation. It is exactly the translated body and does not
  rewrite an operational program term.
- The three `noDivisors` guards are exhaustive and pairwise disjoint over all
  integer pairs: `I<2`; `I>=2 and I>=N`; and `I>=2 and I<N`. The first
  redirects once to 2, the second is the empty-range truth, and the third
  checks a positive divisor and strictly advances toward the base region.
- The two `primeResult` guards are disjoint Boolean complements and exhaustive:
  `N>=2 and noDivisors(N,2)` produces `"YES"`; `N<2 or not
  noDivisors(N,2)` produces `"NO"`.
- The loop circularity matches the exact real `#while` control term and body,
  not a fabricated summary redex. Its one-step invariant equation is ordinary
  divisibility mathematics.
- The entry claim executes the pinned closure through fixed semantics and
  constrains the returned value through the fully defined `primeResult`.

No rule encodes the task answer, preempts or bypasses target execution,
fabricates a used construct, introduces an unconstrained result oracle, or has
a false conclusion on the intended domain. Accordingly, this audit makes no
unsound-rule allegation and no false-rule witness is required.

Stage result: **PASS**.

## 6. Fresh non-vacuity test

I inspected the candidate’s `spec-vacuity.k` only as untrusted evidence and
created a different reviewer-authored mutation:
`evidence/06_spec_vacuity_fresh.k` (identical scratch copy
`audit-spec-vacuity.k`).

Its ground arguments `(10,13)` and `(0,20)` satisfy both ordering
preconditions. Their intersection length is 3, so the trusted canonical,
candidate Python, formal `primeResult`, and real K execution all produce
`"YES"`. The mutation changes the result obligation to the demonstrably false
`"NO"`.

First:

```text
kprove audit-spec-vacuity.k \
  --definition /tmp/audit-work/127-intersection/build/verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
```

exited 0, proving that the mutation parsed and built successfully
(`evidence/06_mutation_build.log`).

The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual `<k>` contained
`str(iCons(89,iCons(69,iCons(83,...))))`, the ASCII codes for the actual
`"YES"` value, which cannot unify with the mutated `"NO"` destination. The
wrapper confirmed both the expected stuck residual and actual value in
`evidence/06_mutation_proof.log`.

This is a reachable unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or dead mutation.

Stage result: **PASS**.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics, for every two exact integer-pair arguments
with ordered endpoints, execution of the submitted function body is partially
correct: if the call terminates, it returns `"YES"` exactly when

```text
min(end1,end2) - max(start1,start2) >= 2
```

and no integer divisor from 2 through one less than that length divides it;
otherwise it returns `"NO"`. The proof also establishes the described loop
summary and restoration of the entry claim’s caller-state cells.

This is a theorem about real fixed-semantics execution. Differential testing,
the candidate’s `PROOF.md`, its logs, and its generation trace are not premises
of that theorem.

### Trusted and informal boundaries

- **Supplied reference semantics.** Trusted by the problem condition as the
  selected language model. Its used integer/tuple/call/control path was
  statically audited and concretely tested. Unused language features and
  behavior outside this subset are not claimed.
- **Trusted translator.** The mounted `py2mpy.py` is an input trust boundary.
  The submitted translation is byte-identical to its fresh output, and the
  proof body is constructor-identical to that output. The translator itself is
  not formally verified here.
- **K implementation and foundations.** The parser, compiler, reachability
  prover, Haskell/LLVM backends, SMT reasoning, and host arithmetic are trusted
  proof infrastructure.
- **Ordinary mathematical intent bridge.** The exhaustive recursive definition
  of `noDivisors(N,2)` for `N>=2` is the standard divisor characterization of
  primality. The prompt’s examples and canonical code confirm that interval
  length means coordinate difference. This reasoning is transparent and does
  not add a proof rule.
- **Opaque supplied primitives.** All 25 are inventoried above. None influences
  this theorem’s control, state, result, exception behavior, or postcondition,
  so no conclusion depends on an interpretation of them.
- **Empirical evidence.** The 25,428 Python comparisons support
  implementation-to-canonical alignment; fresh `krun` assertions support the
  used supplied-semantics bridge on representative cases. These finite checks
  do not replace universal K reachability.

Excluded are malformed tuples, non-integer endpoints, reversed intervals,
total-correctness/termination and complexity claims, and equivalence of unused
semantics features to full CPython.

All seven required stages pass. The proof reconstructs cleanly, executes and
pins the real trusted translation, has a satisfiable and result-constraining
specification, contains no material proof-local soundness gap, and rejects a
fresh false result mutation for the expected reason.

VERDICT: PASS
LEGITIMACY: LEGIT
