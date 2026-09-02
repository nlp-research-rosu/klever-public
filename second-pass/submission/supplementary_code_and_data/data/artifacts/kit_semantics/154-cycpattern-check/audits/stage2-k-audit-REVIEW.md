# Independent adversarial audit: 154-cycpattern-check

This review treats every candidate file, candidate log, generation trace, and
prior report as untrusted evidence. All executable checks used source copied to
`/tmp/audit-work/cycpattern-audit`; neither candidate-provided kompiled
definition was used. Reviewer-authored scripts, mutations, and bounded command
logs are under `/audit-output/evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected mounted paths. The
rendered mode agrees with the mounts: `/reference/reference-semantics` is
present.

The independent checker
[`stage1_integrity.py`](evidence/stage1_integrity.py) verified:

- `/audit-campaign-lock.json` is byte-hash-identical to the recorded
  `ad5dfc...d745`, and its parsed object exactly equals the
  `audit_campaign` block.
- Every pipeline-v3 required record is a readable regular file or directory:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace.
- All recorded individual hashes match the mounted records, including the
  815,726-byte JSONL trace.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- A recursive, type-sensitive manifest of candidate and trusted
  `reference-semantics/` produced the same independent digest,
  `0122ab...f897b`. There are no missing, additional, changed, mistyped, or
  symlinked entries and no symlinks in either semantics tree.

The complete result is in
[`stage1_integrity.log`](evidence/stage1_integrity.log). Generation records
were inspected only as claims. The JSONL inspection parsed all 457 records
(304 response items and 150 event messages); see
[`stage1_generation_trace_inspection.log`](evidence/stage1_generation_trace_inspection.log).
The launcher log inspection is in
[`stage1_generation_output_inspection.log`](evidence/stage1_generation_output_inspection.log).
No provenance or audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two Python words (strings) `a` and `b`, return `True` exactly when `b`
itself or any cyclic rotation of `b` is a contiguous substring of `a`. The six
examples in `/reference/prompt.py` are part of the contract. The contract has
no length bound.

The trusted canonical implementation checks every length-`len(b)` window of
`a` against slices of `b + b`. The submitted `solution.py` first evaluates
`b in a`, then iterates over `b[:-1]`, updating
`rotation = rotation[1:] + c` and accumulating membership with Boolean `or`.
This is a different but extensionally equivalent algorithm on strings. For
`b == ""`, both return `True`.

Trusted regeneration used:

```sh
python3 /tmp/audit-work/cycpattern-audit/trusted/py2mpy.py \
  /tmp/audit-work/cycpattern-audit/candidate-src/solution.py \
  > /tmp/audit-work/cycpattern-audit/candidate-src/solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both translated files have SHA-256
`32e381...29a3`; `cmp` exited 0. Exact evidence is in
[`stage2_translation_identity.log`](evidence/stage2_translation_identity.log).

The independent differential test
[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and candidate entry points and uses a separately written
rotation-oracle. It covers:

- all six documented examples;
- empty strings, one-character boundaries, `b` longer than `a`, initial-hit,
  early-rotation, late-rotation, all-false, repeated, and periodic cases;
- all 3,969 pairs of strings of lengths 0 through 5 over `{a,b}`;
- 5,000 deterministic generated pairs over `abcéΩ🙂`, lengths through 12
  and 9.

The command `python3 /audit-output/evidence/differential_test.py` exited 0
with `total_cases=8992` and `mismatches=0`; see
[`stage2_differential.log`](evidence/stage2_differential.log). These tests are
finite evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

The source-only scratch tree contains candidate `solution.py`,
`solution.mpy`, `verification.k`, `spec.k`, and the integrity-checked
supplied semantics. It contains fresh output directories named
`fresh-runtime-kompiled` and `fresh-verification-kompiled`; the candidate's
`runtime-kompiled/` and `verification-kompiled/` were never copied or read as
definitions.

The live tools are K v7.1.293. Fresh builds used:

```sh
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

Both exited 0. Logs are
[`stage3_kompile_llvm.log`](evidence/stage3_kompile_llvm.log) and
[`stage3_kompile_haskell.log`](evidence/stage3_kompile_haskell.log).
The LLVM compiler's non-exhaustiveness warnings concern unused baseline
operations (`mapStrVS`, float helpers, `joinCodes`, and list `valSeqAt`);
none is on this program's string-only path.

The reviewer concrete fixture
[`concrete_smoke.py`](evidence/concrete_smoke.py) has an AST-identical copy of
the submitted function and 15 normal/boundary assertions. Trusted translation
followed by:

```sh
krun concrete_smoke.mpy --definition fresh-runtime-kompiled
```

exited 0 at `.K`, `NoExc`, and exit code 0. See
[`stage3_concrete_execution.log`](evidence/stage3_concrete_execution.log).

`spec.k` has two positive claims. The auxiliary loop claim independently
closed:

```sh
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.cyc-loop
```

It printed `#Top` and exited 0
([`stage3_kprove_cyc_loop_qualified.log`](evidence/stage3_kprove_cyc_loop_qualified.log)).
The declared all-claims target:

```sh
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC
```

also printed `#Top` and exited 0
([`stage3_kprove_all_claims.log`](evidence/stage3_kprove_all_claims.log)).
This run proves both claims with the loop circularity available to the entry
claim.

For dependency auditing, filtering to only `SPEC.cycpattern-check` removes its
required `SPEC.cyc-loop` circularity. That diagnostic run exited 1 at the
symbolic `#iterNext(str(buildIS(...)))` residual
([`stage3_kprove_entry.log`](evidence/stage3_kprove_entry.log)). This is
positive evidence that the entry theorem actually depends on the loop theorem,
not a failure of the declared two-claim target. An earlier unqualified
`--claims cyc-loop` invocation was rejected as an unused label before proof
execution; the corrected qualified command above is the relevant run.

## 4. Adequacy and real-program pinning

### Entry claim

In plain language, `SPEC.cycpattern-check` assumes an arbitrary pair
`A,B:IntSeq`, the exact initial MPY configuration, and an empty module scope.
It loads the submitted `FuncDef`, calls the resulting binding with
`str(A), str(B)`, and requires the returned `<k>` value to be
`cycPattern(A,B)`. It also requires the module binding to remain exact and
restores `env`, `scopeLoc`, heap, heap allocator, stack, return state,
exception state, and exit code. There is no `requires` restriction and no
finite-size bound.

The mechanical pinning checker
[`check_program_pinning.py`](evidence/check_program_pinning.py) lexes K string
literals, removes only whitespace/comments outside literals, extracts the
balanced `#loadAll` argument, and compares it with regenerated
`solution.mpy`. Both normalized constructor terms have SHA-256
`2587e0...b7f`, and `constructor_term_identity=True`. It also confirms that
the concrete fixture's function AST equals `solution.py`. See
[`stage4_program_pinning.log`](evidence/stage4_program_pinning.log).

Thus the claim executes the submitted binding and body. No external source
filename is standing in for a different theorem term.

### Loop claim

`SPEC.cyc-loop` assumes the real `#loop(str(REMAIN), Name("c"), BODY)` at the
head of an arbitrary continuation. Its local frame contains `a`, `b`, `c`,
`result`, and `rotation` with the exact parent/global-scope shape produced by
the entry claim. It removes the loop and updates:

- `result` to `cycScan(A, REMAIN, ROT, FOUND)`;
- `rotation` to `finalRotation(REMAIN, ROT)`;
- `c` to the last yielded character, or its prior value if `REMAIN` is empty.

Frontend cell completion was independently emitted and inspected in
[`stage4_claim_cell_completion.log`](evidence/stage4_claim_cell_completion.log).
The omitted allocator, heap, stack, return, exception, and exit cells are
arbitrary preserved variables. This is valid for this exact loop body: it
performs only unboxed string operations and three local assignments, contains
no call, allocation, return, exception, break, or continue, and returns through
`#loopLbl` to the framed continuation.

A satisfying entry state is the initial configuration with
`A = "hello"` and `B = "ell"`. A satisfying loop state is obtained with
`L=1`, the real module closure at location 0, any Boolean `FOUND`, any finite
`REMAIN` and `ROT`, and the five exact local bindings. The concrete fixture
and the emitted claim confirm both are realizable.

### Result meaning

For `B = b0...b(n-1)`, the source iterator is
`B[:-1] = b0...b(n-2)`. Starting from `R0=B`, step `i` computes
`R(i+1)=tail(Ri)+bi`, hence
`R(i+1)=B[i+1:]+B[:i+1]`. The initial membership checks offset 0, and the
`n-1` iterations check every other rotation exactly once (possibly with equal
values for periodic strings). For `n=0`, empty-string membership is true and
the loop is empty.

`cycPattern` encodes exactly that fold. Four ground summary instances
(direct hit, false case, rotation-only hit, and empty `b`) normalize to their
expected Booleans and produce `#Top`; see
[`ground-summary.k`](evidence/ground-summary.k) and
[`stage4_ground_summary_config.log`](evidence/stage4_ground_summary_config.log).
The frontend reports these as trivial claims because the closed function terms
normalize before backend execution; they supplement rather than replace the
program proof.

The body-sensitivity mutation
[`fresh-body-sensitivity.k`](evidence/fresh-body-sensitivity.k) changes the
closure actually called to `Return(Bool(true))` while asking for the real
program's false result on `("abcd","abd")`. It builds, executes the mutated
body, and exits 1 at the expected `true ~> .K` residual
([`stage4_body_sensitivity.log`](evidence/stage4_body_sensitivity.log)).
This is a real executed-term mutation.

## 5. Rule-by-rule static soundness review

The exhaustive generated inventory
[`stage5_k_inventory.log`](evidence/stage5_k_inventory.log) covers all 26 K
files used by the proof: the supplied top-level semantics, every helper K file,
`verification.k`, and `spec.k`. It records file/line range, kind, attributes,
disposition, and flattened text for every item. Totals are:

- 1 configuration;
- 232 syntax declarations;
- 703 rules;
- 5 contexts;
- 2 claims.

The attribute audit found 151 declarations carrying `function`, 112 carrying
`total`, 35 concrete-rule blocks, 45 priority-bearing blocks, 26 `owise`
blocks, and 22 explicit `no-evaluators` symbols. There are no local
`simplification`, `functional`, or trusted declarations. Exact attribute
locations are in
[`stage5_special_attributes.log`](evidence/stage5_special_attributes.log).

### Used fixed-semantics path

Every material submitted constructor is declared and executed:

| Program operation | Declaration and rules |
|---|---|
| `Module`, `FuncDef`, statement sequence, docstring `Expr` | `syntax.k`, `core.k`, `functions.k`, `controls.k` |
| binding and `Call(Name(...), ...)` | `core.k`, `call.k`, `functions.k` |
| `Assign`, name lookup, call frame, return/pop | `controls.k`, `core.k`, `functions.k` |
| `For` and target binding | `controls.k`, `iter.k`, `tuple.k` |
| string iterator, literal, concatenation, membership | `str.k`, `operators.k` |
| unary `-1`, Boolean `or` | `int.k`, `bool.k` |
| `b[:-1]` and `rotation[1:]` | `subscript.k` |
| configuration/state restoration | `core.k`, `call.k`, `functions.k` |

Strictness and contexts enforce the source order: assignment RHSs evaluate
before writes; `BinOp` evaluates left then right; comparison evaluates both
operands; `BoolOp("or",...)` short-circuits; a `For` iterable is evaluated once;
and call frames bind arguments left-to-right before body execution. Strings are
unboxed `IntSeq` values, so these operations do not hide heap effects.

The two slice instances are in bounds by construction. `b[:-1]` normalizes to
start 0 and stop `clampLo(isLen(B)-1,1)`. `rotation[1:]` normalizes to
`clampHi(1,isLen(ROT),1)` through the fixed slice rules. `strPrefix` and
`strContains` are complete structural definitions with disjoint base/step
guards.

All remaining supplied rules are listed individually as
`FIXED_SUPPLIED_BASELINE_REVIEWED` in the inventory. Rules outside the table
cannot be reached from this exact program because their constructor, value
sort, operator string, method name, or builtin name does not occur. There is
no global simplification rule that can inject one of those operations onto the
used path. The 22 explicit opaque symbols are the baseline float operations,
`sortVS`, `sortKeyVS`, and `md5hexCodes`; none occurs in the submitted program,
proof-local summaries, claims, or residuals. `MPY-CONCRETE` is present only in
the LLVM definition and contributes no axiom to the Haskell proof definition.

### Proof-local inventory

`verification.k` adds no operational `<k>` rewrite, priority rule,
simplification, concrete rule, opaque symbol, or oracle. It adds five total
functions and eight ordinary equations:

1. `rotateWith(ROT,C)` is exactly the fixed-semantics value of
   `ROT[1:] + C`. Its single equation covers all `IntSeq` values.
2. `cycScan` has disjoint empty/cons equations. The cons equation mirrors the
   exact two loop assignments and strictly recurses on `REST`.
3. `finalRotation` has disjoint empty/cons equations and strictly recurses on
   `REST`.
4. `finalChar` has disjoint empty/cons equations and strictly recurses on
   `REST`, retaining exactly the last one-character yield.
5. `cycPattern` is a single total equation starting with `strContains(B,A)`
   and scanning the fixed-semantics representation of `B[:-1]`.

Coverage, overlap, and descent are therefore complete on the free `IntSeq`
algebra. No proof-local value is fresh or unconstrained.

The loop claim is the bridge-free universal connection theorem for the only
summarized execution region. Its complete context is the exact loop term/body,
the exact local/global binding shape, and an arbitrary preserved continuation
and other cells. One fixed-semantics loop step reaches the same claim with a
strictly smaller `REMAIN`; the empty iterator reaches the RHS. The entry-only
diagnostic residual in Stage 3 confirms the entry theorem does not bypass that
connection claim.

No unsound rule was found, so there is no unsoundness allegation requiring a
false-conclusion witness. The two false residuals in Stages 4 and 6 are
sensitivity evidence, not allegations against a rule.

## 6. Fresh non-vacuity test

The reviewer-created mutation
[`fresh-nonvacuity.k`](evidence/fresh-nonvacuity.k) calls the exact submitted
closure on `("abab","baa")` but changes the result obligation to `false`.
This is meaningfully false: `"baa"` itself is absent, while its left rotation
`"aba"` is a substring. Both trusted canonical Python and candidate Python
return `True`; the witness command and exit 0 are in
[`stage6_witness.log`](evidence/stage6_witness.log).

The proof command was:

```sh
kprove fresh-nonvacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module FRESH-NONVACUITY
```

It parsed and executed successfully, then exited 1 with
`WarnStuckClaimState`; the residual has `true ~> .K` against the requested
`false`. This is the expected unmet result obligation, not a parser error,
timeout, unrelated crash, or unreachable mutation. Full output is in
[`stage6_fresh_nonvacuity.log`](evidence/stage6_fresh_nonvacuity.log).

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following partial-correctness
statement under the supplied MPY semantics:

> For every finite `A,B:IntSeq`, starting in the exact initial configuration,
> loading the constructor term regenerated from `solution.py` and calling
> `cycpattern_check(str(A),str(B))` reaches the Boolean
> `cycPattern(A,B)`, preserves the exact module binding, restores all call
> state, and leaves no exception or nonzero exit.

The structural equations and the loop connection claim establish that
`cycPattern` checks the identity rotation and every nonidentity rotation. The
formal domain is unrestricted in length; it is not a finite unrolling or a
fixed example set.

Trust and evidence boundaries are:

- **Supplied semantics and K implementation.** The integrity-checked reference
  semantics, K frontend, Haskell/LLVM backends, and hooked integer/Boolean/map/
  list/string primitives are trusted. This is the intended low-level boundary,
  not a task-local correctness conclusion.
- **Translator bridge.** The trusted translator is outside the reachability
  theorem. Regeneration establishes byte identity, and constructor extraction
  establishes that the theorem executes that generated term. Differential and
  concrete tests support, but do not universally prove, the translator's
  correspondence with CPython.
- **String model.** Symbolic inputs enter directly as `str(IntSeq)`, so the
  ASCII restriction on source literals affects only the all-ASCII docstring
  and `""`, not the theorem's input domain. Python's material operations here
  (slice, concatenation, iteration, and substring) are sequence operations;
  the `IntSeq` model includes the source-contract string domain and even
  over-approximates it with arbitrary integer elements.
- **Intent bridge.** The equivalence between the transparent `cycPattern`
  equations and “some rotation is a substring” is the elementary index
  argument in Stage 4. It uses no opaque symbol. The 8,992-case differential
  run is additional finite evidence only.
- **Unused opaque primitives.** The 22 supplied float/sort/MD5 opaque symbols
  have no dependent claim and contribute no conclusion here.
- **Termination.** The reported theorem is partial correctness. Structural
  descent makes termination plausible for finite inputs, but no separate
  liveness or resource theorem is claimed.

Gate A passes: the real body executes, summaries are connected by the proved
loop claim, the result is constrained, and both body and result mutations are
rejected. Gate B passes: the theorem covers the unrestricted material
string-contract domain and states the intended predicate. Gate C passes: all
source, commands, outputs, finite evidence, and trust boundaries are preserved
and separated from the formal proof.

VERDICT: PASS
LEGITIMACY: LEGIT
