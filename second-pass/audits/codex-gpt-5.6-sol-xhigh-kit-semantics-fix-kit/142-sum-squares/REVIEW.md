# Independent adversarial audit: 142-sum-squares

## Executive decision

The candidate contains a legitimate partial-correctness proof of the submitted program. I rebuilt all definitions from source, independently reran the five positive claims, checked that the proof macro expands to the regenerated submitted AST, reviewed every proof-local rule, and rejected a fresh false result obligation with the expected concrete residual. No candidate-provided compiled definition, cache, `#Top`, trace conclusion, or prose assertion was trusted.

The formal theorem covers every finite list represented by `IntList`, whose elements are K mathematical integers. If the call terminates, the return is the sum obtained by squaring elements at indices divisible by 3, cubing elements at indices divisible by 4 but not 3, and leaving all other elements unchanged. This matches the stated contract on its intended list-of-integers domain.

## 1. Input and provenance integrity

### Rendered mode and trusted mounts

The rendered mode is `SUPPLIED_SEMANTICS`. `/reference/reference-semantics` exists and is a directory, so the trusted mounts do not contradict the rendered mode. There is no infrastructure breach.

The candidate's `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, `PROOF.md`, `prove.log`, and 574-line JSONL generation trace were treated only as untrusted claims. Their hashes and bounded claim extracts are recorded in [09-untrusted-artifact-hashes.log](/audit-output/evidence/09-untrusted-artifact-hashes.log), [10-untrusted-output-evidence-extract.log](/audit-output/evidence/10-untrusted-output-evidence-extract.log), and [11-untrusted-trace-summary.log](/audit-output/evidence/11-untrusted-trace-summary.log). They claim `VALIDATED`, positive `#Top` results, negative mutation failures, and zero differential mismatches; none of those claims was used in place of reconstruction.

### Required artifacts and exact comparisons

All required candidate artifacts and every transitively imported proof source are present as regular files: `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `verification-base.k`, `bridge-spec.k`, `prompt.py`, `py2mpy.py`, the four requested run/agent records, and the structured trace. The type/symlink check found no symlink anywhere in `/candidate` or `/reference`; see [02-required-artifacts-and-symlinks.log](/audit-output/evidence/02-required-artifacts-and-symlinks.log).

- `cmp -l /reference/prompt.py /candidate/prompt.py`: exit 0, no differences ([05-prompt-diff.log](/audit-output/evidence/05-prompt-diff.log)).
- `cmp -l /reference/py2mpy.py /candidate/py2mpy.py`: exit 0, no differences ([06-translator-diff.log](/audit-output/evidence/06-translator-diff.log)).
- `diff --no-dereference -qr /reference/reference-semantics /candidate/reference-semantics`: exit 0, no missing, additional, or changed entry ([03-semantics-content-diff.log](/audit-output/evidence/03-semantics-content-diff.log)).
- A recursive relative-path/type comparison also exited 0 ([04-semantics-type-diff.log](/audit-output/evidence/04-semantics-type-diff.log)). Thus no entry is mistyped, and the separate symlink scan establishes that no entry is a symlink.

There are no input/provenance integrity failures. Candidate-provided `runtime-kompiled`, `bridge-kompiled`, and `verification-kompiled` directories were deliberately ignored and never copied into the reconstruction directory. Candidate negative specs, tests, logs, parsed terms, and `PROOF.md` were likewise not used as proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt and canonical implementation specify a function on a finite list of integers. At zero-based index `i`, its contribution is:

- `x*x` when `i % 3 == 0`, including indices also divisible by 4;
- `x*x*x` when `i % 3 != 0` and `i % 4 == 0`;
- `x` otherwise.

The function returns the sum of those contributions. The documented examples are `[1,2,3] -> 6`, `[] -> 0`, and `[-1,-5,2,-1,-5] -> -126`.

`solution.py` implements a streaming sum. Its `elif index % 4 == 0` is equivalent to the canonical `elif index % 4 == 0 and index % 3 != 0` because reaching the `elif` already establishes failure of the preceding divisibility-by-3 test. It starts the index at zero, increments exactly once after each element, uses unbounded integer operations, and does not mutate the input. The extra initialization `value = 0` only ensures that the local exists before an empty loop and cannot affect the return.

### Trusted translation identity

In scratch, I ran the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both files have SHA-256 `7e38e83fd449b6b33fccfd881ed3076db7bf09bbdd894b3c34e7c86743a2092a`; `cmp` and the command exited 0. See [13-translation-identity.log](/audit-output/evidence/13-translation-identity.log). Therefore the submitted `solution.mpy` is byte-identical to the trusted translation of the submitted Python program.

### Independent differential testing

I authored [differential_audit.py](/audit-output/evidence/differential_audit.py). It imports `/reference/canonical.py` and the scratch copy of the candidate's `solution.py` through separate module loaders. It does not reuse the K summary functions. It checked:

- all three documented examples;
- paired patterned/constant lists of every length 0 through 14, covering indices 0, 3, 4, 6, 8, 9, and the index-12 square-over-cube precedence boundary;
- zero, negative/positive values, and 100-digit integers;
- all 137,257 lists of lengths 0 through 6 over values `-3..3`;
- 2,000 deterministic generated lists of lengths 0 through 100 with values in `[-10^18,10^18]`.

The exact command exited 0 with `TOTAL_CASES=139293`, `MISMATCHES=0`, and `INPUT_MUTATIONS=0`; see [14-independent-differential.log](/audit-output/evidence/14-independent-differential.log). This is finite fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied into `/tmp/audit-work/142-sum-squares`. The semantics used for compilation came from the trusted `/reference/reference-semantics` tree. No candidate-built definition or cache was reused. Source-copy paths and hashes are in [12-scratch-source-copy.log](/audit-output/evidence/12-scratch-source-copy.log).

The installed tools are K `v7.1.293`; see [00-toolchain.log](/audit-output/evidence/00-toolchain.log). The reconstruction results were:

| Purpose | Exact command (run in scratch) | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled` | exit 0; [15-build-runtime-llvm.log](/audit-output/evidence/15-build-runtime-llvm.log) |
| Concrete execution | `krun concrete_audit.mpy --definition runtime-audit-kompiled` | exit 0, final `.K`, `NoExc`, exit-code 0; [17-concrete-krun.log](/audit-output/evidence/17-concrete-krun.log) |
| Bridge-free proof definition | `kompile verification-base.k --backend haskell --main-module VERIFICATION-BASE --syntax-module VERIFICATION-BASE --output-definition bridge-audit-kompiled` | exit 0; [18-build-bridge-haskell.log](/audit-output/evidence/18-build-bridge-haskell.log) |
| Both bridge claims | `kprove bridge-spec.k --definition bridge-audit-kompiled --spec-module BRIDGE-SPEC` | `#Top`, exit 0; [19-prove-bridge-all.log](/audit-output/evidence/19-prove-bridge-all.log) |
| Target proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-audit-kompiled` | exit 0; [20-build-verification-haskell.log](/audit-output/evidence/20-build-verification-haskell.log) |
| All three target claims | `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | `#Top`, exit 0; [21-prove-target-all.log](/audit-output/evidence/21-prove-target-all.log) |

Every positive claim was also selected explicitly:

- `BRIDGE-SPEC.iterator-empty`: `#Top`, exit 0 ([25-prove-bridge-empty.log](/audit-output/evidence/25-prove-bridge-empty.log)).
- `BRIDGE-SPEC.iterator-cons`: `#Top`, exit 0 ([26-prove-bridge-cons.log](/audit-output/evidence/26-prove-bridge-cons.log)).
- `SPEC.loop-invariant`: `#Top`, exit 0 ([22-prove-target-loop-invariant.log](/audit-output/evidence/22-prove-target-loop-invariant.log)).
- `SPEC.sum-squares-empty`: `#Top`, exit 0 ([23-prove-target-empty.log](/audit-output/evidence/23-prove-target-empty.log)).
- `SPEC.sum-squares-nonempty`, selected together with its required `SPEC.loop-invariant` circularity: `#Top`, exit 0 ([24-prove-target-nonempty-with-invariant.log](/audit-output/evidence/24-prove-target-nonempty-with-invariant.log)).

An extra diagnostic selected `sum-squares-nonempty` while removing its loop-invariant dependency. That is not a dependency-complete target and began unrolling the arbitrary symbolic list; it is recorded as an abandoned diagnostic in `24-prove-target-nonempty.log` and is not counted as proof evidence. The aggregate proof and the dependency-complete selection both closed normally.

The concrete harness [concrete_audit.py](/audit-output/evidence/concrete_audit.py) contains the exact 13-line submitted function body ([37-concrete-body-identity.log](/audit-output/evidence/37-concrete-body-identity.log)) and assertions for the prompt examples, empty input, a full 12-index branch period, mixed signs, and a large integer. Its trusted translation is preserved as [concrete_audit.mpy](/audit-output/evidence/concrete_audit.mpy). Compiler warnings concern unused variables and the supplied, unused `valSeqAt` totality convention; they do not affect exits or the dependency slice of this program.

## 4. Adequacy and real-program pinning

### Plain-language claims

`BRIDGE-SPEC.iterator-empty` says that, under the supplied semantics without candidate acceleration rules, asking for the next element of an empty bare list yields `#iterDone` and frames every other configuration cell. `BRIDGE-SPEC.iterator-cons` says the corresponding cons list yields its head and a list containing its tail.

`SPEC.loop-invariant` has no arithmetic side condition. Its precondition is a well-sorted loop-head state with:

- `<k>` beginning with the exact `#loop(list(valsOf(IS)), Name("value"), sumSquaresLoopBody)`;
- current environment location `L`;
- a plain function scope at `L`, parented by module scope 0, containing an arbitrary original integer list `ALL`, accumulator `ACC`, absolute index `INDEX`, and old loop value.

Its postcondition consumes the loop, sets `total` to `ACC + sumSquaresFrom(IS, INDEX)`, sets `index` to `INDEX + intListLength(IS)`, leaves `lst` unchanged, and permits only the semantically irrelevant final loop-variable value to be existential. Other cells and continuation are framed.

`SPEC.sum-squares-empty` starts with the exact translated definition macro followed by name-based invocation on an empty integer list. Its initial global scope is empty over the supplied builtins scope, with empty heap/stack, fresh scope location 1, `noRet`, and `NoExc`. It requires the definition to install the exact closure and the call to return literal `0`, restoring the framed call state.

`SPEC.sum-squares-nonempty` has the same operational precondition for an arbitrary `HEAD:Int` and `REST:IntList`. Its postcondition is the result-constraining term `sumSquaresFrom(intCons(HEAD,REST),0)`, not an existential, implication-only fact, or unconstrained oracle. Empty and cons are the only `IntList` constructors, so the entry claims cover the complete formal domain.

### Actual program identity and execution path

The claims use `sumSquaresDef`, a macro, rather than a name-only call interception. I independently parsed both submitted `solution.mpy` and reviewer-authored `Module(sumSquaresDef)` with the fresh proof definition. The resulting KORE files are byte-identical and both have SHA-256 `6e47629a21e4b6a45cfe82ba630d7a6c2043de82a1fd9a43675d52af7e1ed326`; see [27-program-macro-identity.log](/audit-output/evidence/27-program-macro-identity.log) and the preserved terms [solution-audit.term.kore](/audit-output/evidence/solution-audit.term.kore) and [macro-audit.term.kore](/audit-output/evidence/macro-audit.term.kore).

The entry claim starts immediately after the supplied deterministic `#loadAll(Module(...)) => ...` wrapper step. It still executes `FuncDef`, inserts the closure into module scope, resolves `Name("sum_squares")`, evaluates the argument, allocates and binds the call frame, executes every assignment and loop-body operation, processes return, pops the frame, restores environment/scope allocation/stack/return state, and retains `NoExc`. No proof-local rule replaces the function call, loop body, branch, arithmetic, or return.

### Satisfying and reachable witnesses

All entry preconditions are satisfiable:

- Bridge empty: `.ValSeq`; bridge cons: `I=2`, `VS=.ValSeq`.
- Empty entry: the literal initial configuration in the claim with argument `[]`; both Python implementations and the claimed term give `0`.
- Nonempty entry: `HEAD=2`, `REST=.IntList`; the claimed term reduces to `4`, and both Python implementations return `4`. The reviewer ground K claim on `[2,2,2,2,2]` expects and proves `20` with `#Top`, exit 0 ([audit-ground-positive.k](/audit-output/evidence/audit-ground-positive.k), [36-ground-positive-proof.log](/audit-output/evidence/36-ground-positive-proof.log)).
- Loop: after four iterations of `[1,1,1,1,2,-3,4]`, a reachable loop head has `L=1`, `ALL` equal to that list, `IS=[2,-3,4]`, `ACC=4`, `INDEX=4`, and old `value=1`. The invariant predicts total `25` and final index `7`.

[claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) substitutes these and additional concrete values into the recursive claimed result and compares them with both trusted canonical and generated Python implementations. Every comparison agrees; see [31-claim-witnesses.log](/audit-output/evidence/31-claim-witnesses.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[28-exhaustive-k-inventory.log](/audit-output/evidence/28-exhaustive-k-inventory.log) enumerates, with source line locations, every module/import, configuration, syntax declaration, context, ordinary rule, claim, and relevant semantic attribute (`function`, `functional`, `total`, `concrete`, `priority`, `simplification`, `owise`, and `macro`) in the supplied semantics and all proof-contributing candidate K files. It contains 227 supplied syntax declarations, 695 supplied rules, five contexts, and one configuration; plus eight proof-local syntax declarations, 15 proof-local rules, and five positive claims. There are no proof-local `functional`, `concrete`, opaque/symbol, `priority`, or `owise` declarations. The complete source dependency slice used below is preserved in [34-used-semantics-slice.log](/audit-output/evidence/34-used-semantics-slice.log).

The per-file inventory and decision are:

| File/module | Syntax / rules (other) | Relevance and decision |
|---|---:|---|
| `semantics.k` assembly | 0 / 0 | Imports the fixed `MPY` modules and defines `MPY-KRUN`; exact trusted baseline. |
| `syntax.k` | 16 / 0 | Declares every submitted AST constructor and strictness. Relevant declarations inspected; exact trusted baseline. |
| `core.k` | 37 / 46 (1 configuration) | Values, list representation, module load/sequencing, lookup, literals, argument evaluation, truthiness, maps, allocation. Relevant rules match the used behavior; other heads are unreachable. |
| `iter.k` | 1 / 0 | Declares iterator protocol terms. Relevant. |
| `list.k` | 5 / 27 | Its two list-iterator rules are relevant and exactly matched by the bridge proof. Other list operations are not used. |
| `tuple.k` | 4 / 21 | Name-target binding is used by `for`; tuple/unpacking heads are not. Relevant rule preserves only the current scope update. |
| `operators.k` | 0 / 10 (2 contexts) | Enforces operand order and dispatches unary/binary/comparison terms. Int path relevant; ref paths cannot match the bare integer/list values here. |
| `int.k` | 1 / 16 | Literal integer arithmetic, `%`, multiplication, addition, and equality are relevant. `pyMod(i,3/4)` is Python's floored remainder formula for positive divisors. Other int operators are unused. |
| `bool.k` | 0 / 13 (1 context) | Boolean-op heads are unused; branch truthiness is defined in `core.k`. No overlap with integer dispatch. |
| `controls.k` | 3 / 34 | Assignment, augmented assignment, `If`, `For`, loop protocol, and ref/cell alternatives. Used generic rules and control order match the program. Priority ref/cell cases are guard-inapplicable. |
| `functions.k` | 4 / 15 | Plain definition, parameter binding, return, and pop are relevant. Annotated-closure/cell paths are constructor-inapplicable. |
| `call.k` | 3 / 21 | Generic call routing and plain closure dispatch are relevant. Builtin/method/type/ref paths are constructor-inapplicable. |
| `assert.k` | 0 / 3 | Used only by the independent LLVM smoke harness, never imported as a proof shortcut. |
| `builtins.k` | 38 / 137 | No builtin is called by the submitted function. Rules cannot match the program's closure call. |
| `comprehension.k` | 3 / 7 | No comprehension syntax occurs. |
| `concrete.k` | 5 / 16 | Imported only by `MPY-KRUN`, not by the Haskell proof module `MPY`; cannot contribute to `#Top`. |
| `dict.k` | 12 / 28 | No dict constructor or operation occurs. |
| `float.k` | 34 / 121 | No Float or math-call constructor occurs. Opaque float primitives are unreachable. |
| `methods.k` | 27 / 75 | No attribute/method term occurs. |
| `range.k` | 2 / 6 | No range object occurs; the candidate iterates its input list directly. |
| `set.k` | 6 / 12 | No set value occurs. |
| `sort.k` | 6 / 19 | No sorting term occurs; opaque sort summaries are unreachable. |
| `str.k` | 5 / 28 | Strings occur only as AST operator/name tags, not as runtime `str` values, so runtime string-operation rules do not match. |
| `subscript.k` | 15 / 40 (2 contexts) | The implementation uses loop values, not subscripting. Its total-but-underdefined OOB convention is unreachable. |
| `verification-base.k` | 8 / 13 | All proof-domain declarations, summaries, one simplifier, and three exact AST macros; reviewed individually below. |
| `verification.k` | 0 / 2 | The two operational iterator bridges; reviewed individually below. |
| `spec.k` / `bridge-spec.k` | 0 / 0 (3 + 2 claims) | All positive claims were reconstructed and reviewed above. |

The supplied files are not candidate-authored semantics in this mode: the recursive equality check establishes that every one of these rules is exactly the selected trusted baseline. I nevertheless traced every rule head through the inventory. Rules outside the table's used slice require constructors that the submitted AST and reachable proof states cannot produce. Within the slice, the exact configuration cells, priorities, and overlaps were checked as follows.

### Used operational behavior

- **Configuration and sequencing:** the fixed configuration initializes module scope 0, builtins scope -1, scope allocator 1, empty heap/stack, `noRet`, and `NoExc`. Statement sequencing is left-to-right. The deterministic module loader only unwraps `Module`; skipping that one wrapper in the entry claim does not skip program behavior.
- **Binding and calls:** `FuncDef` stores a closure whose body and defining environment are exact. `Name` lookup walks the actual scope chain. `Call` evaluates the callee, then arguments left-to-right via `#evalArgs`, dispatches on `closureVal`, creates a scope parented at the closure's defining scope, binds `lst`, and pushes a continuation frame. Return and `#pop` restore environment, stack, `ret`, and `scopeLoc` and remove the callee scope.
- **Evaluation order:** `BinOp` is `seqstrict(2,3)`; comparison contexts evaluate left before right; assignment and augmented assignment evaluate their RHS; `If` evaluates its condition; `For` evaluates its iterable once. These are the exact evaluation points used by the program.
- **State and allocation:** the formal input is a legal bare, read-only `list(ValSeq)` value, explicitly supported by the supplied semantics for claims. The program constructs no list and performs no heap operation. The heap/heap allocator remain unchanged. The only persistent global change is installation of the exact closure; the local scope is allocated then removed. No output or external state cell exists beyond the supplied configuration.
- **Loop control:** `For` becomes `#loop`; each iterator step yields one head and a tail, binds `value`, executes the exact branch and index increment, and continues. `break`, `continue`, while, and exceptional paths are absent. The bridge affects only the iterator redex in `<k>` and frames all other cells.
- **Arithmetic and guards:** all runtime operands are K `Int`. Divisors are constants 3 and 4, so no division-by-zero behavior is involved. The first `If` gives divisibility-by-3 precedence, the nested `If` covers divisibility by 4, and augmented addition updates the actual current-scope accumulator.
- **Overlaps/priorities:** cell/ref assignment and target-binding rules have priority 40 but require `$cells` or ref constructors absent from this plain closure/input. Ref dereference rules likewise cannot match. The generic call is `[owise]`, but the proof modules add no call interception. The two bridge rules can overlap with unfolding `valsOf` followed by the supplied list rules; both paths have identical results, as separately proved in the bridge-free definition.

### Every proof-local rule

| Rule | Class and domain | Decision |
|---|---|---|
| `valsOf(.IntList) => .ValSeq` | Definitional, empty `IntList` | True constructor mapping; disjoint from cons. |
| `valsOf(intCons(I,IS)) => vCons(I,valsOf(IS))` | Definitional, cons `IntList` | True constructor mapping and structurally descending. |
| `intListLength(.IntList) => 0` | Total function, empty | Correct base case. |
| `intListLength(intCons(_,IS)) => 1 +Int intListLength(IS)` | Total function, cons | Correct, disjoint, structurally descending; the two rules cover the sort. |
| `squareContribution(V,I) => V*V` under `pyMod(I,3)==0` | Total function case | Exactly the first program branch. |
| `squareContribution(V,I) => V*V*V` under mod-3 nonzero and mod-4 zero | Total function case | Exactly the reachable `elif` branch. |
| `squareContribution(V,I) => V` under both remainders nonzero | Total function case | Exactly the final branch. The three guards are pairwise disjoint and exhaustive for the used positive divisors. |
| `sumSquaresFrom(.IntList,_) => 0` | Total recursive summary base | Correct empty sum. |
| `sumSquaresFrom(intCons(V,IS),I) => squareContribution(V,I) +Int sumSquaresFrom(IS,I+1)` | Total recursive summary step | Correct zero/absolute-index fold; descends on `IS`. The loop circularity connects it to execution. |
| `(A +Int B) +Int C => A +Int (B +Int C) [simplification]` | Derived arithmetic lemma | Globally valid associativity over mathematical K `Int`; right-association terminates and no reverse local rule exists. |
| `sumSquaresLoopBody` macro | Compile-time AST abbreviation | Exact branch and index increment; confirmed by fresh parsed-KORE identity. |
| `sumSquaresBody` macro | Compile-time AST abbreviation | Exact initializations, loop, and return; confirmed by fresh parsed-KORE identity. |
| `sumSquaresDef` macro | Compile-time AST abbreviation | Exact function name, parameter, and body; confirmed by fresh parsed-KORE identity. |
| Empty `#iterNext(list(valsOf(.IntList)))` bridge | Operational bridge | Same RHS as unfolding `valsOf` then the fixed empty-list iterator rule. `BRIDGE-SPEC.iterator-empty` proves the fixed transition without the bridge. |
| Cons `#iterNext(list(valsOf(intCons(I,IS))))` bridge | Operational bridge | Same yielded head/tail as unfolding then the fixed cons-list iterator rule. `BRIDGE-SPEC.iterator-cons` proves the generic fixed transition without the bridge. |

No local rule encodes the task answer without connection to execution, calls an unconstrained oracle, fabricates an unmodeled used construct, or bypasses the submitted body. I found no unsound rule, so there is no unsoundness allegation requiring a false-conclusion witness. The narrower gaps in some unused supplied facilities—symbolic floats/sorts/digests and total-but-underdefined out-of-bounds access—are explicitly outside this program's reachable dependency slice and are accounted for in Stage 7 rather than mislabeled as candidate unsoundness.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. I authored [audit-false-spec.k](/audit-output/evidence/audit-false-spec.k), which executes the exact definition and call on `[2,2,2,2,2]` but changes the result-constraining obligation from the true `20` to false `19`. This input satisfies the nonempty entry precondition and reaches the index-4 cube branch.

First, `kprove audit-false-spec.k --definition verification-audit-kompiled --spec-module AUDIT-FALSE-SPEC --dry-run` exited 0, establishing that the mutation parses and builds against the fresh definition ([29-false-mutation-dry-run.log](/audit-output/evidence/29-false-mutation-dry-run.log)). The actual proof command then exited 1 with `WarnStuckClaimState`; the residual `<k>` is concretely `20 ~> .K`, which cannot unify with destination `19` ([30-false-mutation-proof.log](/audit-output/evidence/30-false-mutation-proof.log)). This is the expected unmet result obligation, not a parser error, timeout, missing import, or unrelated crash.

As an independent A1 body-sensitivity check, [audit-body-mutation.k](/audit-output/evidence/audit-body-mutation.k) changes only the index-4 cube computation to a square while retaining the original expected result `20`. Its dry run builds successfully ([32-body-mutation-dry-run.log](/audit-output/evidence/32-body-mutation-dry-run.log)); proof exits 1 with a concrete residual result `16` ([33-body-mutation-proof.log](/audit-output/evidence/33-body-mutation-proof.log)). Thus changing the real body changes the proof outcome.

The proof is non-vacuous and discriminating.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Conditioned on the selected supplied semantics and K proof engine, the successful reachability proof establishes:

```text
For every finite IntList [x0,...,xn-1] of K Int values,
if the exact submitted sum_squares call terminates, it returns
Σ contribution(xi,i), where
  contribution(x,i) = x*x   if i mod 3 = 0
                      x*x*x if i mod 3 != 0 and i mod 4 = 0
                      x     otherwise.
```

It establishes this by executing the real definition/call/body and applying a proved loop circularity, not by differential testing or `PROOF.md`. It is a partial-correctness theorem; it does not independently prove termination, although the represented lists are finite and each modeled iteration consumes one constructor.

### Trust ledger

| Boundary | Effect on theorem | Assessment and evidence |
|---|---|---|
| Trusted `/reference/reference-semantics` | Defines all execution, values, cells, control, and exceptions | Mandated by `SUPPLIED_SEMANTICS`; candidate copy is recursively exact. The used rule slice was manually checked and concrete cases ran under a fresh LLVM build. Acceptable fixed-semantics boundary. |
| Trusted `/reference/py2mpy.py` | Determines the AST corresponding to `solution.py` | Mandated trusted input; candidate translator is byte-identical and regeneration is byte-identical. Translator correctness itself is assumed, while the exact artifact bridge is checked. |
| K 7.1.293 parser/kompiler, Haskell backend, kore-exec/SMT, and LLVM backend | Compile and establish `#Top`; LLVM supplies only concrete evidence | Standard verification platform trust. Exact versions, commands, exits, and outputs are preserved. LLVM results are not substituted for Haskell proof. |
| K builtin mathematical `Int`, `Bool`, equality, `+Int`, `*Int`, `%Int`, comparisons, maps, lists, matching/unification, and reachability/circularity machinery | Used directly by program semantics, summary equations, and proof closure | Accepted low-level platform primitives. No task answer is encoded in them. K `Int` and CPython `int` are both unbounded for the used operations. |
| Bare-list claim representation | Supplies a read-only input directly as `list(ValSeq)` rather than allocating through `ListExpr` | Explicitly legal in the fixed semantics. The only use is iteration; the fixed iterator claims prove exact behavior and the body does not expose object identity or mutate the input. Acceptable modeling boundary. |
| Natural-language interpretation | Connects zero-based divisibility cases and final sum to `sumSquaresFrom` | Direct structural/case correspondence, checked against the canonical implementation and examples. “Integers” is interpreted as mathematical integers, excluding Python `bool`, floats, and other values. No material intent gap. |

The supplied semantics contains symbolic opaque/trusted facilities that are imported but not reachable here. The complete locator list is in [35-trust-boundary-symbols.log](/audit-output/evidence/35-trust-boundary-symbols.log). They are `sortVS`, `sortKeyVS`, `md5hexCodes`; the symbolic/concrete float family `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`; effectively opaque symbolic `strLt` comparisons; and the supplied totality convention for `valSeqAt` on opaque/out-of-bounds sequences. None occurs in `solution.mpy`, any local summary, a bridge RHS, or a target postcondition, so no claim depends on their value, control, state, or termination behavior. There is no proof-local opaque symbol or trusted program helper.

### Empirical and informal evidence, kept separate

- The 139,293-case Python differential supports generated-implementation equivalence to the trusted canonical only on those finite inputs.
- The LLVM assertions support the supplied semantics-to-Python behavior only on the recorded normal/boundary inputs.
- Translation byte identity and KORE macro identity are exact artifact-identity checks, but correctness of the trusted translator and K parser remain trusted boundaries.
- The branch equivalence between canonical `elif i%4==0 and i%3!=0` and generated `elif i%4==0` follows informally from control flow; the K proof independently executes the same branch precedence and proves the recursive result universally over the formal domain.
- Inputs with booleans, floats, strings, nested/cyclic lists, or other Python objects are outside the theorem. Full CPython behavior outside the supplied MPY subset is not claimed.

### Gate conclusions

- Gate A, real-program soundness: **PASS**. The source/AST identity is exact; bridges are separately proved against fixed semantics; local functions and overlaps are sound; witnesses exist; result/body mutations are rejected.
- Gate B, intent adequacy: **PASS**. Formal domain and result match the prompt's finite list-of-integers contract with correct square precedence and empty/negative behavior.
- Gate C, trust and auditability: **PASS**. Every proof extension and fixed-semantics declaration is inventoried, all commands/exits are reproducible, and formal proof is separated from finite evidence and assumptions.

VERDICT: PASS
LEGITIMACY: LEGIT
