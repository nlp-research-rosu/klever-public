# Independent adversarial review: 145-order-by-points

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program under the supplied MPY semantics. The
formal input domain is not finitely bounded or reduced to examples. The
qualification is that the entire ordering value comes from the supplied
semantics' opaque external primitive `sortKeyVS`: the mounted artifacts do not
contain a universal theorem connecting that symbol to Python's stable keyed
sort. The candidate states this boundary conditionally, and fresh concrete and
differential evidence supports it, so this is a non-fatal trust-boundary
limitation rather than a substituted-program or unsound-proof failure.

## 1. Input and provenance integrity

`/audit-input.json` declares `pipeline-v3`, problem
`145-order-by-points`, condition `kit-semantics`, and
`SUPPLIED_SEMANTICS`. `/reference/reference-semantics` is present, so the
trusted mounts do not contradict the rendered mode.

The audit campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` as parsed JSON. The lock's independently computed
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which matches the launcher record.

All required `pipeline-v3` records are readable regular files, and none of the
candidate, reference, or generation-evidence entries is a symlink. Independently
computed SHA-256 values match the launcher records for:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, and `usage.json`;
- `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the trace JSONL;
- the trusted canonical, prompt, and translator; and
- the candidate prompt and translator.

The six evidence paths listed by both `generation-result.json` and
`invocation.json` have their recorded hashes. The structured trace contains one
regular JSONL file with 340 valid JSON records; all 63 recorded function calls
and 63 outputs were traversed. The generation records claim success, but no such
claim was used as proof evidence. `usage.json`'s internal
`source_trace_sha256` does not equal the final mounted JSONL's file hash; the
launcher-owned result and invocation do record the actual mounted file hash.
This is an internal discrepancy in an untrusted usage claim, not a missing or
changed launcher mount.

The candidate and trusted `prompt.py` files are byte-identical, as are their
`py2mpy.py` files. A recursive, no-dereference comparison of
`candidate/reference-semantics` against the trusted tree exits 0. Both trees
have exactly one directory plus 24 regular K files and no additional,
mistyped, changed, missing, or symlinked entry. Per-file hashes and an
independent typed-tree manifest are in
`evidence/stage1_integrity.log`; the complete bounded trace inspection is in
the same log. There is no audit-infrastructure breach.

Evidence:

- `evidence/stage1_integrity.py`
- `evidence/stage1_run.sh`
- `evidence/stage1_integrity.log`
- `evidence/trace_commands.py`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every finite list of integers, return a new list ordered by ascending
decimal digit sum, preserving original order between equal keys. The trusted
canonical clarifies the negative convention: the leading decimal digit is
negative and the remaining digits are positive. Thus `-12` has key
`-1 + 2 = 1`, not `3`.

The submitted `solution.py` implements that convention arithmetically:

1. record the sign and replace a negative input by its magnitude;
2. repeatedly add the low digit while at least two digits remain; and
3. add the signed leading digit.

It calls Python `sorted(nums, key=digit_sum)`, whose stability supplies the
original-index tie rule. This is a different but extensionally equivalent
algorithm to the canonical string-based key.

### Trusted regeneration

In the isolated scratch tree, the exact command

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

exits 0. `cmp regenerated-solution.mpy solution.mpy` exits 0. Both files have
SHA-256
`3f4a344aae175b905b99c9da96328e1e037b70bf65b1270e311f72b6e3223435`.

### Independent differential test

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch-copied candidate. It also uses a
separate decimal-string key oracle. Its preserved input recipe covers:

- both documented examples;
- empty, singleton, zero, sign, 9/10, 99/100, loop, and large-integer
  boundaries;
- stability and negative-key ties;
- every list of lengths 0 through 4 over
  `(-12,-11,-10,-1,0,1,9,10,11,12)` (11,111 cases); and
- 2,000 deterministic generated lists with seed `14520260729`, lengths 0
  through 30, and integers through 512 bits or 151 decimal digits.

All 13,129 list cases and 19 scalar branch-boundary cases agree; mismatch count
is zero. The deterministic input-stream SHA-256 is
`74e085f32dd90b9aa020254a59f72767b08fb5257e2d03ed0182a69e501b3f36`.
This is finite fidelity evidence, not a replacement for the K proof.

Evidence:

- `evidence/stage2_run.sh`
- `evidence/stage2_fidelity.log`
- `evidence/differential_test.py`

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/145-order-by-points-002`. No candidate `*-kompiled`,
`__pycache__`, KORE output, proof log, or cache was copied or reused. K
v7.1.293 was used.

The LLVM definition was freshly built from
`reference-semantics/semantics.k` with main module `MPY-KRUN` and syntax module
`MPY-SYNTAX`; `kompile` exits 0. A reviewer-authored concrete program containing
the exact two function bodies and normal/boundary assertions runs to `.K`,
`NoExc`, and modeled exit code 0.

The Haskell definition was freshly built from `verification.k` with main
module `VERIFICATION`; `kompile` exits 0. Compiler output contains only
supplied-semantics exhaustiveness/unused-variable warnings. In particular, the
warnings concern symbols or variables outside the submitted program's used
domain.

The expanded constructor KORE parsed directly from `solution.mpy` and the KORE
for the claim macro `solutionModule` are byte-identical:

```text
547d18b54a37e78df259dec6d8dbb74a6aaa93a82b250782cb291e84f2da65d4
```

Each target was run under the fresh definition:

| Target selection | Exit | Required output |
|---|---:|---|
| `SPEC.digit-sum-loop` | 0 | `#Top` |
| `SPEC.digit-sum-loop,SPEC.digit-sum-function` | 0 | `#Top` |
| `SPEC.order-by-points` | 0 | `#Top` |
| complete `SPEC` | 0 | `#Top` |

The function claim needs the loop claim as its circularity, so the
dependency-correct function run selects both. An initial diagnostic selecting
the function alone omitted that circularity and was stopped; it is visible at
the end of `stage3_rebuild.log` and was not treated as candidate evidence. The
dependency-correct reruns all finish normally within their 300-second bounds.

Evidence:

- `evidence/concrete_probe.py`
- `evidence/stage3_rebuild.sh`
- `evidence/stage3_llvm_compile.log`
- `evidence/stage3_concrete_krun.log`
- `evidence/stage3_haskell_compile.log`
- `evidence/stage3_program_identity.diff`
- `evidence/stage3_program_identity.sha256`
- `evidence/stage3_positive_proofs.sh`
- `evidence/stage3_positive_proofs.log`

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.digit-sum-loop`

- Precondition: at the exact submitted loop head, environment 1 contains an
  arbitrary nonnegative `number = N`, arbitrary integer `sign = SIGN`, and
  arbitrary integer accumulator `total = S`.
- Postcondition: the loop terminates with `number = leadingDigit(N)` and
  `total = lowerDigitSumAcc(N,S)`, while preserving sign and the framed
  continuation/cells.

`SPEC.digit-sum-function`

- Precondition: a fresh module/builtin state loads the exact submitted two
  definitions and calls the actual `digit_sum` closure on any K integer `N`.
- Postcondition: the call returns `signedDigitSum(N)`, restores the module
  environment and call state, leaves the heap empty, and has no exception.

`SPEC.order-by-points`

- Precondition: a fresh module/builtin state loads the exact submitted two
  definitions and calls the actual `order_by_points` closure on
  `list(VS)`, where every member of the arbitrary finite `ValSeq` is a K
  integer.
- Postcondition: the call returns `ref(0)`, allocates exactly
  `list(expectedOrder(VS))` at heap location 0, increments `heapLoc` to 1,
  restores the call state, and has no exception.
- `expectedOrder(VS)` is not a free variable: its sole equation is
  `sortKeyVS(VS, closureVal("number", digitSumBody, 0))`.

The `<k>` terms therefore execute the submitted module, not a surrogate
summary call. Trusted translation plus the empty expanded-KORE diff
mechanically pins both bindings and bodies. The four proof-local body/module
macros are syntax-only abbreviations eliminated to that exact constructor
term.

The formal value domain is every finite list of mathematical K integers. It
does not impose a length or magnitude bound. Excluding non-integer K values
matches the prompt's integer-list contract. The entry theorem uses a fresh
heap, which models the isolated HumanEval call; it does not claim contextual
frame preservation for unrelated preexisting heap objects. This does not
narrow the contract's value domain or result.

Satisfying witnesses include:

- loop: `N=12, S=0, SIGN=-1`, yielding leading digit 1 and lower-digit
  accumulator 2;
- helper: `N=-12`, yielding key 1; and
- target: `[1,11,-1,-11,-12]`, yielding
  `[-1,-11,1,-12,11]`.

Both trusted canonical and submitted Python produce those target results.
Fresh LLVM execution of the exact bodies agrees, including empty, tie,
negative, zero, and loop-boundary inputs.

The reviewer-authored body-sensitivity claim changes the module term actually
executed by replacing `digit_sum` with `return 0` while retaining the
`signedDigitSum(12)` obligation. It builds, executes the changed closure, and
exits 1 with `WarnStuckClaimState`; the residual `<k>` value is 0. This is a
real body mutation, not an edit to a disconnected source file.

Evidence:

- `evidence/adequacy_witnesses.py`
- `evidence/stage4_adequacy_run.sh`
- `evidence/stage4_adequacy.log`
- `evidence/body_sensitivity.k`
- `evidence/stage4_body_sensitivity_proof.log`

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5_rule_inventory.txt` enumerates the complete text and source
location of every mounted supplied-semantics and candidate proof item. It
contains 26 K files, 1,128 top-level items, 234 syntax declarations, 715 rules,
five contexts, one configuration, and three claims. Attributes include 148
function declarations, 110 `total` declarations, 45 priority rules, 35
`concrete` rules, 26 `owise` rules, and 22 `no-evaluators` opaque declarations.
There are no `[simplification]` rules and no `[functional]` declarations.

The inventory was reviewed module by module:

- `syntax.k` declares every submitted constructor with the needed evaluation
  order: `If`, `Assign`, `AugAssign`, and `Return` use strictness; `BinOp`
  uses left-to-right `seqstrict`; `Compare` and `Call` use explicit contexts
  and routing.
- `core.k` supplies the configuration, module sequencing, lexical lookup,
  builtins frame, left-to-right argument evaluation, integer literals, heap
  allocation, and sequence helpers. Its direct `list(VS)` value is explicitly
  legal for read-only claim inputs.
- `operators.k` and `int.k` dispatch the used unary minus, integer
  comparisons, addition, multiplication, positive-divisor Python modulo, and
  floor division. The helper loop reaches `%` and `//` only after normalizing
  its divisor to positive 10 and its dividend to nonnegative.
- `controls.k` performs the used assignments, branch selection, while
  condition/body sequencing, and accumulator updates without an abrupt
  control effect.
- `functions.k` and `call.k` load the exact closures, resolve normal lexical
  and builtin bindings, bind the evaluated arguments, push/pop frames, and
  implement return. The candidate call fixes `digit_sum` in module scope and
  `sorted` in the builtins parent.
- `sort.k` implements the no-`reverse` keyed call by allocating
  `list(sortKeyVS(VS,KV))`. The actual argument shape is disjoint from its
  unkeyed and `reverse` rules.
- `concrete.k`, imported only by `MPY-KRUN`, invokes the real key closure
  once per element and uses stable insertion for the no-`reverse` concrete
  path used in reviewer probes.
- The remaining list, tuple, string, set, dict, range, iterator,
  comprehension, subscript, method, float, MD5, and assertion declarations
  were checked for rule overlap with the submitted constructor/operator/call
  shapes. Except for assertion and list construction in reviewer-only concrete
  probes, they are sort- or name-disjoint and cannot contribute to target claim
  closure. The other 21 opaque symbols (float/MD5/unkeyed-sort primitives) are
  not candidate-reachable. Compiler-reported totality gaps such as
  `mapStrVS` and out-of-bounds `valSeqAt` are likewise unreachable here.

### Candidate-local inventory

There are four exact syntax macros and 16 mathematical/predicate equations:

- `magnitude`: two disjoint, exhaustive sign guards.
- `leadingDigit`: disjoint one-digit, multi-digit, and negative-normalization
  guards. The multi-digit argument strictly decreases.
- `lowerDigitSum` and `lowerDigitSumAcc`: exhaustive sign/base/recursive
  cases; the recursive equation removes exactly the low decimal digit and
  adds it to the accumulator.
- `signedDigitSum`: disjoint sign cases, subtracting only the leading digit
  for negatives, exactly matching the canonical convention.
- `allInts`: empty, integer-head recursion, and guarded non-integer rejection;
  the cases cover `ValSeq` and the recursion structurally decreases.
- `expectedOrder`: one unconditional alias to the supplied keyed-sort symbol
  with the exact proved key closure.

The guards within each equation family are disjoint or agree, cover every use
under the declared `total` domain, and terminate. None is a priority,
`concrete`, simplification, or opaque rule. No local operational rule
intercepts `<k>`, skips a program-defined body, fabricates a return, or encodes
a fixed task answer.

The loop claim is a proved circularity at the exact real loop head. Its matched
continuation and framed cells are exactly as general as the claim itself, and
its body has no return, break, exception, frame pop, or state outside the
listed local bindings. The helper and target claims are proof obligations, not
installed execution rewrites.

### Supplied keyed-sort trust boundary

The only candidate-reachable opaque value is:

```text
sortKeyVS(ValSeq, Val) [function,total,symbol,no-evaluators]
```

The fixed rule's complete operational match is the already evaluated builtin
call
`#applyK(toCall(builtinV("sorted")),
(list(VS),kwV("key",KV),.Vals))`. It replaces the external Python builtin by
`#alloc(list(sortKeyVS(VS,KV)))`. It reads the evaluated sequence and callable,
allocates one result object, advances `heapLoc`, and preserves the surrounding
control/state cells. Its value determines the entire postcondition.

This is not program-defined code and was not added by the candidate. It is an
explicit fixed-semantics trusted primitive whose named contract is “stable
ascending sort by real calls to `KV`.” The theorem is
interpretation-parametric up to that exact symbol, and the report makes the
HumanEval ordering conclusion conditional on the contract. The exact helper
closure is still formally pinned and independently proved for every integer.
No circular use of a fresh candidate oracle occurs.

No mounted bridge-free universal theorem proves the primitive's stable-sort
contract or relates its symbolic value to the separate LLVM insertion
implementation. The concrete K run and broad differential suite are finite
evidence only. Because this boundary is explicit, fixed, external, and
conditional, it does not make the reconstructed reachability claims unsound;
its lack of a mounted universal validation theorem is the reason for
`CONCERNS` rather than `PASS`.

### Concrete false-conclusion witness outside the submitted path

The exhaustive review found one supplied-semantics defect outside the
candidate's call shape. The `reverse=True` concrete keyed-sort rule sorts
stably ascending and then `condRev` reverses the whole list, which reverses
equal-key elements. CPython preserves their original order. The ground witness
is:

```text
sorted([1,2], key=zero_key, reverse=True)
```

where both keys are 0. CPython returns `[1,2]` and the preserved Python probe
exits 0. `MPY-KRUN` produces `[2,1]`; the assertion ends with
`AssertionError`, modeled exit code 1, and process exit 1. This is the required
concrete false-conclusion witness for that rule combination.

It is not material to this candidate: the submitted AST has no `reverse`
keyword, the non-reverse and reverse `Vals` patterns are disjoint, and the
runtime-only `MPY-CONCRETE` module is excluded from the Haskell proof main
module. No false rule conclusion was found on the submitted no-reverse integer
domain.

Evidence:

- `evidence/rule_inventory.py`
- `evidence/stage5_rule_inventory.txt`
- `evidence/reverse_stability_probe.py`
- `evidence/stage5_reverse_probe.sh`
- `evidence/stage5_reverse_probe.log`
- `evidence/stage5_reverse_stability_krun.log`

## 6. Fresh non-vacuity test

The candidate's mutation file was not used. The fresh reviewer mutation
`evidence/fresh_nonvacuity.k` uses the satisfying prompt input and changes the
target result obligation from `expectedOrder(input)` to
`revVS(expectedOrder(input))`. Under the named sort contract, the real result
is `[-1,-11,1,-12,11]`; the mutation requires
`[11,-12,1,-11,-1]`.

The dry-run command builds and KORE-translates the mutation successfully with
exit 0. The actual `kprove` command exits 1, not by parser error, timeout,
missing import, or unrelated crash. It prints `WarnStuckClaimState`; the
residual implication explicitly requires
`revVSAcc(sortKeyVS(...),.ValSeq)` to equal `sortKeyVS(...)`. This is the
expected unmet result constraint. The original theorem is therefore
discriminating.

Evidence:

- `evidence/fresh_nonvacuity.k`
- `evidence/stage6_nonvacuity_run.sh`
- `evidence/stage6_mutation_build.log`
- `evidence/stage6_mutation_proof.log`
- `evidence/stage6_nonvacuity.log`

## 7. Proven versus assumed accounting

### Formally established by the reconstructed K proof

Under the Haskell `VERIFICATION` definition:

1. the exact submitted loop computes the stated leading-digit and
   lower-digit accumulator summaries for every nonnegative loop-head integer;
2. loading and calling the exact submitted `digit_sum` body on every K integer
   returns `signedDigitSum(N)` with normal control/state restoration; and
3. loading and calling the exact submitted `order_by_points` body on every
   finite all-integer `ValSeq` returns a fresh list whose contents are
   `sortKeyVS(VS, exact-digit_sum-closure)`.

This is a partial-correctness statement: it does not separately prove
termination. It is universal over finite list length and integer magnitude,
not an examples-only or bounded-unrolling theorem.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell backend, SMT reasoning, and reachability logic | All machine-checked claims | Ordinary toolchain trust; exact version and fresh commands recorded. |
| Builtin K integer/Boolean/map/list operations | Operational semantics and summary equations | Acceptable low-level mathematical/runtime boundary. Used only in standard, guarded cases here. |
| Trusted `py2mpy.py` | Source-to-`solution.mpy` bridge | Acceptable: launcher hash matches and fresh output is byte-identical. |
| Supplied MPY module/call/control/integer/heap rules | Execution of both program-defined bodies | Acceptable for `SUPPLIED_SEMANTICS`; candidate tree is identical to trusted baseline and relevant rules were statically reviewed. |
| Opaque `sortKeyVS(VS,KV)` stable-keyed-sort contract | Entire ordering/permutation meaning of `expectedOrder` and the target result | Legitimate external primitive, but concerning evidence limitation: conditional contract plus finite concrete/differential support, no mounted universal connection theorem. |
| Trusted canonical implementation and independent decimal-string oracle | Differential fidelity evidence only | Empirical support, never used to close a K claim. |
| Termination of intended finite-list Python execution | Interpreting the partial-correctness result as total behavior | Informal/empirical; not required by the claimed partial correctness. |

### Decision

Gate A passes: the real translated bodies execute, the key helper has a
universal exact execution claim, the target result is structurally constrained,
the program term is mechanically pinned, body sensitivity holds, and the fresh
false result is rejected.

Gate B passes: the theorem covers arbitrary finite integer lists with unbounded
integer magnitudes and matches the signed-leading-digit and stability intent
conditional on the supplied keyed-sort contract. There is no finite-size or
example-only narrowing.

Gate C has a non-fatal limitation: the symbolic keyed-sort primitive determines
the whole returned sequence, while its universal stable-sort contract is not
machine-checked by any mounted artifact. The boundary is explicit and external,
and 13,129 differential cases plus fresh concrete K execution support it. This
warrants `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

The unrelated `reverse=True` supplied-semantics defect is witnessed and
excluded from the submitted call shape and proof dependency graph. It does not
invalidate this theorem.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
