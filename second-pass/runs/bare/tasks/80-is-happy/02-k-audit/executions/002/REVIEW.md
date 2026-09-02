# Independent adversarial review: HumanEval/80 `is_happy`

## Outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program under its generated, idealized semantics. A
fresh reconstruction closes every positive claim; the theorem term is
constructor-identical to the trusted regeneration of `solution.py`; the
semantics executes every construct used by that term; and both a body mutation
and a false-result mutation are rejected for the expected reason.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
generated semantics is connected to Python by an audited but informal
task-specific model, not a universal machine-checked Python refinement theorem.
In particular, it models unbounded recursion: the actual CPython candidate
raises `RecursionError` on a length-1000 valid string while the idealized K
execution returns `true`. This does not falsify the requested partial-correctness
statement—no wrong Boolean return was found, and exceptional/resource
termination is outside partial correctness—but it is a real, documented
language-model limitation.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. I used only its `container_paths`
mounts, not host provenance paths.

The campaign object in `/audit-campaign-lock.json` equals the campaign block in
`/audit-input.json` field for field. Its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

I read and checked the required legacy-selected-stage1 records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- all 225 records in the structured JSONL trace.

The evidence records were treated only as historical claims. Their leaf hashes
match the launcher/result records. The structured trace's only file has the
recorded result hash, and its independently computed content-tree hash matches
`usage.json`. The independently computed candidate content-tree hash is
`e0695ff94065e513581874b71a3f647dcb9dbae0f7baf92e499d8e6c4ff375a2`,
matching both `invocation.json` and `generation-result.json`.

No inspected candidate, reference, or generation-evidence entry is a symlink.
All required records and mounts are readable regular files/directories. The
candidate prompt and translator are byte-identical to the trusted mounts:

- prompt:
  `f6df53687ee0d5e99ab8d7b0e23ccaa81bf7bb578c1789277336f0016d402ac0`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

As required for `GENERATED_SEMANTICS`, `/reference/reference-semantics` is
absent. I did not seek or infer a hidden semantics. There is no infrastructure
breach. Exact checks and trace inventory are in
[provenance.log](evidence/provenance.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for a Python string `s`, return true exactly when
`len(s) >= 3` and every overlapping length-three window contains three
pairwise-distinct characters.

The trusted canonical implementation rejects lengths below three, then scans
all windows and rejects on any equality. The candidate implements the same scan
recursively: `is_happy` rejects short strings, while
`check_happy_triples` checks the three pairwise equalities in the current
window and recurses on `s[1:]`.

Trusted regeneration was exact:

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
# exit 0
```

Both files hash to
`fd871e9b9fe673932b6f77f16595ee6a0fea1ae8d74e89c8fca2e0b11a1e604c`.

The independent differential test uses the trusted canonical entry point and a
separately written adjacent-index oracle. It covers all six prompt examples,
empty and length boundaries, every equality branch, later recursive failures,
NUL/non-ASCII/emoji/combining-code-point cases, every `abc` string through
length 8, and 3,000 seeded generated strings through length 80. Result:

```text
total_cases=12858
mismatch_count=0
```

See [differential_test.py](evidence/differential_test.py) and
[source-fidelity.log](evidence/source-fidelity.log).

The resource-boundary probe found:

```text
length=995  canonical=True generated=True
length=1000 canonical=True generated='RecursionError'
length=1100 canonical=True generated='RecursionError'
```

This is an implementation/idealized-semantics termination discrepancy, not a
wrong returned value. It is retained in
[resource-boundary.log](evidence/resource-boundary.log).

## 3. Clean proof reconstruction

All source artifacts were copied to `/tmp/audit-work/80-is-happy`. No
candidate-built definition or cache was mounted or reused. The live toolchain
is K `v7.1.293`.

Fresh concrete build:

```text
kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-audit-kompiled
# exit 0
```

Fresh proof build:

```text
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition verification-audit-kompiled
# exit 0
```

The original aggregate target proof independently closes:

```text
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC
#Top
# exit 0
```

I also separated the eight targets. The helper claim closes alone; the
universal entry closes with the helper circularity present; each of the six
examples closes in its own one-claim module. Every invocation exits 0 and
prints `#Top`. The exact modules, runner, and output are in
[positive-specs](evidence/positive-specs),
[run_positive_claims.sh](evidence/run_positive_claims.sh), and
[positive-proofs.log](evidence/positive-proofs.log).

Fresh `krun` execution was compared directly with both Python implementations
on 12 normal/boundary/branch/Unicode inputs. All completed at
`<k> pyBool(...) ~> .K </k>` with zero mismatches. See
[semantic_concrete_compare.py](evidence/semantic_concrete_compare.py) and
[semantic-concrete.log](evidence/semantic-concrete.log).

Build commands and bounded output are preserved in
[toolchain-and-build.log](evidence/toolchain-and-build.log).

## 4. Adequacy and real-program pinning

### Plain-language claims

The claims have no side condition beyond K sort membership.

- Helper claim: for every finite `PString S`, executing the submitted
  `check_happy_triples(S)` returns `pyBool(#allTriples(S))`.
- Entry claim: for every finite `PString S`, executing the submitted
  `is_happy(S)` returns `pyBool(#happy(S))`.
- Six example claims instantiate the entry claim at `"a"`, `"aa"`, `"abcd"`,
  `"aabb"`, `"adb"`, and `"xyy"` with their required concrete Boolean.

`#allTriples` is true for strings shorter than three and otherwise is the
conjunction of pairwise distinctness of the first triple and the property of
the one-character tail. `#happy` is false below length three and equals
`#allTriples` otherwise. The postconditions therefore constrain the returned
Boolean exactly; there is no free result variable, implication-only target, or
tautological destination.

Every entry precondition is satisfiable. Examples:

- `S = eps`: helper result `true`; entry/Python result `false`;
- `S = "abc"`: helper result `true`; entry/canonical/generated result `true`;
- `S = "aab"`: helper/entry/canonical/generated result `false`.

These witnesses occur in the positive claims and fresh concrete comparison.

### Mechanical program identity

`verification.k` defines `#solution` as a name for a complete `Module` tree.
I copied that right-hand side, rendered internal `.Stmts` units as the
equivalent empty surface syntax, parsed both it and submitted `solution.mpy`
with the fresh definition, and compared KORE:

```text
submitted-solution.kore
claimed-solution.kore
sha256 for both:
686c06918d650e927bdd2b05eae8fb9116f92124ce542917c25e055dc9ae8085
cmp exit 0
```

Together with trusted byte-identical regeneration, this mechanically pins the
claims to `solution.py`. See
[claimed-solution.mpy](evidence/claimed-solution.mpy) and
[program-pinning.log](evidence/program-pinning.log).

The helper circularity matches real control flow. It is reached only after the
body has checked the current triple and evaluated `s[1:]`; thus the recursive
argument has structurally lost one `ch` constructor. It is not a fixed-size
unrolling.

A separate body-sensitivity mutation changed the actual `#solution` constructor
term from `s[1] == s[2]` to `s[1] == s[1]`. The mutant definition built, but
the positive proof exited 1 with `WarnStuckClaimState` at
`pyBool(false)` versus the required distinct-triple result. See
[body-sensitivity.log](evidence/body-sensitivity.log).

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule/claim listing is
[rule-inventory.txt](evidence/rule-inventory.txt). It inventories every local
syntax declaration, configuration, function/total attribute, ordinary rule,
and claim. There are no local priority, simplification, macro, `anywhere`, or
opaque declarations.

### Construct coverage

| Submitted construct | Declaration and behavior |
|---|---|
| module and functions | `Module`, `FuncDef`, `Params`; `#call/#findCall` select the two unique definitions |
| statements | `If`, `Return`, statement list; `#exec/#choose/#branch/#append` |
| names and calls | `Name`, `Call`; parameter lookup, `len`, and same-module helper calls |
| literals | `Int`, `Bool`; typed `PValue` constructors |
| comparisons | `Compare`, `CmpOp`; exact `len(s) < 3` and integer equality cases |
| indexing and slicing | `Subscript`, `Slice`, `NoBound`; `#at` and `#drop` |
| recursion | same `Program` is retained by lookup and passed through `#exec/#eval` |

Every constructor in submitted `solution.mpy` is covered; unsupported AST
constructs have no fallback rule and therefore cannot silently fabricate a
result.

### Operational and mathematical rules

| Rule group | Static judgment |
|---|---|
| `#len` (2) | Exhaustive structural length on `PString`; recursive descent is strict. |
| `#at` (2) | Correct zero/positive indexing. Partial outside valid indices; all actual calls are 0, 1, or 2 after the length-at-least-three branch. |
| `#drop` (2) | Correct zero/positive prefix removal. Actual slicing uses only `drop 1` on a nonempty string. |
| `#short3` (4) | Exhaustive/disjoint PString constructor split for `len < 3`. |
| `#same` (2) | Exhaustive/disjoint Int equality split; unequal rule is guarded by `=/=Int`. |
| typed projections (4) | Each unwraps the corresponding value constructor; all actual uses have that constructor. |
| `#valueEq` (1) | Truthful integer equality; unused by the submitted execution/proof. |
| `#call/#findCall` (3) | Retains the fixed module and parameter/value binding; unique actual names make lookup deterministic and correct. |
| `#exec` (2) | Return exits; If evaluates its condition and retains the remaining statements. |
| base `#choose` (2) | `yes` selects the then-list and `no` the else-list, preserving continuation and all semantic parameters. |
| contextual `#choose` (6) | Four exact length shapes and two guarded equality cases implement Test evaluation inside `#choose`; they preserve `REST`, binding, value, program, and branch control. |
| `#branch` (3) | Empty branch resumes `REST`; Return discards following statements; nested If concatenates only its local continuation before `REST`. |
| `#append` (2) | Exhaustive, terminating list concatenation. |
| literal/name `#eval` (3) | Correct typed literals and the sole bound parameter. |
| call `#eval` (2) | `len` is disjoint from non-len calls by guard; pure argument evaluation and module retention are correct. |
| comparison `#eval` (2) | Exact two comparison forms used by the program; maps to the exhaustive Test predicates. |
| subscript `#eval` (2) | Exact integer and `[I:]` forms used by the program. |
| `#distinct3` (1) | Exhaustive pairwise inequality on three integers. |
| `#allTriples` (4) | Exhaustive PString split; recursive tail is exactly the next overlapping window. |
| `#happy` (4) | Exhaustive contract: false below three, all-triples otherwise. |
| `#solution` (1) | Definitional name for the mechanically matched program term; it does not summarize execution. |

The only cell is `<k>` because the submitted subset is pure: it has one
parameter, no assignment, heap, I/O, exceptions in the modeled operations, or
observable allocation. Parameter binding is carried explicitly as `(P,V)`.
The complete function body, lookup, arguments, returns, and recursive calls
execute; no rule directly rewrites `is_happy` or `check_happy_triples` to
`#happy`/`#allTriples`.

Overlaps are benign or disjoint:

- len vs non-len call rules are separated by `F =/=String "len"`;
- matching vs skipped function lookup is separated by name disequality;
- index/drop base vs recursion is separated by zero vs positive;
- `#same` and contextual equality branches are separated by equality vs
  disequality;
- PString shape cases and statement-head cases are constructor-disjoint;
- comparison rules have different operator/form patterns.

All `[total]` functions are genuinely exhaustive: `#len`, `#append`,
`#distinct3`, `#allTriples`, and `#happy`. Recursive equations structurally
descend. No local rule asserts the task answer, introduces a fresh
result-bearing symbol, or turns program execution into an oracle.

The six contextual `#choose` rules deserve special attention because the
candidate says they help symbolic execution. Removing exactly those rules and
rebuilding leaves ordinary execution stuck at
`#choose(#short3("abc"), ...)`. Thus they do not preempt or bypass an existing
fixed evaluator; they are the core evaluation contexts for a Test nested in
`#choose`. Their right-hand sides are direct consequences of the corresponding
constructor/equality cases and preserve the entire state footprint (all seven
arguments; there are no omitted cells). The removal experiment and an
intentionally unsuccessful no-context connection attempt are preserved in
[context-rule-audit.log](evidence/context-rule-audit.log).

The syntax admits some programs outside the justified subset—for example,
duplicate function definitions would expose first-definition lookup, unlike
ordinary Python's later rebinding. No such term can arise from the mechanically
pinned submitted module for any input, so this is a reuse limitation, not an
unsound rule witness on the intended program/input domain. Missing semantics
for unused constructs is permitted in generated-semantics mode.

No rule was found that enables a false conclusion on the intended domain;
therefore there is no unsoundness witness to report.

## 6. Fresh non-vacuity test

The candidate supplied no trusted non-vacuity evidence. I created a new
standalone spec that changes the concrete `"abc"` entry result from true to
false. This input satisfies the original unrestricted entry precondition, and
both Python implementations plus fresh `krun` return true.

The mutant parses/builds (`kprove --dry-run` exits 0). Actual proof:

```text
kprove evidence/spec-vacuity.k \
  --definition verification-audit-kompiled \
  -I /tmp/audit-work/80-is-happy \
  --spec-module AUDIT-SPEC-VACUITY
# exit 1
```

The expected residual is:

```text
WarnStuckClaimState
<k>
  pyBool ( true ) ~> .K
</k>
```

This is a reached false result obligation, not a parse error, timeout,
unrelated crash, or unreachable mutation. See
[spec-vacuity.k](evidence/spec-vacuity.k) and
[nonvacuity.log](evidence/nonvacuity.log).

## 7. Proven versus assumed accounting

### Formally established

Under the freshly built K theory:

- for every finite `PString`, the exact submitted helper returns
  `#allTriples` of that string;
- for every finite `PString`, the exact submitted entry function returns
  `#happy` of that string;
- all six prompt examples have their stated result;
- recursive proof reuse occurs after one-character structural progress;
- the result obligation is discriminating and depends on the actual body.

The formal domain is not finitely bounded and is not narrowed relative to the
source string contract. `PString` actually permits arbitrary Int labels, a
sound broadening for the length/equality-only behavior.

### Trust ledger

| Boundary | Influence and assessment |
|---|---|
| K `INT`, `BOOL`, `STRING` builtins and K v7.1.293 backends | Supply mathematical integer/Boolean/string-token operations and proof execution. Standard low-level trusted base; affects all claims. |
| Trusted `py2mpy.py` | Syntactic bridge from Python AST to constructor term. Byte regeneration plus KORE identity checks the submitted instance, but translator correctness in general remains trusted. Acceptable here. |
| `PString` ↔ Python `str` reading | Interprets each `ch(Int,...)` as a character/code-point sequence. Length, equality, indexing, and tail slicing are audited directly and differentially, not related by a universal machine-checked refinement theorem. Non-fatal concern. |
| `len`, character equality, indexing, and slicing equations | Task-specific external-language primitives. They are exhaustive where used and do not contain the desired all-windows result. Acceptable low-level semantics boundary. |
| Idealized recursion/call stack and allocation | K has unbounded mathematical recursion and no `RecursionError`/memory exception. A concrete CPython divergence appears at length 1000. This affects termination/resource behavior, not the Boolean of normally returning executions. Non-fatal for partial correctness; principal concern. |
| `#distinct3`, `#allTriples`, `#happy` | Proof-side definitional summaries only; truthful total equations and used in destinations, never to replace program execution. Formally transparent. |
| `#solution` | Definitional name only; mechanically identical to trusted generated program. Formally transparent. |
| Differential tests | Finite evidence over 12,858 Python cases and 12 K/Python semantic cases. Supports the instance bridge only; it is not substituted for the K proof. |

There are no fresh opaque result symbols, unconstrained oracles, assumed
lemmas, simplification axioms, proof-local operational bridges, or hidden
reference semantics.

Gate A (real-program soundness) passes: positive closure is fresh, execution is
body-sensitive and result-constraining, and all local proof equations are
truthful. Gate B passes for the requested partial-correctness interpretation:
the unrestricted normal-return domain and property match the source contract;
resource/exceptional termination is explicitly excluded. Gate C has
reproducible artifacts and an explicit trust ledger. The benchmark-level
`CONCERNS` status records the non-machine-checked generated-semantics bridge and
the demonstrated CPython recursion-resource difference; neither makes a false
Boolean conclusion provable for a normally returning execution.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
