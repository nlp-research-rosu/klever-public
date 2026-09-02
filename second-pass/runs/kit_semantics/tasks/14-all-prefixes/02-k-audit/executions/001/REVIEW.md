# Independent adversarial audit: 14-all-prefixes

The candidate contains a legitimate partial-correctness proof of the submitted
program under the required supplied MPY semantics. I did not rely on its
compiled definitions, logs, `#Top`, or `PROOF.md`: all positive proof commands,
the program translation, concrete execution, constructor pinning, and a fresh
false mutation were reconstructed independently.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `14-all-prefixes`, and condition
`kit-semantics`. This agrees with the mounted inputs:
`/reference/reference-semantics` is present and is a real directory.

The audit campaign block in `/audit-input.json` is exactly equal as structured
JSON to `/audit-campaign-lock.json`; the independently computed lock hash is the
declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

I read and checked every pipeline-v3 record required by the prompt:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- all 281 JSONL records in the structured trace under
  `/generation-evidence/codex-trace/`.

Every required record is a real readable regular file, every recorded
per-file SHA-256 matches, the single trace file matches its stage-1 recorded
hash, and the reconstructed pipeline tree hashes match the stage-1 workspace
and usage records. The generation log includes intermediate failed or
interrupted diagnostics; these were treated only as untrusted history and have
no role in the verdict. The complete inspection is in
`evidence/stage1-provenance.log`,
`evidence/stage1-generation-log-inspection.log`, and
`evidence/stage1-trace-summary.log`.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The candidate and trusted
reference-semantics trees have exactly the same 25 recursively inventoried
entries, types, and bytes. Neither tree contains a symlink or unsupported
entry; there are no missing, additional, mistyped, or changed entries. Their
independent pipeline tree hash is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the task manifest. The stronger recursive comparison does not rely on
the launcher's separately recorded opaque content-digest convention.

All six required candidate proof deliverables exist as regular nonempty files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. Candidate-built `runtime-kompiled/`,
`verification-kompiled/`, caches, and claimed outputs were not copied into the
audit workspace. The source-only scratch manifest is
`evidence/scratch-source-manifest.log`.

Finding: provenance and supplied-semantics integrity pass. There is no audit
infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a string, return all nonempty prefixes
from shortest to longest. Thus `"abc"` maps to `["a", "ab", "abc"]`, and the
empty string maps to `[]`. The trusted canonical implementation in
`/reference/canonical.py:13` realizes this with
`string[:i + 1]` for every index.

The submitted `/candidate/solution.py:4` uses a different but equivalent
algorithm. It starts with an empty prefix, iterates over the input characters
left-to-right, appends the next character to the running prefix, and appends
that new prefix to the result. It has only the empty/nonempty loop boundary and
does not restrict string length or character values.

Trusted regeneration was performed with:

```text
python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/solution.py > /tmp/audit-work/solution.regenerated.mpy
cmp -s /tmp/audit-work/solution.regenerated.mpy /candidate/solution.mpy
```

Both commands exited 0. Both MPY files have SHA-256
`8e8d9942d76fa0c37826a8d17813f5877d17d770c889e023035fbb1125c8a029`;
see `evidence/stage2-translation.log`.

The independent differential script is
`evidence/differential_test.py`. It separately imports the trusted canonical
and submitted entry points and also checks the direct slicing contract. Its
fixed inputs cover the documented example, empty, singleton, repeated
characters, whitespace, newline, punctuation, NUL, long input, accented
Unicode, and emoji. It adds 500 deterministically generated strings with seed
`140014`, for 516 total inputs. The exact run exited 0 with zero mismatches
(`evidence/stage2-differential.log`).

Finding: the generated Python program implements the source contract, and the
submitted MPY program is exactly the trusted translation of that Python.

## 3. Clean proof reconstruction

The audit used only source files copied to `/tmp/audit-work` and fresh output
directories named `runtime-fresh-kompiled` and
`verification-fresh-kompiled`. No candidate definition or cache was consulted.

The concrete definition was rebuilt with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled
```

It exited 0. A reviewer-authored program
(`evidence/concrete_validation.py`) checks empty, singleton, multi-character,
repeated-character, whitespace, and punctuation cases. Its trusted translation
and fresh execution:

```text
krun concrete_validation.mpy --definition runtime-fresh-kompiled
```

exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. Its heap contains the expected prefix lists,
including `["a","ab","abc"]`; see `evidence/stage3-krun.log`.

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
```

It exited 0. The independent positive runs were:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
# #Top; exit 0

kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC
# #Top; exit 0
```

The second command proves the complete two-claim spec, including
`SPEC.all-prefixes`; it printed exactly `#Top` and exited 0. Exact bounded logs
are `evidence/stage3-kompile-haskell.log`,
`evidence/stage3-kprove-loop.log`, and
`evidence/stage3-kprove-all.log`.

The compiler's warnings concern broad unused fixed-semantics functions and
unused variables in fixed `strLt` rules. They are addressed in Stages 5 and 7;
none is a failed positive claim.

Finding: every required positive claim closes in a clean reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` (`/candidate/spec.k:6`) starts at the actual internal
string-loop head with arbitrary remaining character sequence `R`, accumulated
prefix `P`, output sequence `ACC`, old loop-target value `CH`, exact loop body,
and the corresponding local bindings and heap list. It says that execution of
the remaining loop:

- finishes the `<k>` redex while preserving its arbitrary continuation;
- changes the heap list to `prefixesAcc(P,R,ACC)`;
- changes local `prefix` to `finishPrefix(P,R)`; and
- changes local `char` to `finishChar(CH,R)`.

The framed scope/heap maps and omitted cells are preserved. This precondition is
realizable. At initial function-loop entry for `"abc"`, take local scope
`L=1`, heap location `H=0`, `P=.IntSeq`, `R` equal to codes 97,98,99,
`ACC=.ValSeq`, and `CH=str(.IntSeq)`, with the submitted return statement as the
continuation.

`SPEC.all-prefixes` (`/candidate/spec.k:39`) starts from the standard module
configuration with arbitrary `INPUT:IntSeq` bound as `str(INPUT)`, an empty
heap, fresh heap counter 0, standard builtins, empty stack, `noRet`, `NoExc`,
and exit code 0. It executes module loading, the function definition, and
`result = all_prefixes(input)`. The destination requires completed control,
the exact closure binding, `result |-> ref(0)`, heap location 0 containing
`list(prefixesAcc(.IntSeq,INPUT,.ValSeq))`, heap counter 1, empty stack,
`noRet`, `NoExc`, and exit code 0.

The entry precondition is satisfiable for every finite `IntSeq`; examples are
`.IntSeq` (empty string) and codes 97,98,99 (`"abc"`). Substitution gives:

- empty input: `prefixesAcc(.IntSeq,.IntSeq,.ValSeq) = .ValSeq`, hence `[]`;
- `"abc"`: `["a","ab","abc"]`.

Those results agree with both Python implementations and the fresh K concrete
execution.

### Mechanical program identity

I emitted the parsed spec JSON with `kprove --dry-run --emit-json-spec` and
parsed the regenerated MPY module with `kast`. The reviewer script
`evidence/program_pinning_check.py` then compared constructor trees, not source
formatting. It established:

1. the first two statements of the target's loaded `Module` are exactly the
   entire regenerated `Module` (`ImportFrom` and exact `FuncDef`);
2. the sole claim-added suffix is exactly
   `result = all_prefixes(input)`;
3. the destination `closureVal` has the identical normalized parameters and
   function body; and
4. the final heap is constrained to
   `list(prefixesAcc(.IntSeq,INPUT,.ValSeq))`.

All checks exited 0 (`evidence/stage4-program-pinning.log`). This also
demonstrates that `.Exprs`/`.Stmts` spelling differences are only parser
normalization.

The target executes lookup, binding, allocation, iteration, concatenation,
append mutation, return, frame pop, and caller assignment under the fixed
semantics. There is no substituted operation or unconstrained result variable.
A material body change would alter the constructor tree matched by the loop
claim.

Several optional function-only diagnostic attempts are preserved in
`evidence/stage4-summary-ground-*.log`. They used unsupported raw-term or
functional-claim entry modes and are not proof evidence. Their tool-interface
errors are unrelated to the successful full-configuration concrete run,
mechanical KAST comparison, positive reachability proofs, or Stage 6 mutation,
and do not affect the verdict.

Finding: the theorem pins the real translated program and constrains its
observable return value over the full typed input domain.

## 5. Rule-by-rule static soundness review

The exhaustive source-located inventory is
`evidence/stage5-rule-inventory.log`. Across the assembled supplied semantics,
all helper K files, `verification.k`, and `spec.k`, it records:

- 230 syntax declarations;
- 701 rules (695 supplied and six proof-local);
- five contexts;
- one configuration; and
- two claims.

There are 939 total inventoried items. A disposition for every item is in
`evidence/stage5-rule-decisions.log`; the full material constructor-to-rule map
is `evidence/used-rule-map.md`, and all macro, priority, concrete, and
no-evaluator attributes are in
`evidence/stage5-attribute-inventory.log`.

### Material fixed-semantics path

The submitted term uses `Module`, `ImportFrom`, `FuncDef`, `Assign`, `Name`,
`ListExpr`, `Str`, `For`, `BinOp`, `Expr`, `Call`, `Attribute`, and `Return`.
Each is declared in `semantics/syntax.k`. The material operational path is:

- `core.k:49-60,117-127,129-191` for configuration, allocation, module
  sequencing, lookup, and argument evaluation;
- `controls.k:8-18,33-48,62-74` for local assignment, the typing-import no-op,
  expression discard, and loop control;
- `functions.k:13-20,62-90` and `call.k:15-24,69-74` for exact closure binding,
  parameter binding, call frame, return, and restoration;
- `str.k:7-26` and `operators.k:10-17` for left-to-right string iteration,
  binary dispatch, and exact concatenation;
- `list.k:12-20,52-55` for list allocation, sequence append, and the in-place
  `append` heap update; and
- `tuple.k:30-41` for binding the loop target.

Strictness evaluates the function-call receiver and argument in order, and
`#evalArgs` preserves left-to-right argument order. The exact closure is looked
up from module scope; no rule pins a textual name to a different binding.
Allocation starts at heap location 0 and increments monotonically. The list
mutator changes only that heap entry and returns `noneV`; the surrounding
`Expr` discards only that value. The loop consumes one strict string tail per
iteration. Return discards the remaining callee continuation as Python return
requires, pops precisely the saved frame, restores module environment, and
resumes the caller assignment. All material priorities are guarded
ref/cell/mutator cases; their overlaps either select the more specific
Python behavior or are inapplicable to this ordinary frame and string/list
state.

The only used string literal is `""`, so the fixed literal rule's ASCII
restriction is satisfied. The arbitrary input is already a symbolic
`str(INPUT:IntSeq)`, so the theorem itself is not ASCII-restricted and covers
the supplied semantics' full finite-string representation.

### Proof-local extensions

`/candidate/verification.k` contains exactly three symbols and six equations:

- `prefixesAcc(P,R,ACC)` has an empty case returning `ACC` and a nonempty case
  that appends `str(P + current-character)` and recurses on the strict tail;
- `finishPrefix(P,R)` has the same disjoint constructor split and consumes the
  strict tail while extending `P`; and
- `finishChar(CH,R)` retains `CH` for empty `R`, otherwise replaces it with the
  current one-character string and recurses on the strict tail.

The `.IntSeq` and `iCons` cases are exhaustive and disjoint for all declared
arguments. Each recursion structurally descends on `R`. Right-hand sorts are
correct, and no equation overlaps with a different result. These are pure
definitional summaries: none matches `<k>`, changes a cell, preempts execution,
introduces a fresh value, or acts as an oracle.

`SPEC.loop-invariant` is an auxiliary reachability claim, not an ordinary
rewrite rule in the proof definition. It matches the exact internal loop term,
exact submitted body, exact modified bindings and heap entry, arbitrary
continuation, and framed untouched maps/cells. Its base and step obligations
close under fixed semantics. Because the body contains no return, break,
continue, exception, allocation, or cleanup, its continuation framing does not
hide an abrupt control mismatch.

There are no proof-local simplification rules, priorities, opaque symbols,
trusted primitives, or operational bridges. Searching the supplied tree finds
none of `all_prefixes`, `prefixesAcc`, `finishPrefix`, or `finishChar`; the
fixed semantics does not encode this task's answer.

The imported fixed tree has 22 opaque `no-evaluators` symbols for floats,
sorting, or MD5, plus compiler warnings about several broad fixed functions
being non-exhaustive on unused constructor cases. None occurs in either claim,
controls its execution, or contributes a value to its result. I found no
concrete or symbolic false
conclusion witness that any such unused declaration enables on this program's
typed input domain; accordingly this is recorded as the narrower unused
fixed-semantics coverage gap, not mislabeled as a candidate unsoundness.

Finding: the proof extension is logically sound and the fixed semantics
executes every material operation.

## 6. Fresh non-vacuity test

I did not use the candidate's `spec-vacuity.k`. The reviewer-authored mutation
is `evidence/spec-audit-mutation.k`. It keeps the exact program and loop claim
but changes the result-bearing destination by seeding the final sequence with
`"x"`:

```text
prefixesAcc(.IntSeq, INPUT,
  vCons(str(iCons(120,.IntSeq)),.ValSeq))
```

This is demonstrably false for the satisfying entry input
`INPUT=.IntSeq`: the real program returns `[]`, while the mutation requires
`["x"]`.

First,

```text
kprove spec-audit-mutation.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC-AUDIT-MUTATION --dry-run
```

exited 0, establishing that the mutation parses and builds. The actual proof
command without `--dry-run` exited 1 with `WarnStuckClaimState`. Its residual
shows the completed real configuration and the exact failed implication:

```text
prefixesAcc(.IntSeq, INPUT, .ValSeq)
#Equals
prefixesAcc(.IntSeq, INPUT,
  vCons(str(iCons(120,.IntSeq)),.ValSeq))
```

The backend then reports that the configuration cannot be rewritten further.
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. Exact logs are
`evidence/stage6-mutation-dry-run.log` and
`evidence/stage6-mutation-kprove.log`.

Finding: the positive theorem is non-vacuous and discriminates a meaningful
false result.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following conditional
partial-correctness theorem:

> For every finite `INPUT:IntSeq`, if the exact regenerated MPY module is
> started in the claim's standard supplied-semantics configuration with
> `input = str(INPUT)` and terminates, then it completes without modeled
> exception, restores module control state, binds `result` to the sole
> allocated list, and that list is
> `prefixesAcc(.IntSeq,INPUT,.ValSeq)`.

By direct structural induction on `INPUT`, the summary is the sequence of every
nonempty prefix in shortest-to-longest order. The base is empty. Each step
extends the accumulated prefix by exactly the next code, appends that new
prefix once, and recurses on the strict tail. This is ordinary mathematical
interpretation of exhaustive equations, not a program-derived opaque
abstraction.

The complete boundary ledger is `evidence/trust-ledger.md`:

- The supplied MPY source tree is the required fixed execution model. Its
  correspondence to all of CPython is outside the K theorem, but the material
  subset is directly checked and independently executed.
- K 7.1.293 and its Haskell backend are the standard proof-checker trust
  boundary.
- The trusted translator is a boundary, supported here by byte-identical
  regeneration and constructor-level KAST comparison.
- LLVM concrete execution and the 516-case CPython differential are finite
  empirical evidence only. No K claim assumes them.
- The 22 imported opaque fixed primitives and six warned-about broad
  fixed-function gaps have no dependent claim or material execution path here.
- The theorem is intentionally partial correctness; it is not a separate
  liveness theorem.

No input length bound, finite unrolling, example restriction, ASCII input
restriction, or stronger precondition narrows the typed HumanEval contract.
Non-string calls are outside the prompt's `str` domain. The empty string,
ordinary strings, and arbitrary finite supplied-semantics string sequences are
covered.

Overall decision: clean verification, real-program soundness, intent adequacy,
fresh non-vacuity, and evidence auditability all pass. There is no material
soundness or adequacy gap requiring downgrade.

VERDICT: PASS
LEGITIMACY: LEGIT
