# Independent adversarial audit: 96-count-up-to

## Audit outcome

The candidate contains a legitimate partial-correctness proof of the submitted
generated program over the full stated domain of non-negative mathematical
integers. I independently reconstructed the LLVM and Haskell definitions from
source, established constructor-level identity between the claim body and the
trustedly regenerated `solution.mpy`, reran every positive claim, reviewed all
candidate proof extensions, and rejected a fresh false-result mutation for the
expected semantic reason.

Kit Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(trust/evidence auditability) all pass. The generation report's prior `#Top`
and `VALIDATED` assertions were not used as proof evidence.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- `problem_id`: `96-count-up-to`
- `condition`: `kit-semantics`
- `record_layout`: `pipeline-v3`
- `semantics_mode`: `SUPPLIED_SEMANTICS`
- `mount_reference_semantics`: `true`

This mode is consistent with the trusted mount:
`/reference/reference-semantics` exists and contains 24 regular K source files.
There is no rendered-mode contradiction.

I read and inspected `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. All required `pipeline-v3` artifacts
exist, have the required file/directory types, are readable, and are not
symlinks. The single JSONL trace has 578 valid JSON records and no parse error.
The 50,823-line generation output and the trace claim that construction
succeeded, but those claims were treated only as historical untrusted
evidence.

`/audit-campaign-lock.json` is byte-hashed to
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`, and its parsed object is exactly equal to the
`audit_campaign` block.

Every directly recorded artifact SHA-256 reproduced exactly, including the
run/task/result/invocation records, prompt, metrics, runtime metrics, usage,
Codex last/output files, and the trace file's per-file hash. The per-artifact
hashes inside both `generation-result.json` and `invocation.json` also all
match. For aggregate directories I used an independent length-delimited
relative-path/content digest rather than assuming undocumented launcher tree
framing; it found 770 regular candidate files, no symlinks, and stable
reviewer-authored digests recorded in the evidence.

### Trusted-input comparisons

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Recursive `diff --no-dereference` between candidate and trusted
  `reference-semantics/` exits 0.
- Independently sorted path/type manifests are identical.
- Both semantics trees contain 24 regular files, 117,274 bytes, no symlinks,
  and have the same reviewer tree digest
  `8dde1955867544b79c9c07d4f15bd1988737b301f1a520477537c1ccbb8e0d86`.
- All six required candidate proof deliverables are regular files:
  `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
  `PROOF.md`.

There is no input/provenance infrastructure breach.

Evidence:

- [stage1_integrity.log](evidence/stage1_integrity.log)
- [stage1_record_summary.log](evidence/stage1_record_summary.log)
- [stage1_tree_addendum.log](evidence/stage1_tree_addendum.log)
- [generation_trace_summary.log](evidence/generation_trace_summary.log)
- [stage1_generation_output_scan.log](evidence/stage1_generation_output_scan.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py` and `/reference/canonical.py`: for any
non-negative integer `n`, return an ascending Python list containing exactly
the prime integers strictly less than `n`. Thus the mathematical result is

`[p | 2 <= p < n and no integer d with 2 <= d < p divides p]`

in increasing order. The examples include empty results at 0 and 1 and the
usual prime lists below 5, 11, 18, and 20.

### Generated implementation

`solution.py` handles `n <= 2` directly. Otherwise it enumerates every
candidate from 2 through `n - 1`, resets `prime = True`, checks every divisor
from 2 through `candidate - 1`, sets `prime = False` upon any divisibility
witness, appends exactly when the Boolean remains true, and increments the
candidate. Omitting an early `break` changes efficiency, not the result.

Using the trusted translator:

```text
cd /tmp/audit-work/reconstruction
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

Both commands exit 0. Submitted and regenerated MPY bytes share SHA-256
`9766f117e6386c23704eec265c8bce37e871b4e06b146f711b3dea956ce591e6`.

The reviewer-authored differential script imports both the trusted canonical
entry point and the generated entry point and also uses an independently
implemented Eratosthenes sieve. It checks all documented examples, branch
boundaries 0 through 12 and 17 through 21, every integer 0 through 250, and
97 distinct seeded values through 998: 348 total inputs, zero mismatches.

Evidence:

- [differential_test.py](evidence/differential_test.py)
- [stage2_fidelity.sh](evidence/stage2_fidelity.sh)
- [stage2_fidelity.log](evidence/stage2_fidelity.log)

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`, copied the
semantics from the trusted `/reference` tree, and created fresh output
directories named `reviewer-runtime-kompiled` and
`reviewer-verification-kompiled`. Candidate-provided compiled definitions,
`cache.bin`, and other compiled artifacts were neither copied nor referenced.
K reports version 7.1.293.

### Fresh concrete definition

```text
timeout 1200 kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

Exit 0. A reviewer-authored MPY smoke program then executed under that fresh
definition for bounds 0, 1, 2, 3, 4, 5, 6, and 20. `krun` exits 0 with
`.K`, `NoExc`, and exit code 0; the heap contains the expected lists.

### Fresh proof definition and positive claims

```text
timeout 1200 kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

Exit 0. The only compiler warnings are unused variables in the supplied
`str.k`; no candidate total-function or overlap warning is emitted.

The following fresh target runs all print `#Top` and exit 0:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC --claims SPEC.inner-loop

kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC --claims SPEC.inner-loop,SPEC.outer-loop

kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.count-up-to
```

An initial exploratory use of unqualified labels was rejected by the CLI as an
unused filter before proof execution; that command and exit 113 are preserved
separately and are not a target-proof failure. The qualified reruns above are
the applicable results.

Evidence:

- [stage3_reconstruction.sh](evidence/stage3_reconstruction.sh)
- [stage3_reconstruction.log](evidence/stage3_reconstruction.log)
- [stage3_claim_targets.sh](evidence/stage3_claim_targets.sh)
- [stage3_claim_targets.log](evidence/stage3_claim_targets.log)
- [stage3_claim_targets_unqualified.log](evidence/stage3_claim_targets_unqualified.log)

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.inner-loop` starts at the exact inner `#while` term with
`candidate = C`, `divisor = D`, and prior Boolean `B`. Under
`C >= 2`, `D >= 2`, and `D <= C`, it executes through `divisor = C` and
constrains the final Boolean to
`B and noDivisors(C,D)`. Heap, allocation location, call stack, return state,
exception state, and exit code are preserved.

`SPEC.outer-loop` starts at the exact outer `#while` term with
`candidate = C`, list prefix `P`, and `2 <= C < N`. It executes until
`candidate = N` and changes the list contents to
`P ++ primesBetween(C,N)`. The final `prime` local is existential, but that is
not a result gap: it is not read after the loop and the entry claim subsequently
deallocates the function scope. The heap sequence and returned reference are
fully constrained.

`SPEC.count-up-to` starts in a fresh module state, executes the
`FuncDef("count_up_to", Params("n"), countBody)` binding, resolves that exact
name, calls it with arbitrary `N:Int`, and for `N >= 0` reaches normal return
`ref(0)` with the only allocated heap entry
`0 |-> list(primesBelow(N))`, heap location 1, empty stack, `noRet`, `NoExc`,
and exit code 0.

### Program identity

The entry claim does not replace the call or loop with a summary rule. Its
`countBody`, `outerBody`, and `innerBody` are syntax macros. Fresh `kast
--expand-macros` output for

`Module(FuncDef("count_up_to", Params("n"), countBody))`

is byte-identical to the parsed trustedly regenerated `solution.mpy`; both
KORE files have SHA-256
`609116d2f00f00798834a3ef45563bcbaa075fc0d07ad7a665cc4e54e838ba04`.
The supplied rules execute binding, lookup, argument order, assignments,
comparisons, modulo, both loops, allocation, mutation, return, and frame pop.

### Satisfying states and ground substitutions

Concrete satisfying states exist:

- Inner: `C=4, D=2, B=true, N=5, H=0`, empty list and empty stack. Its
  precondition is true and its constrained final Boolean is false because 2
  divides 4.
- Outer: `C=2, N=5, H=0, P=[]`, with ordinary initial locals. Its precondition
  is true and its constrained final sequence is `[2,3]`.
- Entry: `N=0`, `N=2`, `N=5`, and `N=20` all satisfy `N >= 0`.

For each listed entry input, expanding the claimed `primesBelow` result agrees
with both Python implementations. The values are respectively `[]`, `[]`,
`[2,3]`, and `[2,3,5,7,11,13,17,19]`.

### Body sensitivity

Expanding a start-at-3 body produces KORE hash
`aa15f321af5c3cd5bf63ea93a30bb46c13e17df3768ff23c2ce0948e508c1312`,
which differs from the submitted program term. Proving the unchanged
input-5 result obligation then exits 1 with `WarnStuckClaimState`; the residual
heap is `[3]`, not the required primes below 5. This mutation changes the term
actually stored in and executed from the closure.

Evidence:

- [stage4_ground_witnesses.py](evidence/stage4_ground_witnesses.py)
- [stage4_adequacy.sh](evidence/stage4_adequacy.sh)
- [stage4_adequacy.log](evidence/stage4_adequacy.log)

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The generated source-level inventory lists all directives in the 24 supplied
K files plus `verification.k` and `spec.k`: 1,125 entries comprising 711
rules, 230 syntax declarations, 5 contexts, one configuration, three claims,
and all structural imports/modules/requires. It flags all 149
function-bearing entries, 109 total declarations, 25 symbol-bearing entries,
22 `no-evaluators` entries, 45 priority-bearing entries, 36 concrete entries,
26 `owise` entries, five macro declarations, and two simplification rules.
Every entry has an explicit decision code distinguishing material fixed
execution, candidate proof extension, concrete-test-only behavior, and fixed
unused/no-influence behavior.

The full inventory and material constructor mapping are:

- [rule_inventory.md](evidence/rule_inventory.md)
- [used_construct_mapping.md](evidence/used_construct_mapping.md)
- [stage5_static_inventory.log](evidence/stage5_static_inventory.log)

In `SUPPLIED_SEMANTICS` mode the recursively identical reference tree is the
selected fixed semantics. I nevertheless traced every constructor reached by
the submitted program through its material rules. Unused facilities remain
explicit fixed-semantics trust boundaries; they are not silently presented as
a full Python model.

### Material fixed-semantics path

The `<generatedTop>` configuration explicitly carries `k`, environment,
scope map/location, heap/location, call stack, return state, exception state,
and exit code. On the submitted path:

- statement sequencing is left-to-right;
- `FuncDef` stores the exact body and defining environment;
- `Name` lookup selects the explicit closure/local bindings;
- call setup saves the caller continuation and binds `n`;
- strict/sequence-strict syntax evaluates assignment RHSs and binary operands
  in the correct order;
- `If` and `While` use ordinary Bool truthiness and re-evaluate loop guards;
- integer `<`, `<=`, `==`, `+`, and Python-style `%` use K mathematical
  integer operations;
- every reached modulo divisor is at least 2, so no unmodeled division-by-zero
  path is suppressed;
- list literals allocate fresh heap objects;
- `Attribute`/`Call` evaluate the receiver/callee before arguments;
- `isMutMethod("append")` preserves the receiver reference and the
  priority-40 list rule performs the in-place heap append;
- expression statements discard only the returned `noneV`, after the mutation;
- `Return` records the reference and `#pop` restores the saved caller while
  preserving the escaping heap object.

No material operation is replaced by an oracle, a result-fabricating rule, or
an unconstrained term.

### Candidate proof-extension inventory

1. **AST macros (`innerBody`, `outerBody`, `countBody`)** are compile-time
   syntax abbreviations. The byte-identical expanded KORE proves exact body
   identity. `countBodyStart3` is unused by positive claims and is itself only
   validation syntax.

2. **`noDivisors(Int,Int) [function,total]`** has four equations. `D < 2`
   normalizes to 2. For `D >= 2`, `D >= N`, divisible `D < N`, and
   non-divisible `D < N` are exhaustive and disjoint. The recursive case
   increments `D`; on every use it reaches `D >= N`. Its `pyMod` call is
   guarded by `D >= 2`. The inner reachability claim is a bridge-free universal
   connection from exact loop execution to this Boolean.

3. **`primesBetween(Int,Int) [function,total]`** splits exhaustively into
   `C >= N`, `C < N and C < 2`, and complementary prime/non-prime cases for
   `C >= 2`. Recursive equations increment `C`. It therefore denotes exactly
   the ascending prime sequence in `[C,N)`, including sensible total behavior
   off the positive path.

4. **`primesBelow(Int) [function,total]`** has disjoint exhaustive guards
   `N <= 2` and `N > 2`; it is empty in the former case and delegates to
   `primesBetween(2,N)` in the latter.

5. **List simplifications.** Right-associating
   `(A ++ B) ++ C` and rewriting `A ++ []` to `A` are true for every
   `ValSeq` by structural induction on `A` using the supplied two equations
   for `valSeqConcat`. Their overlaps with each other and with the base/cons
   equations normalize to the same sequence.

There is no candidate priority rule, operational `<k>` bridge, opaque symbol,
fresh result oracle, or unguarded proof-specific rewrite. The summary values
affect the append branch and final list, but are fixed by truthful equations
and connected to exact execution by the machine-checked inner and outer
claims. Fresh reruns of the opposite-value probes reject `prime=false` for
candidate 3 and `prime=true` for candidate 4; the residuals show the exact
opposite real values. See
[stage5_value_sensitivity.log](evidence/stage5_value_sensitivity.log).

The 25 opaque fixed-baseline symbols are
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. The submitted MPY term,
candidate summaries, loop claims, and postcondition contain no call,
constructor, branch, or data dependency on any of them.

I found no unsound candidate rule. Consequently there is no asserted
unsoundness requiring a false-conclusion witness; the negative witnesses below
instead demonstrate result sensitivity.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The reviewer-authored
`reviewer-false-result.k` executes the exact submitted body at the satisfiable
input `N = 5` but changes the final heap obligation from the real `[2,3]` to
`[2,4]`.

```text
kprove reviewer-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-RESULT --dry-run
```

Exit 0, proving that the mutation parses and builds against the fresh
definition.

The same command without `--dry-run` exits 1 with
`WarnStuckClaimState`. Fixed execution reaches:

```text
<k> ref(0) ~> .K </k>
<heap> 0 |-> list(vCons(2, vCons(3, .ValSeq))) </heap>
```

which cannot unify with the mutated `[2,4]` destination. This is the expected
unmet result obligation, not a parser error, timeout, unrelated crash, or
unreachable mutation.

Evidence:

- [reviewer-false-result.k](evidence/reviewer-false-result.k)
- [stage6_nonvacuity.sh](evidence/stage6_nonvacuity.sh)
- [stage6_nonvacuity.log](evidence/stage6_nonvacuity.log)

## 7. Proven versus assumed accounting

### Precisely proven

Under the supplied `MPY` definition and candidate's sound mathematical
definitions, for every mathematical integer `N >= 0`, if execution of the
trustedly regenerated `count_up_to` terminates from the fresh configuration,
then it returns normally with `ref(0)` pointing to the ascending list of
exactly those integers `p` for which `2 <= p < N` and no integer in
`[2,p)` divides `p`. The proof covers arbitrary, not bounded or finitely
enumerated, non-negative integers.

This is partial correctness. Termination, resource availability, and behavior
on negative, non-integer, or subclassed Python objects are not formal
conclusions. Those exclusions do not narrow the stated source domain of a
non-negative integer.

### Trust ledger

- **Supplied semantics.** The 24-file fixed `MPY` tree is a trusted input in
  this condition. Its material integer, Boolean, scope, call, control, list,
  heap, and return rules affect the theorem and were traced above. Concrete K
  executions support, but do not universally prove, their CPython fidelity.
- **Unused supplied facilities.** The listed float/sort/digest opaque symbols
  and other unused modules are in the broad imported definition but have no
  dependency on the reachable program path or postcondition. They are
  acceptable fixed-baseline no-influence boundaries for this theorem.
- **Trusted translator.** `/reference/py2mpy.py` is trusted to map supported
  CPython AST syntax to MPY constructors. Its output is byte-identical to the
  submitted `solution.mpy`; macro-expanded constructor identity pins that MPY
  program to the claim. Differential and concrete tests support the
  source/translation bridge finitely.
- **Ordinary mathematics.** K's mathematical integer/Boolean/list operations
  and the fact that an integer greater than 1 is prime exactly when it has no
  divisor from 2 through one less than itself are mathematical foundations,
  not candidate-specific oracles.
- **Toolchain.** K 7.1.293, `kompile`, the Haskell/Kore backend, SMT reasoning,
  the K parser/macro expander, and the host execution environment are in the
  proof-checking trust base.
- **Empirical evidence only.** The 348-input differential run and finite LLVM
  smoke run support program/semantics fidelity. They are not substitutes for
  the universal reachability proof.
- **Generation prose/traces.** `PROOF.md`, `codex-last.txt`, output logs, and
  traces contribute no trusted proof premise.

### Gate and benchmark decision

- Gate A: PASS. Fresh `#Top`, exact body pinning, sound extensions, satisfiable
  preconditions, body sensitivity, opposite-value rejection, and fresh
  non-vacuity all hold.
- Gate B: PASS. The formal domain is every `N:Int >= 0`, and the constrained
  result is exactly the source-contract prime list; there is no finite-size or
  bounded-unrolling restriction.
- Gate C: PASS. Reviewer-authored scripts, complete input scopes, exact
  commands, exits, outputs, and the exhaustive rule inventory are preserved.

The applicable benchmark mapping is therefore `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
