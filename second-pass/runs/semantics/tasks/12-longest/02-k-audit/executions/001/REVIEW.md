# Independent adversarial audit — 12-longest

The candidate does not contain a completed partial-correctness theorem for the
nonempty case.  Its individual proof fragments are sound and reconstruct to
`#Top`, but the only nonempty entry claim, `call-cons-dispatch`, stops after call
dispatch with the whole function body still on `<k>`.  It has no final returned
value in its postcondition.  Thus the successful proof runs do not establish
that a nonempty call returns the first longest string.

This is a candidate adequacy failure, not an audit-infrastructure failure.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as required.  The trusted mount
therefore does not contradict the rendered mode.

The independent type-and-hash traversal in
`evidence/integrity_audit.py`, run in `evidence/01-integrity.log`, found:

- candidate `prompt.py` is a regular file and byte-identical to
  `/reference/prompt.py` (SHA-256
  `aa62f2bdcae005c83ed5eede68f25a798ece3609af2bf7db30ef714aa7a33927`);
- candidate `py2mpy.py` is a regular file and byte-identical to
  `/reference/py2mpy.py` (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`);
- the candidate and trusted semantics trees each contain 25 entries;
  every relative name, entry type, and file hash agrees;
- none of the required source artifacts or semantics entries is a symlink,
  mistyped entry, changed file, missing entry, or additional entry.

The following requested generation/provenance artifacts are absent from
`/candidate`:

- `run-input.json`;
- `metrics.json`;
- `codex-last.txt`;
- `codex-output.log`;
- any structured generation trace.

There is also no `PROOF.md`.  These omissions prevent checking the generator's
own history or narrative, but they do not prevent independent reconstruction
from the mounted prompt, translator, sources, and supplied semantics.  The
candidate's `kore-exec.tar.gz`, Python bytecode cache, concrete tests, and
`prove.sh` were treated only as untrusted evidence.  In particular, no
candidate-provided backend binary, compiled definition, cache, proof trace, or
test result was reused.

All execution inputs were copied to `/tmp/audit-work`; `/candidate` was not
modified.  Source hashes are recorded in `evidence/03-source-hashes.log`.

Stage result: provenance is incomplete, but the supplied-semantics integrity
boundary passes and there is no mount/infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an input `List[str]`, `longest` must:

1. return `None` for an empty list;
2. otherwise return a string of maximum Python length;
3. when several strings have that length, return the earliest one.

This is the contract in `/reference/prompt.py`, implemented by
`/reference/canonical.py` by computing the maximum length and returning the
first string having that length.

### Generated program

`/candidate/solution.py` maintains `result`, initially `None`.  The first loop
element replaces the sentinel.  A later element replaces `result` only when its
length is strictly greater.  The `<=` branch retains the earlier result, so ties
are handled correctly.  For ordinary integer lengths, the `<=` and `>` tests
are disjoint and exhaustive.

The trusted translator was rerun on the scratch copy:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

The exact recorded command exited 0, and both files have SHA-256
`cd13a20e5b6377f13c2cae63c9d4e8931153cfda90b9b588676f7723ab8684d0`;
see `evidence/02-regenerate-mpy.log`.  The submitted `solution.mpy` is therefore
the trusted translation of the submitted Python source.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and candidate entry point.  Its exact run is in
`evidence/05-differential.log`.  It covered:

- all three documented examples;
- empty, singleton, empty-string, strict-longer, strict-shorter, and tie cases;
- late replacement and late tie retention;
- BMP and non-BMP Python strings;
- all 9,331 lists of lengths 0 through 5 over the six-string atom pool
  `["", "a", "bb", "é", "🧪", "xyz"]`;
- 2,000 deterministic generated cases (seed `120012`), list lengths 0 through
  12 and string lengths 0 through 16.

There were 11,344 total cases and zero mismatches.  The canonical serialization
of all generated inputs has SHA-256
`157cb45dd855e27ed27403ff85a9d4dbc6143821fb7111bfffc7ba5b2455e17a`.
This is finite fidelity evidence, not a substitute for a K theorem.

Stage result: program fidelity passes.

## 3. Clean proof reconstruction

K v7.1.337 was independently found at `/usr/bin/{kompile,kprove,krun}`;
versions and paths are in `evidence/04-tool-versions.log`.

### Fresh concrete definition

The supplied source semantics was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0 (`evidence/06-kompile-runtime.log`).  The reviewer then appended
ground assertions to the exact candidate function, translated that source with
the trusted translator, and ran it with the new definition.  Empty, first-tie,
strictly increasing, shorter-later, equal-length, and all-empty cases reached
`.K`, `NoExc`, and exit code 0.  The source, translated input, command, and full
bounded final configuration are in `evidence/audit_concrete.py`,
`evidence/audit_concrete.mpy`, and `evidence/12-krun-concrete-ascii.log`.

Two non-ASCII probes exposed the supplied model's stated ASCII boundary:

- the non-BMP input is rejected by K's scanner because the trusted translator
  emits surrogate escapes (`evidence/audit_concrete_nonbmp.py`,
  `evidence/08-krun-concrete.log`);
- the BMP non-ASCII input reaches the supplied `strToCodes` operation and
  stops there (`evidence/audit_concrete_bmp.py`,
  `evidence/10-krun-concrete-bmp.log`).

This agrees with the explicit “str literal (ASCII-only)” guard in the supplied
`semantics/str.k`; it is a language-model/intent limitation, not a changed
candidate semantics or a failed positive proof.

### Fresh proof definition and positive claims

The Haskell definition was rebuilt only from scratch sources:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0 (`evidence/13-kompile-verification.log`).  Every submitted positive
label was selected in the candidate's declared dependency groups:

```text
kprove spec.k --definition verification-kompiled \
  --claims loop-init-empty,loop-init-cons,loop-empty,loop-longer,loop-retain

kprove spec.k --definition verification-kompiled \
  --claims load-solution,call-empty,call-cons-dispatch
```

Both commands exited 0 and printed `#Top`; see
`evidence/15-kprove-loop-group.log` and
`evidence/16-kprove-entry-group.log`.  `loop-init-empty` also closed in an
isolated run (`evidence/14-kprove-loop-init-empty.log`).  An isolated
`loop-init-cons` diagnostic was interrupted after about five minutes because
removing the other loop circularities deprived it of its declared dependencies;
that diagnostic is documented in
`evidence/individual-claim-diagnostic.txt` and is not treated as a positive
claim failure.

The reconstruction gate therefore passes for the claims the candidate actually
submitted.  A fresh `#Top` here says those fragmentary reachability claims
close; it does not add a missing end-to-end postcondition.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

The eight claims in `/candidate/spec.k` mean:

- `loop-init-empty`: at the real loop head with `result = None` and no
  remaining element, execute the real return and frame pop and deliver `None`
  to the caller continuation.
- `loop-init-cons`: at the real loop head with `result = None` and at least one
  remaining string, execute the function and deliver
  `longestAcc(first, rest)` to the continuation.
- `loop-empty`: with a string accumulator and no remaining string, return that
  accumulator and pop the frame.
- `loop-longer`: with a string accumulator and a strictly longer next string,
  execute the loop and summarize the outcome by folding the tail from the new
  string.
- `loop-retain`: with a shorter or tied next string, execute the loop and
  summarize the outcome by folding the tail from the existing string.
- `load-solution`: loading the literal submitted module AST into the initial
  configuration installs the exact `longestSolution` closure.
- `call-empty`: a direct call of that closure on the empty abstract string list
  returns `noneV`.
- `call-cons-dispatch`: a direct call on a nonempty abstract string list creates
  the call frame and reaches
  `#bindP ~> assignments ~> For ~> Return ~> #endcall`.

The last item is the decisive defect.  Its destination is not a value and does
not mention `longestAcc`; the body has not executed.  No other submitted entry
claim starts at a nonempty `Call(...)` and ends at a result.  Consequently,
there is no machine-checked candidate theorem of either of these necessary
shapes:

```text
Call(longest, nonempty strings) => longestAcc(...)
Call(longest, nonempty strings) => first-longest-result
```

The helper claims make a plausible transitive derivation available to a human,
but that derivation is not the postcondition of any submitted entry claim and
was not the theorem for which the candidate obtained `#Top`.

### Program identity and state fidelity

The closure macro in `verification.k` is the exact function body in the
byte-verified `solution.mpy`.  `load-solution` embeds that exact whole module
AST.  The helper claims contain the exact translated `For` body and exact
`Return`.  Thus this is not a substituted-program attack.

The internal loop claims also pin the real frame behavior: environment 1 is
restored to 0, the local scope is removed, `scopeLoc` returns from 2 to 1, the
top frame is popped, the caller continuation is preserved, and heap, heap
location, exception, return, and exit-code cells agree.  They do not omit a
write or abrupt control effect used by this function.

The entry claims use a bare read-only `list(ValSeq)` rather than a heap `ref`
whose heap cell holds the list.  The supplied semantics explicitly permits
bare lists in symbolic claims, and the program neither mutates nor returns the
input list, so this abstraction is sound for the exercised behavior.  It is
nevertheless another bridge that the missing end-to-end entry theorem should
have made explicit.

### Satisfiable preconditions and ground substitutions

`evidence/claim_witnesses.py` and
`evidence/20-claim-witnesses.log` exhibit ground satisfying states/inputs for
every claim family:

- `[]` for `loop-init-empty` and `call-empty`, producing `None`;
- `["a", "bb"]` for `loop-init-cons`, producing `"bb"`;
- accumulator `"aa"` with empty remainder for `loop-empty`, producing `"aa"`;
- accumulator `"a"` and next `"bb"` for `loop-longer`, producing `"bb"`;
- accumulator `"aa"` and tied next `"bb"` for `loop-retain`, producing `"aa"`;
- the exact initial empty module state for `load-solution`.

For every result-bearing helper, the substituted `longestAcc` value equals both
Python implementations.  For `call-cons-dispatch` on `["a", "bb"]`, both
Python implementations return `"bb"`, while the submitted K postcondition has
no final-result field at all.  This is a concrete witness to non-constraint,
not an allegation that an individual rule has a false right-hand side.

Stage result: FAIL.  The real code is pinned in sound fragments, but the
nonempty entry theorem required for partial correctness is missing.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/build_rule_inventory.py` generated the line-addressed
`evidence/rule-inventory.tsv`.  Its construction log and SHA-256 are in
`evidence/19-rule-inventory-build.log`.  The inventory has 949 records:

- 704 rules;
- 231 syntax declarations;
- 8 claims;
- 5 contexts;
- 1 configuration.

It covers every K source file in the trusted supplied semantics, candidate
`verification.k`, and candidate `spec.k`.  Each record includes source, module,
line, kind, relevant attributes (`function`, `total`, `symbol`,
`no-evaluators`, `concrete`, `macro`, `priority`, `owise`, strictness, and so
on), a disposition, and the normalized full sentence.

Because this is `SUPPLIED_SEMANTICS`, all byte-matched reference-semantics
sentences are classified as the selected fixed baseline rather than
candidate-authored proof extensions.  This classification does not silently
bless `verification.k`; all 13 of its declarations/rules are separately
classified below.  There are no candidate-local `simplification`,
`functional`, `[concrete]`, opaque-symbol, or `no-evaluators` declarations.

### Construct-to-semantics map

The real `solution.mpy` uses only the following paths:

| Program construct | Syntax / execution source |
|---|---|
| `Module`, `ImportFrom`, `FuncDef` | `semantics/syntax.k`; `core.k` load; `controls.k` import no-op; `functions.k` closure installation |
| `Call(Name("longest"), ...)` | `core.k` lookup/argument loop; `call.k` closure dispatch/frame creation; `functions.k` parameter binding and pop |
| `Assign`, `Name`, `NoneVal` | strict syntax; `controls.k` scope write; `core.k` lookup and literal conversion |
| `For` and target binding | strict syntax; `controls.k` loop protocol; `tuple.k` `#bindTgt`; fixed `list.k` iterator rules |
| `If` | strict syntax; `controls.k` `truthy`/branch rules |
| `Compare(... is None)` | `operators.k` evaluation contexts and `is` rule |
| `Call(len, string)` | `call.k`; `builtins.k` `len`/`seqLen`; `core.k` `isLen` |
| integer `<=` and `>` | `operators.k` dispatch; `int.k` comparison equations |
| `Return` | strict syntax; `functions.k` return state and exact frame pop |

Evaluation is left-to-right where relevant: syntax strictness evaluates
assignment RHS, `For` iterable, `If` condition, and return expression; call
rules evaluate the callee then arguments; explicit comparison contexts evaluate
the left and wrapped right expressions.  The candidate extensions do not
change any of those orders.

The supplied configuration has `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>` cells.
The submitted claims constrain every cell touched by load, call, binding,
looping, return, or pop.

### Candidate-local rules

1. `StringSeq` and `stringVals` declarations plus the two structural equations
   are a transparent string-only embedding into `ValSeq`.  The equations are
   exhaustive and descending.
2. The two priority-40 `#iterNext` rules preserve the arbitrary continuation
   and every other cell.  They yield exactly the result of first expanding the
   structural embedding and then using the two fixed `MPY-LIST` iterator
   rules.
3. `longestAcc` has a base rule, a sentinel-seeding rule, a strictly-longer
   rule, and a retain-on-`<=` rule.  On `noneV`/string accumulators, guards are
   disjoint and exhaustive, recursive calls strictly shorten `StringSeq`, and
   strict comparison preserves the first item on a tie.  These are truthful
   mathematical equations, not an unconstrained answer oracle.
4. `longestSolution` is a macro for the exact translated closure body and
   defining environment 0.  It does not skip execution.

The iterator rules are operational bridges because ordinary `stringVals` does
not reduce under `list(...)`.  The reviewer therefore built a separate
bridge-free definition.  As first written with `stringVals` still ordinary,
the connection claim correctly got stuck
(`evidence/21-kompile-bridge-free.log`,
`evidence/22-kprove-bridge-connection.log`).  The same exhaustive structural
equations were then independently declared as a total mathematical function,
without importing either priority bridge.  Universal empty/cons connection
claims with arbitrary continuations compiled and closed with `#Top`
(`evidence/verification-bridge-free-total.k`,
`evidence/bridge-connection.k`,
`evidence/23-kompile-bridge-free-total.log`,
`evidence/24-kprove-bridge-connection-total.log`).  This establishes the
bridges' value and control equivalence independently.

One narrow declaration gap remains: `longestAcc(Val, StringSeq)` is marked
`[total]`, but for a nonempty sequence there are equations only when the first
argument is `noneV` or `str(...)`.  For example,
`longestAcc(0, sCons(.IntSeq, .StringSeq))` has no defining equation.  Every
actual claim keeps the accumulator in the covered sentinel/string subset, so
this over-broad totality declaration does not enable a demonstrated false
conclusion in this proof.  It is recorded as an evidence/scope gap, not labeled
unsound.

No inventoried candidate rule is labeled unsound, so there is no omitted
false-conclusion witness for a rule.  The decisive failure is instead the
absence of a result-bearing nonempty entry claim.

Stage result: proof-local rule soundness passes on the used domain; adequacy
still fails.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust.  The reviewer created
`evidence/spec-vacuity.k`, which changes the genuine empty-call result
obligation from `noneV` to `str(.IntSeq)`.  The precondition is satisfied by
the concrete input `[]`, for which both Python functions return `None`.

The mutation's dry run:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, demonstrating successful parsing/spec construction
(`evidence/17-vacuity-dry-run.log`).  The real proof command without
`--dry-run` exited 1.  Its `WarnStuckClaimState` shows the reachable `<k>` term
`noneV ~> .K`, which cannot unify with the false destination string; see
`evidence/18-vacuity-proof.log`.

This is meaningful non-vacuity evidence for the submitted empty result
obligation.  It cannot create or validate the absent nonempty result
obligation.

Stage result: the existing result-bearing fragment is non-vacuous, but the
overall requested theorem remains incomplete.

## 7. Proven versus assumed accounting

### What the successful reachability proofs establish

Under the supplied MPY semantics and candidate-local sound equations, the fresh
proofs establish:

1. the literal translated module AST installs the exact submitted function
   closure;
2. a direct empty abstract-list call returns `noneV`;
3. a direct nonempty abstract-list call dispatches into the exact function
   body with the expected new frame;
4. from each stated internal loop-head configuration, execution of the exact
   loop/return/control suffix produces the stated `longestAcc` summary and
   restores the caller state;
5. the summary equations retain the earlier accumulator on ties.

They do **not** establish one reachability claim from a nonempty function call
to that summary or to the first-longest returned string.  They also do not
machine-prove a separate theorem translating the mathematical fold into the
natural-language phrase “first longest,” although the transparent equations and
differential tests support that informal bridge.

### Trust and assumption ledger

- **Supplied semantics:** the entire integrity-matched reference tree is the
  selected fixed semantic level.  Relevant trusted behavior includes K
  integers/booleans/maps/lists/equality, lookup, strictness heating/cooling,
  list iteration, frame allocation/pop, `len`, and `isLen`.
- **K toolchain and solver:** `kompile`, `kprove`, `kore-exec`, Z3, and their
  reachability implementation are trusted primitives of the machine check.
- **Trusted translator:** `/reference/py2mpy.py` is the accepted Python-to-MPY
  bridge.  Byte identity pins its output to the submitted `solution.mpy`; the
  audit does not prove the translator correct.
- **String representation:** formal entry inputs are finite `StringSeq` values
  whose elements are `IntSeq`.  Connecting arbitrary Python `str` values to
  those sequences is informal/empirical.  The supplied concrete literal route
  is explicitly ASCII-only; Python differential testing covers Unicode only on
  the Python side.
- **Proof-local abstractions:** `stringVals` is structurally defined and its
  iterator bridges have the independent universal connection proof described
  above.  `longestAcc` is exhaustively defined on the accumulator cases that
  all claims use.  There is no fresh, unconstrained, result-bearing oracle.
- **Fixed opaque symbols:** the supplied tree declares
  `md5hexCodes`, `sortVS`, `sortKeyVS`, and the float symbols
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
  `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
  `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
  `sqrtF`.  None is reachable from this program or any submitted claim, so no
  theorem result depends on an opaque interpretation.
- **Empirical bridge:** the zero-mismatch 11,344-case differential run supports
  source-to-intent alignment only for tested Python inputs.  The concrete K run
  supports the ASCII execution bridge only for its preserved cases.
- **Partial correctness:** a successful reachability theorem would concern
  terminating executions.  The submitted theorem is incomplete before this
  usual termination boundary matters.

### Decision

The candidate source program appears correct, the trusted translation matches,
the supplied semantics is intact, all submitted claims reconstruct, the local
proof rules are sound on their used domain, and the empty result obligation is
non-vacuous.  Nevertheless, the requested proof is missing its central
nonempty entry-to-result reachability claim.  A `#Top` for dispatch plus
separate loop fragments cannot be reported as the absent theorem.

Under the stated decision boundary, a missing or non-result-constraining program
theorem is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
