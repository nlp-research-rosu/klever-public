# Independent adversarial audit: 89-encrypt

This is a completed seven-stage audit of the immutable candidate in
`/candidate`, under `SUPPLIED_SEMANTICS`. The candidate is not legitimate.
There are two independently decisive defects:

1. The generated Python program does not implement the full trusted source
   contract. It rotates every character, whereas the canonical program
   preserves characters outside `a` through `z`.
2. The proof-local loop-summary rule is materially broader than the loop claim
   used to justify it. A ground binding-shadowing witness makes the rule prove
   the false result `"e"` when fixed semantics executes the same loop to `"m"`.

The fresh positive proof runs nevertheless succeed. That confirms that the
failure is one of legitimacy and adequacy, not a missing tool or a failed
reconstruction.

## 1. Input and provenance integrity

### Launcher records and mode

`/audit-input.json` declares:

- problem `89-encrypt`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The mounted `/reference/reference-semantics` tree is present, as required for
this mode. There is no rendered-mode/mount contradiction and therefore no
audit-infrastructure breach.

I read the launcher-owned audit input and campaign lock before treating any
candidate material as evidence. The JSON object in
`/audit-campaign-lock.json` is field-for-field equal to the `audit_campaign`
block in `/audit-input.json`; its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the recorded hash.

All records required by `legacy-selected-stage1` are present, readable,
regular, non-symlink files:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`

`/generation-evidence/usage.json` is also present and was inspected. Historical
runtime metrics are absent, which is permitted for this declared legacy
layout. The structured trace consists of one regular, non-symlink JSONL file;
all 318 lines parse as JSON. I inspected the trace event inventory, generation
messages, tool calls and bounded tool-output summaries. The generation record
claims two successful proofs, but that claim was not trusted.

Every recorded file hash that maps to a mounted file was recomputed. The run
manifest, task manifest, stage result, invocation, metrics, usage, generation
prompt, final text, output log, trusted canonical, trusted prompt, trusted
translator, and the individual structured-trace file all match their recorded
SHA-256 values. The stage result and invocation also independently record
hashes for `legacy-metrics.json`, `legacy-run-input.json`, and every trace
artifact; those all match.

Evidence:

- `evidence/logs/01-provenance-check.log`
- `evidence/logs/01-provenance-hashes.log`
- `evidence/logs/01-generation-trace-summary.log`
- reviewer scripts `evidence/scripts/provenance_check.py` and
  `evidence/scripts/generation_trace_summary.py`

### Trusted-input comparisons

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive comparison of
path names, entry types, and file bytes shows that
`/candidate/reference-semantics` is exactly equal to
`/reference/reference-semantics`: no entry is missing, added, changed,
mistyped, or symlinked. The trusted semantics tree itself contains no symlink.

The five required proof artifacts—`solution.py`, `solution.mpy`, `spec.k`,
`verification.k`, and `prove.sh`—are regular, non-symlink files. Candidate and
trusted entry types and independently computed per-file hashes are preserved
in:

- `evidence/logs/01-integrity-comparisons.log`
- `evidence/logs/01-artifact-types.log`
- `evidence/logs/01-candidate-file-hashes.log`

Conclusion for stage 1: **integrity passes; no infrastructure failure**.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

`/reference/prompt.py` asks for `encrypt(s)`, rotating the alphabet by
`2 * 2`, i.e. four positions, and gives the examples:

- `"hi"` to `"lm"`
- `"asdfghjkl"` to `"ewhjklnop"`
- `"gf"` to `"kj"`
- `"et"` to `"ix"`

The prompt says the argument is a string and gives no lowercase-only
precondition. `/reference/canonical.py` makes the branch boundary precise: for
each character, rotate it four positions only if it occurs in
`"abcdefghijklmnopqrstuvwxyz"`; otherwise append it unchanged. Thus the trusted
contract covers general strings, with lowercase ASCII letters shifted and all
other characters preserved.

The candidate `/candidate/solution.py` instead executes this expression for
every character:

```python
chr((ord(char) - 97 + 4) % 26 + 97)
```

There is no membership test or other branch preserving non-lowercase input.

### Translation identity

I regenerated the constructor program with the trusted translator:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/89-encrypt-review/solution.regenerated.mpy
```

The regenerated and submitted files have the same SHA-256
`6947167ad520ec343c0075278bcd1c4fdfb8e0db9daefaa3c9d2516a9de85511`
and are byte-identical. Evidence:
`evidence/logs/02-translation-byte-identity.log`.

### Independent differential test

`evidence/scripts/differential_test.py` independently loads the trusted
canonical and generated candidate entry points. It covers all four documented
examples, empty input, the lower-alphabet wrap boundary, every important
lower/non-lower transition around `a` and `z`, uppercase letters, digits,
punctuation, whitespace, control characters, mixed strings, non-ASCII
characters, and 65 deterministic generated strings of lengths 0 through 64.

Exact command:

```text
python3 /audit-output/evidence/scripts/differential_test.py
```

It found 76 mismatches among 90 cases and exited 1 to report the divergence.
Representative results are:

```text
input='A'     canonical='A'     candidate='y'
input='0'     canonical='0'     candidate='h'
input='aZ-9z' canonical='eZ-9d' candidate='exeqd'
input='é'     canonical='é'     candidate='k'
```

The four examples and lowercase-only cases agree. The mismatch is nevertheless
material because neither the prompt nor signature restricts the input to
lowercase strings, and the canonical’s explicit `else` branch defines this
behavior. This is not thin testing used as a universal proof: the concrete
counterexamples themselves refute implementation-to-contract equivalence.

Evidence: `evidence/logs/02-differential.log`.

Conclusion for stage 2: **program fidelity fails on the documented string
domain**.

## 3. Clean proof reconstruction

All candidate-built definitions and caches were ignored. Source files needed
for execution were copied into `/tmp/audit-work/89-encrypt-review`; its
`reference-semantics` came from the trusted mount. The toolchain was independently
checked as K `v7.1.293`.

### Concrete definition

Fresh commands and results:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled
# exit 0

krun concrete-tests.mpy --definition runtime-fresh-kompiled
# exit 0; final <k> .K </k>, NoExc, exit-code 0
```

Evidence:

- `evidence/logs/03-kompile-runtime.log`
- `evidence/logs/03-krun-candidate-tests.log`

### Loop proof

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-fresh-kompiled
# exit 0

kprove --definition verification-fresh-kompiled spec.k \
  --spec-module LOOP-SPEC
# #Top, exit 0
```

Evidence:

- `evidence/logs/03-kompile-loop-proof.log`
- `evidence/logs/03-kprove-loop.log`

### Entry-point proof

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-WITH-LOOP \
  --syntax-module VERIFICATION-WITH-LOOP \
  --output-definition function-verification-fresh-kompiled
# exit 0

kprove --definition function-verification-fresh-kompiled spec.k \
  --spec-module FUNCTION-SPEC
# #Top, exit 0
```

Evidence:

- `evidence/logs/03-kompile-function-proof.log`
- `evidence/logs/03-kprove-function.log`

Both required positive claims therefore reconstruct. This establishes closure
under the supplied semantics plus the candidate’s proof extensions. It does
not validate those extensions or show that the theorem matches the HumanEval
contract.

Conclusion for stage 3: **fresh reconstruction passes**.

## 4. Adequacy and real-program pinning

### Plain-language claims

The `LOOP-SPEC` claim at `/candidate/spec.k:6` has no `requires` clause. For
arbitrary:

- remaining input codes `CS`;
- accumulated output codes `A`;
- old loop-variable string `OLD`; and
- original argument codes `INPUT`,

it starts at the real `#loop(str(CS), Name("char"), encryptLoopBody)` in
environment 1. Its scopes are specifically:

- scope 0 containing only `encrypt -> encryptClosure`, parent −1;
- scope −1 equal to `builtinsScope`;
- scope 1 containing `result -> str(A)`, `char -> OLD`, and
  `s -> str(INPUT)`, parent 0.

The heap must be empty. The post-state consumes the loop, replaces `result`
with `encryptAcc(A, CS)`, and leaves `char` as the last one-character input
string, or as `OLD` when `CS` is empty.

The `FUNCTION-SPEC` claim at `/candidate/spec.k:32` also has no `requires`
clause. For every `IntSeq CS`, it starts with the standard module and builtins
scopes, an empty heap and stack, `scopeLoc` 1, `heapLoc` 0, `noRet`, and
`NoExc`. It calls the bound `encrypt` closure with `str(CS)` and constrains the
result to exactly `str(encryptCodes(CS))`. The result is not a free variable,
tautology, or one-way implication.

Both preconditions are satisfiable. Examples include:

- loop state: `CS = .IntSeq`, `A = .IntSeq`, `OLD = str(.IntSeq)`,
  `INPUT = .IntSeq`;
- entry state: `CS = .IntSeq`, giving the empty-string call;
- non-empty entry state: `CS = iCons(104, iCons(105, .IntSeq))`, giving
  `"hi"`.

### Constructor-level identity

`evidence/scripts/constructor_pinning.py` mechanically parses the submitted
constructor term and the candidate macros. It confirms:

- top-level binding name is exactly `"encrypt"`;
- parameters are exactly `Params("s")`;
- after expanding `encryptLoopBody`, `encryptFunctionBody` is constructor-for-
  constructor equal to the regenerated `FuncDef` body;
- the loop body is constructor-for-constructor equal;
- `encryptClosure` is exactly
  `closureVal("s", encryptFunctionBody, 0)`.

The script exits 0. The fresh concrete module execution also displays the
loaded scope-0 closure with this exact constructor body. Evidence:

- `evidence/logs/04-constructor-pinning.log`
- `evidence/logs/03-krun-candidate-tests.log`

The entry claim therefore pins the real submitted generated program, allowing
only the demonstrated macro and statement-unit normalization.

### Satisfying ground results

`evidence/scripts/postcondition_witnesses.py` evaluates the K postcondition’s
mathematical code map against both Python implementations. On each tested
input, including `""`, `"hi"`, `"wxyz"`, the full alphabet, `"A"`,
`"aZ-9z"`, and `"é"`, the claimed summary equals the generated candidate.
For non-lowercase inputs it does not equal the canonical.

A separate translated K probe covers both ordinary and non-lowercase behavior:

```text
python3 /reference/py2mpy.py \
  /audit-output/evidence/scripts/k_concrete_probe.py \
  > /tmp/audit-work/89-encrypt-review/k_concrete_probe.mpy
krun /tmp/audit-work/89-encrypt-review/k_concrete_probe.mpy \
  --definition /tmp/audit-work/89-encrypt-review/runtime-fresh-kompiled
```

It checks, among other cases, that K execution returns `"y"` for `"A"` and
`"exeqd"` for `"aZ-9z"`; it exits 0 with no exception. Evidence:

- `evidence/logs/04-postcondition-witnesses.log`
- `evidence/logs/04-k-concrete-probe-translate.log`
- `evidence/logs/04-k-concrete-probe-krun.log`

### Body sensitivity

The mutation in
`evidence/mutations/verification-body-plus-one.k` changes the actual
constructor term executed by the loop from `Int(4)` to `Int(5)` while leaving
the claimed `encryptCode` summary at four. This is not a source-only mutation:
it changes `encryptLoopBody`, and therefore the closure body used by the loop
claim.

The mutated definition builds successfully. Its loop proof exits 1 with
`WarnStuckClaimState`; the residual explicitly compares the shift-four term
containing `C +Int -93` against the shift-five execution containing
`C +Int -92`. Evidence:

- `evidence/logs/04-body-mutation-kompile.log`
- `evidence/logs/04-body-mutation-kprove.log`

Conclusion for stage 4: **the formal claim is result-constraining and pins the
submitted program, but that program and result formula are inadequate for the
full trusted contract**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/scripts/k_rule_inventory.py` rebuilds a source-faithful inventory of
every declaration block in the trusted supplied semantics, candidate
verification, and candidate spec. The bounded command log
`evidence/logs/05-rule-inventory.log` contains the exact source path, line,
kind, attributes, and complete multiline block for all 946 entries:

- 233 syntax declaration blocks;
- 1 configuration;
- 5 contexts;
- 705 rules;
- 2 claims.

It includes 151 function-bearing blocks, 113 `total` blocks, 48 concrete
blocks, 29 `owise` blocks, 35 priority-bearing blocks, all macro declarations,
all symbol/no-evaluator declarations, and every continuation line belonging to
those declarations. There are no local `functional` or `simplification`
declarations.

Per-file review:

| File | Inventoried entries | Assessment |
|---|---:|---|
| `semantics/syntax.k` | 16 syntax | Constructor grammar; all submitted constructors declared. |
| `semantics/core.k` | 37 syntax, 1 configuration, 46 rules | Configuration, statement sequencing, scope lookup, values, builtins scope, and shared folds. Used rules are faithful at the supplied semantic level. |
| `semantics/iter.k` | 1 syntax | Iterator protocol declaration only. |
| `semantics/range.k` | 2 syntax, 6 rules | Structural range model; unused by this program. |
| `semantics/operators.k` | 2 contexts, 10 rules | Left-to-right dispatch and reference handling; the submitted arithmetic path is faithful. |
| `semantics/int.k` | 1 syntax, 16 rules | Integer arithmetic and Python-style positive-divisor modulo; used and mathematically valid here. |
| `semantics/bool.k` | 1 context, 13 rules | Boolean dispatch/short-circuiting; unused by the target body. |
| `semantics/float.k` | 34 syntax, 121 rules | Explicit opaque/concrete float trust boundary; unused by the target body. |
| `semantics/str.k` | 5 syntax, 28 rules | String iteration, concatenation and comparisons. Iteration/concatenation are used and match the code-sequence model. |
| `semantics/set.k` | 6 syntax, 12 rules | Structural string-set subset; unused. |
| `semantics/list.k` | 5 syntax, 27 rules | Allocation, list operations and membership; unused by the target. |
| `semantics/tuple.k` | 4 syntax, 21 rules | Target binding is used by `for`; the name-binding rule updates the active scope exactly. Other rules are unused. |
| `semantics/subscript.k` | 15 syntax, 2 contexts, 40 rules | Partial indexing/slicing subset; unused. Totalized opaque/out-of-bounds behavior is outside this theorem. |
| `semantics/comprehension.k` | 3 syntax, 7 rules | Macro lowering; unused. |
| `semantics/methods.k` | 27 syntax, 75 rules | String/list method subset; unused by the target. |
| `semantics/controls.k` | 3 syntax, 34 rules | Assignment, augmented assignment, `for`, loop protocol and control. The submitted control path is faithful. |
| `semantics/functions.k` | 4 syntax, 15 rules | Function binding, parameter binding, return and frame teardown. Used by the entry claim and faithful for this non-capturing closure. |
| `semantics/builtins.k` | 38 syntax, 137 rules | `ord` and `chr` are used. `ord` returns the singleton code and the program’s `chr` argument is always 97–122, inside the supplied `<128` guard. Remaining builtins are unused. |
| `semantics/call.k` | 3 syntax, 21 rules | Callee lookup, argument evaluation and closure/builtin dispatch; used and faithful on the standard binding path. |
| `semantics/sort.k` | 6 syntax, 19 rules | Explicit opaque sort boundary; unused. |
| `semantics/assert.k` | 3 rules | Runtime smoke-test assertion behavior; not part of either target claim. |
| `semantics/dict.k` | 12 syntax, 28 rules | Minimal dict model; unused. |
| `semantics/concrete.k` | 5 syntax, 16 rules | LLVM-only deep-equality/key-sort legs; not imported by either proof definition. |
| `verification.k` | 6 syntax, 10 rules | Five truthful summary/macro groups plus one unsound operational bridge, analyzed below. |
| `spec.k` | 2 claims | The loop and entry claims restated above. |

The supplied semantics intentionally models a Python subset rather than full
CPython. Material limitations include ASCII-only source string literal
conversion, incomplete exception behavior, limited container/method coverage,
and opaque float/sort/digest operations. None is exercised by the submitted
body in a way that affects its result: the entry claim begins with an arbitrary
`str(CS)` value, and the computed output is always lowercase ASCII. I found no
false-conclusion witness for a supplied-semantics rule on the actual target
path.

### Construct-to-rule map for `solution.mpy`

Every material constructor is modeled:

- `Module` and statement concatenation: `core.k` configuration and
  `#loadAll`/statement-sequencing rules.
- `FuncDef` and `Params`: `functions.k` closure binding.
- `Assign`, `Name`, and `Str`: `controls.k` assignment, `core.k` lookup, and
  `str.k` literal/code-sequence rules.
- `For`: strict iterable evaluation in `syntax.k`, `controls.k`’s `#loop`,
  `str.k`’s `#iterNext`, and `tuple.k`’s `#bindTgt`.
- `AugAssign`: `controls.k`, with string `+` in `str.k`.
- `Call`: `call.k` callee and left-to-right argument machinery.
- `ord` and `chr`: ordinary name lookup through `builtinsScope`, followed by
  `builtins.k` singleton-code rules.
- `BinOp("+", "-", "%")`: strict evaluation and dispatch in `operators.k`,
  integer cases and `pyMod` in `int.k`.
- `Return`: strict expression evaluation, abrupt return, stack restoration and
  frame removal in `functions.k`.

Thus no used source operation is silently fabricated or unmodeled.

### Candidate summary functions and macros

The local proof extensions before the bridge are acceptable:

- `encryptCode(C)` is a total definitional summary of the candidate’s arithmetic
  expression. Its single equation is true for every K integer under positive
  modulus 26.
- `encryptCodes` and `encryptAcc` are total, structurally recursive,
  non-overlapping functions. Base and constructor cases cover every `IntSeq`;
  recursive descent is on the tail.
- `lastChar` is total, structurally recursive and non-overlapping. It exactly
  captures Python’s retained loop variable for empty and non-empty sequences.
- `encryptLoopBody`, `encryptFunctionBody`, and `encryptClosure` are macros.
  The mechanical comparison in stage 4 establishes their exact submitted
  constructor terms; they introduce no opaque result.

No candidate-local function is an unconstrained oracle.

### Unsound operational bridge and false-conclusion witness

The rule at `/candidate/verification.k:66` is an operational bridge:

```k
rule <k>
       #loop(str(CS), Name("char"), encryptLoopBody)
       => .K
       ...
     </k>
     <env> 1 </env>
     <scopes>
       ...
       (1 |-> scope(..., parent(0)) => 1 |-> scope(..., parent(0)))
       ...
     </scopes>
     <heap> .Map </heap>
     [priority(40)]
```

It bypasses all lookup, binding, arithmetic, `ord`, `chr`, and concatenation
steps in the real loop. Its match domain fixes scope 1 but leaves scopes 0 and
−1 unconstrained through map ellipses. It also accepts an arbitrary trailing
`<k>` continuation and omits the other configuration cells.

The independently proved `LOOP-SPEC` does **not** justify that domain. Its
precondition fixes the complete scope map: scope 0 contains only the candidate
closure, scope −1 is exactly `builtinsScope`, and scope 1 contains the locals.
It proves the loop only with those bindings and an exact loop-head
continuation. There is no bridge-free universal theorem covering arbitrary
parent scopes or shadowed builtins.

The mismatch is not merely an evidence gap. The following satisfiable ground
state is a false-conclusion witness within the bridge’s match domain:

- input/remaining iterable is `"a"` (`iCons(97, .IntSeq)`);
- active scope 1 has empty `result`, empty `char`, `s = "a"`, parent 0;
- scope 0 binds `"ord"` to `builtinV("len")`, parent −1;
- scope −1 is `builtinsScope`;
- environment is 1 and the heap is empty.

Under fixed semantics, the real loop:

1. binds `char` to `"a"`;
2. resolves `Name("ord")` to the shadowing `len` binding;
3. computes `len("a") = 1`;
4. computes `chr((1 - 97 + 4) % 26 + 97) = chr(109) = "m"`;
5. terminates with `result = "m"`.

The bridge ignores the shadowed binding and substitutes
`encryptCode(97) = 101`, yielding `"e"`.

This is machine-checked in three independent claims:

- fixed semantics to `"m"` prints `#Top`, exit 0:
  `evidence/mutations/bridge-shadow-fixed-m.k` and
  `evidence/logs/05-bridge-fixed-m.log`;
- fixed semantics to `"e"` is rejected with `WarnStuckClaimState`, exit 1:
  `evidence/mutations/bridge-shadow-fixed-e.k` and
  `evidence/logs/05-bridge-fixed-e.log`;
- bridge-enabled semantics to the false `"e"` state prints `#Top`, exit 0:
  `evidence/mutations/bridge-shadow-enabled-e.k` and
  `evidence/logs/05-bridge-enabled-e.log`.

The bridge therefore enables a concrete false conclusion. Priority 40 makes it
preempt ordinary loop execution; priority does not supply the missing
equivalence. The bad shadowing state is not reached by `FUNCTION-SPEC`, whose
scope 0 is fixed, but an off-path globally false rule is still an invalid proof
extension. It must have been narrowed to the exact proved scope/binding domain
or supported by a genuinely universal connection theorem.

Conclusion for stage 5: **static soundness fails on a proof-local operational
bridge**.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate negative result was
trusted.

I created `evidence/mutations/spec-false-result.k`, a distinct spec module that
changes the entry postcondition from:

```k
str(encryptCodes(CS))
```

to the deliberately false:

```k
str(seqConcat(encryptCodes(CS), iCons(97, .IntSeq)))
```

That mutation appends `"a"` to every claimed result. The entry precondition is
satisfiable for `CS = .IntSeq`; the real candidate returns `""`, not `"a"`.

First, a dry run against the freshly built function definition parsed and
compiled the mutation successfully:

```text
kprove --definition function-verification-fresh-kompiled \
  spec-false-result.k \
  --spec-module FUNCTION-SPEC-FALSE-RESULT --dry-run
# exit 0
```

The actual proof then exited 1 with `WarnStuckClaimState`. The residual is the
expected unmet equality:

```text
encryptAcc(.IntSeq, CS)
  =? seqConcat(encryptAcc(.IntSeq, CS), iCons(97, .IntSeq))
```

This is a semantic proof failure, not a parser error, missing import, timeout,
or unrelated crash.

Evidence:

- `evidence/logs/06-false-result-dry-run.log`
- `evidence/logs/06-false-result-kprove.log`

Conclusion for stage 6: **the entry claim is non-vacuous and result-sensitive**.
This does not cure the unsound bridge or wrong source contract.

## 7. Proven versus assumed accounting

### What the successful runs establish

The fixed-semantics `LOOP-SPEC` proof establishes, for every finite K
`IntSeq`, arbitrary accumulated result and loop-variable old value satisfying
its exact state, that executing the candidate’s real loop maps every code
through:

```text
((C - 97 + 4) mod 26) + 97
```

and updates the retained loop variable exactly. The body-sensitivity mutation
supports that the actual body, not merely an external source file, is being
executed.

The successful `FUNCTION-SPEC` run establishes closure only under the extended
theory containing the loop-summary bridge. Its formal statement is that the
actual submitted closure, in the standard initial binding and state, returns
`encryptCodes(CS)` for every `CS`. Ground execution and the independently
proved exact-domain loop claim support the truth of that candidate-behavior
statement, but the actual composed proof is not admissible because its imported
bridge is false on its declared match domain.

Neither proof establishes the trusted HumanEval contract for general strings.
The postcondition intentionally maps every input code into lowercase `a`–`z`;
the canonical preserves every non-lowercase character.

### Trust and assumption ledger

1. **K built-in mathematics and backend.** Integer, Boolean, string, map, list,
   equality and rewrite-logic machinery are trusted as the K `v7.1.293`
   implementation. `pyMod` is defined from K integer operations. This is a
   normal low-level proof boundary.
2. **Supplied MPY semantics.** The recursively matched trusted tree is the fixed
   semantic level. Used rules for scopes, calls, strings, integers, loops,
   returns and `ord`/`chr` were reviewed and dynamically exercised. The model
   is a partial Python subset, not CPython.
3. **Proof-opaque supplied symbols.** The fixed semantics contains the
   proof-opaque or concrete-only symbols `sortVS`, `sortKeyVS`,
   `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
   `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
   `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
   `roundFN`, and `sqrtF`. None occurs in the submitted program term,
   candidate summary, loop claim, or entry postcondition. Their trust does not
   support the target result.
4. **Totalized partial helpers.** Supplied helpers such as opaque/out-of-bounds
   `valSeqAt` rely on K totality beyond concretely covered cases. No such helper
   is on the target path.
5. **ASCII/model bridge.** Source string literals and concrete `chr` are
   ASCII-limited in the supplied semantics. The formal entry accepts an
   arbitrary `str(CS)` value directly, and this candidate always computes
   output codes 97–122, so the used result path satisfies the `chr` guard. This
   does not justify treating non-lowercase inputs as lowercase.
6. **Translator bridge.** The trusted translator connects `solution.py` to
   `solution.mpy`; byte-identical regeneration and mechanical constructor
   comparison support this bridge. It is not assumed from candidate prose.
7. **Canonical/source intent bridge.** The trusted prompt and canonical define
   the source contract. Differential tests provide finite corroboration, while
   explicit inputs such as `"A"` are complete counterexamples to candidate
   equivalence.
8. **Candidate summaries.** `encryptCode`, `encryptAcc`, `encryptCodes`, and
   `lastChar` are fully equational, terminating definitions, not opaque
   assumptions.
9. **Loop operational bridge.** This was presented as a derived lemma, but its
   domain is broader than the proved loop claim and it is concretely false.
   This boundary is illegitimate.
10. **Termination.** The Kit theorem status is partial correctness. The
    structural loop and summaries visibly descend on finite sequences, but no
    separate total-correctness theorem is claimed.
11. **Generation prose, traces and prior `#Top`.** These remain untrusted
    historical evidence and contribute nothing to proof closure or soundness.

### Gate and decision accounting

- Real-program soundness / Gate A: **FAIL**. The loop bridge admits a
  machine-checked false conclusion under a satisfying state in its own match
  domain.
- Intent adequacy / Gate B: **FAIL**. The actual generated program and formal
  postcondition disagree with the unrestricted trusted string contract on
  non-lowercase characters.
- Trust/evidence auditability / Gate C: **FAIL for the candidate report**. The
  candidate supplied no soundness ledger or universal bridge connection and
  tested only lowercase behavior. The auditor’s reconstruction, counterexample,
  differential, and mutation evidence is reproducible, but auditor evidence
  cannot repair the immutable candidate.

Either Gate A or Gate B independently requires `FAIL / NOT_LEGIT` under the
benchmark decision boundary. Successful `#Top` runs, real-program pinning, and
non-vacuity do not override either defect.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
