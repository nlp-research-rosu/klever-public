# Independent adversarial audit: 54-same-chars

## Executive conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full source-contract input domain. The proof was reconstructed
from source with K 7.1.293, its only target claim printed `#Top` and exited 0,
the claim is satisfiable and result-constraining, and a fresh inverted-result
mutation was rejected for the expected unmet obligation.

The proof does not replace `same_chars` with an oracle. Its one proof-local rule
expands a fresh launcher into a normal call of a closure whose parameter and
body constructor trees mechanically equal those in the trusted regeneration of
`solution.mpy`. Fixed supplied semantics then perform lookup, argument
evaluation, the two `set` calls, set equality, return, and frame restoration.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `54-same-chars`;
- condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`.

This is consistent with the mounts: `/reference/reference-semantics` exists and
contains the supplied semantics. I inspected the launcher-owned audit input,
campaign lock, run and task manifests, generation result, invocation, metrics,
usage, last response, output log, prompt, and all 132 records in the structured
JSONL trace. Historical runtime metrics are absent, which is permitted for this
legacy-selected-stage1 layout.

The campaign-lock JSON is structurally identical to the `audit_campaign` block,
and its byte SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every required JSON record parsed, and every required record was a regular file.
The individual recorded hashes for the canonical source, prompt, translator,
run/task/result/invocation records, generation prompt, metrics, usage, last
message, output log, and trace file matched.

Independent pipeline-tree recomputation also matched:

- mounted candidate:
  `2f292394c89b1fd17ad12ae6b59fb8644646b7591a19815b7be7e006b2d8e0ed`;
- candidate and trusted supplied-semantics manifest:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace source tree:
  `008607b5d0ad502b489d0d6f1cf1de8d0659bf19efdd2f78b52c2698c0be92d6`.

The independent reviewer tree digest of both candidate and trusted semantics
was the same:
`d5f0b85afc1aab2d2e4be31bd7e02e17d8525dccf30482093b1cd8592728f23c`.
More importantly, the recursive entry-by-entry comparison found identical entry
sets, identical entry kinds, and byte-identical regular files. There were no
symlinks, missing entries, added entries, or changed entries. Candidate
`prompt.py` and `py2mpy.py` were byte-identical to their trusted mounts.

The generation log is only untrusted history. It records an initial spec parse
error caused by `<exit-code exit="">`, a subsequent correction, and later
claimed `#Top`; none of those claims was used in the decision.

Evidence:

- `evidence/provenance_check.py`
- `evidence/01-provenance-corrected-final.log` — exit 0, no failures
- `evidence/01-provenance.log` and
  `evidence/01-provenance-final.log` — retained reviewer-script diagnostics.
  The first tried to parse trace directories as files; the second paired newer
  secure-digest fields with an older pipeline digest algorithm. Both were
  reviewer-script errors, corrected in the final run, not mount failures.

Stage result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says to check whether two words have the same characters.
The trusted canonical implementation resolves any possible multiplicity
ambiguity as:

```python
return set(s0) == set(s1)
```

Thus order and repetition count are irrelevant. The result is true exactly
when every character occurring in either string also occurs in the other.

The candidate has the required signature and exactly the same executable body:

```python
def same_chars(s0: str, s1: str):
    return set(s0) == set(s1)
```

### Trusted translation

From the clean scratch copy I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both files had SHA-256
`50ea732f523d5b7b821b7f2c3a1055e0456cf1e8b9b57d306d967066453a8d07`.
The submitted `solution.mpy` is therefore byte-identical to fresh output from
the trusted mounted translator.

### Independent differential test

`evidence/differential_test.py` loads the trusted canonical module and candidate
solution independently. It checks:

- all six documented examples;
- 14 empty, singleton, duplicate, ordering, NUL, non-ASCII, and astral-Unicode
  boundary cases;
- every pair among the 121 strings of length 0 through 4 over `abc`
  (14,641 pairs);
- 2,000 deterministic generated pairs over an alphabet containing ASCII, NUL,
  accented, Greek, and astral characters.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py
```

It exited 0 after 16,661 comparisons with `mismatch_count=0`. Differential
testing is finite evidence only; it is not substituted for the K proof.

Evidence:

- `evidence/02-translation-identity.log`
- `evidence/02-differential.log`
- `evidence/04-differential-ground-rerun.log`

Stage result: PASS.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/54-same-chars`. The
`reference-semantics` used there was copied from the trusted `/reference` tree,
not from a candidate compiled definition. No candidate `*-kompiled` directory
or K cache was present or reused.

### Concrete definition

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit 0. Running:

```text
krun concrete_tests.mpy --definition audit-runtime-kompiled --output pretty
```

also exited 0. The final configuration had `.K`, `NoExc`, exit code 0, empty
heap/stack, and the expected translated function binding. This independently
re-executed all six prompt assertions.

### Proof definition and target claim

```text
kompile verification.k --backend haskell \
  --main-module SAME-CHARS-VERIFICATION \
  --syntax-module SAME-CHARS-VERIFICATION \
  --output-definition audit-verification-kompiled
```

Exit 0.

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SAME-CHARS-SPEC
```

Exit 0, output `#Top`. `spec.k` contains exactly one positive target claim, so
all positive target claims were rerun.

LLVM compilation warned about non-exhaustive unrelated helpers such as
`mapStrVS`, float conversion helpers, `joinCodes`, and out-of-bounds
`valSeqAt`. Haskell compilation and proof warned only about unused tail
variables in `strLt`. None of these terms is reachable from this submitted
program or its claim; the result-relevant set operations compiled without a
coverage warning.

Evidence:

- `evidence/03-kompile-llvm.log`
- `evidence/03-krun-concrete-tests.log`
- `evidence/03-kompile-haskell.log`
- `evidence/03-kprove-positive.log`

Stage result: PASS.

## 4. Adequacy and real-program pinning

### Plain-language reading of the entry claim

There is no `requires` clause. The precondition is:

- arbitrary finite `S0:IntSeq` and `S1:IntSeq`;
- current environment 0;
- an empty module scope 0 whose parent is the supplied builtins scope at -1;
- next scope location 1;
- empty heap and stack;
- no pending return or exception;
- exit code 0.

The postcondition is that the returned K Boolean equals:

```text
sameSet(dedupCodes(S0), dedupCodes(S1))
```

`sameSet` is mutual membership. This is an equivalence, not a one-way
implication. The returned result is not a fresh or unconstrained variable.

The formal input domain is not narrowed. Every Python string maps to a finite
sequence of character codes, while the claim actually admits arbitrary finite
integer sequences, a harmless broader domain.

### Mechanical program identity

`evidence/pinning_compare.py` parses both the submitted `solution.mpy` and the
actual `#sameChars` launcher rule with the freshly built K parser. It compares
KAST constructor subtrees rather than source text. It established:

- binding name is exactly `"same_chars"`;
- the parameter constructor tree is identical;
- the complete function-body constructor tree is identical;
- the proof closure captures environment 0;
- argument mapping is exactly `s0 <- str(S0)`, `s1 <- str(S1)`;
- the body's only `Name` tokens are `"set"`, `"s0"`, `"set"`, and `"s1"`.

The translated module would first bind this same closure under `same_chars` in
scope 0. The launcher directly invokes the identical closure and therefore
omits that binding side effect. This omission is semantically inert here:
the body never looks up `same_chars`, returns no closure, and observes no module
dictionary. The lookup of `set` still follows the fixed scope chain to the
supplied builtins scope.

This is a mechanically demonstrated normalization allowed by the benchmark's
pinning rule. The absence of automatic regeneration of `verification.k` is an
artifact-maintenance observation, not an identity failure for this immutable
candidate.

The first pinning run had a doubled-backslash bug in the reviewer's regex; the
corrected rerun exited 0. Both logs are retained:

- `evidence/04-pinning-compare.log`
- `evidence/04-pinning-compare-rerun.log`

### Satisfying states and ground substitution

The exact initial configuration with `S0 = .IntSeq` and `S1 = .IntSeq`
satisfies the precondition. Two more instances exercise distinct results:

- `"ab"` / `"baa"`: claimed K result `true`; canonical and candidate Python
  both return `True`;
- `"a"` / `"b"`: claimed K result `false`; canonical and candidate Python both
  return `False`.

All three reviewer-authored ground K claims printed `#Top` and exited 0.

Evidence:

- `evidence/ground-instances.k`
- `evidence/04-ground-instances-kprove.log`
- `evidence/04-differential-ground-rerun.log`

### Body sensitivity

As a check separate from postcondition non-vacuity, I changed the term actually
executed by the claim: the second `set(s1)` in the closure body became
`set(s0)`. I did not merely edit an external Python file.

The mutated definition compiled successfully. Proof of the original result
failed with exit 1 and `WarnStuckClaimState`; the residual compared the mutated
`sameSet(S0,S0)` behavior with the required `sameSet(S0,S1)`. This is the
expected body-sensitive failure.

Evidence:

- `evidence/verification-body-mutated.k`
- `evidence/spec-body-mutated.k`
- `evidence/04-body-mutation-kompile.log`
- `evidence/04-body-mutation-kprove.log`

Stage result: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.py` scanned every K source in the trusted supplied
semantics plus candidate `verification.k` and `spec.k`. The preserved inventory
contains 931 records:

- 228 syntax declarations;
- 1 configuration;
- 5 evaluation contexts;
- 696 rules;
- 1 target claim.

It identifies 146 function declarations, 107 `total` declarations, 25 named
symbols, 22 explicit `no-evaluators` opaque symbols, 45 priority-bearing rules,
35 concrete rules, 26 `owise` rules, 4 macros, and 2 strictness declarations.
There are no `functional` declarations and no simplification rules.

Every record is listed with file, line, attributes, complete normalized text,
and proof-slice classification in:

- `evidence/05-rule-inventory.log`.

The classification is exhaustive:

1. Result-relevant fixed rules are reviewed below as sound.
2. `MPY-CONCRETE` rules are runtime-only and are not imported by the Haskell
   proof module.
3. Opaque symbols are unreachable from the submitted term and listed in the
   trust ledger.
4. Every other fixed rule has a syntactic head, operand sort, operator string,
   builtin name, method name, or control marker that cannot occur in the
   reachable submitted term. Such a rule cannot enable this conclusion. This
   does not claim the supplied subset models every unused Python behavior.

No inventoried candidate rule was left in an “unknown” category.

### Construct-to-semantics map

| Submitted construct | Declaration | Material rules |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement/argument lists | `semantics/syntax.k:53-61` | Module binding is mechanically omitted as inert; the exact closure body is retained |
| `Return` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78`, `:85` |
| `Compare` / `CmpOp("==", ...)` | `semantics/syntax.k:30-32` | contexts and dispatch at `semantics/operators.k:15-17`; set case at `semantics/set.k:39` |
| `Call` | `semantics/syntax.k:28` | `semantics/call.k:20-21`, `:31`, `:69-74` |
| `Name("set"|"s0"|"s1")` | `semantics/syntax.k:12` | scope lookup at `semantics/core.k:131-154`; registry at `:157-181` |
| strings as code sequences | `semantics/core.k:13-16` | launcher supplies `str(S0)` and `str(S1)` directly |
| `set(str)` | `semantics/builtins.k:17`, `semantics/set.k:8` | `semantics/builtins.k:41`; `semantics/set.k:11-39` |
| proof launcher | `verification.k:8` | exact-body expansion at `verification.k:10-23` |

### Proof-local extension

The candidate adds one syntax declaration and one rule:

```text
#sameChars(S0,S1) => Call(closureVal(exact parameters, exact body, 0),
                          (str(S0),str(S1),.Exprs))
```

Classification: a definitional launcher for a fresh symbol, not an operational
bridge that intercepts a fixed-semantics operation.

- **Domain:** all `IntSeq` arguments and any framed continuation.
- **Context containment:** the rule replaces only the fresh launcher with an
  expression in the same continuation. It introduces no return, pop, exception,
  cleanup, or continuation deletion.
- **State footprint:** the rule itself changes only `<k>` and frames every other
  cell. All scope creation, parameter binding, lookup, return state, and frame
  restoration are performed by fixed semantics.
- **Value influence:** its call result is the entire target result.
- **Value justification:** it creates no opaque value. KAST identity shows the
  fixed semantics executes the exact submitted body. The executed-body mutation
  is rejected.
- **Dependents:** the single entry claim.

There are no proof-local functions, totality declarations, priorities, helper
claims, ordinary mathematical lemmas, opaque symbols, simplifications, or
oracles.

### Fixed execution path

The fixed path is faithful:

1. Generic call routing evaluates the closure and arguments left-to-right.
2. Closure invocation allocates scope 1 with parent scope 0, saves the exact
   continuation, binds `s0` and `s1`, and executes the body.
3. `Name("set")` walks scope 1 to 0 to the supplied builtins scope at -1.
   Parameter names resolve in scope 1.
4. `applyBuiltin("set", str(CS), .Vals)` yields
   `setV(dedupCodes(CS))`.
5. Compare evaluation computes the left call and then the right call. Both are
   pure here.
6. `applyCmp("==", setV(A), setV(B))` yields `sameSet(A,B)`.
7. `Return` records the Boolean, pops scope 1, restores environment 0 and the
   empty stack, and leaves all claimed observable cells as specified.

Modeling these temporary sets as algebraic values rather than mutable heap
objects is exact for this program: they are immediately compared and neither
identity, mutation, aliasing, nor iteration order is observable.

No relevant priority rule preempts this path. The generic `Call` rule is
`owise`, but none of the fixed special-call heads (math, md5, split, sort, and
others in the inventory) matches either the closure call or `Name("set")`.
Heap-reference priority rules cannot match the direct `str` or `setV` values.
The other `applyCmp("==",...)` rules are constructor/sort-disjoint from the
`setV/setV` case.

### Mathematical rules

The result-bearing equations are ordinary, terminating definitions:

- `codeIn` is false on empty and recursively tests head equality or tail
  membership.
- `dedupFrom` consumes one input constructor on every step. Its
  `codeIn` / `notBool codeIn` guards are disjoint and exhaustive.
- `snocCode` structurally appends one code.
- `subsetCodes` is true on empty and otherwise requires head membership and
  recursive subset.
- `sameSet(A,B)` is `subsetCodes(A,B) andBool subsetCodes(B,A)`.

Consequently, `sameSet(dedupCodes(S0),dedupCodes(S1))` is true exactly when the
two finite code sequences have the same distinct elements. Duplicate removal in
the postcondition is redundant but truthful. Guards do not overlap with
different right-hand sides, recursive calls descend structurally, and the
`total` declarations cover all constructor forms used here.

I found no unsound result-relevant rule, so there is no false-conclusion witness
to report. Unused subset limitations are recorded as narrower evidence gaps,
not mislabeled as unsoundness.

Stage result: PASS.

## 6. Fresh non-vacuity test

I created `evidence/spec-vacuity-audit.k` from scratch. It preserves the exact
precondition and program term but changes the result obligation to:

```text
notBool sameSet(dedupCodes(S0), dedupCodes(S1))
```

This is demonstrably false for the satisfying witness
`S0 = S1 = .IntSeq`: the program returns `true`, while the mutation requires
`false`.

First:

```text
kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module SAME-CHARS-SPEC-VACUITY-AUDIT --dry-run
```

exited 0, establishing that the mutation parsed and built.

Then the same command without `--dry-run` exited 1. It produced
`WarnStuckClaimState` and a residual whose unmet implication is precisely:

```text
sameSet-result #Equals notBool sameSet-result
```

The failure was not a parser error, timeout, missing import, unrelated crash, or
unreachable mutation.

Evidence:

- `evidence/spec-vacuity-audit.k`
- `evidence/06-vacuity-dry-run.log`
- `evidence/06-vacuity-kprove.log`

Stage result: PASS.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For arbitrary finite integer sequences `S0` and `S1`, starting from the exact
clean configuration in `spec.k`, execution of the submitted function body under
the supplied semantics terminates normally with:

```text
sameSet(dedupCodes(S0), dedupCodes(S1))
```

All specified state is restored: environment 0, the two initial scopes,
scope-location 1, empty heap and stack, no pending return, no exception, and
exit code 0. Restricted to sequences representing Python strings, that Boolean
is exactly equality of the strings' character sets. This covers empty strings,
arbitrary finite lengths, duplicates, both Boolean outcomes, and the complete
unbounded HumanEval `str, str` domain. It is not a finite-size proof.

### Trust ledger

| Boundary | Influence | Dependents | Assessment/evidence |
|---|---|---|---|
| K 7.1.293 Haskell prover and K built-in Int/Bool/Map/List/equality hooks | Rewriting and mathematical primitives | Entire proof | Standard low-level proof-system trust; fresh build and exact outputs preserved |
| Supplied semantics' relevant call/scope/set/return rules | Value, control, and temporary state | Entry claim | Required fixed semantics; candidate copy is byte-identical to trusted mount; all result-relevant rules reviewed above |
| Trusted `py2mpy.py` and simple AST transliteration | Python-source-to-constructor bridge | Real-program pinning | Trusted mount, byte-identical candidate copy, fresh byte-identical translation, manual construct map, and KAST subtree equality |
| Interpretation of “same characters” as character-set equality | Human contract bridge | Adequacy | Fixed by the trusted canonical implementation and all prompt examples; independently tested |
| CPython executions in the differential test | Finite empirical support | Source/canonical alignment only | 16,661 comparisons, zero mismatches; not used as a universal proof |
| `MPY-CONCRETE` | Concrete smoke behavior only | `krun` evidence | Not imported by the Haskell proof; no formal claim depends on it |

The imported fixed semantics declares 25 named symbols. The 22 explicit
`no-evaluators` symbols are:

```text
intFloatDiv divII floatMod floatLt absF subF divF addF mulF powF
gtF eqF decStrToF divFloatIntV intToF truncF roundF roundFN sqrtF
md5hexCodes sortVS sortKeyVS
```

The three remaining named float helpers with concrete-only defining equations
are `floorFI`, `toF`, and `ceilF`. None can be constructed or reached from this
program term; none affects a branch, result, cell, exception, or postcondition.
There is therefore no opaque result-bearing assumption in the actual proof.

Unused supplied-semantics limitations include ASCII-only source string-literal
conversion, partial coverage for unrelated builtins/methods, opaque symbolic
floating point, sorting, and md5, and intentionally underspecified invalid
indexing. These are visible in the exhaustive inventory and compiler warnings.
They do not match any reachable constructor in this proof. Inputs enter the
claim directly as `str(IntSeq)`, so the ASCII literal restriction does not
narrow the theorem's string-input domain.

### Gate accounting and decision

- Gate A, real-program soundness: PASS. Exact body, ordinary fixed execution,
  no result oracle, satisfiable claim, body sensitivity, and non-vacuity all
  passed.
- Gate B, intent adequacy: PASS. The unrestricted `str, str` contract is
  covered; the formal domain is broader, not narrower.
- Gate C, trust/evidence auditability: PASS. Commands, statuses, bounded logs,
  scripts, mutations, assumptions, and unused opaque boundaries are preserved.

The candidate therefore meets the benchmark's `PASS / LEGIT` boundary.

VERDICT: PASS
LEGITIMACY: LEGIT
