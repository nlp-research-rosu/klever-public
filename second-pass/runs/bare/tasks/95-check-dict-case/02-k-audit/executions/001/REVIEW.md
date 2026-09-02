# Independent adversarial audit: 95-check-dict-case

The candidate is not a legitimate partial-correctness proof of the task over
its intended input domain. A clean reconstruction does prove 11 concrete test
instances, and those instances are non-vacuous and pinned to the submitted
translation. It does not prove a symbolic correctness claim for arbitrary
dictionaries. In addition, the generated semantics gives observably false
results for valid dictionaries whose keys are non-ASCII cased strings.

All candidate material was treated as untrusted. Candidate-built definitions
were not used. Source copies, fresh definitions, and experiments are under
`/tmp/audit-work/candidate-src`; reviewer-authored artifacts and bounded logs
are under `/audit-output/evidence`.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference` contains exactly the
three trusted regular files `canonical.py`, `prompt.py`, and `py2mpy.py`;
`/reference/reference-semantics` is absent. This is the required mount state,
so there is no infrastructure breach and a candidate verdict is appropriate.
See `evidence/01-provenance.log`.

The candidate prompt and translator are byte-identical to their trusted
counterparts:

- `prompt.py`: SHA-256
  `e8a971e0e8838d69639de6628a8eff45638ce938c172670b7274c41d63207631`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

Both `cmp` operations exited 0. No candidate symlinks were found. The required
regular files `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `program.k`, `verification.k`, `spec.k`, and `prove.sh` are
present with the correct types. The structured trace is present below the
regular directory `codex-trace/`. There are no missing, changed, mistyped, or
symlinked required artifacts.

The candidate has one extra derived tree, `verification-kompiled/`. It is
candidate-built output, not a source-integrity failure, and was ignored
entirely. No candidate cache or compiled definition was copied into scratch.

### Untrusted generation claims

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
structured trace were read only as claims. They say that generation exited 0,
that the submitted positive proof printed `#Top`, and that the K model is
ASCII-only while the Python implementation uses CPython's Unicode predicates.
Bounded excerpts are in `evidence/01-generation-claims.log`.

The trace also records that generation tried a symbolic claim over
`KEYS:Values`; it became stuck with two unexplored branches and was then
deleted. The submitted `spec.k` contains only the ground claims. This history
is not proof evidence, but it is consistent with the independent scope audit
below. The exact untrusted excerpts are preserved in
`evidence/01-discarded-universal-trace.log`.

**Stage 1 result:** integrity passes; no infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The prompt requires `check_dict_case(d)` to return false for an empty
dictionary. For a nonempty dictionary it returns true exactly when every key
is a string and either every key satisfies Python's lowercase predicate or
every key satisfies Python's uppercase predicate. Dictionary values are
irrelevant.

The submitted `solution.py` implements that reading with two flags. It rejects
the empty dictionary and any non-string key, clears `lower` or `upper` when a
key fails the corresponding predicate, and returns `lower or upper`.

The trusted `canonical.py` intends a state-machine implementation, but its
control flow contains an `else: break` after a subsequent key agrees with the
current case. It can therefore ignore later keys. For example:

- keys `['a', 'b', 'C']`: submitted solution and prompt oracle return false;
  trusted canonical returns true;
- keys `['a', 'b', 8]`: submitted solution and prompt oracle return false;
  trusted canonical returns true.

This is a material candidate-versus-canonical divergence on the stated domain.
Inspection attributes it to the canonical implementation's early break, not
to the submitted implementation: the latter agrees with the natural-language
contract on these witnesses. The candidate nevertheless supplies no formal
theorem resolving the trusted-canonical versus prompt discrepancy.

### Trusted translation

The trusted `/reference/py2mpy.py` was copied to scratch and run on the copied
`solution.py`. The regenerated `solution.regenerated.mpy` is byte-identical to
the submitted `solution.mpy`; both have SHA-256
`1511fb2791f88d583217b4e0b2ac56aaef3db6543477e048dab3f42e4a36ad92`.
The command and exit-0 result are in `evidence/02-regenerate.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the submitted entry point from explicit scratch paths. Its
oracle is a separate direct reading of the prompt using `all`, `islower`, and
`isupper`. It covers:

- all 5 documented examples;
- 17 explicit boundary cases, including empty, one-key, non-string positions,
  mixed-case boundaries, uncased strings, punctuation/digits, and Unicode;
- 5,861 distinct normalized dictionaries induced by all key sequences of
  length 0 through 4 over a ten-element mixed key pool.

The exit-0 run in `evidence/02-differential.log` reports 5,883 total records,
zero submitted-solution versus prompt-oracle mismatches, and 758 canonical
versus submitted/prompt mismatches. This is finite evidence for the
implementation-to-prompt bridge, not a universal proof.

**Stage 2 result:** translation fidelity passes and `solution.py` has strong
finite support for the prompt; the material canonical divergence is
documented.

## 3. Clean proof reconstruction

K version v7.1.293 was used from `/usr/bin`; see
`evidence/03-toolchain.log`. Only copied source was used.

### Fresh builds

The concrete semantics-only definition was built with:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend haskell --output-definition concrete-kompiled
```

It exited 0 (`evidence/03-kompile-concrete.log`).

The proof definition was independently built with:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module VERIFICATION --backend haskell \
  --output-definition proof-kompiled
```

It exited 0 (`evidence/03-kompile-proof.log`).

The single submitted target command processes all 11 claims in `SPEC`:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

It exited 0 and printed exactly `#Top`
(`evidence/03-kprove-positive.log`). Thus the candidate's finite positive
claims do reconstruct successfully.

### Fresh concrete semantics comparison

`evidence/concrete_semantics_compare.py` executes the actual submitted
`solution.mpy` using the fresh semantics-only definition and compares each
result to both the submitted Python function and an independent prompt oracle.
The final exit-0 run covers 13 normal and boundary inputs
(`evidence/03-concrete-compare-rerun.log`).

All ASCII cases agree, including empty, all-lower, all-upper, mixed case,
non-string at the first and last positions, title case, uncased digits, and
punctuated lowercase. Two valid Unicode cases disagree:

- `DictVal(StrVal("é") StrVal("ß"))`: K false, Python/oracle true;
- `DictVal(StrVal("É") StrVal("İ"))`: K false, Python/oracle true.

The earlier `evidence/03-concrete-compare.log` is a preserved reviewer-harness
failure: `krun` succeeded, but an over-escaped regular expression did not parse
its output. The corrected rerun is the result used here; the initial harness
bug is neither candidate failure nor audit infrastructure uncertainty.

**Stage 3 result:** fresh builds and all submitted positive claims pass, but
fresh concrete execution exposes a real semantics mismatch on the intended
domain.

## 4. Adequacy and real-program pinning

### Exact meaning of the entry claims

Every claim has the same configuration shape. Its precondition is a concrete
state with `<k> solutionProgram </k>`, one exact ground `DictVal` in `<input>`,
an empty local environment, and `NoneVal` in `<result>`. Its postcondition
requires the computation to finish at `.K`, the environment to be empty, and
the result to become `BoolVal(contract(the same exact input))`. There are no
symbolic keys or precondition constraints.

The 11 claims and their ground postcondition values are:

| Claim / source start | Exact key sequence | Required result |
|---|---|---|
| 1, `spec.k:11` | `[]` | false |
| 2, `spec.k:19` | `['a','b']` | true |
| 3, `spec.k:27` | `['a','A','B']` | false |
| 4, `spec.k:35` | `['a',8]` | false |
| 5, `spec.k:43` | `['Name','Age','City']` | false |
| 6, `spec.k:51` | `['STATE','ZIP']` | true |
| 7, `spec.k:59` | `['abc-123','z9']` | true |
| 8, `spec.k:67` | `['ABC-123','Z9']` | true |
| 9, `spec.k:75` | `['123']` | false |
| 10, `spec.k:83` | `['aA']` | false |
| 11, `spec.k:91` | `[True]` | false |

`evidence/claim_witnesses.py` constructs a satisfying initial state for every
entry precondition and substitutes its concrete result. The exit-0 output in
`evidence/04-claim-witnesses.log` shows that both Python implementations and
the prompt oracle agree on all 11 submitted inputs. Each postcondition reduces
to a ground Boolean; none contains a free result variable or one-way
implication.

### Real-program identity

The claims execute `solutionProgram`, a function constant in `program.k`, not
the `.mpy` file directly. The reviewer independently regenerated the wrapper
from the trusted regenerated `.mpy`. The submitted and regenerated `program.k`
files are byte-identical with SHA-256
`4bf27e038facd75321517640c19d46d05a9334081b521bea17eabeb35894943e`;
see `evidence/04-program-pinning.log`. The constant expands to the complete
submitted AST, which is then executed by the operational rules. There is no
substituted program.

There are no helper claims, loop claims, invariants, or circularities. Each
ground loop is simply unrolled.

### Material adequacy failure

The comments at `spec.k:6-9` call six concrete examples “aggregate partitions”
and “exhaustive.” They are not partitions: every input is ground. The file
proves only 11 individual executions and says nothing about any other
dictionary. In particular, it has no theorem over an arbitrary `Values` list,
no loop invariant, and no connection theorem generalizing the examples.

The reviewer-authored symbolic scope probe in
`evidence/spec-universal-audit.k` states the natural modeled generalization
over `KEYS:Values`. With the fresh proof definition it exits 1 with
`WarnStuckClaimState` and two unexplored branches
(`evidence/04-universal-scope-probe.log`). This failure is not used to claim
that the desired theorem is false; it confirms that the submitted source does
not contain the invariant or proof needed to establish it.

The modeled `Value` sort also omits many valid hashable Python key types
(floats, tuples, and user objects). Because all such non-string keys should
produce false, a sound abstraction could cover them, but this candidate does
not provide one. Conversely, it admits `DictVal` as a key even though Python
dictionaries are unhashable. This is a domain-coverage gap; no false-rule
label is based on it.

**Stage 4 result:** each finite claim is pinned and result-constraining, but the
claimed task-wide proof is absent. This alone is a legitimacy failure.

## 5. Rule-by-rule static soundness review

The complete numbered sources, declaration/rule search, counts, and
priority/simplification scan are in `evidence/05-source-inventory.log`.
Candidate-local totals are 47 rules in `semantic.k`, 1 rule in `program.k`, 20
rules in `verification.k`, and 11 reachability claims in `spec.k`.

### Declaration and attribute inventory

- `semantic.k:12-32` declares `PyStmt`, `PyStmts`, `Params`, `Strings`,
  `PyExpr`, and `PyExprs`. The exact constructors are `Module`, `FuncDef`,
  `Assign`, two `If` forms, `For`, `Return`, `Name`, `Bool`, `UnaryOp`,
  `BoolOp`, two `Call` forms, and `Attribute`.
- `semantic.k:43-50` declares `Value` as `NoneVal`, `BoolVal`, `StrVal`,
  `IntVal`, and empty/nonempty `DictVal`, plus the nonempty `Values` list.
- `semantic.k:58-64` declares exactly four state cells: computation, immutable
  input, local environment, and result. There is no heap, allocation, I/O,
  exception, or call-stack cell because the target uses none.
- `semantic.k:75-84` declares the internal scheduling items `eval`,
  `assignTo`, `choose`, `chooseNoElse`, `startFor`, `loop`, `bind`,
  `logicalNot`, `logicalOr`, and `returnValue`.
- `semantic.k:143` declares total function `pyIsString`.
  `semantic.k:156-159` declares functions `pyIsLower`, `pyIsUpper`,
  `lowerScan`, and `upperScan`.
- `program.k:6` declares function `solutionProgram`.
- `verification.k:10-15` declares functions `contract`, `allStringKeys`,
  `allLowerKeys`, `allUpperKeys`, and total functions `lowerKey` and
  `upperKey`.
- The only symbol attributes are the disambiguating symbols `IfNoElse`,
  `CallNoArgs`, and `EmptyDictVal`. There are no candidate-local priority,
  `owise`, simplification, macro, anywhere, fresh, or opaque declarations.
  There are no local priority rules or simplification rules.

Every constructor used by `solution.mpy` is declared and mapped:

| Used construct | Operational coverage |
|---|---|
| `Module`/`FuncDef`/`Params` | exact entry rule at `semantic.k:67` |
| statement sequence | `semantic.k:73` |
| `Assign` | `semantic.k:87-89` |
| no-else `If` | `semantic.k:94-96` |
| `For` and dictionary iteration | `semantic.k:98-105` |
| `Return` | `semantic.k:107-110` |
| `Bool` and `Name` | `semantic.k:113-115` |
| unary `not` | `semantic.k:118-122` |
| two-operand Boolean `or` | `semantic.k:125-127` |
| exact `isinstance(..., str)` call | `semantic.k:132-134` |
| exact `Name.islower()` / `Name.isupper()` calls | `semantic.k:136-141` |

The declared full three-argument `If` form is unused but has ordinary Boolean
behavior at `semantic.k:91-93`. Missing behavior for other unused translator
constructs is permitted in generated-semantics mode.

### Exhaustive operational-rule decisions

The following inventory names every rule by its starting source line:

| Rule starts | Decision |
|---|---|
| `semantic.k:67` | Exact entry for the target name, parameter, empty frame, and input binding. Sound for this one-function module. |
| `semantic.k:73` | Schedules the head statement before the remaining list. Sound sequencing. |
| `semantic.k:87`, `:88` | Evaluate assignment RHS, then update exactly one map binding. Sound for the used name targets. |
| `semantic.k:91`, `:92`, `:93` | Evaluate a full-if Boolean guard, then select exactly one branch. Sound but unused. |
| `semantic.k:94`, `:95`, `:96` | Evaluate the used no-else guard, schedule the body only on true. Sound. |
| `semantic.k:98`, `:99`, `:100` | Evaluate the iterator; empty dictionaries do zero iterations and nonempty dictionaries start a loop. Sound for `DictVal`. |
| `semantic.k:101`, `:103`, `:104` | Bind keys in order, execute a complete body before recurring, and handle the singleton tail. Sound; multi/singleton patterns are disjoint. |
| `semantic.k:107`, `:108` | Evaluate the return expression, discard the remaining function continuation, restore the initially empty outer environment, and set the result. Sound for this top-level call; there is no nested-frame claim. |
| `semantic.k:113`, `:114` | Boolean literal construction and exact environment lookup. Sound. |
| `semantic.k:118`, `:119`, `:120`, `:121`, `:122` | Left-to-right `not`, Boolean negation, and empty/nonempty dictionary truthiness. The singleton and multi-element nonempty cases are disjoint and exhaustive for `Values`. Sound on used terms. |
| `semantic.k:125`, `:126`, `:127` | Evaluate the left operand and short-circuit true, otherwise evaluate the right operand. Python `or` can return non-Booleans generally, but both operands here are Boolean flags and the rules require `BoolVal`; sound for the exact target. |
| `semantic.k:132` | Models the exact unshadowed builtin call on a local name. It reads the environment and changes only `<k>`. Under standard Python builtins it is a sound target-specific primitive over the declared values. |
| `semantic.k:136`, `:139` | Model the exact pure zero-argument string methods on a local name, preserving state. Binding and context are exact for the target, but their result correctness depends on the scanners below. They are unsound for valid non-ASCII cased strings. |
| `semantic.k:144`, `:145`, `:146`, `:147`, `:148`, `:149` | The six `pyIsString` equations cover every declared `Value` constructor with disjoint patterns. Their `[total]` declaration is justified for that local sort. |
| `semantic.k:161`, `:162` | Start lower/upper scans at index 0 with no cased character seen. Structurally sound, but inherit scanner value errors. |
| `semantic.k:164`, `:166`, `:170`, `:174` | End, ASCII-uppercase rejection, ASCII-lowercase recognition, and “other” handling for the lower scan. Guards are disjoint on reachable nonnegative indices and recursion increments toward string length. The “other” equation is false as a model of Python for non-ASCII lowercase characters. |
| `semantic.k:181`, `:183`, `:187`, `:191` | Symmetric upper-scan rules. Guards are disjoint and recursion descends, but the “other” equation is false for non-ASCII uppercase characters. |

There are no overlaps among the entry, scheduling, value-constructor, or
scanner branches that produce conflicting right-hand sides. Map writes,
iteration order, return control, and all observable cells are accounted for.
Dictionary values are intentionally omitted; the submitted program never
reads them. Duplicate keys are not normalized by `DictVal`, but repeating an
identical key cannot change this all-keys case property. This is an acceptable
target-specific abstraction for actual normalized key sequences, not a general
Python dictionary semantics.

### Program and verification-rule decisions

`program.k:7` is the sole program rule. It is a definitional expansion to the
complete byte-pinned AST, not an operational shortcut or answer oracle.

The 20 verification rules are exhaustive as follows:

| Rule starts | Decision |
|---|---|
| `verification.k:17`, `:18` | Empty false; nonempty means all strings and all lower or all upper. This is the prompt's Boolean structure. |
| `verification.k:22`, `:24` | Multi-element and singleton `allStringKeys`; disjoint, exhaustive, and structurally decreasing. |
| `verification.k:26`, `:28` | Multi-element and singleton `allLowerKeys`; disjoint, exhaustive, and decreasing. |
| `verification.k:30`, `:32` | Multi-element and singleton `allUpperKeys`; disjoint, exhaustive, and decreasing. |
| `verification.k:34-39` | Six disjoint equations for total `lowerKey`, covering every `Value` constructor. Non-strings are false; strings delegate to `pyIsLower`. |
| `verification.k:41-46` | The analogous six disjoint, total `upperKey` equations. |

These rules are mathematical specification definitions, not semantic rules
that bypass the program. They have complete local pattern coverage and no
priority or simplification interaction. However, the operational method calls
and the contract both depend on the same `pyIsLower`/`pyIsUpper` primitives.
That sharing is legitimate only if the primitives faithfully model Python.
The Unicode witness shows that they do not.

### Required false-conclusion witness for unsound rules

For `StrVal("é")`, code point 233 is outside all ASCII letter ranges.
`lowerScan` therefore takes the “other” rule at `semantic.k:174` while keeping
`SEEN=false`, then the end rule at `:164` returns false. The analogous upper
scan also returns false. Consequently, the K program returns false for
`DictVal(StrVal("é"))`.

This is a realizable intended-domain input, and CPython evaluates
`"é".islower()` to true; the submitted Python program and prompt oracle return
true. The reviewer-authored claim in `evidence/spec-unicode-witness.k` states
the K model's false result and independently closes with `#Top`, exit 0
(`evidence/05-unicode-witness-kprove.log`). The direct `krun`/Python comparison
in `evidence/03-concrete-compare-rerun.log` supplies the same observable
witness, plus the uppercase witness `['É','İ']`.

Thus the scanner “other” rules can enable a false conclusion about the real
generated program on the intended domain. This is a material semantics
unsoundness, not merely an untested case or narrower evidence gap.

No other rule is labeled unsound without a witness. The limited `Value` sort,
absence of general exceptions, and target-specific direct-call patterns are
reported as scope limitations instead.

**Stage 5 result:** ordinary target control flow is modeled faithfully for the
submitted ASCII ground cases, but the result-bearing string primitive is
materially unsound on valid intended inputs.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was relied on. The fresh mutation
`evidence/spec-vacuity-audit.k` uses the realizable empty-dictionary initial
state and changes the result-bearing obligation from the correct
`BoolVal(false)` to the deliberately false `BoolVal(true)`.

The exact command was:

```text
kprove spec-vacuity-audit.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

The file parsed and executed successfully far enough to reach `.K` with
`BoolVal(false)`. The prover then emitted `WarnStuckClaimState`, displaying
that concrete unmet result, and exited 1. This is the expected semantic
failure, not a parser error, missing import, timeout, or unrelated crash. The
source and full bounded log are `evidence/spec-vacuity-audit.k` and
`evidence/06-vacuity-mutation.log`.

**Stage 6 result:** passes. The submitted ground claims discriminate their
results and are not vacuous.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's K definition and imported K hooks, for each of the 11
exact ground initial configurations listed in Stage 4, execution of the
byte-pinned submitted AST reaches `.K`, restores the empty environment, and
places the corresponding ground `contract` Boolean in `<result>`. The fresh
positive command proves all 11 claims, and the false mutation confirms that
their result constraints matter.

It does **not** establish partial correctness for arbitrary dictionaries,
arbitrary modeled `Values` lists, arbitrary valid Python key types, or Unicode
case behavior. There is no loop invariant or universal entry claim.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell backend, and reachability logic | All build and proof results | Ordinary unavoidable machine-checking trust boundary; rebuilt from source. |
| Imported `BOOL`, `INT`, `STRING`, and `MAP` hooks, including Boolean operations, integer arithmetic/comparisons, `lengthString`, `substrString`, `ordChar`, lookup, and update | Evaluation, scanners, environment | Acceptable low-level primitive boundary; none encodes the task answer. |
| Trusted `py2mpy.py` transliteration | Program identity | Byte identity was independently established. |
| Reviewer regeneration of `program.k` | `solutionProgram` pinning | Byte identity was independently established; no substituted body. |
| Standard unshadowed Python builtins `isinstance` and `str` | Exact call bridges | Acceptable for this source, which does not rebind them. The local value universe is incomplete for arbitrary Python keys. |
| Ordered keys-only `DictVal` representation | Every claim and loop | Values are observationally irrelevant here. Actual dictionary normalization and many key types are outside the modeled domain. |
| ASCII scanner as a model of `str.islower`/`str.isupper` | Operational results and `contract` | Illegitimate for the prompt's unrestricted string domain; concrete false-conclusion witnesses exist. |
| Independent prompt oracle and differential sample | Python-to-intent bridge | Useful finite evidence only: 5,883 tests, not a theorem. |
| Trusted canonical implementation | Candidate-versus-canonical bridge | Materially disagrees on 758 tested inputs because of its apparent early break; no formal equivalence is established. |
| Termination | Task-wide behavior | Reachability claims are partial-correctness claims. Termination beyond the ground executions is not proved. |

The candidate has no proof-local operational bridge, simplification lemma,
priority rule, or opaque result oracle beyond the generated language's direct
builtin primitives. Its defect is not answer smuggling. It is the combination
of a finite example suite presented as an exhaustive proof and a materially
incorrect Unicode semantics.

### Gate and decision accounting

- Real-program soundness over the intended domain: **fails** because the
  result-bearing scanner rules enable false Unicode outcomes.
- Intent adequacy: **fails** because 11 ground inputs do not establish the
  dictionary-wide contract, and the modeled key domain is incomplete.
- Trust/evidence validation: **fails as a task-wide proof** because finite
  differential evidence cannot replace the absent universal reachability
  theorem or repair the Unicode bridge. Reviewer evidence itself is
  reproducible.

The clean `#Top` is legitimate only for the 11 concrete K executions. It is not
a legitimate partial-correctness proof of the requested program contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
