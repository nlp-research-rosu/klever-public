# Independent adversarial review: 156-int-to-mini-roman

This review treats every candidate artifact and generation trace as untrusted.
The executable evidence below was produced from fresh source copies under
`/tmp/audit-work/rebuild`; no candidate-provided kompiled definition, cache,
proof log, `PROOF.md`, or validation script was reused as proof evidence.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, condition `kit-semantics`, and problem
`156-int-to-mini-roman`. I read the launcher-owned audit input, campaign lock,
`/run.json`, `/task.json`, `/generation-result.json`, every required JSON/text
record in `/generation-evidence`, the complete 682-line generation output, and
validated all 2,311 structured JSONL trace records. The generation records claim
success but were not used as proof evidence.

The campaign lock JSON exactly equals the `audit_campaign` block in
`/audit-input.json`, and its SHA-256 is the recorded
`ad5dfc...d745`. Independent SHA-256 checks match every recorded regular-file
digest: campaign lock, run/task/result/invocation manifests, prompt, canonical,
candidate/trusted translators, generation last/output/prompt/metrics/runtime
metrics/usage, and the sole structured trace file. All launcher-declared mounts
and all records required by `pipeline-v3` are readable regular files or real
directories.

The required trusted `/reference/reference-semantics` is present. A recursive
`lstat`/per-file-SHA comparison found exactly 25 entries in each supplied tree;
candidate and trusted relative names, entry types, and bytes are identical.
There are no missing, additional, mistyped, special, or symlinked entries.
Candidate/trusted `prompt.py` and `py2mpy.py` are byte-identical. No symlink or
special entry exists anywhere below `/candidate`, `/reference`, or
`/generation-evidence`.

Evidence:

- `/audit-output/evidence/stage1_integrity.py`
- `/audit-output/evidence/stage1_integrity.log` (exit 0)
- `/audit-output/evidence/trace_inventory.py`
- `/audit-output/evidence/trace_inventory.log` (2,311 valid records, exit 0)

There is no provenance or supplied-semantics infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted source contract is: for an integer `number` satisfying
`1 <= number <= 1000`, return its conventional Roman numeral in lowercase. The
documented examples are `19 -> "xix"`, `152 -> "clii"`, and
`426 -> "cdxxvi"`. The trusted canonical greedily consumes the conventional
tokens `m, cm, d, cd, c, xc, l, xl, x, ix, v, iv, i`.

`/candidate/solution.py` uses three ten-entry lookup tuples for the hundreds,
tens, and ones digits, with a separate `number == 1000` branch returning
`"m"`. This is a different but faithful algorithm on the stated finite domain.
It has no import, global state, I/O, exception, mutation, or helper function.

Using only the trusted `/reference/py2mpy.py`, I regenerated
`solution.py` into scratch. The generated 1,287-byte `solution.mpy` is
byte-identical to the submitted file; both have SHA-256
`4abd6f...161d`.

An independently authored differential script imports
`/reference/canonical.py` and the scratch copy of generated `solution.py`.
It checks every integer `1..1000`, all documented examples, both domain
boundaries, and every lookup/subtractive boundary around 4, 5, 9, 10, 40, 50,
90, 100, 400, 500, 900, and 1000. There is no empty integer input; the nearest
out-of-domain observation, zero, returns `""` in both implementations. The
full intended-domain run reports zero mismatches.

Evidence:

- `/audit-output/evidence/regenerate_and_compare.sh`
- `/audit-output/evidence/translation_identity.log` (both operations exit 0)
- `/audit-output/evidence/differential.py`
- `/audit-output/evidence/differential.log` (1,000 inputs, zero mismatches,
  exit 0)

## 3. Clean proof reconstruction

I copied only `solution.py`, submitted `solution.mpy`, `verification.k`, and
`spec.k` into scratch, then copied the translator/prompt/canonical and supplied
semantics from `/reference`, not from candidate build output. Scratch initially
contained no `*-kompiled` directory or K cache.

K v7.1.293 was independently available. Fresh concrete compilation:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

exited 0. The compiler emitted bounded warnings about unused variables and
non-exhaustive declarations for fixed, unused total helpers; no build error
occurred. Fresh `krun concrete_audit.mpy --definition concrete-kompiled`
exited 0 at `.K`, with empty heap/stack, `NoExc`, exit code 0, and:

```text
1=i, 4=iv, 9=ix, 40=xl, 90=xc, 400=cd, 900=cm, 1000=m
```

Fresh proof compilation:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

also exited 0. The ten fresh target commands select claims 1–100, 101–200,
..., 901–1000 exactly once. Every command exited 0 and printed exactly one
`#Top`. An independent log parser confirmed 100 labels per batch, no duplicate
or missing label, complete coverage of 1..1000, and the required success signal
for every batch. The outer driver exited 0.

Evidence:

- `/audit-output/evidence/tool_versions.log`
- `/audit-output/evidence/kompile_llvm.log`
- `/audit-output/evidence/concrete_audit.py`
- `/audit-output/evidence/concrete_audit.mpy`
- `/audit-output/evidence/krun_concrete.log`
- `/audit-output/evidence/kompile_haskell.log`
- `/audit-output/evidence/run_positive_batches.sh`
- `/audit-output/evidence/kprove_positive_01.log` through
  `/audit-output/evidence/kprove_positive_10.log`
- `/audit-output/evidence/kprove_positive_batches_driver.log`

## 4. Adequacy and real-program pinning

There are 1,000 entry claims, one for each and only each allowed integer. Claim
`roman-NNNN` has no symbolic side condition: its prestate is the real,
satisfiable initial configuration declared by `core.k`—`<k>` loads a ground
module, environment 0, the empty module scope parented by the fixed builtins
scope, allocators at their initial values, empty heap/stack, `noRet`, `NoExc`,
and exit code 0.

Its postcondition requires `.K`; the same environment; a module scope containing
exactly the real function closure and `__result`; the canonical ground lowercase
Roman string for that input; unchanged allocators and heap; empty call stack;
`noRet`; `NoExc`; and exit code 0. The result is neither free nor existential,
and there is no implication weakening. Inputs 1, 19, 152, 426, 999, and 1000
substitute to respectively `i`, `xix`, `clii`, `cdxxvi`, `cmxcix`, and `m` in
the trusted canonical, generated Python, and mechanically checked claim
postconditions.

`verification.k` adds exactly three syntax macros and their three macro
expansion rules. An independent constructor-level comparison removes only
whitespace and the translator’s empty-list surface spelling, then proves:

1. `intToMiniRomanBody` is the exact trusted-regenerated function body;
2. `solutionCall(N)` contains that exact binding followed by
   `Assign("__result", Call("int_to_mini_roman", N))`; and
3. all 1,000 complete claim shapes equal independently generated ground claims
   using the trusted canonical outputs.

The compiled runtime rule inventory contains none of the three macro tokens:
they expand before execution and are not operational bridges. The real fixed
semantics therefore performs binding, argument evaluation, tuple construction,
arithmetic, indexing, branching, concatenation, return/pop, and result
assignment.

A fresh body-sensitivity definition changes the program term actually executed:
only the input-1000 true branch changes from `Return(Str("m"))` to
`Return(Str("x"))`. Its postcondition tracks the mutated closure body exactly
but retains the original required result `"m"`. The mutant definition compiled
successfully (exit 0); its proof exited 1 with `WarnStuckClaimState`. The
residual final state has `__result` code 120 (`"x"`), directly witnessing
sensitivity to the executed body rather than to an external source file.

Evidence:

- `/audit-output/evidence/pinning_audit.py`
- `/audit-output/evidence/pinning_audit.log` (exit 0)
- `/audit-output/evidence/verification-body-mutant.k`
- `/audit-output/evidence/spec-body-mutant.k`
- `/audit-output/evidence/kompile_body_mutant.log` (exit 0)
- `/audit-output/evidence/kprove_body_mutant.log` (expected exit 1 and
  result-bearing stuck residual)

## 5. Rule-by-rule static soundness review

I inventoried every supplied and local declaration. The inventory contains 229
syntax statement starts, 698 rule starts, five contexts, one configuration,
and no proof-local claim. Attribute-bearing lines cover 149 `function`, 110
`total`, 35 `concrete`, 45 priority, 22 `no-evaluators`, and eight macro
entries; there is no `simplification` or `functional` entry. The complete
file/line inventory and per-module decision are preserved below.

The actual program constructor set is `Module`, `FuncDef`, `Params`, `Assign`,
`Name`, `Subscript`, `TupleExpr`, `Str`, `BinOp`, `Int`, `If`, `Compare`,
`CmpOp`, `Return`, plus the call harness. Each is mapped to its declaration and
active rules in `used_constructs.md`.

On the used path:

- left-to-right strictness/contexts evaluate binding, operands, index, guard,
  and return expression in Python order;
- integer `%` and `//` use positive ground divisors 1000, 100, and 10;
- each index is ground 0..9 into a ground ten-element tuple, so the otherwise
  under-specified `valSeqAt [total]` boundary reduces by ordinary equations;
- all string literals are ASCII, and concatenation is structural;
- the `If` alternatives have complementary ground guards;
- the concrete `closureVal` call stores the exact continuation, creates/binds
  one frame, and `Return`/`#pop` restores it while removing only the callee
  scope; and
- every observable cell is constrained afterward.

All float, sort, MD5, and other opaque fixed-semantics symbols are unreachable
and absent from program, control, state, and postcondition. `MPY-CONCRETE` is
not imported into `VERIFICATION`. The task adds no runtime function, totality
claim, priority, simplification, opaque symbol, lemma, circularity, or
operational bridge. The three exact macros skip no operation and contain no
result equation.

For every inventoried fixed rule, the module decision sheet records either its
ordinary subset semantics or an explicit unused trust/partiality boundary.
Guard overlaps on the used redexes were checked pairwise; alternatives are
sort-disjoint, operator-disjoint, or complementary. No rule encodes a Roman
answer or makes a false conclusion provable for a satisfying input. Thus there
is no unsound-rule witness to report.

Evidence:

- `/audit-output/evidence/declaration_inventory.txt`
- `/audit-output/evidence/static_inventory_summary.py`
- `/audit-output/evidence/static_inventory_summary.log`
- `/audit-output/evidence/static_rule_review.md`
- `/audit-output/evidence/used_constructs.md`

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh
`/audit-output/evidence/spec-false.k` changes input 4’s required result from the
true `"iv"` to `"v"` while preserving the real executable term and every other
cell. Input 4 is a concrete satisfying witness, and both trusted Python
implementations return `"iv"`.

`kprove --dry-run` on this artifact exited 0, proving that it parses and builds
against the fresh definition. The actual proof then exited 1 with
`WarnStuckClaimState`; the residual final state explicitly contains codes
105,118 (`"iv"`) where the destination requires code 118 (`"v"`). This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.

Evidence:

- `/audit-output/evidence/spec-false.k`
- `/audit-output/evidence/kprove_false_dry_run.log` (exit 0)
- `/audit-output/evidence/kprove_false.log` (expected exit 1 with stuck result)
- `/audit-output/evidence/negative_probes_driver.log` (reviewer checks exit 0)

## 7. Proven versus assumed accounting

Subject to the supplied fixed semantics and K toolchain, the successful
reachability set establishes: for every integer in the complete source domain
`1..1000`, executing the actual trusted translation of the submitted function
from the default MiniPy state reaches a normal final state whose assigned
`__result` is that integer’s independently canonical lowercase Roman numeral,
with no exception or residual call/state effect. This is a finite exhaustive
proof of the exact finite source domain, not a few examples or a narrowed
domain. It is a partial-correctness statement in the Kit sense.

Trust/assumption ledger:

- **Supplied `reference-semantics/`:** selected fixed execution theory. The
  candidate copy is byte/entry identical; all used rules were statically
  audited and dynamically exercised. Unused partial/opaque operations do not
  influence any target.
- **Trusted `py2mpy.py`:** trusted frontend from Python AST to MiniPy. Byte
  regeneration and constructor pinning prove what K executes. Faithfulness of
  the frontend to CPython is outside K, but independently supported over the
  entire allowed domain by canonical-vs-generated Python differential and by
  branch-boundary `krun`.
- **Roman intent bridge:** the trusted canonical and conventional subtractive
  token table give the meaning of “Roman numeral equivalent.” Each claim
  literal was independently regenerated from that trusted canonical; this is
  an intent bridge, not a proof-side oracle.
- **K v7.1.293/Haskell backend, LLVM backend, K builtins, solver, and host
  arithmetic/string hooks:** standard trusted computing base. The positive
  theorem depends on Haskell/K/solver; LLVM is only corroborating evidence.
- **Candidate macros:** not assumed. They were mechanically proved identical to
  regenerated constructors and absent from runtime rules.
- **Empirical evidence:** the 1,000-input Python differential and finite
  concrete K run support frontend/model adequacy only. They are not substituted
  for any K reachability claim.

Excluded are non-integers, values outside 1..1000, behavior of unused MiniPy
features, total correctness/liveness as a separate theorem, and correctness of
the trusted toolchain itself.

All three Kit validation gates pass: Gate A has exact body execution, no
operational bridge, complete cell/result constraints, body sensitivity, and
fresh non-vacuity; Gate B covers exactly the entire stated finite domain and
the intended result; Gate C has reproducible commands, logs, full-domain
frontend/canonical evidence, and an explicit trust ledger. Under the benchmark
decision mapping, this is a legitimate proof with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
