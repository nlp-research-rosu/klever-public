# Independent adversarial audit: 11-string-xor

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program. I rebuilt every definition from source, independently reran both target
claims, checked the real-program binding at constructor level, audited the only
operational bridge against a bridge-free universal loop claim, reviewed the
complete K rule/declaration inventory, and rejected a fresh false result.

The proof covers the full source-contract domain: arbitrary finite strings made
only of `"0"` and `"1"`, including empty and unequal-length strings. It is not a
finite-size or example-only theorem.

The exact reviewer commands, working directories, statuses, and corresponding
logs are indexed in [evidence/COMMANDS.md](evidence/COMMANDS.md).

## 1. Input and provenance integrity

### Declared layout and required mounts

`/audit-input.json` declares:

- `record_layout = pipeline-v3`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- problem `11-string-xor`;
- condition `kit-semantics`.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` exists as a real directory. The candidate also
contains `reference-semantics/`, and the two trees have the same 25 entries,
entry types, and file bytes. Neither tree contains symlinks or unsupported
entry types.

All pipeline-v3 records required by the prompt are present, regular, readable
files/directories:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- one structured trace file below
  `/generation-evidence/codex-trace/`.

The structured trace contains 601 JSONL records and parses with zero JSON
errors. Its event inventory and the untrusted final generation claim are
recorded in
[evidence/01-generation-record-summary.log](evidence/01-generation-record-summary.log).
Those claims were not used as proof evidence.

### Independent hashes and types

The campaign-lock JSON is exactly equal to the `audit_campaign` block in
`/audit-input.json`, and its independently computed SHA-256 is the recorded
`ad5dfc...d745`.

Every recorded regular-file hash checked independently matched, including the
canonical program, trusted/candidate prompts, trusted/candidate translators,
run/task/result/invocation manifests, metrics, usage, prompt, final response,
output log, and trace JSONL file. The complete checks are in
[evidence/01-provenance.log](evidence/01-provenance.log).

I also independently reproduced the pipeline-v3 length/path/type/content tree
hash encoding:

- mounted `/candidate` hashes to
  `49831c...1f72`, matching both the invocation and generation-result workspace
  hashes;
- both trusted and candidate semantics hash to
  `4e0639...789f`, matching the task manifest and audit-input semantics-manifest
  hash;
- the trace tree hashes to `70f4b0...2b1d`, matching `usage.json`.

See
[evidence/01-pipeline-tree-hashes.log](evidence/01-pipeline-tree-hashes.log).
The launcher also records separate aggregate hashes under its own field names;
the independently reproducible pipeline hashes, recursive byte comparison, and
all file-level hashes agree.

The whole mounted candidate contains 797 entries, zero symlinks, and zero
unsupported types. Required proof artifacts (`solution.py`, `solution.mpy`,
`verification.k`, and `spec.k`) are regular files. Candidate-built compiled
definitions were present under `/candidate` but were never reused.

### Prompt, translator, and supplied semantics integrity

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Candidate `reference-semantics/` is recursively byte/type identical to the
  trusted tree, with no missing, additional, changed, mistyped, or symlinked
  entry.

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt asks for binary XOR of two strings whose characters are only
`0` and `1`, returning the result as a string. The trusted canonical
implementation applies the XOR truth table pairwise through Python `zip`.
Consequently, it returns:

- `"0"` for equal paired bits;
- `"1"` for unequal paired bits;
- a string whose length is the shorter input length.

The prompt does not impose equal lengths. Empty strings and unequal lengths are
therefore in the intended domain, with behavior fixed by the canonical
implementation.

### Submitted implementation

`solution.py` initializes `result`, `x`, and `y`, iterates over
`zip(a, b)`, appends `"0"` when `x == y` and `"1"` otherwise, and returns
`result`. For bit-string inputs this is extensionally the canonical algorithm.
Initializing `x` and `y` is observable only as callee-local state and does not
change the returned result.

### Translation identity

Using only the trusted translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

exited 0. The regenerated and submitted files both hash to
`3e1f7a...40bd`; `cmp -l` exited 0. Evidence:
[evidence/02-translation-identity.log](evidence/02-translation-identity.log).

### Independent differential test

The reviewer script
[evidence/differential_test.py](evidence/differential_test.py) imports the
trusted canonical entry point and candidate entry point independently. It
checks:

- the documented example;
- both-empty and one-empty boundaries;
- all four one-bit truth-table branches;
- both unequal-length directions;
- an alternating multi-bit case;
- every pair drawn from all binary strings of lengths 0 through 7;
- 1,000 deterministic generated pairs up to length 256.

Result: 66,036 comparisons, zero mismatches, exit 0. Evidence:
[evidence/02-differential.log](evidence/02-differential.log).
This is finite implementation-fidelity evidence, not a substitute for the K
proof.

## 3. Clean proof reconstruction

### Isolation

Only source artifacts were copied to `/tmp/audit-work/reconstruction`.
Candidate directories named `runtime-kompiled`,
`verification-base-kompiled`, and `verification-kompiled` are absent there.
Fresh outputs use distinct `*-fresh-kompiled` names. Source hashes match the
mounted candidate, and the scratch semantics still diff exactly against the
trusted semantics. Evidence:
[evidence/03-scratch-source-manifest.log](evidence/03-scratch-source-manifest.log).

The live toolchain is K 7.1.293 and Python 3.10.12:
[evidence/00-toolchain.log](evidence/00-toolchain.log).

### Fresh builds

The following source builds all exited 0:

1. Concrete LLVM definition, `MPY-KRUN`:
   [evidence/03-kompile-runtime.log](evidence/03-kompile-runtime.log).
2. Bridge-free Haskell definition, `VERIFICATION-BASE`:
   [evidence/03-kompile-verification-base.log](evidence/03-kompile-verification-base.log).
3. Bridge-enabled Haskell definition, `VERIFICATION`:
   [evidence/03-kompile-verification.log](evidence/03-kompile-verification.log).

Compiler warnings concern unused variables and incomplete total-function cases
in unrelated supplied-semantics features such as float helpers, `mapStrVS`,
`joinCodes`, and out-of-bounds `valSeqAt`. None is reachable from this program
or used to close either target claim.

### Positive target claims

The bridge-free loop connection theorem was run independently:

```text
kprove spec.k \
  --definition verification-base-fresh-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-invariant
```

It printed `#Top` and exited 0:
[evidence/03-kprove-loop.log](evidence/03-kprove-loop.log).

The entry theorem was run independently:

```text
kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  --claims SPEC.string-xor
```

It printed `#Top` and exited 0:
[evidence/03-kprove-entry.log](evidence/03-kprove-entry.log).

### Fresh concrete reconstruction

The reviewer concrete harness
[evidence/reviewer_concrete.py](evidence/reviewer_concrete.py) contains an AST-
identical copy of the submitted function and eleven normal/boundary assertions.
The trusted translator produced its MPY term, and the function AST identity
check exited 0:
[evidence/03-concrete-harness-prep.log](evidence/03-concrete-harness-prep.log).

Both executions succeeded:

- fixed concrete LLVM semantics: exit 0,
  [evidence/03-krun-runtime-concrete.log](evidence/03-krun-runtime-concrete.log);
- bridge-enabled Haskell semantics: exit 0,
  [evidence/03-krun-verification-concrete.log](evidence/03-krun-verification-concrete.log).

## 4. Adequacy and real-program pinning

### Plain-language claims

`LOOP-SPEC.loop-invariant` starts at the real internal loop form:

```text
#loop(zipObjS(A, B), exact tuple target, exact if/augassign body)
```

in a plain active frame containing exactly `a`, `b`, `result`, `x`, and `y`.
For arbitrary current result `R`, remaining sequences `A` and `B`, arbitrary
initial loop-target values, arbitrary parent/outer scopes, arbitrary omitted
cells, and arbitrary continuation, it proves that the loop finishes and:

- changes `result` to `xorAcc(R, A, B)`;
- changes `x` and `y` to the last pair yielded by the remaining zip, or leaves
  them unchanged if zip is empty;
- preserves `a`, `b`, parent, outer scopes, continuation, and all omitted cells.

`SPEC.string-xor` starts with a call to `string_xor` in the exact initial module
scope/cell state. The name is bound to a closure with parameters `("a","b")`
and the exact submitted function body. Its precondition requires both code
sequences to satisfy `bitString`. Its destination is `str(?OUT)`, and:

```text
ensures ?OUT ==K xorAcc(.IntSeq, A, B)
```

Thus the existential output is not free: it is equal to the structurally
defined pairwise XOR sequence.

### Mechanical program identity

The independent constructor check reports:

- the exact closure derived from regenerated `solution.mpy` occurs exactly once
  in the entry claim;
- normalized closure hash:
  `fcaf10...1983`;
- the operational bridge body and loop-claim body are exactly equal after
  whitespace normalization, both hashing to `e98bda...56e2`;
- `VERIFICATION-BASE` contains zero operational `<k>` rules;
- the loop spec imports only `VERIFICATION-BASE`, while the entry spec imports
  `VERIFICATION`;
- `VERIFICATION` contains exactly one operational rule.

Evidence:
[evidence/04-static-artifact-checks.log](evidence/04-static-artifact-checks.log).

The entry claim does not reload the whole `Module`; it pins the same function
binding/body directly. Trusted byte regeneration plus this constructor-level
comparison satisfies the permitted function-binding form of real-program
pinning. The lack of automatic source-to-spec generation is an artifact-
maintenance observation, not a defect in this immutable candidate.

### Satisfying states and concrete substitution

The precondition is satisfiable. For example:

```text
A = .IntSeq
B = .IntSeq
```

makes both `bitString` predicates true. `xorAcc(.IntSeq,A,B)` is `.IntSeq`;
both Python implementations return `""`, and the ground K claim proves exactly
`str(.IntSeq)`.

For the documented satisfying input:

```text
A = [48,49,48]  ("010")
B = [49,49,48]  ("110")
```

`xorAcc(.IntSeq,A,B)` reduces to `[49,48,48]` (`"100"`). Both Python
implementations return `"100"`. Reviewer ground claims for this example and
the empty witness jointly printed `#Top` and exited 0:
[evidence/spec-ground.k](evidence/spec-ground.k) and
[evidence/04-kprove-ground.log](evidence/04-kprove-ground.log).

### Body and context sensitivity

The inspected body mutation swaps the actual `"0"`/`"1"` append terms inside
the loop claim while retaining the original `xorAcc` postcondition. It is run
against the bridge-free definition, so it changes the program term actually
executed. `kprove` exited 1 with `WarnStuckClaimState`; the residual requires the
false equality between summaries beginning with code 48 and code 49:
[evidence/04-kprove-body-sensitivity.log](evidence/04-kprove-body-sensitivity.log).

I additionally placed an observable assignment immediately after a one-step
loop. Both fixed semantics and bridge-enabled semantics proved the same final
`result`, `x`, `y`, and new `marker` binding:

- bridge-free `#Top`, exit 0:
  [evidence/05-continuation-base.log](evidence/05-continuation-base.log);
- bridge-enabled `#Top`, exit 0:
  [evidence/05-continuation-bridge.log](evidence/05-continuation-bridge.log).

This checks that the bridge's arbitrary continuation frame is preserved.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-line inventory is
[evidence/k-rule-inventory.tsv](evidence/k-rule-inventory.tsv), generated by
[evidence/k_inventory.py](evidence/k_inventory.py). It contains 1,120
declaration/structure entries, including:

- 708 rules: 615 ordinary, 46 priority, 35 concrete-only, and 12
  simplification rules;
- 150 function declarations, of which 22 are explicit
  `no-evaluators` opaque declarations;
- 81 other syntax declarations;
- five contexts, one configuration, two target claims, and all module/import/
  requires structure.

The 708 rules comprise all 695 supplied semantic/helper rules and all 13
candidate-local rules. Each inventory row has a source range, attributes,
classification, review decision, and decision basis. The generator summary is
[evidence/05-k-inventory.log](evidence/05-k-inventory.log).

The complete mapping from every constructor used by `solution.mpy` to its
declaration and material rules is
[evidence/used-constructor-map.md](evidence/used-constructor-map.md).

### Candidate-local declarations and rules

`xorAcc` is a pure definitional summary, not an operational interception.
Its four equations cover:

1. empty left sequence;
2. nonempty left and empty right;
3. both nonempty with equal heads;
4. both nonempty with unequal heads.

The constructor cases are exhaustive; equality and inequality guards are
disjoint; both recursive rules remove one constructor from each input. The
right-hand sides exactly append code 48 for equality and code 49 for
inequality, matching the actual loop body. Its value fixes both the loop result
and entry postcondition.

`bitString` is a pure structurally recursive predicate. Empty is true; a cons
is true exactly when its head is 48 or 49 and its tail is a bit string. It is
the full prompt domain, not a finite bound.

`lastX` and `lastY` are pure structural summaries. Their empty/nonempty cases
are exhaustive and disjoint, and the recursive case removes a pair and records
the corresponding one-character string. They affect only the final loop-target
locals. The bridge-free loop proof independently checks these values.

All twelve equations above are marked `[simplification]`, but the
simplification use is the same truthful structural equation. No overlapping
case has different right-hand sides, every `[total]` declaration is covered,
and every recursive case descends.

The thirteenth local rule is the priority-40 loop bridge. Its complete match
requires:

- `zipObjS(A,B)`;
- the exact tuple target;
- the exact comparison and both exact `AugAssign` branches;
- the exact plain five-key active frame;
- active environment `L`;
- arbitrary but preserved continuation, parent, outer scopes, and omitted
  cells.

Its rewrite changes only `result`, `x`, and `y` as the bridge-free claim does.
It does not return, pop a frame, raise an exception, break, continue, allocate,
or discard a suffix. The separately rebuilt loop theorem has exactly the same
match domain and does not import the bridge. The exact-text check, body
sensitivity failure, and observable-continuation proofs establish context and
value containment.

### Material supplied-semantics path

The fixed rules used by this theorem were traced in execution order:

1. normal name lookup selects the exact closure and the builtins-scope `zip`;
2. call routing evaluates callee then arguments left-to-right;
3. the closure call allocates a plain frame, binds `a` then `b`, and saves the
   complete caller continuation;
4. strictness evaluates assignment RHSs before writes;
5. `zip` of strings creates `zipObjS`, whose iterator yields ordered
   two-element tuples and stops when either input is empty;
6. tuple target binding writes `x` then `y`;
7. comparison contexts evaluate operands left-to-right, and string equality is
   exact `IntSeq` equality;
8. `If` uses the resulting Boolean;
9. `AugAssign` reads `result`, uses structural string concatenation, and writes
   the result;
10. loop control executes the body before recurring;
11. `Return` evaluates `result`, restores the caller, removes the callee frame,
    and resumes the saved continuation.

The exact frame is plain and all live values are strings, so higher-priority
cell/ref rules have false guards (`"$cells"` absent or `isRefV` false). The only
applicable candidate priority rule is the exact loop bridge. No task-specific
call rule preempts normal lookup, argument evaluation, or function entry.

The supplied model uses ASCII code sequences. On the intended bit-string
domain this agrees with Python exactly: only codes 48 and 49 are admitted.
Allocation, exceptions, unrelated collection behavior, floats, and imports are
not touched by the theorem path.

### Opaque and unused imported declarations

The supplied semantics contains 22 explicit no-evaluator symbols:

```text
md5hexCodes;
intFloatDiv, divII, floatMod, floatLt, absF, subF, divF, addF, mulF,
powF, gtF, eqF, decStrToF, divFloatIntV, intToF, truncF, roundF,
roundFN, sqrtF;
sortVS, sortKeyVS
```

The float helpers `floorFI`, `toF`, and `ceilF` also have proof-domain
concrete-only equations. None of these symbols, their routing rules, or any
value derived from them is reachable from the submitted term or appears in a
target precondition/postcondition. They do not contribute to claim closure.
Their exact locations and all other unused baseline declarations are in the
inventory.

I found no rule capable of enabling a false conclusion on the intended
bit-string domain. Therefore I make no unsound-rule finding, and the requested
false-conclusion-witness obligation for such a finding is not triggered.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh reviewer mutation
is [evidence/spec-fresh-vacuity.k](evidence/spec-fresh-vacuity.k).

It uses the satisfying inputs `"010"` and `"110"` but changes the exact
result-constraining destination from the true `"100"` to the false `"101"`.
The term still contains the exact submitted closure and executes through the
same bridge-enabled definition.

The mutation parsed and ran. `kprove` exited 1 with
`WarnStuckClaimState`; its terminal configuration contains:

```text
str(iCons(49, iCons(48, iCons(48, .IntSeq))))   // "100"
```

which does not unify with the mutated `"101"` destination. The failure is the
expected unmet result obligation, not a parser error, timeout, missing import,
or unrelated crash. Evidence:
[evidence/06-fresh-vacuity.log](evidence/06-fresh-vacuity.log).

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics and candidate-local structural definitions:

- the exact real loop has the stated `xorAcc`/`lastX`/`lastY` summary for
  arbitrary finite remaining sequences and arbitrary continuation;
- calling the exact submitted `string_xor` closure on any two `bitString`
  sequences reaches a string result whose codes equal
  `xorAcc(.IntSeq,A,B)`;
- this is the pairwise equality/inequality truth table, truncated when the
  shorter sequence ends;
- the result obligation is discriminating.

The theorem is partial correctness. It does not separately prove termination.
That is the requested proof category; no claim of total correctness is made.

### Trusted boundaries and dependents

1. **Supplied MPY semantics.** The relevant fixed rules for calls, scopes,
   strings, `zip`, loops, target binding, branches, updates, and returns are the
   language-model boundary. Candidate identity with the trusted tree is exact.
   Both target claims depend on this boundary.
2. **K built-ins and elaboration.** Integer/Boolean operations, structural
   equality, maps/lists, generated heat/cool rules, reachability circularity,
   simplification, SMT implication checks, and configuration framing are
   trusted. Both claims depend on them.
3. **K toolchain/backends and host execution.** K 7.1.293, the Haskell and LLVM
   backends, solver integration, compiler/runtime, OS, and hardware are trusted.
4. **Trusted translator.** `/reference/py2mpy.py` is trusted as the Python-AST to
   MPY-constructor bridge. Byte regeneration and exact constructor pinning
   detect drift but do not formally prove the translator implementation.
5. **Prompt/canonical interpretation.** The mounted prompt and canonical
   implementation are trusted task inputs. The mapping of ASCII 48/49 plus
   equality/inequality to the ordinary XOR truth table is a small informal
   mathematics/intent bridge, directly reflected in the structural equations.

There is no opaque program-derived result symbol and no empirical-only
operational bridge. The one operational bridge is justified by a universal,
machine-checked, bridge-free connection claim.

The 22 explicit opaque supplied symbols and three noted concrete-only float
helpers are imported trust surface but not theorem dependencies.

### Empirical evidence, kept separate

- 66,036 Python differential checks support implementation-to-canonical
  fidelity on tested inputs.
- Eleven fixed/bridge concrete K assertions support concrete execution
  agreement on tested boundaries.
- Ground K proofs support the empty and documented witnesses.

None of these finite runs replaces the universal reachability claims.

### Gate and benchmark decision

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy: **PASS**; the unrestricted finite bit-string domain
  is covered.
- Gate C, trust/evidence auditability: **PASS**.

The proof is sound under its explicit ordinary trust boundary, constrains the
result, pins the real submitted program, and has no material domain or adequacy
gap.

VERDICT: PASS
LEGITIMACY: LEGIT
