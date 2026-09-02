# Independent adversarial audit: 155-even-odd-count

The candidate contains a legitimate, freshly reconstructible partial-correctness
proof of the submitted program over the full mathematical-integer input domain.
The proof is not vacuous, the source program is mechanically pinned, and the
only operational shortcut is an exact-context loop bridge backed by a
bridge-free universal reachability claim.

The concern is narrower: for nonzero inputs the postcondition uses
`evenPos`/`oddPos`, opaque total summary functions whose positive cases do not
reduce to ground integers. Their base cases and decimal recurrences are
mathematically correct and uniquely characterize the requested digit counts,
but the K artifacts do not contain an executable positive definition or a
separate K theorem connecting those summaries to a decimal-string count
function. A direct ground obligation for `12` or `123` therefore remains stuck
at `evenPos(12)`/`oddPos(12)` or `evenPos(123)`/`oddPos(123)`. The bridge from
the recurrence characterization to the human-facing contract is supported by
ordinary mathematics and broad independent differential testing, not by a
machine-reducible K specification. Under the benchmark decision boundary this
is a non-fatal auditability/intent-bridge limitation: `CONCERNS / LEGIT`.

## 1. Input and provenance integrity

Status: **PASS**.

`/audit-input.json` declares:

- problem `155-even-odd-count`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`;
- a mounted trusted semantics tree at
  `/reference/reference-semantics`.

The semantics-mode boundary is consistent: the trusted supplied tree is
present, so this is not an infrastructure contradiction and the
`writing-semantics` route is inapplicable.

I read the launcher records required for `pipeline-v3`:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the complete structured trace. The trace
contains one JSONL file, 867 records, and zero JSON parse errors. The generation
transcript and its claims were treated only as untrusted evidence.

The independent checker
[`stage1_check.py`](/audit-output/evidence/stage1_check.py) used `lstat`-style
type checks and a fresh tree-hash implementation. Its exact command and output
are in
[`stage1-integrity.log`](/audit-output/evidence/stage1-integrity.log).
It established:

- every launcher-required file is a real regular file and every required tree
  is a real directory;
- every declared `container_paths` target is present and neither linked nor an
  unsupported node;
- `/audit-campaign-lock.json` is exactly equal as a JSON object to the
  `audit_campaign` block in `/audit-input.json`;
- the campaign-lock digest is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded digest;
- all recorded direct hashes for the canonical source, prompts, translator,
  run/task/result manifests, invocation, metrics, usage, prompt, last message,
  and output log match the mounted bytes;
- the candidate prompt and translator are byte-identical to their trusted
  mounts;
- the generation-result hash for the sole trace file is
  `fd1a587df26029d02e0ab113fe48e7172756446739c09fa5487ace74e17f2c63`;
- the independently reconstructed pipeline tree hash is
  `f57128fca4941f256460299dad5dadf88f7bd2f207b89f59bd953beb9471c7f6`
  for the trace and
  `694bf92870c0ec0716a05cdec0d79cc5e5e94527637abe3b3b8af366671c94b0`
  for the candidate, matching `usage.json` and the generation
  invocation/result records respectively.

For the supplied-semantics integrity boundary, the checker recursively
inventoried relative paths, node types, and SHA-256 file digests. The candidate
and trusted trees contain exactly the same directory and 24 files, no
additional or missing path, no mistyped entry, no symlink, and no content
difference. Their independently reconstructed pipeline tree digest is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the task manifest. Thus the fixed semantics is intact; this does not
bless the proof-local rules in `verification.k`.

Full launcher records are preserved in
[`provenance-records.log`](/audit-output/evidence/provenance-records.log).
The transcript/trace parser and bounded summary are
[`generation_evidence_summary.py`](/audit-output/evidence/generation_evidence_summary.py)
and
[`generation-records.log`](/audit-output/evidence/generation-records.log).
No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **PASS**.

### Contract

The trusted prompt asks `even_odd_count(num)` to accept an integer and return a
two-tuple containing, respectively, the number of even and odd decimal digits
of its absolute value. Thus `0` contributes one even digit; a minus sign is not
a digit. The documented examples are `-12 -> (1, 1)` and
`123 -> (1, 2)`.

The trusted canonical implementation converts `abs(num)` to a decimal string,
iterates every character, and counts the digit parity. The submitted
`solution.py` implements an equivalent arithmetic algorithm:

1. replace `num` by `abs(num)`;
2. return `(1, 0)` for zero;
3. for positive `num`, add `1 - num % 2` to the even count, add
   `num % 2` to the odd count, and replace `num` by `num // 10`;
4. return the counters.

This is defined for arbitrary Python integers. There is no collection-valued
input, so an “empty input” case is inapplicable; integer zero is the relevant
empty-decimal-loop boundary.

### Trusted regeneration

In a scratch copy, the exact command recorded in
[`translator-regeneration.log`](/audit-output/evidence/translator-regeneration.log)
ran the trusted `/reference/py2mpy.py` on the submitted `solution.py`.
The regenerated and submitted `solution.mpy` are byte-identical and both have
SHA-256
`8707fdc3542a46400bf6313e0f35b4689196c8ccbe9ec12390cf07b58ba0c5c0`.

### Independent differential test

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted canonical entry point and the submitted entry point from separate
paths. It checks:

- both documented examples;
- 31 sign, zero, parity, and decimal-length boundaries;
- every integer from `-100000` through `100000`;
- 2,000 deterministic random integers of 1 through 100 digits, seed 155;
- an independent direct contract property computed from the decimal digits,
  including that the two counts sum to the decimal digit length.

The recorded run in
[`differential.log`](/audit-output/evidence/differential.log) made 202,034
comparisons with zero canonical mismatches and zero direct-property failures.
This finite test is evidence of program/canonical fidelity, not a replacement
for the K proof.

## 3. Clean proof reconstruction

Status: **PASS**.

All execution occurred below
`/tmp/audit-work/155-even-odd-count/work`. The scratch copy contains candidate
source artifacts and a copy of the trusted reference semantics; no
candidate-provided `*-kompiled` directory or cache was copied. The copy command
and resulting source-only tree are in
[`scratch-copy.log`](/audit-output/evidence/scratch-copy.log). The live
toolchain is K `v7.1.293`, recorded in
[`toolchain.log`](/audit-output/evidence/toolchain.log).

### Concrete definition

The fresh LLVM command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0; see
[`llvm-build.log`](/audit-output/evidence/llvm-build.log). A freshly translated
concrete harness was mechanically checked to contain the exact submitted
function AST and then run with:

```text
krun audit-concrete-tests.mpy --definition audit-runtime-kompiled
```

It exited 0 with final `.K`, `NoExc`, and exit code 0 after the examples, zero,
all-even, all-odd, and embedded-zero assertions; see
[`concrete-krun.log`](/audit-output/evidence/concrete-krun.log).

### Bridge-free proof definition

The fresh Haskell definition built from `verification.k` with exit 0:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-loop-kompiled
```

See
[`haskell-loop-build.log`](/audit-output/evidence/haskell-loop-build.log).
The identity spec was regenerated from the freshly translated program and was
byte-identical to the submitted identity spec; see
[`identity-regeneration.log`](/audit-output/evidence/identity-regeneration.log).

Both bridge-free positive claims independently closed:

| Claim | Command summary | Exit | Result |
|---|---|---:|---|
| `LOOP-PROOF.loop-tail` | `kprove spec.k --definition audit-loop-kompiled --spec-module LOOP-PROOF` | 0 | `#Top` |
| `IDENTITY-SPEC.translated-program-identity` | `kprove audit-identity-spec.k --definition audit-loop-kompiled --spec-module IDENTITY-SPEC` | 0 | `#Top` |

The bounded outputs and exact commands are
[`loop-proof.log`](/audit-output/evidence/loop-proof.log) and
[`identity-proof.log`](/audit-output/evidence/identity-proof.log).

### Extended proof definition

The fresh Haskell definition built from `verification-with-lemma.k` with exit
0:

```text
kompile verification-with-lemma.k --backend haskell \
  --main-module VERIFICATION-WITH-LEMMA --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

See
[`haskell-extended-build.log`](/audit-output/evidence/haskell-extended-build.log).
Both extended positive claims independently closed:

| Claim | Command summary | Exit | Result |
|---|---|---:|---|
| `SPEC.even-odd-count` | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC` | 0 | `#Top` |
| `CONTEXT-SPEC.caller-continuation` | `kprove context-spec.k --definition audit-verification-kompiled --spec-module CONTEXT-SPEC` | 0 | `#Top` |

The exact evidence is
[`target-proof.log`](/audit-output/evidence/target-proof.log) and
[`context-proof.log`](/audit-output/evidence/context-proof.log).
Every candidate-designated positive proof/audit claim was therefore rebuilt and
rerun successfully.

## 4. Adequacy and real-program pinning

Status: **PASS with a non-fatal evidence limitation**.

### Plain-language claims

`LOOP-PROOF.loop-tail` starts at the exact loop-and-return suffix of the
submitted function. Its state contains nonnegative remaining magnitude `N`,
integer counters `E` and `O`, the exact local/global/builtin scopes, no heap,
the exact saved caller frame, no pending return or exception, and exit code
zero. It says the suffix returns `(E + evenPos(N), O + oddPos(N))`, restores
the caller environment/scopes/stack, and resumes the arbitrary saved
continuation `CONT`.

`SPEC.even-odd-count` has no additional `requires` clause: `N:Int` ranges over
all mathematical integers. From the standard empty-heap, empty-stack module
state with `"even_odd_count"` bound to `evenOddClosure`, it says the call
returns an integer pair `(decEven(N), decOdd(N))` without changing the other
observable cells.

The identity claim says that loading the exact `Module(FuncDef(...))` term
regenerated from `solution.mpy` installs precisely `evenOddClosure`. The context
claim says a caller continuation after a call is preserved: the returned tuple
is discarded by `Expr`, and the following expression produces 7.

### Satisfiable preconditions

The whole-function precondition is realized, for example, by `N = -12` with
the exact initial cells written in the claim. The loop precondition is realized
by `N = 12`, `E = 0`, `O = 0`, `C = evenOddClosure`,
`B = builtinsScope`, and `CONT = .K`; `12 >=Int 0` and all map/frame/cell
requirements are concrete. The identity and context entry states are likewise
the concrete standard configurations shown in their claims. The successful
zero ground claim in
[`ground-zero-proof.log`](/audit-output/evidence/ground-zero-proof.log)
provides a machine-executed entry-state witness.

### Program pinning

The target does not begin with the whole `solution.mpy` module, but pinning is
mechanical and sufficient:

1. the trusted translator regenerated `solution.mpy` byte-for-byte;
2. the generated identity spec embeds that exact constructor term under
   `#loadAll`;
3. the bridge-free identity proof shows that fixed module-loading semantics
   produces the binding `evenOddClosure`;
4. `evenOddClosure` expands to `closureVal("num", evenOddBody, 0)`;
5. `evenOddBody` expands to the exact translated body, including the docstring,
   `abs` call, initializations, zero branch, while condition, all three loop
   assignments, and final return.

Thus the target executes the submitted binding and body, not a merely
name-matched substitute.

A separate body-sensitivity reconstruction regenerated a mutant whose even
update was changed from `even + 1 - num % 2` to `even + num % 2`, embedded the
mutated constructor body under `#loadAll`, and called it on 2. The changed body
actually remained in the final closure, returned `(0,0)`, and failed the
expected `(1,0)` obligation with exit 1 and `WarnStuckClaimState`. See
[`body-mutation-regeneration.log`](/audit-output/evidence/body-mutation-regeneration.log)
and
[`body-sensitivity-proof.log`](/audit-output/evidence/body-sensitivity-proof.log).
This is a genuine program-term mutation, not a change to an unused external
file.

### Concrete substitution and limitation

For `N = 0`, the K target reduces to `(1,0)` and a direct ground claim closes
with `#Top`. Both Python implementations also return `(1,0)`.

For `N = -12`, the K target reduces only to
`(evenPos(12), oddPos(12))`; both Python implementations return `(1,1)`.
For `N = 123`, it reduces only to
`(evenPos(123), oddPos(123))`; both Python implementations return `(1,2)`.
The direct ground K claims fail at those residual equalities, as recorded in
[`ground-negative-proof.log`](/audit-output/evidence/ground-negative-proof.log)
and
[`ground-positive-proof.log`](/audit-output/evidence/ground-positive-proof.log).

This is not an opposite result or a domain restriction. The recurrence axioms
uniquely determine the expected values, but the positive summaries are
intentionally opaque and the prover cannot normalize them to ground integers.
That is the reason for `CONCERNS` rather than `PASS`.

## 5. Rule-by-rule static soundness review

Status: **PASS**; no false-conclusion witness was found for a rule contributing
to the proof.

### Exhaustive inventory

[`k_inventory.py`](/audit-output/evidence/k_inventory.py) scanned every K source
used by the reconstruction. The complete source-derived inventory is
[`rule-inventory.tsv`](/audit-output/evidence/rule-inventory.tsv), with source,
line, kind, attributes, origin class, and the full normalized declaration or
rule. It covers 32 source files and 1,158 records:

- 720 rules;
- 230 syntax declarations;
- 5 contexts;
- 1 configuration;
- 7 claims;
- all modules, imports, and requires.

Attributes inventoried include 149 `function`, 110 `total`, 25 `symbol`, 23
`no-evaluators`, 12 `simplification`, 46 `priority`, 36 `concrete`, 26
`owise`, all strictness declarations, and all macros. There are no local
`functional`, `trusted`, or `anywhere` declarations. The inventory command and
counts are in
[`rule-inventory-command.log`](/audit-output/evidence/rule-inventory-command.log).

The 695 rules and 227 syntax declarations below
`reference-semantics/` are the launcher-selected supplied base, not
candidate-authored semantics. Every one is present unchanged from the trusted
tree. I classified all supplied rows as follows:

- rules on sorts/constructors that cannot occur in the submitted term are
  non-contributing supplied-base rules;
- opaque supplied symbols for floats, sorting, MD5, and other unused operations
  have no data/control path to this theorem;
- generic rules reachable from this program were traced through their complete
  state and are listed below.

This disposition accounts for every supplied row without treating the baseline
as permission for proof-specific conclusions.

### Used-construct mapping

| Submitted construct | Declaration/evaluation rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `syntax.k`; `core.k` `#loadAll` and sequencing; `functions.k` closure creation |
| `Name` | `core.k` `#look`, exact parent-chain lookup, builtins at scope `-1` |
| docstring `Str` and `Expr` | `str.k` ASCII code conversion; `controls.k` value discard |
| `Call(Name("abs"), ...)` | `call.k` callee-before-arguments routing; `core.k` left-to-right arguments and builtin binding; `builtins.k` `absInt` |
| `Assign` | syntax strictness evaluates RHS first; `controls.k` updates the current scope |
| `Int` | `core.k` literal rule |
| `Compare`/`CmpOp` | ordered contexts in `operators.k`; integer cases in `int.k` |
| `If` | strict condition and `truthy`/`#branch` rules in `controls.k` |
| `While` | `While -> #while`, condition evaluation, guarded body/exit, and loop label in `controls.k` |
| `BinOp +`, `-`, `%`, `//` | `seqstrict(2,3)` in `syntax.k`; dispatch in `operators.k`; integer equations and `pyMod` in `int.k` |
| `TupleExpr` | left-to-right `#evalArgs` and tuple construction in `tuple.k` |
| `Return`, `#endcall`, frame pop | strict return evaluation, saved continuation/frame restoration, scope removal, and return reset in `functions.k` |

The configuration explicitly contains `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The claims and bridge mention every one. For this program no
allocation, mutation outside the local scope, output, or exception-producing
operation occurs. The divisors are concrete positive 2 and 10, so no
division-by-zero or negative-divisor semantic gap is reachable. K integers are
unbounded, matching Python's relevant integer behavior.

Evaluation order is faithful: assignment conditions/RHSs are evaluated before
state updates, binary operands and call arguments are left-to-right, the while
condition is reevaluated each iteration, and `Return` discards the remainder of
the callee before restoring the saved caller continuation. Relevant guards are
disjoint or agreeing: integer comparison/operator cases are operator-disjoint;
while truthy/false guards are complements; zero/positive/negative summary
guards partition integers; duplicate zero summary rules agree.

### The 24 proof-local rules

All proof-local rows in `verification.k` were reviewed:

1. `evenOddBody` and `evenOddClosure` are terminating, non-overlapping
   definitional expansions. The identity proof checks their exact connection
   to the regenerated source term.
2. `evenPos(0)=0` and `oddPos(0)=0`, including the duplicate guarded
   simplification forms, agree on their overlap.
3. The two negative rules map `N < 0` once to `-N > 0`; they terminate and
   merely totalize the summary over negative arguments.
4. The six `decEven`/`decOdd` equations have mutually exclusive zero,
   positive, and negative guards and implement absolute-value digit summaries,
   with the correct special case for decimal zero.
5. The six absolute-value equality simplifiers are true: an integer with
   `absInt(N)=0` is zero, while for a nonzero integer the appropriate
   positive-magnitude summary is selected in either sign branch.
6. The four recurrence simplifiers are true for every `N > 0` and arbitrary
   accumulator. Let `d=N mod 10` and
   `q=(N-d)/10`. Then `0 <= d <= 9`, `q < N`,
   and the parity of `N` equals the parity of its last decimal digit because
   10 is even. Hence the last digit contributes
   `1-(N mod 2)` to the even count and `N mod 2` to the odd count, with the
   remaining count at `q`. The reverse-oriented rules assert the same
   equality, not a different fact.

The recurrence descends strictly on positive integers, so together with the
zero base it uniquely characterizes the decimal digit counts. A finite
independent interpretation check exercised 3,400,006 instances of every
proof-local summary equation over public inputs `[-100000,100000]`, positive
recurrences `[1,100000]`, and five accumulator values, with zero mismatch; see
[`proof_rule_math_check.py`](/audit-output/evidence/proof_rule_math_check.py)
and
[`proof-rule-math.log`](/audit-output/evidence/proof-rule-math.log). This
finite check supports, but does not replace, the preceding general
mathematical argument.

### Operational bridge

`verification-with-lemma.k` contains exactly one rule, at priority 40. It is an
operational bridge, not merely a function equation. Its complete match is:

- the exact submitted `#while` condition and three-statement body;
- the exact final `Return(...) ~> #endcall` suffix;
- the same arbitrary `CONT` stored in the sole caller frame and restored on
  the RHS;
- exact callee/module/builtin scopes;
- `N >= 0`;
- empty heap and unchanged heap counter;
- `noRet`, `NoExc`, and exit code 0;
- the exact environment, scope-location, stack, scope-removal, and result
  transitions of ordinary return/pop.

The bridge-free `LOOP-PROOF.loop-tail` claim has the same complete match
domain, continuation quantification, guard, state footprint, and result.
It was proved using `VERIFICATION`, which does not import the bridge. Thus the
bridge match domain is not broader than its justification domain. Priority 40
only selects this already-justified exact transition.

Control sensitivity was checked in two ways. The independently rerun context
claim puts a distinct observable expression after the call and proves it is
preserved. The body mutation changes the displaced loop body; the bridge no
longer matches, ordinary fixed execution returns the mutant result, and the
old result obligation fails. There is no witness that the bridge discards or
fabricates a continuation, return, exception, state update, allocation, or
binding.

### Soundness conclusion

No proof-local rule is globally false on its guard under the stated summary
interpretation, no rule replaces the program with an unconstrained oracle, no
used source construct is silently fabricated, and no priority overlap enables
a false result. Accordingly I do not label any inventoried rule unsound. The
opaque positive summaries are instead recorded as the narrower adequacy and
machine-auditability gap already described.

## 6. Fresh non-vacuity test

Status: **PASS**.

I did not rely on the candidate `spec-vacuity.k`. The reviewer-authored
[`fresh-vacuity-spec.k`](/audit-output/evidence/fresh-vacuity-spec.k) uses the
satisfiable standard entry state and concrete input zero, but changes the
required result from the true `(1,0)` to the false `(2,0)`.

First,

```text
kprove audit-fresh-vacuity-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FRESH-VACUITY-SPEC --dry-run
```

parsed and built the spec successfully with exit 0; see
[`fresh-vacuity-build.log`](/audit-output/evidence/fresh-vacuity-build.log).
The actual proof command then exited 1 with `WarnStuckClaimState`. Its residual
is the reachable final tuple `(1,0)`, which fails to unify with the false
destination `(2,0)`; see
[`fresh-vacuity-proof.log`](/audit-output/evidence/fresh-vacuity-proof.log).
This is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash.

## 7. Proven versus assumed accounting

Status: **Gates A and B pass; Gate C has a documented non-fatal limitation**.

### What is machine-proved

Under the supplied MPY semantics plus the audited proof-local mathematical
rules:

- loading the trusted regeneration of `solution.mpy` installs exactly
  `evenOddClosure`;
- for every `N >= 0` and arbitrary counters/continuation in the exact loop
  state, fixed execution of the exact loop-and-return suffix produces
  `(E + evenPos(N), O + oddPos(N))` and restores the caller state;
- for every mathematical integer `N` in the standard entry state, partial
  correctness of the exact submitted call gives
  `(decEven(N), decOdd(N))`;
- a following caller continuation is preserved;
- the result obligation discriminates against a reachable false result.

The theorem is not bounded to examples or finitely many sizes. The entry claim
has no strengthening that narrows the HumanEval integer domain.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted prompt, canonical source, and translator mounts | Defines intent and the Python-to-MPY term | Integrity and direct hashes pass; trusted by benchmark |
| Supplied reference semantics | All execution, state, binding, and control behavior | Exact trusted-tree equality passes; used rules are adequate for this program |
| K v7.1.293 backend and hooked unbounded integer primitives, including `absInt`, integer arithmetic, equality, maps, and lists | Symbolic execution and arithmetic | Normal low-level proof-system boundary; no task answer is embedded in these primitives |
| `evenOddBody` / `evenOddClosure` | Binds target claim to program | Exact trusted regeneration plus bridge-free identity proof |
| `evenPos`, `oddPos`, `decEven`, `decOdd` and their 16 mathematical/base/recurrence rules | Determines the returned value and invariant | Program-derived definitional summary; equations are generally true and descending, but positive ground values remain opaque in K |
| One loop operational bridge | Replaces exact loop suffix during the whole-function proof | Acceptable: exact state/context match and bridge-free universal connection theorem; body and continuation sensitivity pass |
| Python differential/property suite | Program/canonical and summary-to-contract evidence on tested inputs | 202,034 finite cases, zero mismatch; empirical only |
| Proof-rule interpretation suite | Finite check of proof-local equations | 3,400,006 equation instances, zero mismatch; empirical only |
| Partial-correctness interpretation | Termination is outside the theorem statement | Expected Kit boundary; no claim of a separate termination proof |
| Unused supplied opaque symbols (float, sort, MD5, etc.) | None on reachable target terms | Irrelevant to this theorem |

### Why the final result is `CONCERNS / LEGIT`

Gate A passes: the exact program is executed or connected by bridge-free
claims, the sole bridge preserves all observable state and control, the
proof-local equations are truthful on their complete guards, a satisfying
state exists, body sensitivity passes, and a fresh false-result mutation is
rejected.

Gate B passes for scope: `N:Int` covers the complete source-contract integer
domain, the MPY integer model is adequate for the used operations, and the
recurrence mathematically characterizes exactly the requested even/odd decimal
digit counts.

The concern is Gate C/auditability rather than legitimacy. For positive
arguments the K theory cannot itself normalize or directly prove a concrete
result such as `evenPos(12)=1`; that last summary-to-human-contract step is an
ordinary mathematical interpretation backed by finite differential evidence.
This does not admit a witnessed false result or narrow the theorem, so it is
not `FAIL / NOT_LEGIT`. It is nevertheless a material enough evidence
limitation to withhold an unqualified `PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
