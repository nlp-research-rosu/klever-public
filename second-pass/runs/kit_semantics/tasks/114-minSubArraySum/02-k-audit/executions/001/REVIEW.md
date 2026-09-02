# Independent adversarial review: 114-minSubArraySum

## Overall assessment

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program over the material source-contract domain: every non-empty
finite list of mathematical integers, with unrestricted length and magnitude.
Fresh Haskell reconstruction proves both the loop circularity and the complete
target, and a constructor-level comparison pins the target closure to the
trusted regeneration of `solution.mpy`.

I assign `CONCERNS / LEGIT`, not `PASS`, for two non-fatal auditability limits.
First, the two result-bearing proof-local simplification lemmas are true
sort-specializations of the fixed integer rules, but the exact bridge-free
claims with a symbolic `V:Val` guarded by `isInt(V)` remain stuck because K does
not refine the cast from that predicate. The fixed rules prove the same
equalities over symbolic `Int` arguments, and I found no false conclusion
witness, so this is an evidence gap rather than an unsoundness finding. Second,
the K postcondition is the exact Kadane recurrence; its equivalence to “minimum
sum of a non-empty contiguous sub-array” is established by an ordinary
mathematical induction and differential evidence, not by a second K theorem
that formalizes sub-arrays.

All candidate-provided prose, caches, traces, and prior `#Top` results were
treated only as untrusted claims.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. The required trusted semantics mount
`/reference/reference-semantics` is present, so the rendered mode and mounts do
not conflict.

I independently checked:

- `/audit-campaign-lock.json` is a regular non-symlink, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed JSON exactly equals the `audit_campaign` block.
- Every required pipeline-v3 record is present, readable, regular, and
  non-symlinked: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  Every launcher-recorded file hash matches.
- The sole trace file is regular, has SHA-256
  `95fc2f80c818de12d3ef78a4a5d6496dd0cdf5d688e6c8191a343c74bce0f46f`,
  and its path/hash set exactly matches `/generation-result.json`.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The candidate and trusted `reference-semantics/` trees have exactly the same
  relative entry set, entry types, and file bytes. Neither tree contains a
  symlink or special entry. My independent manifest digest for both trees is
  `51c71872287731bc1458ed960ef68fb8126adae2af5e488b22b5549c1a8e69ec`.

The generation records and trace were read as history only. They claim success,
but no result below depends on that claim. Candidate `runtime-kompiled/`,
`verification-kompiled/`, bytecode, and caches were not copied into scratch or
used.

Evidence: `evidence/01_integrity_check.py`,
`evidence/01_integrity.log`, `evidence/02_copy_sources.log`, and
`evidence/03_copy_trusted_inputs.log`. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py:2-8` requires the minimum sum of any non-empty contiguous
sub-array of an integer array. Thus the material domain is non-empty finite
integer arrays. This reading is also forced operationally by the trusted
canonical implementation: on an empty list it eventually calls `max` on an
empty sequence.

`/reference/canonical.py:14-24` negates the elements and computes a maximum
sub-array sum. `/candidate/solution.py:1-7` uses the equivalent minimum-Kadane
recurrence:

```text
current' = min(value, current + value)
minimum' = min(minimum, current')
```

The implementation is read-only with respect to the input.

### Trusted regeneration

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced byte-identical output to submitted `solution.mpy`. Both
MPY files have SHA-256
`7a9c5daebb3c0d59908bb84ba2f39752d8ac4874252f29782888a7e758bc92a7`.
See `evidence/04_translation_identity.log`.

### Independent differential

`evidence/02_differential.py` independently imports the trusted canonical and
generated entry points and also uses a nested enumeration of all non-empty
sub-arrays as a third oracle. It covers:

- both documented examples;
- singleton positive, negative, and zero values;
- zero, tie, reset, all-positive, all-negative, and mixed-sign boundaries;
- unbounded-Python-integer representatives up to approximately `10**81`;
- every list of lengths 1 through 5 over values `-3..3`;
- 1,000 deterministic lists of lengths 1 through 30 over values
  `-1000..1000`.

The exact run checked 20,621 in-domain cases with zero mismatches
(`evidence/05_differential.log`). On the separately recorded empty boundary,
the canonical raises `ValueError` and the generated function raises
`IndexError`. This exception-type difference is outside the contract because
there is no non-empty sub-array of an empty input; importantly, both reject it.

Program fidelity passes.

## 3. Clean proof reconstruction

All builds and experiments were performed in
`/tmp/audit-work/114-minSubArraySum`. Only K/Python source and the trusted
semantics tree were copied there.

### Concrete definition

The fresh command in `evidence/06_llvm_kompile.log` was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. Fresh `krun solution.mpy --definition
audit-runtime-kompiled` also exited 0, with `.K`, `NoExc`, exit code 0, and a
module binding whose closure body is the expected translated function
(`evidence/07_krun_solution.log`).

The LLVM build reports non-exhaustiveness warnings for several fixed-semantics
`total` functions. The only warned function on this program's path is
`valSeqAt`; the target always indexes a constructor-known non-empty list at
zero, where the explicit first equation applies. The other warnings concern
unused string/float helpers.

### Proof definition and positive claims

The fresh Haskell build in `evidence/08_haskell_kompile.log` was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0. I then ran both proof scopes:

- `SPEC.loop-invariant` alone printed `#Top` and exited 0
  (`evidence/09_kprove_loop.log`).
- The complete `SPEC` module, containing `loop-invariant` and `target`, printed
  `#Top` and exited 0 (`evidence/10_kprove_all.log`).

The complete run is the relevant target run because `SPEC.target` uses the loop
claim as a circularity. No candidate-provided compiled definition was used.
Clean reconstruction passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` (`/candidate/spec.k:6-44`) says:

- Start at the real `#loop(list(VS), Name("value"), BODY)` with an arbitrary
  continuation and stack.
- The local frame contains integer `current = C`, integer `minimum = B`, and
  the other exact locals; every element of `VS` is an integer; the module does
  not shadow builtin `min`.
- When the loop finishes, `current` equals `kadaneCurrent(VS,C)` and `minimum`
  equals `kadaneMinimum(VS,C,B)`. Heap, allocation counters, stack,
  return/exception state, and exit code are preserved. The final loop-target
  local is existentially abstracted, but it is dead after the loop and cannot
  affect the return or any observable cell.

`SPEC.target` (`/candidate/spec.k:46-95`) says:

- Start by calling the exact bound `minSubArraySum` closure on
  `list(vCons(H,XS))`, where `H` is an `Int` and every element of `XS` is an
  `Int`.
- If execution reaches a result, that result is exactly
  `kadaneMinimum(vCons(H,XS),0,H)`.
- The environment, scope store, heap, allocation counters, stack,
  return/exception state, and exit code have returned to the specified
  caller state.

These preconditions admit every non-empty finite list of K mathematical
integers; there is no length or magnitude bound.

### Mechanical program identity

`evidence/03_constructor_compare.py` uses K's parser twice: once on trusted-
regenerated `solution.mpy` and once on the exact `closureVal` text extracted
from `SPEC.target`. It mechanically verifies:

- the source function name equals the target map binding;
- the parameter constructor tree is identical;
- the complete statement constructor tree is identical;
- the closure's defining environment is module frame 0.

The normalized body constructor SHA-256 is
`b0b1217186f7b8ab806c02158a50e921ae95d2bb92ab5bdc6f4a343c0f595067`.
The successful comparison is `evidence/14_constructor_compare.log`. Logs 11
and 13 retain two bounded parser-surface experiments that failed before the
semantic syntax parser and generated-list normalization were selected; they do
not affect the successful comparison.

The target starts after module loading, but trusted regeneration, the KAST
comparison, and fresh concrete loading together establish the allowed
constructor-level normalization from `Module(FuncDef(...))` to the exact bound
closure. This is real-program pinning, not a substituted implementation.

### Real control flow and witnesses

The target executes call lookup, argument evaluation, parameter binding,
`nums[0]`, both initial assignments, the first real loop iteration, circular
loop reuse, both builtin calls, return, and frame pop. The first iteration is
necessarily unrolled because the invariant frame includes the loop-target
binding; subsequent iterations are summarized by the proved circularity.

`evidence/04_satisfying_witness.py` and
`evidence/15_satisfying_witness.log` exhibit:

- a loop state with `VS=[-2,4,-7]`, `C=1`, `B=3`, empty module map, and
  `allInts(VS)=true`, whose claimed post-state is `current=-7`,
  `minimum=-7`;
- target states `[5]`, `[3,-4,2]`, and `[-1,-2,-3]`, whose claimed recurrence
  results are respectively `5`, `-4`, and `-6`, equal to both Python
  implementations.

The independently rerun body mutation embeds a materially changed closure term
(`current = current + value`) and requires `-5` for `[2,-5,3]`. Fresh execution
reaches `-3`, yielding `WarnStuckClaimState` and exit 1
(`evidence/23_body_sensitivity.log`). It therefore tests theorem dependence on
the executed body, not merely on an external source file.

There is no material adequacy or pinning gap. The use of an unboxed `list`
value for a read-only claim input is an explicit convention of the supplied
semantics; no aliasing or mutation behavior is relevant to this program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.py` scans the complete supplied semantics,
`verification.k`, and `spec.k`. The final exhaustive output is
`evidence/18_rule_inventory.log`:

- 1,081 records;
- 703 rules: 695 fixed-semantics rules and 8 proof-local rules;
- 230 syntax declarations: 227 fixed and 3 proof-local;
- 1 configuration, 5 evaluation contexts, and 2 claims;
- 108 `total`, 149 `function`, 45 priority, 26 `owise`, 36 `concrete`,
  25 opaque/backend-symbol, and exactly 2 `simplification` declarations/rules.

The inventory records every module/import, syntax declaration and attributes,
ordinary/equational/operational rule, guard, priority, and complete claim with
source line.

The 695 supplied rules define the selected fixed semantics rather than being
candidate proof extensions. I classify each unused fixed rule as part of that
declared trust boundary; because the program's constructor tree cannot reach
the corresponding syntax, it cannot contribute to target closure. The used
path was reviewed individually as follows.

| Submitted construct/operation | Declaration and fixed rules | Static judgment |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k:53-61`, `core.k:124-127`, `functions.k:14-20` | Module sequencing creates exactly the closure seen in fresh `krun`; no proof-local interception. |
| Function call and parameter `nums` | `call.k:20-21,69-74`, `core.k:185-191`, `functions.k:63-66,78-90` | Callee and arguments evaluate left-to-right, a real frame is pushed, the parameter is bound, return state is set, and the caller frame is restored. |
| Names, integers, statements, assignments | `core.k:125-132,152-181,189-196`, `controls.k:9-18` | Exact lexical lookup reaches the local/module scopes and then `builtinsScope`; ordinary assignments update the current non-cell frame. |
| `nums[0]` | `syntax.k:22,41`, `subscript.k:11-41`, `core.k:223-225` | Strict object/index evaluation followed by `normIdx(0,len)` and the in-bounds head equation. The total out-of-bounds abstraction is unreachable. |
| `for value in nums` | `controls.k:65-74`, `iter.k:8`, `list.k:9-10`, `tuple.k:31-41` | Each constructor is consumed once, the real target binding occurs, the body executes, and control returns to the next real `#loop`. |
| Integer `+` | `syntax.k:15`, `operators.k:12`, `int.k:9` | Operand order is `seqstrict`; fixed dispatch is mathematical integer addition. The local specialization below is value-equivalent. |
| Calls to builtin `min` | `call.k:20-32`, `core.k:131-181,185-191`, `builtins.k:17,96-105` | The invariant's module guard prevents shadowing; lookup selects `builtinV("min")`; both arguments evaluate before the pure variadic fold. |
| `Return(minimum)` | `syntax.k:50`, `functions.k:78-90` | The expression evaluates normally; return discards only the function suffix, restores caller control, and exposes the constrained integer result. |

Heap allocation/mutation, exceptional paths, non-local cells, imports, and
abrupt loop control are not present in the submitted constructor tree. The
configuration fixes an empty heap, and the proof preserves it.

### Proof-local rule decisions

1. **`allInts`** (`verification.k:8-10`) is a total definitional predicate.
   `ValSeq` has only `.ValSeq` and `vCons`; the rules are disjoint, exhaustive,
   and structurally decreasing. It restricts the formal domain and replaces no
   execution.

2. **Guarded `applyBin("+", I:Int, V:Val)`** (`verification.k:12-14`) is a pure
   derived simplification after fixed operand evaluation. Its complete domain
   is `isInt(V)`. On the only satisfying value sort, write `V=J:Int`; the fixed
   `int.k:9` rule and the local right side both equal `I +Int J`. On overlap
   with the fixed rule the right sides are identical. It touches no cell,
   binding, continuation, or control state.

3. **Guarded two-argument builtin `min`** (`verification.k:16-19`) is also a
   pure post-evaluation specialization. For `V=J:Int`, fixed
   `builtins.k:103-105` reduces
   `applyBuiltin("min",J,I,.Vals)` to `minInt(J,I)`, exactly the local right
   side. The target and invariant separately pin name lookup to builtin `min`,
   so this rule does not select a binding or skip argument evaluation.

4. **`kadaneCurrent`** (`verification.k:22-28`) is a structurally decreasing
   definitional summary. Empty and guarded-cons cases are disjoint; every use
   is covered by `allInts`.

5. **`kadaneMinimum`** (`verification.k:30-37`) has the same coverage and
   descent properties and reproduces the two source assignments in order. It
   names the post-state value and never rewrites a program constructor.

There are no proof-local priority rules, operational bridges, abrupt-control
rules, fresh or opaque result symbols, or task-answer oracles. The loop
circularity itself executes the body and fixed controls; it does not appear as
an ordinary semantic rewrite in `verification.k`.

### Connection evidence and limitation

I built `evidence/audit-connection-verification.k`, which imports `MPY` without
any candidate extension. Symbolic fixed-domain claims with both arguments
typed `Int` prove the addition and min equalities (`#Top`, exit 0,
`evidence/20_fixed_dispatch_proof.log`).

The stronger claims retain `V:Val`, add `requires isInt(V)`, and use the K cast,
exactly matching the two simplification guards. Both independently get
`WarnStuckClaimState` because the implication checker does not derive
definedness/equality of `project:Int(V)` from the symbolic sort predicate
(`evidence/21_guarded_connection_attempt.log` and
`evidence/22_guarded_min_connection_attempt.log`). This does not supply a false
conclusion witness. The ground constructors satisfying `isInt` are precisely
the `Int` subsort, and the proved fixed-domain equations then apply. Following
the requested decision rule, I report the narrower universal-evidence gap
rather than calling either rule unsound.

The 25 fixed opaque/backend symbols are: `md5hexCodes`; `sortVS` and
`sortKeyVS`; and the float helpers `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. None is reachable from this program or its
postcondition. The used mathematical primitives are fixed K `Int` addition,
comparison, `minInt`, sort predicates/casts, finite algebraic lists, maps, and
the reachability engine.

No rule reviewed admits a demonstrated false conclusion on the intended input
domain.

## 6. Fresh non-vacuity test

I did not reuse candidate `spec-vacuity.k`. The reviewer-authored
`evidence/audit-false-result.k` invokes the exact submitted closure on the
satisfying input `[3,-4,2]` and changes only the result obligation from the true
`-4` to the false `-3`.

- `kprove ... --dry-run` parsed and built the mutation successfully, exit 0
  (`evidence/24_false_mutation_dry_run.log`).
- The real proof run exited 1 with `WarnStuckClaimState`; its final
  configuration contains `<k> -4 ~> .K </k>` against required `-3`
  (`evidence/25_false_mutation_proof.log`).

This is the expected reachable unmet obligation, not a parser error, timeout,
or unrelated crash. Together with the separate body-sensitivity residual, it
shows both result constraint and dependence on the real body. Non-vacuity
passes.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied `MPY` definition and the eight local equations reviewed
above, for every `H:Int` and every finite `XS:ValSeq` satisfying
`allInts(XS)`, if the exact submitted `minSubArraySum` closure terminates on
`list(vCons(H,XS))`, it returns
`kadaneMinimum(vCons(H,XS),0,H)` and restores the explicitly constrained caller
cells. The helper claim universally characterizes the real loop's `current`
and `minimum` local post-state over every finite integer suffix.

This is partial correctness. Termination is not part of the reachability
theorem, although the fixed list iterator structurally consumes one constructor
per iteration.

### Recurrence-to-contract argument

For a sequence `x1,...,xn`, after processing `xk`, let `Ck` be the recurrence's
`current`. Base execution gives `C1=x1`. Inductively,
`Ck=min(xk,C(k-1)+xk)`, which is exactly the minimum sum of a non-empty
contiguous sub-array ending at position `k`: such an array is either `[xk]` or
extends a minimum ending array at `k-1`. The recurrence's `minimum` is
`min(B(k-1),Ck)`, so by induction it is the minimum over all non-empty
contiguous sub-arrays in the processed prefix. At `n` it is the prompt result.

This short mathematical proof is sound and covers arbitrary length, but it is
an informal intent bridge rather than a separate machine-checked combinatorial
K claim. The 20,621-case independent differential supports, but does not
replace, that induction.

### Trust ledger

| Boundary | Influence | Evidence and assessment |
|---|---|---|
| Supplied `reference-semantics/` and its fixed K primitives | Value, binding, control, state, and exceptions | Integrity-identical to the trusted mount. Used rules were reviewed individually; unused rules/opaque symbols cannot be reached. Acceptable selected-semantics boundary. |
| K v7.1.293 compiler, Haskell/LLVM backends, solver, and reachability implementation | All machine-checking results | Tool versions match the campaign; fresh builds and independent positive/negative runs are reproducible. Necessary standard trust boundary. |
| Trusted `py2mpy.py` and CPython AST parsing | Source-to-MPY bridge | Trusted regeneration is byte-identical; KAST body comparison pins the exact target closure. Acceptable. |
| Two `isInt(V)` sort-specialization lemmas | Result-bearing integer addition and min | Fixed symbolic `Int` equations prove; exact guarded `Val` connection claims remain stuck; constructor/sort analysis supplies the missing reasoning and no false witness exists. Legitimate but auditable only with this manual sort argument, hence a concern. |
| `kadaneCurrent`/`kadaneMinimum` definitions | Loop and final result | Truthful, guarded, structurally decreasing equations; machine-checked loop connection. Acceptable. |
| Kadane recurrence equals minimum non-empty sub-array | Human-facing result meaning | Ordinary induction above plus independent canonical/oracle differential. Sound but not itself a K theorem, hence a concern. |
| Partial-correctness termination premise | Termination only | Explicitly excluded from the formal theorem; finite concrete list iteration is operationally structurally decreasing. Acceptable for the requested proof kind. |
| Fixed unused opaque symbols | None | Enumerated above and unreachable; no target claim depends on them. |

The proof is not bounded to examples or fixed sizes, does not narrow the
HumanEval domain materially, does not substitute a different program term, and
does not obtain `#Top` from an answer-encoding or unconstrained oracle. The
candidate's `PROOF.md` headline `VALIDATED` overstates the universal connection
evidence for the guarded sort refinements, but that overstatement does not make
the reconstructed theorem illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
