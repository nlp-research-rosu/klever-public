# Independent adversarial audit: 88-sort-array

The candidate proof reconstructs successfully and is non-vacuous, but it is not
a proof over the full real input domain.  Its two purported length-at-least-two
claims quantify over heap values containing a new `snocVS` term.  Such values
are not the constructor-only `ValSeq` values used for real MPython lists, and
the candidate supplies no sound connection from the former representation to
the latter.  A priority rule then gives last-index behavior directly to that
new representation.  Thus the successful claims cover empty and singleton real
arrays, plus artificial proof-local list values, rather than all non-negative
integer arrays required by the problem.

All executable work was done below `/tmp/audit-work/88-sort-array`.  Candidate
compiled artifacts and caches were not copied or used.  Reviewer scripts,
split claims, mutations, exact commands, exit statuses, and bounded outputs are
under `/audit-output/evidence/`.  The environment was K v7.1.337 and Python
3.10.12 (`evidence/environment.log`).

## 1. Input and provenance integrity

The rendered mode and trusted mounts are coherent: this is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` exists.  A recursive
`diff -r --no-dereference` between the trusted and candidate
`reference-semantics/` trees exited 0.  Neither tree contains a symlink.
`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted counterparts.  Required proof/program sources are regular files.
Hashes and all checks are recorded in `evidence/stage1-integrity.log`.

The requested provenance files are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace

Consequently there were no generation claims in those files to inspect.
`/candidate/__pycache__/` and its two `.pyc` files are non-source extras; they
were ignored.  `concrete_tests.py`, `concrete_tests.mpy`, and `prove.sh` are
also extra evidence rather than trusted inputs.  There is no infrastructure
mode/mount contradiction, so the audit proceeds to a candidate verdict.

Evidence: `evidence/stage1_integrity.sh`,
`evidence/stage1-integrity.log`, `evidence/setup_scratch.sh`, and
`evidence/scratch-setup.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for any list of non-negative integers, return a new
list containing the same elements sorted ascending when the sum of the first
and last elements is odd, otherwise descending.  The empty result is empty.
The input list must not be changed.  The trusted canonical implementation uses
`sorted(array, reverse=(array[0] + array[-1]) % 2 == 0)` after handling empty
input.

`/candidate/solution.py` implements the same cases:

1. falsey/empty list returns a fresh `[]`;
2. odd endpoint parity returns `sorted(array)`;
3. otherwise it returns `sorted(array, reverse=True)`.

This is valid on the stated domain, including singleton lists: `F + F` is even,
so the descending branch is selected but returns the same singleton value in a
fresh list.

Running the trusted `/reference/py2mpy.py` over the submitted `solution.py`
produced a file byte-identical to `/candidate/solution.mpy`; both SHA-256 hashes
are
`69de41f5b2532bca90ef608aca79778b308b53a10f51745f7c746c1f15f88496`.
See `evidence/stage2-translation-identity.log`.

The independent differential test imports the trusted canonical entry point and
the submitted generated entry point separately.  It checks the four documented
examples, 18 explicit empty/singleton/parity/duplicate/large-integer boundary
cases, every array of lengths 0 through 5 over values 0 through 4, and 1,000
seeded arrays of lengths 0 through 30.  Across 4,928 executions it observed both
parity branches, found zero result mismatches, zero input mutations, and zero
failures of fresh-copy identity.  Exact inputs are in
`evidence/differential-inputs.json`; the test and command are in
`evidence/differential_test.py` and `evidence/stage2-differential.log`.
This is strong finite fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

The scratch tree contains candidate source files, the trusted translator and
canonical source, and a fresh copy of the trusted supplied semantics.  It
contains no candidate-built K definition.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0.  The warnings concern non-exhaustive total functions in supplied,
unused language areas and the deliberately total/underspecified
`valSeqAt`; none prevented the build
(`evidence/stage3-kompile-concrete.log`).

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

Exit 0 (`evidence/stage3-kompile-proof.log`).

The unmodified aggregate positive spec exited 0 and printed `#Top`
(`evidence/stage3-kprove-all-positive.log`).  I also split the four claims
without changing their configurations or conditions and ran each independently:

| Claim | Result | Evidence |
|---|---:|---|
| empty | exit 0, `#Top` | `evidence/stage3-kprove-empty.log` |
| singleton | exit 0, `#Top` | `evidence/stage3-kprove-singleton.log` |
| odd length >= 2 | exit 0, `#Top` | `evidence/stage3-kprove-odd.log` |
| even length >= 2 | exit 0, `#Top` | `evidence/stage3-kprove-even.log` |

The split source claims are preserved under `evidence/positive-claims/`.

A reviewer harness was made by taking the exact bytes of `solution.py` as its
prefix, appending normal and boundary assertions, translating with the trusted
translator, and running with the fresh LLVM definition.  The corrected run
exited 0 with `.K`, `NoExc`, and exit code 0
(`evidence/stage3-krun-concrete-corrected.log`).  The earlier
`evidence/stage3-krun-concrete.log` is intentionally preserved: it failed
because the reviewer initially gave `[3,0,2]` a descending expected result
despite its odd endpoint sum.  The corrected oracle expects `[0,2,3]`; this was
a reviewer test error, not a candidate divergence.

These results establish fresh closure under the supplied theory.  They do not
by themselves establish that the successful symbolic preconditions denote real
program inputs.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

- Empty: calling `sort_array` with heap reference 0 pointing to an empty list
  returns fresh reference 1 pointing to an empty list, preserves reference 0,
  advances `heapLoc` from 1 to 2, restores the caller environment, empties the
  stack, and leaves return/exception/exit state normal.
- Singleton: for `F >= 0`, the same call returns fresh reference 1 containing
  `condRev(sortVS([F]), true)` and preserves the input.
- Odd: for `F,L >= 0`, a non-negative symbolic `MIDDLE`, and
  `pyMod(F+L,2) == 1`, the call returns fresh reference 1 containing
  `sortVS(vCons(F, snocVS(intsVS(MIDDLE), L)))` and preserves the input.
- Even: under the analogous even parity precondition, the result is fresh
  reference 1 containing the reverse of that `sortVS` term.

The returned reference and heap contents are constrained; none of the claims
has a free result or tautological postcondition.  There is no loop or helper
claim.

`sortArrayBody` in `verification.k` is structurally the same body as the
trustedly regenerated `solution.mpy`, including empty handling, endpoint
lookups, parity comparison, and both `sorted` calls.  `sortArrayClosure` binds
that body at definition environment 0.  The call then uses the supplied normal
callee lookup, parameter binding, frame, return, and allocation rules.  Thus
the body is not replaced by a whole-function answer rule.  It is manually
duplicated rather than loaded from the `.mpy` file, but translation identity and
the exact structural comparison pin that duplicate to the current submitted
program.

Concrete substitutions for the four written preconditions are:

| Claim | Substitution/input | Python result |
|---|---|---|
| empty | `[]` | `[]` |
| singleton | `F=5`, `[5]` | `[5]` |
| odd | `F=2`, `MIDDLE=[4,3,0,1]`, `L=5` | `[0,1,2,3,4,5]` |
| even | `F=2`, `MIDDLE=[4,3,0,1,5]`, `L=6` | `[6,5,4,3,2,1,0]` |

Both Python implementations agree on every substitution
(`evidence/stage4-ground-witnesses.log`).  The last two substitutions do produce
satisfiable *formal* claim states when inserted literally, but those formal
states contain `snocVS` in the heap.  That is the decisive distinction.

### Material representation and coverage defect

Real lists in the supplied semantics are `list(ValSeq)` values whose concrete
sequence is built from `.ValSeq` and `vCons`.  List literals allocate exactly
that representation (`semantics/list.k:14-15`), and no real MPython operation
constructs `snocVS`.  The candidate adds:

```text
syntax ValSeq ::= snocVS(ValSeq, Val)
```

without `[function]`, `[total]`, `[anywhere]`, or a representation invariant.
Its two bare rules only compute a `snocVS` term when that proof-local
computation is active; they do not normalize a `snocVS` term stored inside the
heap.  Therefore the odd/even LHS

```text
list(vCons(F, snocVS(intsVS(MIDDLE), L)))
```

is a new proof-local value shape, not a pattern for the ordinary concrete
sequence `F ++ MIDDLE ++ [L]`.

This is machine-visible:

- With the endpoint bridge removed, even the ground term
  `snocVS(vCons(4,vCons(3,.ValSeq)),5)` remains under `vsLen`/`valSeqAt`, and
  the claimed last-index connection fails with a genuine residual
  (`evidence/stage5-connection-ground-no-bridge.log`).
- The universal connection restricted to `intsVS(IntSeq)` also fails, as does
  the bridge's complete `M:ValSeq` match domain
  (`evidence/stage5-connection-intseq-no-bridge.log` and
  `evidence/stage5-connection-complete-domain-no-bridge.log`).
- A direct ground reachability attempt from the heap containing that `snocVS`
  term to the corresponding ordinary constructor-only heap fails: `.K` is
  reached with the `snocVS` heap unchanged, so it does not unify with the
  ordinary-list destination
  (`evidence/stage5-representation-connection.log`).
- Removing only the bridge makes the quantified odd entry claim fail exactly
  at its unresolved negative-index value
  (`evidence/stage5-odd-entry-no-bridge.log`).
- For contrast, independently written claims over the real constructor-only
  lists `[2,4,3,5]` and `[2,4,3,6]` both close through fixed indexing and the
  real body (`evidence/stage5-actual-ground-odd.log` and
  `evidence/stage5-actual-ground-even.log`).  These two finite claims are not
  instances of the candidate's quantified `snocVS` preconditions and do not
  repair universal coverage.

Accordingly, the empty and singleton claims cover real arrays, but the two
claims intended to cover every longer array do not.  This is a material
real-program/input-domain pinning failure, not merely thin test evidence.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.tsv` is a line-addressable exhaustive inventory with
the exact source block for every local module/import, configuration, syntax
declaration, context, and rule.  Its corrected summary is
`evidence/rule-inventory-summary.txt`:

- 1 configuration;
- 232 syntax declarations;
- 5 contexts;
- 704 rules total: 695 trusted supplied-semantics rules and 9 candidate
  proof-local rules;
- 150 function declarations, 111 `total` declarations, 25 `symbol`
  declarations, 22 `no-evaluators` declarations, 46 priority-bearing entries,
  26 `owise` entries, 36 concrete entries, 4 macros and 1 recursive macro;
- no local `[functional]` or `[simplification]` declaration.

Under `SUPPLIED_SEMANTICS`, the recursively identical trusted tree is the fixed
semantics baseline; it does not bless the nine candidate rules.  I reviewed all
695 supplied entries for overlap with this program.  Unused syntax and rules
are inert for these claims.  The used construct mapping is:

| Program construct | Declaration/behavior used |
|---|---|
| `Module`, `FuncDef`, parameters | `syntax.k`; closure creation/frame rules in `functions.k` and `call.k` |
| `Call`, `Name`, arguments | left-to-right lookup/evaluation in `core.k` and `call.k` |
| `If`, `not array` | strict condition, heap-ref dereference, `truthy(list(...))` in `controls.k`, `bool.k`, `core.k` |
| empty `ListExpr` | argument evaluation plus fresh `#alloc` in `list.k`/`core.k` |
| `array[0]`, `array[-1]` | contexts/dereference/index normalization in `subscript.k`; unary minus in `int.k` |
| integer `+`, `%`, `==` | dispatch in `operators.k`; exact integer equations and `pyMod` in `int.k` |
| `KwArg("reverse", true)` | left-to-right tagged argument evaluation in `core.k` |
| `sorted` | builtin scope/lookup/call dispatch, fresh allocation, opaque `sortVS`, and `condRev`/`revVS` in `sort.k` |
| `Return` | return value, frame pop, environment/scope restoration in `functions.k` |

The used fixed rules have consistent evaluation order and cell effects:
callee and arguments evaluate left to right; list operands are dereferenced
read-only; `sorted` allocates a fresh heap object and advances `heapLoc`; the
input heap entry is preserved; calls push/pop a frame and restore `env`,
`scopeLoc`, `stack`, and `ret`; the program has no output or other mutable cell.
Priority rules used here narrow only heap dereferencing or the exact sorted
dispatch.  The empty guard prevents the two in-bounds endpoint reads from
executing on the empty list.

The supplied `sortVS(ValSeq)` is
`[function,total,symbol(sortVS),no-evaluators]` for symbolic proof.  Its
`[concrete]` equations implement insertion sort for integer lists in LLVM.
This is an explicit low-level external-builtin trust boundary, not a theorem in
the candidate: the symbolic proof establishes a result containing `sortVS`,
conditional on interpreting it as Python's ascending `sorted`.  The supplied
`revVS` and `condRev` equations truthfully reverse a sequence.  Concrete K
execution and the 4,928-case Python differential support the sort bridge
finitely, but do not universally prove it.  Treating a fixed builtin sort as an
external primitive is acceptable in principle; it is not the cause of the
verdict.

The compiler warns that supplied `valSeqAt` is declared total without a rule
for empty/out-of-bounds or opaque sequences.  On real intended inputs the
program only indexes after excluding empty, at indices 0 and -1, so this
underspecified branch is not reached.  Other opaque supplied float, digest,
key-sort, and string operations are inventoried but do not occur in the
program or claims.

### Candidate extension dispositions

1. `sortArrayBody` and its one equation: a total nullary definitional constant.
   Its RHS is exactly the submitted body.  It does not skip body execution.
2. `sortArrayClosure` and its equation: a total nullary definitional constant
   with the exact parameter, body, and definition environment.  It dispatches
   through normal call semantics.
3. `intsVS` and its two equations: a total, structurally recursive, disjoint,
   exhaustive conversion on the two `IntSeq` constructors.  Mathematically
   valid.
4. `nonNegativeIS` and its two equations: total, structurally recursive,
   disjoint, and exhaustive on `IntSeq`.  Mathematically valid.
5. `snocVS` and its two equations: the equations give the usual append-one
   result when the term is actually evaluated over `.ValSeq`/`vCons`.  The
   symbol is not declared a function/total operation and its equations do not
   make stored heap occurrences definitional.  It also extends the `ValSeq`
   value domain.  The narrow finding is a missing representation connection,
   not a demonstrated false mathematical append equation.
6. The final priority-40 subscript rule is an operational bridge.  Its complete
   match is
   `Subscript(list(vCons(_F,snocVS(_M,L))), UnaryOp("-",Int(1)))` at the head of
   any continuation.  It reads/writes only the `<k>` cell, preserves the
   continuation and every other cell, returns `L`, and affects the parity
   branch and final result.  It preempts normal unary-index evaluation and
   `valSeqAt`.

For the final rule, there is no bridge-free universal theorem over either its
complete `M:ValSeq` domain or even the `intsVS(IntSeq)` domain used by the
claims.  The recorded connection attempts fail.  Its broad continuation is
not itself control-destructive because it replaces a pure expression with a
value and preserves the suffix.  The endpoint equation is consistent with the
*intended* informal meaning of append-one, so I do not claim a concrete false
value witness for it and do not label that equation mathematically false.
Instead, the evidenced defect is narrower and decisive: the rule fabricates
index behavior for the proof-local value shape that makes the symbolic claims
close, while no theorem connects that shape to real list states.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`.  The fresh
`evidence/spec-vacuity.k` keeps the satisfiable empty-input pre-state but
changes the result-bearing heap obligation from a fresh empty list to a fresh
singleton `[0]`.

The dry run:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, proving the mutation parses and builds
(`evidence/stage6-vacuity-dry-run.log`).  The actual proof command exited 1
with `WarnStuckClaimState`.  Its residual has `ref(1)` returned and heap
`1 |-> list(.ValSeq)`, which cannot unify with the claimed singleton.  This is
the expected reachable unmet result obligation, not a parser/import/backend
failure (`evidence/stage6-vacuity-proof.log`).

Therefore the submitted proof is discriminating and result-constraining.  This
successful non-vacuity check does not cure its input-representation coverage
failure.

## 7. Proven versus assumed accounting

What the successful reachability proof actually establishes, under the
extended theory, is:

- on the exact empty real-list configuration, terminating execution returns a
  fresh empty list and preserves the input;
- on singleton real-list configurations with a non-negative integer,
  terminating execution returns a fresh reverse-of-`sortVS` singleton and
  preserves the input;
- on configurations whose heap contains the proof-local
  `vCons(F,snocVS(intsVS(MIDDLE),L))` value, terminating execution returns a
  fresh `sortVS` value or its reverse according to endpoint parity and
  preserves that proof-local input.

It does **not** universally establish the result for ordinary concrete
constructor-only lists of length at least two.

The trust/assumption ledger is:

| Boundary | Dependents | Accounting |
|---|---|---|
| K v7.1.337 parser/compiler/Haskell/LLVM backends and built-in integer/Boolean/map/list theories | all builds and proofs | unavoidable tool trust; fresh builds and explicit statuses recorded |
| supplied MPython semantics, byte-identical to trusted mount | all semantic execution | selected fixed semantics baseline; used path statically mapped and concretely exercised |
| manual `sortArrayBody` duplicate | all four claims | exact current AST identity established from the trusted translation; not an opaque result summary |
| `sortVS` symbolic primitive | all non-empty postconditions | externally trusted builtin-sort interpretation; concrete K execution plus finite differential evidence, but no universal K sort theorem |
| `valSeqAt` totality outside its equations | endpoint indexing | acceptable only because real endpoint reads are in bounds; opaque/OOB interpretations are excluded |
| proof-local `snocVS` representation and priority endpoint bridge | both length>=2 claims | illegitimate for the claimed real-domain coverage: no fixed-semantics representation or universal operational connection |
| Python canonical differential | implementation/intent and opaque-sort support on 4,928 cases | finite empirical evidence only, not a K proof |
| partial-correctness interpretation | every claim | termination is not proved; if a covered execution terminates, its claimed post-state follows |

For completeness, the supplied tree's full local `symbol`/opaque inventory is:
`sortVS` (used); and `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`,
`floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF` (all unused by this
program and its claims).  The proof therefore cannot depend on an
interpretation of any unused opaque symbol.  The only empirical bridges are
the 4,928-case canonical/generated/contract comparison and the corrected
finite LLVM K harness.  The informal arguments are the exact manual AST
structural comparison, the intended interpretation of `sortVS` as ascending
Python sorting, and the observation that append-one should have last element
`L`; the latter is specifically not accepted as a substitute for the missing
formal `snocVS` representation connection.

Missing provenance logs and the absence of a candidate proof report do not
substitute for any proof step; neither were used.  The fresh `#Top` results,
concrete tests, and false mutation are all genuine, but the formal theorem's
length>=2 preconditions do not pin real generated-program inputs.  That is a
material adequacy/real-program coverage failure and requires
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
