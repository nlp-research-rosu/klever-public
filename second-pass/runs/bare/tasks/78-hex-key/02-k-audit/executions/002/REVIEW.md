# Independent adversarial audit: 78-hex-key

This audit used the mandated `using-kit`, `validating-proof`, and
`writing-semantics` workflows. I treated all candidate and generation records
as untrusted evidence, copied source artifacts into `/tmp/audit-work/rebuild`,
and rebuilt all K definitions there.

## 1. Input and provenance integrity

The launcher record `/audit-input.json` declares:

- problem `78-hex-key`;
- condition `bare`;
- record layout `legacy-selected-stage1`; and
- semantics mode `GENERATED_SEMANTICS`.

All records required for that layout were present, readable, and real regular
files/directories: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The one trace JSONL file contained 104 valid JSON records. The sanitized
line-by-line inspection is in
`evidence/01-trace-inspection.log`; its claims were not used as proof results.

`/audit-campaign-lock.json` was byte-hashed independently and its parsed object
exactly equaled `/audit-input.json.audit_campaign`. Its SHA-256 was the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded file digest checked by
`evidence/provenance_check.py` matched, including the canonical program,
trusted/candidate prompt, trusted/candidate translator, run/task/result
records, generation prompt, metrics, usage, final text, output log, and trace
JSONL.

The candidate prompt and trusted prompt were byte-identical. The candidate
translator and trusted translator were byte-identical. The candidate tree and
trace tree contained no symlink or special-file entries. The independently
recomputed pipeline tree digest of `/candidate` was
`504d481954e44c8dd2c8ac79fcbbb55b8f9f5d50280ec42cdd25a250d4e6161d`,
matching both the invocation and retained-workspace records. The trace tree
digest was
`586d9dc240331f9f7663757237836241d4b2dedf0a030c7296710593a86221af`,
matching `usage.json`; its single file also matched the independently recorded
file digest. `/audit-input.json` additionally records two launcher-specific
directory digests without declaring their serialization. I recorded those
values but did not pretend to recompute them using an invented format; the
independently reproducible component and pipeline-tree hashes all matched.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist, nor does a candidate
`reference-semantics` tree. There is therefore no mode contradiction and no
audit-infrastructure breach. Full results and exact hashes are in
`evidence/01-provenance.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for any valid uppercase hexadecimal string,
including the empty string, return the number of character positions whose
digit is one of `2`, `3`, `5`, `7`, `B`, or `D`.

The trusted canonical program loops over every input position and increments
the total exactly when the character is in that six-element tuple. Candidate
`/candidate/solution.py` instead sums six calls to `str.count`. On the intended
domain those algorithms are equivalent: every target is a distinct,
nonempty, one-character string, so every qualifying input position contributes
to exactly one summand and every other position contributes to none.

I regenerated the constructor program using the trusted mounted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/rebuild/solution.py \
  > /tmp/audit-work/rebuild/regenerated-solution.mpy
```

`cmp` exited 0. Both submitted and regenerated terms had SHA-256
`19e936a519a63db4e4fcc3f41ac8aae3fabb6415c2fd65cef5025e2d87e724b6`.
See `evidence/02-translation-identity.log`.

The independent differential test loaded the trusted canonical and candidate
modules under distinct import names and also used the direct character
predicate as a third oracle. It covered:

- every prompt example;
- the empty, singleton, and multi-character loop boundaries;
- both membership outcomes and all 16 hexadecimal singleton digits;
- all valid strings of lengths zero through four; and
- 512 deterministic strings of lengths 5 through 256.

There were 70,436 unique inputs and zero mismatches. The serialized input-set
digest and exact generator are preserved in `evidence/02-differential.log` and
`evidence/differential_test.py`. This is finite fidelity evidence, not a
replacement for the K proof or the universal distinct-singleton argument above.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/rebuild`; no
candidate-provided kompiled directory or cache was copied. Source hashes before
and after copying are in `evidence/03-scratch-source-hashes.log`. The installed
toolchain was K `v7.1.293`, matching the campaign lock.

Fresh commands and outcomes were:

| Purpose | Result | Evidence |
|---|---|---|
| LLVM compile of `semantic.k`, main module `MPY`, syntax `MPY-SYNTAX` | exit 0 | `evidence/03-kompile-concrete.log` |
| Haskell compile of `verification.k`, main module `VERIFICATION`, syntax `MPY-SYNTAX` | exit 0 | `evidence/03-kompile-proof.log` |
| Sole positive claim in `HEX-KEY-SPEC` | exit 0, `#Top` | `evidence/03-kprove-positive.log` |
| Fresh LLVM executions versus both Python implementations | 25/25 pass | `evidence/03-concrete-semantics.log` |

Concrete cases included empty input, every prompt example, every hexadecimal
singleton, all-prime and no-prime long strings, and a repeated full alphabet.
Every `krun` terminated with `.K` and the expected `intVal`. The preserved
`03-concrete-semantics-parser-bug.log` is a reviewer-script failure: the first
regex looked for a literal backslash sequence even though all captured K
outputs and exit statuses were correct. The corrected parser and successful
rerun are preserved rather than hiding that mistake.

Thus the dynamic reconstruction gate passes independently of candidate logs and
the prior claimed `#Top`.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no `requires` clause. Its variable `S` therefore ranges over all
K `String` values, a domain strictly broader than the prompt's valid uppercase
hexadecimal strings.

Its initial state requires:

- `<k>` to contain the complete `Module(FuncDef(...))` constructor term followed
  by `#invoke("hex_key", S)`;
- `<env>` to be exactly `.Map`; and
- `<result>` to be exactly `noResult`.

Its destination requires:

- `<k>` to be empty;
- `<env>` to contain exactly `"num" |-> strVal(S)`; and
- `<result>` to equal `intVal(primeHexCount(S))`.

`primeHexCount(S)` is not free or opaque. It is defined by one unguarded rule as
the sum of the six `countAllOccurrences` terms for `2,3,5,7,B,D`.

### Mechanical program identity

Program pinning has two independent links:

1. trusted translation regenerated `solution.mpy` byte-for-byte; and
2. I extracted the `Module(...)` term executed by the claim, parsed both it and
   submitted `solution.mpy` using the freshly compiled syntax, and compared the
   JSON KASTs.

The KASTs were byte-identical and had SHA-256
`e6403ed7d31b289cb7b4f972b0f360e54c13747fe009b2af0e118b4e992a4179`.
See `evidence/04-program-pinning.log` and
`evidence/extract_claim_program.py`. There is no omitted typing import,
normalization, substituted helper, or detached summary body.

The invocation rule also pins binding: the same K variable `F` occurs in
`FuncDef(F,...)` and `#invoke(F,...)`. The rule has no arbitrary continuation
frame, and the return rule only matches an exact `Return(E)` computation.

The precondition is satisfiable. For example `S = ""`, `S = "ABED1A33"`, and
`S = "123456789ABCDEF0"` instantiate the exact initial cells. The claimed
results are respectively 0, 4, and 6, agreeing with both Python
implementations and fresh K execution. Details are in
`evidence/04-ground-witnesses.log`.

A separate body-sensitivity mutant changed the program term's final count from
`D` to `E` while leaving the postcondition unchanged. It parsed successfully,
then `kprove` exited 1 with a stuck residual equating the `...+"D"` and
`...+"E"` count sums. `S = "D"` is a concrete false witness: the mutant returns
0 while the claimed result is 1. See `evidence/spec-body-mutant.k` and
`evidence/05-body-mutation-proof.log`. This confirms dependence on the body
actually executed by the claim.

There are no loop/helper claims, fixed-size cases, bounded unrollings, or domain
restrictions. The full source-contract domain is covered.

## 5. Rule-by-rule static soundness review

The candidate contains exactly three local K files: `semantic.k`,
`verification.k`, and `spec.k`. The raw declaration inventory and hashes are in
`evidence/05-local-rule-inventory.log`.

### Local syntax and configuration inventory

| Declaration | Productions / role |
|---|---|
| `Program` | `Module(FunctionDef)` |
| `FunctionDef` | `FuncDef(String, Params, Stmt)` |
| `Params` | one string parameter |
| `Stmt` | `Return(Expr)` |
| `Expr` | `Name`, `Str`, `BinOp`, `Attribute`, `Call` |
| `Val` | `strVal`, `intVal`, `countMethod` |
| `Result` | `noResult` or `Val` |
| `KItem` | `#invoke(String,String)` |
| Functions | `eval`, `asString`, `countReceiver`, `asInt` |
| Verification function | `primeHexCount(String)` |
| Configuration | `<hexKey>` containing exact `<k>`, `<env>`, and `<result>` cells |

The submitted term uses one `Module`, one `FuncDef`, one `Params`, one
`Return`, five `BinOp("+",...)`, and six each of `Call`, `Attribute("count")`,
`Name("num")`, and `Str`. Every construct maps to a declaration and a rule.
Unused Python constructs are deliberately absent and would fail to parse or
remain stuck, which is permitted in generated-semantics mode.

### Exhaustive local rule inventory

| Rule | Complete local domain and assessment |
|---|---|
| `eval(Name(X), X |-> V) => V` | Exact singleton lookup. Correct for the exact one-parameter environment established by invocation; no framed map is silently accepted. |
| `eval(Str(S), _) => strVal(S)` | Correct literal evaluation; environment is intentionally irrelevant. |
| `eval(Attribute(E,"count"),ENV) => countMethod(asString(eval(E,ENV)))` | Correctly binds the used string method to its evaluated receiver. Non-string cases remain stuck at `asString`, rather than fabricating a value. |
| `eval(Call(F,A),ENV) => intVal(countAllOccurrences(countReceiver(eval(F,ENV)),asString(eval(A,ENV))))` | Applies only to the supported bound-count path: other function or argument values remain stuck at the partial projection helpers. For the actual six calls, receiver and argument are strings. |
| `eval(BinOp("+",L,R),ENV) => intVal(asInt(eval(L,ENV)) +Int asInt(eval(R,ENV)))` | Correct integer addition for the actual nested pure count expressions. Non-integer operands remain stuck. |
| `asString(strVal(S)) => S` | Truthful, non-overlapping projection. |
| `countReceiver(countMethod(S)) => S` | Truthful, non-overlapping projection. |
| `asInt(intVal(I)) => I` | Truthful, non-overlapping projection. |
| module/invoke rule | Requires exact function-name equality, exact empty environment, exact module-plus-invocation computation, and installs the sole parameter binding. It skips function-object allocation, which has no modeled or source-contract-observable effect in this isolated entry call. |
| return rule | Requires exact `Return(E)`, reads the established environment, evaluates the pure expression, sets the result, and consumes computation. There is no suffix or control stack that it could discard. |
| `primeHexCount(S)` equation | Unguarded and total over `String`; its six fixed nonempty singleton needles make the sum exactly the prompt's target count on valid inputs. It names the postcondition and does not replace program execution. |

The four semantic helpers `eval`, `asString`, `countReceiver`, and `asInt` have
the `[function]` attribute but no false `[total]` assertion. `primeHexCount` is
`[function,total]`, and its single unguarded equation covers its complete
`String` domain. There are no local `functional`, `opaque`,
`simplification`, `concrete`, `owise`, macro, alias, priority, or proof-only
ordinary rules. There are no overlaps between the constructor-headed `eval`
rules or projection rules.

Evaluation is compressed into pure K functions rather than a Python evaluation
stack. For this exact expression all subexpressions are state-free, all
receivers and arguments have the required type, and arbitrary-precision integer
addition cannot raise; therefore left-to-right versus equational reduction has
no observable result, state, control, or exception difference. The only modeled
state is the local binding and result. Retaining the final local environment is
an instrumentation choice of this minimal configuration, not a claim about a
live CPython call frame, and the intended observable result is fully
constrained.

`STRING`, `INT`, and `MAP` are K's fixed domain modules. The relevant installed
K definition declares `countAllOccurrences` as a total
`STRING.countAllOccurrences` hook and documents/defines it using successive
`findString`, `substrString`, and `lengthString` operations. The exact installed
excerpt is in `evidence/05-k-string-primitive.log`. Mapping Python
`str.count(c)` to that primitive is sound for each fixed nonempty
one-character `c`; it neither encodes the six-prime answer in the operational
semantics nor introduces an unconstrained oracle.

No inventoried original rule was found unsound, so there is no unsupported
unsoundness allegation requiring a false-conclusion witness. The two explicit
false witnesses in this audit apply only to reviewer mutations, not to original
rules.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I created
`evidence/spec-vacuity.k`, preserving the exact submitted program term and
entry state while changing only the required result to
`primeHexCount(S) +Int 1`.

The mutated spec's dry run exited 0, demonstrating that it parsed and built
against the fresh proof definition. Actual proof execution exited 1 with
`WarnStuckClaimState`. The residual explicitly showed the unmet equality
between the six-count sum and that same sum plus 1; it was not a parser error,
missing import, timeout, or unrelated backend failure. Empty input is a
satisfying concrete witness: execution yields 0 while the mutation requires 1.
See `evidence/06-vacuity-dry-run.log` and
`evidence/06-vacuity-proof.log`.

The proof is therefore result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under modules `MPY`, `VERIFICATION`, and K's imported domain semantics, for
every K string `S`, executing the exact regenerated/submitted constructor
program in the claim's exact empty entry configuration reaches empty
computation, the singleton `num` environment, and

```text
intVal(
  countAllOccurrences(S,"2") +
  countAllOccurrences(S,"3") +
  countAllOccurrences(S,"5") +
  countAllOccurrences(S,"7") +
  countAllOccurrences(S,"B") +
  countAllOccurrences(S,"D")
)
```

This is a partial-correctness result. The comment in candidate `spec.k` calls
it “Total functional correctness,” but this audit does not rely on or repeat
that overstatement. The proof is not narrowed to examples or fixed lengths.

### Trust ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K prover/compiler and reachability logic, version 7.1.293 | All machine-checked results | Standard unavoidable proof-system trust; version recorded and definitions rebuilt. Acceptable. |
| Trusted `/reference/py2mpy.py` | Python-source to constructor identity | Launcher-designated trusted input; byte regeneration and KAST pinning checked. Acceptable. |
| K `STRING`, `INT`, and `MAP` primitives | Count values, integer sums, environment | Fixed toolchain primitives, not candidate or proof-local oracles; installed definitions inspected. Acceptable. |
| Generated rules for the used Python fragment | Meaning of the submitted constructor program | Audited rule by rule; every used construct covered, unused constructs fail visibly, and no body is skipped by a proof rule. Acceptable. |
| Python `str.count(c)` versus K `countAllOccurrences(S,c)` for nonempty singleton `c` | Semantic fidelity of the six calls | Direct operation-level correspondence on the complete intended call shape, supported by boundary/long concrete K tests and broad independent Python differential evidence. No contrary witness; acceptable. |
| Six distinct target digits versus natural-language “prime hexadecimal digits” | Intent adequacy | The prompt itself identifies exactly those six symbols. Distinct singleton counts partition qualifying positions, an ordinary universal combinatorial fact. Acceptable. |

Finite tests support the implementation and primitive bridges but are not used
as a universal theorem. No opaque symbol, empirical oracle, unproved loop
summary, proof-local operational bridge, or task-answer semantic shortcut
contributes to claim closure.

Excluded from the theorem are a complete semantics for arbitrary Python
programs, CPython frame/allocation internals, and a total-correctness or
termination guarantee. Those exclusions do not remove any material behavior
from this pure, straight-line function's source contract.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and evidence auditability) all pass. The proof reconstructs cleanly, constrains
the result, executes the real generated program, covers the unrestricted
source-contract domain, and has no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
