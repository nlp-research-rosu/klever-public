# Independent adversarial review: 67-fruit-distribution

## Executive conclusion

The candidate's source-only proof reconstruction does print `#Top`, the
postcondition is non-vacuous, and the K term executed by the claims is
mechanically identical to the regenerated `solution.mpy`. Those facts are not
enough to make this a proof of the HumanEval program over real input strings.

The general claim ranges over a fresh synthetic value
`str(fruitSentenceCodes(A,B))`. Neither `fruitSentenceCodes` nor
`decimalCodes` has an equation connecting it to the actual ASCII code
sequence of a sentence or decimal numeral. Two proof-local rules then
fabricate the five split tokens and decode `decimalCodes(I)` directly to `I`.
There is no bridge-free universal connection theorem. Removing those rules
leaves even the ground witness `A=5, B=6, N=19` stuck in the fixed semantics.
Conversely, equally well-formed opposite interpretations prove `#Top` for
false source-level results 6 and 7, whereas both Python implementations return
8. The four literal example claims are honest but finite.

This is therefore not a legitimate general partial-correctness proof of the
real generated program. It is a proof about a synthetic input constructor
under answer-bearing axioms, plus four concrete examples.

## 1. Input and provenance integrity

### Layout and required records

`/audit-input.json` declares:

- `record_layout = legacy-selected-stage1`
- `semantics_mode = SUPPLIED_SEMANTICS`
- problem `67-fruit-distribution`, condition `semantics`

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` exists as required. I did not use
`writing-semantics`, because this is not `GENERATED_SEMANTICS`.

All records required for `legacy-selected-stage1` are present, readable,
regular non-symlink mounts:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the JSONL trace under `/generation-evidence/codex-trace`
- `/generation-evidence/usage.json`, which is present and was inspected

Historical `runtime-metrics.json` is absent, but the declared legacy layout
does not require it. No historical image observation was reconstructed.

The campaign object in `/audit-campaign-lock.json` equals the
`audit_campaign` object in `/audit-input.json`. Its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The independently calculated hashes for the run manifest, task manifest,
stage-1 result, invocation, metrics, usage, last message, output log,
generation prompt, structured trace, canonical source, prompt, and translator
all match the launcher-recorded hashes. Exact results are in
`evidence/provenance_check.log`.

The structured trace contains 157 successfully parsed JSON events, including
all 30 recorded tool calls. The complete event/tool-call summary and hashes
are in `evidence/generation_record_summary.log`. The generation report and its
prior `#Top` were treated only as untrusted claims.

### Candidate/trusted comparisons

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- A recursive type/name/content comparison of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` found zero differences.
- There are no symlinks, missing entries, additional entries, mistyped
  entries, or changed entries in the candidate supplied-semantics tree.
- The required proof artifacts `solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh` are present, readable regular
  files.

There is no infrastructure breach, so a candidate verdict is appropriate.
The checking script is `evidence/provenance_check.py`.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract and trusted canonical behavior

The prompt says that `s` represents the counts of apples and oranges in a
basket whose total fruit count is `n`; the function returns the remaining
mango count. All four examples have the form:

```text
<nonnegative integer> apples and <nonnegative integer> oranges
```

The trusted canonical implementation does not index fixed positions. It
splits on the literal space character, converts every token for which
`isdigit()` is true, sums those integers, and returns `n - sum(numbers)`.

The candidate implementation is:

```python
fruits = s.split()
return n - int(fruits[0]) - int(fruits[3])
```

It is equivalent to the canonical implementation for the demonstrated
five-token grammar, including arbitrary-precision nonnegative integers and
ordinary extra ASCII spaces. It is not equivalent to the canonical function
on arbitrary strings from which digit tokens can be extracted.

### Translator fidelity

In a clean scratch directory I ran:

```text
python3 py2mpy.py solution.py > regenerated.mpy
cmp -l regenerated.mpy solution.mpy
```

`cmp` exited 0. The submitted `solution.mpy` is byte-identical to trusted
regeneration. See `evidence/translator_regeneration.log`.

### Independent differential test

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and `/candidate/solution.py`. It runs:

- all four documented examples;
- zero counts, equality `A+B=N`, leading zeros, leading/trailing and repeated
  ASCII spaces, punctuation, and arbitrary-precision values;
- a deterministic 243-case grid;
- 200 seeded random valid-form cases;
- empty/no-digit boundaries;
- alternate grammatical placements, an additional digit token, tab
  whitespace, and a signed-token boundary.

There were 462 cases total: 454 matches and eight recorded mismatches. All 454
five-token/near-five-token valid-form tests matched, including all examples.
Representative divergences are:

- `("", 7)`: canonical returns 7; candidate raises `IndexError`.
- `("there are 5 apples and 6 oranges", 19)`: canonical returns 8;
  candidate raises `ValueError`.
- `("5 apples and 6 oranges and 2 labels", 19)`: canonical returns 6;
  candidate returns 8.
- `("5\tapples and 6 oranges", 19)`: canonical returns 13 under its literal
  space splitting; candidate returns 8.

The prompt's examples may reasonably suggest the exact five-token grammar, so
the out-of-grammar mismatches are not the sole basis of the verdict. Even
under the most generous exact-grammar reading, the K general claim never
connects its synthetic input constructor to any actual string. The complete
inputs and results are in `evidence/differential_test.log`.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/reconstruction`. The scratch tree used the trusted mounted
semantics, trusted translator, and candidate source files only. No
candidate-provided kompiled directory, cache, `kprove.out`, or
`concrete-run.out` was reused.

The live toolchain is K 7.1.293. `kup` is absent, but the independently
installed `kompile`, `krun`, and `kprove` binaries all run. See
`evidence/tool_versions.log`.

### Fresh concrete definition

Command:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

Exit status: 0. See `evidence/kompile_llvm.log`.

The reviewer-authored concrete harness first reproduces the exact three-line
candidate function and then asserts eight normal/boundary exact-grammar
cases. Its source is `evidence/k_concrete_tests.py`. The function body was
diffed against `solution.py`, translated with the trusted translator, and run:

```text
krun k_concrete_tests.mpy --definition runtime-audit-kompiled --output pretty
```

Exit status: 0. The final configuration has `.K`, `NoExc`, and
`<exit-code> 0 </exit-code>`. See `evidence/krun_concrete.log`.

### Fresh proof definition and positive claims

Commands:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

Both commands exited 0, and `kprove` printed `#Top`. The one `kprove` command
loads all five claims in `SPEC`; thus the general claim and each of the four
positive example claims were independently reconstructed. Logs:
`evidence/kompile_haskell.log` and `evidence/kprove_positive.log`.

Mechanical closure under the candidate-extended theory therefore passes.
That is verification, not yet validation.

## 4. Adequacy and real-program pinning

### Plain-language restatement of the claims

The general claim at `/candidate/spec.k:6` starts in the standard empty module
configuration, loads `solutionModule`, and calls `fruit_distribution` with:

- first argument `str(fruitSentenceCodes(A,B))`;
- second argument K integer `N`;
- precondition `A >= 0`, `B >= 0`, and `A+B <= N`.

It requires the terminating `<k>` result to be exactly `N-A-B`, the stack to
be empty, `ret` to be `noRet`, no exception, exit code 0, and exactly one heap
allocation (`heapLoc` 0 to 1). Final heap and scopes are existentially
unconstrained.

The other four claims call the same loaded function with the four literal
prompt strings and require the concrete results 8, 2, 95, and 19. They have no
symbolic precondition.

The general precondition is satisfiable. For example:

```text
A = 5, B = 6, N = 19
```

Both Python implementations return 8 on the actual string
`"5 apples and 6 oranges"`, and the claimed arithmetic expression is also 8.
The four literal K claims establish those four concrete executions.

### Program-term identity

`solutionModule` is not an unrelated substituted body. The trusted translator
regeneration was compared mechanically to the rule's complete `Module(...)`
right-hand side. After removing only ASCII whitespace and the explicit
optional empty `.Exprs` list unit/trailing surface comma, the constructor
strings are identical (252 normalized characters each). See
`evidence/program_pinning_check.py` and
`evidence/program_pinning_check.log`.

An additional K claim placed both terms in the `<k>` cell and closed with
`#Top`; see `evidence/pinning-spec.k` and
`evidence/kprove_pinning.log`. An initial functional-sort formulation was
rejected by the Haskell backend before proof execution and is preserved only
as a diagnostic in `evidence/kprove_pinning_functional_failed.log`; it is not
used as evidence.

The executed body contains the actual function binding and material control
flow:

1. module load creates the `fruit_distribution` closure;
2. the call binds `s` and `n`;
3. `s.split()` is evaluated and assigned to `fruits`;
4. indices 0 and 3 are read;
5. both elements are passed through the resolved builtin `int`;
6. the two integer subtractions execute;
7. `Return` pops the frame and produces the exact result.

There are no helper or loop claims.

### Body sensitivity

In scratch I changed the program term actually embedded in
`solutionModule`, replacing the final index 3 with index 0, while leaving the
source theorem unchanged. The mutated definition built successfully, but
`kprove` exited 1 with the meaningful residual:

```text
N -Int A -Int A == N -Int A -Int B
```

See `evidence/body-mutated-verification.k`,
`evidence/body-mutated-spec.k`, and `evidence/body_sensitivity.log`. This
confirms dependence on the embedded body.

### Adequacy failure

Program-term identity passes, and the result is exact rather than free or
tautological. The failure is the input/value connection. No claim establishes:

```text
fruitSentenceCodes(A,B)
  = codes of "<A> apples and <B> oranges"

decimalCodes(I)
  = codes of the decimal representation of I
```

Consequently the general claim is not quantified over actual source-language
strings—not even over actual strings having the exact five-token grammar. The
precondition also narrows to nonnegative counts with `A+B<=N`; that physical
basket condition is plausible from the prose but is not enforced by the
Python entry point. The decisive gap remains the wholly synthetic string
domain.

The four real-string example claims cannot turn a finite set of examples into
an unrestricted theorem. Adequacy/real-input pinning fails.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.md` inventories the assembled supplied semantics,
all helper K files, candidate `verification.k`, and `spec.k`. Multi-line items
are kept as single rows with exact source locations, attributes, target-path
classification, and a decision. Counts:

- 1,105 total source items;
- 698 rules;
- 229 syntax declarations;
- five contexts;
- one configuration;
- five claims;
- all module/import/require declarations.

There are no local `functional` or `simplification` declarations. Function,
`total`, `concrete`, `owise`, priority, strictness, macro, symbol, and
no-evaluator attributes are recorded per row. The generator and count log are
`evidence/rule_inventory.py` and `evidence/rule_inventory.log`.

The supplied tree is fixed by the condition and byte-identical to the trusted
mount. Unused fixed rules do not receive terms from this target and cannot
contribute to claim closure. They are nevertheless individually enumerated in
the inventory. On the material path, the following mapping was checked:

| Program construct | Fixed declaration/rules |
|---|---|
| `Module`/`FuncDef`/`Params` | `syntax.k:53-61`, `core.k:124-127`, `functions.k:14-16` |
| call and binding | `call.k:16-32,69-74`, `core.k:130-191`, `functions.k:63-75` |
| assignment | strict `Assign` at `syntax.k:41`; store update at `controls.k:9-18` |
| `s.split()` | attribute/call routing at `call.k:16-24`; fixed split at `methods.k:72-86`, displaced for the symbolic constructor by the proof rule |
| list allocation/indexing | `core.k:117-121`; `subscript.k:11-41` |
| `int(...)` | builtin resolution at `core.k:157-181`, type dispatch at `call.k:31-32`, concrete integer parsing at `builtins.k:139-160`, displaced for `decimalCodes` |
| left-to-right expression evaluation | `seqstrict` `BinOp` at `syntax.k:15`; call-argument loop at `core.k:183-191` |
| integer subtraction | `operators.k:12`; `int.k:13` |
| return/control cleanup | `functions.k:78-90` |
| configuration/state | `core.k:49-60`, including scopes, heap/allocation counter, stack, return, exception, and exit cells |

The reached rules preserve left-to-right evaluation, select the loaded
function binding and builtin `int` through the actual scope chain, allocate
one list object, dereference the list before indexing, and pop the call frame
on return. No reached opaque float, sort, keyed-sort, or MD5 primitive affects
the value.

The fixed MPY model is intentionally smaller than CPython. Relevant
limitations are explicit:

- strings are ASCII-only;
- `valSeqAt` is total/underspecified out of bounds instead of modeling
  `IndexError`;
- the multi-character `intDigAcc` fold assumes digit codes and does not
  model `ValueError` for arbitrary characters.

Those differences do not falsify the four literal claims or exact
five-token/digit path, but they reinforce that malformed and broader inputs
are excluded rather than proved.

### Candidate proof-local inventory and decisions

| Extension | Class and complete-domain assessment | Decision |
|---|---|---|
| `decimalCodes(Int)` | Fresh opaque constructor of `IntSeq`; no equations, guards, decimal recursion, or connection claim | Rejected as unconnected result-bearing abstraction |
| `fruitSentenceCodes(Int,Int)` | Fresh opaque constructor of `IntSeq`; no equation constructing digits, spaces, or words | Rejected as unconnected input abstraction |
| split rule at `verification.k:15` | Operational bridge. It matches `#applyK(toCall(boundMethodV(str(fruitSentenceCodes(A,B)),"split")),.Vals)` for `A,B>=0`, with arbitrary continuation and other cells framed. It allocates one heap list exactly as the fixed split rule would, so state/control footprint and continuation containment are adequate. Its five token values are not connected to fixed `splitWS`. | Rejected: missing universal value connection |
| `applyBuiltin("int",str(decimalCodes(I)),.Vals) => I` | Result-bearing operational/equational bridge over all `I>=0`. It has no state/control effect and does not overlap the fixed `.IntSeq`/`iCons` parsing cases, but directly supplies a final-result operand. | Rejected: missing universal value connection |
| `solutionModule` total function and equation | Definitional summary, complete on its nullary symbol | Accepted; constructor identity independently checked |

The split bridge's binding is exact: it acts only after method lookup and
argument evaluation have produced the bound method with no arguments. Its
arbitrary continuation is no broader than the corresponding fixed split
rule, and it introduces no return, exception, or frame-pop effect. Therefore
the specific defect is not context/control mismatch; it is the unproved,
result-bearing value substitution.

The `int` bridge similarly has no overlap ambiguity: `decimalCodes(I)` is a
fresh constructor and cannot match the fixed concrete `.IntSeq` or
`iCons(...)` shapes. Priority does not supply a semantic justification.

### Bridge-free and opposite-interpretation evidence

I built a definition that retains only the fresh constructors and exact
`solutionModule`, but removes both operational bridges. The satisfying ground
claim for `A=5, B=6, N=19` then exits 1 with
`WarnStuckClaimState`. The residual explicitly contains:

```text
splitWS(fruitSentenceCodes(5,6), .IntSeq, .ValSeq)
applyBuiltin("int", valSeqAt(...), .Vals)
```

This is the genuine fixed-semantics obligation. See
`evidence/audit-variants.k`, `evidence/bridge-free-spec.k`,
`evidence/kompile_bridge_variants.log`, and
`evidence/kprove_bridge_free.log`.

Two value-sensitivity variants demonstrate why a name/comment is not a
connection theorem:

1. Keep the split bridge but decode every `decimalCodes(I)` as `I+1`. The
   actual program body proves `#Top` for result 6 on the ground witness.
2. Keep ordinary abstract decoding but let the split bridge fabricate
   `decimalCodes(A+1)` as token 0. The body proves `#Top` for result 7.

Both variants build and both proof commands exit 0 with `#Top`; both Python
implementations return 8 on the corresponding real string. See
`evidence/opposite-int-spec.k`, `evidence/opposite-split-spec.k`, and
`evidence/kprove_opposite_interpretations.log`.

This audit does not assert that the candidate's exact equations are globally
mathematically false over K's fresh constructor term algebra. The narrower,
fully evidenced defect is decisive: the constructors have no source meaning
without the very bridges whose correctness is at issue, and the required
bridge-free universal connection theorem is absent. The opposite variants
are false-conclusion witnesses for the admitted alternative interpretations,
not a claim that the candidate returns 6 or 7 under its own exact rules.

Gate A real-program soundness therefore fails under the mandated
`validating-proof` result-bearing abstraction procedure.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created a fresh spec module
that changes only the general result obligation:

```text
N -Int A -Int B
```

to:

```text
(N -Int A -Int B) +Int 1
```

The mutation is demonstrably false for the satisfying witness
`A=5, B=6, N=19`: the execution yields 8 while the mutation demands 9.

The dry run exits 0, so the mutation parses/builds against the clean proof
definition. The actual proof exits 1 with `WarnStuckClaimState` and the exact
unmet implication:

```text
N -Int A -Int B == N -Int A -Int B +Int 1
```

This is a meaningful result failure, not a parser error, missing import,
timeout, or unrelated crash. Artifact and log:
`evidence/spec-vacuity.k` and `evidence/nonvacuity.log`.

Non-vacuity passes. It establishes that the candidate theorem constrains its
synthetic result; it does not establish that the synthetic operations denote
the real string computation.

## 7. Proven-versus-assumed accounting

### What `#Top` actually establishes

Under the supplied MPY semantics plus all rules in candidate
`verification.k`, the successful general reachability proof establishes:

> For K integers `A,B,N` satisfying `A>=0`, `B>=0`, and `A+B<=N`, if the
> submitted function body is invoked on the special K value
> `str(fruitSentenceCodes(A,B))`, and the special split and integer-decoding
> rules are assumed, then the execution reaches result `N-A-B` with no
> exception, empty stack, exit code 0, and one list allocation.

It also establishes four independent concrete executions for the literal
prompt examples under the fixed supplied split/decimal rules.

It does **not** establish a universal theorem for actual strings of the form
`"<A> apples and <B> oranges"`, much less for every string admitted by the
canonical digit-token implementation.

### Trust ledger

| Boundary | Value/control influence | Assessment |
|---|---|---|
| K 7.1.293 backend and builtin INT/BOOL/STRING/MAP/LIST hooks | Foundational rewriting and arithmetic | Ordinary machine-checking trust boundary |
| Launcher-supplied MPY semantics | All source evaluation, scopes, heap, calls, and returns | Accepted selected-semantics boundary after exact tree integrity check; it is intentionally not full CPython |
| Fixed opaque symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, `md5hexCodes` | Potential float/sort/MD5 values in other programs | None is reached by this target; no effect on closure |
| `solutionModule` | Selects the program body | Acceptable definitional summary; exact trusted regeneration and body-sensitivity evidence |
| `fruitSentenceCodes` | Determines symbolic split input and therefore both operands | Illegitimate program-derived abstraction: no definition or connection theorem |
| `decimalCodes` | Determines both `int` results | Illegitimate result-bearing abstraction: no definition or connection theorem |
| proof-local split bridge | Replaces fixed `splitWS` and allocates the list used by indices 0 and 3 | State/control shape is faithful, but value equivalence is unproved and answer-bearing |
| proof-local int bridge | Replaces fixed decimal parsing and directly returns each symbolic operand | Answer-bearing, no bridge-free value theorem |
| 462-case Python differential test | Empirical implementation/canonical comparison | Finite evidence only: 454 matches, eight broader-domain mismatches |
| eight-case LLVM concrete harness and four K example claims | Real exact-grammar executions | Finite evidence only; cannot prove the general bridge |

### Gate/accounting summary

- Clean reconstruction: **PASS** (`#Top`, exit 0, all five positive claims).
- Program constructor identity and body sensitivity: **PASS**.
- Result constraint/non-vacuity: **PASS**.
- Gate A, real-program soundness: **FAIL** because both result-bearing
  operational abstractions lack bridge-free universal connection theorems.
- Gate B, intent adequacy: **FAIL** because the only general theorem ranges
  over a synthetic K constructor rather than actual HumanEval strings. Four
  examples are finite, and the Python rewrite additionally differs from the
  canonical implementation on broader string shapes.
- Gate C, evidence auditability: **PASS with finite scope**. Commands,
  artifacts, inputs, hashes, and results are reproducible; the empirical
  evidence is explicitly not promoted to a universal proof.

The exhaustive command index is `evidence/COMMANDS.md`. The benchmark decision
boundary maps the material source-domain/connection failure to
`FAIL / NOT_LEGIT`, not to a concern-level legitimate result.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
