# Independent adversarial review: HumanEval/3 `below_zero`

This review treats every candidate artifact and generation record as untrusted
evidence. I copied only source artifacts into `/tmp/audit-work/rebuild`, built
new definitions there, and did not use `/candidate/semantic-llvm`,
`/candidate/verification-haskell`, `kore-exec.tar.gz`, or any candidate cache.

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over the full intended `List[int]` domain. The
verdict is `CONCERNS / LEGIT`, rather than `PASS`, because the generated
semantics deliberately uses several rules broader than the exact program
syntax—most notably treating every `ImportFrom` as a no-op—and because its
connection to CPython is an audited model/empirical boundary rather than a
machine-checked language-refinement theorem. Those limitations do not permit a
false result for the immutable submitted program or narrow its input domain.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `3-below-zero`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- candidate mount `/candidate`;
- trusted mounts `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

The legacy-selected layout requires `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. All are present,
readable regular files. `usage.json` is present and was also checked.
`runtime-metrics.json` is absent, which is permitted for this historical
layout. All required directories are real directories, and a recursive
type-aware digest rejected no linked or unsupported candidate/trace entry.

The audit campaign object is byte-independently parsed and exactly equals
`/audit-campaign-lock.json` as a JSON object. Its recorded SHA-256,
`ad5dfcc0...1a78d745`, matches the mounted file. The canonical, trusted prompt,
trusted translator, run manifest, task manifest, stage-1 result, invocation,
metrics, usage, generation prompt, final message, and output log all match
their hashes in `/audit-input.json`. The only trace JSONL file matches its
per-file hash in `/generation-result.json`.

The independently reimplemented pipeline tree digest of `/candidate` is
`639f7233b9f8918bec0053d213458ef1f8a66a190c4488c1b19e0914a5bd2f91`.
It matches both `generation-result.outputs.workspace_sha256` and
`invocation.retained_workspace_sha256`. The corresponding independent trace
digest is
`a4c05b7d4a93a210115c5c78316759e8640b716beedd1105d1980350fb7c8b08`,
matching `usage.source_trace_sha256`. The audit manifest additionally records
launcher-specific tree fingerprints
`75eac349...78a8543` and `eff5029a...c04e5a7`; their serialization is not
declared in the manifest, so the review preserves them rather than pretending
they use the pipeline serialization. The same mounted content is independently
pinned by the pipeline digests and all declared per-file hashes.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounts, agreeing with every field in the manifest integrity block.
As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` does not exist. There is no semantics-mode
contradiction or infrastructure breach.

I parsed all 305 JSON objects in the structured trace, summarized all 62 tool
calls and 62 outputs, and scanned the complete 18,323-line
`codex-output.log`. They claim successful generation and two `#Top` results;
none of those claims was trusted for the later verdict.

Evidence:

- [integrity audit script](/audit-output/evidence/integrity_audit.py) and
  [complete result](/audit-output/evidence/stage1-integrity.log)
- [trace parser](/audit-output/evidence/trace_summary.py) and
  [bounded trace summary](/audit-output/evidence/stage1-trace-summary.log)

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: given a finite list of integer deposits and
withdrawals and an initial balance of zero, return `True` exactly when at least
one running prefix sum is strictly negative; otherwise return `False`.
An exact zero balance is not below zero.

`/candidate/solution.py` implements that contract directly: it initializes
`balance = 0`, adds each operation in order, returns `True` immediately after a
negative prefix, and returns `False` after exhausting the list. It differs from
the trusted canonical implementation only in an immaterial local variable
name and omitted docstring.

I regenerated the constructor program in scratch with the trusted translator:

```text
python3 trusted-py2mpy.py solution.py > solution.regenerated.mpy
sha256sum solution.mpy solution.regenerated.mpy
cmp -l solution.mpy solution.regenerated.mpy
```

Both files have SHA-256
`9ffee3cf630e5a15d0fc1e32c990a029e920330f41b306516f1bcc0b5d44219d`;
`cmp` exits 0. See
[translation log](/audit-output/evidence/stage2-translation.log).

The independent differential script loads the trusted canonical and candidate
entry points by separate paths and compares both with a separately written
prefix-accumulator oracle. It covers:

- the two prompt examples;
- empty, immediate-negative, exact-zero, post-zero-negative, and
  early-return/recovery boundaries;
- arbitrary-precision positive/negative values;
- every list of lengths 0 through 5 over `[-3, 3]` (19,608 lists);
- 1,000 seeded lists of lengths 0 through 30 containing ordinary,
  64-bit-edge, and arbitrary-precision integers.

All 20,618 cases agree, with zero mismatches. The generated scope, seed, and
oracle are preserved in
[differential.py](/audit-output/evidence/differential.py),
[input scope](/audit-output/evidence/differential-input-scope.txt), and the
[result log](/audit-output/evidence/stage2-differential.log).

Stage 2 result: PASS.

## 3. Clean proof reconstruction

The scratch directory contained no candidate-built K definition. The only
pre-build directory was Python's locally generated `__pycache__`. The observed
toolchain was K `v7.1.293` for `kompile`, `krun`, and `kprove`
([versions](/audit-output/evidence/stage3-tool-versions.log)).

Fresh concrete definition:

```text
timeout 600 kompile semantic.k --backend llvm \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-llvm
```

It exited 0
([LLVM build log](/audit-output/evidence/stage3-kompile-llvm.log)).
Eleven fresh `krun` executions covered empty, zero, positive, immediate
negative, both prompt examples, exact-zero and subsequent-negative boundaries,
early return, and values of magnitude `2**80`. Every run exited 0, ended with
`.K`, reset the two internal local cells, and returned the same Boolean as the
independent Python oracle
([script](/audit-output/evidence/semantics_concrete_check.py),
[passing log](/audit-output/evidence/stage3-concrete-semantics-pass.log)).
The earlier
[reviewer-harness attempt](/audit-output/evidence/stage3-concrete-semantics.log)
failed only because the reviewer's output regex was accidentally
double-escaped; the raw output in that log already contained the correct
`BoolV(false)`. The fixed parser and all subsequent runs pass.

Fresh proof definition:

```text
timeout 600 kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-haskell
```

It exited 0
([Haskell build log](/audit-output/evidence/stage3-kompile-haskell.log)).
Every candidate positive target was then run independently:

```text
timeout 600 kprove spec.k --definition audit-verification-haskell \
  --spec-module SPEC --claims SPEC.entry-reaches-loop
#Top
# exit 0

timeout 600 kprove spec.k --definition audit-verification-haskell \
  --spec-module SPEC --claims SPEC.loop-correct
#Top
# exit 0
```

The exact outputs are in the
[entry log](/audit-output/evidence/stage3-kprove-entry.log) and
[loop log](/audit-output/evidence/stage3-kprove-loop.log). Running the complete
spec without claim filtering also printed `#Top` and exited 0
([all-claims log](/audit-output/evidence/stage3-kprove-all.log)).

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claim scope

`entry-reaches-loop` has no explicit `requires`. Its source pattern is the
exact submitted `Module(...)`, arbitrary `OPS:IntList` in `<input>`, balance
and current both zero, and `NoResult`. Its destination is the exact loop body
and post-loop `return False` continuation with all other cells unchanged. In
plain language, it proves that loading the fixed module under this generated
entry-call convention reaches the loop cut point for every integer list.

`loop-correct` also has no explicit `requires`. Its source permits arbitrary
`B:Int`, arbitrary `OPS:IntList`, any original input and prior current value,
and requires `NoResult`. Its destination consumes the computation, resets the
two internal local cells, and puts
`BoolV(belowZeroFrom(B, OPS))` in `<result>`. The target result is neither free
nor existential: it is fixed by a total, transparent recursive function.

The claims compose mechanically. Substituting `B = 0`, `_C = 0`, and
`_ORIGINAL = OPS` makes the destination configuration of
`entry-reaches-loop` exactly the source configuration of `loop-correct`.
Reachability transitivity therefore establishes the full module result
`BoolV(belowZeroFrom(0, OPS))`.

### Constructor-level identity

I extracted the balanced `Module(...)` term from the entry claim, normalized
only the explicit rule-syntax empty list `.Stmts` to its equivalent zero-token
program spelling, and parsed both it and the trusted regenerated
`solution.mpy` with `kast --sort Program --output json`. The two JSON ASTs are
byte-identical with SHA-256
`293fc511dc312bc00e567c8ab5df8164a049a82828db1e45700bdac49aa8ccbe`.
See the
[extractor](/audit-output/evidence/extract_claim_program.py),
[comparison log](/audit-output/evidence/stage4-program-pinning-pass.log), and
the two parsed terms
[from regeneration](/audit-output/evidence/regenerated-program.kast.json) and
[from the claim](/audit-output/evidence/entry-claimed-program.kast.json).
The first comparison attempt is retained separately: its parser error was
precisely why the explicit empty-list spelling needed normalization, not a
constructor mismatch.

### Satisfying states and concrete substitution

The exact initial configuration with
`OPS = cons(1, cons(2, cons(-4, cons(5, .IntList))))` satisfies the entry
claim's source. The corresponding loop cut point with `B = 0`, current zero,
and `NoResult` satisfies the loop claim's source. Fresh ground reachability
claims for both states print `#Top` and exit 0
([witness spec](/audit-output/evidence/ground-witness.k),
[entry result](/audit-output/evidence/stage4-ground-entry.log),
[loop result](/audit-output/evidence/stage4-ground-loop.log)).
The claimed ground result is `BoolV(true)`; both Python implementations return
`True` on `[1, 2, -4, 5]`
([Python result](/audit-output/evidence/stage4-ground-python-pass.log)).

For body sensitivity, I changed the early-return Boolean inside the
`Module(...)` term actually executed by the entry claim while leaving its
destination at the original body. The mutation parses and executes, but
`kprove` exits 1 with `WarnStuckClaimState`; the empty-list residual reaches
`BoolV(false)` and cannot match the original destination
([mutation](/audit-output/evidence/spec-body-sensitivity.k),
[result](/audit-output/evidence/stage5-body-sensitivity.log)).
This is a claim-term mutation, not merely a change to an external Python file.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

There are no generated helper K source files beyond `semantic.k`,
`verification.k`, and `spec.k`. The complete numbered source and counts are in
[the inventory log](/audit-output/evidence/stage5-local-definition-inventory.log):
12 syntax declarations in `semantic.k`, 22 operational rules, one proof-local
syntax declaration with two equations, and two claims.

### Local syntax, configuration, and attributes

The syntax inventory is exhaustive:

1. `Program ::= Module(Stmts)`;
2. the associative `Stmts` list;
3. `Params(Strings)`;
4. the comma-separated `Strings` list;
5. statement constructors `ImportFrom`, `FuncDef`, `Assign`, `AugAssign`,
   `For`, `If`, and `Return`;
6. expression constructors `Name`, `Int`, `Bool`, and `Compare`;
7. `CmpOp`;
8. the comma-separated `CmpOps` list;
9. finite integer lists `.IntList` and `cons`;
10. `PyVal` constructors `IntV`, `BoolV`, and `ListV`;
11. `Result ::= NoResult | PyVal`;
12. internal computations `execStmts`, `setBalance`, `branch`, `loop`, and
    `doReturn`.

The configuration has exactly the needed state: `<k>`, the supplied
`IntList`, two local-variable cells, and the returned result. There is no heap,
allocation, I/O, exception, or call-stack state because the submitted body
does not exercise those features.

The only local function/total declaration is
`belowZeroFrom(Int, IntList) [function, total]`. There are no local
`functional`, `simplification`, `concrete`, `priority`, `owise`, `anywhere`,
`macro`, `trusted`, or opaque declarations. The only special claim attribute
is `[circularity]` on `loop-correct`.

### Construct mapping

Every constructor in `solution.mpy` is covered. `Module` and `Stmts` use
rules 1–3 below; the exact typing import uses rule 4; the exact function
binding uses rule 5; initialization uses rules 6, 7, and 17; iteration uses
rules 9–11 and 19; the update uses rule 8; the conditional uses rules 12–14
and 22; and returns use rules 15, 16, and 18. `Params`, `Strings`, `CmpOp`,
and the nested `Name` terms are structurally matched by those rules.
Rules 20 and 21 provide ordinary standalone lookups as well, although the
specialized update/comparison rules consume those exact nested names directly.

### Operational rules

Each of the 22 local semantic rules was reviewed:

| # | Rule | Static decision |
|---:|---|---|
| 1 | `Module(SS) => execStmts(SS)` | Correct statement-sequence entry for the generated representation. |
| 2 | empty `execStmts` | Correctly consumes an empty sequence. |
| 3 | nonempty `execStmts` | Preserves left-to-right statement order and the suffix. |
| 4 | `ImportFrom(_, _) => .K` | Correct for the fixed typing-only import, but syntactically over-broad; this is a non-fatal scope concern discussed below. |
| 5 | exact `below_zero(operations)` `FuncDef` | Correct entry-call harness for the fixed translated module; it is not a general Python definition rule. |
| 6 | assignment schedules expression then `setBalance` | Correct evaluation order. |
| 7 | `IntV(I) ~> setBalance` | Writes exactly the evaluated integer. |
| 8 | exact `balance += operation` | Adds the current mathematical integer once. The bypassed name lookup is side-effect-free and equal to rule 20 on every admitted input. |
| 9 | exact `for operation in E` | Evaluates the iterable before entering the loop. |
| 10 | empty-list loop | Correct zero-iteration behavior. |
| 11 | `cons` loop | Binds the head before executing the body and recurs on the tail; it preserves the required continuation. |
| 12 | `If` schedules its condition | Correct condition-before-branch order. |
| 13 | true branch | Executes exactly the `then` sequence. |
| 14 | false branch | Executes exactly the `else` sequence. |
| 15 | `Return(E)` | Evaluates the return expression first. |
| 16 | completed return | Stores exactly `V`, discards the current function continuation, and resets only internal local cells. This is correct for the sole entry frame but broader than a general call-stack semantics. |
| 17 | integer literal | Preserves the K mathematical integer. |
| 18 | Boolean literal | Preserves the Boolean. |
| 19 | `operations` lookup | Returns exactly the supplied `IntList`. |
| 20 | `operation` lookup | Returns exactly the current loop element. |
| 21 | `balance` lookup | Returns exactly the current balance. |
| 22 | exact `balance < 0` comparison | Computes K integer strict inequality, matching Python arbitrary-precision integer comparison. |

The empty/nonempty statement and list rules are disjoint. The true/false
branch rules are disjoint. Literal and name constructors are disjoint. No
priority is needed, and no local rule overlap can produce conflicting results.
The specialized update and comparison have no side effects in their skipped
operand lookups and preserve all relevant cells.

Rule 16's abrupt continuation discard was checked against every reachable
context of the submitted body: on early `return True` it removes the remaining
loop and `return False`; on the final `return False` it removes only sequence
bookkeeping. The only observable cell is assigned the already evaluated
Boolean. There is no caller frame or stateful cleanup in this language subset.
The concrete early-return case `[-1, 100]`, exact-zero case `[5, -5]`, proof
claim, ground witness, and false mutation all exercise that distinction.

### Proof-local equations and claims

The base equation
`belowZeroFrom(_, .IntList) => false` and recursive `cons` equation are
constructor-disjoint and cover every finite `IntList`. The recursion descends
strictly on the tail. For a new head, the equation returns `true` exactly when
the new prefix is negative; otherwise it adds that head to the starting
balance and checks the remaining prefixes. By induction on `IntList`, this is
exactly the natural-language prefix-sum property. It is a transparent
definitional summary, not an opaque or program-execution-replacing oracle.

`entry-reaches-loop` executes the complete submitted constructor body to a
real control-flow cut point. `loop-correct` recurs only after the operational
semantics consumes a `cons` iteration and returns to the same shape with a
strictly smaller tail; the empty list closes without circularity. The fresh
false-result mutation confirms that circularity cannot close without satisfying
the result.

There is no proof-local operational bridge, opaque result, task-answer axiom,
unconstrained fresh symbol, or simplification lemma.

### Non-fatal generated-semantics scope concern

Some semantic rules accept more program terms than their justification. For
example, rule 4 also rewrites
`ImportFrom("__definitely_missing__", "x")` to `.K`, whereas CPython would
raise `ModuleNotFoundError`; rule 5 auto-invokes any body under the matching
name/signature, whereas Python module loading alone only binds a function.
Those are concrete off-program differences and prevent treating `semantic.k`
as a reusable Python semantics.

They do not give a false conclusion on the intended domain: the theorem's
program term is mechanically fixed to the submitted module, its only import
is the available typing-only import whose binding is unobserved, the input
domain varies only `operations`, and the function-entry convention is explicit
in the configuration. I found no concrete or symbolic false-result witness for
any `List[int]` satisfying the entry source. Accordingly these are evidence and
reuse limitations, not material semantic unsoundness or domain narrowing.

Stage 5 result: PASS for real-program soundness, with the stated non-fatal
scope concern.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. The fresh
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) copies the exact
`loop-correct` source but changes its result-bearing destination to the
constant `BoolV(true)`.

The source is satisfiable at `B = 0` and `OPS = .IntList`. Both trusted
canonical and candidate Python return `False` for the corresponding input
`[]`; the mutation demands `True`
([witness log](/audit-output/evidence/stage6-vacuity-witness.log)).

First, `kprove ... --dry-run` parses and builds the mutation successfully with
exit 0
([dry-run log](/audit-output/evidence/stage6-vacuity-dry-run.log)). Then:

```text
timeout 600 kprove spec-vacuity.k \
  --definition audit-verification-haskell \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-loop-result
```

exits 1 with `WarnStuckClaimState`. Its reachable residual has `.K` and
`BoolV(false)` under the constraint `OPS #Equals .IntList`, exactly the unmet
result obligation expected—not a parser error, timeout, missing import, or
unreachable mutation. See
[proof log](/audit-output/evidence/stage6-vacuity-proof.log).

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly built K definition, for every finite `OPS:IntList`,
executing the exact regenerated `solution.mpy` module from its initial
configuration reaches `.K` with:

```text
<result> BoolV(belowZeroFrom(0, OPS)) </result>
```

and the two internal local cells reset. More generally, the loop claim proves
the same property from any mathematical starting balance `B`. The transparent
recursive equations establish the prefix-negative result for arbitrary list
lengths; this is not bounded unrolling or a finite-example theorem. The formal
domain therefore matches all finite Python `List[int]` values and does not
materially narrow the HumanEval contract.

### Trusted and informal boundaries

1. **K toolchain and logic.** K `v7.1.293`, its Haskell prover, circularity
   discipline, LLVM interpreter, parser, and standard Boolean/integer/K-sequence
   modules are trusted.
2. **Mathematical primitives.** `+Int`, `<Int`, Boolean values, and `#if` are
   trusted built-ins. K integers are unbounded, matching Python integers for
   the operations used here.
3. **Translator.** `/reference/py2mpy.py` is benchmark-trusted. Its actual
   output is nevertheless byte-reproduced and the claim AST is mechanically
   equal to it.
4. **Input encoding.** Finite Python integer lists are represented by finite
   `.IntList`/`cons` terms in the same order. This bridge is direct but not a
   separately proved serialization theorem.
5. **Generated language model.** The 22 local rules are trusted after the
   exhaustive static review above. There is no machine-checked universal
   refinement from this task-specific language to CPython. Eleven fresh
   generated-semantics executions and 20,618 Python differential cases provide
   finite supporting evidence only.
6. **Human-facing intent.** The induction argument relating
   `belowZeroFrom` to “some running prefix is negative” is ordinary
   mathematics reconstructed in this review; it is not replaced by the
   differential tests.

There are no opaque symbols, external result oracles, empirical axioms,
proof-local operational rewrites, or assumed task answers. Non-integer
elements, arbitrary iterables, alternate source modules/imports, annotation
introspection, exceptions, I/O, concurrency, and nested call frames are outside
the theorem. Those exclusions do not remove any behavior from the declared
`List[int] -> bool` source contract.

### Gate and decision summary

- Gate A, real-program soundness: PASS. Fresh `#Top`, exact program AST
  pinning, transparent result specification, body sensitivity, and a rejecting
  false-result mutation all hold.
- Gate B, intent adequacy: PASS. The theorem is universal over arbitrary finite
  integer lists and exactly captures strict negative prefixes.
- Gate C, trust/evidence auditability: PASS with a documented non-fatal
  generated-semantics limitation. All commands, inputs, scripts, and bounded
  logs exist; empirical results are not presented as universal proof.

The proof is legitimate. The over-broad-but-safe-on-this-program rules and lack
of a universal CPython-refinement theorem justify `CONCERNS` rather than
`PASS`; they do not make a false source-domain conclusion provable and
therefore do not justify `FAIL`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
