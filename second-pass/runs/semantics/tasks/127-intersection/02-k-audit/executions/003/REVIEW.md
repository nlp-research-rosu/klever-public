# Independent adversarial audit: 127-intersection

## Executive decision

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full stated interval domain. I independently rebuilt all K
definitions from source, obtained `#Top` for both positive claims, mechanically
pinned the entry claim's closure body to trusted regeneration of `solution.py`,
reviewed every local K sentence, and obtained the expected failures from both a
real-body mutation and a fresh false-postcondition mutation.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(auditability/trust accounting) all pass.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: legacy-selected-stage1` and
`semantics_mode: SUPPLIED_SEMANTICS`. The mode is consistent with the mounts:
`/reference/reference-semantics` is present as a real directory. There is no
infrastructure breach.

I checked `/audit-input.json` before using candidate evidence. The
`audit_campaign` object is exactly equal to `/audit-campaign-lock.json`, whose
independently calculated SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The required legacy-selected-stage1 records are present, readable regular files:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured trace at
  `/generation-evidence/codex-trace/2026/07/23/rollout-...jsonl`.

`usage.json` is present and was also checked. Historical `runtime-metrics.json`
is absent, which is expressly permitted for this legacy layout. The trace has
573 JSON records and zero parse errors. It records the generation agent's
claimed successful builds and proofs, but none of those claims was relied upon.

Independent SHA-256 checks match every recorded per-file digest used by the
layout, including the run/task/result/invocation/metrics records, generation
prompt/output/last message, canonical source, trusted prompt, and translator.
The independently reimplemented manifest-tree digest is:

- candidate workspace:
  `6dd07c235aae5781b4dd6a5f926270b9db9cd4572c977b450abbbfdefe0cc8f9`,
  matching the retained workspace digest;
- each supplied-semantics tree:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace:
  `0406c89e8eb77207308a984b3bcfbead1f884c32382cac4b007de994e5cb4c5b`,
  matching `usage.json`.

The candidate and trusted `prompt.py` files are byte-identical, as are the two
`py2mpy.py` files. Recursive entry-kind and byte comparison of
`/candidate/reference-semantics` against `/reference/reference-semantics`
found no missing, additional, changed, mistyped, or symlinked entry. The full
check and exact hashes are in
`evidence/provenance_check.py` and `evidence/01-provenance.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says that both arguments are pairs of integers denoting
valid closed intervals (`start <= end`). Let
`L = min(end1,end2) - max(start1,start2)`. The result is `"YES"` exactly when
`L` is prime; touching, disjoint, zero-length, and unit-length intersections
return `"NO"`. This is also the behavior of `/reference/canonical.py`.

`/candidate/solution.py` computes the same endpoints and length, rejects
`length <= 1`, and performs exhaustive trial division over `2 .. length-1`.
It is a different presentation of the canonical nested helper but implements
the same result on the intended domain.

I regenerated the MPY program with the trusted mounted translator:

```text
python3 /tmp/audit-work/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

The regenerated and submitted `solution.mpy` are byte-identical, both with
SHA-256
`dbff75649cdcc014adfb803aec5cfa84ecce5a1f72bfd3e2517e7c7c8c2bda7d`.

The independent differential script imports both the trusted canonical entry
point and the submitted entry point and uses a separately implemented
square-root primality oracle. It covers all prompt examples, the differing
canonical-doc example, disjoint/touching/singleton cases, overlap lengths
0/1/2/3/4/9/97/100, both `min`/`max` operand selections, negative coordinates,
large translated integers, every pair of valid intervals whose endpoints are
in `[-8,8]`, and 5,000 deterministic broader cases. All 28,432 cases agree,
with zero mismatches. See `evidence/differential_test.py` and
`evidence/02-program-fidelity.log`.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/reconstruction`; no
candidate kompiled definition or cache was used. K v7.1.293 rebuilt:

1. the trusted concrete semantics with LLVM (`MPY-KRUN` / `MPY-SYNTAX`);
2. `VERIFICATION-BASE` with the Haskell backend;
3. `VERIFICATION` with the Haskell backend.

All builds exit 0. The compiler reports several fixed-semantics
non-exhaustiveness/unused-variable warnings, but none concerns a construct
reachable in this program.

Every positive target claim was run separately:

- `LOOP-SPEC.loop-correct` against the base definition exits 0 and prints
  `#Top` (`evidence/03d-kprove-loop.log`);
- `SPEC.intersection-correct` against the full definition exits 0 and prints
  `#Top` (`evidence/03e-kprove-intersection.log`).

A reviewer-authored concrete program contains the exact submitted function AST
plus 14 boundary assertions. Translation uses the trusted translator. Its LLVM
execution exits 0 with final `.K`, `NoExc`, and exit code 0
(`evidence/03f-krun-concrete.log`). Build commands and outputs are in
`evidence/03a-kompile-llvm.log` through
`evidence/03c-kompile-full.log`; the exact command index is
`evidence/COMMANDS.md`.

## 4. Adequacy and real-program pinning

### Plain-language claims

`LOOP-SPEC.loop-correct` (`/candidate/spec.k:8`) says: in an active call frame,
when `2 <= DIVISOR <= LENGTH`, running the exact remaining `range` loop with
the submitted divisor body, followed by the final `"YES"` return and call end,
returns `primeFrom(LENGTH,DIVISOR)` to an arbitrary continuation and performs
the corresponding frame pop. The claim fixes the relevant local bindings,
environment, scopes, scope allocation pointer, stack, and return state.

`SPEC.intersection-correct` (`/candidate/spec.k:41`) says: for arbitrary K
integers `A,B,C,D` satisfying only `A <= B` and `C <= D`, calling the
`intersection` closure returns
`primeResult(min(B,D)-max(A,C))`, with the explicitly clean initial environment,
scope, heap, stack, return, exception, and exit-code cells. The postcondition is
an equality to a defined value, not a free variable, implication, or tautology.

### Program identity

The entry claim supplies a closure whose body is `intersectionBody`; it does
not execute a `Module` term. This is legitimate here because identity was
checked mechanically:

1. trusted regeneration established submitted `solution.mpy` identity;
2. `evidence/generate_pinning_spec.py` extracted the only translated
   `FuncDef("intersection", Params("interval1","interval2"), BODY)` constructor
   body, without reimplementing its grammar;
3. K's own `kast` parser normalized the program-syntax list units;
4. `CONSTRUCTOR-PINNING-SPEC` equated that exact normalized constructor term
   with `intersectionBody`.

The pinning claim exits 0 with `#Top`; `WarnTrivialClaim` is positive evidence
here because frontend normalization makes the two constructor terms identical
before rewriting. See `evidence/constructor-pinning.k` and
`evidence/04a-constructor-pinning.log`. `divisorBody` is visibly the exact body
embedded in both `intersectionBody` and the loop theorem.

The entry precondition is satisfiable. For example,
`A=0,B=2,C=-1,D=5` satisfies it, gives overlap length 2, and the claimed,
canonical, and submitted results are all `"YES"`. Four additional concrete
substitutions cover composite and degenerate overlaps in
`evidence/04b-ground-substitutions.log`.

There is no domain narrowing: all mathematical integers and every valid pair of
intervals are covered, with no fixed size, unrolling bound, or finite-example
restriction.

### Body sensitivity

In a separate source tree I changed the constructor term actually executed by
the entry claim from `length <= 1` to `length <= 2`. The mutant definition
builds successfully, but the original universal postcondition exits 1 with
`WarnStuckClaimState` and an unmet result equality. A concrete witness is
`(0,2),(0,2)`: the mutant returns `"NO"` while the required prime result is
`"YES"`. See `evidence/05a-body-mutation.diff`,
`evidence/verification-body-mutant.k`, and
`evidence/05c-body-mutant-kprove.log`.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.tsv` inventories every source-level K sentence in
`semantics.k`, all 23 supplied helper files, `verification.k`, and `spec.k`.
It includes:

- 707 explicit rules and both claims;
- 232 syntax-declaration sentences;
- all configuration, context, module, import, and require sentences;
- 151 declarations marked `function`, 107 marked `total`, 46 priority rules,
  35 concrete rules, 26 `owise` rules, all macro/strictness declarations, and
  all 22 `no-evaluators` opaque symbols.

There are no local `functional`, `simplification`, or `anywhere` declarations.
`evidence/rule-assessment.tsv` gives every inventoried sentence a disposition.
`evidence/construct-map.md` maps every submitted constructor to its declaration
and material rules.

The used route is: closure call and left-to-right argument evaluation; tuple
construction; scoped name and builtin lookup; in-bounds tuple subscripting;
variadic integer `min`/`max`; assignments; integer subtraction/comparison and
Python modulo; integer truthiness and branching; `range(2,length)` construction;
range iteration and loop-target binding; string literal construction; and
return/frame pop. Evaluation order, bindings, and state updates on this route
match the actual program. K integers are unbounded, matching Python integers
for this contract. The only strings are ASCII `"YES"`/`"NO"`.

The fixed supplied semantics contains partial or opaque support for unrelated
Python features (notably floats, sorting, MD5, and some totalized
out-of-bounds/unsupported cases). All 22 opaque symbols are unreachable from
this program. Lists, dictionaries, sets, comprehensions, sorting, methods,
floats, slicing, imports, assertions, lambdas/cells, `while`, `break`, and
`continue` cannot rewrite any reachable submitted constructor. I found no
used-path rule that enables a false conclusion on the intended domain.

The proof-local rules are:

- Map frame-deletion normalization
  (`/candidate/verification.k:9`): for a map containing `1 |-> FRAME` and a
  remainder explicitly disjoint from key 1, deleting key 1 yields the
  remainder. This is an elementary K Map fact and affects no program value.
- `intersectionBody` and `divisorBody`: exact definitional aliases, pinned as
  above.
- `yesV` and `noV`: exact ASCII encodings.
- `primeFrom`: disjoint exhaustive-divisor equations. On every reachable use,
  `N > 1` and `2 <= D <= N`; the base case returns YES when the candidate range
  is exhausted, a zero remainder returns NO, and a nonzero remainder strictly
  advances `D`.
- `primeResult`: disjoint `N <= 1` / `N > 1` cases.
- `overlapLength`: exactly `min(B,D)-max(A,C)`.
- the sole priority-40 loop bridge.

The loop bridge's justification is machine checked without the bridge:
`LOOP-SPEC` imports `VERIFICATION-BASE`, not `VERIFICATION`. Its match domain is
the same exact `#loop`, divisor body, trailing `"YES"` return, `#endcall`,
arbitrary `KONT`, local map, call frame, and guard. The auxiliary claim is
universal over the same continuation and framed cells, so there is no
continuation broadening. The bridge reads the named integer locals and changes
the `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<stack>`, and `<ret>` cells
exactly as the proved execution does. The skipped code allocates nothing and
cannot alter heap, heap location, exception, or exit code under
`2 <= DIVISOR <= LENGTH`; those omitted cells are preserved. Abrupt return and
frame popping are included in both the theorem and bridge.

The summary value is not opaque: `primeFrom` has truthful exhaustive equations,
and the bridge-free loop proof connects real loop execution to it. The
body-sensitivity failure separately confirms that real execution is not
bypassed. I found no unsound candidate rule, so no false-conclusion witness is
applicable.

## 6. Fresh non-vacuity test

`evidence/spec-vacuity.k` is reviewer-authored and changes the result obligation
to `noV` for every valid interval pair. This is demonstrably false for the
satisfying input `(0,2),(0,2)`, whose overlap length is the prime 2.

The exact false artifact first passes `kprove --dry-run` (exit 0), establishing
that it parses and builds (`evidence/06a-vacuity-dry-run.log`). The actual proof
then exits 1 with `WarnStuckClaimState`; its residual explicitly contains the
failed equality between `noV` and `primeFrom(overlapLength,2)` under
`overlapLength >= 2` (`evidence/06b-vacuity-kprove.log`). This is the expected
unmet result obligation, not a parser error, timeout, missing import, or
unrelated crash.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics and proof-local definitions, for every
`A,B,C,D : Int` with `A <= B` and `C <= D`, the submitted function's terminating
execution returns `"YES"` exactly when exhaustive divisor search classifies
`min(B,D)-max(A,C)` as prime, and returns `"NO"` otherwise. The loop theorem
establishes the remaining divisor loop for every symbolic length/divisor in its
guard; the entry theorem executes all pre-loop material operations and uses
that proved theorem at the exact loop head. This is a partial-correctness
statement; the audit does not relabel it as a separate K termination theorem.

### Trust boundary and informal/empirical bridges

1. **K implementation and mathematical hooks.** `kompile`, `kprove`, the
   Haskell/LLVM backends, and K's `Int`, `Bool`, `String`, `Map`, and collection
   hooks are trusted. These primitives provide arithmetic, comparison,
   strings, maps, and symbolic reachability; this is the ordinary unavoidable
   checker boundary.
2. **Supplied semantics.** The immutable trusted semantics defines the theorem's
   execution model. Its used subset was statically reviewed and concretely
   exercised; exact tree identity prevents candidate semantic substitution.
3. **Trusted translator.** The mounted translator is trusted to encode CPython
   AST constructors. Byte-identical regeneration and K-parser-level body
   pinning connect its output to the claim.
4. **Map deletion lemma.** The elementary disjoint-key normalization in
   `verification.k:9` is accepted as a derived K Map fact. It affects only
   removal of the callee scope frame.
5. **Source-contract bridge.** The identification of exhaustive divisibility
   with ordinary primality is a direct mathematical argument, not an opaque
   oracle. The canonical/candidate/oracle differential run is finite evidence
   supporting implementation-to-intent alignment; it is not used as a
   substitute for the K proof.
6. **Opaque fixed symbols.** All fixed float/sort/MD5 opaque symbols are outside
   the dependency cone. No claim result, branch, control action, or state update
   depends on them.

Excluded behavior is limited to inputs outside the source contract (non-integer
elements, malformed pairs, or intervals with `start > end`) and general Python
features not used by this function. Resource limits and CPython implementation
details are not part of the theorem. These exclusions do not narrow the
HumanEval contract.

The evidence is reproducible from `evidence/COMMANDS.md`. Differential testing
is used only for its finite implementation/intent bridge; neither it nor the
generation records substitute for either reconstructed `#Top`.

VERDICT: PASS
LEGITIMACY: LEGIT
