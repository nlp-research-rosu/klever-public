# Independent adversarial audit: 2-truncate-number

## Audit conclusion

The candidate contains a legitimate but limited partial-correctness proof. A clean Haskell definition rebuilt from source, the only submitted positive claim closed with `#Top` and exit 0, the claim executes the exact submitted translated AST through the fixed supplied semantics, and both a false-result mutation and a changed-body mutation were rejected with the expected unmet result obligations.

The limitation is at the intent bridge. The symbolic proof establishes that the result is the supplied semantics' opaque `floatMod(N, 1.0)` primitive. It does not machine-prove in Haskell that this primitive is the mathematical decimal part or that it agrees universally with CPython's binary64 `%`. The trusted LLVM concrete equation, six independent K assertions, 276 positive-finite differential/oracle cases, and an ordinary mathematical argument support that bridge, but they do not turn it into a universal K theorem. The four requested provenance records are also absent. These are concerns, not evidence of a false conclusion or an execution shortcut.

Primary evidence:

| Evidence | Purpose |
|---|---|
| `evidence/stage1_integrity.log` | File types, symlink checks, trusted-input comparisons, recursive semantics comparison, hashes |
| `evidence/differential_test.py`, `evidence/stage2_fidelity.log` | Trusted translation and independent differential/oracle inputs and results |
| `evidence/audit_concrete.py`, `evidence/stage3_reconstruction.log` | Fresh tool versions, LLVM/Haskell builds, concrete execution, positive `#Top` |
| `evidence/rule_inventory.md`, `evidence/stage5_inventory_v2.log` | Exhaustive 931-item source inventory and inventory-generation check |
| `evidence/stage5_declaration_summary_v2.log` | Opaque, priority, function, and total declaration summaries |
| `evidence/ast_pin_check.py`, `evidence/stage5_body_sensitivity.log` | Exact AST pin and rejected changed-body proof |
| `evidence/ground_witness.py`, `evidence/stages4_6_ground_and_vacuity.log` | Satisfying ground states and fresh false-result mutation |
| `evidence/spec-vacuity.k` | Reviewer-authored false postcondition |

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode and mounts are consistent: this is `SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` exists. I found no infrastructure breach, so a candidate verdict is appropriate.

The candidate `reference-semantics/` tree and the trusted tree have the same regular-file/directory shape, contain no symlinks, and compare recursively with no missing, additional, or changed entries:

```text
diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics
[exit 0]
```

This integrity result selects the trusted supplied semantics; it does not bless `verification.k`, which is reviewed independently below.

### Trusted prompt and translator

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Both `cmp -s` commands exited 0. Their paired SHA-256 hashes also agree in `stage1_integrity.log`.

All candidate proof/program inputs used here are regular files. No candidate or trusted-semantics symlink was found.

### Missing provenance evidence

The following requested candidate records are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present under `/candidate`. Consequently, there were no generation claims, reports, or traces to rely on. Their absence limits auditability but does not alter the independently reconstructed proof result.

The candidate contains no compiled definition or cache to trust or reuse. The submitted source artifacts needed for the audit—`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, the supplied-semantics copy, prompt, and translator—are present.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt asks for the fractional/decimal part of a positive floating-point number after decomposition into an integer part and a remainder below one. The trusted canonical implementation is:

```python
def truncate_number(number: float) -> float:
    return number % 1.0
```

The phrase “largest integer smaller than” is imprecise at an exact integer; the canonical implementation resolves the intended behavior to zero for integer inputs. The meaningful intended domain is positive finite Python floats for which this decomposition is defined. The proof's formal domain is broader, as discussed in Stage 4.

`/candidate/solution.py` has the same executable function body and signature as the canonical implementation; it merely omits the docstring. There are no branches, loops, state changes, or alternate algorithms to reconcile.

### Trusted translation

I regenerated the mini-Python AST with the trusted translator:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/proof-audit/solution.regenerated.mpy
[exit 0]
cmp -s /candidate/solution.mpy /tmp/audit-work/proof-audit/solution.regenerated.mpy
[exit 0]
```

Both files have SHA-256 `5d32e9ddf2a574995accfcef87ffef589188b82d429829d07945f85142d5c4e0`. Thus the required byte-identity check passes.

### Independent differential test

`evidence/differential_test.py` independently imports `/reference/canonical.py` and `/candidate/solution.py`. It does not import candidate tests or proof equations. For the human-facing decimal-part oracle it uses `math.modf`, not the submitted `%` expression.

The preserved input set contains:

- the documented `3.5` example;
- the smallest positive subnormal, minimum positive normal, and maximum finite binary64 values;
- exact integers and immediate `nextafter` values on both sides of 1, 2, 3, 10, and \(2^{52}\);
- representative small and large positive values;
- 256 deterministic generated positive finite binary64 values across exponents -1073 through 1023;
- out-of-domain diagnostics for negatives, signed/unsigned zero, infinities, and NaN;
- an empty/missing-argument call, since there is no collection-valued “empty” case for this function.

All 276 intended-domain inputs were printed as exact hexadecimal floats. Results:

```text
CANONICAL_GENERATED_MISMATCHES=0
IN_DOMAIN_ORACLE_MISMATCHES=0
[exit 0]
```

The seven out-of-domain value diagnostics and the missing-argument call also agreed between the two Python implementations. This establishes strong finite fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

All work occurred under `/tmp/audit-work/proof-audit`; candidate files remained read-only. The scratch proof used a fresh copy of the trusted `/reference/reference-semantics`, not a candidate-built definition. Before compilation, the scratch directory contained no `*-kompiled` directory.

The independently installed toolchain was:

```text
K version:    v7.1.337
Build date:   Thu Jun 18 07:59:56 CDT 2026
```

### Fresh concrete definition

The concrete definition was built from trusted supplied source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
[exit 0]
```

The reviewer-authored `audit_concrete.py` was translated with the trusted translator. It asserts the documented case, an integer boundary, a below-one case, and representative fractional values through the real function call. `krun audit_concrete.mpy --definition concrete-kompiled` exited 0 with final `<k> .K </k>`, no exception, and exit code 0.

The LLVM build warned that several supplied total functions are not syntactically exhaustive (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`). None occurs on this program's execution slice. They are addressed as evidence gaps in Stage 5 rather than mislabeled as witnessed false rules.

### Fresh proof definition and every positive target claim

The candidate spec contains exactly one positive claim:

```text
rg -n '^[[:space:]]*claim([[:space:]]|$)' spec.k
10:  claim
[exit 0]
```

The proof definition rebuilt successfully:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
[exit 0]
```

The independently run target proof produced the complete success signal:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
#Top
[exit 0]
```

No helper, loop, or separately labeled positive claim exists to omit.

## 4. Adequacy and real-program pinning

### Plain-language claim

There is no explicit `requires` clause. The only input restriction is K's `N:Float` sort.

The starting state says:

- begin in the supplied semantics' default module state;
- execute `#loadAll(solutionProgram)`;
- then call the newly loaded `truncate_number` with `Float(N)`;
- start at environment 0 with empty module bindings and heap, empty stack, `noRet`, `NoExc`, and exit code 0.

The destination says:

- consume all computation and leave exactly `floatMod(N, 1.0)` in `<k>`;
- retain the loaded `truncate_number` closure in module scope 0;
- remove the temporary call frame and restore environment 0, `scopeLoc` 1, empty stack, `noRet`, unchanged empty heap, no exception, and exit code 0.

This is an equality-shaped result constraint, not a free variable, existential result, tautological `ensures`, or one-way implication.

### Exact program identity

The claim does not parse `solution.mpy` at runtime; `verification.k` defines a `solutionProgram` syntax macro. That macro is acceptable only if it is exactly the submitted AST. Three independent checks establish the pin:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. `evidence/ast_pin_check.py` extracts and whitespace-normalizes the macro and submitted AST;
3. the normalized forms agree exactly:

```text
submitted_normalized=Module(FuncDef("truncate_number",Params("number"),Return(BinOp("%",Name("number"),Float(1.0)))))
macro_normalized=Module(FuncDef("truncate_number",Params("number"),Return(BinOp("%",Name("number"),Float(1.0)))))
AST_MACRO_MATCH=True
[exit 0]
```

The macro expands to program syntax; it does not replace the call, return, or modulo execution.

### Satisfying states and concrete substitution

Because the claim has no `requires`, the exact stated initial cells with `N = 3.5` are a satisfying prestate. `N = 1.0` and `N = 0.25` are additional satisfying instances.

`evidence/ground_witness.py` substitutes all three values into the claimed `floatMod(N, 1.0)` result and compares it with both Python entry points:

```text
N=0x1.c000000000000p+1 claimed_floatMod=0x1.0000000000000p-1 canonical=0x1.0000000000000p-1 generated=0x1.0000000000000p-1 all_equal=True
N=0x1.0000000000000p+0 claimed_floatMod=0x0.0p+0 canonical=0x0.0p+0 generated=0x0.0p+0 all_equal=True
N=0x1.0000000000000p-2 claimed_floatMod=0x1.0000000000000p-2 canonical=0x1.0000000000000p-2 generated=0x1.0000000000000p-2 all_equal=True
```

The LLVM assertions independently confirm the K concrete primitive for these and related inputs.

An additional reviewer experiment asked the Haskell backend to reduce ground `floatMod` terms to float literals. It failed with the documented missing `FLOAT.div` hook before proving those auxiliary ground claims. This is not a failure of the submitted symbolic claim, which closed; it confirms that the Haskell proof treats `floatMod` as opaque and cannot itself discharge the numeric intent bridge.

### Adequacy limitation

The formal claim is stronger than the prompt on input sign because it structurally covers every K `Float`, but it is weaker in human-facing content: it does not state positivity, `0 <= result < 1`, or `result = N - floor(N)`. Those facts are delegated to the fixed `floatMod` primitive. The limitation does not permit a false result under the selected semantics, but it prevents an unqualified claim that K machine-proved the mathematical decimal-part characterization.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` scans the trusted supplied semantics, every helper K file, `verification.k`, and `spec.k`. It checks parsed counts against independent source-start counts and generated `evidence/rule_inventory.md`, which contains the complete text, source lines, classification, attributes, entry-slice status, and audit disposition of every local statement.

The 931 inventoried statements are:

| Source | Statements | Entry relevance |
|---|---:|---|
| `semantics.k` | 0 | assembly/import module |
| `assert.k` | 3 | out of slice |
| `bool.k` | 14 | out of slice |
| `builtins.k` | 175 | builtins scope term only; builtin execution out of slice |
| `call.k` | 24 | generic call and ordinary closure call used |
| `comprehension.k` | 10 | out of slice |
| `concrete.k` | 21 | concrete build only; sort/list rules out of slice |
| `controls.k` | 37 | out of slice |
| `core.k` | 84 | configuration, load, sequence, lookup, and argument evaluation used |
| `dict.k` | 40 | out of slice |
| `float.k` | 155 | float literal and float modulo dispatch used |
| `functions.k` | 19 | definition, binding, return, and pop used |
| `int.k` | 17 | out of slice |
| `iter.k` | 1 | out of slice |
| `list.k` | 32 | out of slice |
| `methods.k` | 102 | out of slice |
| `operators.k` | 12 | binary dispatch used |
| `range.k` | 8 | out of slice |
| `set.k` | 18 | out of slice |
| `sort.k` | 25 | out of slice |
| `str.k` | 33 | out of slice |
| `subscript.k` | 57 | out of slice |
| `syntax.k` | 16 | submitted AST syntax and strictness declarations used |
| `tuple.k` | 25 | out of slice |
| `verification.k` | 2 | exact AST macro declaration/equation |
| `spec.k` | 1 | submitted entry claim |

The inventory dispositions total 59 used fixed-semantics/proof items, 871 supplied items outside the entry slice, and one result-constraining claim with the `floatMod` boundary. “Out of slice” means its constructor, function head, operator tag, callee shape, or guarded cell pattern cannot occur in this claim; it does not mean the source was silently skipped.

### Construct-to-rule mapping and execution

| Submitted construct | Declaration and governing rules |
|---|---|
| `Module`, `Stmts` | `syntax.k:56,61`; `core.k:124-127` loads and sequences statements |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14-16` stores the closure in the current scope |
| `Call`, `Exprs` | `syntax.k:28,37`; `call.k:20-21` evaluates callee then arguments; `core.k:189-191` evaluates arguments left-to-right |
| `Name("truncate_number")`, `Name("number")` | `syntax.k:12`; `core.k:131-154` follows exact lexical scope bindings |
| closure invocation | `call.k:69-74` allocates the callee scope, changes `<env>`, and pushes the exact continuation frame |
| parameter binding | `functions.k:63-66` binds `"number"` to the evaluated float argument |
| `Return` | `syntax.k:50 [strict]`; `functions.k:78-90` records the value, pops the exact frame, restores environment/scope location, and resumes the saved continuation |
| `BinOp("%", ..., ...)` | `syntax.k:15 [seqstrict(2,3)]`; `operators.k:12` dispatches only after both operands are values |
| `Float(N)`, `Float(1.0)` | `syntax.k:10`; `float.k:20-21` turns literals into K `Float` values |
| float `%` | `float.k:37-39` maps two `Float` operands to `floatMod(F1,F2)` |

The actual flow is:

```text
#loadAll exact Module
→ install exact closure in scope 0
→ look up that closure
→ evaluate Float(N)
→ allocate scope 1 and bind number=N
→ evaluate Return strictly
→ look up number
→ evaluate Float(1.0)
→ applyBin("%", N, 1.0)
→ floatMod(N, 1.0)
→ return/pop
→ restore every final cell required by the claim
```

Cell footprints are exact:

- `<scopes>` gains the persistent module closure, temporarily gains scope 1, then deletes scope 1.
- `<env>` changes 0 → 1 → 0.
- `<scopeLoc>` changes 1 → 2 → 1.
- `<stack>` receives and removes exactly one `frame(.K, 0, 1)`.
- `<ret>` changes `noRet` → `retV(floatMod(...))` → `noRet`.
- `<heap>` and `<heapLoc>` never change.
- `<exc>` remains `NoExc`; `<exit-code>` remains 0.

### Functions, totality, overlaps, priorities, and simplifications

The full inventory enumerates all 145 source lines declaring a local `function`, `total`, or `functional` production. There are no local `[simplification]` rules. Every priority occurrence is listed in `stage5_declaration_summary_v2.log`.

On the entry slice:

- The generic call rule is `[owise]`; the higher-priority math/hash patterns require different callee syntax and cannot match `Name("truncate_number")`.
- Heap-reference operator priorities require `ref(...)`; both operands here have sort `Float`.
- Cell-variable lookup/bind priorities require a `"$cells"` marker absent from this ordinary closure frame.
- Annotated-closure rules require `closureValC`, while the program creates `closureVal`.
- Other `applyBin("%",...)` rules require two `Int` operands; the float rule is sort-disjoint.
- Duplicate mixed float arithmetic declarations elsewhere in `float.k` have identical right-hand sides on overlap and do not involve `%`.
- Generated strictness/heat-cool rules enforce callee-before-arguments, left-before-right binary evaluation, and expression-before-return; no competing rule changes that order.

The compiler's non-exhaustive-totality warnings concern terms outside this execution: `cellsMark` arguments to conversion/mapping helpers or an empty/opaque sequence passed to `valSeqAt`. They provide a narrower global coverage gap in the supplied language model. No rule among them yields a false conclusion witness on the intended input domain, and none is reachable from this program, so I do not label them unsound.

### Opaque symbols and proof-local extensions

The supplied semantics declares 22 `[no-evaluators]` symbols:

```text
sortVS, sortKeyVS, md5hexCodes,
intFloatDiv, divII, floatMod, floatLt, absF, subF, divF, addF,
mulF, powF, gtF, eqF, decStrToF, divFloatIntV, intToF,
truncF, roundF, roundFN, sqrtF
```

Only `floatMod` can influence this claim. All others require absent syntax, operators, builtins, methods, or data. `floatMod` is result-bearing, but it is a fixed external language primitive for `%`, not a proof-local abstraction of program-defined code. The proof is interpretation-parametric only in the limited statement “the program returns that primitive.” The separate claim that the primitive means the decimal part is conditional/empirical, not proved by reusing its name.

`verification.k` adds only:

1. `syntax Module ::= "solutionProgram" [macro]`;
2. its exact AST expansion.

This is a definitional source representation. It neither preempts a fixed semantic rule nor skips an operation. There are no proof-local helper functions, totals, opaque values, priorities, lemmas, simplifications, operational bridges, or loop claims.

### Soundness and body sensitivity

No inventoried candidate rule was found to encode the task answer, fabricate an unconstrained result, bypass a body, or enable a false conclusion on the intended domain. Therefore there is no unsound-rule allegation requiring a false-conclusion witness.

As an independent sensitivity test, I changed the macro body to `return 0.0`, adjusted the destination closure to that changed body, rebuilt a separate Haskell definition, and retained the real result obligation. The proof failed with exit 1 and the precise residual:

```text
0.0 #Equals floatMod(N, 1.0)
```

This shows the positive proof depends on the submitted body rather than merely the function name or destination shape.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created `evidence/spec-vacuity.k` independently and copied the identical file into scratch.

The mutation keeps the exact start state and all final cells but changes the result from `floatMod(N,1.0)` to constant `0.0`. It is demonstrably false for the satisfying input `N = 3.5`, for which both Python implementations and the concrete K run return `0.5`.

The mutated spec parsed and reached proof execution against the already fresh definition:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`; the residual implication is exactly:

```text
0.0 #Equals floatMod(N, 1.0)
```

The final configuration otherwise has the expected loaded closure, restored environment, empty stack/heap, `NoExc`, and exit code 0. This is an expected unmet result obligation, not a parser error, missing import, timeout, crash, or unreachable mutation. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the supplied K definition, for any K `Float` value `N`, starting from the exact default cells in `spec.k`, loading the exact submitted AST and calling `truncate_number(N)` executes the actual function body, terminates in the modeled execution, returns exactly `floatMod(N,1.0)`, installs the exact closure in module scope, and restores the call-related state exactly as claimed.

This statement is result-constraining and body-sensitive. It is a reachability theorem about the selected mini-Python semantics, not directly a universal theorem about CPython or real-number fractional parts.

### Trust and assumption ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| Trusted prompt/canonical pair | Defines human-facing intent and reference result | Authoritative task input; candidate body matches canonical |
| Trusted `py2mpy.py` | Connects Python source to mini-Python AST | Trusted mount; regenerated AST is byte-identical |
| Supplied mini-Python semantics | Calls, scopes, strictness, returns, and operator dispatch | Integrity-checked byte-for-byte; the used slice was reviewed rule-by-rule and rebuilt |
| `floatMod(Float,Float)` | Entire returned value/postcondition | Fixed opaque primitive, acceptable for a conditional structural theorem; not a Haskell-proved decimal-part theorem |
| `floatMod` LLVM concrete equation and K float hooks | Concrete modulo behavior | Six reviewer K assertions pass; the Haskell backend cannot evaluate the required `FLOAT.div` hook |
| CPython canonical/generated executions | Python behavioral bridge | 276 positive finite exact inputs plus diagnostics have zero mismatches |
| `math.modf` oracle | Human decimal/fractional-part bridge | Independent finite oracle, zero mismatches on all 276 intended inputs |
| Mathematical equivalence of positive finite `N % 1.0` and fractional part | Natural-language intent | Ordinary informal argument plus finite evidence; not formalized as a K claim |
| Other 21 opaque supplied symbols | None | Constructors/functions are outside the entry slice; no claim dependency |
| Missing generation/provenance records | Audit trail only | Concerning for provenance, but independent reconstruction supplies the decisive proof evidence |

For positive finite binary64 values, the informal argument is especially direct: values below one have floor zero; integers return zero; non-integers below \(2^{52}\) have exactly representable integer floors; above that threshold every binary64 value is integral. Nevertheless, the candidate did not encode or prove this argument in K.

Non-finite floats do not have the prompt's stated integer-plus-decimal decomposition. The structural K claim has no positivity/finiteness precondition and still returns an opaque term; no human-facing correctness conclusion is drawn for those values.

### Gate and verdict rationale

- Fresh reconstruction: **pass**.
- Real-program soundness, body sensitivity, and non-vacuity: **pass**.
- Intent adequacy: **limited but not false**. The proof establishes the fixed modulo primitive, while the decimal-part interpretation remains conditional/empirical.
- Evidence auditability: **concern** because the four provenance records are absent and the Haskell backend cannot check the numeric float equation.

A `FAIL / NOT_LEGIT` verdict would require a failed clean proof, substituted program, non-constraining postcondition, vacuity, or materially unsound rule. None was found. A completely unqualified `PASS` would overstate the opaque float bridge and provenance. The appropriate decision is therefore `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
