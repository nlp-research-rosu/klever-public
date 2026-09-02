# Independent adversarial review: 163-generate-integers

## Overall assessment

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full source-contract domain of two positive integers. I
reconstructed both K definitions from source, reran the sole positive target
claim against the fresh Haskell definition, obtained `#Top` with exit status 0,
mechanically pinned the claim's closure body to trusted regeneration of
`solution.py`, and rejected both a material body mutation and a fresh false
result mutation.

The result is not derived from `PROOF.md`, candidate caches, generation traces,
or a candidate-provided `#Top`. Those artifacts were treated only as untrusted
claims. The decisive records are the reviewer-authored scripts and bounded logs
under `evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem
`163-generate-integers`, and condition `kit-semantics`. The trusted supplied
tree `/reference/reference-semantics` is present, so the mount is consistent
with the rendered mode. There is no infrastructure breach.

I read and checked all records required for this layout:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the JSONL trace below `/generation-evidence/codex-trace/`.

The campaign block in `/audit-input.json` is exactly equal as JSON to
`/audit-campaign-lock.json`, whose directly computed SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All launcher-recorded file-level hashes recomputed by the audit match, including
the run/task/result/invocation records, trusted inputs, generation prompt,
metrics, usage, last message, and 595,105-byte generation log. The structured
trace contains one real regular JSONL file, its hash matches both generation
manifests, and all 278 lines parse as JSON. The full candidate tree has 771
regular files and no linked or unsupported entry; all required proof artifacts
are present. See
[`01_integrity_check.py`](evidence/01_integrity_check.py) and
[`01_integrity_check.log`](evidence/01_integrity_check.log).

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. More importantly for supplied
semantics, the candidate and trusted `reference-semantics/` trees have exactly
the same 24 relative regular-file entries and identical content for every
entry. There are no missing, additional, changed, mistyped, or symlinked
semantics entries. This integrity result does not bless anything in
`verification.k`; that file is audited separately below.

The generation records claim a successful run and validated proof, but I assign
those claims no probative weight. I independently parsed the complete trace
structure and inspected its tool-command/final-message history only as
provenance evidence.

Retained files named `*_initial_reviewer_error.log` document corrected
reviewer-script mistakes: one initially required exact equality before
removing the launcher-added `config` field from the manifest comparison;
another initially used K's external-program parser for a semantic-only
`closureVal` term; and the final checker initially over-escaped a regular
expression. All scripts were corrected and rerun successfully. These are
reviewer harness mistakes, not candidate or infrastructure defects.

Tool versions are K 7.1.293 for `kompile`, `kprove`, and `krun`, and Python
3.10.12; exact commands and statuses are in
[`00_tool_versions.log`](evidence/00_tool_versions.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires: for two positive integers `a` and `b`, return in
ascending order the even decimal digits in the inclusive span between the
endpoints, independent of endpoint order. Because both endpoints are positive,
the only possible returned even digits are `2, 4, 6, 8`. The trusted canonical
computes the same value by clamping the lower bound to 2 and upper bound to 8,
then filtering an inclusive range for even values.

`solution.py` uses a different but equivalent loop-free algorithm. It creates
an empty list and, in ascending order, appends each of `2, 4, 6, 8` exactly when

```text
(a <= digit <= b) or (b <= digit <= a).
```

This handles either endpoint order, equality at each boundary, intervals wholly
outside the digit range, and arbitrarily large positive integers.

I regenerated the constructor program with the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy
cmp /tmp/audit-work/reconstruction/solution.regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy
```

Both commands exited 0. The two files have the same SHA-256,
`dafb407d62efa4ca95522f0d622eef6ac8fc1f185dc7768678e93dd9a6a6d792`.

The independent differential script imports both trusted
`canonical.generate_integers` and candidate `solution.generate_integers`. It
also uses a separately written direct-contract oracle over `(2,4,6,8)`. It
checks:

- all three documented examples;
- a cross-product of values immediately below, at, and above every branch
  threshold, including 1 and the cutoff above 8;
- every ordered pair in `[1,128] x [1,128]`;
- 5,000 deterministic seeded pairs up to `10^12`; and
- reversed and non-reversed 100-digit integer witnesses.

All 21,537 pairs matched among the generated implementation, trusted canonical,
and direct oracle, with zero mismatches. The script, precise scope, commands,
statuses, and result are in
[`02_differential_test.py`](evidence/02_differential_test.py) and
[`02_fidelity_run.log`](evidence/02_fidelity_run.log). These finite tests support
the source/contract bridge; they are not substituted for the K theorem.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction` and copied
the semantics from the trusted `/reference` tree. Candidate
`runtime-kompiled/`, `verification-kompiled/`, bytecode caches, and all
candidate build products were excluded.

First I created an independent concrete harness containing the exact function
body and 14 normal/boundary assertions. I translated it with the trusted
translator, ran the same assertions in CPython, compiled a new LLVM definition,
and ran the resulting `.mpy`:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-llvm-kompiled
krun audit-concrete.mpy --definition fresh-llvm-kompiled
```

Both exited 0. `krun` reached `.K`, an empty stack, `noRet`, `NoExc`, and exit
code 0. The cases include both argument orders, empty results, each endpoint
edge, equality at 2 and 8, the cutoff at 9, the full digit range, and a
31-digit integer. See
[`03a_concrete_build_run.sh`](evidence/03a_concrete_build_run.sh) and
[`03a_concrete_build_run.log`](evidence/03a_concrete_build_run.log).

I then compiled an independent Haskell proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
```

The fresh compilation exited 0. `spec.k` contains exactly one positive target
claim, `SPEC.generate-integers`. The fresh `kprove` run printed `#Top` and
exited 0. The bounded record is
[`03b_proof_rebuild.log`](evidence/03b_proof_rebuild.log).

The Haskell build reported only four unused-variable warnings in an unrelated
string comparison. The LLVM build additionally reported non-exhaustive total
functions `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`.
None of those functions occurs in this program, its postcondition, or its
symbolic path. Their trust impact is accounted for in stages 5 and 7 rather
than hidden.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The precondition is `A >Int 0 andBool B >Int 0`, with `A` and `B` otherwise
unbounded K integers. Initially:

- `<k>` calls `generate_integers` with source-level integer expressions
  `Int(A)` and `Int(B)`;
- environment 0 has the `generate_integers` binding and the supplied builtins
  parent;
- the closure has parameters `a,b`, definition scope 0, and the submitted
  function body;
- heap and call stack are empty, allocation counter is 0, scope counter is 1,
  return state is `noRet`, exception state is `NoExc`, and exit code is 0.

At the destination, the call has returned `ref(0)`. Heap location 0 contains
`list(expectedDigits(A,B))`, heap allocation advances to 1, and environment,
scope, stack, return, exception, and exit-code cells have the required restored
or final values. Thus the result is neither a free variable nor a tautology:
the returned reference, its exact list contents, allocation effect, control
state, and normal completion are all constrained.

### Mechanical source-to-claim identity

The claim preloads the closure rather than first executing the complete
`Module(FuncDef(...))`. This is permitted only if it is the same binding and
body. I checked that mechanically, not by textual visual comparison:

1. parse trusted-regenerated `solution.mpy` with the fresh K definition;
2. extract the sole `FuncDef` name, parameter constructors, and body
   constructors;
3. parse the `closureVal` embedded in `spec.k` with K's rule parser; and
4. compare the parameter and body KAST objects for structural equality.

The objects are identical, the scope is 0, and both binding key and invoked
name are `generate_integers`. Fixed rule
`semantics/functions.k:14` shows that module execution of this sole `FuncDef`
does exactly the prebinding used in the claim: it inserts that
`closureVal(PNS,BODY,0)` into scope 0 without changing heap, control, return,
exception, or exit state. Therefore the omitted module-loading prefix is a
demonstrated semantically inert normalization.

The mechanical checker and four satisfying-state substitutions are in
[`04_pinning_and_witnesses.py`](evidence/04_pinning_and_witnesses.py) and
[`04_pinning_and_witnesses.log`](evidence/04_pinning_and_witnesses.log).
For example:

- `(A,B)=(2,8)` satisfies the precondition and requires
  `[2,4,6,8]`;
- `(10,14)` satisfies it and requires `[]`;
- `(6,6)` satisfies it and requires `[6]`; and
- `(1,10^100)` satisfies it and requires `[2,4,6,8]`.

In every case the instantiated formal sequence equals both Python
implementations.

I also independently reran the candidate's body-sensitivity artifact against
the fresh definition. It changes the `Int(8)` argument inside the closure term
actually executed by the claim to `Int(7)` while leaving the postcondition
unchanged. It builds successfully, then exits 1 with `WarnStuckClaimState`; a
reachable residual heap contains `[7]`, and `(8,8)` is a concrete satisfying
witness requiring `[8]`. This is a real claim-body mutation, not a change to an
external source file. See
[`04b_body_sensitivity_run.log`](evidence/04b_body_sensitivity_run.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`05_rule_inventory.tsv`](evidence/05_rule_inventory.tsv) enumerates every local
entry in trusted `semantics.k`, all 23 helper K files, `verification.k`, and
`spec.k`, with file, line, kind, attributes, classification, decision basis,
and source head. It contains 936 entries:

| Kind or attribute | Count |
|---|---:|
| syntax declarations | 230 |
| ordinary semantic/proof rules | 699 |
| contexts | 5 |
| configurations | 1 |
| target claims | 1 |
| `[function]` declarations | 148 |
| `[total]` declarations | 110 |
| `[functional]` declarations | 0 |
| `symbol(...)` declarations | 25 |
| `[no-evaluators]` declarations | 22 |
| priority rules | 45 |
| `[owise]` rules | 26 |
| `[concrete]` rules | 35 |
| simplification rules | 0 |
| macros / recursive macros | 4 / 1 |

The inventory checker is
[`05_inventory_checks.py`](evidence/05_inventory_checks.py), with results in
[`05_inventory_checks.log`](evidence/05_inventory_checks.log).

### Construct-to-rule mapping for the submitted program

| Submitted construct/effect | Fixed declarations and rules | Audit result |
|---|---|---|
| module function binding | `core.k:124-127`, `functions.k:14` | Creates the exact closure in scope 0; no other state effect. |
| call/name/parameter binding | `core.k:130-152`, `call.k:19-21,69`, `functions.k:63-69` | Binding selects the pinned local function; callee then arguments evaluate left-to-right; `a` and `b` bind in a fresh frame. |
| integer literals and `<=` | `core.k:194`, `operators.k:15-17`, `int.k:23` | Reduces to ordinary unbounded integer comparison. |
| `and` / `or` guards | `bool.k:16-25`, `core.k:199-205` | Correct left-to-right, value-returning short circuit; here every operand is Boolean. |
| empty list construction | `list.k:13-15`, `core.k:117-121,186-191,217-219` | Evaluates elements in order and allocates exactly one list at fresh location 0. |
| assignment, `if`, expression statement | `controls.k:9-18,48,51-54` | Writes the current plain frame, branches on Boolean truth, and discards only the call's `noneV` result. |
| `result.append(digit)` | `call.k:16,19-24`, `list.k:53-55` | Resolves the bound method and mutates the same heap list in place, preserving order. The specific priority rule soundly preempts generic method dispatch. |
| return/frame restoration | `functions.k:78-91` | Returns the list reference, pops the call frame, restores environment/scope counter, and preserves the escaping heap object. |

The complete configuration footprint agrees with the claim. The list literal
allocates location 0 and advances `<heapLoc>` to 1. Appends mutate location 0
without allocation. The call temporarily creates a scope and stack frame, then
the return/pop rules remove it and restore `<env>`, `<scopeLoc>`, `<stack>`, and
`<ret>`. All four guards are evaluated in ascending digit order. No loop,
exceptional operation, external call, output, or other mutable state is
present.

### Proof-local extension audit

`verification.k` adds exactly three symbols and four equations:

- `inClosedSpan(A,B,D)` is the unconditional formula
  `(A <= D <= B) or (B <= D <= A)`;
- `keepDigit(true,D,REST)` prepends `D`, while the disjoint/exhaustive
  `false` case returns `REST`; and
- `expectedDigits(A,B)` applies those definitions to 2, then 4, then 6, then
  8.

They are finite, nonrecursive except for nested evaluation of already smaller
subterms, total over their declared sorts, and pairwise non-conflicting.
`verification.k` contains no `<k>`-cell rewrite, operational bridge, priority,
simplification, concrete rule, opaque symbol, auxiliary claim, or fresh value.
The functions occur in the destination only; they never replace lookup,
argument evaluation, branch execution, list allocation, mutation, or return.
Consequently there is no program-derived oracle and no bridge connection
theorem is needed.

### Priorities, totality, and unused supplied theory

There are no proof-local priority rules. Of the fixed priorities, the only one
materially active on this program is the exact list-`append` rule. It is
narrower than generic bound-method dispatch and preserves the complete
observable state: it returns `noneV`, changes only the addressed list value in
`<heap>`, keeps the same reference, and leaves continuation and all other cells
framed. Reference-dereference and closure-cell priorities are sort- or
guard-disjoint from the integer/Boolean/plain-frame states used here.

The 25 supplied `symbol(...)` boundaries are `floorFI`, `toF`, `ceilF`, the 19
float symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
`divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, plus `sortVS`,
`sortKeyVS`, and `md5hexCodes`. None appears in `solution.mpy`,
`verification.k`, `spec.k`, or a reachable proof state for this claim. The same
is true of the six compiler-warning functions named in stage 3. Their totality
or opacity therefore cannot choose a branch, construct a returned element,
change state, or discharge this postcondition.

The remaining unused fixed rules include documented subset approximations for
imports, encoding, sorting, hashing, floats, closures, and unsupported
exceptional cases. The inventory records these individually. I do not promote
them to a claim of full CPython equivalence, but they cannot syntactically or
sort-wise match this submitted execution. There is thus no intended-domain
false-conclusion witness, and I do not label an unused fixed rule unsound for
this theorem. I found no candidate-local unsound rule, so no unsoundness witness
is asserted or required.

## 6. Fresh non-vacuity test

I inspected candidate `spec-vacuity.k` only as untrusted evidence; it adds a
leading zero to the required list. I did not use it as the required test.

The fresh reviewer mutation is
[`audit-false-result.k`](evidence/audit-false-result.k). It leaves the complete
precondition and executed closure body unchanged but changes the final heap
obligation from

```text
list(expectedDigits(A,B))
```

to the false

```text
list(vCons(10,expectedDigits(A,B))).
```

`(A,B)=(10,14)` is a satisfying witness: the precondition is true, both Python
implementations return `[]`, and the correct formal heap is the empty
`ValSeq`, not `[10]`.

The mutation first passed a `kprove --dry-run` build with exit 0. The real
mutation proof then exited 1 with `WarnStuckClaimState`, not a parse error,
timeout, missing import, or unrelated crash. Its reachable residual has
`<k> ref(0) ~> .K </k>`, normal restored cells, heap location 0 equal to
`list(.ValSeq)`, and constraints placing both inputs above 8; that final state
cannot unify with the false leading-10 destination. The exact commands,
statuses, and bounded residual are in
[`06_false_mutation_run.log`](evidence/06_false_mutation_run.log).

This establishes that the successful theorem is result-discriminating and its
precondition is satisfiable.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics and K integer/Boolean theories, for all
unbounded integers `A,B` satisfying `A>0` and `B>0`, if the pinned submitted
call terminates normally as represented by the reachability claim, it returns
reference 0 to a newly allocated list whose sequence is exactly the ascending
subsequence of `2,4,6,8` lying in the inclusive span between `A` and `B`.
The proof also constrains normal exception/exit state, frame restoration, and
the single allocation. This is the required partial-correctness theorem, not a
finite-size or bounded-unrolling result.

The theorem covers the entire natural-language domain. Zero, negative,
non-integer, Python `bool`-subtype, and exceptional inputs are excluded by the
source contract's “positive integers” premise rather than silently removed by
the proof.

### Trust ledger

| Boundary | Effect on target | Accounting |
|---|---|---|
| K 7.1.293 Haskell prover, SMT reasoning, and built-in unbounded Int/Bool/Map/List theories | Directly trusted by the symbolic theorem | Standard machine-checking trust base; versions and fresh commands recorded. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` to `solution.mpy` | Required benchmark trust boundary; fresh output is byte-identical, and source/claim constructors are mechanically compared. There is no claimed general translator-correctness theorem. |
| Trusted 24-file supplied `MPY` semantics | Defines calls, state, control, allocation, comparison, and mutation | Required `SUPPLIED_SEMANTICS` boundary; candidate copy is recursively identical. Every material operation is executed by fixed rules and reviewed above. General CPython equivalence remains assumed. |
| Preloading the function binding | Could otherwise substitute a program | Not assumed: fixed `FuncDef` behavior plus KAST equality mechanically derives the exact binding/body normalization. |
| `inClosedSpan`, `keepDigit`, `expectedDigits` | Directly determines the destination list | Fully defined by truthful finite equations; no opacity or operational replacement. The successful universal reachability proof connects real execution to them. |
| 25 supplied symbol/opaque boundaries and six non-exhaustiveness warnings | No effect | No target-path occurrence or dependent claim. They neither control a branch nor influence result/state for this theorem. |
| Human-facing reading of “even digits” | Connects formal `2,4,6,8` sequence to the prompt | Direct mathematical reading under positive endpoints, confirmed by trusted canonical and all documented examples; differential testing supplies finite additional evidence. |
| CPython/canonical differential and LLVM concrete runs | Empirical support only | 21,537 Python comparisons and 14 fresh semantic assertions have zero mismatches. Neither is used as a substitute for `kprove`. |
| Candidate `PROOF.md`, compiled definitions, logs, trace, and reports | None | Treated only as untrusted provenance/evidence and not used to establish closure or soundness. |

All result-bearing values in the theorem are therefore either produced by the
fixed execution or fixed by complete mathematical equations. There is no
unconstrained oracle, smuggled task answer, one-way implication in place of
equality, restricted finite domain, or substituted program.

VERDICT: PASS
LEGITIMACY: LEGIT
