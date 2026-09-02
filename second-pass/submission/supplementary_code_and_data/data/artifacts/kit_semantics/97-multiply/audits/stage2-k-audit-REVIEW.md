# Independent adversarial review: 97-multiply

## Overall finding

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full HumanEval integer domain. The proof was reconstructed
from source with K 7.1.293, the only positive target claim independently
printed `#Top` and exited 0, the formal result is constrained, and two fresh
reviewer-authored negative probes were rejected for the expected semantic
reasons. `verification.k` contributes no proof-local rule, equation, lemma,
summary, oracle, or operational bridge.

The submitted Python implementation is extensionally equal to the trusted
canonical implementation for all integer arguments: Python remainder by the
positive divisor 10 is already in `0..9`, so the canonical `abs(a % 10) *
abs(b % 10)` equals the candidate `(a % 10) * (b % 10)`. There is no
candidate-caused domain restriction, supplied-model representation gap, or
canonical/docstring contradiction requiring either campaign-amendment
exception.

## 1. Input and provenance integrity

The launcher record [audit-input.json](/audit-input.json) is a regular,
readable file declaring `pipeline-v3`, problem `97-multiply`, condition
`kit-semantics`, and `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, as this mode requires.

The campaign object in [audit-campaign-lock.json](/audit-campaign-lock.json) is
JSON-identical to the campaign block in `audit-input.json`; its independently
computed SHA-256 is the recorded
`e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`.
The run, task, generation-result, invocation, metrics, runtime-metrics, usage,
generation prompt, output, last-message, and trace records are all present as
real regular files/directories. Their file hashes match the launcher record and
the hashes nested in `generation-result.json`.

The structured trace has one JSONL file and 182 valid JSON events. The
event-by-event index includes every tool call, tool output, patch, message, and
terminal event; it is preserved in
[stage1-trace-index.log](evidence/stage1-trace-index.log). The generation
records were treated only as untrusted history. Their prior `#Top`, claimed
`VALIDATED` status, and negative probes were not used in place of reconstruction.

Independent tree and leaf checks established:

- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts and have their recorded SHA-256 hashes.
- Both supplied-semantics trees have 25 entries, contain no symlink or
  unsupported entry, have identical types and bytes at every relative path,
  and reproduce the pipeline tree-manifest digest
  `e017e7ddcdccc327e74147cf909748f8d5f3a5af556133d79bb556c08f867cb0`.
  The launcher-recorded candidate and trusted content digests are also equal
  (`630509e5...`).
- The mounted candidate reproduces the generation workspace tree digest
  `545c57965af135a2cb4855762f5887a73da6b9dfb931f9e3286d880e23aeeed0`.
  The trace tree reproduces the usage record's source-trace digest
  `22a8ca91453a7f06218fcc3508cf43b9c26f3ad76265345a00c57b335d68cc94`,
  and its JSONL leaf hash matches `generation-result.json`.
- All six required proof deliverables are real regular files. Candidate
  compiled definitions and caches were present but were never copied or used.

Full evidence is in [stage1-integrity.log](evidence/stage1-integrity.log),
[stage1-launcher-records.log](evidence/stage1-launcher-records.log), and
[stage1-generation-records.log](evidence/stage1-generation-records.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `multiply(a, b)` to accept two valid integers and
return the product of their unit digits. Its four examples include positive,
zero-ending, and negative-second-argument cases. The trusted canonical entry
point returns:

```python
abs(a % 10) * abs(b % 10)
```

The candidate returns:

```python
(a % 10) * (b % 10)
```

For every Python integer `x`, `x % 10` is one of `0..9`; therefore `abs` is
an identity here. This establishes implementation fidelity by ordinary integer
semantics, including negative and unbounded-size Python integers.

Running the trusted translator directly on the candidate source produced
`solution.regenerated.mpy` with SHA-256
`acc1e5b3a83d1a9c32d2af4ce43d0207cdf2905d427280a3f57b0ffb639f1e7d`,
byte-identical to submitted `solution.mpy`. The exact command and exit-0
comparison are in
[stage2-regeneration.log](evidence/stage2-regeneration.log).

The independent differential test imports the trusted canonical and candidate
entry points separately. It covers:

- all four documented examples;
- zero, sign, and values immediately around multiples of ten;
- the complete `[-21,21] x [-21,21]` residue cross-product;
- values around `+/-10**1000`; and
- 1,000 deterministic random pairs below `10**150` in magnitude.

There is no meaningful “empty” input for two integer parameters and the
implementation has no source-level branch. All 3,196 test pairs matched,
including value types, with input-set digest
`390b3a27285bc1042bd4a58f9254d330bbf93f04a9dd90e29bd9e7463b6f8614`.
See [differential_test.py](evidence/differential_test.py) and
[stage2-differential.log](evidence/stage2-differential.log). This finite test
supports the bridge; the universal result does not rest on testing.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/reconstruction`. The
semantics copy came from the trusted reference mount. No candidate-built
definition, executable, KORE file, cache, or timestamp was copied.

The observed toolchain is K 7.1.293 and Python 3.10.12
([stage3-tools.log](evidence/stage3-tools.log)). Fresh commands and results:

| Command | Result | Evidence |
|---|---:|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 | [stage3-llvm-build.log](evidence/stage3-llvm-build.log) |
| `python3 k_concrete_probes.py` | exit 0 | [stage3-python-concrete.log](evidence/stage3-python-concrete.log) |
| `krun k_concrete_probes.mpy --definition runtime-kompiled` | exit 0, `.K`, `NoExc`, exit code 0 | [stage3-k-concrete.log](evidence/stage3-k-concrete.log) |
| `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 | [stage3-haskell-build.log](evidence/stage3-haskell-build.log) |
| `kprove spec.k --definition verification-kompiled --spec-module SPEC` | exit 0, `#Top` | [stage3-positive-proof.log](evidence/stage3-positive-proof.log) |

The concrete probe source is reviewer-authored and was translated with the
trusted translator. It checks the four examples plus zero, negative,
multiple-of-ten, and large-integer boundaries under both CPython and K.
Compiler warnings concern unused variables and non-exhaustive helpers for
unrelated strings, floats, maps, and slicing; none is on this program's
integer-only path.

There is exactly one positive target claim: `SPEC.multiply-correct`. No helper,
loop, or auxiliary positive claim was omitted from reconstruction.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim quantifies `A` and `B` over all K `Int` values. Its realizable initial
state has:

- `<k>` equal to a call of `multiply` on `Int(A)` and `Int(B)`;
- current environment location 0;
- scope 0 binding `"multiply"` to a two-argument closure with lexical
  environment 0 and the exact submitted return body;
- the fixed builtins scope at location -1;
- next scope location 1, empty heap and call stack, heap counter 0, `noRet`,
  `NoExc`, and exit code 0.

There is no `requires` clause, sign restriction, magnitude bound, finite
enumeration, or bounded unrolling. The postcondition requires `<k>` to be
exactly `pyMod(A, 10) *Int pyMod(B, 10)`. Every other displayed cell must
return to the same value; the result is not a free variable, tautology, opaque
summary, or implication antecedent.

### Mechanical program identity

The claim does not begin by loading the complete module, which is permitted
only because the exact binding/body equivalence is demonstrated:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. a reviewer parser reconstructs the regenerated `Module(FuncDef(...))`
   constructor tree;
3. it parses the `closureVal` in `spec.k` and proves equality of the function
   name, `(a,b)` parameters, lexical anchor, and full `Return(BinOp(...))`
   body; and
4. a fresh `krun solution.mpy` shows module loading produces exactly that
   closure binding in scope 0, with lexical environment 0.

The mechanical comparison is in
[program_pinning.py](evidence/program_pinning.py) and
[stage4-program-pinning.log](evidence/stage4-program-pinning.log). The fixed
semantics module-load result is in
[stage4-k-module-binding.log](evidence/stage4-k-module-binding.log).
This is constructor-level identity, not a substring-only assertion.

Six concrete satisfying substitutions—including `(148,412)`, negative
arguments, zero, and 250-digit integers—make the claimed expression equal to
both Python implementations; see
[stage4-ground-substitution.log](evidence/stage4-ground-substitution.log).
For example, `A=148, B=412` satisfies the exact entry configuration and all
three results are 16.

The body is execution-sensitive. A fresh mutation changes the first modulus
divisor in the closure from 10 to 9 while retaining the required result 16 at
`(148,412)`. The prover executes the changed body to 8 and rejects the claim.
Thus changing the executed program term, rather than merely changing an
external source file, changes the theorem outcome.

## 5. Rule-by-rule static soundness review

The exhaustive machine-readable inventory is
[stage5-rule-inventory.json](evidence/stage5-rule-inventory.json), with
summary and digest in
[stage5-inventory-summary.log](evidence/stage5-inventory-summary.log). It
covers all 26 applicable source files: the supplied assembly and helper files,
`verification.k`, and `spec.k`.

Inventory totals are 982 sentences: 241 syntax declarations, 734 ordinary
rules, five contexts, one configuration, and one claim. Attribute accounting
finds 171 `function`, 123 `total`, zero `functional`, 47 priority-bearing,
24 opaque `no-evaluators` declaration sentences (26 opaque symbol
occurrences), and zero simplification/simplifier sentences. Each inventory
record includes file/line span, normalized text and hash, attributes,
target-slice role, and a static decision. The 690 unused fixed-model rules and
191 unused declarations are accepted relative to the supplied subset; none has
a target dependency or an identified false-conclusion witness.

Every constructor used by `solution.mpy` or the entry call maps as follows:

| Construct | Declaration and material rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `syntax.k`; `core.k` module load/sequencing; `functions.k` exact closure creation |
| `Call`, argument list | `call.k` callee routing; `core.k` left-to-right `#evalArgs`; `call.k` closure-frame rule |
| `Name` | `core.k` exact scope lookup and guarded parent walk |
| `Int` | `syntax.k`; `core.k` literal rule |
| `Return` | strict syntax; `functions.k` return, `#pop`, and restoration rules |
| `BinOp("%",...)`, `BinOp("*",...)` | `seqstrict(2,3)` syntax; `operators.k` dispatch; `int.k` `%`, `*`, and `pyMod` rules |

On the actual path, call evaluation first resolves the exact scope-0
`"multiply"` binding, evaluates arguments left-to-right, allocates a scope-1
call frame, binds `a` then `b`, evaluates the return expression
left-to-right, computes each fixed-divisor remainder, multiplies the integer
results, and pops the frame while restoring all constrained cells. The plain
parameter-binding and name-lookup rules are selected because the fresh frame
has no `"$cells"` marker. No heap allocation or mutation occurs.

The only result-bearing mathematical chain is:

```text
BinOp("%", Int, Int(10))
  -> applyBin("%", ...)
  -> pyMod(..., 10)
  -> ((I %Int 10) +Int 10) %Int 10
```

followed by ordinary `*Int`. For positive divisor 10 this is Python's floored
remainder in `0..9`, including negative dividends. `pyMod` is defined by an
ordinary fixed-semantics rule; it is neither opaque nor proof-local.

Overlap, priority, totality, and control findings:

- `verification.k` merely imports `MPY`; it defines no local syntax, function,
  totality assertion, lemma, priority rule, rewrite, or bridge.
- The generic call rule is `[owise]`, but no more-specific fixed rule matches
  a call whose callee is the scope-bound closure `multiply`.
- The priority-40 cell/ref rules cannot match the target's concrete plain
  frame and integer values. None of the 47 priority rules affects the proof
  path.
- Function/total equations used on the path are constructor-complete for their
  actual inputs and descend structurally. There are no conflicting equations
  or guard overlaps with disagreeing right-hand sides on the path.
- The 24 opaque declaration sentences cover MD5, floats, and sorting. No
  opaque symbol occurs in the program, initial state, execution path,
  postcondition, or proof residual. `MPY-CONCRETE` rules are used only by the
  LLVM test module and are not imported by the Haskell proof's `MPY` module.
- Return's abrupt control rule is the fixed language rule and matches the
  active function frame; the fresh body mutation confirms the displaced
  computation is actually executed. There is no proof-added control shortcut.

No rule encodes the task answer, bypasses the body, fabricates a used result,
or introduces an unconstrained result-bearing oracle. I found no unsound rule
and therefore have no false-conclusion witness to report.

## 6. Fresh non-vacuity test

The reviewer-authored
[spec-audit-false.k](evidence/spec-audit-false.k) keeps the real body and exact
initial state but requires 73 for the satisfying input `(19,28)`, whose real
result is 72.

First,

```text
kprove spec-audit-false.k --definition verification-kompiled \
  --spec-module SPEC-AUDIT-FALSE --dry-run
```

exited 0, establishing successful parsing and claim construction. The same
command without `--dry-run` exited 1 with `WarnStuckClaimState`; the residual
contains `<k> 72 ~> .K </k>`, which cannot unify with 73. This is the expected
unmet result obligation, not a parser error, timeout, unrelated crash, or
unreachable mutation. Exact logs are
[stage6-false-dry-run.log](evidence/stage6-false-dry-run.log) and
[stage6-false-proof.log](evidence/stage6-false-proof.log).

Separately, reviewer-authored
[spec-audit-body-sensitivity.k](evidence/spec-audit-body-sensitivity.k)
changes the executed closure body (`a % 10` to `a % 9`) and keeps the old
required result. Its dry run exits 0; its proof exits 1 with the executed value
8 visible against required 16. See
[stage6-body-dry-run.log](evidence/stage6-body-dry-run.log) and
[stage6-body-proof.log](evidence/stage6-body-proof.log).

The proof is both result-discriminating and body-sensitive.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following conditional
statement: under the supplied MPY semantics and K's builtin theories, from the
exact claim state and for arbitrary K integers `A,B`, executing the exact
submitted `multiply` closure reaches the result
`pyMod(A,10) *Int pyMod(B,10)` while restoring the displayed environment,
scope, heap, counters, stack, return, exception, and exit-code cells. This is a
partial-correctness result; it is not presented as a separate resource or
total-correctness theorem.

Trust ledger:

| Boundary | Effect and dependents | Assessment and evidence |
|---|---|---|
| Supplied reference semantics | Defines parsing, binding, call/return control, state cells, `%`, and `*` | Acceptable fixed campaign boundary; byte-identical tree, target-slice static audit, clean LLVM/Haskell reconstruction |
| K 7.1.293 frontend, Haskell/LLVM backends, and builtin `Int`/Map/List theories | Checks compilation, symbolic execution, integer arithmetic, and state matching | Necessary low-level trust; independently rebuilt, positive `#Top`, two meaningful rejected mutations |
| Trusted `py2mpy.py` | Connects `solution.py` to the submitted constructor term | Acceptable trusted input; byte-identical regeneration plus independent constructor parser |
| Constructor-binding equivalence | Permits the claim to start with the loaded closure rather than the full module | Mechanically demonstrated and concretely reproduced by clean `krun solution.mpy` |
| MPY integer subset versus CPython | Connects K `pyMod`/`*Int` and call mechanics to the HumanEval meaning | Direct rule inspection and ordinary modulo mathematics; 3,196-pair canonical differential plus K boundary probes provide finite support |
| HumanEval canonical implementation | Supplies benchmark ground truth | Candidate is universally equivalent on integers because canonical `abs` is redundant after `% 10` |

No program-derived value is opaque. No trusted primitive, empirical bridge, or
informal claim determines the returned value inside the proof. The fixed
semantics' unrelated opaque float/sort/MD5 symbols are outside the theorem's
value, control, state, and termination dependencies. There is no documented or
undocumented model representation gap for arbitrary Python integers: both
CPython and the K model represent unbounded integers used by this task.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and reproducible evidence) all pass. The benchmark decision is therefore
`PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
