# Independent adversarial audit: 127-intersection

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed the proof from source under the supplied semantics,
reviewed the proof theory independently, and did not rely on the candidate's
compiled definitions, `#Top` transcript, `PROOF.md`, mutation outputs, or final
report.

## 1. Input and provenance integrity

The launcher record declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. The mode and mounts are consistent:
`/reference/reference-semantics` is present, so there is no infrastructure-mode
contradiction.

I inspected `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required files directly
under `/generation-evidence`, and the structured trace. The trace has one
regular JSONL file and all 699 lines parse as JSON. Its top-level records and
all 148 recorded tool calls/outputs are inventoried in
`evidence/generation-trace-inventory.log`. The much larger terminal output was
checked as an untrusted generation transcript; its recorded hash, start/end,
proof claims, failures, and final report agree with the corresponding
structured records. None of those claims was used as proof evidence.

Independent integrity results are in `evidence/stage1-integrity.log`:

- Every pipeline-v3 required record and every launcher-declared mounted input
  is a regular readable file or directory of the expected kind.
- The campaign lock is JSON-identical to the `audit_campaign` block, and its
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All recorded hashes for the canonical implementation, prompt, translator,
  run/task/invocation/result manifests, metrics, usage, terminal output, and
  generation prompt match independently read bytes.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The trusted and candidate `reference-semantics/` trees have the same 25
  relative entries, types, and per-file hashes. There are no missing, extra,
  changed, special, or symlinked entries. The independent manifest digest is
  `3e7b54d5572c720fb56a9952e5807489844fee3425b4b431cbeb0f304f3a134e`
  for both trees.

The candidate contains all required proof source artifacts. Candidate-built
`runtime-kompiled`, `verification-kompiled`,
`mutation-verification-kompiled`, caches, Python bytecode, and captured outputs
were ignored. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For two integer interval pairs `(A0, A1)` and `(B0, B1)`, with
`A0 <= A1` and `B0 <= B1`, compute the geometric intersection length

```text
min(A1, B1) - max(A0, B0).
```

Return `"YES"` exactly when that length is prime; return `"NO"` for
nonintersection, touching endpoints, lengths 0 or 1, and composite lengths.
The prompt's examples and the trusted canonical implementation both use
geometric length, rather than the number of integer points in a closed
interval.

### Implementation

`/candidate/solution.py` computes the maximum start and minimum end by explicit
branches. It rejects every length below 2, then scans all divisors from 2
through `length - 1`, returning `"NO"` iff one divides the length. This is a
different but extensionally equivalent presentation of the trusted canonical
algorithm. It has no fixed size, bounded unrolling, or endpoint restriction.

Using the trusted translator copied to scratch, I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both translated files have SHA-256
`9392d552bd8b1a10179245ab9ec4be341bcae391aac2eb1241d44cc07a06c6b1`
and are byte-identical. See `evidence/stage2-translation-identity.log`.

The independent test in `evidence/differential_test.py` imports the trusted
canonical entry point and candidate entry point separately and also uses an
independently written square-root primality oracle. It covers:

- all prompt examples and the differing example text in the canonical
  docstring;
- disjoint, touching, zero/one/two/three/four-length, prime, composite,
  negative-coordinate, equal-boundary, and every source branch boundary;
- list-shaped pairs as an implementation robustness check;
- all 23,409 ordered pairs of valid intervals with endpoints in `[-8, 8]`;
- 2,500 deterministic generated cases with starts in `[-500, 500]` and
  widths in `[0, 600]`.

All 25,928 cases agree among candidate, canonical, and independent contract
oracle. The finite run is evidence of program/intent fidelity, not a
replacement for the universal K proof. Exact scope and output are in
`evidence/stage2-differential.log`.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/127-intersection`. The semantics copy came from the trusted
mount, not the candidate tree. No candidate-built definition or cache was
copied or referenced.

The live toolchain is K v7.1.293 and Python 3.10.12
(`evidence/toolchain-versions.log`).

### Concrete definition

The fresh LLVM command was:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0 (`evidence/stage3-kompile-llvm.log`). An auditor-authored concrete
program whose function prefix is byte-identical to `solution.py` exercised nine
normal/boundary assertions. Fresh `krun` reached `<k> .K </k>`, `NoExc`, and
exit code 0 (`evidence/concrete_cases.py`,
`evidence/stage3-concrete-generate-v2.log`, and
`evidence/stage3-krun-concrete.log`). The earlier
`stage3-concrete-generate.log` stopped before generation because my diagnostic
prefix command selected 21 rather than all 23 function lines; the corrected
logged command is the `-v2` artifact and this reviewer-side typo has no bearing
on the candidate.

### Proof definition and every positive claim

The fresh Haskell command was:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0 (`evidence/stage3-kompile-haskell.log`). I then selected claims in
dependency-respecting groups:

1. `SPEC.divisor-loop-true` alone;
2. `SPEC.divisor-loop-true,SPEC.divisor-loop-false`, because the false-flag
   claim uses the true-flag claim on its found-divisor branch;
3. the complete unbounded `SPEC` module, including `intersection-correct`.

Every command exited 0 and printed `#Top`. The exact commands and actual
outputs are in:

- `evidence/stage3-kprove-divisor-loop-true.log`;
- `evidence/stage3-kprove-divisor-loops.log`;
- `evidence/stage3-kprove-all-positive.log`.

Compiler warnings concern unused variables and nonexhaustive fixed-semantics
functions for unused string/float/list features. None appears in the actual
program or postcondition dependency cone.

## 4. Adequacy and real-program pinning

### Plain-language claims

`divisor-loop-true` begins at the exact internal `#while` term and exact
submitted loop body, in a plain local frame with all seven real local
variables. Its precondition is `2 <= D <= N` and `has_divisor = true`. It
states that the loop terminates at `divisor = N`, keeps the flag true, and
preserves all other listed locals and framed configuration cells.

`divisor-loop-false` has the same concrete loop and range precondition, but
starts with `has_divisor = false`. It states that the final divisor is `N` and
the final flag is exactly `scanHasDivisor(false, N, D)`, i.e. whether a divisor
exists from the current candidate through `N - 1`. Its found-divisor branch
then uses the true-flag claim.

`intersection-correct` starts at the complete initial MPY configuration,
expands `solutionModule`, looks up and calls `intersection` with two constructed
integer 2-tuples, and requires exactly the source-contract precondition
`A0 <= A1 and B0 <= B1`. The result in `<k>` is constrained to
`primeResult(overlapLength(A0,A1,B0,B1))`; it is neither free nor related by a
one-way implication. Environment, scope allocator, heap, heap allocator, stack,
return, exception, and exit-code cells are constrained. Only the final
internal scope map is existential, which is unobservable under the HumanEval
return-value contract and does not weaken the result.

### Constructor identity

`evidence/program_pinning.py` mechanically compares the trusted regenerated
`solution.mpy` constructor with the sole RHS of `solutionModule`. The only
normalization is whitespace removal and spelling the standalone parser's
omitted trailing empty statement-list arguments as `.Stmts`. The normalized
constructors are identical, and the entry claim mechanically contains both
`#loadAll(solutionModule)` and `Call(Name("intersection"), ...)`. See
`evidence/stage4-program-pinning.log`.

Thus the actual term executed by the claim is the submitted function binding
and body. Fixed semantics performs module loading, name lookup, left-to-right
argument evaluation, tuple construction/indexing, parameter binding,
comparisons, assignments, modulo, each while iteration, return control, frame
popping, and string construction. There is no operational rule that replaces
the call or loop with the desired answer.

The precondition is satisfiable. Six explicit substitutions cover prime,
composite, length-one, disjoint, and negative-coordinate states. For example,
`((10,13),(0,20))` satisfies the precondition, has formal overlap length 3,
and yields `primeResult = canonical = candidate = "YES"`. All substitutions
are recorded in `evidence/stage4-claim-witnesses.log`.

### Body sensitivity

I changed the final return inside the actual constructor constant from
`Return(Str("YES"))` to `Return(Str("NO"))`; no external Python-only file was
changed. The one-line constructor diff is
`evidence/stage5-body-mutation-diff.log`, and the mutated source is
`evidence/body-mutant-solution-module.k`. Its fresh Haskell build exited 0.
Re-running the original theorem exited 1 with `WarnStuckClaimState`; the
residual exposes the mutated closure body and an actual `"NO"` result on the
prime/no-divisor branch. See
`evidence/stage5-body-mutation-kompile.log` and
`evidence/stage5-body-mutation-kprove.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` generated the complete numbered inventory in
`evidence/stage5-k-rule-inventory.log`. It covers the supplied assembly and all
23 semantic helper files, `solution-module.k`, `verification.k`, and `spec.k`.
`semantics.k` itself has no local syntax, configuration, or rules; it only
assembles the modules. The inventory contains:

- 707 rules, including 60 `[concrete]`, 30 `[owise]`, 52 priority-bearing, and
  four `[simplification]` rules;
- 231 syntax declarations, including 152 function declarations, 114 `total`
  occurrences, 25 named `symbol` occurrences, and four macro declarations;
- five evaluation contexts, one configuration, and all three claims;
- no `functional` declaration.

Every entry includes its source file, line range, full guards/cells/attributes,
and classification. The following table records the decision for every
module's inventory entries; rules in an unused row cannot match any constructor
reachable from the submitted term, and are not silently used as theorem
lemmas.

| Source | Entries | Static decision |
|---|---:|---|
| `semantics.k` | 0 | Assembly only; proof imports `MPY`, not `MPY-CONCRETE`. |
| `assert.k` | 3 | Truthy assertion behavior; used only by concrete audit programs, not the proof claim. |
| `bool.k` | 14 | Boolean equality/short-circuit rules are valid; the program uses Boolean literals/truthiness only. |
| `builtins.k` | 175 | No builtin call occurs in the submitted body. Registry/functions therefore cannot contribute to closure. |
| `call.k` | 24 | Material closure route evaluates callee then arguments left-to-right, allocates the real frame, and binds the real body; other callable routes do not match. |
| `comprehension.k` | 10 | No comprehension constructor is present. |
| `concrete.k` | 21 | LLVM-only deep equality/keyed sorting; not imported into the Haskell `MPY` proof module. |
| `controls.k` | 37 | Material assignment, `If`, and `While` rules preserve evaluation/control order and touch exactly the scope/`k` cells stated by the claims. Imports/for/break/cell rules do not match. |
| `core.k` | 84 | Configuration, module sequencing, lookup, literals, argument evaluation, truthiness, and list helpers are valid on the used constructors. Heap/cell/keyword branches are guarded and unreachable in the plain frame. |
| `dict.k` | 40 | No dictionary constructor or operation is present. |
| `float.k` | 155 | No Float value, float operation, import, or math call is present. Its opaque primitives have no dependency on any claim result. |
| `functions.k` | 19 | The ordinary def/bind/return/pop rules execute the exact function and restore all caller cells. Annotated closure-cell rules do not match. |
| `int.k` | 17 | Used `+`, `-`, `%`, `<`, `>`, and `==` rules are ordinary integer mathematics. `pyMod` is only used with divisor at least 2. |
| `iter.k` | 1 | Declaration only; the submitted loop is `While`, not iterator-based. |
| `list.k` | 32 | No list constructor/operation is in the formal entry call or body. |
| `methods.k` | 102 | No method call is present. |
| `operators.k` | 12 | Strict/left-to-right dispatch reaches the correct integer cases; ref-deref priority rules cannot match tuple/int values here. |
| `range.k` | 8 | No range or `For` occurs. |
| `set.k` | 18 | No set operation occurs. |
| `sort.k` | 25 | No sort operation occurs; opaque sort values cannot influence execution or the postcondition. |
| `str.k` | 33 | Only ASCII `"NO"`/`"YES"` literal conversion is used and fully reduces; iteration/membership/order rules do not match. |
| `subscript.k` | 57 | The entry constructs exact two-element tuples and indexes only 0 and 1, so both accesses are in bounds and reduce through `normIdx`/`valSeqAt`; slice/opaque/OOB cases are absent. |
| `syntax.k` | 16 | Declares exactly the source constructors and strictness used; material strict/seqstrict order matches Python evaluation. |
| `tuple.k` | 25 | Tuple arguments are evaluated left-to-right and remain immutable tuple values; indexing is handled by `subscript.k`; tuple iteration/equality/unpacking do not match. |
| `solution-module.k` | 2 | One total constructor constant with one exact defining equation; no execution is skipped. |
| `verification.k` | 14 | All three functions and ten defining/derived rules are reviewed below. |
| `spec.k` | 3 | All reachability claims have satisfiable domains, real recurring control terms, and result/state-constraining destinations. |

### Material construct-to-rule map

The used source constructs map as follows:

- `Module`/statement sequencing: `syntax.k` and `core.k`'s
  `#loadAll`, statement-list, and `.Stmts` rules;
- `FuncDef`, parameters, call, and return: `functions.k`, `call.k`, and the
  frame/stack/`ret` rules;
- `Name`, integer/Boolean literals, and string literals: `core.k` and `str.k`;
- `TupleExpr` and indices 0/1: `tuple.k` and `subscript.k`;
- `Assign`, `If`, and `While`: `controls.k`;
- `Compare` and `BinOp`: `operators.k`, with the used cases in `int.k`;
- modulo: guarded `pyMod(N,D)` with `D >= 2`.

The fixed semantics therefore executes every material operation and control
effect. The loop claims frame arbitrary continuations soundly because the loop
contains no return, break, continue, exception, allocation, output, or frame
operation; it changes only `divisor` and `has_divisor`.

### Proof-local extensions

`solutionModule` is a definitional constructor constant, not an operational
bridge. Its complete RHS is mechanically pinned in Stage 4.

`overlapLength(A0,A1,B0,B1)` has one exhaustive equation and is exactly
`min(A1,B1) - max(A0,B0)`.

`scanHasDivisor` has five concrete defining cases:

1. an incoming true flag returns true;
2. false with `D < 2` normalizes to `D = 2`;
3. false with `D >= 2` and `D >= N` returns false;
4. `2 <= D < N` and zero remainder returns true;
5. the complementary nonzero-remainder case recurses at `D + 1`.

The guards cover `Bool × Int × Int`, are disjoint where their RHS differs, and
the only recursion strictly advances toward `N`. Division by zero is excluded.
The four symbolic simplifications are the same true/base/divisor equations
plus the fold

```text
scan(false,N,D+1) = scan(false,N,D)
```

under `D >= 2`, `D < N`, and `N % D != 0`. The fold is valid because the
excluded candidate `D` contributes no divisor. Where it overlaps a base or a
divisor at `D+1`, both rewrite paths have the same Boolean value. It is a pure
derived equation: it matches no `<k>` context or operational cell.

`primeResult(N)` is the explicit proper-divisor definition of primality:
`"NO"` for `N < 2` or a found divisor, and `"YES"` otherwise. It is permitted
as a postcondition summary because the fixed-semantics loop claims establish
the universal connection between actual execution and `scanHasDivisor`; it is
not used to replace source execution.

The independently generated proof-local test contains 82 scan, 11
`primeResult`, and four `overlapLength` assertions. Fresh Haskell `krun`
reached `.K`, `NoExc`, exit code 0
(`evidence/generate_summary_checks.py`,
`evidence/stage5-generate-summary-checks.log`, and
`evidence/stage5-proof-local-ground-checks.log`). These checks support the
static equations but are not their universal justification.

There is no answer-smuggling operational bridge, program-derived oracle,
unconstrained result, false priority rule, inconsistent overlap, or
unjustified abrupt control rule in the dependency cone. I therefore make no
material unsoundness allegation and have no false-rule witness to report.

The supplied semantics does contain 25 named opaque symbols:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `md5hexCodes`, `sortVS`, and `sortKeyVS`. None is reachable from
the submitted program or appears in its claims/postcondition. The compile-time
nonexhaustive warnings similarly concern unused fixed-semantics features.

## 6. Fresh non-vacuity test

I did not reuse `/candidate/spec-vacuity.k`. The auditor-authored
`evidence/audit-spec-vacuity.k` calls the real submitted module on
`((10,13),(0,20))`. Both intervals satisfy the formal precondition and their
intersection length is 3. Stage 4 independently records
`primeResult = canonical = candidate = "YES"`. The mutation instead demands
`"NO"`.

First, `kprove ... --dry-run` exited 0, demonstrating successful parsing and
spec construction (`evidence/stage6-false-mutation-dry-run.log`). The actual
unbounded proof then exited 1 with `WarnStuckClaimState`; its residual shows:

```text
str(iCons(89, iCons(69, iCons(83, .IntSeq))))   // "YES"
```

which cannot unify with the mutated `"NO"` destination. This is the expected
unmet result obligation, not a parser failure, missing import, timeout,
unreachable mutation, or unrelated crash. See
`evidence/stage6-false-mutation-kprove.log`.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics and the audited proof-local mathematical
definitions, for every four K integers satisfying the two interval-order
preconditions, if the exact submitted constructor program's call terminates,
its return value is `"YES"` exactly when the geometric intersection length is
at least 2 and has no divisor in `[2, length)`, and is `"NO"` otherwise.
Because that is the ordinary definition of prime, the formal theorem matches
the prompt on its full stated integer-tuple domain.

This is partial correctness. The theorem does not itself prove termination,
although the concrete source loop plainly increments a finite integer
distance. Termination was not required by this benchmark.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, reachability logic, SMT, and hooked Int/Bool/String/Map/List theories | All dynamic and symbolic results | Standard unavoidable proof infrastructure; acceptable. |
| Trusted `/reference/py2mpy.py` | Python-to-constructor bridge | Byte regeneration pins the artifact; translator correctness is launcher-supplied trust, supported by source inspection and differential execution rather than proved in K. Acceptable under the problem's boundary. |
| Trusted supplied `reference-semantics` | Meaning of the MPY constructor program | Exact integrity match and exhaustive material-rule audit; every operation used by this program is concretely and symbolically modeled. Acceptable. |
| `solutionModule` constructor equation | Selects the body executed by the entry claim | Mechanically identical to trusted regeneration and body-sensitive. Proven artifact identity, not an informal substitute. |
| `overlapLength`, concrete `scanHasDivisor`, four simplifications, and `primeResult` | Loop invariant and result value | Pure, exhaustive or derived mathematics reviewed above; loop reachability claims connect them universally to fixed execution. Acceptable, with no opaque value. |
| Fixed-semantics `valSeqAt` totality | Tuple endpoint reads | Only indices 0 and 1 of exact length-2 tuples are reachable, and those cases reduce by explicit equations. No underspecified/OOB value influences the theorem. |
| The 25 fixed-semantics opaque symbols listed in Stage 5 | None | Present in imported semantics but constructor-disjoint and dependency-free for this theorem. They add no assumption to the result. |
| Final scope-map existential | Internal module/function binding state only | Return value and all other operational cells are constrained; scope contents are outside the HumanEval observation. Acceptable. |
| Differential, concrete, ground-summary, body-mutation, and false-result tests | Program/intent bridge and non-vacuity evidence | Finite empirical evidence only. It is not presented as the universal proof. |

The formal domain excludes invalid intervals, malformed/non-integer elements,
and non-pair arguments and their Python exceptions. The prompt states integer
interval pairs and uses 2-tuples, so this does not materially narrow the
HumanEval source-contract domain. ASCII-only string semantics is sufficient
because the only results are `"YES"` and `"NO"`.

Gate A (real-program soundness and non-vacuity), Gate B (intent adequacy), and
Gate C (trust/evidence auditability) all pass. No material adequacy gap or
result-bearing trust limitation remains.

VERDICT: PASS
LEGITIMACY: LEGIT
