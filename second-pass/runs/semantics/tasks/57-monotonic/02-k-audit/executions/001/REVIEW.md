# Independent adversarial audit: 57-monotonic

The candidate is **not a legitimate proof of the real generated program**. Fresh
reconstruction does reproduce `#Top`, and the Python implementation is correct,
but `#Top` depends on a proof-only priority rewrite that replaces fixed list
equality with an under-specified `sortEquality` function. That extension has no
bridge-free connection theorem and is demonstrably incompatible with concrete
instances of its own match domain and with concrete instances of the entry
claim. The result is a symbolic proof of a substituted computation, not a
partial-correctness proof of fixed MPY execution.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` exists. There is no infrastructure-mode
contradiction and therefore no `AUDIT_ERROR` condition.

The candidate `reference-semantics/` tree is recursively identical to the
trusted tree:

- the entry-type inventory is identical;
- `diff --no-dereference --recursive --brief` exits 0;
- the candidate tree contains no symlinks;
- there are no missing, additional, changed, or mistyped semantics entries.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
counterparts. Exact hashes, type inventories, comparisons, and exit statuses
are in `evidence/01_integrity.log`.

### Missing provenance material

The following requested untrusted provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace, `PROOF.md`, or `spec-vacuity.k` is present
either. Thus there were no candidate provenance claims to rely on. The missing
run metadata weakens auditability but is not the reason for the negative
verdict.

All candidate sources needed for execution were copied into
`/tmp/audit-work/57-monotonic`; the scratch proof uses a fresh copy of the
trusted semantics, not candidate kompiled output. The candidate contained no
compiled definition or cache to reuse.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

`/reference/prompt.py` asks for `monotonic(l)` to return true when the list is
monotonically increasing or decreasing. The canonical implementation resolves
that wording as *non-strict* monotonicity:

```python
l == sorted(l) or l == sorted(l, reverse=True)
```

Consequently, equal adjacent elements are allowed; empty and singleton lists
return true. Python requires the list elements to be mutually sortable. The
usual generated-task domain is integer lists, while homogeneous comparable
values such as strings also work. Heterogeneous or otherwise non-sortable lists
may raise `TypeError` and are not given a normal-return contract.

`/candidate/solution.py` directly returns the same Boolean expression. Its
removal of the canonical `if` statement is semantics-preserving.

### Trusted retransliteration

The trusted `/reference/py2mpy.py` regenerated `solution.mpy` from the copied
`solution.py`. The regenerated and submitted files are byte-identical, both
with SHA-256:

```text
efcae99a7903e4a959bb61e2ac1113d385407855b762284799cc7e917b744c66
```

Commands and results are in `evidence/02_prepare_and_translate.log`.

### Independent differential test

`evidence/02_differential.py` imports the trusted canonical entry point and the
copied generated entry point independently. It exercises:

- all three documented examples;
- empty, singleton, equal, strict-increase, and strict-decrease boundaries;
- equality-containing nondecreasing and nonincreasing cases;
- both minimal zigzag branch failures and late direction reversals;
- large-magnitude integers and homogeneous string lists;
- all 3,906 integer lists of length 0 through 5 over
  `{-2,-1,0,1,2}`;
- 1,000 deterministic random integer lists of length 0 through 15.

All 4,925 cases completed with zero exceptions and zero mismatches. Exact
inputs are preserved in `evidence/02_differential_inputs.json` (hash recorded
in the log), and results and exit status 0 are in
`evidence/02_differential.log`. This is strong implementation-to-canonical
evidence, but it is finite testing and does not replace the K proof.

## 3. Clean proof reconstruction

K v7.1.337 was available at `/usr/bin/{kompile,kprove,krun}`. From clean source:

1. the trusted supplied semantics was compiled with the LLVM backend as
   `MPY-KRUN`;
2. a reviewer-generated boundary smoke program was translated with the trusted
   translator and executed to `.K`, `NoExc`, and exit code 0;
3. `verification.k` was compiled with the Haskell backend as
   `MONOTONIC-VERIFICATION`;
4. the submitted aggregate two-claim spec was proved;
5. each entry claim was copied unchanged into its own labeled module and proved
   separately.

All builds exit 0. The original aggregate run and both isolated positive claim
runs each print `#Top` and exit 0. Full bounded commands and output are in
`evidence/03_rebuild.log`; the isolated specs are
`evidence/03_spec_claim_1.k` and `evidence/03_spec_claim_2.k`.

The compiler reports supplied-semantics non-exhaustiveness warnings for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These
constructs are not on this program's integer-list execution path. `valSeqAt`'s
opaque/OOB totalization is explicitly part of the supplied abstraction. The
warnings do not explain the candidate `#Top`.

This stage establishes only closure under the submitted extended theory. It
does not establish that the extensions preserve the selected semantics.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Both claims start from the standard module configuration: environment 0, an
empty module scope whose parent is the supplied builtins scope, fresh scope and
heap locations, empty heap and call stack, `noRet`, `NoExc`, and exit code 0.
Both load `monotonicProgram` and call `monotonic` on the bare list value
`list(VS)`.

Claim 1 says:

> For any `VS` satisfying `nondecreasing(VS)`, execution returns `true`.

Claim 2 says:

> For any `VS` not satisfying `nondecreasing(VS)`, execution returns
> `nonincreasing(VS)`.

The preconditions partition Boolean `nondecreasing(VS)`, and together the
postconditions describe
`nondecreasing(VS) orBool nonincreasing(VS)`. The return value is constrained,
not existential or tautological. Final scope and heap state are existential,
but the stack, return marker, exception, and exit code are fixed; allocating
the two `sorted` results is intentionally allowed.

Concrete satisfying witnesses are preserved in
`evidence/04_claim_witnesses.py` and its log:

| Claim | `VS` | Preconditions | Claimed result | Both Python results |
|---|---|---|---|---|
| 1 | `[1,2,2]` | nondecreasing = true | true | true |
| 2 | `[1,0,1]` | not nondecreasing = true | nonincreasing = false | false |
| 2 | `[2,1]` | not nondecreasing = true | nonincreasing = true | true |

### Program identity

The `<k>` cell does not parse `solution.mpy` at proof time. Instead,
`verification.k` defines a `monotonicProgram` constant containing a handwritten
MPY AST. Independent line-by-line inspection shows that constant is the same
`Module(FuncDef(...))` tree as the trusted regenerated `solution.mpy`, including
the docstring statement, Boolean short circuit, both `sorted` calls, and the
`reverse=true` keyword. This audited identity is adequate to pin the submitted
AST even though it is not an automatic file dependency.

Fixed rules do load the module, bind and call the real function body, evaluate
the docstring, perform name lookup and argument evaluation, allocate sorted
lists, short-circuit `or`, and perform return/pop. However, the
property-bearing list comparisons do **not** execute under fixed rules: the
candidate's priority-45 bridge replaces them. Therefore the real-program
pinning gate fails at the very operation determining the result.

### Ground specialization failure

`evidence/04_ground_entry_spec.k` substitutes the satisfying input `[1,2,2]`
and the zigzag input `[1,0,1]` into the entry claims. The proof definition gets
stuck on ground `sortEquality` terms and exits 1 instead of proving these
instances. In particular, the increasing witness that both Python
implementations map to `true` leaves constraints such as:

```text
true #Equals
  sortEquality(
    vCons(1, vCons(2, vCons(2, .ValSeq))),
    vCons(1, vCons(2, vCons(2, .ValSeq))))
```

The symbolic `#Top` therefore does not validly specialize to a concrete
satisfying input. Running the full concrete smoke program through the Haskell
proof definition likewise exits 111 with assertion branches constrained by
unreduced ground `sortEquality` terms. These results are in
`evidence/04_gate_a_experiments.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/04_rule_inventory.py` independently enumerates every local
configuration, syntax declaration, context, rule, and claim in the assembled
semantics, all 23 helper files, `verification.k`, and `spec.k`.
`evidence/04_rule_inventory.tsv` contains source path, line, kind, all detected
attributes, classification, decision, and normalized full declaration/rule.
Its SHA-256 is:

```text
46999f3fc5b393eba81055d6e1ca5747438d7687a13307f7f8a02d9344cce087
```

The 945 inventoried entries comprise one configuration, 231 syntax
declarations, 706 rules, five contexts, and two claims. There are no
`functional` declarations. The candidate-local inventory is 15 entries:
four syntax declarations and eleven rules. All `function`, `total`, `symbol`,
`no-evaluators`, `concrete`, `owise`, `macro`, `priority`, and
`simplification` attributes are retained in the TSV rather than inferred from
the candidate's comments.

The supplied tree is an exact trusted baseline, but it was still reviewed
statically. Grouped disposition of every inventoried supplied entry is:

| File | Entries | Role and decision |
|---|---:|---|
| `syntax.k` | 16 | AST grammar/strictness; accepted; declares every source node used here |
| `core.k` | 84 | configuration, load, sequencing, lookup, argument order, literals, allocation; accepted on the used path |
| `iter.k` | 1 | iterator declarations; unused |
| `range.k` | 8 | range functions/rules; unused |
| `operators.k` | 12 | comparison contexts, fixed dispatch, ref dereference; accepted and used |
| `int.k` | 17 | integer arithmetic/comparison; accepted; `<=`/`>=` used by summaries |
| `bool.k` | 14 | truth and short-circuit order; accepted and used |
| `float.k` | 155 | float opaque/concrete boundary; unused here; compiler coverage warnings recorded |
| `str.k` | 33 | string model/order; docstring literal path used, string ordering otherwise unused |
| `set.k` | 18 | set operations; unused |
| `list.k` | 32 | list structure and fixed equality `A ==K B`; accepted and central |
| `tuple.k` | 25 | tuple/binding operations; unused |
| `subscript.k` | 57 | indexing/slicing; unused; supplied totalization warning recorded |
| `comprehension.k` | 10 | macro expansion; unused |
| `methods.k` | 102 | string/list methods; unused |
| `controls.k` | 37 | expression-statement discard used for docstring; other controls unused |
| `functions.k` | 19 | function definition, call-frame return/pop; accepted and used |
| `builtins.k` | 175 | builtins registry implementations; only registry relationship is used |
| `call.k` | 24 | callee/argument order and closure/builtin dispatch; accepted and used |
| `sort.k` | 25 | opaque symbolic sort plus concrete int/string sort; trusted boundary and used |
| `assert.k` | 3 | smoke-only assertion behavior |
| `dict.k` | 40 | dict operations; unused |
| `concrete.k` | 21 | LLVM-only deep equality/key sort; absent from Haskell proof import |

No candidate-local rule outside the list-equality abstraction has a false
witness on the intended integer-list domain:

- `monotonicProgram` is a terminating definitional constant and is independently
  pinned to the regenerated AST.
- `nondecreasing` and `nonincreasing` recurse structurally, have disjoint
  empty/singleton/long-list cases, and faithfully define adjacent non-strict
  order wherever `applyCmp("<=")`/`applyCmp(">=")` is modeled.
- `isMonotonic` is the correct disjunction, but the entry claims do not use it
  directly.

The formal `ValSeq` domain is broader than Python's normally returning sortable
lists; many heterogeneous `Val` comparisons are not modeled. No false result
witness was found from that breadth because such terms generally remain
undefined rather than fabricate a Boolean. This is an adequacy limitation, not
the unsoundness finding below.

### Used-construct map and control/state audit

| Submitted MPY construct | Declaration | Execution rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k`/`functions.k` value syntax | `#loadAll`, statement sequencing, `FuncDef` closure binding |
| `Expr(Str(...))` | `syntax.k`, `core.k`, `str.k` | ASCII string construction, then expression-value discard |
| `Return` | `syntax.k` | strict result evaluation, `retV`, `#pop`, environment/stack restoration |
| `BoolOp("or",...)` | `syntax.k` | head-only heat/cool and truth-based short circuit in `bool.k` |
| `Compare`, `CmpOp` | `syntax.k` | comparison contexts and fixed `applyCmp` dispatch in `operators.k` |
| `Name` | `syntax.k` | lexical/builtins lookup in `core.k` |
| `Call` | `syntax.k` | callee first, then left-to-right arguments, closure/builtin dispatch |
| `KwArg`, `Bool(true)` | `syntax.k` | keyword tagging and Boolean literal in `core.k` |
| `sorted(l)` | builtins scope and `sort.k` | dereference input, allocate `list(sortVS(VS))` |
| `sorted(l, reverse=True)` | same | `condRev`, `revVS`, `revVSAcc`, then allocation |
| list `==` | `operators.k`, `list.k` | fixed result is structural `A ==K B`; candidate bridge preempts it |

Argument and Boolean evaluation order match Python for this body. Function
entry allocates a scope, binds `l`, and pushes a continuation frame; return pops
the frame. `sorted` allocates fresh heap objects while preserving the input.
The exception and exit cells remain unchanged on the proved symbolic paths.
There is no loop or helper reachability claim.

### Rejected proof-local extension

The decisive extension is:

```k
rule <k>
       Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq)))
       => sortEquality(A, B)
     ... </k>
     [priority(45)]
```

Its complete match domain is **every** list/list equality in any continuation.
It has no guard, omits all non-`<k>` cells, preserves the continuation, and
reads or writes no state cell. The fixed semantics would instead use the
comparison contexts, the generic comparison rule, and:

```k
applyCmp("==", list(A), list(B)) => A ==K B
```

Thus it is an operational bridge, not merely a name for a value. Priority 45
causes it to preempt fixed execution.

The replacement is declared:

```k
sortEquality(ValSeq, ValSeq)
  [function, total, symbol(sortEquality), no-evaluators]
```

but has only two simplification equations, for exactly
`(VS, sortVS(VS))` and
`(VS, revVSAcc(sortVS(VS), .ValSeq))`. The equations are disjoint and express
ordinary monotonicity facts if `sortVS` is assumed to be a real ascending sort.
No concrete or symbolic false witness was found for those *narrow mathematical
facts themselves*, so this review does not label those facts false.

The operational bridge is nevertheless invalid over its declared/matched
domain:

- `sortEquality` is not total. Equal ground singleton lists, empty ground
  lists, and almost every arbitrary pair match the bridge but match neither
  equation.
- The bridge accepts far more contexts and values than the two equations
  justify.
- There is no bridge-free universal connection theorem relating fixed
  `A ==K B` to `sortEquality(A,B)`.
- The same new symbol supplies both the replaced execution value and the
  postcondition-driving summaries; without an independent connection, that is
  circular.
- When `sortVS`'s supplied `[concrete]` rules reduce a ground sort, the special
  syntactic wrapper disappears before either equation can match. This is why
  the symbolic proof does not specialize.

The required concrete false-conclusion/behavior witness is the intended-domain
singleton equality:

```text
Compare(list([1]), CmpOp("==", list([1])))
```

Under fixed semantics, `evidence/04_fixed_equal_lists_spec.k` proves that the
result is `true` (`#Top`, exit 0). Under the candidate extension,
`evidence/04_extended_equal_lists_spec.k` gets irreducibly stuck at
`sortEquality([1],[1])` (exit 1). Commands and residual are in
`evidence/04_ground_bridge_witness.log`.

The stronger real-program witness is `[1,2,2]`: it satisfies entry claim 1 and
both Python implementations return true, while the candidate's ground entry
claim is stuck. Therefore the symbolic candidate claim's purported universal
reachability conclusion is false for a concrete satisfying specialization of
the submitted definition.

### Ablation and missing connection

`evidence/04_verification_no_bridge.k` removes only the bridge and its two
equations while retaining the exact program constant and monotonicity
definitions. It recompiles successfully. The entry proof then exits 1 with the
genuine residual `VS ==K sortVS(VS)` /
`VS ==K revVSAcc(sortVS(VS), .ValSeq)`.

`evidence/04_bridge_connection_spec.k` attempts both required bridge-free
universal connections directly. It builds, but `kprove` exits 1 with the
expected failed implication between fixed structural equality and the
monotonicity summary. This failure does not prove the mathematical sorting
lemma false; it proves that the submitted K theory contains no independent
machine-checked connection. Exact residuals are in
`evidence/04_gate_a_experiments.log`.

Gate A therefore fails. The positive `#Top` is unusable as a proof of the real
program.

## 6. Fresh non-vacuity test

The reviewer-created `evidence/06_false_mutation.k` changes claim 1's required
result from `true` to `false` while retaining its satisfiable
`nondecreasing(VS)` precondition. The empty list is a concrete witness:
`nondecreasing(.ValSeq)` is true and both Python implementations return true.

The mutation:

- parses and compiles under `kprove --dry-run` with exit 0;
- runs under the fresh proof definition;
- exits 1 with `WarnStuckClaimState`;
- leaves `true` in `<k>` while the destination demands `false`.

The failure is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. Commands, status, residual, and
Python witness are in `evidence/06_nonvacuity.log`.

This shows that the submitted symbolic proof is result-discriminating. It does
not repair the independent real-program soundness failure.

## 7. Proven versus assumed accounting

### What the successful `#Top` actually establishes

Under the *extended symbolic theory*, and while a symbolic `sortVS(VS)` wrapper
remains syntactically present, the proof establishes:

- if `nondecreasing(VS)` is true, the substituted comparison summary returns
  true;
- otherwise, the substituted reverse-sort summary returns
  `nonincreasing(VS)`;
- the function-call/control machinery reaches a normal returned value with
  empty stack, `noRet`, `NoExc`, and exit code 0.

That is a theorem about `sortEquality`-substituted symbolic execution. Because
fixed list equality is neither executed nor independently connected, it is not
a theorem about all executions of the submitted MPY program.

### Trust and assumption ledger

1. **K toolchain and builtin theories.** K v7.1.337, the Haskell/LLVM backends,
   and imported integer, Boolean, string, map, list, float, and K-equality hooks
   are foundational trust. This is an ordinary and acceptable verification
   boundary.

2. **Supplied MPY semantics.** The exact trusted tree is the selected fixed
   semantics. Its subset choices, totalizations, and unused coverage warnings
   are conditional model boundaries. Integrity is established, and no
   candidate change to this tree exists.

3. **`sortVS`.** This is the only supplied result-bearing opaque symbol used by
   the theorem. The semantics declares it a trusted ascending sort for symbolic
   lists and supplies concrete insertion-sort rules for ground integer/string
   lists. Its universal correctness is not proved in this candidate. LLVM smoke
   execution and the Python differential test provide finite support only.
   Treating it as an external primitive is acceptable if conclusions remain
   conditional on its named sorting contract.

4. **Other supplied opaque symbols.** `sortKeyVS`, `md5hexCodes`,
   `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
   `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
   `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
   `sqrtF` appear in the trusted full semantics but are unreachable from this
   submitted program and do not contribute to either claim.

5. **`sortEquality`.** This is candidate-created, result-bearing, and directly
   determines branches and the final result. It is not an acceptable trusted
   primitive: it replaces a program operation inside the theorem, is falsely
   declared total, has no bridge-free connection, and fails concrete
   fixed-versus-extended witnesses.

6. **Program-to-canonical intent bridge.** Source inspection, exact trusted
   translation, and 4,925 differential cases strongly support the Python
   implementation. This finite empirical evidence supports only fidelity to
   the canonical implementation; it cannot validate the missing K connection.

7. **Partial correctness/termination scope.** A legitimate reachability proof
   would establish only normal terminating executions from its precondition.
   The candidate claims do require normal final exception/exit state. The
   verdict is not based on a termination obligation.

### Decision

Stages 1–3 establish clean provenance where present, Python fidelity, fresh
buildability, and reproducible positive `#Top`. Stage 6 establishes
non-vacuity. Stage 5 nevertheless supplies a concrete intended-domain witness
that the result-bearing operational bridge does not preserve fixed execution,
and Stage 4 shows that even a satisfying ground entry instance is not proved.
This meets the decision boundary for a substituted/unsound proof theory.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
