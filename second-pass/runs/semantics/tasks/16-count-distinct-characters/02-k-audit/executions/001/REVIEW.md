# Independent adversarial audit: 16-count-distinct-characters

## Executive decision

**CONCERNS / LEGIT.** The candidate's two positive reachability claims rebuild
and close independently, the result claim is non-vacuous, and its only
proof-local rules expand to and execute the exact submitted function body. A
reviewer-authored connection claim additionally proves, using a fresh
bridge-free definition, that loading the exact submitted `Module(FuncDef(...))`,
resolving its binding by name, and calling it yields the candidate's same
symbolic postcondition.

The proof is nevertheless not a proof of the full CPython `str.lower()` contract
over arbitrary Unicode strings. The supplied semantics defines only ASCII case
conversion. Concrete witnesses separate the models: for `"\u0130"` the formal
postcondition is `1` while both trusted canonical Python and submitted Python
return `2`; three other recorded Unicode witnesses also diverge. This is a
language-model/intent bridge limitation, not a false candidate-added K rule:
the candidate used the mandated, byte-identical supplied semantics. Required
generation provenance files are also absent, although that did not prevent a
fresh reconstruction.

All candidate material was treated as untrusted. `/candidate` was not modified.
Builds, generated claims, and experiments were performed below
`/tmp/audit-work`; reviewer artifacts and bounded logs are in `evidence/`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present as a real directory, so there is no
mode/mount contradiction and no infrastructure breach. The candidate's
`reference-semantics/` contains 25 recursive entries, exactly matching the
trusted tree's 25 entries by relative path, file type, and SHA-256 content.
There are no missing, additional, changed, mistyped, or symlinked entries.
There are no symlinks anywhere under `/candidate`.

The candidate `prompt.py` and `py2mpy.py` are regular files and byte-identical
to `/reference/prompt.py` and `/reference/py2mpy.py`, respectively.

Evidence: [`evidence/stage1-integrity.log`](evidence/stage1-integrity.log) and
the reviewer script
[`evidence/stage1_integrity.sh`](evidence/stage1_integrity.sh).

### Missing provenance artifacts

The following requested top-level artifacts are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace is present. Therefore there were no provenance
claims in those files to inspect. These omissions limit auditability, but the
source proof artifacts needed for independent reconstruction are present:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and the complete
supplied-semantics tree. Candidate-provided `prove.sh`, concrete tests, and
`__pycache__` were not treated as authority or reused as proof evidence.

The live toolchain was independently identified as K version `v7.1.337`
(`kompile` and `kprove` from `/usr/bin`).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks for `count_distinct_characters(string: str) -> int`:
count the number of distinct characters regardless of case. The trusted
canonical implementation returns:

```python
len(set(string.lower()))
```

The submitted `solution.py` has the same entry-point name and exactly the same
executable expression. It omits the canonical docstring, which has no behavioral
effect.

The trusted translator was run on the scratch copy:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/solution.regenerated.mpy
cmp -s /tmp/audit-work/solution.regenerated.mpy /candidate/solution.mpy
```

The comparison exited 0. Both files have SHA-256
`2e97b9f354373f39763938a074e4f09fb6a259868fdc704ed07b670ed65ccfc9`.
Thus the submitted MPY term is byte-for-byte the trusted translation of the
submitted Python. Evidence:
[`evidence/stage2-translate.log`](evidence/stage2-translate.log).

### Independent differential test

[`evidence/stage2_differential.py`](evidence/stage2_differential.py) imports the
trusted canonical and submitted entry points directly by path. It does not use
candidate tests, K equations, or the proof postcondition. Its scope was:

- the two documented examples;
- empty, singleton, exact-duplicate, case-duplicate, all-duplicate,
  distinct-character, punctuation/digit, whitespace/control, embedded-NUL,
  and Unicode lowercasing boundaries;
- every string of length 0 through 5 over
  `['a', 'A', 'b', '1', '!', 'Σ']`; and
- 1,000 deterministic generated strings of length 0 through 32 over a mixed
  ASCII/Unicode alphabet, seed `160016`.

There were 10,349 comparisons, zero mismatches, and zero execution errors.
The exact command and summary are in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log); all
per-input results are in
[`evidence/stage2-differential-results.jsonl`](evidence/stage2-differential-results.jsonl).
This finite test supports Python implementation fidelity; it is not a substitute
for the K proof.

## 3. Clean proof reconstruction

The source artifacts were copied to `/tmp/audit-work/candidate-src`. No
candidate-built definitions or caches existed there when reconstruction
started; new output directories were created from source.

### Concrete definition

The LLVM definition was rebuilt with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit status was 0. The compiler emitted non-exhaustiveness warnings for several
unused total helpers (`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt`);
these are accounted for in Stages 5 and 7. Full bounded output:
[`evidence/stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log).

The candidate concrete assertion program was then executed against this fresh
definition. `krun concrete_tests.mpy --definition runtime-kompiled` exited 0
with final `<k> .K </k>`, `NoExc`, and exit code 0. This is only a fresh
concrete smoke test, not proof evidence. Log:
[`evidence/stage3-krun-candidate-concrete-tests.log`](evidence/stage3-krun-candidate-concrete-tests.log).

### Proof definition and positive claims

The Haskell proof definition was rebuilt with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit status was 0:
[`evidence/stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log).

The original aggregate command

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`:
[`evidence/stage3-kprove-all.log`](evidence/stage3-kprove-all.log).

Because both candidate claims are unlabeled, verbatim scratch-only one-claim
modules were created so each target could be run independently:

- load claim:
  [`evidence/spec-load-only.k`](evidence/spec-load-only.k), exit 0 and `#Top`
  in [`evidence/stage3-kprove-load-only.log`](evidence/stage3-kprove-load-only.log);
- result claim:
  [`evidence/spec-call-only.k`](evidence/spec-call-only.k), exit 0 and `#Top`
  in [`evidence/stage3-kprove-call-only.log`](evidence/stage3-kprove-call-only.log).

Every positive target therefore passes clean reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claims

The **load claim** has no explicit `requires`. Its complete initial state is the
empty module scope at location 0, the supplied builtins scope at `-1`, empty
heap and stack, `noRet`, `NoExc`, and exit code 0. It says that executing
`#loadCountDistinct` consumes the computation and adds exactly one module
binding, `count_distinct_characters`, whose closure has parameter `string`,
parent scope 0, and the exact translated return body. All other cells remain
unchanged.

The **result claim** also has no explicit `requires`. For every algebraic
`CS:IntSeq`, from the same empty initial module state, it says that
`#callCountDistinct(CS)` terminates in the value

```text
isLen(dedupCodes(mapLower(CS)))
```

with environment, scopes, allocation counters, heap, stack, return state,
exception state, and exit code restored unchanged. This is an equality-like
result constraint in the `<k>` rewrite, not a free RHS variable, tautology, or
one-way implication.

Both preconditions are satisfiable. One load witness is exactly the initial
configuration printed above. For the result claim, `CS = .IntSeq` with those
same cells is a concrete satisfying state and yields 0.

### Submitted-program identity and control flow

`verification.k` adds only two wrapper constructors and two ordinary rules:

1. `#loadCountDistinct` rewrites to the exact `FuncDef` occurring inside the
   byte-verified submitted `solution.mpy`.
2. `#callCountDistinct(CS)` rewrites to `#applyK(toCall(closureVal(...)),
   (str(CS), .Vals))`, with the same exact parameter, body, and defining scope.

The second wrapper does not first execute the module loader or look up the
global function name. That is an adequacy point requiring validation. It does
not replace the function body with a result summary: after the wrapper fires,
the fixed semantics executes parameter binding, all three nested calls,
`string` and builtin lookup, `.lower`, `set`, `len`, `Return`, frame popping,
and state restoration.

To test the skipped load/name-resolution context independently, the reviewer
built [`evidence/fixed-only.k`](evidence/fixed-only.k), which imports only
`MPY` and contains neither candidate wrapper. The audit-only claim
[`evidence/spec-end-to-end-audit.k`](evidence/spec-end-to-end-audit.k) starts
with the exact submitted `Module(FuncDef(...))`, loads it through `#loadAll`,
then invokes `Call(Name("count_distinct_characters"), (str(CS), .Exprs))`.
It proves the same symbolic result and the exact surviving global binding.

The fixed-only definition compiled successfully
([`evidence/stage4-kompile-fixed-only.log`](evidence/stage4-kompile-fixed-only.log));
the connection claim passed `--dry-run`
([`evidence/stage4-end-to-end-dry-run.log`](evidence/stage4-end-to-end-dry-run.log))
and then exited 0 with `#Top`
([`evidence/stage4-end-to-end-kprove-final.log`](evidence/stage4-end-to-end-kprove-final.log)).
An earlier audit draft had one missing close parenthesis and produced the
preserved parser error in `stage4-end-to-end-kprove.log`; the corrected artifact
passed both parsing and proof and the earlier error is not candidate evidence.

This bridge-free theorem confirms that the wrapper's accepted context is an
exact auxiliary invocation of the submitted program for this body. The global
binding omitted by the wrapper is observationally irrelevant to this function:
the body reads only its parameter and the fixed `len`/`set` builtins.

### Concrete result substitutions

The ground K witness module
[`evidence/spec-ground-witnesses.k`](evidence/spec-ground-witnesses.k) proves
empty input gives 0, `"xyzXYZ"` code points give 3, and the supplied model gives
1 for U+0130. It exits 0 with `#Top`:
[`evidence/stage4-ground-kprove.log`](evidence/stage4-ground-kprove.log).

The reviewer bridge script
[`evidence/stage4_bridge_check.py`](evidence/stage4_bridge_check.py) evaluates
the exact K postcondition equations and both Python implementations. ASCII
examples agree. Four Unicode inputs do not:

| Input | Formal K postcondition | Trusted canonical | Submitted Python |
|---|---:|---:|---:|
| `"\u0130"` | 1 | 2 | 2 |
| `"Σσς"` | 3 | 2 | 2 |
| `"\u1e9eß"` | 2 | 1 | 1 |
| `"\U00010400\U00010428"` | 2 | 1 | 1 |

Full output:
[`evidence/stage4-bridge-check.log`](evidence/stage4-bridge-check.log).
The cause is explicit in supplied `semantics/methods.k`: `lowerC` changes only
codes 65 through 90 by adding 32, whereas CPython Unicode lowercasing can map
non-ASCII code points and can expand one code point into multiple code points.
The prompt does not restrict its `str` input to ASCII. This is the material
adequacy concern behind the verdict.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated inventory
[`evidence/stage5-rule-inventory.md`](evidence/stage5-rule-inventory.md) contains
the complete source block, file, line, guards, cells, and attributes for every
local declaration. It records:

- 228 `syntax` declaration blocks;
- 697 ordinary semantic/proof rules;
- 2 claims;
- 1 configuration;
- 5 contexts;
- 0 aliases;
- 0 `[simplification]` rules and 0 `functional` declarations;
- 149 source lines bearing `[function]`, 114 bearing `[total]`,
  45 priority rules, 29 `owise` rules, and 39 concrete-attribute lines; and
- 22 `[no-evaluators]` opaque symbols and 25 explicitly named `symbol(...)`
  declarations.

The exact generation command, exit 0, line count 6,727, and inventory SHA-256
are in
[`evidence/stage5-inventory-command.log`](evidence/stage5-inventory-command.log);
the generator is
[`evidence/stage5_inventory.py`](evidence/stage5_inventory.py).

The following disposition table accounts for every inventoried rule. “Unused”
means the rule's head symbol/constructor cannot occur in the theorem's initial
term or any transitive successor in the used call path; there are no global
simplification axioms that can introduce it.

| Source module | Syntax | Rules | Disposition for this theorem |
|---|---:|---:|---|
| `assert.k` | 0 | 3 | Unused assertion/exception subset |
| `bool.k` | 0 | 13 | Unused boolean operations |
| `builtins.k` | 38 | 137 | `applyBuiltin("set",...)`, `applyBuiltin("len",...)`, `seqLen(setV(...))` used; all other builtin/fold/eval/md5 rules unused |
| `call.k` | 3 | 21 | Attribute cooling, generic Call/callee/argument path, method/builtin dispatch, and ordinary closure dispatch used; heap/annotated-closure cases unused |
| `comprehension.k` | 3 | 7 | Unused macros |
| `concrete.k` | 5 | 16 | LLVM-only; absent from proof definition and irrelevant to claim closure |
| `controls.k` | 3 | 34 | Unused statements and loops |
| `core.k` | 37 | 46 | Configuration, module sequencing, name lookup, builtins scope, argument evaluation, `appendVal`, and `isLen` used; allocation/cell/literal/other helpers unused |
| `dict.k` | 12 | 28 | Unused dictionary subset |
| `float.k` | 34 | 121 | Unused float subset and opaque float primitives |
| `functions.k` | 4 | 15 | ordinary `FuncDef`, parameter binding, `Return`, `#endcall`, and `#pop` used; cell-closure cases unused |
| `int.k` | 1 | 16 | No MPY integer operator dispatch used; built-in integer arithmetic is used inside helpers |
| `iter.k` | 1 | 0 | Iterator declaration unused |
| `list.k` | 5 | 27 | Unused list subset |
| `methods.k` | 27 | 75 | `applyMethod(...,"lower",...)`, `isUpperC`, `lowerC`, and `mapLower` equations used; all other methods unused |
| `operators.k` | 0 | 10 | Unused operator dispatch |
| `range.k` | 2 | 6 | Unused range subset |
| `set.k` | 6 | 12 | `setV`, `codeIn`, `dedupCodes`, `dedupFrom`, and `snocCode` declarations/equations used; set comparison helpers unused |
| `sort.k` | 6 | 19 | Unused opaque sorting boundary |
| `str.k` | 5 | 28 | No string literal/operator rule is used; the argument enters as semantic `str(CS)` |
| `subscript.k` | 15 | 40 | Unused indexing/slicing subset |
| `syntax.k` | 16 | 0 | Declares the submitted AST constructs; declarations add no theorem equation |
| `tuple.k` | 4 | 21 | Unused tuple subset |
| assembled `semantics.k` | 0 | 0 | Imports exactly the modules above |
| `verification.k` | 1 | 2 | Both exact wrappers are used and reviewed below |

### Used-syntax and rule mapping

The submitted MPY uses `Module`, `FuncDef`, `Params`, `ParamNames`, `Stmts`,
`Return`, `Call`, `Name`, `Attribute`, and `Exprs` from `syntax.k`. The
transitive operational path is:

```text
Module/#loadAll -> FuncDef/closureVal
exact closure call -> new frame -> bind string
Name(string) -> Attribute(lower) -> applyMethod/mapLower/lowerC
Name(set) -> applyBuiltin(set)/dedupCodes
Name(len) -> applyBuiltin(len)/seqLen/isLen
Return -> #pop -> final Int
```

Every used constructor has a declaration and every used redex has a rule.
Argument evaluation is left-to-right through `#evalArgs`; here all wrapper
arguments are already values. Binding is exact: `string` is installed in a
fresh child scope, while `len` and `set` fall through to the immutable supplied
builtins scope. The wrapper closure has defining scope 0, the same as the loaded
function. Closure invocation pushes the existing continuation and caller
environment; `Return` sets `retV`, and `#pop` restores environment, removes the
callee scope, rewinds `scopeLoc`, pops the stack, and emits the value. No heap
allocation, output, exception, or other observable state occurs on this path.

The used guards are exhaustive and disjoint:

- local name-hit versus parent-fallthrough use `X in_keys(M)` and its negation;
- the cell-lookup priority rule requires a `"$cells"` binding absent here;
- `lowerC`'s ASCII-uppercase guard and `owise` complement do not overlap;
- `dedupFrom` uses `codeIn` and its negation;
- the algebraic base/cons equations for `mapLower`, `codeIn`, `snocCode`, and
  `isLen` cover all values of their declared sequence sorts.

The generic `Call` rule is `owise`, but no special call interception matches
these calls. The relevant higher-priority heap/cell/split rules require
constructors or bindings absent from the state. There is therefore no
priority/overlap route that changes the used execution.

### Candidate-added rules

`#loadCountDistinct` is a definitional wrapper around the exact submitted
`FuncDef`; it does not summarize a result or preempt a fixed MPY redex.
`#callCountDistinct` introduces an exact auxiliary invocation configuration.
It skips module binding and global name lookup, but not program-defined
execution. Its binding, body, argument, defining scope, continuation, and all
state cells were checked, and the bridge-free end-to-end claim described in
Stage 4 establishes the omitted fixed-semantics context over the complete
symbolic `IntSeq` domain.

Neither rule is a function, total declaration, priority rule, simplification,
opaque symbol, or oracle. No fresh symbol reaches the result. The postcondition
uses the same fully defined `mapLower`, `dedupCodes`, and `isLen` equations that
fixed execution produces, rather than an unconstrained summary.

### Opaque and total boundaries

The 22 imported no-evaluator symbols are:

`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`.

The additional named symbols `floorFI`, `toF`, and `ceilF` have equations but
also generated LLVM non-exhaustiveness warnings on the full `Val` sort. Other
warnings identify `mapStrVS`, `joinCodes`, and `valSeqAt` total declarations
whose source equations do not cover every constructor. All of these symbols
are outside the result/control/state dependency slice. No claim condition,
branch, or observable cell contains them, and no simplification rule can
introduce them. Their total/opaque status is a broad supplied-semantics trust
boundary, but it contributes no value to this proof.

The ASCII `lowerC` equations are complete and consistent as equations of the
selected supplied model. They are not labeled unsound in this audit because
they do not make a false conclusion about that selected model. Their divergence
from CPython is instead reported, with concrete witnesses, as Gate B intent
inadequacy. No candidate-added or proof-relevant fixed rule was found unsound,
so there is no unsupported “unsound rule” allegation requiring a separate false
conclusion witness.

## 6. Fresh non-vacuity test

The reviewer did not rely on any candidate vacuity artifact. The fresh module
[`evidence/spec-vacuity-fresh.k`](evidence/spec-vacuity-fresh.k) changes the
result obligation from

```text
isLen(dedupCodes(mapLower(CS)))
```

to that expression plus one. The original precondition remains unchanged.
`CS = .IntSeq` is a satisfying witness: real/formal execution returns 0, while
the mutation demands 1.

The mutated module first passed `kprove --dry-run` with exit 0, proving the
artifact parsed and compiled:
[`evidence/stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log).
The actual proof then exited 1 with `WarnStuckClaimState`. Its residual shows
the expected failed implication:

```text
isLen(dedupFrom(mapLower(CS), .IntSeq)) +Int 1
#Equals
isLen(dedupFrom(mapLower(CS), .IntSeq))
```

It ends with the expected backend “configuration cannot be rewritten further”
error, not a parser error, missing import, timeout, or unrelated crash:
[`evidence/stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log).
The result claim is therefore discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under K `v7.1.337` and the exact supplied MPY semantics:

1. In the stated empty initial module configuration, the exact submitted
   function definition loads to the exact closure recorded by the first claim.
2. For every finite algebraic `CS:IntSeq`, if the exact function-body execution
   represented by the second claim terminates, it returns
   `isLen(dedupCodes(mapLower(CS)))` and restores every modeled state cell.
3. The reviewer connection theorem establishes the same result when execution
   begins with the exact submitted `Module(FuncDef(...))`, uses the ordinary
   loader, resolves the function by name, and calls it under the fixed semantics.

This is partial correctness. The reachability proof does not independently
state a termination theorem, although all result-relevant recursive functions
structurally descend finite algebraic sequences and concrete execution
terminates on the tested cases.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment/evidence |
|---|---|---|
| K compiler, Haskell backend, Kore prover, and builtin INT/BOOL/STRING/MAP/LIST/K-EQUAL theories | Foundation for every build and proof | Necessary ordinary machine-checking trust; fresh builds and independent claim runs recorded |
| Trusted mounted supplied semantics | Defines the execution model for both claims | Integrity-verified byte-for-byte; used dependency slice statically audited |
| Trusted `py2mpy.py` | Connects submitted Python syntax to submitted MPY | Candidate copy identical; regenerated MPY byte-identical |
| Exact-AST correspondence between wrappers and `solution.mpy` | Pins candidate helpers to submitted code | Direct inspection, translation hash, separate load claim, and bridge-free end-to-end `#Top` connection claim |
| `mapLower` as a model of Python `str.lower()` | Determines the final result for every input | Acceptable only for ASCII case behavior; illegitimate as an unconditional full-Unicode bridge. Four false bridge witnesses recorded |
| Mapping Python strings to arbitrary `IntSeq` | Relates K theorem domain to intended Python domain | Informal and over-broad: K permits arbitrary integers; valid Python strings use Unicode code points, and Python lower may expand them |
| 22 opaque no-evaluator symbols plus partial total helpers in unused modules | Could affect other programs using floats, sort, md5, keyed helpers, etc. | Concerning broad supplied-semantics boundary, but none influences this claim's value, control, state, or conditions |
| Python differential suite | Supports submitted-vs-canonical behavior | Finite evidence only: 10,349 recorded inputs, zero mismatches |
| Ground K/Python bridge cases | Tests meaning of the formal summary | Finite evidence; confirms ASCII cases and exposes Unicode counterexamples rather than pretending to prove equivalence |
| Missing generation metadata/logs/trace | Prevents checking generation-process claims and resource history | Auditability concern; not used to infer proof success |

### Gate summary and verdict rationale

- **Real-program soundness and non-vacuity:** PASS. Fresh `#Top` reconstruction,
  exact-body execution, bridge-free end-to-end connection, state/control
  inspection, satisfying witnesses, and expected false-mutation rejection all
  pass.
- **Intent adequacy:** LIMITED. The formal theorem matches the submitted program
  under supplied semantics, but the supplied ASCII-only lowercase model does
  not match the unqualified Python-string contract on Unicode.
- **Trust/evidence auditability:** LIMITED. Evidence is reproducible, but
  generation provenance files are missing and the Unicode bridge is
  demonstrably conditional rather than universal.

The candidate therefore contains a legitimate, result-constraining
partial-correctness proof of the exact generated program under the mandated
supplied semantics, but its bridge to the full natural-language/CPython intent
has a documented material limitation. That is `CONCERNS / LEGIT`, not
`PASS / LEGIT`; no materially unsound proof-local rule, substituted body,
vacuity, or reconstruction failure justifies `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
