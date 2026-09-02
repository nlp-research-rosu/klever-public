# Independent adversarial audit: 17-parse-music

The candidate is **not** a legitimate proof of the requested HumanEval
contract. Fresh reconstruction does confirm that all 11 submitted reachability
claims close under the submitted generated semantics, that the claims execute
the submitted constructor program, and that the fixed result claims are
non-vacuous. Those facts do not establish the required theorem.

There are two independent fatal adequacy defects:

1. The submitted Python program is not extensionally equal to the trusted
   canonical program on the source-contract domain. In particular,
   `parse_music("")` returns `[1]` instead of `[]`, and leading, trailing, or
   repeated separators add spurious quarter notes.
2. `spec.k` has result-bearing entry claims for only four fixed strings. Its
   symbolic loop claims prove isolated one-step transitions, and its three
   symbolic source claims stop before the loop with `<result> noResult`. There
   is no entry claim whose postcondition characterizes the returned list for an
   arbitrary finite music string.

The benchmark decision rule explicitly maps this materially narrowed
HumanEval domain to `FAIL / NOT_LEGIT`, even though the limited claims
themselves are sound.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`.

I read and parsed:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`,
  `legacy-metrics.json`, and `legacy-run-input.json`;
- all 234 JSONL records in the structured trace at
  `/generation-evidence/codex-trace/2026/07/22/`;
- all submitted files in `/candidate`.

`runtime-metrics.json` is absent, which is permitted for the declared legacy
layout. `usage.json` is present and was inspected. The untrusted generation
record claims `KPROVE_PASSED`; that claim was not used as proof evidence.

The campaign-lock JSON object is structurally identical to the
`audit_campaign` block. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`.

Every required mount and record is a readable regular file or real directory.
No required candidate or generation-evidence entry is a symlink. All
launcher-recorded leaf hashes match. The independently recomputed pipeline tree
digests are:

- candidate workspace:
  `503241fc3afda05fc2a2b9a7fa83373d0b67fde6d393fbee24d789c5887e7b54`,
  matching both the stage result and invocation;
- trace tree:
  `0cbfdd68b578853ce843658211327e747de70ef8654c3c0b3604fafc313ea960`,
  matching `usage.json`; the sole trace file also matches its recorded
  `62b15485...` hash.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. `/reference/reference-semantics` is absent, as required for
`GENERATED_SEMANTICS`; no hidden or inferred reference semantics was used.

The complete reproducible integrity check and output are
`evidence/01_provenance.py` and `evidence/01_provenance.log`. There is no audit
infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt specifies a string of musical notes in the ASCII notation
`o`, `o|`, and `.|`, returning respectively 4, 2, and 1 beat for each note.
The trusted canonical implementation splits on the literal space and filters
empty fields:

```python
note_map = {'o': 4, 'o|': 2, '.|': 1}
return [note_map[x] for x in music_string.split(' ') if x]
```

There is no nonempty-input or exactly-one-separator precondition in the prompt.
The canonical `if x` gives empty strings and extra separators a definite
meaning: empty fields are ignored.

The submission instead executes:

```python
for note in music_string.split(" "):
    if note == "o":
        ...
    elif note == "o|":
        ...
    else:
        beats = beats + [1]
```

Thus the `else` branch treats both `".|"` and every empty field as a quarter
note. Concrete false witnesses include:

| Input | Trusted canonical | Submitted program |
|---|---:|---:|
| `""` | `[]` | `[1]` |
| `" "` | `[]` | `[1, 1]` |
| `"o "` | `[4]` | `[4, 1]` |
| `"o  o|"` | `[4, 2]` | `[4, 1, 2]` |
| `" o| .| "` | `[2, 1]` | `[1, 2, 1, 1]` |

### Trusted translation

In fresh scratch, the exact command

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp regenerated-solution.mpy solution.mpy` also exited 0; both
files hash to
`1fb428ec561d73756e95f130d99b6985c7157011cdf2b75d0798c6dfb78e7eec`.
See `evidence/02_translation.log`.

### Independent differential test

`evidence/02_differential.py` imports the trusted canonical and submitted entry
points independently. It covers the documented example, all three branch
tokens, empty and whitespace-only strings, leading/trailing/repeated
separators, and every sequence of one through four valid notes under several
separator layouts.

The command exited 1 because it found 361 mismatches among 482 inputs. The exit
is the test's intentional mismatch signal, not an infrastructure failure. The
full bounded input scope and results are in
`evidence/02_differential.log`.

This is a material implementation-versus-contract failure, not merely a thin
evidence limitation.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`; no
candidate-built definition or cache was copied or reused. K v7.1.293 was
available independently.

### Generated semantics

The fresh LLVM build command was:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-PROGRAM-PARSING \
  --output-definition audit-semantic-kompiled
```

It exited 0 (`evidence/03_kompile_llvm.log`). Fresh `krun` executions covered
the documented example, each branch, empty input, whitespace-only input,
repeated separators, and leading/trailing separators. K agreed with the
submitted Python on every checked input, including its incorrect boundary
behavior. For example:

```text
input=''       K=[1]       submitted_python=[1]       canonical_python=[]
input='o  o|'  K=[4,1,2]   submitted_python=[4,1,2]   canonical_python=[4,2]
```

See `evidence/03_concrete_compare.py` and
`evidence/03_concrete_compare.log`. An initial reviewer regex error is
preserved separately in `evidence/03_concrete_compare_attempt1.log`; it did not
affect the corrected execution.

### Proof definition and positive claims

The fresh Haskell build command was:

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-PROGRAM-PARSING \
  --output-definition audit-verification-kompiled
```

It exited 0 (`evidence/03_kompile_haskell.log`). The candidate's aggregate
target command

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`
(`evidence/03_kprove_all.log`).

For independent per-claim confirmation, I made a semantically identical copy
of the spec with labels only (`evidence/03_spec-labeled.k`). Each of its 11
claims was then selected and run separately. Every run exited 0 and printed
`#Top`; commands and outputs are in `evidence/03_run_each_claim.sh` and
`evidence/03_kprove_each.log`.

Clean reconstruction therefore passes. This establishes closure of the
submitted claims under the submitted theory, not adequacy of those claims.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory and satisfiable witnesses

None of the 11 claims has a `requires` clause. Their cell patterns are their
preconditions.

| Claim | Precondition | Postcondition | Satisfying ground witness |
|---:|---|---|---|
| 1 | Exact program, empty state, input `"o"` | Terminates with result/env `[4]` and the exact function binding | The displayed empty initial maps and `noResult` |
| 2 | Exact program, empty state, documented 11-note input | Terminates with the documented 11 integers and exact final state | The displayed empty initial maps and `noResult` |
| 3 | Exact program, empty state, input `"o|"` | Terminates with result/env `[2]` | The displayed empty initial maps and `noResult` |
| 4 | Exact program, empty state, input `".|"` | Terminates with result/env `[1]` | The displayed empty initial maps and `noResult` |
| 5 | Loop head is `"o"`; arbitrary `PREFIX, REST`; env contains only `beats=PREFIX` | Consumes that iteration, appends 4, binds `note`, leaves loop on `REST` | `PREFIX=.List`, `REST=.List` |
| 6 | Same, with head `"o|"` | Appends 2 and leaves loop on `REST` | `PREFIX=.List`, `REST=.List` |
| 7 | Same, with head `".|"` | Appends 1 and leaves loop on `REST` | `PREFIX=.List`, `REST=.List` |
| 8 | Empty loop followed by final return; arbitrary `PREFIX` | Terminates and returns exactly `PREFIX` | `PREFIX=.List` |
| 9 | Exact program, empty state, input `"o" + " " + T` | Reaches an unexecuted loop over `"o"` plus `splitWords(T)`, with empty beats and `noResult` | `T=""` |
| 10 | Same, with `"o|"` prefix | Reaches the corresponding unexecuted loop; no result | `T=""` |
| 11 | Same, with `".|"` prefix | Reaches the corresponding unexecuted loop; no result | `T=""` |

For the four result-bearing entry claims, concrete substitution gives the same
values in both Python implementations: `[4]`, the documented list, `[2]`, and
`[1]`. Those fixed claims are honest.

Claims 5-8 are standalone local transitions. Claims 9-11 are also standalone
target claims, not a final-result theorem: their destination deliberately
contains the loop and `Return` continuation and keeps `<result> noResult`.
There is no twelfth claim connecting an arbitrary entry state through repeated
loop steps to a mapped return list. Proving each component separately does not
state, let alone prove, the missing universally quantified entry
postcondition.

### Program identity

The proof-side `theProgram`, `parserFunctionBody`, and `parserBranch` functions
expand to the same constructors as trusted regeneration. The only
normalization is the K list-production spelling `ListExpr(.Exprs)` for
translator text `ListExpr()`.

`evidence/04_program-identity-spec.k` places `theProgram` against the complete
trusted-regenerated constructor term. It builds and proves with `#Top`
(`evidence/04_program_identity.log`). The preserved first attempt
(`evidence/04_program_identity_attempt1.log`) documents the required
surface-syntax normalization.

A body-sensitivity test changed the whole-note `Int(4)` to `Int(5)` inside the
actual `theProgram` expansion, rebuilt a distinct Haskell definition, and
reran the `"o"` entry claim. The definition built successfully, but the proof
exited 1 with a genuine stuck state showing both `beats` and `result` equal to
`[5]`, not `[4]`. See:

- `evidence/04_body-mutation-verification.k`;
- `evidence/04_body_mutation_build.log`;
- `evidence/04_body_mutation_proof.log`.

The claims therefore pin and depend on the submitted program term. The fatal
problem is theorem and source-contract adequacy, not program substitution.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule inventory is
`evidence/05_rule_inventory.md`; the source scan is
`evidence/05_static_scan.log`. It enumerates all 15 local syntax declarations,
all 36 semantic rules, all three proof-local equations, all 11 claims, and all
attributes.

### Syntax and used-construct coverage

The submitted constructor program uses `Module`, `ImportFrom`, `FuncDef`,
`Params`, multi-statement sequencing, `Assign`, `For`, `If`, `Return`, `Name`,
`Str`, `Int`, `ListExpr`, `Attribute`, `Call`, `Compare`, `CmpOp`, and `BinOp`.
Every one is declared and has an applicable operational path:

| Operation group | Semantic rules |
|---|---|
| module loading and statement order | 73-78 |
| function lookup, binding, and entry | 80-82 |
| assignment and return | 85-91 |
| conditional control | 93-95 |
| list iteration and loop-variable binding | 97-103 |
| literals, lookup, and used list literals | 106-111 |
| explicit-separator string splitting | 115-138 |
| string comparison | 141-146 |
| list concatenation | 148-152 |

The configuration has `<k>`, `<functions>`, `<env>`, and `<result>`. The
program requires no heap, external state, output, exception cell, or allocation
identity. Evaluation order is explicit: receiver before method argument, left
before right for equality and concatenation, iterable before loop setup, guard
before branch, and expression before assignment/return. The loop binds the head
before its body and recurs only after the body.

The semantics is intentionally not full Python. For example, `invoke` has no
general call stack and `finishReturn` would not discard an arbitrary trailing
continuation. The exact submitted program has one top-level call and its
`Return` is final. I found no satisfying intended-input state of the submitted
program on which either limitation enables a false conclusion. Under the
benchmark's witness requirement, these are scope limitations, not asserted
unsound rules.

### Functions, simplifications, overlap, and totality

`splitWords : String -> List` is the sole semantic helper marked `[function]`;
it is not declared `[total]`. Its five equations implement CPython's
explicit-separator `str.split(" ")`, preserving empty fields:

- three specialized, truthful prefix simplifications for `"o "`, `"o| "`,
  and `".| "`;
- a no-separator base case guarded by `findString == -1`;
- a first-separator recursive case guarded by `findString >= 0`.

The general guards are disjoint and cover K strings. Recursive calls strictly
shorten the suffix. Each specialized equation overlaps the general recursive
case, but its right-hand side is exactly the corresponding instance of that
case; the specialized prefixes are pairwise disjoint.

`parserBranch`, `parserFunctionBody`, and `theProgram` are nullary
`[function,total]` declarations. Each has one unguarded equation, so coverage is
complete and there is no overlap. They name exact constructor fragments and do
not replace program execution with a result summary.

There are no local `functional` declarations, opaque symbols, priority rules,
proof-local operational bridges, result oracles, or answer-encoding
simplifications. The three `[simplification]` rules are only the truthful
`splitWords` prefix equations.

### Rule soundness conclusion

For the exact submitted program and its intended valid-token inputs, the
generated semantics faithfully executes every material operation. Fresh K
execution agrees with submitted Python even on the inputs where the submitted
program disagrees with the canonical implementation.

I do **not** label any local K rule unsound: no required false-conclusion
witness exists for a semantic rule on the submitted program's intended input
domain. The concrete `"" -> [1]` witness instead exposes a defect in the
submitted source algorithm, which the K semantics models faithfully. Likewise,
the absence of a universal postcondition is a spec adequacy defect, not a
semantic inconsistency.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`. I created
`evidence/06_spec-vacuity.k` in scratch from the independently labeled spec and
changed only the `"o"` entry result from `[4]` to `[5]`, leaving the true final
environment requirement `beats=[4]`. The initial state is satisfiable:
`functions=.Map`, `env=.Map`, and `result=noResult` with input `"o"`.

The dry-run command parsed and built the mutation successfully and exited 0:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims 'SPEC-VACUITY.label(entry-o)' --dry-run
```

See `evidence/06_vacuity_build.log`.

The real proof command exited 1 with `WarnStuckClaimState`. Its residual is the
fully terminated real execution with `beats=[4]` and `result=[4]`, which cannot
unify with the mutated `[5]` destination. See
`evidence/06_vacuity_proof.log`.

This is meaningful non-vacuity evidence for the fixed `"o"` claim. Together
with the independent body-sensitivity failure, it shows that the fixed entry
claims constrain execution and result. It cannot supply the missing
unrestricted theorem.

## 7. Proven versus assumed accounting

### What the successful K proof actually establishes

Conditional on the submitted generated semantics and imported K builtins, the
successful proof establishes exactly:

1. the exact submitted constructor program returns the specified final states
   for `"o"`, `"o|"`, `".|"`, and the documented 11-note example;
2. a loop state with one known legal head token appends the corresponding
   integer and advances by one element, for arbitrary K-list prefix and rest;
3. an empty loop followed by the submitted final return returns the current
   prefix;
4. an invocation whose string syntactically begins with one legal note plus a
   space reaches a corresponding unexecuted loop state for arbitrary suffix
   `T`.

It does not establish:

- a returned-value postcondition for an arbitrary music string;
- induction from arbitrary source strings through every loop iteration;
- equivalence to the trusted canonical implementation;
- filtering of empty split fields;
- correctness for empty, leading-space, trailing-space, or repeated-space
  inputs;
- termination for an unrestricted input domain.

### Trust ledger

| Boundary | Influence | Dependents | Assessment |
|---|---|---|---|
| K v7.1.293 parser, compiler, Haskell prover, LLVM runner | All parsing, execution, and closure | Every claim | Standard low-level trusted toolchain; exact versions and fresh commands recorded |
| Imported `INT`, `STRING`, `BOOL`, `MAP`, `LIST`, and `PROGRAM-LISTS` modules | Values, guards, maps, list and string operations | All concrete and symbolic execution | Standard K builtin trust boundary |
| `findString`, `substrString`, `lengthString`, `==String`, string concatenation | Split behavior and branches | Claims involving input processing | Equations were statically audited; finite concrete checks support but do not universally prove the CPython bridge |
| Erasure of `ImportFrom("typing","List")` | Module loading only | Every program-entry claim | Acceptable: this import is typing-only for the submitted program |
| Generated semantics' restricted call/return/list model | Control, local state, result | Every claim | Adequate for the exact submitted body; not a claim about full Python |
| Trusted `py2mpy.py` | Program identity | Every entry claim | Byte regeneration passed; proof-side constructor identity also passed |
| Trusted `canonical.py` as source-contract oracle | Adequacy comparison | HumanEval correctness judgment | Launcher-designated trusted input; independent differential script does not share implementation logic with the candidate |

There are no opaque values, unconstrained result symbols, empirical oracles
inside the K theory, or proof-local rules that bypass the function body.
Differential testing is used only as finite evidence for program/semantics
bridges, never as a substitute for the reachability proof.

### Gate accounting and decision

- Clean dynamic reconstruction: **PASS**. Every submitted positive claim
  independently closes with exit 0 and `#Top`.
- Gate A, soundness and non-vacuity of the theorem actually stated: **PASS**.
  The limited claims execute the real constructor body, are result-constraining
  where they claim a result, and use no unsound proof extension.
- Gate B, source intent and domain adequacy: **FAIL**. The implementation
  materially disagrees with the canonical contract, and the formal result
  claims cover only four fixed strings. The symbolic component claims never
  state a universal entry result.
- Gate C, trust/evidence auditability of the limited theorem: **PASS with a
  finite-evidence boundary**. Commands, versions, assumptions, and finite
  differential scope are explicit; the CPython/K bridge is supported by rule
  review and concrete tests rather than a universal cross-language theorem.

Generic Kit terminology would call a sound but materially restricted theorem
`SOUND-BUT-LIMITED`. The controlling benchmark prompt expressly maps material
narrowing of the unrestricted HumanEval source-contract domain to
`FAIL / NOT_LEGIT`. The independent source mismatch is an additional fatal
reason for the same result.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
