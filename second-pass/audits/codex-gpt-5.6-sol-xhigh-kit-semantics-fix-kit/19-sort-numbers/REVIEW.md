# Independent adversarial audit: 19-sort-numbers

The candidate contains a legitimate, non-vacuous partial-correctness theorem
about the actual submitted function under the supplied K semantics. The theorem
does **not**, however, derive the central human-facing fact that the result is a
stable ascending numeric sort: keyed sorting is the supplied semantics'
uninterpreted `sortKeyVS` primitive. Concrete K and differential tests support
that bridge only finitely. The appropriate result is therefore
`CONCERNS / LEGIT`, not an unconditional pass.

All execution was reconstructed below `/tmp/audit-work`. Candidate build
directories and caches were not reused. Reproducible scripts, generated audit
specs, and bounded command logs are in `/audit-output/evidence/`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it: `/reference/reference-semantics` exists. This is not an infrastructure
breach.

- `/candidate/run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the structured JSONL trace were present and read only
  as untrusted generation claims. They claim `#Top`, two rejected mutations,
  and differential success. The excerpts, claim index, and structured trace
  index are preserved in `04-provenance-excerpts.log`,
  `05-provenance-claims.log`, and `06-trace-summary.log`. The unavailable `jq`
  attempt in log 05 was replaced by the reviewer-authored
  `summarize_trace.py`; no candidate trace parser was used.
- Every candidate entry under `reference-semantics/` is a regular file or
  directory; there are no symlinks or mistyped special entries. Recursive
  `diff -qr --no-dereference` against the trusted tree exited 0. There were no
  missing, changed, or additional semantics entries.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  versions. The paired SHA-256 values are recorded in `02-integrity.log`.
- Required candidate sources `solution.py`, `solution.mpy`, `verification.k`,
  `spec.k`, `prove.sh`, and `PROOF.md` are present as regular files. Candidate
  compiled definitions, bytecode caches, tests, logs, and mutation specs are
  additional top-level evidence, not trusted build inputs.

Evidence: `01-trees.log`, `02-integrity.log`, `03-provenance-index.log`,
`04-provenance-excerpts.log`, `05-provenance-claims.log`,
`06-trace-summary.log`, and `07-scratch-copy.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract accepts a space-delimited string whose nonempty tokens are
the English numeral names `zero` through `nine`, and requires the tokens in
ascending numeric order, joined by single spaces. Duplicates are preserved. The
documented example maps `"three one five"` to `"one three five"`. The trusted
canonical implementation filters empty space-separated fields and stable-sorts
with a word-to-integer map.

The candidate uses the exact ordered tuple of ten words and
`sorted(numbers.split(), key=order.index)`. On the intended domain this is
equivalent to the canonical algorithm. It additionally accepts tabs, line
feeds, carriage returns, and mixed whitespace; that is a benign behavior outside
the prompt's space-delimited domain, not a restriction of the required domain.

The trusted command

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy
```

exited 0, and `cmp` against submitted `solution.mpy` exited 0. Both files have
SHA-256 `3b4cb68e1c5910d00262cebe2c74b11ba3f5087d866349a0bad32f43f2222b35`.

The independent `differential_audit.py` loads the trusted canonical and
candidate entry points directly. It covers the documented example, empty and
all-space strings, leading/trailing and repeated spaces, all ten singleton
tokens, all nine adjacent ordering boundaries, ascending/descending lists,
duplicates, every word sequence of lengths 0 through 4 (11,111 cases), and
2,000 seeded generated cases of lengths through 40. Result: 13,138 comparisons,
zero mismatches, exit 0. The explicit named inputs and generator are preserved.

Evidence: `08-source-review.log`, `09-program-fidelity.log`,
`09b-differential-inputs.log`, and `differential_audit.py`.

## 3. Clean proof reconstruction

The audit used K v7.1.293 from `/usr/bin`. Only source artifacts were copied to
`/tmp/audit-work/candidate-src`; trusted supplied semantics were copied from
`/reference`, not from a candidate build product.

Fresh LLVM construction:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit: 0. The warnings identify known non-exhaustive total helpers in the
supplied partial semantics; none is a build failure. The `joinCodes` warning is
relevant to the opaque-sort limitation discussed below.

Fresh Haskell construction:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Exit: 0. Source inspection found one positive target claim,
`SPEC.sort-numbers`. The independent proof command was:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0. Candidate `verification-kompiled` was never
used.

Although concrete execution is not an extra mode requirement for supplied
semantics, the audit also translated a test module whose first 14 lines compare
byte-for-byte with `solution.py`. Four assertions covered the documented
example, empty input, all words descending, and duplicates. Fresh LLVM `krun`
ended with `.K`, `NoExc`, exit-code cell 0, and process exit 0.

Evidence: `00-toolchain.log`, `10-llvm-build.log`, `11-haskell-build.log`,
`12-positive-proof.log`, `14-k-concrete-witness.log`,
`k_concrete_witness.py`, and `k_concrete_witness.mpy`.

## 4. Adequacy and real-program pinning

### Entry precondition

In plain language, the claim splits the input code sequence on space, tab, LF,
or CR, drops empty fields, and requires every resulting token to be exactly one
of `zero` through `nine`. Empty input is admitted. This includes every prompt
input and excludes the tuple-index exception path.

The precondition is satisfiable. For `"three one five"`, a fresh ground K claim
reducing
`validNumeralTokens(splitWS(strToCodes("three one five"), ...))` to `true`
printed `#Top` and exited 0. The first functional-claim form was unsupported by
this backend and is retained in `15a-precondition-functional-attempt.log`; the
configuration-form witness in `15-precondition-witness.log` is the successful
check.

### Entry postcondition

In plain language, normal return must be the string obtained by joining with
ASCII space the value

```text
sortKeyVS(splitWS(CS), boundMethodV(numberOrder, "index"))
```

The claim also fixes both heap allocations, advances `heapLoc` from 0 to 2,
restores the module environment and scope counter, empties the call stack,
restores `noRet`, leaves `NoExc`, and leaves exit code 0. The returned value is a
specific input-dependent term, not a free or existential result, tautology, or
one-way implication.

### Real-program connection

`solution.mpy` contains one `FuncDef`. The claim starts at the public function
entry rather than re-running module load, but it installs the exact translated
closure that normal `FuncDef` execution creates: the same name, parameter list,
defining environment, assignment, ten tuple literals in the same order, and
return expression. It then executes that body through the ordinary call,
lookup, argument, assignment, allocation, return, and pop rules. There are no
helper or loop claims and no substituted callback. This is an adequate
function-entry harness for the actual submitted program.

For the satisfying substitution `CS = strToCodes("three one five")`, both
trusted canonical and candidate Python return `"one three five"`, and fresh
concrete K accepts the same assertion. However, a fresh Haskell ground claim
that asks the *formal postcondition term itself* to equal those expected codes
is stuck with exit 1: `sortKeyVS` remains uninterpreted. That probe is not a
candidate failure; it precisely identifies the formal intent bridge that the
positive theorem does not contain.

Evidence: `08-source-review.log`, `15-precondition-witness.log`,
`precondition-witness.k`, `16-intent-bridge-probe.log`,
`intent-bridge-probe.k`, and `used-path-map.md`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`rule-inventory.tsv` enumerates every declaration from the trusted assembled
semantics, all 23 helper K files, and candidate `verification.k`, with file,
line, flattened declaration, attributes, and audit disposition. Its 936 records
are:

- 230 syntax declaration records: 227 supplied and 3 proof-local;
- 700 rules: 695 supplied and 5 proof-local;
- 5 evaluation contexts; and
- 1 configuration.

Attribute inventory includes 149 syntax records carrying `function`, 110
carrying `total`, 22 carrying `no-evaluators`, 32 concrete-rule records, 29
priority-rule records, and 27 `owise` records. There are no `functional` or
`simplification` declarations/rules. Multiple function alternatives on one
syntax line remain explicitly visible in the inventory record, so these are
record counts rather than a claim about the number of function symbols.

The full priority and opaque-symbol extracts are in
`18-special-inventory.log` and `21-symbol-inventory.log`. Rules outside the
submitted program's syntactic and dynamic cone are classified narrowly as
supplied partial-semantics rules with no candidate effect; that classification
does not claim full CPython coverage for unused constructs. No such unused rule
can overlap the actual method names, value constructors, or control terms on
this proof path. No concrete or symbolic false-conclusion witness on the
intended program domain was found for them, so none is mislabeled unsound.

### Proof-local functions and rules

- `numberOrder` has one unconditional ground equation. Its RHS is exactly the
  tuple constructed by the submitted body. It names a value and does not
  intercept execution.
- `isNumeralCodes` has one unconditional Boolean equation over every `IntSeq`.
  It is exactly membership in the ten literal code sequences, with no overlap.
- `validNumeralTokens` has disjoint empty, string-head recursive, and non-string
  `owise` cases. The recursive case strictly descends through `ValSeq`; together
  the cases cover the declared domain.

All three `total` annotations have truthful coverage for their declared sorts.
There are no local priorities, opaque symbols, operational bridges,
simplifications, or axioms. All five local equations are sound.

### Used operational rules and state

The exact construct-to-rule map is in `used-path-map.md`. In summary:

1. The pinned closure is selected by ordinary scope lookup; the callee is
   evaluated before left-to-right argument evaluation.
2. A fresh call scope and frame are allocated, and `numbers` is bound normally.
3. Strict assignment evaluates every tuple string left-to-right and stores the
   tuple in the callee scope.
4. `split()` reads the bound argument, uses the supplied whitespace tokenizer,
   and allocates heap object 0.
5. The key keyword evaluates to the bound, pure tuple `index` method.
6. The supplied symbolic sorted rule allocates heap object 1 around
   `sortKeyVS`.
7. The non-mutating `join` path dereferences that object, constructs the formal
   output, and the ordinary return/pop rules restore all framed cells.

The priorities used here only select heap dereference, `split`, and keyed-sort
dispatch over their generic fallbacks. Their guards and constructor/method
patterns are disjoint on the actual state. The program has no mutation,
exception, output, callback side effect, or loop to omit. Tuple `index` is pure,
and the precondition guarantees every key lookup exists.

### Supplied opaque sort boundary

`sortKeyVS(ValSeq, Val)` is declared `[function, total, symbol,
no-evaluators]`. The ordinary supplied rule at `semantics/sort.k:61-62`
replaces the property-bearing keyed sort with this term and preserves the list
allocation. It does not prove that the output is a permutation, that every
element is a string, that keys were called, that order is stable, or that the
order is ascending. For this candidate, skipped key calls have no state/control
effect because the pinned key is pure tuple `index` and all tokens are valid;
the remaining mathematical result is still an explicit trust assumption.

This is not a false rewrite equation and does not let K prove an arbitrary
concrete output: the ground intent probe remains stuck. It is therefore an
acceptable supplied low-level trust boundary for a *conditional structural
theorem*, but it prevents an unconditional proof of the natural-language
sorting result. The LLVM-only `MPY-CONCRETE` module supplies real key calls and
stable insertion for tests; it is deliberately absent from the Haskell proof.

The LLVM warning that `joinCodes` is not exhaustively defined for arbitrary
non-string `ValSeq` heads reinforces the same limitation. On real intended
executions, concrete sorting preserves the input strings. In the symbolic
theorem, that preservation is not derivable from opaque `sortKeyVS`; the nested
total term remains formal. This is an evidence/adequacy gap, not a witnessed
false local equation.

Evidence: `13-inventory-counts.log`, `17-inventory-run.log`,
`rule-inventory.tsv`, `inventory-summary.txt`, `18-special-inventory.log`,
`21-symbol-inventory.log`, `inventory_k.py`, and `used-path-map.md`.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was inspected only as untrusted evidence. The
audit created the distinct `spec-fresh-mutation.k`, changing only the required
join separator on the RHS from code 32 (space) to code 45 (hyphen), while
leaving the executable closure, precondition, heap, and other state obligations
unchanged.

`"three one five"` satisfies the precondition. Both Python implementations
return `"one three five"`; the mutated obligation is `"one-three-five"`, so it
is demonstrably false. The corrected reviewer witness exits 0 after confirming
`obligation_holds=False`. An earlier disposable one-line Python rendering had a
syntax error and is visible in `19-fresh-mutation-build.log`; it did not affect
the K check and was replaced by preserved `mutation_witness.py`.

The K mutation itself built successfully:

```text
kprove --dry-run spec-fresh-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FRESH-MUTATION
```

Exit: 0. The actual proof then produced `WarnStuckClaimState` and exit 1. Its
residual explicitly compares the real `joinCodes(iCons(32,...), ...)` with the
mutated `joinCodes(iCons(45,...), ...)`. This is the expected reachable unmet
result obligation, not a parse error, timeout, missing import, or unrelated
crash. Non-vacuity passes.

Evidence: `19-fresh-mutation-build.log`,
`19b-fresh-mutation-witness.log`, `20-fresh-mutation-proof.log`,
`mutation_witness.py`, and `spec-fresh-mutation.k`.

## 7. Proven versus assumed accounting

### What is machine-proved

Subject to `validNumeralTokens(splitWS(CS))`, execution of the exact submitted
`sort_numbers` closure under the supplied symbolic MPY semantics reaches normal
return with the two specified allocations and the result

```text
str(joinCodes(
  iCons(32, .IntSeq),
  sortKeyVS(
    splitWS(CS, .IntSeq, .ValSeq),
    boundMethodV(numberOrder, "index"))))
```

with restored scope/call state, `NoExc`, and exit code 0. This is a
partial-correctness reachability result. It is result-constraining and
body-sensitive, but it is not a K theorem that the opaque sequence is a stable
ascending permutation.

### Trust ledger

| Boundary | Dependency and effect | Assessment |
|---|---|---|
| Supplied `sortKeyVS` | Directly determines the result and heap object 1; skips key calls and ordering computation in the proof definition. | Material concern. Acceptable only because it is supplied, explicit, pure on this pinned key/domain, and the formal conclusion remains conditional rather than asserting a concrete sort theorem. |
| `joinCodes` over the opaque result | The theorem needs a total formal string term; element-string preservation comes only from the intended sort contract. | Same concern, not an independent proof. Concrete intended executions are covered by finite evidence. |
| LLVM-only keyed-sort rules in `MPY-CONCRETE` | Bridge the symbolic primitive to real key calls and stable insertion for concrete tests. | Empirical support only; absent from `kprove` and not a universal theorem. |
| Other supplied symbolic primitives | `sortVS`; float symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`; and `md5hexCodes`. | Imported but not reached and not a dependency of this claim. Exact declarations are in `21-symbol-inventory.log`. |
| Remaining supplied MPY rules and K builtins | Define syntax, ASCII strings, maps/lists, lookup, calls, allocation, and control. | Task-selected semantics/toolchain trust. Used-path rules were inspected; unsupported unused CPython behavior is excluded. |
| Trusted `py2mpy.py` | Connects Python source to submitted MPY AST. | Acceptable fixed translator assumption; byte identity was independently reproduced. |
| K compiler, Haskell prover, LLVM backend | Compile and execute the definitions. | Standard toolchain trust; K version and all fresh commands are recorded. |
| Trusted canonical, CPython, and differential generators | Support source-intent equivalence and the concrete sort bridge over finite cases. | Evidence only. They do not replace the reachability proof or establish universal equivalence. |

The empirical bridge consists of 13,138 independent canonical-versus-candidate
comparisons and four fresh concrete K assertions, all successful. The natural
language argument is that tuple positions 0 through 9 are the numeric ranks and
that the supplied keyed-sort primitive performs stable ascending sorting by
those ranks. The first part is visible in the executed body; the second remains
assumed and finitely tested.

### Verdict rationale

Clean reconstruction, real-body pinning, a satisfiable precondition, a
constrained result, and fresh non-vacuity all pass. No unsound candidate-local
rule or used-path false equation was found. The candidate is therefore
legitimate. An unconditional `PASS` would overstate the result because the
central ordering/permutation property is not derived in K and the ground intent
probe demonstrates that limitation. The candidate-authored `VALIDATED`
headline is consequently stronger than this independent audit supports.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
