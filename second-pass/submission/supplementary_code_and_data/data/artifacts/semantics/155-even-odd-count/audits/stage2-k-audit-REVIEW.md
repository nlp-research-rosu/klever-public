# Independent adversarial audit: 155-even-odd-count

The candidate is not a legitimate proof under the required validation
standard. Fresh reconstruction does reproduce both advertised `#Top` results,
the implementation is faithful to the HumanEval contract, and the theorem is
non-vacuous. The fatal defect is the proof-local loop-summary rewrite in
`/candidate/verification.k:62-86`: its match domain is broader than the
bridge-free theorem offered to justify it, and it demonstrably proves a false
loop completion on a state in that broader domain. Thus the entry `#Top` is
obtained in a theory containing a materially unsound operational bridge.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout` =
`legacy-selected-stage1`, condition `semantics`, and
`semantics_mode` = `SUPPLIED_SEMANTICS`. The mode and trusted mounts agree:
`/reference/reference-semantics` is present as a real directory.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/usage.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and the JSONL trace under
`/generation-evidence/codex-trace`. Runtime metrics are not a required
historical record for this declared layout.

The campaign-lock JSON is structurally identical to the `audit_campaign` block
and its SHA-256 is the declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The directly recorded hashes for the run manifest, task manifest, generation
result, invocation, metrics, usage, prompt, last message, output log, trace
file, canonical program, problem prompt, and translator all matched. A
type-aware independent tree digest produced:

- candidate:
  `b6e38d7cb00a36a22416b17d9ae57f620b7cd17596b37d3d5e7d1f560ffdb563`,
  matching the retained workspace hash in the generation records;
- candidate and trusted supplied-semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`
  for each;
- structured-trace tree:
  `ebf4b0a149b9a3be987159d483b392396e1402e90cbb758b7d6f5072fff24bdc`,
  matching `usage.json`.

The candidate prompt and translator are byte-identical to their trusted
mounts. A recursive, no-symlink comparison of
`/candidate/reference-semantics` and
`/reference/reference-semantics` found no missing, additional, mistyped, or
changed entries. No symlink exists anywhere in the candidate, reference, or
generation-evidence mounts. The structured trace contains 382 valid JSON
events. The generation records claim success, but I did not use that claim as
proof evidence.

Evidence:

- `evidence/01_provenance_checks.sh` and
  `evidence/01_provenance_checks.log`
- `evidence/01_tree_hashes.py` and `evidence/01_tree_hashes.log`
- `evidence/01_generation_inspection.py` and
  `evidence/01_generation_inspection.log`

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for an integer `num`, return a pair whose first
component is the number of even decimal digits and whose second component is
the number of odd decimal digits. The sign is ignored. In particular, zero is
represented by one even digit, so `even_odd_count(0) == (1, 0)`.

The canonical program converts `abs(num)` to decimal text and tests
`int(digit) % 2`. The candidate converts the same value to text and tests
`ord(digit) % 2`. Decimal ASCII codes 48 through 57 have the same parity as
their represented digits, so the algorithms agree on the intended integer
domain. Initializing `digit = 0` before the loop is semantically inert for the
return value and gives the proof a defined empty-loop local.

Running the trusted `/reference/py2mpy.py` on `/candidate/solution.py`
reproduced `/candidate/solution.mpy` byte-for-byte; both files hash to
`4eb2b3f6755b8446a0c9559d07c8c85a6e525b69fe8126b31b411763bb0ecc3c`.

The independent differential script imports the trusted canonical function and
the candidate Python function directly. It tested the two documented examples,
zero, positive and negative single digits, every small branch boundary from
-20 through 20, all-even and all-odd values, 600 boundaries around powers of
ten through `10**100`, signed 32- and 64-bit boundaries, and 2,000 seeded
random integers in `[-10**100, 10**100]`. There were 2,646 unique inputs and
zero mismatches.

Evidence:

- `evidence/02_differential.py`
- `evidence/02_fidelity_checks.sh`
- `evidence/02_fidelity_checks.log`

Program-fidelity result: pass.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/fresh`; candidate-built
definitions and caches were not copied. K 7.1.293 was available independently.

The exact reconstruction is in `evidence/03_reconstruction.sh` and its complete
bounded output is in `evidence/03_reconstruction.log`. It performed:

1. trusted translation of the reviewer-authored concrete test program;
2. fresh LLVM compilation of the trusted supplied semantics as `MPY-KRUN`;
3. concrete execution of nine normal and boundary assertions;
4. fresh Haskell compilation with main module
   `EVEN-ODD-VERIFICATION`;
5. proof of `EVEN-ODD-LOOP-SPEC`;
6. fresh Haskell compilation with main module
   `EVEN-ODD-VERIFICATION-SUMMARY`;
7. proof of `EVEN-ODD-SPEC`.

The LLVM execution ended with `.K`, `NoExc`, and exit code 0. Both independent
positive `kprove` commands printed `#Top` and exited 0:

```text
kprove ... --spec-module EVEN-ODD-LOOP-SPEC
#Top
[exit 0]

kprove ... --spec-module EVEN-ODD-SPEC
#Top
[exit 0]
```

Compiler warnings concern non-exhaustive functions in unused parts of the
fixed semantics (`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt`) and
unused variables in `strLt`; none is on this program's execution path. There
was no build, timeout, or backend failure.

Fresh-reconstruction result: the advertised closure is reproducible.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

The loop claim in `/candidate/spec.k:8-35` has no arithmetic side condition.
For any `IntSeq` `CS`, integers `N`, `E`, and `O`, value `D`, and continuation
`CONT`, it starts at the real `#loop` over `str(CS)` in environment 1 with an
exact three-frame scope map: builtins at -1, the submitted function at 0, and
the current locals at 1. It says the loop reaches `CONT`, adds the even and odd
code counts of `CS` to the two counters, and sets `digit` to the last
one-character string (or leaves `D` for an empty sequence). All other
configuration cells are framed.

The entry claim in `/candidate/spec.k:42-64` has precondition `N:Int` and the
normal empty call configuration. It calls the binding named
`even_odd_count`. It postconditions the returned value to exactly

```text
(
  evenDigits(strToCodes(Int2String(absInt(N)))),
  oddDigits(strToCodes(Int2String(absInt(N))))
)
```

It is an equality-shaped reachability destination, not a free result, tautology,
or one-way implication. Its formal domain is every mathematical K integer, so
it does not narrow the HumanEval integer domain.

### Program identity

The entry claim does not load the complete module text, but this is adequately
handled by immutable constructor-level pinning. `evidence/04_body_pinning.py`
uses fresh-definition `kast --expand-macros --output json` results. It extracts
the sole `FuncDef` from the trusted regeneration and compares that constructor
tree to `#evenOddFunctionBody`; it then verifies that
`#evenOddModuleScope` binds the same name, parameter sequence, body, defining
environment 0, and parent -1. The body and macro KAST hashes are both
`0939411132f65948e5c346f1acc8fc16c41afd2acc9484464b8f7103ce6533d0`.
Thus the entry executes the actual submitted function body, allowing only the
candidate's named syntax macros.

### Satisfying states and substitutions

Every entry precondition is satisfiable; examples are `N = -12`, `N = 0`, and
`N = 123` in the explicitly supplied empty call configuration. A separate
three-claim K check reduced those cases to `(1,1)`, `(1,0)`, and `(1,2)` and
printed `#Top`/exit 0. Both Python implementations produce the same values.
The loop precondition is also satisfiable, for example with
`CS = .IntSeq`, `N = E = O = 0`, `D = 0`, and `CONT = .K`.

Evidence:

- `evidence/04_body_pinning.py` and `evidence/04_body_pinning.log`
- `evidence/04_macro_term.mpy` and `evidence/04_scope_term.mpy`
- `evidence/04_concrete_substitutions.k` and
  `evidence/04_concrete_substitutions.log`

Adequacy result considered in isolation: the claims cover the requested
domain, pin the submitted body, and constrain the intended return value.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.log` enumerates, with source locations, every
module/import, syntax declaration, configuration, context, rule, claim, and
relevant attribute in the supplied semantics and candidate proof files. It
contains 232 syntax-start lines, 705 rules, two claims, five contexts, and one
configuration. There are 147 function-declaration lines, 109
total-declaration lines, no `[functional]` declarations, 46 priority
attributes, no simplification rules, and 27 `no-evaluators` opaque declaration
lines. Per-file counts are in `evidence/05_inventory_counts.tsv`.

The 695 supplied-semantics rules break down as follows:

```text
assert 3; bool 13; builtins 137; call 21; comprehension 7;
concrete 16; controls 34; core 46; dict 28; float 121;
functions 15; int 16; iter 0; list 27; methods 75; operators 10;
range 6; set 12; sort 19; str 28; subscript 40; syntax 0; tuple 21.
```

The assembly and syntax declarations define the expected AST, value,
configuration, scope, heap, continuation, and iterator constructors. The
core/call/functions/controls path used here evaluates callee then arguments,
allocates and pops the function frame, resolves the real binding through
scopes, evaluates assignment/loop/branch/return in order, and preserves all
observable cells correctly. The used domain rules are:

- `abs(Int)` and `str(Int)` in `builtins.k`;
- `ord` on a one-character `str`;
- integer `%`, `==`, and `+` in `int.k`;
- string iteration in `str.k`;
- tuple construction in `tuple.k`.

These used rules are guarded and non-overlapping on this path. `pyMod` is used
only with divisor 2. `str(abs(N))` supplies only decimal ASCII characters, so
the one-character `ord` rule applies. The loop writes only the local-scope
bindings that the claim records. The remaining supplied modules and all 27
opaque float/sort/digest declarations are unreachable from the submitted
program; they cannot influence its branch, result, state, exception, or
postcondition. The supplied-semantics tree is also byte-identical to the
trusted baseline.

### Candidate-local declarations and rules

The ten candidate-local rules were reviewed individually:

1. `evenDigits(.IntSeq) => 0` is the true base equation.
2. The `evenDigits(iCons(...))` equation adds exactly one iff the head code is
   even and structurally descends.
3. `oddDigits(.IntSeq) => 0` is the true base equation.
4. The `oddDigits(iCons(...))` equation adds exactly one iff the head code is
   odd and structurally descends.
5. `lastSeen(.IntSeq,D) => D` is the correct empty-loop value.
6. Recursive `lastSeen` records the current one-character string and
   structurally descends, yielding the actual final loop target.
7. `#digitLoopBody` is a syntax macro exactly matching the regenerated loop
   body.
8. `#evenOddFunctionBody` is a syntax macro exactly matching the regenerated
   function body.
9. `#evenOddModuleScope` is a syntax macro for the exact submitted binding.
10. The priority-40 loop summary is an operational bridge. It is unsound.

The first six are exhaustive, disjoint constructor equations with decreasing
recursion. The three macros are compile-time names and do not invent runtime
behavior. There are no proof-local opaque symbols or simplification rules.

### Fatal operational-bridge defect

The bridge-free loop theorem requires the complete scopes map

```text
-1 |-> builtinsScope
 0 |-> #evenOddModuleScope
 1 |-> current-loop-frame
```

and proves the loop transition for arbitrary `CONT`. The summary rule,
however, matches only

```text
... 1 |-> current-loop-frame ...
```

It neither requires scope 0 nor scope -1. Those cells are not irrelevant:
executing the real body resolves `ord` by following frame 1's parent to scope
0 and then to the builtins scope at -1. Therefore the rule's complete match
domain is not a subset of its justification domain. Its priority 40 makes it
preempt the fixed loop rule.

This is not merely an absent proof. There is a concrete false-conclusion
witness in `evidence/05_bridge_malformed_base.k` and
`evidence/05_bridge_malformed_witness.k`:

- use the intended integer value `N = 1`, the decimal one-character sequence
  `iCons(49,.IntSeq)`, zero counters, environment 1, and exactly the local
  scope that the summary accepts, but omit scope 0;
- use continuation `Name("odd_count")`;
- fixed semantics binds `digit` and then gets stuck at `#look("ord",0)`, so
  the claim that this state returns 1 and updates the odd counter fails with
  `WarnStuckClaimState`/exit 1;
- the summary-enabled definition proves that same claimed completion with
  `#Top`/exit 0.

The symbolic claim whose precondition exactly reproduces the bridge's broad
ellipsis shape also fails against fixed semantics, leaving the same missing
`ord`-lookup branches. The witness uses an intended integer and digit value
and lies inside the operational rule's declared match domain; the omitted
scope dependency is the sole reason fixed execution cannot make the
fabricated transition.

`evidence/05_body_sensitivity.sh` provides a separate sensitivity test. It
changes the actual executed comparator from `== 0` to `== 1`. The bridge-free
loop theorem then fails with the expected counter residual, but the entry
theorem alone still prints `#Top` because the summary directly supplies the
original result. Running both candidate positive targets prevents that
particular mutant from passing the candidate's script, but it does not turn
the broader false rewrite into a valid derived rule.

To be admissible, the summary would need to match the exact scope-0 and
scope--1 dependencies established by the loop theorem, or be supported by a
new bridge-free theorem over its complete broad match domain. The present
candidate contains neither.

Evidence:

- `evidence/05_rule_inventory.log`
- `evidence/05_inventory_counts.tsv`
- `evidence/05_bridge_generalization.k`
- `evidence/05_bridge_malformed_base.k`
- `evidence/05_bridge_malformed_witness.k`
- `evidence/05_bridge_tests.sh` and `evidence/05_bridge_tests.log`
- `evidence/05_verification_body_mutant.k`
- `evidence/05_body_sensitivity.sh` and
  `evidence/05_body_sensitivity.log`

Static-soundness result: fail. The rule enables a false conclusion and is
material to closure of the entry theorem.

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation artifact. The fresh mutation in
`evidence/06_spec_vacuity.k` changes the returned first component to

```text
evenDigits(strToCodes(Int2String(absInt(N)))) +Int 1
```

while leaving the actual call and all precondition cells intact. It is
demonstrably false at the satisfying input `N = 0`: the real/original result
is `(1,0)`, while the mutation requires `(2,0)`.

`kprove --dry-run` exited 0, establishing that the mutation parsed and built.
The real proof run exited 1 with `WarnStuckClaimState`; its residual explicitly
contains the failed equality

```text
evenDigits(...) +Int 1 == evenDigits(...)
```

This is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash.

Evidence:

- `evidence/06_spec_vacuity.k`
- `evidence/06_nonvacuity.sh`
- `evidence/06_nonvacuity.log`

Non-vacuity result: pass. This does not cure the unsound operational bridge.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

Under the bridge-free supplied semantics, the loop claim establishes the
stated counter and final-target transformation for the exact three-frame
scope configuration. Under the extended theory containing the priority-40
summary rule, the entry claim establishes that a call from the normal initial
configuration reaches the tuple of `evenDigits` and `oddDigits` applied to
the code sequence for `str(abs(N))`.

The second statement is not accepted as a proof about the real program because
the extended theory contains the false operational transition demonstrated in
stage 5. A prior proof of a narrower claim is not a universal connection
theorem for the broader rewrite.

### Trust ledger

- **Trusted supplied semantics.** The unchanged mounted semantics defines
  integers, strings, calls, scopes, loops, iteration, and returns. This is the
  benchmark-selected language model. Its unrelated incomplete or opaque
  operations are not used.
- **K mathematical primitives.** `absInt`, `Int2String`, `ordChar`, integer
  arithmetic, string hooks, maps, and equality are low-level K trust
  boundaries. They are generic operations, not task-answer oracles.
- **Translator.** The trusted Python-AST translator is an external trusted
  bridge. Byte-identical regeneration and KAST comparison pin exactly what it
  emitted; the proof does not prove the translator itself correct.
- **Decimal-code intent bridge.** `str(abs(N))` is represented by
  `strToCodes(Int2String(absInt(N)))`. Decimal digit codes have the same parity
  as their digits because code 48 is even. This is ordinary mathematics over
  the fixed string representation and is additionally supported, but not
  universally proved, by the independent differential run.
- **Partial correctness.** The claims establish results for terminating
  executions; they do not prove termination. The fixed loop is finite for the
  finite decimal representation supplied by `Int2String`.
- **Unused opaque symbols.** The 27 no-evaluator declarations for floats,
  sorting, and digest behavior are outside this program's dependency slice.
- **Proof-local loop summary.** This is not an acceptable trust boundary. It
  replaces program-defined execution, affects the returned counters, and has a
  match domain for which fixed semantics provably disagrees.
- **Tests and traces.** Concrete K execution and 2,646 Python differential
  cases are finite supporting evidence only. Candidate prose, generation
  traces, and old `#Top` reports are not proof premises.

The implementation, formal domain, postcondition, real-program pinning, and
non-vacuity checks are otherwise adequate. The verdict is nevertheless
`FAIL / NOT_LEGIT` because the reconstructed entry proof relies on a materially
unsound proof rule that makes a false completion provable.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
