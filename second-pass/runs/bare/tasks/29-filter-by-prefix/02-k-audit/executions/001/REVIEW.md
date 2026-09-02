# Independent adversarial audit: 29-filter-by-prefix

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact regenerated program under its generated K semantics. Fresh
LLVM and Haskell definitions built from source; the loop claim, the
compositionally isolated program claim, and the original complete spec each
closed with `#Top` and exit 0. The result and body mutations were both rejected
for the expected semantic obligation.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
individually generated semantics is a small, informal model of the used Python
subset rather than a machine-checked refinement of CPython. Several rules are
deliberately broader than general Python but remain sound for every execution
of this submitted, well-typed source. No concrete or symbolic false conclusion
witness was found on the intended domain.

All candidate prose, traces, logs, and compiled output were treated only as
untrusted claims. The detailed rule inventory is
`/audit-output/evidence/05_rule_inventory.md`; commands and bounded transcripts
are under `/audit-output/evidence/`.

## 1. Input and provenance integrity

### Semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
the three regular files `/reference/prompt.py`, `/reference/canonical.py`, and
`/reference/py2mpy.py`; `/reference/reference-semantics` is absent as required.
The candidate's untrusted `run-input.json` says `"semantics": false`, consistent
with generation without supplied semantics. There is no mount contradiction,
so the audit proceeded. See `evidence/01_integrity.log`.

### Required artifacts and identity

All required candidate artifacts are regular, non-symlink files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and executable `prove.sh`. The structured trace is
present as one regular JSONL file. No candidate symlink exists.

The candidate prompt is byte-identical to the trusted prompt
(SHA-256 `a173ce6b1e3767cabcf0ff73457d20e4eac07e0968b173b76afa0b35c0799646`).
The candidate translator is byte-identical to the trusted translator
(SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
There are no missing, changed, mistyped, or symlinked required source
artifacts.

Extra generated outputs are `/candidate/semantic-kompiled/` and
`/candidate/__pycache__/`. They are not source integrity failures, but none was
copied or used. The complete extra-file listing is in
`evidence/01_integrity.log`. There are no extra top-level K helper files:
`semantic.k`, `verification.k`, and `spec.k` are the complete candidate K
source set (`evidence/05_source_inventory.log`).

### Untrusted provenance claims read

`run-input.json`, `metrics.json`, `codex-last.txt`, the full 25,295-line
`codex-output.log`, and all 347 JSON records in the structured trace were read.
The trace parsed with zero JSON errors. Those sources claim an exit-0
generation, four concrete tests, and `KPROVE_PASSED`; none was used as proof
evidence. Hashes, counts, bounded command mentions, and the final untrusted
claim are in `evidence/01_provenance_scan.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite `List[str]` and a `str` prefix, return a new list containing
exactly the input strings whose beginning equals the prefix, in original order.
Thus duplicates are preserved, an empty prefix selects every string, and a
prefix longer than a candidate string does not select it. This is the contract
in `/reference/prompt.py`; `/reference/canonical.py` implements it as
`[x for x in strings if x.startswith(prefix)]`.

`/candidate/solution.py` implements the same stable filter with an initially
empty result list, one source-order loop, a `startswith` guard, and one append
per matching item. It neither mutates the input list nor changes the signature.
The intended domain is the annotated `List[str], str`; dynamic Python values
outside that domain are not claimed.

### Translation pin

Running the trusted translator on the copied `solution.py` regenerated
`solution.mpy` at
`/tmp/audit-work/generated/solution.mpy`. It is byte-identical to the submitted
file; both have SHA-256
`7d10644743b0d635231400e73ff58c5755e17dd09b7a73f64b79fd8fa0a12269`.
The exact command, hashes, `cmp` exit 0, and differential run are in
`evidence/02_program_checks.log`.

### Independent CPython differential

`evidence/02_differential.py` independently imports the trusted canonical entry
and the copied generated entry. It checks:

- all documented examples and 12 additional fixed boundary/Unicode/escape
  cases (14 fixed cases total);
- every list of lengths 0 through 3 over eight representative strings, crossed
  with eight prefixes (4,680 exhaustive small cases);
- 2,000 deterministic generated cases with list lengths 0 through 8
  (seed `290029`).

All 6,694 cases matched, both implementations preserved the input, and the
generated result remained a `list`. Exit was 0 with zero mismatches. This is
finite fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Every source used for execution was copied to `/tmp/audit-work`; the six copied
candidate source artifacts compare byte-for-byte equal to their originals
(`evidence/03_scratch_identity.log`). Candidate definitions and caches were not
copied.

Tooling was Python 3.10.12 and K v7.1.293
(`evidence/00_environment.log`). From copied source:

1. `kompile --backend llvm semantic.k --main-module MPY
   --syntax-module MPY-SYNTAX --output-definition
   /tmp/audit-work/concrete-kompiled` exited 0.
2. `kompile --backend haskell semantic.k --main-module SEMANTIC
   --syntax-module VERIFICATION --output-definition
   /tmp/audit-work/proof-kompiled` exited 0.

The exact transcript is `evidence/03_build.log`. The LLVM definition uses
`MPY`, so proof-only summaries are not imported into concrete program
execution.

### Fresh generated-semantics execution

`evidence/03_concrete_compare.py` invoked the submitted `solution.mpy` directly
against the fresh LLVM definition. It independently decoded the `<output>` cell
and compared it with both Python entries for 10 cases: empty input, the
documented example, empty prefix, longer prefix, equal matching and
equal-nonmatching strings, stable duplicates, composed/decomposed Unicode,
emoji, spaces, tabs, quotes, and backslashes. Every `krun` exited 0, ended with
`.K`, and matched both Python results. The complete bounded configurations and
commands are in `evidence/03_concrete_compare.log`.

### Fresh positive proofs

All positive targets closed with `#Top` and exit 0:

- `--claims loop-correct` independently proved the helper claim.
- `--trusted loop-correct` then proved `program-correct` compositionally. Here
  “trusted” is a command-local composition mechanism for the exact loop claim
  proved by the immediately preceding independent command, not an unproved
  candidate assumption.
- Running the original `SPEC` without filters proved both submitted claims
  together.

Commands and outputs are in `evidence/03_positive_proofs.log`. This satisfies
the positive gate independently of the candidate's prior `#Top`.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop-correct` has no textual `requires`; its sort and configuration pattern
are its precondition. At the exact loop head, `INPUT` is the finite remaining
string list, `ACC` is the result accumulated so far, the environment contains
the same `PREFIX`, and the continuation is exactly the source return followed
by `functionEnd` and `.K`. If execution terminates, `<k>` is consumed and
`<output>` is exactly `listVal(filterAcc(INPUT,PREFIX,ACC))`. The functions,
external input, and prefix cells are preserved; only the final environment is
existentially framed.

`program-correct` starts with empty environment and function table, arbitrary
`INPUT:StrList` and `PREFIX:String`, and `noOutput`. If the exact encoded
program terminates, `<k>` is consumed and output is exactly
`listVal(filterByPrefix(INPUT,PREFIX))`.

Neither result is a free variable, tautology, or one-way property. `filterAcc`
and `filterByPrefix` are covered constructor-recursive definitions whose two
guarded branches are disjoint and exhaustive after `startsWith` evaluates.
Existentials occur only for irrelevant final environment/function maps.

### Exact source execution

The program claim begins with `solutionProgram()`, but this is not an oracle or
execution shortcut. Its only equation expands to the complete module
constructor term. `loopBody()` likewise expands to the exact translated
`If`/`startswith`/`append` body. Explicit `.Strings` and `.Stmts` tails are the
canonical spelling of the list syntax appearing implicitly in the submitted
file. Trusted regeneration proves byte identity of that submitted constructor
file, while direct fresh `krun` executes the file itself.

The loop claim matches the real stable loop-head term and the exact return
continuation reached from this source. It does not admit an arbitrary
continuation. The source body is not replaced by an opaque result: the
operational rules execute it, and the universal loop claim is the connection
theorem to `filterAcc`.

### Satisfiable states and concrete substitution

`evidence/04_ground_instances.k` supplies and proves two ground instances:

- Program state: empty env/functions, input
  `["abc","bcd","cde","array"]`, prefix `"a"`, and `noOutput`. The claimed,
  canonical, and generated-Python results are all `["abc","array"]`.
- Loop state: accumulator `["prior"]`, remaining input `["abc","b"]`, prefix
  `"a"`, exact return continuation, empty functions, and `noOutput`. The
  claimed result and `ACC +` each Python implementation's filtered remainder
  are all `["prior","abc"]`.

The ground spec dry-run exited 0, its proof printed `#Top` with exit 0, and both
Python comparisons passed (`evidence/04_ground_instances.log`). These states
demonstrate that both claim preconditions are realizable.

## 5. Rule-by-rule static soundness review

The exhaustive inventory in `evidence/05_rule_inventory.md` enumerates:

- 42 local syntax productions/declarations, including all runtime
  continuations and proof-side function symbols;
- the six-cell configuration;
- 33 candidate semantic rules (four mathematical function equations and 29
  operational rules);
- six verification equations, for 39 local rules total;
- both reachability claims and every construct-to-rule mapping.

There are no local opaque symbols, `functional` declarations, priority rules,
`concrete` rules, or trusted claims. `startsWith` is the only `total`
declaration. The only simplification rules are the true/false `filterAcc`
branches.

### Static conclusions

- Evaluation order is explicit: receiver/function before argument, RHS before
  assignment, iterable before loop, guard before branch, and return expression
  before control transfer.
- State updates are confined to function registration and environment
  bindings. The result list is constructed fresh and only its binding is
  appended. Input, prefix, and output cells are preserved except where
  deliberately read or returned.
- `startsWith` guards (`>` versus `<=` length) are disjoint and exhaustive;
  valid substring bounds follow from the latter guard. `If` guards (`true`
  versus `false`) and `filterAcc` guards are likewise disjoint and exhaustive.
- `appendOne`, `filterAcc`, and `filterByPrefix` descend structurally. No false
  totalization or overlapping unequal equation was found.
- `solutionProgram` and `loopBody` are exact definitional syntax
  abbreviations. `filterAcc` is a result-bearing summary, but source execution
  is universally connected to it by `loop-correct`; there is no unconstrained
  result oracle or circular reuse of an opaque symbol.
- The loop connection's matched context is contained in its justification:
  it fixes the entire trailing return/function-end computation. Its framed
  function/input cells are not read or changed by the loop body; its
  environment frame excludes the explicitly bound prefix/result keys.
- Import ignoring, name-based append binding, value-only list modeling, finite
  list iteration, and return-continuation discard are intentionally minimal.
  They would not constitute general Python semantics, but the exact source has
  only a type import, no rebinding/alias-sensitive interleaving, no mutation of
  the iterated input, no nested source calls, and one top-level return. Thus no
  satisfying intended-domain state witnesses a false conclusion from those
  broader rules.

The proof definition imports the verification functions, but concrete source
terms contain none of `filterAcc`, `filterByPrefix`, `loopBody`, or
`solutionProgram`; the fresh LLVM `MPY` build further excludes them. No
proof-specific rule preempts execution of a constructor in `solution.mpy`.

As an execution-sensitivity check, the reviewer replaced the guarded source
loop body with unconditional append. The mutant definition built successfully,
but the unchanged proof exited 1 with `WarnStuckClaimState` on the false loop
summary. The ground witness `strings=["b"], prefix="a"` makes the divergence
explicit: the mutant returns `["b"]` while the spec requires `[]`.
Artifacts and transcript are
`evidence/04_verification_body_mutant.k` and
`evidence/04_body_sensitivity.log`.

No inventoried local rule was classified as unsound on the intended domain.
Accordingly, this review makes no unsoundness allegation requiring a false
conclusion witness; the narrower modeling/evidence limitations are accounted
for in Stage 7.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity spec. The reviewer-authored
`evidence/06_spec_vacuity.k` keeps the exact loop lemma and changes the
program's result obligation to append `"__AUDIT_FALSE__"` to every result.
For the satisfying state `INPUT=nil`, `PREFIX="a"`, empty env/functions, and
`noOutput`, concrete execution returns `listVal(nil)` while the mutation
requires `listVal(cons("__AUDIT_FALSE__",nil))`.

The mutated spec dry-run exited 0, demonstrating successful parsing/building.
With the already independently proved loop claim used compositionally, the
mutated proof exited 1 and emitted `WarnStuckClaimState`. Its residual contains
the unmet equality between `filterAcc(INPUT,PREFIX,nil)` and
`appendOne(filterAcc(INPUT,PREFIX,nil),"__AUDIT_FALSE__")`. This is a reachable
result failure, not a parser error, timeout, unrelated crash, or dead mutation.
The exact commands, statuses, and residual are in
`evidence/06_nonvacuity.log`.

## 7. Proven versus assumed accounting

### Formally established

Under the compiled candidate theory, for every finite `INPUT:StrList` and
`PREFIX:String` satisfying the entry configuration, terminating execution of
the exact submitted program term returns the stable constructor-list result
defined by `filterByPrefix`. The loop proof connects every remaining list and
accumulator to `filterAcc`; the program proof connects empty initialization and
the exact source body to that lemma. This is a partial-correctness statement,
not a claim about arbitrary dynamically typed arguments or all of Python.

### Trust and evidence ledger

| Boundary | Influence | Assessment and support |
|---|---|---|
| K v7.1.293 parser, compiler, LLVM/Haskell backends, and reachability/circularity logic | All execution and proof closure | Necessary low-level trusted checker boundary; fresh builds and independent commands avoid candidate caches |
| Imported `Bool`, `Int`, `String`, and symbolic `Map` primitives (`lengthString`, `substrString`, equality/comparison, lookup/update) | Prefix branches, bindings, result | Legitimate fixed K primitives, not task-answer oracles; guards were statically checked and Unicode/escape behavior was concretely exercised |
| Trusted `/reference/py2mpy.py` | Python-source-to-constructor pin | Authoritative translator; regeneration is byte-identical |
| Generated MPY semantics versus CPython for the used source subset | Evaluation/control/state meaning and therefore theorem-to-program bridge | Informal rule-by-rule argument plus 10 direct K/Python comparisons; no machine-checked refinement theorem. This is the principal concern. |
| Trusted canonical implementation and CPython runtime | Natural-language intent bridge | 6,694 finite differential cases and exact examples support the bridge; they do not prove universal equivalence |
| Well-typed domain `List[str], str` and finite lists | Entry scope | Matches prompt annotations and K sorts; off-domain Python behavior, exceptions, subclasses, custom iterables, and external effects are excluded |

There are no candidate-local opaque values, unconstrained branch oracles, or
unproved program-defined helpers. The temporary `--trusted loop-correct` use in
one reconstruction command is discharged by the separate exact claim proof
and corroborated by the unfiltered original-spec proof; it is not part of the
candidate theory.

The empirical tests support only their stated source/semantics bridges. They
are not being substituted for the reachability proof. Conversely, `#Top`
establishes closure only under the audited theory; it does not eliminate the
informal generated-semantics-to-CPython boundary. That bounded limitation, plus
the intentionally source-specific rules noted in Stage 5, warrants
`CONCERNS` without making the proof illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
