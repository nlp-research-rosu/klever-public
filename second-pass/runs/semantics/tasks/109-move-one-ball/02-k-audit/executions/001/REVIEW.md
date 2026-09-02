# Independent adversarial audit: 109-move-one-ball

The candidate is **not a legitimate proof of the real generated program**. A
fresh build and all three positive reachability obligations do produce `#Top`,
and a fresh false-result mutation is correctly rejected. However,
`verification.k:53-56` installs a priority operational bridge that returns `1`
for the length of *every* nonempty encoded list under an arbitrary continuation.
For the intended unique input `[10, 20]`, the extended theory therefore proves
the false result `len([10, 20]) == 1` and the false observable comparison
`len([10, 20]) == 1` is true. The correct result `2` gets stuck after the bridge
has produced `1`. This is a concrete real-semantics unsoundness witness, not
merely missing evidence.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. This is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is present, so there
is no infrastructure breach and a candidate verdict is appropriate.

- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted `/reference` counterparts (`cmp` exit 0).
- The complete candidate `reference-semantics/` tree is recursively identical
  to `/reference/reference-semantics`; `diff -qr --no-dereference` exits 0 and
  all 24 per-file SHA-256 hashes agree.
- No candidate entry is a symlink. There are no missing, additional, mistyped,
  changed, or symlinked entries inside the supplied-semantics tree.
- The candidate contains the required proof sources `solution.py`,
  `solution.mpy`, `spec.k`, and `verification.k`. The additional
  `concrete-tests.*`, `prove.sh`, and `__pycache__` were treated only as
  untrusted candidate material.
- The requested provenance artifacts `run-input.json`, `metrics.json`,
  `codex-last.txt`, and `codex-output.log` are all missing. No structured
  generation trace, JSONL event file, or trace-named file is present. Their
  untrusted claims could therefore not be inspected. This is an auditability
  limitation, but not the reason for the proof verdict.

Evidence: [stage1-integrity.sh](evidence/stage1-integrity.sh) and
[stage1-integrity.log](evidence/stage1-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks whether a finite list of pairwise-distinct integers can
be made non-decreasing by any number of right cyclic shifts; the empty list
must return `True`.

The trusted canonical implementation rotates the list so that its minimum is
first and compares that rotation with `sorted(arr)`. The candidate instead
counts strict descents while scanning left-to-right and adds the wrap descent
from the last element back to the first, returning `drops < 2`.

For a nonempty distinct list, a sorted cyclic rotation has at most one circular
descent. Conversely, if there is at most one circular descent, cutting the
cycle after it produces a strictly increasing linear order; a right rotation
can make that order the list. A singleton has zero descents, and empty is
handled separately. The candidate algorithm therefore matches the natural
contract on its intended domain.

### Translation identity

Regenerating with the trusted translator produced byte identity:

```text
f7554210119c8a42792c645561475c851dcf773ef0d3b0d68a752a31dae6d6af
```

for both the regenerated and submitted `solution.mpy`; `cmp` exited 0.

### Independent differential run

The reviewer-authored script imports `/reference/canonical.py` independently
from the scratch copy of `solution.py`. It covers:

- both documented examples;
- empty, singleton, two-element, inner-descent, wrap-descent, and the
  `drops == 1`/`drops == 2` return boundary;
- all permutations of fixed distinct integer sets for lengths 0 through 8;
- 5,000 deterministic random distinct-integer lists of lengths 0 through 32
  with seed `1092026`;
- eight supplemental duplicate cases, explicitly outside the promised domain.

There were 51,246 intended-domain comparisons and zero mismatches. Two of the
eight supplemental duplicate cases differ from the canonical implementation:
`[1,2,1]` and `[1,2,2,1]`. The prompt guarantees unique elements, so those are
not implementation defects; they remain visible in the log.

Evidence:
[stage2-fidelity.log](evidence/stage2-fidelity.log),
[differential.py](evidence/differential.py), and the complete
[differential-inputs.jsonl](evidence/differential-inputs.jsonl), whose SHA-256
is `7655a16803898a3cb2aeaab0ee0c524623dc20628de29a11221b1d0d16a0d7c0`.

## 3. Clean proof reconstruction

All candidate artifacts needed for execution were copied to
`/tmp/audit-work/109-move-one-ball`; no candidate compiled definition or cache
was copied or reused. The scratch tree initially contained no `*-kompiled`
directory. K was independently available as version `v7.1.337`.

Fresh source builds succeeded:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
exit 0

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
exit 0
```

The compiler reported baseline non-exhaustive-match warnings for `mapStrVS`,
several float helpers, `joinCodes`, and `valSeqAt`, plus unused variables in
`strLt`. These warnings are preserved in the build log and considered in stage
5; none is an infrastructure failure.

Every positive claim closed in a fresh invocation with its required dependency
set:

| Target | Claims retained | Result |
|---|---|---|
| Loop induction | `SPEC.move-one-ball-loop-induction` | `#Top`, exit 0 |
| Loop entry | induction + `SPEC.move-one-ball-loop-entry` | `#Top`, exit 0 |
| Entry correctness | both loop claims + `SPEC.move-one-ball-correct` | `#Top`, exit 0 |

The loop-entry and entry-correctness runs retain the earlier circularities on
which they depend; removing those dependencies would not be an independent run
of the stated proof.

Evidence:
[stage3-rebuild.sh](evidence/stage3-rebuild.sh),
[stage3-rebuild.log](evidence/stage3-rebuild.log),
[stage3-prove.sh](evidence/stage3-prove.sh), and
[stage3-prove-final.log](evidence/stage3-prove-final.log).

These results establish closure under the candidate-extended theory. They do
not establish that the extensions are faithful; that is the failed stage-5
gate.

## 4. Adequacy and real-program pinning

### Claims in plain language and satisfiable witnesses

1. `move-one-ball-loop-induction` starts at a nonempty `#loop` after the local
   name `current` already exists. It consumes the encoded remainder, preserves
   `arr` and `first`, changes `drops` to `scanDrops`, and leaves both
   `previous` and `current` equal to the last scanned item. A concrete
   satisfying state is `C=2`, `IS=.IntSeq`, `D=0`, `F=2`, `P=2`,
   `_OLD=99`, `KONT=.K`, `BUILTINS=builtinsScope`,
   `MODSCOPE=scope(.Map,parent(-1))`, and any well-sorted `ARR:Val`.

2. `move-one-ball-loop-entry` states the same nonempty loop summary before
   `current` exists. Its first fixed semantic iteration creates the name and
   then the induction circularity applies. The preceding witness with the
   `current` binding omitted satisfies this claim.

3. `move-one-ball-correct` starts in an otherwise fresh module configuration
   whose `move_one_ball` binding is the candidate closure. For every
   `IS:IntSeq`, it says a call on `list(intVals(IS))` returns
   `moveOneBallSpec(intVals(IS))`: true for empty, otherwise circular strict
   descents less than two. `IS=.IntSeq` is an immediate satisfying entry
   witness; the two documented lists are nonempty witnesses.

The entry postcondition is result-constraining. It is neither a free variable,
tautology, nor one-way implication.

### Program and concrete substitutions

`MOVE-ONE-BALL-BODY` is an exact constructor-for-constructor transcription of
the byte-verified `solution.mpy` function body, and the closure has the same
single parameter and definition scope as fixed `FuncDef` loading. A fresh
full-module LLVM run, generated from the actual scratch `solution.py` with the
trusted translator and ten reviewer assertions, ended with `.K`, `NoExc`, and
exit-code 0. Thus the manual closure body itself is not a substituted
algorithm.

For `[]`, `[3,4,5,1,2]`, and `[3,5,4,1,2]`, candidate Python, canonical Python,
and fresh K ground claims all return `True`, `True`, and `False`. The K ground
artifact checks both the proof-local `intVals` encoding and, for the two
documented nonempty examples, the supplied semantics' real
`vCons` representation.

Evidence:
[auditor-concrete.py](evidence/auditor-concrete.py),
[stage4-concrete-k.log](evidence/stage4-concrete-k.log),
[spec-ground-adequacy.k](evidence/spec-ground-adequacy.k), and
[stage4-ground.log](evidence/stage4-ground.log).

### Material pinning gap

The universal entry theorem does **not** quantify over real fixed-semantics
`list(vCons(...))` values. It quantifies over the fresh constructor
`list(intVals(IS))`, which the supplied semantics cannot produce and does not
interpret. Candidate operational bridges give that fresh representation
iteration, length, and index-zero behavior. No bridge-free reachability claim
connects actual `vCons` lists to this representation. The finite real-list
ground checks support examples only; they do not supply the missing universal
connection.

This gap becomes decisively illegitimate because one of those representation
bridges is observably false, as stage 5 demonstrates.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated inventory contains every top-level configuration,
syntax declaration, context, rule, and claim in the supplied tree,
`verification.k`, and `spec.k`: 1 configuration, 236 syntax declarations, 5
contexts, 717 rules, and 3 claims, for 962 entries total.

The 928 supplied-semantics entries are byte-identical to the trusted fixed
baseline. They were classified as the selected operational semantics rather
than candidate proof extensions. The relevant target path was checked through
syntax strictness; sequencing and lookup; closure calls, binding, returns, and
frame restoration; assignment; branching; iteration; integer operations;
length; and index-zero access. Unused opaque supplied primitives and the
compiler coverage warnings are listed in the detailed decision record.

Every proof-local entry 929-959 and claim 960-962 has an individual
classification and decision in
[proof-local-rule-review.md](evidence/proof-local-rule-review.md). The complete
machine-generated inventory is
[k-rule-inventory.md](evidence/k-rule-inventory.md), SHA-256
`1779d1be615a760803d884f7642fe69de54b1d18c65f8e3c9c35ba8884ba9e7c`.

### Construct-to-rule mapping

| Submitted construct | Selected rules |
|---|---|
| `Module` / function body | `core.k:124-127`; exact proof-local body/closure definitions at `verification.k:9-32` |
| `Call` / `Name` / return | `core.k:130-191`, `call.k:19-32,69-94`, `functions.k:63-90` |
| literals and comparisons | `core.k:193-205`, `operators.k:10-17`, `int.k:22-27`, `bool.k:10-11` |
| `Assign` / `AugAssign` / `If` | `controls.k:9-31,51-54` |
| `For` | `controls.k:62-74`; proof-local encoded iterator rules at `verification.k:43-47` |
| `len(arr)` | fixed `builtins.k:20-26`, preempted for encoded inputs by `verification.k:49-56` |
| `arr[0]` | fixed `subscript.k:27-41`, preempted for encoded inputs by `verification.k:60-62` |
| mathematical summary | `verification.k:67-97` |

The fold equations `addDrop`, `scanDrops`, `scanLast`, `circularDrops`, and
`moveOneBallSpec` are terminating and truthful on the integer domain used by
the claims. Their constructor cases are disjoint. There are no proof-local
simplification rules, `[functional]` declarations, or opaque result oracles.

### Unsound operational bridge and required false witness

The critical rule is:

```k
rule <k> #applyK(toCall(builtinV("len")),
                 (list(intVals(iCons(_I:Int, _IS:IntSeq))), .Vals))
      => 1 ... </k>
     [priority(40)]
```

Classification: operational bridge. It preempts fixed builtin dispatch, reads
no cells, writes no cells, and replaces the returned value. Its complete match
domain is every nonempty `intVals` sequence under any continuation and any
framed configuration admitted by `...`. The candidate justifies only the
particular later comparison with zero, but the rule is not restricted to that
continuation. Priority changes which behavior executes; it does not prove
equivalence.

There is no bridge-free universal connection theorem. The only claims are the
two loop summaries and main theorem, and they all import the bridge itself.

Concrete false-conclusion witness on the intended unique-integer domain:

- Python: `len([10,20])` is `2`, and `len([10,20]) == 1` is `False`.
- Fresh K with the supplied real `vCons` list proves length `2`.
- The candidate-extended theory proves `#Top` for length `1` on the documented
  corresponding `intVals(iCons(10,iCons(20,.IntSeq)))`.
- An observable comparison continuation immediately after the call also proves
  `#Top` for the false result `len(...) == 1 => true`.
- The opposite expected result, length `2` on that encoded list, exits 1 with
  `WarnStuckClaimState`; the residual `<k>` cell is exactly `1`.

Evidence:
[spec-len-bridge-witness.k](evidence/spec-len-bridge-witness.k),
[spec-len-bridge-opposite.k](evidence/spec-len-bridge-opposite.k), and
[stage5-len-bridge-final.log](evidence/stage5-len-bridge-final.log).

This witness satisfies the required standard for labeling a rule unsound. The
rule happens to preserve the submitted program's immediate `== 0` branch, but
globally false proof rules cannot be justified by saying the bad continuations
were not intended. The universal main proof depends on this bridge to decide
the nonempty branch, so its `#Top` is not a usable real-program proof state.

The other `intVals` iterator, empty-length, and index-zero rules are
mathematically consistent with the intended representation, but they likewise
lack a bridge-free theorem relating that fresh representation to actual fixed
lists. No false conclusion is asserted for those rules beyond the narrower
connection gap.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. The auditor created a fresh ground
mutation for the satisfiable entry input `[]`, changing the required result
from the actual `true` to `false`.

- Candidate Python confirms `move_one_ball([])` is `True`.
- `kprove --dry-run` on the mutation exits 0, establishing that it parses and
  builds against the fresh definition.
- The real proof attempt exits 1 with `WarnStuckClaimState`; its residual
  `<k>` cell is `true`, which cannot unify with destination `false`.

This is a meaningful, reachable unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. Non-vacuity therefore passes.

Evidence:
[spec-vacuity-auditor.k](evidence/spec-vacuity-auditor.k),
[stage6-nonvacuity.sh](evidence/stage6-nonvacuity.sh), and
[stage6-nonvacuity.log](evidence/stage6-nonvacuity.log).

Passing non-vacuity shows that the extended theorem distinguishes return
values. It does not validate the semantics used to obtain those values.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the supplied semantics **plus all rules in `verification.k`**, a direct
call of the exact closure body on the fresh abstract value
`list(intVals(IS))` reaches the pure predicate that counts circular strict
descents and tests whether the count is less than two. The two loop claims
establish the associated fold summaries under that same extended theory.

It does not establish a universal theorem for the supplied semantics' actual
`vCons` lists, and it does not establish real Python execution because the
extended theory gives at least one used operation an observably false result.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.337`, Haskell reachability backend, and K integer/Boolean/map/list primitives | All reconstructed claims | Ordinary machine-checking trust boundary; acceptable and explicitly identified. |
| Byte-identical supplied K semantics | Program execution | Required fixed baseline for this mode; acceptable as selected semantics. Unused opaque float/sort/MD5 primitives do not affect this proof. |
| Manual body/closure transcription | Main claim | Exact by static constructor comparison, byte-identical translation, and full-module concrete execution; acceptable evidence for this body. |
| `intVals` as representing every finite integer list | All three claims | Program-derived abstraction with no bridge-free universal connection to actual `vCons` values; concerning and materially unproved. |
| Nonempty `len` bridge returns `1` | Main claim's nonempty branch | Illegitimate. The bridge is false on `[10,20]`, admits arbitrary continuations, and is directly used by the proof. |
| Iterator/empty-length/index-zero bridges for `intVals` | Loop claims and main claim | Structurally truthful under the intended encoding, but supported only by inspection and finite ground behavior, not the required connection theorem. |
| `addDrop`/scan/circular summary equations | Loop and final postcondition | Ordinary terminating integer mathematics; acceptable on the formal integer domain. |
| Circular-descents criterion equals the right-rotation contract for unique lists | Natural-language intent | Informal mathematical bridge, supported by the argument in stage 2 and zero intended-domain differential mismatches; not itself formalized in K. |
| Differential and concrete tests | Python equivalence and finite semantics behavior | Reproducible finite evidence only; not used as a substitute for the K theorem or missing universal bridge. |

Gate accounting:

- Fresh verification closure: pass (`#Top`, exit 0 for every target with its
  dependencies).
- Real-program soundness: **fail**, due to the witnessed false nonempty-`len`
  operational bridge and the missing actual-list connection.
- Intent alignment of the Python algorithm: supported on the promised unique
  domain.
- Non-vacuity: pass.
- Evidence auditability: limited by the missing generation/provenance bundle,
  but reviewer evidence is reproducible.

Because real-program soundness fails with a concrete false conclusion witness,
the successful `#Top` results cannot qualify as a legitimate
partial-correctness proof. Correct implementation behavior and passing
differential tests do not repair an unsound proof theory.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
