# Independent adversarial audit: 104-unique-digits

The candidate's two target claims reconstruct and print `#Top`, and the Python
implementation is correct on the intended positive-integer domain. The K proof
is nevertheless **not legitimate**. Its priority-40 condition rule replaces the
program's property-bearing digit tests with an unconstrained opaque Boolean
`hasOnlyOddDigits(N)`, and its postcondition filters with the same symbol.
Consequently the theorem closes while remaining unable to distinguish the real
results for `[1]` and `[2]`. Fresh residuals explicitly admit the false cases
`hasOnlyOddDigits(1) = false` and `hasOnlyOddDigits(2) = true`; a control
definition that executes the real condition proves the correct opposite ground
results.

All evidence was generated independently. Candidate prose, compiled
definitions, logs, traces, and prior `#Top` output were treated only as
untrusted claims.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory is present as a real directory, so
there is no mode/mount contradiction and no infrastructure breach.

I used the required `/kit-skills/using-kit/SKILL.md` and
`/kit-skills/validating-proof/SKILL.md`, including their proof-extension
soundness contract. I did not use `writing-semantics`, as required for supplied
semantics.

### Byte/type provenance

The symlink-safe reviewer check in
[provenance_check.py](/audit-output/evidence/provenance_check.py) recursively
compared entry names, types, and SHA-256 digests without following candidate
symlinks. Its complete output is
[01-provenance.log](/audit-output/evidence/01-provenance.log).

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`bebe5af48f3614d96f23c19fa6134409f0b3bfe2f759662569f0987e15e0507c`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Every directory and all 24 files in candidate `reference-semantics/` match
  the trusted supplied tree by type and bytes.
- There are no missing, additional, changed, mistyped, or symlinked entries in
  candidate `reference-semantics/`.
- Required regular files `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
  `spec.k`, and `verification.k` are present.
- The candidate tree has no symlinks or special filesystem entries.
- One structured trace is present as a regular file.

The check exited `0` with `PROVENANCE_FAILURES=0`.

### Untrusted generation records

[generation_claims_digest.py](/audit-output/evidence/generation_claims_digest.py)
consumed the complete four requested generation records and every line of the
structured trace. The bounded digest is
[01-generation-claims.log](/audit-output/evidence/01-generation-claims.log).
The 813 JSONL records had zero parse failures. They claim `VALIDATED`, two
successful positive proofs, three expected negative failures, 5,508 Python
cases, and 148 LLVM assertions. Those claims were not relied upon.

Candidate-provided `runtime-kompiled/`, `verification-*-kompiled/`,
`mpy-proof-kompiled/`, `PROOF.md`, scripts, logs, and mutation artifacts were
ignored for reconstruction. Only source artifacts were copied to
`/tmp/audit-work`, with the semantics copied from the trusted reference mount
rather than from the candidate.

The live tools are `/usr/bin/kompile`, `/usr/bin/kprove`, and `/usr/bin/krun`,
K version `v7.1.293`; see
[00-toolchain.log](/audit-output/evidence/00-toolchain.log).

**Stage 1 result:** PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of positive integers, return a new list containing every
input occurrence whose ordinary base-10 notation has only odd digits
(`1,3,5,7,9`), sorted in increasing numerical order. Duplicates are preserved.
The prompt examples are `[15,33,1422,1] -> [1,15,33]` and
`[152,323,1422,10] -> []`.

The trusted canonical implementation converts each positive integer to decimal
text and retains it exactly when every character has odd numeric parity. The
candidate rejects a number when its decimal text contains any of
`0,2,4,6,8`. These conditions are equivalent for positive integers. Its final
`sorted(result)` preserves accepted multiplicity and establishes ascending
order.

### Translation identity

The exact command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited `0`, and `cmp -s regenerated-solution.mpy solution.mpy` exited `0`.
Both files have SHA-256
`f5ca9b8faf2114fa1f3b4c0fdb853eaa292333b4c385a1018a6fa06db257a45e`.
See [02-program-fidelity.log](/audit-output/evidence/02-program-fidelity.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and candidate entry points under separate module names. It
tests:

- both documented examples;
- empty, singleton, sorting, and duplicate cases;
- every even digit at first, middle, and last decimal positions;
- all-odd and large positive values;
- every singleton integer from 1 through 10,000; and
- 2,000 deterministic generated lists of length 0 through 20, with values up
  to `10^18` and injected duplicates.

The command exited `0` with `TOTAL_CASES=12015` and `MISMATCHES=0`.
The explicit zero probe also agrees. The script records the excluded-domain
case `[-1]`: the canonical raises `ValueError`, while the candidate returns
`[-1]`. This is not an intended-domain divergence because the prompt and K
precondition both require strictly positive elements, but it makes the domain
restriction material and visible.

**Stage 2 result:** PASS for the intended domain.

## 3. Clean proof reconstruction

No candidate-provided compiled definition or cache was copied or referenced.
All output definitions below were freshly created under `/tmp/audit-work`.

### Concrete definition and execution

The reviewer-authored
[concrete_harness.py](/audit-output/evidence/concrete_harness.py) contains the
submitted function plus twelve assertions covering the examples, empty and
singleton inputs, every even digit, all-odd acceptance, ordering, and
duplicates. It was translated with the trusted translator.

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

The build exited `0`
([03b-kompile-llvm.log](/audit-output/evidence/03b-kompile-llvm.log)).

```text
krun concrete_harness.mpy --definition audit-runtime-kompiled
```

Execution exited `0` with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`
([03c-krun-concrete.log](/audit-output/evidence/03c-krun-concrete.log)).

### Isolated loop claim

The base proof definition deliberately excludes the candidate's imported loop
rule:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-base-kompiled
```

Build exit: `0`
([03d-kompile-verification-base.log](/audit-output/evidence/03d-kompile-verification-base.log)).

```text
kprove spec.k --definition audit-verification-base-kompiled \
  --spec-module LOOP-SPEC --claims LOOP-SPEC.outer-loop
```

Proof output: `#Top`; exit: `0`
([03e-kprove-loop.log](/audit-output/evidence/03e-kprove-loop.log)).

### Whole-entry claim

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION-WITH-LOOP --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Build exit: `0`
([03f-kompile-verification-full.log](/audit-output/evidence/03f-kompile-verification-full.log)).

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.entry
```

Proof output: `#Top`; exit: `0`
([03g-kprove-entry.log](/audit-output/evidence/03g-kprove-entry.log)).

Thus every positive target claim closes in a fresh reconstruction. This is
verification under the candidate's extended theory, not yet validation of that
theory.

**Stage 3 result:** PASS mechanically.

## 4. Adequacy and real-program pinning

### Plain-language claims

`LOOP-SPEC.outer-loop` starts at the real `#loop` control item with:

- a represented remaining input `REM`, all of whose elements are positive;
- the exact loop target and submitted loop body;
- the exact trailing `Return(sorted(result)) ~> #endcall`;
- function environment 1 and a complete local scope;
- accumulator list at heap location 0;
- exact frame, allocation counters, return, exception, and exit state.

It claims that the remaining loop filters into heap object 0 according to
`hasOnlyOddDigits`, `sorted` allocates heap object 1 containing
`sortVS(...)`, the function returns `ref(1)`, and the frame/scope are removed.

`SPEC.entry` starts in the supplied initial configuration, loads
`uniqueDigitsModule`, and calls `unique_digits` with
`list(intsToVals(INPUT))`, subject to `positiveIntSeq(INPUT)`. It claims the
same oracle-relative filtered object at location 0 and opaque sorted object at
location 1, plus exact restored scopes, stack, counters, return state,
exception state, and exit code.

### Program identity

The macros at [verification.k](/candidate/verification.k:8) expand to the
submitted AST: docstring, empty result allocation, `for`, assignment to
`digits`, the five exact membership tests, conditional `append`, and final
`sorted` return. `uniqueDigitsModule` wraps that exact body in the submitted
function name and parameter. Together with the trusted translator byte-identity
check, the entry `<k>` term structurally pins `solution.mpy`; it does not prove a
substituted algorithm.

The loop theorem and imported rule also use the real control suffix
`uniqueDigitsReturn ~> #endcall`, not an arbitrary continuation. All
configuration cells are present. I found no independent macro, binding,
allocation, or continuation-pinning defect.

### Satisfiable preconditions

The entry precondition is satisfiable with `INPUT = .IntSeq`; its recursive
definition reduces to `true`, and the listed initial configuration is exactly
the supplied configuration. It is also satisfiable with
`INPUT = iCons(1,.IntSeq)` and `INPUT = iCons(2,.IntSeq)`.

The loop precondition is satisfiable, for example, with
`REM=.IntSeq`, `ORIGINAL=.IntSeq`, `ACC=.ValSeq`, `OLDNUMBER=1`,
`OLDDIGITS=.IntSeq`, and the literal maps/cells in the claim.

### Concrete result substitution

The reviewer specialization
[spec-concrete-adequacy.k](/audit-output/evidence/spec-concrete-adequacy.k)
substitutes concrete satisfying inputs into the claimed result:

| Input | Both Python implementations | Candidate theory | Fixed-condition control |
|---|---|---|---|
| `[]` | `[]` | `#Top`, exit `0` | not needed |
| `[1]` | `[1]` | stuck, exit `1`; admits rejection | `#Top`, exit `0` |
| `[2]` | `[]` | stuck, exit `1`; admits acceptance | `#Top`, exit `0` |

The `[1]` residual in
[04-kprove-accepted-one.log](/audit-output/evidence/04-kprove-accepted-one.log)
reaches a returned empty list under:

```text
false #Equals hasOnlyOddDigits(1)
iCons(49,.IntSeq) #Equals decimalCodes(1)
```

The `[2]` residual in
[04-kprove-rejected-two.log](/audit-output/evidence/04-kprove-rejected-two.log)
reaches a returned list containing `2` under:

```text
true #Equals hasOnlyOddDigits(2)
iCons(50,.IntSeq) #Equals decimalCodes(2)
```

These are concrete false-result witnesses on the intended domain. The
postcondition cannot establish the expected list because it uses the same
unconstrained predicate as the execution bridge.

For a direct operational comparison, the reviewer control definition
[audit-no-condition-bridge.k](/audit-output/evidence/audit-no-condition-bridge.k)
retains the exact program macros and structural input iterator but omits
`decimalCodes`, `hasOnlyOddDigits`, `selectOddAcc`, and the loop summary. It
therefore executes the real five tests using the supplied semantics. A fresh
Haskell build exited `0`, and its ground `[1] -> [1]` and `[2] -> []` claims
both printed `#Top` and exited `0`; see
[05a-kompile-no-condition-bridge.log](/audit-output/evidence/05a-kompile-no-condition-bridge.log),
[05b-kprove-no-bridge-one.log](/audit-output/evidence/05b-kprove-no-bridge-one.log),
and
[05c-kprove-no-bridge-two.log](/audit-output/evidence/05c-kprove-no-bridge-two.log).

The candidate thus pins the program's syntax and outer control flow, but not
the result of its property-bearing computation.

**Stage 4 result:** FAIL.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[05-rule-inventory.tsv](/audit-output/evidence/05-rule-inventory.tsv) enumerates
every declaration and rule in the assembled supplied semantics, all helper K
files, candidate `verification.k`, and `spec.k`, with source line, attributes,
full condensed source, and a decision. The generating script and status log are
[inventory_k.py](/audit-output/evidence/inventory_k.py) and
[05-rule-inventory.log](/audit-output/evidence/05-rule-inventory.log).

Inventory totals are:

| Origin | Configuration | Contexts | Syntax declarations | Rules | Claims |
|---|---:|---:|---:|---:|---:|
| Supplied semantics | 1 | 5 | 227 | 695 | 0 |
| Candidate proof/spec | 0 | 0 | 10 | 20 | 2 |

Each of the 695 supplied rules is marked as the exact byte-matched
`SUPPLIED_FIXED_SEMANTICS`, `SUPPLIED_CONCRETE_RULE`, or
`SUPPLIED_OPAQUE_OR_SYMBOLIC_PRIMITIVE`. Because the problem designates this
tree as trusted supplied semantics, these rules define the selected operational
baseline; they are not candidate proof extensions. The audit nevertheless
traced every construct used by the submitted program through that baseline and
reviewed every candidate extension individually.

### Construct-to-semantics mapping

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, statement list | `syntax.k:61`; `core.k:124-127` loads and sequences statements |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14-16` installs the closure |
| `Call` | `syntax.k:28`; `call.k:20-32` evaluates callee/arguments; `call.k:69-75` creates the function frame |
| `Name` | `syntax.k:12`; `core.k:130-154` walks local/module/builtin scopes |
| docstring `Expr(Str(...))` | `syntax.k:13,52`; `str.k:13-17`; `controls.k:48` discards the value |
| `ListExpr`, allocation | `syntax.k:17`; `list.k:13-15`; `core.k:117-121` allocates heap object 0 |
| `Assign` | `syntax.k:41`; `controls.k:9-18` updates the current scope |
| `For` and target binding | `syntax.k:45`; `controls.k:65-74`; `tuple.k:31-41`; list iteration is `list.k:9-10` |
| `str(number)` | builtin lookup in `core.k:156-181`; call dispatch in `call.k`; `builtins.k:148` |
| `BoolOp` | `syntax.k:16`; fixed short-circuit context/rules in `bool.k:16-25` |
| `Compare`, `CmpOp("not in",...)` | `syntax.k:30,32`; operand order in `operators.k:14-17`; string membership in `str.k:28-41` |
| `If` | `syntax.k:49`; truthiness/branches in `controls.k:51-54` |
| `Attribute(...,"append")` | `syntax.k:29`; bound-method cooling in `call.k:16`; mutation in `list.k:53-55` |
| `sorted(result)` | builtin lookup/call dereference in `core.k`/`call.k`; allocation and `sortVS` in `sort.k:18-37` |
| `Return` and frame pop | `syntax.k:50`; `functions.k:77-90` fixes return, stack, env, scopes, and scope counter |

The supplied configuration accounts for `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The claims constrain all of them. Strictness/contexts and the
shared `#evalArgs` loop establish the relevant evaluation order. The candidate
condition bridge is priority 40 and preempts the fixed BoolOp lookup,
membership, and short-circuit path.

### Candidate extension decisions

1. **Exact macros, lines 8-37 — accepted.** Five syntax aliases exactly
   reproduce `solution.mpy`. They expand at compile time and have no runtime
   state footprint.

2. **`decimalCodes`, lines 41-45 — accepted only as a value-naming boundary.**
   The guarded simplification names
   `strToCodes(Int2String(N))` on `N >= 0`, which covers the strictly positive
   formal domain. It is pure and does not alter cells or control. It overlaps
   the supplied concrete string-code equations; on ground values the residuals
   retain the expected equality, such as
   `decimalCodes(1) = iCons(49,.IntSeq)`. I do not label this rule unsound:
   it can consistently interpret the fresh symbol as the old pure term.
   However, no independent K lemma gives useful decimal-code equations.

3. **Opaque `hasOnlyOddDigits`, lines 50-52 — rejected.** It is declared
   `[function,total,symbol,no-evaluators]` with no equation for any integer.
   It directly determines append/no-append and the final filtered value. This
   is a result-bearing oracle, not an acceptable low-level primitive.

4. **Condition bridge, lines 56-75 — unsound relative to the supplied fixed
   semantics.** It rewrites the entire exact BoolOp to the opaque oracle before
   executing lookups, five string-membership tests, and short-circuit control.
   Its guards pin the local bindings and decimal-code name, and the expression
   is otherwise pure, so arbitrary continuation framing is not the defect.
   The defect is value equivalence: nothing establishes which Boolean the
   oracle returns.

   Required false-conclusion witnesses:

   - For satisfying input `[1]`, the supplied fixed semantics proves that the
     condition accepts and the result is `[1]`. The bridge-enabled theory also
     admits `hasOnlyOddDigits(1)=false` and returns `[]`.
   - For satisfying input `[2]`, the supplied fixed semantics proves that the
     condition rejects and the result is `[]`. The bridge-enabled theory also
     admits `hasOnlyOddDigits(2)=true` and returns `[2]`.

   The exact residuals and fixed-semantics control `#Top` runs are cited in
   Stage 4. Thus this is not merely an absent derivation; the rule enables
   observably false result transitions on the intended domain.

5. **`intsToVals` and iterator exposure, lines 78-87 — accepted.** Empty and
   cons equations are structurally exhaustive and descending. The two iterator
   rules are exactly the corresponding supplied list-iterator steps; they
   preserve the continuation and all state.

6. **`positiveIntSeq`, lines 89-92 — accepted.** The total function covers the
   disjoint empty/cons `IntSeq` constructors and recursively requires every
   head to exceed zero.

7. **`selectOddAcc`, lines 96-113 — locally sound only relative to the rejected
   oracle.** Base equations agree on their overlap. True and negated guards are
   disjoint and exhaustive for a Boolean, and every recursive equation consumes
   one sequence constructor. It correctly defines stable filtering by an
   arbitrary predicate. It does not define filtering by odd decimal digits.

8. **Loop rule, lines 122-152 — exact theorem exposure but tainted.** The rule
   has the same complete `<k>` suffix, bindings, cell transitions, and positive
   precondition as the independently closed loop claim; its `BUILTINS ==
   builtinsScope` guard narrows the variable to the claim's literal scope.
   There is no separate continuation-containment flaw. But the auxiliary theorem
   was proved with the rejected condition bridge in scope, and its result is
   expressed through the same oracle. Exposing it cannot repair that defect.

The candidate defines no other syntax, functions, total/functional
declarations, priority rules, simplifications, ordinary rules, or claims.

### Supplied totality warnings and opaque terms

The LLVM compiler warned that supplied `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt` total matches are non-exhaustive for recently added
`cellsMark` values or an empty sequence. None is reached by this submitted
program or its entry theorem. These are limitations of the trusted supplied
semantics, not candidate modifications, and they do not explain either
positive `#Top`.

The reachable supplied opaque primitive is `sortVS`. It deliberately represents
symbolic ascending sorting, while `[concrete]` rules implement ground insertion
sort in the LLVM definition. That boundary is explicit and low-level. In
contrast, candidate `hasOnlyOddDigits` replaces the central property the task
asks to prove and is reused in the postcondition.

**Stage 5 result:** FAIL because of the condition bridge/result oracle.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`.
[spec-fresh-vacuity.k](/audit-output/evidence/spec-fresh-vacuity.k) specializes
the satisfiable empty input and deliberately changes the result-bearing heap
obligation from empty to `[1]`.

The dry-run command:

```text
kprove spec-fresh-vacuity.k --definition audit-verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC \
  --claims FRESH-VACUITY-SPEC.empty-returns-one --dry-run
```

exited `0`, demonstrating successful parsing and claim construction; see
[06a-fresh-vacuity-dry-run.log](/audit-output/evidence/06a-fresh-vacuity-dry-run.log).

The actual proof command without `--dry-run` exited `1` with
`WarnStuckClaimState`. Its reachable state has returned `ref(1)` but both heap
objects contain `.ValSeq`, directly contradicting the mutated singleton target;
see
[06b-fresh-vacuity-proof.log](/audit-output/evidence/06b-fresh-vacuity-proof.log).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

The candidate theory is therefore discriminating for this false empty-input
postcondition. Non-vacuity does not imply adequacy: the positive theorem still
defines nonempty filtering through the same unconstrained Boolean.

**Stage 6 result:** PASS.

## 7. Proven versus assumed accounting

### What the successful reachability proofs actually establish

Under the candidate-extended K theory, for a finite `IntSeq` of positive K
integers:

- the exact submitted module is loaded and its function frame is created;
- the list accumulator is allocated at location 0;
- the loop traverses the represented input;
- each exact source condition is replaced by an arbitrary total Boolean
  `hasOnlyOddDigits(N)`;
- append behavior and `selectOddAcc` agree on that same Boolean;
- `sorted` allocates location 1 containing the supplied opaque
  `sortVS` of that oracle-filtered sequence;
- the function returns `ref(1)` and restores/removes the exact scopes, stack,
  return state, exception state, and counters in the claim.

This is a partial-correctness theorem relative to an oracle. It neither proves
termination nor proves that the oracle means “all decimal digits are odd.”

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment/evidence |
|---|---|---|
| Trusted supplied MPY source semantics | Defines the language execution for all claims | Authorized fixed baseline; byte-integrity passed. Concrete reviewer harness passed. |
| K built-ins/backend (integers, strings, maps/lists, SMT/reachability engine) | Underlies every semantic and proof step | Ordinary toolchain trust boundary; K version recorded. |
| Trusted translator | Connects `solution.py` to `solution.mpy` | Acceptable; trusted translator reproduced the submitted MPY bytes exactly. |
| `sortVS` | Determines ascending order of the returned symbolic sequence | Explicit supplied primitive. LLVM concrete rules plus finite Python/K evidence support it, but universal sorting correctness is assumed by the formal proof. |
| `decimalCodes` | Names positive integer decimal-code sequences and guards the condition bridge | Pure proof-local abstraction; accepted as a guarded naming boundary, with ground equalities visible. |
| `hasOnlyOddDigits` | Determines the loop branch and final selected elements | Illegitimate result-bearing oracle. No equations or exact auxiliary execution theorem; false ground branches are exhibited. |
| `LOOP-SPEC.outer-loop` exposed as a rule | Summarizes loop, return, allocation, and frame pop for the entry proof | Mechanically derived under the candidate theory, but inherits the oracle defect. |
| Python canonical differential | Supports implementation-to-intent equivalence over 12,015 finite inputs | Strong finite evidence only; it does not prove universal equivalence or exercise `verification.k`. |
| LLVM concrete harness | Supports the submitted program under supplied concrete semantics for twelve cases | Finite evidence only. The LLVM definition imports `MPY-KRUN`, not candidate proof extensions, so it cannot validate the condition bridge. |
| Fixed-condition Haskell control | Shows the supplied condition computes true for 1 and false for 2 | Exact ground proof evidence and an operational-sensitivity witness; not a universal odd-digit theorem. |
| Informal decimal observation | For a positive base-10 numeral, absence of even digit characters is equivalent to all digits being odd | Mathematically elementary and supported by differential tests, but absent from the candidate K theorem because the opaque predicate has no defining equations. |

For completeness, every opaque/symbolic primitive in the supplied source is
enumerated in the inventory. Their names are `md5hexCodes`, `intFloatDiv`,
`divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`,
`divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, and
`sortKeyVS`. Only `sortVS` is reachable here. Candidate-local opaque symbols
are `decimalCodes` and `hasOnlyOddDigits`; both are reachable, and the latter
is fatal.

### Gate accounting and decision

- **Gate A — real-program soundness: FAIL.** The program-defined condition does
  not execute in the proof and has no exact auxiliary theorem. The priority
  bridge admits false observable results for `[1]` and `[2]`.
- **Gate B — intent adequacy: FAIL.** The formal postcondition says “filtered by
  `hasOnlyOddDigits`” without defining that symbol as the natural-language
  predicate.
- **Gate C — trust/evidence auditability: FAIL.** The finite Python and LLVM
  tests support the implementation and supplied concrete semantics, but do not
  exercise or justify the proof-local bridge. Candidate `PROOF.md` incorrectly
  treats this empirical evidence and opaque naming as validation.

The candidate's implementation is faithful, its positive K commands genuinely
close, and its fresh false empty-input result is rejected. Those facts cannot
substitute for a result-constraining theorem about the real condition. The
candidate relies on exactly the forbidden pattern of replacing a
property-bearing computation with an unconstrained oracle and restating that
oracle in the postcondition.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
