# Independent adversarial review: 70-strange-sort-list

The candidate contains a real, non-vacuous K proof of a finite collection of
small-list cases, but it does not prove the unrestricted HumanEval contract.
The formal claims quantify over all integer values only at exact list lengths
0 through 4, then add two concrete length-5 examples. This material narrowing
is a benchmark-level legitimacy failure even though the submitted `kprove`
invocation reconstructs to `#Top`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. This agrees with the task and run
manifests. The generated-semantics boundary is internally consistent:
`/reference/reference-semantics` is absent.

I inspected all records required for this layout:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- all 200 JSONL records in the structured trace below
  `/generation-evidence/codex-trace/`.

All required mounts and candidate source artifacts are real files or
directories; there are no symlinks below the candidate, reference, or
generation-evidence trees. The candidate, generation evidence, and trusted
reference mounts report read-only mount options. See
[01_mount_integrity.log](/audit-output/evidence/01_mount_integrity.log).

The object in `/audit-campaign-lock.json` exactly equals the `audit_campaign`
block in `/audit-input.json`. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded hash. The rendered audit prompt also hashes to the
campaign's recorded prompt hash.

All reproducible file hashes in `/audit-input.json` match their mounted bytes,
including the trusted canonical, prompt and translator; run/task/result and
invocation manifests; generation prompt, metrics, usage, final response, and
full output log. The trace JSONL file hashes to
`6de547d81a6afcfb851a79533c0ed0ad4ea9928b0627bacc2953b6abb9a274ac`,
matching both generation manifests. An independent schema-v2 tree digest of
the complete candidate is
`eeea2c3fb04b6bc6446e019497215ff4687551264a60acc18524d9731480d7de`,
matching the invocation's input, retained-workspace, and result workspace
hashes. The analogous trace tree digest matches `usage.json`. The launcher
also records separate aggregate mount digests without specifying their
serialization; the independent file-level and schema-v2 tree checks bind every
mounted entry. Full results are in
[01_provenance.log](/audit-output/evidence/01_provenance.log). An initial
reviewer check incorrectly expected the audit manifest's added `config` field
to occur in `/task.json`; that reviewer-only failure is preserved in
[01_provenance_attempt1.log](/audit-output/evidence/01_provenance_attempt1.log)
and was corrected by comparing the schema's shared fields.

The candidate's [prompt.py](/candidate/prompt.py) and
[py2mpy.py](/candidate/py2mpy.py) are byte-identical to the trusted mounts.
The generation records only claim that 39 claims closed; no generation report,
trace, or old `#Top` was used as proof evidence.

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an arbitrary finite list of integers, return a list obtained by repeatedly
selecting the minimum remaining value, then the maximum remaining value, then
the minimum, and so on. The documented examples include the empty list,
duplicates, and a four-element ascending list. The trusted canonical
implementation performs exactly that process by mutating its local list
argument.

The generated [solution.py](/candidate/solution.py) uses a different
value-level algorithm: sort the list, then recursively take the first and last
elements and recurse on the interior. For mathematical finite integer lists,
this has the same returned value as the contract.

Trusted regeneration with

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy
cmp -s /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy
```

exited 0 and established byte identity with the submitted
[solution.mpy](/candidate/solution.mpy). The exact command is in
[02_regenerate_mpy.log](/audit-output/evidence/02_regenerate_mpy.log).

The independent differential script
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and generated entry points independently. It covers the
three examples, empty/singleton/two-element branch boundaries, duplicates,
negative and large integers, exhaustive lists of lengths 0 through 7 over
`{-2,-1,0,1,2}`, and 500 fixed-seed random lists through length 30. All 98,171
returned values agreed. See
[02_differential.log](/audit-output/evidence/02_differential.log).

There is nevertheless a concrete full-domain implementation limitation. Under
the audit's CPython 3.10 default recursion limit of 1,000, the generated
recursive implementation raises `RecursionError` on `list(range(2000))`,
whereas the trusted iterative canonical returns 2,000 values. This is recorded
by [large_domain_divergence.py](/audit-output/evidence/large_domain_divergence.py)
and [02_large_domain_divergence.log](/audit-output/evidence/02_large_domain_divergence.log).
If Python resource limits are abstracted away, the generated algorithm is
mathematically equivalent; the formal finite-size gap below remains independently
fatal.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/candidate-src`. No
candidate-built definition or cache existed or was reused.

The concrete generated semantics rebuilt with the LLVM backend:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/concrete-kompiled
```

Exit 0 is recorded in
[03_kompile_concrete.log](/audit-output/evidence/03_kompile_concrete.log).
Fresh `krun` executions on empty, singleton, prompt length-4, unsorted
length-5, and length-6 inputs all exited 0 and returned the independently
expected lists. The individual logs are
[03_krun_empty.log](/audit-output/evidence/03_krun_empty.log),
[03_krun_singleton.log](/audit-output/evidence/03_krun_singleton.log),
[03_krun_prompt.log](/audit-output/evidence/03_krun_prompt.log),
[03_krun_unsorted5.log](/audit-output/evidence/03_krun_unsorted5.log), and
[03_krun_len6.log](/audit-output/evidence/03_krun_len6.log).

The reviewer-authored
[semantics_differential.py](/audit-output/evidence/semantics_differential.py)
mechanically parsed fresh K results and compared them with both Python
implementations on six normal/boundary cases. All agreed; see
[03_semantics_differential.log](/audit-output/evidence/03_semantics_differential.log).

The proof definition rebuilt with the Haskell backend:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/verification-kompiled
```

It exited 0
([03_kompile_proof.log](/audit-output/evidence/03_kompile_proof.log)).
The candidate designates one positive target-proof invocation, covering every
claim in `SPEC`:

```text
kprove spec.k --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC
```

It independently exited 0 and printed exactly `#Top`; see
[03_kprove_positive.log](/audit-output/evidence/03_kprove_positive.log).
The tool versions were K v7.1.293 and Python 3.10.12
([00_tool_versions.log](/audit-output/evidence/00_tool_versions.log)).

Thus clean reconstruction succeeds. Reconstruction success does not establish
that the submitted claims have the required scope.

## 4. Adequacy and real-program pinning

### Program identity and active computation

This generated semantics uses `<result>` as its active computation cell rather
than a conventional `<k>` cell. Its initial rule rewrites `pending` to
`invoke(ENTRY, pList(INPUT), PGM)`, and function lookup then evaluates the body
stored in `<program>`. Each claim fixes `<program>` to `solutionProgram` and
`<entry>` to `"strange_sort_list"`.

The `solutionProgram` equation is the complete constructor tree from
`solution.mpy`. A mechanical comparison removed whitespace and normalized the
translator's omitted empty `Stmts` branches against explicit `.Stmts`; the two
546-character normalized terms were identical. See
[constructor_compare.py](/audit-output/evidence/constructor_compare.py) and
[02_constructor_compare.log](/audit-output/evidence/02_constructor_compare.log).
There is no execution-summary rule that replaces either program-defined
function.

A body-sensitivity mutation removed the embedded `sorted` call from the actual
`solutionProgram` term while leaving `strangeSpec` unchanged. The mutated
definition built successfully, but the original proof failed on the
two-element `A >Int B` claim with a residual result `cons(A,cons(B,nil))`.
That is the expected dependence on the real body. The mutation and evidence
are [verification-body-mutation.k](/audit-output/evidence/verification-body-mutation.k),
[04_body_mutation_kompile.log](/audit-output/evidence/04_body_mutation_kompile.log),
and [04_body_mutation_kprove.log](/audit-output/evidence/04_body_mutation_kprove.log).
A reviewer-only parenthesis error in the first mutation build is separately
preserved in
[04_body_mutation_kompile_attempt1.log](/audit-output/evidence/04_body_mutation_kompile_attempt1.log).

### What each entry claim says

All 39 declarations are entry claims; there are no loop, helper-execution, or
auxiliary circularity claims.

| Claims | Plain-language precondition | Exact postcondition |
|---|---|---|
| 1 | input is `[]` | returned list equals `strangeSpec([])` |
| 2 | input is `[A]`, for arbitrary mathematical integer `A` | returned list equals `strangeSpec([A])` |
| 3–4 | input has exactly two arbitrary integers, partitioned by `A <= B` versus `A > B` | returned list equals `strangeSpec(input)` |
| 5–10 | input has exactly three arbitrary integers, split into the six exhaustive insertion-order paths | returned list equals `strangeSpec(input)` |
| 11–34 | input has exactly four arbitrary integers, split into the 24 exhaustive insertion-order paths | returned list equals `strangeSpec(input)` |
| 35–37 | the three fixed prompt examples | the fixed documented returned list |
| 38–39 | exactly `[3,-1,2,3,0]` or `[4,1,7,2,6]` | one fixed expected returned list |

The postconditions are exact destination terms, not free variables,
existentials, implications, or tautologies. The representative finite
partition check found exactly one applicable path for every tested assignment,
including equality boundaries
([04_claim_partitions.log](/audit-output/evidence/04_claim_partitions.log)).

Every precondition is satisfiable. The reviewer found and printed a concrete
witness for each of the 39 claims, substituted it into the destination, and
compared the result with both Python implementations. Every comparison agreed.
See [claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and
[04_claim_witnesses.log](/audit-output/evidence/04_claim_witnesses.log).

### Material adequacy failure

The source contract has no list-length bound. The formal union covered by the
symbolic claims is:

```text
all integer lists of lengths 0, 1, 2, 3, or 4
plus exactly two particular lists of length 5
```

There is no claim with an arbitrary `PList` tail, no invariant or induction
claim, and no universal summary connection theorem. For example, the
satisfying intended-domain input `[9,-9,4,4,0,2]` has the result
`[-9,9,0,4,2,4]` under fresh K and both Python implementations, but it unifies
with no submitted entry claim. A general length-5 input such as
`[0,1,2,3,4]` is likewise uncovered.

Finitely many fixed sizes and examples cannot prove the unrestricted
HumanEval domain. The proof is adequately pinned and result-constraining for
its finite cases, but materially too narrow for the requested theorem.

## 5. Rule-by-rule static soundness review

The complete mechanical inventory is
[static_inventory.py](/audit-output/evidence/static_inventory.py) with output
in [05_static_inventory.log](/audit-output/evidence/05_static_inventory.log).
It found 49 rules in `semantic.k` and 5 rules in `verification.k`. An initial
reviewer-only f-string syntax error is preserved in
[05_static_inventory_attempt1.log](/audit-output/evidence/05_static_inventory_attempt1.log).

### Syntax, configuration, and attributes

The local AST declarations at `semantic.k:7–29` cover `Module`, statement
lists, `FuncDef`, `Assign`, `If`, `Return`, one-parameter `Params`, and the
expression/index/bound constructors. The submitted program uses:

```text
Module FuncDef Params If Return Name Int ListExpr Call Compare CmpOp
BinOp UnaryOp Subscript Slice NoBound
```

Every used constructor maps to those declarations. `Assign` is declared and
modeled but unused. Missing syntax for other Python constructs is acceptable
under `GENERATED_SEMANTICS` because the translated target does not contain
them.

The value declarations at `semantic.k:41–51` model finite integer lists,
integers, booleans, list values, normal environments, return, and the pending
start marker. The configuration's `program`, `input`, `entry`, and `result`
cells are all read by execution; the first three are preserved and only
`result` changes. Environments are explicit `Map` arguments. No heap, I/O, or
other state is needed by this pure target.

There are 21 `[function]` declarations in `semantic.k` and three in
`verification.k`. There are no local `total`, `functional`, `simplification`,
`concrete`, `owise`, priority, or opaque declarations. Unsupported or
ill-typed terms therefore stop rather than being fabricated by a totalization
rule.

### Exhaustive rule decisions

The following IDs enumerate every local rule in source order.

| Rule IDs and source | Decision and justification |
|---|---|
| S01 (`semantic.k:61–64`) | Sound start rule: preserves program/input/entry and begins evaluation of exactly that program. |
| S02 (`:68`) | Sound definitional dispatch from a module to lookup over its definitions. |
| S03–S04 (`:71–77`) | Matching-name and unequal-name lookup rules are disjoint and sound for this target's two unique function names. A module with duplicate definitions would require Python's last-binding behavior, but no such module occurs. |
| S05 (`:80`) | Soundly extracts only an explicit returned value; missing returns remain stuck rather than invented. |
| S06–S07 (`:83–84`) | Correct empty/cons statement-list execution; recursion structurally consumes a statement. |
| S08–S09 (`:87–88`) | Correctly propagates return (discarding the remaining local statements) or continues with the updated environment. |
| S10–S12 (`:91–95`) | Assignment evaluates before update, return evaluates its expression, and `If` evaluates its condition before branching. Assignment is unused; the target's expressions are pure, so the abstract big-step order preserves all observable target behavior. |
| S13–S14 (`:98–99`) | Disjoint/exhaustive boolean branches; target guards always produce `pBool`. |
| S15–S23 (`:103–116`) | Each used expression constructor dispatches to the corresponding lookup, literal, list, call, equality, list addition, negation, or indexing operation. All operators occurring in `solution.mpy` are covered. No answer or unconstrained value is introduced. |
| S24 (`:119`) | Truthful two-integer list construction, exactly the only nonempty literal form used. |
| S25–S27 (`:122–125`) | `len` and `sorted` are selected by exact builtin names; all other names invoke program definitions. Guards are disjoint. Target bindings do not shadow either builtin. |
| S28–S30 (`:128–134`) | Integer equality, list concatenation, and integer negation are ordinary truthful equations on the matched value sorts. |
| S31–S33 (`:137–141`) | Positive indexing, negative indexing, and the exact `[1:-1]` slice map correctly to `nth` and `interior` on all reachable target states. `nth` is partial out of bounds, but the recursive branch is reached only at length at least 2. |
| S34–S35 (`:145–146`) | Correct, disjoint, structurally recursive list length equations. |
| S36–S37 (`:149–150`) | Correct zero/positive `nth`; recursion decreases the positive index. Negative and out-of-range cases remain unmodeled/stuck and are unreachable in this program. |
| S38–S39 (`:153–154`) | Correct, disjoint, structurally decreasing append equations. |
| S40–S42 (`:157–159`) | Correct and exhaustive `dropLast` equations for empty, singleton, and length-at-least-two lists; the recursive list shortens. |
| S43–S44 (`:162–163`) | Correct interior operation: empty stays empty; nonempty drops the head and then the last of the tail. |
| S45–S46 (`:166–167`) | Correct insertion-sort recursion over every finite `PList`; recursive input shortens. |
| S47–S49 (`:170–172`) | Correct insertion into empty or nonempty sorted lists. `<=Int` and `>Int` guards are disjoint and exhaustive over K integers, including equality. |
| V01 (`verification.k:10–29`) | Sound definitional abbreviation for the exact submitted constructor tree, confirmed mechanically and by body sensitivity. It does not replace execution. |
| V02–V04 (`:34–38`) | Truthful, disjoint and exhaustive definition of alternating first/last elements for empty, singleton, and longer lists; recursion removes two elements. It appears only in the postcondition side. |
| V05 (`:41`) | Truthful contract definition: insertion-sort the input, then weave its ends. It does not rewrite a program operation or introduce an oracle. |

No inventoried rule smuggles the task answer into program execution, bypasses a
program-defined body, introduces a fresh result, or creates an inconsistency.
There are no operational bridges or opaque result-bearing abstractions in
`verification.k`. The property is encoded, appropriately, in `strangeSpec` on
the destination side and is independently computed from the executed result.

Evaluation order is abstracted by pure K functions. That is sound for the
covered program because its subexpressions have no state, I/O, allocation
identity, or target-domain exceptions. K `Int` matches Python's mathematical
integer values. The main language-model limitation is that the semantics has
unbounded mathematical recursion and no CPython recursion-limit exception.
The length-2,000 witness in Stage 2 demonstrates that model/implementation
boundary. It does not make a false submitted small-list claim provable, but it
prevents treating this generated semantics as a universal refinement of
concrete CPython.

## 6. Fresh non-vacuity test

The fresh reviewer mutation
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) uses the realizable
input `[]` but changes the exact destination from `[]` to the demonstrably
false `[0]`.

First,

```text
kprove spec-vacuity.k \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, proving that the mutation parsed and built successfully
([06_nonvacuity_dry_run.log](/audit-output/evidence/06_nonvacuity_dry_run.log)).
The actual proof command without `--dry-run` exited 1 with
`WarnStuckClaimState`; its final configuration contains `pList(nil)` and
cannot unify with the demanded `pList(cons(0,nil))`. See
[06_nonvacuity_kprove.log](/audit-output/evidence/06_nonvacuity_kprove.log).

This is a meaningful result-obligation failure, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation. The submitted
finite theorem is non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under the freshly built K definition, executing the exact submitted program
from the entry configuration returns `strangeSpec(input)`:

- for every K integer at exact lengths 0 and 1;
- for every pair, triple, and quadruple of K integers, through exhaustive
  linear-order path partitions;
- and it returns the stated concrete values for the redundant prompt examples
  and two particular length-5 inputs.

The proof establishes normal reachability for these cases, not merely an
implication about a free result. It does not establish the result for arbitrary
finite lists.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, `kore-exec`, and built-in `INT`, `BOOL`, `MAP`, and `STRING` theories | all executions and proofs | Fundamental accepted toolchain boundary; version and commands are recorded. |
| Trusted `py2mpy.py` translation | source-to-constructor identity | Approved benchmark boundary. Fresh output is byte-identical to `solution.mpy`. |
| `solutionProgram` transcription | every claim | Not assumed after audit: normalized constructor equality and the body-sensitivity mutation connect it to the submitted program. |
| Generated operational semantics as a model of the used Python subset | every K execution claim | Individually audited rule by rule and tested on boundaries. There is no formal universal CPython refinement theorem; concrete recursion-resource behavior differs at length 2,000. |
| `length`, `sortInts`, `insertInt`, `nth`, `append`, `interior`, and `weaveEnds` equations | program execution or postcondition | Not opaque primitives: their exhaustive structural equations were audited for truth, disjointness, coverage on all uses, and descent. |
| Natural-language “alternating min/max” intent to `strangeSpec = weaveEnds(sortInts(L))` | interpretation of the postcondition | Direct informal mathematical bridge, supported by 98,171 independent differential cases. Finite testing does not make it a universal proof. |
| CPython termination/resource behavior | full source-contract interpretation | Excluded by the K model and contradicted by the recorded length-2,000 `RecursionError`; this limitation lies beyond the submitted small-list claims. |

There are no fresh symbols, unconstrained oracles, proof-local simplification
axioms, priority shortcuts, or empirical values inside the proof theory.
Differential testing supports only source/semantic and intent bridges; it is
not counted as a substitute for `kprove`.

In Kit terms, Gate A passes for the exact submitted finite claims: the program
is pinned, the local theory is sound on those claims, the result is constrained,
and both body-sensitivity and false-result probes discriminate. Gate B fails
because the source-contract domain is materially narrowed. Gate C evidence is
reproducible, but the semantics-to-concrete-Python and intent bridges remain
informal/finite and the recursion-limit witness exposes their universal
boundary.

The benchmark explicitly maps a `SOUND-BUT-LIMITED` theorem caused by
materially narrowing the HumanEval domain to failure. Clean `#Top`, honest
finite claims, and non-vacuity therefore cannot make this a legitimate proof
of the requested program contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
