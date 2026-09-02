# Independent adversarial audit: 146-specialFilter

## Audit conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program on the material HumanEval domain: arbitrary finite lists of integers.
The proof was reconstructed from source using the trusted supplied semantics;
the two positive claims close, the entry claim executes the submitted function
body, and fresh false result and body mutations are rejected for the expected
semantic reason.

The candidate's compiled definitions, `prove.log`, `PROOF.md`, generation
trace, and reported `#Top` were not trusted. They were inspected only as claims.

## 1. Input and provenance integrity

### Launcher and campaign records

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and problem
`146-specialFilter`. `/reference/reference-semantics` is present, as required
for that mode.

I read the launcher-owned audit input, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`, and every required
pipeline-v3 generation record:

- `invocation.json`, `metrics.json`, `runtime-metrics.json`, and `usage.json`;
- `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured JSONL trace below `codex-trace/`.

The campaign block in `/audit-input.json` is structurally identical to the
mounted lock. The lock's independent SHA-256 is
`e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`,
matching the launcher record.

All launcher-declared container paths and all pipeline-v3-required records are
present, readable, of the expected file/directory type, and not symlinks.
Direct SHA-256 values for the campaign, canonical program, prompts,
translator, manifests, metrics, usage, generation output, prompt, and trace
file match the corresponding recorded hashes. An independent typed-tree
digest was also computed for every mounted tree. In particular, the candidate
and trusted semantics trees produced the same reviewer digest over all 25
entries.

The exact commands and results are in
[`integrity.log`](evidence/integrity.log), produced by
[`integrity-check.sh`](evidence/integrity-check.sh).

### Structured generation evidence

The untrusted structured trace contains 462 valid JSON lines. The independent
parser consumed all of them and recorded 79 function calls and 79 matching
function outputs, along with the final generation claim. See
[`trace_summary.py`](evidence/trace_summary.py) and
[`generation-trace-summary.log`](evidence/generation-trace-summary.log).
Nothing in those generation claims was used as proof evidence.

### Trusted-input comparisons

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  SHA-256 is
  `310a71d2feca4b63bf4ab0279cac60820a61a57157a413efd62823e6c69eb917`.
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`; SHA-256 is
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- A recursive, no-symlink comparison of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` reports no missing, added, changed, or
  mistyped entry. Modes also match.
- No symlink exists anywhere below `/candidate`, `/reference`, or
  `/generation-evidence`.

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks for the number of array elements that:

1. are greater than 10; and
2. have odd first and last decimal digits.

The material domain is finite integer arrays. The examples are integer-only,
and the trusted canonical implementation converts the first and last decimal
characters to integer digits before testing membership in
`(1, 3, 5, 7, 9)`. Non-integral Python representations are not specified by
the prompt's digit contract.

The trusted canonical program iterates through the input, applies exactly
those three tests, and increments a counter. The submitted program implements
the same predicate using the parity of `ord()` for the endpoint decimal
characters. For decimal digits, the code point is `48 + digit`; because 48 is
even, character-code parity equals digit parity. The `num > 10` test ensures
that any string examined is the nonempty decimal representation of a positive
integer.

The extra initializations of local variables `num` and `text` in
`solution.py` are result-inert, including on empty input.

### Translator identity

The trusted translator was rerun in `/tmp/audit-work`:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy submitted-solution.mpy
```

Both commands exited 0. The regenerated and submitted files have identical
SHA-256
`258b46a7972abe684d63fa03b80c5dc1b3c69fc61cb236130d844ebfa38d25ea`.

### Independent differential test

[`differential.py`](evidence/differential.py) separately imports the trusted
canonical function and the submitted `solution.py`. It also uses an
independently written endpoint-digit oracle. Its deterministic scope is:

- both documented examples and the empty input;
- threshold and all four endpoint-parity branch combinations;
- repeated, negative, zero, and 1,000-digit integer cases;
- every singleton integer from -1000 through 10000;
- every list of lengths 0 through 4 over 11 branch representatives;
- 2,000 seeded random lists of lengths 0 through 64 with integer magnitudes
  up to 150 digits.

Actual result:

```text
total_cases=29117 mismatches=0
EXIT: 0
```

Commands and output are in
[`program-fidelity.log`](evidence/program-fidelity.log). The submitted program
is faithful to canonical on the intended domain.

## 3. Clean proof reconstruction

### Isolation and builds

Only source artifacts needed for execution were copied into
`/tmp/audit-work`. The semantics copy came from the trusted
`/reference/reference-semantics`, not from a candidate kompiled directory.
No candidate definition, cache, interpreter, compiled KORE, or proof log was
reused.

The live toolchain is K v7.1.293; paths and versions are recorded in
[`toolchain.log`](evidence/toolchain.log).

The following definitions were freshly built:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition replay-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition replay-verification-kompiled
```

Both exited 0. The concrete build reported supplied-model non-exhaustiveness
warnings in functions unrelated to this program; the Haskell build reported
only unused variables in the supplied `strLt` rules. No proof-local warning
indicates a missing or conflicting rule.

The submitted `.mpy` module and a reviewer harness containing normal,
threshold, parity, empty, and large-integer assertions were run under the
fresh LLVM definition. Both exited 0 with final `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`. The harness source is
[`concrete_checks.py`](evidence/concrete_checks.py). Complete bounded build
and execution output is in
[`clean-rebuild.log`](evidence/clean-rebuild.log).

### Positive claims

Every positive claim was exercised against the fresh Haskell definition:

| Proof run | Result |
|---|---|
| `SPEC.filter-loop` alone | `#Top`, exit 0 |
| complete `SPEC` aggregate, with no trust flag | `#Top`, exit 0 |
| `SPEC.special-filter`, composed with the exact independently proved `SPEC.filter-loop` claim | `#Top`, exit 0 |
| reviewer ground claims for empty, `[15]`, and the second example | `#Top`, exit 0 |

The entry-isolation command uses `--trusted SPEC.filter-loop` only after that
exact claim independently printed `#Top`; it is a mechanical proof-composition
check, not a new assumption. More importantly, the aggregate command proves
both claims together and uses no trust flag.

Selecting only `SPEC.special-filter` removes the separate loop circularity
from K's active claim set and therefore unrolls the symbolic loop. That
diagnostic behavior is not a claim failure; the correct aggregate and
composed commands both close.

Exact commands, `#Top`, and exit statuses are in
[`proof-replay.log`](evidence/proof-replay.log), produced by
[`proof-replay.sh`](evidence/proof-replay.sh).

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.filter-loop` says:

- starting at the real `#loop(list(INPUT), Name("num"), filterBody())`
  control point inside the active function call;
- with integer-only remaining input, current integer counter `COUNT`, exact
  locals, exact module binding, empty heap, real call frame, and the real
  trailing `Return(Name("count")) ~> #endcall`;
- the loop reaches that same return continuation with `count` increased by
  exactly `specialCount(INPUT)`.

It intentionally leaves only the final scratch locals `num` and `text`
existential. The input binding, counter, environment, scopes, heap, allocation
counters, stack, return state, exception state, and exit code are otherwise
preserved or constrained.

`SPEC.special-filter` says:

- load a module containing `specialFilter` with the submitted parameter and
  function body;
- resolve and call that actual binding on any finite `ValSeq` satisfying
  `allInts`;
- return exactly `specialCount(INPUT)`;
- restore the caller environment and stack, remove the local call scope,
  preserve an empty heap and its counter, leave no return or exception state,
  and retain the loaded module binding.

The RHS is not a free result, implication-only result, or tautology.
`specialCount(INPUT)` is a structurally recursive mathematical function fixed
by disjoint equations.

### Constructor-level program identity

The submitted regenerated module and this claim term:

```text
Module(FuncDef("specialFilter", Params("nums"), specialFilterStmts()))
```

were independently parsed with the fresh proof definition and expanded with
`kast --expand-macros --output kore`. The two resulting 7,015-byte KORE terms
are byte-identical, with SHA-256
`7898f6d22109b0c13c22115ca6fe4f0c1f7257bc7e5ee3e7e62391774266e65b`.

See [`pinning.log`](evidence/pinning.log),
[`submitted-expanded.kore`](evidence/submitted-expanded.kore), and
[`claim-expanded.kore`](evidence/claim-expanded.kore). This is a mechanical
constructor-level pin, not a prose source correspondence.

There is no Call-level interception for `specialFilter`. The fixed semantics
loads the `FuncDef`, performs scope lookup, evaluates the argument, creates a
real frame, binds `nums`, executes all statements, returns, and pops the frame.

### Satisfying states and substitutions

The entry precondition is satisfiable for `.ValSeq`, for
`vCons(15, .ValSeq)`, and for the second documented list; `allInts` reduces to
true on each. The loop precondition is satisfiable, for example, at the
reachable empty-loop state with `INPUT = ORIGINAL = .ValSeq`, `COUNT = 0`,
`num = 0`, `text = ""`, environment 1, module scope 0, call frame
`frame(.K, 0, 1)`, empty heap, and no exception.

[`spec-ground.k`](evidence/spec-ground.k) substitutes those concrete inputs
into the actual program claim. Its aggregate proof prints `#Top`. The same
inputs return 0, 1, and 2 respectively from both Python implementations.

The independent threshold-100 body mutation in stage 6 changes the actual
function term loaded and stored in the closure; it is rejected. Thus body
sensitivity is tested against the executed term, not against an unrelated
external source file.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule-inventory.txt`](evidence/rule-inventory.txt), generated by
[`inventory_k.py`](evidence/inventory_k.py), is a line-addressable inventory
containing the complete text, guards, and attributes of every declaration,
configuration, context, rule, and claim in:

- all supplied `reference-semantics/**/*.k` files;
- `verification.k`;
- `spec.k`.

Inventory totals are 249 syntax records, 757 rules, 5 contexts, 1
configuration, and 2 claims. It identifies 165 function-declaration records,
119 total-declaration records, 25 `no-evaluators` declaration records, 47
priority-bearing records, 55 concrete records, and all 13 simplification
records. There are no `[functional]` declarations. Per-file counts are at the
end of the inventory.

Of the 757 rules, 734 belong to the fixed supplied model and 23 are
proof-local. The supplied `MPY-CONCRETE` rules are inventoried even though the
proof definition imports `MPY`, not `MPY-CONCRETE`.

### Material fixed-semantics path

Every source constructor used by `solution.mpy` has an ordinary execution path:

| Program construct | Fixed declaration and behavior checked |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax in `syntax.k`; `#loadAll`, statement sequencing, and closure creation in `core.k`/`functions.k` |
| `Assign`, `Name`, integer and string literals | strict RHS evaluation and scope writes in `controls.k`; chained lookup and literals in `core.k`; ASCII string construction in `str.k` |
| `Call(Name("specialFilter"), ...)` | callee then left-to-right argument evaluation in `call.k`; real frame creation, parameter binding, return, and pop in `call.k`/`functions.k` |
| bare `list(INPUT)` and `For` | list iterator rules in `list.k`; `For` to `#loop`, `#iterNext`, target binding, body, and `#loopLbl` in `controls.k`/`tuple.k` |
| nested `If` and `Compare` | strict condition evaluation and `#branch` in `controls.k`; ordered operand contexts and dispatch in `operators.k` |
| integer `>` and `==` | exact integer comparisons in `int.k` |
| `str(num)` | real builtin binding and call dispatch in `core.k`/`call.k`; integer-to-decimal rule in `builtins.k` |
| `text[0]`, `text[-1]` | object then index contexts, negative-index normalization, and `intSeqAt` in `subscript.k`; integer unary minus in `int.k` |
| `ord(...) % 2` | one-character `ord` in `builtins.k`; Python-style integer modulo and comparison in `int.k` |
| `count += 1` | current-scope lookup/write and exact integer addition in `controls.k`/`int.k` |
| `Return(count)` | strict return, abrupt transfer to `#pop`, real stack restoration, and scope removal in `functions.k` |

Evaluation order is the translated Python order. The program allocates no heap
object: its input is the read-only bare-list representation allowed by the
supplied model, and integer strings are values. The target's empty heap and
zero heap counter are therefore preserved. Scope 1 is allocated for the call
and removed on pop; the module closure remains in scope 0. No exception path
is possible on the integer domain because every examined integer is positive
and its decimal string is nonempty.

The supplied priority rules either implement dereference/interception for
constructs not reached here or refine real lookup, call, assignment, and
iteration behavior. None preempts this program with a result oracle. The
concrete-only rules do not enter the Haskell proof theory.

The supplied opaque symbols for floats, sorting, and MD5 are inert here:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `floatFinite`, `ltFI`, `ltIF`,
`eqIF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. No constructor,
binding, or rule on the target path can produce any of them.

The LLVM non-exhaustiveness warnings concern unused functions such as
`mapStrVS`, float conversion, `joinCodes`, and out-of-bounds `valSeqAt`.
They do not match any target operation. The used string index is provably
in-bounds.

### All 23 proof-local rules

1. `filterBody()` and `specialFilterStmts()` are two syntax macros. Expansion
   is mechanically identical to the submitted module. They replace no
   execution.
2. The two `allInts` equations are disjoint structural recursion over
   `.ValSeq` and `vCons`; they exactly state the claim domain.
3. `definedProjectInt(V) => isInt(V)` is the fixed sort predicate under a
   name.
4. The five projection/cast rules characterize the defined `Val :> Int`
   subsort projection, orient it for concrete and symbolic simplification,
   reduce it on an actual `Int`, and state idempotence. On the only domain
   where a projection influences a result, `definedProjectInt` is entailed.
   The total extension remains underdetermined off that domain, but no
   off-domain value reaches control, state, `specialCount`, or a
   postcondition.
5. The guarded `applyCmp(">", V, I)` rule is the fixed
   `applyCmp(">", I1:Int, I2:Int)` equation after the proved sort projection.
   Its overlap with the fixed rule has the same RHS.
6. The guarded `applyBuiltin("str", V, .Vals)` rule is exactly the fixed
   integer `str` equation after the same projection. Its overlap also agrees.
7. `firstDecimalCode` and `lastDecimalCode` select indices 0 and length minus
   one of the fixed `Int2String`/`strToCodes` representation. Integer decimal
   strings are nonempty.
8. `firstDigitOdd`, `lastDigitOdd`, and `isSpecial` are total definitional
   equations. Modulo-2 character-code parity is equivalent to decimal-digit
   parity.
9. The six `specialCount` equations consist of the empty case and five
   mutually exclusive cons cases: qualifying integer, integer at most 10,
   first endpoint even, last endpoint even, and non-integer. They are
   exhaustive, agree with the program's branch order, and recurse strictly on
   the tail.

No proof-local rule rewrites a `Call`, `For`, `#loop`, `Return`, frame,
configuration cell, or complete program expression to a summary. There is no
operational bridge and no program-derived opaque result oracle.
`specialCount` is connected to execution by the proved loop reachability
claim, not assumed by a rewrite.

I found no proof-local false rule and therefore no false-conclusion witness.
For the fixed supplied semantics, all material rules above match the modeled
Python behavior; every remaining inventoried rule is sort- or
constructor-inert for this program. There is no narrower evidence gap that can
affect this theorem.

## 6. Fresh non-vacuity test

The candidate's mutation files were not relied upon. I created
[`reviewer-spec-vacuity.k`](evidence/reviewer-spec-vacuity.k), which loads the
actual submitted body, calls it on the satisfying integer input `[12]`, and
falsely claims result 1. The real result is 0 because the last digit is even.

The mutation parses, builds against the fresh definition, and runs to the
relevant terminal state. It exits 1 with `WarnStuckClaimState`; the residual
contains:

```text
<k>
  0 ~> .K
</k>
```

against the claimed result 1. This is an unmet result obligation, not a parser
error, missing import, timeout, or unrelated crash.

I separately created
[`reviewer-spec-body-mutation.k`](evidence/reviewer-spec-body-mutation.k).
It changes the executed comparison threshold from 10 to 100 and retains the
original expected result 1 for `[15]`. It also builds, reaches actual result 0,
and exits 1 with `WarnStuckClaimState`.

Exact commands, full bounded residuals, and statuses are in
[`negative-replay.log`](evidence/negative-replay.log):

```text
fresh false result mutation: EXIT: 1
fresh body-sensitivity mutation: EXIT: 1
EXPECTED_FAILURES_CONFIRMED=1
```

The proof is non-vacuous and sensitive to both its result and executed body.

## 7. Proven versus assumed accounting

### What is formally established

Relative to the supplied MPY definition and K reachability logic:

- for every finite constructor `ValSeq` whose elements satisfy `isInt`;
- starting from the exact module-load and call configuration in
  `SPEC.special-filter`;
- if execution terminates, the submitted `specialFilter` body returns
  `specialCount(INPUT)`;
- `specialCount` adds one exactly for each integer greater than 10 whose first
  and last decimal character codes are odd;
- the function executes through real lookup, argument evaluation, binding,
  loop control, builtin calls, state updates, return, and frame pop;
- the stated final module binding, environment, scopes, counters, heap, stack,
  return state, exception state, and exit code hold.

The theorem is unbounded in finite list length and K integer magnitude. It is
not a finite-size unrolling.

### Trust ledger

| Boundary | Influence and dependents | Assessment and evidence |
|---|---|---|
| K v7.1.293 parser, kompilers, Haskell backend, SMT support, and reachability logic | All machine-checked closure results | Necessary foundational trust; versions recorded, clean replay reproducible |
| Trusted supplied MPY semantics | Defines the modeled program execution and cells | Authorized fixed model; candidate copy is byte-identical; relevant operational rules were statically audited and concretely exercised |
| K integer/string hooks, especially `Int2String`, `substrString`, `ordChar`, and integer arithmetic | Decimal representation and both endpoint predicates | Acceptable low-level primitive boundary; these are fixed semantics operations, not task-answer rules; concrete large-integer tests and the canonical differential support the bridge |
| K sort membership and `Val :> Int` projection | Dynamic symbolic integer dispatch | Proof-local rules connect the projection exactly under `isInt`; all result-bearing uses are guarded |
| Trusted translator | Source-to-constructor identity | Trusted mounted translator regenerated the submitted `.mpy` byte-for-byte |
| Macro-to-program correspondence | Whether the claim executes the submitted body | Not merely assumed: expanded submitted and claim KORE terms are byte-identical |
| Decimal code parity equals digit parity | Human-facing odd-digit meaning | Ordinary mathematics: ASCII digit code is `48 + digit`; independently supported by 29,117 differential cases |
| Canonical equivalence | Program fidelity to benchmark ground truth | Finite empirical evidence only, not substituted for the K proof; zero mismatches over the recorded independent suite |
| Fixed opaque float/sort/MD5 symbols listed in stage 5 | None; unreachable from this program and absent from the postcondition | Harmless inert supplied-model surface, not a proof assumption |
| Off-domain values of `projectIntTotal` | None under `allInts`; no off-domain projection reaches result or control | Acceptable guarded totalization, not an unconstrained result oracle |

There is no trusted proof claim in the successful aggregate run, no
proof-local trusted primitive carrying the answer, and no empirical bridge
used in place of symbolic execution.

### Excluded results

- This is partial correctness, not a separate termination or complexity
  theorem.
- Non-integer list elements are outside the source digit contract and formal
  precondition.
- The proof does not verify the implementation of K, its hooks, the trusted
  translator, or CPython itself.
- Finite differential testing supports program/canonical and decimal-hook
  fidelity only; it is not the source of the unbounded list theorem.

### Gate and benchmark mapping

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS.
- Gate C, trust and evidence auditability: PASS.
- Kit status: `VALIDATED`.
- Benchmark mapping: the proof is sound, result-constraining, pins the real
  regenerated program, and covers the full material integer-list contract.

VERDICT: PASS
LEGITIMACY: LEGIT
