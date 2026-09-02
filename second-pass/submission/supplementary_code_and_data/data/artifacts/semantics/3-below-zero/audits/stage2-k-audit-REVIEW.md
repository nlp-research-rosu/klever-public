# Independent adversarial review: HumanEval/3 `below_zero`

This review treats every candidate artifact and generation record as untrusted
evidence. I rebuilt from source in `/tmp/audit-work/reconstruction` using K
7.1.293 and wrote reviewer artifacts and bounded logs under
`/audit-output/evidence`.

## 1. Input and provenance integrity

The launcher declares `record_layout=legacy-selected-stage1`,
`condition=semantics`, and `semantics_mode=SUPPLIED_SEMANTICS`. The supplied
semantics boundary is internally consistent: `/reference/reference-semantics`
exists, as required for this mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all records required for the declared
legacy-selected layout, optional `usage.json`, both generation text logs, the
generation prompt, and every JSONL event in the structured trace. The trace has
one 552-line file. Historical `runtime-metrics.json` is absent, but that record
is not required for `legacy-selected-stage1` and was not reconstructed.

Independent checks found:

- the campaign-lock object exactly equals the `audit_campaign` block;
- its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value;
- all launcher-declared mounts and all records required for this layout are
  present, readable, regular directories/files as appropriate, and not
  symlinks;
- the recorded hashes for the canonical program, trusted/candidate prompt,
  trusted/candidate translator, run/task/result/invocation records, generation
  metrics, usage, generation prompt, final text, and full output log all match;
- every generation-evidence entry listed in `generation-result.json`,
  including the structured JSONL trace, independently hashes to its recorded
  value;
- candidate `prompt.py` is byte-identical to trusted `prompt.py`;
- candidate `py2mpy.py` is byte-identical to trusted `py2mpy.py`;
- recursive entry-name, type, and byte comparison of the supplied trusted and
  candidate `reference-semantics` trees found 26 entries and zero differences,
  missing entries, additions, type changes, or symlinks;
- all five required candidate proof deliverables exist as ordinary files:
  `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`.

Generation claims such as `KPROVE_PASSED` were not used as proof evidence.
The complete independent integrity transcript and tree manifests are
`evidence/01-provenance.log`, `evidence/candidate-tree-manifest.tsv`,
`evidence/candidate_semantics-tree-manifest.tsv`, and
`evidence/trusted_semantics-tree-manifest.tsv`.

Stage 1 result: **PASS; no infrastructure breach**.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: starting from balance zero, process an arbitrary
finite `List[int]` in order; return `True` as soon as a running balance is
strictly negative, and return `False` if no prefix balance is negative.

`solution.py` implements that algorithm. Its additional
`operation = 0` initialization is overwritten on the first nonempty iteration
and is unobservable for an empty list. The implementation preserves the
signature and uses unbounded Python integer arithmetic.

I regenerated the constructor program with the trusted translator:

```text
python3 /tmp/audit-work/reconstruction/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
```

`cmp` exited 0. Both files have SHA-256
`5e9e907167be11a2f30b29f110fb940b866c050c1efacbb6f638a39bfc96bab5`.

The independent `evidence/differential.py` loads the trusted canonical and
candidate entry points separately. It exercises the documented examples,
empty input, exact-zero and just-below-zero boundaries, immediate and late
failure, recovery after a negative prefix, arbitrary-precision integer
extremes, every list of length 0 through 6 over elements -3 through 3, and
5,000 seeded lists of length 0 through 50. Results:

```text
total_cases=142275
canonical_true_count=102667
canonical_false_count=39608
mismatch_count=0
```

The script, exact command, exit 0, and output are preserved in
`evidence/differential.py` and `evidence/02-program-fidelity.log`.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`, taking the
semantics from the trusted supplied tree. I did not copy or use candidate
compiled definitions, caches, the candidate `kore-exec.tar.gz`, or prior proof
logs.

### Concrete definition

The fresh LLVM command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. A reviewer-authored translated smoke module then exercised normal,
empty, exact-zero, just-negative, early-negative, and arbitrary-precision
cases:

```text
krun auditor-concrete-tests.mpy --definition runtime-kompiled
```

It exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. See `evidence/03b-kompile-llvm.log` and
`evidence/03c-krun-concrete.log`.

The LLVM compiler reported non-exhaustive-total warnings for unused functions
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is
reachable from this integer-list program or either proof claim; these warnings
do not explain either proof closure.

### Positive claims

`spec.k` contains exactly two positive claims. I independently built and ran
both:

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

kprove spec.k --definition verification-base-kompiled \
  --spec-module AUX-SPEC
```

Both commands exited 0 and the proof printed an exact `#Top` line.

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION-LEMMA --syntax-module MPY-SYNTAX \
  --output-definition verification-lemma-kompiled

kprove spec.k --definition verification-lemma-kompiled \
  --spec-module MAIN-SPEC
```

Again both commands exited 0 and the proof printed an exact `#Top` line.
Complete bounded logs are `evidence/03d-kompile-base.log`,
`evidence/03e-kprove-aux.log`, `evidence/03f-kompile-lemma.log`, and
`evidence/03g-kprove-main.log`.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

`AUX-SPEC` starts at the exact function loop head with:

- arbitrary remaining integer list `IS`;
- arbitrary current balance `B`;
- the real submitted loop body;
- the real final `return False` and `#endcall`;
- the concrete callee environment/frame shape;
- arbitrary original input, old loop variable, module map, builtins scope,
  heap, and heap counter.

It proves that fixed semantics completes that call with the Boolean
`prefixBelow(B, IS)`, removes the callee frame/scope, restores environment 0,
and preserves the framed heap, exception, and exit state. The otherwise
unrelated original input is correctly unconstrained: after iterable evaluation,
the loop depends only on the captured iterator remainder and current balance.

`MAIN-SPEC` starts from a fresh module configuration, loads the exact submitted
module, and calls `below_zero` on an arbitrary finite integer list `IS`. It
proves the returned K result is `prefixBelow(0, IS)` and constrains the final
module scope to contain the exact submitted closure while preserving all other
configuration cells.

`prefixBelow` is not a free result. Its exhaustive equations are:

- empty list: `false`;
- nonempty list: `true` iff the new balance is negative, otherwise recurse on
  the tail with the updated balance.

This is equivalent, not merely one-way implied, to the natural-language
running-prefix property.

### Mechanical program identity

The claim does not merely reference an external source filename. The three
macros in `verification.k` spell the translated loop body, complete function
body, and module binding. I parsed both trusted-regenerated `solution.mpy` and
the claim term `solutionProgram` against the fresh base definition with
`--module BELOW-ZERO-COMMON --sort Module --expand-macros --output kore`.
`cmp` exited 0; both KORE files have SHA-256
`63152660ba0e1143764d8d99dd1c5d29e44ecb5de982b0f99e865113e698f755`.
See `evidence/04-program-term.log`.

The claim therefore executes the submitted constructor term, including the
typing import, both assignments, `For`, `AugAssign`, comparison, early return,
and final return. Treating the typing-only import as a no-op does not alter the
entry result or control behavior.

### Satisfiability and concrete substitutions

A satisfying main state is:

```text
IS=intCons(1,intCons(-2,.IntVals))
env=0, scopes={0:scope(.Map,parent(-1)),-1:builtinsScope}
scopeLoc=1, heap=.Map, heapLoc=0, stack=.List
ret=noRet, exc=NoExc, exit-code=0
```

A satisfying auxiliary state is:

```text
IS=intCons(-2,.IntVals), B=1
INPUT=intCons(1,intCons(-2,.IntVals)), OLD=1
MODULE=.Map, BUILTINS=builtinsScope, HEAP=.Map, NEXT=0
env=1, scopeLoc=2, stack=[frame(.K,0,1)]
ret=noRet, exc=NoExc, exit-code=0
```

`evidence/claim_witnesses.py` substitutes empty, true, false, and boundary
lists. In every case its independent mathematical fold, trusted canonical, and
candidate implementation agree. The exact results are in
`evidence/04d-claim-witnesses.log`.

### Body sensitivity

A reviewer mutation changed the actual macro-expanded comparison from `< 0`
to `> 0`. The fresh bridge-free auxiliary proof then exited 1 with a genuine
symbolic unmet-condition residual. The admitted main-summary rule by itself
still closed, which is expected and demonstrates why the submitted auxiliary
claim is essential. Since the intact candidate requires both positive claims
and the auxiliary theorem is exact, this is positive body-sensitivity evidence,
not a shortcut. See `evidence/07-body-sensitivity.log`.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

I rebuilt an exhaustive lexical inventory rather than relying on the
candidate's prose. `evidence/05-rule-inventory.tsv` contains the complete
normalized text, file, line, module, kind, and attributes for every local
declaration in all supplied K sources, `verification.k`, and `spec.k`:

```text
695 supplied-semantics rules
8 proof-local rules
2 reachability claims
233 syntax declarations
5 contexts
1 configuration
```

There are 146 local function declarations, 108 marked `total`, 36
concrete-only declarations/rules, 46 priority rules, 26 `owise` rules, and no
local `simplification` or `functional` declarations. Counts by file and the
inventory-generation command are in `evidence/05-inventory-summary.log`.

`evidence/05-rule-review-ledger.md` gives the disposition of every module and
individually classifies all proof-local declarations. The material used path is:

```text
load/sequence
  -> no-op typing import and exact closure binding
  -> callee lookup and left-to-right argument evaluation
  -> fresh function frame and exact parameter binding
  -> Assign(0), Assign(0)
  -> For/#loop over the proof list representation
  -> integer AugAssign(+), integer Compare(<), If/branch
  -> Return/#pop or iterator tail
```

Every material state update and control transfer is represented. Integer
operations use mathematical unbounded `Int`, matching Python integers.

### Proof-local rules

- The three macro rules are definitional and were mechanically matched to the
  submitted KORE term.
- `IntVals` is the free inductive datatype
  `.IntVals | intCons(Int,IntVals)`, so it covers every finite length and every
  integer magnitude; it is not a bounded unrolling.
- The two `asValSeq` iterator rules are exhaustive/disjoint and reproduce the
  fixed `.ValSeq`/`vCons` list iterator equations head-for-head and tail-for-tail.
  They introduce no result oracle and structurally descend.
- The two `prefixBelow` equations are exhaustive/disjoint, mathematically true,
  and structurally descending.
- The loop-summary rule is an operational bridge. Its match includes the exact
  body, exact trailing return and `#endcall`, exact frame, environment/scope
  transition, return/exception state, heap, allocation counters, and exit code.
  It has no arbitrary continuation ellipsis. `AUX-SPEC` proves exactly this
  universally quantified transition in a definition that does not import the
  summary. Thus every bridge match is inside the independent theorem's
  justification domain. Priority does not broaden that domain.

Although `prefixBelow` occurs in both the summary and final postcondition, this
is not circular: the bridge-free auxiliary claim first derives that exact value
by executing the loop. The body mutation confirms that derivation is
comparison-sensitive.

The supplied semantics contains 25 explicitly opaque symbols for float
operations, sorting, and MD5. They are enumerated in the static ledger. None is
reachable from or mentioned by either target claim. Runtime-only
`MPY-CONCRETE` is not imported by either proof main module. The unused
non-exhaustive-total warnings are coverage limitations for other programs, not
false equations on this program's domain.

No candidate or supplied rule contributing to closure encodes the task answer,
fabricates a used operation's result, replaces a used operation with an
unconstrained oracle, has overlapping guards with inconsistent right sides, or
admits a false conclusion witness on any `List[int]` input. Unused broad
semantics rules cannot synthesize symbols on this execution path. I therefore
do not label them unsound without the concrete/symbolic false-conclusion witness
the audit standard requires.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I did not rely on a candidate vacuity artifact. The fresh
`spec-audit-mutation.k` uses the complete real-program entry configuration on
the satisfying input `[-1]`, but changes the result obligation to `false`.
Both trusted and candidate Python return `True`, and
`prefixBelow(0,intCons(-1,.IntVals))` is `true`.

First:

```text
kprove spec-audit-mutation.k \
  --definition verification-lemma-kompiled \
  --spec-module AUDIT-MUTATION --dry-run
```

exited 0, proving the mutation parses and builds. The actual proof command
exited 1 with `WarnStuckClaimState`. Its residual had `<k> true ~> .K </k>`
while the destination demanded `false`, followed by the expected “cannot be
rewritten further” prover error. This is an unmet result obligation, not a
parser error, import failure, timeout, or unrelated crash.

The mutation source, exact commands, statuses, and bounded residual are
`evidence/run-mutation.sh`, `evidence/06a-mutation-dry-run.log`, and
`evidence/06b-mutation-proof.log`.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics, for every finite `IntVals` and every
mathematical integer element, executing the exact submitted module and calling
its exact `below_zero` closure from the specified fresh configuration returns
`prefixBelow(0, IS)`. The bridge-free auxiliary theorem establishes the exact
loop/frame transition for arbitrary starting balance, remainder, heap, module,
and irrelevant original-input binding. `prefixBelow` is definitionally the
existence of a strictly negative running prefix balance.

This is an unrestricted partial-correctness result over all finite
`List[int]` values. It is not a proof of finitely many sizes, examples, or an
unrolled bound.

### Trust and assumptions

1. **K implementation and built-in integer/Boolean/map/list theories.** Their
   implementation is outside this theorem. They affect symbolic execution and
   arithmetic. This is the ordinary acceptable theorem-prover trust boundary;
   the locked and live K versions both report 7.1.293.
2. **The supplied MPY semantics for the used subset.** It is selected by the
   benchmark, byte/type verified against the trusted tree, and statically
   reviewed above. The proof depends on its module loading, scopes, calls,
   assignments, iteration protocol, integer operators, branching, returns, and
   frame restoration. Fresh LLVM execution provides finite corroboration, not
   a replacement proof.
3. **Trusted translator/source bridge.** The launcher designates
   `py2mpy.py` trusted. Regeneration is byte-identical, and macro-expanded KORE
   mechanically pins that output. The translator's trust does not substitute
   for the K proof; it identifies the K term corresponding to `solution.py`.
4. **Input representation bridge.** `IntVals`/`asValSeq` is a proof-side
   structural encoding of arbitrary finite integer lists. Its only used
   operation is iteration, and its exhaustive equations are exactly the fixed
   list iterator equations. Because the program does not mutate, compare,
   index, alias, or inspect identity of the input list, the read-only unboxed
   representation preserves every material behavior. This is an acceptable
   structural input boundary, not a result-bearing oracle.
5. **Typing import abstraction.** `from typing import List` is modeled as a
   no-op. It affects neither entry-result evaluation nor control and is an
   acceptable typing-only abstraction for this theorem.
6. **Opaque supplied symbols.** The 22 float symbols, two sort symbols, and
   MD5 symbol listed in `evidence/05-rule-review-ledger.md` have no dependents
   in either claim. No conclusion here is conditional on their interpretation.
7. **Empirical evidence.** Differential testing, ground witnesses, concrete
   K execution, and mutations support fidelity/non-vacuity only over their
   recorded cases. None is presented as a universal substitute for the two
   successful reachability proofs.

### Gate and verdict mapping

- Gate A, real-program soundness: **PASS**. Program identity, complete bridge
  context, bridge-free connection theorem, value equations, satisfiable
  witnesses, body sensitivity, and false-result rejection all pass.
- Gate B, intent adequacy: **PASS**. The theorem covers arbitrary finite
  `List[int]` values and proves the exact negative-prefix property with
  unbounded integers.
- Gate C, trust/evidence auditability: **PASS**. All evidence is reproducible,
  assumptions and opaque symbols are enumerated, and no unproved
  result-bearing abstraction affects the conclusion.

The reconstructed proof is result-constraining, pins the real generated
program, covers the full source-contract domain, and uses no materially
unsound proof or semantics rule. The appropriate benchmark decision is
`PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
