# Independent adversarial review: 82-prime-length

The candidate's positive K claim can be rebuilt and closes with `#Top`, the
claim is non-vacuous, and the proved macro is byte-for-byte pinned to the
submitted translated program. It nevertheless is not a proof of the real
Python program over its intended string domain. The generated semantics maps
Python `len` to K `lengthString`, which does not count all Unicode strings the
way CPython does. For the satisfying input `"λ"`, both Python implementations
return `False` because the Python length is 1, while the rebuilt K semantics
stores length 2 and returns `True`. For `"🙂🙂"`, both Python implementations
return `True` because the Python length is 2, while K stores length 8 and
returns `False`. These are concrete false-conclusion witnesses on the intended
input domain.

All candidate prose, logs, traces, KORE files, caches, and compiled definitions
were treated only as untrusted claims. All execution used fresh source copies
under `/tmp/audit-work/82-prime-length`. Reviewer-authored scripts and bounded
logs are in `/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The required infrastructure
condition holds: `/reference/reference-semantics` is absent, including as a
symlink. This was checked before candidate evaluation. There is therefore no
infrastructure breach and no hidden or supplied semantics was used.

Evidence:

- `evidence/stage1_integrity.sh`
- `evidence/stage1-integrity.log` (exit 0)
- `evidence/stage1-integrity.status`

### Trusted-input comparisons

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`ed81b55d1d505600cf191ac150a087e2e81199bfd968e4fd6d9b3cad12bb28fa`).
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
(SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
Both `cmp` commands exited 0.

The following required generation deliverables are present and correctly
typed as regular files:

| Artifact | Integrity observation |
|---|---|
| `solution.py` | Present, regular file |
| `solution.mpy` | Present, regular file |
| `semantic.k` | Present, regular file |
| `verification.k` | Present, regular file |
| `spec.k` | Present, regular file |
| `prove.sh` | Present, regular executable file |

The audit-required provenance artifacts `run-input.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, and one structured JSONL trace are also
present as regular files. No required artifact is missing, mistyped, or
symlinked. There are no candidate helper `.k` files beyond `semantic.k`,
`verification.k`, and `spec.k`.

The candidate also contains untrusted extras:
`semantic-kompiled/`, `verification-kompiled/`, `solution.kore`,
`specified-solution.kore`, and `__pycache__/`. They are generation byproducts,
not integrity failures, and none was copied into or used by the audit build.
The scratch-copy inventory is recorded in
`evidence/stage1-scratch-copy.log` (exit 0).

### Untrusted provenance claims reviewed

`run-input.json` claims problem `82-prime-length`, condition `bare`, no supplied
semantics, and the same prompt/translator hashes independently observed above.
`metrics.json` claims a successful non-timeout run. `codex-last.txt`,
`codex-output.log`, and the trace claim that nine concrete checks passed, the
program-term comparison matched, and the single proof printed `#Top`. Those
claims were not accepted as proof evidence; they were reconstructed below.

The complete 1,260,284-byte text log and all 198 JSONL events were read by the
bounded extractor. Its first/last relevant lines, event counts, original
generation request, and final claimed status are preserved in:

- `evidence/stage1_provenance_extract.py`
- `evidence/stage1-provenance-extract.log` (exit 0)

The independent toolchain is K v7.1.293. `kompile`, `krun`, `kprove`, and
`kast` resolved from `/usr/bin`; `kup` was absent, but an independently
installed working K toolchain was available, so the live audit path was used.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical behavior

The trusted prompt requires:

> Given a Python string, return `True` exactly when its length is a prime
> number, and `False` otherwise.

The documented examples require lengths 5 and 7 to be true and length 6 to be
false. The trusted canonical implementation computes Python `len(string)`,
returns false for lengths 0 and 1, checks every candidate divisor in
`range(2, length)`, and returns true exactly when none divides the length.
Thus the intended domain is Python `str`, including Unicode strings, and the
relevant length operation is CPython's code-point count.

`/candidate/solution.py` implements:

```python
def prime_length(string):
    n = len(string)
    return n >= 2 and all(n % i != 0 for i in range(2, n))
```

This is a different but extensionally correct algorithm for the trusted
contract: the `n >= 2` guard rejects 0 and 1, and the finite `all` expression
states that no integer in `[2,n)` divides `n`.

### Trusted translation

The audit copied the trusted translator, ran:

```text
python3 trusted/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.submitted.mpy
```

Both submitted and regenerated files are 476 bytes with SHA-256
`d1228a6510b7b7b80112c0b2b55ea1ab564682c421757a9af789432390dec86d`;
`cmp` exited 0. See `evidence/stage2-translation.log`.

### Independent differential test

`evidence/stage2_differential.py` independently imports the trusted canonical
entry point and the scratch copy of the candidate entry point. Its third oracle
uses trial division only through `isqrt(length)` and does not reuse a K
equation. The preserved input scope is:

- all four documented examples;
- explicit empty, length 1, loop-empty length 2, first nonempty prime length 3,
  first divisor length 4, prime/composite boundaries, Unicode, and embedded-NUL
  cases;
- every length from 0 through 300;
- 250 deterministic generated strings over ASCII, whitespace, NUL, accented,
  Greek, and non-BMP characters, seed 820082.

All 566 complete inputs and results are in
`evidence/stage2-differential.log`. There were zero mismatches among the
candidate Python function, trusted canonical function, and independent oracle;
the command exited 0. This validates the candidate Python algorithm on the
tested domain, but it is finite evidence and does not replace the K proof.

## 3. Clean proof reconstruction

### Fresh builds

Only these candidate sources were copied to scratch:
`solution.py`, submitted `solution.mpy`, `semantic.k`, `verification.k`, and
`spec.k`. Trusted prompt, canonical implementation, and translator were copied
separately. No `*-kompiled` directory or candidate KORE file entered scratch.

The exact fresh build/proof results were:

| Operation | Result | Evidence |
|---|---:|---|
| `kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition semantic-audit-kompiled` | exit 0 | `evidence/stage3-build-semantic.log` |
| `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled` | exit 0 | `evidence/stage3-build-verification.log` |
| Fresh `kast` of submitted, regenerated, and specified macro terms | all identical, exit 0 | `evidence/stage3-program-pinning.log` |
| `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | `#Top`, exit 0 | `evidence/stage3-kprove-positive.log` |

There is exactly one positive claim in `spec.k`; there are no helper claims or
other target claims to run independently.

The three fresh KORE terms—submitted `.mpy`, trusted-regenerated `.mpy`, and
`solutionProgram` after macro expansion—each have SHA-256
`1a81cc0563915ca1faff783814e18fedc9949f6139ba00b3be631fb33995c534`
and size 5,243 bytes.

### Fresh generated-semantics execution

`evidence/stage3_concrete.py` ran the fresh semantics on normal, empty,
boundary, prime, composite, square, and Unicode inputs, comparing each result
with both Python implementations and an independent numeric oracle.

All tested ASCII cases agreed, including lengths 0, 1, 2, 3, 4, 5, 6, 8, 49,
and 97. The generated semantics did not agree on the intended full Python
string domain:

```text
input: "🙂🙂"
Python length: 2
candidate Python: True
trusted canonical: True
fresh K <env> n: VInt(8)
fresh K <return>: VBool(false)
```

Every individual `krun` invocation exited 0; the comparison driver exited 1
solely because it detected this semantic result mismatch. The full final
configuration and exact command are in `evidence/stage3-concrete.log`.
This is candidate evidence, not a timeout, parser failure, container failure,
or audit-infrastructure uncertainty.

Accordingly, clean internal proof reconstruction succeeds, but the mandatory
generated-semantics concrete fidelity gate fails.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole claim has no `requires` clause. Its precondition therefore accepts
every K `String` value `S` in this exact initial state:

- `<k>` is `run(solutionProgram, VStr(S))`;
- `<env>` is the empty map;
- `<return>` is `noResult`.

It claims reachability to:

- empty computation `.K`;
- an environment containing exactly
  `"string" |-> VStr(S)` and
  `"n" |-> VInt(lengthString(S))`;
- return value
  `VBool(isPrime(lengthString(S)))`.

The precondition is satisfiable. For example,
`S = ""`, `S = "ab"`, and `S = "λ"` each form a concrete initial
configuration accepted by the claim. There is no strengthened or hidden input
precondition.

The postcondition is result-constraining: it gives an exact Boolean term, not a
free result variable, existential oracle, tautology, or one-way implication.
There are no loop/helper claims to assess against control flow.

### What is pinned and what is not

The syntactic pinning chain is strong:

```text
candidate solution.py
  -> trusted py2mpy.py
  -> byte-identical submitted solution.mpy
  -> byte-identical macro-expanded solutionProgram KORE
  -> sole entry claim
```

A body-sensitivity probe changed the source threshold from `n >= 2` to
`n >= 3` while retaining the same supported AST shape. The translated KORE
then differed from the specified macro (`cmp` exit 1), and the audit assertion
that a difference must be detected exited 0. See
`evidence/solution-body-mutated.py` and
`evidence/stage5-body-sensitivity.log`. Thus the present source body is not
silently ignored.

Syntactic identity does not establish semantic identity. The claim applies the
candidate rule

```text
valueLength(VStr(S)) => lengthString(S)
```

and writes that same K value into both the environment and return predicate.
K's observed `lengthString` behavior for these parsed strings differs from
Python `len`.

### Ground substitution comparison

`evidence/stage4_substitution.py` substituted five satisfying inputs into the
claim and compared the formal right-hand side, fresh K execution, candidate
Python, and trusted canonical Python:

| Input | Python `len` | Observed K `lengthString` | Formal/K result | Both Python results |
|---|---:|---:|---:|---:|
| `""` | 0 | 0 | `False` | `False` |
| `"ab"` | 2 | 2 | `True` | `True` |
| `"Hello"` | 5 | 5 | `True` | `True` |
| `"λ"` | 1 | 2 | `True` | `False` |
| `"🙂🙂"` | 2 | 8 | `False` | `True` |

The script found zero internal formal-execution mismatches and zero
candidate-versus-canonical Python mismatches, but two formal-to-Python
adequacy mismatches. See `evidence/stage4-substitution.log` (exit 0; adequacy
mismatches are reported data, not script failures).

The `"λ"` case is a minimal false-conclusion witness:

1. It satisfies the entry precondition.
2. The real submitted Python and trusted canonical both return `False`.
3. The generated K semantics and proved postcondition return `True`.

Therefore the formal claim pins the submitted AST to an internally consistent
but incorrect string model; it does not pin the real generated program's
behavior on the intended domain.

## 5. Rule-by-rule static soundness review

The full numbered sources, searches for every proof-relevant attribute, used
constructor/token counts, and candidate K/helper-file inventory are preserved
in `evidence/stage5-inventory.log`.

### Complete local syntax and declaration inventory

`MPY-SYNTAX` locally declares:

| Sort | Complete local productions |
|---|---|
| `Program` | `Module(Stmts)` |
| `Stmts` | separator-free list of `Stmt` |
| `Stmt` | `FuncDef(String,Params,CellVars,FreeVars,Stmts)`, `Assign(Expr,Expr)`, `Return(Expr)` |
| `Params`, `CellVars`, `FreeVars` | wrappers around `Strings` |
| `Strings` | comma-separated list of `String` |
| `Expr` | `Int`, `Bool`, `Str`, `Name`, `Call`, `BinOp`, `BoolOp`, `Compare`, `GenExp` |
| `Exprs` | comma-separated list of `Expr` |
| `CmpOp`, `CmpOps` | comparison pair and comma-separated comparison list |
| `CompFor`, `CompFors` | comprehension generator and separator-free generator list |
| `Value` | `VInt`, `VBool`, `VStr` |
| `Result` | `noResult` or `Value` |
| `KItem` | `run(Program,Value)` and internal `#exec(Stmts)` |

`SEMANTIC` adds six local function declarations:

- `eval(Expr, Map) : Value` `[function, total]`;
- `valueLength(Value) : Int` `[function, total]`;
- `asInt(Value) : Int` `[function, total]`;
- `asBool(Value) : Bool` `[function, total]`;
- `noDivisors(Int,Int,Int) : Bool` `[function, total]`;
- through `VERIFICATION`, `isPrime(Int) : Bool` `[function, total]`.

`VERIFICATION` also declares the nullary `solutionProgram : Program` macro.
There are no local `[functional]` declarations, opaque symbols, priority rules,
`owise` rules, `anywhere` rules, hooks, strictness attributes, or ordinary
proof-module rewrites. The only simplification rules are the three
`noDivisors` equations, each also carrying a `concrete(...)` restriction. The
only macro rule is `solutionProgram`.

The configuration has only:

- `<k>` for the invocation/execution term;
- `<env>` for the parameter/local binding map;
- `<return>` for the result.

No heap, allocation, I/O, exceptions, or general call stack is modeled. Those
omissions are acceptable for the submitted single-function, pure, direct-entry
program only to the extent that the modeled primitives are faithful.

### Used-construct coverage

Every constructor in submitted `solution.mpy` has a local declaration:
`Module`, `FuncDef`, `Params`, `CellVars`, `FreeVars`, `Assign`, `Return`,
`Name`, `Call`, `Int`, `Bool`, `BoolOp`, `Compare`, `CmpOp`, `GenExp`,
`CompFor`, and `BinOp`. The fresh KAST comparison also confirms that the empty
`FreeVars()` list parses as `.Strings` in the macro.

The rules cover the actual control path:

```text
run Module/FuncDef
  -> bind "string"
  -> execute Assign n = len(string)
  -> execute Return(and/comparison/all-generator)
  -> .K with exact env and return cells
```

The generator has no mutations, output, allocation, exceptions on the used
range, or observable control effect beyond its Boolean. Eager evaluation of
the right side of `and` therefore changes neither the result nor state for this
specific submitted program, even though it is not a generally valid Python
short-circuit semantics.

### Exhaustive rule inventory and decisions

The 19 rules in `semantic.k` and two in `verification.k` are:

| Rule | Class and complete used-domain decision |
|---|---|
| `run(Module(FuncDef(...)), ARG) => #exec(BODY)` with empty env and function-name guard | Entry operational rule. It binds the sole parameter and ignores closure metadata. Exact for this one top-level `prime_length` invocation; it assumes the intended direct entry point and standard module environment. |
| `#exec(Assign(Name(X),E) SS)` | Operational assignment. Evaluates `E` in the old map and updates `X`; exact for local `n`. |
| `#exec(Return(E) _SS)` | Operational return. Evaluates in the current env, consumes the computation, and writes `<return>`. Discarding trailing statements matches Python return for this flat body. |
| `eval(Int(I),ENV) => VInt(I)` | Literal equation; sound. |
| `eval(Bool(B),ENV) => VBool(B)` | Literal equation; sound. |
| `eval(Str(S),ENV) => VStr(S)` | Literal equation; unused by the submitted AST but internally sound. |
| `eval(Name(X),ENV) => ENV[X]` when bound | Name lookup; sound on the path because `"string"` and `"n"` are bound, and generator handling does not invoke general lookup for `"i"`. |
| `eval(Call(Name("len"),E),ENV) => VInt(valueLength(eval(E,ENV)))` | Direct standard-builtin bridge. Binding/evaluation is adequate for this unshadowed source in the normal HumanEval environment, but its result inherits the invalid `valueLength` equation below. |
| `valueLength(VStr(S)) => lengthString(S)` | **Materially invalid Python bridge.** False-conclusion witness: for satisfying input `"λ"`, K yields 2 and proves/returns prime=`True`, while Python `len("λ")` is 1 and both Python implementations return `False`. A second witness is `"🙂🙂"`: K length 8/false versus Python length 2/true. |
| `eval(BinOp("%",E1,E2),ENV)` | Integer modulo bridge through `asInt`; sound on the used range because divisors start at 2. It does not model Python's zero-divisor exception off path. |
| `asInt(VInt(I)) => I` | Sound coercion on all actual calls. |
| `eval(Compare(...,">=", ...),ENV)` | Integer comparison; sound on actual operands. |
| `eval(Compare(...,"!=", ...),ENV)` | Integer inequality; sound on actual operands. |
| `eval(BoolOp("and",E1,E2),ENV)` | Eager Boolean conjunction. It is over-broad as general Python semantics, but the actual right operand is pure, finite, and exception-free, so there is no false conclusion witness on the intended execution path beyond inherited length behavior. |
| `asBool(VBool(B)) => B` | Sound on all actual calls. |
| Exact `eval(Call(all, GenExp(...range...)), ENV)` pattern | Pure-expression operational summary. It matches the submitted generator shape, checks the captured numerator and high-bound names are bound and distinct from the iteration variable, and returns `noDivisors`. It does not model general generators, but minimal used-construct coverage is permitted in generated-semantics mode. It assumes standard `all`/`range` bindings. |
| `noDivisors(N,D,HI) => true` for `D >= HI` | Correct empty-range equation. Guard is disjoint from the recursive cases. |
| `noDivisors(N,D,HI) => false` for `D < HI` and `N % D == 0` | Correct first-divisor equation on the used domain `D >= 2`. |
| `noDivisors(N,D,HI) => noDivisors(N,D+1,HI)` for a non-divisor | Correct descending-range equation on the used domain; `HI-D` strictly decreases. Its guard is disjoint from the divisor equation. |
| `solutionProgram => Module(FuncDef(...))` `[macro]` | Compile-time program name, not an oracle. Fresh KAST equality proves it is the submitted translated AST. |
| `isPrime(N) => N >= 2 andBool noDivisors(N,2,N)` | Transparent definitional summary. Over mathematical integers, this is the usual definition of primality because every nontrivial factor has a divisor in `[2,N)`. It does not repair the invalid Python-to-K length mapping. |

### Functions, totality, overlaps, and trust implications

The `eval`, `valueLength`, `asInt`, and `asBool` declarations are marked
`[total]` despite lacking equations for many values admitted by their declared
sorts. For example, there is no `valueLength(VInt(_))`, `asInt(VStr(_))`, or
general `eval` equation for arbitrary call/operator strings. `noDivisors` also
has an off-path gap when a range reaches divisor zero because `%Int 0` is not
defined. These declarations let K treat the symbols as total outside their
specified equations, but no such case is reached from the entry claim:
`valueLength` receives `VStr`, integer coercions receive `VInt`, Boolean
coercions receive `VBool`, and `noDivisors` starts at 2 with a nonnegative
string length.

Under the problem's generated-semantics boundary, missing behavior for unused
constructs is not itself a defect. No concrete or symbolic false conclusion on
the intended entry path was found from those off-path totality gaps, so they
are recorded as a narrower evidence/reuse limitation, not mislabeled as
another unsound rule.

The function-rule patterns used on the path are disjoint. The three
`noDivisors` guards partition the reachable ground cases: `D >= HI`, or
`D < HI` with modulo equal/non-equal to zero. There are no competing
priorities. Map updates preserve the parameter and add `n`. No allocation or
hidden state is fabricated.

The exact `all`/generator rule is task-specific but is not an unconstrained
oracle: its result is fixed by three executable recursive equations, and
fresh ground runs exercise both divisor and exhaustion outcomes. It skips a
general generator machine, so the summary-to-Python bridge is supported by
the exact pattern, purity, ordinary range/all mathematics, and finite concrete
evidence rather than a separate universal K connection theorem. That is a
documented trust limitation. The decisive rejection instead has a direct
false witness in the used `valueLength` bridge.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted or reused. The
audit created `evidence/spec-vacuity-audit.k`, preserving the complete entry
configuration and environment obligation but changing the result to the false
universal postcondition `VBool(true)`.

The mutation is demonstrably false for the satisfying input `S = ""`: the
fresh semantics returns `VBool(false)`.

1. A `kprove ... --dry-run` build of the mutation exited 0. Its generated
   `kore-exec` command is in `evidence/stage6-mutation-build.log`.
2. The actual mutation proof exited 1 with `WarnStuckClaimState`. The residual
   shows the unmet implication between constant `true` and
   `lengthString(S) >= 2 andBool noDivisors(...)`, while the final configuration
   is otherwise reached. See `evidence/stage6-mutation-proof.log`.

This is the expected proof-obligation failure, not a parser error, missing
import, timeout, or unrelated crash. It establishes that the original return
obligation is discriminating.

For completeness,
`evidence/solution-body-mutated-attempt1-parser-error.py` and
`evidence/stage5-body-sensitivity-attempt1-parser-error.log` preserve an
earlier exploratory source mutation that removed the generator and
consequently produced a translator AST form outside this minimal syntax. That
status 113 event is not used as non-vacuity evidence. It was replaced by the
valid body-sensitivity mutation described in Stage 4, and the independent
Stage 6 false-postcondition mutation builds successfully.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate K definition and K's built-in theories, the sole successful
claim establishes this partial-correctness statement:

> For every K `String` term `S`, execution of the exact submitted translated
> AST through the candidate `run` entry wrapper from empty environment and
> `noResult` reaches empty computation, the specified two-entry environment,
> and the exact Boolean
> `isPrime(lengthString(S))`.

It also establishes the exact final `string` and `n` bindings. The result is
not free, and the fresh false mutation confirms that a contradictory result
does not prove.

It does **not** establish that K `lengthString(S)` equals CPython `len(string)`
for the corresponding intended Python string. It does not establish a general
Python semantics for calls, generators, closures, exceptions, or
short-circuiting. It does not prove that arbitrary monkey-patched
`len`/`range`/`all` bindings behave like the standard builtins. Finally,
differential Python testing does not connect the K string model to CPython.

### Trust ledger

| Boundary or assumption | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, parser, Haskell backend, and prover | All build, execution, and proof results | Necessary low-level trusted computing base; acceptable for this audit. |
| K built-in integer, Boolean, map, modulo, comparison, and string operations | All evaluator equations and the claim | Integer/Boolean/map portions are acceptable on the used domain. The chosen string-length bridge is illegitimate for the intended Python domain, with two concrete false witnesses. |
| Trusted `/reference/py2mpy.py` | Source-to-`.mpy` identity | Acceptable trusted input; byte identity was independently checked. |
| Trusted canonical Python implementation | Intent oracle in differential and ground comparisons | Authoritative trusted input; used as an executable oracle, not as a K proof. |
| `run` as a direct invocation wrapper | Entry binding and control | Acceptable for the stated single-entry HumanEval call, conditional on a standard module environment. |
| Standard unshadowed `len`, `range`, and `all` | Call rules | Reasonable HumanEval execution assumption, but not modeled through Python name resolution. |
| Exact `all`/generator-to-`noDivisors` summary | Returned value and `isPrime` postcondition | Transparent/executable on ground used inputs and mathematically justified for the exact pure pattern; lacks a separate universal connection theorem to a general generator semantics. Concerning but not an unconstrained oracle. |
| `noDivisors` recursive equations | Generator result and primality predicate | Acceptable for reachable `D >= 2`; disjoint and terminating over the finite interval. Off-path divisor-zero/totality behavior is not established. |
| Ordinary mathematical bridge from no divisors in `[2,N)` to prime | Natural-language intent | Sound elementary mathematics; not separately stated as a K theorem because `isPrime` is defined by that characterization. |
| Python differential test over 566 cases | Candidate Python versus canonical behavior | Strong finite support only. It cannot validate untested inputs universally and cannot replace the K/Python semantic bridge. |
| Fresh K concrete tests | Generated-semantics bridge | They expose rather than cure the Unicode mismatch. |

### Decision

The fresh `#Top`, exact program-term pinning, and successful non-vacuity test
show that this is not merely a missing, stale, or vacuous proof. The formal
theorem is internally coherent for the submitted K definition. However,
real-program soundness fails at the used rule
`valueLength(VStr(S)) => lengthString(S)`. The witness `"λ"` makes the K
theorem conclude `True` where the real submitted Python and trusted canonical
both conclude `False`; `"🙂🙂"` gives the opposite Boolean discrepancy.

The proof therefore establishes a substituted byte-oriented string-length
model, not partial correctness of the real generated Python program over its
intended string domain. This meets the `FAIL / NOT_LEGIT` decision boundary for
materially unsound generated semantics with explicit false-conclusion
witnesses.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
