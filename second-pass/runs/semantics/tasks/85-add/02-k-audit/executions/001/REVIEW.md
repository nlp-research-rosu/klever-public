# Adversarial audit: 85-add

The candidate is **not a legitimate whole-program proof**, despite both
submitted claims reconstructing to `#Top`. The arithmetic loop invariant is
genuine and the program appears extensionally correct, but the whole-function
proof uses an operational loop-summary rule whose omitted stack/control cells
make its match domain materially broader than its justification. A concrete
non-empty integer-list witness closes under the candidate extension and fails
under fixed semantics with observably different control and locals.

Exact commands, statuses, and bounded logs are indexed in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the mode and there is no infrastructure breach.

The independent manifest checker
[`evidence/01_integrity_check.py`](evidence/01_integrity_check.py) found:

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `1b531c91af204375f7c6a3e26b64368b1cbbf1bde6d61e83f47f1451c2c7a222`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- The complete candidate `reference-semantics/` manifest has the same 25
  file/directory entries, entry types, and file digests as the trusted tree.
  There are no missing, additional, changed, mistyped, or symlinked semantics
  entries.
- All core source/proof artifacts (`solution.py`, `solution.mpy`, `spec.k`,
  and `verification.k`) are regular files. No candidate symlink exists.
- Required untrusted provenance artifacts `run-input.json`, `metrics.json`,
  `codex-last.txt`, and `codex-output.log` are all missing. No structured
  generation-trace candidate is present. They could not be read as claims and
  provide no audit support.
- Candidate `__pycache__/solution.cpython-310.pyc` is an extra generated
  non-source artifact. It was ignored and not copied to scratch.

The detailed manifest result is
[`evidence/01_integrity.log`](evidence/01_integrity.log). Only source artifacts
were copied into `/tmp/audit-work`; no candidate cache or compiled definition
was reused.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for a non-empty list of integers, sum the elements
that are both at odd zero-based indices and even. Thus
`[4, 2, 6, 7]` returns `2`. The trusted canonical implementation iterates
indices `1, 3, ...`, filters values divisible by two, and sums them.

Candidate `solution.py` implements the same computation with a Boolean
`odd_index` flag. It starts false, toggles after every element, and adds the
current value exactly when the flag is true and the value is even. The initial
`value = 0` is redundant but harmless. Empty input, though excluded by the
prompt, also returns zero and is included by the formal claim.

Fresh translation with the trusted translator produced
[`evidence/02_solution.regenerated.mpy`](evidence/02_solution.regenerated.mpy).
It is byte-identical to submitted `solution.mpy`; both have SHA-256
`17a2689caa9b09f7d9c2d776cba052b70c85fdec5f16fcc1f3bf2ed8ab4fe227`.
See
[`evidence/02_translation_identity.log`](evidence/02_translation_identity.log).

The independent differential harness
[`evidence/02_differential.py`](evidence/02_differential.py) imports the trusted
canonical entry point and scratch candidate entry point separately. It ran:

- 15 documented/boundary cases, including empty, lengths one and two, index
  boundaries, even/odd/zero/negative values, mixed signs, and large integers;
- every list of lengths 0 through 5 over
  `[-3,-2,-1,0,1,2,3]` (19,608 cases); and
- 1,000 deterministic generated non-empty lists of lengths 1 through 40 with
  values in `[-10^30,10^30]`.

All 20,623 preserved inputs are in
[`evidence/02_all_cases.json`](evidence/02_all_cases.json), digest
`797b266c602a07ae84e7639b89780d841a630f0397d062aaf5d4d5a0864e8846`.
There were zero mismatches and exit status was zero
([`evidence/02_differential.log`](evidence/02_differential.log)). This is finite
fidelity evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

K v7.1.337 and Python 3.10.12 were available
([`evidence/03_tool_versions.log`](evidence/03_tool_versions.log)).

From the source-only scratch copy:

1. The supplied concrete semantics compiled freshly with LLVM, module
   `MPY-KRUN`, exit zero
   ([`evidence/03_kompile_llvm.log`](evidence/03_kompile_llvm.log)).
2. `concrete_tests.py` was freshly translated with the trusted translator; the
   result was byte-identical to submitted `concrete-tests.mpy`. The regenerated
   program ran under the fresh LLVM definition to `<k>.K</k>`,
   `<exit-code>0</exit-code>`, exit zero
   ([`evidence/03_krun_regenerated_concrete_tests.log`](evidence/03_krun_regenerated_concrete_tests.log)).
3. `verification.k` compiled freshly with the Haskell backend, exit zero
   ([`evidence/03_kompile_haskell.log`](evidence/03_kompile_haskell.log)).
4. `SPEC.loop-invariant-bound` was selected and run independently. It exited
   zero and printed `#Top`
   ([`evidence/03_kprove_loop.log`](evidence/03_kprove_loop.log)).
5. `SPEC.add-correct` was selected and run independently. It exited zero and
   printed `#Top`
   ([`evidence/03_kprove_entry.log`](evidence/03_kprove_entry.log)).

These are valid verification results under the submitted extended theory. They
do not by themselves establish that every proof-local rewrite is sound.

The LLVM build warned about non-exhaustive `[total]` matches in supplied,
unused operations (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`). None lies on this integer-only program/proof slice. I therefore
record these as fixed-semantics coverage limitations, not as witnessed
unsoundness.

## 4. Adequacy and real-program pinning

### Claim meanings

`loop-invariant-bound` has the following precondition: `INPUT` is any finite
`IntSeq`; the current K computation is exactly the real loop over
`list(intVals(INPUT))` with target `value` and the exact submitted loop body;
the active scope has integer accumulator `ACC`, Boolean phase `ODD`, integer
old `value`, arbitrary `lst`, and a non-colliding scope location. Other
configuration cells are framed. Its postcondition is termination of that loop
with the active scope's `total` equal to
`addAccSpec(INPUT, ODD, ACC)`. Other final bindings are existential. In plain
language, it says the remaining loop adds exactly the even elements visited
while the alternating phase flag is true.

`add-correct` has no extra `requires` clause. Its formal input domain is every
finite integer sequence, including empty. It starts from the exact initial
module/builtins configuration, loads `solutionModule`, and calls `add` on the
encoded list. It requires the final K result to be exactly
`addAccSpec(INPUT,false,0)`; the result is not a free variable, tautology, or
one-way implication. Environment, heap, allocation counters, stack, return
state, exception state, and exit code are fixed to their initial/final values;
only final scopes are existential.

### Program identity and satisfying states

The claim names a macro rather than reading `solution.mpy` at proof time, so I
checked the expansion rather than trusting visual similarity. Fresh `kast`
parsing/expansion of submitted `solution.mpy` is byte-identical to expanded
`solutionModule`; both KAST files have SHA-256
`aeb750aa8fa758142a95e2d87224da892d687ec98055253a5f1528a7bc108bc0`.
See [`evidence/04_program_pinning.log`](evidence/04_program_pinning.log),
[`evidence/04_solution.parsed.kast`](evidence/04_solution.parsed.kast), and
[`evidence/04_solution-macro.kast`](evidence/04_solution-macro.kast). The
formal K term therefore pins the actual submitted generated AST.

Fresh ground claims in
[`evidence/04_ground-witness.k`](evidence/04_ground-witness.k) exhibit:

- the complete entry precondition with input `[4,2,6,7]`, proving ground result
  `2`; and
- a loop precondition with remaining input `[2,3]`, `ODD=true`, `ACC=5`, and a
  concrete active scope, proving final `total=7`, final phase true, and final
  `value=3`.

Both ground claims exit zero with `#Top`
([entry log](evidence/04_ground_entry.log),
[loop log](evidence/04_ground_loop.log)). For the documented entry witness,
the candidate Python function, trusted canonical Python function, and
`addAccSpec` all yield `2`. The preserved mixed-sign witness
`[1,-2,3,4,5,-6]` yields `-4` in both Python implementations and by direct
substitution into the four `addAccSpec` equations.

Thus the claims are satisfiable, result-constraining, and syntactically pin the
real program. Adequacy does not cure an unsound contributing rule.

## 5. Rule-by-rule static soundness review

The complete source inventory is
[`evidence/05_rule_inventory.md`](evidence/05_rule_inventory.md), generated by
the preserved inventory script
[`evidence/05_inventory.py`](evidence/05_inventory.py). It enumerates every
local declaration/rule in the supplied root/helper files, `verification.k`,
and `spec.k`, folding all cells, guards, and attributes into each record:

- 658 ordinary rules and 48 priority rules;
- 123 non-opaque function declarations and 25 opaque/symbol declarations;
- 85 other syntax declarations, five contexts, one configuration, and two
  claims; and
- zero simplification/simplifier rules.

Because this is supplied-semantics mode and tree integrity passed, every
supplied item is accepted as part of the selected fixed semantic level. The
program's used syntax/rule slice, configuration/cell behavior, evaluation
order, calls/returns, iteration, binding, guards, integer operations, and
state changes are mapped with source lines in
[`evidence/05_rule_assessment.md`](evidence/05_rule_assessment.md).

### Candidate-local inventory

`verification.k` contributes four ordinary syntax declarations, two function
declarations, eight ordinary rules, and three priority rules:

- `intVals(IntSeq)` plus two disjoint/exhaustive iterator rules truthfully
  expose the head and tail of a finite integer input. They do not overlap the
  supplied `.ValSeq`/`vCons` list iterator rules.
- Total `scopeMap(scope(M,P)) = M` is exhaustive because `scope` is the only
  `Scope` constructor. It is unused.
- `addAccSpec` has a base equation and three recursive cases. Recursion
  strictly descends; false/true phase cases cover both Booleans; the two true
  branches have complementary modulo guards. It is a fully defined
  mathematical summary, not an oracle.
- `addLoopBody`, `addFunctionBody`, and `solutionModule` are exact macros. The
  KAST identity check above independently pins them to the submitted AST.
- The priority-30 rule at `/candidate/verification.k:57` is an operational
  bridge. It replaces the complete loop, the empty statement tail, and the
  exact `Return(total) ~> #endcall` suffix with
  `Return(addAccSpec(INPUT,false,0)) ~> #endcall`.

The loop's value summary is independently defensible: after removing the
operational bridge and rebuilding a separate Haskell definition, the same
universal loop invariant still exits zero with `#Top`
([source](evidence/05_loop-only-no-bridge.k),
[log](evidence/05_kprove_loop_no_bridge.log)). Changing the actual body to
test odd rather than even values builds successfully and makes the original
summary fail with the expected result-condition residual
([mutant](evidence/05_verification-body-mutant.k),
[claim](evidence/05_body-sensitivity.k),
[log](evidence/05_kprove_body_mutant.log)). The loop proof is body-sensitive.

### Materially unsound operational bridge

The bridge is nevertheless unsound on its complete match domain. It checks the
K suffix, environment location, and four exact local bindings, but omits
`<stack>`, `<ret>`, `<scopeLoc>`, heap, exception, and exit cells. Its conclusion
also skips all loop updates to `total`, `odd_index`, and `value`. A valid call
frame would later delete those locals, but the rule does not require such a
frame.

The required false-conclusion witness is
[`evidence/05_bridge-domain-witness.k`](evidence/05_bridge-domain-witness.k):

- intended non-empty integer input `[4,2]`;
- exact local bindings `lst=[4,2]`, `total=0`, `odd_index=false`, `value=0`;
- exact submitted loop/return continuation;
- `ret=noRet`; but
- `stack=.List`, which the bridge admits because the cell is omitted.

Under the candidate definition, `kprove` exits zero with `#Top`, proving the
bridge target `Return(2) ~> #endcall` while all initial locals remain unchanged
([`evidence/05_bridge_domain_extended.log`](evidence/05_bridge_domain_extended.log)).
Under the freshly rebuilt definition with only the bridge removed, the same
claim fails. Fixed execution performs the loop, reaches `total=2`,
`value=2`, `retV(2)`, and sticks at `#pop` because there is no frame; it cannot
reach the candidate target
([fixed claim](evidence/05_bridge-domain-witness-no-bridge.k),
[fixed log](evidence/05_bridge_domain_fixed.log)).

This is a concrete, machine-checked false reachability conclusion on an
intended-domain input, with differences in control state and local state. It is
not merely a missing generality proof. It also demonstrates why the broader
bridge-connection diagnostics could not be established without the candidate
rule; those failed diagnostics are retained in the command index.

The whole-function symbolic execution reaches precisely the bridge's
function-entry match and uses that rule to obtain the returned summary.
Therefore the reconstructed `#Top` for `add-correct` depends on a materially
unsound proof extension. The fact that the bridge behaves observationally as
intended on the normal valid-frame path, and that the intended result happens
to be true, does not make the submitted proof theory sound. The decision rule
permits an over-broad rule as a concern only when it does not make a false
conclusion provable; this rule does.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I created the independent
mutation
[`evidence/06_spec-vacuity-audit.k`](evidence/06_spec-vacuity-audit.k), changing
the whole-function result to
`addAccSpec(INPUT,false,0) +Int 1`.

The witness `[4,2,6,7]` satisfies the original entry precondition. Both Python
implementations and the correct formal summary return `2`; the mutation
requires `3`.

The mutated spec dry-run built/parsed successfully, exit zero
([`evidence/06_vacuity_dry_run.log`](evidence/06_vacuity_dry_run.log)). The
actual proof exited one with `WarnStuckClaimState` and the expected unmet
condition
`addAccSpec(INPUT,false,0) +Int 1 == addAccSpec(INPUT,false,0)`
([`evidence/06_vacuity_proof.log`](evidence/06_vacuity_proof.log)). This is a
reachable, result-bearing failure, not a parser error, import error, timeout,
or unrelated crash. Non-vacuity therefore passes.

## 7. Proven-versus-assumed accounting

What is genuinely established:

- Under the supplied fixed semantics plus the honest `intVals` and
  `addAccSpec` definitions/macros, the bridge-free loop reachability claim
  establishes that the real loop's final accumulator is
  `addAccSpec(INPUT,ODD,ACC)` for every finite integer sequence.
- Under the full candidate theory, including the unsound priority-30 bridge,
  `add-correct` establishes that the expanded submitted function returns
  `addAccSpec(INPUT,false,0)` from the stated initial configuration.
- The second statement is not a legitimate fixed-semantics proof because the
  contributing theory can prove the false bridge-domain transition above.

Trust and assumption ledger:

1. **K toolchain and built-in domains.** K v7.1.337, Haskell/LLVM backends, and
   built-in unbounded integer, Boolean, String, Map, List, equality, and
   arithmetic hooks are trusted. This is the ordinary unavoidable
   machine/prover boundary.
2. **Supplied semantics.** The exact trusted `reference-semantics` tree is the
   mandated fixed semantic level. Its full inventory is preserved. The used
   integer/control/function slice directly governs the theorem; unused
   coverage warnings are disclosed above.
3. **Supplied opaque/symbol declarations.** The 25 inventoried names are
   `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
   `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
   `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
   `roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`. None is reachable from
   `solution.mpy`, `addAccSpec`, or either submitted claim, so none influences
   the verdict or result.
4. **Input representation.** `intVals` is a structural encoding of a finite
   Python integer list into the K algebraic `IntSeq`; its two iterator
   equations fully expose that structure. This is an acceptable explicit
   formal-domain bridge, not an unconstrained primitive.
5. **Intent bridge.** The statement that `addAccSpec(INPUT,false,0)` means “sum
   even elements at odd indices” follows informally by induction over its four
   equations and is supported by zero mismatches over 20,623 independent
   differential cases. The finite tests support only this source/intent
   bridge; they do not prove universal equivalence.
6. **Source/AST bridge.** Trusted translation is byte-identical to submitted
   `solution.mpy`, and expanded `solutionModule` is KAST-identical to that file.
   This bridge is machine-checked and acceptable.
7. **Operational bridge at `verification.k:57`.** The candidate assumes exact
   execution equivalence over a match domain that omits necessary control
   cells. Its dependent is the whole-function `add-correct` closure. The
   opposite fixed-semantics witness is rejected while the extended witness
   closes, so this assumption is illegitimate.

The missing generation logs and metrics further reduce provenance
auditability, but they are not being used as a substitute reason for the
verdict. The verdict follows from the reconstructed, machine-checked
proof-extension counterexample.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
