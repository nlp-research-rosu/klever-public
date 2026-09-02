# Independent adversarial review: 18-how-many-times

The candidate contains a legitimate partial-correctness proof, but its
`VALIDATED` label is too strong. Fresh reconstruction closes the real entry
proof and the proof pins the submitted program. I found no false semantic or
proof-local rule. The concern is narrower: the proof critically accelerates the
fixed `buildIS` slice computation with a proof-local simplification, while the
candidate's bridge-free universal connection claim does not close. The equation
has a complete ordinary mathematical justification and survived independent
fixed-semantics ground/opposite-result checks, so this is a non-fatal
trust-boundary limitation rather than an unsoundness or substituted-program
finding.

## 1. Input and provenance integrity

The launcher declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, condition `kit-semantics`, and problem
`18-how-many-times`. The trusted `/reference/reference-semantics` mount is
present, as this mode requires.

I used the container paths in `/audit-input.json`, not the host provenance
paths. All launcher-required records are present, readable regular files, and
not symlinks:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the JSONL file under `/generation-evidence/codex-trace/`.

The campaign block in `/audit-input.json` equals
`/audit-campaign-lock.json`, and the lock's actual SHA-256 equals the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded direct file hash checked by the reviewer matches. The
structured trace artifact also matches the per-file hash in
`/generation-result.json`; all 442 JSONL events parsed, with zero malformed
events. The complete untrusted output log (1,337,498 bytes and 39,092 lines)
was read and summarized. These generation records claim prior success but were
not used as proof evidence.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Recursive
`diff -qr --no-dereference` between the candidate and trusted semantics trees
exits 0. Both have the same 25-entry reviewer manifest digest
`a68c92da30659ef48463705583dacee8ec648296a94fdc96a5028f4813773530`;
there are no missing, additional, changed, mistyped, special, or symlinked
semantics entries. No mounted candidate/reference/generation input contains a
symlink. The independent candidate-tree manifest covered 799 entries and has
reviewer digest
`a71f653d5bc10e24c642ed9412bc217158e75f195745e8fecd591fc0e6c23f66`.

Evidence and exact commands:

- [integrity script](evidence/01_integrity.sh) and
  [integrity log](evidence/01_integrity.log);
- [generation inspection script](evidence/01_generation_inspect.py) and
  [generation inspection log](evidence/01_generation_inspect.log).

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for two Python strings, return the number of starting
positions at which `substring` occurs contiguously in `string`, counting
overlapping occurrences. The examples require `("", "a") = 0`,
`("aaa", "a") = 3`, and `("aaaa", "aa") = 3`. The trusted canonical loop
also fixes the boundary behavior: an empty pattern occurs at all
`len(string) + 1` boundaries, and a pattern longer than the source occurs zero
times.

The candidate implements a different but equivalent scan. For a nonempty
pattern, it tests `startswith` at each nonempty successive suffix; testing
suffixes shorter than the pattern contributes zero. It handles the empty
pattern explicitly with `len(string) + 1`.

Running the trusted translator on the scratch copy of `solution.py` produced
SHA-256
`403f1076780caef08d26666444c0a88884b3401aa311c839c3d22821228ce707`,
identical to the submitted `solution.mpy`; `cmp` exits 0.

The independent differential test imports the trusted canonical entry point and
the candidate entry point. It covers the documented examples; empty
source/pattern; exact, absent, overlapping, shifted, and longer-pattern
boundaries; NUL, newline, composed/non-composed Unicode, and astral characters;
all source lengths 0–5 and pattern lengths 0–4 over `{"a","b","🙂"}`; and
2,000 deterministic random pairs over a broader alphabet. The final scope is
46,011 unique pairs with zero mismatches.

Evidence:

- [differential script](evidence/02_differential.py);
- [translator/differential command script](evidence/02_program_fidelity.sh);
- [program-fidelity log](evidence/02_program_fidelity.log).

## 3. Clean proof reconstruction

All sources needed for execution were copied to
`/tmp/audit-work/review/candidate-src`. Candidate-provided `*-kompiled`
directories, caches, traces, and old `#Top` files were not copied or used.

Fresh K 7.1.293 results:

1. LLVM build from
   `reference-semantics/semantics.k`, main module `MPY-KRUN`, syntax module
   `MPY-SYNTAX`: exit 0
   ([command](evidence/03_build_runtime.sh),
   [log](evidence/03_build_runtime.log)).
2. The reviewer-authored concrete program was translated with the trusted
   translator and run with the fresh definition: exit 0. Its ten results are
   `0, 1, 1, 0, 3, 3, 3, 2, 0, 4` for the recorded empty, exact, longer,
   overlapping, shifted, absent, and empty-pattern cases
   ([input Python](evidence/03_concrete_cases.py),
   [input MPY](evidence/03_concrete_cases.mpy),
   [command/log](evidence/03_run_concrete.log)).
3. Haskell build from `verification.k`, main module `VERIFICATION`, syntax
   module `MPY-SYNTAX`: exit 0
   ([command](evidence/03_build_proof.sh),
   [log](evidence/03_build_proof.log)).
4. Focused `SPEC.loop-inv`: exit 0 and exact `#Top`
   ([command](evidence/03_prove_loop.sh),
   [log](evidence/03_prove_loop.log)).
5. Full `SPEC`, which proves both the loop circularity and target entry claim:
   exit 0 and exact `#Top`
   ([command](evidence/03_prove_all.sh),
   [log](evidence/03_prove_all.log)).

The build warnings concern unrelated nonexhaustive helpers in the concrete
definition and unused variables in `strLt`; none is on this program's proof
path.

I also rebuilt plain `MPY` without `verification.k` and reran the candidate's
bridge-free `slice-tail` claim. The definition build exits 0, but `kprove`
exits 1 with `WarnStuckClaimState`; the residual is the symbolic `buildIS`
term. This is not a positive target claim and does not refute the slice
equation, but it confirms that the candidate did not machine-establish the
connection from the fixed rules
([command/log](evidence/03_bridge_free_slice.log)).

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`SPEC.loop-inv` assumes a nonempty pattern and a scope whose only local
bindings are remaining string `str(S)`, fixed substring `str(P)`, and current
integer count `C`. Starting at the exact submitted `#while` term, it preserves
the arbitrary continuation and outer configuration, empties `string`, and
changes `count` to `C + overlapCount(S,P)`.

`SPEC.target` has no additional requires-clause. For arbitrary
`S,P:IntSeq`, it starts from an exact module configuration binding
`how_many_times` to the candidate closure, with the builtins scope, empty
heap/stack, normal return/exception/exit state, and calls it with
`str(S), str(P)`. If the call terminates, the returned integer `?R` must satisfy
the equality `?R ==Int overlapCount(S,P)`. The result is not free, tautological,
or constrained by only a one-way implication.

### Mechanical program pinning

The reviewer script parses balanced constructor applications from
`solution.mpy` and the target claim. It checks the `"how_many_times"` binding,
the two parameter names, closure environment 0, and the complete body
constructor term. After deleting only the explicit `.Stmts` list identity that
the translator omits in empty branches, both normalized bodies have length 391
and are identical. All checks pass
([script](evidence/04_pinning_check.py),
[log](evidence/04_adequacy.log)).

This body executes through fixed name lookup, argument evaluation and binding,
conditionals, `len`, `startswith`, integer addition, slicing, assignment,
while control, return, frame pop, scope removal, and restoration of all fixed
cells. There is no program-call interception rule.

### Satisfying witnesses and substitution

The exact target state is satisfiable, for example with
`S = "aaaa"` and `P = "aa"` encoded as `IntSeq`; the formal summary,
canonical implementation, and candidate implementation all return 3. For
`("abc","")` all three return 4, and for `("","a")` all three return 0.

The loop precondition is satisfiable with `L=1`, `PAR=parent(0)`,
`string="aa"`, `substring="a"`, and `count=5`; its post-state has empty
`string` and count 7. These substitutions are recorded in
[the witness script](evidence/04_claim_witnesses.py) and
[adequacy log](evidence/04_adequacy.log).

An independent body-sensitivity mutation changes the constructor term actually
executed by the closure from `string[1:]` to `string[2:]`; it does not merely
edit an external source file. The mutated program returns 2 on
`("aaaa","aa")`, and the original obligation demanding 3 is rejected with that
residual. The mutation dry-run exits 0 and its proof exits 1 for the expected
reason
([mutation](evidence/05_audit_spec_body_slice_mutation.k),
[command/log](evidence/05_body_sensitivity.log)).

The formal domain contains all semantic `str(IntSeq)` values and therefore does
not narrow the HumanEval string domain. It overapproximates valid Python Unicode
code-point sequences with arbitrary K integers; the used operations are only
equality, prefix, length, and suffix. This over-breadth does not make a false
conclusion about intended Python strings.

## 5. Rule-by-rule static soundness review

The source-level inventory enumerates every local import, module,
configuration, syntax declaration, context, rule, attribute, and claim in the
supplied tree, `verification.k`, `spec.k`, and `slice-lemma-spec.k`. It records
701 rules, 229 syntax declarations, 45 priority rules, 109 `total`
declarations, 22 explicit `no-evaluators` declarations, and exactly one
`simplification` rule. See
[inventory generator](evidence/05_inventory.py) and
[complete inventory](evidence/05_rule_inventory.log).

### Exhaustive file disposition

The following disposition applies to every rule listed for each file in the
inventory. The candidate copy is byte-identical to the selected supplied
semantics, so these are fixed-semantic rules rather than candidate extensions.

| Source | Rules | Disposition in this proof |
|---|---:|---|
| `assert.k` | 3 | Unreachable; no `Assert`. |
| `bool.k` | 13 | No `BoolOp`/boolean comparison; unreachable except K's imported ordinary Bool operations. |
| `builtins.k` | 137 | Only `len -> seqLen -> isLen` is reachable; it is exact for `str(IntSeq)`. Other builtins are unreachable. |
| `call.k` | 21 | Generic callee-first route, left-to-right argument evaluation, bound-method/builtin dispatch, and ordinary closure frame creation are reachable and faithful. Heap-reference/annotated-closure branches are unreachable. |
| `comprehension.k` | 7 | Unreachable. |
| `concrete.k` | 16 | Imported only by `MPY-KRUN`, not the proof module `MPY`; used only for independent concrete execution and irrelevant to proof closure. |
| `controls.k` | 34 | Ordinary `Assign`, integer `AugAssign`, `If`, and `While/#whileCond/#loopLbl` rules are reachable and match the source. Imports, for-loops, break/continue, reference branches are unreachable. |
| `core.k` | 46 | Configuration, algebraic sequences/values, scope lookup, builtins scope, statement sequencing, argument evaluation, literals, truthiness, and length helpers are reachable and coherent. Allocation/cell rules are unreachable. |
| `dict.k` | 28 | Unreachable. |
| `float.k` | 121 | Unreachable. |
| `functions.k` | 15 | Parameter binding, return, `#endcall`, and `#pop` are reachable. They restore env/ret/scopeLoc/stack and remove the callee scope. Closure-cell variants are unreachable. |
| `int.k` | 16 | Integer `+` and `==`/`!=` dispatch used by the body/guards are ordinary unbounded integer operations. Other arithmetic is unreachable. |
| `iter.k` | 0 | Declaration only; iterator protocol unreachable. |
| `list.k` | 27 | Program-level list operations unreachable. The configuration stack uses the K builtin List independently. |
| `methods.k` | 75 | Only string `startswith` routing and its three exhaustive `startsWith` equations are reachable. They compare the requested prefix with the receiver in the correct argument order. |
| `operators.k` | 10 | Comparison/BinOp evaluation contexts and generic dispatch are reachable and enforce the intended evaluation order. Reference priorities are unreachable. |
| `range.k` | 6 | Unreachable. |
| `set.k` | 12 | Unreachable. |
| `sort.k` | 19 | Unreachable, including its opaque sort symbols. |
| `str.k` | 28 | Empty literal loading, string equality/inequality, and their algebraic sequence comparisons are reachable and faithful. Other string operators are unreachable. |
| `subscript.k` | 40 | Bound evaluation, positive-step defaults, `slAdjust/clampHi`, string `doSlice`, `buildIS`, and in-bounds `intSeqAt` are reachable. The program's `[1:]` always uses indices in range. Indexing, negative steps, and list/tuple paths are otherwise unreachable. |
| `syntax.k` | 0 | Sixteen syntax declarations include every constructor used by `solution.mpy`; strict/seqstrict attributes supply RHS/operand evaluation. |
| `tuple.k` | 21 | Unreachable. |

All 22 fixed opaque/no-evaluator symbols and all fixed sort/float/MD5
abstractions are unreachable from the submitted constructor term. None can
influence its branches, state, exceptions, or result. The candidate adds no
opaque symbol and no priority rule.

### Material construct-to-rule map

- `Call`, `Name`, argument order, closure binding and return:
  `core.k:131-154,183-191`, `call.k:16-32,69-75`,
  `functions.k:63-66,78-90`.
- `If`, `While`, assignment, augmented assignment:
  `controls.k:9-31,51-54,65-82,85`.
- `Compare`, `BinOp`, integer `+`, string `==`/`!=`:
  `operators.k:10-17`, `int.k:9-27`, `str.k:14-17,24-26`.
- `len`: `builtins.k:17-26` and `core.k:227-229`.
- `Attribute`/`startswith`: `call.k:16,20-24`,
  `methods.k:61,166-169`.
- `[1:]`: `subscript.k:27-29,49-69,72-106,116-121`.

These rules preserve callee binding, left-to-right evaluation, current-scope
writes, loop continuation, return control, stack frame, exception/exit state,
and heap/scope allocation. No overlap or priority can route a string receiver
through the irrelevant reference/list branches.

### The six proof-local rules

1. `tailIS(.IntSeq) => .IntSeq`: true.
2. `tailIS(iCons(_,CS)) => CS`: true. Together these rules are disjoint,
   exhaustive, and terminating for every `IntSeq`, validating `[total]`.
3. Empty-pattern `overlapCount(S,.IntSeq) => isLen(S)+1`: exactly the
   canonical boundary count.
4. Empty-source/nonempty-pattern `overlapCount(.IntSeq,P) => 0`: true.
5. Nonempty/nonempty recursive `overlapCount`: adds one exactly when
   `startsWith(P,S)` and recurses on `tailIS(S)`. The three summary cases are
   pairwise disjoint, exhaustive, and the recursion strictly decreases source
   length, validating `[total]`.
6. The simplification
   `buildIS(S,clampHi(1,isLen(S),1),isLen(S),1) => tailIS(S)` for nonempty
   `S`: true, but not universally machine-connected in the candidate.

For rule 6, let `n=isLen(S)`. Nonemptiness gives `n>=1`.
`clampHi(1,n,1)=1` both when `n=1` and when `n>1`. The fixed `buildIS`
equations then select exactly the in-bounds indices `1,...,n-1`; by induction
on the number of remaining indices, `intSeqAt` yields precisely the constructor
tail, and the base case accesses no out-of-bounds index. Thus the equation is
valid over its complete guard and agrees with the fixed equations on every
overlap. It has no cell footprint, allocation, exception, or abrupt control
effect, but its value determines the next loop suffix and therefore the result.

Under the Kit behavioral classification, rule 6 is an operational acceleration
of a fixed-semantics helper, not merely a harmless name. The bridge-free
universal claim remains stuck, so the strict machine-connection evidence is
missing. Independent fixed-semantics ground claims for source lengths 1, 2,
and 4 print `#Top`, while the deliberately wrong claim that `[97,98][1:]` is
empty exits 1 with residual `[98]`
([claims and log](evidence/05_slice_ground_checks.log)). These finite checks do
not replace the universal theorem. I found no false-conclusion witness because
the rule is mathematically true; accordingly I record an evidence/trust
limitation, not an unsoundness.

The loop claim is a coinductive auxiliary claim over the exact real `#while`
term. It accepts an arbitrary continuation, but its proof is equally quantified
over that continuation, and the loop body contains no return, break, exception,
cleanup, or frame pop. Its one-step state footprint is exactly the local
`string` and `count` updates represented in its post-state.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation uses the
satisfying input `("ababa","aba")`, whose formal summary, canonical result, and
candidate result are 2, and changes the result-constraining target to demand 3.
It executes the actual closure constructor term.

`kprove --dry-run` exits 0, establishing that the mutation parses and builds.
The actual proof exits 1 with `WarnStuckClaimState` and residual
`<k> 2 ~> .K </k>`. The script verifies both markers and exits 0 only after
observing the intended rejection.

Evidence:

- [fresh mutation](evidence/06_audit_spec_vacuity.k);
- [command script](evidence/06_nonvacuity.sh);
- [complete bounded log](evidence/06_nonvacuity.log).

This is meaningful non-vacuity evidence: the precondition is satisfiable, the
mutated obligation is false, the relevant call executes, and the failure is the
expected unmet result rather than a parser error, missing import, timeout, or
unrelated crash.

## 7. Proven versus assumed accounting

### What is formally established

Under the supplied `MPY` theory plus the six audited rules in
`verification.k`, the exact submitted `how_many_times` closure has this partial
correctness property:

> For every semantic source `str(S)` and pattern `str(P)`, if the call
> terminates from the target configuration, it returns
> `overlapCount(S,P)`.

The coinductive loop claim establishes the corresponding accumulated-count
invariant for every nonempty pattern. The recursive definition of
`overlapCount` is the requested count of overlapping starting positions,
including `n+1` boundaries for the empty pattern.

The proof does not establish termination. Termination is informally evident
for finite `IntSeq`: on the nonempty-pattern branch the loop replaces a
nonempty source with its strict tail. This omission is immaterial because the
requested theorem is partial correctness.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied, integrity-checked `MPY` semantics | Entire execution theorem | Authorized selected semantics. Material used rules were reviewed above; unused rules/opaque symbols cannot match the program. |
| Trusted `py2mpy.py` translation | Program identity | Acceptable: fresh regeneration is byte-identical, then constructor-level pinning independently matches the claim. |
| K 7.1.293 parser/compiler, Haskell/LLVM backends, SMT/builtin Int/Map/List machinery | Build, concrete run, symbolic closure | Standard unavoidable toolchain trust. |
| Proof-local `tailIS` and `overlapCount` definitions | Loop and target postconditions | Acceptable ordinary mathematics: complete, disjoint, terminating equations, with concrete substitutions and differential support. |
| Proof-local `[1:]` simplification | Loop step and target result | Concerning but not illegitimate: complete mathematical derivation and fixed ground/opposite checks support it, but no bridge-free universal K theorem closes. |
| Interpretation of `overlapCount` as the HumanEval result | Human-facing contract | Acceptable ordinary induction over starting suffixes; 46,011 independent Python differential cases support but do not prove this bridge. |
| Python Unicode versus semantic `IntSeq` | Source-domain adequacy | Non-fatal overapproximation. Symbolic inputs bypass the ASCII-only literal loader; intended Python strings are included and only code-point equality/prefix/length/suffix are used. |

No external or opaque result oracle, empirical replacement of program-defined
code, answer-encoding call rewrite, free result symbol, bounded input
precondition, or finite unrolling contributes to closure. The proof covers the
unrestricted typed string domain rather than finitely many sizes.

The positive `#Top` results, differential tests, and mutation results are kept
in their proper roles: only `kprove` establishes reachability under the stated
theory; testing supports program/summary bridges; and the static audit decides
whether the extra theory is honest.

### Decision

The proof reconstructs, is result-constraining and non-vacuous, pins the real
generated body, and covers the full HumanEval string contract. No candidate
rule enables a demonstrated false conclusion. It is therefore legitimate.
It is not a clean `PASS`, because the result-bearing slice acceleration lacks
the universal bridge-free machine theorem required for the candidate's claimed
`VALIDATED` strength. Under the benchmark decision boundary, that is a
documented non-fatal trust/evidence limitation.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
