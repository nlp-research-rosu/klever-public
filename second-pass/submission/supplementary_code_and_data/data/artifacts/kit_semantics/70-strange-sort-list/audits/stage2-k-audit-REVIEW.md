# Independent adversarial audit: 70-strange-sort-list

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over the full stated domain of finite integer
lists. I reconstructed both positive claims from source, verified exact
constructor-level program pinning, and obtained meaningful failures from fresh
result and body mutations.

The qualification is that the formal postcondition deliberately retains the
supplied semantics' opaque `sortVS(VS)` primitive. The K proof does not prove
that this value is an ascending permutation. That supplied-builtin contract,
plus the ordinary mathematical step from alternating endpoints of an ascending
permutation to repeated minimum/maximum selection, is an explicit conditional
intent bridge supported only by finite execution evidence here. This is a
non-fatal trust-boundary limitation and therefore maps to `CONCERNS / LEGIT`
under the benchmark's decision rule.

## 1. Input and provenance integrity

The launcher declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, and condition `kit-semantics`.
The trusted `/reference/reference-semantics` mount is present, so the trusted
mounts agree with the rendered mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and every required pipeline-v3
generation record: `invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the JSONL structured trace. The trace has
436 valid JSON records and no malformed line. The generation narrative and its
old `#Top` results were treated only as untrusted claims.

Independent checks found:

- The campaign-lock JSON equals the `audit_campaign` block, and its SHA-256 is
  the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All required records and mounts are real, readable files/directories, all
  launcher-owned mounts report `ro`, and no symlink or special node occurs
  below the candidate, supplied-semantics, or trace trees.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts. Their respective hashes are
  `431d1a56bd425ed0718c9996fd486badefa4547c69e80bc5e81526cec2abae70`
  and
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- `diff -r --no-dereference` found no difference between candidate and trusted
  `reference-semantics/`. Both trees have exactly the same 25 regular files,
  relative paths, modes, and per-file hashes; there are no additional,
  missing, mistyped, or linked entries.
- The independent pipeline tree digest of `/candidate` is
  `e5ddc1c29390fe36f2c23bb6435be13695327077c320ba472673effb8c171095`,
  exactly the stage result's workspace digest. Both semantics trees have
  pipeline digest
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  exactly the task manifest's semantics digest. The trace tree digest matches
  `usage.json`.
- All required candidate proof artifacts are present and regular:
  `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
  `PROOF.md`.

The complete command script, file inventory, hashes, and bounded result log are
in [01_integrity_check.sh](/audit-output/evidence/01_integrity_check.sh) and
[01_integrity_check.log](/audit-output/evidence/01_integrity_check.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires: for any finite list of integers, repeatedly select
the minimum remaining value, then the maximum remaining value, continuing in
that alternating order; empty input returns an empty list. The trusted
canonical implementation performs those repeated selections and removals.

The submitted implementation instead sorts a copy once and walks inward with
`left` and `right`. For an ascending sequence, those endpoints are exactly the
minimum and maximum remaining elements. It handles all loop/if boundary shapes:
empty, singleton, even length, and odd length. The different algorithm is
return-value equivalent on the intended domain; unlike the canonical
implementation it does not consume its input, but input mutation is not part of
the source contract.

Trusted regeneration was exact:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy /candidate/solution.mpy
exit 0
SHA-256 of both: 48f23c44f76daad6a3893e5f76052fb5294b0c80fc385617399084cfe46d60d2
```

The independent differential imports the trusted canonical function, the
scratch candidate function, and a separately written endpoint oracle. It
checked all prompt examples, lengths 0 through 8 exhaustively over
`{-2,-1,0,2}`, explicit branch-boundary and large-integer cases, and 2,000
seeded random cases of lengths 0 through 40. Result: 89,391 cases and zero
mismatches. The script fixes the random seed and records the complete generated
input scope.

Evidence: [02_differential.py](/audit-output/evidence/02_differential.py) and
[02_differential.log](/audit-output/evidence/02_differential.log).

## 3. Clean proof reconstruction

I created `/tmp/audit-work/reconstruction.tZYoqF` and copied only source
artifacts, the trusted translator/canonical/prompt, and the trusted semantics
tree. I did not copy either candidate-provided kompiled directory, any
`__pycache__`, or any candidate proof cache. K reports version 7.1.293.

The fresh Haskell definition compiled from source:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
exit 0
```

Every submitted positive target command was then run against that definition:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
#Top
exit 0

kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --trusted SPEC.loop-invariant
#Top
exit 0
```

Thus the loop connection claim is first proved without assuming itself. The
second command uses that exact, already-closed claim as a composition
circularity and proves the sole remaining entry claim. An additional
non-candidate diagnostic combining `--claims SPEC.entry-point` with
`--trusted` exhibited a CLI/backend performance pathology and was interrupted;
it is not a submitted target command and is not used as proof evidence.

I also built a new LLVM definition from the trusted semantics source with
`MPY-KRUN` and executed reviewer-authored programs covering empty, singleton,
even, duplicate, and negative odd-length lists. Every run terminated with
`.K`, empty stack, `noRet`, `NoExc`, and exit code 0. The final heap values were
respectively `[]`, `[9]`, `[1,4,2,3]`, `[5,5,5,5]`, and
`[-1,4,0,3,2]`.

Evidence: [03_concrete.py](/audit-output/evidence/03_concrete.py) and
[03_reconstruction.log](/audit-output/evidence/03_reconstruction.log).

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` starts at the real `#while` head with:

- the exact loop body followed by the exact midpoint `If`, `Return`, and
  `#endcall` continuation;
- the actual six local bindings in scope 1;
- separate sorted-list and result-list heap objects;
- the exact callee frame, environment, return/exception state, and exit code;
- arbitrary finite sequences `A` and `S`, integer bounds `L,R`, and
  precondition `L >= 0`.

It executes that complete tail, returns the existing result reference, changes
the result heap to `strangeAcc(A,S,L,R)`, pops the frame and local scope, and
restores the caller control state. It does not accept an arbitrary suffix.

`SPEC.entry-point` starts with an empty heap, module environment 0, the real
builtins scope, and a binding of `strange_sort_list` to the exact submitted
closure. Its only data precondition is `allInts(VS)`. It calls that binding on
`list(VS)`. The postcondition requires return reference 1, sorted heap object 0,
and result heap object 1 containing:

```text
strangeAcc(.ValSeq, sortVS(VS), 0, vsLen(sortVS(VS)) - 1)
```

It also fixes heap allocation, scopes, stack, return state, exception state,
and exit code. The returned value is not free, existential, tautological, or
guarded only by a one-way implication.

### Satisfiability and concrete substitution

`VS = .ValSeq` satisfies `allInts` and gives the prompt's empty-list result.
`VS = vCons(1,vCons(2,.ValSeq))` is another satisfying state. Substitution in
the claimed summary, using the supplied sort contract, gives `[1,2]`; both
trusted canonical Python and submitted Python return `[1,2]`, and fresh K/LLVM
execution also stores `[1,2]`. The five-element witness
`[4,-1,3,2,0]` gives summary/result `[-1,4,0,3,2]` in both Python
implementations and in the recorded K heap.

### Mechanical program identity

I parsed the trusted-regenerated `solution.mpy` to JSON KAST and independently
emitted the compiled JSON KAST for the entry claim. A reviewer script extracted
the `FuncDef` parameter/body and the claim's bound `closureVal`
parameter/body. The parameter subtrees are identical, and both body subtrees
have canonical JSON hash
`bc6d3bc2ae99655a54f5b4edee6ac10f017df4148496dae3cca51c5934e946d7`.
The call name and binding name are both `"strange_sort_list"` and the captured
environment is 0. This mechanically accounts for inert parser normalization
such as explicit empty list terminators.

Evidence: [04_pinning_compare.py](/audit-output/evidence/04_pinning_compare.py)
and [04_pinning.log](/audit-output/evidence/04_pinning.log).

The fresh body-sensitivity probe in Stage 6 changes the second append inside
the actually executed closure, not merely `solution.py`; it changes the reached
heap value from `[1,2]` to `[1,1]` and invalidates the original obligation.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[05_rule_inventory.md](/audit-output/evidence/05_rule_inventory.md), generated
by [05_rule_inventory.py](/audit-output/evidence/05_rule_inventory.py), lists
every outer configuration, syntax declaration, context, function/total
declaration, ordinary rule, concrete rule, priority rule, simplification rule,
and claim in all 24 supplied K files plus `verification.k` and `spec.k`.
There are 938 inventoried sentences: 1 configuration, 229 syntax/function
declarations, 5 contexts, 701 rules (including the simplification), and 2 claims.
Each row includes exact source lines, normalized text, attributes, task-slice
classification, and assessment.

All supplied rules outside the execution slice were checked for potential
label/sort/guard overlap with reachable task terms. They are fixed-semantics
rules for constructs never produced here—floats, strings, sets, dicts, tuples,
comprehensions, ranges, keyed sorting, assertions, and unrelated builtins—or
sort/guard-disjoint cases of shared dispatch symbols. They cannot contribute to
either positive claim. This classification does not claim those unused
language fragments are a universal CPython semantics; it records why they are
irrelevant to this theorem.

The submitted MPY constructors map to fixed declarations and behavior as
follows:

| Program construct | Declaration | Material rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k` 53, 57, 61 | The claim pins the already-bound closure; module loading/definition is constructor-compared mechanically. |
| `Assign`, `AugAssign` | `syntax.k` 41, 44 | `controls.k` 9-31, with strict RHS evaluation and current-scope writes. |
| `While`, `If`, `Return`, `Expr` | `syntax.k` 46, 49-52 | `controls.k` 48-54 and 65-103; `functions.k` 78-90. |
| `Int`, `Name`, `BinOp`, `Compare` | `syntax.k` 9, 12, 15, 30-32 | `core.k` 130-154, 193-205; `operators.k` 10-18; `int.k` integer `+`, `-`, `<`, `==`. |
| `Call`, `Attribute` | `syntax.k` 28-29 | `core.k` left-to-right argument loop 183-191; `call.k` 15-75. |
| `ListExpr`, `append` | `syntax.k` 17 | `list.k` 12-20 and 52-55; `core.k` allocation 117-121. |
| `Subscript` | `syntax.k` 22 | `subscript.k` 6-41, including heap dereference, normalization, and sequence access. |
| `sorted`, `len` | normal builtin lookup in `builtinsScope` | `sort.k` 18-37; `builtins.k` 17-26; builtin argument dereference in `call.k` 34-50. |
| Function call/return frames | core value/config declarations | `call.k` 69-75; `functions.k` 63-90. |

The configuration exposes every material cell: computation, environment,
scopes, scope allocator, heap, heap allocator, stack, return state, exception,
and exit code. The claims constrain each. Evaluation is left-to-right via
strictness/contexts and the common argument loop. The append rule preserves
reference identity and updates the correct heap object. The sort rule allocates
a new object. Return performs the modeled abrupt control transfer and frame
pop; the loop theorem's continuation and stack are exact.

Priority/overlap review found no harmful overlap on the task path:

- generic call routing is `owise`; sort and append dispatch reach their
  correctly typed specific rules;
- mutating methods retain receiver references, while non-mutating receiver
  dereference is guarded by `isMutMethod`;
- reference-preemption rules are higher priority than generic structural
  consumers;
- integer operator cases are sort-disjoint from float/string/list cases;
- the loop/if true and false guards are complements.

### Proof-local extension inventory

`allInts` is a definitional predicate. Empty/cons cases are exhaustive and
disjoint over `ValSeq`, recursion strictly follows the tail, and its only
influence is the entry precondition.

`strangeAcc` is a definitional result summary, not an operational bridge. Its
`L>R`, `L==R`, and `L<R` guards partition all integer pairs. The recursive
case reduces `R-L` by two and appends exactly left then right. It fixes the
complete returned sequence in both claims.

The sole simplification rule says:

```text
(M K |-> V)[K <- undef] = M  when K is not a key of M.
```

Map-fragment matching already makes the displayed binding disjoint from `M`;
the guard prevents deleting any second occurrence. Thus deleting that known
binding leaves exactly `M`. It normalizes the result of fixed `#pop`; it does
not skip execution or fabricate a result.

There is no proof-local operational bridge or fresh oracle. The loop claim used
as trusted in the entry run is an exact auxiliary execution theorem. Its
complete match domain—continuation, binding, stack, cells, and guards—is the
same domain independently proved by the first `#Top` run. The body-sensitivity
failure confirms that this composition depends on displaced execution.

### Supplied abstractions and narrower model gaps

`sortVS` is a result-bearing but externally supplied builtin primitive, not
program-defined code and not a candidate extension. Fixed semantics performs
name lookup, argument evaluation, dispatch, allocation, and returns exactly
`list(sortVS(VS))`; the formal postcondition retains that same term. The theorem
is therefore interpretation-parametric and the human-facing result is
conditional on the named contract “ascending permutation.” Without that
contract, for example, treating the sort result of `[1,2]` as `[2,1]` would
make the formal endpoint result `[2,1]`, not the source-contract result. This
is a trust-dependence witness, not a claim that the supplied rule is false.

The other opaque supplied symbols are `sortKeyVS`, `md5hexCodes`, and the
float/conversion symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. None is reachable from this integer-list
program.

`valSeqAt` is total but deliberately under-specified for out-of-bounds and
opaque-sequence symbolic access. The real entry computes its bounds from the
same sorted sequence length and accesses only live endpoints; empty input sets
`right=-1` and takes no access. The auxiliary loop theorem is broader than
those reachable bounds, but its postcondition retains the same `valSeqAt`
terms under the fixed semantics. I found no intended-domain false conclusion
witness. This is a language-model limitation, not a candidate-local
soundness failure.

## 6. Fresh non-vacuity test

I ignored the candidate's mutation files and authored
[06_mutations.k](/audit-output/evidence/06_mutations.k) from scratch.

`AUDIT-FALSE-RESULT` uses the satisfying integer-list input `[1,2]`, executes
the exact submitted closure, but demands result `[1,1]`. Its dry run compiled
successfully with exit 0. The proof then exited 1 with
`WarnStuckClaimState`; the reached residual heap contained `[1,2]`, exactly the
expected unmet obligation.

`AUDIT-BODY-SENSITIVITY` changes the second append in the closure term from
`ordered[right]` to `ordered[left]` while retaining the original `[1,2]`
postcondition. It too dry-ran successfully, then exited 1 with a stuck residual
whose actual result heap was `[1,1]`.

These are semantic failures at reached final configurations, not parse errors,
timeouts, missing imports, or unrelated crashes. Exact commands, statuses, and
bounded residuals are in
[06_mutations.log](/audit-output/evidence/06_mutations.log).

## 7. Proven versus assumed accounting

What is machine-proved under the supplied MPY theory:

- for every finite `ValSeq` whose elements are K integers, the exact submitted
  closure call reaches the fully constrained final configuration in
  `SPEC.entry-point`;
- the entire real body executes through lookup, calls, allocation, loop,
  midpoint branch, return, and cleanup;
- result heap object 1 is exactly the `strangeAcc` endpoint traversal of
  supplied `sortVS(VS)`;
- the independently closed loop connection theorem justifies its composed use;
- the result and actual body are discriminating under fresh mutations.

Trusted or informal components:

- The supplied semantics contract that `sortVS(VS)` denotes the ascending
  permutation. It affects every returned element and the minimum/maximum
  interpretation. It is acceptable as the fixed external `sorted` boundary,
  but it is not universally proved in this candidate.
- Ordinary mathematical induction that alternating left/right endpoints of an
  ascending permutation equals alternating minimum/maximum removal. The
  `strangeAcc` equations make this transparent, but no separate K theorem
  states permutation/order.
- The trusted translator, supplied MPY semantics, K compiler/backend, and K
  integer/Map/List hooks. These are the ordinary verification infrastructure.
- The total-but-under-specified out-of-bounds portion of `valSeqAt`; intended
  executions do not reach it.

Finite empirical support, not proof:

- 89,391 CPython return-value differentials against both the canonical entry
  point and an independent oracle;
- five fresh K/LLVM executions spanning every control boundary and representative
  duplicates/negative values;
- exact trusted regeneration and exact parsed-KAST source-to-claim identity.

The theorem has no fixed-size bound and does not materially narrow the
HumanEval source domain. The remaining sorting/intent and unused exception
model limitations do not let a false result be proved for an intended
integer-list execution under the named supplied-builtin contract, so they do
not make the candidate illegitimate. They do prevent an unqualified `PASS`
because the human-facing minimum/maximum statement is not wholly established
inside K.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
