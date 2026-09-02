# Independent adversarial review: 149-sorted-list-sum

## Decision

The reconstructed target claims do print `#Top`, the submitted Python program
matches the return-value contract on substantial independent testing, and a
fresh false-return mutation is rejected. Those facts do not make the proof
legitimate.

The decisive defect is `verification.k:71-93`: a priority-40 operational rule
replaces the submitted `for` loop with the desired `evenAppend` result. There is
no bridge-free connection theorem. Worse, the rule is false on its stated match
domain because a nonempty Python `for` loop binds its target variable `word`,
while the rule leaves the scope unchanged and admits an arbitrary continuation
that can observe `word`. A fixed-semantics witness establishes the real binding;
the candidate extension proves the contrary symbolic transition for a
satisfiable nonempty input. Thus the rule both bypasses the computation that
must be proved and enables a false conclusion.

This is a candidate failure, not an audit-infrastructure failure.

## 1. Input and provenance integrity

The declared mode is `SUPPLIED_SEMANTICS`. The infrastructure boundary is
consistent: `/reference/reference-semantics` exists as a real directory. The
candidate's `reference-semantics/` recursively matches it with the same
directory/regular-file types and byte contents, has no missing or extra entries,
and contains no symlinks. The candidate `prompt.py` and `py2mpy.py` are likewise
regular files byte-identical to the trusted versions. The recursive manifests
and checks are in
[`01_provenance.log`](evidence/01_provenance.log), with the exact command and
status in [`01_provenance.cmd`](evidence/01_provenance.cmd) and
[`01_provenance.status`](evidence/01_provenance.status) (exit 0).

The following requested generation records are missing from `/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured trace candidate (`*trace*.json`, `*.jsonl`, or trace log) is
present. Therefore there were no such claims to trust or validate. These are
provenance/auditability gaps, but the executable source artifacts were sufficient
for a fresh audit. No candidate `PROOF.md` or `spec-vacuity.k` is present.

The regular source artifacts needed for reconstruction are present:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and the supplied
semantics tree. Non-required candidate artifacts (`__pycache__/`, a `.pyc`,
`concrete-run.out`, `concrete_tests.py/.mpy`, `kprove.out`, and `prove.sh`) were
treated only as untrusted claims. No candidate-built definition or cache was
copied into the audit build.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks for a `list[str]` result that:

1. removes strings of odd length;
2. orders the remaining strings by ascending length; and
3. orders equal-length strings alphabetically, retaining duplicates.

The sentence saying all words have the same length conflicts with both examples
and the preceding general ordering rule. The trusted canonical implementation
settles the intended executable behavior: it lexically sorts the input, filters
even-length strings, then performs a stable length-keyed sort. It mutates its
argument as an incidental effect of `lst.sort()`.

The submitted implementation filters first, lexically sorts the filtered list,
then performs the same stable length-keyed sort. It does not mutate its input.
These algorithms have the same returned value for the stated list-of-strings
domain. The prompt constrains the returned list, not mutation of the argument,
so the mutation difference is recorded but is not a result-contract divergence.

### Translation identity

Using `/reference/py2mpy.py` on the scratch copy of `solution.py` produced a
file byte-identical to submitted `solution.mpy`. Both hashes are
`39fcb6e88010732b87b6c5dee672f79d7d5b9e807254fb8074454cc36ed79662`.
See [`02_translation_identity.log`](evidence/02_translation_identity.log),
[`02_translation_identity.cmd`](evidence/02_translation_identity.cmd), and
[`02_translation_identity.status`](evidence/02_translation_identity.status)
(exit 0).

### Independent differential

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and submitted entry points from separate scratch copies. It also uses
an independently written contract oracle, sorting by `(len(word), word)`.
The exact 5,194 inputs are preserved in
[`differential_inputs.jsonl`](evidence/differential_inputs.jsonl). Coverage was:

- the two documented examples;
- 11 empty/boundary/tie/duplicate/Unicode cases;
- all 4,681 lists of length 0 through 4 over a pool spanning string lengths
  0 through 4, lexical ties, and duplicates; and
- 500 deterministic generated lists with list lengths 0 through 12 and string
  lengths 0 through 8.

There were zero return-value mismatches among the canonical implementation,
submission, and independent oracle. The canonical mutated 4,594 test arguments;
the submission mutated none. See
[`03_differential.log`](evidence/03_differential.log),
[`03_differential.cmd`](evidence/03_differential.cmd), and
[`03_differential.status`](evidence/03_differential.status) (exit 0).
This is finite behavioral evidence, not a K proof.

## 3. Clean proof reconstruction

All sources needed for execution were copied into
`/tmp/audit-work/reconstruction`. Candidate compiled definitions and caches were
not copied or referenced. The tools were Python 3.10.12 and K v7.1.337; see
[`26_tool_versions.log`](evidence/26_tool_versions.log).

### Concrete definition

The LLVM definition was built from the verified supplied-semantics copy:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

It exited 0. Its warnings concern fixed-semantics totality/exhaustiveness in
unrelated helpers and are preserved in
[`04_kompile_concrete.log`](evidence/04_kompile_concrete.log); the exact command
is in [`04_kompile_concrete.cmd`](evidence/04_kompile_concrete.cmd).

The reviewer-authored [`concrete_harness.py`](evidence/concrete_harness.py)
contains the exact submitted function body plus documented, empty, length
0/1/2/3, tie, duplicate, and mixed-length assertions. It was translated with the
trusted translator (exit 0,
[`05_translate_concrete.log`](evidence/05_translate_concrete.log)) and executed
under the fresh LLVM definition (exit 0,
[`06_krun_concrete.log`](evidence/06_krun_concrete.log)). The final configuration
has `.K`, `NoExc`, and exit code 0.

### Proof definition and all positive claims

The Haskell proof definition was freshly built:

```text
kompile verification.k --backend haskell \
  --main-module HUMANEVAL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

The command exited 0; see
[`07_kompile_proof.log`](evidence/07_kompile_proof.log) and its
[`command`](evidence/07_kompile_proof.cmd).

The two candidate claims were copied into separate reviewer modules
[`spec-loop.k`](evidence/spec-loop.k) and
[`spec-entry.k`](evidence/spec-entry.k), then also run together from the original
`spec.k`.

| Target | Exit | Result | Evidence |
|---|---:|---|---|
| Loop claim alone | 0 | `#Top` | [`08_kprove_loop.log`](evidence/08_kprove_loop.log), [`command`](evidence/08_kprove_loop.cmd) |
| Entry claim alone | 0 | `#Top` | [`09_kprove_entry.log`](evidence/09_kprove_entry.log), [`command`](evidence/09_kprove_entry.cmd) |
| Both original claims | 0 | `#Top` | [`10_kprove_all.log`](evidence/10_kprove_all.log), [`command`](evidence/10_kprove_all.cmd) |

Dynamic reconstruction therefore succeeds as a statement about the extended K
theory. Stage 5 shows that the theory is materially unsound.

## 4. Adequacy and real-program pinning

### Loop claim

In plain language, the first claim says: from a loop head over any symbolic
string-list remainder `INPUT`, with target `word`, exact submitted filter body,
an arbitrary continuation `CONT`, an `even_words` list at heap address `H`, and
accumulator contents `ACC`, execution can skip directly to `CONT` and replace
the accumulator by `ACC` followed by all even-length strings in `INPUT`.

The formal precondition is satisfiable. For example, choose `L = 1`, `H = 0`,
`INPUT = .StrList`, `_WHOLE = .StrList`, `ACC = .ValSeq`, `CONT = .K`, a scope
containing exactly `lst` and `even_words` as shown by the claim, and heap address
0 containing the empty list. A nonempty satisfiable instance is the `"aa"`
witness in Stage 5.

The loop head and `filterBody` macro do correspond syntactically to the real
`For` control state and translated body. The post-state does not correspond to
real nonempty-loop control flow: fixed semantics writes the target binding
`word` on every iteration, while the claim leaves the scope unchanged. Because
`CONT` is arbitrary, this is observable and material.

### Entry claim

In plain language, the second claim starts from the initial module environment,
defines the exact submitted `sorted_list_sum` body, and directly calls it on an
unboxed semantic list of symbolic strings. It says that execution:

- installs the exact function closure in the global scope;
- allocates heap 0 for the filtered input in original order;
- allocates heap 1 for `sortVS(filtered)`, the lexical sort;
- allocates heap 2 for the stable `sortKeyVS(..., builtinV("len"))`;
- returns `ref(2)`;
- advances `heapLoc` from 0 to 3; and
- restores the call frame with no exception and exit code 0.

An entry precondition witness is `INPUT = .StrList` with the exact initial
builtins/global scopes, `env = 0`, `scopeLoc = 1`, empty heap, `heapLoc = 0`,
empty stack, `noRet`, `NoExc`, and exit code 0.

The `solutionBody` macro is an exact structural rendering of regenerated
`solution.mpy`: empty-list assignment, `For`, parity `If`, list `append`, nested
lexical `sorted`, stable keyed `sorted(key=len)`, and `Return`. `solutionClosure`
and `solutionGlobals` truthfully name the closure and global map. The entry uses
a bare semantic list rather than allocating source syntax `ListExpr`; supplied
semantics explicitly permits bare read-only list inputs in claims, and this
function does not mutate `lst`. The initial `FuncDef` plus call is the
function-entry theorem rather than a full top-level `#loadAll(Module(...))`
wrapper.

The return is genuinely constrained: `ref(2)` and the exact heap-2 expression
are fixed, not free variables or implications. Ground substitutions for empty,
mixed, duplicate, and ordering-sensitive inputs are preserved in
[`22_ground_claim_results.log`](evidence/22_ground_claim_results.log), generated
by [`ground_claim_results.py`](evidence/ground_claim_results.py). For
`["zzzz","aa","bbbb","cc","x","aa"]`, the three claimed lists are:

- heap 0: `["zzzz","aa","bbbb","cc","aa"]`;
- heap 1: `["aa","aa","bbbb","cc","zzzz"]`; and
- heap 2 / returned list: `["aa","aa","cc","bbbb","zzzz"]`.

Both Python implementations return the heap-2 list.

Syntactic program pinning and result constraint pass. Semantic pinning fails
because the entry proof reaches its postcondition through the rejected loop
bridge rather than proving execution of the loop body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule_inventory.md`](evidence/rule_inventory.md), generated by
[`inventory_k.py`](evidence/inventory_k.py), is the exhaustive line-addressed
inventory for all 24 supplied-semantics K files plus `verification.k` and
`spec.k`. It includes every local configuration, syntax declaration, context,
rule, claim, guard, and attribute in normalized full-block form, with a per-item
`ACCEPT`, `TRUST`, `TARGET`, or `REJECT` assessment.

Inventory totals are:

- 1 configuration;
- 234 syntax declarations, including 148 `[function]`, 110 `[total]`,
  25 `[symbol]`, 22 `[no-evaluators]`, 6 macros, and 1 recursive macro;
- 5 evaluation contexts;
- 705 rules, including 35 `[concrete]`, 26 `[owise]`, one priority 39,
  42 priority 40, and three priority 45 rules; and
- 2 reachability claims.

There are no local `[simplification]` rules and no `[functional]` claims or
declarations. The assessment totals are 922 accepted declarations/rules, 22
explicit opaque trust boundaries, two target claims, and one rejected rule.
The inventory command exited 0; see
[`23_rule_inventory_assessed.log`](evidence/23_rule_inventory_assessed.log).

The supplied tree is the selected fixed semantics. Rules in its used execution
slice were checked against the submitted constructs; rules in unreachable
language features were reviewed and marked unreachable rather than used as
proof evidence. Concrete-only rules are separated from the Haskell proof
definition. Opaque primitives are accounted for in Stage 7.

### Used-construct map and operational checks

| Submitted construct | Declaration and governing rules |
|---|---|
| `Module`, statement sequence | `semantics/syntax.k`; `core.k` `#loadAll`, statement sequencing, `.Stmts` |
| `FuncDef`, parameters, call, return | `syntax.k`; `functions.k` closure installation/binding/return/pop; `call.k` callee and left-to-right argument evaluation |
| `Assign`, `ListExpr` | `controls.k` assignment; `list.k` argument fold and fresh `#alloc`; `core.k` heap allocation |
| `For` over list | `controls.k` `For => #loop`, loop step; `list.k` iterator; `tuple.k` `#bindTgt(Name, V)` |
| `If`, comparison, `%`, integer literals | `controls.k` branching; `operators.k` dispatch/evaluation; `int.k` `pyMod` and equality; `core.k` truth |
| `Name("len")` and calls | `core.k` lexical lookup/builtins scope; `call.k`; `builtins.k` `len => seqLen`; `core.k` `isLen` |
| `Attribute(...,"append")`, expression statement | `call.k` bound-method routing; `list.k` in-place append; `controls.k` discards the returned `noneV` |
| nested `sorted`, `KwArg("key",len)` | `core.k` keyword tagging; `call.k`; `sort.k` allocation through `sortVS` and `sortKeyVS`; `concrete.k` executes real key calls in LLVM only |
| symbolic strings | candidate `StrList/strVals`; fixed `str(IntSeq)` and `isLen`; `str.k` lexical concrete ordering |

The fixed rules preserve the expected evaluation order: `For` evaluates its
iterable once; calls evaluate callee then arguments left-to-right; the condition
evaluates `len(word)`, modulo 2, and equality before branching; append writes the
heap in place; nested sorting allocates two fresh result lists; function return
pops and restores the caller frame. With an unboxed input, the allocation
sequence is exactly heap 0 for `even_words`, heap 1 for lexical sort, and heap 2
for keyed sort.

### Candidate-local rules other than the bridge

- `strVals(.StrList)` and the `sCons` equation are truthful structural
  conversions.
- `evenAppend` has a correct base case. Its two recursive guards
  `pyMod(isLen(CS),2) == 0` and `=/= 0` are disjoint and exhaustive for the
  structurally represented strings; recursion strictly decreases `REST`.
- `filterBody` and `solutionBody` are exact macros for regenerated
  `solution.mpy`.
- `solutionClosure` and `solutionGlobals` are total definitional names with one
  equation covering their declared argument domains.

These rules neither overlap inconsistently nor introduce fresh/unconstrained
result values.

### Rejected operational bridge

The rule at `verification.k:71-93` is an operational bridge, not an invariant or
derived lemma:

```text
<k> #loop(list(strVals(INPUT)), Name("word"), filterBody) ~> CONT
 => CONT </k>
...
<heap> ... H |-> list(ACC)
 => H |-> list(evenAppend(ACC, INPUT)) ... </heap>
[priority(40)]
```

Its complete match domain includes every `StrList INPUT`, arbitrary `CONT`,
arbitrary `L/H/ACC`, the exact two-local ordinary function frame, and all
omitted configuration cells. Priority 40 preempts the fixed default `#loop`
step. It reads the continuation, environment, scope, and accumulator heap cell;
it writes only the accumulator heap cell. Fixed execution also writes the
current scope by binding `word` on every nonempty iteration. The bridge neither
preserves nor abstracts that effect in its destination, and its arbitrary
continuation may immediately read `word`.

There is no bridge-free universal connection theorem over this match domain.
The first target claim is textually the same transition as the rule, so it
closes by applying the assumed operational rule; it is not an independent
induction or circularity proof. The same rule directly encodes the task-bearing
filter result with `evenAppend` and bypasses execution of `len`, `%`, the branch,
and `append`.

#### Required false-conclusion witness

The reviewer files are:

- fixed support without the candidate bridge:
  [`witness-fixed.k`](evidence/witness-fixed.k);
- true ground fixed-semantics claim:
  [`witness-fixed-true-spec.k`](evidence/witness-fixed-true-spec.k);
- false unchanged-scope fixed claim:
  [`witness-fixed-false-spec.k`](evidence/witness-fixed-false-spec.k); and
- the same false transition enabled by the bridge:
  [`witness-bridge-false-spec.k`](evidence/witness-bridge-false-spec.k).

For the ground input `["aa"]` and continuation `Name("word")`, fixed semantics
proves that the loop appends `"aa"`, binds `"word" |-> "aa"` in the function
scope, and evaluates the continuation to `"aa"`:
[`21_fixed_true_witness_final.log`](evidence/21_fixed_true_witness_final.log)
prints `#Top` and exits 0.

Fixed semantics rejects the candidate-style conclusion that the heap changes but
the scope remains without `word`:
[`18_fixed_rejects_false_witness_v2.log`](evidence/18_fixed_rejects_false_witness_v2.log)
exits 1 with `WarnStuckClaimState`; its residual explicitly contains
`"word" |-> str(97,97)` and the final string value.

With the candidate bridge imported, the false unchanged-scope transition under
the satisfiable precondition `INPUT =/=K .StrList` prints `#Top` and exits 0:
[`19_bridge_proves_symbolic_false.log`](evidence/19_bridge_proves_symbolic_false.log).
The precondition has the concrete witness
`INPUT = sCons([97,97], .StrList)`, i.e. `["aa"]`. This establishes a symbolic
false-conclusion witness on the intended nonempty list-of-strings domain.

Earlier witness iterations 13-15, 17, and 20 are preserved rather than hidden;
they failed because reviewer harnesses initially omitted the builtins/global
scopes or rewrote them out of the destination. The corrected fixed definition
build is log 16, and the conclusive runs are logs 18, 19, and 21. These earlier
harness defects are unrelated to the candidate verdict.

The bridge therefore fails binding fidelity, state preservation, context
containment, body sensitivity, and the requirement for a bridge-free connection
theorem. This single rejected rule is material and makes the proof
`NOT_LEGIT`.

## 6. Fresh non-vacuity test

There was no candidate vacuity artifact to trust. The fresh mutation
[`spec-vacuity.k`](evidence/spec-vacuity.k) changes the entry result from
`ref(2)` to `ref(1)` while retaining the exact post-state heap. This is
demonstrably false: heap 1 is the intermediate lexical sort, heap 2 is the
returned keyed sort, and the ordering-sensitive ground case in Stage 4 gives
different list contents at those references.

The mutation parsed and built successfully with `kprove --dry-run` (exit 0):
[`24_vacuity_build.log`](evidence/24_vacuity_build.log) and
[`24_vacuity_build.cmd`](evidence/24_vacuity_build.cmd).

The actual mutation proof exited 1 with `WarnStuckClaimState`. Its residual is
the complete intended post-state with `<k> ref(2) ~> .K </k>`, which fails to
unify with the mutated `ref(1)` destination. See
[`25_vacuity_expected_failure.log`](evidence/25_vacuity_expected_failure.log),
[`25_vacuity_expected_failure.cmd`](evidence/25_vacuity_expected_failure.cmd),
and [`25_vacuity_expected_failure.status`](evidence/25_vacuity_expected_failure.status).
This is meaningful non-vacuity evidence. It shows the entry postcondition
constrains the result; it does not validate the assumed loop summary.

## 7. Proven versus assumed accounting

### What the successful reachability run actually establishes

Under the supplied MPY semantics **plus** the candidate priority-40 loop axiom,
the structurally encoded function call reaches `ref(2)` with heap cells
`evenAppend`, `sortVS(evenAppend(...))`, and
`sortKeyVS(sortVS(evenAppend(...)), builtinV("len"))`, restores its call frame,
and has no modeled exception. The entry claim is universal over the candidate
`StrList` representation and is partial-correctness only.

It does not establish that fixed semantics executes the submitted loop to
produce `evenAppend`. That property is assumed by the rejected bridge. The
positive loop claim merely restates and applies the assumption.

### Trust ledger

1. **Supplied operational semantics and K backend.** The configuration,
   allocation, maps/lists, integer and Boolean hooks, strictness-generated
   contexts, call stack, and operational rules are selected fixed semantics.
   This is the legitimate base trust boundary. The complete per-rule accounting
   is in `rule_inventory.md`.

2. **Used result-bearing supplied primitives.** `sortVS(ValSeq)` and
   `sortKeyVS(ValSeq, Val)` are `[function,total,symbol,no-evaluators]` in the
   Haskell proof. The entry theorem is structural and conditional on their
   supplied contracts: ascending lexical sort, then stable ascending key sort.
   LLVM has concrete insertion/key-call implementations, and the independent
   differential supplies finite support. No candidate rule defines their result,
   so this is an explicit supplied-semantics limitation rather than smuggled
   candidate correctness.

3. **Unused supplied opaque/symbolic primitives.** `md5hexCodes`; the float
   family `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`,
   `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
   `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
   `sqrtF` are imported by the broad fixed language but unreachable from this
   submitted program and do not influence its branch, result, state, or claims.

4. **Candidate structural definitions.** `StrList`, `strVals`, `evenAppend`,
   `filterBody`, `solutionBody`, `solutionClosure`, and `solutionGlobals` are
   truthful definitions/macros. `evenAppend` names the mathematical filter but
   does not itself connect that result to execution.

5. **Illegitimate candidate assumption.** The `#loop => CONT` rule is a
   result-bearing operational bridge over program-defined computation. It
   changes observable state incorrectly, has no bridge-free universal
   connection theorem, and is exactly what the claims depend on. This is not an
   acceptable primitive or informal bridge.

6. **Empirical and informal bridges.** Translation identity connects
   `solution.py` to `solution.mpy` byte-for-byte. Manual structural comparison
   connects `solution.mpy` to the K macros. The 5,194-case differential and
   LLVM harness support Python/MPY behavior and supplied sort interpretations
   only on tested inputs. The interpretation of the contradictory
   same-length sentence follows the examples and canonical executable oracle.
   None of this substitutes for the missing K connection proof.

### Final judgment

The candidate passes clean reconstruction and non-vacuity, and its Python
return values agree with the intended behavior. It nevertheless relies on a
materially unsound proof-local rule that bypasses the real loop and proves a
false state transition on a satisfiable intended-domain input. Under the stated
decision boundary this requires `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
