# Independent adversarial review: 111-histogram

This review treats all candidate files and generation records as untrusted
evidence. All executable artifacts were copied to `/tmp/audit-work/fresh`; no
candidate-provided compiled definition or cache was used. Reviewer-authored
sources and bounded logs are in `/audit-output/evidence/`, with an exact command
index in `/audit-output/evidence/COMMANDS.md`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`.

The following required objects are real (non-symlink) readable files or
directories: `/audit-input.json`, `/audit-campaign-lock.json`, `/candidate`,
`/reference/canonical.py`, `/reference/prompt.py`, `/reference/py2mpy.py`,
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and
`/generation-evidence/codex-trace/`. `usage.json` is present and was also
inspected. Runtime metrics are not required for this historical layout.

The campaign lock is byte-hash-identical to the hash in `audit-input.json` and
its JSON object exactly equals the `audit_campaign` object. Every recorded
regular-file SHA-256 checked by the reviewer matches, including the trusted and
candidate prompt and translator, the canonical program, all three manifests,
the generation result, invocation/metrics/usage records, prompt, last message,
and complete Codex output. Candidate `prompt.py` and `py2mpy.py` are byte
identical to their trusted mounts.

The independent pipeline tree digest of `/candidate` is
`e334660928b723c8142b1c5e422a9894f5f0cd5174c7102674de83e887e89856`,
matching the generation result's workspace digest. The corresponding trace
digest is
`181d933c067e5e039a8e16e863ee4cca20c2a490adb366dd68ab219e664fe813`,
matching `usage.json`. The launcher also records its own tree hashes
(`a235...` and `c324...`); its distinct tree-hash encoding is not declared in
the manifest, so those values were recorded rather than incorrectly compared
to a different encoding. All individual declared file hashes match, and the
tree walks reject symlinks or unsupported nodes.

The complete 2,142,709-byte, 50,381-line generation output was read. All 395
JSONL trace records parse; event counts and hashes are in
`evidence/01b-integrity.log`. Generation claims such as prior `#Top` markers
were not used as proof evidence.

There is no `/reference/reference-semantics`, as required in
`GENERATED_SEMANTICS` mode. No infrastructure breach was found. The candidate
contains all required proof sources as regular files. See
`evidence/integrity_check.py` and `evidence/01b-integrity.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for `histogram(test)`: for a string representing
space-separated lowercase letters, return a dictionary containing every letter
with maximum frequency, mapped to that frequency; include all ties; return
`{}` for the empty string. The trusted canonical implements that contract using
`test.split(" ")`, repeated `count`, and a maximum.

The submitted Python uses `test.split()`, a count dictionary, a running maximum,
and a second pass selecting all entries equal to the maximum. On the ordinary
contract grammar (empty, or lowercase letters separated by single ASCII
spaces), it implements the requested algorithm.

### Translation and constructor identity

Running the trusted `/reference/py2mpy.py` on the scratch `solution.py` produces
1,071 bytes byte-identical to submitted `solution.mpy`.

The `histogramProgram()` term in `verification.k` is mechanically identical to
that regenerated constructor after exactly the generated K-list identity
normalizations:

- omitted empty call arguments to `.Exprs`;
- empty dictionaries to `.Entries`;
- omitted empty `if` branches to `.Stmts`.

No executable node, binding, operator, statement, or control edge differs.
See `evidence/constructor_compare.py` and
`evidence/02c-constructor-compare.log`. Earlier `02`/`02b` and `09` logs are
reviewer parser/extraction attempts superseded by the successful constructor
comparison; they are not candidate failures.

### Differential testing

The independent test imports the trusted canonical and submitted Python
directly. It covers all five examples, empty input, every count/maximum/select
branch boundary, all token sequences of length at most six over `a,b,c`,
leading/trailing/repeated-space representation probes, and 500 seeded generated
cases. Among 1,626 unique cases:

- zero mismatches occur on the explicit empty-or-single-space lowercase-letter
  grammar;
- eleven mismatches occur on representation-boundary strings with repeated or
  edge spaces.

For example, trusted canonical returns `{"": 1, "a": 1}` on `" a"`, while the
submitted implementation returns `{"a": 1}`. This is outside the strict
single-space letter grammar but means a broader reading of “space separated”
would expose an implementation/reference discrepancy. The mismatch remains
visible in `evidence/03b-differential.log`; it is not the primary verdict basis.

## 3. Clean proof reconstruction

Tool versions were independently observed as K/`kprove` 7.1.293 and Python
3.10.12.

Fresh builds:

- LLVM `semantic.k`: exit 0.
- Haskell `verification.k` without loop lemmas: exit 0.
- Haskell `lemmas.k` with the loop equations: exit 0.

The LLVM build reports non-exhaustive `[total]` definitions for `envGet` and
`execFor`; those warnings are assessed in Stage 5.

Fresh concrete execution was compared with both Python implementations for:
empty input, a singleton, repeated and fresh count keys, maximum raise/keep,
single winner, tied winner, and whitespace boundaries. The generated K
semantics agrees with submitted Python for the ASCII-space cases tested.
Commands and results are in `evidence/04-kompile-semantic-llvm.log` and
`evidence/05-concrete-runs.log`.

Every one of the 15 positive claims was then run separately by fully qualified
label. Every command exited 0 and printed `#Top`:

- count claims: `count-empty`, `count-existing-raises-step`,
  `count-fresh-step`, `count-existing-keeps-step`,
  `count-fresh-keeps-step`;
- selection claims: `select-empty`, `select-equal-step`,
  `select-unequal-step`;
- examples: `example-all-once`, `example-tied-two`,
  `example-filter-one`, `example-single-winner`, `example-empty`;
- entries: `all-token-lists`, `all-space-separated-strings`.

The build logs are `evidence/06-kompile-verification.log` and
`evidence/07-kompile-lemmas.log`. `evidence/run_all_claims.sh`,
`evidence/08-all-claims-summary.log`, and the per-claim logs preserve each exact
command, output, and status.

Thus the dynamic reconstruction gate succeeds as a statement about the
candidate's extended K theory. It does not validate that theory.

## 4. Adequacy and real-program pinning

### Claim meanings and satisfiable preconditions

Neither entry claim has a `requires` clause.

- `all-token-lists` says that, for every K `List` of arbitrary `PyVal` tokens,
  executing the exact histogram body with `test = pyWords(WORDS)` returns
  `histogramSpec(WORDS)`.
- `all-space-separated-strings` says that, for every K `String`, executing the
  exact histogram body with `test = pyString(INPUT)` returns
  `histogramSpecString(INPUT)`.

Both preconditions are satisfiable. `WORDS = .List` and `INPUT = ""` execute to
`pyDict(.Map,.List)`. For `INPUT = "a b b"`, the formal summary, fixed K
execution, trusted canonical, and submitted Python all give `{"b": 2}`.

All helper guards are also realizable: fresh/raise uses an empty count map and
maximum 0; fresh/keep uses maximum 1; existing/raise uses count 1 and maximum 1;
existing/keep uses count 1 and maximum 2; equal selection uses value/maximum 1;
unequal selection uses value 1 and maximum 2. Empty-loop claims accept any
environment.

The five examples constrain exact returned dictionaries. The two entries do
not return a free variable: their right sides are fully defined functions. The
constructor comparison proves that the left side uses the submitted binding and
body, rather than a substituted program.

### Body sensitivity

The reviewer changed the `maximum` initialization inside the constructor
actually returned by `histogramProgram()` from 0 to 2, leaving the summary at
0. The mutated theory compiled, but the main all-string proof exited 1 with a
residual explicitly comparing the two initial states. This is a genuine
executed-body sensitivity check, preserved in
`evidence/body-mutation-verification.k` and
`evidence/12-body-sensitivity.log`.

### Adequacy defects

First, the literal formal domain is all K strings, but the semantic rule used
for Python's zero-argument `str.split()` only splits ASCII space. The real
submitted Python uses all Python whitespace. Concrete witness:

```text
input: "a\tb a"
submitted Python: {"a": 2}
generated K execution: {"a\tb": 1, "a": 1}
```

This input is outside the narrow single-ASCII-space lowercase-letter grammar,
but it is inside the entry claim's unguarded `INPUT:String` domain. Therefore
the all-string claim cannot be interpreted as a theorem about the real
submitted Python over its stated formal precondition. See
`evidence/16-whitespace-model-probe.log`.

Second, the postcondition is an execution-shaped duplicate:
`histogramSpecString` splits, runs `countLoop`, and runs `selectLoop`. There is
no formal statement that its result contains exactly all and only maximum-
frequency input letters. That intent bridge is plausible by ordinary induction
and well supported by finite tests, but it is informal; equality to a
candidate-authored duplicate algorithm is not itself the requested
human-facing histogram property.

## 5. Rule-by-rule static soundness review

`evidence/10-rule-inventory.log` is the machine-generated line inventory.
There are no local priority rules, `[concrete]` rules, opaque symbols,
`[functional]` declarations, or proof simplifications beyond the four map
lookup simplifications identified below.

### Syntax and configuration inventory

`semantic.k:9-33` declares all local source constructors:
`Program/Module`; list-valued `Stmts`; `FuncDef`, `Assign`, `For`, `If`,
`Return`; `Params`; list-valued `Exprs` and `Entries`; `Entry`; `CmpOp`; and
`Name`, `Int`, `Str`, `DictExpr`, `Attribute`, `Call`, `Subscript`, `BinOp`,
`Compare`. Submitted `solution.mpy` uses every statement constructor and uses
`Name`, `Int`, empty `DictExpr`, `Attribute` inside `Call`, `Subscript`,
`BinOp("+")`, and comparisons `in`, `>`, `==`. `Str`, nonempty `Entry`, and
standalone `Attribute` are unused.

`semantic.k:41-52` declares the six runtime values (`pyInt`, `pyString`,
`pyWords`, `pyList`, ordered `pyDict`, `pyBool`), two `ExecResult` forms, and
the `execute`/`executeWords` K items. `semantic.k:54` has one `<k>` cell.
Local environments and dictionaries are explicit immutable K maps threaded
through functions, so the submitted program needs no separate heap, stack,
I/O, or exception cell.

All of these declarations are recognizable constructor representations of the
translated source. Minimal syntax for unused Python constructs is not required
in generated-semantics mode.

### `semantic.k` function and rule inventory

All functions below are declared `[function,total]`.

| Lines | Complete local rule group | Assessment |
|---|---|---|
| 58-66 | two entry rules; two `resultOf` rules | The exact histogram binding/body is selected and the local state is passed explicitly. Returning a value is correct. `normal(_) => pyBool(false)` is not Python's fall-through `None`, but the submitted body always reaches `Return`; this fallback is unused on the contract domain. |
| 70-84 | four `splitWords`; three `splitValue` | The four guards exhaust ASCII-space splitting and correctly skip empty fields. `pyWords` is a verification harness. The owise non-string fallback is unused. Material defect: zero-argument Python `split()` recognizes non-ASCII-space whitespace, while these unguarded rules do not. The tab witness above is a concrete false real-program conclusion over the formal all-string domain. |
| 87-100 | nine `eval` rules | Literal/name/empty-dict/call/subscript/add/compare behavior matches every expression used. Used expressions are side-effect free, so nested functional reduction does not change Python evaluation effects. The owise `false` fabricates a value for unsupported expressions, but no submitted expression reaches it. |
| 102-106 | three `envGet`, first two `[simplification]` | Map-update lookup and shadow skipping are valid and the overlap agrees. The declaration is not exhaustive for an absent key, as the compiler warns. All names used by the submitted body are bound before lookup; no wrong result is fixed on the unmatched domain, so this is an evidence/totality gap rather than a witnessed false rule on intended states. |
| 108-114 | four `dictGet`, first two `[simplification]` | Update lookup and unequal-key stripping are valid; overlaps agree. Missing/non-dictionary lookup returns false rather than raising `KeyError`, but all submitted subscript reads are protected by membership or iterate existing keys. |
| 116-129 | two `addValues`, four `compareValues`, three `truth` | Integer addition, integer `>`, dictionary membership, equality of the integer values used, and Boolean truth are correct. Owise fallbacks do not model Python type errors/truthiness, but are unused by submitted valid executions. |
| 133-151 | three `assign`, three `dictSet`, three `iterable` | Name/subscript assignment, persistent dictionary update, insertion-order key tracking, list iteration, and dictionary-key iteration match the program. The target/key/value expressions used have no side effects. Owise no-op/empty behavior is outside used forms. |
| 155-189 | `exec` (2), `execNext` (2), `execStmt` (5), `execIf` (2), `execFor` (2), `execForNext` (2) | State is threaded in source order; returns stop later statements; guards partition Bool; for-loops assign each element and propagate returns. The actual loops do not mutate the iterated collection. The `execStmt` owise case would silently ignore unsupported statements but is not used. `execFor` receives a non-exhaustiveness warning for symbolic builtin-list shapes; concrete proper lists generated by split/dictionary keys execute. |

Numeric values are mathematical integers, compatible with Python integers for
this program. Ordered dictionary keys are modeled explicitly; equality in the
task depends on mapping contents, while the extra order component soundly
overconstrains the examples.

### `verification.k` inventory

There are 18 `[function,total]` declarations and 25 defining rules:

- `histogramProgram` (one rule) is the exact normalized submitted constructor.
- `nextCount` (three), `putCount` (one), `raiseMaximum` (two),
  `countIteration` (one), and `countLoop` (two) duplicate one count iteration
  and its list fold. The existing/fresh and raise/keep guards are exhaustive
  for reachable integer-valued count states; their overlaps agree.
- `selectIteration` (two) and `selectLoop` (two) duplicate the equality branch
  and selection fold; Boolean guards are disjoint and exhaustive.
- `dictKeys` (two) is a correct ordered-dictionary projection with an unused
  fallback.
- `initialEnvWith`, `initialEnv`, `afterCountWith`, `afterCount`,
  `beforeSelectWith`, and `beforeSelect` (one rule each) name the exact states
  after the corresponding submitted statements.
- `histogramSpecWith`, `histogramSpec`, and `histogramSpecString` (one rule
  each) compose those definitions into the duplicate algorithm.

These equations are deterministic, terminating on proper finite lists, and
ground tests agree with fixed execution. They do not independently formalize
the maximum-frequency property.

### `lemmas.k` operational bridges

The only two ordinary rules in `lemmas.k:10-29` rewrite the actual count and
selection `execFor` terms to `normal(countLoop(...))` and
`normal(selectLoop(...))`. They are operational bridges, not merely names:
they preempt all fixed-semantics loop execution inside the main theorem.

Their complete match domains admit arbitrary `WORDS:List`, arbitrary
`ENV:Map`, and any functional context in which the matching `execFor` appears.
They read all state through `ENV`, return a complete new environment, and have
no hidden-cell or abrupt-control effect. Ground fixed-versus-extended runs for
empty, singleton, raise/keep, winner, and tie cases are byte-identical, including
the real continuations after both loops (`evidence/15-bridge-ground-compare.log`).

But the claimed justification does not contain the match domain:

- the candidate proves an empty-list claim;
- its nonempty count claims cover only a singleton list and restricted
  existing/fresh integer count/maximum shapes;
- its nonempty selection claims cover only a singleton list and restricted
  count/result shapes;
- no candidate claim covers an arbitrary tail or the bridge's arbitrary
  environment/context.

The reviewer wrote exact bridge-free universal connection claims importing only
`VERIFICATION`. Both build but exit 1 at symbolic `execFor`
(`evidence/bridge-connection.k`,
`evidence/11-bridge-connection.log`). Removing the bridges from the exact main
claim likewise builds and then exits 1 at the first symbolic count loop
(`evidence/main-no-bridge.k`, `evidence/14-main-no-bridge.log`).

I did not find a ground counterexample to the two equations on reachable
contract states, and therefore do **not** label the equations mathematically
false. The narrower, decisive finding is that the candidate assumes as
ordinary rules the universal operational connections needed to prove the main
claim; singleton branch checks plus an informal structural-induction argument
are not the bridge-free universal machine theorem required by Kit Gate A.

### `spec.k` claim inventory

All 15 claims are listed in Stage 3. The five count and three selection claims
are genuine fixed-semantics empty/singleton checks. The five examples genuinely
execute the exact program under the bridge-free definition. The two universal
entries are result-constraining and body-sensitive, but their closure depends
on the two unsupported operational bridges.

## 6. Fresh non-vacuity test

The reviewer created a new spec claiming that input `"a"` returns
`{"a": 2}`. Both trusted canonical and submitted Python return `{"a": 1}`.

The mutation's `kprove --dry-run` exits 0, proving that it parses and builds
against the fresh fixed definition. The actual proof exits 1 with
`WarnStuckClaimState`; the residual is the fully executed dictionary containing
`pyInt(1)`, which does not unify with mutated `pyInt(2)`. This is the expected
unmet result obligation, not a parser error, crash, timeout, or unreachable
mutation. See `evidence/spec-vacuity-audit.k` and
`evidence/13-non-vacuity.log`.

Non-vacuity therefore passes. It does not repair the semantic and operational-
bridge defects.

## 7. Proven versus assumed accounting

### What the successful K runs actually prove

Under the extended theory consisting of `semantic.k`, the 25 duplicate-summary
equations in `verification.k`, and the two `execFor` equations in `lemmas.k`,
K proves:

1. the exact translated constructor returns the five stated example
   dictionaries;
2. every fixed empty/singleton branch claim has the stated transition;
3. for arbitrary K token lists and K strings, the extended interpreter's return
   equals its candidate-authored `histogramSpec` duplicate.

The result is constrained, non-vacuous, and sensitive to the embedded program
body. It is not a bridge-free proof of the arbitrary loops, nor a formal theorem
of the natural-language maximum-frequency predicate.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| Trusted translator and constructor grammar | Program identity | Acceptable; byte regeneration and constructor comparison pass. |
| K `INT`, `STRING`, `BOOL`, `MAP`, `LIST`, map update/key membership, substring/find/length primitives | All semantics/proofs | Ordinary low-level K trust boundary; accepted for this audit. |
| Generated big-step interpreter | Every claim | Mostly faithful on used contract constructs, but its unguarded zero-argument split model is false for actual Python whitespace; tab witness recorded. Fatal to the literal all-string real-program reading. |
| `envGet`/`execFor` totality outside covered patterns and owise false/no-op fallbacks | Symbolic execution | Unmatched/unsupported cases are not reached by strict valid-input executions. They are documented evidence limitations, not used as independent verdict bases. |
| `countLoop`/`selectLoop` definitions | Universal postcondition | Truthful executable summaries on tested proper lists; their connection to the human maximum-frequency property remains informal/empirical. |
| Two `lemmas.k` loop equations | Both universal entry claims | Fatal proof assumption. They replace program-defined loops over a domain broader than the candidate's fixed-semantics claims, and no bridge-free universal connection theorem closes. |
| Differential and ground bridge tests | Python/K and summary bridges | Reproducible finite support only: 1,626 Python cases, concrete K boundaries, and fixed/extended ground comparisons. They cannot establish the missing universal theorem. |

### Gate assessment and decision

- Kit Gate A (real-program soundness): **FAIL**. The main theorem is dependent
  on two unsupported operational bridges, and the generated split model has a
  concrete mismatch with the real submitted program over the entry claim's
  unguarded all-string domain.
- Intent adequacy: limited. The strict single-space lowercase-letter source
  grammar is empirically covered, but the formal postcondition is a duplicate
  algorithm rather than an independently stated maximum-frequency property.
  A broader space-representation reading also exposes the preserved canonical
  discrepancies.
- Trust/evidence auditability: the reconstructed commands, finite evidence,
  body mutation, and non-vacuity mutation are reproducible, but they do not
  discharge Gate A.

Fresh `#Top` results are therefore real closure results only under an extended
theory that assumes the core universal loop connections. Under the mandated
Kit validation boundary this is not a legitimate partial-correctness proof of
the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
