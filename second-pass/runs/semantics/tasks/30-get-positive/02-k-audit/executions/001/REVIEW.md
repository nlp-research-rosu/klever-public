# Independent adversarial review: 30-get-positive

This audit was performed against the trusted mounts, from fresh source builds in
`/tmp/audit-work/30-get-positive`. Nothing under `/candidate` was executed or
modified in place, and no candidate-provided compiled definition or cache was
used.

The proof is legitimate but limited. It machine-checks the real submitted
function body for arbitrary finite integer sequences represented through a
proof-local input adapter. The result is constrained and the proof is
non-vacuous. The limitations are that the entry claim manually seeds the exact
closure instead of loading the submitted `Module(...)` term, the universal
input is a synthetic `intVals(IntSeq)` representation rather than the supplied
semantics' ordinary `vCons` list representation, and the formal theorem covers
integers only although the prose says “numbers.” These are visible,
non-oracular bridges; they do not enable a false conclusion in the theorem's
formal domain, but they preclude an unqualified PASS.

## 1. Input and provenance integrity

### Mount-condition check

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no mount contradiction,
so this is a candidate audit rather than an infrastructure error.

The recursive command

```text
diff -ruN --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics
```

exited 0 with no differences. A complete type walk found only directories and
regular files in both semantics trees. A separate whole-candidate symlink scan
found no symlink. Thus there are no missing, added, changed, mistyped, or
symlinked entries under the candidate's required `reference-semantics/` tree.
This integrity result does not bless the proof-local rules in
`verification.k`; those are reviewed separately below. Exact commands, hashes,
types, and statuses are in `evidence/00_provenance.log`.

The candidate prompt and translator are byte-identical to their trusted
versions:

| Artifact | Trusted/candidate SHA-256 | `cmp` |
|---|---|---|
| `prompt.py` | `278875ddc3e598e47227263e6384f3c169b8526e9ab6475e52e939d6a151f00b` | exit 0 |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exit 0 |

The required proof and program sources are regular files. Their copied scratch
versions retain the candidate hashes; see `evidence/09_static_checks.log`.
The candidate's `__pycache__/solution.cpython-310.pyc` was treated as an
irrelevant, untrusted cache and was not copied.

### Missing generation records

The following named generation records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No file with `trace` in its name and no JSONL structured trace exists below the
candidate root at depth two. Consequently there were no untrusted generation
claims to compare with the reconstruction. This is a provenance/auditability
defect, but not a substitute for—or a contradiction of—the fresh source-level
reconstruction.

Stage 1 result: integrity of all available proof inputs and supplied semantics
passes; generation metadata is missing and contributes to the concerns verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

`/reference/prompt.py` requires `get_positive` to return only the positive
numbers from its input list. `/reference/canonical.py` implements that as
`[e for e in l if e > 0]`. In plain language, the expected output:

- contains exactly the elements whose comparison with zero is true;
- excludes negative values and zero;
- preserves original order and duplicates; and
- is a newly constructed list.

`/candidate/solution.py` implements the same operation using an accumulator,
one left-to-right `for` loop, an `if x > 0` guard, and `append`. It has no
additional branch, state effect, or reordering.

### Trusted translation

The trusted command

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/30-get-positive/solution.py \
  > /tmp/audit-work/30-get-positive/regenerated-solution.mpy
```

exited 0. `cmp` against the submitted `solution.mpy` exited 0, and both files
have SHA-256
`f89d5ec0a7acf90c31ffe400ceaba3d0cb4541b997eb34f372421069bc02948e`.
See `evidence/01_translation.log`.

### Independent differential test

`evidence/02_differential.py` loads the trusted canonical and scratch-copied
submitted modules independently by path. It does not import candidate tests or
reuse any proof equation. It covers:

- both documented examples;
- the empty list;
- integer and float values immediately below, at, and above zero;
- all-negative, all-positive, duplicate/order, large-integer, Boolean, NaN,
  and infinity cases;
- every list of lengths zero through five over `[-3, -1, 0, 1, 3]`; and
- 1,000 deterministic random integer or finite-float lists with seed 30030.

The exact run covered 4,917 inputs and reported zero mismatches with exit 0.
The script, scope, oracle, command, and result are preserved in
`evidence/02_differential.py` and `evidence/02_differential.log`. This is finite
evidence of implementation/canonical alignment; it is not used as a universal
K proof.

Stage 2 result: PASS.

## 3. Clean proof reconstruction

### Fresh definitions and concrete runs

Only source artifacts were copied into `/tmp/audit-work/30-get-positive`.
Candidate definitions and caches were neither copied nor referenced.

With K version `v7.1.337`, the fresh concrete build

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

exited 0. The compiler emitted supplied-semantics warnings about several
over-broad `[total]` declarations; these are accounted for in Stages 5 and 7
and are not on this program's execution path.

Fresh `krun solution.mpy` exited 0 with `.K`, `NoExc`, exit code 0, and the
module scope binding `get_positive` to a closure containing the exact submitted
translated body. A reviewer-authored assertion harness was translated with the
trusted translator and run under the fresh LLVM definition. Both CPython and
K executions exited 0 for the examples, empty input, the `[-1, 0, 1]` branch
boundary, and a duplicate/order case. The complete final K configuration
records the expected output heaps. See:

- `evidence/04_reviewer_concrete.py`
- `evidence/04_concrete_rebuild.sh`
- `evidence/04_concrete_rebuild.log`

### Fresh symbolic definition and claims

The fresh Haskell command

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

exited 0. Each positive target was then checked:

| Check | How dependencies were handled | Result |
|---|---|---|
| `SPEC.filter-loop` | selected alone | exit 0, `#Top` |
| `SPEC.get-positive-correct` | selected with only the already independently proved `SPEC.filter-loop` marked trusted as a staged lemma | exit 0, `#Top` |
| submitted SPEC as a whole | both claims untrusted in the original joint proof | exit 0, `#Top` |

Commands and full bounded outputs are in `evidence/05_claims.log`. The staged
use of `--trusted SPEC.filter-loop` is not an unproved assumption: the same
fresh definition first proved that exact claim alone, and the final joint run
also proved both original claims without a trusted label.

An earlier diagnostic in `evidence/05_proof_rebuild.log` selected only the
entry claim, thereby removing its loop circularity from the retained claim set.
That diagnostic was manually stopped and is not counted as success or failure.
The conclusive checks are the three exit-0/`#Top` runs above.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claim meanings

The `filter-loop` claim has this precondition:

- computation is the real loop head
  `#loop(list(intVals(INPUT)), Name("x"), positiveLoopBody)` followed by an
  arbitrary continuation `CONT`;
- the current local frame has `l`, `result`, and `x`, with `result` referring
  to heap location `ACC_LOC`;
- the heap at that location contains the current sequence `PREFIX`; and
- all other configuration state is framed.

Its postcondition consumes the loop, preserves the continuation and all framed
state, allows only `x` to have an existential final value, and changes the
accumulator heap sequence to `filterPositive(PREFIX, INPUT)`.

The `get-positive-correct` entry precondition has:

- computation `Call(Name("get_positive"), list(intVals(INPUT)))`;
- environment 0;
- an exact module-scope closure for `get_positive`;
- the supplied builtins frame;
- fresh scope location 1, an empty heap with fresh location 0, an empty call
  stack, no pending return or exception, and exit code 0.

Its postcondition fixes the returned value to `ref(0)`, fixes heap location 0 to
`list(filterPositive(.ValSeq, INPUT))`, advances `heapLoc` to 1, and restores
the other entry state. The returned value is neither free nor tautological.
`filterPositive` is a fully recursive, result-bearing mathematical filter, not
an uninterpreted oracle.

### Satisfiable states and ground substitution

Both claim preconditions are satisfiable. For the entry claim,
`INPUT = .IntSeq` with the exact listed initial configuration is one witness.
For the loop claim, use `INPUT = .IntSeq`, `PREFIX = .ValSeq`,
`LOCAL = 1`, `ACC_LOC = 0`, an ordinary local scope with the three specified
bindings and parent 0, and a heap containing `0 |-> list(.ValSeq)`.

A nonempty witness was also checked:

```text
INPUT = iCons(-2, iCons(0, iCons(3, iCons(1, .IntSeq))))
```

The formal claimed sequence reduces to `vCons(3, vCons(1, .ValSeq))`.
The trusted canonical and submitted Python implementations both returned
`[3, 1]`, and the corresponding ground K reachability claim closed with
exit 0 and `#Top`. See `evidence/06_ground_compare.py`,
`evidence/06_ground-spec.k`, `evidence/06_ground_witness.sh`, and
`evidence/06_ground_witness.log`.

### Pinning strengths and limitations

The macro `getPositiveBody` expands to the same `Assign`, `For`, `If`,
`Compare`, `append`, and `Return` tree found in the byte-verified submitted
`solution.mpy`; `positiveLoopBody` is its exact nested loop body. Fixed
semantics execute those terms. A fresh concrete load of `solution.mpy` produced
the exact closure used by the claim, and changing the macro's comparison from
`> 0` to `> 1` caused the original summary proof to fail at the expected
obligation (`evidence/08_body_sensitivity.log`).

There is nevertheless a pinning limitation: the entry `<k>` cell starts from a
manually seeded closure call. It does not itself contain and execute the
submitted top-level `Module(FuncDef(...))`. The fixed module-load and function
definition rules make the bridge straightforward, and the concrete load
confirms the exact state, but that load-to-entry bridge is not an auxiliary
reachability theorem in the candidate.

There is also an input-representation limitation. `intVals(IntSeq)` is a fresh
proof-local `ValSeq` constructor whose two iterator rules make it yield the
same integers, in the same order, as the intended ordinary `vCons` sequence.
This program observes its input only through iteration, so the adapter is
behaviorally adequate for this body. But the candidate does not contain a
bridge-free universal theorem connecting `list(intVals(INPUT))` to ordinary
source-created/heap-allocated lists. The bridge is therefore an explicit
informal intent bridge, supported by ground and differential evidence rather
than universally proved in K.

Finally, `INPUT` has sort `IntSeq`. The formal theorem covers finite integer
sequences, not floats or other Python “numbers.” The implementation agrees with
the canonical on the tested broader numerical cases, but that broader behavior
is empirical, not part of the K theorem.

These limitations do not expose a false formal conclusion or a substituted
function body. They are the principal reason for `CONCERNS` rather than `PASS`.

Stage 4 result: sound and result-constraining, with documented intent and
entry-representation limitations.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/RULE-INVENTORY.md` is a generated, line-addressed inventory of every
configuration declaration, syntax declaration, context, rule, and claim in the
selected supplied-semantics theory, `verification.k`, and `spec.k`. It contains
232 syntax declarations, 703 rules, five contexts, one configuration, and two
claims. Function, total, macro, concrete, owise, priority, symbol, and
no-evaluators attributes are attached to their declarations/blocks. There are
no `[functional]` or `[simplification]` declarations in this selected theory.
The inventory was generated by the reviewer-authored
`evidence/03_k_inventory.py`; its command exited 0.

For every inventoried rule from `reference-semantics/`, the audit disposition
is: accepted at the selected supplied-semantics boundary after confirming that
the candidate copy is byte-identical and contains no local alteration.
Rules in unused modules cannot contribute to this claim's closure. Rules on the
used path were additionally checked against control flow, state, and values as
described below. This is not an assertion that the supplied subset models every
Python behavior; it is a decision relative to the authoritative supplied
semantics and the constructs this submitted program uses.

File-level review and relevance:

| Source | Role and audit decision |
|---|---|
| `semantics.k` | Exact assembly of MPY and MPY-KRUN; import split is coherent. Haskell uses MPY, LLVM additionally uses MPY-CONCRETE. |
| `syntax.k` | Declares every submitted AST constructor. Strictness/evaluation positions for assignment, iterable, condition, call components, expression statements, and return are appropriate. |
| `core.k` | Configuration, module sequencing, lookup, allocation, literals, truthiness, and sequence helpers. Used rules preserve allocation counters and framed maps. |
| `iter.k` | Declares the iterator protocol only. Proof-local iterator cases are checked below. |
| `range.k` | Unused, constructor-complete arithmetic range iteration. |
| `operators.k` | Used comparison dispatch evaluates left then wrapped right and routes integer `>` to `applyCmp`. Heap dereference rules are irrelevant to integer elements. |
| `int.k` | Used `applyCmp(">", I, 0) => I >Int 0`; this is the exact branch predicate. Other arithmetic rules are unused. |
| `bool.k` | Boolean operator rules are unused; no conflicting comparison rule overlaps the integer `>` case. |
| `float.k` | All float and opaque float symbols are unused by the integer theorem. |
| `str.k` | String operations are unused. Compiler's unused-variable warnings are harmless. |
| `set.k` | Unused. |
| `list.k` | Used list literal allocation, concatenation, list iteration, and the priority-40 in-place `append` heap update. The append rule preserves all cells except the named heap entry and returns `noneV`. |
| `tuple.k` | Used `#bindTgt(Name("x"), I)` updates only `x` in the current scope; tuple/unpack rules are unused. |
| `subscript.k` | Unused. Its warned total `valSeqAt` gap does not occur on this path. |
| `comprehension.k` | Unused by the submitted loop implementation. It is not used as a shortcut to canonical behavior. |
| `methods.k` | Pure method bodies are unused. Call routing distinguishes mutating `append`, whose actual rule is in `list.k`. |
| `controls.k` | Used assignment, expression discard, if branch, for-loop iterator protocol, and one-time iterable handling. Loop rules sequence binding, the real body, and the next loop head in the correct order. |
| `functions.k` | Used return, frame pop, and closure frame lifecycle. It restores environment, stack, return state, and scope allocation after returning the heap reference. |
| `builtins.k` | General builtins are unused. `builtinsScope` itself is defined in `core.k`. The opaque MD5 symbol is inert. |
| `call.k` | Used name/callee evaluation, left-to-right argument evaluation, closure frame creation, and bound-method dispatch. Mutating `append` retains the list reference rather than dereferencing it. |
| `sort.k` | Opaque sorting symbols and all sort rules are unused. |
| `assert.k` | Excluded from the proof path; used only by the independent concrete harness. |
| `dict.k` | Unused. |
| `concrete.k` | Not imported into the Haskell proof. Its LLVM-only rules are irrelevant to symbolic closure and were used only in concrete reconstruction where applicable. |

### Submitted-construct mapping

Every construct in `solution.mpy` has both a declaration and an execution
route:

| Submitted construct | Declaration | Execution route |
|---|---|---|
| `Module`, statement sequence | `syntax.k:61`, `core.k:124-127` | load and left-to-right sequencing |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` creates the exact closure |
| `Assign`, `Name` | `syntax.k:12,41` | strict RHS, `controls.k:9-18`, lookup in `core.k:129-154` |
| `ListExpr` | `syntax.k:17` | argument/element fold and fresh allocation in `list.k:12-15`, `core.k:117-121` |
| `For` | `syntax.k:45` | `controls.k:62-74`, list/proof-local iterator rules |
| `If` | `syntax.k:49` | `controls.k:50-54` |
| `Compare`, `CmpOp`, `Int` | `syntax.k:9,30,32` | `operators.k:14-17`, `int.k:22-27`, literal rule `core.k:194` |
| `Attribute`, `Call` | `syntax.k:28-29` | `call.k:15-24`; `append` state change in `list.k:52-55` |
| `Expr` | `syntax.k:52` | evaluate for effect then discard in `controls.k:46-48` |
| `Return` | `syntax.k:50` | `functions.k:77-90` |

The resulting control path is: evaluate the closure and argument, bind `l`,
allocate the empty result at heap location 0, evaluate `l` once, repeatedly
obtain an integer, bind `x`, compare it with zero, conditionally execute the
real `append`, and finally return and pop the frame. The loop invariant's cell
footprint matches this path: `x` and the accumulator heap entry can change;
`l`, other scopes, other heap entries, counters, exception state, and the
arbitrary continuation are preserved.

### Proof-local extension inventory and decisions

| Extension | Class and complete decision |
|---|---|
| `getPositiveBody` macro/rule | Definitional macro. Exact translated submitted function body; no state or value is invented. Accepted. |
| `positiveLoopBody` macro/rule | Definitional macro. Exact real loop body. Accepted; the `> 1` mutation rejected the original theorem. |
| `intVals(IntSeq)` | Fresh input representation, not a result oracle. It influences iteration and therefore output. Accepted within the formal theorem; its bridge to ordinary Python/K lists is informal and causes a concern. |
| empty `intVals` iterator rule | Operational adapter for a fresh constructor. Matches any continuation but reads/writes only `<k>`, exactly like the fixed empty-list iterator rule. It does not preempt a fixed rule because `.IntSeq`, `iCons`, and `vCons`/`.ValSeq` heads are disjoint. Accepted. |
| nonempty `intVals` iterator rule | Operational adapter. Yields exactly head `I` and tail `intVals(IS)`, preserves every cell, has no abrupt control effect, and is disjoint from all fixed iterator rules. Accepted, subject to the same representation bridge limitation. |
| `filterPositive` declaration and base rule | Definitional mathematical summary. Empty remainder returns the accumulator. Accepted. |
| `filterPositive` recursive rule | Definitional summary. Uses exactly the same `I >Int 0` predicate as execution and descends structurally on `IS`. Accepted. |
| `filterPositiveBranch` declaration and two rules | `[function,total]`; `Bool` is exhausted by disjoint `true` and `false` rules. The true case appends exactly one `I` at the right, the false case preserves the accumulator, and both descend through `filterPositive`. Accepted. |

There are no proof-local priorities, simplification rules, opaque functions,
or `[functional]` declarations. The only proof-local `[total]` function has
complete and nonoverlapping Boolean coverage. `filterPositive` has
constructor-complete `IntSeq` coverage and structural descent. The iterator
rules do not overlap the supplied ordinary-list rules. No extension replaces a
program-defined helper or fabricates a result.

### Supplied opaque and total symbols

The selected supplied semantics declares these `symbol(...)` boundaries:

- sorting/digest: `sortVS`, `sortKeyVS`, `md5hexCodes`;
- float/conversion: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`.

The exact declarations are listed in `evidence/09_static_checks.log`. None is
reachable from this integer filter program or appears in either claim or
summary, so none affects control, state, result, or claim closure.

The LLVM compiler warned that `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt` have non-exhaustive matches despite totality
declarations. These are unchanged supplied-semantics declarations and none is
on the proof path. The warnings expose limitations of the wider supplied
language subset, not a false rule used to prove this theorem. No rule in those
modules is labeled unsound here because there is no false conclusion witness
for this proof domain.

No materially unsound proof-local or used supplied rule was found. Therefore
there is no false-conclusion witness to report. The two narrower evidence gaps
are the absent universal `intVals`/ordinary-list connection theorem and the
non-literal module-load entry bridge already stated in Stage 4.

Stage 5 result: PASS for formal soundness; intent-bridge concerns remain.

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`.

The reviewer-created `/tmp/audit-work/30-get-positive/spec-vacuity.k` retains
the real entry and the already independently proved loop lemma but changes the
result obligation to append `0` to every filtered result:

```text
list(valSeqConcat(
  filterPositive(.ValSeq, INPUT),
  vCons(0, .ValSeq)))
```

This is demonstrably false for the satisfying input `INPUT = .IntSeq`: the
real and originally claimed output is `list(.ValSeq)`, while the mutation
demands `[0]`.

`kprove --dry-run` exited 0 and generated a 316-byte KORE claim, establishing
that the mutation parsed and built. The actual proof, with only the separately
proved loop claim staged as trusted, exited 1 with `WarnStuckClaimState`. Its
reachable residual shows:

- `<k> ref(0) ~> .K </k>`;
- heap `0 |-> list(.ValSeq)`; and
- path condition `INPUT #Equals .IntSeq`.

Thus it failed at the intended false result obligation, not from parsing,
imports, timeout, an unrelated crash, or unreachable code. The artifact,
commands, raw output, and checked wrapper are:

- `/tmp/audit-work/30-get-positive/spec-vacuity.k`
- `evidence/07_spec-vacuity.k` (preserved byte-identical copy)
- `evidence/07_non_vacuity.sh`
- `evidence/07_non_vacuity.raw.log`
- `evidence/07_non_vacuity.log`

As a separate body-sensitivity check, changing only the program predicate from
`I >Int 0` to `I >Int 1` while retaining the original positive-filter summary
built successfully and failed with a residual contrasting those predicates.
The mutated definition/spec are preserved as
`evidence/08_verification-body-mut.k` and `evidence/08_body-mut-spec.k`; see
`evidence/08_body_sensitivity.log`.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What is formally established

Under the selected supplied semantics and proof-local definitions, the
successful reachability proof establishes partial correctness:

For every finite `INPUT:IntSeq`, every terminating execution from the exact
seeded call configuration, calling the exact submitted `get_positive` body on
`list(intVals(INPUT))`, returns `ref(0)`, and heap location 0 contains the
elements of `INPUT` whose integer comparison with zero is true, in original
order with duplicates preserved. The loop claim establishes the corresponding
accumulator invariant for every finite suffix and every prefix sequence.

The proof does not establish total correctness/termination as a separately
stated theorem, behavior for non-integer elements, Python exception behavior
outside the modeled path, or a universal theorem about an actual
source-allocated list reference.

### Trust and evidence ledger

| Boundary | Dependents | Assessment and evidence |
|---|---|---|
| K toolchain/backend, SMT reasoning, and built-in Int/Bool/Map/List theories | Both claims | Necessary ordinary machine-checking trust. Fresh v7.1.337 build and proof outputs are preserved. |
| Byte-identical supplied semantics | All execution steps | Authorized fixed semantics boundary. Recursively verified; used rules statically reviewed. Wider unused gaps are disclosed. |
| Exact body macro and manually seeded closure | Entry and loop claims | Not opaque and body-sensitive. Exact AST correspondence, trusted translation, concrete module load, and failed body mutation support it. Candidate lacks a separate load-to-entry reachability theorem, so this remains a documented bridge concern. |
| `intVals` input representation and iterator rules | Loop control and returned elements | Rules are exhaustive, disjoint, value-fixing, and preserve state; no wrong branch or result is admitted inside the formal domain. The universal connection to ordinary source lists is informal rather than machine-checked, so the natural-language conclusion is conditional on this representation interpretation. |
| `filterPositive` / `filterPositiveBranch` | Final heap postcondition | Fully defined recursive mathematics, with the same predicate and append order as execution. Acceptable definitional summary, not an assumption or oracle. |
| Canonical-to-natural-language interpretation | Intent adequacy | Canonical comprehension directly expresses the prompt. Differential testing supports the submitted implementation bridge on 4,917 cases but is finite evidence only. |
| Supplied opaque symbols listed in Stage 5 | None | Inert for this proof; no claim depends on their interpretation. |
| Missing generation logs/metrics/trace | Audit provenance only | Prevents auditing the generation narrative, but does not weaken the fresh machine reconstruction itself. |

The proof is therefore formally sound and non-vacuous in its stated integer
`intVals` domain, and it executes an exact copy of the submitted function body.
Its two main bridges—synthetic input representation and manually seeded
closure—are transparent and supported, not answer-encoding oracles. Together
with the integer-only formal domain and missing generation records, they
constitute limitations sufficient for `CONCERNS / LEGIT`, but not a basis for
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
