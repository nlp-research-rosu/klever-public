# Independent adversarial audit: 19-sort-numbers

## Audit result

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. Clean reconstruction succeeded, the
claim is result-constraining, and the proof-local equations do not bypass the
program.

The qualification is substantive but not disqualifying: symbolic keyed sorting
is the fixed supplied opaque primitive `sortKeyVS`. The K theorem proves that
the real program returns and stores a term containing that primitive; it does
not prove within K that the primitive is a stable ascending sort or that it
invokes the submitted key closure. The natural-language sorted-order conclusion
therefore remains conditional on the supplied primitive's documented contract,
with finite concrete evidence for the bridge. This is the documented informal
intent limitation contemplated by `CONCERNS / LEGIT`.

Every command log under `evidence/` begins with the exact command and ends with
`EXIT_STATUS`. Candidate-generated logs and prose were not used as proof
authority.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no mode/mount
contradiction and therefore no infrastructure breach.

The recursive, no-dereference comparison in
`evidence/01-integrity.log` found:

- `/candidate/prompt.py` byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` byte-identical to `/reference/py2mpy.py`;
- all 24 files in the candidate `reference-semantics/` tree byte-identical to
  the trusted tree;
- no missing, additional, mistyped, changed, or symlinked semantics entry; and
- all required metadata files present as regular files.

Relevant hashes include:

- prompt:
  `61b0d963a0d3797bc5ef83253bf35a531d7e31eedbd18181ff117b0e07e5c940`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- supplied top-level `semantics.k`:
  `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`.

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
292-record structured generation trace were inspected only as claims. Their
bounded contents and reported statuses are retained in
`evidence/01b-structured-trace-summary.log` and
`evidence/01c-untrusted-metadata-claims.log`. They claim `VALIDATED`, eleven
claims, 115 LLVM assertions, and two rejected mutations; none of those claims
was accepted without reconstruction.

The candidate-supplied compiled directories and caches were not copied or
used. Only source artifacts were copied to
`/tmp/audit-work/reconstruction`, as recorded in
`evidence/02-scratch-copy-and-translation.log`.

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires `sort_numbers(numbers: str) -> str` to accept a
space-delimited sequence of the words `zero` through `nine` and return those
words ordered by numeric value. The example maps `"three one five"` to
`"one three five"`.

The trusted canonical implementation builds the exact word-to-integer map,
splits on ASCII space, removes empty fields, sorts by the map, and joins with
one ASCII space (`/reference/canonical.py:8`).

The candidate uses an ordinary helper chain whose ten intended-domain results
are 0 through 9, then evaluates:

```python
" ".join(sorted(numbers.split(), key=_number_value))
```

(`/candidate/solution.py:1` and `/candidate/solution.py:23`). This is a
different but correct algorithm on the intended space-delimited domain.
Its fallback maps any invalid word to 9, but invalid words are outside both the
natural contract and the K entry precondition.

The candidate's no-argument `split()` also accepts tab, LF, and CR delimiters,
whereas the canonical implementation does not. That is an extension outside
the literal space-delimited intended domain, not a divergence on the intended
domain. Leading, trailing, and repeated ASCII spaces agree because the
canonical implementation removes empty fields.

### Translation identity

The trusted translator was run over the scratch copy of `solution.py`.
`regenerated-solution.mpy` is byte-identical to the submitted
`solution.mpy`, with SHA-256
`bdaf0518a7e333048fb35958865d1736d0bb9d56178a363fa9363e2ca92d1edd`.
See `evidence/02-scratch-copy-and-translation.log`.

### Independent differential test

`evidence/differential_check.py` loads the trusted canonical and candidate
modules under distinct names. It tested:

- the documented example;
- empty, one-space, all-space, leading/trailing, and repeated-space cases;
- ascending and descending all-word cases;
- duplicates and alternating zero/nine;
- every single word and every ordered word pair; and
- 256 fixed-seed generated inputs of lengths 3 through 16.

There were 378 distinct intended-domain inputs and zero mismatches. The
complete inputs, both outputs, command, and exit 0 are in
`evidence/03-python-differential.log`.

Stage 2 result: PASS.

## 3. Clean proof reconstruction

The independently observed toolchain is K v7.1.293
(`evidence/00-toolchain.log`).

### Concrete definition

The supplied semantics was freshly compiled from the scratch source:

```text
kompile --backend llvm reference-semantics/semantics.k
  --main-module MPY-KRUN
  --syntax-module MPY-SYNTAX
  --output-definition runtime-kompiled-audit
```

The command exited 0; see `evidence/04-kompile-llvm.log`. No candidate-built
definition was referenced.

`evidence/make_k_concrete_tests.py` appended seven assertions to an exact
byte-prefix copy of `solution.py`. Translation with the trusted translator and
`krun` under the fresh LLVM definition exercised the example, empty/spacing
boundaries, reverse order, and duplicates. All seven assertions passed with
exit 0 (`evidence/05-krun-concrete.log`).

The LLVM compiler emitted totality warnings for some broad supplied helpers.
The only warning on a used value path is that `joinCodes` has no constructor
equation for an exotic non-string list element. Under the named keyed-sort
contract, this program's sorted list contains only the input strings. Without
that contract, the warning reinforces the documented opacity limitation; it is
not evidence of a false conclusion on an intended input.

### Proof definition and all positive claims

The proof definition was freshly compiled:

```text
kompile --backend haskell verification.k
  --main-module VERIFICATION
  --syntax-module MPY-SYNTAX
  --output-definition verification-kompiled-audit
```

This exited 0 (`evidence/06-kompile-haskell.log`).

Each claim was then selected in a separate `kprove` invocation. All eleven
commands exited 0 and each printed exactly one `#Top`:

- `number-value-zero` through `number-value-nine`; and
- `sort-numbers`.

The commands and aggregate counts are in
`evidence/07-positive-claims-summary.log`; each full output is in the
corresponding `evidence/07-kprove-*.log`.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The ten `number-value-*` claims have no symbolic precondition. Each begins in
an exact, satisfiable state containing the submitted helper closure, an empty
heap and stack, normal return/exception/exit cells, and a fixed ground word.
Each claim says that executing the real call returns its corresponding integer
while restoring the call-control state.

The `sort-numbers` entry claim has:

- precondition
  `validNumberWords(splitWS(CS, .IntSeq, .ValSeq))`;
- an initial default module configuration;
- execution of `#loadAll(solutionModule())` followed by an actual call to
  `sort_numbers(str(CS))`; and
- postcondition
  `str(joinCodes(space, sortKeyVS(splitWS(CS), numberValueClosure())))`,
  together with the exact loaded module scope, split list at heap location 0,
  sorted list at heap location 1, `heapLoc == 2`, restored environment and
  scope location, empty stack, `noRet`, `NoExc`, and exit code 0.

The precondition accepts empty input and every code sequence whose MPY
whitespace split consists solely of the ten allowed words. It also accepts
ASCII tab/LF/CR separators; this broadens but does not weaken the theorem on
the intended space-delimited domain.

### Actual-program identity

`solutionModule()` expands to the exact two `FuncDef` terms in the regenerated
translator output. `numberValueBody()` and `sortNumbersBody()` only name those
exact AST bodies. They are constructor equations, not execution summaries.
`evidence/audit-pinning-spec.k` records the exact regenerated RHS, and the
configuration-form auxiliary check closed with `#Top` in
`evidence/09b-kprove-exact-program-pinning.log`. The backend first rejected a
functional-form diagnostic because it does not support functional claims;
that reviewer-only diagnostic is transparently retained in
`evidence/09a-pinning-functional-claim-unsupported.log` and has no bearing on
the candidate claims.

The real control path is:

1. `#loadAll` executes both real `FuncDef` statements and installs their
   closures.
2. Normal name lookup selects the installed `sort_numbers` closure.
3. The call rules allocate and bind its frame.
4. The strict return expression evaluates the `join` receiver and the
   `sorted` argument left-to-right.
5. `numbers.split()` allocates heap location 0.
6. `_number_value` is looked up and passed as the key value.
7. the supplied keyed-sort rule allocates heap location 1 containing
   `sortKeyVS(...)`;
8. `join` dereferences that list and builds the returned string; and
9. the real return/pop rules restore the caller state.

There is no helper or loop claim substituting for this entry execution, and
the program contains no loop.

### Satisfying witness and ground substitution

For the main entry, take
`CS = strToCodes("three one five")`. `splitWS` yields the three accepted
tokens, so the precondition is true. Under the fixed primitive's named
stable-key-sort interpretation, substituting that `CS` into the claimed result
gives `"one three five"`. The trusted canonical, candidate Python, and fresh
concrete K execution all returned that value
(`evidence/03-python-differential.log` and
`evidence/05-krun-concrete.log`). Empty input is a second satisfying witness.
The ten helper entry configurations are themselves concrete satisfying states,
one for each allowed word.

The result is not free, existential, tautological, or merely constrained by a
one-way implication. The exact opaque result term is fixed. What remains
unproved is the human meaning of `sortKeyVS`, not which term execution
produces.

Stage 4 result: PASS, with the keyed-sort intent bridge carried to Stage 7.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/build_rule_inventory.sh` inventories every declaration start and
every attribute-bearing line in the supplied tree, `verification.k`, and
`spec.k`. The corrected complete result is
`evidence/10b-exhaustive-rule-inventory.log`. An earlier reviewer regex error
is retained separately as `evidence/10a-inventory-attribute-regex-error.log`
and was not used.

The inventory contains 26 K source files, 237 syntax declaration groups, 707
rules, one configuration, five contexts, and eleven claims. There are no
aliases, `[functional]` attributes, or `[simplification]` rules. The following
file-level decision applies to every declaration and rule enumerated for that
file in the complete line-by-line inventory:

| File | Syntax | Rules | Static decision |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Exact supplied assembly; imports MPY and concrete-only MPY-KRUN legs. |
| `assert.k` | 0 | 3 | Fixed and unreachable from the proof; ordinary truth/failure rules. |
| `bool.k` | 0 | 13 | Fixed and unreachable on this program path. |
| `builtins.k` | 38 | 137 | Fixed registry/helper layer; generic declarations are imported, but no answer-specific rule applies. Unused totality warning for `mapStrVS`. |
| `call.k` | 3 | 21 | Used; callee-first and left-to-right argument evaluation, dereference, closure entry, and state footprint agree with the submitted calls. |
| `comprehension.k` | 3 | 7 | Fixed and unreachable. |
| `concrete.k` | 5 | 16 | LLVM-only; the keyed-sort leg calls the real closure and stable-inserts by its integer key. Used only as finite test evidence, never by `kprove`. |
| `controls.k` | 3 | 34 | Used only for the helper's real `If` branches; guards are complementary and control is preserved. Other control rules are unreachable. |
| `core.k` | 37 | 46 | Used; configuration, module sequencing, lookup, allocation, literals, keyword tagging, and left-to-right argument evaluation match the claimed cells. |
| `dict.k` | 12 | 28 | Fixed and unreachable. |
| `float.k` | 34 | 121 | Fixed and unreachable; all float opaque symbols and concrete twins are irrelevant to this theorem. |
| `functions.k` | 4 | 15 | Used; exact definition binding, parameter binding, return, stack frame, scope deallocation, and caller restoration are represented in the post-state. |
| `int.k` | 1 | 16 | Ground integer results/comparisons are ordinary K integer mathematics; other rules are unreachable. |
| `iter.k` | 1 | 0 | Iterator declarations only; unreachable. |
| `list.k` | 5 | 27 | Fixed list representation is used by allocation/dereference; list operations themselves are not answer shortcuts. |
| `methods.k` | 27 | 75 | Used `splitWS`, `flushTok`, `isWSC`, `joinCodes`, and method dispatch agree with the modeled no-arg split and string join. |
| `operators.k` | 0 | 10 | Used comparison evaluation contexts and dispatch preserve left-to-right evaluation. |
| `range.k` | 2 | 6 | Fixed and unreachable. |
| `set.k` | 6 | 12 | Fixed and unreachable. |
| `sort.k` | 6 | 19 | Used fixed external boundary. The call/heap transition is faithful; `sortKeyVS`'s ordering and key-call meaning are opaque in symbolic proof. |
| `str.k` | 5 | 28 | Used string literal/code conversion, equality, and sequence operations are constructor-recursive and mathematically ordinary. |
| `subscript.k` | 15 | 40 | Fixed and unreachable; its `valSeqAt` totality warning cannot affect this program. |
| `syntax.k` | 16 | 0 | Declares exactly the AST constructors mapped below. |
| `tuple.k` | 4 | 21 | Fixed and unreachable. |
| `verification.k` | 10 | 12 | All candidate-local rules reviewed individually below; sound definitional equations only. |
| `spec.k` | 0 | 0 | Eleven reachability claims, not semantic/proof rules. |

All `[priority]`, `[concrete]`, `[owise]`, `[function]`, and `[total]`
occurrences are enumerated with source line numbers in the inventory. The 25
fixed `symbol(...)` declarations are:

```text
absF addF ceilF decStrToF divF divFloatIntV divII eqF floatLt
floatMod floorFI gtF intFloatDiv intToF md5hexCodes mulF powF
roundF roundFN sortKeyVS sortVS sqrtF subF toF truncF
```

Only `sortKeyVS` is reachable from the audited symbolic entry. None is
candidate-defined.

### Used construct map

| Submitted construct | Declaration | Governing execution |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `syntax.k:53-61` | `core.k:124-127`, `functions.k:14-16` |
| `Name`, `Int`, `Str` | `syntax.k:9-13` | `core.k:130-154,193-196`, `str.k:13-16` |
| `If`, `Compare`, `CmpOp` | `syntax.k:30-32,49` | strict/context rules plus `controls.k:51-54`, `operators.k:14-20`, `str.k:25-26` |
| `Call`, `Attribute`, `KwArg` | `syntax.k:25,28-29` | `core.k:95-102,183-191`, `call.k:15-24` |
| no-arg `split` | method/bound-method values | `call.k:56-67`, `methods.k:70-86`, `core.k:117-121` |
| keyed `sorted` | builtin and `sortKeyVS` | `core.k:156-181`, `call.k:38-46`, `sort.k:44-64` |
| string `join` | `applyMethod`, `joinCodes` | `call.k:24,63-67`, `methods.k:23-31` |
| strict `Return` and calls | `syntax.k:50` | `call.k:69-75`, `functions.k:62-90` |

The priority rules relevant to the path only select the intended specialized
split/dereference rules and, for LLVM testing, the concrete keyed-sort leg.
No candidate priority rule exists. The proof has no output cell or exception
side effect to omit; all configured observable cells are either exactly
constrained or unchanged.

### Candidate-local rule decisions

The six nullary body/closure/module/scope equations
`numberValueBody`, `sortNumbersBody`, `numberValueClosure`,
`sortNumbersClosure`, `solutionModule`, and `solutionScopes` exactly name
constructor terms or the final scope. They do not match `<k>` and cannot
preempt execution.

`isNumberWord` has one string equation and a disjoint `[owise]` fallback.
`validNumberWords` has exhaustive empty/cons equations and structurally
descends. `validNumberInput` is one unconditional equation over `IntSeq`.
These three symbols affect only the precondition.

`sortNumbersResult` is one unconditional RHS-only constructor equation. It
names the exact value reached through the fixed split, keyed-sort, and join
semantics; it does not rewrite a program term. It does not assert that the
opaque keyed-sort term has ascending-order meaning.

Thus every proof-local `[total]` symbol has either one unconditional equation
or disjoint exhaustive constructor/`[owise]` cases. There is no local opaque
symbol, operational bridge, ordinary `<k>` rule, priority rule,
simplification, overlap inconsistency, or non-descending recursion.

No rule is labeled unsound in this audit. In particular, there is no concrete
false-conclusion witness for a candidate-local rule. The opaque keyed-sort
boundary is instead recorded as an evidence/intent gap: the false ground
result mutation fails, showing that opacity does not itself prove an arbitrary
concrete answer.

Stage 5 result: PASS for soundness; intent limitation recorded.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not reused.
`evidence/audit-vacuity-spec.k` is a fresh reviewer mutation of the entry
result for the satisfying ground input `"three one five"`. It demands the
demonstrably false result `"five three one"` while retaining the original
program execution and exact final heap/control obligations.

The mutation first compiled successfully with `kprove --dry-run`, exit 0
(`evidence/12a-vacuity-dry-run.log`). The actual proof then exited 1 with
`WarnStuckClaimState` (`evidence/12b-vacuity-proof-expected-failure.log`).
The residual is the expected unmet equality between the wrong reversed code
sequence and:

```text
joinCodes(space, sortKeyVS([three, one, five], numberValueClosure()))
```

It is not a parser error, missing import, timeout, unrelated crash, or
unreachable mutation. Both Python implementations and the fresh concrete K
run produce `"one three five"` for this same satisfying input.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY definition, for every `CS` satisfying
`validNumberInput(CS)`, if the entry execution terminates, the exact submitted
module loads, the exact `sort_numbers` body executes, and the final state is:

- result
  `str(joinCodes(space, sortKeyVS(splitWS(CS), numberValueClosure())))`;
- scope 0 containing the two exact submitted closures and the unchanged
  builtin parent;
- heap location 0 containing the split tokens;
- heap location 1 containing the opaque keyed-sort result;
- `heapLoc == 2`;
- restored environment and scope location;
- empty call stack, `noRet`, `NoExc`, and exit code 0.

The ten separate claims formally execute the program-defined helper on every
allowed word and establish its complete intended-domain key graph.

### Assumptions and trust boundaries

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted translator and byte-identity regeneration | Connects `solution.py` to `solution.mpy` | Acceptable and directly checked. |
| Supplied MPY semantics and K toolchain | Defines every execution and proof step | Required fixed trust base; rebuilt from source. |
| `sortKeyVS(ValSeq, Val)` | Determines final token order and sorted heap object | Acceptable external-builtin boundary for legitimacy because it is fixed, not candidate-defined, and the formal theorem remains interpretation-parametric. It is a concern for the unconditional natural-language conclusion because no K theorem connects it to stable key sorting. |
| `joinCodes` on the opaque sort result | Determines the returned code sequence | Defined for string sequences; its broad `[total]` treatment relies on `sortKeyVS` preserving the string elements, part of the same named contract. |
| Other 24 fixed opaque symbols | None | Unreachable and irrelevant to all claims. |
| Keyed LLVM concrete leg (`#ksort`, `insPair`, `kLt`) | Supplies concrete K test behavior | Finite empirical bridge only; it is absent from the Haskell proof definition. |
| Trusted canonical plus CPython execution | Supports implementation-to-intent fidelity | 378-case finite evidence, not a theorem. |
| Termination | Whether a post-state is reached | Not proved; correctly outside partial correctness. All tested executions terminate. |

The helper claims alone do not make `sortKeyVS` use those helper results; the
connection from the opaque primitive plus the proved key graph to ascending
numeric order is informal and conditional. Conversely, the proof does not use
the same opaque term to assert a concrete sorted string: the fresh false-result
mutation is rejected. This is an honest abstraction boundary rather than a
smuggled false conclusion.

The finite Python differential test supports source fidelity, and the seven
fresh concrete K assertions support the translator/LLVM behavior on their
recorded inputs. Neither is treated as a replacement for the reachability
proof or as a universal proof of sorting.

Stage 7 result: the proof is sound and pins the real generated program, but the
natural-language ordering conclusion is conditional on an unproved fixed
primitive contract. That limitation warrants `CONCERNS`, not `FAIL`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
