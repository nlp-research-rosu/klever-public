# Independent adversarial audit: 40-triples-sum-to-zero

The candidate does not contain a legitimate proof of the real submitted
program. Fresh reconstruction succeeds, all seven submitted claims are
non-vacuous and result-constraining, and the Python implementation is faithful
to the canonical implementation. The decisive defect is real-program pinning:
the claims prove a new `#runTriples` entry that manually constructs a closure
containing a copy of the function body. They never load or execute the submitted
`solution.mpy` module. A fresh body-sensitivity experiment replaces
`solution.py` and `solution.mpy` with an always-false implementation; the
length-three K proof still rebuilds and prints `#Top`. The formal claims also
cover only exact input lengths zero through six, while the contract covers
arbitrary finite lists of integers.

All candidate material was treated as untrusted. All execution occurred below
`/tmp/audit-work/forty-triples-audit`, using reviewer-created definitions. The
reviewer-authored scripts, complete deterministic test inputs, mutation, exact
command wrappers, exit statuses, and bounded logs are under
`/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. The trusted mounts therefore do
not contradict the rendered mode; this is not an infrastructure breach.

A strict non-dereferencing recursive comparison found 25 entries in each
semantics tree and found exact entry-name, entry-type, and byte-content
identity. There were no missing, additional, changed, mistyped, or symlinked
entries in `/candidate/reference-semantics`. This comparison is implemented in
`evidence/compare_tree.py` and recorded in
`evidence/01_integrity.log`.

The following candidate artifacts were present as ordinary files/directories:

- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`,
  `verification.k`, and `reference-semantics/`.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- No symlink occurs anywhere in `/candidate`.

The following expected provenance artifacts were absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any recognized structured generation trace

Their absence is a candidate provenance/evidence gap, not an audit
infrastructure failure. No `PROOF.md` or candidate `spec-vacuity.k` was
present. The top-level `__pycache__/solution.cpython-310.pyc` was ignored and
never copied into a build. Candidate `prove.sh`, concrete harnesses, and their
claims were inspected only as untrusted evidence. No candidate-provided K
compiled definition was present or reused. Source hashes are in
`evidence/01_integrity.log`.

The tool environment was K 7.1.337 and Python 3.10.12; paths and version output
are preserved in `evidence/00_environment.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From trusted `prompt.py` and `canonical.py`, the function accepts a finite
Python list of integers and returns a Python Boolean. It returns `True` exactly
when there are three distinct positions `i < j < k` whose values sum to zero;
otherwise it returns `False`. Repeated values are allowed when they occur at
distinct positions. Lists of length less than three return `False`. Python
integers are unbounded for this contract.

Candidate `solution.py` uses the same three nested increasing-index loops as the
trusted canonical implementation. It differs only by omitting the docstring and
comments, not algorithmically.

### Trusted translation identity

The trusted translator was run on the scratch copy of candidate `solution.py`.
The regenerated file and submitted `solution.mpy` both have SHA-256
`252f0f098f80b0578b66958658ec4d41bcbd78919a509d45dc018e941f0f8dc5`
and are byte-identical. See the exact command and exit 0 in
`evidence/02_translate_identity.sh` and
`evidence/02_translate_identity.log`.

### Independent differential test

`evidence/differential.py` independently imports the trusted canonical entry
point and candidate entry point. It checks:

- all five documented examples;
- empty, length-one, length-two, length-three true/false, first-hit, late-hit,
  repeated-value/distinct-position, and large-integer boundaries;
- an explicit length-seven case outside the K proof's scope;
- every list of lengths 0 through 6 over values `-3..3` (137,257 inputs);
- 4,000 deterministic generated lists of lengths 0 through 14 over values
  `-20..20`.

All 141,272 comparisons agreed, with 0 mismatches. The complete generated input
set is `evidence/differential-inputs.json`, whose recorded SHA-256 is
`302a745b1789ec4109d898dea9a60171adbfc5b59dc521269fa2926fbbe18638`.
The command, named cases, counts, and exit 0 are in
`evidence/02_differential.log`.

This is strong finite evidence that `solution.py` implements the intended
function. It is not a universal K proof and does not connect the submitted file
to the synthetic K entry.

## 3. Clean proof reconstruction

All needed source was copied into
`/tmp/audit-work/forty-triples-audit/candidate-src`. Candidate caches and
compiled definitions were excluded. The selected supplied semantics in the
scratch copy was the candidate tree already shown byte-identical to the trusted
tree.

### Fresh builds and concrete execution

The reviewer freshly built:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/forty-triples-audit/runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/forty-triples-audit/verification-kompiled
```

Both exited 0. Exact scripts and bounded output are
`evidence/03_build_runtime.sh`, `evidence/03_build_runtime.log`,
`evidence/03_build_proof.sh`, and `evidence/03_build_proof.log`.

LLVM compilation warned that several fixed-semantics `[total]` functions are
not syntactically exhaustive (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`). Only `valSeqAt` is on this program's execution
path, and the nested range bounds ensure every used index is in bounds, where
its defining equations reduce. The other warned functions are unused here.
The Haskell build emitted only unused-variable warnings in fixed `strLt` rules.

The candidate's concrete harness was independently retransliterated with the
trusted translator, required byte identity with its submitted `.mpy`, and ran
to a final configuration with `.K`, `NoExc`, and exit code 0. A separate
reviewer harness contains the candidate source as a byte-identical prefix and
adds empty, under-three, true/false length-three, later-hit, and length-seven
cases. It also ran to `.K`, `NoExc`, and exit code 0. Evidence:
`evidence/03_concrete_candidate.log`,
`evidence/actual_program_tests.py`, and
`evidence/03_concrete_reviewer.log`.

### Independently selected positive claims

Every positive target was run independently, using the claim label without
relying on a combined proof:

| Claim | Result | Evidence |
|---|---|---|
| `empty` | exit 0, `#Top` | `evidence/03_prove_empty.log` |
| `length-one` | exit 0, `#Top` | `evidence/03_prove_length-one.log` |
| `length-two` | exit 0, `#Top` | `evidence/03_prove_length-two.log` |
| `length-three` | exit 0, `#Top` | `evidence/03_prove_length-three.log` |
| `length-four` | exit 0, `#Top` | `evidence/03_prove_length-four.log` |
| `length-five` | exit 0, `#Top` | `evidence/03_prove_length-five.log` |
| `length-six` | exit 0, `#Top` | `evidence/03_prove_length-six.log` |

The exact command form was:

```text
kprove spec.k \
  --definition /tmp/audit-work/forty-triples-audit/verification-kompiled \
  --spec-module SPEC --claims <label> --output pretty
```

An initial diagnostic attempt used `SPEC.empty`, which this K version rejected
as an unused filtering label with exit 113. It is retained in
`evidence/03_prove_empty_label_attempt.log`; rerunning with the accepted
`empty` label closed. This was a claim-selection syntax diagnostic, not a
failed target proof.

The dynamic reconstruction gate therefore passes for the submitted formal
claims. Successful reconstruction alone does not establish that those claims
denote the submitted program.

## 4. Adequacy and real-program pinning

### Entry preconditions and postconditions

The seven entry claims have no explicit `requires` clause. Their sorted
variables are arbitrary K mathematical `Int` values. Each fixes the following
initial state:

- environment location 0;
- module scope 0 empty with parent builtins scope `-1`;
- `scopeLoc` 1;
- empty heap and `heapLoc` 0;
- empty call stack;
- `noRet`, `NoExc`, and exit code 0.

The only difference among the claims is the exact input length:

| Label | Formal input shape | Plain-language result |
|---|---|---|
| `empty` | exactly 0 integers | `false` |
| `length-one` | exactly 1 arbitrary integer | `false` |
| `length-two` | exactly 2 arbitrary integers | `false` |
| `length-three` | exactly 3 arbitrary integers | whether their sum is zero |
| `length-four` | exactly 4 arbitrary integers | whether one of 4 triples sums to zero |
| `length-five` | exactly 5 arbitrary integers | whether one of 10 triples sums to zero |
| `length-six` | exactly 6 arbitrary integers | whether one of 20 triples sums to zero |

Each postcondition replaces the head computation by
`hasZeroTriple(the same ValSeq)` while preserving the framed continuation and
requires the explicitly shown non-`<k>` cells to be restored. The returned
value is therefore constrained. It is not a fresh variable, tautology, or
one-way implication.

The `hasZeroTriple`, `hasZeroPair`, and `hasZeroThird` equations reduce the
result to a Boolean disjunction over increasing-position triples. Concrete
satisfying witnesses for all seven preconditions agree with that summary and
both Python implementations:

| Claim | Witness | Claimed/Python result |
|---|---|---|
| empty | `[]` | `false` |
| length-one | `[0]` | `false` |
| length-two | `[0,0]` | `false` |
| length-three | `[0,0,0]` | `true` |
| length-four | `[1,2,3,7]` | `false` |
| length-five | `[50,60,-3,1,2]` | `true` |
| length-six | `[2,4,-5,3,9,7]` | `true` |

The executable record is `evidence/claim_witnesses.py` and
`evidence/04_claim_witnesses.log`.

### Decisive pinning failure

The actual submitted `.mpy` is a
`Module(FuncDef("triples_sum_to_zero", ...))`. Under the fixed semantics, real
module execution begins with `#loadAll(Module(...))`, executes `FuncDef` to
install a named closure in scope 0, looks up the function by name, evaluates
arguments, and dispatches the call.

No submitted claim does that. `verification.k:29-61` declares a new
`#runTriples(ValSeq)` symbol and rewrites it directly to:

```text
#applyK(toCall(closureVal(copied-parameters, copied-body, 0)),
        list(VS), .Vals)
```

The copied body accurately reflects the body inside submitted `solution.mpy`,
and the fixed call/loop semantics genuinely executes that copy. Nevertheless:

- `verification.k` does not require, parse, or import `solution.mpy`;
- the claim's initial scope contains no `triples_sum_to_zero` binding;
- `Module` loading, `FuncDef` binding, and `Name`-based dispatch are absent;
- there is no bridge-free auxiliary reachability claim connecting actual module
  execution to `#runTriples`;
- there is no source/body dependency that would make a changed submitted
  program invalidate the proof.

The fresh body-sensitivity test makes this observable. In a new scratch tree,
the reviewer replaced `solution.py` with:

```python
def triples_sum_to_zero(l: list):
    return False
```

The trusted translator generated the corresponding changed `solution.mpy`.
That real changed program returns `False` on `[0,0,0]`, contradicting the
intended result. A fresh Haskell build of the unchanged proof sources still
exited 0, and the symbolic `length-three` claim still exited 0 with `#Top`.
Exact commands and output are in `evidence/04_body_sensitivity.sh`,
`evidence/mutated_solution.py`, and
`evidence/04_body_sensitivity.log`.

This demonstrates that the proved theorem is insensitive to the submitted
program artifact. It is a theorem about a manually substituted closure, not a
proof pinned to the real generated program. Concrete tests of the real module
do not supply the missing universal connection theorem.

### Domain inadequacy

The source contract contains no length-six upper bound. `spec.k` has no claim
for length seven or any inductive arbitrary-length input. The differential test
and concrete K test show the implementation behaves correctly beyond six, but
testing does not prove it. Thus even the synthetic closure is proved only on
seven finite shape families, not on the intended domain of all finite integer
lists.

The real-program pinning failure is independently sufficient for rejection.
The arbitrary-length omission is a second material adequacy gap.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/static_inventory.py` inventoried every declaration in
`reference-semantics/semantics.k`, all 24 helper `.k` files,
`verification.k`, and `spec.k`. The complete 944-row record is
`evidence/static-inventory.tsv`; its generation log and SHA-256 are in
`evidence/05_static_inventory.log`.

The inventory contains:

- 229 syntax/function declarations;
- 702 rules;
- 5 evaluation contexts;
- 1 configuration;
- 7 target claims.

Of the fixed supplied-semantics entries, it classifies 422 equational rules,
238 operational rules, 35 concrete-only rules, 205 other syntax/function
declarations, 22 opaque/no-evaluator declarations, 5 contexts, and 1
configuration. The inventory also records every `function`, `total`, `symbol`,
`no-evaluators`, `concrete`, `owise`, macro, strictness, and priority
attribute. There are no `[functional]` declarations and no
`[simplification]` rules. All 45 priority-bearing declarations and all 22
opaque declarations are in the byte-identical fixed supplied semantics, not in
candidate `verification.k`.

Every fixed-semantics inventory row is marked as accepted at the selected
semantics level because it is byte-identical to the trusted mounted tree. This
does not bless the candidate-local rules. The used execution path was
separately checked below. Unused fixed opaque primitives include float,
sorting, and digest operations; none can influence this program's branch,
return value, state, or postcondition.

### Candidate-local rule decisions

Candidate `verification.k` adds exactly two syntax declarations and seven
rules:

1. `hasZeroTriple(.ValSeq) => false` is the correct empty existential case.
2. `hasZeroTriple(vCons(A, REST))` checks pairs beginning with the head or
   recurses on the tail. These two alternatives partition triples by whether
   they use the head.
3. `hasZeroPair(_, .ValSeq) => false` is the correct no-second-element case.
4. `hasZeroPair(A, vCons(B, REST))` checks thirds after `B` or recurses to the
   next `B`. These alternatives partition increasing-position pairs.
5. `hasZeroThird(_, .ValSeq) => false` is the correct no-third-element case.
6. `hasZeroThird(S, vCons(C, REST))` checks `S+C==0` or recurses to a later
   third element.
7. `#runTriples(VS)` directly calls the manually embedded closure.

Rules 1-6 are truthful definitional summaries on the claims' integer
sequences. Constructor cases are disjoint, recursion strictly descends a
`ValSeq`, and the equations cover every summary use in the seven claims. They
encode the requested mathematical predicate, but do not replace the loop
execution: the copied loop body executes and is proved equal to the summary.
There are no local priorities, opaque symbols, totality assertions,
simplifications, or helper claims.

Rule 7 is locally a well-defined entry for the copied closure. It has no false
equation merely as a definition of the new symbol. Its defect is the absent
connection to the submitted module. If the candidate comment claiming it
represents the `solution.mpy` function is construed as a universal connection
assertion, the always-false body-sensitivity experiment is a concrete false
connection witness: submitted `[0,0,0]` evaluates to `false`, while the
unchanged synthetic proof still establishes the summary value `true`.

No other candidate-local rule is labeled unsound, so no unsupported
unsoundness allegation is made.

### Used fixed-semantics path

The full construct-to-rule map is
`evidence/construct-map.md`. The key checks are:

- `Module` and `FuncDef` syntax/rules exist and correctly establish the normal
  load/binding route, but submitted claims bypass them.
- Within the copied closure, `Call` evaluates the callee then arguments
  left-to-right; `#applyK` creates a frame, binds `l`, runs the body, and
  restores the caller environment.
- Each `For` evaluates its range once, uses `#iterNext`, binds its target, and
  preserves nesting/continuation order.
- `len(list(VS))`, `range` with step 1, integer `+`, list indexing, integer
  `==`, Boolean truthiness, `If`, early `Return`, and final `Return(false)` all
  have fixed, applicable rules.
- The increasing ranges establish `0 <= i < j < k < len(l)`, so used
  `valSeqAt` calls are in bounds. The fixed `[total]` under-specification for
  out-of-bounds values cannot fabricate a result on this program path.
- The input is a bare read-only `list(VS)`, so skipping heap allocation changes
  no mutation behavior inside this particular pure body. Frame creation/pop
  restores environment, scope location, stack, and return state; the body
  allocates no heap object and raises no modeled exception on integer lists.
- Early return discards the remaining nested-loop continuation and pops the
  active frame, matching the real control flow.

There is no rule overlap or priority interaction among candidate-local rules.
Fixed priority rules either handle heap dereferencing/cell cases disjointly or
are inactive for this bare-list, plain-frame execution. The selected
fixed-semantics rules are adequate for every construct actually used.

The static review therefore finds no result oracle, false mathematical lemma,
or vacuous postcondition. It does find the material, experimentally confirmed
source-pinning gap described in Stage 4.

## 6. Fresh non-vacuity test

The reviewer created `evidence/spec-vacuity.k`, a distinct
`SPEC-VACUITY` module. It keeps the satisfiable length-three precondition but
changes the result-constraining postcondition from `hasZeroTriple(A,B,C)` to
`false`. This mutation is demonstrably false at the satisfying input
`A=B=C=0`, for which the copied body, canonical Python, and candidate Python
all return `true`.

First, `kprove --dry-run` parsed and built the mutation successfully with exit
0; see `evidence/06_mutation_dry_run.sh` and
`evidence/06_mutation_dry_run.log`. Then the actual proof command exited 1 with
`WarnStuckClaimState`, not a parser/import/backend error. Its residual contains:

- final `<k>` headed by `true`;
- the path condition `0 == A +Int B +Int C`;
- the unmet destination demanding `false`.

The expected proof failure and complete bounded residual are in
`evidence/06_mutation_prove.sh` and
`evidence/06_mutation_prove.log`.

This is valid non-vacuity evidence for the submitted synthetic theorem. It
shows that changing its result obligation matters. It does not repair or test
the missing dependency on `solution.mpy`; that separate operational-sensitivity
test failed in Stage 4.

## 7. Proven versus assumed accounting

### What the successful K proofs actually establish

Conditional on K 7.1.337 and the selected supplied semantics, for each exact
length `n` from 0 through 6 and every choice of `n` K integers, starting in the
specified clean configuration, execution of the manually constructed closure
in `verification.k` reaches a restored caller configuration whose head result
is `hasZeroTriple` of the same sequence. The transparent summary equations make
that result the existential “three increasing positions sum to zero” predicate.

The proofs execute the copied function body under fixed semantics. They do not
establish a reachability theorem from the submitted
`Module(FuncDef(...))`, do not establish normal named dispatch, and do not
establish the result for lists of length at least seven.

### Trust and evidence ledger

| Boundary | Effect | Assessment |
|---|---|---|
| K parser, kompiler, Haskell prover, LLVM runner, and K built-in Int/Bool/Map/List theories | All build, execution, and proof results | Ordinary toolchain trust; versions and fresh logs recorded. |
| Trusted mounted supplied-semantics tree | Defines the language being proved | Acceptable by the rendered problem condition; exact candidate-tree identity independently checked. |
| Fixed `valSeqAt(...)[total]` outside defining in-bounds equations | Could under-specify out-of-bounds access | Concerning globally but inactive here: all program indices come from increasing in-range loops. It does not support the result conclusion on this path. |
| Fixed float/sort/digest and other opaque symbols | Could affect results in programs that use them | None occurs in `solution.mpy` or the proof's result path; no submitted claim depends on them. |
| `hasZeroTriple`/pair/third equations | Give the human-facing meaning of the K result | Acceptable transparent mathematics: disjoint exhaustive head/tail cases and structural descent; not an unconstrained oracle. |
| Trusted translator identity and retransliteration | Connects `solution.py` to submitted `solution.mpy` | Strong, reproducible byte-identity evidence. |
| Manual closure copy in `#runTriples` | Purports to connect formal execution to submitted program | Illegitimate as real-program pinning: no source dependency or connection claim, and a contradictory source mutation leaves `#Top` unchanged. |
| Concrete K execution of reviewer/candidate harnesses | Supports normal module semantics on selected inputs | Finite empirical evidence only; cannot replace a universal connection theorem. |
| 141,272-case Python differential test | Supports candidate implementation versus canonical intent | Strong finite evidence only; cannot replace the K proof or repair its target. |
| Exact-length enumeration in `spec.k` | Limits theorem domain | Material omission: no formal result for arbitrary-length lists. |

The candidate's successful `#Top` outputs and the fresh false-postcondition
rejection establish an honest, non-vacuous theorem about the synthetic closure.
They do not establish partial correctness of the real generated program as
required. The body-sensitivity witness meets the decisive rejection boundary
for a substituted/unpinned program, and the missing arbitrary-length theorem is
an additional material adequacy gap.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
