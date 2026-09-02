# Independent adversarial audit: 117-select-words

## Executive finding

The candidate's Python implementation is faithful to the trusted canonical
implementation, the submitted translation is genuine, the fresh builds
succeed, every isolated positive claim prints `#Top`, the claims contain the
actual submitted program term, and a fresh false-result mutation is rejected.
Those facts are not enough to make this a legitimate proof.

There are two independently material defects:

1. `semantic.k:102-121` is a program-specific operational bridge for the
   complete nested-comprehension expression. It replaces all material
   evaluation of `split`, both comprehensions, binding, `lower`, membership,
   `len`, and equality with
   `pyList(filterWords(words(S), N))`. None of those used expression constructs
   has independent operational rules. `verification.k:12-13` defines the
   purported contract as exactly the same helper term. There is no
   bridge-free connection theorem. Removing this one rule leaves the proof
   stuck at the untouched expression. The universal `#Top` is therefore a
   consequence of an answer-encoding semantics rule and its matching
   postcondition, not a proof that the real language operations compute the
   contract.
2. The helper semantics is concretely wrong on an input allowed by the
   source contract. `İ` is a letter. For `select_words("İ", 2)`, both the
   trusted canonical and submitted Python functions return `[]`, because
   Python iterates one character and counts one consonant. The freshly rebuilt
   K semantics processes the rendered string as two units and returns
   `pyList(WCons("\xc4\xb0", .Words))`. This is a false-result witness for the
   `substrString`-based character-count model in `semantic.k:163-174`. The
   prompt never restricts “letters” to ASCII, and the symbolic claim itself
   admits every K `String`.

The first defect fails real-program semantic soundness even under an
ASCII-only reading. The second is also a material source-domain mismatch.

## 1. Input and provenance integrity

Status: PASS; no audit-infrastructure breach.

- The required `using-kit`, `writing-semantics`, and `validating-proof`
  instructions were applied in that order. The fully read session copies are
  byte-identical to the approved `/kit-skills` mounts
  (`evidence/00-kit-skill-integrity.log`).
- `/audit-input.json` declares `record_layout = "pipeline-v3"`,
  `semantics_mode = "GENERATED_SEMANTICS"`, condition `bare`, and problem
  `117-select-words`.
- Every pipeline-v3 required record is present as a real regular file, and the
  candidate, generation root, and trace are real directories. No symlinks
  occur below `/candidate`, `/generation-evidence`, or `/reference`.
- `/reference/reference-semantics` is absent, as GENERATED_SEMANTICS requires.
  No hidden or inferred reference semantics was used.
- `/audit-campaign-lock.json` is structurally identical to the
  `audit_campaign` block and hashes to the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Independently computed SHA-256 values match the recorded values for the
  campaign lock, canonical, trusted and candidate prompt, trusted and
  candidate translator, run manifest, task manifest, stage-one result,
  invocation, metrics, runtime metrics, usage, generation prompt, final
  message, output log, and trace leaf.
- The candidate prompt and translator are byte-identical to their trusted
  mounts. The embedded task view adds the run-level `config` field; every raw
  `/task.json` field agrees, and its independently computed hash agrees with
  both `task_manifest_sha256` and `manifest_sha256`.
- The structured trace contains one regular JSONL leaf with 217 valid JSON
  records. Its leaf hash agrees with both the stage result and audit input.
  The large output log and complete trace were read and independently
  summarized. Their statements remain untrusted generation history.
- A complete SHA-256 leaf manifest of the mounted candidate was recorded.
  Candidate-provided compiled trees and bytecode were inventoried but never
  reused.

Evidence:

- `evidence/01-provenance.log` — exact provenance command, all checks, candidate
  leaf manifest, exit 0.
- `evidence/02-trace-extract.log` — all structured tool calls/results rendered
  for review, exit 0.
- The untrusted trace is consistent with the final artifact and also records
  that an initially separate `specFilterWords` obligation got stuck and was
  deleted before `selectWordsSpec` was changed to the same `filterWords` term.
  This history is corroboration only; the judgment below comes from the
  submitted files and fresh experiments.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

The trusted contract is: for a string containing only letters and spaces and a
natural number `n`, split the string into words, retain in original order
exactly the words containing `n` consonants, and return `[]` for empty input.
The trusted canonical counts a character as a consonant when its lowercase
value is not one of `a`, `e`, `i`, `o`, `u`.

`solution.py` implements the same computation using nested list
comprehensions. Iterating a word directly instead of iterating indices and
testing membership in `"aeiou"` instead of a five-element list are equivalent
for the documented inputs.

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
871478db9cc95201ae736b7927051df9bb1bd36087181e043189bb57bbad0482
```

The independent differential test imports `/reference/canonical.py` and
`/candidate/solution.py`. It covers all five prompt examples, empty and
spaces-only cases, leading/trailing/repeated spaces, zero and positive
consonant boundaries, vowel/consonant and include/exclude branches, upper
case, and `n` above every word length. It then checks:

- every string of length 0 through 7 over `"aB "` for every `n` from 0 through
  8 (3,280 strings, 29,520 comparisons); and
- 5,000 deterministic generated ASCII-letter/space cases, length 0 through
  80 and `n` from 0 through 24.

Including 16 named cases, all 34,536 comparisons agree.

Evidence:

- `evidence/03-scratch-copy.log` — explicit source-only scratch copy, exit 0.
- `evidence/04-translation-identity.log` and
  `evidence/regenerated-solution.mpy` — trusted regeneration and byte
  comparison, exit 0.
- `evidence/differential_test.py` and `evidence/05-differential.log` — complete
  scope, oracle, seed, results, zero mismatches, exit 0.

These are finite fidelity results, not a universal K connection proof.

## 3. Clean proof reconstruction

Status: mechanical reconstruction PASS.

Only source files were copied to
`/tmp/audit-work/117-select-words-audit`. The candidate's
`semantic-kompiled`, `verification-kompiled`, caches, and bytecode were not
copied or used. The observed tools are K v7.1.293.

Fresh builds:

- LLVM `semantic-fresh-kompiled`: exit 0
  (`evidence/06-kompile-concrete.log`).
- Haskell `verification-fresh-kompiled`: exit 0
  (`evidence/07-kompile-proof.log`).

Fresh generated-semantics execution was compared with both Python
implementations on nine normal and boundary cases. Every run exited 0, ended
with `.K`, and had the same list result
(`evidence/k_concrete_compare.py`, `evidence/08-concrete-compare.log`).

The candidate has seven anonymous positive claims. A reviewer script split
them without changing their claim text. The aggregate command printed `#Top`
and exited 0 (`evidence/10-kprove-all.log`). Each claim was then run in its own
spec module; every one printed `#Top` and exited 0
(`evidence/11-kprove-claim-1.log` through
`evidence/11-kprove-claim-7.log`). The splitter and its output record are
`evidence/split_claims.py` and `evidence/09-split-claims.log`.

The Unicode probes are also fresh generated-semantics executions. They expose
the semantic mismatch discussed in stages 5 and 7:
`evidence/24-unicode-letter-probe.log` and
`evidence/25-unicode-false-positive.log`.

## 4. Adequacy and real-program pinning

Status: program identity PASS; result independence and semantic adequacy FAIL.

The seven entry claims mean:

1. For arbitrary K `String` `S` and integer `N >= 0`, execute the exact
   submitted module and finish with
   `selectWordsSpec(S, N)`.
2. On `"Mary had a little lamb", 4`, return `["little"]`.
3. On `"Mary had a little lamb", 3`, return `["Mary", "lamb"]`.
4. On `"simple white space", 2`, return `[]`.
5. On `"Hello world", 4`, return `["world"]`.
6. On `"Uncle sam", 3`, return `["Uncle"]`.
7. On `"", 0`, return `[]`.

All preconditions are satisfiable. The six concrete claims have no
preconditions. For the symbolic claim, `S = "b", N = 1` is one witness, and
both Python programs and fresh K execution return `["b"]`.

`evidence/claim_program_compare.py` extracts all seven `<k>` programs and
compares them with `solution.mpy`. After erasing whitespace and only the
explicit empty-list unit spellings (`.Strings`, `.Exprs`, `.CmpOps`,
`.CompFors`), every 417-character constructor term is identical
(`evidence/12-claim-program-identity.log`). Thus this is not a substituted
source body.

The independent body-sensitivity mutation changes the actual claim term from
`Str("aeiou")` to `Str("aeio")`, leaving the postcondition unchanged. It
parses successfully (`evidence/14-body-mutation-dry-run.log`) and then exits 1
with the changed expression stuck at `eval`
(`evidence/spec-body-mutation.k`,
`evidence/15-body-mutation-proof.log`). This confirms exact syntactic pinning,
but it also demonstrates that the evaluator supports only the hard-coded
program shape.

The fatal adequacy issue is the result specification:

```k
rule selectWordsSpec(S, N)
  => pyList(filterWords(words(S), N))
```

That right-hand side is exactly the right-hand side produced by the complete
expression rule. The claimed “independent contract” is therefore not
independent, and no claim establishes that this common term is the denotation
of the material Python operations.

## 5. Rule-by-rule static soundness review

Status: FAIL.

### Exhaustive local inventory

There are no generated helper K files beyond `semantic.k`; the only
proof-local file is `verification.k`. The full numbered source and attribute
search are preserved in `evidence/16-rule-inventory.log`.

Syntax declarations in `MPY-SYNTAX`:

- sorts/list sorts: `Module`, `Stmt`, `Stmts`, `Expr`, `Exprs`, `Strings`,
  `CmpOp`, `CmpOps`, `CompFor`, and `CompFors`;
- `Module(Stmts)`;
- statement constructors: ordinary `FuncDef`, closure-annotated `FuncDef`,
  `Return`, and `Expr`;
- expression constructors: `Name`, `Str`, `Int`, `Attribute`, `Call`,
  `ListComp`, and `Compare`; and
- `CmpOp` and `CompFor`.

Semantic value/control syntax:

- `Words`: `.Words`, `WCons`;
- `PyValue`: `pyList`;
- `Result`: `noResult` or `PyValue`;
- `KItem`: `exec`, `eval`, `finish`;
- functions `words`, `scanWords`, `appendWord`, `filterWords`, and
  `countConsonants`; and
- proof-local function `selectWordsSpec`.

All six local functions carry only `[function]`. There are no `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, priority, `owise`, opaque,
or local macro declarations. There are no local lemmas or auxiliary claims
outside `spec.k`.

The configuration has exactly `<k>`, `<inputS>`, `<inputN>`, and `<result>`
inside `<select-words>`.

All 21 local rules:

1. Two module-entry rules select ordinary or closure-annotated
   `select_words("s", "n")`.
2. One docstring rule discards a leading string expression.
3. One return rule packages `eval(E, S, N) ~> finish`.
4. One finish rule stores a `PyValue`.
5. One complete-expression `eval` rule maps the exact nested comprehension to
   `pyList(filterWords(words(S), N))`.
6. One `words` rule initializes scanning.
7. Five `scanWords` rules cover empty input/current word and the
   space/non-space cases.
8. Two `appendWord` rules recursively append to `Words`.
9. Three `countConsonants` rules cover empty, vowel, and non-vowel cases.
10. Three `filterWords` rules cover empty, equal-count, and unequal-count
    cases.
11. One `selectWordsSpec` rule aliases the expression bridge's result.

### Adjudication

- The syntax declarations are behaviorally inert and parse the submitted
  term.
- The two module-entry, docstring, return, and finish rules are plausible for
  this exact external-entry harness. They preserve the continuation and the
  only observable result cell. The input cells stand in for argument binding;
  there is no general environment or call stack. That abstraction is
  acceptable only for the exact entry invocation.
- The complete-expression rule at `semantic.k:102-121` is an operational
  bridge, not ordinary per-construct semantics. Its matched expression is
  exact, its explicit `S,N` parameters avoid a free-value oracle, and its
  helper computation agrees with the ASCII samples. Nevertheless, it skips
  every material property-bearing operation in the submitted body. There is
  no bridge-free semantics or universal connection theorem establishing
  binding, comprehension evaluation, `lower`, membership, `len`, equality,
  and returned-list equivalence over the bridge's full domain.

  This is not merely an unproved optimization. With the rule removed, the
  source still builds, but the symbolic proof exits 1 at the untouched `eval`
  expression (`evidence/semantic-no-bridge.k`,
  `evidence/18-kompile-no-bridge.log`,
  `evidence/19-kprove-no-bridge.log`). Thus claim closure depends entirely on
  the task-specific bridge. Finite tests do not supply the required universal
  connection.
- The `words`/`scanWords` guards are disjoint for empty/nonempty input, current
  word empty/nonempty, and U+0020/non-U+0020. The recursive calls remove one K
  string unit. They correctly discard repeated ASCII spaces and preserve word
  order in tested ASCII cases.
- The two `appendWord` equations are disjoint and structurally decreasing.
- The three `countConsonants` guards are disjoint assuming the imported
  `findString` contract returns `-1` or a nonnegative index. They decrease the
  K string by `substrString(..., 1, ...)`. This is not Python character
  iteration over the full source domain.

  Concrete false-conclusion witness: U+0130 LATIN CAPITAL LETTER I WITH DOT
  ABOVE (`İ`) is a letter and satisfies the prompt's letters/spaces
  restriction. Python evaluates both the canonical and submitted program as:

  ```text
  select_words("İ", 2) == []
  ```

  The fresh K execution evaluates it as:

  ```text
  pyList(WCons("\xc4\xb0", .Words))
  ```

  See `evidence/25-unicode-false-positive.log`. The inverse discrepancy is
  also recorded for `n = 1` in
  `evidence/24-unicode-letter-probe.log`. This is a concrete intended-domain
  witness that the `substrString`-based counter can enable a false result; it
  is not an inference from a timeout or a missing rule.
- The three `filterWords` equations have disjoint integer-equality guards and
  structurally decrease `Words`. They correctly filter relative to the local
  counter, but inherit its false Unicode result.
- `selectWordsSpec` is a terminating definitional alias with no overlap. Its
  equation is true by its own definition, but it is not an independently
  justified HumanEval contract. Because it is the identical term used by the
  operational bridge, it makes the universal reachability implication
  circular with respect to the property that needed proof.

I do not label the helper equations extensionally false on the tested ASCII
subdomain: the fresh executions and differential tests support that narrower
bridge. The defects are the absent universal real-operation connection, the
answer-encoding evaluator, and the explicit Unicode counterexample on the
unrestricted letters domain.

## 6. Fresh non-vacuity test

Status: PASS, but not curative.

The candidate contains no `spec-vacuity.k`. The reviewer generated a distinct
claim over the exact submitted program with satisfying input `S = "b", N = 1`
and mutated only the required result from the true `["b"]` to false `[]`.

- Both Python implementations return `["b"]`.
- Fresh concrete K execution returns
  `pyList(WCons("b", .Words))`.
- The mutation dry-run succeeds, proving it parses and builds.
- Actual `kprove` exits 1 with `WarnStuckClaimState`; the residual is the final
  configuration with `WCons("b", .Words)`, exactly the unmet result
  obligation.

Evidence:

- `evidence/make_false_postcondition.py`,
  `evidence/spec-vacuity.k`,
  `evidence/20-make-false-postcondition.log`;
- `evidence/21-vacuity-witness.log`;
- `evidence/22-vacuity-dry-run.log`; and
- `evidence/23-vacuity-proof.log`.

The proof is result-sensitive under its own theory. Non-vacuity does not prove
that the theory is a sound semantics of the source.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate-authored theory, for every K `String` `S` and integer
`N >= 0`, this exact constructor term is loaded, its docstring is skipped, its
return expression is replaced by the one whole-expression rule, and the
result cell becomes:

```text
pyList(filterWords(words(S), N))
```

The destination becomes the same term after unfolding `selectWordsSpec`.
The six concrete claims additionally establish the six listed ground outputs
under that theory. This is partial correctness under the supplied rewrite
system. It is not a universal theorem about executing the Python constructs.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293, Haskell/LLVM backends, imported `BOOL`, `INT`, `STRING`, and domain syntax | Parsing, string/int primitives, rewriting, and every claim | Ordinary low-level trust boundary. Its observed string-unit behavior exposes, rather than excuses, the Python-model mismatch. |
| Trusted `py2mpy.py` | Source-to-constructor identity | Acceptable and byte-checked. |
| External `<inputS>/<inputN>` binding and direct entry selection | Replaces a general Python call/environment | Acceptable for this exact entry harness; not a general Python semantics. |
| `semantic.k:102-121` whole-expression evaluator | Determines the symbolic and every concrete program result | Illegitimate program-derived operational bridge: no independent used-construct semantics or bridge-free universal connection theorem. |
| `words`, `scanWords`, `appendWord`, `countConsonants`, `filterWords` | Defines the value produced by the bridge | Finite ASCII evidence only; the Unicode witness falsifies the claimed full letters-domain bridge. |
| `selectWordsSpec` | Entire symbolic postcondition | Circular alias of the bridge result, not an independently proved contract. |
| Python differential testing | Candidate implementation vs trusted canonical on 34,536 inputs | Strong finite implementation evidence, but no K universal connection theorem. |
| Nine ASCII K/Python comparisons and Unicode probes | Empirical generated-semantics bridge | Finite evidence; the Unicode mismatch is a direct counterexample. |

There are no opaque symbols, proof-local simplification rules, priorities,
totality declarations, or auxiliary lemmas to add to the ledger.

Gate A fails because the only evaluator is an unjustified task-specific
operational bridge and because its helper semantics has a concrete false
source-domain result. Gate B fails because the proof's “contract” is the same
term as the bridge and the language model materially narrows the letters
domain. Gate C cannot repair either failure; all finite evidence has been
reported with its actual scope.

The clean `#Top`, exact AST pinning, Python fidelity, and successful
non-vacuity mutation are genuine but conditional facts. They do not outweigh
the answer-encoding semantic bridge or the witnessed semantic divergence.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
