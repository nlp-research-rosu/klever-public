# Independent adversarial review: HumanEval/0 `has_close_elements`

The candidate contains nine genuine, non-vacuous K reachability theorems about
the submitted constructor term under its generated exact-integer/rational
interpreter. It does **not** contain a proof of the unrestricted HumanEval
contract. Its only symbolic nontrivial lists have fixed lengths two, three, and
four; it has no arbitrary-list claim or induction/circularity. In addition, its
exact-rational value model is not CPython binary-float semantics, and a concrete
rounding witness makes the generated K execution disagree with both Python
implementations. Under the benchmark's explicit mapping, this materially
narrowed `SOUND-BUT-LIMITED` result is `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

I treated every candidate and generation record as untrusted evidence.

- `/audit-input.json` declares `record_layout =
  legacy-selected-stage1`, `condition = bare`, and `semantics_mode =
  GENERATED_SEMANTICS`. The campaign block is structurally identical to
  `/audit-campaign-lock.json`; the lock's observed SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- I inspected `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, both legacy supplemental JSON records, and
  every JSONL record in the structured trace. All required layout records are
  real readable files, and the trace is a real directory containing one
  regular file and no links. The trace contains 419 valid JSON records and 89
  tool calls. Its final `KPROVE_PASSED` statement was used only as an untrusted
  claim. See [stage1-integrity.log](evidence/stage1-integrity.log) and
  [generation-trace-summary.log](evidence/generation-trace-summary.log).
- Every launcher-recorded single-file hash independently recomputed in
  [stage1_integrity.py](evidence/stage1_integrity.py) matches: canonical,
  trusted/candidate prompt, trusted/candidate translator, campaign lock, run
  and task manifests, result and invocation, metrics, usage, generation
  prompt, Codex output, and Codex last message. The trace file's SHA-256
  `7c76633c...` also matches `/generation-result.json`.
- A legacy pipeline-v2 length-delimited tree hash of `/candidate` is
  `2e4679e5...`, matching the retained workspace hash recorded by both
  `/generation-result.json` and `invocation.json`. The corresponding trace-tree
  hash is `32f4161b...`, matching `usage.json`. The differently named aggregate
  tree hashes in `/audit-input.json` use an unstated launcher framing; the
  underlying file hashes and both layout-native tree records match.
- `/candidate/prompt.py` and `/reference/prompt.py` are byte-identical.
  `/candidate/py2mpy.py` and `/reference/py2mpy.py` are byte-identical.
  Candidate entries are regular files, with no missing, additional
  reference-semantics tree, or symlinks.
- `/reference/reference-semantics` is absent, as required for
  `GENERATED_SEMANTICS`. I did not infer or use a hidden reference semantics.
- The mounted toolchain reports K `v7.1.293`, agreeing with the campaign lock.
  Historical runtime metrics absent from this legacy-selected layout were not
  reconstructed.

No infrastructure-stop condition was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` requires
`has_close_elements(numbers: List[float], threshold: float) -> bool`. It must
return `True` exactly when two distinct list elements have absolute difference
strictly less than `threshold`; otherwise it must return `False`. The prompt has
no list-length bound and gives the two examples reproduced in the candidate.
The canonical implementation checks all ordered distinct-index pairs with
Python `abs`, subtraction, and `<`.

`solution.py` uses two recursive functions. For executions that return normally,
`close_to_first` checks the first element against every tail element, and
`has_close_elements` advances the head, so the algorithm enumerates every
unordered pair. Its strict comparison and empty/singleton behavior agree with
the contract.

### Translation fidelity

I regenerated the constructor term with the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
cmp /tmp/audit-work/regenerated-solution.mpy /candidate/solution.mpy
```

The command exited 0 and the files are byte-identical, both with SHA-256
`72ab5b828433279d72f5d206ad80275be823630222794f4eb041ff7b8057178d`.
See [translator-byte-identity.log](evidence/translator-byte-identity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and generated entry points independently. Its deterministic corpus
contains:

- both documented examples;
- empty, singleton, exact-threshold, just-above, and just-below cases;
- each recursive branch position, duplicates, zero/negative thresholds,
  negative values, infinities, and NaN;
- 160 generated cases from seed `0xC10E`; and
- an unrestricted-domain list of 1,050 spaced floats.

The 17 named ordinary cases and all 160 generated cases had zero mismatches.
The valid long case did not:

```text
canonical: return False
generated: raise RecursionError
```

The script exited 1 specifically because of that mismatch; its exact command,
corpus hash, and result are in
[differential-test.log](evidence/differential-test.log). This is a material
implementation-to-contract divergence on an unbounded `List[float]`, not an
audit or tool failure. Although partial correctness need not prove termination,
a Python `RecursionError` is observable exceptional behavior, and the generated
K semantics silently models unbounded mathematical recursion instead.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/candidate-src`, used no
candidate-built definition or cache, and generated fresh output directories.

The following all exited 0:

- LLVM concrete semantics:
  `kompile semantic.k --backend llvm --main-module MPY --syntax-module
  MPY-SYNTAX --output-definition
  /tmp/audit-work/build/semantic-llvm-kompiled`
  ([build log](evidence/build-semantic-llvm.log)).
- Haskell semantic-only definition:
  `kompile semantic.k --backend haskell ... --output-definition
  /tmp/audit-work/build/semantic-haskell-kompiled`
  ([build log](evidence/build-semantic-haskell.log)).
- Haskell proof definition:
  `kompile verification.k --backend haskell --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  /tmp/audit-work/build/verification-haskell-kompiled`
  ([build log](evidence/build-verification-haskell.log)).

The unmodified candidate `spec.k` then exited 0 and printed exactly `#Top`;
see [proof-original-spec.log](evidence/proof-original-spec.log). I also made a
semantically identical labelled copy and selected each of the nine claims
separately. Every invocation exited 0 and printed `#Top`; the commands and
summary are in [prove_individual_claims.sh](evidence/prove_individual_claims.sh),
[proof-individual-summary.log](evidence/proof-individual-summary.log), and
`proof-claim-01.log` through `proof-claim-09.log`.

The fresh LLVM semantics executed the actual submitted `solution.mpy` on prompt,
empty, singleton, strict-boundary, branch-position, negative-threshold, and all
symbolic-claim witness inputs. Thirteen of fourteen K runs agreed with both
Python functions. The one disagreement is a numeric-model witness:

```text
numbers   = [0.30000000000000004, 0.3]
threshold = 5e-17

exact-decimal VRat K result: True
CPython canonical result:    False
CPython solution.py result:  False
```

The candidate's natural exact-decimal representation makes the gap `4e-17`;
CPython's binary-float gap is about `5.55e-17`. All `krun` commands exited 0,
so this is a semantic mismatch rather than a stuck execution. See
[concrete_semantics_check.py](evidence/concrete_semantics_check.py) and
[concrete-semantics.log](evidence/concrete-semantics.log).

Two initial reviewer probes are retained but are not used as candidate evidence:
`concrete-semantics-parser-bug.log` records an over-escaped output parser, and
the `*-bad-label.log` files record an incorrect first `--claims` spelling.
Both were corrected before the results above.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

None of the nine claims has a `requires` clause; each displayed ground or
symbolic shape is therefore satisfiable.

| Claim | Formal input domain and postcondition | Satisfying witness |
|---|---|---|
| 1 | One exact rational length-3 prompt input returns `False`. | The claim's ground input. |
| 2 | One exact rational length-6 prompt input returns `True`. | The claim's ground input. |
| 3 | The empty list returns `False` for every integer threshold. | `([], 0)`. |
| 4 | Any one-integer list returns `False` for every integer threshold. | `([7], -3)`. |
| 5 | Every two-integer list returns exactly `absInt(X-Y) < T`. | `([0,1], 2)` returns `True`. |
| 6 | Every three-integer list returns `hasCloseRef` for that same list and threshold. | `([0,5,5], 1)` returns `True`. |
| 7 | Every four-integer list returns `hasCloseRef` for that same list and threshold. | `([0,10,20,20], 1)` returns `True`. |
| 8 | Exact rational `[1.0,1.5]` at threshold `0.5` returns `False`. | The claim's ground input. |
| 9 | The same exact rational pair at threshold `0.5000001` returns `True`. | The claim's ground input. |

The witness runs agree with both Python implementations and are recorded in
[concrete-semantics.log](evidence/concrete-semantics.log). The destinations are
result-constraining: they are concrete booleans or boolean expressions fixed by
the initial symbols. There is no RHS-only existential result, tautological
postcondition, or one-way implication in place of equality.

### Mechanical pinning

The claims begin with the proof harness term `verify`, not a source-file read.
The actual chain is:

```text
verify(ARGS)
  -> call("has_close_elements", ARGS, solutionFunctions)
  -> call("has_close_elements", ARGS, collect(solutionProgram statements))
```

[program_pinning_check.py](evidence/program_pinning_check.py) extracts the
`solutionProgram` RHS, normalizes only K's internal `.Stmts` spelling to the
concrete empty-list spelling, parses all terms with `kast`, and compares their
constructor JSON. The trusted-regenerated term, submitted `solution.mpy`, and
embedded `solutionProgram` AST are identical. The check exited 0; see
[program-pinning.log](evidence/program-pinning.log). The typing-only import is
present in the term and is ignored by the interpreter's explicit `collect`
rule.

The program-defined bodies are not replaced by `hasCloseRef` or another result
oracle. `call` enters the collected `FuncDef` bodies, and the reference helper
appears only in claims 6 and 7's destinations.

A separate body-sensitivity mutation changed the executed
`has_close_elements` empty-list return from `False` to `True`. The mutated
definition built successfully, and its original `False` obligation exited 1
with a residual `VBool(true)`. See
[verification-body-mutant.k](evidence/verification-body-mutant.k),
[build-body-mutant.log](evidence/build-body-mutant.log), and
[proof-body-mutant.log](evidence/proof-body-mutant.log).

### Fatal adequacy gap

Claims 3 through 7 cover only lengths 0, 1, 2, 3, and 4, and claims 1, 2, 8,
and 9 are four fixed examples. There is no claim with a symbolic tail, no
recursive invariant/circularity, and no induction theorem for arbitrary list
length. In particular, the length-6 prompt example is merely ground execution,
not a size-general theorem. Unrestricted HumanEval inputs of length 5 and
greater are not symbolically covered at all.

The symbolic element domain is also integer-only. Four isolated positive-
denominator rational examples do not prove all finite Python floats, and the
rounding witness in Stage 3 refutes the informal rational-to-binary-float
bridge. This is material domain narrowing, not a maintenance observation.

## 5. Rule-by-rule static soundness review

The exhaustive source-derived inventory, including exact declaration text and
line ranges, is [k-rule-inventory.log](evidence/k-rule-inventory.log). It finds
24 local syntax declarations, one configuration, 52 local rules, and nine
claims. There are 22 `[function]` symbol occurrences, one `[simplification]`
rule, and no local `[total]`, `[functional]`, `[concrete]`, priority, `owise`,
`trusted`, macro, alias, or opaque declarations.

### Syntax, functions, and configuration

The 24 syntax declarations are:

1. `Pgm=Module(Stmts)`, the `Stmts` list, and `Stmt` alternatives
   `ImportFrom`, `FuncDef`, `If`, and `Return`.
2. `Strings`, `Params`, `Exprs`, `CmpOps`, `CmpOp`, `Index`, `Bound`, `Slice`,
   and the expression alternatives `Name`, `Int`, `Float`, `Bool`, `BinOp`,
   `Compare`, `Call`, and `Subscript`.
3. Values `VInt`, `VRat`, `VBool`, `VList`, `VNone`; `PValues`; and stored
   `function(Params,Stmts)`.
4. Operational terms `runProgram`, `call`, `exec`, `branch`, `eval`,
   `subValue`, `absValue`, `compareValue`, `subscriptValue`, `sliceOne`,
   `lengthValue`, `evalExprs`, `concatStmts`, `collect`, `bind`, `verify`, and
   `lengthValues`.
5. Verification terms `solutionProgram`, `solutionFunctions`, `functionsOf`,
   `closePair`, `closeFirstRef`, `hasCloseRef`, and `boolOf`.

The 22 function symbols are `call`, `exec`, `branch`, `eval`, `subValue`,
`absValue`, `compareValue`, `subscriptValue`, `sliceOne`, `lengthValue`,
`evalExprs`, `concatStmts`, `collect`, `bind`, `lengthValues`,
`solutionProgram`, `solutionFunctions`, `functionsOf`, `closePair`,
`closeFirstRef`, `hasCloseRef`, and `boolOf`. They are deliberately partial;
no false totality assertion is present.

The sole configuration is `<k> runProgram($PGM,$ARGS) </k>`. A separate mutable
store, heap, allocation cell, I/O cell, or call stack is unnecessary for this
pure subset: local bindings and the function table are explicit `Map`
arguments, and calls are pure nested terms.

Every constructor used by `solution.mpy` is mapped:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, typing `ImportFrom`, `FuncDef` | `semantic.k:9-15`, collected by rules 74-80; the typing import is semantically inert. |
| `If`, `Return` | `semantic.k:14-15`, executed by rules 89-103. |
| `Name`, `Int`, `Bool` | `semantic.k:27-34`, evaluated by rules 109-111. |
| subtraction and `==`/`<` comparison | rules 113-116 and 143-162. |
| `len`, `abs`, and user calls | rules 118-128. |
| index `0` and slice `[1:]` | rules 130-141. |
| parameter, expression, statement, and value lists | list declarations plus bind/eval/concat/length rules. |

`Float(Float)` syntax is declared but has no `eval(Float)` rule. The submitted
body contains no float literal, so this is not an unused-construct coverage
defect. It does, however, highlight that source floating-point *arguments* are
injected as `VRat` without a faithful Python-float value semantics.

### All 41 `semantic.k` rules

| Lines | Rule(s) | Static judgment |
|---|---|---|
| 74-75 | `runProgram(Module(SS),ARGS)` enters the named entry with `collect(SS)`. | Faithful task-entry setup. |
| 77 | Empty `collect`. | Correct map base. |
| 78 | Ignore `ImportFrom`. | Correct for the typing-only import actually used. |
| 79-80 | Collect a `FuncDef`. | Correct for the two unique function names. Duplicate-name Python rebinding is outside this generated subset. |
| 82 | Empty `bind`. | Correct base for equal arity. |
| 83-84 | Cons `bind`. | Correct positional binding; mismatched arity visibly remains partial. |
| 86-87 | Function lookup and `call`. | Executes the selected stored body with fresh local bindings and the same function table. |
| 89 | `Return` evaluates its expression and discards remaining statements in that function. | Correct abrupt return for the used pure call encoding; it does not discard an outer K continuation. |
| 90-91 | `If` evaluates its condition then forms `branch`. | Correct for boolean conditions used by the program. |
| 93-97 | Concrete boolean branch concatenates selected body with remaining statements. | Correct source control flow. |
| 98-103 | Distribute `branch` over symbolic `#if`; `[simplification]`. | Valid case split with identical environment, function table, and statement continuations on each side; no result oracle. |
| 105 | Empty `concatStmts`. | Correct. |
| 106-107 | Cons `concatStmts`. | Correct, structurally descending. |
| 109 | Environment name lookup. | Correct for uniquely bound used names. |
| 110 | Integer literal. | Correct. |
| 111 | Boolean literal. | Correct. |
| 113-114 | Binary `"-"` delegates evaluated operands to `subValue`. | Correct for pure used operands. |
| 115-116 | One-link comparison delegates to `compareValue`. | Correct for the non-chained comparisons emitted here. |
| 118-119 | Built-in `len`. | Correct on used lists. |
| 120-121 | Built-in `abs`. | Correct on used integers and positive-denominator rationals. |
| 122-124 | User call, excluding names `len` and `abs`. | Guards are disjoint from the two built-ins; correct function binding for the exact table. |
| 126 | Empty argument evaluation. | Correct. |
| 127-128 | Cons argument evaluation. | Structurally correct. Evaluation is pure here, so the absence of a stateful sequencing cell changes no observable behavior. |
| 130-131 | General subscript delegates evaluated base/index. | Correct on the used index-zero case. |
| 132-133 | Exact slice `[1:]`. | Correct used slice. |
| 135 | List length wrapper. | Correct. |
| 137 | Empty `lengthValues`. | Correct. |
| 138 | Cons `lengthValues`. | Correct and descending. |
| 140 | Index zero on a nonempty list. | Correct; source guards make it reachable only when nonempty. |
| 141 | Drop one element. | Correct; used only on nonempty lists. |
| 143 | Integer subtraction. | Correct arbitrary-precision integer arithmetic. |
| 144-145 | Rational-rational subtraction. | Correct when denominators are positive; positive denominators remain positive. |
| 146 | Rational-integer subtraction. | Correct on the same representation. |
| 147 | Integer-rational subtraction. | Correct on the same representation. |
| 149 | Integer absolute value. | Correct. |
| 150 | Rational absolute numerator. | Correct for the positive-denominator representation used by every claim. The unguarded constructor also admits nonpositive denominators; this is a reuse/coverage gap, not an intended-domain false-rule allegation. |
| 152 | Integer equality. | Correct; used for `len(rest)==0`. |
| 153 | Integer less-than. | Correct. |
| 154-156 | Rational less-than. | Correct under explicit positive-denominator guards. |
| 157-159 | Rational-integer less-than. | Correct under its positive-denominator guard. |
| 160-162 | Integer-rational less-than. | Correct under its positive-denominator guard. |

The arithmetic rules are truthful exact-rational equations on their stated or
reachable positive-denominator domain. They do **not** become Python
floating-point equations merely because decimal examples are encoded with
`VRat`. The false behavioral witness is the concrete one from Stage 3: those
exact-rational rules derive `True`, while the real generated and canonical
Python programs both return `False` on the corresponding binary floats.

### All 11 `verification.k` rules

| Lines | Rule | Static judgment |
|---|---|---|
| 9-44 | `solutionProgram` expands to a closed constructor term. | Truthful definitional syntax summary; mechanically identical to trusted regeneration. |
| 48 | `solutionFunctions -> functionsOf(solutionProgram)`. | Truthful setup. |
| 49 | `functionsOf(Module(SS)) -> collect(SS)`. | Exactly the fixed semantic collection step. |
| 50 | `verify(ARGS)` enters `has_close_elements` with `solutionFunctions`. | A proof-harness entry adapter, not a result-bearing oracle; it preserves the framed K continuation and causes the exact body to execute. |
| 59 | `boolOf(VBool(B)) -> B`. | Correct projection. |
| 60-61 | `closePair` is exact `abs(X-Y) < T` using the same arithmetic domain. | Truthful mathematical definition, used only in destinations. |
| 63 | Empty-tail `closeFirstRef`. | Correct existential-pair base. |
| 64-65 | Cons-tail `closeFirstRef`. | Correct and descending disjunction. |
| 67 | Empty-list `hasCloseRef`. | Correct. |
| 68 | Singleton `hasCloseRef`. | Correct. |
| 69-71 | Two-or-more `hasCloseRef`. | Correct decomposition into head/tail pairs and tail-only pairs; structurally descending. |

There is no local rule that replaces the program's pair computation with
`hasCloseRef`, no fresh opaque result, and no circular use of a shared oracle
in execution and postcondition. The helper uses the same trusted low-level
arithmetic, but it is a transparent recursive definition.

I attempted a semantic-only universal connection claim for
`runProgram(Module(SS),ARGS) -> call(...collect(SS))` under an arbitrary module,
argument list, and suffix. It stuck on definedness of the deliberately partial
`collect`/`call` functions for unconstrained malformed modules and arities; see
[proof-runprogram-connection.log](evidence/proof-runprogram-connection.log).
I do not call the entry rule unsound on that basis: the submitted program is
well formed, has two arguments, the fixed semantic rule has literally the same
RHS, constructor pinning succeeds, and body sensitivity succeeds. The failed
over-broad theorem is retained as a narrower universal-evidence limitation.

### Evaluation, state, overlap, and trust observations

- Map lookup and parameter binding select the exact two stored functions and
  preserve the recursive binding.
- All source expressions used here are pure. Thus the functional reduction
  strategy does not hide a state, output, allocation, or exception-order
  difference within the modeled subset.
- The `len`/`abs` call rules and guarded user-call rule are disjoint. Index and
  slice rules have distinct syntax. Integer, rational, and mixed arithmetic
  clauses have distinct value shapes. Empty/singleton/cons recursion clauses
  do not overlap inconsistently.
- Every recursive helper descends on a source or value list. There is no local
  totality assertion whose coverage must be trusted.
- Built-in K `Int`, `Bool`, `Map`, `String`, list machinery, `absInt`,
  integer arithmetic/comparison, `#if`, `orBool`, and K equality are the
  low-level trust boundary. That is acceptable for the exact mathematical
  theorem.
- The generated semantics does not model CPython IEEE-754 values, NaN rules,
  infinities, recursion limits, or exceptions. The float-rounding and
  recursion-depth witnesses show that these omissions are material to the real
  source contract.

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`; none was credited.

I created [spec-vacuity-auditor.k](evidence/spec-vacuity-auditor.k), changing
the empty-list result obligation from the true `VBool(false)` to the false
`VBool(true)` at the satisfiable input `([], 0)`.

1. `kprove ... --dry-run` exited 0, establishing that the mutation parses and
   builds against the fresh proof definition
   ([vacuity-dry-run.log](evidence/vacuity-dry-run.log)).
2. The actual `kprove` exited 1 with `WarnStuckClaimState`; its residual is
   exactly `<k> VBool(false) ~> .K </k>`, which cannot unify with the mutated
   destination ([vacuity-proof.log](evidence/vacuity-proof.log)).

This is expected unmet-result evidence, not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation. The formal claims are
discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the candidate's generated pure interpreter and K's built-in mathematical
primitives, `kprove` establishes partial correctness of the exact submitted AST
for:

- four fixed rational example/boundary inputs;
- empty and singleton integer lists;
- all two-integer lists, with exact result `abs(X-Y) < T`; and
- all three- and four-integer lists, with exact result equal to the transparent
  recursive `hasCloseRef` pair-existence definition.

All nine theorems close independently, constrain the return value, have
satisfiable starts, execute the exact body, and reject both a body mutation and
a false-result mutation.

### Trust and limitation ledger

| Boundary or assumption | Dependents/effect | Judgment |
|---|---|---|
| K built-in unbounded integers, booleans, maps, lists, arithmetic, and logical connectives | Every execution and claim. | Acceptable low-level mathematical trust boundary. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor identity. | Acceptable; byte regeneration and parsed-AST comparison succeed. |
| `solutionProgram` and the `verify` entry adapter | All nine claims. | Acceptable for the immutable candidate: exact constructor equality and body sensitivity are demonstrated; it does not summarize a result. |
| Positive-denominator `VRat` as exact rationals | Four ground rational claims and any rational concrete run. | Sound exact-rational mathematics, but not a proved Python-float model. |
| Exact-rational values standing for CPython binary floats | Any claim presented as a theorem about `List[float]`. | Illegitimate for the full contract; the recorded rounding witness gives opposite K/Python results. |
| Unbounded semantic recursion standing for CPython calls | Long lists. | Illegitimate for the full implementation contract; the 1,050-element witness returns in the canonical function and raises `RecursionError` in `solution.py`. |
| `hasCloseRef` recursive equations | Claims 6 and 7. | Acceptable transparent mathematical definition, but proved equivalent only at fixed lengths 3 and 4. |
| Differential evidence | Source rewrite and numeric adequacy checks on the tested corpus. | Finite empirical support only; it does not extend the K theorem. One material mismatch remains visible. |
| Failed over-broad semantic-only connection claim | Universal entry-wrapper auditability. | Nonfatal evidence limitation for the finite theorems; it supplies no proof of unrestricted typed inputs. |

### Gate and benchmark decision

- **Gate A, formal theorem honesty:** PASS for the nine stated exact-domain
  theorems. The proof is result-constraining, non-vacuous, body-sensitive, and
  executes the pinned program term; no unsound answer-smuggling rule was found.
- **Gate B, intent adequacy:** FAIL. Fixed list lengths 0-4 plus four examples
  do not cover an unrestricted `List[float]`. The generated numeric and
  recursion models also have concrete disagreements with real Python.
- **Gate C, evidence auditability:** The reproduced builds, proofs, tests, and
  mutations are auditable. Finite tests are reported only as finite evidence,
  and the failed bridge probe remains disclosed.

In generic Kit terms this is at best `SOUND-BUT-LIMITED`. The benchmark prompt
explicitly maps material narrowing of the HumanEval source-contract domain to
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
