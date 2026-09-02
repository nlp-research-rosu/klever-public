# Adversarial audit: 72-will-it-fly

## Executive decision

The candidate contains a legitimate, result-constraining partial-correctness
proof for finite lists of integers and an integer weight. I independently
rebuilt the supplied concrete semantics and the Haskell proof definition,
proved each of the three entry claims separately, checked that the named K
program is structurally identical to the trusted translation of
`solution.py`, and obtained the expected stuck residual from a fresh false
postcondition.

The decision is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for three
non-fatal limitations:

1. `verification.k` adds two operational summaries, for full reverse slicing
   and integer `sum`. They are mathematically correct on every finite
   constructor `ValSeq` in the intended integer-list domain, and ground
   fixed-versus-extended Haskell executions agree exactly, but the candidate
   includes no bridge-free universal K connection theorem.
2. The rules are syntactically broader than that ground domain: they also
   match symbolic or opaque `ValSeq` terms for which the fixed theory does not
   establish the same equation. I found no concrete or symbolic false
   conclusion on the intended integer-list domain, so this is an evidence and
   scope concern, not an unsoundness finding.
3. The natural-language prompt does not explicitly state that elements and
   `w` are integers, while all three formal claims require an integer
   `ValSeq` and `W:Int`. The theorem does not cover floats or other
   Python-summable values.

All evidence below was generated from source in
`/tmp/audit-work/72-will-it-fly`; no candidate-built definition or cache was
used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode. There is no infrastructure breach.

I recursively compared the candidate semantics tree against the trusted tree
using `diff --no-dereference -r`. The trees are identical, with no symlink or
non-file/non-directory entry:

- command and result: `evidence/05_semantics_integrity.log`
- candidate inventory: `evidence/01_candidate_inventory.log`
- trusted inventory: `evidence/02_reference_inventory.log`

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted counterparts. Their SHA-256 values and `cmp` statuses are in
`evidence/04_prompt_translator_compare.log`.

### Missing and additional evidence

The following requested provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present under `/candidate`. This is
recorded in `evidence/03_provenance_presence.log`. Their absence prevents
auditing generation chronology but does not prevent independent
reconstruction from the submitted source.

The candidate also contains untrusted convenience evidence (`prove.sh`,
`concrete-tests.py`, `concrete-tests.mpy`, and a Python bytecode cache). None
was trusted or reused. Only source artifacts needed for reconstruction were
copied; source-copy paths and hashes are in
`evidence/06_scratch_source_copy.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From trusted `prompt.py` and `canonical.py`, `will_it_fly(q, w)` returns true
exactly when:

1. `q` is balanced, meaning it reads the same forwards and backwards; and
2. `sum(q) <= w`.

Otherwise it returns false. The examples cover an unbalanced object, a
balanced overweight object, a balanced object within the bound, and a
singleton.

The formal proof selects the domain:

- `q`: a finite K `ValSeq` whose elements are all K integers;
- `w`: a K integer.

On that domain, the candidate implementation

```python
def will_it_fly(q, w):
    return q == q[::-1] and sum(q) <= w
```

is extensionally equivalent to the canonical early-return/loop
implementation. It also preserves Python's short-circuit order: reverse and
equality execute first; `sum` executes only when the list is palindromic.

### Translation fidelity

Using `/reference/py2mpy.py`, I regenerated `solution.mpy` from the submitted
`solution.py`. The regenerated file is byte-identical to the submitted file:

- `translation_byte_cmp=0`
- submitted and regenerated SHA-256:
  `7c0e0763451ba64ad5a942a7e0cf477e9755446d733bd21ae8221636efd7efa0`

See `evidence/07_trusted_translation.log`.

### Independent differential test

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch copy of the generated
`solution.py`. Its deterministic input definition is preserved both in the
script and in `evidence/differential-inputs.json`. It covers:

- all four documented examples;
- empty-list, singleton, negative-sum, even-palindrome, and exact-weight
  boundaries;
- every list of length 0 through 5 over `{-2,-1,0,1,2}`, with weights just
  below, at, and just above its sum plus fixed weights;
- 2,000 seeded lists of lengths 0 through 20 with values in `[-100,100]`.

The run compared 23,118 cases and found zero mismatches. The exact command,
case-stream hash, label counts, and status are in
`evidence/08_differential.log`.

Differential testing is finite evidence for the Python-to-intent bridge; it
is not used as a substitute for the K proof.

## 3. Clean proof reconstruction

### Toolchain and clean builds

The installed toolchain is K v7.1.337
(`evidence/00_toolchain.log`). Scratch was populated only from candidate
source and trusted mounted source. No candidate-provided compiled definition
exists in the scratch source copy.

I built the concrete definition from the trusted supplied semantics:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The command exited 0. The compiler emitted several non-exhaustive-totality
warnings in the supplied semantics; the only one in the submitted program's
dependency cone is `valSeqAt`. Its use in a full slice is in bounds for a
finite constructor list. Full output is in
`evidence/10_kompile_concrete.log`.

An independently authored K concrete assertion harness,
`evidence/k_concrete_tests.py`, embeds an AST-identical copy of the submitted
entry point and includes one satisfying input for each claim plus empty,
threshold, even-palindrome, and negative-sum boundaries. Its trusted
translation is recorded in `evidence/09_concrete_harness_translation.log`.
`krun` exited 0 with empty `<k>`, `NoExc`, and exit code 0
(`evidence/11_krun_concrete.log`).

I then built the proof definition from `verification.k` and the trusted
semantics:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0; see `evidence/12_kompile_proof.log`.

### Every positive target claim

The combined candidate `spec.k` exited 0 and printed `#Top`
(`evidence/13_kprove_all.log`). I also extracted each claim unchanged into a
one-claim module and ran it independently:

| Claim | Artifact | Evidence | Exit/result |
|---|---|---|---|
| balanced and within weight | `evidence/spec-balanced.k` | `evidence/14_kprove_balanced.log` | 0, `#Top` |
| unbalanced | `evidence/spec-unbalanced.k` | `evidence/15_kprove_unbalanced.log` | 0, `#Top` |
| balanced but overweight | `evidence/spec-overweight.k` | `evidence/16_kprove_overweight.log` | 0, `#Top` |

Thus the positive reconstruction gate passes. This establishes closure under
the supplied semantics plus the actual proof extensions; it does not by
itself establish that those extensions are sound.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

All claims begin in a clean module environment with the trusted builtins
scope, empty heap, no stack frame, no pending return or exception, and exit
code 0. They load `willItFlyModule`, call `will_it_fly` with the bare list
value `list(VS)` and integer `W`, and constrain the final stack/control cells.
The slice allocates heap location 0 containing the reverse and advances
`heapLoc` from 0 to 1.

1. **Balanced and within weight:** if every element of `VS` is an integer,
   `VS == reverseVS(VS)`, and `sumIntVS(VS) <= W`, execution returns the
   literal K Boolean `true`.
2. **Unbalanced:** if every element is an integer and
   `VS != reverseVS(VS)`, execution returns literal `false`, independently of
   `W`. This matches the generated program's short circuit.
3. **Balanced but overweight:** if every element is an integer,
   `VS == reverseVS(VS)`, and `sumIntVS(VS) > W`, execution returns literal
   `false`.

The claims jointly cover every finite integer list and integer weight:
palindrome/non-palindrome is exhaustive, and for a palindrome the integer
sum is either `<= W` or `> W`.

### Exact program and control-flow pinning

The `<k>` cell does not cite `solution.mpy` by filename. Instead,
`verification.k` names the translated expression, module, and closure.
I mechanically expanded those aliases and compared the result to submitted
`solution.mpy`:

- expanded `willItFlyModule` equals compacted submitted `solution.mpy`;
- expanded `willItFlyClosure` equals the closure created by loading that
  module and body;
- both comparisons are true, with hashes in
  `evidence/29_program_pinning.log`.

Therefore this is a named copy of the actual submitted translated program,
not a substituted algorithm.

The execution path is real: `#loadAll` executes `FuncDef`; normal name lookup
finds the loaded closure; call routing evaluates arguments left-to-right;
the call rule allocates and binds a frame; `Return` evaluates the submitted
`BoolOp`; `#pop` restores and removes the call frame. There is no helper or
loop claim because the generated implementation has no loop.

The returned value is a literal `true` or `false`, not a free variable,
oracle, or implication-only postcondition. The claims also constrain the
scope, heap allocation, stack, return, exception, and exit-code cells.

### Satisfiable preconditions and concrete substitution

`evidence/claim_witnesses.py` and
`evidence/28_claim_witnesses.log` exhibit and evaluate:

| Claim | `q` | `w` | Preconditions | Canonical/generated |
|---|---:|---:|---|---|
| balanced-within | `[3,2,3]` | 9 | palindrome, sum 8 <= 9 | true/true |
| unbalanced | `[1,2]` | 5 | not palindrome | false/false |
| balanced-overweight | `[3,2,3]` | 1 | palindrome, sum 8 > 1 | false/false |

Thus none of the entry preconditions is empty, and concrete substitutions
agree with both Python implementations.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and review method

The exhaustive normalized inventory is:

- `evidence/k-statement-inventory.md`
- `evidence/k-statement-inventory.tsv`
- generator and counts: `evidence/k_inventory.py` and
  `evidence/20_k_inventory.log`

It contains 952 statements from every supplied K source, `verification.k`,
and `spec.k`: 234 syntax declarations, 709 rules, 5 contexts, 1
configuration, and 3 claims. Each row records file/line, full normalized
statement including guard and attributes, opaque status, and a disposition.

The fixed supplied tree is the selected semantics in
`SUPPLIED_SEMANTICS` mode. Of its inventoried statements, 185 are in the
closed program's execution/proof dependency cone and 743 are unreachable
from the submitted syntax and initial configurations. The unreachable rules
cannot contribute to claim closure. The used subset is mapped below and was
checked against program behavior. This supplies a disposition for every
inventoried fixed rule without treating unused float, dict, comprehension,
sort, method, and other constructs as candidate proof extensions.

There are 25 opaque or symbol-designated primitives in the supplied tree
(float operations, sorting, and MD5). Every one is marked unreachable in the
inventory. No opaque primitive can influence a branch, state cell, or result
of this program. There are no `[simplification]` or `[functional]` rules in
the inventoried sources.

### Used-construct map

| Submitted construct | Declaration and operative rules | Check |
|---|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | `syntax.k`; load/sequencing in `core.k`; closure creation/return/pop in `functions.k`; closure dispatch in `call.k` | Exact body, arguments, defining scope 0, return, stack and frame cleanup are pinned |
| `Name("q")`, `Name("w")`, `Name("sum")` | lookup and `builtinsScope` in `core.k` | Local parameters shadow builtins; `sum` falls through to scope -1 |
| `BoolOp("and",...)` | syntax/context and short-circuit rules in `bool.k` | Left operand executes first; false returns immediately; true evaluates sum comparison |
| `Compare`/`CmpOp("==")` | contexts/dispatch in `operators.k`; list equality in `list.k` | Both operands evaluate; sliced ref is dereferenced; integer-list equality is structural K equality |
| `Subscript`/`Slice`/`NoBound` | `subscript.k` bound evaluation, list dereference, slice, allocation, and fixed slice helpers | Step evaluates to -1; list slice allocates; bridge replaces only the pure `doSlice` value |
| `UnaryOp("-", Int(1))` | literal rule in `core.k`, unary dispatch in `operators.k`, integer negation in `int.k` | Produces step -1 |
| `Call(Name("sum"), Name("q"))` | callee/argument evaluation and builtin routing in `call.k`; list iteration and sum fold in `list.k`/`builtins.k` | Correct binding and left-to-right argument evaluation; bridge applies only to accumulator 0 and all-int sequences |
| `CmpOp("<=", Name("w"))` | comparison dispatch and integer comparison in `operators.k`/`int.k` | Produces the final Boolean for the second operand |
| configuration/cells | `core.k` configuration; allocation, frame, return and exception rules | Claims provide a realizable clean state and constrain all active cells |

The syntax uses no assignment, mutation, exception, external state, loop, or
user-defined helper call. Rules for those constructs are outside the
dependency cone.

### Candidate proof-extension inventory

`verification.k` contributes 21 inventoried statements: 7 declarations and
14 defining/operational rules. They fall into the following complete groups.

| Extension | Class and domain | State/control footprint | Static decision |
|---|---|---|---|
| `allInts` and 3 equations | Definitional predicate over `ValSeq` | None | Empty/Int-head/non-Int-head cases cover ground constructor sequences; guarded cases do not disagree |
| `sumIntVS` and 2 equations | Definitional integer sum, used under `allInts(VS)` | None | Base/recursive equations are ordinary integer summation and descend on the tail. `[total]` is broader than its explicit non-int equations, but non-int cases are excluded on intended inputs |
| `snocVS` and 2 equations | Definitional append-one | None | Constructor-complete, disjoint, tail-recursive descent |
| `reverseVS` and 2 equations | Definitional reverse via `snocVS` | None | Constructor-complete and terminating on finite sequences |
| specialized `doSlice(...,-1) => list(reverseVS(VS))` at priority 40 | Operational bridge over any `ValSeq` | Pure term only; allocation has already been selected by the fixed `<k>` rule; no cell or abrupt-control change | Correct by the supplied `slStart/slStop/slStep/buildVS` equations for finite constructor sequences; universally broader than the checked domain and lacks a machine-checked connection theorem |
| `<k> #sumAcc(list(VS),0) => sumIntVS(VS) ... </k>` under `allInts`, priority 40 | Operational bridge over any continuation | Reads no cells, writes no cells, preserves continuation and control; replaces a terminating pure list fold | Correct by induction over finite all-int sequences; guard excludes Python/K non-int summation behavior; lacks a machine-checked connection theorem |
| `willItFlyResult` plus defining rule | Exact syntax alias | Expands to submitted expression | Mechanically identical to submitted translation |
| functional `willItFlyModule` plus defining rule | Exact module alias | Expands to submitted module | Ground, terminating, no overlap |
| functional `willItFlyClosure` plus defining rule | Exact loaded-closure alias | Pins params/body/defining scope | Mechanically identical to the closure fixed semantics creates |

There are exactly two candidate priority rules: the two operational bridges.
There is no candidate opaque symbol, simplification, lemma, auxiliary claim,
or rule that returns the task answer without executing the submitted
expression.

### Bridge checks and limitations

For operational sensitivity, `evidence/bridge_ground_tests.py` runs reverse
and sum on empty, ordinary, and negative-valued lists and immediately feeds
each result into a distinct arithmetic continuation. I ran it with:

- fixed Haskell semantics without either bridge:
  `evidence/24_bridge_ground_fixed_haskell.log`;
- the candidate extended Haskell definition:
  `evidence/23_bridge_ground_extended.log`.

The complete final configurations are byte-identical
(`final_configuration_diff=0` in
`evidence/25_bridge_ground_haskell_compare.log`). This checks value, active
continuation, scopes, allocation, stack, return, exception, and exit code for
the ground witnesses. The LLVM fixed run also returns successfully
(`evidence/22_bridge_ground_fixed.log`), although its final heap omits the
temporary slice allocations that the Haskell backend retains. The returned
results agree, and the same-backend Haskell comparison shows that the
candidate bridge does not cause the heap difference. This backend-level
state discrepancy in the supplied semantics is an additional empirical
limitation, not a false-result witness for the proof.

I independently attempted bridge-free universal claims using
`evidence/bridge-base.k`, which contains only renamed mathematical
definitions and no operational bridge:

- The slice connection attempt builds, then sticks on the missing universal
  equality between `buildVS(VS, vsLen(VS)-1, -1, -1)` and reverse
  (`evidence/18_kprove_slice_connection.log`).
- The sum connection attempt enters a symbolic float alternative despite the
  `auditAllInts` condition and terminates on a missing Haskell float hook
  (`evidence/19_kprove_sum_connection.log`).

The latter is an auxiliary-audit backend failure, not a failed candidate
positive claim. Neither result is counted as proof that a bridge is false.
For every finite ground `ValSeq`, the algebraic equations establish the two
equalities by ordinary induction, and the fixed-versus-extended ground
checks find no opposite result.

The syntactic bridge domains also admit opaque terms such as
`list(sortVS(...))`, where the fixed supplied theory leaves the connection
unproved. Such terms are not realizable values of the intended input
encoding from a finite Python integer list. Because the audit found no
false conclusion witness on a satisfying intended input, I classify this as
over-broad-but-sound-on-the-intended-domain, not as an unsound rule.

## 6. Fresh non-vacuity test

I created `evidence/spec-false-balanced.k`. It keeps the balanced/within
precondition and all state obligations unchanged but changes the required
result from `true` to `false`.

The mutation is demonstrably false: `VS = [3,2,3]` and `W = 9` satisfy
`allInts`, palindrome, and sum 8 <= 9, while both Python implementations
return true (`evidence/28_claim_witnesses.log`).

The mutation parsed and compiled to KORE successfully:

- command: `kprove ... --spec-module SPEC-FALSE-BALANCED --dry-run`
- exit: 0
- evidence: `evidence/26_mutation_dry_run.log`

The actual proof then failed for the expected obligation:

- exit: 1;
- `WarnStuckClaimState`;
- residual final `<k>` is `true`, while the destination requires `false`;
- all original balanced preconditions remain in the residual.

See `evidence/27_mutation_kprove.log`. This is a meaningful reachable
postcondition failure, not a parser error, timeout, missing import, or
unrelated crash. The proof is non-vacuous and result-sensitive.

## 7. Proven-versus-assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics plus the two proof-local summary rules, for
every finite constructor sequence of K integers and every K integer `W`:

- a palindromic sequence with sum at most `W` returns true;
- a non-palindromic sequence returns false for every `W`;
- a palindromic sequence with sum greater than `W` returns false.

Execution is of the exact submitted translated expression through module
load, name lookup, argument evaluation, function binding, return, and frame
cleanup. The claims also establish the specified reverse-slice heap object,
allocation counter, clean stack/return/exception cells, and exit code.

Together, the claims characterize the result as
`q == reverse(q) and sum(q) <= w` on the formal integer domain. This is a
partial-correctness result: it asserts the postcondition for the modeled
executions; termination of arbitrary Python outside this finite input model
is not a theorem here.

### Trust ledger

| Boundary | Dependents/influence | Assessment |
|---|---|---|
| K v7.1.337 parser/compiler, Haskell/LLVM backends, Kore engine, builtin integer/Boolean/map/list equality operations | All builds and proofs | Necessary toolchain trust; clean reconstruction and exact logs make it auditable |
| Trusted mounted supplied semantics | Entire operational execution | Required selected semantics boundary; candidate copy is recursively identical. Used rules were mapped and concretely exercised |
| Trusted `py2mpy.py` | Python-to-MPY syntax bridge | Byte identity proves the submitted MPY is its output; purity of the trusted translator is an external trusted input |
| `allInts`, `sumIntVS`, `snocVS`, `reverseVS` equations | Claim preconditions and bridge results | Ordinary terminating algebraic definitions on constructor sequences; no opaque result on intended inputs |
| Reverse-slice bridge | Palindrome comparison and final heap | Informally justified by supplied slice equations and ground fixed/extended equality; no bridge-free universal theorem, so concerning but not illegitimate on intended inputs |
| Integer-sum bridge | Weight comparison | Informally justified by the supplied iterator fold and ground fixed/extended equality; no bridge-free universal theorem, so concerning but not illegitimate on intended inputs |
| Python finite integer lists/K `ValSeq`, Python integers/K `Int` adequacy bridge | Natural-language interpretation | Sound for unbounded integer arithmetic and structural list equality; excludes floats and other values not explicitly excluded by the prose |
| Trusted canonical implementation | Differential oracle only | Supports implementation-to-intent alignment over 23,118 cases; is not part of, and does not replace, the K proof |
| Supplied opaque float/sort/MD5 symbols | None | All are unreachable from this program and the claims |

### Final gate assessment

- Fresh reconstruction and positive closure: pass.
- Real-program identity, result constraint, satisfiable preconditions, and
  non-vacuity: pass.
- Static soundness on finite integer-list inputs: pass; no false conclusion
  witness found.
- Universal bridge evidence and formal-domain-to-prose breadth: concern.
- Proven facts, conditional trust, finite evidence, and excluded behavior
  are separated above.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
