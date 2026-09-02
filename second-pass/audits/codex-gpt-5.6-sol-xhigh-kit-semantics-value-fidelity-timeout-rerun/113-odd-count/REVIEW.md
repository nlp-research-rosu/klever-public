# Independent adversarial audit: 113-odd-count

The reconstructed K proof is legitimate, pins the submitted translated
program, constrains its result, and is non-vacuous. I assign `CONCERNS` rather
than `PASS` because two proof-local primitive summaries are opaque during
symbolic proof and connected to the supplied primitive equations only by
ground-exhaustive `[concrete]` rules plus finite testing, not by separate
universal symbolic connection claims. The connection is exact for every ground
program execution and wrong ground interpretations are rejected, so this is an
evidence/auditability limitation rather than a false-rule witness or a reason
to reject legitimacy. A second, narrower concern is that `codesProj(Val)` is
declared `[total]` although only its string-constructor case is equated; every
use in the theorem is guarded to strings.

This review does not rely on the candidate's `#Top`, compiled definitions,
`PROOF.md`, logs, or trace. Those were read only as untrusted claims. All
executed artifacts were copied or created under `/tmp/audit-work`; all reported
evidence is under `/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode. This is not an infrastructure breach.

`evidence/stage1-integrity.sh` checked types and symlinks for all required
candidate and trusted artifacts, then ran:

```text
cmp -s /reference/prompt.py /candidate/prompt.py
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
diff -r --no-dereference --brief \
  /reference/reference-semantics /candidate/reference-semantics
```

All three commands exited 0. The recursive semantics manifests in
`evidence/stage1-integrity.log` contain the same directory and 23 regular-file
entries, sizes, and SHA-256 hashes on both sides. There are no symlinks anywhere
in either semantics tree. Thus there are no missing, additional, changed,
mistyped, or symlinked entries in the candidate's `reference-semantics/`.

The required candidate artifacts are all regular files:

- `run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`.

There are no missing, changed, extra, mistyped, or symlinked required
artifacts. Candidate-created compiled definitions, caches, logs, tests, and
mutation files are additional top-level evidence, not entries in the
integrity-constrained semantics tree. They were deliberately excluded from all
fresh reconstruction.

The trusted/candidate prompt hash is
`2e684f86c7166a064ce81c06ad2a26b4d974f41c507e6e65e4dccd32f2345bcd`.
The trusted/candidate translator hash is
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
These also match the untrusted values in `run-input.json`.

I read the untrusted generation claims in the four named files. The candidate
claimed a successful proof, 11,115 differential cases, and two expected
negative failures. I did not use those results. The structured trace is one
valid 846-line JSONL file; its final event repeats the same claims.
`evidence/summarize_trace.py` and `evidence/trace-summary.log` record the trace
structure and final claim without treating it as proof.

Stage result: integrity passed; no audit infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From trusted `prompt.py` and `canonical.py`, the intended input is a list of
strings, each containing only decimal digits. For each input string `s`, let
`n` be the number of odd digits in `s`. The output has the same length and
order, and its corresponding element is exactly:

```text
"the number of odd elements " + str(n)
+ "n the str" + str(n)
+ "ng " + str(n)
+ " of the " + str(n)
+ "nput."
```

The canonical implementation computes
`sum(int(d) % 2 == 1 for d in s)`. The candidate computes the sum of
`s.count("1")`, `"3"`, `"5"`, `"7"`, and `"9"`. These are equivalent on the
documented digit-only domain. The candidate returns a fresh list and preserves
input order. The formal K precondition is slightly broader—every element must
be a modeled string, but it need not contain only digits. On that broader
domain the implementation consistently counts occurrences of those five
characters; this does not exclude or mis-handle an intended-domain input.

### Trusted translation identity

Only source artifacts were copied into `/tmp/audit-work/source`; the exact copy
commands and manifest are in `evidence/prepare-scratch.sh` and
`evidence/prepare-scratch.log`. The trusted translator was then run:

```text
python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/source/regenerated-solution.mpy
cmp -s /tmp/audit-work/source/regenerated-solution.mpy \
       /tmp/audit-work/source/solution.mpy
```

Both commands exited 0. Both MPY files have SHA-256
`5ca67da6ad518093d1c6a5bec859ee2e96bf00a7746dfc9c20cd8f23713e3a24`
(`evidence/stage2-fidelity.log`). The submitted `solution.mpy` is therefore
byte-for-byte the trusted translation of `solution.py`.

### Independent differential execution

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch copy of the generated entry point. It does not
reuse any K summary equation. It materializes the complete input list as
`evidence/differential-inputs.json` and checks:

- both documented examples;
- empty outer and inner lists/strings;
- individual even and odd digits;
- all-even, all-odd, and mixed strings;
- output-count boundaries 9, 10, 11, and 12;
- a mixed multi-element list;
- every individual decimal string of lengths 0 through 4 (11,111 cases);
- 500 deterministic generated multi-element cases, with string lengths through
  30 and seed 113.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py
```

It exited 0 with `total_cases=11628` and `mismatches=0`. The materialized input
file hash is
`50d035ecb08e2c824f43abfd9fbb92d5782958ad81127c2789c4ffd7735269fd`.
This is strong finite fidelity evidence, not a universal proof.

Stage result: program and translation fidelity passed.

## 3. Clean proof reconstruction

No candidate `*-kompiled` directory or cache was copied. K v7.1.293 was
available independently at `/usr/bin/{kompile,kprove,krun}`.

`evidence/stage3-reconstruction.sh` issued these material build commands from
`/tmp/audit-work/source`:

```text
kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/base-llvm-kompiled

kompile verification.k \
  --backend llvm --main-module VERIFICATION-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-llvm-kompiled

kompile verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled
```

All three fresh compilations exited 0. Compiler output is preserved in the
three `evidence/stage3-kompile-*.log` files. The warnings concern unused
variables in the supplied `strLt` equations and intentionally abstract locals
in the loop claim; there is no build error.

The reviewer-authored `evidence/concrete_reconstruction_test.py` includes the
empty case, both prompt examples, an empty string, even-only and odd-only
strings, and count-10/count-11 rendering boundaries. It was translated with
the trusted translator and run under both fresh LLVM definitions:

```text
krun /tmp/audit-work/build/concrete_reconstruction_test.mpy \
  --definition /tmp/audit-work/build/base-llvm-kompiled

krun /tmp/audit-work/build/concrete_reconstruction_test.mpy \
  --definition /tmp/audit-work/build/verification-llvm-kompiled
```

Both exited 0 and ended with `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. Their complete output logs compare byte-for-byte
equal (`evidence/stage3-concrete-compare.log`). This comparison covers every
cell, not just the returned strings.

The positive proofs were independently executed:

```text
kprove spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC --claims SPEC.odd-loop

kprove spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC
```

The separate loop proof and the complete specification proof each exited 0 and
printed `#Top`. See `evidence/stage3-kprove-odd-loop.log` and
`evidence/stage3-kprove-full.log`. The complete invocation proves both positive
claims in `SPEC`; the separate invocation additionally confirms the helper
circularity closes on its own.

Because this is supplied-semantics mode, no generated-semantics rebuild or
generated-semantics concrete comparison is applicable.

Stage result: clean proof reconstruction passed.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.odd-loop` starts at an actual recurring `#loop` head. Its remaining
iterable is `list(INPUT)`, the target is local `s`, and the body is the exact
translated loop body. The active function frame contains `lst`, `result`,
`s`, and `count`; heap location 0 contains an accumulated output `ACC`.
Provided every remaining input value is a string, termination of that loop
consumes the loop computation and changes the heap sequence to
`oddRun(ACC, INPUT)`. Module binding, allocation counters, stack frame, return
state, exception state, and exit code are fixed. The old/final `s` and `count`
values are intentionally existential because they are unobservable after the
loop.

`SPEC.odd-count` starts from the complete initial state, loads a module
containing `odd_count`, resolves that binding normally, and calls it on
`list(INPUT)`, with `allStringValues(INPUT)`. At termination it must return
`ref(0)`; heap location 0 must contain exactly
`list(oddRun(emptyOutput, INPUT))`; the function frame must be popped; the
module closure must contain the exact body; allocation must be exactly one
list; and return, exception, and exit cells must be normal.

### Exact program identity

The entry claim uses an `oddBody` syntax macro instead of textually embedding
`solution.mpy`. I freshly compiled an identity definition, parsed both the
submitted MPY file and reviewer-authored `evidence/program-macro.mpy` at depth
zero, and compared the expanded JSON configurations:

```text
krun /tmp/audit-work/source/solution.mpy \
  --definition /tmp/audit-work/build/identity-kompiled \
  --depth 0 --output json \
  --output-file /audit-output/evidence/stage4-solution-config.json

krun /audit-output/evidence/program-macro.mpy \
  --definition /tmp/audit-work/build/identity-kompiled \
  --depth 0 --output json \
  --output-file /audit-output/evidence/stage4-macro-config.json

cmp -s /audit-output/evidence/stage4-solution-config.json \
       /audit-output/evidence/stage4-macro-config.json
```

All exited 0. Both JSON files have SHA-256
`71b4ef4b97c417f330576f4fcb7cfa3e40bc6efb80ffb6b1bdb0ac9176935d96`
(`evidence/stage4-identity-compare.log`). An earlier diagnostic in
`stage4-pinning.log` compared combined stdout/stderr logs and saw different
backend PID text in depth-limit warnings; the output-file comparison above
correctly compares only the configurations and supersedes that diagnostic.

The loop helper matches real control flow. On entry to the first iteration,
`s` and `count` do not yet both exist, so the entry proof unrolls that
iteration. Assignment creates both locals. Subsequent control returns to the
exact `#loop(list(REST), Name("s"), oddLoopBody)` state accepted by the
circularity. The empty branch exits directly. There is no substituted helper
program or rule that skips `odd_count`.

### Result constraint and satisfiable states

The result is not a free variable or implication-only postcondition:
`ref(0)`, the entire output `ValSeq`, heap map, heap counter, stack, return
state, exception, and exit status are fixed.

Concrete satisfying witnesses exist:

- Entry claim: `INPUT=.ValSeq` in the literal initial state. Then
  `allStringValues(.ValSeq)=true`, and the claimed heap result is the empty
  sequence.
- Loop claim: choose `INPUT=.ValSeq`, `ACC=.ValSeq`, `ORIGINAL=.ValSeq`,
  `PREVN=0`, and `PREVS=str(.IntSeq)` in the displayed frame. Its precondition
  is true and the base loop exits with `oddRun(.ValSeq,.ValSeq)=.ValSeq`.
- A nonempty entry witness is
  `INPUT=vCons(str(strToCodes("1234567")),.ValSeq)`.

`evidence/ground-spec.k` substitutes the empty input, both prompt inputs, and a
ten-odd-digit boundary directly into entry configurations and demands explicit
literal output strings rather than `oddRun` summaries. The exact command:

```text
kprove /audit-output/evidence/ground-spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module GROUND-SPEC
```

exited 0 and printed `#Top` (`evidence/stage4-ground-kprove.log`).
`evidence/ground_python_results.py` independently ran the same four inputs
through both Python implementations; every pair was equal and matched those K
literals (`evidence/stage4-ground-python.log`).

Stage result: adequacy and real-program pinning passed.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` inventories the trusted root semantics, all 22
supplied helper K files, `verification.k`, and `spec.k`. The full normalized
source, file, line, attributes, assessment, and rationale for every item are
in `evidence/k-inventory.jsonl`. The source hashes and per-file counts are in
`evidence/k-inventory-summary.md`.

The inventory contains 955 items:

- 710 rules;
- 237 syntax declarations;
- five evaluation contexts;
- one configuration;
- two claims.

It flags 154 function declarations, 115 `total` declarations, 28 opaque
`symbol` declarations, 25 `no-evaluators` declarations, 47 priority-bearing
rules, 37 actual `[concrete]` rules, 26 `[owise]` rules, and five macro-bearing
items. There are no `[functional]` declarations and no simplification rules.
Every candidate rule and claim has a line-specific assessment; no item is left
unclassified.

In supplied-semantics mode the recursively identical `/reference` tree is the
selected, trusted semantic level. Its 928 inventory items are still enumerated.
Rules reachable from this program were reviewed for control, guards, cells,
and helper equations. Unused float, sorting, dictionary, set, slicing,
comprehension, hashing, and related rules are syntactically unreachable from
`solution.mpy` and cannot affect either claim. Some of those unused supplied
features deliberately expose opaque or partial subset behavior; that is a
base-semantics scope limitation, not a candidate extension and not reachable
here.

### Construct-to-semantics map

Every source construct has a declaration and execution path:

| Submitted construct | Declaration and relevant fixed rules |
|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `syntax.k:53-61`; load/sequence `core.k:124-127`; closure binding `functions.k:14-16` |
| `Name` | `syntax.k:12`; lexical lookup `core.k:130-154`; builtins scope `core.k:157-181` |
| `Assign` | `syntax.k:41` has strict RHS; scope update `controls.k:9-18` |
| `ListExpr` | `syntax.k:17`; left-to-right element evaluation and allocation `list.k:13-15`, `core.k:117-121` |
| `For` | `syntax.k:45` has strict iterable; list iteration `list.k:9-10`; loop protocol `controls.k:65-74`; target binding `tuple.k:31-41` |
| `Call`, `Attribute` | `syntax.k:28-29`; receiver/callee then arguments `call.k:16-24`, `core.k:183-191`; closure call/frame `call.k:69-74` |
| `BinOp("+",...)` | `syntax.k:15` is left-to-right `seqstrict`; dispatch `operators.k:12`; integer addition `int.k:9`; string concatenation `str.k:20-24` |
| `Str` | `syntax.k:13`; ASCII code construction `str.k:13-17` |
| `s.count(one-char)` | fixed equation `methods.k:34-44`, after ordinary method dispatch |
| `str(count)` | fixed equation `builtins.k:148`, after ordinary name/type dispatch |
| `result.append(value)` | mutator route preserves the reference and updates only its heap value, `list.k:52-55` |
| `Expr(call)` | value discarded after effects, `controls.k:46-48` |
| `Return` | strict expression declaration `syntax.k:50`; return/pop and restoration `functions.k:77-90` |

The fixed configuration contains `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`.
The entry/loop claims constrain all material cells. Evaluation is left-to-right:
`BinOp` is `seqstrict(2,3)`; assignment, loop iterable, return, and expression
statements are strict; the call layer evaluates the callee first and arguments
through the ordered `#evalArgs` accumulator.

### Candidate-local rule decisions

The 15 candidate rules are exhausted by these groups:

1. `oddBody` and `oddLoopBody` (`verification.k:10,16`) are compile-time
   macros. Fresh expanded-program identity proves they denote the submitted
   AST exactly. They do not execute as operational shortcuts.
2. `allStringValues` (`:72-74`) has disjoint empty/cons equations and strictly
   consumes the tail. It is a true, exhaustive formal precondition.
3. `codesProj(str(CS)) => CS` (`:78`) is a true constructor projection.
   Declaring `codesProj(Val)` total is over-broad because there is no equation
   for non-string `Val`; however, `allStringValues`, the bridge guard, and the
   `oddRun` guard ensure all theorem uses are strings. The unspecified total
   extension supplies no false equation and cannot influence an intended
   state.
4. `digitOccurrences` (`:85-87`) has the ground-exhaustive equation
   `cntSub(CS,iCons(D,.IntSeq))`. It strictly delegates to the supplied count
   helper for every ground `CS,D`.
5. The `applyMethod` bridge (`:92-99`) is discussed below.
6. `oddDigits` (`:102-108`) is a pure sum of the occurrence counts for ASCII
   codes 49, 51, 53, 55, and 57.
7. `intStringCodes` (`:113`) has the ground-exhaustive equation
   `strToCodes(Int2String(N))` for every ground integer.
8. The `applyBuiltin("str",...)` bridge (`:114-115`) is discussed below.
9. `oddSentenceCodes` and `oddSentence` (`:118-138`) reproduce the source's
   nine left-associated concatenation pieces in their exact order.
10. `oddRun` (`:143-150`) has disjoint empty and string-headed cases, appends
    exactly one sentence, and strictly consumes the input tail.
11. `emptyOutput` (`:153`) is exactly `.ValSeq`.

All pure equations are true on their guards. Recursive definitions descend.
There is no overlapping candidate equation with conflicting right-hand sides,
no answer-encoding rewrite of a program body, no simplification lemma, and no
unconstrained fresh result.

### Operational bridges, priorities, and false-witness search

There are exactly two candidate operational bridges.

For `str.count`, the supplied rule on the accepted overlap is:

```text
applyMethod(str(CS), "count", str(iCons(D,.IntSeq)), .Vals)
  => cntSub(CS, iCons(D,.IntSeq))
```

The candidate priority-40 rule yields:

```text
digitOccurrences(codesProj(str(CS)),D)
  => digitOccurrences(CS,D)
  => cntSub(CS,iCons(D,.IntSeq))   // every ground CS,D
```

Its `isStrV(V)` guard and exact one-character argument make the overlap no
broader than that equality. It is reached only after receiver, method, and
argument evaluation. Because it is a pure function rule, it reads/writes no
configuration cell and introduces no return, exception, allocation, or
continuation effect.

For `str(int)`, the supplied overlap is:

```text
applyBuiltin("str",N,.Vals)
  => str(strToCodes(Int2String(N)))
```

The candidate priority-40 rule produces `str(intStringCodes(N))`, and the
ground-exhaustive equation gives the identical supplied term. It is reached
only after ordinary `str` lookup, callee resolution, and argument evaluation.
It likewise changes no cell or control effect.

The complete base-versus-extended LLVM configurations were byte-identical on
the reviewer test, including heap, environments, allocation, control, and
exceptions. This is finite context evidence. More directly,
`evidence/bridge-correct.k` establishes the ground values
`digitOccurrences("1110",49)=3` and `intStringCodes(10)="10"`.
`evidence/bridge-opposite.k` demands the opposite values 2 and `"11"`.
The correct claims print `#Top`; each wrong claim separately exits 1 with
`WarnStuckClaimState`, leaving respectively 3 and code sequence `[49,48]`.
Commands and outputs are in `evidence/stage5-bridge-values.sh` and
`evidence/stage5-bridge-values.log`.

I found no candidate rule that enables a false conclusion on the intended
domain, so I make no unsoundness allegation. In particular, there is no missing
false-conclusion witness hidden behind an "unsound" label. The narrower evidence
gap is that the bridge equality is not packaged as a universal symbolic
connection theorem; `[concrete]` supplies every ground equation while symbolic
proof remains parametric.

### Body/control sensitivity

As a separate operational-sensitivity check, I removed the real `For` from
`oddBody` while keeping the claimed result unchanged. The mutation is exactly
the one-line diff in `evidence/stage5-body-mutation.diff`; the complete mutated
source is `evidence/body-mutation-verification.k`.

The mutated definition compiled successfully, but:

```text
kprove spec.k \
  --definition /tmp/audit-work/build/body-mutation-kompiled \
  --spec-module SPEC
```

exited 1 with `WarnStuckClaimState`. The residual has the mutated closure body,
the actual empty heap, and the unmet equality to `oddRun(.ValSeq,INPUT)`.
See `evidence/stage5-body-sensitivity.log`. Thus the proof depends on execution
of the real loop rather than only on matching function name or postcondition.

Stage result: static soundness passed, with the two non-material concerns
stated above.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`.
`evidence/fresh-false-spec.k` is a fresh mutation of the entry postcondition.
It preserves the program and loop obligation but appends one `noneV` to the
demanded result:

```text
list(valSeqConcat(
  oddRun(emptyOutput, INPUT),
  vCons(noneV,.ValSeq)))
```

This is demonstrably false for the satisfying input `INPUT=.ValSeq`: execution
returns `[]`, while the mutation demands `[None]`.

The dry run:

```text
kprove /audit-output/evidence/fresh-false-spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module FRESH-FALSE-SPEC --dry-run
```

exited 0, so the mutation parsed and built successfully. The same command
without `--dry-run` exited 1 with `WarnStuckClaimState`. Its reachable residual
fixes `INPUT=.ValSeq` and shows the actual heap
`0 |-> list(.ValSeq)`. This is the expected result mismatch, not a parser
error, missing import, timeout, or unrelated backend crash. The source,
commands, statuses, and bounded output are in
`evidence/stage6-nonvacuity.sh`, `evidence/stage6-false-dry-run.log`,
`evidence/stage6-false-kprove.log`, and `evidence/stage6-nonvacuity.log`.

Stage result: fresh non-vacuity passed.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied MPY transition system plus the two ground-defined
proof-local primitive summaries, for every modeled ground `ValSeq` whose
elements are strings, if the exact submitted `odd_count` execution terminates
from the stated initial state, then:

- it returns the one allocated output list at `ref(0)`;
- the list contains one result per input string, in order;
- each result is the exact sentence built by the submitted concatenations;
- its repeated number is the sum of occurrences of codes for
  `1,3,5,7,9`;
- call frames are popped, no modeled exception is present, and the exit code
  remains zero.

On the prompt's digit-only domain, ordinary parity arithmetic makes that sum
exactly the number of odd digits. Ground substitution proofs demonstrate the
prompt strings and a two-digit count. This is partial correctness; no separate
termination theorem is claimed.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Trusted `py2mpy.py` translates the relevant CPython AST faithfully | Connects `solution.py` to the byte-identical `solution.mpy`; affects the entire K theorem | Acceptable mandated translator boundary; byte identity was independently checked, but translator correctness itself is not proved here |
| Supplied MPY semantics and K toolchain/hooks implement their documented subset | Defines every execution, value, cell, and proof step | Acceptable selected semantics boundary; integrity is exact and all used rules were statically traced |
| `digitOccurrences(CS,D)` ground equation equals supplied `cntSub(CS,[D])` | Affects `count`, all four rendered numbers, `oddDigits`, `oddSentence`, `oddRun`, and both claims | Acceptable low-level primitive abstraction for ground executions; exact equation and rejected opposite witness; concern because no separate universal symbolic connection claim |
| `intStringCodes(N)` ground equation equals `strToCodes(Int2String(N))` | Affects all four decimal substitutions and both claims | Same classification and concern as above |
| `codesProj` is unspecified on non-string `Val` despite `[total]` | Could affect a misuse outside its one equation | Concerning declaration breadth but harmless here: every use is guarded by `isStrV`/`allStringValues`; it adds no false equation |
| K integers, ASCII code sequences, `Int2String`, and integer/string hooks have their documented mathematical meaning | Connects modeled values to decimal/ASCII strings | Acceptable low-level supplied/K boundary on the intended ASCII digit domain |
| Codes 49,51,53,55,57 are precisely digit characters 1,3,5,7,9 and those are exactly the odd decimal digits | Connects the formal sum to the English contract | Straightforward ordinary mathematics, not a tested-only program summary |
| CPython canonical implementation expresses the intended HumanEval contract | Oracle for differential evidence | Trusted problem input; finite differential results support implementation alignment only |

Opaque supplied symbols for float arithmetic, sorting, keyed sorting, and MD5
are also part of the base trust surface, but none is syntactically reachable
from this program or mentioned by the claims. They cannot affect this result.

The 11,628-case differential test supports the candidate-versus-canonical
bridge and ground primitive behavior. It does not replace the reachability
proof, prove the translator, or establish a universal semantic equivalence.
Likewise, the base/extended concrete comparison is finite operational evidence;
the static equality analysis supplies the general ground bridge argument.

### Decision

All positive claims reconstruct from clean source; the macro expands to the
submitted program; the result is fixed; satisfiable states and ground
substitutions exist; candidate-local equations and bridges are true for all
ground uses; opposite values and two independent mutations are rejected. There
is no material adequacy gap and no false-rule witness.

The opaque-during-symbolic-proof presentation and over-broad `codesProj`
totality declaration reduce audit clarity enough for `CONCERNS`, but neither
permits a false conclusion on the formal or intended domain. The proof remains
legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
