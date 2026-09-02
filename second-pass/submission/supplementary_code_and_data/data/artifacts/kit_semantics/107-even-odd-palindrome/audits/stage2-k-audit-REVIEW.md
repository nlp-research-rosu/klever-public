# Independent adversarial review: 107-even-odd-palindrome

The candidate contains a legitimate partial-correctness proof for the complete
source-contract domain. I reconstructed both K definitions from source, proved
all 108 positive claims independently, mechanically pinned the executed closure
to the trusted translation of `solution.py`, exhaustively checked the finite
`1..1000` contract domain, inventoried every local K declaration and rule, and
obtained the required meaningful failure from a fresh false-result mutation.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3` and
`semantics_mode = SUPPLIED_SEMANTICS`. This agrees with the rendered condition:
the trusted `/reference/reference-semantics` tree exists. There is no
mode/mount contradiction.

The independent integrity program
[integrity_audit.py](/audit-output/evidence/integrity_audit.py) did the
following without relying on the launcher’s Boolean integrity claims:

- Required real, readable files were found for `/audit-input.json`,
  `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, all nine pipeline-v3 generation records, the
  trusted canonical/prompt/translator, and all required candidate proof
  artifacts. The required candidate, trace, and supplied-semantics paths were
  real directories. No required entry was a symlink or unsupported node.
- The campaign lock JSON exactly equals the `audit_campaign` block. Its
  SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly as recorded.
- Every directly recorded pipeline-v3 file hash matched, including the run and
  task manifests, stage-1 result/invocation, prompt, metrics, runtime metrics,
  usage, Codex output/last message, canonical, trusted prompt, and translator.
- The independently computed length-delimited candidate-tree digest is
  `f82c9d533b5d5132abe30319663dfc27eeefa1e6dbeaf363e22f55c97b62a601`,
  matching the stage-1 output digest. The trace-tree digest is
  `3dfecb484c75c9b5b62dc1581192b13913523267aeb607e2efa30cd0e64ffa43`,
  matching `usage.json`.
- Recursive `lstat`, relative-path, type, and content-hash comparison found
  exactly 25 entries in each supplied-semantics tree and zero differences.
  The two pipeline tree digests are both
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
  Thus there are no missing, additional, changed, mistyped, or symlinked
  candidate semantics entries.
- Candidate `prompt.py` and `py2mpy.py` match their trusted mounts byte for
  byte and by the recorded hashes.
- The structured trace’s one JSONL file was read in full: 655/655 lines parsed,
  with zero malformed events. `codex-output.log` was also read in full. Their
  reports of prior success were treated only as untrusted claims.

The command exited 0; exact values and checks are in
[01-integrity.log](/audit-output/evidence/01-integrity.log). There is no audit
infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires, for a positive integer `n` with
`1 <= n <= 10^3`, a tuple containing respectively the number of even and odd
integer palindromes in the inclusive range `1..n`. Its examples are
`3 -> (1,2)` and `12 -> (4,6)`. The trusted canonical implementation iterates
through that inclusive range, detects palindromes by string reversal, and
increments the appropriate parity count.

The candidate implementation is a different but permissible algorithm: a
107-comparison decision tree whose 108 leaves return the cumulative result
between successive palindromes. It has no loops, calls, mutable state, or
external effects inside its body.

### Trusted regeneration

I regenerated `solution.mpy` using the trusted mounted translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

The command exited 0. `cmp -s` exited 0, and both files have SHA-256
`abc2ad630f330b4db097e197609bfdcc437104fafded3ae2f8523403dc874df8`.
See
[03-translator-identity.log](/audit-output/evidence/03-translator-identity.log)
and the preserved
[regeneration](/audit-output/evidence/solution.regenerated.mpy).

### Independent differential

[differential_test.py](/audit-output/evidence/differential_test.py) separately
imports the trusted canonical entry point and the scratch candidate entry
point. It checked:

- both documented examples;
- the minimum and maximum permitted inputs;
- both sides of all 107 decision thresholds, yielding 208 distinct branch
  boundary inputs;
- 250 deterministic generated inputs (seed 107); and
- exhaustively every integer in `1..1000`.

There is no meaningful “empty collection” input because the contract accepts
one positive scalar integer; this is recorded explicitly. There were zero
mismatches. Adjacent excluded values were also observed, without treating them
as obligations: the implementations differ at `0` and `1001`, confirming why
the exact source domain matters. The script and command exited 0; see
[04-differential.log](/audit-output/evidence/04-differential.log).

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/reconstruction`.
Candidate `runtime-kompiled`, `verification-kompiled`,
`verification-mutation-kompiled`, caches, logs, and traces were not copied or
used. The supplied semantics in scratch came from the trusted reference mount,
after the exact recursive comparison above.

The live tools are K `v7.1.293`; see
[05-tool-versions.log](/audit-output/evidence/05-tool-versions.log).

Fresh concrete definition:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

This exited 0. The warnings concern non-exhaustive supplied-semantics functions
that the submitted program does not use. An independently authored translated
harness asserted results at `1, 2, 3, 11, 12, 99, 100, 101, 202, 999, 1000`.
`krun concrete_cases.mpy --definition runtime-audit-kompiled` exited 0 and
ended with `.K`, `NoExc`, and exit code 0. See
[06-kompile-llvm.log](/audit-output/evidence/06-kompile-llvm.log),
[09-concrete-execution.log](/audit-output/evidence/09-concrete-execution.log),
and the preserved
[harness](/audit-output/evidence/concrete_cases.py).

Fresh proof definition and complete positive proof:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

Both commands exited 0, and `kprove` printed literal `#Top`. This one invocation
loads and proves every claim in `SPEC`; the independent parser confirmed that
there are exactly 108 claims and no unparsed extra claim. See
[07-kompile-haskell.log](/audit-output/evidence/07-kompile-haskell.log) and
[08-kprove-positive.log](/audit-output/evidence/08-kprove-positive.log).

## 4. Adequacy and real-program pinning

Each entry claim says, in plain language:

> From the exact empty module/caller state shown in the claim, call the
> submitted one-argument closure on an integer `N` in one stated nonempty
> interval. Execution must return the stated concrete two-integer tuple, with
> environment 0 restored, the temporary scope removed, heap and stack empty,
> `noRet`, `NoExc`, and exit code 0.

The preconditions are not vacuous. The 108 intervals are nonempty, pairwise
disjoint, and have union exactly `1..1000`. For every claim, its lower bound is
a concrete satisfying witness. Every such witness’s target equals both Python
implementations; checking every point of every interval gives 1000/1000
agreement. The complete witness table is
[claim_witnesses.csv](/audit-output/evidence/claim_witnesses.csv), generated by
the independent
[pinning_and_claims.py](/audit-output/evidence/pinning_and_claims.py); its
command exited 0 in
[10-pinning-and-claims.log](/audit-output/evidence/10-pinning-and-claims.log).

The executed term is genuinely pinned to the submitted program:

- Trusted regeneration establishes `solution.py -> solution.mpy` byte
  identity.
- A constructor lexer and balanced-term extractor found the module binding
  name `"even_odd_palindrome"`, source parameter `Params("n")`, proof closure
  parameter `("n", .ParamNames)`, and definition environment `0`.
- The source function body and proof closure body each contain 3,974
  constructor tokens, with exact token-for-token identity.
- Every claim’s left side is exactly
  `Call(solutionClosure(), Int(N))`. The only `solutionClosure` equation
  unfolds to that exact parameter/body/environment closure.

Direct closure invocation omits module loading and subsequent name lookup, but
this is a semantically inert normalization here: the submitted module contains
only that `FuncDef`, and the fixed `FuncDef` rule binds precisely the same
closure at environment 0. All property-bearing body operations—argument
binding, name lookup, comparisons, branch selection, tuple construction,
return, frame pop, and state restoration—still execute under fixed semantics.

A fresh body-sensitivity check changed the actual closure leaf for `N=1` from
`(0,1)` to `(9,9)`, rebuilt the proof definition successfully, and attempted
the original target. `kprove` exited 1 with `WarnStuckClaimState`; the residual
contained the reached `(9,9)` tuple. This changed the term executed by the
claim, not merely an external source file. See the preserved
[mutated definition](/audit-output/evidence/auditor-body-mutation.k),
[sensitivity claim](/audit-output/evidence/auditor-body-sensitivity-spec.k),
and
[13-body-sensitivity.log](/audit-output/evidence/13-body-sensitivity.log).

The returned value is therefore concrete and discriminating, not a free
variable, tautology, implication-only condition, or opaque program-result
symbol.

The table also matches the human-facing property. In `1..1000`, the
palindromes are the nine one-digit values, the nine two-digit repeated values,
and the ninety three-digit values `101a + 10b` for
`a in 1..9, b in 0..9`; `1000` is not a palindrome. Parity is determined by
the final digit. This gives the final `(48,60)` count and exactly the threshold
increments used by the 108 intervals. The independent canonical and
arithmetic-reversal comparisons exhaust, rather than sample, the finite
contract domain.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 24 supplied `.k` files plus
`verification.k`. It records the complete source statement, attributes,
classification, execution-slice role, decision, and rationale for every row:

```text
930 total records
  228 syntax declarations
  696 rules
    45 priority rules
   651 ordinary rules
     0 explicit simplification rules
    5 contexts
    1 configuration

156 function declarations
116 total function declarations
  0 functional declarations
 22 opaque/no-evaluator function symbols
```

See [rule_inventory.csv](/audit-output/evidence/rule_inventory.csv),
[function_inventory.csv](/audit-output/evidence/function_inventory.csv),
[opaque_symbols.csv](/audit-output/evidence/opaque_symbols.csv), and
[11-rule-inventory.log](/audit-output/evidence/11-rule-inventory.log).

Every inventoried row has one of these decisions:

- 63 fixed-semantics declarations/rules are on the complete submitted-program
  execution or source-identity slice and are marked
  `VALID_ON_COMPLETE_INTENDED_EXECUTION_SLICE`.
- The two proof-local rows—the `solutionClosure` syntax and its equation—are
  marked `SOUND_DEFINITIONAL_EXTENSION`.
- The other 865 rows belong to the required fixed supplied semantics and are
  marked `FIXED_SEMANTICS_OUTSIDE_REACHABLE_SLICE`. Their redex constructors
  are absent from the submitted closure and do not overlap a used ground
  redex. Consequently they cannot enable a false conclusion for
  `N in 1..1000`; no broader CPython-fidelity claim is inferred for them.

The material constructor-to-rule map is:

| Submitted construct | Declaration and fixed behavior |
|---|---|
| module/function identity | `syntax.k` `Module`, `FuncDef`, `Params`; `core.k` load/sequencing; `functions.k` function binding |
| call and parameter | `call.k` callee/argument routing and closure-frame rule; `functions.k` `#bindP` |
| `Int(N)` and `Name("n")` | `core.k` integer literal and lexical lookup rules |
| `n < constant` | `operators.k` left/right contexts and comparison dispatch; `int.k` exact `<Int` equation |
| nested `if` | strict condition declaration and the three `controls.k` branch rules |
| result tuple | `tuple.k` left-to-right argument evaluation and `vals2valSeq` construction |
| return/state | strict `Return`; `functions.k` return, `#pop`, environment/scope/stack restoration |

Evaluation order is fixed: call arguments and tuple elements use the shared
left-to-right accumulator; comparisons evaluate left then right; `If` and
`Return` are strict in their expression. The one argument is bound in a fresh
scope whose parent is definition environment 0. Return discards the remaining
callee continuation as Python return should, then `#pop` restores the caller,
deletes the temporary scope, and resets `scopeLoc`. No body operation allocates
heap data, writes output, or raises on the integer domain.

The proof-local equation is a truthful definitional summary, not an operational
bridge: it has a nullary match domain, one exhaustive unguarded equation, no
overlap, no recursion, and no fresh or opaque result. It merely supplies the
exact closure value and does not replace a call, comparison, branch, tuple, or
return step. Although the program’s body contains the precomputed answer
table, those constants are part of the real submitted program and are reached
only by executing its real comparison tree; no proof rule substitutes the
desired output.

All 45 priority rules are fixed-semantics rules for shapes such as heap
references, cell variables, special builtins, float/math calls, dicts, lists,
and slices. None matches this closure’s integer-only call path. The 22
no-evaluator symbols cover float operations, sorting, and MD5; none occurs in
the submitted program, claim, target, or an applicable rule. The LLVM
non-exhaustiveness warnings likewise concern unused `mapStrVS`, float helpers,
`joinCodes`, and `valSeqAt`. On the relevant slice, total functions such as the
nullary closure, argument append, and value-sequence conversion have exhaustive
and structurally descending equations; `truthy` and `applyCmp` are fixed at the
used `Bool` and integer-`<` cases. Guards and sorts exclude competing equations.

No local rule was found unsound, so no unsoundness label is asserted without
the required false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on the candidate’s `spec-vacuity.k`. The fresh
[auditor-false-spec.k](/audit-output/evidence/auditor-false-spec.k) fixes the
satisfying witness `N=1000` but changes the required even count from the true
`48` to the false `49`.

First:

```text
kprove auditor-false-spec.k \
  --definition verification-audit-kompiled \
  --spec-module AUDITOR-FALSE-SPEC --dry-run
```

exited 0 and emitted KORE, establishing that the mutation parses and builds.
Then the same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its reachable residual was exactly
`tuple(vCons(48, vCons(60, .ValSeq)))`, which cannot unify with the false
`(49,60)` destination. This is the expected unmet result obligation, not a
parser error, missing import, timeout, unrelated crash, or unreachable
mutation. Exact commands, statuses, hash, and bounded residual are in
[12-fresh-nonvacuity.log](/audit-output/evidence/12-fresh-nonvacuity.log).

## 7. Proven versus assumed accounting

### What the K proof establishes

For every mathematical K integer `N` from 1 through 1000, exactly one of the
108 claims applies. Starting from the fully specified clean caller
configuration, calling the closure whose parameters, body, and definition
environment match the trusted translation reaches the claim’s concrete
two-integer tuple. The caller environment and scope map are restored, the heap
and stack are empty, return state is `noRet`, exception state is `NoExc`, and
exit code is 0. This is reported as partial correctness in accordance with the
Kit workflow.

The positive reachability proof is the K evidence. Neither `PROOF.md`,
generation traces, nor differential execution was used as a substitute for it.

### Trust ledger

1. **K toolchain and builtin theories.** K `v7.1.293`, its Haskell/LLVM
   backends, and builtin integer, Boolean, map, list, and rewriting theories are
   foundational trusted primitives. They affect all claims and are an
   unavoidable, acceptable machine-checking boundary.
2. **Supplied semantics.** The exact trusted fixed semantics is assumed to be
   the selected execution model. Its relevant integer/call/control/tuple slice
   was reviewed above; the remaining fixed rules and 22 opaque primitives are
   unreachable here. This boundary does not smuggle a result because no opaque
   symbol or unrelated rule influences a branch, return, state, or
   postcondition.
3. **Trusted translator.** `/reference/py2mpy.py` is assumed to implement the
   benchmark’s source-to-constructor translation. Byte identity and the
   constructor-level closure comparison support the exact source/proof link.
4. **Direct-closure normalization.** The claim starts after module binding and
   calls the exact closure. Mechanical comparison plus the fixed `FuncDef` rule
   establishes why omitted module loading/name lookup is inert for this
   one-definition module. No body computation is omitted.
5. **Intent bridge.** The K targets are a finite interval table rather than a
   K-defined palindrome-count function. The elementary one/two/three-digit
   characterization above, the trusted canonical, and an independent
   arithmetic-reversal oracle support that bridge. The executable comparison
   covers all 1000 permitted inputs, so its evidence is limited exactly to—and
   complete for—the material source domain. It does not claim anything about
   excluded inputs.
6. **Excluded behavior.** Integers below 1 or above 1000, non-integers, Python
   `bool` values, module rebinding, and unsupported Python constructs are
   outside the prompt and theorem. The observed divergences at 0 and 1001 are
   therefore not hidden.

Gate A passes: the real translated body executes, the result and state are
constrained, the proof is non-vacuous, and a body mutation changes the reached
result. Gate B passes: the formal integer domain exactly matches the explicitly
bounded prompt, and the interval table matches the complete intended behavior.
Gate C passes: assumptions and opaque symbols are enumerated, all cited
evidence is preserved with exact commands/statuses, and formal proof is
separated from finite executable and informal intent evidence.

VERDICT: PASS
LEGITIMACY: LEGIT
