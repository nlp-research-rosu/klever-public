# Independent adversarial audit: 7-filter-by-substring

Audit result: **FAIL / NOT_LEGIT**.

The candidate's six submitted proof commands do reconstruct from source and
print `#Top`, and the Python implementation is faithful to the trusted
canonical function. Those facts do not establish correctness of the real
program under the intended Python behavior. The individually generated
semantics is observably false on an intended boundary input:

```text
strings = [""]
substring = ""
trusted canonical Python = [""]
candidate Python         = [""]
fresh generated K        = []
```

The cause is `semantic.k`'s definition
`findString(HAYSTACK, NEEDLE, 0) >=Int 0`: on the ground case
`HAYSTACK = NEEDLE = ""`, it drives the drop branch although Python's
`"" in ""` is true. This is a concrete false program-result witness, preserved
in
[`evidence/stage5-unsound-empty-empty-witness.log`](evidence/stage5-unsound-empty-empty-witness.log).

There is a second material adequacy failure. The sole arbitrary-input entry
claim stops at the internal `evalComp(...)` term. The base and step claims are
conditional induction obligations, but no submitted K claim states and closes
the universal entry result `execute(...) => filterRef(...)`. An auditor-written
version of that missing claim builds, then gets stuck on precisely the unproved
symbolic equality. Even an informal assembly of the induction obligations would
only connect execution to `filterRef`, which reuses the same incorrect
`containsString` predicate.

## 1. Input and provenance integrity

### Trusted-boundary result

The rendered mode and trusted mounts are consistent:

- `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py` are present as regular files.
- `/reference/reference-semantics` is absent, as required for
  `GENERATED_SEMANTICS`.
- I did not search for, infer, or use any hidden reference semantics.
- The candidate prompt is byte-identical to `/reference/prompt.py`.
- The candidate translator is byte-identical to `/reference/py2mpy.py`.
- No symlinks occur anywhere under `/candidate`.

The candidate has all original-generation deliverables as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. It also contains untrusted `.kbuild`, documentation, logs, metrics,
and a structured trace. The compiled `.kbuild` was not copied or used. There
are no candidate helper `.k` files beyond the three named K files. No
`PROOF.md` or `spec-vacuity.k` is present; neither was a required deliverable
of the original bare-generation prompt.

The exact tree, hashes, comparison statuses, and file modes are in
[`evidence/stage1-provenance-complete.log`](evidence/stage1-provenance-complete.log).
An earlier provenance command reached an unavailable optional `file` utility
and exited 127 after already recording its preceding checks; it is retained
transparently as
[`evidence/stage1-provenance.log`](evidence/stage1-provenance.log). The
successful replacement uses `stat`.

### Untrusted generation claims

I read the complete 1,735,634-byte `codex-output.log` and the complete
785,714-byte, 422-line structured JSONL trace. The trace has no malformed JSON
lines. I also read `run-input.json`, `metrics.json`, and `codex-last.txt`.
Their relevant claims are:

- condition `bare`, no supplied semantics;
- generator exit 0 without timeout;
- immutable prompt/translator hashes;
- `prove.sh` exit 0;
- two concrete examples matched;
- six positive claims printed `#Top`;
- final marker `KPROVE_PASSED`.

These were treated only as claims. The full-read counts and final claimed
message are preserved in
[`evidence/stage1-untrusted-generation-summary.log`](evidence/stage1-untrusted-generation-summary.log).
The structured trace and output contain no vacuity test claim.

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and intended domain

From trusted `/reference/prompt.py` and `/reference/canonical.py`: for a finite
Python `List[str]` and a Python `str` substring, return a new list containing
exactly the input strings for which `substring in string` is true, preserving
input order and duplicates. The empty substring is contained in every Python
string, including the empty string. The empty input returns the empty list.

Candidate `solution.py` is the same list-comprehension algorithm modulo the
bound variable name:

```python
return [string for string in strings if substring in string]
```

It is faithful over the full typed input domain. It introduces no mutation,
I/O, exceptions on valid typed inputs, reordering, or duplicate elimination.

### Translator identity

I regenerated the constructor program in scratch with the trusted command:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/7-filter-by-substring/solution.py \
  > /tmp/audit-work/7-filter-by-substring/regenerated-solution.mpy
```

The command exited 0, `cmp` exited 0, and both files have SHA-256
`03ce6c305c9520c8bb56a7c65fbfff1316e16bc1007e005af3665b2774e60866`.
See
[`evidence/stage2-translation-identity.log`](evidence/stage2-translation-identity.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical entry point directly from `/reference/canonical.py` and the
scratch candidate entry point from `solution.py`; it does not reuse proof
equations. Its scope was:

- 10 named cases: both documented examples, empty needle/haystack, exact
  matches, start/middle/end matches, absent and longer needles, duplicates,
  Unicode, and a NUL character;
- 2,400 exhaustive cases over lists of lengths 0–3, seven small strings, and
  six needles;
- 2,000 deterministic generated Unicode/NUL cases with seed 7007.

All 4,410 cases agreed. Exact inputs are in
[`evidence/differential_cases.json`](evidence/differential_cases.json), and the
command/result is in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log).
This is finite support for candidate-Python/canonical equivalence, not a K
proof.

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/7-filter-by-substring`. Candidate compiled definitions and
caches were ignored.

Tool versions were K v7.1.293 and Python 3.10.12; see
[`evidence/toolchain.log`](evidence/toolchain.log).

### Fresh concrete definition

The generated semantics was freshly compiled with LLVM:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition semantic-llvm-kompiled
```

Exit status was 0
([build log](evidence/stage3-kompile-semantic-llvm.log)).

I then compared fresh `krun` results with both trusted canonical Python and
candidate Python on six concrete cases: empty input, the prompt example, empty
substring with duplicates and an empty string, all-drop, exact/start/end
matches, and a needle longer than every string. Five agreed. The intended
boundary `(["x", "x", ""], "")` did not:

```text
Python: ["x", "x", ""]
K:      ["x", "x"]
```

Commands, exit statuses, complete final configurations, and comparisons are in
[`evidence/stage3-concrete-semantics.log`](evidence/stage3-concrete-semantics.log).
Every `krun` command itself exited 0; this is a semantic result divergence, not
a tooling error.

### Fresh proof definition and positive claims

The proof theory was freshly compiled with Haskell:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition verification-haskell-kompiled
```

Exit status was 0
([build log](evidence/stage3-kompile-verification-haskell.log)).

Each submitted positive claim was then run independently. All exited 0 and
printed exactly one `#Top`:

| Claim | Exit | `#Top` |
|---|---:|---:|
| `UNIVERSAL-PROGRAM-REDUCTION` | 0 | 1 |
| `UNIVERSAL-BASE` | 0 | 1 |
| `UNIVERSAL-STEP-KEEP` | 0 | 1 |
| `UNIVERSAL-STEP-DROP` | 0 | 1 |
| `EMPTY-EXAMPLE` | 0 | 1 |
| `PROMPT-EXAMPLE` | 0 | 1 |

The aggregate is
[`evidence/stage3-positive-claims-summary.log`](evidence/stage3-positive-claims-summary.log);
each exact command and output is separately preserved as
`evidence/stage3-kprove-<CLAIM>.log`.

Thus the candidate's narrow reconstruction claim is true. Closure under the
candidate theory does not cure that theory's semantics defect or enlarge what
the submitted claims state.

## 4. Adequacy and real-program pinning

### Program identity

`verification.k` defines `solutionProgram` as a concrete `Module(...)` term.
An independent extraction and whitespace-normalized comparison found that RHS
identical to the trusted-translator-generated `solution.mpy` term. Both compact
terms have SHA-256
`ad589baa638c0498b405895787e452d512c20e0ad5e3661345e884dd067aeef6`.
See
[`evidence/program_pinning_check.py`](evidence/program_pinning_check.py) and
[`evidence/stage4-program-pinning.log`](evidence/stage4-program-pinning.log).

Together with byte-identical translation, this statically pins the
`solutionProgram` alias to the submitted generated program. There is no helper,
loop, alternate function body, free result oracle, abrupt control bridge, or
substituted program.

### Claims in plain language

| Claim | Precondition | Postcondition |
|---|---|---|
| `UNIVERSAL-PROGRAM-REDUCTION` | Any `PyList` and K `String`. | The exact entry program reaches the internal `evalComp(INPUT,substringFilter(SUBSTRING))` term. |
| `UNIVERSAL-BASE` | Empty list and any substring. | Empty evaluator reaches empty `filterRef`. |
| `UNIVERSAL-STEP-KEEP` | `containsString(HEAD,SUBSTRING)` and an assumed equality of evaluator/reference on `TAIL`. | The Cons evaluator reaches the Cons reference. |
| `UNIVERSAL-STEP-DROP` | Negated predicate and the same assumed tail equality. | The Cons evaluator reaches the dropping reference. |
| `EMPTY-EXAMPLE` | Ground prompt empty input. | Returns `Nil`. |
| `PROMPT-EXAMPLE` | Ground four-string prompt input. | Returns `["abc","bacd","array"]`. |

Every precondition is satisfiable. One explicit substitution for each, with
trusted and candidate Python results, is in
[`evidence/stage4-claim-witnesses.log`](evidence/stage4-claim-witnesses.log).
For example:

- keep step: `HEAD="a"`, `TAIL=Nil`, `SUBSTRING="a"`; predicate true and tail
  equality `[] == []`;
- drop step: `HEAD="b"`, `TAIL=Nil`, `SUBSTRING="a"`; negated predicate true
  and tail equality `[] == []`;
- general entry: `INPUT=Cons("a",Nil)`, `SUBSTRING="a"`;
- base and ground examples use their literal inputs.

Those witnesses agree with both Python implementations. A different,
equally satisfying entry state, `INPUT=Cons("",Nil)` and `SUBSTRING=""`,
exposes the semantics divergence: both Python implementations return `[""]`,
while fresh K returns `Nil`.

### Missing result-constraining entry theorem

The arbitrary-input entry postcondition is not the requested result; it is an
internal evaluator term. The candidate comments say the other three universal
claims prove evaluator/reference equality by induction, but the submitted
proof never states or closes the combined universal entry claim.

I created the exact missing claim in
[`evidence/spec-intended-universal-audit.k`](evidence/spec-intended-universal-audit.k):

```text
execute(solutionProgram, "filter_by_substring", INPUT, SUBSTRING)
  => filterRef(INPUT, SUBSTRING)
```

Its dry run exits 0
([log](evidence/stage4-intended-universal-dry-run.log)), proving it parses and
builds. Its actual proof exits 1 with `WarnStuckClaimState` at:

```text
evalComp(INPUT, substringFilter(SUBSTRING))
  #Equals filterRef(INPUT, SUBSTRING)
```

See
[`evidence/stage4-intended-universal-kprove.log`](evidence/stage4-intended-universal-kprove.log).
This diagnostic is not being substituted for the candidate claims; it shows
exactly the theorem the submitted positive claims do not establish in K.
An informal structural induction can assemble the base and two conditional
steps mathematically, but it remains outside the successful reachability
claims, and its conclusion uses the faulty shared predicate.

Adequacy therefore fails independently of the semantics counterexample.

## 5. Rule-by-rule static soundness review

The exhaustive local inventory is
[`evidence/rule-inventory.md`](evidence/rule-inventory.md). It covers all 29
syntax/configuration/function declarations in `semantic.k`, all 13 semantic
rules, both declarations and four equations in `verification.k`, and all six
submitted claims. There are no helper K files and no local priorities,
simplification rules, `functional` declarations, opaque/fresh symbols,
`anywhere` rules, macros, or operational proof bridges.

### Construct coverage

Every constructor in `solution.mpy` is declared and has a sound narrow route
for the exact submitted program:

```text
Module / statement list
  -> ImportFrom skip
  -> FuncDef lookup
  -> Params, CellVars, FreeVars parse
  -> Return extraction
  -> ListComp with one CompFor
  -> Name("strings") list lookup
  -> Compare(Name("substring"), CmpOp("in", Name(target)))
  -> Name("substring") string lookup
  -> evalComp over Nil/Cons
```

The `<k>`-only configuration is adequate for this pure typed function.
Function selection preserves name binding; the invocation map installs the
two distinct actual parameter names; list/string lookups are typed; the
list-comprehension rule is deliberately exact-shape; recursion descends on the
tail; and keep/drop guards are complementary. Order and duplicates are
preserved. Unsupported unused constructs visibly stick rather than receiving
fabricated behavior, which is acceptable for generated minimal semantics.

`solutionProgram` is a terminating exact definition, not an execution bypass.
`filterRef` is total on `PyList` under the local Boolean predicate, its cases
are disjoint, and its recursion descends. There is no unconstrained result
oracle.

### Materially unsound result-bearing rule

The one local rule that falsely models a used Python construct is
`semantic.k:97–98`:

```k
rule containsString(HAYSTACK, NEEDLE)
  => findString(HAYSTACK, NEEDLE, 0) >=Int 0
```

Its value controls both execution's S11/S12 branch and `filterRef`'s V05/V06
branch, and therefore the final returned list and all universal comments.

Required false-conclusion witness:

```text
HAYSTACK = ""
NEEDLE   = ""
INPUT    = Cons("", Nil)

Python fact:       "" in "" == True
Canonical result: [""]
Candidate result: [""]
K result enabled by the rule and drop branch: Nil
```

This satisfying typed state is executed in
[`evidence/stage5-unsound-empty-empty-witness.log`](evidence/stage5-unsound-empty-empty-witness.log).
The K command exits 0 and produces `Nil`, so this is not an evidence gap,
timeout, or unsupported construct. It is a concrete false observable
conclusion on the intended domain.

The keep/drop and `filterRef` rules are not independently inconsistent under
their stated K guards; they are structurally valid conditional rules. They
inherit the false intended interpretation because both use `containsString`.
Using that same predicate in program execution and the purported reference is
circular evidence for Python-membership correctness: their agreement cannot
validate the predicate they share.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was available. I created
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k), using the
satisfiable prompt input but mutating the result to wrongly omit the matching
final `"array"`:

```text
claimed false result: ["abc", "bacd"]
actual result:        ["abc", "bacd", "array"]
```

The dry run exited 0 and emitted a valid `kore-exec ... --prove` command, so the
mutation built successfully
([dry-run log](evidence/stage6-vacuity-dry-run.log)). The proof then exited 1
with `WarnStuckClaimState`; its residual is exactly the reachable actual result:

```text
<k>
  Cons("abc", Cons("bacd", Cons("array", Nil))) ~> .K
</k>
```

See
[`evidence/stage6-vacuity-kprove.log`](evidence/stage6-vacuity-kprove.log).
This is the expected unmet result obligation. The submitted ground proof is
non-vacuous and result-sensitive. That does not repair the semantics or missing
universal postcondition.

## 7. Proven-versus-assumed accounting

### Precisely what the successful reachability proofs establish

Under the candidate K theory:

1. the exact translated AST, on an arbitrary `PyList`/K-`String` input, reduces
   to the candidate's `evalComp` term;
2. `evalComp` and `filterRef` agree on the empty constructor;
3. if they agree on a tail, each of the shared-predicate keep and drop cases
   agrees on the corresponding Cons value;
4. the empty prompt example and the four-string prompt example return their
   stated ground outputs.

They do **not** machine-check a universal entry reachability claim whose
destination is `filterRef` or the natural-language filtering result. More
importantly, they do not establish that the shared K predicate is Python
substring membership; that unconditional bridge is false.

### Trust and assumption ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Trusted `/reference/prompt.py` and `/reference/canonical.py` | Defines intended typed behavior and differential oracle. | Approved input. |
| Trusted `/reference/py2mpy.py` | Connects candidate Python syntax to `solution.mpy`. | Approved input; byte identity and exact AST pinning verified. |
| K toolchain/backends and imported Bool/Int/String/Map/K-equality operations | Parsing, rewriting, strings, maps, guards, equality, and proof closure. | Ordinary low-level trust boundary. Fresh builds/runs avoid candidate caches. |
| `findString(H,N,0) >=Int 0` as Python `N in H` | Controls every keep/drop result in both `evalComp` and `filterRef`, hence every universal intended conclusion. | **Illegitimate unconditional bridge.** Ground opposite-outcome witness `H=N=""` is admitted and produces the wrong result. |
| Shared `containsString` in execution and `filterRef` | Makes evaluator/reference equality insensitive to the predicate's intended meaning. | Concerning/circular as intent validation; the same defect is on both sides. |
| External structural induction assembling base and steps | Needed to infer arbitrary-list evaluator/reference equality and then the intended entry theorem. | Informally plausible over `PyList`, but not a successful submitted K entry claim; auditor formulation gets stuck. Material adequacy gap. |
| Typed finite-list/string domain | Excludes non-list elements, Python subclasses, malformed calls, and unsupported AST forms. | Acceptable alignment with `List[str], str`; minimal semantics need not model unused constructs. |
| Finite Python differential suite | Supports candidate-Python/canonical equivalence on 4,410 cases. | Useful empirical bridge only; does not prove K semantics or universal equivalence. |
| Six concrete K/Python cases | Tests normal and boundary generated-semantics execution. | Finite evidence; it directly falsifies the bridge on one boundary. |
| Partial-correctness/termination scope | Claims concern terminating executions; recursion descends on finite `PyList`, and intended Python inputs are finite. | Acceptable scope. |

### Final decision

Gate A (real-program soundness): **FAIL**. The result-bearing substring rule
enables a demonstrably false returned list on an intended input. The same
predicate on both sides does not provide a connection theorem.

Gate B (intent adequacy): **FAIL**. Python treats the empty substring as
contained in the empty string, while the generated semantics does not.
Additionally, no universal result-constraining entry claim is submitted and
closed.

Gate C (auditability): **PASS for reproducibility, not for correctness**.
Sources rebuild, commands and statuses are preserved, the Python differential
is reproducible, and the fresh mutation is meaningful. These facts expose
rather than cure the Gate A/B failures.

The decision boundary therefore requires `FAIL / NOT_LEGIT`: the candidate
relies on materially unsound generated semantics and does not contain a closed
universal entry/result theorem for the intended behavior.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
