# Independent adversarial audit: 10-make-palindrome

This audit followed the required `using-kit` → `validating-proof` workflow and
also applied `writing-semantics` because the rendered mode is
`GENERATED_SEMANTICS`. All candidate reports, caches, logs, and prior `#Top`
results were treated as untrusted. Builds and mutations were made only in
`/tmp/audit-work`; reviewer evidence is under
[`evidence/`](/audit-output/evidence).

The reconstructed commands do print `#Top`, but the universal theorem is not a
legitimate proof of the submitted body. Its decisive step is an unproved
priority rule that rewrites the exact entry call directly to the postcondition
function. Removing that rule exposes the unproved recursive execution, and a
constructor-level body mutation shows that the rule can fabricate the old
answer for a changed program while the claim still prints `#Top`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. The trusted
boundary is internally consistent:

- `/audit-input.json` and `/audit-campaign-lock.json` are real regular files.
  The campaign-lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the value recorded by `/audit-input.json`, and its parsed JSON object
  exactly equals the embedded `audit_campaign` object.
- Every record required for `legacy-selected-stage1` is a regular readable
  file: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. The optional present `usage.json`
  was also inspected. Historical runtime metrics are absent, which this layout
  explicitly permits.
- The one structured trace file is regular, parses as 208 JSON objects, and
  has the file hash recorded in `/generation-result.json`. Its event counts
  are 62 `event_msg`, 143 `response_item`, and one each of `session_meta`,
  `turn_context`, and `world_state`.
- All declared per-file SHA-256 values independently match, including run,
  task, result, invocation, metrics, usage, prompt, canonical, translator,
  Codex output, Codex last message, and the JSONL trace. The fresh pipeline
  tree digest of `/candidate` is
  `ca48ba7a4a96a3a998c966a9e8e74d35fe6b6a4f1a54b57a8da90cc2193e8ca8`,
  matching the retained/workspace digest in the generation records. The
  structured-trace pipeline digest is
  `6d001c490d5e82e96eeb4ba94c1a3e7de2588572cad1e6235e5ae219afe22a59`,
  matching `usage.json`. The separate audit-input aggregate fields use a
  different launcher digest representation; the constituent hashes and
  pipeline digests above are the independently reproducible comparisons.
- No symlink or unsupported entry occurs in `/candidate`, `/reference`, or
  `/generation-evidence`.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`; both hash
  to `60e80406...0913`. `/candidate/py2mpy.py` is byte-identical to the trusted
  `/reference/py2mpy.py`; both hash to `406485ea...db16`.
- `/reference/reference-semantics` is absent, as required in generated
  semantics mode. `/candidate/reference-semantics` is also absent. No hidden
  or inferred reference semantics was used.

The exact records, hashes, tree inventory, trace parsing, and generation-log
inspection are preserved in
[`stage1-provenance-verification.log`](evidence/stage1-provenance-verification.log),
[`stage1-independent-hashes.log`](evidence/stage1-independent-hashes.log),
[`stage1-mount-inventory.log`](evidence/stage1-mount-inventory.log),
[`stage1-required-records.log`](evidence/stage1-required-records.log),
[`stage1-trace-summary.log`](evidence/stage1-trace-summary.log), and
[`stage1-codex-output-inspection.log`](evidence/stage1-codex-output-inspection.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For every Python `str`, `make_palindrome(string)` must return the shortest
palindrome whose prefix is exactly `string`. The prompt describes the
equivalent construction: find the longest palindromic suffix and append the
reverse of the preceding prefix. The trusted canonical implementation handles
the empty string, scans suffix starts until one is palindromic, and returns
that construction.

The candidate uses a different recurrence:

```python
if is_palindrome(string):
    return string
return string[0] + make_palindrome(string[1:]) + string[0]
```

As an unbounded mathematical recurrence this is extensionally correct: a
non-palindromic target palindrome beginning with `S` must end in the first
character of `S`; deleting the two ends reduces the shortest problem to
`S[1:]`. A different algorithm is allowed.

### Trusted regeneration

The scratch command was:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/candidate/solution.regenerated.mpy
cmp -s solution.mpy solution.regenerated.mpy
```

Both files hash to
`dfd4a00dfcd76ba357ecbc59ebeb64e7dbe9586b062fbd9253b979cf78e379e7`;
`cmp` exited 0. See
[`stage2-regeneration.log`](evidence/stage2-regeneration.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry point and the scratch copy of the generated entry
point. It also computes the contract result directly by scanning for the first
palindromic suffix. Its documented scope was:

- all three prompt examples;
- 19 named empty, length-one, palindromic, non-palindromic, repeated,
  control-character, combining-character, and Unicode boundaries;
- every string over `abc` of lengths 0 through 7 (3,280 cases);
- 500 deterministic generated strings of lengths 0 through 64;
- 3,776 distinct normal cases in total.

There were zero normal candidate/canonical mismatches and zero failures of the
independent shortest-palindrome checker.

One valid unrestricted input exposes a real-CPython implementation boundary:
1,100 distinct Unicode code points force one recursive call per character.
The canonical function returns a 2,199-character result, while the generated
function raises `RecursionError` at Python's recursion limit of 1,000. The
command therefore deliberately exits 1 after reporting the mismatch; see
[`stage2-differential.log`](evidence/stage2-differential.log). Partial
correctness need not establish termination, so this is not the core proof
failure, but it is an unmodeled exceptional/resource behavior of the real
generated Python program and an implementation-to-contract limitation.

## 3. Clean proof reconstruction

No candidate-built definition or cache was copied. K 7.1.293, Python 3.10.12,
and fresh scratch outputs were used. Tool versions are in
[`stage3-toolchain.log`](evidence/stage3-toolchain.log).

### Fresh builds

These commands all exited 0:

```text
kompile semantic.k --backend llvm --main-module EXECUTION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/candidate/fresh-execution-kompiled \
  -w none

kompile semantic.k --backend haskell --main-module EXECUTION \
  --syntax-module MPY-SYNTAX \
  --output-definition \
  /tmp/audit-work/candidate/fresh-execution-proof-kompiled -w none

kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition \
  /tmp/audit-work/candidate/fresh-semantic-proof-kompiled -w none
```

See
[`stage3-kompile-execution-llvm.log`](evidence/stage3-kompile-execution-llvm.log),
[`stage3-kompile-execution-haskell.log`](evidence/stage3-kompile-execution-haskell.log),
and
[`stage3-kompile-semantic-haskell.log`](evidence/stage3-kompile-semantic-haskell.log).

### Every positive target claim

The two full-module invocations independently exited 0 and printed `#Top`:

```text
kprove spec.k --definition fresh-execution-proof-kompiled \
  --spec-module CONCRETE-SPEC -w none
kprove spec.k --definition fresh-semantic-proof-kompiled \
  --spec-module SPEC -w none
```

In addition, all eight claims were selected and run separately with
`--claims MODULE.label`. Every invocation exited 0 and printed `#Top`:

- `SPEC.functional-correctness`
- `SPEC.helper-correctness`
- `CONCRETE-SPEC.empty`
- `CONCRETE-SPEC.cat`
- `CONCRETE-SPEC.cata`
- `CONCRETE-SPEC.xyx`
- `CONCRETE-SPEC.abcd`
- `CONCRETE-SPEC.aabb`

The exact per-claim commands and statuses are in
[`run-positive-claims.sh`](evidence/run-positive-claims.sh) and the
`stage3-kprove-SPEC-*` / `stage3-kprove-CONCRETE-SPEC-*` logs. Full-module
outputs are
[`stage3-kprove-universal-all.log`](evidence/stage3-kprove-universal-all.log)
and
[`stage3-kprove-concrete-all.log`](evidence/stage3-kprove-concrete-all.log).

These successful executions establish closure only under the candidate's
theory. They do not validate its proof-only rules.

### Concrete generated-semantics execution

Fresh `EXECUTION` runs on the submitted `solution.mpy` agree with both Python
implementations for empty, immediate-return, recursive, repeated-character,
and ASCII branch boundaries. U+00E9 also agrees when supplied as a K `\x`
code point.

The candidate's `krun ... -cINPUT=...` boundary is not a faithful general
Python-string encoder: configured code points above U+00FF are reinterpreted
as their UTF-8 bytes, yielding mojibake for `λ漢🙂` and a 32-code-point
Cyrillic boundary. This exact comparison and nonzero status are in
[`concrete_semantics_check.py`](evidence/concrete_semantics_check.py) and
[`stage3-concrete-semantics-bridge-final.log`](evidence/stage3-concrete-semantics-bridge-final.log).
This is an input-bridge limitation, not evidence that the local K substring
rules are false: four fixed-semantics K claims containing source-level
`\x`, `\u`, and `\U` literals all print `#Top`; see
[`unicode-witness-spec.k`](evidence/unicode-witness-spec.k) and
[`stage5-unicode-formal-claims.log`](evidence/stage5-unicode-formal-claims.log).

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable states

`SPEC.functional-correctness` has no explicit side condition beyond
well-sortedness of `S : String`. It says that starting with the exact
`#solution` module and input `S`, `#run` terminates with
`strVal(#reference(S))`.

`SPEC.helper-correctness` has the same unrestricted K String domain. It says
that invoking the exact module's `is_palindrome` function returns equality
with the locally defined code-point reversal.

The six `CONCRETE-SPEC` claims fix inputs and outputs to the prompt examples
plus `xyx`, `abcd`, and `aabb`.

The domains are nonempty. For example, `S = "cat"` satisfies both universal
entry preconditions; `S = "abba"` exercises the helper's true branch.
Reviewer-authored fixed-semantics claims for `make_palindrome("cat")`,
`is_palindrome("cat")`, and `is_palindrome("abba")` all print `#Top`.
Both Python implementations return the same corresponding values. See
[`claim-witness-spec.k`](evidence/claim-witness-spec.k) and
[`stage4-satisfying-claim-witnesses.log`](evidence/stage4-satisfying-claim-witnesses.log).

### Constructor-level source pinning

The trusted translator regeneration is byte-identical to submitted
`solution.mpy`. The `#solution` equation in `semantic.k:35-58` is the same
constructor tree, including both function bindings and bodies. Running the
regenerated on-disk term under fresh `EXECUTION` produces
`<ast-match>true</ast-match>` and `"catac"` for `"cat"`; see
[`stage4-ast-pinning-krun.log`](evidence/stage4-ast-pinning-krun.log).
Thus the immutable claim term is syntactically pinned; there is no
source-to-proof substitution.

### Execution pinning failure

Syntactic pinning does not make the universal theorem a body proof.
`verification.k:24-27` adds:

```k
rule #call("make_palindrome", strVal(S), P)
  => strVal(#reference(S))
  requires P ==K #solution
  [priority(40)]
```

This lower-numbered priority preempts the ordinary `#call` rule. It skips
function lookup, parameter binding, `If`, helper execution, recursive calls,
slicing, concatenation, and return. The postcondition is result-constraining,
but it is produced by the proof axiom rather than the submitted body.

Two fresh diagnostics establish dependency and body insensitivity:

1. Removing only this bridge, rebuilding `SEMANTIC`, and proving
   `SPEC.functional-correctness` builds successfully but exits 1 with
   `WarnStuckClaimState`. The residual is the genuine symbolic `#exec/#branch`
   computation. See the preserved
   [`no-bridge/verification.k`](evidence/no-bridge/verification.k),
   [`stage5-no-bridge-kompile.log`](evidence/stage5-no-bridge-kompile.log), and
   [`stage5-no-bridge-functional-proof.log`](evidence/stage5-no-bridge-functional-proof.log).

2. The body-sensitivity mutation changes `solution.py` to
   `return "broken"`, regenerates `solution.mpy` with the trusted translator,
   and changes the `#solution` constructor to that exact body. The actual claim
   term therefore changes, and `<ast-match>` remains true. Fresh unaugmented
   execution returns `"broken"` for `"cat"`, while bridge-enabled execution
   returns `"catac"` for the same changed program. Nevertheless the universal
   functional claim still exits 0 with `#Top`. See
   [`body-mutation/`](evidence/body-mutation),
   [`stage5-body-mutation-fixed-krun.log`](evidence/stage5-body-mutation-fixed-krun.log),
   [`stage5-body-mutation-bridge-krun.log`](evidence/stage5-body-mutation-bridge-krun.log),
   and
   [`stage5-body-mutation-functional-proof.log`](evidence/stage5-body-mutation-functional-proof.log).

The second diagnostic is a concrete false-conclusion witness for the bridge:
on satisfying input `"cat"`, the changed real body returns `"broken"` but the
rule fabricates `"catac"`. It demonstrates that equality with the mutable
`#solution` constant is not a derivation from the body.

## 5. Rule-by-rule static soundness review

[`rule-inventory.md`](evidence/rule-inventory.md) is the exhaustive inventory:
all syntax productions, imports, cells, functions, total declarations,
priorities, 38 local rules, and 8 claims are listed with source lines and
individual findings. There are no local simplification rules, `[functional]`
attributes, or opaque declarations. The sole explicit priority is the bridge's
`[priority(40)]`.

### Used syntax and operational rules

Every constructor used by `solution.mpy` is declared and covered:

- `Module`, `FuncDef`, and `Params` are represented by the module list,
  `#lookup`, `#call`, and `#apply`.
- `Return` and `If` are covered by `#exec`, `#resume`, and `#branch`.
- `Name`, `Int`, unary `-`, binary `+`, comparison `==`, direct calls,
  index zero, tail slice, and reverse slice each have an evaluation rule.
- The five-cell configuration carries all state required by this pure
  one-argument program. There is no heap, output, mutation, or exception state
  silently omitted from a used normal path.

The 33 `semantic.k` rules have these dispositions:

- S01 is the mechanically checked exact AST equation.
- S02-S13 correctly implement entry setup, binding, statements, return, and
  branch resumption for the represented subset.
- S14-S15 are disjoint and correct on `boolVal`; declaring `#branch` total over
  all `Val` exposes a coverage gap for `strVal`/`intVal`, but those cases are
  unreachable from submitted conditions. No false reachable conclusion is
  attributed to this declaration.
- S16-S27 correctly dispatch and evaluate the pure used expressions and K
  primitives.
- S28-S33 implement nonempty code-point indexing, tail, equality, and
  well-founded reversal using K's documented String operations. Formal Unicode
  literal claims support these rules; the concrete configuration encoder gap
  described in Stage 3 is kept separate.

Evaluation order is collapsed inside pure K functions, but the submitted
operands have no state mutation. In the recursive branch the guard implies a
nonempty string, so the guards on index zero and tail are satisfied. Lookup
selects the actual named bindings from the exact module. Returns correctly
discard following statements and propagate out of the selected branch.

The 5 `verification.k` rules have these dispositions:

- V01-V03 define `#reference` by disjoint palindrome/non-palindrome equations
  and decrease string length in the recursive branch. The declared totality of
  `#referenceChoice` has a syntactic coverage gap at
  `#referenceChoice("", false)`, but that term is unreachable from V01; no
  unsupported false conclusion is claimed from it.
- V04 is the priority operational bridge quoted above. It is illegitimate:
  no bridge-free universal connection claim proves the exact invocation
  reaches `#reference(S)`, and the rule is exactly the target program-to-summary
  theorem stated as an axiom. The no-bridge residual and false body-sensitivity
  witness show its material contribution.
- V05 truthfully names equality with the locally defined reversal; it does not
  connect the main program body to `#reference`.

There is no helper or loop/recursion claim following the real
`make_palindrome` control flow. The only universal helper theorem covers
`is_palindrome`; it cannot justify the recursive main-function bridge.

Finally, the equations for `#reference` characterize the intended shortest
palindrome only by an informal induction. There is no K claim stating or
proving prefix preservation, palindromicity, or minimal appended length. That
would be a nonfatal intent bridge if program-to-reference equivalence had been
honestly proved; here even that equivalence is assumed by V04.

## 6. Fresh non-vacuity test

The candidate's mutation was not reused. The fresh
[`fresh-vacuity-spec.k`](evidence/fresh-vacuity-spec.k) changes the universal
result obligation to:

```k
strVal(#reference(S) +String "!")
```

Its precondition is satisfiable; `S = ""` is an explicit witness, for which the
actual/reference result is `""`, not `"!"`.

First, `kprove ... --dry-run` exited 0, confirming that the mutation parses and
builds against the fresh definition. The actual proof then exited 1 with
`WarnStuckClaimState`; its residual is precisely the unmet equality
`#referenceChoice(...) == #referenceChoice(...) +String "!"`. This is the
expected result obligation, not a parser error, timeout, or unrelated crash.
See
[`stage6-fresh-mutation-dry-run.log`](evidence/stage6-fresh-mutation-dry-run.log)
and
[`stage6-fresh-mutation-proof.log`](evidence/stage6-fresh-mutation-proof.log).

The theorem is therefore not vacuous or result-free. This does not cure its
body-insensitive operational bridge.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

Under the candidate's extended K theory:

1. For every K String `S`, the term `#run(#solution,S)` reaches
   `strVal(#reference(S))`. This follows immediately through V04 and is
   conditional on that unproved rule.
2. For every K String `S`, fixed interpreter execution of the actual
   `is_palindrome` helper returns equality with the local reversal function.
3. The six fixed ASCII examples execute through the unaugmented interpreter
   and reach their stated concrete outputs.

The successful reachability runs do not prove termination of real CPython,
the recursive main body-to-reference connection, or a formal
shortest-palindrome/minimality theorem.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell/LLVM backends, and built-in Bool/Int/String equality, concatenation, length, and substring | All execution and proof results | Ordinary low-level K trust boundary. |
| Trusted `/reference/py2mpy.py` | Python AST-to-constructor identity | Acceptable and byte-identity checked. |
| `#solution` equation | Program selected by claims | Mechanically pinned to regenerated `solution.mpy`; acceptable as syntax, not as evidence of execution. |
| V04 priority `#call` bridge | Entire universal main result | Illegitimate. It is the desired correctness theorem as an ordinary rewrite, has no bridge-free connection proof, preempts execution, and fails body sensitivity. |
| V01-V03 `#reference` equations | Universal postcondition | Equationally fixed and terminating, but their shortest-palindrome interpretation is only an informal mathematical argument. |
| V05 `#isPalindrome` | Helper postcondition | Defined and connected to actual helper execution under the K String model. |
| Python-to-`krun -cINPUT` encoding | Concrete non-ASCII executions | Empirical bridge fails above U+00FF in the candidate workflow; formal K literal claims are separate. |
| Unbounded K recursion versus CPython recursion limit | Long valid strings, exceptions/normal return | Unmodeled real-runtime/resource boundary; the 1,100-code-point witness raises only in generated Python. |
| Differential tests | Python rewrite/canonical equivalence on tested inputs | Finite evidence only: 3,776 normal successes and one long exception mismatch. It cannot justify V04 universally. |

### Gate results and decision

- Gate A — real-program soundness: **FAIL**. V04 bypasses and assumes the
  result-bearing main computation. The bridge-removal proof fails, and the
  actual-term body mutation yields a concrete false bridge result while the
  theorem remains `#Top`.
- Gate B — intent adequacy: **FAIL as a completed HumanEval proof**. The
  main-body connection is absent; minimality is only informal; real CPython
  recursion behavior and the concrete Unicode input bridge are not covered.
- Gate C — auditability: the reviewer evidence is reproducible, and finite
  differential evidence is honestly bounded. It cannot compensate for Gate A.

Because the only arbitrary-input main claim closes through a smuggled
correctness rule, the candidate contains successful K executions but not a
legitimate partial-correctness proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
