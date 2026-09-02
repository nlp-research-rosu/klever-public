# Independent adversarial audit: 37-sort-even

This audit used the required `/kit-skills/using-kit` and
`/kit-skills/validating-proof` workflows. It treats all candidate and generation
records as untrusted claims. All executable work was reconstructed below
`/tmp/audit-work/37-sort-even`; reviewer scripts and bounded logs are preserved
in `/audit-output/evidence/`.

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program. The final status is `CONCERNS / LEGIT`, not
`PASS`, because two proof-audit boundaries remain conditional or less
machine-auditable than ideal:

1. the fixed supplied semantics deliberately leaves `sortVS` opaque during
   symbolic proof, so the human-facing “ascending permutation” conclusion
   depends on that named primitive contract and finite differential evidence;
2. the candidate's specialized singleton `#bindP` rule is mechanically an exact
   two-step instance of fixed rules, and fixed concrete execution exercises it,
   but a bridge-free universal `kprove` attempt gets stuck on the Haskell
   narrowing ambiguity that motivated the specialization.

Neither issue narrows the formal entry precondition, substitutes another
program, frees the result, or supplies a false target conclusion witness.

## 1. Input and provenance integrity

### Gate result: PASS

`/audit-input.json` declares:

- problem `37-sort-even`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`.

The trusted `/reference/reference-semantics` tree is present, as this rendered
mode requires. The launcher-owned inputs and all records required by
`legacy-selected-stage1` are readable regular files/directories and are not
symlinks. `usage.json` is present and was inspected. Historical runtime metrics
were not required and were not reconstructed.

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` exactly. The lock's independently computed SHA-256
is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded hash.

Independent hashes match every recorded file hash checked:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `invocation.json`, `metrics.json`, `usage.json`, `prompt.txt`;
- `codex-last.txt`, `codex-output.log`, and the structured trace file;
- trusted canonical, prompt, and translator;
- candidate prompt and translator.

The complete 785,006-byte generation log was read and hashed. The complete
708,117-byte structured trace was read; all 346 JSONL events parse, including 69
tool calls. These records were used only to inventory the generation claims.
They were not accepted as proof evidence.

The candidate prompt and translator are byte-identical to their trusted mounts.
A recursive, type-sensitive manifest comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` found the same directory and 24 files with the
same bytes. Neither tree contains a symlink, missing entry, additional entry, or
type mismatch. The auditor-defined tree digest for both is
`bda538d8ff7bdad4388aba62366f2fbd3120d4802726644dbf6e6cc22ac9b39f`.

Evidence:

- [provenance checker](/audit-output/evidence/provenance_audit.py)
- [complete bounded provenance report](/audit-output/evidence/01-provenance.log)
- [scratch preparation record](/audit-output/evidence/02-prepare-scratch.log)

No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Gate result: PASS

### Source contract

The trusted prompt says that `sort_even(l)` returns a list with:

- every odd-index value unchanged at the same index; and
- the multiset of even-index values placed at the even indices in ascending
  order.

The examples require:

- `[1, 2, 3] -> [1, 2, 3]`;
- `[5, 6, 3, 4] -> [3, 6, 5, 4]`.

The natural executable domain is finite Python lists for which sorting the
even-index subsequence is defined. The HumanEval examples and differential
suite here use integers. The formal K entry claim itself does not impose an
integer or size bound: its input is arbitrary `VS:ValSeq`.

### Implementation comparison

The canonical implementation slices evens and odds, sorts evens in place,
interleaves `zip(evens, odds)`, and appends a final even when necessary. The
candidate uses `sorted(l[::2])`, loops over the odd slice, appends one sorted
even and the current odd, then concatenates the unused even suffix. These are
extensionally equivalent on the contract domain, including empty and odd-length
lists. Neither implementation mutates `l`.

Running the trusted translator from the scratch copy regenerated
`solution.mpy` with SHA-256
`fd4ff5d27b4f28364c69a9794290cfa53b00c3040f3fc10c09c26daeac68659c`.
It is byte-identical to the submitted `solution.mpy`.

The independent differential script imports the trusted canonical entry point
and generated entry point by path. It records every input and both results. It
exercised 4,918 cases:

- 12 hand cases covering the two prompt examples, empty, singleton, loop-zero,
  even/odd length, duplicates, negatives, already/reverse-sorted evens, and
  arbitrary-size integers;
- all 3,906 lists of lengths 0 through 5 over
  `{-2, -1, 0, 1, 2}`;
- 1,000 deterministic generated lists of lengths 0 through 64 with values in
  `[-10^12, 10^12]`.

There were zero mismatches and zero input mutations.

Evidence:

- [fidelity commands and statuses](/audit-output/evidence/02-fidelity.log)
- [independent differential script](/audit-output/evidence/differential_test.py)
- [all differential inputs and results](/audit-output/evidence/02-differential-results.jsonl)

## 3. Clean proof reconstruction

### Gate result: PASS

No candidate-built definition, cache, or `__pycache__` entry was copied.
Candidate source artifacts were copied explicitly. The supplied semantics,
canonical, prompt, and translator came from `/reference`.

The independently installed K toolchain is version `v7.1.293` for `kompile`,
`krun`, and `kprove`.

Fresh commands and results:

1. Concrete definition:

   `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled-fresh`

   Exit 0.

2. Independent K assertions:

   `krun audit-concrete-tests.mpy --definition runtime-kompiled-fresh --output pretty`

   Exit 0 with `.K`, `NoExc`, empty stack, `noRet`, and exit code 0. The eight
   assertion cases include the prompt examples and both loop/suffix boundaries.

3. Proof definition:

   `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX -I . --output-definition verification-kompiled-fresh`

   Exit 0.

4. Auxiliary loop claim:

   `kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC --claims SPEC.loop-correct --output pretty`

   Exit 0 and output `#Top`.

5. Entry claim using the separately closed loop claim:

   `kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC --claims SPEC.loop-correct,SPEC.sort-even-correct --trusted SPEC.loop-correct --output pretty`

   Exit 0 and output `#Top`.

The `--trusted` use in command 5 is theorem composition, not an unproved loop
assumption in this audit: command 4 independently closes the identical loop
claim from the identical fresh sources.

Evidence:

- [reconstruction summary](/audit-output/evidence/03-reconstruction-summary.log)
- [LLVM build](/audit-output/evidence/03-llvm-build.log)
- [concrete execution](/audit-output/evidence/03-concrete-krun.log)
- [Haskell build](/audit-output/evidence/03-haskell-build.log)
- [loop proof](/audit-output/evidence/03-prove-loop.log)
- [entry proof](/audit-output/evidence/03-prove-entry.log)

Compiler warnings about `mapStrVS`, several float helpers, and `joinCodes` concern
target-unused fixed-semantics functions. The material `valSeqAt` warning reflects
the supplied semantics' explicit total-but-underspecified treatment of
out-of-bounds indexing; the target's accesses are in-bounds under the named
`sortVS` ascending-permutation contract.

## 4. Adequacy and real-program pinning

### Gate result: PASS, with the trust qualifications in Stage 7

### Claims in plain language

`SPEC.loop-correct` has no explicit `requires`. Its start state is a loop head
whose current scope contains `l`, heap references for `evens`, `odds`, and
`result`, index `I`, and the current `odd`. The heap contains:

- all even values `EVS`;
- the original odd list `OALL`;
- accumulated output `ACC`.

For any remaining iterator sequence `OVS` and continuation `K`, the claim says
the loop resumes `K`, advances `i` by `len(OVS)`, leaves the even and odd heap
objects unchanged, and changes the result object to
`ACC ++ pairedVS(EVS, OVS, I)`. The final `odd` is existential, correctly
covering both empty and nonempty suffixes.

`SPEC.sort-even-correct` also has no `requires`. From an exact clean call state
with `sort_even` bound to the submitted closure and the fixed builtins scope, it
says:

`sort_even(list(VS))`

returns the structural list

`assembledEvenSort(sortVS(evenIndices(VS)), oddIndices(VS))`,

with stack, return state, exception state, and exit code restored. Fresh heap
addresses and unreachable allocations are existentially abstracted, but
`#observeResult` dereferences the returned list before matching the
postcondition, so the returned contents are not free.

### Program identity

The proof does not execute the full `Module(FuncDef(...))` text. It injects the
closure binding and body term. That is allowed only if the binding and body are
mechanically identical.

The reviewer parser:

- extracted the `FuncDef("sort_even", Params("l"), BODY)` constructor from
  regenerated `solution.mpy`;
- extracted `sortEvenBody` and `loopBody` right-hand sides from
  `verification.k`;
- expanded `loopBody`;
- normalized only the inert empty-list spelling
  `ListExpr()` versus `ListExpr(.Exprs)`;
- compared the normalized constructor trees.

All eight checks pass: function name, parameter, loop body, entire body, closure
rule, scope binding, entry call, and constrained postcondition. The complete
normalized body strings are retained in the log.

The claim's bare `list(VS)` argument omits source-level input-object allocation.
The fixed semantics expressly permits a bare list value for read-only claim
inputs. This function never mutates or identity-tests `l`; all constructed
lists allocate normally. Fresh fixed-semantics concrete runs with ordinary
allocated list arguments agree.

### Satisfiable witnesses

The entry precondition is satisfiable, for example with:

- `VS = .ValSeq` (empty list); or
- `VS = [5, 6, 3, 4]` encoded as a `vCons` sequence in the exact clean cells.

For `[5, 6, 3, 4]`, the formal summary components are:

- `evenIndices = [5, 3]`;
- `oddIndices = [6, 4]`;
- interpreting the named primitive contract,
  `sortVS(evenIndices) = [3, 5]`;
- `pairedVS = [3, 6, 5, 4]`;
- `evenSuffix = []`;
- result `[3, 6, 5, 4]`.

This equals both trusted canonical Python and generated Python. Empty,
singleton, and a seven-element duplicate/negative case also agree.

### Body sensitivity

A reviewer mutation changed only the actual executed body term from
`l[::2]` to `l[::3]`. The mutation built. The unchanged loop lemma still
closed. A generic symbolic mutant entry run was manually interrupted after
about four minutes and is explicitly not used as evidence.

The bounded ground replacement is decisive on input `[5, 6, 3, 4]`:

- the mutant's actual result obligation `[4, 6, 5, 4]` prints `#Top`;
- the original required result `[3, 6, 5, 4]` exits 1 with
  `WarnStuckClaimState`, showing the reached mutant result
  `[4, 6, 5, 4]`.

Thus a material body change changes the term and invalidates the original
obligation.

Evidence:

- [constructor and ground-summary checks](/audit-output/evidence/04-pinning.log)
- [constructor comparison source](/audit-output/evidence/constructor_compare.py)
- [body mutation diff](/audit-output/evidence/04-body-sensitivity.diff)
- [bounded mutant correct-result proof](/audit-output/evidence/04b-body-sensitivity-ground-correct.log)
- [bounded mutant rejected original result](/audit-output/evidence/04b-body-sensitivity-ground-wrong.log)
- [inconclusive universal-run note](/audit-output/evidence/04-body-sensitivity-universal-note.txt)

## 5. Rule-by-rule static soundness review

### Gate result: PASS, with one auditability concern

The source inventory contains 956 items:

- 236 syntax declarations;
- 712 rules;
- five contexts;
- one configuration;
- two claims.

Every item has an ID, source location, complete one-line source rendering,
attributes, target-materiality classification, and disposition in
[the exhaustive TSV inventory](/audit-output/evidence/05-rule-inventory.tsv).
Counts by file and disposition are in
[the inventory summary](/audit-output/evidence/05-rule-inventory-summary.log).

The supplied semantics accounts for 939 items. At the selected minimal-Python
semantics level:

- 139 fixed rules are target-material and accepted;
- 553 fixed rules are target-unused and do not contribute to claim closure;
- 199 fixed declarations, five contexts, and the configuration are accepted;
- 24 fixed opaque declarations are target-unused;
- five fixed non-exhaustive total declarations are target-unused;
- `valSeqAt` is the one material total-but-OOB-underspecified fixed primitive;
- `sortVS` is the one material named opaque fixed primitive.

This acceptance does not claim that the supplied language is full Python. The
unused rules are outside this target execution. No candidate rule imports or
activates a target-unused opaque result. Every material operation in the
submitted body has a declaration and execution path:

| Submitted construct | Fixed declarations/rules |
|---|---|
| `Call`, callee/argument order, closure frame | `syntax.k`, `core.k` argument loop, `call.k`, `functions.k` |
| names and builtins binding | `core.k` lookup and `builtinsScope` |
| `l[::2]`, `l[1::2]`, suffix slicing | `subscript.k` contexts, dereference, bound evaluation, `sl*`, `buildVS` |
| `sorted(...)` | `sort.k` allocation and `sortVS` |
| assignments and integer `i += 1` | `controls.k`, `operators.k`, `int.k` |
| list literal and list concatenation | `list.k`, `core.k` allocation |
| `for odd in odds` and target binding | `controls.k`, `iter.k`, `list.k`, `tuple.k` |
| `result.append(...)` | `call.k` attribute/bound-method routing and `list.k` heap update |
| `len(odds)` | `call.k`, `builtins.k`, `core.k` `vsLen` |
| `return` and frame restoration | `functions.k` |

Evaluation is left-to-right where material, the loop snapshots the sliced odds
object, append updates the result heap object, list concatenation allocates,
return pops the exact frame, and the entry claim constrains normal exception,
stack, return, and exit-code cells.

### Candidate declarations and rules

There are nine candidate syntax declarations and 17 candidate rules:

1. `loopBody`, `sortEvenBody`, and `sortEvenClosure` are constant,
   total definitional aliases. Mechanical constructor comparison establishes
   exactness.
2. `evenIndices` and `oddIndices` invoke the same fixed `slStart`, `slStop`,
   `slStep`, and `buildVS` functions used by execution.
3. The two `pairedVS` equations are disjoint, exhaustive on `ValSeq`, and
   recurse on the odd tail. They alternate the indexed even with the current
   odd.
4. The two `advancedIndex` equations are disjoint, exhaustive, and recurse on a
   strictly smaller sequence.
5. `evenSuffix` is exactly the fixed slice with start `len(odds)` and default
   stop/step.
6. `assembledEvenSort` concatenates `pairedVS` and `evenSuffix`.
7. `valSeqConcat(VS, .ValSeq) = VS` is right identity. Its overlap with the
   fixed left-identity equation agrees.
8. The reassociation
   `(A ++ B) ++ C = A ++ (B ++ C)` is list associativity, oriented to reduce
   left nesting. Its overlaps with identities agree.
9. Removing the five known non-`"$cells"` map entries from the membership query
   is true because K maps require distinct keys. It changes no operational
   state.
10. The two `#observeResult` rules are disjoint (`ref` versus `not isRefV`),
    preserve their continuation and heap, and merely define the structural
    observation inserted after the call.
11. The specialized singleton `#bindP` rule reads `env`, writes only the new
    current scope's empty map to `"l" |-> V`, preserves the arbitrary parent,
    continuation, surrounding scopes, and all other cells, and consumes the
    singleton binding.

### Specialized binder connection

The candidate binder preempts two fixed steps. Mechanical source matching gives
the universal substitution:

`P = "l", PS = .ParamNames, VS = .Vals, M = .Map`.

The fixed recursive binder produces:

- intermediate `#bindP(.ParamNames, .Vals)`;
- `.Map["l" <- V]`, whose map normal form is `"l" |-> V`.

The fixed empty binder then produces `.K`. This is exactly the candidate rule's
right-hand side and state update. The mechanical check passes all six source
conditions in
[the derivation log](/audit-output/evidence/05-bind-derivation.log).
Moreover, the fixed-only LLVM definition executes this binding repeatedly in
the independent concrete tests.

A fixed-only Haskell connection definition builds, but the attempted universal
reachability claim remains stuck at the binding redex. This is not a false
conclusion witness: the residual shows no divergent successor at all. It is the
known higher-priority closure-cell narrowing ambiguity that the exact
specialization avoids. The failed attempt is preserved in
[the connection proof log](/audit-output/evidence/05-bind-connection-proof.log).
Because the semantic equivalence is an exact two-rule source instance rather
than an unproved value oracle, this is an auditability concern, not an
illegitimate operational shortcut.

### Overlap, totality, opacity, and priorities

- Candidate function guards are constructor-disjoint or single-equation total.
- Candidate recursion structurally descends.
- Candidate simplification overlaps agree as described above.
- Candidate priority 30 on singleton binding selects the same fixed result;
  priority 40 on reference observation selects the reference-specific equation.
- No candidate `no-evaluators`, opaque value, oracle, or task-answer rewrite
  exists.
- The only result-bearing opaque target symbol is fixed `sortVS`.
- The loop claim is broader than reachable entry states, but remains sound in
  the supplied total-index model. The entry path is in-bounds under the
  `sortVS` permutation/length contract.

No rule is labeled unsound, because the audit found no concrete or symbolic
false target conclusion witness enabled by any candidate rule.

## 6. Fresh non-vacuity test

### Gate result: PASS

There was no candidate `spec-vacuity.k` to rely on. The reviewer created a
fresh ground entry claim against the unmodified body and fresh proof definition.
The exact initial state uses the satisfying input `[5, 6, 3, 4]`. Its
destination was deliberately changed from the real `[3, 6, 5, 4]` to false
`[4, 6, 5, 4]`.

The dry run parses and builds the mutation with exit 0. The actual proof exits
1 with `WarnStuckClaimState`; the residual has normal control state and shows
the reached structural result `[3, 6, 5, 4]`, which does not unify with the
false destination. It did not fail from parsing, imports, timeout, or an
unreachable mutation.

Evidence:

- [fresh mutation source](/audit-output/evidence/06-spec-vacuity.k)
- [mutation summary](/audit-output/evidence/06-nonvacuity-summary.log)
- [successful dry run](/audit-output/evidence/06-nonvacuity-dry-run.log)
- [expected semantic failure](/audit-output/evidence/06-nonvacuity-proof.log)

## 7. Proven versus assumed accounting

### Precisely proven

Under the fresh supplied MPY semantics plus the reviewed candidate definitions,
for every `VS:ValSeq`, if the exact entry call terminates normally, executing
the constructor body mechanically equal to submitted `solution.mpy` returns:

`assembledEvenSort(sortVS(evenIndices(VS)), oddIndices(VS))`.

The proof establishes the loop's alternating append behavior, index advance,
even suffix, normal call/return control, result observation, and restoration of
stack/return/exception/exit state. It is unrestricted in list length; it is not
a finite unrolling or examples-only theorem.

### Assumptions and trust ledger

| Boundary | Influence | Dependents | Judgment/evidence |
|---|---|---|---|
| K 7.1.293 compiler and Haskell/LLVM backends | All parsing, execution, and proof closure | All claims | Standard toolchain trust; fresh builds and both positive `#Top` runs recorded |
| K built-in Int/Bool/String/Map/List theories | Arithmetic, maps, sequence encodings | Fixed semantics and summaries | Standard low-level mathematical/runtime trust |
| Trusted `py2mpy.py` | Python AST to submitted constructor term | Program identity | Candidate translator matches trusted bytes; trusted regeneration is byte-identical |
| Supplied MPY operational semantics | All modeled Python execution | Entry and loop claims | Integrity is exact; material rules were statically mapped and concretely exercised |
| `sortVS(ValSeq)` contract | Sorted-even value, permutation, and length | Entry result, loop in-bounds interpretation, natural-language sortedness | Fixed external builtin primitive, intentionally opaque in symbolic proof; concrete insertion rules and 4,918 integer Python differential cases support it, but finite tests are not a universal theorem |
| `valSeqAt` total OOB behavior | Indexing an opaque sorted sequence | `pairedVS` and loop | Fixed selected-semantics boundary; intended entry accesses are in-bounds conditional on `sortVS` preserving length |
| Bare structural input list | Omits allocation/identity of `l` at claim boundary | Entry-call bridge | Acceptable here because `l` is read-only and never identity-tested; allocated-list concrete runs agree |
| Separately trusted loop claim in entry command | Loop summarization | Entry `#Top` | The identical loop claim independently printed `#Top` first |
| Specialized singleton binder | Function parameter binding/control | Entry proof | Exact two-step fixed-rule source instance; fixed concrete execution passes; bridge-free universal Haskell attempt is stuck, creating the stated auditability concern |

### Why the remaining concerns are not a failure

`sortVS` is a fixed external builtin primitive, not program-defined code and
not a candidate task-answer oracle. The theorem is interpretation-parametric in
that symbol, and the ascending-permutation conclusion is explicitly conditional
on its named contract. No source-contract size restriction was introduced.

The singleton binder does not fabricate or constrain a program-derived result.
It composes two existing fixed rules with a constructor substitution and has the
same binding, continuation, parent, and state footprint. The failed universal
connection attempt exhibits prover incompleteness at the original redex, not a
different behavior or false conclusion.

Differential tests, ground witnesses, and traces are not treated as substitutes
for the reachability proof. They support only source/canonical equivalence,
concrete fixed-semantics behavior, and the named primitive bridge.

Accordingly, the proof is sound and pins the real generated program. The opaque
sorting contract and binder connection auditability prevent the stronger
no-reservation `PASS`, but they do not make the candidate non-legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
