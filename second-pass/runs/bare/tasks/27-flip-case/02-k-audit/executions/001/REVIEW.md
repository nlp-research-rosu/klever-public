# Independent adversarial audit: 27-flip-case

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the exact submitted `solution.mpy` under the freshly compiled Haskell
definition. The proof is result-constraining, executes the submitted function
body, and is sensitive to changes in the result, body, and `swapcase`
dispatch rule.

The result is **legitimate with concerns**, rather than an unqualified pass,
because the Unicode bridge is explicitly tied to the Haskell backend's
UTF-8-byte behavior for K `String`. A separately rebuilt LLVM definition
executes ASCII correctly but fails on normal non-ASCII inputs. For example,
on the UTF-8 representation of `Straße Δelta`, LLVM returned
`sTRAße ΔELTA` instead of Python's `sTRASSE δELTA`. The Haskell concrete and
proof definitions return the correct result. This is a real backend-portability
and intent-bridge limitation, but it does not make a false result provable in
the Haskell proof theory actually used by the candidate.

The exact commands and statuses are indexed in
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The required negative integrity
check passed: `/reference/reference-semantics` does not exist. The trusted mount
contains only `canonical.py`, `prompt.py`, and `py2mpy.py`. There is therefore
no hidden or supplied semantics to compare or use. This is not an
infrastructure breach.

### Required artifacts and types

The candidate contains all generation deliverables:

- `solution.py`, `solution.mpy`
- `semantic.k`, helper `unicode-case.k`
- `verification.k`, `spec.k`
- `prove.sh`
- generator `gen_unicode_case.py`
- provenance files `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and one structured JSONL trace

Every inspected artifact is a regular file. No symlinks occur anywhere in
`/candidate`. The extra `verification-kompiled/` tree is a candidate-built
cache/definition, not a source deliverable. It was deliberately omitted from
the scratch copy and never used.

The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`497a1ae9517dff889ad676a36f0e0bdcbe5afec3d283ad12045fd34df3e1dba4`).
The candidate's `py2mpy.py` is byte-identical to the trusted translator
(SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
No required source artifact is missing, changed, mistyped, or symlinked.

The untrusted run metadata reports condition `bare`, problem
`27-flip-case`, a zero generator exit, and a final claim that all three proofs
closed. The full 229-record structured trace was parsed, but those claims were
not used as proof evidence. The trace also records several failed development
attempts before the final candidate, reinforcing why its reported `#Top`
cannot be trusted without reconstruction.

Evidence:

- [01-integrity.log](/audit-output/evidence/logs/01-integrity.log)
- [01-untrusted-claims.log](/audit-output/evidence/logs/01-untrusted-claims.log)
- [01-untrusted-trace-summary.log](/audit-output/evidence/logs/01-untrusted-trace-summary.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For an input Python `str`, `flip_case` must return a string in which lowercase
characters are changed to uppercase and uppercase characters are changed to
lowercase. The documented example is `flip_case("Hello") == "hELLO"`.
The trusted canonical implementation is `return string.swapcase()`, so its
operative interpretation includes Python's Unicode case mappings,
multi-code-point expansions such as `ß -> SS`, and unchanged uncased
characters.

The candidate's [solution.py](/candidate/solution.py:1) is:

```python
def flip_case(string: str) -> str:
    return string.swapcase()
```

This preserves the required signature and has the same executable body as
the trusted canonical function.

### Trusted translation

Running the trusted translator on the scratch copy produced a byte-identical
file to the submitted `solution.mpy`. Both hashes are
`f34d90ab871c6106c87ea64aa17e5ae4da5bfd5e86ca7ce805959554f8ae8620`.
The translated program is exactly one `FuncDef` whose body returns the
zero-argument `swapcase` attribute call on the parameter `string`.

Evidence: [02-fidelity.log](/audit-output/evidence/logs/02-fidelity.log).

### Independent differential test

The reviewer-authored differential test imports the trusted canonical and
candidate modules independently. It checked:

- the documented example and empty input;
- ASCII upper/lower branch boundaries and adjacent uncased characters;
- digits, punctuation, NUL, combining marks, Greek, expansion mappings,
  and 1/2/3/4-byte Unicode regions;
- lone Python surrogate values;
- every one of the 1,114,112 possible one-code-point Python strings;
- 5,000 deterministic generated strings of lengths 0 through 40 using seed
  `270027`.

There were zero mismatches. The 5,000 exact generated inputs are preserved in
[differential-inputs.jsonl](/audit-output/evidence/differential-inputs.jsonl).

This differential is finite for multi-character strings, and both Python
implementations intentionally call the same CPython primitive. It is therefore
support for program fidelity, not a substitute for the K proof or for the
semantic audit.

Evidence:

- [02_differential.py](/audit-output/evidence/02_differential.py)
- [02-differential.log](/audit-output/evidence/logs/02-differential.log)

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/candidate-src`. Candidate definitions and caches were neither
copied nor referenced. K version `v7.1.293` and Python `3.10.12` were available
independently.

### Fresh builds

The following source-only builds succeeded:

| Definition | Backend | Source/main module | Exit |
|---|---|---|---:|
| `concrete-kompiled` | LLVM | `semantic.k` / `MPY` | 0 |
| `concrete-haskell-kompiled` | Haskell | `semantic.k` / `MPY` | 0 |
| `proof-kompiled` | Haskell | `verification.k` / `VERIFICATION` | 0 |

The Unicode helper was also regenerated in a separate directory using the
copied generator. It was byte-identical to the submitted helper, with SHA-256
`c09aed4113b37b80c83100360298de60c66f669ffce8001f0ef56b91c76325d5`.

Build evidence:

- [03-kompile-llvm.log](/audit-output/evidence/logs/03-kompile-llvm.log)
- [03-kompile-concrete-haskell.log](/audit-output/evidence/logs/03-kompile-concrete-haskell.log)
- [03-kompile-haskell.log](/audit-output/evidence/logs/03-kompile-haskell.log)
- [03-regenerate-unicode-helper.log](/audit-output/evidence/logs/03-regenerate-unicode-helper.log)

### Independent positive proof runs

For independent selection only, the scratch `spec.k` was given labels without
altering any claim term, precondition, or postcondition. Each target was then
run separately:

| Claim | Exit | Required output |
|---|---:|---|
| `SPEC.symbolic` | 0 | `#Top` |
| `SPEC.example-hello` | 0 | `#Top` |
| `SPEC.example-unicode` | 0 | `#Top` |

Evidence:

- [03-kprove-SPEC-symbolic.log](/audit-output/evidence/logs/03-kprove-SPEC-symbolic.log)
- [03-kprove-SPEC-example-hello.log](/audit-output/evidence/logs/03-kprove-SPEC-example-hello.log)
- [03-kprove-SPEC-example-unicode.log](/audit-output/evidence/logs/03-kprove-SPEC-example-unicode.log)

### Concrete generated-semantics execution

The fresh Haskell build of `semantic.k` was executed on empty input, the
documented example, ASCII boundaries, Unicode expansions, and leading-byte
boundaries spanning valid 1/2/3/4-byte UTF-8. Its returned byte strings matched
independently computed Python results in every case:

| Input | Python and Haskell result |
|---|---|
| `""` | `""` |
| `"Hello"` | `"hELLO"` |
| ``"@AZ[`az{"`` | ``"@az[`AZ{"`` |
| `"Straße Δelta"` | `"sTRASSE δELTA"` |
| `"ßİŉﬃ"` | `"SSi\u0307ʼNFFI"` |
| mixed 2/3/4-byte boundaries | exact Python byte result |

The bridge was additionally distinguished from a code-point ambiguity:
Python `"\u00c3\u009f"` was supplied as its four UTF-8 bytes
`c3 83 c2 9f` and correctly became `c3 a3 c2 9f`. A lone surrogate encoded
with `surrogatepass` remained unchanged in both Python and K.

Evidence:

- [03-concrete-runs-haskell-semantic-only.log](/audit-output/evidence/logs/03-concrete-runs-haskell-semantic-only.log)
- [03-encoding-bridge.log](/audit-output/evidence/logs/03-encoding-bridge.log)

### Backend-portability concern

The separately built LLVM definition agreed on empty and ASCII cases but did
not apply the generated non-ASCII equations. Concrete false-result witness:

```text
input Python str:       Straße Δelta
Python/Haskell result:  sTRASSE δELTA
LLVM result:            sTRAße ΔELTA
```

Both `\u`-escaped and UTF-8-byte-escaped input spellings exhibited this
LLVM divergence. Raw source Unicode also produced backend-sensitive behavior.
K's installed string documentation explicitly says the backend-hooked Unicode
implementation is incomplete beyond the first 256 code points. The candidate
uses the Haskell backend's actual byte behavior and its proof is built on that
backend, so the divergence does not falsify the reconstructed Haskell theorem.
It does prevent an unqualified portability/intent claim for `semantic.k`.

Evidence:

- [03-concrete-runs.log](/audit-output/evidence/logs/03-concrete-runs.log)
- [03-backend-unicode.log](/audit-output/evidence/logs/03-backend-unicode.log)
- [05-k-string-docs.log](/audit-output/evidence/logs/05-k-string-docs.log)

## 4. Adequacy and real-program pinning

### Entry claims in plain language

1. **Symbolic entry claim, [spec.k](/candidate/spec.k:8).**  
   Precondition: the `<k>` cell contains the exact translated one-function
   module; `<arg>` contains an arbitrary K `String` `S`; and `<functions>` and
   `<env>` are empty. There is no additional `requires` condition.  
   Postcondition: execution returns `strVal(flipSpec(S))`, installs exactly the
   submitted `flip_case` function body in `<functions>`, preserves the argument,
   and leaves `<env>` empty.

2. **Documented example, [spec.k](/candidate/spec.k:26).**  
   The same exact initial program and empty maps are used with argument
   `"Hello"`. The result is constrained to `strVal("hELLO")`; the final function
   map and environment are also constrained.

3. **Unicode example, [spec.k](/candidate/spec.k:45).**  
   The same exact initial program is used with the UTF-8 bytes for
   `"Straße Δelta"`. The result is constrained to the UTF-8 bytes for
   `"sTRASSE δELTA"`, with the same final-state constraints.

All three preconditions are satisfiable. Concrete initial states with `S = ""`,
`S = "Hello"`, and the encoded Unicode example were executed in Stage 3.
Substituting those inputs into the symbolic postcondition gives, respectively,
`""`, `"hELLO"`, and `"sTRASSE δELTA"` under `pySwapCase`; both Python
implementations and the fresh Haskell semantics agree.

### Actual-program identity

The claim contains `Module(FuncDef("flip_case", Params("string"), ...))` with
the exact `Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))` body.
The `.Exprs` term is the generated empty-list unit. Parsing the submitted
translator output and an independently written term with the translator's
external empty-list spelling produced byte-identical KAST hashes
`7e9dfee5a183644b16a80f4e4d99f40a86b573b533b99d8c99bccc2abb9d1f25`.

Evidence:

- [04_claim-program.mpy](/audit-output/evidence/04_claim-program.mpy)
- [04-pinning-corrected.log](/audit-output/evidence/logs/04-pinning-corrected.log)

There are no helper or loop claims. The operational path is the real program:
load its `FuncDef`, look up and bind `string`, evaluate its `Name`, form the
bound `swapcase` method, call it with zero arguments, and perform its `Return`.
The proof neither substitutes another program nor jumps from the initial
module directly to the postcondition.

### Result constraint

`flipSpec` is not a free variable or opaque oracle. It has the transparent
equation `flipSpec(S) => pySwapCase(S)`, and `pySwapCase`/`pySwapChar` have
executable defining equations. Although the symbolic proof can normalize both
execution and postcondition to the same `pySwapCase(S)` term, the concrete
claims and the fresh false mutation demonstrate that the result remains
constrained. The connection of `pySwapCase` to Python is accounted for in
Stages 5 and 7 rather than being inferred from `#Top`.

## 5. Rule-by-rule static soundness review

The machine-readable inventories contain every local declaration and rule:

- [syntax-inventory.tsv](/audit-output/evidence/syntax-inventory.tsv)
- [rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv)
- [claim-inventory.tsv](/audit-output/evidence/claim-inventory.tsv)

The inventory found 14 syntax-declaration blocks, one configuration, 2,837
rules, and three target claims. There are four `[function]` declarations, of
which two are `[total]`; two `[owise]` rules; and no opaque/symbolic
declarations, priority rules, `[functional]` declarations, or simplification
rules.

### Complete local syntax inventory

| File/lines | Declarations |
|---|---|
| `semantic.k:6-21` | `Module`; recursive `Stmts`; `Stmt` forms `FuncDef` and `Return`; `Strings`; `Params`; `Exprs`; expression forms `Str`, `Name`, `Attribute`, and `Call` |
| `semantic.k:34-43` | values `strVal`, `function`, `boundStringMethod`; `KResult ::= Value`; control items `#invoke`, `#attribute`, `#callNoArgs`, `#return`, `#endCall` |
| `semantic.k:88` | `pySwapCase(String) [function]` |
| `semantic.k:89` | `utf8CharLen(String) [function, total]` |
| `unicode-case.k:6` | `pySwapChar(String) [function, total]` |
| `verification.k:8` | `flipSpec(String) [function]` |

The configuration has exactly the state used by this program: `<k>`, `<arg>`,
`<functions>`, and `<env>`. There is no heap, output, exception, allocation,
or call-stack state for the exact program to mutate.

### Construct-to-rule map

Every constructor in `solution.mpy` is covered:

| Used construct | Declaration | Executing rule(s) |
|---|---|---|
| `Module` | `semantic.k:6` | line 55 |
| `FuncDef` / `Params` | lines 11, 15 | lines 58, 60 |
| `Return` | line 12 | lines 67, 82 |
| `Call(..., .Exprs)` | lines 17, 21 | lines 78-80 |
| `Attribute` | line 20 | lines 74-76 |
| `Name` | line 19 | lines 69-70 |

`Str` is not in the submitted body, but its line-72 rule is used by the
reviewer's body-sensitivity mutation. The general recursive statement-list
rule is sound and harmless for this one-statement module.

### All 19 rules in `semantic.k`

| Start line | Rule and decision |
|---:|---|
| 55 | `Module(BODY)` schedules the actual body followed by an exact `flip_case` invocation. This is the HumanEval harness, not a result shortcut. It reads `<arg>` and does not alter it. |
| 58 | `S REST => S ~> REST` supplies left-to-right statement sequencing. |
| 60 | `FuncDef` installs the untranslated params/body in `<functions>`. |
| 63 | `#invoke` selects the stored binding, schedules that exact body and `#endCall`, and binds the single parameter in an initially empty `<env>`. |
| 67 | `Return(E)` schedules evaluation of `E` before `#return`. |
| 69 | `Name(N)` retrieves the matching value from `<env>`. |
| 72 | `Str(S)` produces `strVal(S)`. |
| 74 | `Attribute(E, NAME)` evaluates its receiver first. |
| 75 | A string receiver becomes `boundStringMethod(NAME,S)` without state change. |
| 78 | A zero-argument `Call` evaluates its callee before `#callNoArgs`. |
| 79 | The exact bound name `"swapcase"` consumes `#callNoArgs` and returns `strVal(pySwapCase(S))`. This is the one external-Python-primitive bridge; detailed below. |
| 82 | A returned `Value` consumes `#return ~> #endCall` and clears the local environment. It neither drops nor invents an admitted continuation. |
| 91 | `pySwapCase("") = ""`, the recursion base. |
| 92 | Nonempty `pySwapCase` swaps one computed-width byte sequence and recurses on the suffix. On a valid encoded input the suffix is strictly shorter. |
| 101 | Leading byte below 128 has width 1. |
| 103 | Leading byte in `[192,224)` has width 2. |
| 106 | Leading byte in `[224,240)` has width 3. |
| 109 | Leading byte in `[240,248)` has width 4. |
| 112 | The `owise` width-1 fallback covers other byte strings, including malformed encodings. |

The four explicit width guards are disjoint; the `owise` rule is their
complement. `utf8CharLen` is therefore covered as declared `[total]`.
`pySwapCase` has disjoint empty/nonempty rules. Its termination argument is
needed only for valid Python encodings; the proof remains a partial-correctness
proof for arbitrary K byte strings.

The operational `swapcase` bridge is context-safe for the modeled operation.
It matches an already bound string receiver, the exact method name, and zero
arguments. Python `str.swapcase` has no modeled receiver mutation or external
state effect and returns normally for a `str`; the rule preserves `<arg>`,
`<functions>`, and `<env>`, returns a value into the existing continuation,
and introduces no abrupt control. Changing just this bridge to identity made
the original `"Hello"` proof reach `strVal("Hello")` and fail, so proof closure
is sensitive to it.

### All 2,817 rules in `unicode-case.k`

The helper consists of:

- 2,816 distinct ground `pySwapChar` equations, one for each CPython 3.10.12 /
  Unicode 13.0 code point whose `swapcase()` differs;
- one final `pySwapChar(C) => C [owise]` rule.

Every individual equation is represented as its own row in
`rule-inventory.tsv`. The independent audit decoded every K byte literal and
compared it with `chr(codepoint).swapcase().encode("utf-8")` for all
1,114,112 code points. Results:

```text
explicit rules:          2816
expected mapped points:  2816
duplicates:              0
missing:                 0
extra:                   0
wrong right-hand sides:  0
multi-code-point RHS:    76
LHS widths:              52/910/1404/450 for 1/2/3/4 bytes
owise rules:             exactly 1
```

Thus the explicit guards are pairwise disjoint, the `owise` rule covers their
exact complement, and the `[total]` declaration is justified in the Haskell
byte-string interpretation. Evidence:
[05-unicode-rule-audit.log](/audit-output/evidence/logs/05-unicode-rule-audit.log).

### The sole rule in `verification.k`

`flipSpec(S) => pySwapCase(S)` is a transparent definitional wrapper. It has
no guard, overlap, recursion, opacity, priority, or simplification attribute.
It names the postcondition but does not replace execution; execution reaches
`pySwapCase` through the source program's method call independently.

### Static conclusion and the LLVM witness

No individually false rule was found under the Haskell UTF-8-byte
representation used to compile and prove the claims. In particular, the
Unicode table is not an unconstrained oracle: its complete finite domain is
fixed by checked ground equations plus the checked complement rule.

The narrower evidence gap is backend interpretation. The same source-level
escaped literals do not match non-ASCII runtime substrings under LLVM. The
concrete `Straße Δelta` witness above demonstrates the resulting false Python
execution conclusion for that backend. This is why the review does not award
an unqualified pass. It is not labeled as a false proof-local equation in the
Haskell theory, because that theory's concrete runs and exhaustive byte
mapping checks agree with the stated encoding bridge.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. The reviewer created
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k), retaining the exact
program and realizable `"Hello"` initial state but changing the required result
from `"hELLO"` to the false `"hELLo"`.

The mutation dry-run built successfully (exit 0). Actual proof exited 1 with
`WarnStuckClaimState` after real execution reached:

```text
<k> strVal("hELLO") ~> .K </k>
```

That residual is the expected unmet result obligation, not a parser failure,
missing import, timeout, or unrelated crash.

As separate body-sensitivity evidence,
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k) replaced
the submitted body with `Return(Str("WRONG"))` while retaining the original
expected result. It built, executed to `strVal("WRONG")`, and failed. The
`swapcase`-to-identity semantic mutation also built and failed the original
example at `strVal("Hello")`.

Evidence:

- [06-vacuity-dry-run.log](/audit-output/evidence/logs/06-vacuity-dry-run.log)
- [06-vacuity-proof.log](/audit-output/evidence/logs/06-vacuity-proof.log)
- [06-body-mutation-proof.log](/audit-output/evidence/logs/06-body-mutation-proof.log)
- [06-bridge-mutation-diff.log](/audit-output/evidence/logs/06-bridge-mutation-diff.log)
- [06-bridge-mutation-proof.log](/audit-output/evidence/logs/06-bridge-mutation-proof.log)

The proof is non-vacuous, result-sensitive, body-sensitive, and primitive-rule
sensitive.

## 7. Proven versus assumed accounting

### What is machine-checked

Relative to the freshly compiled Haskell definition, the universal reachability
claim establishes:

> For every K `String` byte sequence `S`, if the exact submitted translated
> module starts with argument `S` and empty function/environment maps and the
> execution reaches the modeled return, then it returns
> `strVal(pySwapCase(S))`, installs the exact submitted function body, preserves
> the argument, and clears the local environment.

The two ground claims additionally establish the documented ASCII result and
the encoded Unicode result. This is partial correctness; it is not a K theorem
of total termination for every arbitrary malformed byte sequence.

### Trust and assumption ledger

| Boundary | Effect | Assessment and support |
|---|---|---|
| Trusted `py2mpy.py` | Program identity | Acceptable. Trusted translator regeneration is byte-identical, and parsed KAST is pinned to the claim. |
| K Haskell backend and imported `BOOL`, `INT`, `MAP`, `STRING` hooks | Parsing, maps, equality, concatenation, length, substring, `ordChar` | Necessary low-level trust boundary. No local redefinition bypasses it. K's incomplete Unicode support motivates the explicit byte model. |
| UTF-8 / `surrogatepass` encoding from Python `str` to Haskell K `String` bytes | Connects formal `S` to source-language input | Concerning but usable. It is described informally in `semantic.k`, not expressed by a formal precondition or a machine-checked encoder theorem. Distinguishing and surrogate witnesses support it. |
| `str.swapcase` as an external Python primitive | Determines the program's returned value | Acceptable as an external primitive because it is outside the program-defined function body and is also the trusted canonical operation. It is not left opaque: all 2,816 changing code points and the complement are fixed and exhaustively checked. |
| CPython 3.10.12 / Unicode 13.0 mapping | Version-specific case results | Explicitly pinned by the generated helper and current trusted runtime. Exact regeneration and exhaustive rule comparison support it. A different Python Unicode database could change the bridge. |
| Characterwise composition of `swapcase` | Lifts checked single-character equations to strings | Ordinary induction on a finite encoded string: width decoding consumes one encoded scalar, applies its exact mapping, and recurses on the suffix. Concrete 1/2/3/4-byte boundary tests support the hook behavior. |
| Candidate-vs-canonical differential | Implementation fidelity | Finite evidence only. It found zero mismatches, but both sides call the same primitive; source-body identity and the K proof do the substantive work. |
| Haskell-only Unicode behavior | Proof-to-runtime portability | Material concern. Haskell matches Python under the byte bridge; LLVM does not. No claim of backend-independent Unicode correctness is justified. |

There are no opaque symbols, trusted auxiliary claims, circular loop
invariants, simplification lemmas, result oracles, or unproved program-defined
helpers.

### Gate summary

- **Real-program soundness:** passes for the Haskell definition. The exact body
  executes, state/control footprints match the used program, the result
  primitive is fully defined rather than opaque, and body/result/bridge
  mutations fail.
- **Intent adequacy:** passes with a documented limitation. The Haskell
  UTF-8-byte interpretation covers the intended Python strings (including the
  demonstrated reversible surrogate bridge), but that encoding connection is
  informal and the LLVM backend contradicts it on normal Unicode.
- **Evidence auditability:** passes. Scripts, deterministic inputs, exact
  commands, exit statuses, positive `#Top` outputs, negative residuals, and the
  complete rule inventory are preserved under `/audit-output/evidence`.

Accordingly, the proof is legitimate but carries a substantial,
backend-specific semantics concern.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
