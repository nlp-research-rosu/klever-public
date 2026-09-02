# Independent adversarial audit: 163-generate-integers

## Audit result

The submitted reachability proof is legitimate. A fresh Haskell definition
compiled from the recursively verified supplied semantics and candidate source,
and the sole target claim exited 0 with `#Top`. The claim executes an AST that
is KORE-identical to the submitted `solution.mpy`, constrains the returned heap
object to the intended digit sequence, and rejects a fresh false-result
mutation.

I select `CONCERNS / LEGIT`, not `PASS`, for two non-soundness limitations:
the candidate lacks all four requested provenance records and a structured
generation trace, and the final bridge from the formal `evenDigits` definition
to the natural-language/canonical intent remains an independently reviewed and
finitely tested bridge rather than a second universal K theorem. Neither
limitation makes a false conclusion provable or weakens the reconstructed
reachability result.

The audit used the required `using-kit` then `validating-proof` workflows. It
did not use `writing-semantics`, because the rendered mode is
`SUPPLIED_SEMANTICS`. Everything from `/candidate` was treated only as
untrusted evidence and copied to `/tmp/audit-work/submitted`; candidate caches
and compiled definitions were not used.

## 1. Input and provenance integrity

### Mode boundary

The trusted mount agrees with the rendered mode:
`/reference/reference-semantics` exists. There is no infrastructure breach.

The candidate `reference-semantics/` tree and trusted tree have identical path
and type inventories, no symlinks, no missing or additional entries, and a
recursive byte comparison exits 0. Candidate `prompt.py` and `py2mpy.py` are
also byte-identical to the trusted copies. Exact commands, SHA-256 hashes,
tree/type checks, and exit statuses are in
[`01_integrity.sh`](evidence/01_integrity.sh) and
[`01_integrity.log`](evidence/01_integrity.log).

### Missing and extra artifacts

The following requested provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any discoverable structured generation trace (`*trace*`, `*.jsonl`, or
  `*.json` within two levels)

No claim from those missing records was needed or reconstructed by assumption.
The candidate also contains `__pycache__/solution.cpython-310.pyc`; this is a
candidate-built cache, was ignored, and was not copied into the proof source
set. No candidate `PROOF.md` is present.

The proof sources needed for reconstruction are regular files:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prove.sh`, and the
complete supplied-semantics tree. The candidate also supplies concrete test
files, but the audit did not rely on them as its independent behavioral oracle.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two positive integer endpoints `a` and `b`, return, in ascending order,
every even decimal digit in the inclusive interval between them. Thus the only
possible elements are `2`, `4`, `6`, and `8`; endpoint order is irrelevant.
Examples are `(2,8) -> [2,4,6,8]`, `(8,2) -> [2,4,6,8]`, and
`(10,14) -> []`.

This is the contract in trusted `/reference/prompt.py`. Trusted
`/reference/canonical.py` clamps the interval to `[2,8]` and filters the range
for even integers.

### Source inspection

Candidate `solution.py` initializes an empty list, checks each of the four
digits in ascending order with

`(a <= D <= b) or (b <= D <= a)`,

appends exactly those satisfying the inclusive test, and returns the list.
This is equivalent to the canonical implementation over the intended positive
integer domain. It is a straight-line implementation rather than the
canonical comprehension, which is permitted.

### Translator and differential evidence

The trusted translator regenerated `solution.mpy` from the scratch copy of
`solution.py`; `cmp` exited 0 and both files have SHA-256
`dafb407d62efa4ca95522f0d622eef6ac8fc1f185dc7768678e93dd9a6a6d792`.

The reviewer-authored differential test imports the scratch copies of trusted
canonical and candidate entry points. It covers:

- 22 named examples, empty-result cases, exact digit points, both endpoint
  orders, all immediate threshold neighbors, and large positive values;
- the exhaustive positive grid `1..64 × 1..64`; and
- 500 seeded positive pairs in `1..1,000,000`.

All 4,618 cases matched. The independent script, complete generated input list,
commands, and result are:

- [`02_differential.py`](evidence/02_differential.py)
- [`02_differential_inputs.json`](evidence/02_differential_inputs.json)
- [`02_fidelity.sh`](evidence/02_fidelity.sh)
- [`02_fidelity.log`](evidence/02_fidelity.log)

This is finite evidence for the Python-to-intent bridge, not a substitute for
the K proof.

## 3. Clean proof reconstruction

### Fresh definitions

K version 7.1.337 was available at `/usr/bin`. From source in the scratch copy,
the audit ran:

```text
kompile .../reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition .../runtime-kompiled

kompile .../verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition .../verification-kompiled
```

Both exited 0. No candidate-built definition or cache was present in, copied
to, or used by these commands.

The compilers emitted unused-variable warnings in the supplied `str.k`.
The LLVM build additionally warned that total `valSeqAt` has no `.ValSeq`
equation. The submitted program has no strings or subscripts; neither warning
lies on the target execution path or contributes to closure.

### Independent concrete execution

The reviewer concrete driver has a byte-identical 367-byte function body
followed by independent assertions for documented examples, empty cases, and
each digit boundary. Translation with the trusted translator and execution
under the fresh LLVM definition exited 0 with:

- empty `<k>`;
- empty stack;
- `NoExc`;
- exit code `0`; and
- heap values corresponding to all asserted results.

The source is [`03_concrete_audit.py`](evidence/03_concrete_audit.py).

### Every positive target claim

Static enumeration found exactly one `claim`, in `spec.k`, and no helper claim
in `verification.k`. Independently running it with the fresh Haskell definition:

```text
kprove .../spec.k \
  --definition .../verification-kompiled \
  --spec-module SPEC --smt-timeout 10000
```

printed `#Top` and exited 0. Full build, concrete, claim-enumeration, and proof
commands with statuses and bounded output are in
[`03_build_and_prove.sh`](evidence/03_build_and_prove.sh) and
[`03_build_and_prove.log`](evidence/03_build_and_prove.log).

## 4. Adequacy and real-program pinning

### Entry claim in plain language

Precondition:

- `A` and `B` are K mathematical integers with `A > 0` and `B > 0`;
- execution starts with the exact solution module followed by a call to
  `generate_integers(A,B)`;
- the current environment is the empty module scope 0 with the supplied
  builtins scope at `-1`;
- heap and frame stack are empty, allocator locations start at 0/1 as shown,
  no return or exception is pending, and exit code is 0.

Postcondition:

- execution has completed and returned `ref(0)`;
- module scope 0 contains the exact generated function closure;
- heap location 0 contains `list(evenDigits(A,B))`;
- exactly one heap location was allocated, the transient call scope was
  removed, the stack is empty, no return state or exception remains, and exit
  code is 0.

The heap assertion makes the result constraining: `ref(0)` is not free, and
`evenDigits` is a total, fully equated sequence. The claim is not an implication
with an unconstrained converse or a tautology.

### Exact submitted program

The claim uses the macro `solutionModule`, so the audit parsed both:

1. the submitted scratch `solution.mpy`; and
2. the reviewer term `solutionModule`

as sort `Module` in module `VERIFICATION`, expanded macros, emitted KORE, and
required byte equality. `cmp` exited 0. Thus the module executed in `<k>` is
exactly the submitted translated AST, not a substituted implementation.

The exact check and its successful rerun are in
[`04_adequacy.sh`](evidence/04_adequacy.sh) and
[`04_adequacy.log`](evidence/04_adequacy.log). The first reviewer attempt,
preserved in [`04_adequacy_attempt1.log`](evidence/04_adequacy_attempt1.log),
omitted `--module VERIFICATION --expand-macros` and therefore could not parse
the macro token; that was a reviewer command error, not candidate evidence.

### Satisfying ground state

Set `A=3`, `B=7` in the complete entry configuration. Both are positive, so
this concrete state satisfies the sole entry precondition. The formal expected
sequence reduces to `[4,6]`. A separate ground claim with that exact heap value
printed `#Top` and exited 0. Trusted canonical Python and candidate Python both
returned `[4,6]`.

The ground claim and run are
[`04_ground_spec.k`](evidence/04_ground_spec.k) and
[`04_adequacy.log`](evidence/04_adequacy.log).

There are no loops and no helper reachability claims. The straight-line four
branch structure in the proof macro is the real control flow.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The lexical inventory covers all K source in the verified supplied tree,
`verification.k`, and `spec.k`. It contains 942 complete declaration blocks:

- 702 `rule` blocks;
- 233 `syntax` blocks;
- 5 `context` blocks;
- 1 configuration; and
- 1 claim.

It also identifies 148 function-bearing declaration blocks, 110 `total`
blocks, zero `functional` blocks, 45 priority rules, 26 `owise` rules, 35
`concrete` blocks, 22 `no-evaluators` blocks, seven macros, one recursive
macro, and zero simplification declarations.

Every inventory row includes source/line, normalized full declaration, markers,
theorem-path relevance, and a decision. The generator, summary log, and complete
333 KB table are:

- [`05_inventory.py`](evidence/05_inventory.py)
- [`05_inventory.log`](evidence/05_inventory.log)
- [`05_rule_inventory.md`](evidence/05_rule_inventory.md)

The supplied-semantics entries are byte-identical to the trusted selected
semantics. They are therefore assessed at that fixed semantics level, not
silently treated as candidate proof extensions. Used-path entries received an
additional manual Python-behavior check. Unused-path entries cannot contribute
to this claim’s closure. No supplied or proof-local rule is labeled unsound in
this audit, so no false-conclusion witness is asserted.

### Construct and state mapping

The submitted AST uses only module/function loading, integer/name expressions,
empty list allocation, assignment, integer `<=`, Boolean `and/or`, `if`,
attribute/call for `append`, expression-statement discard, and return. The
reviewed rule path preserves:

- left-to-right expression and argument evaluation;
- local binding of `a`, `b`, and `result`;
- one fresh heap allocation at location 0;
- four conditional in-place list appends in ascending digit order;
- call frame push/pop and abrupt return behavior;
- module closure persistence and transient-scope deletion; and
- every cell in the supplied configuration.

The detailed declaration/rule map is
[`05_used_construct_map.md`](evidence/05_used_construct_map.md).

### Candidate proof-local inventory

`verification.k` adds exactly:

1. three macros, `generateIntegersBody`, `solutionModule`, and
   `generateIntegersClosure`;
2. total `betweenEndpoints(A,B,D)` with one unconditional inclusive-endpoint
   Boolean equation;
3. total `keepDigit(B,D,REST)` with disjoint, exhaustive `true` and `false`
   equations; and
4. total `evenDigits(A,B)` with one finite equation nesting digits
   `2,4,6,8`.

The macros were independently tied to the exact submitted AST. The three
functions occur on the expected-result side and do not replace, intercept, or
accelerate program execution. Their equations are terminating, exhaustive,
non-overlapping, and ordinary integer/sequence mathematics.

There is no proof-local priority, simplification, `concrete`, `owise`, opaque
symbol, helper claim, or operational bridge. In particular there is no rule of
the forbidden form “execute generate_integers by returning evenDigits”; the
fixed semantics executes every source statement.

### Fixed-semantics opaque and trust boundaries

For completeness, the full supplied definition contains unused symbolic
boundaries:

- sorting: `sortVS`, `sortKeyVS`;
- digest: `md5hexCodes`; and
- float/conversion operations: `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
  `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
  `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`.

They are declared with `symbol` and/or have only concrete evaluators. None can
occur in this integer/list/branch program, its formal expected value, or its
proof path. Likewise, unused rules for strings, sets, tuples, dictionaries,
comprehensions, slicing, loops, imports, sorting, and assertions do not affect
the theorem. Their presence does not smuggle this task’s answer.

## 6. Fresh non-vacuity test

The reviewer mutation changes the result-bearing heap obligation from

`list(evenDigits(A,B))`

to

`list(vCons(2, evenDigits(A,B)))`.

This demands one spurious leading `2`. It is false, for example, at the
satisfying input `(3,7)`: both Python implementations return `[4,6]`, while the
mutated destination is `[2,4,6]`.

The mutation first passed `kprove --dry-run` with exit 0, establishing that it
parses and builds against the fresh definition. The actual proof then exited 1
with `WarnStuckClaimState` and the expected non-unification/unmet destination,
not a parser error, missing import, timeout, or unrelated crash. The residual
shows a reachable completed configuration with heap `0 |-> list(.ValSeq)` on
one positive branch, which cannot match the extra-leading-2 destination.

The mutation, command, raw bounded residual, exact exit statuses, and witness
are:

- [`06_spec_vacuity.k`](evidence/06_spec_vacuity.k)
- [`06_nonvacuity.sh`](evidence/06_nonvacuity.sh)
- [`06_nonvacuity.log`](evidence/06_nonvacuity.log)

This is positive evidence that the successful original claim is result
constraining and discriminating.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the exact supplied K semantics, for arbitrary mathematical integers
`A,B > 0`, execution from the complete entry state of the exact submitted
`solution.mpy` AST reaches the claimed completed state: it returns heap
reference 0, whose value is precisely the ascending sequence consisting of
each of `2,4,6,8` whose value lies inclusively between the endpoints. The proof
also constrains allocation counters, module binding, frame cleanup, stack,
return state, exception state, and exit code.

This is a reachability/partial-correctness theorem. It is not a theorem about
inputs outside the positive-integer precondition, not a proof of the whole
supplied Python subset, and not a universal proof that the trusted translator
implements every Python construct correctly.

### Assumptions and boundaries

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.337 parser, compiler, Haskell backend, rewrite engine, and SMT reasoning | Machine closure of the target and ground claims; mutation rejection | Standard unavoidable proof-tool trust boundary; exact version and outputs recorded |
| K built-in `INT`, `BOOL`, `MAP`, `LIST`, `STRING`, and K equality operations | Integer comparisons/logic, scopes/heap, stack, string binding names | Acceptable low-level mathematical/runtime primitives; used operations are ordinary and directly traced |
| Trusted supplied-semantics tree | Meaning of the submitted MPY AST and configuration | Required by `SUPPLIED_SEMANTICS`; candidate copy is recursively identical; used fragment manually reviewed |
| Trusted `/reference/py2mpy.py` | Bridge from `solution.py` to submitted `solution.mpy` | Acceptable condition-provided translator; regenerated bytes are identical |
| Macro-to-submitted-AST equality | Real-program pinning | Machine checked by independent parsing, macro expansion, KORE output, and byte comparison |
| `betweenEndpoints`/`keepDigit`/`evenDigits` equations | Formal expected result | Not assumed: exhaustively equated, terminating, disjoint/covered, and reviewed as ordinary mathematics |
| Natural-language and canonical interpretation | Statement that formal `evenDigits` is the requested HumanEval result | Informal source review plus 4,618-case independent differential evidence; finite evidence, hence the reported concern |
| Definition-wide opaque sort/float/digest symbols listed above | Unrelated supplied-language features | Acceptable here because syntactically and operationally unreachable; no target result/control/state depends on them |
| Missing generation records/trace | Historical provenance only | Auditability concern; no proof step or conclusion depends on their contents |

No empirical oracle, opaque symbol, fresh value, or informal result summary is
used inside claim closure. Differential testing supports only the
implementation-to-intent bridge. It is not presented as a replacement for the
successful reachability proof.

## Evidence index

All reviewer-authored scripts, mutations, inputs, and bounded command logs are
under `/audit-output/evidence/`. All build products and transient generated
files are under `/tmp/audit-work/submitted/`. Nothing under `/candidate` was
modified.

The central proof facts are:

- supplied-semantics integrity: exit 0;
- trusted translation byte identity: exit 0;
- independent differential: 4,618 cases, 0 mismatches;
- fresh LLVM and Haskell builds: exit 0;
- independent concrete K execution: exit 0, `NoExc`, exit code 0;
- sole target claim: exit 0 and `#Top`;
- exact macro/submitted-module KORE identity: exit 0;
- satisfying ground claim `(3,7)`: exit 0 and `#Top`; and
- false-result mutation: build exit 0, proof exit 1 with
  `WarnStuckClaimState`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
