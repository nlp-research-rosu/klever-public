# Independent adversarial review: HumanEval 12 `longest`

The submitted Python implementation is correct, its translation is authentic,
and all submitted K claim groups reconstruct to `#Top`. The proof is modular:
one claim pins public-call dispatch to the exact function body, fixed semantics
performs parameter binding and the two initial assignments, and the five
result-bearing loop claims cover both constructors of every finite string
sequence. Together they constrain the returned value to the `longestAcc`
first-on-tie maximum-length fold.

The candidate does not include a single assembled nonempty entry claim, and
its two proof-domain iterator bridges lack a bridge-free machine-checked
connection theorem. These are genuine auditability limitations. They do not
provide a false-behavior witness or make the modular theorem unsound: the
constructor linkage and deterministic control-flow connection are exact, and
a body mutation in the result-bearing loop is rejected. The completed finding
is therefore legitimate with concerns, not an infrastructure or integrity
failure.

## 1. Input and provenance integrity

### Launcher records and layout

`/audit-input.json` declares:

- problem `12-longest`;
- condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`;
- a required supplied-semantics mount.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/usage.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and the JSONL trace under
`/generation-evidence/codex-trace/`. The optional usage record is present.
Historical `runtime-metrics.json` is absent, which is permitted for this
legacy-selected-stage1 layout. The legacy auxiliary records
`legacy-metrics.json` and `legacy-run-input.json` are also present.

`evidence/provenance-structural-check.log` records an independent standard
library parser/hash check. It established:

- the campaign-lock JSON object exactly equals the `audit_campaign` object in
  `/audit-input.json`;
- the lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly as recorded;
- every direct launcher hash for the canonical program, prompt, translator,
  manifests, generation logs, prompt, metrics, usage, and result matches;
- both stage records' per-file evidence hashes match all seven mounted
  generation evidence artifacts;
- all 734 structured-trace lines parse as JSON: 205 `event_msg`, 526
  `response_item`, one `session_meta`, one `turn_context`, and one
  `world_state`;
- the usage record points to the trace's token-count event at line 733.

The old legacy workspace/tree digests and the newer audit tree digests use
distinct recorded schemes; the same supplied-semantics tree is correspondingly
recorded with both a legacy and a manifest hash. I did not equate those opaque
cross-scheme values. Instead, I checked the mounted artifacts directly and
recursively.

All provenance mounts are real, readable, non-symlinked, and read-only;
`evidence/mount-readonly-check.log` records the mount options. The required K
toolchain is present at version 7.1.293
(`evidence/toolchain-versions.log`).

### Trusted-versus-candidate integrity

The rendered mode is internally consistent:
`/reference/reference-semantics` exists as required.

The independent tree comparison found:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- `/candidate/reference-semantics` contains exactly the same 24 regular files
  and one subdirectory as `/reference/reference-semantics`;
- there are no missing, additional, changed, mistyped, linked, or unsupported
  entries in the candidate semantics tree;
- all 36 candidate files are regular files and the candidate tree contains no
  symlinks.

The historical generation records claim successful concrete execution and two
`#Top` proof groups. Those records were treated only as untrusted claims.
Fresh reconstruction below is the operative evidence.

There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt and canonical implementation specify:

- input: an unrestricted finite `List[str]`;
- empty list: return `None`;
- nonempty list: return an element having maximum Python string length;
- ties: return the earliest such element.

The canonical implementation computes the maximum length and returns the first
element of that length. The candidate maintains a current result, initializes
it from the first element, replaces it only on a strict length increase, and
therefore implements the same contract.

### Trusted translation

In the fresh scratch tree I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

The submitted and regenerated files both hash to
`cd13a20e5b6377f13c2cae63c9d4e8931153cfda90b9b588676f7723ab8684d0`
and compare byte-for-byte equal. Exact command and status are in
`evidence/translation-byte-identity.log`.

### Independent differential execution

`evidence/differential_test.py` independently imports the trusted canonical
entry point and candidate entry point. It covers:

- all prompt examples;
- the empty list and singleton boundary;
- empty strings;
- first-element initialization;
- strict-longer, shorter, and tied branches;
- ties before and after longer elements;
- NUL, newline, composed/decomposed Unicode, emoji, and CJK strings;
- every list of length 0 through 4 over seven fixed strings;
- 1,000 deterministic generated lists of lengths 0 through 20.

The exact run in `evidence/differential-test.log` tested 3,814 inputs, exited
zero, and reported `mismatches=0`. This finite evidence supports program
fidelity; it is not substituted for the K proof.

Stage 2 passes.

## 3. Clean proof reconstruction

All execution used the fresh source-only tree
`/tmp/audit-work/12-longest-fresh`. Candidate-provided compiled directories,
caches, the Python bytecode cache, and `kore-exec.tar.gz` were not copied or
used. The executable semantics came from the trusted reference mount.

### Concrete definition

The following fresh build exited zero:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

See `evidence/kompile-runtime.log`. Compiler warnings concern incomplete
matches in fixed, unused general-purpose functions; none is on this program's
path.

`python3 concrete_tests.py` exited zero
(`evidence/concrete-python-tests.log`). A fresh
`krun concrete_tests.mpy --definition runtime-kompiled` also exited zero,
finished at `.K`, kept `NoExc`, and had exit code 0
(`evidence/concrete-k-tests.log`).

### Proof definition and submitted positive claims

This source build exited zero:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

See `evidence/kompile-verification.log`.

The candidate declares two positive target commands because the five loop
claims are mutually supporting circularities. Both were independently rerun:

```text
kprove spec.k --definition verification-kompiled \
  --claims loop-init-empty,loop-init-cons,loop-empty,loop-longer,loop-retain
```

and

```text
kprove spec.k --definition verification-kompiled \
  --claims load-solution,call-empty,call-cons-dispatch
```

Each printed `#Top` and exited 0. The bounded outputs and exact statuses are in
`evidence/kprove-loop-group.log` and
`evidence/kprove-entry-group.log`.

I additionally ran `loop-init-empty`, `loop-empty`, `load-solution`,
`call-empty`, and `call-cons-dispatch` in separate prover invocations; each
printed `#Top` and exited zero. Their logs are
`evidence/kprove-loop-init-empty.log` and
`evidence/kprove-individual-loop-empty.log`,
`evidence/kprove-individual-load-solution.log`,
`evidence/kprove-individual-call-empty.log`, and
`evidence/kprove-individual-call-cons-dispatch.log`. An isolated
`loop-init-cons` run was stopped with status 130 after removing its mutually
supporting longer/retain circularities caused non-progress. This supplemental
isolation is not treated as a candidate failure; the exact submitted group
closes.

Thus the dynamic reconstruction gate confirms exactly what the stage-one
record claimed: all *submitted* claims close. It does not establish that those
claims state the requested theorem.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each claim

The five helper claims begin inside an already-created function frame, at the
program's actual loop followed by its actual return:

1. `loop-init-empty`: with accumulator `None` and no remaining elements, the
   function returns `None` and restores the caller frame.
2. `loop-init-cons`: with accumulator `None` and a nonempty remaining
   sequence, the first element initializes the accumulator and execution
   returns `longestAcc(first, rest)`.
3. `loop-empty`: with a string accumulator and no remaining elements,
   execution returns that accumulator.
4. `loop-longer`: if the next string is strictly longer than the string
   accumulator, execution returns the fold summarized from the new string.
5. `loop-retain`: if the next string is shorter or tied, execution returns the
   fold summarized from the earlier accumulator.

The remaining claims mean:

6. `load-solution`: loading the complete submitted `Module(...)` into a clean
   module scope installs `longestSolution`.
7. `call-empty`: calling that closure with the represented empty list returns
   `noneV` in the clean entry configuration.
8. `call-cons-dispatch`: calling that closure with a represented nonempty list
   allocates the callee scope and stack frame and reaches
   `#bindP ~> exact-body ~> #endcall`.

Claim 8 alone does **not** execute to a return in its destination. The return
obligation is carried by claims 1–5. Their connection is exact: from claim 8's
destination, fixed rules bind `strings`, execute `result = None` and
`string = None`, evaluate the already-bound list once, and lower the `For` to
the same `#loop(...) ~> Return(...) ~> #endcall` term used by the loop claims.
The environment, callee scope, stack frame, heap, and continuation at that
point instantiate the loop-claim cells directly.

### Satisfiable preconditions and ground substitution

Every precondition is satisfiable. Irrelevant symbolic fields may be
instantiated with `.Map`, `0`, `.List`, the exact closure, and arbitrary valid
current bindings. Concrete examples recorded in
`evidence/claim-witnesses.log` include:

| Claim shape | Satisfying input/state | Claimed summary | Canonical and candidate Python |
|---|---|---|---|
| init-empty / call-empty | `[]` | `None` | `None` |
| init-cons | `["a", "bbb"]` | `"bbb"` | `"bbb"` |
| loop-empty | accumulator `"x"`, no rest | `"x"` | `"x"` |
| loop-longer | accumulator `"x"`, next `"yy"` | `"yy"` | `"yy"` |
| loop-retain, shorter | accumulator `"xx"`, next `"y"` | `"xx"` | `"xx"` |
| loop-retain, tie | `"first"`, then `"later"` | `"first"` | `"first"` |
| nonempty public call | `["a", "bbb", "cc"]` | `"bbb"` via init-cons/loop claims | `"bbb"` |

The helper postconditions agree with both Python implementations on these
witnesses. Reachability transitivity connects the exact dispatch/prefix to the
result-bearing loop postcondition in the last row.

### Mechanical program pinning

There are two independent pinning checks:

1. trusted regeneration gives byte identity for `solution.mpy`;
2. `evidence/extract_load_module.py` extracts the `Module(...)` term executed
   by `load-solution`, normalizes only the parser spelling of empty `.Stmts`,
   and parses both terms with `kast --expand-macros --output json`.

The constructor JSON hashes are identical:

```text
74114ab08c87f6b712b57e36251f69dbbb4c83c91a8a12574d20bb417009bb57
```

See `evidence/constructor-pinning-check-final.log`. The load claim and macro
therefore pin the exact generated body; typing-only imports are handled by the
fixed no-op import rule.

### Modular entry composition and body sensitivity

The candidate does not include the following convenient assembled theorem:

```text
Call(Name("longest"),
     list(stringVals(sCons(HEAD, TAIL))), .Exprs)
  => longestAcc(str(HEAD), TAIL)
```

with the caller configuration restored. Its absence is an auditability
limitation, but it is not a missing semantic case. The submitted claims provide
the same derivation modularly:

1. `load-solution` machine-checks that the exact module installs the exact
   `longestSolution` closure.
2. `call-cons-dispatch` machine-checks the selected binding and exact complete
   body, including the active continuation and frame state.
3. Fixed semantics performs only parameter binding, two constant
   initializations, name lookup of the input list, and `For` lowering before
   the loop-claim source is reached.
4. `loop-init-cons` handles every nonempty `StringSeq`; `loop-init-empty`
   handles the empty constructor. The longer/retain claims cover the disjoint
   and exhaustive length comparison at every subsequent cons.
5. Return and frame restoration are inside every loop claim's source and
   destination.

Thus every material operation and control effect of the generated body is
executed, and the modular proof constrains a nonempty return to
`longestAcc(str(HEAD), TAIL)`.

I separately machine-checked the finite link rather than relying only on
visual term comparison. `evidence/spec-prefix-steps.k` states four
reviewer-authored reachability steps for the exact clean frame: bind
`strings`, assign `result = None`, assign `string = None`, and evaluate/lower
the represented-list `For` to the submitted `#loop` shape. The combined
command:

```text
kprove spec-prefix-steps.k --definition verification-kompiled \
  --spec-module SPEC-PREFIX-STEPS \
  --claims bind-input-step,init-result-step,init-string-step,for-lowering-step
```

printed `#Top` and exited zero
(`evidence/kprove-prefix-steps.log`). These supplemental claims use only the
fresh supplied proof definition; they add no semantic rules.

The dispatch theorem would be insufficient *by itself*. In
`evidence/verification-dispatch-mutant.k`, the closure term actually executed
by the claim retains the submitted loop but materially changes its final
statement to `Return(NoneVal)`. For every nonempty list this is wrong whenever
the required result is a string. The corresponding claim in
`evidence/spec-dispatch-mutant.k` has exactly the submitted
`call-cons-dispatch` theorem shape: it ends at that wrong body's initial call
frame. A fresh definition built successfully and:

```text
kprove spec-dispatch-mutant.k \
  --definition dispatch-mutant2-kompiled \
  --spec-module SPEC-DISPATCH-MUTANT \
  --claims call-cons-dispatch-mutant
```

printed `#Top` and exited zero. See
`evidence/kompile-dispatch-mutant2.log` and
`evidence/kprove-dispatch-mutant2.log`. This mutation changes the program term
actually selected by the claim; it does not merely edit an external source
file. It demonstrates why the dispatch claim must be read together with the
result-bearing loop claims and exact body comparison; it does not invalidate
that complete modular proof.

The proof as a whole is body-sensitive.
`evidence/spec-body-sensitivity.k` changes the loop body actually executed by
the result-bearing claim so it incorrectly retains `"x"` when the remaining
string is `"ab"`, while keeping the true `"ab"` destination. After correcting
an initial reviewer parser typo, the meaningful run in
`evidence/kprove-body-sensitivity-corrected.log` reached terminal `"x"`,
reported `WarnStuckClaimState`, and exited 1. A materially wrong loop body
therefore breaks the result proof as required.

I also authored `evidence/spec-omitted-entry.k` to state the missing composed
entry theorem. An import-based supplemental run was stopped after 120 seconds
without output. To exclude the possibility that claim imports hid the helper
circularities, `evidence/make_combined_spec.py` then mechanically copied all
original claims unchanged into `evidence/spec-combined-entry.k` and added only
the missing entry obligation. That prover remained CPU-active without `#Top`
or a residual for about seven minutes and was stopped with status 130. Neither
unsubmitted experiment is credited to or charged against the candidate as a
timeout failure. They do not replace the candidate artifacts and show that a
single assembled theorem is not independently available as a quick
reconstruction. The supplied modular derivation remains exact by the
machine-checked dispatch/loop endpoints and the finite fixed-semantics prefix.

The formal `StringSeq` domain itself is not narrowed: it inductively denotes
arbitrary finite lists, each element is an arbitrary finite `IntSeq`, and no
size bound appears.

Stage 4 passes, with a non-fatal auditability concern because the transitive
composition is not packaged as one positive entry claim.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/static-rule-inventory.tsv` inventories every local K entry in the
supplied semantics and `verification.k`:

- 941 entries total;
- 1 configuration;
- 231 syntax declarations;
- 5 evaluation contexts;
- 704 rules;
- 148 function-bearing entries;
- 111 totality-bearing entries;
- 36 priority rules;
- 29 `owise` rules;
- no `functional` or `simplification` attributes.

`evidence/static-review-decisions.md` gives the per-file count and decision for
all 941 entries, then decides each of the 13 candidate-local entries
individually. The supplied entries are byte-identical to the selected fixed
semantics. I checked intended-Python adequacy in detail for every rule reachable
from this program; unused fixed modules cannot participate in claim closure.

### Mapping of used constructors to semantics

| Submitted construct | Declaration and material rules |
|---|---|
| `Module`, statement list | `syntax.k:56–61`; `core.k:124–127` loads and sequences statements |
| `ImportFrom("typing",...)` | `syntax.k:43`; `controls.k:35–44`, where non-`math` imports are no-ops |
| `FuncDef`, `Params` | `syntax.k:53–60`; `functions.k:14–16` installs the closure |
| `Name` | `syntax.k:12`; `core.k:130–154` performs scope-chain lookup |
| `NoneVal` and `is None` | `core.k:196`; `operators.k:19` |
| `Assign` | strict RHS in `syntax.k:41`; local update in `controls.k:9–18` |
| `For` | strict iterable in `syntax.k:45`; `controls.k:69–74` plus iterator rules |
| loop target binding | `tuple.k:31–41` updates the current scope's name |
| `If` | strict condition in `syntax.k:49`; `controls.k:51–54` |
| `Call` and argument order | `call.k:20–32`; `core.k:183–191` evaluates left-to-right |
| user call/frame | `call.k:69–75`; `functions.k:63–90` binds, returns, restores, and deletes frame |
| builtin `len` | `builtins.k:17–26`; strings reduce through `isLen` in `core.k:227–229` |
| integer `<=`, `>` | comparison contexts in `operators.k:14–20`; cases in `int.k:23–24` |
| `Return` | strict expression in `syntax.k:50`; abrupt return/pop in `functions.k:78–90` |

These rules preserve evaluation order, the local scope changes, loop
continuation, return control, and the clean call's unchanged heap. The source
performs no material allocation for its unboxed proof input. On the stated
`List[str]` domain, no modeled exception is reachable.

### Candidate-local extensions

The local inventory is:

- `StringSeq` and `stringVals`: an unbounded proof-domain representation;
- two truthful constructor equations for that representation;
- two priority-40 iterator operational bridges;
- `longestAcc`, with base, initialize, longer, and retain equations;
- the exact `longestSolution` macro.

The `longestAcc` `>` and `<=` guards are disjoint and exhaustive over integer
lengths. Each recursive equation descends structurally. The summary is used
only with `noneV` or `str(...)`; its declared `Val` argument is broader, but
missing equations on other value constructors leave those unused cases
uninterpreted and enable no false equality here.

The two iterator bridges preserve every cell, accept the same arbitrary
continuation as the fixed iterator rules, and implement exactly:

- represented empty sequence to `#iterDone`;
- represented cons to yield its head string and residual represented list.

I attempted the validating-proof bridge-free connection test using
`evidence/verification-no-iter-bridge.k` and
`evidence/spec-iter-connection.k`. It built, but the proof exited 1 with
`WarnStuckClaimState`: ordinary `stringVals` equations do not contextually
reduce beneath `#iterNext(list(...))`. This means the candidate lacks a
machine-checked universal connection theorem for the bridges. It is an
evidence gap, not a demonstrated unsound rule. There is no false-conclusion
witness: on both complete constructor cases, the bridge transition is the
ordinary mathematical list-iterator transition and changes no other state.
Per the audit instruction, I do not label it unsound without such a witness.

The fixed semantics declares 22 opaque `no-evaluators` primitives for floats,
sorting, and MD5. None is reachable from this solution or any submitted claim.
No local opaque oracle, task-answer rule, execution-bypassing summary, or
contradictory overlap was found.

Static soundness therefore does not add a false-rule finding. It also does not
remove the auditability concern created by leaving the nonempty entry
composition unpackaged as a single submitted claim.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact; none was submitted.

`evidence/spec-vacuity.k` creates a fresh ground, satisfiable state:

- current best is `"x"` (code sequence `[120]`);
- the sole remaining string is `"ab"` (codes `[97, 98]`);
- the actual submitted loop body and return execute;
- the false destination incorrectly retains `"x"`.

The claim parses and reaches the backend, so this is not a parser/build probe.
The exact command was:

```text
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims false-retain-longer
```

It exited 1 with `WarnStuckClaimState`. The residual terminal `<k>` cell is
`str(iCons(97, iCons(98, .IntSeq))) ~> .K`, i.e. `"ab"`, which does not unify
with the false `"x"` destination. The exact bounded output is in
`evidence/kprove-vacuity-mutation.log`.

The loop theorem is therefore result-sensitive and non-vacuous. This stage
passes. Here the result-bearing loop theorem composes with the exact dispatch
claim and deterministic fixed-semantics prefix described in Stage 4.

## 7. Proven versus assumed accounting

### What the successful K runs establish

Under the supplied K theory, the reconstructed claims and reachability
transitivity establish:

- the exact regenerated module loads the exact submitted closure;
- an empty represented-list call returns `None`;
- a nonempty represented-list call dispatches to the exact function body and
  creates the expected call frame;
- fixed deterministic rules bind the input, perform the two initializations,
  and lower the actual `For` statement to the loop source used by the helper
  claims;
- from the submitted loop-head states, the exact loop and return compute the
  `longestAcc` recurrence and restore the caller frame;
- consequently, every nonempty represented-list public call returns
  `longestAcc(str(HEAD), TAIL)`.

The `longestAcc` recurrence is mathematically the first-on-tie maximum-length
fold over its represented string sequence. Together with the empty case, this
is the required partial-correctness result for every finite `StringSeq`, with
no length bound.

The candidate's machine-checked claims do not package the complete nonempty
composition in one positive target. The finite control-flow prefix was
separately reconstructed to `#Top` during this audit, while the local iterator
bridges are not justified by a separate bridge-free K theorem. The latter link
is established by exhaustive constructor inspection rather than by an
additional closing `#Top`.

### Trust and evidence ledger

| Boundary | Role | Assessment |
|---|---|---|
| K reachability prover/backend and built-in Int/Map/List/String hooks | Machine-checking foundation | Necessary trusted toolchain boundary. |
| Supplied, byte-identical reference semantics | Defines the selected execution model | Acceptable fixed boundary; used rules were statically checked against this program. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Supported by byte-identical regeneration; does not prove source semantics universally. |
| `StringSeq`/`stringVals` representation | Abstract finite list-of-strings domain | Sound and unbounded by constructor inspection. |
| Two local iterator bridges | Interpret represented sequence at list iteration | Truthful on both constructors, but lacking a bridge-free machine-checked connection theorem; documented evidence limitation. |
| `longestAcc` meaning | First-longest mathematical fold | Directly follows from exhaustive/disjoint recursive equations; no opaque value oracle. |
| Opaque float/sort/MD5 fixed symbols | General semantics capabilities | Unreachable and non-dependent. |
| Differential tests | Finite Python implementation evidence | 3,814 zero-mismatch cases; supports fidelity only. |
| Constructor comparison | Program-term identity | Exact parsed constructor equality. |
| Reviewer prefix-step claims | Dispatch-to-loop connection | Four exact supplied-semantics steps close together with `#Top`; no added rules. |
| Wrong-body dispatch mutation | Dispatch-claim sensitivity | Demonstrates that dispatch alone proves body selection, not correctness; the result-bearing loop claims are necessary. |
| Wrong-loop-body mutation | Whole-proof body sensitivity | A materially false loop body reaches the wrong terminal value and fails the true destination. |
| False-result mutation | Non-vacuity | Meaningful expected failure with the exact wrong-result residual. |

### Gate and decision summary

- Provenance/infrastructure: pass.
- Program and translation fidelity: pass.
- Fresh reconstruction of all submitted positive targets: pass.
- Local extension soundness on the used domain: no false-rule witness found.
- Non-vacuity of result-bearing loop claims: pass.
- Real-program public-entry result constraint: pass by exact modular
  reachability composition.
- Intent adequacy for the requested partial-correctness theorem: pass.
- Evidence packaging and local-bridge justification: concern.

The candidate proves the unrestricted finite source-contract domain rather
than examples or bounded sizes. Its exact program term, call frame, real loop,
return, and result recurrence are all constrained. The lack of a monolithic
entry claim and a bridge-free connection theorem makes the proof harder to
audit and leaves an informal constructor-level trust bridge, but neither
limitation enables a false conclusion or materially narrows the domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
