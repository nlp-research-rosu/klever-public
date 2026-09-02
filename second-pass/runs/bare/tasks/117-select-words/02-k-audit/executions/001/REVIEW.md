# Independent adversarial review: 117-select-words

The candidate is not a legitimate partial-correctness proof of the real
generated Python program over the source-contract domain. Fresh builds and all
seven submitted reachability claims do close, the claim is non-vacuous, and
the exact translated program is pinned. Those facts are outweighed by two
Gate-A failures in the generated semantics:

1. The only evaluation rule for the property-bearing expression atomically
   replaces this task's exact nested-comprehension AST with the same
   `filterWords(words(S),N)` term used in the postcondition. There is no
   independent execution semantics or bridge-free connection theorem.
2. That summary is concretely false for a valid letters-only input. For
   `s = "é", n = 1`, trusted and submitted Python both return `["é"]`; the
   generated K semantics returns `[]` and instead selects `"é"` at `n = 2`.
   The recurrences count the two UTF-8 units exposed by the K string
   operations, whereas Python iterates one Unicode character.

## 1. Input and provenance integrity

`/audit-input.json` declares `pipeline-v3`, condition `bare`, and
`GENERATED_SEMANTICS`. All launcher-declared mounts and all required
pipeline-v3 records were present, regular/readable, and non-symlinked:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace.

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json`; its independently calculated SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded single-file hash checked by the reviewer matches. The one trace
file has 217 valid JSONL records and the exact hash recorded by
`generation-result.json`; the untrusted textual generation log has 20,119
lines. The generation records' prior `#Top` and success report were not used
as proof evidence.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. No
`/reference/reference-semantics` exists, as required in generated-semantics
mode. There are no symlinks under the candidate, reference, or generation
evidence trees. All required proof source artifacts are regular files.

Two aggregate fields in `/audit-input.json` are not reproducible with the
installed pipeline tree-hash algorithm:

- candidate audit field `7a44...` versus independently computed
  `42e75f...`;
- trace audit field `3a269d...` versus independently computed `48db97...`.

The latter computed values exactly match, respectively,
`generation-result.json.outputs.workspace_sha256` and
`usage.json.source_trace_sha256`; every constituent file hash also matches its
record. I therefore record this as an aggregate-hash/serialization provenance
limitation, not a missing or unreadable mount and not a candidate-content
change. It is not the basis for the candidate verdict.

Evidence: `evidence/01-provenance-check.py` and
`evidence/01-provenance.log` (exit 0). The toolchain record is
`evidence/00-toolchain.log`: `kompile`, `krun`, `kprove`, and `kast` are K
v7.1.293.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks for all whitespace-separated words, in source order,
whose characters contain exactly natural number `n` consonants; the input
contains only letters and spaces, and empty input returns an empty list. The
canonical implementation counts each Python character whose lowercase form is
not in the ASCII vowel set. The candidate implements the same algorithm with
nested list comprehensions.

The exact regeneration command was:

```sh
cd /tmp/audit-work/fresh
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
cmp solution.mpy regenerated-solution.mpy
```

Both translated files have SHA-256
`871478db9cc95201ae736b7927051df9bb1bd36087181e043189bb57bbad0482`;
`cmp` exited 0.

The independent differential script imports the trusted canonical module and
the submitted module separately. It covers the five examples, empty input,
zero/positive `n`, only spaces, leading/trailing/repeated spaces, vowel and
consonant branches, filter boundaries, long words, all 19,531 strings of
length 0 through 6 over `aAbB ` for `n = 0..7`, 5,000 seeded ASCII cases, and
1,000 seeded Unicode-letter cases. It ran 162,272 comparisons with zero
mismatches.

Evidence: `evidence/02-differential.py`,
`evidence/02-program-check.sh`, and
`evidence/02-program-check-final.log` (exit 0). The Python implementation
matches the canonical implementation; the later discrepancy is in K, not in
`solution.py`.

## 3. Clean proof reconstruction

Only the source artifacts were copied to `/tmp/audit-work/fresh`. Candidate
`semantic-kompiled/`, `verification-kompiled/`, bytecode, and caches were not
copied or reused.

The concrete definition was rebuilt with:

```sh
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
```

Nine normal and boundary `krun` executions exited 0 and reached `.K` with the
same results as both Python implementations: a normal prompt case, both empty
input branches, only spaces, repeated-space/vowel/consonant branches, uppercase
vowels, include/exclude filtering, and order preservation. This establishes
only those concrete cases.

The proof definition was independently rebuilt with:

```sh
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The build exited 0. `spec.k` contains seven claims; the whole-file `kprove`
exited 0 and printed `#Top`. A reviewer script then mechanically isolated each
unchanged claim into a one-claim module. All seven individual `kprove`
commands exited 0 and printed `#Top`.

Evidence:

- `evidence/03a-build-concrete.sh` and
  `evidence/03a-build-concrete.log` (exit 0);
- `evidence/03-concrete-compare.py` (nine cases, zero failures);
- `evidence/03b-build-proof-and-prove.sh` and its log (exit 0, `#Top`);
- `evidence/03c-prove-each-claim.py` and its log (seven exit-0 `#Top`
  results).

The dynamic reconstruction gate succeeds as a statement about the candidate
theory. It does not establish that the theory is a sound Python semantics.

## 4. Adequacy and real-program pinning

The universal entry claim's precondition is: an arbitrary K `String S`, an
integer `N >= 0`, the exact submitted module in `<k>`, and `noResult` initially.
Its postcondition is `.K` with
`result = selectWordsSpec(S,N)`. The alphabet restriction is only mentioned in
a comment; it is not formalized. This is a result-constraining equality, not a
free variable or one-way implication.

The other six claims use the exact same program term and fixed initial
inputs/results: the five prompt examples and empty input. They are regression
claims, not helpers or loop invariants.

Program identity was checked at constructor level. `kast --output json` parsed
the submitted `solution.mpy` and the first claim's extracted LHS `Module` term.
After only syntax-level normalization of explicit versus omitted empty list
units, both canonical JSON terms have SHA-256
`56d987077eed0ab869d355a2249ec0c7232fcc1cff68d50235a16580974957c5`,
and compare equal. Thus the theorem executes the submitted function binding and
body rather than a substituted source program.

A satisfying state is `S = "Mary had a little lamb", N = 4`; both Python
implementations and fresh `krun` produce `["little"]`. The empty and branch
states in Stage 3 provide additional satisfying instances.

The body-sensitivity mutation changes the `Str("aeiou")` inside the program
term actually executed by the claim to `Str("aeio")`, leaving the original
postcondition unchanged. At `S = "u", N = 0`, the original program returns
`["u"]` and the changed body returns `[]`. `kprove` exits 1 with
`WarnStuckClaimState` at the changed `eval(ListComp(...Str("aeio")...))`.
This confirms syntactic pinning, while also showing that the semantics knows
only the exact original expression pattern.

Evidence: `evidence/04-pinning-check.py`,
`evidence/04-pinning-and-body-sensitivity.sh`, and the corrected
`evidence/04-pinning-and-body-sensitivity-rerun.log` (wrapper exit 0; mutation
`kprove` exit 1 for the expected residual). The earlier log preserves an
initial standalone-parser spelling issue before normalization; it is not a
candidate failure.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is `evidence/05-rule-inventory.md`. It enumerates all
15 local declaration groups, all 20 rules in `semantic.k`, the one rule in
`verification.k`, the configuration, every used constructor mapping, and all
seven claims. There are six `[function]` declarations and no local `total`,
`functional`, `simplification`, `owise`, priority, macro, alias, context, or
opaque declarations. There are no helper K files.

The loader, docstring, return, finish, word scanning, append, and filter rules
have disjoint patterns or complementary guards on their stated K domains.
Recursion structurally reduces a string/list for the tested ASCII inputs.
There are no conflicting overlaps or priority preemptions. The pure program
needs no heap, I/O, allocation, or exception cell on its source-contract
inputs.

Two material failures remain.

### 5.1 Exact-expression bridge and circular result summary

`semantic.k:102-121` is the only operational rule for every material
expression constructor in the body. It matches this task's exact outer and
inner `ListComp`, calls to `split`, `len`, and `lower`, comparisons, names, and
filters, then rewrites the whole expression directly to:

```text
pyList(filterWords(words(S), N))
```

`verification.k:12-13` defines `selectWordsSpec(S,N)` to exactly that same
term. The proof therefore connects execution to the postcondition by using an
identical summary on both sides. There is no generic execution of `Call`,
`Attribute`, `ListComp`, `Compare`, variable binding, or character iteration,
and no bridge-free universal connection claim establishing that the submitted
body computes this summary.

The reviewer removed only this rule, freshly compiled the rest, and ran the
real submitted `solution.mpy`. Execution stopped at the full
`eval(ListComp(...), "Mary had a little lamb", 4) ~> finish` term with
`noResult`. This is direct evidence that the bridge preempts all
property-bearing source execution rather than summarizes a result reached by
fixed component semantics.

Under the Kit extension contract this is an illegitimate result-bearing
operational bridge and task-answer encoding. Finite differential tests cannot
supply the missing universal connection theorem.

### 5.2 Concrete false conclusion on the intended domain

The source says letters and spaces, not ASCII letters. Python strings and the
canonical loop iterate Unicode characters. `"é"` is a letter and therefore a
valid source input.

Concrete witness:

```text
s = "é"
n = 1
trusted canonical result = ["é"]
submitted solution result = ["é"]
fresh generated-K result = []
```

At `n = 2`, both Python implementations return `[]`, while the fresh K
semantics returns a one-element list containing `"é"`. The generated
`countConsonants` recursion is operating over two UTF-8 units exposed by this
K string representation, not the one Python character. Consequently the exact
AST bridge together with `semantic.k:163-174` enables a false conclusion for a
satisfying input in the intended domain.

This is a material domain narrowing that is not stated in the claim or source
contract. Per the benchmark decision boundary it is `FAIL / NOT_LEGIT`, not a
non-fatal limitation. An additional `s = "a\tb", n = 1` probe shows that the
bridge's unguarded all-`String` match domain is also false outside the
letters/spaces source domain, but the verdict does not rely on that off-domain
witness.

Evidence: `evidence/05-static-probes.py`,
`evidence/05-static-probes.sh`, and
`evidence/05-static-probes-final2.log` (wrapper exit 0 with all expected
residual/divergence assertions true). The initial discovery logs are retained
and superseded by the final probe.

## 6. Fresh non-vacuity test

The reviewer-created mutation uses the exact program term and concrete,
realizable input `s = "b", n = 1`, for which both Python implementations return
`["b"]`. It deliberately changes the required result to the empty list.

Exact proof command:

```sh
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

The mutation parses and builds, then `kprove` exits 1 with
`WarnStuckClaimState`. Its residual is a completed `.K` configuration with
`result = pyList(WCons("b",.Words))`, directly exposing the unmet mutated
result obligation. This is valid non-vacuity evidence: the original proof does
constrain its result.

Evidence: `evidence/06-spec-vacuity-audit.k`,
`evidence/06-run-vacuity.py`, and `evidence/06-vacuity.log`. The audit wrapper
exits 0 because the internal proof's exit 1 and residual are exactly expected.
Non-vacuity does not repair the semantic-fidelity failures in Stage 5.

## 7. Proven versus assumed accounting

What the successful K proof actually establishes is precise but circular:
under the candidate rewrite theory, the exact submitted AST, for any K string
and `N >= 0`, rewrites through the whole-expression `eval` rule to
`pyList(filterWords(words(S),N))`; the proof-local `selectWordsSpec` rewrites
to the same term. It also establishes the six fixed regression outcomes under
that theory.

Trust and assumption ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, rewrite engine, `BOOL`, `INT`, and `STRING` built-ins | All builds and claims | Ordinary low-level trusted primitive boundary. The concrete Unicode run reveals how the chosen string primitives differ from Python character iteration. |
| Trusted `py2mpy.py` translation | Program identity | Acceptable and mechanically checked by byte equality plus constructor-level KAST equality. |
| Whole-expression `eval` rule at `semantic.k:102-121` | Universal claim and all regressions | Illegitimate program-derived operational bridge. It has no bridge-free theorem and supplies the exact result term used by the postcondition. |
| `words`, `countConsonants`, `filterWords` recurrences | Bridge result and `selectWordsSpec` | Transparent rather than opaque, and plausible for ASCII samples, but materially false as a Python-character model on the `"é"` witness. |
| `selectWordsSpec` equation | Universal postcondition | Definitional, but circular with the execution bridge and inherits its false Unicode behavior. |
| Differential testing | Python candidate/canonical bridge only | Strong finite evidence (162,272 cases), not a universal K/Python connection theorem. It confirms that the semantic counterexample is not a candidate-Python bug. |
| Partial-correctness termination premise | Universal theorem | Normal for reachability partial correctness; not the source of failure. |

There are no fresh opaque symbols, unconstrained result variables, helper
lemmas, loop circularities, or empirical external calls. Gate A fails because
the result-bearing bridge is not independently justified and has an
in-domain false witness. Gate B also fails because the semantics materially
narrows/mis-models the stated letters domain. Gate C evidence is reproducible
apart from the documented aggregate-hash encoding anomaly, but later-gate
auditability cannot rescue Gates A or B.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
