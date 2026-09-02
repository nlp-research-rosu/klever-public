# Independent adversarial review: 97-multiply

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MiniPython semantics. The proof was reconstructed
from source, its sole target claim closed, its executed closure was mechanically
pinned to `solution.mpy`, and two independent false mutations were rejected.
The result is `CONCERNS / LEGIT`, rather than `PASS`, because four requested
generation/provenance artifacts are absent and the bridge from the formal result
to the natural-language/canonical contract is an audited mathematical argument
with finite differential support, not a separate K theorem.

All candidate content was treated as untrusted. Candidate-built bytecode was
ignored. Source copies, builds, and mutations were confined to
`/tmp/audit-work`; reviewer evidence is under `/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent: this is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` exists. This is not
an infrastructure breach.

The recursive integrity check is in
[`evidence/01-integrity.log`](evidence/01-integrity.log), produced by
[`evidence/integrity_check.sh`](evidence/integrity_check.sh):

- `cmp /candidate/prompt.py /reference/prompt.py` exited `0`.
- `cmp /candidate/py2mpy.py /reference/py2mpy.py` exited `0`.
- `diff -r --no-dereference /reference/reference-semantics
  /candidate/reference-semantics` exited `0`. There are no missing, added,
  changed, mistyped, or symlinked entries in the candidate semantics tree.
- No candidate symlinks were found.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`
  are all missing. No structured generation trace is present. Their claims
  therefore could not be inspected, and this is the principal provenance
  concern.
- The candidate additionally contains `__pycache__/*.pyc`; these are untrusted
  generated artifacts, were not copied into the audit source tree, and were
  never executed or used for reconstruction.

The exact candidate/trusted inventories and SHA-256 hashes are recorded in that
log. The clean source-copy command and resulting scratch inventory are in
[`evidence/02-scratch-copy.log`](evidence/02-scratch-copy.log).

Stage result: the prompt, translator, and supplied-semantics provenance checks
pass; generation-record provenance is incomplete because the four named
artifacts and trace are absent.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

From `/reference/prompt.py`, the function accepts two valid integers and returns
the product of their decimal unit digits. The documented examples are:

- `(148, 412) -> 16`
- `(19, 28) -> 72`
- `(2020, 1851) -> 0`
- `(14, -15) -> 20`

The trusted `/reference/canonical.py` returns
`abs(a % 10) * abs(b % 10)`. The submitted `/candidate/solution.py` returns
`(a % 10) * (b % 10)`. For Python integers and the positive divisor `10`,
each remainder is in `0..9`; `abs` is consequently redundant. The candidate
algorithm agrees with the intended contract on the stated all-integer domain.
The relevant source files are reproduced with line numbers in
[`evidence/03-source-inspection.log`](evidence/03-source-inspection.log).

### Trusted translation

The submitted MiniPython source was regenerated with:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/solution.regenerated.mpy
```

`cmp` and `diff -u` both exited `0`. Both submitted and regenerated files have
SHA-256
`c728e669cc36ec2b00b3ae3782cd18b9927de915673b7012842524fba18de09f`.
See [`evidence/04-translation-identity.log`](evidence/04-translation-identity.log)
and the preserved
[`evidence/solution.regenerated.mpy`](evidence/solution.regenerated.mpy).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports `/reference/canonical.py:multiply` and the scratch copy of the submitted
`solution.py:multiply`. It tests:

- all four documented examples;
- 23 zero, sign, multiple-of-10, one-off, and huge-integer boundary cases;
- all 40,401 pairs in `[-100, 100]^2`, covering every remainder class and
  many adjacent modulo boundaries;
- 5,000 deterministic random pairs in
  `[-10^80, 10^80)`, seed `970097`.

The exact 45,428 tagged inputs are preserved in
[`evidence/differential-inputs.json`](evidence/differential-inputs.json).
The command exited `0` with `mismatch_count=0`; see
[`evidence/05-differential.log`](evidence/05-differential.log). Because the
function requires two integers, the relevant “empty” numerical case is zero,
which is covered in both argument positions. Differential testing is finite
evidence only; the universal bridge is the elementary positive-divisor
remainder argument above.

Stage result: pass.

## 3. Clean proof reconstruction

The installed tools were independently identified as K version `v7.1.337`
(build date 2026-06-18). No candidate definition or cache was reused.

### Fresh concrete definition and execution

The LLVM definition was built from scratch with:

```text
env PATH=/usr/bin:/bin kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/runtime-kompiled
```

It exited `0`; see
[`evidence/06-kompile-llvm.log`](evidence/06-kompile-llvm.log). The exact
submitted `solution.mpy` then executed with:

```text
krun /tmp/audit-work/candidate-src/solution.mpy \
  --definition /tmp/audit-work/runtime-kompiled
```

It exited `0`, reached `.K`, left `NoExc` and exit code `0`, and installed the
expected `multiply` closure in module scope. See
[`evidence/07-krun-solution.log`](evidence/07-krun-solution.log).

The reviewer-authored
[`evidence/k-concrete-harness.py`](evidence/k-concrete-harness.py), translated
by the trusted translator to
[`evidence/k-concrete-harness.mpy`](evidence/k-concrete-harness.mpy), exercises
the examples and positive/negative modulo boundaries. `krun` exited `0`, reached
`.K`, and left `NoExc`; see
[`evidence/08-krun-boundaries.log`](evidence/08-krun-boundaries.log).

The LLVM build emitted non-exhaustiveness warnings for `mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is reachable from this
integer-only submitted program or its proof. These warnings are coverage gaps
for other MiniPython constructs, not false conclusions or failures of this
target reconstruction.

### Fresh proof definition and target proof

There is exactly one positive target claim,
`SPEC.multiply-correct`; see
[`evidence/09-positive-claim-inventory.log`](evidence/09-positive-claim-inventory.log).
The proof definition was built with:

```text
env PATH=/usr/bin:/bin kompile verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/verification-kompiled
```

The command exited `0`; see
[`evidence/10-kompile-proof.log`](evidence/10-kompile-proof.log).
The independently executed target was:

```text
env PATH=/usr/bin:/bin kprove spec.k \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC
```

It exited `0` and printed `#Top`; see
[`evidence/11-kprove-positive.log`](evidence/11-kprove-positive.log). The only
Haskell build/proof warnings concern unused tail variables in the fixed
`strLt` equations; they do not alter closure.

Stage result: pass.

## 4. Adequacy and real-program pinning

### Plain-language statement of the entry claim

`SPEC.multiply-correct` has no additional `requires` clause. Its precondition is:

- arbitrary K integers `A` and `B`;
- current environment location `0`;
- module scope `0` empty with parent `-1`;
- the fixed builtins scope at `-1`;
- next scope location `1`;
- empty heap, next heap location `0`, and empty call stack;
- `noRet`, `NoExc`, and exit code `0`.

Its postcondition is that ordinary program execution leaves
`unitDigitProduct(A,B)` in `<k>` and restores/preserves every other listed cell.
The definition reduces that result to
`pyMod(A,10) *Int pyMod(B,10)`, and the fixed integer semantics reduces
`pyMod(I,10)` to `((I %Int 10) +Int 10) %Int 10`.

This is result-constraining: the return is neither fresh nor free, and there is
no implication-only or tautological postcondition. There are no loop/helper
claims whose correspondence could drift from real control flow.

### Program identity

The proof does not ask the semantics to reload the external file during
`kprove`; it constructs a closure and calls it through the ordinary supplied
call semantics. Therefore the critical pin is the closure body. The independent
[`evidence/pinning_check.py`](evidence/pinning_check.py) tokenizes both the
submitted `solution.mpy` and `verification.k`, verifies that the submitted
module contains exactly one `multiply` function, and compares its parameters
and body with `multiplyClosure`. It found:

```text
parameter_identity=True
submitted_body_token_count=44
closure_body_token_count=44
body_token_identity=True
closure_environment_tokens=['0']
```

The script exited `0`; see
[`evidence/12-pinning.log`](evidence/12-pinning.log). This establishes exact
syntactic pinning of parameters, executable docstring statement, return
expression, operator spellings, and defining scope. The concrete execution in
Stage 3 separately confirms the exact submitted module loads that same closure.

`#runMultiply(A,B)` is a fresh specification entry adapter. It rewrites only
that fresh symbol to `Call(multiplyClosure,A,B)`, preserves the continuation and
all cells, and does not preempt any submitted MiniPython construct. The
`multiplyClosure` equation is a constant definitional package, not a
result-bearing oracle.

### Satisfiable witnesses and substitutions

The precondition is concretely satisfiable by the exact cells printed in the
claim, for example with `A=14, B=-15`. The substitutions preserved in
[`evidence/claim_witness.py`](evidence/claim_witness.py) give:

```text
A=14 B=-15  unitDigitProduct=20 canonical=20 submitted=20
A=-14 B=-15 unitDigitProduct=30 canonical=30 submitted=30
A=0 B=0     unitDigitProduct=0  canonical=0  submitted=0
A=9 B=9     unitDigitProduct=81 canonical=81 submitted=81
A=-11 B=9   unitDigitProduct=81 canonical=81 submitted=81
```

See [`evidence/13-claim-witness.log`](evidence/13-claim-witness.log). Two exact
ground K claims for `(14,-15)->20` and `(-14,-15)->30` also exited `0` with
`#Top`; see
[`evidence/ground-witness.k`](evidence/ground-witness.k) and
[`evidence/14-kprove-ground-witness.log`](evidence/14-kprove-ground-witness.log).

As an independent body-sensitivity check, the reviewer changed the closure body
operator from `*` to `+`, left the product postcondition unchanged, and rebuilt
the definition successfully. The mutated proof exited `1` with a stuck residual
requiring the sum of remainders to equal their product. See
[`evidence/verification-body-mutated.k`](evidence/verification-body-mutated.k),
[`evidence/18-body-mutation-kompile.log`](evidence/18-body-mutation-kompile.log),
and
[`evidence/19-body-mutation-proof.log`](evidence/19-body-mutation-proof.log).

Stage result: pass.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/build_k_inventory.py`](evidence/build_k_inventory.py) generated the
exhaustive source-level ledger
[`evidence/k-rule-inventory.tsv`](evidence/k-rule-inventory.tsv). Every record
contains an ID, source location, kind, full statement, attributes, proof-slice
classification, decision, and rationale. Its SHA-256 is
`bea4fbd478d8318214eed54ef6573f4999557a2fd98dd1e93ad46ba44f41f361`.
The ledger contains:

- 1,175 fixed-semantics records: 695 rules, 227 syntax declarations,
  5 contexts, 1 configuration, 25 modules, 86 imports, and 136 requires;
- 11 `verification.k` records: 4 syntax declarations and 4 rules, plus its
  module/import/require;
- 4 `spec.k` records, including the sole target claim.

Across the inventory there are 150 `[function]`, 111 `[total]`, 45 priority,
22 `[no-evaluators]` opaque, 37 `[concrete]`, and 26 `[owise]` records. There
are no source `[functional]` or `[simplification]` declarations. Counts and the
complete evidence-file manifest are in
[`evidence/15-k-inventory-build.log`](evidence/15-k-inventory-build.log) and
[`evidence/20-evidence-manifest.log`](evidence/20-evidence-manifest.log).

The exact mapping from every submitted AST construct (`Module`, `FuncDef`,
`Params`, statement sequencing, `Expr`, `Str`, `Return`, `BinOp`, `Name`,
`Int`) plus the proof entry `Call` to declarations and execution rules is in
[`evidence/construct-map.tsv`](evidence/construct-map.tsv).

### Used execution slice

The used rules and generated strictness contexts preserve the real control and
state transition:

- `Module` loading and `FuncDef` binding create the same scope-0 closure seen in
  the concrete run. The proof starts from the equivalent pinned closure.
- `Call` evaluates the callee, then arguments left-to-right; it allocates fresh
  scope `1`, pushes the saved continuation/environment, and binds `a` then `b`.
  The claim's exact scope map and `scopeLoc=1` satisfy the allocation invariant.
- `Name` lookup finds `a` and `b` in the fresh callee scope. Cell-reference
  priority rules cannot overlap because this ordinary frame has no `$cells`
  entry.
- `Expr(Str(...))` evaluates the ASCII docstring then discards it. It cannot
  affect the returned integer.
- `[seqstrict(2,3)]` on `BinOp` fixes left-to-right operand evaluation.
  `Int(10)`, the two `Name` lookups, integer `%`, and integer `*` dispatch to
  disjoint sort/operator equations.
- For the only divisor used, `10`, `pyMod(I,10) =
  ((I %Int 10)+Int 10)%Int 10` is Python's nonnegative remainder. The two
  `applyBin("%",Int,Int)` calls and final `applyBin("*",Int,Int)` therefore
  produce the stated result.
- `Return` evaluates its expression, writes `retV`, discards the remaining
  function-body suffix as Python return does, and `#pop` restores environment,
  scope location, stack, and `noRet`. No heap allocation or exception occurs.

The initial/final cells, evaluation order, binding, allocation, call frame,
return control, and result were checked against the fixed rules. No used rule
has an overlapping guard with a conflicting right-hand side. No used priority
rule preempts this path with different behavior.

### Proof-local extensions

Each proof-local rule was reviewed individually:

1. `multiplyClosure` (`verification.k:8-20`) is a total constant equation. It
   packages the exact submitted parameters/body with defining environment `0`.
   Classification: definitional entry package. It does not compute or assume a
   result.
2. `#runMultiply` (`verification.k:22-24`) changes the fresh specification-only
   entry symbol into an ordinary `Call`. Its matched continuation is preserved
   by `...`; it reads/writes no other cell. Classification: entry adapter, not
   an operational bridge over a fixed program term.
3. `unitDigit(I) => pyMod(I,10)` (`verification.k:27-28`) is a total
   mathematical definition over `Int`.
4. `unitDigitProduct(A,B) => unitDigit(A) *Int unitDigit(B)`
   (`verification.k:30-32`) is a total mathematical definition over two
   integers.

All four have one equation each, so there are no proof-local equation overlaps,
coverage gaps, recursive-descent issues, opaque result symbols, priority rules,
or totalization guard conflicts. No proof-specific lemma, rewrite, or oracle
replaces `%`, `*`, name lookup, argument binding, body execution, or return.

### Fixed-semantics modules outside the slice

The remaining fixed rules were reviewed by module and individually recorded in
the ledger:

- `core`, `syntax`, `iter`, `range`, `operators`, `int`, `bool`, `str`, and
  `controls` use sort-disjoint dispatch, explicit truth/iteration guards, and
  constructor-recursive sequence helpers.
- `list`, `tuple`, `set`, `dict`, `subscript`, and `comprehension` model
  allocation, structural folds, indexing/slicing, and binding. They are not
  reached by this AST.
- `methods` and `builtins` provide guarded subset operations and folds. They
  are not called by this program.
- `functions` and `call` contain the used ordinary closure path plus annotated
  closure, method, builtin, and heap-reference paths whose guards do not
  overlap the used plain-frame call.
- `concrete.k` is imported only by `MPY-KRUN`; none of its rules exists in the
  Haskell proof definition.

The 22 explicit opaque fixed-semantics boundaries are the float-operation
family in `float.k`, `sortVS`/`sortKeyVS` in `sort.k`, and `md5hexCodes` in
`builtins.k`. They remain uninterpreted in symbolic proofs and have concrete
twins or named external contracts where supplied. None can affect a branch,
cell, return, or postcondition here because this program constructs only
integers and one discarded string literal and calls no builtin.

The LLVM non-exhaustiveness warnings noted in Stage 3 are recorded as narrower
coverage gaps for unused constructs. There is no concrete or symbolic false
conclusion witness on the intended all-integer entry domain, so they are not
labeled unsound. No rule encodes the multiplication answer, fabricates a
result, bypasses a used computation, or introduces an unconstrained
result-bearing symbol.

Stage result: pass.

## 6. Fresh non-vacuity test

The fresh mutation is
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k). It changes the
result-constraining obligation to:

```text
unitDigitProduct(A,B) +Int 1
```

This is demonstrably false at the satisfying witness `A=14, B=-15`, where the
program and original claim return `20`, not `21`.

First, the exact mutated artifact was compiled to KORE with:

```text
env PATH=/usr/bin:/bin kprove /tmp/audit-work/spec-vacuity-audit.k \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

It exited `0`, proving this is not parser/import/build rejection; see
[`evidence/16-vacuity-dry-run.log`](evidence/16-vacuity-dry-run.log).

The live mutated proof used the same command without `--dry-run`. It exited `1`
with `WarnStuckClaimState`. The residual is exactly the unmet implication:

```text
formalModuloProduct +Int 1 #Equals formalModuloProduct
```

and the residual configuration contains the executed original product. See
[`evidence/17-vacuity-proof.log`](evidence/17-vacuity-proof.log). This is
meaningful result non-vacuity, independent of the body-sensitivity mutation in
Stage 4.

Stage result: pass.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics, from the exact initial state in
`SPEC.multiply-correct`, for arbitrary K integers `A` and `B`, if the pinned
submitted function call terminates, its result in `<k>` is:

```text
((A %Int 10 +Int 10) %Int 10)
*Int
((B %Int 10 +Int 10) %Int 10)
```

and the environment, scope store/location, heap/location, stack, return state,
exception state, and exit code are restored/preserved as stated. This is a
partial-correctness result; it does not separately claim total correctness.
The straight-line function concretely terminates in all tested and symbolic
proof paths, but termination is not elevated beyond the reachability theorem's
stated partial-correctness interpretation.

### Trust and assumption ledger

- **Supplied semantics:** the exact trusted
  `/reference/reference-semantics` tree is the language-model boundary. Its
  source was rebuilt and statically inventoried. This is acceptable because the
  rendered mode expressly supplies that semantics, and candidate bytes match it
  recursively.
- **K implementation and builtins:** K v7.1.337, the Haskell reachability
  backend, LLVM concrete backend, and builtin arbitrary-precision integer,
  Boolean, map, list, string, `%Int`, `+Int`, and `*Int` operations are trusted.
  They affect execution and arithmetic. Fresh builds, concrete runs, ground
  claims, and mutation residuals provide reproducible consistency evidence.
- **Trusted translator:** `/reference/py2mpy.py` is outside the theorem. Byte
  identity of trusted regeneration with the submitted `solution.mpy` supports
  the source-to-MiniPython bridge.
- **Closure-to-file pin:** `kprove` executes an embedded closure rather than
  reading `solution.mpy` dynamically. The independent token comparison proves
  exact identity for this fixed submission, and the body mutation demonstrates
  sensitivity. This is an empirical/audit bridge, not a K-internal file-link
  theorem.
- **Natural-language/canonical bridge:** the K theorem returns the product of
  remainders modulo positive `10`. Equating this with “product of unit digits”
  and with the canonical `abs` formulation uses the ordinary mathematical fact
  that Python remainder by `10` is in `0..9`. The 45,428-case independent
  differential run supports but does not prove that universal fact.
- **Opaque fixed symbols:** the 22 float/sort/MD5 opaque symbols are trusted
  boundaries of the supplied language but have no dependent rule or claim in
  this proof. There is no proof-local opaque symbol or empirical
  result-bearing oracle.
- **Excluded inputs/behavior:** non-integer arguments, Python `bool` as an
  `int` subclass, arity errors, arbitrary Python modules, and unused
  MiniPython subset constructs are outside the formal entry domain. The prompt
  says the inputs are valid integers, so this does not narrow the intended
  contract materially.

Differential tests, concrete traces, candidate prose, and prior generated
artifacts were not used as substitutes for the successful reachability proof.
They support only translation, intent, concrete execution, and pinning bridges.

### Decision

All soundness, reconstruction, adequacy, and non-vacuity gates pass. The proof
executes a syntactically exact copy of the submitted function body through the
ordinary supplied call semantics, constrains the real return value, and depends
on no answer-smuggling or opaque proof-local rule. It is therefore legitimate.
The missing provenance records and non-K intent/file-pinning bridges are
documented evidence limitations, so the appropriate completed-audit status is
`CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
