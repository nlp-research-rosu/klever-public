# Independent adversarial review: 149-sorted-list-sum

This review treats every file under `/candidate` as an untrusted claim. I used
only fresh definitions built under `/tmp/audit-work/audit149`; no candidate
`*-kompiled` directory, cache, `kprove.out`, or `krun` output contributed to the
decision. Reviewer-authored scripts, mutations, and bounded logs are under
`/audit-output/evidence`.

The candidate's K claims reconstruct successfully and are non-vacuous, and the
submitted program is pinned accurately. The decisive defect is instead in the
generated Python-string semantics: the formal domain is every K `Words` value,
but the model relies on K's incompletely supported Unicode `String` hooks with
no character-set restriction. Fresh concrete executions give wrong filtering
and ordering results for valid Python strings outside Latin-1. Because string
length is the central result-bearing operation, this is a material semantic
gap on the stated input domain.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode and trusted mounts agree:

- `/reference/reference-semantics` does not exist.
- The trusted inputs `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py` are regular files.
- I did not search for or use any hidden reference semantics.

This is therefore a candidate audit, not an infrastructure-breach case.

### Candidate artifacts

The required candidate deliverables are present as regular, non-symlink files:
`solution.py`, `solution.mpy`, `semantic.k`, `solution-program.k`,
`verification.k`, `spec.k`, and `prove.sh`. The required provenance artifacts
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
structured JSONL trace are also present. A recursive symlink check found no
symlinks anywhere under `/candidate`. No required artifact is missing,
mistyped, or symlinked. Candidate compiled definitions and caches are additional
generated build products; they were deliberately ignored, not treated as
source.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
SHA-256 values are respectively
`387c54540db444ab39a66ed7c465db9a9145f9437273960b116cd1c7c974727a`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The untrusted metadata says the generation completed without timeout and
claims that all proofs closed, two concrete ASCII examples passed, and 1,000
lowercase-ASCII Python tests passed. The generation trace confirms those
commands were attempted. I used none of those results as proof evidence.

Evidence:

- `evidence/stage1_2_commands.sh` and `evidence/stage1_2.log` contain the
  regular-file, symlink, mount, hash, and byte-comparison checks; exit 0.
- `evidence/untrusted_claims_commands.sh`,
  `evidence/summarize_trace.py`, and `evidence/untrusted_claims.log` contain a
  bounded readout of all untrusted provenance claims; exit 0.
- `evidence/toolchain.log` records K v7.1.293 and Python 3.10.12.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for `sorted_list_sum(lst)` on a list of strings. It
must remove strings of odd Python length, retain duplicates, and return the
remaining strings ordered first by increasing length and then alphabetically.
The final sentence claiming all words have the same length conflicts with the
preceding length-order requirement and with both mixed-length examples. The
trusted canonical implementation resolves that ambiguity by implementing the
general length-then-lexicographic behavior.

The candidate implementation is:

```python
sorted(
    [word for word in lst if len(word) % 2 == 0],
    key=lambda word: (len(word), word),
)
```

This is result-equivalent to the canonical implementation over Python lists of
strings. Unlike the canonical implementation, it does not sort the argument
list in place. The prompt specifies the returned list, not an observable
argument-mutation postcondition, so I do not treat that incidental side-effect
difference as an implementation error.

### Translation identity and proof constant

Running the trusted translator on the copied `solution.py` produced
`regenerated-solution.mpy`, byte-identical to the submitted `solution.mpy`
(both SHA-256
`7448e9074619e7708048bd97cac0340352cbc72f51aaf7f0b830421eb63ea554`).
Regenerating `solution-program.k` from that fresh translation also produced a
byte-identical file (SHA-256
`abcfab010fe834bd7007bddea6f7b9c20856f4a24d328ec9c0e7be9f017e1fed`).
The generator's only semantic-neutral adjustments spell empty K list units as
`.Exprs`, `.Strings`, and `.Stmts`.

### Independent differential test

`evidence/differential_test.py` imports copied trusted canonical and generated
entry points independently and also uses an independently written
filter-and-tuple-sort oracle. It covers:

- both prompt examples;
- empty input and the empty string;
- word lengths 0 through 4;
- both parity outcomes;
- lexical forward/reverse branches;
- equal keys and duplicates;
- mixed lengths;
- Unicode examples;
- every list of length 0 through 4 over an eight-word vocabulary; and
- 500 deterministic generated lists (seed 1492026).

All 5,197 return values agreed with both the canonical implementation and the
oracle. Ordered-case-set SHA-256 is
`a4efcba5e803d80c79151d928763ab460f26466b1f3483e8e5163ff227db421b`.
The canonical argument mutated in 4,589 cases; the generated argument never
did. The command, scope, hashes, outputs, and exit 0 are in
`evidence/stage1_2.log`. This is finite Python-to-Python evidence only; it does
not validate the K language model.

## 3. Clean proof reconstruction

### Fresh builds

The scratch tree initially contained no `semantic-kompiled` or
`verification-kompiled` directory. From copied source I ran:

```text
kompile semantic.k --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX --backend llvm \
  --output-definition semantic-kompiled -w none

kompile verification.k --main-module SORTED-LIST-VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition verification-kompiled -w none
```

Both exited 0. Exact commands and statuses are in
`evidence/stage3_commands.sh` and `evidence/stage3.log`.

### Positive proof targets

I ran each target separately with `--claims`, rather than accepting the
candidate's aggregate `#Top`:

| Claim | Exit | Output |
|---|---:|---|
| `universal-correctness` | 0 | `#Top` |
| `base` | 0 | `#Top` |
| `symbolic-two` | 0 | `#Top` |
| `symbolic-two-reverse` | 0 | `#Top` |
| `symbolic-three` | 0 | `#Top` |
| `prompt-example-one` | 0 | `#Top` |
| `prompt-example-two` | 0 | `#Top` |

The bounded output for every invocation is in `evidence/stage3.log`.

### Concrete generated-semantics reconstruction

Fresh LLVM `krun` executions matched independent Python results on the empty
list, both parity branches, duplicates, reverse lexical order, empty strings,
and mixed ASCII lengths. They did not match the intended Python result for
valid non-Latin-1 strings:

- Input `["😀"]`: Python returns `[]`; K retains the emoji.
- Input `["e\u0301"]`: Python retains the two-code-point word; K removes it.
- Input `["😀😀", "aaaa"]`: both words have even Python length and Python
  orders the emoji word first (length 2 before length 4); K orders `"aaaa"`
  first because its hooked length for the parsed emoji representation is 8.

The focused `krun` outputs and Python expectations are in
`evidence/unicode_witness.log`. Directly executing the modeled `len("😀")`
through the runtime grammar produces `VInt(4)`, while CPython prints `1`;
see `evidence/primitive_string_witness.run` and
`evidence/primitive_string_witness.log`.

There is an important front-end distinction, but it does not cure the submitted
domain claim. A Unicode literal compiled inside a K spec is filtered correctly,
while the same raw literal parsed through the candidate's concrete `.run`
route is converted to the four-byte K string and retained. Both results are
recorded in `evidence/unicode_bridge.log`. The installed K distribution itself
documents that its Unicode `String` implementation is incomplete beyond the
first 256 code points; the exact local documentation excerpt is preserved in
`evidence/k_string_boundary.log`. Thus this is a documented representation and
primitive boundary selected by the generated semantics, not a failed build,
timeout, or unexplained audit-container event.

`evidence/stage3.log` has overall exit 1 only because the independent Unicode
expectation failed. Both builds and all seven proof invocations succeeded.

## 4. Adequacy and real-program pinning

### Claim meanings and satisfiable preconditions

- `universal-correctness` has no explicit precondition beyond
  `INPUT:Words`. It says every finite K list of strings reaches
  `VList(sortedListSumSpec(INPUT))`. The empty list is a satisfying witness.
- `base` has no precondition and fixes empty input/output.
- `symbolic-two` requires two K strings of length 2 with `A <String B`;
  `A="aa", B="bb"` satisfies it and yields `["aa","bb"]`.
- `symbolic-two-reverse` requires two K strings of length 2 with
  `notBool(A <String B)`; `A="bb", B="aa"` satisfies it and yields
  `["aa","bb"]`.
- `symbolic-three` requires lengths 4, 2, and 3; `["zzzz","aa","odd"]`
  satisfies it and yields `["aa","zzzz"]`.
- The final two claims have the fixed prompt-example inputs and outputs.

Both Python implementations and the independent oracle agree on every listed
ASCII witness. Exact JSON records are in `evidence/claim_witnesses.py` and
`evidence/stage4.log`.

The universal precondition also admits the intended Python input `["😀"]`; no
claim restricts strings to Basic Latin or Latin-1. That satisfying input is the
material adequacy counterexample described in Stage 3.

### Program identity and result constraint

Every entry claim starts with `Run(solutionProgram, Call(...))`.
`solutionProgram` rewrites to the exact freshly translated submitted AST, as
shown by the byte-identical regeneration in Stage 2. The execution follows the
real function definition, parameter binding, `Return`, comprehension shape,
and `sorted` call shape. There are no loop/helper claims and no substituted
program.

The destination result is not a free variable and is not stated through a
one-way implication: each claim requires a specific `Result(VList(...))`.
Stage 6 confirms this constraint is proof-relevant.

There is nevertheless a specification-independence limitation. The universal
postcondition's `sortedListSumSpec(WS)` is defined by the single equation
`sortByKey(filterEven(WS))`, using the same two functions introduced by the
semantic rules that directly summarize the exact comprehension and `sorted`
expression. Thus the universal K theorem is primarily an execution
characterization under the generated semantics, not a separate universal
theorem that the result is sorted and contains exactly the even-Python-length
words. `evenSorted` is a separately written insertion specification, but it is
connected only by bounded symbolic/example claims, not by a universal
equivalence claim. This alone would require careful trust accounting; combined
with the concrete Unicode counterexample, it cannot establish the full prompt
contract.

## 5. Rule-by-rule static soundness review

The complete numbered sources are preserved in
`evidence/numbered_k_sources.txt`; the extracted declaration/rule inventory is
in `evidence/static_inventory.log`. Local totals are:

| File | Syntax declaration lines | Rules | Claims | Configuration |
|---|---:|---:|---:|---:|
| `semantic.k` | 31 | 58 | 0 | 1 |
| `solution-program.k` | 1 | 1 | 0 | 0 |
| `verification.k` | 2 | 10 | 0 | 0 |
| `spec.k` | 0 | 0 | 7 | 0 |

There are 31 local `[function]` declarations and 35 constructor `[symbol]`
productions. There are no local `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, priority, or `[owise]` declarations/rules, and no opaque local
symbol. All local functions have visible equations.

### Syntax, configuration, and construct coverage

`MPY-SYNTAX` declares:

- `Program`: `Module`;
- statement forms: `FuncDef`, `Return`, `If`;
- parameter/string, statement, expression, comparison, comprehension, cell
  variable, free variable, word, and value lists;
- expression forms: `Name`, `Int`, `Str`, `ListExpr`, `BinOp`, `BoolOp`,
  `Compare`, `Call`, `Subscript`, `ValueExpr`, `ListComp`, `Lambda`,
  `TupleExpr`, and `KwArg`;
- `CmpOp`, `Slice`/`NoBound`, `CompFor`, `CellVars`, `FreeVars`;
- values `VInt`, `VStr`, `VBool`, `VList`, `VNone`; and
- `Run` and `Result`.

The submitted `solution.mpy` uses `Module`, `FuncDef`, `Params`, `Return`,
`Call`, `Name`, `ListComp`, `CompFor`, `Compare`, `BinOp`, `Int`, `KwArg`,
`Lambda`, `CellVars`, `FreeVars`, and `TupleExpr`. The entry harness additionally
uses `Run`, `ValueExpr`, `VList`, and `Result`; fixed examples use `ListExpr`
and `Str`. Every used constructor is declared. `If`, `BoolOp`, `Subscript`,
`Slice`, and several value forms are unused; missing coverage for other Python
constructs is not a defect in generated-semantics mode.

The sole configuration is `<k> $PGM:Run </k>`. Environments, program text, and
execution results are passed as pure function arguments; the generated program
uses no mutation, heap, I/O, exceptions, or allocation, so no omitted state
cell affects its intended path.

### All 58 `semantic.k` rules

| Lines | Rules inventoried | Assessment |
|---|---|---|
| 94 | `Run` to `Result(evalExpr(...))` | Correct top-level sequencing; preserves the sole cell. |
| 96 | `programStmts` | Correct `Module` projection. |
| 98, 100-102 | two `findFunction` equations | Correct ordered search; equality and guarded inequality cases are disjoint. Missing functions visibly remain stuck. |
| 104-106 | two `bindParams` equations | Correct for equal-arity parameter/value lists; the submitted one-argument call is covered. |
| 108-111 | `ValueExpr`, integer, string, and name evaluation | Correct constructor/lookup behavior on covered, bound terms. |
| 113-116 | three `evalExprs` equations | Empty/singleton/cons behavior is complete for used argument lists. Any singleton overlap with a unit tail has the same normal form. |
| 118-123, 126 | list expression, three `makeList`, and `prependWord` | Correct for the modeled lists of strings; non-string list expressions visibly remain unsupported. |
| 128, 130-131 | `BinOp` dispatch, integer `%`, list `+` | Correct on covered values. Division by zero is not used (the real divisor is 2) and remains a hooked partial operation rather than a fabricated value. |
| 133, 135-137 | comparison dispatch and integer/string `==`/`<` | Internally faithful to the imported K hooks on covered values. The Python Unicode bridge for the imported string hook is subject to the documented limitation below. |
| 139, 141-142 | boolean dispatch and two-argument `and` | Correct for the pure covered form; unused by the exact program path after the comprehension summary matches. |
| 144-145 and 180-182 | `len`, string/list `valueLength` | List length is structurally correct. The string equation is **not a sound Python bridge over the claimed unrestricted domain**. Witness: the candidate runtime representation of raw `😀` makes this rule conclude 4 while CPython concludes 1 (`evidence/primitive_string_witness.log`). |
| 150-159 | exact list-comprehension denotation | The match is narrow and binder-consistent, and the recursive result is transparent rather than opaque. It bypasses generic predicate/iteration execution but is a permissible minimal denotation only where `filterEven` models Python length. It is materially unsound over the unrestricted domain through that dependency. Witness: raw input `["😀"]` is retained by K and removed by Python (`evidence/unicode_witness.log`). |
| 161-168 | exact `sorted(..., key=lambda...)` denotation | The match pins the exact lambda and has no arbitrary continuation/control effect. Its value is transparent through insertion-sort equations, but its key uses the unsupported string-length bridge. Witness: for `["😀😀","aaaa"]`, K returns `["aaaa","😀😀"]` while Python returns `["😀😀","aaaa"]`. |
| 170-178 | guarded user call, `callFunction`, `returnedValue` | Built-in names are disjoint from the user-call rule; function search, pure argument evaluation, body execution, and return extraction match the submitted one-function program. |
| 184 | `valueWords` | Correct projection on `VList`. |
| 186-192 | `filterEven` and two decision equations | Structurally terminating and Boolean guards are exhaustive/disjoint. As Python semantics, the `lengthString` decision is false on valid non-Latin-1 inputs; the `["😀"]` and `["e\u0301"]` witnesses give opposite wrong parity outcomes. |
| 194-206 | `sortByKey`, insertion, `semanticKeyLess`, decisions | The insertion recursion terminates and the true/false guards are disjoint. It correctly sorts by the K key, retaining indistinguishable duplicates. As Python tuple-key semantics it inherits the unsupported K length; the `["😀😀","aaaa"]` result is a concrete false ordering conclusion on the intended domain. I found no separate evidence that `<String` itself reverses valid Python lexical order, so I make no broader unsoundness claim about that hook. |
| 208-212 | subscript dispatch, index 0, tail slice | Correct for the two explicitly modeled shapes; unused by the submitted program. Other indexes/slices stop visibly. |
| 214-227 | empty/return/if statement execution, two branch equations, two continuation equations | Return correctly discards following statements; Boolean branches are exhaustive/disjoint; normal continuation and abrupt return are preserved. These rules are unused except `Return` on the real path, and no observable state is omitted there. |

Evaluation is equational rather than strict-cell based. On the real path all
arguments and summaries are pure, so the lack of an explicit evaluation stack
does not change state or exception behavior within the stated list-of-strings
domain. Exceptions and side effects outside that domain are visibly unmodeled,
not silently assigned results.

### `solution-program.k`

The one local `solutionProgram [function]` rule expands to the exact submitted
AST. It is not opaque and was regenerated byte-for-byte from the trusted
translation. It reads/writes no cells and fabricates no result.

### All 10 `verification.k` rules

| Lines | Rules inventoried | Assessment |
|---|---|---|
| 19-21 | `keyLess` | Same transparent tuple-key equation as `semanticKeyLess`; it inherits the unsupported Python Unicode-length bridge. |
| 23 | `sortedListSumSpec` | Truthful definitional alias to `sortByKey(filterEven(...))`, but not an independent connection theorem or independent universal postcondition. |
| 25-34 | `evenSorted`, two `keepAfterDecision` equations | Structurally terminating and guard-complete; intended insertion/filter specification on supported strings. It also uses `lengthString`, so it inherits the same unrestricted-Unicode defect. |
| 36-42 | `insertByKey` and two `insertAfterDecision` equations | Correct structurally recursive insertion by `keyLess`; guards are disjoint/exhaustive. |

There are no operational cell bridges, proof-local opaque values, priority
rules, simplifications, or claimed totalizations to audit. The central
result-bearing trust boundary is instead the imported `STRING.length`/ordering
behavior and the exact high-level denotations in `semantic.k`. The local K
distribution explicitly warns that the chosen string implementation does not
fully support code points beyond U+00FF (`evidence/k_string_boundary.log`).
The candidate neither narrows its guards nor states a precondition at that
boundary.

For a proof-level witness of what the concrete input bridge enables,
`evidence/spec-unicode-false-conclusion.k` uses the four K bytes produced by
the candidate runtime parser for raw `😀`. The candidate theory proves
retention with `#Top`, while the actual generated Python function returns
`[]`; see `evidence/false_conclusion.log`. This is a false conclusion about the
raw intended input through the submitted concrete representation bridge, not a
claim that K's abstract byte string is internally inconsistent.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted. I created
`evidence/spec-vacuity-audit.k`, whose universal destination prepends
`"AUDIT_SENTINEL"`:

```text
Result(VList("AUDIT_SENTINEL", sortedListSumSpec(INPUT)))
```

It is demonstrably false for the satisfying witness `INPUT = .Words`, for
which the actual result is empty. The mutation:

1. parsed and compiled through `kprove --dry-run` with exit 0;
2. ran against the fresh proof definition;
3. exited 1 with `WarnStuckClaimState`; and
4. left a residual failed equality containing `AUDIT_SENTINEL`.

Exact commands, statuses, and residual are in
`evidence/stage6_commands.sh` and `evidence/stage6.log`. This is meaningful
non-vacuity evidence: the destination result is proof-relevant. It does not
repair the semantics-to-Python gap.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the freshly compiled candidate K theory, the universal claim establishes:

> For every finite K `Words` value `INPUT`, evaluating the exact submitted AST
> from `Run(solutionProgram, Call(... ValueExpr(VList(INPUT))))` reaches
> `Result(VList(sortByKey(filterEven(INPUT))))`.

The other six claims establish the fixed empty/examples and several
two-/three-element symbolic cross-checks with `evenSorted`. This statement is
result-constraining and body-pinned. It is a theorem about the submitted K
theory.

### Assumptions and trust boundary

| Boundary | Dependents | Accounting |
|---|---|---|
| Trusted `py2mpy.py` transliteration | Program identity | Acceptable trusted input; byte identity was independently re-established. |
| K BOOL, INT, MAP, list, and STRING hooks | All execution/proof claims | Ordinary low-level trust boundary, except the documented String limitation is result-bearing and material here. |
| Mapping Python `str` to K `String` | Parity filter, key length, lexical ordering, every substantive claim | Illegitimate at the claimed unrestricted domain without a precondition or sound Unicode model. Concrete raw-input counterexamples exist. |
| Exact comprehension rule at `semantic.k:150` | Universal and all nontrivial entry claims | Transparent recursive summary, not an oracle, but sound only conditional on the string bridge. There is no more general iteration semantics or independent connection theorem. |
| Exact `sorted` rule at `semantic.k:161` | Universal and all nontrivial entry claims | Transparent insertion-sort summary, but likewise conditional on the string bridge. |
| `sortedListSumSpec => sortByKey(filterEven(...))` | Universal postcondition | Definitional reuse of semantic helpers; it does not independently prove the human-facing filter/sorted properties. |
| `solutionProgram` generator's empty-list normalization | Program pinning | Independently reviewed and regenerated byte-identically; acceptable. |
| K toolchain/parser/backend | Build, proof, concrete execution | Builds/proofs were stable. The Unicode limitation is explicitly documented by the installed toolchain and exposed by reproducible tests, not treated as an unexplained infrastructure failure. |

There are no local opaque symbols, unconstrained oracles, simplification
lemmas, totality assumptions, priority rules, or external state assumptions.

The 5,197-case Python differential test supports the generated
implementation-to-canonical bridge only on those finite cases. The ASCII K
executions support the semantic bridge only on those cases. Neither is a
universal connection theorem. The Unicode K executions actively refute the
candidate's unrestricted concrete bridge.

### Decision

Clean reconstruction and non-vacuity succeed, but they prove the wrong
semantic model for part of the stated input domain. The prompt permits any
Python strings; the claims quantify over all `Words`; and string length controls
both filtering and ordering. The candidate chose a documented incomplete
Unicode primitive without a domain restriction, and fresh concrete witnesses
produce materially wrong returned lists. This is a result-bearing semantic
unsoundness/adequacy failure, not a thin-evidence concern and not an audit
infrastructure error.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
