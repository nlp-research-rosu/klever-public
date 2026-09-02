# Independent adversarial audit — 86-anti-shuffle

This audit used the required `using-kit` and `validating-proof` procedures. I
treated every candidate artifact as untrusted, copied only source inputs into
`/tmp/audit-work/reconstruction`, and did not use either candidate kompiled
definition. The rendered mode is `SUPPLIED_SEMANTICS`.

The reconstructed proof is legitimate. It executes and constrains the real
translated program, its proof-local rules are sound on their stated domains,
and a fresh false-result mutation is rejected for the expected reason. The
qualification is that symbolic K does not prove that the supplied opaque
`sortVS` primitive is an ascending permutation. That natural-language bridge is
conditional on the supplied primitive's documented contract and supported by
finite concrete evidence. This warrants `CONCERNS / LEGIT`, not failure.

## 1. Input and provenance integrity

### Infrastructure and semantics boundary

`/reference/reference-semantics` is present, as required by
`SUPPLIED_SEMANTICS`. I compared entry names, entry types, link targets, and
contents recursively with `/candidate/reference-semantics`. Both trees contain
the same regular files and directories; neither tree contains a symlink; and
`diff -ruN --no-dereference` produced no differences. Thus there is no
mode/mount contradiction and no infrastructure breach.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
counterparts:

- `prompt.py` SHA-256:
  `f8a02b3472de03cd4fa7b7d9d47abd5a5d64cb8eea267c81dc575e2a281aa972`
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The required candidate artifacts `solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, `prove.sh`, and `PROOF.md` are present as regular
files. `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and one structured JSONL trace are also regular files.
There are no missing, changed, extra, mistyped, or symlinked entries in the
candidate's required supplied-semantics tree.

The candidate additionally contains caches, bytecode, prior outputs, and
`runtime-kompiled` / `verification-kompiled`. Those are generation debris, not
source-integrity failures. They were deliberately excluded from reconstruction.

Evidence:

- [candidate source inventory](evidence/01-candidate-source-inventory.log)
- [trusted-tree, prompt, and translator comparison](evidence/01-trusted-integrity.log)
- [fresh source hashes and tool versions](evidence/01-source-hashes-and-tools.log)

### Untrusted generation claims

I read, but did not rely on, the generation record. `run-input.json` names
problem `86-anti-shuffle` and the `kit-semantics` condition. `metrics.json`
claims exit 0 without timeout. `codex-last.txt`, `codex-output.log`, and
`PROOF.md` claim `#Top`, validation, differential success, and negative-probe
success. The JSONL trace is valid JSONL with 789 records spanning 2026-07-23
02:03:09Z through 02:40:54Z. These are claims only; every material result below
was reconstructed.

Evidence:

- [untrusted generation record excerpts](evidence/01-untrusted-generation-record.log)
- [structured trace summary](evidence/01-structured-trace-summary-corrected.log)

An initial trace-summary command failed with a local reporting-script
`TypeError`, then the corrected command succeeded. The failed command and exit
1 remain visible in
[the initial trace-summary log](evidence/01-structured-trace-summary.log); it
has no bearing on the candidate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a Python string `s`, split words specifically at U+0020 space characters,
sort each word's characters in ascending character-code order, retain word
order, and retain every space in its original position. In particular, empty
input, leading/trailing spaces, and repeated spaces must be preserved. The
trusted canonical implementation expresses this as
`' '.join(''.join(sorted(list(i))) for i in s.split(' '))`.

The candidate implements the same transformation in one pass. `word` collects
non-space characters; encountering a space appends the sorted current word and
one space, then clears `word`; the return appends the sorted final word. The
space and non-space branches, as well as the final empty-word case, align with
the canonical split/join behavior.

Source evidence is in
[program and contract sources](evidence/02-program-and-contract-sources.log).

### Trusted translation

I regenerated the MPY term in scratch with:

```text
python3 /reference/py2mpy.py solution.py > reviewer-regenerated-solution.mpy
cmp -l reviewer-regenerated-solution.mpy solution.mpy
```

`cmp` produced no differences. Both files have SHA-256
`8f75a29a7f2fd90ba2fda627a4232a3488b680325aa5ebe4544b596ae8bcea0b`.
See [translator regeneration](evidence/02-translator-regeneration.log).

### Independent differential test

The reviewer-authored
[differential script](evidence/differential_check.py) independently imports
`/reference/canonical.py` and the scratch copy of `solution.py`. It also uses an
insertion-sort contract oracle that does not call either implementation.

Coverage was:

- all three documented examples;
- empty input and 18 explicit boundaries, including empty words, one/multiple
  spaces, leading/trailing spaces, both branch outcomes, NUL, tabs/newlines,
  non-ASCII text, and an emoji;
- every string of length 0 through 5 over alphabet `" !0Aa~"` (9,331 generated
  cases);
- 2,000 deterministic strings of length 0 through 20 over a broader alphabet.

After deduplication, all three computations agreed on 11,128 inputs:
`canonical_mismatches=0` and `contract_mismatches=0`. The complete inputs are
preserved in [02-differential-inputs.json](evidence/02-differential-inputs.json)
and the command, hash, examples, counts, and exit 0 are in
[02-differential-results.log](evidence/02-differential-results.log).

This finite test supports program/intent fidelity; it is not used as a
substitute for the K proof.

## 3. Clean proof reconstruction

All commands in this stage ran in `/tmp/audit-work/reconstruction` against
copied source. The installed tools report K v7.1.293. No candidate cache or
kompiled directory was used.

### Fresh builds

The concrete definition was built with:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

It exited 0. See [fresh LLVM build](evidence/03-fresh-llvm-build.log).

The proof definition was built with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

It exited 0. See [fresh Haskell build](evidence/03-fresh-haskell-build.log).
Compiler warnings concern unused variables and several non-exhaustive total
functions. The only warned function on this program's value path is
`joinCodes` for impossible/non-string list elements; its actual argument is the
supplied opaque `sortVS(charsOf(W))`, discussed as a trust boundary in stage 7.
No build warning closes or bypasses a claim.

### Positive claims

The fresh combined command:

```text
kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC
```

printed `#Top` and exited 0. This proves both claims together:
[combined proof log](evidence/03-positive-all-claims.log).

I then selected the loop claim by itself. It printed `#Top` and exited 0:
[isolated loop log](evidence/03-positive-loop-claim.log).

Finally, I staged the entry proof by retaining both claims but marking only the
already independently verified loop claim trusted:

```text
kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.anti-loop,SPEC.anti-shuffle \
  --trusted SPEC.anti-loop
```

This printed `#Top` and exited 0:
[staged entry log](evidence/03-positive-entry-staged.log). In this staging,
`--trusted` is reuse of the separately closed loop theorem, not an unproved
candidate assumption.

For completeness, two diagnostics selected only the entry label and thereby
removed its loop circularity. They made no progress and were interrupted by
the reviewer with status 130. Those expected diagnostic limitations are
recorded in
[entry-only diagnostic](evidence/03-positive-entry-claim-selected.log) and
[filtered-trust diagnostic](evidence/03-positive-entry-with-verified-loop.log);
they are not positive target-proof failures.

### Fresh concrete execution

The reviewer harness contains the exact submitted function body followed by 10
normal and spacing-boundary assertions. A source `diff` confirmed the first 10
lines are the submitted `solution.py`. CPython and trusted translation
succeeded, and fresh LLVM execution ended with `.K`, `NoExc`, and modeled
`<exit-code> 0 </exit-code>`.

Evidence:

- [concrete harness](evidence/concrete_harness.py)
- [harness preparation](evidence/03-concrete-harness-prepare.log)
- [fresh K execution](evidence/03-concrete-krun.log)

## 4. Adequacy and real-program pinning

### Claim meanings

`SPEC.anti-loop` has this plain-language precondition:

- execution is at the real `#loop(str(CS), Name("char"), antiLoopBody())`;
- environment 1 is a plain local frame containing
  `result=str(O)`, `word=str(W)`, and a disjoint remainder `M`;
- scope 0 contains the exact `anti_shuffle` closure, and scope -1 is the fixed
  builtins scope;
- the heap is `H`, its next location is `N`, control/exception/return state is
  normal, and `freshFor(CS,W,N,H)` holds;
- local bindings cannot shadow `list` or `sorted`, and the frame is not a
  closure-cell frame.

Its postcondition says the loop is consumed; `result`, `word`, and the final
`char` binding are exactly `scanOut`, `scanWord`, and `scanFrame`; the heap and
allocator are exactly `heapAfter` and `locAfter`; and the continuation, stack,
return state, exception state, and exit code are preserved.

`SPEC.anti-shuffle` begins at the fixed default module configuration, loads an
exact `FuncDef("anti_shuffle", Params("s"), antiFunctionBody())`, and calls that
binding with arbitrary modeled string `str(CS)`. Its destination directly
requires return value `str(antiShuffleCodes(CS))`, the exact surviving module
binding, exact final heap and heap location, empty stack, `noRet`, `NoExc`, and
exit code 0. There is no free result variable, implication-only result, or
tautological destination.

### Program identity and body sensitivity

The three proof macros expand to the exact translated AST:

- `antiLoopBody()` is MPY lines 6–19;
- `antiFinalExpr()` is MPY lines 21–26;
- `antiFunctionBody()` is MPY lines 3–26.

The entry `<k>` cell loads that body and then resolves and invokes its actual
module binding. Calls, lookups, argument evaluation, allocations, loop steps,
return, and frame pop remain fixed-semantics execution; no local rule rewrites
an invocation or replaces the function with an oracle.

A reviewer mutation changed only `word = ""` to `word = "x"`. Its translation
is not byte-identical to `solution.mpy`; on satisfying input `""`, both CPython
and fresh K reject the original expected result. K reaches `AssertionError`,
modeled exit code 1, and process exit 1:

- [body-sensitivity source](evidence/body_sensitivity_harness.py)
- [translation/Python result](evidence/04-body-sensitivity-prepare.log)
- [fresh K body-sensitivity result](evidence/04-body-sensitivity-krun.log)

### Satisfiable states and concrete substitution

The entry precondition is realized by `CS=.IntSeq` in the displayed initial
configuration. The loop precondition is also realizable with empty `CS`, `W`,
and `O`; `M = "s" |-> str(.IntSeq)`; `H=.Map`; `N=0`; and an empty stack.
All name-exclusion and freshness guards reduce to true.

For the nontrivial satisfying input `"ba  c"`,
`CS=[98,97,32,32,99]`. The formal recurrence reduces to
`scanOut=[97,98,32,32]`, `scanWord=[99]`, and
`antiShuffleCodes=[97,98,32,32,99]`, i.e. `"ab  c"`. Both the trusted canonical
and candidate Python functions return `"ab  c"`. Empty input and
`"Hello World!!!"` were substituted as additional witnesses with the same
three-way agreement. See
[claim substitution evidence](evidence/04-claim-substitution.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-derived inventory covers every declaration beginning with `syntax`,
`configuration`, `context`, `rule`, or `claim` in the supplied semantics,
`verification.k`, and `spec.k`. It contains 1,003 records:

- 753 rules;
- 242 syntax declaration statements;
- 5 contexts;
- 1 configuration;
- 2 reachability claims.

Of these, 928 are in the byte-verified supplied semantics, 73 are proof-local
(58 rules and 15 syntax statements), and 2 are target claims. The proof-local
attributes comprise 3 macro statements, 11 statements carrying
`function,total`, and 34 simplification rules. There are no proof-local
priority rules, opaque/no-evaluator declarations, or operational `<k>` rules.
Multisymbol syntax statements, such as the statements declaring both
`scanOut`/`scanWord` and `heapAddWord`/`heapAfter`, are preserved in full in the
inventory record.

The complete exact source blocks, attributes, hashes, origin, and disposition
are in:

- [machine-readable inventory](evidence/05-rule-inventory.json)
- [one-row-per-declaration inventory](evidence/05-rule-inventory.md)
- [proof-local summary](evidence/05-proof-local-inventory-summary-corrected.log)
- [all semantics declaration locations](evidence/05-semantics-source-summary.log)

The supplied tree is the selected fixed semantics, not a candidate extension.
Rules in unused modules are inert for this AST because their outer constructors,
receiver sorts, operation names, or builtin names do not match. I separately
traced every rule family reachable from this program:

| Submitted construct | Declaration and fixed-semantics path |
|---|---|
| `Module`, `FuncDef`, statement sequence | `syntax.k`; `core.k` `#loadAll`/sequencing; `functions.k` closure installation |
| `Name`, `Str`, local assignment | `core.k` literal/lookup; `controls.k` plain-frame assignment |
| `For` over a string | `controls.k` `For/#loop/#loopStep`; `str.k` string iterator |
| loop-target `Name("char")` | `tuple.k` plain-frame `#bindTgt` |
| `If` and string `==` | strictness from `syntax.k`; `controls.k` branch; `operators.k` comparison dispatch; `str.k` equality |
| string `BinOp("+",...)` | left-to-right strictness; `operators.k`; `str.k` `seqConcat` |
| `list(word)` | `call.k` lookup/call/argument routing; `builtins.k` `charsOf` and list allocation; `core.k` `#alloc` |
| `sorted(list(...))` | `call.k` heap dereference; `sort.k` sorted allocation and supplied `sortVS` |
| `Str("").join(...)` | `call.k` bound-method routing and argument dereference; `methods.k` `joinCodes` |
| `Return` | `functions.k` `Return`, `#pop`, frame restoration |

The relevant configuration cells are all pinned or framed appropriately.
Evaluation is left-to-right through strictness and `#evalArgs`; lookup follows
the fixed scope chain; list and sorted calls allocate at the current fresh
heap location; string iteration consumes one character; and return restores
the caller state. Priority-40 cell-variable rules are disabled by the proved
absence of `"$cells"` in the plain frame. Priority dereference rules preserve
the exact heap values they read. The sorted dispatch preempts the generic
`[owise]` builtin route without skipping argument evaluation.

### Proof-local rules

Every proof-local rule was reviewed on its full domain:

- `heapCount`/`heapOf` are constructor-complete structural definitions.
  `heapCount(HS)` is absent from `heapOf(HS)` by induction.
- The membership, lookup, and overwrite simplifications are ordinary finite-map
  equalities. Constant keys (`result`, `word`, `char`, `list`, `sorted`,
  `$cells`) are distinct where used. The two-integer-update normalization is
  guarded by freshness of both keys and their inequality.
- The three macros are exact syntax abbreviations and have no state behavior.
- `sortedWord` only names the fixed-semantics expression
  `joinCodes(.IntSeq, sortVS(charsOf(W)))`; it does not replace execution.
- `scanOut`, `scanWord`, `scanFrame`, `heapAfter`, `locAfter`, and `freshFor`
  recurse on the tail of `IntSeq`. Empty, code-32, and guarded non-32 cases are
  disjoint and exhaustive.
- `heapAddWord` describes the same two consecutive map updates performed by
  `list(word)` and `sorted(...)`. Claims use it only where `freshFor` supplies
  the allocator guards.
- The broad freshness simplifications at lines 219–243 are valid structural
  induction results: `heapOf(HS)` occupies exactly the locations below
  `heapCount(HS)`, and each encountered space appends exactly two consecutive
  fresh locations. Their overlaps with base equations have the same result.
- `antiShuffleCodes`, `antiFinalHeapMap`, and `antiFinalHeapLoc` are
  definitional summaries. They are connected to fixed execution by the proved
  loop claim and entry symbolic execution; they are not answer-smuggling
  operational rewrites.

No local equation has conflicting overlapping right-hand sides, a missing
constructor case, non-descending recursion, an unguarded allocator step, or an
abrupt control effect. No local rule encodes a substituted program, returns an
unconstrained value, or bypasses body execution.

I do not label any inventoried rule unsound, so there is no unsupported
unsoundness allegation requiring a false-conclusion witness. The narrower
evidence limitation is the supplied opaque sorting boundary described below.

### Independent concrete check of the supplied sort path

The reviewer generated expected strings with insertion sort, embedded them as
assertions around the exact submitted function, translated the harness with the
trusted translator, and ran it under the fresh LLVM semantics. All 163 unique
cases passed with process exit 0: the examples/boundaries plus every string of
length 0 through 3 over alphabet `" !Aa~"`.

Evidence:

- [generator/oracle](evidence/generate_k_differential.py)
- [complete successful inputs](evidence/05-k-differential-inputs.json)
- [preparation and hashes](evidence/05-k-differential-small-prepare.log)
- [K execution](evidence/05-k-differential-small-krun.log)

An attempted 788-case harness was killed while K parsed the much larger MPY file
(exit 137), before program execution. It is an infrastructure/resource result,
not a mismatch or candidate verdict. The attempted inputs and exact failure are
preserved in
[large inputs](evidence/05-k-differential-inputs-large-failed.json) and
[large-run failure](evidence/05-k-differential-krun.log).

## 6. Fresh non-vacuity test

I did not reuse the candidate `spec-vacuity.k`. The reviewer-authored
[mutation](evidence/reviewer-spec-vacuity.k) keeps the exact precondition, heap,
control, and module obligations but changes the returned value to
`str(iCons(33, antiShuffleCodes(CS)))`.

This is demonstrably false for the satisfying witness `CS=.IntSeq`: the
program and original claim return `str(.IntSeq)`, while the mutation requires
`"!"`.

The dry run successfully parsed and built the mutated spec, printing the
backend command and exiting 0:
[vacuity dry run](evidence/06-vacuity-dry-run.log).

The actual proof exited 1 with `WarnStuckClaimState`. Its residual shows the
expected unmet implication:

```text
iCons(33, antiShuffleCodes(CS)) #Equals antiShuffleCodes(CS)
```

The residual is at the final result state with the expected scopes, heap,
allocator, stack, return, exception, and exit-code cells. This is a meaningful
postcondition failure, not a parse error, timeout, missing import, or unrelated
crash. See [vacuity proof log](evidence/06-vacuity-proof.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY theory, for every modeled `str(CS)`, if the exact
submitted translated program terminates from the stated initial configuration,
then it:

1. preserves every code-32 delimiter in position and order;
2. replaces each intervening word by
   `joinCodes(.IntSeq, sortVS(charsOf(word)))`;
3. returns exactly `str(antiShuffleCodes(CS))`;
4. installs the exact module closure, restores caller control state, leaves no
   exception, and maintains exit code 0; and
5. leaves exactly the characterized list/sorted heap allocations and next heap
   location.

This is partial correctness. It is not a separate termination theorem.

### Trust ledger

| Boundary | Effect | Assessment and evidence |
|---|---|---|
| Supplied MPY semantics and K's MAP/INT/BOOL libraries | Defines values, evaluation, control, allocation, calls, and all claims | Required fixed trust boundary in `SUPPLIED_SEMANTICS`; candidate tree is byte-identical; fresh builds, proof, and concrete execution succeeded |
| K parser/compiler/Haskell prover/LLVM backend | Executes and checks the theory | Ordinary toolchain trust; version and all actual statuses recorded |
| Trusted `py2mpy.py` | Bridges `solution.py` to the proved MPY AST | Acceptable supplied bridge; byte regeneration and body-sensitivity evidence pin the artifact |
| `sortVS` in supplied `sort.k` | Determines every word's character order and corresponding heap value | Concerning but legitimate: intentionally opaque/no-evaluators in symbolic proof. Ascending-permutation/type-preservation meaning is assumed from the supplied primitive contract, not proved by this candidate. Supported by fresh 163-case K execution and 11,128-case Python differential evidence |
| `joinCodes` over the opaque sort | Produces returned code sequence | Conditional on `sortVS` returning the documented list of one-character strings. The proof shares the same deterministic composite term between execution and postcondition; the false-result mutation confirms it is not an unconstrained result oracle |
| Python-to-MPY character model | Relates modeled integer-code strings to Python strings | ASCII literals execute concretely in MPY. The formal claim is broader (`IntSeq` permits arbitrary integers), while reviewer Python tests include Unicode. The full Unicode K/Python bridge is not concretely exercised |
| Proof-local map and freshness lemmas | Enables symbolic lookup/allocation normalization | Acceptable derived mathematics after exhaustive domain, overlap, and descent review; no operational control rewrite |
| Trusted canonical implementation and finite tests | Supports implementation/intent and opaque-sort bridges | Reproducible finite evidence only; not a universal proof and not substituted for `kprove` |

There are no illegitimate assumptions, operational shortcuts, or empirical
tests standing in for the reachability proof. The documented concern is the
formal-to-natural-language interpretation of the supplied opaque sorting
primitive, especially beyond concretely tested ASCII MPY literals. It does not
permit a false K conclusion, does not detach the theorem from the real program,
and therefore does not make the proof illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
