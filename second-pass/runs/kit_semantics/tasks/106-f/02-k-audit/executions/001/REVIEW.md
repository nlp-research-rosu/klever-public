# Independent adversarial review — HumanEval 106-f

The candidate contains a legitimate partial-correctness proof under the
supplied MPY semantics. I did not rely on the candidate’s compiled
definitions, `#Top` logs, `PROOF.md`, generation trace, or final report. The
proof and concrete semantics were rebuilt from source in
`/tmp/audit-work/reconstruction`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `106-f`, and condition
`kit-semantics`. The rendered mode is consistent with the presence of
`/reference/reference-semantics`.

All required pipeline-v3 records are regular, readable, non-symlink files:
`/run.json`, `/task.json`, `/generation-result.json`, invocation/metrics/
runtime-metrics/usage, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and
the one-file structured trace. All 384 structured-trace lines parse as JSON.
The trace and generation prose were inspected only as untrusted construction
claims.

The campaign block in `/audit-input.json` equals
`/audit-campaign-lock.json`, whose independently computed SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All 15 directly declared file hashes checked by the reviewer match. The
independent pipeline tree hash for the mounted candidate is
`fc500de9d9017d91c43a6b74791a11424341f40c9247955198439e192347cef6`,
matching the stage result’s workspace hash. The trace tree hash is
`989ebe528e7a5d4aa917f6128cc6f178fa2ea84c384c87d4e469bf8ef27879bf`,
matching `usage.json`; the trace file’s direct hash also matches the stage
result.

The candidate prompt and translator are byte-identical to their trusted
mounts. A recursive path/type/content manifest comparison proves that all 25
entries in candidate `reference-semantics/` exactly equal the trusted tree;
neither tree contains a symlink or unsupported node. Both trees independently
hash to
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`
under the pipeline tree algorithm. Required proof artifacts inside
`/candidate` are present and regular.

Reproducible checks and bounded output are in
`evidence/integrity_check.py` and `evidence/stage1-integrity.log`.
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for an integer-size list whose one-based position
`i`, for `i = 1..n`, is `i!` when `i` is even and
`1 + ... + i` when `i` is odd. Thus the meaningful size domain is
nonnegative integers. The example is
`f(5) == [1, 2, 6, 24, 15]`; `n=0` yields the empty list.

The trusted canonical implementation recomputes each factorial or sum using
an inner `for` loop. The submitted implementation uses running accumulators:
before each append it updates `fact *= i` and `total += i`, then appends the
former on even `i` and the latter on odd `i`. This is a different but
extensionally equivalent algorithm over the intended domain.

Trusted regeneration with

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

is byte-identical to submitted `solution.mpy` (`cmp` exit 0).

The reviewer-authored differential test imports the scratch copies of the
trusted canonical entry point and submitted entry point independently. It
checks the empty boundary, every early parity/branch boundary, the prompt
example, larger fixed values, and a deterministic generated sample through
150: 80 distinct intended-domain cases, zero mismatches. As an observation
outside the formal contract, both Python implementations also return `[]` for
the tested negative integers. See `evidence/differential_test.py` and
`evidence/stage2-fidelity.log`.

## 3. Clean proof reconstruction

Only source artifacts were copied to scratch. Candidate
`runtime-kompiled/`, `verification-kompiled/`, caches, pyc files, proof
outputs, and mutation outputs were not copied or reused. The trusted
semantics tree and trusted translator were used.

K v7.1.293 freshly compiled the supplied concrete semantics with LLVM and the
candidate proof definition with Haskell. Both `kompile` commands exited 0.
LLVM reported only known non-exhaustive warnings in unused fixed helpers and
unused variables in `str.k`; Haskell reported only the same unused `str.k`
variables.

Fresh concrete K execution at `n = 0, 1, 2, 5, 10` exited 0, ended with
`NoExc` and exit code 0, and produced exactly the Python lists. This includes
the empty boundary, both branches, the prompt example, and multiple loop
iterations.

The focused loop claim independently closes:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
#Top
exit 0
```

The complete positive suite closes both the helper circularity and target
entry claim:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
#Top
exit 0
```

A diagnostic selection of only `SPEC.f-correct` exits 1 because that command
also removes the loop-invariant claim from the proof theory. Its residual is
the first unclosed loop step. This confirms the intended dependency on the
auxiliary circularity; it is not the positive two-claim suite, which closes.
Exact commands, statuses, and bounded outputs are in
`evidence/stage3-reconstruction.log`.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`SPEC.loop-invariant` begins at the exact internal `#while` for the submitted
guard and body. Its state has current environment `L`, parameter `n=N`, result
reference `H`, current accumulators `F,T`, current index `I`, and heap sequence
`VS`. Its precondition is `I >= 1` and `N >= I-1`. It removes the loop and
sets:

- `i` to `N+1`;
- `fact` to `factRun(I,N,F)`;
- `total` to `totalRun(I,N,T)`; and
- heap object `H` to `resultRun(VS,I,N,F,T)`.

All framed scopes, heap entries, continuation, and other configuration cells
are preserved. A reachable satisfying witness is the state immediately after
the four initial assignments for `n=0`:
`L=1, H=0, N=0, I=1, F=1, T=0, VS=.ValSeq`, with parent scope 0. Its
precondition reduces to `1>=1` and `0>=0`.

`SPEC.f-correct` starts before lookup/call in module environment 0 with `f`
bound to the exact one-parameter closure, empty heap, `heapLoc=0`,
`scopeLoc=1`, empty stack, `noRet`, `NoExc`, and arbitrary integer `N>=0`.
It returns `ref(0)`, restores the caller control state, advances `heapLoc` to
1, and constrains heap location 0 to
`list(resultRun(.ValSeq,1,N,1,0))`. The initial configuration with `N=0`
is a direct satisfying witness.

### Program identity and result constraint

The entry claim intentionally begins at the bound function, rather than at
module loading. This is legitimate because pinning was checked mechanically:
fresh `krun` loaded regenerated `solution.mpy`; the reviewer extracted the
unique resulting runtime `closureVal`; `kast` parsed the literal `closureVal`
from `spec.k`; their fully expanded constructor trees are equal. This includes
the parameters, all assignments, exact while guard/body, both append branches,
increment, return, and defining environment. See
`evidence/pinning_compare.py` and `evidence/stage4-adequacy.log`.

The return is not free or tautological: it is fixed to `ref(0)`, and the full
heap sequence is fixed by exhaustive recursive equations. Ground K summary
checks at `N=0` and `N=5` close with `#Top` and produce respectively `[]` and
`[1,2,6,24,15]`, equal to both Python implementations. The ground artifact is
`evidence/spec-summary-witness.k`.

The `N>=0` precondition does not materially narrow the source contract:
“list of size n” and the specified positions `1..n` give a nonnegative
integer-size domain. Negative sizes and non-integer Python objects are not
contract inputs.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.txt`, generated by
`evidence/inventory_k.py`, is an exhaustive source-level inventory:

- 25 K source files;
- 230 syntax declarations;
- one configuration and five contexts;
- 709 rules (695 supplied, 14 proof-local);
- 148 function declarations, 110 `total` attributes, no `functional`
  declaration;
- 42 `concrete`, 26 `owise`, 45 priority, and seven simplification rules.

`evidence/static-review.md` assigns every inventoried entry to a file-level
decision, maps every construct used by `solution.mpy` to its declarations and
rules, and separately reviews all 14 proof-local rules.

The material supplied rules execute real module/function binding, lookup,
argument evaluation, parameter binding, scope/frame changes, assignments,
unbounded integer arithmetic, guard evaluation, while/if control, list
allocation, in-place append, return, and frame restoration. Evaluation order
and continuation handling match the submitted program. Heap allocation and
append are explicitly tracked by the claim. No material priority rule changes
the value or discards control.

The proof-local theory contains no rule matching `<k>`, operational bridge,
priority rule, abrupt control, fresh result, or opaque theorem-specific
oracle. Its three functions are:

- `factRun`: the exact remaining `fact *= i` fold;
- `totalRun`: the exact remaining `total += i` fold; and
- `resultRun`: the exact even/odd append fold while advancing both
  accumulators.

Their base/step guards are exhaustive and pairwise disjoint. Recursive steps
increase `I`, decreasing `max(N-I+1,0)`. Every simplification is the exact
defining equality in reverse under the same guard. The three
`no-evaluators` annotations do not create opacity: exhaustive equations fix
every use.

The supplied semantics has 22 fixed `no-evaluators` opaque boundaries in
float/sort/md5 support, plus deliberately partial helpers for unrelated
Python features. None occurs in the submitted term, claims, summaries, path
conditions, or result. `MPY-CONCRETE` is absent from the Haskell proof
definition. Per the required witness standard, these off-path fixed
limitations are not labeled theorem unsoundness: no intended-domain input can
route this program through them or let their interpretation affect its result.

No inventoried material rule enables a false conclusion on `N>=0`, so there
is no unsoundness witness to report.

## 6. Fresh non-vacuity test

The reviewer did not reuse candidate `spec-vacuity.k`. The fresh
`evidence/audit-spec-vacuity.k` preserves the exact submitted closure,
precondition, helper claim, return reference, and cells, but changes only the
result obligation to require a leading `42`.

`N=0` satisfies the entry precondition, while the real result is empty.
`kprove --dry-run` exits 0, proving that the mutation parses and builds. The
actual proof reaches the final state and exits 1 with
`WarnStuckClaimState`; its residual is exactly:

```text
resultRun(.ValSeq,1,N,1,0)
= vCons(42,resultRun(.ValSeq,1,N,1,0))
```

under `N>=0`. This is the expected unmet result obligation, not a parser
error, timeout, crash, or unreachable mutation. Full bounded evidence is in
`evidence/stage6-vacuity.log`.

## 7. Proven versus assumed accounting

Formally established under the fresh Haskell definition: for every K integer
`N>=0`, the exact submitted closure, starting from the stated initial cells,
has the claimed partial-correctness result. If execution terminates, it
returns `ref(0)` whose heap object is exactly the recursive sequence produced
by the submitted loop, with the stated allocation, scope, stack, return,
exception, and exit-code state. The loop claim universally connects every
source iteration to the three summaries.

Trust and informal boundaries are:

1. The byte-verified supplied MPY semantics, including ordinary K
   integer/Boolean/map/list hooks, is trusted as the intended model for the
   exercised Python subset. It affects value, control, and state. Fresh LLVM
   comparisons support—but do not prove—its Python fidelity.
2. The trusted `py2mpy.py` translator is trusted. Byte regeneration and the
   constructor-level runtime/spec comparison provide direct program-identity
   evidence.
3. K v7.1.293 and its frontend, Haskell prover, LLVM backend, and host runtime
   are the standard machine-checking trust boundary.
4. Ordinary mathematical induction identifies `factRun` with the product
   `1*...*i`, `totalRun` with `1+...+i`, and `resultRun` with the requested
   parity-indexed sequence. This intent bridge follows directly from the
   displayed exhaustive equations; it is not supplied by differential tests.
5. The 80-case Python differential and five LLVM runs are finite adequacy
   evidence only. They do not replace the reachability proof.

There is no result-bearing external primitive, empirical oracle, or informal
assumption inside the proof theory. Excluded claims are total correctness,
resource bounds, all of CPython, and behavior outside the nonnegative-integer
source domain.

All seven stages pass. The clean proof is sound, result-constraining, covers
the material source-contract domain, and mechanically pins the real generated
program.

VERDICT: PASS
LEGITIMACY: LEGIT
