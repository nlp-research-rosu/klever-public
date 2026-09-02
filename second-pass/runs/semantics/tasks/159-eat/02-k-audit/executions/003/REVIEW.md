# Adversarial proof audit — HumanEval 159 `eat`

The candidate contains a legitimate partial-correctness proof of the submitted
program over the complete stated input domain. I independently rebuilt both K
definitions, proved each positive claim separately, mechanically pinned the
proof-local closure to the trusted regeneration of `solution.mpy`, reviewed the
source rules and declarations, and obtained meaningful failures from both a
body mutation and an off-by-one postcondition mutation.

## 1. Input and provenance integrity

The launcher declares `record_layout: legacy-selected-stage1`,
`condition: semantics`, and `semantics_mode: SUPPLIED_SEMANTICS` in
`/audit-input.json`. `/reference/reference-semantics` is present, as required
for this mode.

The independent checker in
[`evidence/check_provenance.py`](evidence/check_provenance.py) established:

- `/audit-campaign-lock.json` is byte-hash
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash recorded in `/audit-input.json`, and its parsed object
  exactly equals the `audit_campaign` block.
- The independently computed SHA-256 values for the canonical source, trusted
  prompt, trusted translator, candidate prompt, candidate translator,
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the present `usage.json` all match
  their launcher-recorded hashes.
- All eight required records for `legacy-selected-stage1` are regular,
  readable files. Historical runtime metrics are not required for this layout
  and were not reconstructed.
- The trusted and candidate semantics trees each contain the same 25 relative
  entries (one directory and 24 files beneath the root), with identical
  entry types, sizes, and per-file hashes. There are no symlinks, missing
  entries, extra entries, or changed entries. Candidate `prompt.py` and
  `py2mpy.py` also match the trusted mounts exactly.
- The one structured trace file has its recorded SHA-256, contains 125 valid
  JSON lines, and has the expected event structure. The complete
  `codex-output.log` is valid readable UTF-8. I inspected these records only as
  untrusted generation history; their prior `#Top` claims were not accepted as
  proof evidence.
- All five required candidate proof artifacts are present as regular readable
  files.

The full output is
[`evidence/provenance_integrity.log`](evidence/provenance_integrity.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For integers `number`, `need`, and `remaining`, each in `[0,1000]`, the rabbit
eats `min(need, remaining)` carrots. The function must return:

```text
[number + min(need, remaining), remaining - min(need, remaining)]
```

Equivalently, if `need <= remaining`, it returns
`[number + need, remaining - need]`; otherwise it returns
`[number + remaining, 0]`. This is the behavior in
`/reference/prompt.py:2-29` and `/reference/canonical.py:35-38`.

`/candidate/solution.py:1-4` implements those two branches. Its second return
is syntactically after the `if` rather than inside an `else`, but the first
branch returns, so the control behavior is equivalent.

### Trusted regeneration

I ran the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py`. The regenerated file and submitted `solution.mpy` are
byte-identical, both with SHA-256
`49f9697d0fa8809c3144fc5b812d49e68db0cdbb56b74617e8c089e0a8c6e78a`.
See [`evidence/translator_regeneration.log`](evidence/translator_regeneration.log).

### Independent differential execution

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical function and candidate function independently. It checks:

- all four documented examples;
- eleven explicit zero, maximum, and branch-boundary cases;
- every `(need, remaining)` pair in `[0,1000]^2` for
  `number` equal to `0`, `1`, `999`, and `1000`; and
- 100,000 deterministic samples from the complete contract cube.

All 4,108,019 comparisons matched. There is no meaningful “empty” input for a
three-integer signature. The command and result are in
[`evidence/differential_test.log`](evidence/differential_test.log). This is
finite program-fidelity evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/159-eat`. I did not use a candidate-provided definition or
cache; none is part of the proof reconstruction. Fresh outputs were written
under `/tmp/audit-work/159-eat/fresh`.

### Concrete definition

The supplied semantics was freshly compiled with LLVM as `MPY-KRUN`.
`kompile` exited 0; see
[`evidence/kompile_llvm.log`](evidence/kompile_llvm.log).

[`evidence/make_concrete_harness.py`](evidence/make_concrete_harness.py)
appends eleven assertions to the exact submitted `Module(...)` term, preserving
the submitted function-definition prefix. `krun` exited 0 with:

- `<k> .K </k>`;
- `<exc> NoExc </exc>`;
- `<exit-code> 0 </exit-code>`; and
- the expected normal and boundary list results in the heap.

See [`evidence/krun_concrete.log`](evidence/krun_concrete.log). Concrete
execution is supporting evidence only.

### Proof definition and positive claims

`/candidate/verification.k` was freshly compiled with the Haskell backend as
module `EAT-VERIFICATION`. The build exited 0:
[`evidence/kompile_haskell.log`](evidence/kompile_haskell.log).

The two candidate claims are unlabeled, so
[`evidence/split_positive_claims.py`](evidence/split_positive_claims.py)
mechanically copied each exact claim into a one-claim module. I ran:

- branch `need <= remaining`: `#Top`, exit 0;
- branch `remaining < need`: `#Top`, exit 0; and
- the unmodified combined `spec.k`: `#Top`, exit 0.

The bounded logs are
[`evidence/kprove_branch_1.log`](evidence/kprove_branch_1.log),
[`evidence/kprove_branch_2.log`](evidence/kprove_branch_2.log), and
[`evidence/kprove_all.log`](evidence/kprove_all.log). Exact commands are
collected in [`evidence/COMMANDS.md`](evidence/COMMANDS.md).

The compiler emitted unused-variable warnings in unrelated string rules. The
LLVM build also reported incomplete total-function coverage for unrelated
`mapStrVS`, float helper, `joinCodes`, and out-of-bounds `valSeqAt` cases.
None occurs in this integer/call/list path, none contributes to claim closure,
and no warning was treated as a success signal.

## 4. Adequacy and real-program pinning

### Plain-language claims

The first claim, `/candidate/spec.k:6-34`, assumes all three arguments are
integers in `[0,1000]` and `need <= remaining`. Starting from a clean caller
state with `eat` bound to `eatClosure`, it requires the call to finish at
`ref(0)`, with heap location 0 containing exactly:

```text
[NUMBER + NEED, REMAINING - NEED]
```

It also requires the caller environment, scopes, stack, return state,
exception state, and exit code to be restored or preserved as shown.

The second claim, `/candidate/spec.k:36-64`, has the same contract bounds and
assumes `remaining < need`. It requires exactly:

```text
[NUMBER + REMAINING, 0]
```

The integer order is total, so `need <= remaining` and `remaining < need`
partition the whole contract domain. There is no finite-size narrowing beyond
the source contract itself.

Both preconditions are satisfiable. For `(5,6,10)`, branch one produces
`[11,4]`; for `(2,11,5)`, branch two produces `[7,0]`. Canonical Python,
candidate Python, and the substituted K heap expressions agree; see
[`evidence/claim_witnesses.log`](evidence/claim_witnesses.log).

### Program identity

The entry claims do not reload the complete `Module`; they install the
function binding and invoke it through the ordinary `Call(Name("eat"), ...)`
rules. This is permitted only if that installed closure is the submitted
function.

That connection was checked in three independent ways:

1. Trusted translation regenerates the submitted `solution.mpy` byte-for-byte.
2. [`evidence/constructor_pinning.py`](evidence/constructor_pinning.py)
   derives the only `FuncDef` and its closure body from the trusted translator's
   in-memory constructor tree, extracts the candidate `eatClosure` right-hand
   side, normalizes only explicit `.Stmts` list terminators and insignificant
   surface whitespace, and obtains identical constructor terms. Preserved terms
   are
   [`evidence/expected-closure.kterm`](evidence/expected-closure.kterm) and
   [`evidence/actual-closure-raw.kterm`](evidence/actual-closure-raw.kterm).
3. The generated pinning claim closes with `#Top` and exit 0. It is reported as
   trivial after function preprocessing because `eatClosure` is a K function;
   the independent normalized constructor comparison prevents treating that
   warning as identity evidence by itself. See
   [`evidence/constructor_pinning.log`](evidence/constructor_pinning.log).

The claim therefore executes the exact submitted body: comparison, selected
branch, integer arithmetic, list construction, and return control all run
through the fixed semantics. It does not substitute a result oracle.

### Body sensitivity

As a separate operational-sensitivity check, I changed the true-branch body
inside the actually executed `eatClosure` from `number + need` to
`number - need`, rebuilt a fresh Haskell definition successfully, and reran the
original positive spec. The proof exited 1 with `WarnStuckClaimState`; its
residual requires the false equality:

```text
NUMBER -Int NEED = NUMBER +Int NEED
```

The mutation and logs are
[`evidence/verification-body-mutant.k`](evidence/verification-body-mutant.k),
[`evidence/body_mutation_kompile.log`](evidence/body_mutation_kompile.log), and
[`evidence/body_mutation_kprove.log`](evidence/body_mutation_kprove.log).
This changes the term executed by the claim, not merely an external source
file.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/inventory_k_rules.py`](evidence/inventory_k_rules.py) inventoried
all source-level declarations in the assembled supplied semantics, every
helper K file, and `verification.k`. The line-addressable inventory and
per-entry decision are in
[`evidence/rule_inventory.md`](evidence/rule_inventory.md):

- 25 K files;
- 930 entries;
- 228 `syntax` declarations;
- one configuration;
- five explicit contexts;
- 696 rules;
- 147 entries declaring functions;
- 107 entries with `total`;
- 25 entries with `symbol`, of which 22 have `no-evaluators`;
- 45 entries containing priority rules;
- 26 entries containing `owise`;
- 35 entries containing concrete rules; and
- no source-level `[simplification]` or `[functional]` declarations.

The inventory includes declarations and rules outside the submitted program.
For each such entry, it records whether it is a fixed declaration, a fixed
unused fragment, a concrete-only rule excluded from the proof module, or an
opaque fixed-semantics boundary. I found no concrete or symbolic witness by
which an unused rule can enable a false conclusion for this program and domain;
accordingly, I do not label those rules unsound.

### Used syntax and execution path

Every constructor in `solution.mpy` is mapped to its declaration, evaluation
rules, overlap analysis, and cell footprint in
[`evidence/semantic_path_map.md`](evidence/semantic_path_map.md). The executed
path is:

```text
Name lookup → callee evaluation → left-to-right Int arguments
→ fresh closure frame and parameter binding
→ integer <= comparison → If branch
→ left-to-right integer + / - expressions
→ list allocation → Return → frame pop
```

Relevant conclusions from the source review:

- `Call` selects the closure stored under `eat`; no math, md5, method, builtin,
  or other higher-priority call interception matches.
- The fresh callee scope starts at location 1, absent from the claim's scope
  map. Parameter binding and local lookup therefore have concrete bindings and
  cannot take cell-closure priority rules.
- `Compare` sees two integers and selects the fixed integer `<=` equation.
  Ref-specific comparison rules cannot match.
- Both `BinOp` operands are integers. The ordinary operator dispatcher selects
  the fixed `+Int` and `-Int` equations; list, float, and ref alternatives do
  not overlap.
- `ListExpr` evaluates elements left-to-right, constructs the exact two-element
  `ValSeq`, and allocates it at the fresh heap location constrained by the
  postcondition.
- `Return` records the constructed ref, discards the remaining function-body
  continuation as Python return must, pops exactly one call frame, restores
  the caller's environment/scope state, and leaves the allocated list in the
  heap. `<exc>` and `<exit-code>` stay normal.
- Python integers and the used K integers are unbounded. Inputs are at most
  1000 and the maximum returned total is 2000, so there is no representation
  mismatch.

### Proof-local extension

`/candidate/verification.k:9-27` contains the entire local extension inventory:

- `eatClosure`: a zero-argument `Val` function symbol; and
- one equation mapping it to the exact submitted closure.

This is a definitional summary, not an operational bridge. It does not replace
the body execution, introduce abrupt control, read or write a cell, or invent a
result. Its equation is ground, terminating, fully covered, and has no overlap.
The result-bearing values are computed by the fixed semantics after the
closure is invoked.

### Opaque and total symbols

The fixed semantics declares these 22 explicit `no-evaluators` primitives:

```text
intFloatDiv divII floatMod floatLt absF
subF divF addF mulF powF gtF eqF decStrToF
divFloatIntV intToF truncF roundF roundFN sqrtF
sortVS sortKeyVS md5hexCodes
```

It also declares `floorFI`, `toF`, and `ceilF` as total symbolic helpers whose
equations are concrete-only. None of these 25 symbols occurs in the submitted
program, either postcondition, or any reachable proof state. They influence no
branch, result, state, exception, or control decision in this theorem.

Likewise, the unrelated incomplete-totality compiler warnings are an evidence
limitation of the broad supplied language subset, not a route to this proof.
The used helpers (`appendVal` and `vals2valSeq`) have exhaustive structural
equations over the concrete finite argument list.

Static Gate A passes. No rule was found unsound on the theorem's intended
domain, so there is no claimed-unsound rule requiring a false-conclusion
witness.

## 6. Fresh non-vacuity test

The candidate did not supply a vacuity test that I relied on. I generated a
fresh spec that changes only the first branch's first result component:

```text
NUMBER +Int NEED
```

to:

```text
NUMBER +Int NEED +Int 1
```

The witness `(NUMBER, NEED, REMAINING) = (5,6,10)` satisfies that branch's
precondition. The real result is `[11,4]`; the mutated postcondition demands
`[12,4]`.

The mutation is preserved as
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k). Its K dry run exited 0,
showing that it parsed and compiled. The actual proof then exited 1 with
`WarnStuckClaimState` and the expected unmet equality:

```text
NUMBER +Int NEED +Int 1 = NUMBER +Int NEED
```

See
[`evidence/non_vacuity_dry_run.log`](evidence/non_vacuity_dry_run.log) and
[`evidence/non_vacuity_kprove.log`](evidence/non_vacuity_kprove.log). The
failure is a reachable result obligation, not a parser error, timeout, missing
import, or unrelated crash. The proof is discriminating.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the supplied `MPY` semantics and the exact entry configurations in
`spec.k`, for every integer triple satisfying the HumanEval bounds:

- if `need <= remaining`, the submitted closure call reaches a normal final
  state whose returned ref denotes exactly
  `[number + need, remaining - need]`; and
- if `remaining < need`, it reaches a normal final state whose returned ref
  denotes exactly `[number + remaining, 0]`.

The claims constrain the observable result and the relevant control/state
cells. Together they cover the complete source-contract domain. There are no
loops, circularity claims, auxiliary summaries, or bounded unrollings.

### Trust ledger

| Boundary | Influence on this theorem | Assessment |
|---|---|---|
| K 7.1.293 parser, kompiler, Haskell backend, and reachability logic | All machine-checking | Standard unavoidable proof-tool trust. Version and exit evidence are in [`evidence/tool_versions.log`](evidence/tool_versions.log). |
| K builtin `Int`, `Bool`, `Map`, `List`, equality, and generated strictness/cooling machinery | Integer arithmetic/order, scope/heap maps, sequencing | Acceptable low-level semantics boundary; the used equations were statically checked and concretely exercised. |
| Supplied `MPY` semantics | Calls, frames, branches, list allocation, return | Fixed semantics selected by the benchmark. Its candidate copy exactly matches the trusted mount. All source declarations/rules are inventoried; the used fragment has no identified mismatch. |
| Trusted `py2mpy.py` | Source-to-constructor translation | Explicit trusted input. Fresh regeneration is byte-identical, and the closure constructor is mechanically compared. |
| `eatClosure` | Chooses the program body executed by the claims | Not an assumption or oracle: one exact definitional equation, pinned to the trusted translation and body-sensitive. |
| 25 fixed opaque/symbolic primitives | None | Unreachable and absent from the theorem; no dependent claim. |
| Natural-language contract to canonical implementation | Intent interpretation | Direct static agreement, examples, branch partition, and independent finite differential evidence. No differential result is promoted to a universal K theorem. |
| K model to full CPython | Language adequacy | Informal only in general, but the used fragment consists solely of unbounded integer operations, deterministic control, local calls, and list construction; its operational rules were reviewed directly. |

### Gate status and decision

- Gate A, real-program soundness: **PASS**. The real closure body executes,
  result and state are constrained, body sensitivity holds, and the false
  postcondition is rejected.
- Gate B, intent adequacy: **PASS**. The two claims exactly partition and cover
  all integer inputs allowed by the HumanEval source contract.
- Gate C, trust and auditability: **PASS**. Commands, scripts, mutations, and
  bounded logs are preserved under `evidence/`; finite evidence is described
  only as finite evidence.

There is no material adequacy gap, narrowed domain, unconstrained result,
substituted program, or unsound proof-local rule. The candidate is therefore a
legitimate partial-correctness proof.

VERDICT: PASS
LEGITIMACY: LEGIT
