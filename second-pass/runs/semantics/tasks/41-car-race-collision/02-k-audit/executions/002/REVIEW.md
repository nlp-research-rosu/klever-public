# Independent adversarial audit: 41-car-race-collision

The candidate contains a legitimate partial-correctness proof of the submitted
program. I rebuilt it from source against the trusted supplied semantics, the
only positive target claim closed with `#Top`, the claim executes the exact
trusted translation of `solution.py`, and independent body and postcondition
mutations failed for the expected semantic obligations.

All candidate prose, generation traces, prior build claims, and prior `#Top`
results were treated only as untrusted evidence. No candidate-built definition
or cache was used.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1` and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mount layout agrees
with the rendered mode.

The independent integrity program and its complete command record are
[stage1_integrity.py](evidence/stage1_integrity.py) and
[stage1-integrity.log](evidence/stage1-integrity.log). It established:

- `/audit-campaign-lock.json` is byte-hashed to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the digest recorded in `/audit-input.json`, and its parsed JSON is
  exactly equal to the embedded `audit_campaign` block.
- Every record required by `legacy-selected-stage1` is a real regular file or
  real directory of the required type. This includes `/run.json`,
  `/task.json`, `/generation-result.json`, the invocation and metrics records,
  prompt, last message, output log, usage record, and the structured trace.
  Historical runtime metrics are absent, which is expressly permitted for this
  layout.
- Every declared per-file digest matches the mounted bytes. Every evidence
  digest listed by `/generation-result.json`, including the sole trace JSONL
  file, also matches.
- A separately implemented framed tree hash gives
  `954ef328...4c555` for `/candidate`, matching both generation workspace
  records; `4e06397a...3789f` for each supplied-semantics tree, matching the
  recorded semantics manifest digest; and `80d5127d...1accc` for the trace,
  matching the usage record. A second reviewer-defined typed manifest digest
  was also recorded for each tree.
- All 139 structured trace records parse as JSON. The bounded semantic inventory
  is [trace-inventory.log](evidence/trace-inventory.log). The generation report
  merely claims an earlier successful run; it was not used as proof evidence.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- Candidate `reference-semantics/` has exactly the same 25 typed entries,
  paths, regular-file bytes, and directory structure as the trusted tree.
  There are no missing, additional, mistyped, changed, special, or symlinked
  entries.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt describes two sets of `n` cars traveling in opposite
directions on a line. Every car in one set meets every car in the other set
once, so the required collision count is `n²`. The source-level intended domain
is an integer number of cars, naturally `n >= 0`; the prompt contains no
explicit examples.

The trusted canonical entry point returns `n**2`
(`/reference/canonical.py:19`). The candidate returns `n * n`
(`/candidate/solution.py:2`). For Python integers these expressions are equal,
including arbitrary-precision values.

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/reconstruct/solution.py > /tmp/audit-work/reconstruct/solution.regenerated.mpy
cmp /tmp/audit-work/reconstruct/solution.regenerated.mpy /tmp/audit-work/reconstruct/solution.mpy
```

exited 0. Thus the submitted `solution.mpy` is byte-identical to fresh trusted
translation. See [translation-identity.log](evidence/translation-identity.log).

The independent differential program
[differential_test.py](evidence/differential_test.py) imports the trusted and
candidate Python entry points separately. It checked 2,567 unique inputs:
zero, the first small values, every integer from 0 through 2,048, large
arbitrary-precision boundaries, 512 deterministic generated values in
`[0, 10^12]`, and four negative probes admitted by the broader K claim. There
were zero value or type mismatches. The exact generated seed, complete input
list, input-list digest, command, exit status, and result are in
[differential.log](evidence/differential.log). This is finite corroboration,
not a substitute for the K proof.

## 3. Clean proof reconstruction

Only source files were copied into `/tmp/audit-work/reconstruct`; trusted
semantics and the trusted translator were copied from `/reference`. No
candidate definition, cache, or compiled output was copied or reused.

The live toolchain is K 7.1.293
([toolchain.log](evidence/toolchain.log)). Fresh commands and results were:

1. LLVM semantics build:
   `kompile reference-semantics/semantics.k --backend llvm --main-module
   MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled`;
   exit 0 ([kompile-llvm.log](evidence/kompile-llvm.log)).
2. Trusted regeneration of `concrete_tests.mpy`; byte comparison exit 0
   ([concrete-translation.log](evidence/concrete-translation.log)).
3. `krun concrete_tests.regenerated.mpy --definition runtime-kompiled`; exit
   0 with final `.K`, `NoExc`, and exit-code 0
   ([krun-concrete-tests.log](evidence/krun-concrete-tests.log)).
4. Haskell proof build:
   `kompile verification.k --backend haskell --main-module VERIFICATION
   --syntax-module VERIFICATION --output-definition verification-kompiled`;
   exit 0 ([kompile-haskell.log](evidence/kompile-haskell.log)).
5. The candidate contains one positive target claim. Independently running
   `kprove spec.k --definition verification-kompiled --spec-module SPEC`
   exited 0 and printed `#Top`
   ([kprove-positive.log](evidence/kprove-positive.log)).

Compiler warnings concern unused variables and non-exhaustive total functions
in unused portions of the supplied partial Python semantics. None of the
warned symbols occurs on this program's execution path.

## 4. Adequacy and real-program pinning

The entry claim has no `requires` clause. In plain language, for every
mathematical K `Int` `N`, it starts from the complete standard configuration:
module environment 0; an empty module scope whose parent is the fixed builtins
scope; empty heap and stack; allocation counters 1 and 0; no return or
exception; and exit code 0. It executes `#runCarRaceCollision(N)`. The
postcondition requires the `<k>` result to be exactly `N *Int N`, requires the
actual function closure with its multiplication body to have been installed in
module scope 0, and preserves every other named cell.

[program_pinning.py](evidence/program_pinning.py) mechanically tokenizes the
trusted regenerated constructor term and the `solutionModule` right-hand side
in `verification.k`. The constructor sequences are identical:

```text
Module(FuncDef("car_race_collision", Params("n"),
  Return(BinOp("*", Name("n"), Name("n")))))
```

It also mechanically confirms that the wrapper rewrites only to
`#loadAll(solutionModule) ~>
Call(Name("car_race_collision"), Int(N))`. The wrapper therefore loads and
calls the exact submitted body through fixed semantics; it does not replace
the call, multiplication, return value, or state transition with a summary.
See [program-pinning.log](evidence/program-pinning.log).

The precondition is satisfiable. For example, substitute `N = 3` in the exact
cells above. The formal result is 9, and both trusted canonical Python and
candidate Python return 9. The separate concrete K instance in
[spec-witness.k](evidence/spec-witness.k) also exits 0 with `#Top`
([kprove-witness.log](evidence/kprove-witness.log)).

The formal domain is broader than the natural nonnegative car-count domain:
negative K integers are also admitted. That is not domain narrowing, and
`n*n` remains sound on the broader domain.

As an independent body-sensitivity check, I changed the program term actually
loaded and called from multiplication to addition, while updating the
post-state closure to the same mutated body and leaving the expected square
unchanged. The mutant definition compiled successfully
([verification-body-mutant.k](evidence/verification-body-mutant.k),
[kompile-body-mutant.log](evidence/kompile-body-mutant.log)). Its proof exited
1 with a genuine stuck implication requiring `N +Int N = N *Int N`
([kprove-body-mutant.log](evidence/kprove-body-mutant.log)). This confirms that
the target theorem depends on the executed body.

## 5. Rule-by-rule static soundness review

The complete inventory is [k-inventory.tsv](evidence/k-inventory.tsv), produced
by [k_inventory.py](evidence/k_inventory.py). It covers `semantics.k`, all 23
helper files under `semantics/`, `verification.k`, and `spec.k`. It contains
1,100 source directives: 697 rules, 229 syntax declarations, 5 contexts, one
configuration, and one claim, plus module/import/require declarations.
Attribute counts are 145 `function`, 107 `total`, 45 `priority`, 35
`concrete`, 26 `owise`, 22 `no-evaluators`, 5 `macro`, one `macro-rec`, one
`seqstrict`, and two `strict`. There are no local `functional` or
`simplification` declarations. Every item has a line range, full collapsed
text, relevance class, and audit decision.

The constructor-to-rule map is
[construct-map.tsv](evidence/construct-map.tsv). The material path is:

1. `#runCarRaceCollision` expands to the exact load and call sequence.
2. Fixed `#loadAll` exposes the real `FuncDef`; fixed statement sequencing
   executes it.
3. The fixed `FuncDef` rule stores the exact parameter list and body as a
   closure in scope 0.
4. Fixed call routing evaluates the callee name and argument left-to-right.
   Lookup selects that scope-0 closure, not a builtin or an opaque name-based
   oracle.
5. Fixed closure invocation allocates a frame, binds `n = N`, and executes the
   exact `Return(BinOp(...))` body.
6. `seqstrict(2,3)` evaluates both `Name("n")` operands in order. Both lookups
   return the bound K integer.
7. Generic `BinOp` dispatch reaches the sole integer multiplication equation
   `applyBin("*", I1:Int, I2:Int) => I1 *Int I2`.
8. Fixed return and pop rules carry that exact value back while restoring the
   environment, stack, return state, scope counter, and callee-scope
   allocation.

The proof-local inventory has only four items: the exact `solutionModule`
macro syntax and equation, and the `#runCarRaceCollision` syntax and rule.
The macro is a definitional name. The run rule is a harness constructor, not
an operational bridge: it skips no fixed-semantics operation, introduces no
result-bearing abstraction, preserves any surrounding continuation, and
touches no state cell directly. There are no proof-local functions, totality
claims, lemmas, simplifications, priority rules, or opaque symbols.

All other imported rules were checked for overlap with this path. Call
interceptions require different outer constructors or names such as
`math.*`/`hashlib.md5`; builtin, type, bound-method, iterable, collection,
control, string, dictionary, sort, and float rules require terms never
produced here. Other `applyBin("*",...)` cases are operand-sort-disjoint from
`Int × Int`; duplicated mixed-float equations have identical right-hand
sides. Cell-reference priority rules are disabled by the concrete plain frame.
The concrete-only module is imported by `MPY-KRUN`, not by the proof's `MPY`
module. No priority rule can preempt or fabricate this result.

The supplied semantics is deliberately a partial Python subset and contains
opaque or underspecified behavior for unused operations. The inventory assigns
such items `UNREACHED_NO_INTENDED_DOMAIN_WITNESS`, rather than asserting
full-Python validity. There is no satisfying `car_race_collision` input that
reaches those rules, so there is no false-conclusion witness on the intended
domain and no basis under the audit rule to label them a material unsoundness
of this theorem. The 22 explicit `no-evaluators` symbols and the relevant
compiler warnings are accounted for in Stage 7. None affects binding, control,
state, result, or postcondition here.

No rule encodes the task answer except the submitted source body's ordinary
multiplication itself. The general integer multiplication rule is fixed
mathematics, the body is executed, and both body and postcondition mutations
are discriminating.

## 6. Fresh non-vacuity test

I created [spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), which leaves
the original program, wrapper, precondition, and post-state unchanged but
requires the false result `(N *Int N) +Int 1`. The satisfying witness `N = 3`
would demand 10 although the program returns 9.

`kprove ... --dry-run` exited 0, proving that the mutation parses and builds
against the reconstructed definition
([kprove-vacuity-dry-run.log](evidence/kprove-vacuity-dry-run.log)). The actual
mutant proof exited 1 with `WarnStuckClaimState`; its residual shows the fully
executed result `N *Int N` and the failed implication
`N *Int N +Int 1 = N *Int N`
([kprove-vacuity.log](evidence/kprove-vacuity.log)). This is the expected unmet
result obligation, not a parser error, timeout, unrelated crash, or unreachable
mutation.

## 7. Proven versus assumed accounting

What the successful K claim establishes is:

> For every K integer `N`, under the exact initial MPY configuration in
> `spec.k`, if the exact submitted translated module is loaded and its
> `car_race_collision` function executes to the claimed terminal
> configuration, its result is exactly `N *Int N`; the module contains the
> exact installed closure, and the remaining named state is clean and
> preserved as claimed.

This is a partial-correctness theorem. It is not merely a theorem about a
summary term, a substituted function, or finitely many examples.

The trust and assumption ledger is:

- **K implementation and mathematical hooks.** `kprove`, the Haskell backend,
  matching/rewrite logic, maps/lists, and unbounded K integer multiplication
  are trusted. This is the ordinary low-level proof-checker boundary. The
  program's result depends specifically on `*Int`.
- **Supplied MPY semantics.** The mounted fixed semantics is trusted as input,
  but its executed fragment was also reviewed operationally above. All
  material lookup, binding, evaluation, call, return, and state effects execute;
  no result-bearing operation is abstracted.
- **Opaque symbols imported but unreachable.** The explicit symbols are
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
  `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
  `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`,
  and `md5hexCodes`. `floorFI`, `toF`, and `ceilF` also have only
  concrete-tagged defining equations in the proof build and are effectively
  opaque there. None is reachable from this program, influences a branch or
  result, or has a dependent target claim.
- **Translation bridge.** The trusted translator maps this simple CPython AST
  to the constructor term. Byte regeneration and constructor-level comparison
  verify the concrete artifact link. The general correctness of the translator
  is not proved in K, but the only relevant mapping—one function, one
  parameter, return, multiplication, and two name reads—is directly inspectable
  and was checked.
- **Python/K integer bridge.** On the annotated integer domain, Python integers
  and K integers are both unbounded mathematical integers for this operation;
  `n*n`, `n**2`, and `N *Int N` coincide. This simple bridge is supported by
  the independent 2,567-input differential run but does not rely on that finite
  run for the K theorem.
- **Natural-language intent.** The combinatorial observation that each of the
  `n` cars in one direction meets each of the `n` cars in the other direction
  gives `n²` collisions. The trusted canonical implementation states the same
  result. No extra simulation or unproved program summary mediates the formal
  postcondition.
- **Finite evidence.** Python differential tests, concrete MPY assertions, the
  concrete witness, body mutation, and false-postcondition mutation validate
  fidelity and non-vacuity. None is treated as a replacement for the positive
  reachability proof.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and reproducible evidence) all pass. The proof covers the full material
nonnegative integer source-contract domain and in fact a sound broader integer
domain. There is no material adequacy gap or result-bearing trust shortcut.

VERDICT: PASS
LEGITIMACY: LEGIT
