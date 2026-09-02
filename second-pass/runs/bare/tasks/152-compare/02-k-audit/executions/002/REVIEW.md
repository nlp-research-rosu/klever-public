# Independent adversarial review: 152-compare

The candidate contains a legitimate, non-vacuous partial-correctness proof for
the material HumanEval domain of finite, equal-length integer score lists. The
proof was rebuilt from source and pins the exact translated submitted program.
I assign `CONCERNS / LEGIT`, rather than `PASS`, because the formal claim has no
type/length precondition even though the generated semantics totalizes
out-of-range indexing and non-integer subtraction in ways that are not Python
behavior. The intended equal-length integer executions never reach those
totalizations. A second explicit limitation is the usual unbounded-resource
abstraction: the recursive Python implementation reaches CPython's recursion
limit on sufficiently long lists, while the K semantics has an unbounded call
continuation.

## 1. Input and provenance integrity

I first read `/audit-input.json`. It declares:

- problem `152-compare`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics; and
- the mounted paths under `container_paths`, rather than the host provenance
  strings elsewhere in the document.

The condition boundary is internally consistent:
`/reference/reference-semantics` does not exist. I did not search for or use a
hidden reference semantics.

The complete independent check is in
`/audit-output/evidence/stage1_integrity.py` and
`/audit-output/evidence/stage1_integrity.log` (exit 0). Its material results
were:

- `/audit-campaign-lock.json` is a real regular file, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its JSON object exactly equals the `audit_campaign` block.
- The task manifest matches the manifest view in `/audit-input.json` after
  accounting for the launcher-normalized `config` field. The recorded
  `/task.json` hash is exact.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace
  are present, readable, regular/non-symlinked artifacts as required for
  `legacy-selected-stage1`. Historical `runtime-metrics.json` is absent, which
  is allowed for this layout and was not reconstructed.
- Every launcher-recorded file digest checked by the script matches, including
  the run/task/result/invocation records, prompt, usage, output log, canonical,
  trusted prompt, and trusted translator. The evidence map in
  `generation-result.json` exactly equals the one in `invocation.json`, and
  every entry in that map has the recorded digest.
- The sole trace file has SHA-256
  `53a5e85b04041b060d09a8ee02e3abf01bedfdab14ee1f3e0539d8a17242e850`,
  exactly as recorded by the invocation. All 259 JSONL events parse. The trace
  contains 46 tool calls, their matching outputs, and no malformed event.
- The complete 696,449-byte `codex-output.log` was read as data (16,002 lines,
  no NUL bytes). The candidate's past `#Top` and final report were treated only
  as untrusted claims.
- Every entry under `/candidate`, `/generation-evidence`, and `/reference` was
  independently inventoried and hashed. No symlink or unsupported entry was
  found.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

The required proof artifacts `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` are present as ordinary files.
There is no provenance or mount breach, so an audit verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py:2` and `/reference/canonical.py:6`, the function
receives two equal-length arrays of match scores and guesses and must return an
array of the same length whose element at each position is the absolute
difference between score and guess. The examples require:

- `compare([1,2,3,4,5,1], [1,2,3,4,2,-2]) == [0,0,0,0,3,3]`;
- `compare([0,5,0,0,0,4], [4,1,1,0,0,-2]) == [4,4,1,0,0,6]`.

The prompt does not contain a Python type annotation or the word “integer.”
I interpret “scores,” the examples, and the available MPY value representation
as the ordinary HumanEval domain of finite integer lists. The lack of an
explicit type sentence is retained as an intent-bridge limitation in stage 7;
it is not silently used to claim support for floats or arbitrary Python
objects.

`/candidate/solution.py:1-7` is a recursive implementation. It stops on an
empty `game`, otherwise computes `game[0] - guess[0]`, negates a negative
difference, and prepends it to the recursive result on both tails. On
equal-length integer lists this is extensionally the canonical zip/list
comprehension.

### Trusted regeneration

From the clean scratch copy I ran:

```text
python3 /reference/py2mpy.py /tmp/audit-work/152-compare/solution.py \
  > /tmp/audit-work/152-compare/regenerated-solution.mpy
cmp /tmp/audit-work/152-compare/regenerated-solution.mpy /candidate/solution.mpy
sha256sum /tmp/audit-work/152-compare/regenerated-solution.mpy /candidate/solution.mpy
```

Exit status was 0. Both files have SHA-256
`8b1459d8f7e47fe17ad740613f5b14392282cdd23d81b304779d1994f6c83e5b`.
See `/audit-output/evidence/translator_regeneration.log`.

### Independent differential test

`/audit-output/evidence/differential_test.py` independently imports the trusted
canonical and scratch-copied submission. It covers both examples, empty input,
the negative/zero/positive branch boundaries, negative values, unbounded-size
integers, and deterministic generated equal-length inputs of lengths 0 through
900. Exact command:

```text
python3 /audit-output/evidence/differential_test.py
```

It exited 0 with 200 ordinary cases and zero value mismatches. The serialized
ordinary test-input digest is
`6b9e09d5e4511f822bc1ce48f307cb64ad84e0b468233cae90d7dc482cdc6682`.
The full input generator and results are in
`/audit-output/evidence/differential_test.log`.

The same run separately tested CPython's resource boundary. At list lengths
950, 975, 990, and 995 both implementations returned equal lists. At lengths
999, 1000, 1050, and 1100 the canonical returned but the recursive submission
raised `RecursionError`. This is not a wrong returned value, and the requested
theorem is partial correctness, but it is an explicit difference between real
CPython and the unbounded-stack generated semantics.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/152-compare`. I did not copy
or reuse any candidate-built definition/cache. The installed tools are
`/usr/bin/kompile`, `/usr/bin/krun`, and `/usr/bin/kprove`, all K v7.1.293
(`/audit-output/evidence/toolchain.log`).

### Generated semantics build and concrete execution

Fresh LLVM build:

```text
kompile semantic.k --backend llvm \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition reviewer-semantic-kompiled
```

It exited 0. See `/audit-output/evidence/kompile_semantic_llvm.log`.

`/audit-output/evidence/k_concrete_differential.py` then ran ten independent
`krun solution.mpy` commands against that definition. Cases include empty,
every sign branch boundary, negative inputs, both examples, a mixed list, and
40-digit integers. For every case it compared the K terminal `<k>` term with
the trusted canonical result and also compared the submitted Python result.
Command:

```text
python3 /audit-output/evidence/k_concrete_differential.py
```

It exited 0 with `case_count=10 mismatch_count=0`. Every exact `krun` command,
input term, exit status, result, and expected result is in
`/audit-output/evidence/k_concrete_differential.log`.

### Proof build and positive target

Fresh Haskell proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

Exit status was 0
(`/audit-output/evidence/kompile_verification_haskell.log`).

`spec.k` contains exactly one positive target claim. I ran:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed exactly `#Top`; see
`/audit-output/evidence/kprove_spec.log`. Thus clean dynamic reconstruction
passes.

## 4. Adequacy and real-program pinning

### Plain-language claim

The claim at `/candidate/spec.k:6-7` has no `requires` clause. Its formal
precondition is therefore:

- the `<k>` cell begins with
  `execute(solutionProgram, VList(GS), VList(US)) ~> REST`;
- `GS` and `US` are arbitrary values-list terms; and
- `REST` is an arbitrary K continuation.

Its postcondition says execution replaces that call with exactly
`VList(expected(GS,US))` and preserves `REST`. The result is not free, omitted,
or guarded by a one-way implication.

A satisfying state is `GS = VNil`, `US = VNil`, `REST = .K`; both Python
implementations and K return the empty list. A nonempty satisfying intended
state is `GS = VCons(VInt(0),VNil)`,
`US = VCons(VInt(1),VNil)`, `REST = .K`; `expected` is `[1]`, and all three
executions returned `[1]` (concrete differential case 1).

### Exact program term

`solutionProgram` at `/candidate/verification.k:8-28` expands to a literal
constructor tree. `/audit-output/evidence/check_program_pinning.sh` extracts
that right-hand side and compares it mechanically with the trusted-regenerated
`solution.mpy`, removing only K's explicit `.Exprs`/`.Stmts` spellings of empty
constructor lists and whitespace. The normalized terms have the same SHA-256
`81da63e859bdb746509b1a65d0b63850d28a773bc8aad7fae26b7382ba844c95`;
the comparison exited 0
(`/audit-output/evidence/program_term_pinning.log`).

The entry rule does not bypass that body. It binds `game` and `guess`, executes
the body's actual `If`, `Assign`, second `If`, and `Return`, and recursive calls
reuse the same `Pgm` body. There is no helper/loop claim substituting a
different algorithm.

As a body-sensitivity check, I changed the actual executed program term's
negative branch from
`difference = -difference` to `difference = difference`. The exact mutation is
preserved in `/audit-output/evidence/verification-body-mutation.k`. Its Haskell
definition built successfully (exit 0), but the unchanged target proof exited
1 with `WarnStuckClaimState`; the residual requires a negative difference to
equal its negation. See `body_mutation_build.log` and
`body_mutation_kprove.log`. This is strong evidence that claim closure depends
on the material submitted statement.

There is no automatic source-to-`solutionProgram` generator in the candidate.
For this immutable submission, trusted translation plus the mechanical exact
comparison pins it; the duplication is only a future-maintenance observation.

## 5. Rule-by-rule static soundness review

The full numbered sources and declaration/rule index are preserved in
`/audit-output/evidence/static_inventory.log`. It counts 54 semantic rules,
four verification equations, one claim, and zero local priority,
`simplification`, or `owise` attributes.

### Exhaustive local syntax and symbol inventory

`MPY-SYNTAX` declares every following production:

- `Pgm`: `Module(Stmts)`;
- `Stmts`: juxtaposed statement list;
- `Stmt`: `FuncDef`, `Return`, `Assign`, `If`;
- `Params` and comma-separated `Strings`;
- `Expr`: `Name`, `Int`, `ListExpr`, `BinOp`, `UnaryOp`, `Compare`,
  `Subscript`, `Call`;
- comma-separated `Exprs` and `CmpOps`;
- `CmpOp`;
- `Index`: the `Expr` injection and `Slice`;
- `Bound`: the `Expr` injection and `NoBound`.

`SEMANTIC` declares:

- value constructors `VInt`, `VBool`, `VList`, `VNil`, `VCons`;
- environments `EmptyEnv`, `Bind`;
- outcomes `Ongoing`, `Returned`;
- all 20 control items: `execute`, `invokeK`, `execK`, `evalK`,
  `evalExprsK`, `makeReturned`, `extractReturned`, `assignK`, `ifK`,
  `continueK`, `listHeadK`, `listTailK`, `binLeftK`, `binRightK`,
  `unaryK`, `compareLeftK`, `compareRightK`, `subscriptK`, `callArgK`,
  and `callInvokeK`;
- functions `lookupEnv`, `lookupAt`, `indexValue`, `headValue`,
  `dropValues`, `concatValues`, `tailValues`, `isEmptyValues`, and
  `valueAsInt`.

The declarations marked `[total]` are `headValue`, `tailValues`,
`isEmptyValues`, and `valueAsInt`. The other semantic functions are partial
and have rules for the well-formed uses reached by the submitted program.

`VERIFICATION` adds exactly two functions, both `[function,total]`:
`solutionProgram` and `expected`. There are no locally declared opaque
symbols, `functional` attributes, priority rules, or simplification rules.

Every constructor in `solution.mpy` is covered: module/function/parameters and
statement lists; return, assignment and conditional control; names and integer
literals; empty/singleton lists; subtraction and list concatenation; unary
negation; empty-list equality and integer less-than; index zero; slice
`[1:]`; and the recursive two-argument call.

### All 54 semantic rules

The rules at `/candidate/semantic.k:85-179` were assessed individually:

1. `execute` enters `invokeK`.
2. `invokeK` matches the exact single `compare(game,guess)` binding, creates a
   fresh local environment, preserves the exact body as `Pgm`, and arranges
   return extraction.
3. Empty statements produce `Ongoing`.
4. `Return` evaluates its expression and ignores following statements.
5. `Assign(Name(...))` evaluates before binding.
6. `If` evaluates its guard before choosing a branch.
7. `makeReturned` wraps a value.
8. `extractReturned` extracts it.
9. `assignK` shadows the environment and continues.
10. The true `ifK` rule runs `THEN`.
11. The disjoint false `ifK` rule runs `ELSE`.
12. `Ongoing` resumes the following statements.
13. `Returned` propagates past `continueK`.
14. Name evaluation performs environment lookup.
15. Integer literals produce `VInt`.
16. List expressions enter element evaluation.
17. Empty expression lists produce `VList(VNil)`.
18. Nonempty expression lists evaluate the head first.
19. The list continuation then evaluates the tail.
20. `listTailK` reconstructs the list in source order.
21. Binary expressions evaluate the left operand first.
22. The binary continuation evaluates the right operand second.
23. `-` subtracts right from left.
24. `+` concatenates left and right lists.
25. Unary expressions evaluate their operand.
26. Unary `-` performs integer negation.
27. Comparisons evaluate the left side first.
28. Their continuation evaluates the right side second.
29. The used `game == []` case tests whether the evaluated left list is empty.
30. Integer `<` compares left against right in the correct orientation.
31. Subscripts evaluate their base first.
32. The continuation applies the index.
33. Nonnegative integer indices call `lookupAt`.
34. The used nonnegative `[N:]` slice calls `dropValues`.
35. The exact recursive `compare` call evaluates `game` first.
36. It then evaluates `guess`.
37. It invokes the same program body with those values.
38. Environment lookup returns the first matching binding.
39. A guarded nonmatching binding recurses; its guard is disjoint from rule 38.
40. `isEmptyValues(VNil)` is true.
41. `isEmptyValues(VCons(...))` is false.
42. `headValue(VNil)` is totalized to `VInt(0)`.
43. A nonempty head returns its value.
44. `tailValues(VNil)` is totalized to `VNil`.
45. A nonempty tail returns the remainder.
46. `valueAsInt(VInt(I))` returns `I`.
47. `valueAsInt(VBool(...))` is totalized to 0.
48. `valueAsInt(VList(...))` is totalized to 0.
49. Index zero uses `headValue`.
50. A positive index recurses with a strictly smaller integer.
51. Dropping zero elements is identity.
52. A positive drop recurses with a strictly smaller integer.
53. Concatenating an empty left list returns the right list.
54. Concatenating a cons recursively preserves the left spine.

Rules 1-41, 43, 45-46, 49-54 follow the submitted program's behavior on
finite equal-length `VInt` lists. They implement left-to-right evaluation,
sequential control, environment shadowing, recursive call/return, immutable
lists, and mathematical unbounded integers. No heap or allocation cell is
needed because the program performs no mutation, identity comparison, I/O, or
observable allocation.

The true/false guards, environment guards, zero/positive recursion guards, and
`expected` sign guards are disjoint. `lookupAt` and `dropValues` descend for
positive indices. All `[total]` functions cover every constructor of their
argument sort.

Rules 42, 44, 47, and 48 are explicit totalizations, not faithful general
Python operations. Rule 44 is consistent with empty-list slicing, but rule 42
fabricates 0 for an out-of-range index, rule 47 maps both booleans to 0 even
though Python booleans participate as 0/1 integers, and rule 48 replaces a
Python type error with 0. These conventions are unreachable when both inputs
are equal-length lists of ordinary integer scores: the program indexes only
after proving `game` nonempty, equal length makes `guess` nonempty, and both
heads are integers.

The conventions do affect the claim's broader formal domain because the claim
forgot a `validPair`-style precondition. Concrete witnesses are in
`/audit-output/evidence/semantic_boundary_diagnostics.log`:

- with `game=[7]`, `guess=[]`, the submitted Python raises `IndexError`, while
  K returns `[7]` through `headValue(VNil) => VInt(0)`;
- with K boolean scores corresponding to Python `[True]` and `[False]`, both
  Python implementations return `[1]`, while K returns `[0]` through the
  boolean totalization.

The first witness violates the source's equal-length condition. The second
lies outside the ordinary-integer-score interpretation but exposes why the
unqualified formal claim must not be advertised as a theorem for arbitrary
Python values. Because no false returned result was found for an equal-length
ordinary integer input, I classify this as a non-fatal bridge/scope concern,
not a materially unsound rule on the intended domain.

### Four verification equations and the claim

1. `solutionProgram` is a definitional summary of the exact constructor tree.
   It does not replace a program operation; mechanical identity and the body
   mutation validate it.
2. The empty `expected` equation returns `VNil`.
3. The negative-difference equation prepends the negated difference.
4. The complementary nonnegative equation prepends the difference.

The three `expected` guards are exhaustive and disjoint over `Values`. The
recursive cases descend on `GS`. On equal-length integer lists the equations
are exactly pairwise absolute difference. `expected` appears only in the
postcondition and never rewrites execution, so it is not a circular
result-bearing oracle or operational bridge.

The sole reachability claim uses the real execution rules and its own
structurally recurring recursive-call configuration as a circularity. It
frames the arbitrary continuation `REST` consistently. There are no auxiliary
claims, operational bridges, priority preemption, proof-local semantic
rewrites, or unconstrained values that can determine the result.

## 6. Fresh non-vacuity test

The final reviewer-authored mutation is
`/audit-output/evidence/spec-vacuity.k`. It uses the satisfying ground input
`game=[]`, `guess=[]` but demands the deliberately false result `[1]`.

First I checked that it parses/builds against the fresh definition:

```text
kprove spec-vacuity.k --definition reviewer-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit status was 0; see `vacuity_dry_run.log`.

Then I ran the actual proof:

```text
kprove spec-vacuity.k --definition reviewer-verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`. The residual is the actual terminal
configuration `<k> VList(VNil) ~> .K </k>`, which does not unify with the false
destination. See `vacuity_kprove.log`. This is the expected unmet
result-constraining obligation, so the positive proof is non-vacuous.

For completeness, an initial symbolic “add 1 for every input” mutation reached
a backend `DecidePredicateUnknown` error. I did not count that unrelated
failure as non-vacuity evidence; its source and logs are preserved as
`spec-vacuity-attempt1.k`, `vacuity_dry_run_attempt1.log`, and
`vacuity_kprove_attempt1.log`.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly compiled `semantic.k` and `verification.k`, the successful
claim establishes:

> For arbitrary K `Values` spines `GS` and `US` and arbitrary continuation
> `REST`, executing the exact constructor term regenerated from the submitted
> `solution.py` rewrites to `VList(expected(GS,US))` followed by the same
> `REST`.

On finite equal-length lists containing only `VInt`, the audited equations make
`expected` exactly the list of pairwise absolute integer differences. The
program body, both conditional branches, recursive call, and list construction
are executed by operational rules; this fact is not assumed from
`PROOF.md`, a prior trace, or testing.

### Trusted and informal boundaries

- **K toolchain and logic:** K v7.1.293, the Haskell prover, reachability
  circularity soundness, and compilation are trusted. Every target and
  mutation command is independently reproducible in the evidence logs.
- **Built-in primitives:** `INT`, `BOOL`, and `STRING` arithmetic, comparison,
  Boolean connectives, and string equality from `domains.md` are trusted
  primitives. They affect values/guards but do not encode this task's answer.
- **Translator:** `/reference/py2mpy.py` is launcher-trusted. Byte-identical
  regeneration establishes the source-to-MPY artifact link.
- **MPY-to-Python bridge:** The generated semantics is candidate-authored.
  Its alignment with normal Python execution on equal-length integer lists is
  supported by exhaustive static rule review, ten concrete K/Python
  comparisons, and 200 canonical/submission differential cases. These finite
  tests support, but do not replace, the operational proof.
- **Input intent:** The proof-to-source-contract bridge assumes the material
  score domain is ordinary integers. The prompt gives integer examples and
  score terminology but no explicit type annotation; floats and arbitrary
  Python objects are not represented.
- **Exceptions and resources:** The theorem is partial correctness in an
  unbounded-resource abstract machine. It does not prove CPython termination,
  absence of `RecursionError`, or behavior for type/index exceptions. The
  observed recursion boundary and off-domain totalization witnesses remain
  explicit exclusions.
- **Canonical oracle:** `/reference/canonical.py` is trusted only as the
  independent executable oracle requested by the audit. Differential evidence
  is finite and is not treated as the K proof.

### Gate and decision summary

- Gate A (real-program soundness): passes for the material equal-length `VInt`
  domain. There is no operational shortcut, oracle, or false-postcondition
  closure; body and result sensitivity both succeed.
- Gate B (intent adequacy): covers unrestricted finite list lengths
  symbolically under partial-correctness/unbounded-resource semantics. The
  integer-score interpretation and omission of CPython resource exceptions are
  explicit boundaries, not fixed-size proof bounds.
- Gate C (auditability): commands, exits, positive `#Top`, concrete tests,
  body mutation, and fresh non-vacuity failure are preserved. The theorem's
  unguarded off-domain K behavior is not conflated with Python behavior.

The proof is therefore legitimate for the material source-contract domain, but
the missing formal `validPair` precondition and the generated semantics'
off-domain totalizations are enough to withhold an unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
