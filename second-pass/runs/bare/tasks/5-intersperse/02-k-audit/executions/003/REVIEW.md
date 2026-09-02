# Independent adversarial review: HumanEval/5 `intersperse`

The candidate has a real, non-vacuous K reachability proof under its submitted
abstract machine, and the claim executes the submitted constructor-level
function body. It is nevertheless not a legitimate proof of the real generated
Python program over the HumanEval contract domain. The claim and K semantics
cover every finite integer list, but the submitted recursive Python function
raises `RecursionError` on valid sufficiently long lists. The generated
semantics silently removes that observable exceptional behavior and instead
returns the claimed list. There is also an independently witnessed globally
false parameter-binding generalization in the generated entry rule.

## 1. Input and provenance integrity

The launcher declares:

- problem `5-intersperse`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- `mount_reference_semantics = false`.

The generated-semantics boundary is internally consistent:
`/reference/reference-semantics` is absent. I did not seek or use any hidden
reference semantics.

All records required for `legacy-selected-stage1` are present, readable,
regular files or real directories, and free of symlinks:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the complete `codex-trace/` tree;
- the present optional `/generation-evidence/usage.json`;
- the legacy side records `legacy-metrics.json` and `legacy-run-input.json`.

Historical `runtime-metrics.json` is not present and is not required for this
layout. The one JSONL trace contains 189 records and has zero JSON parse errors.
The generation report's `KPROVE_PASSED` marker, prior output, and trace were
treated only as untrusted claims.

The campaign object embedded in `/audit-input.json` is exactly equal as parsed
JSON to `/audit-campaign-lock.json`; the mounted lock SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. Direct SHA-256 checks also match every recorded
single-file hash for the run/task/result manifests, invocation and metrics,
generation prompt/output/last/usage, trusted prompt, translator, and canonical
implementation.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Their hashes are respectively
`388474ac...4012` and `406485ea...db16`, exactly as recorded. An independent
pipeline-format content-tree digest of `/candidate` is
`f33f116b...ab0`, matching all three legacy provenance assertions
`invocation.inputs.workspace_sha256`,
`invocation.outputs.workspace_sha256`, and
`generation-result.outputs.workspace_sha256`. The corresponding trace-tree
digest is `e7a5a5af...a588`, matching `usage.json`'s
`source_trace_sha256`. The additional audit-input tree-digest fields use a
different, undeclared digest encoding; I did not compare unlike encodings.
Per-file hashes and the legacy content-tree digests establish that the mounted
content is the retained generated content.

The immutable candidate contains all proof deliverables: `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
There are no candidate-provided kompiled definitions to reuse. All execution
below used copies under `/tmp/audit-work/5-intersperse-audit`.

Evidence:

- `/audit-output/evidence/01_mount_inventory.log`
- `/audit-output/evidence/02_generation_records.log`
- `/audit-output/evidence/03_trace_inventory.log`
- `/audit-output/evidence/04_integrity_checks.log`
- `/audit-output/evidence/25_tree_hashes.log`

Stage result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires:

> For a finite `List[int]` and an integer `delimeter`, return a list containing
> the same input elements in order with `delimeter` inserted between every two
> consecutive elements.

Thus empty and singleton lists are unchanged in value, a two-element list is
the branch boundary that first receives a delimiter, and there is no stated
length bound.

The trusted canonical implementation handles empty input separately, then
iteratively appends each non-final element and a delimiter before appending the
final element. The candidate instead uses:

```python
if len(numbers) <= 1:
    return numbers
return [numbers[0], delimeter] + intersperse(numbers[1:], delimeter)
```

This is extensionally correct while the recursion completes. Returning the
same object for length zero or one, instead of the canonical implementation's
new list, is not a violation of the value-level HumanEval contract.

### Trusted regeneration

I regenerated from the scratch copy with the trusted translator:

```text
python3 /tmp/audit-work/5-intersperse-audit/trusted/py2mpy.py \
  /tmp/audit-work/5-intersperse-audit/candidate/solution.py \
  > /tmp/audit-work/5-intersperse-audit/candidate/regenerated-solution.mpy
cmp -l regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`573abe2a7612d161ca044eb091d7aa5affb4cb2339b007c15f2763b11e4c214a`;
`cmp` exited 0. See `06_regeneration.log`.

### Independent differential testing

`differential_test.py` independently imports the trusted canonical and
candidate entry points. It tests:

- both documented examples;
- singleton and length-two branch boundaries;
- duplicates, negative values, zero delimiter, and arbitrary-size integers;
- all lists of lengths 0 through 6 over `{-1,0,2}`, for delimiters
  `{-3,0,5}`;
- 300 deterministic random lists of lengths 0 through 79;
- lengths around CPython's reported recursion limit.

On Python 3.10.12 with recursion limit 1000, 3,590 cases ran. There were three
mismatches:

| Input | Trusted canonical | Candidate |
|---|---|---|
| `list(range(1000)), -11` | returns 1,999 elements | raises `RecursionError` |
| `list(range(1001)), -11` | returns 2,001 elements | raises `RecursionError` |
| `list(range(1100)), -11` | returns 2,199 elements | raises `RecursionError` |

For length 1000 the canonical result has SHA-256
`ce47ff346835662d7d9d92c98355e0f0027aa8c354679bc81773d4a7cb7068a5`.
The script correctly exited 1 because of these mismatches. This is a material
restriction of the source-contract domain, not an example-only difference.

Evidence:

- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/07_differential.log`
- `/audit-output/evidence/05_candidate_sources.log`

Stage result: FAIL for fidelity over the unrestricted HumanEval domain.

## 3. Clean proof reconstruction

The observed toolchain is K 7.1.293 for `kompile`, `krun`, and `kprove`.
No candidate cache or compiled definition was copied. I built fresh named
definitions from the source copy.

### Concrete semantics

Command:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled-fresh
```

Exit status: 0. See `09_llvm_build.log`.

Fresh runner terms were mechanically wrapped around the regenerated
`solution.mpy`. Concrete `krun` results were:

| Input | K result | Exit |
|---|---|---|
| `[], 4` | `[]` | 0 |
| `[-7], 9` | `[-7]` | 0 |
| `[-7,5], -3` | `[-7,-3,5]` | 0 |
| `[1,2,3], 4` | `[1,4,2,4,3]` | 0 |

All agree with both Python implementations on those inputs.

The decisive length-1000 run also terminates in K. For
`list(range(1000)), -11`, K returns 1,999 elements, first
`[0,-11,1,-11,2,-11]`, last
`[-11,997,-11,998,-11,999]`, with result SHA-256
`ce47ff346835662d7d9d92c98355e0f0027aa8c354679bc81773d4a7cb7068a5`.
That is exactly the canonical value, while the submitted Python function
raises `RecursionError`. This directly witnesses the semantics-to-real-program
gap.

Evidence:

- `/audit-output/evidence/make_k_run.py`
- `/audit-output/evidence/summarize_krun.py`
- `/audit-output/evidence/10_concrete_inputs.log`
- `/audit-output/evidence/11_krun_small.log`
- `/audit-output/evidence/12b_krun_long.log`

`12_krun_long.log` preserves an earlier reviewer summarizer regex error. It is
not used as semantic evidence; the corrected rerun is `12b_krun_long.log`.

### Symbolic proof

Command:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-fresh
```

Exit status: 0. See `13_haskell_build.log`.

There is one positive target claim. I ran all of `SPEC`:

```text
kprove spec.k --definition verification-kompiled-fresh \
  --spec-module SPEC
```

It printed exactly `#Top` and exited 0. See `14_positive_kprove.log`.

Stage result: PASS for reconstruction under the candidate theory. This success
does not validate that theory as Python semantics.

## 4. Adequacy and real-program pinning

### Plain-language claim

The entry claim has no explicit `requires` clause. Sort inference therefore
gives this precondition:

- `IS` is any finite K `Ints` sequence;
- `D` is any mathematical K integer;
- `KONT` is any K continuation;
- `<k>` begins with an `Invoke` of the displayed function binding and body,
  followed by `KONT`.

Its postcondition is exact, not existential or implicational: the computation
must reach `VList([intersperseSpec(IS,D)]) ~> KONT`. The result variable is not
free. `intersperseSpec` recursively retains each input integer and inserts `D`
between adjacent elements.

### Constructor identity and control-flow match

The claim contains the complete `Module`, typing import, `FuncDef`, parameter
names, `If`, both `Return` nodes, list literal, index, tail slice, concatenation,
and recursive call. A mechanical constructor-token comparison finds one exact
contiguous occurrence after normalizing only `.Stmts`, the explicit K spelling
of the empty `Stmts` list that the trusted translator renders as whitespace.
See `compare_claim_program.py` and `15c_claim_program_identity.log`.
`15_claim_program_identity.log` and `15b_claim_program_identity.log` preserve
two superseded reviewer-tokenizer attempts and are not mismatch evidence.

There are no separate helper or loop claims. The entry claim itself supplies
the recursive circularity. Generalizing over `KONT` is faithful and necessary:
the recursive `Invoke` occurs below the pending concatenation continuation, and
that continuation is preserved on both sides.

The typing import is pattern-matched but not executed. For this exact standard
library, typing-only import and the value-level function contract, treating it
as inert is an acceptable explicit abstraction. The entry rule does execute
the exact displayed body rather than replacing it with `intersperseSpec`.

### Satisfiable ground witness

`IS = [1,2,3]`, `D = 4`, and `KONT = .K` satisfies the unconstrained
precondition. Substitution reduces the demanded result to `[1,4,2,4,3]`.
The canonical Python, candidate Python, and concrete K run all return that
value. See `16_ground_witness.log` and `11_krun_small.log`.

### Body sensitivity

The reviewer body mutation changes the term actually executed by the claim:
the body inserts `Int(99)` instead of `Name("delimeter")`, while the
postcondition remains `intersperseSpec(IS,D)`. It parses successfully with
`--dry-run` (exit 0), then `kprove` exits 1 with a meaningful
`WarnStuckClaimState` residual containing `#Not { D #Equals 99 }`.
Thus the successful target proof is sensitive to the body, not merely to an
external `solution.py` file.

Evidence:

- `/audit-output/evidence/spec-body-mutation.k`
- `/audit-output/evidence/17_body_mutation_dry_run.log`
- `/audit-output/evidence/18_body_mutation_kprove.log`

Stage result: PASS for constructor pinning, local control flow, satisfiability,
and result constraint. Intent adequacy nevertheless fails because the formal
machine omits the real recursion exception for inputs admitted by this same
precondition.

## 5. Rule-by-rule static soundness review

There are no generated helper K files beyond `semantic.k`. The immutable proof
sources are `semantic.k`, `verification.k`, and `spec.k`; reviewer mutation
files copied to scratch are not candidate extensions.

### Complete local declaration inventory

`MPY-SYNTAX` declares:

1. `Pgm ::= Module(Stmts)`;
2. `Stmts ::= List{Stmt,""}`;
3. `Strings ::= List{String,","}`;
4. `Params ::= Params(Strings)`;
5. `Stmt ::= ImportFrom | FuncDef | If | Return`;
6. `Exprs ::= List{Expr,","}`;
7. `Expr ::= Name | Int | Call | Compare | BinOp | ListExpr | Subscript`;
8. `CmpOp ::= CmpOp(String,Expr)`;
9. `Bound ::= Expr | NoBound`;
10. `Index ::= Expr | Slice(Bound,Bound,Bound)`;
11. `Ints ::= List{Int,","}`;
12. `Val ::= VInt | VBool | VList`;
13. `Vals ::= List{Val,","}`;
14. `Run ::= Invoke(Pgm,String,Vals)`.

`MPY` declares the single `<k>` configuration, `Env ::= env(Ints,Int)`, and
these eleven continuation/internal constructors:
`exec`, `eval`, `decide`, `listSecond`, `makePair`, `binopRight`,
`concatWith`, `concat`, `prepend`, `callSecond`, and `callWith`.

`VERIFICATION` adds exactly one symbol:
`intersperseSpec(Ints,Int) [function,total]`.

There are no local opaque symbols, priority rules, `functional` declarations,
`simplification` rules, `concrete`, `anywhere`, or `owise` rules. The only
claim is the entry claim in `SPEC`.

### Construct-to-rule coverage

Every material constructor in regenerated `solution.mpy` is covered:

| Source construct | Declaration/rules |
|---|---|
| module/import/function binding/parameters | `Module`, `ImportFrom`, `FuncDef`, `Params`; entry `Invoke` rule at `semantic.k:63` |
| call arguments and recursive call | `Call`, `callSecond`, `callWith`; rules at lines 127, 129, 131 |
| `if` and `return` | `If`, `Return`, `exec`, `decide`; lines 74–81 |
| `len(numbers) <= 1` | `Compare`, `Call`, `CmpOp`; the three structural rules at lines 90, 94, 98 |
| variable and integer evaluation | `Name`, `Int`; lines 83–85 |
| `numbers[0]` and `numbers[1:]` | `Subscript`, `Slice`, `NoBound`; lines 103–109 |
| two-element list literal | `ListExpr`, `listSecond`, `makePair`; lines 111–115 |
| list `+` | `BinOp`, `binopRight`, `concatWith`, `concat`, `prepend`; lines 117–125 |

Unmodeled shapes of the larger declared grammar stop visibly. Missing behavior
for unused shapes is acceptable in `GENERATED_SEMANTICS`.

### Exhaustive ordinary-rule decisions

| Rule(s) | Decision |
|---|---|
| `semantic.k:63–72`, `Invoke` entry | On the exact submitted module it selects the displayed function name/body, preserves the continuation, and creates the values used by the body. On its complete match domain it is **unsound** because it ignores `PARAMS` and always creates bindings named `numbers` and `delimeter`. Concrete false-conclusion witness below. |
| line 74, `exec(Return(E) REST,...)` | Sound: Python return evaluates `E` and abandons the remaining function statements. |
| lines 75–77, `exec(If...)` | Sound left-to-right condition setup for the submitted control form. |
| lines 78–79, true `decide` | Sound on every branch that can complete in this minimal semantics: it executes the chosen branch, and a completing modeled branch returns. It is incomplete, rather than result-fabricating, for branch bodies that finish normally. |
| lines 80–81, false `decide` with empty else | Sound for the exact submitted empty `else`; nonempty else is deliberately unmatched. |
| line 83, `Name("numbers")` | Sound for the submitted environment, but participates in the false parameter-binding generalization of the entry rule. |
| line 84, `Name("delimeter")` | Same assessment as line 83. |
| line 85, integer literal | Sound mathematical-integer value rule. |
| lines 90–93, empty-list `len <= 1` | Sound; yields true. |
| lines 94–97, singleton `len <= 1` | Sound; yields true. |
| lines 98–101, length-at-least-two `len <= 1` | Sound; yields false. The three list patterns are disjoint and exhaustive for finite `Ints`. |
| lines 103–105, index zero | Sound for nonempty integer lists. Empty input is unmatched, and the submitted guard prevents use there. |
| lines 106–109, slice from one | Sound tail operation for nonempty integer lists. |
| lines 111–112, list-literal first expression | Sound left-to-right evaluation. |
| lines 113–114, list-literal second expression | Sound continuation and order. |
| line 115, pair construction | Sound for the two integer expressions used by the program. |
| lines 117–118, binary `+` first operand | Sound left-to-right evaluation. |
| lines 119–120, binary `+` second operand | Sound continuation and order. |
| line 121, enter `concat` | Sound for the list operands produced by this body. Other value combinations visibly stick. |
| line 122, empty-left concatenation | Sound identity equation. |
| lines 123–124, nonempty-left concatenation | Sound structural recursion, decreasing the left list by one. |
| line 125, `prepend` | Soundly reconstructs list order. |
| lines 127–128, recursive-call first argument | Sound left-to-right evaluation for the exact function name. |
| lines 129–130, recursive-call second argument | Sound continuation and order. |
| lines 131–132, recursive `Invoke` | Sound binding for the exact single submitted function, preserving the active concatenation continuation. |

The `intersperseSpec` equations are also individually sound:

| Equation | Decision |
|---|---|
| empty list maps to empty | true |
| singleton maps to itself | true |
| `I,J,REST` maps to `I,D,intersperseSpec(J,REST,D)` | true recursive definition of interspersing |

Their patterns are disjoint and exhaustive over finite `Ints`; recursion
strictly decreases input length. `[function,total]` is therefore justified.
This symbol is a definitional summary used only in the destination. It never
rewrites or bypasses program execution, so it is not a result-bearing oracle or
an operational bridge.

### False-conclusion witnesses

#### Material real-program witness: recursion/exception behavior

The entry precondition admits
`IS = [0,1,...,999]`, `D = -11`, `KONT = .K`.
The generated K semantics returns the exact 1,999-element canonical list
(`12b_krun_long.log`), and the universal `#Top` claim asserts that normal
destination. The real submitted Python function instead terminates
exceptionally with `RecursionError` (`07_differential.log`). Therefore the
generated semantics enables a false normal-return conclusion about the exact
submitted program on its intended input domain.

This is not a merely absent unused construct. It is allocation/control behavior
of the recursive call used by the program, affects the observable outcome, and
is included in the theorem's unrestricted formal precondition.

#### Global parameter-binding witness

The `Invoke` rule matches this term:

```text
Invoke(
  Module(
    ImportFrom("typing", "List")
    FuncDef("f", Params("x", "y"), Return(Name("numbers")))),
  "f", VList([1]), VInt(2))
```

The rule ignores `Params("x","y")`, installs the hard-coded `numbers` binding,
and K returns `[1]`. The equivalent Python function
`def f(x,y): return numbers` raises `NameError`. Both executions and statuses
are preserved in `20_parameter_binding_false_witness.log`; the exact K witness
is `unsound-params-witness.mpy`. This proves the rule false on its declared
match domain. The exact submitted program happens to use the expected names,
but the rule remains an unsound generated-language semantic generalization.

Evidence:

- `/audit-output/evidence/19_static_inventory.log`
- `/audit-output/evidence/20_parameter_binding_false_witness.log`
- `/audit-output/evidence/unsound-params-witness.mpy`
- `/audit-output/evidence/semantic_false_witness.py`

Stage result: FAIL. The recursion witness is material to the target claim; the
parameter-binding witness is an additional global semantic soundness failure.

## 6. Fresh non-vacuity test

I did not rely on a candidate vacuity artifact; none was submitted.

The accepted reviewer mutation preserves the exact executed program and changes
only the destination from `intersperseSpec(IS,D)` to
`intersperseSpec(IS,D +Int 1)`. It is demonstrably false for the satisfying
input `IS = [1,2]`, `D = 4`, `KONT = .K`: the real and modeled program return
`[1,4,2]`, while the mutated destination requires `[1,5,2]`.

The mutation built successfully:

```text
kprove spec-vacuity.k --definition verification-kompiled-fresh \
  --spec-module SPEC-VACUITY --dry-run
```

Exit status: 0 (`23_vacuity2_dry_run.log`).

The actual mutated proof:

```text
kprove spec-vacuity.k --definition verification-kompiled-fresh \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. The residual contains the expected unmet
condition `#Not { D #Equals D +Int 1 }` and a list prefix with actual delimiter
`D` versus mutated summary delimiter `D +Int 1`. This is a meaningful
result-obligation failure, not a parse/build/timeout failure.

`spec-vacuity-attempt1.k` and logs `21_vacuity_dry_run.log` /
`22_vacuity_kprove.log` preserve a rejected first mutation. Although it parsed,
it stopped on an unrelated backend `DecidePredicateUnknown`; it is explicitly
not counted as non-vacuity evidence.

Evidence:

- `/audit-output/evidence/spec-vacuity.k`
- `/audit-output/evidence/23_vacuity2_dry_run.log`
- `/audit-output/evidence/24_vacuity2_kprove.log`
- `/audit-output/evidence/spec-vacuity-attempt1.k`

Stage result: PASS. The proof is result-constraining and discriminating under
the submitted theory.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the rules in `semantic.k` and the mathematical K built-ins, for every
finite K integer sequence `IS`, integer `D`, and continuation `KONT`, executing
the exact constructor-level submitted function through `Invoke` reaches:

```text
VList([intersperseSpec(IS,D)]) ~> KONT
```

The recursion is executed through the ordinary semantic rules. The
postcondition summary is not injected into execution. The successful proof is
body-sensitive and non-vacuous.

It does **not** establish that the real CPython execution returns that value for
every valid `List[int]`. In particular, it does not establish the contract for
the length-1000 witness.

### Trust ledger

| Boundary | Dependents/effect | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell/LLVM backends, reachability engine | all build, concrete, and proof results | Standard low-level trusted tool boundary; acceptable. |
| K built-in mathematical `Int`, `Bool`, and algebraic finite lists | values, guards, helper equations | Appropriate for Python arbitrary-precision integers and finite value lists; acceptable for the value-level contract. |
| Ignoring the typing-only `from typing import List` during invocation | module initialization/state | Acceptable for this pure return-value theorem, conditional on the standard typing import succeeding and its external side effects being out of scope. |
| Structural rules for `len <= 1`, index zero, slice from one, and list concatenation | branch, recursive arguments, final value | Truthful equations on the exact integer-list shapes; supported by branch/boundary concrete runs. Acceptable. |
| Direct lookup of the sole displayed `intersperse` binding | recursive control and return | Locally justified by the exact pinned module, which contains one function and no rebinding. Acceptable for this term. |
| Hard-coded `numbers`/`delimeter` bindings despite arbitrary `PARAMS` | name lookup and return | Illegitimate globally; concrete `NameError` witness shows the entry rule false on its match domain. |
| Unlimited recursive K rewriting with no CPython recursion resource or exception | control, exception, final result | Illegitimate for the unrestricted real-program theorem. It directly changes a valid length-1000 execution from `RecursionError` to the claimed list. |
| `intersperseSpec` equations | postcondition only | Total, disjoint, descending definitional summary; acceptable and not circular with execution. |
| Python differential and concrete K tests | empirical source/semantics bridge | Reproducible finite evidence only. They do not replace the K proof; here they expose a counterexample to the claimed bridge. |

### Gate accounting and decision

- Reconstruction and `#Top`: PASS.
- Program-term pinning, local body sensitivity, result constraint: PASS.
- Fresh non-vacuity: PASS.
- Real-program soundness: FAIL because a satisfying intended input has an
  exceptional real outcome but a claimed normal K result.
- Source-contract/domain adequacy: FAIL because the recursive implementation
  materially narrows the unbounded `List[int]` contract domain.
- Generated-semantics global rule validity: FAIL because the parameter-binding
  rule has a concrete false-conclusion witness.
- Evidence auditability: PASS; exact scripts, inputs, commands, exits, and
  bounded outputs are under `/audit-output/evidence/`.

The benchmark mapping is decisive: even if the locally sound, unlimited-stack
abstract-machine theorem were described as `SOUND-BUT-LIMITED`, materially
narrowing the HumanEval source-contract domain is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
