# Independent adversarial review: 108-count-nums

## Audit conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I rebuilt both semantics definitions
from source, reconstructed all seven positive claims, mechanically pinned the
four closure terms in the proof to the regenerated `solution.mpy`, and obtained
the expected failures from fresh result and body mutations.

The classification is not an unqualified pass because the human-facing
interpretation of `countNumsSpec` depends on a result-bearing external
conversion contract: for every nonnegative integer, the supplied
`Int2String`/`strToCodes` primitive must produce its ordinary finite ASCII
base-10 digits. The candidate names that result `decimalCodes` and states the
dependency honestly. This is an acceptable low-level boundary rather than a
program-derived oracle: `str` is a fixed supplied primitive, the K theorem is
interpretation-parametric in its returned sequence, and the source body still
executes. But the universal ordinary-decimal property is not itself proved
inside K; only the fixed hook, concrete execution, and finite differential
evidence support the human-intent bridge. Under the benchmark decision boundary,
that is a non-fatal trust-boundary limitation.

## 1. Input and provenance integrity

The launcher declares `record_layout = pipeline-v3` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mode and mounts do not
contradict one another.

I independently checked the mounted records rather than following host-only
paths in `/audit-input.json`:

- `/audit-campaign-lock.json` is a regular file, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object is exactly equal to the `audit_campaign` block.
- All required pipeline-v3 records are present, regular, readable, and valid
  JSON or text as appropriate: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace.
- Every recorded single-file hash checked against its mounted file. The trace
  output hash also agrees independently with both `generation-result.json` and
  `invocation.json`.
- The one structured trace file contains 1,191 valid JSONL records and no
  malformed record. The full 1,375,234-character generation output was read
  and scanned. These records were treated only as untrusted generation claims.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- The candidate and trusted `reference-semantics/` trees each have 25 entries.
  Recursive type/path/content comparison found no missing, additional,
  mistyped, changed, special, or symlinked entry. Their independently computed
  manifest digests are both
  `fb82afa13469ffea33e06ad5a22b24e978d4c11da0cabb55d021f3e6f317fb8a`.
- A scan of the entire candidate tree found no symlink. I also computed
  independent manifests for the whole candidate and trace trees instead of
  relying on launcher aggregate digests whose serialization is not part of the
  proof.

Evidence:
[stage1-integrity-rerun.log](evidence/stage1-integrity-rerun.log),
[stage1-generation-records.log](evidence/stage1-generation-records.log), and
the reviewer scripts
[integrity_check.py](evidence/integrity_check.py) and
[generation_records_check.py](evidence/generation_records_check.py).

There is no audit-infrastructure breach. The scratch workspace
`/tmp/audit-work/108-count-nums-audit` was populated only with candidate source
artifacts and the trusted semantics/translator/reference sources. Candidate
compiled definitions and caches were not copied or used.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks for the number of elements in a finite integer array
whose signed digit sum is positive. For a negative number, only its first
decimal digit is negative: for example, the sum for `-123` is
`-1 + 2 + 3`.

The trusted canonical implementation converts the magnitude to decimal digits,
negates the first digit when required, and counts positive sums. The generated
`solution.py` implements the same operation imperatively:

1. iterate over each integer;
2. convert its magnitude to a string;
3. accumulate its digit values and remember the first nonzero digit;
4. for a negative input, subtract twice that first digit;
5. increment the result exactly when the corrected sum is positive.

Ordinary decimal integer strings have no leading zero except the representation
of zero, so the implementation's “first nonzero” accumulator equals the first
decimal digit on the intended domain. Zero contributes zero.

### Trusted regeneration

Running the trusted translator on the copied `solution.py` produced SHA-256
`35828b43a01410f15e3e246d26eeb1d1ac6630d72e76e878c2b7e5f611af3a20`,
exactly the hash of the submitted `solution.mpy`; `cmp` exited 0. See
[stage2-translate.log](evidence/stage2-translate.log).

### Independent differential test

The independent test imports the trusted canonical function and the generated
function separately and also evaluates a third mathematical signed-digit
oracle. Its deterministic input scope is:

- all three documented examples;
- eight curated groups covering empty input, zero, both signs, the
  `sum < 0`/`sum = 0`/`sum > 0` boundaries, powers of ten, 100-digit values,
  and values around `2**4096`;
- every list of length 0 through 3 over a 22-value boundary pool (11,155
  cases);
- 2,000 seeded random lists of length 0 through 20, including integers with up
  to 100 decimal digits and values around powers of ten.

All 13,166 cases matched among the canonical implementation, generated
implementation, and independent oracle. The ordered input digest was
`4504d88d4e2bf46fea1444221a8ed5006bf3e346eb5be603ee14541a923f5c8f`.

Evidence:
[differential_test.py](evidence/differential_test.py),
[differential-inputs.json](evidence/differential-inputs.json), and
[stage2-differential.log](evidence/stage2-differential.log). This is finite
fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

The available tools are K 7.1.293. The clean source hash record is
[stage3-scratch-source-hashes.log](evidence/stage3-scratch-source-hashes.log).

### Concrete definition

I translated a fresh assertion harness containing the exact submitted function
body and normal/boundary calls, then ran:

```text
kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled
krun audit-concrete.mpy --definition runtime-audit-kompiled
```

The fresh LLVM build exited 0. Concrete execution ended with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`. See
[stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log),
[audit_concrete.py](evidence/audit_concrete.py), and
[stage3-krun-concrete.log](evidence/stage3-krun-concrete.log).

### Proof definition and positive claims

I built the Haskell definition from the copied `verification.k` and trusted
semantics:

```text
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled
```

The build exited 0. The only warnings were unused variables in the trusted
semantics. See
[stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log).

The candidate intentionally proves six mutually supporting claims in one
command—the two structural loop circularities must be available together—and
the empty entry claim in a second command:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.digit-loop,SPEC.outer-loop-empty,SPEC.outer-loop-step,SPEC.call-setup-nonempty,SPEC.outer-loop-initial,SPEC.count-nums-nonempty
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.count-nums-empty
```

Both commands printed `#Top` and exited 0. Thus all seven positive claims were
independently reconstructed:
[stage3-kprove-six-mutual.log](evidence/stage3-kprove-six-mutual.log) and
[stage3-kprove-count-nums-empty.log](evidence/stage3-kprove-count-nums-empty.log).

For diagnostics, `digit-loop`, `outer-loop-empty`, and
`call-setup-nonempty` also close separately. `outer-loop-step` does not close
when selected alone because that selection removes the required inner-loop
circularity; its residual is preserved in
[stage3-kprove-outer-loop-step.log](evidence/stage3-kprove-outer-loop-step.log).
This is not a failed target reconstruction: the declared positive target is the
mutual six-claim command, and that complete set closes. A concurrent diagnostic
invocation once failed to detect Java; the exact same call-setup claim closed
sequentially with `#Top`, so the preserved parallel-attempt log is an
infrastructure-only observation, not candidate evidence.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `digit-loop` says that iterating the exact inner body over any remaining
  finite sequence of digit codes adds their numeric values to `digit_sum`,
  updates the first-nonzero accumulator, and leaves `char`/`digit` equal to the
  last visited code. Its premises require every code to be in `48..57`.
- `outer-loop-empty` says an exhausted outer loop follows the exact source
  `Return`, pops the exact call frame, restores the root environment, and
  returns the current count.
- `outer-loop-step` says processing one arbitrary integer head and an arbitrary
  all-integer tail with the exact source body returns the starting count plus
  `countNumsSpec` of that head and tail.
- `call-setup-nonempty` performs actual name lookup, call routing, frame
  creation, parameter binding, `count = 0`, and evaluation of the outer
  iterable. It summarizes no program result.
- `outer-loop-initial` connects that initial loop state, before temporary
  locals exist, to the recurrent outer-loop result.
- `count-nums-empty` executes the exact closure on the empty list and returns
  0.
- `count-nums-nonempty` executes the exact closure on
  `list(vCons(I:Int,R))`, requires `allInts(R)`, and constrains the returned
  integer by
  `?RESULT ==Int countNumsSpec(vCons(I,R))`.

The two entry claims cover every finite integer list: empty separately and an
arbitrary integer head with an arbitrary structurally recursive all-integer
tail. There is no length, digit-count, or integer-magnitude bound.

### Mechanical program identity

I parsed regenerated `solution.mpy` with the fresh K definition, extracted all
four `closureVal` occurrences in `spec.k`, wrapped each body back into a
`Module(FuncDef(...))`, and parsed those terms through K's rule parser. Every
constructor tree is exactly equal to the regenerated program tree. All five
terms have KAST SHA-256
`b10b646e84cc3f6c1c33ba73f67db876af5df18fa9989c1e01747185c7c318eb`.
This comparison also demonstrates that explicit `.Stmts` terminators in the
claim are parser normalization, not a different body.

Evidence:
[program_pinning.py](evidence/program_pinning.py) and
[stage4-program-pinning.log](evidence/stage4-program-pinning.log).

The control-flow claims contain the same loop bodies and exact suffix
`Return(Name("count")) .Stmts ~> #endcall`; the entry state pins the
`count_nums` root binding to the identical closure. No rule summarizes
`count_nums` by name, replaces the function body, or intercepts its call.

### Satisfiability and concrete substitution

The exact claim cells with input `[]` satisfy the empty precondition. Inputs
`[11]`, `[-11]`, `[-12]`, `[-12,0,11]`, and
`[-101,-102,999]` satisfy the nonempty precondition. Substituting these values
into the claimed recursive result under the named decimal contract gives,
respectively, `0`, `1`, `0`, `1`, `2`, and `2`; both Python implementations
produce the same values. See
[claim_witnesses.py](evidence/claim_witnesses.py) and
[stage4-claim-witnesses.log](evidence/stage4-claim-witnesses.log).

`?RESULT` is not a free or tautological result: its `ensures` equality binds it
to `countNumsSpec`. The fresh false postcondition in stage 6 is rejected.

### Body sensitivity

I made a separate fresh mutation inside the closure term actually executed by
the nonempty entry claim, changing only its `count` initializer from 0 to 1
while retaining the old postcondition. The mutated spec parsed successfully,
then `kprove` exited 1 with an implication residual showing the actual returned
summary is the old summary plus 1. The residual configuration contains the
mutated closure itself.

Evidence:
[make_body_mutation.py](evidence/make_body_mutation.py),
[audit-body-false.k](evidence/audit-body-false.k),
[stage4-body-mutation-diff.log](evidence/stage4-body-mutation-diff.log),
[stage4-body-mutation-dry-run.log](evidence/stage4-body-mutation-dry-run.log),
and
[stage4-kprove-body-mutation.log](evidence/stage4-kprove-body-mutation.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source inventory covers 26 K files and 975 top-level sentences:

- 724 rules;
- 238 syntax declarations;
- 5 contexts;
- 1 configuration; and
- 7 positive claims.

Of these, the recursively identical supplied semantics contributes 695 rules,
227 syntax declarations, all 5 contexts, and the configuration. Candidate
`verification.k` contributes 11 syntax declarations and 29 rules; `spec.k`
contributes the 7 claims. The inventory records every source span, normalized
sentence, attribute, file hash, function/total/no-evaluator declaration,
simplification, concrete/symbolic rule, priority, and `owise` rule in
[k-rule-inventory.md](evidence/k-rule-inventory.md). No local declaration uses
`functional`, and no candidate-local rule has a priority attribute.

The 695 fixed semantic rules are the selected trusted semantics level, not
candidate proof extensions. The recursive integrity check makes their exact
source the launcher-supplied baseline. I therefore classify each inventory
entry marked “trusted supplied semantics” as accepted at that semantics level,
not as an independently regenerated Python semantics. I nevertheless traced
every construct used by this program through the relevant fixed rules:

| Program construct | Declaration and material fixed behavior |
|---|---|
| `Module`, statement sequencing | `syntax.k:41-61`; `core.k:124-127` loads and sequences the exact statements left-to-right |
| `FuncDef`, closure and calls | `functions.k:14-20`; `call.k:20-32,69-74`; `functions.k:63-66,78-90` preserve lookup, argument evaluation, binding, stack/frame creation, return, scope removal, and caller restoration |
| `Name`, `Int`, `Str` | `core.k:131-154,194`; `str.k:13-17` perform normal scoped lookup and literal evaluation |
| `Assign`, `AugAssign` | `controls.k:9-31` write only the active scope and use fixed integer `applyBin` for updates |
| `If` | `syntax.k:49`; `controls.k:51-54` evaluates the guard before selecting one branch |
| outer and inner `For` | `controls.k:65-74`, `list.k:9-10`, and `str.k:8-10` consume exactly one head at a time and carry the remainder in the continuation |
| unary/binary/comparison operations | `operators.k:10-17,44-46`; `int.k:7-27` preserve operand evaluation and implement the used `-`, `+`, `*`, `<`, `==`, and `>` integer operations |
| `str(n)` and `int(char)` | `call.k:20-32`; `builtins.k:148-160` resolve the normal type bindings, convert integers to character sequences, and accept exactly digit-character singletons on this path |
| `Return` | `functions.k:78-90` sets the return state, pops the single exact frame, restores the caller, and removes the callee scope |

The entry claims start with an empty heap; this program allocates no source
container internally on the claim path. Local assignment changes only the
callee scope. The loop and return claims explicitly preserve or restore every
configuration cell: `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`,
`<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`.

Running the concrete harness under the proof definition as well as the fixed
LLVM definition produced the same normal result and state shape. See
[stage5-krun-proof-extensions-ground.log](evidence/stage5-krun-proof-extensions-ground.log).

### Candidate-local extension assessment

| Lines in `verification.k` | Declarations/rules | Classification and audit |
|---|---|---|
| 9-12 | `allInts` and its two equations | Sound total structural predicate. Empty/cons cases are exhaustive; recursion descends on the tail. It restricts entry inputs to exactly the prompt's integer-list domain. |
| 18-37 | `definedProjectInt`, `projectIntTotal`, cast ceiling and projection simplifications | Guarded sort-projection summary. Every result-bearing use is under `isInt`. On that domain, the cast and projected integer are identical. The concrete/symbolic orientations agree on overlap and the idempotence rule is valid. `[total]` gives an arbitrary extension off the guarded domain, but no entry/path conclusion uses that value; it introduces no false intended-domain equation. |
| 41-48 | guarded `applyCmp("<",V,J)` and `applyUn("-",V)` | Sound derived twins of the fixed `Int` rules. The `isInt(V)` guard exactly narrows the dynamic `Val` to the fixed integer match domain, and `projectIntTotal` then returns that same integer. They are pure function rules and skip no lookup, evaluation, state, exception, or control step. |
| 50-52 | `magnitude` | Sound, disjoint, exhaustive split of mathematical integers at zero. |
| 57-67 | opaque `decimalCodes`, `strToCodes(Int2String(N))` naming rule, and guarded `applyBuiltin("str",V)` | Result-bearing trusted external boundary. On nonnegative integers the fixed rule is `str(strToCodes(Int2String(I)))`; the candidate RHS is the same value under the named definition/contract. The dynamic twin applies only after normal binding/argument evaluation and changes no cell or continuation. It does not replace program-defined code. The absence of an in-K universal proof of the ordinary-decimal contract is the review's stated concern. |
| 69-78 | `allDigitCodes` and the `decimalCodes` digit fact | Constructor equations are sound, disjoint, exhaustive, and descending. The opaque-instance rule is true under the named standard decimal contract and is explicitly part of that same external boundary. It supplies exactly the premise needed for `int(char)`; it does not determine a task answer by itself. |
| 80-83 | `codeDigitSum` | Sound total structural sum of `(code - 48)` with strict descent. |
| 86-93 | `chooseFirst` | Sound model of the source accumulator. Empty, zero-accumulator, and nonzero-accumulator cases are disjoint/exhaustive; recursive cases descend. |
| 95-97 | `lastCode` | Sound total tail recursion for the final visited character. |
| 99-106 | `signedDigitSum` | Sound sign split. On negatives it subtracts twice the remembered first digit, changing that digit's positive contribution to negative; on nonnegatives it keeps the ordinary sum. Human decimal meaning is conditional on the external conversion contract. |
| 108-117 | `countNumsSpec` | Sound total structural count. Integer and noninteger head guards are complementary. The noninteger equation is a harmless totalization outside the entry domain; all intended uses take the integer equation. |

All structural guards are disjoint or have identical RHSs on overlap, all
recursive functions descend, and all `total` functions used on the proof path
have constructor/guard coverage. The candidate adds no priority rule, abrupt
return bridge, frame manipulation, heap allocation, exception rewrite, or
unconstrained result symbol.

The result-bearing `decimalCodes` value affects the inner loop, branches,
`signedDigitSum`, and final count. It appears in both execution and the summary,
so merely sharing the symbol would not prove ordinary-decimal meaning. What
makes the formal execution theorem legitimate is the narrower external-boundary
classification: the replaced operation is the fixed supplied `str` primitive,
not program-defined code, and the theorem remains parametric/conditional on
that primitive's returned sequence. The human interpretation additionally
assumes that the fixed hook has the stated ordinary-decimal contract.

I found no candidate rule for which a satisfiable intended-domain state yields
a concrete false conclusion under that fixed standard interpretation.
Accordingly, I do not label any rule unsound and do not invent a false witness.
The decimal issue is the narrower universal-evidence gap described above.

### Claim/circularity assessment

The `digit-loop` circularity consumes one `IntSeq` constructor before returning
to its invariant. The `outer-loop-step` circularity consumes one `ValSeq`
constructor before recurring. Their base cases execute the fixed iterator and
return rules. `call-setup-nonempty` and `outer-loop-initial` are exact
connection claims, not operational rules available in arbitrary contexts.
`outer-loop-empty` fixes the complete return suffix and exact one-frame stack.
Thus the mutual proof does not obtain `#Top` through an unguarded,
arbitrary-continuation shortcut.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh generator copied the
positive spec into `AUDIT-SPEC-FALSE` and made exactly one result mutation:

```text
ensures ?RESULT ==Int countNumsSpec(vCons(I, R)) +Int 1
```

No precondition, body, helper, or configuration cell changed. Input `[11]` is
a satisfying witness: the established/canonical result is 1, while the mutated
obligation requires 2.

The mutated claim set built successfully with `kprove --dry-run` (exit 0).
Actual proof then exited 1 with `WarnStuckClaimState`; the configuration unified
with the destination, but the implication check required
`countNumsSpec + 1 == countNumsSpec`. This is the expected unmet result
obligation, not a parse failure, timeout, missing import, or unrelated crash.

Evidence:
[make_false_mutation.py](evidence/make_false_mutation.py),
[audit-spec-false.k](evidence/audit-spec-false.k),
[stage6-mutation-diff.log](evidence/stage6-mutation-diff.log),
[stage6-mutation-dry-run.log](evidence/stage6-mutation-dry-run.log), and
[stage6-kprove-false-mutation.log](evidence/stage6-kprove-false-mutation.log).

The proof is non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY transition system plus the reviewed local extensions,
for every finite MPY list of mathematical integers:

- the exact regenerated `count_nums` closure, started in the entry
  configuration stated by `spec.k`, is partially correct;
- the empty list returns 0;
- a nonempty list returns the structurally recursive `countNumsSpec` value;
- `countNumsSpec` counts exactly the loop-computed signed sums relative to the
  code sequence returned by the fixed `str` primitive; and
- normal return restores the root environment and stack with no exception and
  exit code 0.

This is unrestricted over finite list length and mathematical integer
magnitude. It is partial correctness, not an independent termination/resource
proof or a theorem about CPython implementation limits.

### Trust ledger

| Boundary | Exact assumption and influence | Assessment |
|---|---|---|
| Supplied MPY semantics, including K integer/string hooks | Defines every fixed transition, mathematical integer operation, and `Int2String` behavior. All claims depend on it. | Acceptable foundational boundary for `SUPPLIED_SEMANTICS`; recursively integrity-checked and freshly rebuilt. |
| `decimalCodes` / standard nonnegative integer conversion | The fixed primitive returns a finite nonempty ASCII base-10 representation, with zero as `48` and no leading zeros. Its exact value controls loop characters, branches, and the result. | Legitimate external primitive boundary, but universally unproved inside this K development. This is the non-fatal concern. Concrete K execution and differential testing are finite support only. |
| Trusted `py2mpy.py` | The translator maps the Python AST to the submitted MPY constructors faithfully. | Acceptable source-to-model bridge here: byte-identical regeneration, constructor-level pinning, CPython differential evidence, and actual-body mutation all agree. It remains outside the K theorem. |
| K compiler, backend, solver, and standard mathematical hooks | Machine implementation correctly checks reachability and arithmetic constraints. | Ordinary proof-tool trust boundary. |
| Mapping “array of integers” to finite MPY `list(ValSeq)` with `allInts` | Captures the HumanEval material domain, excluding noninteger elements and infinite/non-list iterables. | Adequate, not a material narrowing of the stated source contract. |
| Differential/concrete tests | 13,166 Python cases plus fresh LLVM/Haskell concrete runs show no mismatch. | Reproducible finite evidence only; not used as a universal proof substitute. |

Gate A passes: the fixed program body executes, state/control are preserved,
the local equations are sound under the named external contract, and the
result/body mutations discriminate. Gate B passes for the full material
source-contract domain; its ordinary-decimal interpretation is explicitly
conditional. Gate C is reproducible and auditable, but the unproved universal
decimal-hook contract remains a documented trust-boundary limitation.

The fresh reconstruction, pinning, exhaustive inventory, and mutations support
legitimacy. The external decimal-intent bridge prevents an unqualified pass but
does not make a false conclusion provable or substitute a different program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
