# Independent adversarial review: 88-sort-array

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program, but it is not fully self-validating. The two
material limitations are (1) the supplied semantics' explicit opaque
`sortVS` contract for Python's external `sorted` builtin and (2) a
proof-local last-index operational bridge whose mathematical snoc/last lemma
is credible and ground-sensitive but has no bridge-free universal K theorem.
Neither limitation produced a false conclusion witness on the intended domain,
so the benchmark decision is concerns rather than failure.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`semantics_mode = SUPPLIED_SEMANTICS`, and problem `88-sort-array`. The mode
and mounts are consistent: `/reference/reference-semantics` is present.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required
`/generation-evidence` records, the present `usage.json`, both retained legacy
records, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and every one of
the 190 structured JSONL trace records. The historical runtime-metrics record
is absent, which this legacy-selected layout explicitly does not require.
Generation prose, commands, and prior `#Top` reports were treated only as
untrusted claims.

Independent results:

- The campaign block equals `/audit-campaign-lock.json` as JSON, and its
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every direct launcher-recorded file hash checked in
  `evidence/stage1_stage2.log` matches. Every evidence-file hash in
  `/generation-result.json`, including the structured trace file, also
  matches.
- Every launcher `container_paths` target is present, readable, correctly
  typed, and not symlinked.
- The structured trace is valid JSONL, has one file and 190 records, and has
  no symlinked entry.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Recursive, type-aware comparison of candidate and trusted
  `reference-semantics` finds exactly the same 25 entries and contents, with
  no missing, additional, mistyped, changed, or symlinked entry.

There is no audit-infrastructure breach. Reproducible checks and full output
are in `evidence/integrity_check.py`, `evidence/run_stage1_stage2.sh`, and
`evidence/stage1_stage2.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is:

> Given any finite array of non-negative integers, return a new sorted array.
> Use ascending order when the first-plus-last value is odd and descending
> order when it is even. Return `[]` for empty input and do not mutate the
> supplied array.

The trusted canonical implementation passes `reverse=True` exactly when a
nonempty input's endpoint sum is even. Candidate `solution.py` handles empty
input separately, selects ascending when modulo 2 is 1, and otherwise selects
descending. For non-negative integers, these partitions are equivalent.

Fresh translation with trusted `/reference/py2mpy.py` produced SHA-256
`69de41f5b2532bca90ef608aca79778b308b53a10f51745f7c746c1f15f88496`
and was byte-identical to submitted `solution.mpy`.

The independent test `evidence/differential_test.py` imports the trusted
canonical and scratch-copied candidate modules separately. It ran:

- all 4 documented examples;
- 14 explicit empty, singleton, endpoint-parity, and large-integer boundaries;
- all 9,331 arrays of lengths 0 through 5 over values 0 through 5;
- 300 deterministic generated arrays, lengths up to 64 and values below
  `10^12`.

All 9,649 results matched; 4,810 nonempty cases used the odd branch and 4,835
used the even branch. Neither implementation mutated its input, and both
returned a distinct list object. Differential testing is finite evidence, not
a replacement for the K proof.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/88-sort-array`, used the
trusted translator and trusted semantics copy, and created new LLVM and Haskell
definitions. No candidate definition or K cache was copied or reused. The live
toolchain is K v7.1.293.

The main clean commands were:

```text
kompile .../reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition .../runtime-audit-kompiled
krun .../concrete_tests.mpy --definition .../runtime-audit-kompiled
kompile .../verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition .../verification-audit-kompiled
kprove .../spec.k --definition .../verification-audit-kompiled \
  --spec-module SPEC
```

Both builds exited 0. Concrete execution ended with `.K`, `NoExc`, exit code
0, and the expected fresh and unchanged heap objects. The unmodified aggregate
proof exited 0 and printed `#Top`.

For independent per-claim execution, `evidence/spec-labeled.k` adds only labels
to exact copies of the four candidate claims. `empty`, `singleton`, `odd`, and
`even` each separately exited 0 and printed `#Top`.

`evidence/generate_pinning_spec.py` parses the freshly translated module with
K, extracts the normalized `FuncDef` body, and emits body/closure equality
claims. The pinning proof exited 0 with `#Top`; its “trivial claim” warnings are
expected because normalization made the constructor terms literally
identical. This is an identity check, not evidence substituted for the entry
proof.

The exact successful commands, exit statuses, and bounded outputs are in
`evidence/reconstruction.log`. Two retained preliminary logs record
reviewer-authored pinning harness syntax corrections; neither is a candidate
failure.

## 4. Adequacy and real-program pinning

The four entry claims mean:

1. **Empty:** from input heap object 0 equal to `[]`, the call returns fresh
   object 1 equal to `[]`, leaves object 0 unchanged, advances `heapLoc` from 1
   to 2, restores the caller frame, and raises no exception.
2. **Singleton:** for any `F >= 0`, input `[F]` is preserved and a fresh object
   containing `condRev(sortVS([F]), true)` is returned. This is the even branch.
3. **Odd length-at-least-two shape:** for non-negative first `F`, last `L`,
   and every non-negative integer in arbitrary recursive `MIDDLE`, endpoint
   modulo 2 equal to 1 returns a fresh `sortVS` result and preserves the input.
4. **Even length-at-least-two shape:** the same unrestricted recursive domain
   with endpoint modulo 2 equal to 0 returns a fresh reverse of `sortVS` and
   preserves the input.

These cases cover every finite non-negative integer list. `IntSeq` is an
unbounded recursive sequence, not a bounded unrolling: empty and singleton are
separate, and every length of at least two is uniquely representable as first,
arbitrary middle, and last. The non-negativity predicate recursively checks
the complete middle. No size or integer upper bound is imposed.

The claims execute `Call(Name("sort_array"), ref(0))` with an exact scope
binding to `sortArrayClosure`. The closure's parameter, defining environment,
and body match the freshly generated `solution.mpy` constructor term. Thus the
claim does not call a free function variable or substituted algorithm.
Full-module concrete execution independently installs that same closure.

Every precondition is satisfiable. `evidence/claim_witnesses.log` records
`[]`, `[5]`, `[2,4,3,0,1,5]`, and `[2,4,3,0,1,5,6]`; the formal summaries
correspond respectively to `[]`, `[5]`, ascending `[0,1,2,3,4,5]`, and
descending `[6,5,4,3,2,1,0]` under the named `sortVS` contract. Both Python
implementations agree on all four.

The body-sensitivity test changes the odd branch in the actual K closure body
to reverse sorting. The original odd postcondition then fails with a
`WarnStuckClaimState` residual requiring reverse output to equal ascending
output. This confirms sensitivity to the term the entry claims execute, not
merely to an external `solution.py` file. See
`evidence/run_body_sensitivity.sh` and `evidence/body_sensitivity.log`.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.md` is the exhaustive, source-located inventory:
232 syntax declarations, 704 rules, 5 contexts, 1 configuration, and 4 claims.
It identifies every function/total/macro/concrete/opaque/priority/owise
attribute. There is no local simplification rule and no `[functional]`
declaration. `evidence/static_analysis.md` gives the per-file disposition,
used-constructor map, priority/overlap analysis, and the rule-by-rule candidate
extension review.

The actual path faithfully models binding, callee and argument evaluation,
list truthiness, integer operations, input dereference, first indexing,
branching, `sorted` dispatch, reverse selection, fresh allocation, return, and
frame restoration. The `sorted` rule is reached only after ordinary lookup
selects the builtin binding; no textual-name shortcut bypasses shadowing. No
proof rule encodes the task's desired array or directly fabricates the final
branch result.

The proof-local extensions are:

- constant `sortArrayBody` and `sortArrayClosure`, mechanically pinned;
- exhaustive, disjoint, descending `intsVS` and `nonNegativeIS` functions;
- the standard two-equation `snocVS` definition;
- one priority-40 bridge reducing the last subscript of
  `F :: snocVS(M,L)` to `L`.

The bridge reads and writes no cell, preserves any continuation, and skips only
pure `-1` evaluation plus fixed indexing. Ground fixed-semantics constructor
lists and bridge-enabled proof representations agree for empty and one-element
middles while an observable `+10` continuation is present.

The concern is universal connection. With the bridge removed, both the exact
entry domain `snocVS(intsVS(MIDDLE),L)` and the broader admitted
`snocVS(MIDDLE:ValSeq,L)` domain build successfully but fail to prove. The
residual is exactly:

```text
valSeqAt(vCons(F,snocVS(...,L)),vsLen(snocVS(...,L))) = L
```

The candidate supplies no bridge-free induction/connection theorem, and its
match domain is broader than the entry claim representation. The rule is
nevertheless the ordinary true lemma `last(F :: (M ++ [L])) = L`; all intended
ground lists satisfy it, continuation behavior agrees, and I found no concrete
or symbolic false conclusion witness on the source-contract domain. Per the
benchmark boundary, I report the narrower evidence gap and do not call the
rule unsound. Full output is in `evidence/bridge_audit.log`.

The compiler's incomplete-totality warnings concern `mapStrVS`, float
conversions, `joinCodes`, and `valSeqAt`. All but `valSeqAt` are unreachable
here. The actual first index uses the reducing in-bounds `vCons` equation, and
the preconditions exclude empty indexing. These gaps can leave unsupported
terms abstract or stuck; they do not supply a false equality used by this
proof.

## 6. Fresh non-vacuity test

`evidence/spec-vacuity.k` is reviewer-authored and changes the empty claim's
result-bearing heap obligation from a fresh empty list to a fresh `[99]` list.
Input `[]` satisfies the unchanged precondition.

The mutation parsed and built against the clean proof definition. `kprove`
exited 1 with `WarnStuckClaimState`: execution reached `ref(1)` with heap object
1 equal to `list(.ValSeq)`, which did not unify with the mutated
`list(vCons(99,.ValSeq))`. This is the expected unmet obligation, not a parser
error, timeout, missing import, or unrelated crash. Exact artifact, command,
exit status, and residual are in `evidence/spec-vacuity.k`,
`evidence/run_nonvacuity.sh`, and `evidence/nonvacuity.log`.

## 7. Proven versus assumed accounting

What the successful K reachability proof establishes, under its theory, is:

- partial correctness for every finite non-negative integer list;
- execution of the submitted closure's actual body and its parity control flow;
- fresh result allocation and preservation of the original heap object;
- empty output on empty input;
- `sortVS(input)` on odd endpoint parity and
  `reverse(sortVS(input))` on even parity;
- normal return with caller state restored and no modeled exception.

It does **not** prove termination as a separate total-correctness theorem.

Trust and assumptions:

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 parser/compiler/Haskell prover and trusted builtin theories | All machine-checking | Standard unavoidable proof-tool trust. |
| Trusted `py2mpy.py` | Python AST to constructor identity | Byte integrity, fresh regeneration, K normalization, and body pinning checked; translator correctness remains trusted tooling. |
| Supplied semantics | Python-subset execution | Integrity is exact. Every material construct is covered; unused subset gaps do not affect this path. |
| `sortVS` external primitive | Entire nonempty returned ordering | Explicitly opaque in symbolic K. The proof is conditional on “`sortVS` equals ascending Python `sorted`”; LLVM's concrete insertion sort and 9,649 independent Python comparisons provide finite support, not a universal K theorem. |
| Candidate snoc/last bridge | Last endpoint and therefore parity branch | Ordinary mathematics and ground/continuation sensitivity support it, but no bridge-free universal K theorem covers its complete match domain. This is the principal validation concern. |
| Python/K integer and list model | Contract adequacy | K unbounded integers and finite value sequences align with the intended non-negative integer domain used here; Python behaviors outside that domain are excluded. |

The prior generation report, traces, differential tests, and concrete `krun`
are not treated as substitutes for the reconstructed K proof. They support
only provenance, program equivalence, and the explicitly named empirical
bridges.

The proof closes freshly, is non-vacuous, constrains the returned heap object,
pins the real generated body, and covers the full source-contract domain. The
opaque external sort contract and unproved-but-witness-consistent snoc/last
bridge prevent an unqualified pass, but neither makes a false intended-domain
conclusion provable. The appropriate benchmark pairing is therefore concerns
with legitimacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
