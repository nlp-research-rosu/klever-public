# Independent adversarial review: 150-x-or-y

## Executive decision

The candidate contains a legitimate partial-correctness proof of the submitted
program. I rebuilt both proof definitions from source, proved the loop claim
without the loop-summary rule, then proved the universal entry claim after
importing exactly that proved summary. Both positive targets exited zero and
printed `#Top`. The entry term is mechanically constructor-identical to the
trusted regeneration of `solution.mpy`; it is not a substitute algorithm or an
oracle. A reachable body mutation and an independent false-postcondition
mutation both compiled and failed on the expected result mismatch.

The contract is covered for every K integer `n` and arbitrary supplied-semantics
values `x` and `y`, not for finitely many sizes or a narrowed positivity
precondition. No material adequacy gap or soundness defect remains.

Commands, exit statuses, and artifact locations are indexed in
[evidence/COMMANDS.md](evidence/COMMANDS.md).

## 1. Input and provenance integrity

I first read `/audit-input.json`, including `record_layout`,
`container_paths`, all recorded hashes, and the `integrity` block. It declares
`legacy-selected-stage1` and `SUPPLIED_SEMANTICS`. I used the container paths,
not the host provenance paths.

The mounted inputs are internally consistent:

- `/audit-input.json` and `/audit-campaign-lock.json` are regular readable
  files. The campaign blocks are structurally equal and the lock's independent
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every record required for `legacy-selected-stage1` is present and regular:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  All recorded individual hashes match. All JSON records parse; the one JSONL
  trace parses as 604 structured records. Historical `runtime-metrics.json` is
  neither present nor required for this legacy layout.
- The candidate workspace's independently computed pipeline tree digest is
  `31b4566c19b2805f8b5ca6552daf9c2be7fc18f8fafcbe9eaeae88dd7828c749`,
  matching both the generation result and invocation. The trace tree digest
  matches `usage.json`. The audit file also preserves older composite hashes;
  I did not incorrectly compare those to the distinct pipeline tree algorithm.
- The trusted supplied semantics exists as required. Recursive inventories of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` have the same 25 entries, types, and file
  hashes. Neither tree contains a symlink or special entry. Their independently
  computed manifest tree digest is the recorded
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions. The canonical, prompt, and translator hashes also match
  `/audit-input.json`.

The generation logs and prior `KPROVE_PASSED` marker were inspected only as
untrusted historical claims and were not used to establish proof success.
There is no missing mount, malformed record, mode contradiction, or other
infrastructure breach. The full independent check and its zero status are in
[stage1-provenance.log](evidence/stage1-provenance.log); its implementation is
[check_provenance.py](evidence/check_provenance.py).

## 2. Program fidelity and candidate-versus-canonical checks

The prompt's contract is: given integer `n` and values `x,y`, return `x` if
`n` is prime and `y` otherwise. Thus integers below 2 are non-prime; `2` is
prime; and for `n >= 2`, primality is equivalent to having no divisor in
`[2,n)`.

`solution.py` implements exactly that trial division:

1. return `y` when `n < 2`;
2. test every integer divisor from 2 through `n-1`, returning `y` on the first
   zero remainder;
3. return `x` after exhausting the range.

Running the trusted translator on the scratch copy produced a byte-identical
`solution.mpy`; both files have SHA-256
`9e433dad65c9d0b01eb8a7ca08fbff0520c2c931235b4ba7561fc7878f8f81c0`
([regeneration log](evidence/stage2-regeneration.log)).

The independent differential test exercised 2,630 cases: both documented
examples, negative and empty-range boundaries, every branch class, primes,
composites with first and later divisors, 526 distinct fixed/seeded/generated
integers, and five `x,y` payload pairs including non-integers. The candidate
had zero mismatches against an independently coded mathematical primality
oracle ([script](evidence/differential_test.py),
[results](evidence/stage2-differential.log)).

The trusted canonical Python implementation differs for `n <= 0`: it only
special-cases `n == 1`, so its empty range returns `x` for non-positive
integers. There were 700 candidate/canonical result differences, all at
`n <= 0`. This is a defect in the canonical implementation relative to the
unrestricted prose contract, not a narrowing or defect in the candidate:
non-positive integers are not prime, and the candidate returns `y`. Candidate
and canonical agree throughout the usual positive-integer HumanEval domain.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/150-x-or-y-review` and did not
copy or use any candidate-provided compiled definition or cache. The available
toolchain is K/pyk 7.1.293 and Python 3.10.12.

Fresh reconstruction results:

| Target | Fresh action | Result |
|---|---|---|
| Concrete semantics | LLVM `kompile` of trusted `reference-semantics/semantics.k` | exit 0 |
| Concrete program | `krun` of a reviewer-authored translated test module | exit 0, final `.K`, `NoExc`, exit code 0 |
| Loop base definition | Haskell `kompile`, main module `X-OR-Y-VERIFICATION` | exit 0 |
| `loop_correct` | `kprove` against the base definition | exit 0, `#Top` |
| Summary definition | Haskell `kompile`, main module `X-OR-Y-SUMMARY` | exit 0 |
| `main_correct` | `kprove` against the summary definition | exit 0, `#Top` |

The concrete test executes the actual translated module on normal and boundary
inputs including `-3,0,1,2,4,7,9,15,49,97`, with assertions matching Python.
Its source and translation are
[concrete_audit.py](evidence/concrete_audit.py) and
[concrete_audit.mpy](evidence/concrete_audit.mpy); the execution is
[stage3-krun-concrete.log](evidence/stage3-krun-concrete.log).

The positive proof logs are
[stage3-kprove-loop.log](evidence/stage3-kprove-loop.log) and
[stage3-kprove-main.log](evidence/stage3-kprove-main.log). Fresh compile logs
are linked from the command index. Compiler warnings concern unused variables
or imported total functions; none is a failed target or an operation reached by
this program.

## 4. Adequacy and real-program pinning

### Claim meanings

`loop_correct` assumes `N >= 2` and `D >= 2` and an exact reachable function
frame: the range iterator starts at `D` and ends before `N`, locals are
`divisor=OLD,n=N,x=X,y=Y`, the continuation is exactly the translated
`Return(x)` followed by `#endcall`, the heap is empty, and there is one call
frame with no exception. It proves that the loop and suffix pop the frame,
return `primeSelect(N,D,X,Y)`, and update `divisor` to the exact last value
`scanLast(N,D,OLD)`, while preserving the rest of the complete configuration.
For example, `N=9,D=3,OLD=2,X=1,Y=2` is a concrete reachable state after the
non-dividing iteration at 2.

`main_correct` has no restrictive side condition. From the supplied semantics'
exact initial state, it executes `#xOrY(N:Int,X:Val,Y:Val)` and proves the
returned K value is `primeSelect(N,2,X,Y)`. The postcondition is an equality to
a recursively defined result, not a free variable, tautology, implication, or
existential escape.

### Mechanical program identity

I parsed the regenerated `solution.mpy`, expanded `xOrYBody`, and expanded a
ground `#xOrY` with `kast`, then compared constructor trees rather than source
text. There is exactly one translated `FuncDef`; its name and parameters match;
the macro-expanded body is exactly the translated body; the entry closure uses
that body, the same ordered parameters, module environment 0, and unchanged
arguments. The body reads only `divisor,n,range,x,y`; it does not read its own
module binding `x_or_y`. Therefore invoking the exact closure rather than first
executing the `Module(FuncDef(...))` binding is a semantically inert
normalization for this body: `range` resolves from the same builtins parent and
the omitted self-binding is unused. See
[constructor_compare.py](evidence/constructor_compare.py) and its
[passing log](evidence/stage4-constructor-compare.log).

Ground instances for `n=7,15,1,0,-3` all prove `#Top` with the contract's
concrete result ([adequacy-ground.k](evidence/adequacy-ground.k),
[log](evidence/stage4-ground-claims.log)). These instances are witnesses and
cross-checks; the actual theorem remains universal.

For body sensitivity, I separately compiled a mutation of the program term
that returns `x` instead of `y` on a found divisor. At the reachable
`N=9,D=3,OLD=2,X=1,Y=2` state, the original result obligation requires `2`,
but the mutated body produces `1`; `kprove` exits 1 with
`WarnStuckClaimState`. See
[body-mutation-verification.k](evidence/body-mutation-verification.k),
[body-sensitivity.k](evidence/body-sensitivity.k), the
[compile log](evidence/stage4-kompile-body-sensitivity.log), and the
[valid failing proof](evidence/stage4-body-sensitivity-valid.log). An earlier
structurally invalid probe is preserved in `stage4-body-sensitivity.log` and is
explicitly excluded from the evidence.

## 5. Rule-by-rule static soundness review

The complete mechanical inventory is
[rule-inventory.tsv](evidence/rule-inventory.tsv), generated by
[build_rule_inventory.py](evidence/build_rule_inventory.py). It covers all 26
K source files used here—top-level supplied semantics, every helper, the
candidate verification module, and the claims—and gives a source location,
text, attributes, reachability class, decision, and justification for each of
1,119 items. Counts are:

- 706 ordinary rules, 232 syntax declarations, 5 contexts, 1 configuration,
  and 2 reachability claims;
- 147 function declarations, including 107 `total` declarations and no
  `functional` declarations;
- 25 opaque-symbol declarations, 46 priority items, and no simplification
  rules.

The 25 opaque declarations are supplied float, sort, and hashing primitives.
None is reachable from `solution.mpy`. The selected supplied semantics is the
fixed semantic level for this condition; exhaustive inventory confirms that
the candidate neither changed it nor added an opaque/concrete twin there.

Every material submitted constructor is mapped to its declaration, rules,
evaluation order, and state effect in
[task-path-map.md](evidence/task-path-map.md). The used path has ordinary
left-to-right call/argument evaluation, parameter and local-scope binding,
positive-step `range` iteration, integer comparison, positive-divisor Python
modulus, conditional choice, return/frame restoration, and exact loop target
updates. It uses no heap allocation, I/O, exception-producing operation,
floating point, sort, hash, collection, subscript, import, or opaque symbol.
The configuration cells and state footprint are consistent throughout.

All proof-local declarations and rules are individually analyzed in
[verification-rule-analysis.md](evidence/verification-rule-analysis.md):

- `xOrYLoopBody`, `xOrYBody`, and `#xOrY` are transparent syntax macros.
  Constructor comparison proves they preserve the actual program and call.
- `primeSelect` has four disjoint guarded equations: `N<2`, exhausted range,
  zero modulus, and nonzero-modulus recursion. `scanLast` has the corresponding
  three loop-state equations. On every use `D>=2`; guards cover all cases,
  disagreeing right sides do not overlap, and recursive calls strictly increase
  `D` while `D<N`.
- There are no proof-local `total`, `functional`, `simplification`, `concrete`,
  `owise`, or opaque declarations.
- The sole proof-local priority rule is the exact loop summary. Normalized
  claim and rule bodies match line-for-line. Its source location occurs zero
  times in the base definition used to prove `loop_correct` and once in the
  summary definition used for `main_correct`
  ([separation log](evidence/stage5-loop-bridge-separation.log)). Thus it cannot
  prove itself. It has an exact continuation, stack, environment, scope, heap,
  exception, location counters, exit code, guards, and updates; it is not an
  over-broad shortcut.

No rule encodes a task answer, fabricates an unconstrained value, bypasses a
used operation, or yields a false conclusion on the intended domain. Therefore
there is no claimed unsound rule requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh
[spec-vacuity.k](evidence/spec-vacuity.k) starts from the satisfying initial
input `n=7,x=34,y=12` but changes the result-constraining postcondition to the
demonstrably false value `12`. The mutation parses and builds: `kprove
--dry-run` exits 0 and emits the backend command
([dry-run log](evidence/stage6-vacuity-dry-run.log)). The real proof then exits
1 with `WarnStuckClaimState`; its residual `<k>` contains the actual result
`34`, which cannot match `12`
([proof log](evidence/stage6-vacuity-proof.log)). This is the expected reachable
unmet obligation, not a parser error, timeout, import failure, or unrelated
crash.

## 7. Proven versus assumed accounting

What is proved is the following partial-correctness statement inside the exact
supplied MPY semantics: for every K integer `N` and every `Val` pair `X,Y`, a
call of the constructor-identical submitted `x_or_y` body from the initial
configuration returns `primeSelect(N,2,X,Y)` without an exception. The
definition of `primeSelect` selects `Y` for `N<2` or when any integer in
`[2,N)` divides `N`, and selects `X` only after that entire interval is
exhausted. By ordinary integer mathematics, this is exactly “`X` iff `N` is
prime, otherwise `Y`.”

The trust and evidence boundaries are:

- **Trusted translator and mounted source provenance:** accepted inputs under
  the benchmark. Translation was nevertheless rerun and compared bytewise.
- **Exact supplied semantics:** the selected semantic level, independently
  integrity-checked against the trusted tree. The target uses its integer,
  Boolean, range, scope, call, return, Map, and List machinery.
- **K 7.1.293 parser, compiler, Haskell prover, LLVM execution backend, and
  builtin integer operations:** the unavoidable low-level proof-tool trust
  boundary. Both definitions were rebuilt, not reused.
- **Supplied opaque float/sort/hash symbols:** present in the baseline but
  unreachable from the entry term, so they cannot support this conclusion.
- **Proof-local mathematical summaries:** not opaque assumptions. Their
  equations are guarded and executable, and the operational bridge is imported
  only after its identical reachability claim closes in a definition that does
  not contain the bridge.
- **Source-to-entry normalization:** supported by exact KAST equality, parameter
  and argument equality, free-name analysis, concrete module execution, and a
  mutation of the actual executed body. The only omitted module effect is an
  unused self-binding.
- **Primality interpretation:** the elementary informal theorem that an integer
  `N>=2` is prime exactly when no integer `2 <= D < N` divides it. This is not a
  hidden computational oracle.
- **Differential and ground testing:** empirical corroboration of translation,
  Python behavior, and concrete instances only. It is not counted as the K
  proof and does not replace the universal claims.
- **Trusted canonical discrepancy:** for `N<=0`, the canonical implementation
  conflicts with the prose notion of primality. The proof establishes the
  submitted program and the prose contract; it does not incorrectly claim
  equivalence to that canonical edge-case behavior.

These boundaries are either mandated low-level trust or independently checked
bridges; none assumes the desired correctness conclusion or materially limits
the source-contract domain.

VERDICT: PASS
LEGITIMACY: LEGIT
