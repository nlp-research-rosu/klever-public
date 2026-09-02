# Independent adversarial audit: 22-filter-integers

## Outcome

The candidate cleanly reconstructs four non-vacuous reachability proofs under
the supplied K semantics, and the proof executes an AST identical to the
submitted `solution.mpy`. Those facts are not enough to constitute the requested
proof of the real Python program:

1. the four claims cover only four fixed input shapes, not the stated
   `List[Any]` domain; and
2. the submitted `order-and-scalars` theorem is false for a concrete satisfying
   input in both the trusted canonical Python and `solution.py`. For
   `[True, 7, None, "x", 9]`, the formal postcondition says `[7, 9]`, while both
   Python implementations return `[True, 7, 9]`.

The second issue is a concrete semantic-adequacy failure, not merely thin
testing or an informal bridge. CPython's `bool` is a subclass of `int`, whereas
the supplied model's `isIntV` function classifies K `Bool` as non-`Int`.

All candidate artifacts were treated as untrusted. No candidate-provided
compiled definition or cache was used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is no
mode/mount contradiction and therefore no audit-infrastructure breach.

The reviewer-authored checker
[`evidence/stage1_integrity.py`](evidence/stage1_integrity.py) recursively
compared entry names, entry types, symlink status, and SHA-256 digests. Its run
is in [`evidence/stage1-integrity.log`](evidence/stage1-integrity.log):

- candidate `reference-semantics/` and the trusted tree are identical;
- there are no missing, additional, mistyped, changed, or symlinked semantics
  entries;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

The complete typed inventories are recorded in
[`evidence/stage1-tree-inventory.log`](evidence/stage1-tree-inventory.log).
`solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular files.
The candidate also contains auxiliary `concrete_tests.*`, `prove.sh`, and a
`__pycache__/solution.cpython-310.pyc`; none was used as trusted proof evidence
or copied as a build product.

### Missing provenance records

The candidate has no `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, or structured generation-trace file. The exhaustive root
inventory also shows no differently named trace-like artifact. The explicit
checks are in [`evidence/stage1-metadata.log`](evidence/stage1-metadata.log).
This limits generation provenance but does not prevent an independent source
reconstruction.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks `filter_integers(values: List[Any])` to return the input
elements that are instances of Python `int`, preserving their order. The
trusted canonical implementation is:

```python
return [x for x in values if isinstance(x, int)]
```

Consequently, on the declared Python domain, Boolean values and instances of
an `int` subclass are retained: `isinstance(True, int)` is true.

The submitted `solution.py` implements the same filter with an explicit
accumulator, `for` loop, `if isinstance(value, int)`, and `append`. It does not
mutate the input and preserves order and duplicate occurrences.

The source inspection, including trusted prompt/canonical and all candidate K
sources, is preserved in
[`evidence/stage2-source-inspection.log`](evidence/stage2-source-inspection.log).

### Trusted regeneration

In the isolated scratch tree, the trusted translator was run as:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -l solution.mpy regenerated-solution.mpy
```

Both files have SHA-256
`caa0e9fffddb1e422387467f4480c6bdfb3bb7ce7d5ed0394eb61b8a51a0e0f9`;
`cmp` exited 0. See
[`evidence/stage2-translation-fidelity.log`](evidence/stage2-translation-fidelity.log).

### Independent differential test

The reviewer-authored differential test is
[`evidence/stage2_differential.py`](evidence/stage2_differential.py). It imports
the entry points directly from the trusted `/reference/canonical.py` and
untrusted `/candidate/solution.py`; it does not reuse K equations. Its corpus
contains:

- both documented examples;
- the empty list;
- all-integer and all-non-integer lists;
- alternating branch outcomes;
- zero, negative, huge positive, and huge negative integers;
- `False`, `True`, an `int` subclass, floats, infinity, NaN, strings, `None`,
  lists, dictionaries, tuples, and sets;
- all 11,111 lists of length zero through four over ten representative atoms;
- 500 deterministic generated lists of length zero through twenty with seed
  `220726`.

The command exited 0 with 11,621 cases and zero mismatches. The script, exact
command, named results, deterministic input construction, and summary are in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log).
This is finite evidence supporting source-to-canonical fidelity, not a K proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to the fresh directory
`/tmp/audit-work/22-filter-integers-review`. The semantics was copied from the
trusted `/reference/reference-semantics`, not from a candidate cache. No
`*-kompiled` directory, `.pyc`, or other built candidate artifact was copied.
The copy command and resulting source-only inventory are in
[`evidence/stage2-scratch-copy.log`](evidence/stage2-scratch-copy.log).

The available independently installed tools report K
`v7.1.337`, build date June 18, 2026. See
[`evidence/stage3-toolchain.log`](evidence/stage3-toolchain.log).

### Concrete definition

The concrete definition was freshly built with:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. The compiler emitted bounded warnings about non-exhaustive
unrelated total functions and unused string-rule variables; it did not fail.
The exact output is in
[`evidence/stage3-kompile-concrete.log`](evidence/stage3-kompile-concrete.log).

### Proof definition

The proof definition was freshly built with:

```text
kompile verification.k \
  --backend haskell \
  --main-module FILTER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; see
[`evidence/stage3-kompile-proof.log`](evidence/stage3-kompile-proof.log).

### Every positive target claim

Each claim was selected and run independently with the shape:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FILTER-SPEC \
  --claims FILTER-SPEC.<label>
```

All four exited 0 and printed `#Top`:

| Claim | Evidence |
|---|---|
| `empty` | [`evidence/stage3-kprove-empty.log`](evidence/stage3-kprove-empty.log) |
| `prompt-example-one` | [`evidence/stage3-kprove-prompt-example-one.log`](evidence/stage3-kprove-prompt-example-one.log) |
| `prompt-example-two` | [`evidence/stage3-kprove-prompt-example-two.log`](evidence/stage3-kprove-prompt-example-two.log) |
| `order-and-scalars` | [`evidence/stage3-kprove-order-and-scalars.log`](evidence/stage3-kprove-order-and-scalars.log) |

Thus the submitted claims genuinely close under the submitted proof module and
the intact supplied semantics. This mode does not call for generated-semantics
validation.

## 4. Adequacy and real-program pinning

### Shared claim state

Every claim starts in a satisfiable pristine configuration:

- `<k>` loads `FILTER-PROGRAM` and then calls its `filter_integers`;
- environment location is 0;
- scope 0 is an empty module scope with the supplied builtins scope at -1;
- scope allocation starts at 1;
- the heap is empty and heap allocation starts at 0;
- call stack is empty, return state is `noRet`, exception is `NoExc`, and exit
  code is 0.

Every destination requires termination at `ref(0)`, the loaded exact closure in
scope 0, the result list at heap location 0, heap location advanced to 1, an
empty stack, no pending return/exception, and exit code 0. The result is not a
free variable: the heap value is explicitly constrained in every claim.

### Plain-language meaning of each entry claim

| Claim | Precondition and postcondition |
|---|---|
| `empty` | On exactly `[]`, return a fresh reference whose list is `[]`. |
| `prompt-example-one` | On exactly a three-element list containing an arbitrary K string, arbitrary K float, and arbitrary K integer, return exactly the integer. |
| `prompt-example-two` | On exactly six elements—three arbitrary K integers, an arbitrary K string, an empty K dictionary value, and an empty K list value—return the three integers in order. |
| `order-and-scalars` | On exactly five elements—an arbitrary K Boolean, integer `A`, `None`, arbitrary K string, and integer `C`—return exactly `[A, C]`. |

There are no helper claims, loop claims, invariants, or circularities. The
finite input lists are simply unrolled by symbolic execution. This makes the
four statements easy to interpret, but it also means there is no theorem for
an arbitrary list length or arbitrary element sequence.

### Exact program identity

The candidate encodes the submitted AST with four macros. I independently
parsed and macro-expanded both `solution.mpy` and the expression
`FILTER-PROGRAM` through the freshly built proof definition:

```text
kast solution.mpy ... --sort Module --expand-macros --output json
kast --expression FILTER-PROGRAM ... --sort Module --expand-macros --output json
cmp submitted-program.json claimed-program.json
```

Both expanded JSON terms have SHA-256
`3dc2d8774e7072b81947c64f97471edef855a1700e2628fadc4e862abb4a04cf`,
and `cmp` exited 0. See
[`evidence/stage4-program-macro-identity.log`](evidence/stage4-program-macro-identity.log).
The formal `<k>` cell therefore executes the actual submitted translated
program, not a substituted algorithm.

### Satisfying witnesses and concrete substitution

The reviewer-authored K harness
[`evidence/stage4_k_claim_witnesses.py`](evidence/stage4_k_claim_witnesses.py)
uses the submitted function body and supplies one ground witness for each
claim:

```text
[]
["a", 3.14, 5]
[1, 2, 3, "abc", {}, []]
[True, 7, None, "x", 9]
```

Trusted translation followed by `krun` exited 0 with `.K`, no exception, and
exit code 0. Its heap shows the last K result as `[7, 9]`. See
[`evidence/stage4-k-claim-witnesses.log`](evidence/stage4-k-claim-witnesses.log).

The last input satisfies `order-and-scalars` with
`B=true`, `A=7`, `S="x"`, and `C=9`. The independent Python substitution in
[`evidence/stage4_python_claim_witness.py`](evidence/stage4_python_claim_witness.py)
produces:

```text
formal_order_and_scalars_postcondition=[7, 9]
trusted_canonical_result=[True, 7, 9]
submitted_python_result=[True, 7, 9]
canonical_matches_formal=False
submitted_matches_formal=False
```

The exact run is in
[`evidence/stage4-python-claim-witness.log`](evidence/stage4-python-claim-witness.log).
This is a material false conclusion on the declared `List[Any]` domain.

### Adequacy decision

Program pinning and result constraint pass. Intent adequacy fails materially:

- no claim quantifies over an arbitrary `ValSeq` and relates the result to a
  truthful filter function;
- lengths other than 0, 3, 5, and one particular 6-element layout are not
  covered;
- most mixtures of supported values are not covered; and
- one of the four submitted theorems explicitly gives the wrong result for the
  corresponding real Python input.

This is not an acceptable “thin differential coverage” concern. A false
result is formally provable for a satisfying intended-domain input.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory generator is
[`evidence/stage5_k_inventory.py`](evidence/stage5_k_inventory.py). Its complete
one-entry-per-declaration/rule output is
[`evidence/stage5-rule-inventory.log`](evidence/stage5-rule-inventory.log).
It inventories `reference-semantics/semantics.k`, every supplied helper K file,
`verification.k`, and the four specification claims:

| Kind | Count |
|---|---:|
| configuration | 1 |
| syntax declarations | 231 |
| evaluation contexts | 5 |
| rules | 699 |
| claims | 4 |
| total | 940 |

The inventory explicitly classifies functions, total declarations, opaque
symbols, concrete rules, priorities, `owise` cases, macros, and operational
rules. There are no local `[simplification]` rules. The exact module/import
graph, all function/total/opaque declarations, and every
priority/`owise`/`concrete` occurrence are in
[`evidence/stage5-module-graph.log`](evidence/stage5-module-graph.log).

All fixed-semantics declarations and rules were screened for task-specific
answer encoding, unguarded result fabrication, overlap relevant to this
program, and active opaque values. Except for the documented Python-model gap,
the rules are constructor-recursive equations or ordinary operational steps of
the fixed semantics. Forty-eight concrete-only equations/rules are absent from
or inactive in the proof run. Twenty-five opaque declarations are listed
individually in the inventory; none is invoked by the four submitted claims.

### Proof-local inventory

`verification.k` contributes exactly:

- four `[macro]` syntax declarations:
  `FILTER-LOOP-BODY`, `FILTER-FUNCTION-BODY`, `FILTER-CLOSURE`, and
  `FILTER-PROGRAM`; and
- four macro expansion rules.

It contributes no function, total/functional declaration, opaque symbol,
priority rule, simplification, ordinary semantic rewrite, operational bridge,
or auxiliary reachability claim. The macro-expanded whole program is
byte-identical as JSON KAST to `solution.mpy`, as shown in Stage 4. The macros
therefore name syntax without bypassing execution or encoding the output.

### Mapping of every used syntactic construct

The exact declarations and active source excerpts are preserved in
[`evidence/stage5-active-slice.log`](evidence/stage5-active-slice.log).

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, statement list | `syntax.k:56-61`; `core.k:124-127` loads and sequences each real statement. |
| `ImportFrom("typing", ...)` | `syntax.k:43`; `controls.k:35-44` makes unsupported imports a no-op. This is harmless here because annotations were erased by the trusted translator. |
| `FuncDef`, `Params` | `syntax.k:53-60`; `functions.k:14-16` installs the exact body as a closure. |
| `Name` | `syntax.k:12`; `core.k:129-154` performs current-to-parent lookup, reaching real builtins. |
| docstring `Expr(Str(...))` | `syntax.k:13,52`; `str.k:13-17` creates a string value and `controls.k:48` discards the expression value. |
| `Assign(Name, ListExpr())` | strict RHS at `syntax.k:41`; `list.k:13-15` evaluates left-to-right and allocates; `controls.k:9-18` binds the resulting reference. |
| `For(Name, Name, body)` | strict iterable at `syntax.k:45`; `controls.k:69-74`, `list.k:9-10`, and `tuple.k:31-41` iterate the supplied list snapshot and bind each real element in order. |
| `If` | strict condition at `syntax.k:49`; `controls.k:52-54` dispatches on `truthy`. |
| `Call` | `syntax.k:28`; `call.k:20-32`, `core.k:183-191`, and `call.k:69-74` evaluate callee and arguments left-to-right, push the real function frame, and dispatch calls. |
| `isinstance(value, int)` | the builtins binding is in `core.k:157-181`; `builtins.k:291-295` routes to `isIntV`. |
| `Attribute(..., "append")` | strict receiver at `syntax.k:29`; `call.k:16,23-24` creates/dispatches the bound method. |
| list `append` | `list.k:52-55` updates the addressed heap list in place and returns `noneV`. |
| `Return(Name("result"))` | strict return at `syntax.k:50`; `functions.k:78-90` records the actual value, restores the caller frame/environment, and resumes its exact continuation. |

The active rules preserve all observable cells relevant here: module/function
bindings in `<scopes>`, result allocation and append mutations in `<heap>`,
monotone `<heapLoc>`, call allocation/restoration in `<env>`, `<scopeLoc>`, and
`<stack>`, returned reference in `<ret>`/`<k>`, and exception/exit state. No
active rule silently omits an output, exception, or mutation that the submitted
program can produce on these claim shapes.

### The material model-gap rule and false-conclusion witness

The relevant fixed rules are:

```text
builtins.k:291
  applyBuiltin("isinstance", V, typeV("int"), .Vals) => isIntV(V)
builtins.k:294
  isIntV(_:Int) => true
builtins.k:295
  isIntV(_:Val) => false [owise]
```

Within K's disjoint `Bool` and `Int` constructors, these rules are
deterministic and non-overlapping. They are not a candidate-added inconsistent
axiom. They nevertheless fail the required bridge to the behavior of the real
Python program.

Concrete false-conclusion witness:

- satisfying intended input: `[True, 7, None, "x", 9]`;
- the K `Bool` reaches the `owise` rule at `builtins.k:295`, so the proof and
  concrete K run exclude it and conclude `[7, 9]`;
- CPython evaluates `isinstance(True, int)` to true;
- both trusted canonical and submitted source return `[True, 7, 9]`.

This witness is reproduced dynamically in the Stage 4 logs. I therefore
classify the rule as a sound definition of the supplied miniature model but a
materially inadequate implementation of Python `isinstance` for the theorem
the candidate chose to state. No other rule is labeled unsound without a
witness.

## 6. Fresh non-vacuity test

The reviewer-created mutation is
[`evidence/spec-vacuity-review.k`](evidence/spec-vacuity-review.k). It retains
the satisfiable original `empty` precondition but changes the result-bearing
heap obligation from `list(.ValSeq)` to the demonstrably false
`list(vCons(1, .ValSeq))`.

First, the mutation was copied to scratch and built with:

```text
kprove spec-vacuity-review.k \
  --definition verification-kompiled \
  --spec-module FILTER-SPEC-VACUITY-REVIEW \
  --dry-run
```

This exited 0 and emitted a valid `kore-exec` proof command; see
[`evidence/stage6-mutation-build.log`](evidence/stage6-mutation-build.log).

The real proof command used the same arguments without `--dry-run`. It exited
1 with `WarnStuckClaimState`. The residual had `<k> ref(0) ~> .K </k>` and the
actual heap `0 |-> list(.ValSeq)`, which cannot unify with the mutated `[1]`
destination. This is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. See
[`evidence/stage6-mutation-proof.log`](evidence/stage6-mutation-proof.log).

The proof is therefore discriminating and result-constraining.

## 7. Proven versus assumed accounting

### What the successful K proofs establish

Conditional on K `v7.1.337`, its builtin theories, and the supplied semantics,
the freshly reconstructed reachability proofs establish termination and the
fully specified final configurations for the four exact input shapes restated
in Stage 4. They execute the exact submitted translated AST and include its
real function body, list allocation, finite loop iterations, `isinstance`
dispatch, conditional appends, return, and frame restoration.

They do **not** establish:

- filtering correctness for every Python `List[Any]`;
- a loop invariant or induction over arbitrary list length;
- equivalence between K `isIntV` and CPython `isinstance(_, int)`;
- correct retention of Boolean values or arbitrary `int` subclasses;
- a general summary function whose meaning is proven to be the requested
  filter; or
- universal equivalence between `solution.py` and the canonical implementation.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| Supplied `/reference/reference-semantics` | Defines all execution used by every claim. | Integrity is exact, but supplied status does not prove Python adequacy. Its Bool/Int distinction materially breaks one submitted claim's bridge to real Python. |
| K toolchain/backend and builtin `Int`, `Bool`, `Float`, `String`, `Map`, `List`, equality, arithmetic, parsing, and reachability engine | Compilation and closure of all claims. | Ordinary unavoidable machine-checking trust boundary; version and outputs recorded. |
| Trusted `/reference/py2mpy.py` | Bridges `solution.py` to `solution.mpy`. | Byte regeneration succeeds. Source inspection confirms the simple translated constructs; this is not a universal translator-correctness theorem. |
| `isIntV`/`isStrV`, ordinary builtin and method dispatch, iterator, allocation, frame, and collection rules | Active operational semantics. | Executed rather than replaced by proof-local bridges. `isIntV` is the documented material Python-model gap. |
| Opaque float symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF` | Trusted/opaque proof-level float operations in the fixed semantics. | None is invoked: the arbitrary float in one claim is only classified by `isIntV` and discarded. They cannot affect closure or the result. |
| Opaque `sortVS`, `sortKeyVS`, and `md5hexCodes` | Trusted sort/digest abstractions in unused language features. | Not syntactically or transitively used by this program or its claims. |
| Trusted canonical Python implementation | Independent executable oracle for source fidelity and ground claim substitution. | Authoritative for intended behavior; finite differential testing supports but does not prove universal source equivalence. |
| Reviewer differential tests | 11,621 source-versus-canonical cases. | Empirical evidence only. It establishes zero mismatches on the recorded corpus and exposes the Boolean expectation; it is not substituted for K proof. |
| Macro-to-program identity comparison | Connects `FILTER-PROGRAM` to `solution.mpy`. | Exact parsed/macro-expanded KAST identity, not an empirical behavior sample. |
| Informal intent bridge | Interprets prompt plus canonical as retaining exactly CPython `int` instances in order. | Directly supported by trusted source. The candidate's K Boolean theorem contradicts it. |

### Gate accounting and final decision

- Fresh verification gate: **pass** for all four submitted claims.
- Proof-local extension soundness/program identity: **pass**; there are only
  exact syntax macros, no operational bridge or oracle.
- Result constraint and non-vacuity: **pass**.
- Natural-language/Python adequacy: **fail materially** because a satisfying
  Boolean input proves the wrong result.
- Contract coverage: **fail materially** because no arbitrary-list property is
  claimed or proved.
- Evidence auditability: the reviewer evidence is reproducible; missing
  generation metadata is documented and does not explain away the two
  substantive failures.

The candidate contains genuine machine-checked facts about four configurations
of the supplied miniature semantics. It does not contain a legitimate
partial-correctness proof of the real generated Python program against the
stated contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
