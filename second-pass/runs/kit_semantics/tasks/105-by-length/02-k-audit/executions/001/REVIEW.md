# Independent adversarial audit: HumanEval 105 `by_length`

## Conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program over the material source-contract domain: every finite list of Python
integers represented by the supplied MPY semantics. I reconstructed both K
definitions from source, independently proved the loop claim and the complete
specification, checked the submitted program term mechanically, audited the
proof-local theory, and obtained meaningful failures from fresh result and body
mutations.

The candidate's prior `#Top`, compiled directories, logs, `PROOF.md`, and
generation narrative were not used as proof results.

## 1. Input and provenance integrity

The launcher record declares:

- `record_layout`: `pipeline-v3`
- `problem_id`: `105-by-length`
- `condition`: `kit-semantics`
- `semantics_mode`: `SUPPLIED_SEMANTICS`

The rendered mode and mounts agree: `/reference/reference-semantics` is
present. There is no infrastructure breach.

I read `/audit-input.json` first and used only its `container_paths` for mounted
inputs, not the host provenance paths. I then read every required pipeline-v3
record: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. The sole trace JSONL file contains 607
records, parses without error, and has the leaf hash recorded by both the
invocation and result records. These records were treated only as untrusted
claims. The record inspection is in
`/audit-output/evidence/01-generation-records.log`.

The independent integrity checker is
`/audit-output/evidence/verify_integrity.py`; its exact run and results are in
`/audit-output/evidence/01-integrity.log`. Material results:

- `/audit-campaign-lock.json` is a regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object exactly equals the `audit_campaign` block in
  `/audit-input.json`.
- Every launcher-declared mount and every pipeline-v3 required record is
  present with the required regular-file or real-directory type. No required
  record is symlinked.
- The independent pipeline-v3 digest of `/candidate` is
  `14e1f68e49e379a8cc0b7d20c097a2d26bd08ae55fa7d35bc7f0ec3ef7991aea`,
  exactly the generation-result workspace digest.
- All result/invocation evidence leaf hashes match the mounted files,
  including the 1,746,807-byte Codex output and 962,149-byte structured trace.
- The candidate and trusted prompt are byte-identical, both with SHA-256
  `7610e97e9e03b58b9d2f83c6ffb2e08c7a8827a982645a091f53b347cdfa7a5b`.
- The candidate and trusted translator are byte-identical, both with SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- `/reference/canonical.py` has the recorded SHA-256
  `d77e97cb34926421f10b487c7fde94b3dfaafd8fad779f54c9356889365174e6`.
- The trusted and candidate supplied-semantics trees each have exactly 25
  entries. Their relative paths, entry types, and file bytes match
  recursively. Neither tree contains a symlink or unsupported entry. Their
  independent pipeline-v3 digests are both
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the trusted manifest hash.

Thus the candidate did not alter, omit, add to, mistype, or symlink any supplied
semantics entry. This integrity result does not bless `verification.k`; that
file is audited separately below.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `by_length(arr)` to keep integers 1 through 9,
sort them ascending, reverse that order, and replace each digit with its
capitalized English name. It must preserve duplicates, ignore all other
integers, and return `[]` for an empty input.

The canonical implementation sorts descending, then performs dictionary lookup
under `try/except`. On integer-list inputs this returns one name for each
occurrence of 9, then 8, through 1, ignoring every other integer.

The generated implementation uses `collect_digit` nine times, for digits 9
down to 1, and concatenates the nine result lists. Each helper preserves the
number of occurrences of its selected digit. This is a different but
extensionally equivalent algorithm on the intended domain; it does not mutate
the input.

### Trusted regeneration

In a scratch-only copy I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy submitted-solution.mpy
```

The command exited 0. Both MPY files have SHA-256
`405272f000c4e2e3f6b9e509e4ac57529a2aaff6d26d89107f88406753d30be7`.
The exact command and status are in
`/audit-output/evidence/02-regenerate-mpy.log`.

### Independent differential test

`/audit-output/evidence/differential_test.py` imports the trusted canonical
entry point and the generated entry point independently. It checks:

- all three documented examples;
- empty, lower-hit/miss (0/1), upper-hit/miss (9/10), every digit branch,
  duplicates, out-of-range integers, and very large magnitudes;
- every list of lengths 0 through 4 over
  `[-100, -1, 0, 1, 2, 8, 9, 10, 55]`; and
- 10,000 deterministically seeded random lists of lengths 0 through 60.

It compared return/exception outcomes and checked that neither implementation
mutated the input. The run checked 17,393 inputs, found zero mismatches, and
exited 0. See `/audit-output/evidence/02-differential.log`. This is finite
evidence for the Python implementation-to-canonical bridge, not a replacement
for the K proof.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/reconstruction`: the trusted
semantics, trusted translator and references, and candidate `solution.py`,
`solution.mpy`, `verification.k`, and `spec.k`. I did not copy either
candidate-provided kompiled directory, any cache, or a candidate proof log.

The live toolchain is K 7.1.293. Tool paths and versions are recorded in
`/audit-output/evidence/03-toolchain.log`.

### Fresh proof definition and positive claims

The proof definition was built from source:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

It exited 0; see `03-kompile-haskell.log`.

I then ran the helper claim independently:

```text
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.collect-loop
```

It printed `#Top` and exited 0; see `03-kprove-collect-loop.log`.

The complete positive target was:

```text
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC
```

This retains `SPEC.collect-loop` as the circularity needed by
`SPEC.by-length`, proves every claim in the module, prints `#Top`, and exits 0.
See `03-kprove-all.log`.

For completeness, I also tried filtering to `SPEC.by-length` alone. That filter
removes the helper claim from the active claim set, so the prover unrolls the
symbolic loop rather than running the submitted proof architecture. It stayed
CPU-active and was interrupted as a diagnostic, not counted as a positive
failure. The command, reason, process sample, and tool-reported exit 130 are in
`03-focused-entry-diagnostic.txt` and `03-kprove-by-length.log`.

### Fresh concrete definition and execution

I independently built the concrete supplied semantics:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

It exited 0; see `03-kompile-llvm.log`. The independently authored test source
is `/audit-output/evidence/concrete_k_test.py`. Its first 21 lines were compared
byte-for-byte with `solution.py` before translation, so the tests execute the
submitted bodies. They cover the prompt examples, empty input, 0/1/9/10, and
duplicates. The fresh `krun` execution ended with `<k>.K</k>`, `NoExc`, an
empty stack, `noRet`, and exit code 0. See `03-concrete-test-translation.log`
and `03-krun-concrete.log`.

The clean dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.collect-loop` says: starting at the real internal list-loop head with
remaining integer sequence `VS`, accumulator list `ACC`, selected digit `D`,
and selected name `N`, execution terminates that loop prefix and updates the
heap accumulator to `collectAcc(VS,D,N,ACC)`. Other framed state and the active
continuation are preserved. The loop variable may have any final value, which
is correct and irrelevant after the helper returns.

`SPEC.by-length` says: from the ordinary module environment containing the two
real function closures, an empty heap, allocator 0, empty stack, `noRet`,
`NoExc`, and exit code 0, calling `by_length` on an all-integer sequence `VS`
returns `ref(H)` where heap location `H` contains
`list(byLengthVS(VS))`. The module environment and empty stack are restored,
and no exception is introduced. Intermediate heap objects and the advanced
allocator are existentially framed.

The entry precondition is `allInts(VS)`, structurally true exactly when every
element is a K `Int`. It places no bound on list length or integer magnitude.
The formal domain therefore covers the material HumanEval contract rather than
examples, fixed sizes, or bounded unrollings.

### Program term identity

The claim starts from preloaded closures rather than reparsing the module. That
is adequate only if those bindings and bodies are the submitted module. I
checked this mechanically, in the fresh definition:

```text
kast regenerated-solution.mpy ... --sort Module --expand-macros --output kore
kast --expression solutionModule ... --sort Module --expand-macros --output kore
cmp -s parsed-regenerated.kore claimed-solution.kore
```

Both expanded KORE terms have SHA-256
`10e5049cb20bf2a85f351cf3e6d25ac6dfc24baa471271ef41555f3b5132bd80`;
`cmp` exited 0. See `04-program-term-identity.log`. The supplied module-load
and `FuncDef` rules produce exactly the two closure bindings pinned in the entry
claim. This is constructor identity, not a source-name or prose bridge.

The input is the supplied semantics' explicit bare `list(VS)` representation
for read-only claim inputs. Constructed Python list literals allocate refs, but
the semantics deliberately permits bare list values at claim boundaries. This
program never mutates `arr` or observes its identity. The concrete K tests also
exercise ordinary allocated list arguments and agree on all tested cases.

### Result constraint and satisfying witnesses

The return is not free: the returned reference and the heap entry at that same
location are jointly constrained to `list(byLengthVS(VS))`. The summary is a
total structural expression containing, in descending digit order, one name
for each matching input occurrence.

Two explicit satisfying precondition witnesses are:

- `VS = .ValSeq`, for which `allInts(VS)` and `byLengthVS(VS) = .ValSeq`;
- `VS = [0,1,9,10]` in constructor form, for which `allInts(VS)` is true and
  `byLengthVS(VS)` reduces to `["Nine","One"]`.

Both Python implementations return `["Nine","One"]` on the latter witness, as
recorded in `02-differential.log`, and the fresh K concrete test asserts the
same result.

The fresh body-sensitivity mutation changes the closure body actually executed
by the claim to `return []` while retaining the original expected `["One"]` on
input `[1]`. The proof reaches `ref(0)` containing `list(.ValSeq)`, becomes
stuck on the original result obligation, reports `WarnStuckClaimState`, and
exits 1. See `fresh-body-sensitivity.k` and
`04-fresh-body-sensitivity.log`. Thus the theorem depends on the real body, not
only on an external source file or function name.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/k_rule_inventory.py` read every byte of the 24 supplied
K source files plus `verification.k`. Its 1,099-line inventory is
`05-rule-inventory.log` and records each declaration with file, line, complete
normalized text, and attributes. Counts are:

- 1 configuration, 234 syntax declarations, 5 contexts, and 705 rules;
- 149 function-bearing declarations and 110 `total` declarations;
- 45 priority-bearing rules, 35 concrete rules, and 26 `owise` rules;
- 22 `no-evaluators` declarations, 25 explicit symbols, 8 macros plus 1
  recursive macro; and
- exactly 1 simplification rule, in `verification.k`.

There are no `functional` declarations and no proof-local opaque symbols.
There are 695 supplied fixed-semantics rules and 10 rules in
`verification.k`. The two reachability claims are reviewed separately above.

No task symbol (`by_length`, `collect_digit`, `byLengthVS`, `collectAcc`, or
`allInts`) occurs in the supplied semantics. See
`05-task-symbol-isolation.log`. Thus the trusted tree contains no task-answer
rule.

### Every proof-local declaration

1. `collectLoopBody`, `collectDigitBody`, `byLengthBody`, and
   `solutionModule` are syntax macros with four expansion rules. They have no
   runtime state footprint or continuation match. Expanded constructor identity
   with the trusted-regenerated module was established mechanically in Stage 4.

2. `allInts` is a total structural Boolean function. Its empty and `vCons`
   equations are disjoint and exhaustive, and recursion strictly descends on
   the tail. It affects only the precondition.

3. The sole simplification rewrites
   `applyCmp("==", V:Val, I:Int)` to `{V}:>Int ==Int I` under `isInt(V)`.
   It is not an operational bridge: operand evaluation, lookup, comparison,
   `If`, and branch control still execute under fixed semantics. Its complete
   guard is the generated K predicate that says `V` belongs to sort `Int`; the
   cast then recovers that integer. On this domain the supplied MPY-INT rule at
   `semantics/int.k:26` has exactly the same right-hand side.

   I built a separate Haskell definition from supplied semantics only,
   excluding `verification.k`. The statically sorted universal equation
   `applyCmp("==", X:Int, I:Int) => X ==Int I` closes with `#Top` and exit 0;
   see `fixed-semantics-lemma.k`, `05-kompile-fixed-haskell.log`, and
   `05-fixed-semantics-lemma.log`. An attempted direct guarded `Val` statement
   got a condition/cast implication residual because the backend did not infer
   the generated sort refinement; that bounded negative result is preserved in
   `fixed-semantics-guarded-attempt.k` and
   `05-fixed-semantics-guarded-attempt.log`. It is an automation limitation,
   not a false-rule witness. The remaining step is the standard generated
   `isInt`/down-cast contract of K's sort system, part of the named toolchain
   trust boundary.

4. `collectAcc` is a total structural function with empty and `vCons`
   equations. They are disjoint and exhaustive; the recursive call descends on
   `REST`. On an integer head it appends `N` exactly when the fixed equality is
   true. Its off-domain branch ignores non-integers, but no reachability claim
   uses that branch because `allInts(VS)` is required. Crucially, it does not
   replace program execution: `SPEC.collect-loop` is the fixed-semantics
   universal connection theorem from the exact loop configuration to this
   summary, and that claim independently closes.

5. `byLengthVS` is one total definitional equation. It concatenates nine
   `collectAcc` results for digits 9 through 1. It is not an oracle and has no
   operational rewrite. The entry reachability claim connects execution of all
   nine real helper calls and eight real list concatenations to it.

The local equations have no inconsistent overlap, uncovered total case,
non-descending recursion, priority preemption, unconstrained fresh value, or
abrupt control rewrite. There is no operational bridge requiring a
continuation-containment theorem.

### Used supplied-semantics slice

Every material source constructor maps to supplied syntax and rules:

- `Module`, `FuncDef`, `Params`, statements, expressions, and list forms are
  declared in `semantics/syntax.k`.
- The configuration, module sequencing, allocation, name lookup, left-to-right
  argument evaluation, literals, and sequence helpers are in
  `semantics/core.k`.
- Definition binding, parameter binding, return, frame pop, callee evaluation,
  calls, and stack/environment restoration are in `functions.k` and `call.k`.
- `Assign`, `If`, `For`, loop steps, and target binding are in `controls.k` and
  `tuple.k`.
- List iteration, empty-list allocation, concatenation allocation, and
  in-place `append` are in `list.k`.
- comparison evaluation order is given by the contexts in `operators.k`;
  integer equality is in `int.k`; ASCII string literal conversion is in
  `str.k`.

Strictness/contexts evaluate assignment RHSs, loop iterables, conditions,
returns, expression statements, attributes, and nested binary operands in the
required order. Calls evaluate the callee and arguments left-to-right. A
function call allocates a scope frame, binds parameters, pushes the
continuation, executes the exact body, and restores the caller on return.

The relevant priority rules are sound and narrow: list `+` at priority 45
allocates the concatenated list before generic binary dispatch; heap-ref
deref rules preserve the pointed-to list value; `append` at priority 40 updates
only the receiver's heap entry. The loop claim reads the current scope and
accumulator heap entry, writes only the loop variable and that heap entry, and
frames every other cell. The entry claim constrains return, heap, environment,
stack, exception, and exit-code behavior.

### Remaining supplied rules and warnings

The other supplied declarations were inventoried and checked for task-specific
smuggling, reachable symbol overlap, priority interference, and opaque value
flow into this theorem. They introduce symbols not present in the submitted
constructor term or its summaries and therefore cannot rewrite a reachable
target subterm. In particular, none of the 22 `no-evaluators` symbols
(`sortVS`, `sortKeyVS`, the float abstractions, and `md5hexCodes`) occurs in the
program, local theory, precondition, branch conditions, or postcondition.

The LLVM build reports six incomplete-match warnings in the supplied baseline:
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and out-of-bounds
`valSeqAt`. None is reachable from this program. A missing equation for an
unused input is not a concrete false conclusion witness, so I do not label
these rules unsound. They are a precise unused-semantics limitation, not a
material adequacy gap for this theorem.

No reviewed rule encodes the task answer, fabricates a reachable result,
bypasses a program-defined operation, or admits a concrete/symbolic false
conclusion on the intended input domain.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation is
`/audit-output/evidence/fresh-false-result.k`, copied unchanged into scratch.
Its precondition is the concrete satisfying input `[1]`. It preserves the real
closures and real body but changes the result-bearing postcondition from
`["One"]` to `[]`.

The exact command was:

```text
kprove fresh-false-result.k \
  --definition fresh-verification-kompiled \
  --spec-module FRESH-FALSE-RESULT
```

It parsed and executed successfully up to the false obligation. The residual
contains returned `ref(16)` and heap location 16 equal to a singleton string
with character codes for `"One"`, while the destination requires an empty
list. It reports `WarnStuckClaimState` and exits 1. This is the expected unmet
postcondition, not a parser error, missing import, timeout, or unrelated crash.
See `06-fresh-false-result.log`.

The proof is therefore result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What is formally proven

Under the supplied MPY semantics and the proof-local definitions audited above,
for every finite `ValSeq` consisting only of K integers, if the pinned
`by_length` call terminates from the stated ordinary module configuration, then
it returns a heap reference whose object is exactly the concatenation of the
digit-name groups for 9 down to 1. The call restores the module environment and
empty stack, leaves `noRet` and `NoExc`, and preserves exit code 0. The helper
loop theorem establishes the exact accumulator transformation used by the
entry theorem.

This implies the requested filter/sort-descending/name behavior because grouping
one identical name per occurrence of 9, then 8, through 1 is mathematically the
same result as filtering integer digits, sorting ascending, reversing, and
mapping names. Duplicates and empty input are handled structurally. The proof
does not establish termination; that is appropriate for the requested
partial-correctness judgment.

### Trust ledger

- **K 7.1.293 frontend, Haskell prover, LLVM backend, SMT reasoning, and
  reachability/circularity implementation:** trusted toolchain boundary. All
  proof conclusions depend on it.
- **The supplied semantics tree:** trusted fixed model after exact integrity
  comparison. The actually used subset was statically audited above. Its model
  uses unbounded mathematical integers and ASCII strings, which are adequate
  for this integer-input task and its English output constants.
- **K builtin Int/Bool/String/Map/List theories, generated sort predicates and
  casts:** trusted low-level mathematical/runtime boundary. The proof-local
  equality refinement depends on the generated `isInt`/Int-cast relation.
- **Trusted `py2mpy.py`:** trusted source-to-constructor frontend. Byte
  regeneration and expanded constructor identity connect `solution.py`,
  `solution.mpy`, and the claim bodies.
- **Ordinary mathematical intent bridge:** concatenating occurrence groups in
  order 9 through 1 equals descending sort followed by name mapping. This is a
  direct finite digit partition argument, not an empirical oracle.
- **Differential and concrete tests:** finite supporting evidence only. They
  support Python fidelity and concrete semantics execution but are not used as
  substitutes for either reachability claim.
- **Opaque/imported symbols:** no proof-local opaque symbol exists, and no
  supplied `no-evaluators` symbol influences execution, control, state, or the
  postcondition of this theorem.
- **Excluded behavior:** non-integer elements, non-list inputs, mutation/identity
  observations of the input, unsupported Python features, and termination are
  outside the formal theorem. These exclusions do not narrow the stated
  HumanEval contract, which asks for an array of integers and partial
  correctness.

Gate A passes: the real program executes, the proof-local theory is sound on
its complete used domain, the result is constrained, and both mutation tests
are discriminating. Gate B passes: the unbounded integer-list precondition and
postcondition cover the material source contract. Gate C passes: assumptions
and finite evidence are explicit and all reviewer artifacts and exact command
logs are preserved below `/audit-output/evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
