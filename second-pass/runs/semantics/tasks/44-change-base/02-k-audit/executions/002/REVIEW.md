# Independent adversarial review: 44-change-base

## Executive conclusion

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted `solution.mpy` under the supplied MPY semantics.
Both reachability claims close after a clean rebuild, the proof executes the
submitted recursive body, and independent body and postcondition mutations are
rejected for the expected reasons.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
source prompt leaves the nonnegative-input/lower-base assumptions implicit and
the supplied semantics deliberately models unbounded recursion rather than
CPython's finite recursion limit. Those are non-fatal intent/model boundaries:
the proof covers the material base-conversion domain, `x >= 0` and
`2 <= base < 10`, without a finite-size bound.

## 1. Input and provenance integrity

The launcher declares:

- problem `44-change-base`, condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` exists, and the candidate's
`reference-semantics` has the same 25 non-root entries (one directory and 24
regular files), no symlink or unsupported entry, and byte-identical contents.
There is no candidate modification, omission, or addition in that tree.

The campaign-lock JSON is exactly equal to the `audit_campaign` block in
`audit-input.json`; its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. Direct hashes for `run.json`, `task.json`,
`generation-result.json`, the invocation and metrics, usage, prompt, output,
last-message record, canonical implementation, trusted prompt, and translator
all match. The independently computed pipeline tree digest for the mounted
candidate is
`bf35f7abd3089fe22dc3395c66123fcc2a5ab11d5cccd02c5eeb42de4481b6b7`,
matching the generation result and invocation; the trace-tree digest is
`7c393e07a6a2a0df509e022514267338cc545cdd5593172ad8678bff6b2177c8`,
matching `usage.json`. The supplied-semantics pipeline digest on both mounts is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.

All records required for `legacy-selected-stage1` are real, readable regular
files or real directories. `usage.json` is present and was inspected.
Historical runtime metrics are not required for this layout. The one structured
trace file was independently parsed as 355 valid JSON events; all event types,
tool calls, and bounded readable previews are recorded. Generation-time
`KPROVE_PASSED`, `#Top`, and prose were treated only as untrusted history.

The candidate prompt and translator are byte-identical to their trusted mounts.
All required proof artifacts (`solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, and `prove.sh`) are present as regular files. There is no
infrastructure breach.

Evidence:

- [provenance check](evidence/01-provenance-check.log)
- [generation records](evidence/01-generation-records.log)
- [structured trace parser](evidence/01-generation-trace-parse.log)
- [structured trace inventory](evidence/01-generation-trace-summary.tsv)
- [toolchain versions](evidence/01-toolchain.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks `change_base(x: int, base: int)` to return the string
representation of `x` in a base below 10. A numerical base is conventionally
at least 2. The trusted canonical implementation repeatedly prepends
`str(x % base)` while `x > 0`, updates `x //= base`, and returns the accumulated
string. Its canonical zero result is the empty string.

The generated implementation uses equivalent recursion on the material domain:

```python
if x == 0:
    return ""
return change_base(x // base, base) + chr(48 + x % base)
```

For `x > 0` and `2 <= base < 10`, `x % base` is in `0..8`,
`chr(48 + remainder)` is exactly the decimal digit character, and
`x // base < x`. The recursive and iterative algorithms therefore produce the
same big-endian digits; both return `""` at zero.

Running the trusted translator and piping its output directly to `cmp` against
the submitted `solution.mpy` exits 0. Thus the submitted constructor term is a
byte-faithful trusted translation, not a hand-edited substitute.

The independent differential script imports the trusted canonical entry point
and generated entry point separately. It covers all examples; `x=0` and
`x=1`; bases 2 and 9; values immediately below, at, and above powers for every
base 2 through 9; and 2,000 deterministic generated integers up to `10**50`.
There were 2,430 distinct in-domain cases and zero mismatches.

The same script records excluded/model-boundary behavior rather than hiding it:
negative `x` returns `""` in the canonical implementation but eventually raises
`RecursionError` in the generated recursive Python; a positive 1,201-bit
binary input likewise exposes CPython's recursion limit, while the iterative
canonical function returns normally. These are not a finite restriction in the
K claim. Negative numerals are not a material intended behavior—the canonical
does not implement signed conversion either—but this ambiguity and the
recursion-model difference motivate the `CONCERNS` verdict.

Evidence:

- [trusted source, submitted source, constructor term, and claims](evidence/02-source-and-claims.log)
- [trusted translator inspection](evidence/02-trusted-translator.log)
- [translation identity](evidence/02-translation-identity.log)
- [differential script](evidence/differential_test.py)
- [differential results](evidence/02-differential.log)

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/44-change-base`; the semantics copy came from the trusted
reference mount. No candidate-built definition or cache was copied.

The observed toolchain is K `v7.1.293` and Python `3.10.12`, matching the
campaign's K version. Fresh commands and results were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
exit 0

krun concrete_tests.mpy --definition runtime-kompiled
exit 0; final .K, NoExc, exit-code 0

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
exit 0

kprove spec.k --definition verification-kompiled --spec-module SPEC
exit 0; #Top
```

The LLVM compiler reports several non-exhaustive `total` declarations in
unused fixed-semantics features (`mapStrVS`, float helpers, `joinCodes`, and
`valSeqAt`). None is reachable from this program; no proof-local declaration is
`total`. The Haskell build has only unused-variable warnings.

Every positive claim also has a staged independent record. An exact copy of the
recursive-call claim in `SPEC-APPLY-ONLY` exits 0 with `#Top`. A labeled copy of
both original claims then marks that already-proved helper as trusted and proves
the remaining whole-module target:

```text
kprove spec-labeled.k --definition verification-kompiled \
  --spec-module SPEC-LABELED --trusted SPEC-LABELED.apply
exit 0; #Top
```

The `--trusted` use here is proof staging, not an unproved assumption: the exact
helper was first proved against the same clean definition. The unlabelled
original two-claim run independently closes all claims as well.

For transparency, two helper-free isolation diagnostics and one
`--claims`/`--trusted` filter experiment were interrupted. Removing or filtering
the recursive-call circularity changes the dependency graph and causes
unbounded recursive unrolling; those diagnostics are not treated as candidate
failures or positive evidence.

Evidence:

- [LLVM build](evidence/03-kompile-llvm.log)
- [concrete run](evidence/03-krun-candidate-tests.log)
- [Haskell build](evidence/03-kompile-haskell.log)
- [original two-claim proof](evidence/03-kprove-all.log)
- [recursive helper proof](evidence/03-kprove-apply-only.log)
- [whole-module proof with separately proved helper](evidence/03-kprove-module-trusted-helper.log)

## 4. Adequacy and real-program pinning

### Claim 1: recursive call

In plain language, for every `X >= 0` and `2 <= B < 10`, the first claim starts
an exact call to the `change_base` closure with arguments `(X,B)` in any
continuation `K`. It permits arbitrary framed heap and continuation state but
requires a fresh positive scope allocator satisfying `freshScopes`. It proves
that the call returns `str(baseDigits(X,B))` immediately before the same
continuation and restores every displayed state cell: environment, scopes,
scope allocator, heap, heap allocator, stack, return state, exception state,
and exit code.

A concrete satisfying state is:
`X=8`, `B=3`, `K=.K`, `L=0`, `FRAMES=.Map`, `N=1`, `H=.Map`,
`HL=0`, `ST=.List`, and `EC=0`. Here `freshScopes(1,.Map)` reduces to true.

### Claim 2: whole submitted module

For every `X >= 0` and `2 <= B < 10`, the second claim loads
`solutionModule` from the exact initial module/builtins state, calls
`change_base(X,B)`, and reaches exactly `str(baseDigits(X,B))` with no exception
or exit-code change. Its scope rewrite also requires the actual function
binding to remain installed; all other displayed cells are fixed.

The mechanical constructor comparison expands `changeBaseBody` inside
`solutionModule`, normalizes only the translator's empty statement-list spelling
(`""` versus `.Stmts`), and compares the complete constructor text. The
expanded claim module and trusted-regenerated `solution.mpy` are both 484
whitespace-free characters and byte-equal after that inert normalization. The
function name, parameter order, closure body, and defining scope also match.

Ground substitution checks for `(0,2)`, `(1,2)`, `(8,3)`, `(9,9)`, `(31,5)`,
and `(999,9)` reduce the claimed digit sequence to, respectively, `""`, `"1"`,
`"22"`, `"10"`, `"111"`, and `"1330"`; both Python implementations return the
same values.

Body sensitivity was tested separately from postcondition non-vacuity. A fresh
definition changed the digit constructor actually executed by the claim from
`Int(48)` to `Int(49)`, while retaining the original postcondition. It compiled
successfully, but `kprove` exited 1 with a `WarnStuckClaimState` whose residual
requires equality between otherwise identical sequences ending in
`remainder + 48` and `remainder + 49`. The theorem is therefore sensitive to
the real body.

Evidence:

- [constructor-level comparison script](evidence/program_term_compare.py)
- [constructor comparison result](evidence/04-program-term-compare.log)
- [satisfiable and ground witnesses](evidence/04-claim-witnesses.log)
- [body mutant](evidence/verification-body-mutant.k)
- [body-mutant build](evidence/04-kompile-body-mutant.log)
- [body-mutant rejection](evidence/04-kprove-body-mutant.log)

## 5. Rule-by-rule static soundness review

The exhaustive lexical inventory contains 1,112 K sentences. It includes every
module/include/import, 232 syntax declarations, the configuration, all five
contexts, 705 rules (695 supplied-semantics rules and 10 proof-local rules), and
both claims. Each row records source lines, attributes, relevance, decision,
and normalized text.

The submitted program uses these constructor/control families:

- `Module`, `FuncDef`, `Params`, statement sequencing, docstring `Expr`, `If`,
  `Return`;
- `Name`, `Int`, `Str`, `Compare`, `CmpOp`, `BinOp`, and `Call`;
- module loading, lexical lookup, closure construction, left-to-right callee
  and argument evaluation, scope allocation, parameter binding, return, frame
  pop, and state restoration;
- integer `==`, `//`, `%`, and `+`; string concatenation; and builtin `chr`.

The supplied declarations and rules cover every item. `BinOp` is
`seqstrict(2,3)`, comparison contexts evaluate left then right, `If` is strict
in the guard, and the call rules evaluate the callee followed by arguments
left-to-right. Recursive lookup selects the module binding through the frame's
parent. With the claim guards, the remainder is `0 <= r < B < 10`, so the
ASCII-only `chr` rule's `0 <= 48+r < 128` guard always holds. Return pops the
callee frame, restores the exact caller continuation and environment, deletes
the fresh scope, and restores the saved scope allocator. No used operation
changes the heap, exception, output, or exit-code cells.

### Proof-local extension inventory

| Extension | Class and decision | Complete justification |
|---|---|---|
| `freshScopes` syntax and base/step rules | Definitional invariant; accepted | It recognizes a consecutive descending suffix of allocated scope keys. Base and step domains are disjoint. |
| `L in_keys(S) => false requires freshScopes(L,S)` | Derived lemma; accepted | Induction on the only ways `freshScopes(L,S)` can become true shows every key in `S` is below `L`; hence `L` is absent. |
| Fresh insertion normalization | Derived K-Map equality; accepted | If `L` is absent, `S[L <- V]` equals disjoint union `(L |-> V) S`. It exposes the fixed call rule's symbolic state update and does not invent a value or control effect. |
| Unique deletion normalization | Derived K-Map equality; accepted | If `L` is absent from `S`, deleting `L` from `(L |-> V) S` equals `S`. This exactly models the fixed frame-pop update. |
| `changeBaseBody`, `solutionModule`, `changeBaseClosure` | Definitional aliases; accepted | Mechanical expansion pins the exact binding, parameters, body, and scope. No execution is skipped. |
| `baseDigits` zero and positive equations | Mathematical summary; accepted | Guards are disjoint; for `N>0,B>=2`, the recursive quotient is a nonnegative strict decrease and the appended code is the remainder digit. The symbol is partial outside that domain and is not declared `total`. |

The local theory has five `[function]` declarations, no `[total]` declaration,
no opaque/no-evaluator symbol, no priority rule, and two simplification rules
(the two `baseDigits` equations). Pairwise overlaps are either disjoint or
agree. No local rule intercepts the submitted call or replaces the function
body with an oracle. The first claim is a coinductive reachability
circularity over the exact call state, not an operational rewrite smuggling the
answer.

The fixed semantics contains opaque float, sorting, and MD5 boundaries and the
LLVM totality warnings noted above. They are all unreachable from this
constructor tree and cannot influence its branch, result, state, or claim.
Without a reachable false-conclusion witness, they are recorded as unused
fixed-semantics limitations, not labeled unsound.

Evidence:

- [complete rule inventory](evidence/05-rule-inventory.tsv)
- [inventory counts](evidence/05-rule-inventory-summary.log)
- [used semantics, part A](evidence/05-used-semantics-a.log)
- [used semantics, part B](evidence/05-used-semantics-b.log)
- [remaining supplied semantics](evidence/05-unused-semantics.log)

## 6. Fresh non-vacuity test

The valid fresh mutation retains the correctly proved recursive helper and
changes only the whole-module destination from:

```text
str(baseDigits(X,B))
```

to:

```text
str(seqConcat(baseDigits(X,B), iCons(48,.IntSeq)))
```

It therefore requires one spurious trailing zero digit. The state
`X=0,B=2` satisfies the target precondition; real execution and the original
claim return `""`, while the mutant requires `"0"`.

`kprove --dry-run` exits 0, proving the artifact parses and builds. The live
proof exits 1 with `WarnStuckClaimState` at the mutated target and the direct
unmet condition:

```text
baseDigits(X,B) !=
seqConcat(baseDigits(X,B), iCons(48,.IntSeq))
```

This is the expected semantic rejection, not a parser error, timeout, or
unrelated crash.

An earlier attempted mutation of the arbitrary-continuation helper reached an
unrelated unavailable float-min hook after its result mismatch and is preserved
as invalid evidence; it is not counted. Replacing it, rather than accepting an
arbitrary nonzero exit, is material to this audit.

Evidence:

- [valid false-result spec](evidence/spec-vacuity.k)
- [valid mutation dry run](evidence/06-vacuity-dry-run.log)
- [valid mutation rejection](evidence/06-kprove-vacuity.log)
- [invalid first attempt](evidence/spec-vacuity-invalid-arbitrary-continuation.k)
- [invalid-attempt log](evidence/06-kprove-vacuity-invalid.log)

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY definition plus the audited proof-local equalities, for
all mathematical integers `X >= 0` and `2 <= B < 10`, executing the exact
submitted constructor program from the claimed initial state reaches
`str(baseDigits(X,B))` with `NoExc`, exit code 0, empty heap, restored call
state, and the exact installed module binding. The helper establishes the same
return for an exact closure invocation in every continuation and every
allocator/store state satisfying `freshScopes`.

`baseDigits(0,B)` is empty; for positive `N`, it is the digits of the quotient
followed by character code `48 + (N mod B)`. This is partial correctness: the
reachability proof does not itself claim termination.

### Trust ledger

- **K toolchain and logical kernel.** The Haskell backend, reachability
  circularity mechanism, and hooked `INT`, `MAP`, `STRING`, Boolean, and
  equality operations are trusted. Every proof depends on this standard
  machine-checking boundary.
- **Supplied MPY semantics.** Its exact trusted bytes are the fixed language
  model. The target depends only on the manually reviewed module/call/return,
  scope, integer, string, and `chr` subset. Unused float/sort/MD5 abstractions
  have no dependent path.
- **Translator.** The trusted translator is a syntactic CPython-AST
  transliterator. Its relevant `FunctionDef`, `If`, `Return`, `Call`,
  `Compare`, and `BinOp` clauses were inspected; byte regeneration and
  constructor expansion connect the source to the theorem.
- **K Map equalities and `freshScopes` lemma.** These proof-local facts are
  justified by ordinary finite-map algebra and induction. They influence only
  symbolic exposure and restoration of the call frame; they do not influence
  the digit value.
- **Intent bridge.** The mathematical statement that quotient/remainder digit
  recursion is base conversion is ordinary arithmetic, supported—though not
  universally proved by—2,430 independent differential cases.
- **Model/domain limits.** The theorem excludes negative `x` and invalid bases,
  and the fixed model has unbounded symbolic call stacks rather than CPython's
  `RecursionError`. These are the documented reason for `CONCERNS`, not an
  unsound proof shortcut or a finite bound on the material HumanEval domain.

### Gate and benchmark decision

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy on the material nonnegative base-conversion domain:
  **PASS with the documented implicit-domain/CPython-stack limitation**.
- Gate C, trust and evidence auditability: **PASS**.

The proof is non-vacuous, constrains the returned value, executes the exact
submitted body, and quantifies over all nonnegative integers rather than fixed
examples or bounded sizes. The remaining limitations are non-fatal trust and
intent boundaries, so the candidate is legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
