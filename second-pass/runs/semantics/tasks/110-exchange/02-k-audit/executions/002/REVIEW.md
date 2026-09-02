# Independent adversarial review: HumanEval 110-exchange

## Audit outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program for the source contract's non-empty integer-list domain.
I rebuilt every definition from source, reproduced `#Top`, mechanically pinned
the claim body to the regenerated program, audited all proof-local rules, proved
the custom list-representation connection from the supplied list semantics, and
made both a body mutation and a false-result mutation fail for the expected
reason.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `110-exchange`;
- condition `semantics`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- `record_layout: legacy-selected-stage1`; and
- complete input provenance.

The required trusted semantics mount `/reference/reference-semantics` is
present, so the trusted mounts do not contradict the rendered semantics mode.
The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

I read and validated `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. All 612 JSONL trace
records parse. The legacy-selected layout does not require historical
`runtime-metrics.json`; its absence is not a breach. The generation prose,
logs, and trace were treated only as untrusted claims.

Every launcher-recorded regular-file hash checked by
`evidence/stage1_integrity.py` matches. In particular:

- trusted canonical:
  `4d0bd867017d71a10bfa51e6920bb47dacae89f4413c59319336ce49a390cb58`;
- trusted/candidate prompt:
  `3ae7e8bd32a483624eaf7543bf375fec87e33e448f4c417e879a21a04dd0dba6`;
- trusted/candidate translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- run, task, stage result, invocation, metrics, usage, prompt, last-message,
  and output-log hashes all match their launcher declarations.

The candidate and trusted supplied-semantics trees each have the same 26
entries. The relative paths, file/directory types, modes, and file bytes match
recursively. Neither tree contains a symlink; there are no missing, additional,
mistyped, or changed entries. Candidate `prompt.py` and `py2mpy.py` are also
byte-identical to their trusted mounts. All five required candidate proof
artifacts are ordinary readable files.

Evidence: `evidence/stage1-integrity.log` (exit 0).

**Stage 1 result: PASS.**

## 2. Program fidelity and canonical comparison

### Contract

The trusted prompt says that both input lists are non-empty. Elements are
numbers on which odd/even parity is meaningful, i.e. the intended HumanEval
domain is integer lists. Arbitrarily many swaps may be made. Therefore making
the first list all-even is possible exactly when:

`number of odd elements in lst1 <= number of even elements in lst2`.

The trusted canonical implementation counts `i % 2 == 1` in `lst1`, counts
`i % 2 == 0` in `lst2`, and returns `"YES"` exactly under that inequality.
Candidate `solution.py` counts `number % 2 != 0` instead. For every Python
integer, including negative integers, modulo 2 is either 0 or 1, so these tests
are equivalent. The reversed spelling `odd <= even` versus `even >= odd` is
also equivalent.

### Trusted regeneration

From the scratch copy I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated `solution.mpy` have the same
SHA-256,
`0a7ce271d769befb3c9f4c307998e9d32975d9d190b9f537e254a0c5f711c6eb`.
Evidence: `evidence/stage2-fidelity.log`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical and generated
solution as separate modules and compares both with an independently written
count oracle. It covers:

- both documented examples;
- empty-list cases as excluded boundary robustness checks;
- equality, less-than, and greater-than count boundaries;
- zero, negative, and very large integers;
- every pair among 156 small lists of length 0 through 3 over
  `{-2,-1,0,1,2}`; and
- 5,000 deterministic generated list pairs of length 0 through 20.

The run covered 29,348 input pairs, observed both `"YES"` and `"NO"`, and found
zero candidate/canonical/oracle mismatches. Evidence:
`evidence/stage2-differential.log` (exit 0). This is finite bridge evidence, not
a substitute for the K proof.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

I copied only source artifacts and the trusted semantics into
`/tmp/audit-work/review`. Candidate caches, compiled definitions, the
candidate-provided archive, and prior traces were not used. The live toolchain
is K v7.1.293 (`evidence/stage3-toolchain.log`).

Fresh commands and outcomes:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
# exit 0

krun concrete-tests.mpy --definition audit-runtime-kompiled --output pretty
# exit 0; .K, NoExc, exit-code 0

kompile verification.k --backend haskell \
  --main-module EXCHANGE-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
# exit 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module EXCHANGE-SPEC --output pretty
# #Top; exit 0
```

Evidence is in `evidence/stage3-kompile-runtime.log`,
`stage3-krun-concrete.log`, `stage3-kompile-proof.log`, and
`stage3-kprove-all.log`.

I also ran the two reusable circularities independently using their correct
module-qualified labels:

```text
--claims EXCHANGE-SPEC.odd-loop
# #Top; exit 0

--claims EXCHANGE-SPEC.even-loop
# #Top; exit 0
```

The corresponding logs are
`evidence/stage3-kprove-odd-loop-qualified.log` and
`stage3-kprove-even-loop-qualified.log`. Initial short-label attempts failed at
the CLI filter with “Unused filtering labels”; this was a reviewer invocation
diagnostic, not proof execution.

An entry-only filter is not dependency closed because `--claims
EXCHANGE-SPEC.exchange-correct` removes both loop circularities. I interrupted
that non-representative unrolling diagnostic with SIGINT (status 130). The
aggregate command above is the positive target proof and closes all three
claims. This is documented in `evidence/stage3-filter-diagnostic.md`.

Compiler warnings concern unused variables and non-exhaustive helper functions
outside this program path. The fresh candidate functions themselves compile
without a totality/overlap warning.

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Claims in plain language

`odd-loop` (`/candidate/spec.k:7`) says: from a non-empty remaining first-list
iteration, with integer `odd`, `even`, and `number` locals, execute the real odd
loop body and arbitrary continuation. The continuation is reached with `odd`
increased by exactly the number of odd integers in the entire remaining
sequence. `lst1`, `lst2`, `even`, the parent, and framed cells are preserved.
The final loop-target value is existential because it does not affect the
result.

`even-loop` (`/candidate/spec.k:37`) is the analogous statement for the second
list and the count of even integers.

`exchange-correct` (`/candidate/spec.k:68`) starts from the standard empty
module configuration, loads `Module(exchangeDef)`, looks up and calls
`exchange` on two arbitrary non-empty finite integer sequences, and reaches
exactly `exchangeResult` for those sequences. The result function reduces to
the precise code sequence for `"YES"` iff odd-count is at most even-count, and
to `"NO"` otherwise. It is not a free variable, tautology, or one-way
postcondition.

The unrestricted final scopes map is harmless: the observable return value is
fully constrained, while heap, heap location, scope location, stack, return
state, exception, and exit code are required to return to their initial values.

### Mechanical program identity

Using the fresh proof definition, I parsed:

- submitted `solution.mpy`; and
- the claim term `Module(exchangeDef)`;

with `kast --expand-macros --sort Module --output json`. The resulting JSON
ASTs are byte-identical and share SHA-256
`6d1ce3c40bab274b8c2f3854f278a1f8e2f20f22db3a844cde74851640af0514`.
Thus the three macros at `/candidate/verification.k:41`,
`/candidate/verification.k:49`, and `/candidate/verification.k:57` expand to
the exact trusted-regenerated program constructor tree. Evidence:
`evidence/stage4-ast-identity.log`, `solution.ast.json`, and
`claim-program.ast.json`.

### Satisfiable witnesses and body sensitivity

The entry precondition is satisfiable, for example:

- `A=1, AS=.IntSeq, B=2, BS=.IntSeq`, representing `([1],[2])`, with result
  `"YES"`; and
- `A=1, AS=iCons(3,.IntSeq), B=2, BS=.IntSeq`, representing
  `([1,3],[2])`, with result `"NO"`.

Both ground claims close for candidate `intVals` and for supplied-semantics
ordinary `vCons` lists (`evidence/stage4-ground-symbolic-representation.log`
and `stage4-ground-real-lists.log`). The independent Python run reports the
same results.

I changed the executed ODD-BODY comparison from `!= 0` to `== 0`, rebuilt the
mutated definition successfully, and ran the original proof obligations. The
odd-loop claim became stuck on the contradictory accumulator equality and the
prover exited 1. This changes the program term actually executed by the claim,
not merely an external source file. Evidence:
`evidence/verification-body-mutated.k`,
`stage4-body-mutation-build.log`, and `stage4-body-mutation-proof.log`.

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5-rule-inventory.log` enumerates every module, import,
configuration, context, syntax declaration, rule, claim, and relevant
attribute in the supplied semantics, `verification.k`, and `spec.k`, with
source line, normalized text, and disposition. Totals are:

- 708 rules;
- 234 syntax declarations;
- 5 contexts;
- 3 claims;
- 1 configuration;
- 110 declarations/rules carrying `total`;
- 148 carrying `function`;
- 45 priority rules;
- 35 concrete rules;
- 22 `no-evaluators` declarations;
- 25 explicit symbols;
- 26 `owise` rules; and
- no simplification rule.

The expanded program contains only 18 distinct constructor labels, inventoried
in `evidence/stage5-program-constructs.log`. I traced these through 45
fixed-semantics rules/contexts on the program path. The other 650 supplied
rules have no match along this submitted constructor/control path; none can
enable the target conclusion. They remain part of the fixed supplied language
model, but are not silently treated as proof of this task.

### Fixed-semantics path

The relevant rules implement, in order:

1. module loading and statement sequencing;
2. function binding in module scope;
3. callee lookup, left-to-right argument collection, fresh call frame, and
   positional parameter binding;
4. integer literal evaluation and local assignment;
5. one-time iterable evaluation, `#iterNext`, target binding, body execution,
   and loop continuation;
6. left-to-right `%`, `!=`/`==`, and `<=` evaluation using unbounded K
   integers and the fixed positive-divisor `pyMod`;
7. guard truthiness, branch selection, and integer `AugAssign`;
8. return, frame pop, environment restoration, and exact string-code
   construction.

The program uses bare read-only list inputs, allocates no heap objects, performs
no output, and raises no modeled exception. The loop claims preserve all
omitted/framed cells. The arbitrary `CONT` is safe because the loop summaries
return normally to exactly that continuation; they introduce no return,
exception, break, cleanup, or frame-pop effect.

Relevant rules have compatible guards and priorities. The ref/cell/mutator
priority rules do not match these bare integer-list states. Integer dispatch is
sort-specific. Comparison guards are disjoint. Function lookup and binding are
pinned by the initial scope and the loaded closure, rather than by a textual
name shortcut.

### All 13 proof-local rules

1. The two `intVals` iterator rules distinguish empty from cons and are
   exhaustive over `IntSeq`. They change only the active iterator term and
   reproduce the fixed list protocol's value, remainder, and control exactly.
2. The three `oddAcc` equations are structurally descending. Their
   `pyMod(I,2)==0` and `=/=0` guards are disjoint and exhaustive, and increment
   exactly on odd integers.
3. The three `evenAcc` equations have the same properties and increment
   exactly on even integers.
4. The two `exchangeResult` equations use the disjoint and exhaustive integer
   order partition `<=` versus `>`, returning exact `"YES"`/`"NO"` code
   sequences.
5. The three macro rules are eliminated before execution and were mechanically
   shown to equal the regenerated program AST.

There is no proof-local opaque symbol, priority rule, simplification rule,
unconstrained oracle, task-answer rewrite, or rule that bypasses a
program-defined helper.

### Iterator representation connection

To avoid accepting the `intVals` explanation informally, I built
`evidence/verification-real-encoding.k`, which removes both candidate
`#iterNext` rules and defines only the structural embedding:

```text
intSeqVals(.IntSeq) => .ValSeq
intSeqVals(iCons(I,R)) => vCons(I,intSeqVals(R))
```

Using that definition and the supplied `MPY-LIST` rules, the auditor-authored
empty and cons connection claims reproduce the candidate transitions
universally. Both print `#Top` and exit 0
(`evidence/stage5-iterator-connection-proof.log`). This supplies the
bridge-free connection over the complete match domain.

A diagnostic attempt to rerun the entire proof directly over the embedding
failed because circularity matching retained
`intSeqVals(IS) = vCons(I0,intSeqVals(IS0))` instead of deriving the
corresponding `IntSeq` constructor equality. That residual is preserved in
`stage5-real-encoding-proof.log` and `stage5-real-encoding-proof-attempt2.log`.
It is a prover matching limitation; the two universal transition connection
claims and ordinary-list ground executions establish the semantic relation.

No rule was found unsound on the intended domain, so there is no unsound-rule
false-conclusion witness to report.

**Stage 5 result: PASS.**

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted. I created
`evidence/spec-auditor-vacuity.k`, which executes the exact program on the
satisfiable input `([1],[2])` but changes the result obligation from the true
`"YES"` to false `"NO"`.

```text
kprove spec-auditor-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-AUDITOR-VACUITY --dry-run --output pretty
# exit 0

kprove spec-auditor-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-AUDITOR-VACUITY --output pretty
# WarnStuckClaimState; exit 1
```

The residual is the fully executed `"YES"` code sequence
`[89,69,83]`, which cannot unify with mutated `"NO"` `[78,79]`. This is an
expected unmet result obligation, not a parser error, timeout, unreachable
mutation, or unrelated crash. Evidence:
`evidence/stage6-mutation-dry-run.log` and
`stage6-mutation-proof.log`.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics, for every pair of finite non-empty integer
sequences, execution from the specified standard configuration of the exact
regenerated `exchange` program reaches:

- `"YES"` exactly when the number of odd integers in the first sequence is no
  greater than the number of even integers in the second; and
- `"NO"` otherwise.

The two loop claims establish the accumulator effects for arbitrary finite
tails and arbitrary normal continuations. The entry claim establishes the
load, binding, call, both loops, branch, return, and restoration of all
explicitly fixed machine cells. This is the requested partial-correctness
result; it is not merely agreement on finitely many sizes or examples.

### Trust ledger

- **K toolchain and backend:** K v7.1.293 parsing, compilation, symbolic
  execution, SMT reasoning, and `#Top` are trusted. All commands were run
  fresh.
- **Supplied MPY semantics:** trusted as the benchmark's selected semantics
  level after byte/type identity with `/reference/reference-semantics`.
  Relevant operational rules were statically reviewed. The model uses
  unbounded integers and an ASCII code representation for these output
  strings, both adequate here.
- **Trusted translator:** trusted CPython-AST-to-constructor bridge; its mounted
  hash matches, regeneration is byte-identical, and the executed claim AST is
  mechanically identical.
- **`intVals` representation:** no longer merely assumed. Its complete two-rule
  iterator behavior is connected by bridge-free `#Top` claims to a structural
  ordinary-list embedding. It has no other observable operation in the
  program.
- **Mathematical intent bridge:** the swap condition is the elementary count
  inequality above. It agrees with the trusted canonical implementation and
  29,348 independent tests. Testing supports this bridge but does not replace
  the K proof.

No opaque supplied float, digest, sort, evaluation, or other trusted primitive
is reachable from this program or influences its result.

### Excluded behavior

- Empty lists are excluded by the source contract and entry claim. The
  implementation happens to agree with the canonical on tested empty cases,
  but the theorem does not claim them.
- Non-integer numeric values, booleans as numeric list elements, malformed
  calls, and Python behaviors outside the supplied Mini-Python subset are not
  claimed. Odd/even parity and the canonical program make integer lists the
  material source domain, so this is not a domain narrowing.
- The theorem is about the supplied semantics, not all of CPython's object,
  exception, mutation, or numeric behavior.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(trust/evidence auditability) all pass. There is no material adequacy gap or
unresolved result-bearing assumption.

VERDICT: PASS
LEGITIMACY: LEGIT
