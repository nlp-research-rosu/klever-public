# Independent adversarial audit: 86-anti-shuffle

Audit result: **CONCERNS / LEGIT**. The dependency-complete reachability proof rebuilds cleanly, closes with `#Top`, constrains the returned value, and executes the actual translated program under the supplied semantics. I found no unsound proof-local rule. The concern is an explicit limitation rather than a legitimacy failure: symbolic sorting is represented by the supplied opaque primitive `sortVS`, so the human-facing statement that each word is an ascending permutation is conditional on that primitive's intended meaning and finite concrete evidence. The source-to-MPY bridge is likewise trusted and finitely tested, not proved in K.

All execution used fresh source copies in `/tmp/audit-work/86-anti-shuffle`. No candidate `*-kompiled` directory, cache, final configuration, trace, or reported `#Top` was reused.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is coherent with it: `/reference/reference-semantics` exists as a real directory. This is not an infrastructure-breach case.

I read `/candidate/run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the JSONL structured trace only as untrusted claims. They report a successful generation, positive proofs, negative probes, and a `VALIDATED` conclusion. The trace also records earlier stuck states and later edits. None of those reports supplied verdict-bearing evidence; their sizes and the claims extracted from them are recorded in [provenance_claims.log](evidence/provenance_claims.log).

The independent integrity check found:

- All required generation metadata and deliverables are regular, non-symlink files.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py` (SHA-256 `f8a02b3472de03cd4fa7b7d9d47abd5a5d64cb8eea267c81dc575e2a281aa972`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Recursive `diff --no-dereference -qr` between the trusted and candidate `reference-semantics/` trees exited 0. The candidate tree contains no symlink. Thus there is no missing, additional, changed, mistyped, or symlinked semantics entry.
- Candidate-supplied compiled definitions and mutation/test artifacts are additional top-level evidence, not required-source integrity failures. They were ignored for reconstruction.

The reusable checker, exact command, hashes, and status are in [integrity_audit.sh](evidence/integrity_audit.sh) and [integrity.log](evidence/integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`: `anti_shuffle(s)` takes a string, splits words specifically at literal spaces, sorts the characters of each word in ascending ASCII/code order, preserves word order, and preserves every blank space. The examples require `"Hi" -> "Hi"`, `"hello" -> "ehllo"`, and `"Hello World!!!" -> "Hello !!!Wdlor"`. The canonical implementation is `' '.join(''.join(sorted(list(i))) for i in s.split(' '))`.

### Source inspection and translation identity

`/candidate/solution.py` scans left to right. A non-space is appended to `word`; a space emits `sorted(word)` plus that exact space and clears `word`; termination emits the sorted final word. This is extensionally the canonical split/sort/join algorithm, including empty input, leading/trailing spaces, and runs of spaces.

Running the trusted translator over the scratch copy and comparing stdout directly against submitted `solution.mpy` gave byte identity (`cmp` exit 0). The translator therefore did not regenerate a substituted MPY program.

### Independent differential test

[differential_audit.py](evidence/differential_audit.py) imports the trusted canonical entry point and the scratch candidate entry point independently. It covers the three documented examples, 16 unique explicit boundary/branch cases, every unique string through length 5 over `" aAzZ09!~"`, and 1,991 unique deterministic longer generated cases over spaces, tabs/newlines, ASCII classes, and selected Unicode characters. Result: 68,432 unique inputs, zero mismatches, exit 0. The command, group counts, samples, and result digest are in [fidelity.log](evidence/fidelity.log).

This finite test supports source/canonical agreement; it is not the K proof and does not establish universal equivalence.

## 3. Clean proof reconstruction

K v7.1.293 was available independently. From the scratch source copy I built:

```text
kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
Exit 0

kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX --output-definition audit-verification-kompiled
Exit 0
```

The LLVM build emitted bounded exhaustiveness warnings for supplied partial/opaque helper domains; the Haskell build emitted only supplied `str.k` unused-variable warnings. Neither build emitted an error.

The positive proof reconstruction was:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant
#Top
Exit 0

kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
#Top
Exit 0
```

The complete command is the entry-proof result: both claims must be present because `SPEC.loop-invariant` is the circularity used by `SPEC.anti-shuffle`. As a diagnostic, filtering to `SPEC.anti-shuffle` alone removed that circularity and continued symbolic unrolling until I interrupted it after 8m24s with no output. That deliberately incomplete dependency run is neither a positive target command nor a candidate failure.

Fresh concrete execution of nine reviewer-authored ASCII normal/boundary assertions ended with `.K`, `NoExc`, empty stack, `noRet`, and exit code 0. Sources and bounded logs are [concrete_cases.py](evidence/concrete_cases.py) and [reconstruction.log](evidence/reconstruction.log).

Thus both the fresh dynamic-reconstruction gate and every dependency-complete positive target claim pass.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` starts at the real MPY `#loop` over remaining string codes `CS`, with exact global/builtin/local scope structure, current `result = OUT`, current `word = WORD`, arbitrary previous `char`, and an integer-key heap whose keys are all below `NEXT`. It says the loop consumes all of `CS`, updates `result` to `emittedAfter(CS, WORD, OUT)`, updates `word` to `wordAfter(CS, WORD)`, leaves `s` unchanged, preserves the framed continuation and other control cells, and leaves a heap/next pair still satisfying the freshness invariant.

`SPEC.anti-shuffle` starts from the supplied initial module state, executes `FuncDef("anti_shuffle", Params("s"), antiBody)`, performs ordinary lookup and calls it on `str(CS)`, and requires the final `<k>` value to be exactly `str(antiShuffleCodes(CS))`. Environment 0, scope location 1, empty stack, `noRet`, `NoExc`, and exit code 0 are pinned at the destination. Final scopes, garbage heap contents, and numeric heap location are existential because they are not part of the function-result contract.

### Satisfiability

The entry precondition is realized, for example, by `CS = .IntSeq` in the exact supplied initial configuration. A loop-precondition witness is `L = 1`, `CS = WORD = OUT = INPUT = OLDCHAR = .IntSeq`, `HEAP = .Map`, `NEXT = 0`, with the stated builtin, global, and local scopes; `keysBelow(.Map, 0)` is true. Fresh concrete execution also realizes the empty-input entry and returns the empty string.

### Actual program and result pinning

The entry claim begins immediately after the fixed loader's `#loadAll(Module(...))` step, not at an invented helper call. `antiBody`, `antiLoopBody`, and `antiFinalExpr` are macro abbreviations of the exact submitted AST. Independently running submitted `solution.mpy` and `proof-program.mpy` under the freshly built proof definition produced byte-identical complete final configurations (`cmp` exit 0). The trusted translator comparison separately pins `solution.py` to `solution.mpy`.

The call, name binding, argument evaluation, source body, loop, `list`, `sorted`, `join`, allocations, return, and frame pop all execute through supplied semantic rules. No proof-local rule intercepts `Call`, `#applyK`, `#loop`, allocation, `Return`, or `#pop`.

The return is not a free variable, tautology, or one-way implication: it is the input-dependent term `str(antiShuffleCodes(CS))`. Four ground substitutions (`""`, `"ba"`, `"a  b"`, and the long documented example) normalized to the expected code sequences in K and agreed with both Python implementations. See [model_witnesses.k](evidence/model_witnesses.k), [claim_witness_compare.py](evidence/claim_witness_compare.py), and [fidelity.log](evidence/fidelity.log).

The claim intentionally does not prove a reusable post-call module/heap identity. That weakening does not affect the requested returned string or normal-control result, and the temporary list objects do not escape.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.tsv](evidence/rule_inventory.tsv), generated by the reviewer-authored [k_inventory.py](evidence/k_inventory.py), contains 951 individually located entries: 232 syntax declarations, 711 rules, 5 contexts, 1 configuration, and 2 claims. It covers trusted `semantics.k`, every helper K file under `reference-semantics/semantics/`, candidate `verification.k`, and `spec.k`. Attributes recorded include every `function`/`functional`, `total`, `symbol`, `no-evaluators`, `concrete`, `priority`, `owise`, `macro`, `strict`/`seqstrict`, and `simplification` occurrence. Twenty-five supplied opaque declarations are labeled `BOUNDARY-OPAQUE`; only `sortVS` is reachable here.

`ACCEPT-NO-FALSE-WITNESS` in the inventory means the declaration/rule follows the selected supplied-semantics abstraction or ordinary mathematics on its declared domain, with no concrete or symbolic false-conclusion witness found. It is not a claim that this deliberately partial MPY language is a complete CPython semantics. Unused semantic modules were checked for overlap with the used syntax and proof helpers; they are unreachable from this submitted program and introduce no proof-local rewrite of its path.

### Construct coverage and used semantic path

Every submitted constructor is declared and has a used rule path:

| Submitted construct | Declaration/evaluation path |
|---|---|
| `Module`, statement sequence | `MPY-SYNTAX`; configuration and `#loadAll`/sequencing in `core.k` (inventory K0297, K0324-K0326) |
| `FuncDef`, `Params`, `Return` | `syntax.k`; closure creation, parameter binding, return, and frame pop in `functions.k` (K0565, K0577-K0582) |
| `Assign`, `If`, `For` | strict declarations in `syntax.k`; state update and branches/loop protocol in `controls.k` (K0248-K0249, K0260-K0269, K0274) |
| `Name`, `Str` | lexical lookup through exact local/global/builtin parents in `core.k` (K0327-K0330); ASCII program literals and string values in `str.k` (K0801 and neighbors) |
| `Compare`, `CmpOp`, `BinOp("+")` | left/right evaluation contexts and dispatch in `operators.k` (K0736-K0739); string equality/concatenation and structural `seqConcat` in `str.k` (K0805-K0807 and adjacent rules) |
| `Call`, `Attribute`, argument lists | callee-first and left-to-right argument evaluation in `call.k`/`core.k` (K0193-K0197, K0334-K0338), with exact local/global/builtin lookup |
| `list(word)` | actual builtin dispatch, fresh allocation, and `charsOf` recursion (K0029-K0032 plus allocator K0321-K0322) |
| `sorted(...)` | actual call/dereference/allocation path and supplied `sortVS` result (K0205, K0773-K0785) |
| `''.join(...)` | bound-method formation, list dereference, `applyMethod`, and `joinCodes` fold (K0193, K0211, K0641-K0645) |

Evaluation order is preserved by `seqstrict`/strict contexts and the shared `#evalArgs` loop. The entry scopes ensure `list` and `sorted` resolve to the builtin bindings rather than a shadowed oracle. Allocations write the heap and advance `heapLoc`; the proof neither removes those operations nor fabricates the return.

### Every proof-local extension

- K0931-K0938: the three macro declarations and three expansions are textually the real loop body, final expression, and full function body. They are syntax abbreviations, not operational bridges. Fresh macro-versus-submitted execution identity passed.
- K0939, `sortedWord(CS)`: exactly composes supplied `charsOf`, `sortVS`, and `joinCodes(.IntSeq, ...)`, matching the value from `''.join(sorted(list(word)))`. It does not rewrite a program call.
- K0940-K0942, `emittedAfter`: empty, space-head, and guarded non-space-head cases are exhaustive and disjoint. The recursive call strictly consumes `REST`; the space case matches the source's left-associated concatenation and preserves one literal space.
- K0943-K0945, `wordAfter`: the same exhaustive/disjoint structural split tracks the current word and strictly consumes `REST`.
- K0946, `antiShuffleCodes`: concatenates the emitted prefix with exactly one final `sortedWord` of the remaining word, matching the source return.
- K0947-K0948, `keysBelow`: `.Map` and recursive unique integer-map cases define that every heap key is below `NEXT`. AC map-choice overlaps yield the same conjunction.
- K0949: if every integer heap key is below `NEXT`, then `NEXT` is absent. This is a true guarded freshness lemma.
- K0950-K0951: raising an integer bound by 1 or 2 preserves the strict upper-bound property. Both guarded simplifications are true; overlaps agree on `true`.

The scan helpers are declared total with complete constructor coverage and decreasing recursion. `keysBelow` is deliberately not total on arbitrary maps with non-integer keys; fixed allocation starts from `.Map` and adds only integer keys, so every use is covered. No false off-domain equation is added.

The auxiliary loop claim is a proved reachability circularity, not an ordinary semantic rewrite. Its framed suffix is safe: the exact body has no `return`, exception, `break`, `continue`, cleanup, or other abrupt effect, and neither loop iteration nor the summaries inspect the suffix. Its entry use has exactly the builtin/global/local binding chain and freshness invariant in its justification scope. There are zero proof-local operational bridges, so no bridge admits a broader continuation or different state footprint requiring a separate continuation-sensitivity mutation.

No inventoried proof-local rule was labeled unsound. Consequently there is no unsoundness accusation requiring a false-conclusion witness. The narrower evidence gaps are the explicitly opaque sort meaning and finite translator/model adequacy evidence discussed in stage 7.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`. The fresh mutation [audit_vacuity.k](evidence/audit_vacuity.k) uses the satisfiable initial state and concrete input `""`, but changes the result-constraining destination from the true `str(.IntSeq)` to false `str(iCons(33, .IntSeq))` (`"!"`).

It parsed, built, executed through the real function, and exited 1 with `WarnStuckClaimState`. The residual `<k>` is the actual `str(.IntSeq) ~> .K`, with normal environment/control and two real temporary list allocations; it cannot unify with the false destination. This is the expected unmet obligation, not an import error, parser failure, timeout, unrelated crash, or unreachable mutation. Exact command and bounded residual: [vacuity.log](evidence/vacuity.log).

The proof is therefore discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Conditioned on the supplied MPY semantics and proof-local mathematical equations, for every modeled `CS:IntSeq`, if the exact translated `anti_shuffle` call terminates from the stated fresh module configuration, it returns `str(antiShuffleCodes(CS))` with normal control. The loop proof formally establishes the left-to-right delimiter scan, preservation of each literal space, current-word accumulation, emission placement, ordinary calls/allocations, and final concatenation. It is a partial-correctness result, not a liveness/total-correctness theorem.

### Trust ledger

| Boundary | Effect and dependents | Assessment/evidence |
|---|---|---|
| Supplied `sortVS(ValSeq)` (`sort.k`, inventory K0773) | Determines the character order within every `sortedWord`; therefore affects both claims and the natural-language “ascending permutation” conclusion | Acceptable fixed trusted primitive for this mode, but a real evidence limitation. It is opaque on symbolic lists; concrete insertion-sort rules run on ground strings. Nine fresh concrete K assertions passed, ground model witnesses normalized, and the Python differential had zero mismatches. These finite facts do not universally prove the opaque contract. |
| Supplied MPY semantics and K/Haskell/LLVM/SMT implementation | Defines all value, state, control, and proof behavior | Required trusted foundation selected by the problem. Integrity matched the trusted tree; both definitions were rebuilt, positive proofs closed, concrete tests ran, and the negative mutation was rejected. |
| Trusted `py2mpy.py` translation boundary | Connects `solution.py` to the actual submitted MPY AST | Submitted MPY is byte-identical to fresh trusted translation. The source agrees with the canonical function on 68,432 cases, and fresh MPY concrete tests cover normal and boundary ASCII cases. This is strong finite evidence, not a universal compiler-correctness theorem. |
| Proof-local scan and allocator equations | Enable symbolic loop closure and fresh allocation | Audited as total/disjoint/decreasing where declared total and as true guarded integer-map mathematics. They are not oracles and do not replace program execution. |
| MPY string model | Formal inputs are `IntSeq`; program literals are ASCII-only. Full CPython Unicode/exception/resource behavior is absent | The prompt expressly asks for ASCII ordering, and the theorem is honest about the MPY domain. Unicode cases in the Python differential support source agreement only; they do not enlarge concrete MPY literal support. |

The candidate's `PROOF.md`, generation trace, and differential results were not used as substitutes for the K proof. The fresh differential supports only the source/canonical bridge; the fresh K assertions support only the tested concrete semantics; neither discharges the universal `sortVS` assumption.

### Decision

The proof is sound under its disclosed supplied-semantics trust boundary, constrains the result, and pins the real translated program. There is no material adequacy gap warranting `FAIL / NOT_LEGIT`. It does not merit an unconditional `PASS`, because the requested ascending-order meaning is not derived symbolically: it remains conditional on opaque `sortVS` plus finite evidence, with a second finite bridge through the translator. Under the required decision boundary, that is `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
