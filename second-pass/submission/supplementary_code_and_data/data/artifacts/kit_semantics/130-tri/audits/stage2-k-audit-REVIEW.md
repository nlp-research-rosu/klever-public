# Independent adversarial audit — HumanEval 130-tri

Decision: **PASS / LEGIT**. The candidate contains a fresh-reconstructible,
result-constraining partial-correctness proof of the submitted generated
program over the full stated domain of non-negative integers. I found no
task-answer semantic rule, execution-bypassing bridge, opaque result oracle,
domain narrowing, or material adequacy gap.

All candidate and generation records were treated as untrusted evidence.
Candidate compiled definitions and caches were never used. The exact reviewer
commands, statuses, and log locations are indexed in
`evidence/COMMANDS.md`.

## 1. Input and provenance integrity

`/audit-input.json` is readable and declares `record_layout =
pipeline-v3`, `semantics_mode = SUPPLIED_SEMANTICS`, problem `130-tri`, and
condition `kit-semantics`. The trusted `/reference/reference-semantics` tree is
present, so the mounts agree with the rendered semantics mode; there is no
infrastructure breach.

The independent checker in `evidence/provenance_check.py` established:

- `/audit-campaign-lock.json` has the launcher-recorded SHA-256
  `ad5dfc...8d745` and is JSON-equal to the `audit_campaign` block;
- `/run.json`, `/task.json`, `/generation-result.json`, invocation, metrics,
  runtime metrics, usage, prompt, last message, output log, and trace all have
  their launcher-recorded hashes;
- every pipeline-v3 evidence hash in both invocation and result agrees;
- trusted canonical, prompt, and translator hashes agree with
  `/audit-input.json`;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- the candidate and trusted supplied-semantics trees have the same 25 entries
  (one directory plus 24 regular files), identical paths, types, and file
  hashes;
- no symlink exists under candidate, reference, or generation-evidence; and
- all six required proof deliverables are regular, non-symlink files.

`evidence/candidate-files.sha256` independently hashes all 779 mounted
candidate files. The detailed provenance run is
`evidence/stage1-provenance.log`; its exit is 0 and final result is
`OVERALL=PASS`.

I also parsed all 408 JSONL events in the structured trace and scanned every
line of `codex-last.txt`, the 29,413-line `codex-output.log`, and `prompt.txt`.
The trace has 95 recorded tool calls and parses without error. Its historical
claims include an interrupted dependency-free entry diagnostic and a later
successful full proof; none of those claims is used as proof evidence here.
See `evidence/generation_trace_audit.py` and
`evidence/stage1-generation-trace-audit.log`.

Stage 1: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every non-negative integer `n`, return a list of the first `n+1` sequence
values. Index 0 is 1, index 1 is 3, each even index `i>=2` is `1+i/2`, and
each odd index `i>=3` satisfies
`t(i)=t(i-1)+t(i-2)+t(i+1)`. The documented example is
`tri(3) == [1,3,2,8]`.

The trusted canonical builds the sequence forward. The candidate uses the
equivalent closed forms while iterating `i=0..n`:

- 1 at index 0;
- 3 at index 1;
- `1+i//2` at even indices; and
- `(i//2+1)*(i//2+3)` at odd indices.

For `i=2k+1`, the odd formula is `(k+1)(k+3)`. The recurrence sum is
`(k+1) + k(k+2) + (k+2) = (k+1)(k+3)`, so the algorithm implements the
stated sequence.

Using only `/reference/py2mpy.py`, I regenerated `solution.mpy` in scratch.
The submitted and regenerated files are byte-identical and have SHA-256
`583efb...1262d` (`evidence/stage2-translation-identity.log`).

`evidence/differential_test.py` independently imports
`/reference/canonical.py::tri` and the candidate `solution.py::tri`. It tests
the documented/boundary values 0 through 5, every value 0 through 256, 200
deterministic generated values in 0 through 2000, and large boundaries through
10,000: 438 distinct inputs, zero documented-example mismatches, and zero
numeric/list-result mismatches (`evidence/stage2-differential.log`, exit 0).

The trusted canonical uses Python `/`, so elements from index 2 are integral
floats; the generated program returns equal-valued Python integers. This
produced type observations on 436 inputs but no list inequality. It is not a
contract defect: the prompt specifies sequence numbers, displays integer
results, and Python numeric/list equality equates these exact integral values.
The K theorem proves the generated program actually submitted, whose operations
are all integer operations.

Stage 2: **PASS**.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/reconstruction`, copied the
trusted semantics from `/reference`, and created new output definitions named
`fresh-runtime-kompiled` and `fresh-verification-kompiled`. No path under
`/candidate/*-kompiled` was copied or referenced. The live tools report K
v7.1.293.

Fresh concrete reconstruction:

- the trusted translator produced `audit-smoke.mpy` from the reviewer-authored
  `evidence/k_smoke.py`;
- LLVM `kompile` exited 0
  (`evidence/stage3-concrete-build.log`); and
- `krun` exercised `n=0,1,2,3,4,5,10` and ended with `.K`, `NoExc`, semantic
  exit code 0, and process exit 0
  (`evidence/stage3-concrete-run.log`).

Fresh proof reconstruction:

- Haskell `kompile` exited 0
  (`evidence/stage3-proof-build.log`);
- `tri-loop`, `tri-at-zero`, `tri-at-one`, `tri-at-even`, and
  `tri-at-odd-recurrence` each independently printed `#Top` and exited 0;
- the dependency-closed selection `tri-loop,tri-entry` printed `#Top` and
  exited 0; and
- the full six-claim command printed `#Top` and exited 0
  (`evidence/stage3-proof-all.log`).

The four mathematical claims emit `WarnTrivialClaim` because preprocessing
normalizes their arithmetic; that is a success diagnostic, not a stuck state.
Selecting only `tri-entry` removes `tri-loop` from the circularity set and
therefore unrolls the symbolic loop indefinitely. I interrupted that diagnostic
with exit 130. The proof architecture requires the loop circularity, and both
the minimal dependency closure and the intended full command close quickly.

Stage 3: **PASS**.

## 4. Adequacy and real-program pinning

The claims mean:

- `tri-loop`: for `N>=0` and `0<=I<=N+1`, an arbitrary list prefix `P` at a
  real loop head is extended by the values at indices `I` through `N`; `i`
  becomes `N+1`. Unrelated heap/scope entries and the continuation are framed.
- `tri-entry`: from the ordinary empty MPY module configuration, load the
  function, resolve `tri`, call it with any `N>=0`, return `ref(0)`, and leave
  exactly `list(triResult(N))` at heap location 0, with allocation counter 1,
  empty stack, `noRet`, `NoExc`, and exit code 0.
- `tri-at-zero` and `tri-at-one`: the two base values.
- `tri-at-even`: the even clause for every even `N>=2`.
- `tri-at-odd-recurrence`: the recurrence for every odd `N>=3`.

The entry precondition is satisfiable; `N=3` is a concrete witness. A loop
witness is `N=3, I=0, L=1, H=0, P=.ValSeq`, satisfying all loop guards. There
is no free return variable or one-way implication: the entry result is
`ref(0)`, and the entire heap value is constrained by the total definitions of
`triResult`, `triComplete`, and `triValue`.

Real-program pinning is mechanical. I parsed trusted regenerated
`solution.mpy` and separately parsed `Module(triDefinition)` with
`--expand-macros`. The JSON KAST files are byte-identical, both SHA-256
`5f37fe...654e` (`evidence/pinning-solution.ast.json`,
`evidence/pinning-claim.ast.json`, and
`evidence/stage4-constructor-pinning.log`). Thus the claim executes the same
function binding and body, not a substituted summary.

Reviewer ground claims reduce `triResult(0)`, `(3)`, `(4)`, and `(10)` to
explicit lists and close with `#Top`
(`evidence/ground-witness.k`, `evidence/stage4-ground-witness-k.log`). Those
lists equal both Python implementations numerically
(`evidence/stage4-witness-compare.log`).

Stage 4: **PASS**.

## 5. Rule-by-rule static soundness review

`evidence/K-INVENTORY.md` is a complete 302-KiB inventory generated by
`evidence/k_rule_inventory.py`. Its source-count cross-check is exact:

- 705 raw and parsed rule blocks;
- 233 raw and parsed syntax blocks;
- six raw and parsed claims;
- one configuration and five contexts;
- 467 equational, 193 operational, and 45 priority rules;
- 160 `function`, 118 `total`, zero `functional`, zero `simplification`, 36
  `concrete`, and 22 `no-evaluators` attribute occurrences.

Every inventory entry includes its full source text and an
`ACCEPT`, `BOUNDARY`, or `TARGET` disposition. Module-level rationales and the
constructor-to-rule map are in `evidence/USED-CONSTRUCTS.md`.

### Target execution

The path uses ordinary fixed rules for module loading, closure binding/name
lookup, left-to-right call argument evaluation, frame creation/parameter
binding, list allocation, assignment, integer literals, integer comparison and
arithmetic, nested branches, while control, bound-method dispatch, in-place
append, increment, return, and frame pop. Configuration cells, allocation
counters, mutation, exception state, stack, and return state are preserved or
explicitly constrained.

The applicable priorities are sound containment cases: heap-reference
dereference and list `append` preempt generic value/pure-method dispatch. Cell
priorities cannot match because this capture-free function has no `$cells`
binding. Strictness and contexts preserve source evaluation order. The body
contains no exception, break, continue, nested return, output, or external
effect that the loop claim could discard.

### Proof-local theory

The four AST aliases are parse-time macros, proven identical to the submitted
constructor tree. They are not operational rewrites. `triValue` has disjoint
and exhaustive negative/odd/even guards; its non-negative equations are exactly
the source branches. `triComplete` has disjoint/exhaustive `I>N` and `I<=N`
guards and descends under measure `N-I+1` while active. `triResult` starts the
fold at the empty sequence. There are no local priority rules, simplification
rules, concrete rules, opaque symbols, operational bridges, or task-answer
rules.

### Supplied boundaries

The 22 explicit opaque symbols implement supplied float, digest, and sort
support. Additional concrete-only float evaluators are also external
boundaries. None is syntactically reachable from this integer/list program,
none occurs in a claim or postcondition, and no successful claim depends on
one. `MPY-CONCRETE` is absent from the Haskell proof definition.

The supplied semantics documents partial-model exclusions such as unsupported
imports, exceptions for invalid operations, ASCII-only strings, out-of-bounds
access, nonzero range/slice steps, and non-escaping nested closures. The target
uses none of them. Its only divisor is literal 2, its list accesses are append
mutations, and its closure is module-level and capture-free. These limitations
do not enable a false conclusion for any state satisfying the entry
precondition.

I found no materially unsound rule and therefore make no unsoundness allegation
requiring a false-conclusion witness. As a separate operational-sensitivity
check, `evidence/body-sensitivity.k` changes the actually executed function term
to `return [99]` while retaining the original `[1]` obligation. It parses,
executes to heap `[99]`, and fails with `WarnStuckClaimState` and exit 1
(`evidence/stage5-body-sensitivity.log`).

Stage 5: **PASS**.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh
`evidence/fresh-false-result.k` uses the satisfying input `N=5`, executes
`Module(triDefinition)`, and changes only the final required element from the
true 15 to the false 16.

The mutation parsed and ran. `kprove` exited 1 with
`WarnStuckClaimState`; its residual is the fully terminated real program with
heap `[1,3,2,8,3,15]`, which does not unify with the mutated destination.
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. See
`evidence/stage6-fresh-false-result.log`.

Stage 6: **PASS**.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the supplied MPY definition and K implementation, for every K
integer `N>=0`, if the exact submitted translated function reaches termination
from the stated initial configuration, it returns a reference to a list
containing `triValue(0)` through `triValue(N)` in order. The proof also
establishes the base, even, and odd-recurrence equations for `triValue`.
Together these are the requested sequence contract over the unrestricted
non-negative-integer domain. This is partial correctness; termination and
resource bounds are not separately proved.

### Trust ledger

- **Trusted translator:** `/reference/py2mpy.py`. Its relevant CPython AST
  mappings were inspected; byte regeneration and expanded-KAST identity pin the
  submitted source to the executed term. Dependent fact: source/program
  identity.
- **Supplied MPY semantics:** all 24 trusted files, integrity-checked and
  exhaustively inventoried. Dependent fact: correspondence of K execution to
  the documented integer/list/function Python subset.
- **K toolchain:** K v7.1.293 compiler, Haskell backend, LLVM backend, integer
  hooks/solver, and reachability-logic implementation. Dependent facts: every
  machine-checked closure result.
- **Opaque supplied primitives:** 22 named float/digest/sort symbols plus
  concrete-only float helpers. Dependents in this proof: none; they have no
  value, control, state, or postcondition influence on the target.
- **Empirical bridge:** finite Python differential testing supports
  implementation/canonical alignment on 438 inputs and records the
  int-versus-integral-float type observation. It is not used in place of the
  universal K execution proof or the universal arithmetic recurrence claims.
- **Natural-language interpretation:** treating the prompt’s displayed
  integer-valued sequence as numeric values, not requiring the canonical
  implementation’s incidental float element types. This is supported by the
  prompt example, exact arithmetic, and Python’s stated/result equality
  behavior; it does not narrow the input domain.

Gate A (real-program soundness): **PASS**.  
Gate B (intent adequacy): **PASS**.  
Gate C (trust/evidence auditability): **PASS**.

VERDICT: PASS
LEGITIMACY: LEGIT
