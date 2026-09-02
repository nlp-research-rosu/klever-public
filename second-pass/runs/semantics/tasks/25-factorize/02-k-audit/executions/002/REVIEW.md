# Independent adversarial review: HumanEval 25-factorize

## Executive finding

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted positive-integer factorization program. I rebuilt every
definition from mounted source, proved both positive claims independently, and
found no execution-bypassing or false local rule.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
non-fatal limitations. First, K proves that the returned list is exactly the
defined recurrence `primeFactors(N)`, but the K artifact does not state or
prove separate predicates for primality, nondecreasing order, and product. The
bridge from that recurrence to the words “ordered prime factorization” is an
elementary but reviewer-supplied mathematical argument. Second, the generic
loop claim/rule also admits non-entry-reachable states such as `N=2,D=3`,
where both the real loop and its summary recursion diverge; partial correctness
does not establish total operational equivalence there. The actual entry
always invokes the bridge at `D=2`, inside the terminating invariant described
below. Neither limitation leaves the intended returned value unconstrained or
makes a false target-domain result provable.

All exact commands and exit statuses are indexed in
`evidence/COMMANDS.md`. Command transcripts end with
`COMMAND_EXIT_CODE`, and reviewer-authored probes are preserved alongside
them.

## 1. Input and provenance integrity

The launcher record `/audit-input.json` declares:

- problem `25-factorize`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The trusted `/reference/reference-semantics` mount is present, as required for
this mode. There is no rendered-mode contradiction and therefore no audit
infrastructure breach.

Independent results:

- `/audit-campaign-lock.json` is byte-hashed as
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`, and its decoded JSON object exactly equals the
  `audit_campaign` block.
- Every launcher-declared container path is readable and is not a symlink.
- All records required by `legacy-selected-stage1` are present:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json`
  is present and was also checked. Historical runtime metrics are not required
  for this layout and were not reconstructed.
- All directly recorded SHA-256 values match the mounted bytes, including the
  run/task/result manifests and every generation-evidence output.
- The one 491-line structured JSONL trace parses with zero malformed events;
  all lines were read. The 25,455-line Codex output log was also read and
  scanned in full. These generation records were treated only as untrusted
  historical claims.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`b619821e...b3788`), and `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (`406485ea...db16`).
- The candidate and trusted `reference-semantics/` trees each have 25
  recursively inventoried entries. There are no missing, additional, changed,
  mistyped, or symlinked entries. Every per-file hash matches.
- The required proof artifacts `solution.py`, `solution.mpy`,
  `verification.k`, and `spec.k` are regular files in the intact candidate
  mount.

Evidence:

- `evidence/provenance_check.py`
- `evidence/provenance_check.log` (exit 0)
- `evidence/generation_trace_summary.py` and its log (exit 0)
- `evidence/generation_output_summary.py` and its log (exit 0)

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks `factorize(n: int)` to return the prime factors of the
given integer, smallest first, with multiplicity, such that their product is
the input. It gives `8 -> [2,2,2]`, `25 -> [5,5]`, and
`70 -> [2,5,7]`.

The meaningful source domain is positive integers:

- prime factorization and the stated product condition are meaningful there;
- both implementations include the empty factorization for 1;
- the trusted canonical implementation raises `ValueError` for negative
  integers and returns `[]` for zero, which would not have product zero.

Thus the proof precondition `N >=Int 1` does not materially narrow the
supported HumanEval contract. It has no finite-size or unrolling bound.

`/candidate/solution.py` uses increasing trial divisors. On divisibility it
appends the divisor and divides `n`; otherwise it increments the divisor. This
is a different loop condition from the trusted square-root implementation but
computes the same result on the intended domain.

### Trusted regeneration

In clean scratch, the trusted translator regenerated `solution.mpy` with exact
byte identity:

```text
59f618a068725a224caa41c6973b799c1b91758d35d264cdfb848013a7912ee4  solution.mpy
59f618a068725a224caa41c6973b799c1b91758d35d264cdfb848013a7912ee4  solution.mpy.submitted
```

See `evidence/translation_identity.log` (exit 0).

### Independent differential test

`evidence/differential_factorize.py` independently imports the trusted
canonical and candidate entry points. It checks:

- all three documented examples;
- the empty-result/loop-boundary input 1;
- the smallest primes, repeated factors, mixed divisible/non-divisible paths,
  prime squares, powers, a larger prime, and every branch boundary listed in
  its output;
- every integer 1 through 2000;
- 250 deterministic pseudorandom integers in 1 through 100,000.

Across 2,245 distinct positive inputs there were zero differential mismatches
and zero independent failures of sortedness, primality, or product. The
separate nonpositive observations record the canonical/candidate difference
on negatives rather than hiding it. The initial audit-script run that called
the canonical function on a negative and raised `ValueError` is retained as
`differential_factorize.log`; the corrected, successful run is
`differential_factorize_rerun.log`.

This testing is finite supporting evidence, not the universal proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/25-factorize`. The supplied semantics came from
`/reference/reference-semantics`, not from a candidate-built definition.
No candidate cache or compiled directory was copied or reused.

The independently installed tools report K version `v7.1.293`; see
`evidence/toolchain.log`.

### Concrete definition

The trusted semantics rebuilt under LLVM:

```sh
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit: 0. The warnings are confined to supplied-semantics exhaustiveness and
unused-variable diagnostics. `krun solution.mpy` exits 0 and displays the
loaded closure containing the translated function body. The independent
assertion harness `evidence/concrete_audit.py`, whose first 13 lines are
byte-equal to `solution.py`, also exits 0 for 1, 2, 3, 4, 8, 25, 70, 97, and
360. See `kompile_llvm.log`, `krun_solution_module.log`, and
`krun_concrete_audit.log`.

### Positive proof claims

The base Haskell definition was rebuilt from `verification.k` and the trusted
semantics. The universal loop claim was then run on its own:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module FACTORIZE-LOOP-SPEC --output pretty
Output: #Top
Exit: 0
```

The lemma-enabled definition was separately rebuilt from source, and the
entry claim was run on its own:

```text
kprove spec.k --definition audit-verification-with-lemma-kompiled \
  --spec-module FACTORIZE-SPEC --output pretty
Output: #Top
Exit: 0
```

The complete build and proof logs are
`evidence/kompile_base_proof.log`, `evidence/kprove_loop.log`,
`evidence/kompile_lemma_proof.log`, and `evidence/kprove_entry.log`.
Both required positive targets therefore satisfy the dynamic gate.

## 4. Adequacy and real-program pinning

### Claims in plain language

The `factorize-loop` claim assumes:

- an arbitrary continuation `KONT`;
- current integer `N >= 1` and divisor `D >= 2`;
- a current local scope containing exactly `n=N`, `divisor=D`, and
  `factors=ref(H)`;
- heap object `H` containing an arbitrary value sequence `VS`.

As a partial-correctness claim, it says that if the actual lowered while loop
terminates, it does so without changing the continuation, leaves `n=1`, leaves
the exact recursively computed final divisor `factorDivisor(N,D)`, and mutates
the existing list at `H` to `factorLoop(N,D,VS)`. Omitted configuration cells
are framed unchanged.

The `factorize-correct` claim assumes any mathematical integer `N >= 1`, the
ordinary initial module environment, the exact `factorize` closure, empty heap,
and clean call/return state. It says any terminating call returns reference 0;
heap object 0 is exactly `list(primeFactors(N))`; heap allocation advances
once; and the scope allocator, stack, return state, exception state, and
module bindings are restored as stated.

### Mechanical program identity

The entry claim does not load the whole module; it binds the submitted
function directly. That binding is pinned as follows:

1. Trusted translation is byte-identical to the submitted `solution.mpy`.
2. `kast --expand-macros` produces byte-identical KORE for
   `factorizeDef` and the actual translated `FuncDef` constructor term:
   both hash to
   `9c7bfebc2b591c7751dbed08989db225e00785471707861494377c85748ba37a`.
   See `evidence/program_term_comparison.log` and
   `evidence/actual_factorize_term.mpy`.
3. The closure printed by fresh concrete execution contains the same body.
4. The only omitted module statement is the typing-only
   `ImportFrom("typing","List")`; the supplied semantics reduces non-math
   `ImportFrom` to `.K`, so omission is semantically inert.

This is constructor-level identity, not a source-filename assumption.

### Satisfying witnesses and result constraint

The entry precondition is satisfied, for example, by `N=1`, `N=8`, and
`N=70` with the explicitly stated initial configuration. A separate K spec
substitutes those values and exact result lists; all three claims close with
`#Top` and exit 0. Both Python implementations return exactly the same lists:

```text
N=1  K_target=[]        canonical=[]        candidate=[]
N=8  K_target=[2,2,2]   canonical=[2,2,2]   candidate=[2,2,2]
N=70 K_target=[2,5,7]   canonical=[2,5,7]   candidate=[2,5,7]
```

See `evidence/spec_concrete_substitutions.k`,
`kprove_concrete_substitutions.log`, and
`concrete_substitution_compare.log`.

The result is not a free variable: it is the normal form of three guarded,
recursive `factorLoop` equations starting from divisor 2 and an empty
sequence.

### Body and continuation sensitivity

A fresh mutation changes the executable `factorizeBody` initialization from
divisor 2 to divisor 3. The mutation compiles, but the entry proof exits 1 with
the expected unmet obligation
`factorLoop(N,2,.ValSeq) = factorLoop(N,3,.ValSeq)`. This changes the term
executed by the claim; it is not merely an external source edit. See
`evidence/verification_body_mutation.k`,
`kompile_body_mutation.log`, and `kprove_body_mutation.log`.

The promoted loop rule accepts arbitrary `KONT`, exactly as its connection
theorem does. A boundary probe uses `N=4,D=2` and follows the loop with
`Assign(Name("after"),Int(99))`. Both the fixed-semantics definition and the
lemma-enabled definition prove the same final list `[2,2]` and the observable
scope update `after=99`. See `evidence/spec_bridge_continuation.k` and the two
`kprove_bridge_continuation_*.log` files.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` reads all 2,371 lines of the assembled supplied
semantics, its 23 helper files, `verification.k`, and `spec.k`.
`evidence/k_rule_inventory.log` is a line-addressed inventory containing every
module/import, configuration, syntax declaration, context, ordinary rule,
guard, attribute, and claim. The totals are:

- 706 explicit `rule` declarations: 695 supplied-semantics rules and 11
  candidate verification rules;
- 233 explicit `syntax` declarations;
- 5 evaluation contexts;
- 1 configuration;
- 2 reachability claims.

There are no `[functional]` or `[simplification]` declarations. All macro,
priority, concrete, owise, function, total, symbol, and no-evaluators
occurrences are displayed with their complete source blocks in the inventory.

File-level disposition:

| File | Rules | Review disposition |
|---|---:|---|
| `semantics.k` | 0 | Assembly only; exact trusted baseline. `MPY` excludes the concrete-only leg and `MPY-KRUN` adds it. |
| `syntax.k` | 0 | Constructor grammar and strictness/context declarations; the used subset is mapped below. |
| `core.k` | 46 | Values, configuration, allocation, sequencing, name lookup, argument order, literals, truthiness, and list helpers. Relevant rules preserve the observed cells. |
| `controls.k` | 34 | Assignment, inert typing import, `If`, `While`, and `AugAssign`; relevant branch and loop rules agree with the submitted control flow. |
| `functions.k` | 15 | Closure binding, parameter binding, return, frame pop; the real call path uses the ordinary closure rules and restores all claimed cells. |
| `call.k` | 21 | Left-to-right callee/argument evaluation, method dispatch, and ordinary closure call. No call interception replaces `factorize`. |
| `operators.k` | 10 | Operand evaluation and dispatch; the integer cases used here do not encounter heap-deref ambiguity. |
| `int.k` | 16 | Exact unbounded-integer `>`, `==`, `+`, `%`, and floor-division equations. Divisors are at least 2, so no zero-divisor gap is reachable. |
| `bool.k` | 13 | Boolean truthiness used by loop/branch guards; no opaque Boolean affects this proof. |
| `list.k` | 27 | Fresh empty-list allocation and in-place `append`; `valSeqConcat` is a total structural recursion. |
| `methods.k` | 75 | Declares method dispatch used by the call layer; its string/list helper cases are otherwise outside this program's execution cone. |
| `builtins.k` | 137 | Builtin folds and helpers are not called by the program. The initial builtin scope is fixed in `core.k`. |
| `assert.k` | 3 | Used only by the independent LLVM harness, not by either proof claim. |
| `concrete.k` | 16 | LLVM-only deep equality/keyed sort leg; absent from symbolic definitions and incapable of closing the proof. |
| `float.k` | 121 | Supplied opaque/concrete float boundary, completely unreachable from this integer-only term. |
| `sort.k` | 19 | Supplied opaque sort boundary, unreachable because `sorted`/`.sort` never appears. |
| `dict.k` | 28 | Unused. |
| `subscript.k` | 40 | Unused; its documented total out-of-bounds abstraction cannot influence the theorem. |
| `str.k` | 28 | Unused except as syntax/support for the fixed environment. |
| `set.k` | 12 | Unused. |
| `tuple.k` | 21 | Unused by program execution. |
| `range.k` | 6 | Unused. |
| `iter.k` | 0 | Iterator declarations only; unused. |
| `comprehension.k` | 7 | Unused macros. |

The supplied theory contains 25 declared opaque `symbol(...)` boundaries:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None occurs in the program,
the two claims, the candidate summary equations, or any residual from the
positive proofs. They therefore do not bear on value, control, state, or
postcondition here.

### Construct-to-rule mapping for `solution.mpy`

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, `ImportFrom` | `syntax.k:43,61`; `core.k:124-127`; non-math no-op in `controls.k:35-36`. |
| `FuncDef`, `Params`, entry `Call` | `syntax.k:28,53,57`; `functions.k:14-16`; `call.k:18-21,69-74`; parameter/frame rules `functions.k:63-90`. |
| `Name`, `Int` | `syntax.k:9,12`; lookup/literal rules `core.k:130-154,194`. |
| `Assign` | strict RHS in `syntax.k:41`; current-scope update `controls.k:9-11`. |
| `ListExpr()` | `syntax.k:17`; left-to-right list construction and allocation `list.k:13-15`, `core.k:117-121,183-191`. |
| `While` | `syntax.k:46`; `controls.k:65-82,85`. |
| `Compare` `>` / `==` | `syntax.k:30,32`; contexts/dispatch `operators.k:14-17`; integer equations `int.k:22-27`; Boolean truthiness `core.k:199-205`. |
| `If` | strict condition `syntax.k:49`; `controls.k:51-54`. |
| `BinOp` `%` / `//` | sequential strictness `syntax.k:15`; dispatch `operators.k:12`; `pyMod` and floor division `int.k:15-20`. |
| `Attribute(...,"append")`, `Call`, `Expr` | `syntax.k:28-29,52`; attribute/callee/argument rules `call.k:15-24`; effect discard `controls.k:46-48`; in-place append `list.k:52-55`. |
| `AugAssign(...,"+",1)` | strict RHS `syntax.k:44`; integer addition `int.k:9`; local update `controls.k:20-23`. |
| `Return` | strict expression `syntax.k:50`; return/pop lifecycle `functions.k:77-90`. |

Every material operation is executed by fixed semantics before the derived
loop rule is used.

### Candidate-local extension inventory

1. `factorizeStep`, `factorizeBody`, and `factorizeDef` are definitional syntax
   macros. Their constructor expansions match the trusted translation exactly.
2. `factorLoop(N,D,VS)` is a result-bearing definitional summary:
   - `N <= 1` returns the accumulator;
   - `N > 1`, `D > 0`, and zero remainder appends `D` and recurses on exact
     quotient `N/D`;
   - the complementary nonzero-remainder guard increments `D`.
   On the claim domain, guards are disjoint and exhaustive. The function is
   intentionally partial: for example `factorLoop(2,3,VS)` recurses forever,
   just as the corresponding real loop does. On states reachable from the
   entry (`D=2` initially, `D <= N` whenever `N>1`, and no remaining prime
   divisor is below `D`), each division lowers `N`, and nondivisible increments
   cannot pass `N`; termination follows.
3. `primeFactors(N)` is the definition `factorLoop(N,2,.ValSeq)`. It adds no
   oracle or axiom.
4. `factorDivisor` has the same disjoint transition cases and records only the
   final local divisor. It does not influence the returned list.
5. `factorize-loop-lemma` is an operational bridge with priority 40. Its body
   and guard are byte-identical to lines 9-34 of the separately proved loop
   claim (both extracted bodies hash to
   `06be58e5...a397`). The connection theorem was proved against
   `FACTORIZE-VERIFICATION`, which does not import the bridge. Its match and
   justification domains both quantify the same arbitrary continuation,
   scope remainder, heap remainder, and omitted framed cells. It neither
   returns abruptly nor discards a continuation. Its guard is nevertheless
   broader than the entry-reachable terminating invariant: the bridge-free
   claim is only a partial-correctness theorem on states such as `N=2,D=3`.
   This is an extension-reuse/control-equivalence limitation, not an
   intended-domain false-result witness; the public theorem applies the bridge
   at `D=2`, where the stronger terminating invariant holds.

For the factorization interpretation, starting from divisor 2 maintains:

- accumulated values are nondecreasing primes;
- their product times current `N` is the original input;
- current `N` has no prime divisor below current `D`.

On a divisible step, `D` must be prime: a composite `D` would have a smaller
prime divisor of current `N`, contradicting the invariant. Appending and exact
division preserve product and ordering. On a nondivisible step, incrementing
`D` preserves the absence of smaller prime divisors. At exit `N=1`, so the
accumulator is precisely the ordered prime factorization with multiplicity.
This is the informal intent bridge noted in the executive finding.

No candidate-local equation has overlapping guards with different right-hand
sides, no `[total]` or opaque declaration supplies a missing value, and no
rule encodes a fixed answer or bypasses an unproved program-defined operation.
Accordingly, there is no unsoundness finding for which a false-conclusion
witness is required.

## 6. Fresh non-vacuity test

The fresh mutation `evidence/spec-vacuity.k` changes the result obligation from
`primeFactors(N)` to `primeFactors(N + 1)` while keeping the executable
program, initial state, and satisfiable precondition `N >= 1` unchanged.

The witness `N=1` is demonstrably false:

- actual/K target: `primeFactors(1) = []`;
- mutated target: `primeFactors(2) = [2]`.

The mutation's dry run builds successfully and exits 0. The actual proof exits
1 with `WarnStuckClaimState`; its residual contains the unmet equality

```text
factorLoop(N +Int 1, 2, .ValSeq)
= factorLoop(N, 2, .ValSeq)
```

and ends with the expected prover “cannot be rewritten further” error. This is
a reached result obligation, not a parser failure, missing import, timeout, or
unrelated crash. See `evidence/spec_vacuity_build.log` and
`evidence/kprove_vacuity.log`.

## 7. Proven versus assumed accounting

### What the successful reachability proofs establish

Under the supplied `MPY` theory:

1. For every `N >= 1`, `D >= 2`, accumulator `VS`, matching scope/heap
   remainder, and continuation, every terminating execution of the actual
   submitted while loop has the exact `factorLoop`/`factorDivisor` summary
   while preserving the continuation and framed state.
2. For every unbounded K integer `N >= 1`, the exact submitted `factorize`
   function, from the stated clean module configuration, returns `ref(0)` and
   leaves heap object 0 equal to `list(primeFactors(N))`, with the other named
   cells in the claimed final state.

These are partial-correctness reachability results. No separate termination
theorem is claimed.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell prover, and builtin integer/map/list theories | Entire machine check | Standard accepted proof-tool boundary; versions and fresh commands are recorded. |
| Supplied `MPY` semantics | Binding, order, calls, control, heap/state, integer/list operations | Accepted for this task after exact trusted-tree integrity and exhaustive used-rule review. Known partial-language behavior is outside the submitted execution cone. |
| Trusted `py2mpy.py` | Python-to-constructor bridge | Accepted with strong mechanical evidence: candidate/trusted translator identity, regenerated byte identity, expanded constructor equality, fresh runtime body display, and body sensitivity. The translator itself is not formally verified. |
| `factorize-loop-lemma` promotion | Replaces loop execution in the entry proof | Accepted for the target entry domain: separately proved without the bridge, exact body/guard identity, identical context scope, and fixed-versus-bridge continuation witness. Its broader non-entry-reachable, potentially divergent match domain is a non-fatal reuse/control-equivalence concern. |
| `factorLoop`/`factorDivisor` equations | Exact returned sequence and final divisor | Accepted partial definitional summaries; exhaustive/disjoint on the proof domain and terminating on entry-reachable states. On off-path `D>N>1` states they diverge with the real loop. No opaque value enters the intended result. |
| Recurrence means ordered prime factors | Human-language contract | Legitimate but informal mathematical bridge; this is the principal reason for `CONCERNS` rather than `PASS`. |
| Positive-integer domain | Theorem scope | Acceptable, not a narrowing defect: it is the meaningful prompt/canonical domain; negatives are rejected by the canonical implementation and zero violates the stated product property. |
| Imported float/sort/MD5 opaque symbols | None | Inert for this program and theorem; listed exhaustively above. |
| Differential and concrete tests | Finite adequacy support | Supporting evidence only. They are not used as a substitute for either K reachability proof. |

Gate A (real-program soundness): **PASS**.  
Gate B (intent adequacy): **PASS with a non-fatal formalization limitation**;
the unrestricted positive domain is covered, while the recurrence-to-prime
properties argument is informal.  
Gate C (trust/evidence auditability): **PASS**; all claimed evidence is
present, reproducible, scoped, and distinguished from formal proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
