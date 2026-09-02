# Independent adversarial audit: 143-words-in-sentence

## Decision summary

The candidate's source implementation is faithful to the trusted canonical
implementation on the stated length domain, its submitted MiniPy translation is
byte-identical to a fresh translation, and both submitted positive K claims
reconstruct to `#Top` from source. The entry postcondition is result-constraining,
the fresh false-result mutation is rejected for the expected unmet equality, and
the K macro used by the entry claim expands to the exact submitted `solution.mpy`
AST.

Those facts do not make the proof legitimate. The successful proof relies on:

1. a priority rule at `/candidate/verification.k:220` which bypasses name
   lookup for `len`; its match domain permits a shadowing local `len`, and the
   loop claim quantifies over exactly such states through its arbitrary `REST`
   map; and
2. result-bearing `sentenceCodes` and `wordsVals` abstractions whose split and
   iteration behavior is asserted by priority rules without a bridge-free
   universal connection to concrete `IntSeq` strings and `ValSeq` lists.

The first issue has a concrete false-conclusion witness. On the contract-valid
input `"aa"` with a matching local scope containing `len = 4`, Python raises
`TypeError` and the fixed supplied semantics gets stuck at
`#applyK(toCall(4), ...)`; the candidate-extended semantics ignores that binding,
fabricates length 2, and completes an assertion that should not complete.
Removing just that bridge makes the loop proof fail. The second issue means the
entry theorem starts from an opaque symbolic string which no concrete sentence
can instantiate and therefore does not pin fixed-semantics execution on the
real input representation.

This is a candidate proof failure, not an infrastructure failure.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The required trusted directory
`/reference/reference-semantics` is present and is a real directory. There is
no mode/mount contradiction, so the audit proceeded to a candidate decision.

The independent type, entry, symlink, and SHA-256 checker is
`evidence/integrity_check.py`; its command, exit 0, and output are in
`evidence/01-integrity.log`.

- `/candidate/prompt.py` is a regular file and is byte-identical to
  `/reference/prompt.py`.
- `/candidate/py2mpy.py` is a regular file and is byte-identical to
  `/reference/py2mpy.py`.
- `/candidate/reference-semantics/` is recursively identical to the trusted
  semantics tree: 25 entries, with no missing, additional, changed, mistyped,
  or symlinked entry.
- The trusted baseline was used only as the selected fixed semantics. It does
  not validate any rule in `/candidate/verification.k`.

### Missing generation records

The following requested candidate artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present under `/candidate`. Their absence is
a provenance/auditability gap, not an infrastructure contradiction and not the
basis of the proof failure.

The top-level untrusted extras are `__pycache__/`, `kore-exec.tar.gz`,
`prove.sh`, `smoke.py`, `smoke.mpy`, and `spec.json`. No candidate-compiled
definition, Python cache, backend archive, prior trace, or prior output was used
as proof evidence.

All source needed for execution was copied to `/tmp/audit-work`; all definitions
were rebuilt there. `/candidate` remained read-only.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py` and `/reference/canonical.py`: for a sentence of
length 1 through 100 containing words in their original order, return one
space-separated string containing exactly those words whose lengths are prime.
The examples require:

- `"This is a test"` to produce `"is"`;
- `"lets go for swimming"` to produce `"go for"`.

The prompt says words are separated by a space and that the sentence contains
only letters. Read consistently with its multiword examples, the intended core
domain is alphabetic words separated by spaces. The submitted proof further
restricts this to nonempty ASCII alphabetic words separated by exactly one ASCII
space; that restriction is discussed under adequacy.

### Source review

`/candidate/solution.py:1-40` splits on whitespace, enumerates every prime from
2 through 97, retains a word exactly when its length is in that enumeration, and
inserts one space only between retained words. Because the stated total sentence
length is at most 100, a word cannot require a prime above 97. The unused
`_plain` local does not affect Python behavior.

### Trusted translation identity

Fresh command:

```text
python3 trusted/py2mpy.py source/solution.py > build/solution.regenerated.mpy
cmp -s build/solution.regenerated.mpy source/solution.mpy
```

Both files have SHA-256
`d6c23e7e5125adc01e2c7abdca0439b4a64d92a4fc1f3609e86d5653e2c4d808`.
The command exited 0. See `evidence/02-translation-identity.log`.

### Independent differential test

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and `/candidate/solution.py`. It records every input
in `evidence/differential-inputs.json` and every paired result in
`evidence/differential-results.json`.

The 976-case scope contains:

- both documented examples;
- the empty string (outside the stated nonempty contract);
- minimum length 1 and exact total length 100;
- every single-word length 1 through 100, exercising equality and non-equality
  at every branch of the prime disjunction;
- prime/composite and empty/nonempty-accumulator transitions in two-word cases;
- all-retained, none-retained, and mixed-retention cases;
- a leading/trailing/repeated/tab/newline whitespace extension; and
- 750 deterministic generated valid cases using random seed 143.

The command exited 0 with `case_count=976` and `mismatch_count=0`; see
`evidence/03-differential.log`. This is strong finite evidence that the generated
Python implementation matches the canonical Python implementation. It is not a
universal K connection theorem.

## 3. Clean proof reconstruction

K tool version for the reconstruction was v7.1.337. The scratch build used only
the copied source and did not reuse candidate caches or compiled definitions.

| Target | Exact command (arguments abbreviated only here; full shell-escaped command is in the cited log) | Exit / relevant result |
|---|---|---|
| Concrete supplied semantics | `kompile source/reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition build/runtime-kompiled` | 0; fresh definition, `evidence/04-kompile-runtime.log` |
| Concrete smoke execution | trusted retranslation, byte comparison, then `krun build/smoke.regenerated.mpy --definition build/runtime-kompiled` | 0; final `.K`, `NoExc`, exit code 0, `evidence/05-concrete-smoke.log` |
| Proof definition | `kompile source/verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition build/verification-kompiled` | 0, `evidence/06-kompile-verification.log` |
| Loop claim | `kprove source/spec.k --definition build/verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant --output pretty` | 0 and `#Top`, `evidence/07-kprove-loop.log` |
| Entry claim | `kprove source/spec.k --definition build/verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant,SPEC.words-in-sentence-correct --trusted SPEC.loop-invariant --output pretty` | 0 and `#Top`, `evidence/08-kprove-entry.log` |

The loop lemma was first proved without trusting a claim. The entry invocation
then used that independently closed lemma as trusted composition evidence.
Thus both submitted positive targets close under the submitted theory. The
static audit below shows why that theory is not sound enough to establish the
real-program theorem.

Because this is `SUPPLIED_SEMANTICS`, the generated-semantics-only concrete
cross-check requirement does not apply. The supplied runtime was nevertheless
rebuilt and exercised as shown above.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` at `/candidate/spec.k:8-43` says:

- begin at a `#loop` over `list(wordsVals(W))`, binding each item to local
  `word` and executing the exact submitted loop-body macro;
- the current local `result` is `str(A)`, `word` and `n` already exist, and
  `_plain` is 0;
- `$cells` is absent from the complete local map;
- after the loop, `<k>` is empty, `result` is
  `str(filterWords(A, W))`, `_plain` and every map remainder are preserved,
  while final `word` and `n` may be arbitrary values.

There is no validity or length guard on this helper claim. In particular,
`REST` is an arbitrary map and may contain a binding for `"len"`.

`SPEC.words-in-sentence-correct` at `/candidate/spec.k:48-84` says:

- start from the exact initial module configuration and load
  `solutionProgram`;
- call its `words_in_sentence` closure with
  `str(sentenceCodes(W))`;
- require `W` to be a sequence of nonempty ASCII alphabetic words and require
  the modeled single-space sentence length to be from 1 through 100;
- finish with return value `str(filterWords(.IntSeq, W))`;
- install the submitted function closure and allocate heap location 0 as
  `list(wordsVals(W))`; and
- leave the stack, return marker, exception marker, and exit code in their
  stated normal final states.

The entry postcondition is an equality to a recursively defined result. It is
not a free variable, tautology, or one-way implication.

### Submitted-program identity

The entry claim names a macro rather than reading the file at proof time.
Independent `kast --expand-macros` parsing under module `VERIFICATION` shows
that `solutionProgram` expands to the exact parsed `solution.mpy` module. The
two expanded JSON KAST files have the same SHA-256
`55200913c91914d654ca0dca55a86a4fc4b9978c4e7808bb065f82912a3186b7`.
See `evidence/macro-program.mpy` and
`evidence/09b-program-macro-identity.log`. Together with the trusted translation
identity, this rules out a substituted program AST.

`evidence/09-program-macro-identity.log` records an initial diagnostic parse
with the wrong parser module; it was discarded and corrected by the successful
module-explicit check above.

### Satisfying witness and claimed result

Take:

```text
W = ["This", "is", "a", "test"]
```

with each word represented by its ASCII `IntSeq`. This satisfies `validWords`;
`sentenceLen(W)` is 14, so both entry length bounds hold. The formal
`filterWords(.IntSeq, W)` result is ASCII `"is"`. The three ground K checks for
validity, length 14, and result `"is"` close with `#Top` in
`evidence/10c-ground-witness.log`; their source is
`evidence/ground-witness.k`. Both Python implementations also return `"is"`, as
recorded by the differential evidence.

Two earlier ground-harness attempts are retained in
`evidence/10-ground-witness.log` and `evidence/10b-ground-witness.log`; they were
rejected for proof-module syntax/functional-claim form and are not treated as
semantic evidence.

### Material real-input pinning failure

No rule defines `sentenceCodes(W)` as the concrete concatenation of the word
code sequences with code 32 separators. No rule defines `wordsVals(W)` as the
fixed `vCons(str(...), ...)` value sequence. Instead:

- `/candidate/verification.k:144-152` directly maps a `split` call on opaque
  `sentenceCodes(W)` to an allocated list containing opaque `wordsVals(W)`;
- `/candidate/verification.k:17-22` directly supplies iterator observations for
  opaque `wordsVals(W)`.

Consequently, even the ground witness above invokes the program on
`str(sentenceCodes(ground-W))`, not on the concrete character sequence for
`"This is a test"`. A concrete `iCons(...)` sentence cannot unify with the
distinct `sentenceCodes(...)` constructor. There is no bridge-free theorem
showing that fixed split produces the asserted list.

The audit compiled a bridge-free definition containing only the new data
declarations over the fixed semantics:

- with the candidate bridges enabled, the ground split and iterator claims
  close (`evidence/23-bridge-enabled-proof.log` and
  `evidence/25-iterator-enabled-proof.log`);
- without the bridges, fixed split gets stuck at
  `splitWS(sentenceCodes(...), .IntSeq, .ValSeq)` and cannot establish equality
  to `wordsVals(...)` (`evidence/24-bridge-free-proof.log`);
- without the bridge, `#iterNext(list(wordsVals(...)))` is irreducible
  (`evidence/26-iterator-bridge-free-proof.log`).

These failures are not offered as false-conclusion witnesses for the split or
iterator rules. They establish the narrower but decisive evidence gap: no
universal fixed-semantics connection exists in the submitted proof, so the
entry theorem is about a newly axiomatized abstract input/list representation,
not the concrete submitted program on actual sentence codes.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and used-language map

`evidence/static_inventory.py` inventories every declaration and rule by source
location and emits:

- `evidence/static-inventory.json`; and
- `evidence/static-inventory.md`.

The successful inventory log is `evidence/11b-static-inventory.log`. It contains
967 entries with zero unassessed candidate-local entries:

- supplied semantics: 695 rules, 227 syntax declarations, 5 contexts, and 1
  configuration;
- `verification.k`: all 25 rules and all 12 syntax declarations;
- `spec.k`: both claims.

The supplied 928 entries are byte/type-identical to the problem-selected trusted
semantics and are accepted at that explicit semantic boundary. The exact fixed
declarations and rules used by every construct in `solution.mpy` are mapped in
`evidence/program-construct-map.md`: module loading, function definition and
call frames, scope lookup, strict evaluation, split, allocation, list iteration,
loop binding, assignment, integer/string literals, Boolean short-circuiting,
comparison, string concatenation, conditionals, and return/frame popping.

`verification.k` has no simplification rule, `functional` declaration, or
proof-local claim. It has five `[function,total]` declarations, four macro
declarations, two semantically opaque projections, and ten priority-30
operational rules.

### Every candidate-local declaration

| Location | Decision |
|---|---|
| `verification.k:9-10` `WordSeq` | Sound free-algebra representation for structural induction. |
| `verification.k:15` `wordsVals` | Opaque result-bearing `ValSeq` projection; no constructor equations or connection theorem. |
| `verification.k:27` `sentenceCodes` | Opaque result-bearing `IntSeq` projection; no concrete-code equations or connection theorem. |
| `verification.k:29`, `35`, `43`, `57`, `68` | `sentenceLen`, `validWords`, `primeLength`, `selectWord`, and `filterWords` are total proof functions. Their rule decisions are below. |
| `verification.k:74`, `104`, `120`, `133` | `primeTest`, `solutionLoopBody`, `solutionBody`, and `solutionProgram` are macros. Expanded-program KAST identity confirms that these do not substitute a different AST. |

### Every candidate-local rule

| Rule location(s) | Class and decision |
|---|---|
| `verification.k:17`, `:20` | Operational iterator bridges. They state correct-looking empty/cons observations, but `wordsVals` has no bridge-free connection to fixed `ValSeq`. They are unproved result-bearing abstractions, not established consequences of list semantics. |
| `verification.k:30`, `:31`, `:32` | Truthful, disjoint structural equations for empty, one-word, and multiword modeled sentence length, including one separator per adjacent word. |
| `verification.k:36`, `:37` | Truthful structural equations requiring every modeled word to be nonempty and ASCII alphabetic. |
| `verification.k:44` | Exact membership in the primes through 97. This is truthful for every length reachable under the entry bound 1..100. It is not a global primality characteristic (for example it returns false at 101), so the name/comment must not be generalized beyond the theorem domain; this is not labeled unsound on the intended bounded domain. |
| `verification.k:58`, `:61`, `:65` | Truthful and disjoint selection cases: empty/nonempty accumulator for prime length and unchanged accumulator for nonprime length. The guards cover every bounded use. |
| `verification.k:69`, `:70` | Truthful terminating structural filter base/step equations. |
| `verification.k:75`, `:105`, `:121`, `:134` | Macro expansion rules. Independent expanded KAST identity establishes that the four expansions reproduce the submitted expression, loop body, function body, and module. They do not replace runtime execution after expansion. |
| `verification.k:144` | Result-bearing operational split bridge. It preserves allocation shape but replaces fixed recursive split with the asserted `wordsVals(W)` output. No bridge-free universal theorem covers its match domain. The bridge-free ground residual is recorded in `evidence/24-bridge-free-proof.log`. This is an unconnected abstraction/pinning failure; no stronger false-output label is asserted without a concrete interpretation theorem for the opaque constructor. |
| `verification.k:157` | Plain-frame target-binding shortcut. On entry-reachable and loop-precondition states, `$cells` is absent and it performs the same map update as `tuple.k:32-34`. Its complete syntactic match domain does not itself prohibit `$cells`; thus reuse outside the guarded theorem could preempt cell-write behavior. The audited claims keep the rule in the plain-frame subdomain, so this broader reuse risk is not used as the verdict witness. |
| `verification.k:178` | Existing-`n` assignment shortcut. RHS is already an `Int`; on the audited plain frame it matches the fixed current-scope update and preserves all other cells/map entries. |
| `verification.k:199` | Existing-`result` assignment shortcut. It is equivalent on the audited `$cells`-free states. Like the target-binding shortcut, its complete reusable match domain is broader than that state invariant, so it should have carried the same explicit no-cells guard. |
| `verification.k:220` | **Unsound operational bridge.** It rewrites `Call(Name("len"), Name("word"))` directly to `isLen(C)`, without resolving `Name("len")`, evaluating the callee, or checking that the selected binding is the builtin. `M` may contain a shadowing `"len"` binding. Concrete false-conclusion witness below. |
| `verification.k:237`, `:252`, `:267` | Direct lookup of explicit unique local entries `n`, `word`, and `result`. On audited plain-frame states, these agree with fixed scope lookup; subsequent ordinary evaluation/control remains intact. |

### Required false-conclusion witness for the unsound `len` rule

`evidence/len-shadow-witness.py` uses the contract-valid sentence `"aa"` and the
same local names/pattern required by the bridge, but puts `len = 4` in the local
map. Its translated call is exactly
`Call(Name("len"), Name("word"))`.

Observed results:

- Python: exit 1 with `TypeError: 'int' object is not callable`
  (`evidence/15-len-shadow-python.log`).
- Fixed supplied semantics: it resolves local `len` to 4 and gets stuck at
  `#applyK(toCall(4), str("aa"), .Vals)`; it does not finish the assertion
  (`evidence/16-len-shadow-fixed-krun.log`).
- Candidate-extended semantics: the priority-30 rule ignores local `len`, returns
  2, treats `"aa"` as selected, and reaches final `.K` with the false assertion
  accepted (`evidence/17-len-shadow-extended-krun.log`).

This is a direct false conclusion about control and result: the bridge-enabled
theory produces normal completion and `"aa"` where fixed execution has no
return. It is within the `len` rule's complete match domain and uses an intended
sentence input.

It also lies within the formal loop claim's quantified state domain: choose
`W = wCons(codes("aa"), .WordSeq)`, initial `A = .IntSeq`, and put
`"len" |-> 4` in `REST`. The loop precondition forbids only `$cells`, not
`"len"`. Therefore the invalid case is not merely an unrelated reusable-rule
case; it is included in a submitted positive helper theorem.

Dependency was checked by removing only lines 220-235 in scratch. The altered
definition compiled (`evidence/19-kompile-no-len.log`), but the loop proof then
exited 1 with `WarnStuckClaimState` at unresolved `#look("len", L)` and conditions
over whether `"len"` belongs to `REST`
(`evidence/21-kprove-loop-no-len.log`). This confirms that closure of the
submitted loop theorem depends on the invalid shortcut.

### Evaluation, state, and control summary

The fixed semantics enforces left-to-right strictness for the used AST nodes,
LEGB scope lookup, heap allocation for split results, one-time iterable
evaluation, iterator-driven loop steps, current-scope assignment, and
return/frame restoration. The entry claim pins every configuration cell and
normal exit. The candidate assignment/name shortcuts preserve the used
plain-frame footprint, and no exception or abrupt-return bridge is introduced
there.

The `len` bridge does not preserve binding or call control, as the witness
shows. The split/iterator bridges preserve the superficial heap/continuation
shape but introduce unconnected result-bearing values. Priorities make these
rules preempt the fixed execution paths; priority is not a justification for
their equivalence.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. The audit created the independent
`evidence/spec-vacuity.k`.

The mutation changes the entry's required returned codes from:

```text
filterWords(.IntSeq, W)
```

to:

```text
seqConcat(filterWords(.IntSeq, W), iCons(120, .IntSeq))
```

That is, it appends ASCII `"x"` to every expected result. For the satisfying
ground witness `"This is a test"`, both Python implementations and the formal
filter return `"is"`, not `"isx"`.

The dry run exited 0, proving that the mutation parses and builds:
`evidence/12-vacuity-dry-run.log`.

The actual proof exited 1 with `WarnStuckClaimState`. Its residual explicitly
requires the false equality:

```text
filterWords(.IntSeq, W)
  = seqConcat(filterWords(.IntSeq, W), iCons(120, .IntSeq))
```

The failure is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. See
`evidence/13-vacuity-proof.log`. The submitted entry claim is therefore
discriminating and result-constraining under its theory; the proof fails for
soundness/pinning reasons, not vacuity.

## 7. Proven versus assumed accounting

### What the successful reachability runs actually establish

Under the complete extended K theory in `/candidate/verification.k`:

- the abstract loop over `list(wordsVals(W))` transforms the accumulator
  according to `filterWords`; and
- loading the exact submitted program AST and calling it on the opaque value
  `str(sentenceCodes(W))` reaches
  `str(filterWords(.IntSeq, W))` with the specified normal final cells,
  assuming the entry guards.

That statement is partial correctness under the extended theory. It is not a
sound theorem of fixed supplied semantics for concrete sentence code sequences.

### Trust and assumption ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Entire byte-identical supplied semantics and K builtins/backend | Defines configuration, parsing, evaluation, maps, integer/Boolean/string operations, allocation, calls, loops, and reachability for all claims | Explicitly selected trusted boundary in `SUPPLIED_SEMANTICS`; acceptable. Compiler/backend execution remains ordinary tool trust. |
| Supplied opaque symbols: `md5hexCodes`; float symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`; sorting symbols `sortVS`, `sortKeyVS` | Present in the trusted definition | Exhaustively listed in `evidence/static-inventory.*`; none is reachable from `solution.mpy` or either target claim, so none supports this result. |
| `sentenceCodes(W)` | Determines the entry argument and all downstream split behavior | Illegitimate program-derived opaque abstraction: no concrete encoding equations and no bridge-free universal connection theorem. |
| `wordsVals(W)` | Determines allocated list contents, iteration, loop values, and ultimately the return | Illegitimate program-derived opaque abstraction: its only observers are asserted by candidate operational rules. |
| `filterWords`, `selectWord`, `primeLength`, `sentenceLen`, `validWords` | Determines guards and the postcondition | Equations are ordinary mathematics and truthful on the formal 1..100 domain. They specify the answer but do not by themselves prove that fixed execution computes it; that connection depends on the operational proof. |
| `solutionProgram`, `solutionBody`, `solutionLoopBody`, `primeTest` macros | Pin the executed AST | Acceptable: independent expanded-KAST identity connects them to the submitted translation. |
| `SPEC.loop-invariant` trusted by the entry invocation | Supplies loop induction | Illegitimate as submitted because its universal precondition includes shadowed-`len` states and its proof depends on the unsound `len` bridge. |
| Priority `len` bridge | Controls `n`, every prime branch, accumulator updates, and return | Illegitimate. Concrete false-conclusion witness and removal sensitivity are recorded. |
| Python differential testing | Bridges candidate Python to trusted canonical Python on 976 cases | Acceptable finite empirical support only. It does not connect concrete `IntSeq` strings to `sentenceCodes/wordsVals` and cannot replace the K theorem. |
| Ground example checks | Show a syntactically satisfiable `W`, modeled length 14, and modeled result `"is"` | Useful non-vacuity/adequacy evidence only. The K input remains opaque `sentenceCodes(ground-W)`, not concrete sentence codes. |
| Informal domain bridge | Interprets `WordSeq` as exactly-one-space-separated ASCII words | Limited and unproved. It excludes non-ASCII letters and leading, trailing, repeated, tab, or newline separators, even though Python `split()` handles the tested whitespace extension. |

The missing generation records reduce provenance auditability, but the decisive
negative result is independently reproducible from the candidate source. The
fresh builds, successful target runs, false mutation, operational witnesses, and
complete inventory are all preserved under `/audit-output/evidence/`. Diagnostic
harness mistakes are retained rather than hidden, and corrected successful
artifacts are explicitly identified above.

The candidate therefore contains a machine-closing proof only under an
unsound/unconnected proof extension. It is not a legitimate partial-correctness
proof of the real generated program on concrete intended inputs.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
