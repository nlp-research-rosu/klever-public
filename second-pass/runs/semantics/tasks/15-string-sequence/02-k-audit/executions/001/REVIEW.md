# Adversarial audit: 15-string-sequence

## Outcome

The candidate's source solution is correct on the intended integer domain, its
submitted `.mpy` file is an exact trusted translation, and every submitted
positive claim freshly reconstructs to `#Top`. The claims are also
result-constraining: a fresh off-by-one postcondition mutation fails for the
expected semantic reason.

Nevertheless, this is not a legitimate proof of the submitted artifact. The
public claims close through the priority-40 operational bridge at
`/candidate/verification.k:59-66`. That bridge is broader than the separately
proved loop theorem and is false on part of its match domain. A machine-checked
witness with the intended input `n = 1` shows that fixed semantics returns
`"0"` when the module scope shadows `range` with an empty-range closure, while
the bridge-enabled theory proves the false result `"0 1"`. In addition, the
proof build never consumes `solution.mpy`; it proves a manually restated
`sequenceBody`. A material mutation of the submitted `.mpy` body leaves a fresh
proof build and positive proof at `#Top`.

These are Gate A real-program soundness and pinning failures. Successful
reconstruction and non-vacuity do not make a proof under a materially unsound
extension legitimate.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the trusted mounts do not
contradict the rendered mode. This is not an infrastructure breach.

I recursively compared the candidate tree against the trusted tree with:

```text
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
```

The command exited 0. A separate type scan found no candidate symlinks or
special filesystem entries. Thus there are no missing, additional, changed,
mistyped, or symlinked entries in the supplied-semantics copy. Candidate and
trusted `prompt.py` are byte-identical (SHA-256
`1eb46648867a6e499ee7e4fa6500b594937f325209204606d7391c8cad9df9c4`);
candidate and trusted `py2mpy.py` are byte-identical (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
The exact checks, manifest hashes, and exit statuses are in
[01-integrity-rerun.log](evidence/01-integrity-rerun.log), driven by
[audit-stage1.sh](evidence/audit-stage1.sh).

The following requested provenance artifacts are missing from `/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace (`*trace*` or `*.jsonl`) is present. These
omissions limit provenance auditability but do not create a semantics-mode
infrastructure contradiction. The candidate's `proof.log`, two `.pyc` files,
and prose comments were treated only as untrusted claims. No candidate-built
definition or cache was used.

For transparency, [01-integrity.log](evidence/01-integrity.log) records an
initial logging-wrapper failure: `script` invoked `sh`, whose `set` rejected
`pipefail`, and exited 2 before performing the check. The successful explicit
Bash rerun above is the operative evidence.

All execution artifacts were copied from source into
`/tmp/audit-work/reconstruction`. All builds and mutations occurred below
`/tmp/audit-work`; the candidate tree remained read-only.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

`/reference/prompt.py` requires `string_sequence(n: int)` to return the decimal
representations of every integer from `0` through `n`, inclusive, separated by
single spaces. Its documented examples are:

```text
n = 0  -> "0"
n = 5  -> "0 1 2 3 4 5"
```

The trusted canonical implementation is:

```python
return " ".join([str(x) for x in range(n + 1)])
```

Consequently, on the full Python-integer domain, negative `n` values produce
the empty string because `range(n + 1)` is empty. For `n >= 0`, the result is
exactly `"0 1 ... n"`.

`/candidate/solution.py` implements the same behavior with an explicit
negative branch and an iterative concatenation. The preliminary assignment
`i = 1` is overwritten by the loop on nonempty ranges and is harmless. No
material source/canonical discrepancy was found.

### Trusted retranslation

From scratch I ran:

```text
python3 /tmp/audit-work/trusted/py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`60cf784fb6f13949ec29c039132b0b33491b84f0bd69a4943bcd8186fdb23aed`.
This establishes byte identity between the submitted `solution.mpy` and a
fresh translation by the trusted translator.

### Independent differential test

[differential.py](evidence/differential.py) independently imports
`/tmp/audit-work/trusted/canonical.py:string_sequence` and
`/tmp/audit-work/reconstruction/solution.py:string_sequence`. It tests:

- both documented examples;
- negative empty-range cases and the `-1/0/1` branch boundaries;
- decimal-width boundaries `9/10`, `99/100`, and `999/1000`;
- 128 deterministic generated integers from `[-100, 300]` using seed `150015`
  (115 unique cases after combining and deduplicating the complete input set).

The command exited 0 with `case_count = 115` and `mismatch_count = 0`. The
complete inputs, outputs, output hashes, exact command, and status are in
[02-program-fidelity.log](evidence/02-program-fidelity.log), driven by
[audit-stage2.sh](evidence/audit-stage2.sh). This is finite bridge evidence,
not a universal proof.

## 3. Clean proof reconstruction

The available toolchain was K `v7.1.337`. I built only from copied source in
`/tmp/audit-work/reconstruction`.

### Concrete definition

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0; see
[03a-kompile-runtime.log](evidence/03a-kompile-runtime.log). I then freshly
translated the concrete assertion harness, required byte identity with the
submitted harness, and ran:

```text
krun concrete_tests.mpy --definition runtime-kompiled --output none
```

It exited 0; see [03b-krun-concrete.log](evidence/03b-krun-concrete.log).
The fixed semantics issued known non-exhaustive-function warnings for
off-program-path operations such as float conversion and opaque sequence
access; none occurs on this program's execution path.

### Loop proof against fixed semantics plus definitional helpers

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec-loop-only.k --definition verification-base-kompiled \
  --spec-module AUDIT-LOOP-ONLY
```

The build exited 0 and the independently isolated loop claim exited 0 with
`#Top`; see
[03c-kompile-proof-base.log](evidence/03c-kompile-proof-base.log) and
[03d-kprove-loop-only.log](evidence/03d-kprove-loop-only.log). The isolated
claim is preserved as [spec-loop-only.k](evidence/spec-loop-only.k).
Crucially, `VERIFICATION-BASE` does not import the later body-summary bridge.

### Public claims

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

The build exited 0; see
[03e-kompile-proof-full.log](evidence/03e-kompile-proof-full.log). Each public
target was then run in its own spec module:

| Claim | Command module | Result |
|---|---|---|
| symbolic `N < 0` | `AUDIT-NEGATIVE-ONLY` | exit 0, `#Top` |
| ground `N = 0` | `AUDIT-ZERO-ONLY` | exit 0, `#Top` |
| symbolic `N >= 1` | `AUDIT-POSITIVE-ONLY` | exit 0, `#Top` |

Exact commands and outputs are in
[03f-kprove-negative-only.log](evidence/03f-kprove-negative-only.log),
[03g-kprove-zero-only.log](evidence/03g-kprove-zero-only.log), and
[03h-kprove-positive-only.log](evidence/03h-kprove-positive-only.log). The
isolated specs are
[spec-negative-only.k](evidence/spec-negative-only.k),
[spec-zero-only.k](evidence/spec-zero-only.k), and
[spec-positive-only.k](evidence/spec-positive-only.k).

As a cross-check, the unmodified original `LOOP-SPEC` and `FULL-SPEC` modules
also each exited 0 with `#Top`; see
[03i-kprove-original-loop-module.log](evidence/03i-kprove-original-loop-module.log)
and
[03j-kprove-original-full-module.log](evidence/03j-kprove-original-full-module.log).

Therefore clean reconstruction succeeds. It establishes closure under the
candidate's theory, not soundness of every added rule.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim says:

- `N >= 0`;
- `1 <= I <= N + 1`;
- before iteration `I`, local `result` is the string `"0 ... I-1"`;
- `i` may contain any integer `J`, because the next iterator yield overwrites
  it;
- executing the remaining range loop, the final `return`, and frame pop yields
  `"0 ... N"`, deletes the callee scope, restores environment 0, and empties
  the one saved frame.

The public claims partition all integer inputs:

- if `N < 0`, calling `string_sequence(N)` returns the empty string;
- if `N = 0`, it returns `sequenceCodes(0)`, namely `"0"`;
- if `N >= 1`, it returns `sequenceCodes(N)`, namely `"0 1 ... N"`.

The postconditions are genuine equalities to concrete/string-summary values;
the result is not a free variable, a tautology, or merely an implication.

### Satisfiable preconditions and ground substitution

[adequacy_witnesses.py](evidence/adequacy_witnesses.py) exhibits:

- negative entry witness `N = -1`, result `""`;
- zero entry witness `N = 0`, result `"0"`;
- positive entry witness `N = 1`, result `"0 1"`;
- loop witness `N = 0, I = 1, J = 7, result = "0"`;
- nontrivial loop witness
  `N = 5, I = 3, J = -99, result = "0 1 2"`.

Every formal precondition evaluates true. The substituted final result agrees
with both trusted canonical Python and candidate Python. The exact command,
inputs, and results are in
[04-precondition-witnesses.log](evidence/04-precondition-witnesses.log).

### Current transcription is exact, but the artifact is not pinned

The `sequenceLoopBody` and `sequenceBody` macros at
`/candidate/verification.k:33-47` are an exact manual transcription of the
current function body in `solution.mpy`. The initial public-claim scope also
contains the correct name, parameter list, body, defining environment, and
builtins parent. The used-construct mapping is recorded in
[05-used-construct-map.md](evidence/05-used-construct-map.md).

However, the entry `<k>` cell starts at `Call(Name("string_sequence"), N)` with
a manually seeded `closureVal`; it does not execute
`#loadAll(Module(FuncDef(...)))` from the submitted `solution.mpy`. Neither
proof `kompile` command nor any `kprove` command names or imports
`solution.mpy`. The translator run in `prove.sh` regenerates that file, but the
proof definition does not consume it.

I tested body sensitivity with
[solution-body-mutant.mpy](evidence/solution-body-mutant.mpy), changing the
material final statement to `Return(Str("MUTATED"))`. In a clean source-only
directory containing that file as `solution.mpy`, I freshly rebuilt
`verification.k` and reran the positive proof. The mutant differed from the
submitted `.mpy` at byte 544, yet the build exited 0 and the proof again exited
0 with `#Top`. Commands and hashes are in
[audit-body-sensitivity.sh](evidence/audit-body-sensitivity.sh) and
[04-body-sensitivity.log](evidence/04-body-sensitivity.log).

Thus the proof is body-insensitive at the artifact boundary. Its manually
restated body happens to equal the current submission, but there is no
machine-checked source/term connection and the `<k>` cell does not execute the
submitted program term. This is a material real-program pinning gap under the
audit requirement.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](evidence/inventory_k.py) inventories every `configuration`,
`syntax`, function/total/functional declaration, context, ordinary rule,
priority rule, simplification rule, concrete rule, opaque symbol declaration,
and macro in:

- `reference-semantics/semantics.k`;
- every helper under `reference-semantics/semantics/*.k`;
- `verification.k`.

The complete 940-entry inventory is
[05-rule-inventory.tsv](evidence/05-rule-inventory.tsv): 230 syntax
declarations (147 function-bearing), 465 equational rules, 239 operational
rules, one configuration, and five contexts. Its reproducibility hash and
counts are in
[05-inventory-command-rerun.log](evidence/05-inventory-command-rerun.log).

The 928 entries preceding `verification.k` are byte-identical trusted supplied
semantics. In this mode they define the selected language semantics rather
than being candidate-authored proof extensions. Every off-program-path entry
is marked as such in the inventory. The used path was manually traced through:

- configuration, module/statement sequencing, scope lookup, and builtins in
  `core.k`;
- strict/sequence-strict expression evaluation in `syntax.k` and
  `operators.k`;
- function frame creation, parameter binding, return, and pop in
  `call.k`/`functions.k`;
- `If`, assignment, `For`, and loop control in `controls.k`;
- range creation and iteration in `builtins.k`/`range.k`;
- integer addition/comparison and string literal/concatenation/conversion in
  `int.k`/`str.k`;
- target binding in `tuple.k`.

The flow preserves left-to-right argument and binary-operand evaluation,
looks up `range` and `str` through the actual environment chain, evaluates the
iterable once, binds each yielded integer before the loop body, updates the
current scope, and restores the call frame on `Return`. The program allocates
no list/dict objects and has no observable heap changes. The selected
semantics uses unbounded K integers and an ASCII string-code model; all
program-produced characters are ASCII digits, minus signs only in off-target
negative conversion paths, and spaces. No unused opaque float, sort, MD5,
subscript, collection, or method symbol can influence these claims.

### Candidate-local declaration/rule decisions

The candidate adds exactly inventory entries `K0929` through `K0940`:

| Entries | Decision |
|---|---|
| `K0929` `sequenceCodes(Int)` `[function, injective]` | The summary is result-bearing. It is injective and well-founded on the used domain `N >= 0`; global behavior on negatives is not justified and is unused by the negative entry claim. |
| `K0930` base equation | `sequenceCodes(0) = "0"` is true. |
| `K0931` `[owise]` recurrence | It agrees with the intended recurrence for `N >= 1`. For negative integers it descends forever and does not define the canonical empty result; this is an over-broad/off-domain termination gap, not the false-conclusion witness used for the verdict. |
| `K0932` guarded simplification recurrence | Same right-hand side as `K0931`; the guard `N >= 1` is correct and overlaps consistently. |
| `K0933` `inRange(I, I+D, 1) => D > 0` | True integer identity under fixed `inRange`. |
| `K0934` `I < I+D => D > 0` | True integer identity. |
| `K0935` inverse `seqConcat` simplification | Exactly the guarded `sequenceCodes(X)` recurrence for `X >= 1`; true. |
| `K0936-K0937` loop macro | Exact syntax of the submitted loop body; definitional and non-operational by itself. |
| `K0938-K0939` function-body macro | Exact syntax of the current submitted function body; definitional and non-operational by itself. |
| `K0940` priority-40 body summary | **Unsound operational bridge.** It replaces program execution over a domain broader than its alleged loop-theorem justification and can prove a false result. |

The function equations have no disagreeing overlap on the used domain. Their
positive recursion decreases to zero. The simplification equations are
ordinary mathematics. The decisive issue is `K0940`.

### Operational-bridge context and state audit

The bridge is:

```text
<k> sequenceBody ~> #endcall
 => Return(str(sequenceCodes(N))) ~> #endcall </k>
<env> 1 </env>
<scopes> ... 1 |-> scope("n" |-> N, parent(0)) ... </scopes>
requires N >= 0
[priority(40)]
```

It reads `N`, replaces the entire function body, and determines the returned
value. It skips the docstring expression, negative branch, assignments,
lookups and calls of `range` and `str`, iterator control, loop-local writes,
and all nested call/control effects those resolved bindings might have. Its
priority preempts fixed execution.

The separately proved loop claim is not a universal connection theorem for
this bridge. Its precondition pins a complete three-scope map with the real
`string_sequence` closure and `builtinsScope`, an exact frame stack
`frame(.K, 0, 1)`, `scopeLoc = 2`, and the loop-head state after
initialization. The bridge instead:

- matches before initialization;
- permits arbitrary other scopes;
- does not constrain the module-scope bindings reached through `parent(0)`;
- omits stack, heap, return, exception, allocation, and scope-location cells.

Therefore the bridge's match domain is not contained in the loop theorem's
justification domain. No bridge-free auxiliary claim proves the omitted
prefix or the complete operational match domain.

### Concrete false-conclusion witness

I used the intended integer input `n = 1` and a bridge-matching state in which
module scope 0 legally shadows `range` with a two-argument closure returning
`rangeObj(0, 0, 1)`. Scope 1 still contains exactly `"n" |-> 1` with
`parent(0)`, so `K0940` matches.

Under fixed `VERIFICATION-BASE`, real lookup selects the shadow closure, the
loop is empty, and the function returns `"0"`:

```text
kprove spec-shadow-base-correct.k \
  --definition verification-base-kompiled \
  --spec-module AUDIT-SHADOW-BASE-CORRECT
```

This exited 0 with `#Top`; see
[spec-shadow-base-correct.k](evidence/spec-shadow-base-correct.k) and
[05a-shadow-base-correct.log](evidence/05a-shadow-base-correct.log).

Under bridge-enabled `VERIFICATION`, the same starting state proves the false
result `"0 1"`:

```text
kprove spec-shadow-bridge-wrong.k \
  --definition verification-kompiled \
  --spec-module AUDIT-SHADOW-BRIDGE-WRONG
```

This also exited 0 with `#Top`; see
[spec-shadow-bridge-wrong.k](evidence/spec-shadow-bridge-wrong.k) and
[05b-shadow-bridge-wrong.log](evidence/05b-shadow-bridge-wrong.log).

The complementary checks discriminate the two semantics:

- fixed semantics demanding `"0 1"` exits 1 with
  `WarnStuckClaimState`, leaving actual `"0"`:
  [05c-shadow-base-wrong-rejected.log](evidence/05c-shadow-base-wrong-rejected.log);
- bridge semantics demanding `"0"` exits 1 with
  `WarnStuckClaimState`, leaving bridge result `"0 1"`:
  [05d-shadow-bridge-correct-rejected.log](evidence/05d-shadow-bridge-correct-rejected.log).

This is a concrete false conclusion enabled by the candidate rule for an
integer in the intended input domain. The submitted entry state's module
scope happens not to shadow `range`, which explains why the target result is
empirically and mathematically correct. That does not validate a globally
false proof rule or supply the required universal connection theorem.

## 6. Fresh non-vacuity test

There is no candidate `spec-vacuity.k`; none was trusted. I created
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), preserving the positive
entry precondition `N >= 1` but changing the result obligation from
`sequenceCodes(N)` to the deliberately false `sequenceCodes(N + 1)`.

The satisfying witness `N = 1` makes the error concrete:

```text
actual/valid result: "0 1"
mutated obligation:  "0 1 2"
```

First:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited 0, proving that the mutation parsed and built; see
[06a-vacuity-dry-run.log](evidence/06a-vacuity-dry-run.log). The actual proof
command without `--dry-run` exited 1 with `WarnStuckClaimState`. Its residual
says the destination unifies but the implication between the actual
`sequenceCodes(N)` result and the extra `N+1` suffix fails; see
[06b-vacuity-proof-expected-failure.log](evidence/06b-vacuity-proof-expected-failure.log).

This is valid non-vacuity evidence. It confirms that the public claim constrains
the result; it does not establish the bridge's operational soundness.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

The independent `VERIFICATION-BASE` loop run establishes, under the fixed
supplied MPY semantics plus the reviewed mathematical `sequenceCodes`
simplifications, the partial-correctness loop invariant for every
`N >= 0` and `1 <= I <= N+1`.

The public `VERIFICATION` runs establish only this conditional statement:

> In the candidate-extended K theory, a manually seeded closure whose body is
> the `sequenceBody` macro returns the specified string for negative, zero, and
> positive K integers.

For negative values the fixed body executes normally. For nonnegative values,
the public proof depends on the priority-40 body bridge. Because that bridge is
not a consequence of fixed semantics on its complete match domain, `#Top`
cannot be promoted to a sound theorem about real execution.

All K results are partial-correctness results. They do not separately prove
termination, Python resource behavior, or equivalence outside the modeled
subset.

### Trust ledger

| Boundary | Value/control influence | Assessment |
|---|---|---|
| Byte-identical `/reference/reference-semantics` | Defines all execution, cells, calls, and values | Acceptable mandated fixed-semantics boundary in `SUPPLIED_SEMANTICS` mode. |
| K integer/string hooks, notably `Int2String`, `ordChar`, `substrString`, integer arithmetic | Determines decimal codes and ASCII literals | Acceptable selected-semantics primitives; used outputs are ASCII and concrete checks agree. |
| Candidate `sequenceCodes` equations and simplifications | Determines the positive postcondition and loop invariant | Sound and terminating on the used nonnegative domain; negative global behavior is incomplete but not used for the negative claim. |
| Machine-checked `LOOP-SPEC` circularity | Summarizes the real remaining loop from an exact loop-head state | Acceptable: proved at `#Top` without importing the body bridge. |
| `verification.k:59-66` body summary | Replaces all nonnegative body execution and fixes the final result | Illegitimate: no complete bridge-free connection theorem; false-result witness exists. |
| Manual `sequenceBody`/`sequenceLoopBody` transcription | Selects the program body actually present in the theorem | Currently textually exact, but not artifact-pinned; a body mutant leaves the proof unchanged. |
| Differential Python testing (115 cases) | Supports implementation/canonical intent bridge | Useful finite evidence only; not a K theorem or universal source/proof connection. |
| Concrete MPY assertions at `0, 5, 10` | Supports the selected semantics on examples | Finite smoke evidence only. |
| Unused opaque float, sort, MD5, and totalized collection/subscript symbols in supplied semantics | None on this program path | Irrelevant to these claims; inventoried but unreachable. |
| Missing generation metadata/logs/trace | Provenance auditability | Concerning omission, but not the basis of the legitimacy failure. |

### Gate accounting and decision

- Clean reconstruction: **PASS**.
- Program/canonical differential fidelity: **PASS** on the recorded finite
  scope.
- Result constraint and fresh non-vacuity: **PASS**.
- Gate A real-program soundness: **FAIL** because `K0940` is a false
  operational bridge with no complete connection theorem.
- Real submitted-program pinning: **FAIL** because the proof does not consume
  `solution.mpy` and is body-insensitive at that boundary.
- Intent adequacy of the actual Python implementation: **PASS** for integer
  inputs, but it cannot rescue the invalid proof theory.

The actual program appears correct, and the intended target theorem is true.
The candidate has not supplied a legitimate K proof of it.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
