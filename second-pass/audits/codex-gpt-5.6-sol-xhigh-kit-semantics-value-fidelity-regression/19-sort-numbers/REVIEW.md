# Independent adversarial audit: 19-sort-numbers

Decision: **CONCERNS / LEGIT**.

The two submitted reachability claims rebuild and close independently, the main
claim executes an exact constructor representation of the submitted program,
and a fresh false-result mutation reaches the post-state and is rejected.
There is no proof-local execution shortcut or false equation. The concern is
that the supplied semantics deliberately models keyed `sorted` with the opaque,
result-bearing symbol `sortKeyVS`. The K theorem proves that the program returns
the exact term containing that symbol; it does not prove in K that the symbol is
a stable ascending sort. The bridge from that symbolic result to the task's
human-facing sorted output is therefore conditional on the supplied primitive's
contract and supported only finitely by concrete/differential evidence.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent: this is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` exists as an ordinary
directory. I did not use the generated-semantics audit route.

The candidate has ordinary, non-symlink files for `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `spec.k`, and `verification.k`. There is one
structured JSONL generation trace. There are no symlinks anywhere under
`/candidate`.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. A recursive
`diff -qr --no-dereference` between the candidate and trusted
`reference-semantics/` trees exited 0. Thus there are no missing, additional,
changed, mistyped, or symlinked entries in the supplied-semantics tree. Exact
hashes and the comparison commands are in
`evidence/stage1-integrity.log`.

I read the small generation records directly and processed the complete
structured trace and 1.2 MB text log as untrusted claims. They claim a prior
`VALIDATED` result, three `#Top` outputs, mutation failures, and finite
differential tests. None was used as proof evidence. Bounded summaries,
record counts, hashes, and relevant excerpts are in
`evidence/stage1-untrusted-claims.log` and
`evidence/stage1-untrusted-trace-summary.log`.

Candidate-provided `runtime-kompiled/`, `verification-kompiled/`, Python caches,
`proof-run.log`, `PROOF.md`, smoke files, and mutation files were ignored for
reconstruction. Only source artifacts were copied to the new
`/tmp/audit-work/reconstruction` tree. No candidate-built definition or cache
was copied.

Stage result: pass; no provenance or supplied-semantics integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation specify: the input contains
zero or more numeral words `zero` through `nine`, delimited by spaces; return
the same multiset of words in numerical order, joined by single spaces. The
canonical code removes empty fields from literal-space splitting, maps each
word to 0 through 9, and uses a keyed sort.

The candidate implements a different but appropriate algorithm. `_number_rank`
returns 0 through 8 in nine explicit branches and 9 otherwise; `sort_numbers`
uses `numbers.split()`, keyed `sorted`, and single-space `join`
(`/candidate/solution.py:1` and `:23`). On the intended valid-word,
literal-space domain this agrees with the canonical implementation. It is more
permissive for tabs/newlines because Python's no-argument `split()` treats them
as separators, while the canonical code uses `split(' ')`. That behavior is
outside the prompt's literal-space domain and does not remove any intended
case.

Fresh translation used the trusted command:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`e8d45ee0928b794fc8c8dfbf015bda1d3afc84d6e1afc2033dfa8561455947ab`;
the command exited 0 (`evidence/stage2-translation.log`).

The independent script `evidence/stage2_differential.py` imports the trusted
canonical entry point and the scratch copy of the generated entry point. It
tested the documented example, empty and repeated-space inputs, each of the ten
helper outcomes, ascending/descending/duplicate cases, a 1,000-token case,
every word sequence through length four, and deterministic longer samples.
There were 11,611 distinct cases and zero mismatches. The exact generated input
corpus is `evidence/stage2-inputs.json`; its SHA-256 and the command/status are
in `evidence/stage2-differential.log`.

Stage result: pass on the intended domain.

## 3. Clean proof reconstruction

The live toolchain is K v7.1.293 (build 2025-10-03) and Python 3.10.12
(`evidence/stage3-toolchain.log`).

I freshly built the concrete definition from the integrity-checked source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. The LLVM compiler reported supplied-semantics exhaustiveness
warnings for unrelated or deliberately partial domains, plus unused variables
in `strLt`; none is reachable with the submitted valid string-list program.
The full bounded output is `evidence/stage3-kompile-llvm.log`.

The independently authored smoke program
`evidence/stage3_audit_smoke.py` covered the example, empty input, all-space
input, zero/nine, descending order, duplicates, repeated spaces, and
tab/newline whitespace. Translation plus `krun --output none` exited 0
(`evidence/stage3-krun-smoke.log`). A broader independently generated LLVM
batch used a counting oracle on 117 cases, including all sequences through
length two; `krun` again exited 0
(`evidence/stage3-k-differential.log` and its recorded input JSON).

I then freshly built the proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; its only warnings are the supplied unused `strLt` tail variables
(`evidence/stage3-kompile-haskell.log`).

Every submitted positive target was run separately:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.number-rank-connection
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.sort-numbers
```

Each command exited 0 and printed `#Top`
(`evidence/stage3-kprove-number-rank.log` and
`evidence/stage3-kprove-sort-numbers.log`). Running the entire spec also exited
0 with `#Top` (`evidence/stage3-kprove-all.log`). These are fresh results, not
candidate logs.

Stage result: pass.

## 4. Adequacy and real-program pinning

### Claim meanings

`SPEC.number-rank-connection` (`/candidate/spec.k:6`) assumes an initial module
scope that binds `_number_rank` to the exact submitted closure, with empty heap
and stack and normal return/exception/exit cells. For every `CS:IntSeq`, it
executes the actual call and says the return is `numberRank(CS)`, preserving the
stated observable cells.

`SPEC.sort-numbers` (`/candidate/spec.k:22`) starts with module loading followed
by a call to `sort_numbers(str(CS))`. Its precondition says that the supplied
`splitWS` turns `CS` into only the ten valid numeral words (the empty list is
allowed). Its postcondition fixes the result to
`str(sortNumbersResult(CS))`, fixes both loaded function bindings, records the
split list at heap location 0 and the keyed-sort list at location 1, advances
the heap counter to 2, restores the module environment, empties the call stack,
and leaves normal return/exception/exit state.

Both preconditions are satisfiable. `CS = strToCodes("nine")` is a helper
witness; `CS = strToCodes("three one five")` is a main-claim witness. Ground
substitution gives rank 9 and, under the named keyed-sort contract,
`"one three five"`. Both Python implementations return that value. Empty,
descending, and repeated-space witnesses also agree
(`evidence/stage4-witnesses.log`).

### Program identity and execution path

The trusted translation is byte-identical to submitted `solution.mpy`. I also
expanded the raw program-list notation to explicit K list terminators in
`evidence/stage4-normalized-solution.mpy` and proved, in a complete
configuration, that `solutionProgram` is that exact constructor term. The
reachability check printed `#Top` and exited 0
(`evidence/stage4-program-identity-reachability-kprove.log`). Its
`WarnTrivialClaim` means frontend function normalization had already made the
two constructor terms identical.

Two earlier reviewer attempts to paste raw program-parser notation directly
into a rule and to use a functional claim exited 113
(`stage4-program-identity-kprove.log`,
`stage4-program-parse-identity.log`, and
`stage4-program-identity-normalized-kprove.log`). Those are preserved harness
experiments, not candidate failures; the corrected reachability identity check
succeeded.

The main execution is not replaced by a proof-local rule. `#loadAll` executes
the two `FuncDef`s. Lookup selects the module-bound `sort_numbers`; call
evaluation creates and later removes its frame. `numbers.split()` allocates
heap object 0. Lookup of the builtin `sorted` and the module-bound
`_number_rank` evaluates left-to-right; the keyed-sort rule allocates object 1.
The non-mutating join path dereferences object 1, `joinCodes` builds the
returned string, and `Return/#pop` restores the caller state. These transitions
account exactly for the postcondition's cells.

The result is constrained, not a free variable, tautology, or one-way
implication: `sortNumbersResult` expands to `joinCodes` of `splitWS` and the
fixed `sortKeyVS(..., numberRankClosure)` term
(`/candidate/verification.k:108`). The important limitation is that
`sortKeyVS` itself remains opaque in the proof backend, so the exact K result
does not reduce to a concrete ordered string.

Stage result: pass for real-program pinning; documented conditional
intent-bridge concern.

## 5. Rule-by-rule static soundness review

`evidence/stage5-rule-inventory.md` is the exhaustive source-level inventory
for `semantics.k`, all 23 supplied helper K files, `verification.k`, and
`spec.k`. The generating script and command are preserved. It enumerates 961
units:

- 1 configuration, 81 non-function syntax declarations, 131 function
  declarations, 22 explicit `no-evaluators` opaque declarations, 3 additional
  `symbol` declarations, and 5 contexts;
- 471 equational rules, 200 ordinary semantic rules, 45 priority semantic
  rules, and 2 claims;
- no proof-local or supplied `[simplification]` rule and no explicit
  `[functional]` declaration.

Every inventory row has one of these dispositions: manually reviewed reachable
fixed semantics; manually reviewed proof-local definition; manually reviewed
concrete empirical bridge; reachable trusted opaque primitive; or outside the
submitted program's reachable slice with no intended-domain false-conclusion
witness. The last disposition is deliberately not a global endorsement of
unused general-purpose semantics.

### Proof-local inventory

All 31 `verification.k` source units were reviewed individually:

- `numberRankBody`, `sortNumbersBody`, `numberRankClosure`,
  `sortNumbersClosure`, and `solutionProgram` each have one unguarded nullary
  constructor equation. Their `[function,total]` declarations are exhaustive,
  the equations merely construct the exact submitted syntax/closures, and none
  rewrites a running program configuration.
- `numberRank` has nine pairwise-disjoint literal guards for zero through eight
  and an `owise` value 9. This matches the helper's final return for `nine` and
  for every other string. Its universal execution connection independently
  closed.
- `validNumberWord` is the ten-literal membership predicate.
  `validNumberWords` has disjoint empty, string-head recursive, and `owise`
  non-string-head cases; recursion removes one `vCons`. `validNumberInput`
  applies that predicate to the same supplied `splitWS` used by the program.
- `sortNumbersResult` has one exhaustive equation and names the exact
  fixed-semantics result. It does not rewrite a `Call`, bypass lookup, suppress
  control, or alter any cell.

There are no proof-local priority rules, operational bridges, simplifications,
fresh result symbols, `no-evaluators` declarations, or overlapping equations.

### Used syntax and fixed-semantics rules

| Submitted construct | Declaration and behavior reviewed |
|---|---|
| `Module`, `FuncDef`, `Params`, statement/expression lists | `syntax.k`; `core.k:124-127`; `functions.k:14` |
| `Name`, builtin/module lookup | `core.k:130-158`, including parent-chain guards and the higher-priority cell case (inapplicable to these unannotated functions) |
| `Int`, `Str`, `Compare`, `CmpOp("==", ...)` | `core.k:194`; `str.k:13-16,25`; `operators.k:14-17` |
| `If` and early `Return` | strict condition declaration in `syntax.k`; `controls.k:51-54`; `functions.k:78-89` |
| `Call`, `Attribute`, positional/keyword argument evaluation | `core.k:95-102,185-191`; `call.k:16-24,69-77` |
| `numbers.split()` | `methods.k:72-86`; structural recursion, four ASCII whitespace codes, empty-token dropping, allocation |
| `sorted(..., key=_number_rank)` | `sort.k:49,61-62`; exact closure value is passed, but the produced `sortKeyVS` is opaque |
| `" ".join(...)` | call-layer non-mutating dereference and `methods.k:26-31`; recursion preserves order and inserts one separator |
| Concrete keyed sort used only by LLVM evidence | `concrete.k:25-59`; real key calls, mutually exclusive insertion guards, equality inserted after prior equals (stability), allocation and unpairing |

The configuration includes every operational cell used by these paths.
Evaluation is callee-first and then left-to-right over arguments. Module and
function scope locations, heap allocation, returns, exceptions, and stack
restoration match the claims. The valid-word precondition prevents type/key
errors on the intended domain.

The LLVM warnings about total functions such as `joinCodes` concern constructors
outside this path. For example, `joinCodes` is not defined for a
`cellsMark` list element, but valid input plus the keyed-sort contract yields
only the original string elements. There is no satisfying intended-domain
witness that reaches those warned cases.

### Opaque and priority review

The only reachable opaque declaration is
`sortKeyVS(ValSeq, Val)` (`sort.k:49`). The ordinary rule at `sort.k:61-62`
preserves the exact argument list and key closure and performs the expected
fresh allocation, but intentionally leaves the sorted value abstract. The
LLVM-only rules at `concrete.k:28-59` preempt that rule with priority 40 and
execute key calls and stable insertion; those rules are not imported by the
Haskell proof definition. This is a supplied external-primitive boundary, not
a candidate-added task-answer rule.

The other symbolic/opaque names are unreachable from this program:
`sortVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
and `sqrtF`. They have no dependent submitted claim.

I found no materially unsound proof-local or reachable fixed-semantics rule and
therefore make no unsupported unsoundness allegation. In particular, no rule
on the intended domain was found for which a concrete or symbolic false
conclusion witness can be exhibited. The narrower evidence gap is the absence
of a universal K connection between opaque `sortKeyVS` and the concrete keyed
sort.

Stage result: pass for soundness of the theorem actually stated; concern for
the opaque result-to-intent bridge.

## 6. Fresh non-vacuity test

I inspected the candidate's `spec-vacuity.k` only as an untrusted claim, then
created the distinct auditor mutation
`evidence/stage6-audit-vacuity.k`. For the satisfying input
`"three one five"`, it changes only the returned-value obligation by prefixing
the actual symbolic result with code 33 (`!`), demanding
`"!one three five"` rather than `"one three five"`.

The mutation first passed:

```text
kprove audit-vacuity.k --definition verification-kompiled \
  --spec-module AUDIT-VACUITY --dry-run
```

with exit 0 (`evidence/stage6-vacuity-dry-run.log`), establishing that it builds
and selects a real claim. The actual proof command exited 1 with
`WarnStuckClaimState`. Its residual is the expected failed implication between
`joinCodes(...sortKeyVS...)` and
`iCons(33, joinCodes(...sortKeyVS...))`, after the complete final scopes, two
heap allocations, counters, empty stack, and normal exception/exit cells had
been reached (`evidence/stage6-vacuity-kprove.log`). This was not a parse error,
missing import, timeout, unrelated crash, or unreachable mutation.

Stage result: pass; the main proof is result-discriminating.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the supplied `MPY` proof semantics, the helper claim establishes the
isolated exact-call result `numberRank(CS)` for every `IntSeq`. Independently,
for every `CS` satisfying `validNumberInput`, the main partial-correctness claim
establishes that loading and invoking the exact submitted constructor program
reaches `str(sortNumbersResult(CS))` with the exact scopes, two heap objects,
allocation counter, stack, return, exception, and exit cells in the claim.

The main proof does not need or apply the helper claim: symbolic keyed sorting
retains the helper closure as an argument of opaque `sortKeyVS`. Consequently,
the K theorem is interpretation-parametric in that supplied symbol. The helper
claim plus inspection of the pure helper body supports the intended key
interpretation, but the helper theorem itself is stated only for an isolated
empty-heap/empty-stack call rather than every continuation and heap in which a
sort callback could run.

### Trust and evidence ledger

- **Supplied MPY semantics and K toolchain:** trusted proof foundation selected
  by the task mode. The candidate copy is exactly the trusted tree; the
  reachable rules were statically reviewed and rebuilt. K's Int, Bool, String,
  Map, List, equality theories, parser, Haskell backend, and solver remain
  ordinary checker trust.
- **`sortKeyVS`:** externally supplied, result-bearing opaque primitive.
  Acceptable for the exact conditional theorem because Python `sorted` is an
  external builtin and the postcondition retains the primitive explicitly.
  Concerning for the natural-language contract because no K axiom or universal
  connection theorem establishes stable ascending keyed sorting.
- **Concrete keyed-sort bridge:** the LLVM-only `#ksort`/`insPair` rules execute
  real callback calls and stable insertion. The independent 117-case K batch
  and smaller smoke run had no failures. This is finite evidence and does not
  universally constrain the Haskell-side `sortKeyVS`.
- **Implementation-to-canonical bridge:** 11,611 intended-domain CPython cases
  had zero mismatches against the trusted canonical entry point. This strongly
  supports program fidelity but is not a proof over unbounded input lengths.
- **Translator and constructor normalization:** the trusted translator
  regenerated the submitted term byte-for-byte, and the normalized constructor
  identity reachability claim closed. Manual normalization of K list
  terminators is an informal syntactic bridge, independently checked by the
  successful identity claim.
- **Unused opaque symbols:** the 24 names listed in Stage 5 are present in the
  general supplied semantics but have no value, control, state, or theorem
  influence here.
- **Mathematical intent argument:** given the external contract that
  `sortKeyVS` stably sorts by real calls to its key closure, the proved helper
  ranks the ten valid words uniquely from 0 to 9, and `joinCodes` therefore
  yields exactly the requested order. This argument is conditional/informal,
  not an additional K theorem.

The claims are partial-correctness claims; they do not separately prove
termination. Invalid numeral words are excluded. The formal splitter recognizes
ASCII space, tab, newline, and carriage return, so the formal domain is slightly
broader than the prompt's literal-space domain but narrower than all Unicode
whitespace accepted by CPython `split()`; neither difference removes an
intended prompt input.

Gate A passes for the exact theorem under the selected supplied semantics. Gate
B is adequate only conditionally on the named keyed-sort contract. Gate C
passes for auditability: every independent command, status, bounded output,
script, and generated input set used here is preserved under `evidence/`.

The proof is therefore legitimate but does not merit an unconditional `PASS`:
its central sorting-to-intent bridge is an explicit, high-level opaque trust
boundary rather than a universal K result. It also does not merit `FAIL`: the
proof never equates that opaque value to an unjustified concrete answer, the
real submitted program is pinned, and no reachable false rule was found.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
