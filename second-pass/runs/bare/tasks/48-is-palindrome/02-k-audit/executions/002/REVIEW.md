# Independent adversarial audit: 48-is-palindrome

The candidate reconstructs to a real, result-constraining K reachability proof of
the submitted constructor term, but not to a legitimate proof of the real Python
program on its source-contract domain. The decisive defect is the generated
semantics for `text[::-1]`: it claims Unicode-code-point reversal while actually
reversing the K backend's string units/bytes outside Latin-1. A one-character
Python string such as `"Ā"`, `"中"`, or `"🙂"` is necessarily a palindrome, but
both freshly rebuilt K backends return `false`.

## 1. Input and provenance integrity

I treated every candidate and generation record as untrusted evidence.

- `/audit-input.json` declares `record_layout =
  legacy-selected-stage1`, condition `bare`, problem `48-is-palindrome`, and
  `semantics_mode = GENERATED_SEMANTICS`.
- The campaign object in `/audit-campaign-lock.json` is exactly equal as parsed
  JSON to `audit_input.audit_campaign`. Its independently computed SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  equal to the recorded hash.
- The required legacy-selected-stage1 records are regular, readable files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`. The optional-present `usage.json` was
  also inspected. Historical `runtime-metrics.json` is not required for this
  layout.
- The declared run, task, stage-result, invocation, metrics, prompt, usage,
  final-message, and output-log SHA-256 values all match their mounted bytes.
  The evidence maps in `generation-result.json` and `invocation.json` are
  identical, and every listed evidence-file hash matches. The single structured
  trace file has SHA-256
  `88f9dd14f745816d22fa5a08d9e3a4949c6881a20be684fe80bf6485fa6754b4`;
  all 165 JSONL events parse. Independent per-entry candidate and trace
  inventories, rather than host provenance paths, are recorded in the log.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py` at
  SHA-256
  `6d590205867a7577346310fe8cba6e45655e25a7ef57acb964a6d34b02363081`.
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py` at
  SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- No symlinked entry occurs in the candidate, reference, or generation-evidence
  trees. The launcher-declared mounts are read-only.
- The generated-semantics boundary is intact:
  `/reference/reference-semantics` does not exist, the two corresponding
  audit-input hashes are null, and no hidden/supplied semantics was sought or
  used.
- The structured trace and prose record only the generator's claims that it
  compiled, ran four examples, and saw `#Top`. They were not used as proof
  authority. The trace records the same session ID and Codex version as the
  manifests, and its claims were independently reconstructed below.

Evidence:
`evidence/01-provenance.log`,
`evidence/19-mount-readonly.log`, and
`evidence/20-generation-trace-summary.log`.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for an input Python `str`, return whether the
entire sequence of characters reads the same forwards and backwards. The empty
string is a palindrome. The prompt imposes neither an ASCII/Latin-1 restriction
nor a length bound. The trusted canonical implementation compares symmetric
Python string elements and therefore applies to ordinary Unicode Python
strings.

The submitted implementation is:

```python
def is_palindrome(text: str):
    return text == text[::-1]
```

This is a different but source-equivalent algorithm. Running the trusted
translator on the scratch copy generated `regenerated-solution.mpy` with
SHA-256
`8278b02d667e625ef15bdd083acb6461d92384f78a36828c230508569475e863`,
byte-identical to the submitted `solution.mpy`.

The reviewer-authored differential test imports the trusted canonical entry
point and the scratch candidate entry point independently. It tests all four
prompt examples, empty/singleton/two-character boundaries, mismatches at
different positions, whitespace, NUL/control characters, combining text,
non-BMP characters, and 2,640 seeded generated cases of lengths 0 through 32.
All 2,662 cases returned actual `bool` values and had zero mismatches (1,416
true and 1,246 false results).

Evidence:
`evidence/02-translation-identity.log`,
`evidence/differential_test.py`, and
`evidence/03-python-differential.log`.

This establishes strong finite evidence for Python implementation fidelity. It
does not validate the generated K string semantics.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/source`; no candidate-built
definition or cache was copied or reused.

Fresh concrete build:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled-llvm
```

Exit 0. Evidence: `evidence/04-kompile-concrete.log`.

Fresh proof build:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-haskell
```

Exit 0. Evidence: `evidence/05-kompile-proof.log`.

There is exactly one positive target claim in `spec.k`. Its independent run was:

```text
kprove spec.k --definition verification-kompiled-haskell --spec-module SPEC
```

It exited 0 and printed exactly `#Top`. Evidence:
`evidence/06-kprove-positive.log`.

The generated semantics nevertheless fails the required concrete
reconstruction gate. The final 23-case LLVM comparison used both Python
implementations as oracles and found six mismatches:

| Satisfying Python input | Python result | Fresh K result |
|---|---:|---:|
| `"e\u0301x\u0301e"` | `true` | `false` |
| `"Ā"` (U+0100) | `true` | `false` |
| `"中"` | `true` | `false` |
| `"🙂"` | `true` | `false` |
| `"🙂🙃🙂"` | `true` | `false` |
| `"𐀀x𐀀"` | `true` | `false` |

The immediately adjacent boundary `"ÿ"` (U+00FF) returns `true` in both, while
the next code point `"Ā"` (U+0100) returns `true` in Python and `false` in K.
The comparison log intentionally exits 1 when it finds mismatches.
`evidence/07c-k-semantics-differential.log` is the authoritative final run.
`evidence/07-k-semantics-differential.log` preserves an earlier reviewer regex
bug, and `evidence/07b-k-semantics-differential.log` preserves the first
correctly parsed mismatch run; neither is attributed to the candidate.

A value-bearing witness executes the same slice rule but returns the slice
itself. Python leaves each one-character string unchanged. Fresh K instead
produces:

```text
"é"  -> "\xe9"
"Ā"  -> "\x80\xc4"
"中" -> "\xad\xb8\xe4"
"🙂" -> "\x82\x99\x9f\xf0"
```

Thus the helper reverses the multi-byte encoding, not Python Unicode code
points. Evidence: `evidence/unicode-slice-witness.mpy` and
`evidence/08-unicode-slice-witness.log`.

The fresh Haskell definition used by the proof has the same observable defect:
it returns `true` for `"é"` but `false` for each of `"Ā"`, `"中"`, and `"🙂"`.
Evidence: `evidence/10-haskell-unicode-concrete.log`.

The clean positive `#Top` is real, but it closes under a materially false model
of the submitted Python program.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole claim has no `requires` precondition. For every K `String` `S`, it
starts with:

- the complete submitted `Module(FuncDef(...))` constructor in `<k>`, followed
  by `#invoke("is_palindrome", PyString(S))`;
- an empty function map; and
- an empty environment.

It requires termination with:

- `<k>` equal to `PyBool(isPalindrome(S))`;
- the function map containing the submitted parameter and body; and
- the environment restored to empty.

`isPalindrome(S)` is defined as
`S ==String reverseString(S)`. The result is not a free variable, existential,
tautological cell frame, or one-way implication. The false-postcondition probe
in stage 6 confirms that this result position is discriminating.

### Program identity

The mechanical constructor parser compares the trusted-regenerated submitted
`Module` term with the entry claim's `Module` term, then separately compares
the claimed `#function` parameter/body and `#invoke` target. All comparisons
pass. The normalized constructor has reviewer-computed SHA-256
`87f3c330d21704dfef2830067fe6717f51952210d14d66765ab80732a7658904`.
Evidence: `evidence/claim_pinning_check.py` and
`evidence/09c-claim-pinning.log`. Two earlier reviewer-script diagnostics
(`09-claim-pinning.log` and `09b-claim-pinning.log`) are preserved and were
fixed without changing candidate sources.

There are no helper or loop claims. The operational claim executes the actual
submitted body.

### Satisfiable states and substitutions

Because there is no precondition, the exact initial cells with `S = ""` are a
satisfying state. Fresh execution reaches `PyBool(true)`, agreeing with both
Python functions. `S = "ab"` reaches `PyBool(false)`, also agreeing with both.
But `S = "Ā"` is equally satisfying and reaches `PyBool(false)` in K while both
Python functions return `true`. The universal entry domain therefore includes
a concrete counterexample to the source-level conclusion.

### Body sensitivity

A separate operational-sensitivity mutation changes the term actually executed
by the claim, in both the initial module and expected retained function binding,
to `return text == text`, while leaving the original palindrome postcondition.
It dry-runs successfully. Concrete execution on `"ab"` returns `true`, and
`kprove` exits 1 with `WarnStuckClaimState` and the residual comparison
`S ==String S` versus the original reverse predicate.

Evidence:
`evidence/spec-body-mutation.k`,
`evidence/body-mutation.mpy`,
`evidence/11-body-mutation-dry-run.log`,
`evidence/12-body-mutation-concrete.log`, and
`evidence/13-body-mutation-kprove.log`.

Program pinning and body sensitivity pass. Intent adequacy fails because the
result-bearing string reversal is not Python reversal on the material source
domain.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

`semantic.k` declares:

1. `Program ::= Module(Stmt)`.
2. `Stmt ::= FuncDef(String, Params, Stmt) | Return(Expr)`.
3. `Params ::= Params(String)`.
4. `Expr ::= Name(String) | Int(Int) | Str(String) |
   UnaryOp(String, Expr) | Subscript(Expr, Slice) |
   Compare(Expr, CmpOp) | PyVal`.
5. `CmpOp ::= CmpOp(String, Expr)`.
6. `Slice ::= Slice(Bound, Bound, Bound)`.
7. `Bound ::= Expr | NoBound`.
8. `PyVal ::= PyString(String) | PyInt(Int) | PyBool(Bool)`.
9. Internal `Function ::= #function(String, Stmt)`.
10. Internal `KItem` forms `#load`, `#invoke`, `#return`, `#returnFrame`,
    `#compareRight`, `#compareValues`, `#applySlice`, and `#unaryMinus`.
11. `reverseString(String)` and `reverseStringN(String, Int)`, both
    `[function]`.

`verification.k` declares `isPalindrome(String)` as a `[function]`.

The configuration has exactly `<k>`, `<functions>`, and `<env>` beneath
`<py>`. There are no local `[total]` or `[functional]` declarations, opaque
symbols, priorities, `owise` rules, macros, anywhere rules, simplification
rules, or concrete-only rules. `spec.k` contains one ordinary reachability
claim. There are no generated helper K files.

The complete annotated source and attribute search are preserved in
`evidence/14-source-rule-inventory.log`.

### Construct coverage

Every constructor in `solution.mpy` is declared and has a target path:

- `Module`, `FuncDef`, and `Params` use the load rules at semantic lines 53-60.
- `Return` uses lines 63-65.
- `Compare`/`CmpOp("==", ...)` use lines 77-81.
- Both `Name("text")` occurrences use lines 70-71.
- `Subscript` and the exact `Slice(NoBound, NoBound,
  UnaryOp("-", Int(1)))` use lines 84-87.
- `UnaryOp` and `Int` are present syntactically in the slice pattern. The
  special slice rule matches this pure literal step directly; omitting separate
  evaluation of that literal has no state, exception, or ordering effect for
  this exact program.

`Str`, general integer evaluation, and executable unary-minus rules are
additional minimal-subset support but are not reached by this submitted body.
Missing behavior for other Python constructs is not a defect in generated
semantics.

### Complete ordinary-rule inventory and judgment

| Rule | Role | Static judgment |
|---|---|---|
| `semantic.k:53` | `Module(FD)` schedules `#load(FD)` | Sound for the exact one-function module; continuation is preserved. |
| `55-56` | Load `FuncDef` into initially empty map | Sound for the exact initial configuration and submitted module. |
| `58-60` | Invoke singleton-bound function, save old env, bind parameter | Sound for this already-valued single argument and body. It reads the selected binding and preserves the old env in the frame. |
| `63` | Evaluate `Return(E)` before return marker | Sound and preserves evaluation order. |
| `64-65` | Return `PyVal`, consume frame, restore env | Sound for the exact call stack; return value and trailing continuation are preserved. |
| `68` | `Int(I)` to `PyInt(I)` | Ordinary faithful literal rule; not independently executed in the target slice path. |
| `69` | `Str(S)` to `PyString(S)` | Ordinary faithful literal rule; unused by the target. |
| `70-71` | Singleton-env name lookup | Sound for the target's singleton local environment. |
| `73` | Schedule unary-minus operand | Correct evaluation order; unused as a runtime step in the target. |
| `74` | Negate `PyInt` | Correct unbounded-integer arithmetic; unused as a runtime step in the target. |
| `77` | Evaluate comparison left operand | Correct left-to-right ordering. |
| `78-79` | Then evaluate right operand and retain left/operator | Correct for the target and preserves value/control. |
| `80-81` | Python-string-shaped equality via K `==String` | Correct equality of represented K strings for the target operands. |
| `84` | Evaluate subscript base, retain slice | Correct base-before-slice ordering for the target; the retained exact literal slice has no effects. |
| `85-87` | Replace Python `s[::-1]` with `reverseString(S)` | **Materially unsound operational bridge on the intended domain.** See the concrete false-conclusion witness below. |
| `94` | Define `reverseString(S)` through K `lengthString` | Deterministic helper equation, but it selects the backend's unsupported units beyond Latin-1; it does not establish Python code-point reversal. |
| `95` | Zero-length reverse is empty | True base equation. |
| `96-98` | Prepend `substrString(S,N-1,N)` and recurse for `N>0` | Guard is disjoint from zero and recursion descends. With K's hooks it reverses backend units/bytes; it is not a universal Python-Unicode connection theorem. Negative `N` is uncovered, but the helper is not `[total]` and target calls it only with nonnegative `lengthString`. |
| `verification.k:8` | Define `isPalindrome(S)` using the same `reverseString` | Internally definitional, but inadequate as the source postcondition and circular as evidence for the slice bridge: the same result-bearing summary appears in execution and the destination. |

There are no rule overlaps or priority interactions on the target path.
Function guards for `reverseStringN` are disjoint, and every target-created
nonnegative `N` is covered by zero or positive cases. State consists only of
the function map and environment; the audited rules preserve or restore both.
The target has no heap, allocation, I/O, exceptions, mutation, loops, or
multiple calls requiring additional cells.

### Required false-conclusion witness for the unsound rule

The installed K 7.1.293 `domains.md` explicitly states that its hooked Unicode
string implementation is incomplete and does not fully support encodings/code
points beyond the first 256 code points (Basic Latin and Latin-1 Supplement).
The candidate nevertheless comments that lines 94-98 reverse “by Unicode code
point” and uses that helper as the exact semantics of Python `s[::-1]`.
Evidence: `evidence/15-k-string-boundary.log`.

Take the satisfying intended input `S = "Ā"` (U+0100), a one-code-point Python
string. Python's material operation has the conclusion:

```text
"Ā"[::-1] == "Ā"
```

Candidate rule 85-87 instead enables:

```text
Subscript(... exact -1 slice ...) => PyString(reverseString("Ā"))
                                    => PyString("\x80\xc4")
```

Consequently the submitted program returns `true` in both trusted/candidate
Python executions but `false` in both fresh K definitions. `"中"` and `"🙂"`
give the same kind of false conclusion. This is a concrete witness over the
intended input domain, not merely an untested concern.

No bridge-free universal connection theorem relates `reverseString` to Python
slice execution. The helper's use on both the operational side and in
`isPalindrome` makes the positive proof close without establishing the missing
connection. Finite Latin-1 examples cannot supply that theorem.

Gate A (real-program soundness): **FAIL**.  
Gate B (intent/domain adequacy): **FAIL**. The source contract is not restricted
to Latin-1; imposing that restriction would materially narrow HumanEval's
Python `str` domain.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I created a fresh proof module containing
the exact submitted program term and cells but changed the result obligation
from `PyBool(isPalindrome(S))` to `PyBool(false)`.

- The mutation parses and builds under `--dry-run` with exit 0. The only
  diagnostic is an expected unused-RHS-variable warning.
- The satisfying witness `S = ""` executes under the fresh concrete definition
  to `PyBool(true)`, so the mutation is demonstrably false and reachable.
- The actual mutated `kprove` exits 1 with `WarnStuckClaimState`. Its residual
  retains the executed final value
  `PyBool(S ==String reverseStringN(S, lengthString(S)))` and the unmet
  condition requiring `S` to equal its reverse in order to unify with the
  fixed `false` destination. This is the expected result obligation, not a
  parser error, timeout, missing import, or unrelated crash.

Evidence:
`evidence/spec-vacuity-audit.k`,
`evidence/16-vacuity-dry-run.log`,
`evidence/17-vacuity-empty-witness.log`, and
`evidence/18-vacuity-kprove.log`.

The K claim is non-vacuous and result-constraining under the supplied theory.
That does not cure the theory's false Python-slice bridge.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate-generated `SEMANTIC` rules and K 7.1.293 hooks, for every K
`String` `S`, executing the exact submitted constructor module from empty
function/environment cells reaches:

```text
PyBool(S ==String reverseString(S))
```

with the submitted function binding retained and the environment restored.
This is a genuine partial-correctness reachability theorem in that K theory.
Operationally, `reverseString` behaves as backend-unit/byte reversal beyond the
documented Latin-1 boundary. Therefore the theorem does not establish that the
real Python function returns whether an arbitrary Python `str` is a palindrome.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 compiler, LLVM/Haskell backends, and `kprove` reachability engine | Parsing, execution, and proof closure | Ordinary low-level proof-tool trust; both definitions were rebuilt from source. |
| Trusted `/reference/py2mpy.py` | Python-AST to constructor identity | Acceptable benchmark trust. Byte identity and constructor-level claim comparison were checked independently. |
| K Map, Int, Bool, and string-equality hooks | Binding/state, arithmetic, guards, final equality | Acceptable for the exact modeled operations, subject to the explicit string-representation limitation below. |
| K `STRING.length`, `STRING.substr`, and `STRING.concat` hooks | Every computed reverse and therefore the returned Boolean | **Illegitimate as an unconditional Python-Unicode bridge.** Installed documentation states the limitation, and U+0100/non-BMP witnesses produce wrong values. |
| Candidate call/return/name/compare rules | Binding, order, control, retained function map, restored env | Target-specific but manually exhaustive and body-sensitive; acceptable for this simple body. |
| `Subscript(...[::-1]) => reverseString(S)` | Replaces the material Python slice and determines the return value | **Illegitimate operational bridge.** No independent connection theorem; concrete false conclusion witness. |
| `reverseString` reused by `isPalindrome` | Both program-derived value and postcondition | Not opaque, but circular as source-correctness evidence. Its equations fix the wrong value outside Latin-1. |
| Trusted canonical Python implementation and CPython differential tests | Implementation fidelity and concrete bridge checks | Finite empirical evidence only. They support Python-to-Python equivalence and expose the K mismatch; they are not a substitute for a K connection proof. |

There are no opaque external symbols, proof-local simplification axioms,
priority rules, auxiliary lemmas, or loop invariants to credit. The candidate's
`#Top`, prose, and generation traces establish no additional trusted fact.

### Decision

The positive claim reconstructs and is non-vacuous, and the claim pins the
actual submitted constructor body. Nonetheless, the generated semantics makes
a false result-bearing conclusion on ordinary satisfying Python strings. At
best the construction would be limited to a Latin-1-like subdomain, which is a
material narrowing not stated by the HumanEval source contract. Under the
benchmark's explicit decision boundary, that is not a concern-only result; it
is not a legitimate proof of the requested unrestricted program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
