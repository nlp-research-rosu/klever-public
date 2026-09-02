# Independent adversarial review: HumanEval/8 `sum_product`

## Executive conclusion

The candidate's two positive proof commands reconstruct from clean source and
both print `#Top`. The postcondition is non-vacuous, the executed module macro
is constructor-identical to trusted regeneration of `solution.py`, and the
staged loop-summary rule is independently derivable over its complete match
domain.

The proof is nevertheless not a legitimate proof for the real supplied-semantics
input domain. Its entry claim calls the real function body on
`list(intVals(IS))`, where `intVals` is a new, opaque proof-local `ValSeq`
constructor. Real lists in the supplied semantics contain `.ValSeq`/`vCons`
sequences. There is no equation, macro, relation, or bridge-free connection
theorem connecting these representations. The two proof-local `#iterNext`
rules make the opaque constructor iterate and thereby determine the returned
sum and product. Removing only those rules leaves even the ground one-element
iteration stuck. Thus the successful proof establishes a theorem about an
extended surrogate input representation, not about the ordinary `list[int]`
values covered by the source contract.

This is a real-program/domain-pinning failure, not an infrastructure failure and
not a claim that the candidate's arithmetic equations are mathematically false.

The complete bounded command record is
[`evidence/commands.log`](/audit-output/evidence/commands.log), and the static
inventory is
[`evidence/rule_inventory_summary.md`](/audit-output/evidence/rule_inventory_summary.md).

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `8-sum-product`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` is present. All required launcher records for
the declared layout are present, readable regular files/directories, and no
required candidate, reference, or generation-evidence entry is a symlink.
Historical `runtime-metrics.json` is absent but is expressly not required for
this legacy layout; `usage.json` is present and was inspected.

I read `/run.json`, `/task.json`, `/generation-result.json`, all required
generation records, the 24,359-line `codex-output.log`, the prompt, and the
structured trace. The trace is valid JSONL for all 475 lines and contains 109
recorded execution calls and matching outputs. These generation records were
treated only as untrusted historical claims.

### Campaign and hashes

The parsed object in `/audit-campaign-lock.json` exactly equals the
`audit_campaign` object in `/audit-input.json`. Its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

Independent SHA-256 checks match the recorded values for the campaign lock,
canonical implementation, trusted/candidate prompt, trusted/candidate
translator, run/task/result records, invocation, metrics, usage, prompt,
Codex output/last message, and the sole trace JSONL file. Exact values are in
[`commands.log`](/audit-output/evidence/commands.log).

Recursive, no-dereference comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` exits 0. The file inventory is identical and
contains only regular directories/files. Candidate `prompt.py` and `py2mpy.py`
are byte-identical to their trusted mounts. This satisfies the supplied
semantics integrity condition; it does not bless `verification.k`.

No infrastructure-breach stop condition was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires, for any finite Python `List[int]`, a pair:

1. the sum of every element, with empty identity `0`; and
2. the product of every element, with empty identity `1`.

The domain has no size or magnitude bound. The trusted canonical program uses
the direct accumulator loop.

Candidate `solution.py` implements the same algorithm with renamed locals. Its
extra initialization `number = 0` affects only the loop-target local and cannot
change the returned `total` or `product`. It preserves arbitrary-precision
Python integer behavior and handles the empty list correctly.

### Trusted translation

From the isolated scratch tree, this command exits 0:

```text
python3 trusted/py2mpy.py work/solution.py | cmp -s - work/solution.mpy
```

Thus trusted regeneration is byte-identical to the submitted `solution.mpy`.

### Independent differential testing

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports the
trusted canonical entry point and the scratch candidate entry point independently.
It tests:

- 13 explicit examples/boundaries, including empty, one iteration, zero at
  different positions, sign changes, and very large integers;
- all 19,608 lists of lengths 0 through 5 over `[-3, 3]`;
- 2,000 deterministic generated lists, lengths 0 through 50, with signed
  integers up to 40 decimal digits.

The command exits 0 with `total_cases=21621` and `mismatches=0`. This strongly
supports implementation fidelity, but it is finite evidence and not the K
proof.

## 3. Clean proof reconstruction

I copied source artifacts only into
`/tmp/audit-work/8-sum-product-audit-002`; no candidate-compiled definition or
cache was copied or reused.

### Concrete definition

Fresh LLVM compilation of the supplied source semantics exits 0:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

`krun solution.mpy` terminates with `.K`, `NoExc`, and exit code 0.
`krun concrete-tests.mpy` likewise terminates cleanly, so all four candidate
assertion cases pass. Compiler warnings concern broad, unused supplied helper
functions and unused variables in `strLt`; none is a build error.

### Positive proof targets

Fresh Haskell compilation and the auxiliary proof:

```text
kompile verification.k --backend haskell \
  --main-module SUM-PRODUCT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled \
  --spec-module SUM-PRODUCT-LOOP-SPEC --output pretty
```

Both exit 0; `kprove` prints `#Top`.

Fresh compilation with the staged rule and the entry proof:

```text
kompile verification.k --backend haskell \
  --main-module SUM-PRODUCT-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemma-kompiled

kprove spec.k --definition verification-lemma-kompiled \
  --spec-module SUM-PRODUCT-FUNCTION-SPEC --output pretty
```

Both exit 0; `kprove` prints `#Top`.

Fresh dynamic reconstruction therefore passes. It proves closure under the
candidate's extended theory; stages 4 and 5 determine why that is not yet the
requested theorem.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop-correct` starts with:

- environment location 1;
- the fixed builtins scope, a global scope, and one local scope;
- arbitrary integer accumulators `SUM`, `PRODUCT`, and current loop target;
- arbitrary continuation `CONT`;
- a loop over `list(intVals(IS))`, for arbitrary finite `IntSeq IS`.

It says the loop reaches `CONT`, replacing the two accumulators with left-folded
integer sum/product and setting `number` to the final element (or preserving
the old value for an empty sequence).

`function-correct` starts from the clean module configuration, loads
`sumProductModule`, and calls its `sum_product` binding on
`list(intVals(IS))`. It says the returned value is exactly:

```text
(intSeqSumFrom(0, IS), intSeqProductFrom(1, IS))
```

It also pins the final module binding and all configuration cells. This is an
exact equality-style reachability destination, not a free result, tautology, or
one-way implication.

### Satisfiable witnesses

The formal preconditions are satisfiable in the extended syntax. For example,
`IS = .IntSeq` makes the formal result `(0, 1)`, while
`IS = iCons(2, iCons(-3, iCons(4, .IntSeq)))` makes it `(3, -24)`.
[`claim_witnesses.py`](/audit-output/evidence/claim_witnesses.py) confirms these
and two other ground folds agree with both Python implementations.

That comparison checks the arithmetic summary. It does not establish that the
K input term is an ordinary supplied-semantics list.

### Program-body identity

The three macros in `verification.k` transcribe the translated loop body,
function body, and module. Parsing trusted-regenerated `solution.mpy` and
parsing `sumProductModule` with macro expansion yield identical KORE streams
with SHA-256
`f2c97a7dc3701b9a386906e93ea121072f6f9f2d82dc7b8862f65b9a08312039`.

A body-sensitivity mutation changes the multiplication statement in the macro
actually executed by both claims to addition. The mutant definition compiles,
but the loop proof exits 1 with the expected unmet obligation:

```text
intSeqProductFrom(PRODUCT +Int I, IS0)
  = intSeqProductFrom(PRODUCT *Int I, IS0)
```

The candidate theorem is therefore sensitive to and pins the submitted
function body.

### Fatal input-representation mismatch

The supplied list representation is:

```text
list(.ValSeq)
list(vCons(V, REST))
```

The entry claim instead uses:

```text
list(intVals(IS))
```

`intVals` is neither a macro nor a function with equations to `.ValSeq` and
`vCons`. KORE inspection of the one-element terms gives different constructor
trees:

- real list term hash:
  `0bd0abe7a0cd72fbe2cedcc045a1b8f200ae8b90f5eee8e2423e5ebdc2c94e2c`;
- claimed `intVals` term hash:
  `11010c62ec13c3f0178bfdea83f680c53d819ac40e87c6a66227744b0a1634c0`.

The roots are respectively the supplied `vCons` symbol and the proof-local
`intVals` symbol. They do not unify and are not equated anywhere. Consequently
no ordinary real-list state is an instance of the entry claim's input term.
The unrestricted `IntSeq` parameter covers all lengths and integer magnitudes,
but only inside a substituted semantic representation.

This is material: iteration is the operation that computes both requested
results, and the fixed list iterator does not execute on `intVals`.

## 5. Rule-by-rule static soundness review

### Inventory

[`inventory_rule_heads.sh`](/audit-output/evidence/inventory_rule_heads.sh)
reproduces an exact source-location inventory of all declarations, rules,
contexts, attributes, and claims. The reviewed sources contain:

- 234 syntax-declaration heads;
- 707 rule heads;
- five explicit evaluation contexts;
- one configuration;
- two reachability claims.

The per-file exhaustive disposition is in
[`rule_inventory_summary.md`](/audit-output/evidence/rule_inventory_summary.md).
There are no local `functional`, `simplification`, or `anywhere` declarations.
The fixed proof definition imports `MPY`, not LLVM-only `MPY-CONCRETE`.

All fixed-semantics modules were reviewed. Rules in unused modules are inert
because no target constructor reaches them. Fixed opaque primitives are the
float family, sorting summaries, and MD5 summary; none occurs on either target
path and none affects the result.

### Used fixed-semantics path

Every construct in `solution.mpy` maps as follows:

| Program construct | Declaration/rules |
|---|---|
| `Module`, statement lists | `syntax.k`; `core.k` `#loadAll` and sequencing |
| `ImportFrom("typing", ...)` | `syntax.k`; `controls.k` non-math no-op |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` closure creation |
| `Call`, parameter | `syntax.k`; `call.k` callee/argument/closure frame; `functions.k` `#bindP` |
| docstring `Expr(Str(...))` | `syntax.k`; `str.k` ASCII literal; `controls.k` expression discard |
| `Assign`, `Name`, `Int` | `syntax.k`; `controls.k` scope update; `core.k` lookup/literal |
| `For` and loop target | `syntax.k`; `controls.k` loop protocol; `tuple.k` `#bindTgt` |
| `AugAssign +/*` | `syntax.k`; `controls.k` scope update; `int.k` exact `+Int`/`*Int` |
| `Return(TupleExpr(...))` | `syntax.k`; `tuple.k` left-to-right tuple construction; `functions.k` return/pop |

The fixed path preserves left-to-right evaluation, the current environment,
local scope updates, the arbitrary continuation, frame allocation/pop, return
state, heap, exception, and exit-code cells. Integer arithmetic uses
mathematical K integers, matching Python arbitrary-precision integers for this
program.

### Candidate-local extension inventory

1. `sumProductLoopBody`, `sumProductBody`, and `sumProductModule` are macro
   syntax plus three macro equations. They are definitional program
   abbreviations, and mechanical expansion proves exact identity.
2. `intVals(IntSeq)` is a fresh opaque `ValSeq` constructor. It has no defining
   equation or relation to fixed list sequences.
3. Two ordinary `<k>` rewrites turn
   `#iterNext(list(intVals(.IntSeq)))` into `#iterDone`, and the `iCons` case
   into `#iterYield`. These are result-bearing operational bridges.
4. `intSeqSumFrom`, `intSeqProductFrom`, and `lastInt` are three `[function,
   total]` declarations with six equations. Empty/cons guards are
   constructor-disjoint, recursion strictly descends on `IntSeq`, coverage is
   exhaustive, and the equations are ordinary mathematics.
5. The priority-40 staged loop rule summarizes the loop and preserves its
   arbitrary continuation and `REST` scope map.

The staged loop rule initially appears broader than the candidate's separately
proved claim because its scope map has arbitrary `REST`. I therefore proved
[`lemma-scope-probe.k`](/audit-output/evidence/lemma-scope-probe.k), which is
the exact rule domain, without importing `SUM-PRODUCT-LEMMA`. It exits 0 and
prints `#Top`. Thus that rule is sound relative to the already extended
`intVals` theory; it reads `<k>`, `<env>`, and the two named scopes, updates
only `total`, `product`, and `number`, preserves `REST`, and returns to the
same arbitrary `CONT`.

### `intVals` operational bridge failure

The bridge's two cases are non-overlapping and describe the intended integer
sequence informally. The problem is not a demonstrated false arithmetic
equation. The problem is the absence of the required fixed-semantics
connection:

- The bridge's value determines each yielded loop element.
- Those elements determine both accumulators and the final tuple.
- The same `IS` is consumed by the proof-side folds in the destination.
- No bridge-free theorem states that fixed execution on an actual
  `.ValSeq`/`vCons` list produces this sequence of values.

[`bridge-free.k`](/audit-output/evidence/bridge-free.k) adds only the
`intVals` syntax constructor to fixed `MPY`, omitting the proposed operational
rules. Its ground one-element claim:

```text
#iterNext(list(intVals(iCons(2, .IntSeq))))
  => #iterYield(2, list(intVals(.IntSeq)))
```

builds successfully but exits 1 with `WarnStuckClaimState`; the exact
`#iterNext` term cannot rewrite. This is the required fixed-versus-extended
control/result witness. The extension fabricates iteration behavior for a term
outside the supplied representation, and the final theorem depends on that
fabrication.

I do not label the two constructor-case equations mathematically false, so
there is no invented “false conclusion” witness. The narrower, evidenced defect
is that they are unconnected operational axioms on a surrogate input and hence
cannot transfer the theorem to real list values. The KORE constructor mismatch
is a direct witness that the entry precondition excludes those values.

### Gate findings

- Real-program soundness gate: **FAIL**. The body is exact, but the
  result-bearing input/iteration bridge has no bridge-free universal
  connection to fixed list execution.
- Intent adequacy gate: **FAIL**. The theorem does not range over the actual
  supplied-semantics representation of the source-contract `List[int]`
  domain. This is not a finite-size restriction, but it is still a material
  domain substitution.
- Evidence/auditability gate: finite Python differential evidence is good and
  all auditor commands are reproducible, but testing cannot discharge the
  missing universal K connection.

## 6. Fresh non-vacuity test

The reviewer-authored
[`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k) changes the entry
postcondition's first tuple component from:

```text
intSeqSumFrom(0, IS)
```

to:

```text
intSeqSumFrom(0, IS) +Int 1
```

`IS = .IntSeq` is a satisfying witness: the actual formal result is `(0, 1)`,
while the mutation demands `(1, 1)`.

The mutation dry-run exits 0, establishing successful parsing/build against the
fresh definition. The actual proof exits 1 with `WarnStuckClaimState`. Its
residual contains the returned unmutated tuple and precisely the unmet
condition:

```text
intSeqSumFrom(0, IS) +Int 1
  = intSeqSumFrom(0, IS)
```

This is meaningful non-vacuity evidence: the result is constrained and the
entry claim is reachable. It does not validate the representation bridge.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under supplied `MPY` plus the candidate extensions, for every finite `IntSeq
IS`, if the extended execution of the exact submitted function terminates on
the synthetic value `list(intVals(IS))`, it returns the left-folded K-integer
sum and product. The loop invariant also establishes the exact accumulator and
loop-target updates for arbitrary initial accumulators and continuation.

### Trusted or assumed boundaries

| Boundary | Effect | Assessment |
|---|---|---|
| K prover/backend and K mathematical integers | Reachability engine and exact arithmetic | Ordinary accepted toolchain trust. |
| Supplied `MPY` semantics | Module loading, closures, scopes, calls, loop control, tuples, integer operations | Required fixed semantics; candidate copy is byte-identical. |
| Trusted `py2mpy.py` | Source-to-constructor translation | Byte identity independently checked. |
| Three program macros | The term executed by the claims | Machine-compared to trusted regeneration; acceptable. |
| Three fold functions | Result summaries | Exhaustive, disjoint, descending mathematical definitions; acceptable. |
| Staged loop rule | Accelerates the proven loop under arbitrary continuation/REST | Exact bridge-free scope theorem independently prints `#Top`; acceptable relative to the base extended theory. |
| `intVals` plus two iterator rules | Supplies every input element that drives the result | Illegitimate for the target theorem: no actual-list representation equation or universal fixed-semantics connection. |
| Python differential test | Candidate implementation versus canonical on 21,621 inputs | Strong finite fidelity evidence only; cannot transfer the K theorem. |
| Partial correctness | Says nothing if execution does not terminate | Standard theorem mode; not the cause of failure. |

No fixed float, sort, MD5, or other opaque primitive influences this theorem.

### Verdict rationale

The positive `#Top` results and successful non-vacuity test are genuine facts
about the extended theory. They cannot establish the requested HumanEval
contract because the entry claim's list is a distinct proof-local constructor
whose material iteration behavior is axiomatized only for the proof. Repair
would require a definitional expansion to real `.ValSeq`/`vCons` values, or a
bridge-free universal connection theorem that relates the complete real-list
execution to the abstraction before using it in the entry proof.

Under the benchmark decision boundary, proving a substituted semantic input
instead of the full real source-contract domain is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
