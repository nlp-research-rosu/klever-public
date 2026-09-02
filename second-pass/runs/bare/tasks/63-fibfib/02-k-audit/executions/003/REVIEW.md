# Independent adversarial audit: 63-fibfib

The candidate contains a legitimate partial-correctness proof of the submitted
program for every nonnegative integer input. I rebuilt both definitions from
source, executed the regenerated program under the generated semantics, proved
the claims afresh, mechanically compared the claim's program macro with the
trusted-regenerated constructor term, reviewed every local declaration and
rule, and rejected two independent false mutations.

## 1. Input and provenance integrity

`/audit-input.json` declares `legacy-selected-stage1`,
`GENERATED_SEMANTICS`, problem `63-fibfib`, and condition `bare`. The mounted
records required for that layout are present, readable regular files:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one JSONL trace below `/generation-evidence/codex-trace/`;
- the additionally retained `legacy-run-input.json` and
  `legacy-metrics.json`.

The independent checks are in
`evidence/stage1_integrity.py` and
`evidence/stage1_integrity.log`. The exact command was:

```text
python3 /audit-output/evidence/stage1_integrity.py
```

It exited 0. Every launcher-recorded ordinary-file hash matched, including the
trace file hash recorded by `generation-result.json`. An independent
pipeline-format digest of `/candidate` was
`88fe6f2159111185510bb69a53df1be53714742c15550e135a7944127d23c4d8`,
equal to the selected-stage `workspace_sha256`. The corresponding trace-tree
digest was
`322d3185675c335e48ed0de4ce8d5744d5fda597aee2474d038808206077883f`,
equal to `usage.json`'s `source_trace_sha256`. The audit-input also records
launcher-specific aggregate digests; all independently inspectable
constituents and the selected-stage tree digests agree.

`/audit-campaign-lock.json` has SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`, and its parsed object is exactly the embedded
`audit_campaign` object. The task manifest matches all embedded task fields;
the embedded copy additionally carries the launcher-added `config` field.

There are no symlinks or unsupported entry types in the candidate or trace
trees. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`, respectively. The required
proof sources `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`,
and `spec.k` are present.

The generated-semantics boundary is consistent: there is no
`/reference/reference-semantics` and no candidate `reference-semantics/`.
Thus no hidden or supplied semantics was used.

I parsed all 181 structured trace records and scanned the full 9,820-line
generation log. The bounded inventory is in
`evidence/generation_record_inspection.log`; these records were treated only
as untrusted historical claims. No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract defines the integer FibFib sequence on nonnegative indices:

```text
F(0) = 0
F(1) = 0
F(2) = 1
F(n) = F(n-1) + F(n-2) + F(n-3), for n >= 3
```

The prompt asks for an efficient computation of its `n`-th element. Negative
indices are not elements of this recursively based sequence; the trusted
canonical implementation also has no normal value for them. Therefore the
formal restriction `N >= 0` does not narrow the source-contract domain.

The trusted canonical implementation is recursive. The candidate implements
the equivalent iterative state:

```text
(a,b,c) = (F(i),F(i+1),F(i+2))
```

starting at `i=0`, advancing the triple once per loop iteration, and returning
`a` at `i=n`.

I regenerated the constructor term with the trusted translator:

```text
python3 /tmp/audit-work/63-fibfib/trusted/py2mpy.py solution.py > solution.trusted-regenerated.mpy
cmp --silent solution.mpy solution.trusted-regenerated.mpy
```

Both commands exited 0. Both files have SHA-256
`4ae5eadda2bc9e05737c549a4ae38413d20a0bd9a520a71bf1100855124657f0`.
See `evidence/stage2_fidelity.sh` and `evidence/stage2_fidelity.log`.

The independent differential script
`evidence/differential_test.py` imports the trusted canonical and submitted
entry points. It tested the documented examples, lower and recurrence
boundaries `0..4`, deterministic generated inputs (seed `630063`), and
representative inputs through `20`. All 17 distinct cases matched, including
`F(0)=0`, `F(5)=4`, `F(8)=24`, and `F(20)=35890`; mismatch count was zero.
This is finite fidelity evidence, not the universal proof.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/63-fibfib`; no candidate
compiled definition or cache was used. K 7.1.293 was independently available.
The exact clean build commands were:

```text
kompile --backend llvm semantic.k --main-module FIBFIB \
  --syntax-module FIBFIB-SYNTAX --output-definition concrete-kompiled

kompile --backend haskell semantic.k --main-module FIBFIB \
  --syntax-module FIBFIB-SYNTAX --output-definition proof-kompiled
```

Both exited 0. Complete commands and bounded logs are in
`evidence/stage3_reconstruct.sh`, `evidence/stage3_reconstruct.log`,
`evidence/stage3_concrete_build.log`, and
`evidence/stage3_proof_build.log`.

Fresh LLVM execution of the actual regenerated `solution.mpy` was compared
with both Python implementations for `n = 0,1,2,3,5,8,10,20`. Every `krun`
exited 0 and all results matched. The exact commands and results are in
`evidence/semantics_concrete_compare.py` and
`evidence/stage3_concrete_execution.log`. Full final states for `n=0..3`,
including the environment triple and loop counter, are in
`evidence/stage5_state_execution.log`.

The fresh positive proof commands were:

```text
timeout 120s kprove spec.k --definition proof-kompiled \
  --spec-module FIBFIB-SPEC \
  --claims FIBFIB-SPEC.loop-invariant -w none

timeout 120s kprove spec.k --definition proof-kompiled \
  --spec-module FIBFIB-SPEC -w none
```

The auxiliary invariant alone exited 0 and printed exactly `#Top`. The
all-claims command, which proves `program-correct` with its required
`loop-invariant` circularity and also proves that circularity, exited 0 and
printed exactly `#Top`. See `evidence/stage3_proofs_continue.sh` and
`evidence/stage3_proofs_continue.log`.

As a diagnostic, selecting only `program-correct` while deliberately filtering
out its auxiliary circularity timed out after 15 seconds with no result
(`evidence/stage3_program_only_diagnostic.log`). This is not a failed target
proof: claim filtering removed a declared proof dependency, whereas the
complete positive proof set closes immediately.

## 4. Adequacy and real-program pinning

In plain language, `program-correct` says:

- for arbitrary K integer `N` satisfying `0 <= N`;
- start the submitted FibFib module with invocation argument `N`, an empty
  environment, and result cell `0`;
- execution reaches an empty computation;
- the final environment is exactly
  `a=F(N), b=F(N+1), c=F(N+2), i=N, n=N`;
- the returned result is exactly `F(N)`.

This is result-constraining and stronger than the requested return-value
property.

The `loop-invariant` claim says that for arbitrary `0 <= I <= N`, a real loop
head with environment
`a=F(I), b=F(I+1), c=F(I+2), i=I, n=N`, followed by the actual return
continuation, reaches the same final environment and returns `F(N)`. Its
arbitrary initial result cell is overwritten by the real return rule.

The theorem executes the submitted program rather than a substitute.
Using the fresh concrete definition, I parsed both `solution.mpy` and the
claim's `fibfibProgram` with module `FIBFIB-VERIFICATION`, sort `Pgm`, and
`--expand-macros`. The resulting KORE files are byte-identical and both have
SHA-256
`c4a554fe1c9fdf9cf8e55a400ab532fc86e251d055391fe903aa7256cbd57652`.
The exact commands are in `evidence/stage4_pinning.sh`; the terms are
`evidence/kast_solution_expanded.kore` and
`evidence/kast_fibfibProgram_expanded.kore`.

Satisfiable witnesses are explicit:

- `program-correct`: `N=5`, empty environment, result `0`; its claimed result
  is `F(5)=4`, matching both Python implementations.
- `loop-invariant`: `I=2, N=5`, environment
  `a=1,b=1,c=2,i=2,n=5`, and any initial result (the evidence uses `77`);
  the claimed final state is `a=4,b=7,c=13,i=5,n=5`, result `4`.

Additional substitutions at `N=0,2,5,8` agree with both Python
implementations; see `evidence/claim_witnesses.py` and
`evidence/stage4_pinning.log`.

For body sensitivity, I changed the `fibfibProgram` macro's executed
initializer from `c=1` to `c=2`, not merely an external source file. The
mutation is preserved as `evidence/body-mutation-verification.k`. It compiled
successfully, then the complete proof exited 1 with `WarnStuckClaimState` and
the residual environment `c |-> 2`. See
`evidence/stage4_body_sensitivity.sh` and its logs. The theorem therefore
depends on the actual body.

## 5. Rule-by-rule static soundness review

There are exactly three local K source files and no hidden helper K file. The
numbered sources are preserved in `evidence/stage5_numbered_sources.log`.

### Local syntax and attributes

The complete local syntax inventory is:

| ID | Location | Declaration and assessment |
|---|---|---|
| S1 | `semantic.k:7` | `Pgm ::= Module(Stmts)`, symbol `moduleAst`; exact translated module shape. |
| S2 | `semantic.k:9` | `Stmts ::= List{Stmt,""}`; preserves source order. |
| S3-S6 | `semantic.k:11-14` | `FuncDef`, `Assign`, `While`, `Return`, with AST symbols; these are all statement forms used. |
| S7 | `semantic.k:16` | `Params(Strings)`, symbol `paramsAst`. |
| S8 | `semantic.k:17` | comma-separated `Strings` list. |
| S9-S13 | `semantic.k:19-23` | `Name`, `Int`, `BinOp`, `Compare`, `TupleExpr`, with AST symbols; these are all expression forms used. |
| S14-S16 | `semantic.k:25-27` | expression list, `CmpOp`, and comparison-operation list. |
| S17-S28 | `semantic.k:37-48` | control items `invoke`, `finish`, `assignTo`, `binRhs`, `applyBin`, `compareRhs`, `applyCompare`, `tupleSecond`, `tupleThird`, `tupleStore`, `whileDecision`, `returnValue`. Each represents one explicit evaluation stage. |
| S29 | `semantic.k:50` | results are K `Int` or `Bool`; the target's expressions produce only these. |
| V1 | `verification.k:5` | `fibfibMath(Int)` is `[function,total]`. |
| V2-V4 | `verification.k:6-8` | macros `fibfibProgram`, `loopCondition`, and `loopBody`. |

There is no local `functional` declaration, opaque symbol, priority rule,
`simplification` rule, or other attribute affecting proof strength. The
configuration (`semantic.k:52-57`) has only the computation, integer-valued
environment map, and result cells actually read or written.

The grammar intentionally admits some unused strings, list lengths, and
constructor combinations for which no semantic rule applies. Such unsupported
terms stop visibly. Every combination occurring in `solution.mpy` is covered;
missing semantics for unused combinations is permitted in
`GENERATED_SEMANTICS`.

### Operational rules

Every ordinary semantic rule is inventoried below:

| Rule | Location | Review |
|---|---|---|
| R1 module/invoke | `semantic.k:59-61` | Matches the exact single `fibfib(n)` binding and body, initializes only `n`, and schedules that captured body plus `finish`. It cannot select a same-named external body. |
| R2 statement head | `:63` | Executes the head before the remaining statement list. |
| R3 empty statements | `:64` | Removes only the empty statement-list token. |
| R4 integer literal | `:66` | Maps translated `Int(I)` to the same unbounded K integer. |
| R5 name lookup | `:67-68` | Reads the value under exactly `X`; unbound names get stuck rather than fabricate a value. |
| R6-R8 binary addition | `:70-72` | Evaluates left operand, then right operand, then applies `+Int`. Other operator strings stop. This is Python's order and value on the used integer `+`. |
| R9-R11 comparison | `:74-76` | Evaluates the left then the single right operand and implements only the used integer `<`. |
| R12-R13 scalar assignment | `:78-80` | Evaluates before updating exactly one map binding. |
| R14-R17 triple assignment | `:82-89` | Evaluates all three RHS expressions left-to-right in the old environment, then performs the three target writes. This preserves Python tuple evaluation and simultaneous-assignment behavior; duplicate target names would also end with the rightmost write. |
| R18-R20 while | `:91-94` | Re-evaluates the condition each iteration; true schedules body then loop, false exits. No state cell is skipped. |
| R21 return evaluation | `:96` | Evaluates the return expression before control transfer. |
| R22-R23 top-level return | `:97-100` | Match only the exact empty-list/direct `finish` contexts and store the evaluated integer. They do not accept an arbitrary continuation or hide effects. Both overlapping normalization paths have the same result and final control. |

These rules cover `Module`, the exact function and parameter, ordered scalar
initializations, integer/name expressions, the `<` guard, `+`, the three-name
tuple assignment, scalar counter update, loop control, and return. Concrete
`n=0` exercises the zero-iteration path; positive cases exercise every
remaining material rule.

The semantics is deliberately smaller than Python: unsupported operators,
chained comparisons, differently shaped tuple assignments, unbound variables,
and a non-final return can get stuck. None occurs in the submitted term or the
claims. No used construct is replaced by an oracle or fabricated result.

### Verification rules and claims

`verification.k` has exactly six rules:

| Rule | Review |
|---|---|
| M1 `loopCondition` (`:10-11`) | Exact alias for `i < n`; compile-time normalization, not an execution bridge. |
| M2 `loopBody` (`:13-18`) | Exact alias for the two translated body statements. |
| M3 `fibfibProgram` (`:20-28`) | Exact alias for the complete submitted constructor tree, mechanically confirmed by KORE equality. |
| F1 `fibfibMath(N)=>0` when `N<=1` (`:30`) | Defines the two nonnegative bases used by the theorem and a harmless total extension below zero. |
| F2 `fibfibMath(2)=>1` (`:31`) | Exact third base. |
| F3 recurrence for `N>=3` (`:32-35`) | Exact contract recurrence; all recursive arguments decrease. |

The three function guards are pairwise disjoint and cover every K integer, so
the `[total]` declaration is justified. The only extension below the sequence
domain is the explicit value 0 for negative arguments; no claim or recurrence
step in the `N>=0` theorem can depend on a negative call. There is no overlap,
non-descent, opaque value, circular oracle, or operational preemption.

`spec.k` contains exactly the target claim and its loop circularity. The latter
matches the real stable loop head, exact invariant environment, and exact
return/finish continuation. It does not summarize an arbitrary continuation or
omit a modified state cell.

No rule was found unsound, so there is no false-conclusion witness to report.
The actual-body mutation instead confirms execution sensitivity.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created the distinct reviewer
artifact `evidence/spec-vacuity-audit.k`. It preserves the genuine loop
invariant and changes only the target result to
`fibfibMath(N) +Int 1`.

`N=0` is a satisfying witness: the real and claimed original result is 0,
whereas the mutation demands 1. The exact commands were:

```text
kprove spec-vacuity-audit.k --definition proof-kompiled \
  --spec-module FIBFIB-SPEC-VACUITY --dry-run -w none

timeout 120s kprove spec-vacuity-audit.k \
  --definition proof-kompiled \
  --spec-module FIBFIB-SPEC-VACUITY -w all
```

The dry run exited 0, proving the mutation parsed and built. The proof exited 1
without timeout and produced `WarnStuckClaimState`; its implication residual
explicitly contains:

```text
fibfibMath ( N ) +Int 1 #Equals fibfibMath ( N )
```

Thus failure is the expected unmet result obligation, not a parser, import,
backend, or reachability accident. See `evidence/stage6_nonvacuity.sh`,
`evidence/stage6_vacuity_dry_run.log`, and
`evidence/stage6_vacuity_kprove.log`.

## 7. Proven versus assumed accounting

What is formally proved under the rebuilt K theory is:

- for every unbounded K integer `N >= 0`, symbolic execution of the exact
  trusted-regenerated constructor program from the stated initial cells
  satisfies the exact final environment and returns `fibfibMath(N)`;
- the loop invariant is valid for every symbolic `0 <= I <= N`;
- `fibfibMath` has precisely the three source-contract equations.

This is a partial-correctness statement in the Kit sense. It does not claim
behavior for negative indices or for Python constructs absent from this closed
program.

The trust and evidence ledger is:

| Boundary | Influence | Judgment and support |
|---|---|---|
| K parser, kompilers, Haskell/LLVM backends, and reachability/circularity machinery | Proof execution and closure | Standard low-level trusted computing base; fresh builds and cross-backend concrete/proof runs succeeded. |
| Built-in `Int`, `Bool`, `Map`, list, and K-sequence operations | Arithmetic, guards, environment updates, scheduling | Ordinary K primitives; no candidate axiom changes them. |
| Trusted `/reference/py2mpy.py` | Python-AST-to-constructor bridge | Launcher hash verified; trusted regeneration is byte-identical. |
| Generated `semantic.k` | Meaning of every used constructor | Not assumed: audited rule by rule above and concretely exercised on zero and positive loop paths. |
| `fibfibMath` equations | Final result and invariant values | Not opaque or empirical: exhaustive, disjoint, decreasing equations exactly state the source sequence contract. |
| `fibfibProgram`/loop macros | Program identity and invariant syntax | Exact definitional aliases; expanded KORE equality pins the submitted term. |
| Trusted canonical Python implementation | Differential oracle only | Seventeen source-level and eight K/Python cases matched; finite evidence is not used as the universal proof. |
| Informal source-intent reading | Domain is nonnegative indices of a sequence | Supported by the base/recurrence definition and the canonical's lack of a normal negative-index value; no material domain restriction. |

There is no result-bearing opaque symbol, external program-derived primitive,
operational bridge, proof-local priority rule, or unproved lemma. Gate A
(real-program soundness and non-vacuity), Gate B (full intent adequacy), and
Gate C (auditable trust/evidence) all pass. The generated-semantics audit
therefore supports `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
