# Independent adversarial review — 27-flip-case

## Executive decision

The candidate contains a legitimate, freshly reconstructed partial-correctness
proof under the supplied K semantics. The single entry claim closes from clean
source, fixes the returned value, and executes the exact constructor tree
submitted in `solution.mpy`; it does not use an oracle, body-skipping rewrite,
free result, or vacuous precondition.

The result is `CONCERNS / LEGIT`, rather than `PASS`, because the supplied
string semantics implements ASCII case switching only, whereas the trusted
canonical Python program uses Unicode-aware `str.swapcase()` and the prompt
does not restrict inputs to ASCII. This is an adequacy limitation in the bridge
from the formally proved code-sequence theorem to the natural-language Python
contract, not an unsound candidate-local proof rule. In addition, all named
generation/provenance metadata is absent from the candidate, although the
source-level proof remains independently reconstructible.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount
`/reference/reference-semantics` exists as a real directory. There is therefore
no mode/mount contradiction and no infrastructure breach.

The candidate root contains regular source files for `solution.py`,
`solution.mpy`, `spec.k`, `verification.k`, `prompt.py`, `py2mpy.py`,
`prove.sh`, `concrete-tests.mpy`, and the supplied semantics tree. It also
contains an untrusted `__pycache__/solution.cpython-310.pyc`; that cache was
ignored and was not copied into the clean reconstruction.

The following requested untrusted provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present under `/candidate`. Their absence
limits provenance review but does not prevent independent review of the regular
source artifacts.

`cmp` exited 0 for both `/candidate/prompt.py` against
`/reference/prompt.py` and `/candidate/py2mpy.py` against
`/reference/py2mpy.py`. A no-symlink structural and SHA-256 comparison of the
two `reference-semantics/` trees found no missing, additional, changed,
mistyped, or symlinked entries. Thus the candidate supplied-semantics copy is
byte-identical to the trusted tree. This integrity result does not bless
`verification.k`, which was audited separately.

Evidence:

- `evidence/stage1_inventory.log`
- `evidence/stage1_prompt_cmp.log`
- `evidence/stage1_translator_cmp.log`
- `evidence/stage1_semantics_integrity.log`
- `evidence/check_integrity.py`
- `evidence/stage1_inventory.sh`

All executable source artifacts were copied to
`/tmp/audit-work/27-flip-case`; candidate-built definitions and caches were not
copied or reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

`/reference/prompt.py` asks for `flip_case(string: str) -> str`: lowercase
characters become uppercase and uppercase characters become lowercase. Its
documented example is `"Hello" -> "hELLO"`. No ASCII-only restriction is
stated, so the intended domain is Python `str`.

`/reference/canonical.py` implements the contract as:

```python
return string.swapcase()
```

`/candidate/solution.py` has the same entry point and the same implementation.
It is a valid, simpler presentation of the canonical algorithm.

The trusted translator was run from the clean trusted copy:

```text
python3 /tmp/audit-work/27-flip-case/trusted/py2mpy.py /tmp/audit-work/27-flip-case/candidate/solution.py > /tmp/audit-work/27-flip-case/candidate/regenerated.solution.mpy
```

It exited 0, and `cmp` between the regenerated and submitted `solution.mpy`
exited 0. The submitted MiniPy program is therefore byte-identical to trusted
translation output. Its AST is:

```text
Module(
  FuncDef("flip_case", Params("string"),
    Return(Call(Attribute(Name("string"), "swapcase"), ))))
```

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical function and the
clean copied submitted function as different modules. It covers:

- the documented example;
- empty input;
- boundaries immediately below, at, and above `A..Z` and `a..z`;
- digits, punctuation, NUL, combining marks, and representative non-ASCII
  casing behavior;
- all 7,381 strings of length 0 through 4 over a nine-symbol branch alphabet;
- every one of the 1,114,112 possible one-code-point Python strings, including
  Python's internally permitted surrogate code points;
- 2,000 deterministic generated strings of length 0 through 64.

The exact run made 1,123,511 comparisons, found zero mismatches, and exited 0.
This is finite empirical evidence for implementation fidelity; it is not used
as a substitute for the K reachability proof.

Evidence:

- `evidence/stage2_translate.log`
- `evidence/stage2_mpy_byte_identity.log`
- `evidence/differential_test.py`
- `evidence/stage2_differential.log`

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

K was independently available as v7.1.337 at `/usr/bin/kompile` and
`/usr/bin/kprove`. The scratch tree initially contained no `*-kompiled`
directories.

### Concrete definition

The following fresh LLVM build exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled
```

Fresh `krun` executions of both the translated `solution.mpy` and
`concrete-tests.mpy` exited 0. The concrete tests call the real submitted
function on `"Hello"`, `"Python 3.11"`, and `""`; the final configuration had
`.K`, `NoExc`, and exit code 0. The `solution.mpy` run independently showed the
submitted body installed as the `flip_case` closure.

### Proof definition and positive target

The following fresh Haskell build exited 0:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled
```

Source inventory found exactly one positive target claim, the entry claim in
`spec.k`, and no auxiliary or loop claims. The independent proof command was:

```text
timeout 180s kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`. The compiler warnings concern unused variables
in unrelated `strLt` rules; they do not change the success signal.

Evidence:

- `evidence/stage3_kompile_llvm.log`
- `evidence/stage3_krun_solution.log`
- `evidence/stage3_krun_concrete_tests.log`
- `evidence/stage3_kompile_haskell.log`
- `evidence/stage3_claim_inventory.log`
- `evidence/stage3_kprove_spec.log`

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The precondition admits every algebraic `S:IntSeq` and requires the standard
module-entry state:

- `<k>` contains `#runFlipCase(S)`;
- current environment is scope 0;
- scope 0 is empty and has the builtins scope at `-1` as parent;
- scope allocation begins at 1;
- heap and frame stack are empty;
- return state is `noRet`, exception state is `NoExc`, and exit code is 0.

There is no contradictory `requires` clause. For example,
`S = iCons(72,iCons(101,iCons(108,iCons(108,iCons(111,.IntSeq)))))`
and the displayed cells form a concrete satisfying state.

The postcondition requires:

- the `<k>` result to be exactly `str(mapSwap(S))`;
- scope 0 to contain the actual submitted closure body;
- every other listed cell to retain its exact final value.

There is no free result variable, tautology, implication weakening, or omitted
observable cell. The claim is result-constraining.

### Actual program identity

`verification.k` defines `flipCaseBody` and `solutionModule` only as macros.
Their expansions match the byte-validated `solution.mpy` constructor tree,
including the empty `.Exprs` call argument. `#runFlipCase` expands to:

```text
#loadAll(solutionModule) ~> Call(Name("flip_case"), str(S))
```

It still performs module loading, closure binding, name lookup, parameter
binding, receiver evaluation, method call, return, and frame cleanup under the
fixed supplied semantics. It does not replace the submitted function body with
a summary.

As an independent pinning check, I built a second Haskell definition importing
only `MPY`, not `verification.k`, then proved a universal claim starting from
the exact submitted constructor tree copied directly into `<k>`. That
helper-free claim exited 0 with `#Top`. This establishes that the local runner
is only setup syntax and that claim closure is available from actual fixed
execution.

For the concrete satisfying `"Hello"` state,
`evidence/adequacy-witness.k` replaces the symbolic RHS by the literal code
sequence `[104,69,76,76,79]` for `"hELLO"`. It exited 0 with `#Top`.
`evidence/adequacy_python_witness.py` independently showed the same value from
both Python implementations and exited 0.

There are no loops or helper claims to align with control flow.

Evidence:

- `evidence/direct-pinning.k`
- `evidence/stage4_kompile_fixed_haskell.log`
- `evidence/stage4_kprove_direct_pinning.log`
- `evidence/adequacy-witness.k`
- `evidence/stage4_kprove_ground_witness.log`
- `evidence/adequacy_python_witness.py`
- `evidence/stage4_python_ground_witness.log`

Stage 4 result: **PASS** for formal pinning and result adequacy within the
supplied model.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` rebuilt a source-level inventory over all 24 supplied
semantics files plus `verification.k` and `spec.k`. The resulting
`evidence/rule-inventory.md` contains every directive with source line range,
full text, attributes, reachability classification, and static decision:

- 935 directives total;
- 230 `syntax` declarations;
- 698 `rule` declarations;
- five `context` declarations;
- one `configuration`;
- one `claim`.

Attribute inventory includes 155 functions, 115 `total`, 35 `concrete`, 41
`priority(40)`, three `priority(45)`, one `priority(39)`, 26 `owise`, seven
macro/macro-rec entries, and 22 `no-evaluators` entries. There are no
source-level `functional` or `simplification` attributes.

The supplied tree is the selected trusted semantics level. Every out-of-slice
entry is individually marked as fixed supplied baseline and was checked not to
match a term produced by this program. All reachable entries received a
separate execution-slice review in `evidence/reachable-rule-map.md`.

### Reachable syntax and execution

The submitted constructors map to declarations in
`semantics/syntax.k`: `Module`, `FuncDef`, `Params`, `Return`, `Call`,
`Attribute`, `Name`, `Stmts`, and `Exprs`. The relevant path is:

```text
#loadAll
  -> FuncDef closure installation
  -> Name("flip_case") lookup
  -> closure call and temporary frame
  -> bind string = str(S)
  -> strict Return expression
  -> Name("string") lookup
  -> Attribute(..., "swapcase") bound method
  -> empty left-to-right argument evaluation
  -> applyMethod(..., "swapcase", .Vals)
  -> str(mapSwap(S))
  -> Return/#pop and full caller-state restoration
```

The call saves the exact continuation. Parameter binding, lookup, and method
dispatch preserve evaluation order. The call allocates only a temporary scope;
it performs no heap allocation. `#pop` restores the environment, stack, scope
location, and continuation, and removes that scope. The claimed heap,
exception, return, and exit cells agree with this footprint.

Relevant priority rules for closure cells cannot match because this is an
ordinary unannotated closure and its frame has no `$cells` entry. Other
specialized calls have disjoint receiver, callable, method-name, or argument
patterns. The generic `Call` rule therefore routes this expression normally.

`swapC` has disjoint guards `65 <= C <= 90` and `97 <= C <= 122`; its `owise`
case is their complement. `mapSwap` has disjoint empty/cons equations and
strictly descends the sequence. Thus the result function is covered, terminating,
and non-overlapping in the supplied ASCII code-sequence model.

### Candidate-local extensions

There are six candidate-local directives in `verification.k`:

1. the `flipCaseBody` macro syntax and exact expansion;
2. the `solutionModule` macro syntax and exact expansion;
3. the `#runFlipCase` syntax and setup expansion.

The two macros are definitional aliases. The runner is a fresh entry helper,
not a bridge replacing an existing fixed-semantics operation; it preserves any
continuation and every state cell while placing the exact module load and call
in front. No local function, totality assertion, opaque symbol, priority,
simplification, answer-encoding rule, return shortcut, or unconstrained oracle
exists.

### Opaque and incomplete supplied features

The imported supplied baseline includes opaque or concrete-only symbols for
floats, sorting, and MD5, including `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`.
None is reachable from this submitted program or influences its branch,
result, state, exception, or postcondition.

The fresh compiler reported non-exhaustive `total` definitions for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None occurs
in the reachable term graph. Their presence is recorded as an unused supplied
trust boundary, not silently treated as evidence for this result.

### Intent-model limitation, with witness

The reachable supplied equations define ASCII switching, not Python Unicode
`swapcase`. `evidence/semantics_bridge_test.py` compared the exact supplied
single-code-point map with Python for every code point. It found zero ASCII
mismatches but 2,764 non-ASCII mismatches. Concrete witnesses include:

- `U+00E9` (`"é"`): supplied model leaves code 233 unchanged; Python returns
  `"É"` (`U+00C9`);
- `U+00DF` (`"ß"`): supplied model leaves code 223 unchanged; Python returns
  the two-character string `"SS"`.

Reachability-form K claims for those two supplied-model results exited 0 with
`#Top`. An initial attempt to state them as bare functional claims exited 113
because this backend does not support functional claims; that diagnostic is
preserved, and the supported reachability restatement succeeded. This
supplemental tool limitation did not affect any candidate claim.

I do not label the ASCII equations unsound within the selected supplied model:
they are truthful and exhaustive for that model. The narrower conclusion is
that interpreting `IntSeq` as arbitrary Python Unicode strings is not justified.
That bridge gap is material to the unrestricted natural-language `str`
contract and determines the `CONCERNS` verdict.

Evidence:

- `evidence/k_inventory.py`
- `evidence/rule-inventory.md`
- `evidence/stage5_rule_inventory.log`
- `evidence/reachable-rule-map.md`
- `evidence/semantics_bridge_test.py`
- `evidence/stage5_semantics_bridge.log`
- `evidence/unicode-model-witness.k`
- `evidence/stage5_kprove_unicode_model_functional_attempt.log`
- `evidence/stage5_kprove_unicode_model_reachability.log`

Stage 5 result: **PASS** for real-program soundness under the selected supplied
semantics, with the documented Unicode adequacy limitation.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation evidence was
trusted. I created `evidence/spec-vacuity.k`, which changes the result to:

```text
str(iCons(33, mapSwap(S)))
```

That mutation requires an impossible leading `"!"` on every result. The
satisfying concrete witness is `S = .IntSeq`: both Python implementations
return `""`, while the mutation requires `"!"`.
`evidence/mutation_witness.py` confirms this and exits 0.

The exact dry run:

```text
timeout 180s kprove /audit-output/evidence/spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run
```

exited 0, so the mutation parsed and built successfully. The actual proof run
used the same command without `--dry-run`; it exited 1 with
`WarnStuckClaimState`. The residual is the expected unmet result equality:

```text
iCons(33, mapSwap(S)) #Equals mapSwap(S)
```

The residual configuration had already executed the submitted function to
`str(mapSwap(S))`, so this is neither an unreachable mutation nor a parser,
import, timeout, or unrelated backend failure.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/mutation_witness.py`
- `evidence/stage6_mutation_witness.log`
- `evidence/stage6_mutation_dry_run.log`
- `evidence/stage6_mutation_kprove.log`

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the proof establishes

Under the byte-validated supplied K semantics, for every algebraic
`S:IntSeq`, starting in the displayed standard module state, execution of the
exact submitted MiniPy module followed by `flip_case(str(S))` reaches
`str(mapSwap(S))`. It leaves the installed `flip_case` closure in module scope,
restores the temporary call state, and leaves heap, stack, return, exception,
and exit-code cells as specified. This is a partial-correctness reachability
theorem: it states the result of terminating executions under the model.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.337 parser, compiler, Haskell/LLVM backends, and K built-in integer/Boolean/map/list operations | All builds and proofs | Standard low-level toolchain trust boundary; fresh reconstruction and discriminating mutation provide appropriate evidence but do not re-prove K itself. |
| `/reference/reference-semantics` | Defines MiniPy execution | Designated trusted supplied baseline and byte-identical in the candidate. The complete reachable path was audited. |
| Supplied `mapSwap`/`swapC` equations | Fix the theorem's returned value | Fully defined and non-opaque for ASCII case mapping. Acceptable for the formal theorem; concerning as a bridge to unrestricted Python Unicode strings. |
| Unused float/sort/MD5 opaque symbols and incomplete totalized functions listed in Stage 5 | Imported but not reached | No dependent branch, result, or cell in this proof; acceptable unused baseline boundary. |
| Trusted `/reference/py2mpy.py` and byte comparison | Connects `solution.py` to `solution.mpy` | Exact translator output identity, not an informal similarity claim. |
| Static macro-to-AST equality plus helper-free direct K claim | Connects `verification.k` aliases to the submitted MiniPy artifact | Strong source-pinning evidence. The candidate proof duplicates the AST rather than reading the file dynamically, but the independent exact-AST claim removes a material substitution concern. |
| `/reference/canonical.py` and Python execution | Connect implementation behavior to the HumanEval intent | Trusted reference oracle. Differential coverage is broad but finite; source inspection also shows the candidate and canonical use the same `str.swapcase()` operation. |
| Natural-language “character case” to supplied ASCII code map | Connects the formal theorem to all Python strings | Not universally valid. The Unicode counterexamples are the material adequacy concern. |
| Missing generation metadata and trace | Provenance only | Reduces auditability of how the candidate was generated, but does not alter the independently reconstructed source theorem. |

Differential testing, concrete K tests, and the natural-language explanation
support only their stated bridges. They are not treated as substitutes for the
successful reachability proof.

### Gate summary

- Gate A, real-program soundness: **PASS**. The exact body executes, all local
  extensions are definitional/setup-only, the result is fixed, a satisfiable
  state exists, and the false mutation is rejected for the expected reason.
- Gate B, intent adequacy: **LIMITED**. The theorem is adequate for the supplied
  ASCII code-sequence model but not a universal proof of Python Unicode
  `swapcase` behavior.
- Gate C, trust and evidence auditability: **PASS with provenance concern**.
  Reviewer evidence is reproducible and exact; the candidate's named generation
  metadata is absent.

The Unicode issue does not make a false candidate-local rule prove the target:
it limits what the otherwise sound supplied-semantics theorem says about the
unrestricted Python contract. The appropriate decision boundary is therefore
`CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
