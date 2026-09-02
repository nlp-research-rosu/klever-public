# Independent adversarial review: 67-fruit-distribution

## Executive finding

The positive proof reconstructs: a clean Haskell `kprove` run exits 0 and
prints `#Top`, the theorem is result-constraining, and the term named
`solutionProgram` is mechanically identical to the trusted translation of
`solution.py`. Those facts are not enough to make this a proof over the real
HumanEval input domain.

The only universal claim invokes the real body with `s` bound to the invented
non-Python value `VFruits(A,O)`. Its task-specific `split` rule directly places
`A` and `O` in the two result-bearing word positions. The same `A` and `O`
appear in the postcondition, and there is no bridge-free theorem connecting
this path to execution on any actual string. Actual strings occur only in four
ground example claims. Moreover, the generated string semantics disagrees
with both Python implementations on a repeated-space input accepted by both.
This is a substituted-input proof and a material narrowing, which the
benchmark maps to `FAIL / NOT_LEGIT`.

The command index is `evidence/COMMANDS.md`. All reconstruction and mutations
were performed below `/tmp/audit-work/fruit67`; no candidate-provided
definition or cache was reused.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `67-fruit-distribution`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`; and
- no mounted reference semantics.

The campaign object is structurally identical to
`/audit-campaign-lock.json`, and the lock's file digest is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly as recorded. The mounted canonical, prompt, translator, run/task
manifests, stage result, invocation, metrics, usage, generation prompt,
generation final message, and generation log all match their recorded
file-level SHA-256 values. Candidate `prompt.py` and `py2mpy.py` are byte
identical to their trusted mounts. All required candidate, record, and trace
entries are regular files/directories rather than symlinks or special files.
See `evidence/01_provenance_check.py` and
`evidence/01_provenance_check.log` (exit 0).

The independently computed pipeline tree digest of the mounted candidate is
`3fe91c599f63a5d1fc1b8379466bcf5590765192112b0395a5a86ef80048e8f3`;
it exactly equals both `generation-result.json`'s output-workspace digest and
`invocation.json`'s retained-workspace digest. The corresponding trace digest
is `88578b8239308798ac3172e2f5f52e8bf6afa3f38eb9d55b594f6947ebdd6622`,
matching `usage.json`. The launcher also records separate tree-digest fields
whose algorithm is not stated in the record; they were retained as provenance
claims, not substituted for these independently calculated digests.

All 15,326 lines of `codex-output.log` and all 222 JSONL trace records were
streamed and inspected; every trace line is valid JSON. The untrusted
generation report claims `KPROVE_PASSED` and contains `#Top`, but no verdict
below depends on that claim. See `evidence/01_generation_record_scan.py` and
its exit-0 log. `usage.json` was present and inspected. Historical
`runtime-metrics.json` is absent, which is permitted for this declared legacy
layout. `/reference/reference-semantics` and
`/candidate/reference-semantics` are both absent, exactly as required for
`GENERATED_SEMANTICS`.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The prompt's contract is: `s` describes the apple and orange counts in a
basket, `n` is the total fruit count, and the function must return the number
of mangoes, namely `n - apples - oranges`. The trusted canonical scans every
literal-space-delimited token, converts every `isdigit()` token, sums them,
and returns `n - sum(numbers)`.

The submitted implementation instead evaluates:

```python
words = s.split()
return n - int(words[0]) - int(words[3])
```

Trusted regeneration produced a byte-identical `solution.mpy`:

```text
TRANSLATOR_EXIT_STATUS=0
CMP_EXIT_STATUS=0
SHA256(regenerated) = SHA256(submitted)
                    = a1215c2919dc54784dd3505ec12199891cb1307512e572cbc32bfd72b0ee34f2
```

See `evidence/02_translation_identity.log`.

The independent differential script used separately imported trusted
`canonical.py` and submitted `solution.py`. It found:

- 0 mismatches on all four documented examples;
- 0 mismatches on nine exact-format boundary cases;
- 0 mismatches on 500 seeded generated exact-format cases; and
- 7 mismatches on 7 canonical robustness probes.

The mismatches include the empty string (canonical returns `n`, submitted code
raises `IndexError`), alternate word placement, additional numeric tokens,
tabs, and signed text. Full inputs and outcomes are in
`evidence/02_differential.py` and `evidence/02_differential.log` (exit 0).
Finite testing supports equivalence on the exact five-word example grammar; it
does not prove that grammar is the whole source contract. The prompt does not
formally impose the candidate's fixed positions, while the trusted canonical
accepts a materially broader set of strings.

## 3. Clean proof reconstruction

Only source files were copied to scratch. Fresh output directories were
created with explicit names. The following commands, all preserved verbatim
in `evidence/03_rebuild.log`, succeeded:

```text
kompile semantic.k --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition audit-semantic-llvm-kompiled
# exit 0

krun solution.mpy --definition audit-semantic-llvm-kompiled --output pretty
# exit 0; registers the exact function body

kompile verification.k --main-module VERIFICATION --syntax-module VERIFICATION \
  --backend llvm --output-definition audit-verification-llvm-kompiled
# exit 0

kompile verification.k --main-module VERIFICATION --syntax-module VERIFICATION \
  --backend haskell --output-definition audit-verification-haskell-kompiled
# exit 0

kprove spec.k --definition audit-verification-haskell-kompiled \
  --spec-module SPEC
# output #Top; exit 0
```

The single positive target command proves every one of the five claims in
`spec.k`; none is filtered out.

Fresh Haskell concrete runs returned 0, 8, and 7 on exact-format boundary,
normal, and large inputs, matching both Python implementations. Ground
`runFruit` tests returned 0 and 8 as encoded. See
`evidence/03_concrete_compare.log` (exit 0).

There is also a material concrete semantics failure. For
`("5  apples and 6 oranges", 19)`, both Python implementations return 8, but
the Haskell K execution yields `#Bottom`. The corresponding reachability claim
fails with `words[3] = VStr("and")`; see
`evidence/05_string_boundary_claim.log`. This is an expected unmet semantic
obligation, not a parser error or unrelated crash.

## 4. Adequacy and real-program pinning

### Plain-language claims

The entry claim at `/candidate/spec.k:9` says: for all mathematical integers
`A`, `O`, and `N` with `A >= 0`, `O >= 0`, and `N >= A+O`, start from empty
function/environment cells, install `solutionProgram`, invoke it through
`invokeFruit(A,O,N)`, and terminate with exactly
`VInt(N-A-O)` and empty cells.

The claims at lines 20, 27, 34, and 41 say the exact submitted program returns
8, 2, 95, and 19 for the four literal example strings. They have no symbolic
input domain.

All entry states are satisfiable. For the universal claim,
`A=5, O=6, N=19` satisfies the precondition and predicts 8; both Python
functions return 8 on `"5 apples and 6 oranges"`. Each ground claim is itself
a concrete satisfying state and was independently checked in stage 2.

### Program identity

Fresh depth-zero KAST output for parsed `solution.mpy` is byte-identical to
depth-zero KAST output for `solutionProgram`; both files hash to
`8a5bde8c642f5c081d240a211ec09b547ad4f78f068cd5910427df80e4aac463`.
Thus the macro executes the submitted function binding and body rather than a
different AST. See `evidence/04_pinning_and_body_sensitivity.log`.

A reviewer body mutation changed the executed second subscript from
`words[3]` to `words[0]`. The mutated definition compiled, but its proof failed
with the expected residual
`N -Int A -Int A #Equals N -Int A -Int O`. This establishes body sensitivity.
The preserved artifacts are `evidence/verification-body-mut.k` and
`evidence/spec-body-mut.k`.

### Fatal adequacy gap

Constructor identity does not make the symbolic input real. The universal
claim never supplies a `String`. `/candidate/semantic.k:72-74` overwrites the
parameter environment with:

```text
s |-> VFruits(A,O)
n |-> VInt(N)
```

`VFruits` is not a Python value or a translation of a string. Lines 91-92 then
make its `split` call return a five-element value with `A` and `O` already in
positions 0 and 3. There is no auxiliary claim that executes a real string,
extracts its counts, and reaches this representation. Indeed, the same
result-bearing `A` and `O` occur in this operational rule and in the
postcondition. That is the circular program-derived abstraction prohibited by
Gate A, not a trusted external primitive.

Consequently, the exact submitted body is executed, but on a substituted
input model that supplies the answer-bearing components by rule. Four finite
actual-string examples cannot repair this missing universal connection.

## 5. Rule-by-rule static soundness review

`evidence/04_rule_inventory.log` is the lexical inventory. There are no helper
K files beyond the three reviewed K files. There are no `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, priority rules, opaque
symbols, fresh variables, or proof-local lemmas.

### Syntax, attributes, and configuration

| Location | Inventory and judgment |
|---|---|
| `semantic.k:5-22` | `Program`, one-or-more `Stmts`, `FuncDef`, `Assign`, `Return`, two `Params`, and `Int`/`Name`/`Attribute`/0- or 1-argument `Call`/`Subscript`/`BinOp` expressions cover every constructor in `solution.mpy`. The `strict` and `seqstrict` attributes enforce the relevant Python left-to-right evaluation order. |
| `semantic.k:32-41` | `VInt`, `VStr`, `VWords`, `VSplit`, and `VBuiltinInt` are adequate small-step values for the used concrete path. `VFruits` and `VNum` have no Python counterparts and form the illegitimate abstract path. All `PyValue`s are declared `KResult`; this is adequate for the used strictness contexts. |
| `semantic.k:43-49` | `function`, `exec`, `setVar`, `finishCall`, `invokeFruit`, and `invokeString` are declared. `invokeFruit` is task-specific rather than language-level. |
| `semantic.k:51-56` | `<k>`, `<functions>`, and `<env>` model the used top-level subset. There is no stack, exception state, heap, or I/O. Those omissions are acceptable only for the exact terminating top-level path, not for the rules' broader apparent domains. |
| `verification.k:8,22-23` | The exact `solutionProgram` macro and `runFruit`/`runString` driver syntax are the only verification declarations. |

All `[symbol(...)]` declarations are constructor labels only. The only
`[function]` symbols are `spaceAt` and `nextSpace`; neither is declared total.
The sole `[macro]` is `solutionProgram`.

### Operational and functional rules

| Rule(s) | Decision |
|---|---|
| `semantic.k:58` | `Module(SS) => exec(SS)` faithfully begins module execution. |
| `semantic.k:60` | Splitting a nonempty statement sequence into `exec(S) ~> exec(SS)` preserves source order. |
| `semantic.k:61` | `exec(S) => S` faithfully exposes a single statement. |
| `semantic.k:63-64` | Function definition stores the exact parameter names and body under the exact function name. Sound on the submitted module. |
| `semantic.k:66` | Name assignment evaluates the RHS before `setVar`; correct for the only used assignment target. |
| `semantic.k:67-68` | `setVar` updates the environment with the computed value; correct. |
| `semantic.k:70` | `Return(E) => E` is adequate only because the submitted return is last and `finishCall` is immediately behind it. In a return followed by another statement it leaves a result in front of the residual statement rather than modeling abrupt return; this is an unmodeled-context gap, not a false conclusion used by this proof. |
| `semantic.k:72-74` | `invokeFruit` selects the named binding and executes its exact body, but replaces the real string argument with `VFruits(A,O)` while overwriting arbitrary prior environment state and admitting an arbitrary continuation. No theorem justifies that complete match domain. This is an illegitimate operational bridge and the universal claim depends on it. Ground witness: at `A=5,O=6,N=19` the rule yields 8 without selecting or parsing any string at all. |
| `semantic.k:76-78` | `invokeString` binds an actual `VStr(S)` and exact `VInt(N)`. It is adequate for the claims' empty, top-level context, but its wildcard environment overwrite is not a general Python call rule. |
| `semantic.k:80-82` | `finishCall` returns the value and clears both maps. This matches the empty top-level claims; it is overbroad for a caller context because no caller environment or function map is restored. |
| `semantic.k:84-85` | Environment lookup is correct when the key exists. |
| `semantic.k:86` | `Name("int") => VBuiltinInt` selects the needed builtin. It overlaps environment lookup if `int` is shadowed; the submitted environment never binds `int`, so the used path is deterministic, but the rule is not a general Python name-resolution model. |
| `semantic.k:87` | Integer literals become `VInt`; correct. |
| `semantic.k:89` | `Attribute(V,"split") => VSplit(V)` is false over its full `PyValue` domain. Concrete false-conclusion witness: `Attribute(VInt(1),"split")` becomes a callable split value, while Python raises `AttributeError`. The intended string case should have been guarded to `VStr`. |
| `semantic.k:91-92` | `VSplit(VFruits(A,O))` fabricates `VNum(A)` and `VNum(O)` in the exact positions read by the program. It is not an execution summary connected to `str.split`; it is the result-bearing correctness conclusion. `A=5,O=6` is the concrete witness to the bypass: a five-word result appears despite there being no source string. |
| `semantic.k:96` | `spaceAt(S,0)` delegates to the first-space search; sound when a first space exists. |
| `semantic.k:97-98` | The recursive nth-space scheme descends for `I>0`, but has no guard for a failed prior search or an out-of-range start. It is partial, as its declaration permits. |
| `semantic.k:100` | `nextSpace(S,START) => START + findString(S," ",START)` assumes `findString` returns a relative offset. The standard/LLVM hook returns an absolute index. Concrete witness: searching `"5 apples and 6 oranges"` from 2 returns 8, so this equation concludes 10 although the next space is at 8. `evidence/05_find_hook_witness.log` shows LLVM `8` and Haskell `6`, both with exit 0. The equation is therefore backend-dependent and false against the standard absolute-index hook; the Haskell proof happens to compensate for its backend's relative result. |
| `semantic.k:102-108` | The `VStr.split` rule does not implement Python `str.split`: it always makes five words, hardcodes words 1, 2, and 4, and uses the flawed space helpers for word 3. Concrete false-conclusion witness: on `"5  apples and 6 oranges"` it constructs word 3 as `"and"` while both Python executions split to a list whose word 3 is `"6"` and return 8. The K claim becomes bottom (`evidence/05_string_boundary_claim.log`). |
| `semantic.k:110` | Index 0 lookup from the modeled five-word value is correct. |
| `semantic.k:111` | Index 3 lookup from the modeled five-word value is correct. |
| `semantic.k:113` | `int(VInt(I)) = VInt(I)` is correct. |
| `semantic.k:114` | `int(VNum(I)) = VInt(I)` is internally consistent but applies only to the invented `VNum` path and carries the fabricated result into the return. |
| `semantic.k:115` | `int(VStr(S))` delegates to `String2Int`; adequate for the positive decimal substrings in the four examples, but it does not model the whole Python conversion/error domain. |
| `semantic.k:117` | Integer subtraction uses mathematical K integers and is correct for the submitted operation. |
| `verification.k:9-20` | Macro expansion is constructor-identical to trusted translation; sound and body-sensitive. |
| `verification.k:25-26` | `runFruit(P,A,O,N) => P ~> invokeFruit(A,O,N)` is a transparent driver expansion, but inherits the invalid `invokeFruit` abstraction. The target claim uses the expanded form directly. |
| `verification.k:28-29` | `runString(P,S,N) => P ~> invokeString(S,N)` is a transparent top-level driver expansion. |

There are five claims and no auxiliary claims. The universal claim is exact
and non-tautological under the supplied theory, but proves the synthetic
`VFruits` path. Each ground claim constrains an actual example result, but
none generalizes. No priority or simplification rule hides another execution
path.

Construct coverage for `solution.mpy` is complete syntactically: module and
function definition, two statements, assignment, return, name lookup,
zero-argument attribute call, subscripts, integer literals, one-argument
`int` calls, and two subtractions all have declarations and rules. The defect
is not a missing used constructor; it is the meaning assigned to string
splitting and to the universal synthetic input.

## 6. Fresh non-vacuity test

The reviewer-authored mutation `evidence/spec-vacuity-audit.k` changes the
universal destination from `N-A-O` to the demonstrably false `N-A-O+1`.
`A=5,O=6,N=19` satisfies the entry precondition; the real and original K
result is 8 while the mutation demands 9.

The exact command was:

```text
kprove spec-vacuity-audit.k \
  --definition audit-verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

The spec parsed and reached proof execution, then exited 1 with
`WarnStuckClaimState` and the expected failed equality:

```text
N -Int A -Int O #Equals N -Int A -Int O +Int 1
```

See `evidence/06_nonvacuity.log`. This is valid non-vacuity evidence: the
original theorem constrains its result. It does not validate the synthetic
input bridge.

## 7. Proven versus assumed accounting

What `#Top` precisely establishes is:

1. Under the candidate's K rules and the Haskell backend, for every constrained
   `A,O,N`, execution of the exact submitted body with `s=VFruits(A,O)`
   terminates at `VInt(N-A-O)` with empty maps.
2. Under the same rules/backend, the exact submitted body returns the stated
   result for four literal example strings.

It does **not** establish a universal reachability theorem for
`fruit_distribution(s,n)` on real strings.

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted translator plus constructor comparison | Program identity | Acceptable. Byte identity, KAST identity, and body sensitivity are independently evidenced. |
| K mathematical integers, maps, strictness machinery, `substrString`, `String2Int`, and arithmetic | All claims | Ordinary low-level trust boundary, acceptable when correctly used. |
| `findString` interpretation | All actual-string claims | Material problem. The direct LLVM/Haskell witness gives different values; the candidate equation relies on the Haskell-relative result and is false for the standard absolute-index behavior. |
| `VFruits`, `VNum`, `invokeFruit`, and the `VFruits.split` equation | Universal claim | Illegitimate. These are program-derived, result-bearing abstractions with no bridge-free universal connection theorem. They affect the returned value and postcondition directly. |
| `VStr.split` equation | Four ground string claims and any attempted real-string generalization | Illegitimate as a general Python bridge. The repeated-space satisfying witness produces a false modeled word and a failed reachability claim. |
| Exact-five-word format equivalence between submitted and canonical Python | Implementation intent | Only empirically supported on 513 cases. Seven broader canonical inputs diverge. No universal proof is supplied. |
| Prompt-to-fixed-position grammar | Adequacy | Informal and unsupported. The prose does not state the fixed positions or single-space restriction. |

Gate accounting:

- Gate A (real-program soundness): **FAIL**. The universal proof depends on an
  unconnected result-bearing synthetic input bridge, and the actual-string
  bridge has concrete false conclusions.
- Gate B (intent adequacy): **FAIL**. Only four actual strings are proved;
  finitely many examples and an invented `VFruits` domain do not cover the
  unrestricted source-contract string domain.
- Gate C (trust/evidence auditability): **FAIL** for the claimed universal
  bridge. The finite differential evidence is reproducible, but there is no
  required machine-checked connection theorem and the backend discrepancy is
  material.

The proof closes and is non-vacuous, but it is not a legitimate
partial-correctness proof of the real generated program over the material
HumanEval contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
