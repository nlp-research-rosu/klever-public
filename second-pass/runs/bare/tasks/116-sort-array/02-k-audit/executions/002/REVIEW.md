# Independent adversarial audit: 116-sort-array

The candidate reconstructs successfully and its local K claims are
result-constraining, body-sensitive, and tied to the submitted translated AST.
It nevertheless does **not** prove the HumanEval contract over its unrestricted
finite-list domain.  Its exhaustive symbolic entry claims stop at length three;
all longer claims are fixed examples.  Under the benchmark's explicit decision
boundary, that material domain narrowing is `FAIL / NOT_LEGIT`, even though the
bounded theorems themselves are sound.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`.

- All layout-required launcher files and directories are readable real
  files/directories, not symlinks.  This includes `/run.json`, `/task.json`,
  `/generation-result.json`, the invocation/metrics/last/output/prompt records,
  `usage.json`, and the structured trace.  The candidate and trace trees contain
  no linked or unsupported nodes.  See
  [stage1-provenance.log](evidence/stage1-provenance.log).
- `/audit-campaign-lock.json` is exactly equal as parsed JSON to the campaign
  block in `/audit-input.json`; its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- Every recorded regular-file hash independently checked in
  [stage1-provenance.log](evidence/stage1-provenance.log) matches: trusted and
  candidate prompt/translator, canonical, run/task/result manifests,
  invocation, metrics, usage, prompt, last message, output log, and every file
  listed by the invocation evidence map.
- The mounted candidate's pipeline-v2 tree digest is
  `232f142190d7d3fceee6ceb97f284eb126696d47b2a682e20f172e032c163e13`,
  matching both the invocation and generation-result workspace hashes.  The
  mounted trace's digest under the same recorded pipeline algorithm is
  `cf12390a8888819d9a7968f80e03c03a8c77bf2fa43cb2751c6b7bd55fdf1468`,
  matching `usage.json`.  `/audit-input.json` also carries two audit-side tree
  digests without specifying their serialization; the independently
  reproducible pipeline digests and every constituent file hash match, so there
  is no observed content or mount discrepancy.
- The 228-line JSONL trace parses completely with zero malformed records.
  [stage1-trace-index.log](evidence/stage1-trace-index.log) indexes every record;
  the generation records merely claim that bounded claims and examples passed,
  and are not used as proof authority.
- The installed live tools are K `v7.1.293` and Python `3.10.12`, as recorded in
  [stage1-toolchain.log](evidence/stage1-toolchain.log).
- The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.  In the required generated-semantics boundary,
  `/reference/reference-semantics` is absent and not a symlink.  No hidden or
  inferred reference semantics was used.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says that a finite list of non-negative integers is ordered
ascending by the number of `1` bits in each integer's binary representation,
with decimal value as the tie-breaker.  Thus the mathematical key is
`(x.bit_count(), x)`.

The prompt's displayed examples conflict with that prose and with the trusted
canonical program.  For example, the prose/canonical result for
`[1, 5, 2, 3, 4]` is `[1, 2, 4, 3, 5]`, not the displayed ordinary numeric
sort.  The canonical implementation first sorts numerically and then stably
sorts by binary-one count, which is equivalent to the tuple key on the stated
non-negative domain.

The candidate is a pure recursive insertion sort.  `count_ones` uses
`int.bit_count`; `comes_before` implements the tuple ordering; `insert_sorted`
and `sort_array` recursively build fresh lists.  This is a different but
extensionally suitable algorithm under ideal unbounded recursion.

### Translation and differential evidence

The trusted translator regenerated `solution.mpy` byte-for-byte; both copies
have SHA-256
`914cbcea1a3b771d1d2d753a4b028d2559f181c5cc1b736c3bc98cd558882034`.
See [stage2-regenerate-mpy.log](evidence/stage2-regenerate-mpy.log).

The independent differential driver
[differential_test.py](evidence/differential_test.py) imports the trusted and
candidate entry points separately.  It compared:

- all documented inputs and 13 targeted boundary cases;
- every list of length 0 through 5 over values 0 through 5 (9,331 cases);
- 3,000 seeded non-negative lists of length 0 through 20 with values below
  `2**80`; and
- 1,000 supplemental mixed-sign lists.

There were zero result mismatches and neither implementation mutated its input
([stage2-differential.log](evidence/stage2-differential.log)).

There is, however, a real CPython resource-boundary divergence.  With the
standard recursion limit 1000, the candidate matches at lengths 990 and 995 but
raises `RecursionError` at lengths 1000 and 1050; the canonical implementation
returns a list.  See
[recursion_boundary_test.py](evidence/recursion_boundary_test.py) and
[stage2-recursion-boundary.log](evidence/stage2-recursion-boundary.log).
Ordinary partial-correctness models often abstract resource exhaustion, so this
is recorded as an implementation/language-model limitation rather than the
primary verdict basis.  The formal domain narrowing below is independently
decisive.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/candidate`; the
candidate's `__pycache__` and any prior compiled definition were not reused.

Fresh builds:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition semantic-concrete-kompiled
Exit 0

kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --backend haskell --output-definition verification-proof-kompiled
Exit 0
```

The bounded build logs are
[stage3-build-concrete.log](evidence/stage3-build-concrete.log) and
[stage3-build-proof.log](evidence/stage3-build-proof.log).  Their warnings are
unused-variable warnings, not semantic or build failures.

Every one of the 22 positive claims was then selected and run independently
with:

```text
kprove spec.k --definition verification-proof-kompiled \
  --spec-module SPEC --claims SPEC.<label> --warnings none
```

All 22 exited 0 and printed exactly one `#Top`.  The labels and statuses are in
[stage3-positive-claims-summary.log](evidence/stage3-positive-claims-summary.log);
each exact command and output has a separate
`evidence/stage3-claim-<label>.log`.  Running the complete spec in one command
also exited 0 and printed `#Top`
([stage3-all-claims.log](evidence/stage3-all-claims.log)).  The backend reports
the claims as trivial after functional normalization; this is not accepted on
its own as validation, which is why the functions and rules are audited in
Stage 5.

The fresh LLVM definition was concretely compared with trusted Python on eight
normal/boundary inputs: empty, singleton zero, a tie-break pair, the
distinguishing example, duplicates, a length-four case beyond the symbolic
theorem, a seven-element large-integer case, and the negative supplemental
example.  All K results matched Python.  A first reviewer harness run visibly
produced the right K results but mis-parsed them due to an over-escaped regular
expression; both that failed harness log and the corrected zero-mismatch rerun
are preserved as
[stage3-concrete-compare.log](evidence/stage3-concrete-compare.log) and
[stage3-concrete-compare-rerun.log](evidence/stage3-concrete-compare-rerun.log).

## 4. Adequacy and real-program pinning

### Claim meanings

The candidate claims establish the following, under its generated semantics:

| Claims | Plain-language precondition and postcondition |
|---|---|
| `count-correct` | For any mathematical integer `N`, executing `count_ones(N)` returns the generated semantics' `popcount(N)`. |
| `comparator-correct` | For non-negative `A,B`, executing `comes_before(A,B)` returns the tuple-order predicate `beforeEq(A,B)`. |
| `insert-empty` | For any `X`, inserting into `[]` returns the model singleton. |
| `insert-at-front` | For any nonempty `Y::YS` satisfying `beforeEq(X,Y)`, insertion returns the model's front-insertion result.  There is no general recursive insertion claim for the opposite branch. |
| `sort-empty-symbolic`, `sort-singleton-symbolic` | Exact model equality for lengths zero and one. |
| `sort-pair-before`, `sort-pair-after` | Exact model equality for both comparator outcomes at length two. |
| six `sort-triple-*` claims | Exact model equality for the six path partitions at length three. |
| `example-one`, `example-three`, `empty`, `duplicates`, `wide-popcounts`, `negative-extension` | Exact returned lists for six fixed inputs. |
| `example-ordered`, `example-permutation` | Two true mathematical checks for one fixed distinguishing example only. |

Every entry RHS fixes the complete returned `listV`; there is no free result,
existential oracle, tautological implication, or unconstrained output.

The six triple preconditions are satisfiable and jointly partition their
three-comparison path space.  Concrete witnesses used in the audit are:
`[0,1,3]`, `[1,0,3]`, `[3,0,1]`, `[0,3,1]`, `[1,3,0]`, and `[3,1,0]`
for `abc`, `bac`, `bca`, `acb`, `cab`, and `cba`, respectively.  Witnesses for
the pair branches are `[1,3]` and `[3,1]`; helper and all remaining entry
claims also have concrete satisfying states.  All 22 witness results agree
with the mathematical model and both Python implementations; see
[claim_witnesses.py](evidence/claim_witnesses.py) and
[stage4-claim-witnesses-rerun.log](evidence/stage4-claim-witnesses-rerun.log).

### Program identity

The `<k>` entry terms use `#run(solutionProgram, ...)`.
`solutionProgram` expands to `solutionDefs`, whose constructor tree is a
literal copy of all four submitted function bodies.  Independently expanding
the macro and parsing the freshly regenerated `solution.mpy` produced
byte-identical KORE with SHA-256
`9a96d862db22077a3e400f6230d59118251f082ee1d8fd8b26e24fb749ee635b`.
See [stage4-program-kore-identity.log](evidence/stage4-program-kore-identity.log).
Thus the claims pin the submitted program, not a substituted implementation.

### Fatal adequacy gap

There is no entry claim for an arbitrary symbolic `Ints`, no induction or
recursive invariant, and no general recursive-insertion theorem.  The
exhaustive symbolic entry proof is exactly bounded to lengths 0, 1, 2, and 3.
Claims on lengths 5 and 6 are concrete examples, not universal theorems.
Neither `allNonnegative` nor `ordered`/`sameMultiplicity` is used to state a
universal source-contract theorem.

The source contract has no list-length bound.  Consequently the candidate does
not prove the requested partial-correctness property for lists of length four
or greater.  Finite differential tests and successful concrete `krun` runs
cannot fill that proof gap.

## 5. Rule-by-rule static soundness review

There are no generated helper K files.  The exhaustive lexical inventory is
[stage5-source-inventory.log](evidence/stage5-source-inventory.log): 23 syntax
sentences and 57 rules in `semantic.k`, six syntax sentences and 19 rules in
`verification.k`, and 22 claims in `spec.k`.

### Declarations and construct coverage

`MPY-SYNTAX` declares `Module`; statement lists; `FuncDef`, `If`, and `Return`;
parameter/string/expression/comparison lists; integer, Boolean, name, unary,
binary, Boolean, comparison, call, attribute, list, and subscript expressions;
comparison operators; slices; and bounds.  Runtime declarations provide
integer lists (`.Ints`, `::`), values, argument lists, definitions, outcomes,
the interpreter functions, and the sole `<k>` configuration.

The submitted constructor tree uses:

- `Module`/`FuncDef`/one- and two-argument `Params`, covered by
  `#run`, definition lookup, call, and invoke rules at
  `semantic.k:89-103`;
- `If` and `Return`, covered at `semantic.k:106-119`;
- `Name`, `Call`, `Attribute(...,"bit_count")`, `BoolOp`, and one-link
  `Compare`, covered at `semantic.k:121-145`;
- `Int(0)`, `Int(1)`, empty/singleton `ListExpr`, subscript zero, slice
  `1:`, and list `+`, covered at `semantic.k:121`, `140-160`, and
  `186-190`; and
- integer comparison, Boolean combination, and bit count, covered at
  `semantic.k:166-180`.

No used constructor is fabricated or left unmodeled.  Heap, mutation, object
identity, I/O, exceptions, and allocation cells are omitted; the submitted
well-typed program is pure and observes only integer/list values.

There are two `[symbol]` constructors (`intsCons`, `valsCons`), ordinary
`[function]` declarations, and two `[macro]` syntax productions.  There are no
`[total]`, `[functional]`, `[simplification]`, `[concrete]`, priority, `owise`,
or opaque declarations.  No priority rule can preempt execution.

### `semantic.k`: all 57 rules

Each item below explicitly accounts for the indicated rule.

- `89 #run` calls the submitted `sort_array`; `91` definition-hit and `92`
  guarded definition-miss implement first matching global definition; `96`
  composes lookup and invocation; `99` and `101` bind the one- and
  two-parameter functions; `104` unwraps a returned value.  These seven rules
  are faithful on the unique function names and exact arities in the program.
- `106` maps statement-list exhaustion to normal completion; `107` performs
  abrupt return and ignores the suffix; `109` evaluates an `If`; `112` and
  `115` are disjoint true/false branches; `118` preserves return across the
  suffix; `119` continues after normal branch completion.  These seven rules
  correctly model the actual control paths.
- `121` integer, `122` Boolean, `123` name, and `124` environment lookup are
  direct.  `125` unary, `127` binary, `129` Boolean, and `131` comparison
  expressions recursively evaluate operands.  `133` handles `len`, `135`
  handles the `bit_count` method, and `137` handles user-function names under a
  guard disjoint from `len`.  `140` constructs lists; `142` indexes an
  expression; `144` handles exactly slice `1:`.  All 14 rules are correct for
  the submitted well-typed calls.

  Rule `129` is eager whereas Python `and`/`or` short-circuit.  Its full syntax
  domain is therefore broader than the demonstrated language fragment.
  However, every Boolean operand in the submitted comparator is pure, total on
  integer arguments, side-effect-free, and exception-free, so eagerness cannot
  change a branch, value, state, or normal termination for any intended input
  reaching this function.  There is no intended-program false-conclusion
  witness, so this is recorded as a generality/evidence gap, not labeled an
  unsound proof rule.
- `147`/`148` evaluate empty/nonempty argument lists; `151`/`152` evaluate
  empty/nonempty list literals; `155` extracts an integer; `157` implements
  unary minus; `159` integer addition; `160` list concatenation; `161` guarded
  modulo; and `163` guarded integer division.  These ten rules are
  sort-disjoint where operators overlap.  The program uses only list
  concatenation; modulo/division are also used internally by positive
  `bitCount`.  Potential Python corner behavior for negative `//` is outside
  every submitted expression and cannot enable a false candidate conclusion on
  the intended program.
- `166` integer equality; `167` empty-list equality; `168` nonempty-versus-empty;
  `169` empty-versus-nonempty; `170` integer `<`; and `171` integer `<=` are
  truthful and pairwise sort/shape-disjoint.  Nonempty-to-nonempty list equality
  is intentionally absent, but the submitted program compares only against
  `[]`, so the used cases are complete.
- `173` Boolean `and` and `174` Boolean `or` implement their value tables.
  Short-circuit control is addressed at rule `129`.
- `176` bridges the modeled `bit_count` call to `bitCount`; `177` reduces a
  negative integer to its magnitude; `178` is the zero base case; `179`
  recursively sums the low bit for positive integers.  Guards
  `N<0`, `N=0`, and `N>0` are disjoint and exhaustive, and positive division by
  two descends.  These four rules compute Python's magnitude bit count over
  mathematical integers; they do not encode the sorting answer.
- `182` delegates modeled `len`; `183`/`184` recursively calculate list
  length; `186` returns index zero of a nonempty list; `187` returns its tail;
  `189`/`190` recursively append lists.  These eight rules are mathematically
  correct.  Unsupported indices/slices or empty indexing visibly stick rather
  than fabricating a result, and actual control guards prevent them.

Function-rule overlaps are either syntactically disjoint or guard-disjoint:
lookup hit/miss, true/false `If`, builtin/user call, expression/slice
subscript, typed `+`, list-empty comparisons, and the three bit-count cases.
There is no declared totality obligation, and every partial function case
reached by the submitted program on well-typed integer lists has coverage.

### `verification.k`: all 19 rules

- `11 solutionProgram` and `12 solutionDefs` are macro expansion rules.  They
  do not summarize or skip execution; KORE identity and body sensitivity
  independently validate them.
- `68 popcount` is a definitional alias to the audited `bitCount`; `70`
  defines lexicographic `(popcount, decimal)` order.
- `74` empty insertion, guarded `75` front insertion, and guarded `77`
  recursive insertion are complementary and truthful.  `80`/`81` define
  recursive model sorting.
- `83` empty ordering, `84` singleton ordering, and `85` adjacent recursive
  ordering are truthful.  `87`/`88` truthfully recognize all-non-negative
  lists, although no target entry claim uses that predicate.
- `90` empty occurrence count, `91` equal-head occurrence, and guarded `92`
  unequal-head occurrence are disjoint and truthful.
- `98` ends the finite probe list for `sameMultiplicity`; `99` checks the
  current probe value then recurses.  These equations are true.  The helper
  alone does not exclude a novel output value absent from the probe list, so
  its comment is stronger than the predicate in isolation.  The only claim
  using it is a fixed output already produced by `sortModel`; no universal
  permutation theorem is claimed or proved.

The model functions occur on postcondition sides and never rewrite a submitted
program invocation.  There is no operational bridge, fresh result-bearing
symbol, oracle, proof-specific simplification, or task-answer rule.  `popcount`
shares the primitive `bitCount` implementation rather than independently
formalizing CPython, which is listed as a trust boundary in Stage 7.

### Operational/body sensitivity

As a fresh test, the executed macro body—not merely external `solution.py`—was
mutated so that the empty branch returns `[99]`.  Its expanded program KORE
changed from
`9a96...635b` to `b63c...81a5`
([stage5-body-mutation-kore.log](evidence/stage5-body-mutation-kore.log)).
The original empty-result obligation then parsed/built but failed with a stuck
state containing `listV(99 :: .Ints)`, exit 1
([stage5-body-mutation-proof.log](evidence/stage5-body-mutation-proof.log)).
The preserved mutation sources are
[verification-body-mutation.k](evidence/verification-body-mutation.k) and
[spec-body-mutation.k](evidence/spec-body-mutation.k).

## 6. Fresh non-vacuity test

The reviewer-created mutation
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) changes the expected last
element for input `[1,5,2,3,4]` from `5` to `6`.  The precondition is
satisfiable, and both trusted Python implementations concretely return
`[1,2,4,3,5]`.

The exact dry-run command successfully compiled the mutated claim and exited 0
([stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log)).  The
ordinary proof command then exited 1 with `WarnStuckClaimState`; its residual is
the actual `listV(1 :: 2 :: 4 :: 3 :: 5 :: .Ints)`, which does not unify with
the false destination.  See
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log).  This is the
expected unmet result obligation, not a parse error, timeout, missing import,
or unrelated crash.  The proof is non-vacuous over its claimed cases.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the candidate's generated K theory, the successful reachability proof
establishes exactly:

1. the four helper facts listed in Stage 4;
2. exact `sortModel` equality for every integer list of length at most three,
   split across explicit path claims;
3. exact outputs for six fixed longer/boundary examples; and
4. orderedness and probed multiplicity for one fixed model result.

It does **not** establish sorting, orderedness, multiplicity preservation, or
canonical equivalence for an arbitrary-length input list.

### Trust ledger

- **K toolchain and builtins:** K `INT`, `BOOL`, `STRING`, and `MAP`
  operations, parsing, LLVM execution, Haskell symbolic execution, and the
  correctness of `kompile`/`kprove` are foundational trust.  All target claims
  depend on them.
- **Trusted translator/source mounts:** byte identity of the trusted prompt and
  translator and mechanical KORE identity connect the claims to the submitted
  AST.  This boundary is strong and reproducible.
- **Generated Python-subset semantics:** the 57 rules are the candidate's
  language model, not a supplied trusted definition.  Static review found no
  intended-program false rule witness or task-answer shortcut; fresh concrete
  comparisons support the used fragment.  Short-circuiting and CPython resource
  exceptions are abstracted as described above.
- **`int.bit_count` bridge:** `evalBitCount` and `bitCount` are transparent
  mathematical equations, not opaque symbols.  Their agreement with CPython is
  audited by the magnitude/halving definition and finite execution evidence,
  not by a second formal Python semantics.  `popcount` reuses this primitive,
  so `count-correct` is not independent evidence for the bridge.
- **Finite empirical evidence:** 13,347 Python differential inputs and eight K
  executions support only those tested bridges and inputs.  They do not prove
  arbitrary length, semantic equivalence, or termination.
- **No opaque/oracle boundary:** there are no fresh uninterpreted
  result-bearing symbols, proof-local operational bridges, simplification
  lemmas, totality assertions, or priority rules.

### Gate results and verdict

- Gate A (local real-program soundness and non-vacuity): **PASS** for the 22
  claims actually stated.
- Gate B (source-contract adequacy): **FAIL**.  Symbolic entry coverage is
  bounded to length three, while the HumanEval domain is unrestricted.
- Gate C (trust/evidence accounting): **PASS with the explicitly recorded
  generated-semantics and resource abstractions**; finite evidence is not
  promoted to proof.

In generic Kit terminology this is `SOUND-BUT-LIMITED`.  The benchmark prompt
explicitly maps a material HumanEval-domain narrowing of that kind to
`FAIL / NOT_LEGIT`, not to `CONCERNS / LEGIT`.  The fixed examples and bounded
unrollings cannot constitute the requested unrestricted partial-correctness
proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
