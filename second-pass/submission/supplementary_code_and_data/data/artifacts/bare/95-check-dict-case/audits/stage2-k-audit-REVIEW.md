# Independent adversarial audit: 95-check-dict-case

The candidate is **not a legitimate proof of the unrestricted HumanEval
contract**. A clean reconstruction does prove eleven concrete examples, and
those claims genuinely execute the submitted constructor term and constrain
their results. That finite fact is far weaker than the requested theorem.
Moreover, the generated semantics implements only ASCII case classification:
fresh concrete execution returns `False` for the valid lowercase key `"é"` and
the valid uppercase key `"É"`, while the submitted Python program returns
`True`. The postcondition's purportedly independent contract calls the same
case-classification functions used by execution.

## 1. Input and provenance integrity

The integrity gate passed; this is a candidate verdict, not an infrastructure
error.

- `/audit-input.json` declares `legacy-selected-stage1`,
  `GENERATED_SEMANTICS`, problem `95-check-dict-case`, and condition `bare`.
  All records required for that layout are regular, non-symlink files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/{invocation.json,metrics.json,usage.json,codex-last.txt,codex-output.log,prompt.txt}`,
  and the structured trace. Historical `runtime-metrics.json` is neither
  present nor required for this layout.
- `/audit-campaign-lock.json` is a regular file. Its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value, and its parsed JSON object is exactly equal to
  `audit_campaign` in `/audit-input.json`.
- The candidate directory contains nine regular files and no symlink or
  unsupported entry. The required proof sources
  `solution.py`, `solution.mpy`, `semantic.k`, `program.k`,
  `verification.k`, `spec.k`, and `prove.sh` are present.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  `/reference` mounts. Their independently computed SHA-256 values,
  `e8a971...7631` and `406485...db16`, match `/audit-input.json`.
  `/reference/canonical.py` hashes to the recorded
  `6918f3...a34e`.
- All independently computed hashes of the run, task, result, invocation,
  metrics, usage, prompt, final text, output log, and trace file match their
  recorded per-file hashes. In particular, the sole JSONL trace hashes to
  `8c30c858...ecaf3`, as recorded by both the invocation and result records.
- All 190 JSONL trace entries parse. I reviewed its tool-call chronology and
  the 17,329-line output record only as untrusted history. The trace records
  that generation tried an arbitrary-`Values` claim, received
  `WarnStuckClaimState`, deleted that claim, and retained the ground examples.
  It also explicitly acknowledges the ASCII/Unicode distinction. Neither
  admission is used as proof; both were checked afresh below.
- The generated-semantics boundary is correct: `/reference` contains only
  `canonical.py`, `prompt.py`, and `py2mpy.py`;
  `/reference/reference-semantics` does not exist.

Exact checks, hashes, types, record counts, and exits are in
`/audit-output/evidence/01-provenance-check.sh` and
`/audit-output/evidence/01-provenance.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The prompt says: for a nonempty dictionary, return `True` exactly when every
key is a string and either every key is lowercase or every key is uppercase;
return `False` otherwise. “Lowercase” and “uppercase” are the Python string
predicates used by the trusted canonical implementation, so Unicode cased
letters are in scope. Dictionary values are irrelevant.

The submitted Python implements that direct reading: it starts `lower` and
`upper` as true, rejects a non-string key, clears the corresponding flag for
each string, and returns their disjunction. Trusted translation in scratch
produced a file byte-identical to submitted `solution.mpy` (`cmp` exit 0).

The trusted canonical implementation has a separate source discrepancy. Once
its state is `lower` or `upper`, a second matching key takes its final `else:
break`, so later keys can be ignored. For example:

- `{"a": 0, "b": 0, "C": 0}`: canonical `True`, submitted program `False`,
  prompt contract `False`;
- `{"a": 0, "b": 0, 8: 0}`: canonical `True`, submitted program `False`,
  prompt contract `False`.

The independent differential corpus contained all ordered selections of zero
through three distinct keys from a 14-element pool, 100 seeded four-key
samples, every prompt example, branch boundaries, non-string positions,
uncased strings, and Unicode. Across 2,487 unique dictionaries:

- submitted program versus prompt contract: **0 mismatches**;
- trusted canonical versus prompt contract: **382 mismatches**;
- trusted canonical versus submitted program: **382 mismatches**.

Thus the submitted Python is faithful to the natural-language contract even
though it is not extensionally identical to the trusted canonical bug. The
script, deterministic input construction, named results, capped mismatch
records, commands, and zero exit are in
`/audit-output/evidence/differential.py`,
`/audit-output/evidence/02-fidelity.sh`, and
`/audit-output/evidence/02-fidelity.log`.

## 3. Clean proof reconstruction

All candidate artifacts were copied to
`/tmp/audit-work/95-check-dict-case-audit`. No candidate-built definition or
cache was present before compilation. K reports version `7.1.293`.

Fresh commands and results were:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition concrete-fresh-kompiled
exit 0

kompile verification.k --main-module VERIFICATION \
  --syntax-module VERIFICATION --backend haskell \
  --output-definition verification-fresh-kompiled
exit 0

kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC
#Top
exit 0
```

I made a label-only copy of the claims and mechanically confirmed that all
eleven claim bodies equal the originals. Each claim was then selected and run
separately with `--claims SPEC-LABELED.<label>`; every command exited 0 and
printed `#Top`. The full build and per-claim record is
`/audit-output/evidence/03-reconstruct.log`; the exact label-only artifact is
`/audit-output/evidence/spec-labeled.k`.

Fresh LLVM execution of the actual `solution.mpy` was compared with the
submitted Python:

| Input class | K | Python | Match |
|---|---:|---:|---|
| empty | false | false | yes |
| ASCII lower | true | true | yes |
| ASCII upper | true | true | yes |
| mixed case | false | false | yes |
| non-string key | false | false | yes |
| uncased-only string | false | false | yes |
| `{"é": 0}` | false | true | **no** |
| `{"É": 0}` | false | true | **no** |

The final corrected concrete log is
`/audit-output/evidence/03-concrete-check-final.log`, with exact K inputs,
commands, exits, complete final configurations, and Python results. The earlier
`03-concrete-check.log` and `03-concrete-check-rerun.log` transparently retain
two reviewer-probe mistakes (`--pattern` without LLVM search support, then an
over-escaped result regex); neither is treated as candidate evidence.

## 4. Adequacy and real-program pinning

### Pinning

Trusted regeneration plus a constructor-level comparison establishes the
source-to-claim link:

```text
normalized regenerated solution.mpy:
  3f4c16b750dfa4236ba7e9912faa6ca8a759650e8f762e69b5f6769fb0e69458
normalized program.k rule RHS:
  3f4c16b750dfa4236ba7e9912faa6ca8a759650e8f762e69b5f6769fb0e69458
constructor_terms_equal=True
```

Whitespace was removed only outside quoted K strings. The `<k>` cell in every
claim starts with `solutionProgram`, whose function equation expands to that
exact term. A body-sensitivity mutation changed the executed constructor body
to `Return(Bool(false))`; the mutated definition built successfully, and the
lowercase claim failed with a reachable final `BoolVal(false)` rather than the
required `true`. See `/audit-output/evidence/04-adequacy-final.log` and
`/audit-output/evidence/04-body-sensitivity.log`.

### What each entry claim says

None has a `requires` or `ensures` clause, symbolic variable, or free result.
Each precondition is instead the complete exact initial configuration:
`<k> solutionProgram </k>`, the listed ground `DictVal`, empty environment,
and `NoneVal` result. Each postcondition requires empty computation, the same
input, empty environment, and
`BoolVal(contract(the same ground input))`.

| Claim/input keys | Reduced required result |
|---|---:|
| empty | false |
| `"a"`, `"b"` | true |
| `"a"`, `"A"`, `"B"` | false |
| `"a"`, integer `8` | false |
| `"Name"`, `"Age"`, `"City"` | false |
| `"STATE"`, `"ZIP"` | true |
| `"abc-123"`, `"z9"` | true |
| `"ABC-123"`, `"Z9"` | true |
| `"123"` | false |
| `"aA"` | false |
| Boolean `true` | false |

Every precondition is satisfiable: its displayed ground configuration is a
witness. Substitution into both Python implementations and the prompt contract
agrees for all eleven; the complete witness ledger is in
`04-adequacy-final.log`.

### Fatal adequacy gap

These are eleven examples, not six symbolic “aggregate partitions.” An input
such as `{"abc": 0, "def": 0, "ghi": 0}` is not covered merely because one
proved input happens to represent the all-lower behavioral class. There is no
quantifier or variable ranging over keys, strings, or list length, and no loop
invariant or recursive reachability claim. A fresh arbitrary-`KEYS:Values`
strengthening does not close and stops before even decomposing the symbolic
sequence (`/audit-output/evidence/05-universal-probe.log`). That failed probe
is not evidence that the desired theorem is false; it demonstrates that the
candidate did not establish it.

The HumanEval input domain is unrestricted by size or by a finite list of key
values. Under the benchmark's explicit mapping, this material finite-domain
narrowing is `FAIL / NOT_LEGIT`, even though each individual ground theorem is
honest.

## 5. Rule-by-rule static soundness review

The exhaustive numbered source and declaration extraction is
`/audit-output/evidence/05-rule-inventory.log`. It inventories all syntax,
configuration, function attributes, ordinary rules, and claims. There are no
local priority, `[functional]`, simplification, `[concrete]`, `[owise]`, or
opaque declarations.

### Syntax, configuration, and construct coverage

- `semantic.k:12-32` declares every target statement/expression constructor:
  `Module`, `FuncDef`, `Assign`, both `If` forms, `For`, `Return`, `Name`,
  `Bool`, `UnaryOp`, `BoolOp`, both `Call` forms, and `Attribute`, plus
  nonempty parameter and expression lists.
- `semantic.k:43-50` declares `NoneVal`, Boolean, string, integer, empty and
  nonempty dictionary-key values, and singleton/cons value sequences.
- `semantic.k:58-64` has exactly the state used by the submitted program:
  computation, abstract input, local environment, and result. There is no
  heap, I/O, allocation, or exception cell.
- `semantic.k:75-84` declares all internal continuations:
  `eval`, `assignTo`, both choice forms, loop setup/iteration/bind,
  `logicalNot`, `logicalOr`, and `returnValue`.
- `program.k:6` adds the nullary functional program symbol.
- `verification.k:10-15` declares six contract functions.

The target constructors extracted mechanically from `solution.mpy` are
`Assign`, `Attribute`, `Bool`, `BoolOp`, `Call`, `For`, `FuncDef`, `If`,
`Module`, `Name`, `Params`, `Return`, and `UnaryOp`; all map to the declarations
above. No used source constructor is silently fabricated. A dictionary literal
is not in the program; dictionary keys enter through the configuration.

### Operational rules

Each rule is classified below; grouped rows explicitly cover every listed rule.

| Rules | Static decision |
|---|---|
| `semantic.k:67-70` module/function entry | Sound for the exact function name, one `dict` parameter, fresh local environment, and externally supplied argument used here. It is deliberately not a general Python module semantics. |
| `73` statement-list scheduling | Sound left-to-right sequencing for the constructor list. |
| `87-89` assignment/effect | Sound: expression is evaluated first and the local map key is updated. |
| `91-96` both `If` forms and true/false choices | Pairwise disjoint and sound for the reachable `BoolVal` conditions. |
| `98-105` `For`, empty/nonempty setup, multi/single iteration, and bind | Sound for iteration over the abstract dictionary key sequence; the loop binds in order and returns to a stable computation. Multi and singleton cases are disjoint. |
| `107-110` return scheduling and abrupt return | Sound for this top-level, no-call-stack subset: it discards the remaining continuation, clears locals, and stores the returned value. The program has no cleanup, output, or exception cell to preserve. |
| `113-115` Boolean literal and name lookup | Sound for the used expressions and local map. |
| `118-122` `not` and Boolean/empty/nonempty dictionary truthiness | Sound and disjoint for all reachable operands in this program. |
| `125-127` two-operand `or` | Sound short-circuit control for the Boolean flags used by the program. |
| `132-134` abstract `isinstance(key, str)` | Sound over the declared `Value` constructors conditional on the trusted `pyIsString` primitive below. It pins the textual builtin because this reduced semantics has no globals or rebinding; that is valid for this exact body but not a general Python theorem. |
| `136-141` `islower`/`isupper` method-call bridges | **Materially unsound as Python semantics over the intended string domain.** They bypass receiver evaluation and dispatch to the candidate predicates. Plain local names make evaluation-order effects inert for this body, but the predicates are ASCII-only and no bridge-free connection theorem to CPython exists. |

### Semantic functions

The custom semantic functions are `pyIsString [function,total]`,
`pyIsLower`, `pyIsUpper`, `lowerScan`, and `upperScan`.

| Equations | Static decision |
|---|---|
| `semantic.k:144-149` all six `pyIsString` cases | Sound, disjoint, and collectively total over every declared `Value` constructor. |
| `161-162` string predicate entry equations | Definitional delegation to the scan functions; terminating from index zero. Their claimed Python meaning inherits the scan defect. |
| `164-165`, `181-182` end-of-scan equations | Sound: return whether an ASCII cased character has been seen. |
| `166-169` uppercase character makes `lowerScan` false; `183-186` lowercase makes `upperScan` false | Sound for the ASCII intervals and disjoint from the other guarded cases. |
| `170-173` ASCII lowercase updates `lowerScan`; `187-190` ASCII uppercase updates `upperScan` | Sound for the ASCII intervals and strictly increase the index. |
| `174-179`, `191-196` “all other code points are uncased” | **Unsound relative to Python.** These guards include every code point above 122, including Unicode cased letters. They are the concrete false-conclusion rules described below. |

For a nonnegative reachable index, each scan's end, opposite-case, matching-case,
and catch-all guards are pairwise disjoint and cover the K code-point cases;
recursion strictly increments the index. The functions are not declared total
for arbitrary negative or non-string calls, and those calls are unreachable
from this program.

**Required false-conclusion witness.** For the intended input `{"é": 0}`,
CPython has `"é".islower() == True`, and submitted `solution.py` returns
`True`. In K, code point 233 satisfies the `>Int 122` catch-all at
`semantic.k:174-179`; `SEEN` remains false, so `pyIsLower(StrVal("é"))`
becomes false. `pyIsUpper` is also false, both program flags become false, and
the K execution concludes `BoolVal(false)`. The fresh final configuration is
recorded in `03-concrete-check-final.log`. The uppercase witness `"É"`
(code point 201) analogously triggers `191-196`; Python returns `True`, while
K concludes false. These are concrete false program conclusions on the source
domain, not merely missing evidence.

### Program and verification functions

- `program.k:7-24` is the sole equation for `solutionProgram`. It is a
  definitional macro, exactly tied to regenerated `solution.mpy`; it does not
  summarize or skip the body.
- `verification.k:17-20` defines empty contract false and nonempty contract as
  all strings and (all lower or all upper). This is mathematically the prompt
  shape, conditional on the meanings of the lower/upper predicates.
- `22-24`, `26-28`, and `30-32` are the cons/singleton equations for
  `allStringKeys`, `allLowerKeys`, and `allUpperKeys`. Each is structurally
  descending; its two cases are disjoint and cover the nonempty `Values`
  grammar.
- `34-39` exhaustively define total `lowerKey`; `41-46` exhaustively define
  total `upperKey`. The five non-string constructor cases correctly return
  false. The string cases delegate to the same `pyIsLower` and `pyIsUpper`
  symbols used by the operational bridges.

That last delegation defeats the comment that the contract is independent.
The same result-bearing abstraction drives both program execution and the
postcondition, with no bridge-free universal theorem establishing its CPython
meaning. This is circular under the Kit validation contract. It happens to
compute correct answers for the eleven ASCII ground cases, but it would make
execution and contract agree on the false Unicode interpretation too.

### Claims and model boundaries

All eleven `spec.k` claims are ordinary ground reachability claims; there are
no auxiliary claims, loop circularities, lemmas, simplification equations,
priorities, or opaque result symbols. Their rule-by-rule result is covered in
Stage 4.

The value domain also omits many legal hashable non-string Python keys (tuples
are enough as a witness), the Python object model, subclasses/overridden string
methods, and exceptions. Omitting unused language constructs is allowed in
generated-semantics mode, but legal input values are part of the source
contract. Since the candidate only proves ground values anyway, this is an
additional domain limitation rather than a hidden universal theorem.

## 6. Fresh non-vacuity test

I created a new spec for the satisfiable input `{"a": 0, "b": 0}` and changed
the required result from true to false. It uses the original program term and
fresh proof definition.

```text
kprove spec-vacuity-review.k --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY-REVIEW --dry-run
exit 0

kprove spec-vacuity-review.k --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY-REVIEW
WarnStuckClaimState
reachable result: BoolVal(true)
exit 1
```

This is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash. The mutation and complete bounded
log are `/audit-output/evidence/spec-vacuity-review.k` and
`/audit-output/evidence/06-non-vacuity.log`. The eleven ground claims are
therefore result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under the candidate's generated K theory, from each of the eleven exact ground
configurations in Stage 4, execution of the exact submitted constructor body
reaches empty computation and environment with the corresponding listed
Boolean contract value. This is a machine-checked set of eleven terminating
examples. It is not a theorem over an arbitrary dictionary, arbitrary number
of keys, or arbitrary strings.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 Haskell reachability engine and LLVM execution | All build, execution, and proof results | Ordinary low-level trust boundary. |
| Builtin K Boolean, integer, string, `ordChar`/substring/length, and map hooks | Evaluation, scans, local state | Acceptable primitives as K operations; they do not establish correspondence to all of CPython. |
| Trusted `py2mpy.py` translation | Source-to-constructor identity | Acceptable and mechanically checked by byte regeneration plus constructor comparison. |
| `DictVal` as ordered keys with values omitted | All modeled inputs | Acceptable for plain dictionaries because this body observes only keys; incomplete for the full Python key-object domain. |
| Textually pinned `isinstance`, `islower`, and `isupper` bridges | Branches, flags, final result, contract | `isinstance` is acceptable over declared values. Case bridges are illegitimate over the intended Unicode domain and lack a universal connection theorem. |
| Reuse of `pyIsLower`/`pyIsUpper` in `contract` | Every postcondition | Circular result-bearing abstraction, not independent evidence of Python meaning. |
| Differential corpus | Python/prompt alignment and finite K bridge observations | Reproducible finite evidence only; it cannot replace a universal K theorem. |
| Trusted canonical implementation | Differential oracle | Its late-key behavior conflicts with the prompt; the discrepancy is explicitly reported rather than used to redefine the contract. |

In Kit terms, the literal eleven ground claims reconstruct and discriminate,
but Gate A does not validate them as a proof under faithful real-program
semantics because of the Unicode operational bridge and circular contract
predicate. Gate B independently fails because the theorem domain is only
eleven fixed inputs. Gate C evidence is reproducible, but finite testing cannot
repair either defect.

The decisive benchmark mapping is unambiguous: fixed examples do not prove an
unrestricted HumanEval domain, and the semantics also produces concrete false
program results on that domain. The candidate is therefore not legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
