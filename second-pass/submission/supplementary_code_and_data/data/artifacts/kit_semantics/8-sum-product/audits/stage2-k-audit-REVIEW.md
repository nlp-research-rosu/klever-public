# Independent adversarial audit: 8-sum-product

The candidate contains a legitimate partial-correctness proof of the real
generated `sum_product` program over the full HumanEval source-contract domain:
arbitrary finite lists of integers, with no length or magnitude bound. I
reconstructed the definitions from source, reproduced `#Top`, mechanically
pinned the target claim to the trusted-regenerated program, inventoried all K
rules, and obtained the expected failure from a fresh false result obligation.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`problem_id: 8-sum-product`, and `semantics_mode: SUPPLIED_SEMANTICS`.
The required trusted `/reference/reference-semantics` tree is present, so the
trusted mounts do not contradict the rendered mode.

The independent integrity script:

- compared `/audit-campaign-lock.json` structurally with the
  `audit_campaign` block and obtained equality;
- recomputed the lock SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- verified every required pipeline-v3 record is a readable regular file and
  every declared directory is real rather than symlinked;
- recomputed and matched the recorded SHA-256 values for `/run.json`,
  `/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, the trusted prompt/translator/canonical,
  and every trace file;
- recomputed the pipeline tree digest of the structured trace as
  `c0c71447077c89e71d59d5b0001bd25e66243492e3b6030c42fdcbb661fc4a55`,
  matching `usage.json`;
- recomputed the mounted candidate pipeline digest as
  `1ba212743136486053546c8c441c2f88479626048a6b1de123247f265c0647a4`,
  matching both the invocation and stage result;
- recursively compared all 25 entries in candidate and trusted
  `reference-semantics` trees. Paths, entry types, and file hashes are equal;
  there are no missing, additional, changed, mistyped, or symlinked entries;
- verified candidate `prompt.py` and `py2mpy.py` are byte-identical to their
  trusted mounts; and
- verified every required candidate proof artifact is a regular file.

The structured trace contains 357 valid JSON records and no parse error. The
reviewer read every record, inventoried all generation commands/messages, and
scanned all 830,456 bytes (22,688 lines) of `codex-output.log`. These records
were treated only as untrusted claims. The generation-time Kit commit in
`run.json` and the audit-campaign Kit lock describe different pipeline stages;
the required audit-campaign block itself exactly matches its lock.

Evidence:
[stage1 records](evidence/stage1-records.log),
[integrity results](evidence/stage1-integrity.log), and
[generation trace inspection](evidence/stage1-generation-trace-summary.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires:

> For a finite list of integers, return a pair containing the sum and product
> of all elements; the empty identities are 0 and 1.

The examples are `[] -> (0,1)` and `[1,2,3,4] -> (10,24)`. The trusted
canonical initializes `(sum,product)` to `(0,1)`, iterates over every element,
adds and multiplies it, and returns the pair. Candidate `solution.py` uses the
same algorithm with locals `total`, `product`, and `number`. It does not impose
a value, sign, magnitude, or length restriction.

Running the trusted `/reference/py2mpy.py` on candidate `solution.py` produced
a file byte-identical to submitted `solution.mpy`; both SHA-256 values are
`14adc08f673914888ccafe621ea8b6321ecaf598b067d8b4f1ef2ff348b5cad3`.
See [trusted regeneration](evidence/stage2-translation.log).

The independent differential test imports the trusted canonical and generated
entry points separately. Its 20,137 cases comprise:

- 17 explicit examples and boundaries, including zero, one, and many loop
  iterations, signs, zeros in different positions, cancellation, repeated
  values, 100- and 200-digit integers, and a 128-element list;
- every list of length 0 through 5 over `[-3,3]` (19,608 inputs); and
- 512 deterministic lists of length 0 through 64 with mixed ordinary and
  scaled large integers.

The preserved case-set digest is
`73e5b6eb7bbaba2fa661ac1202dd334c10d184fa96f45605f8fe255c48d43093`.
There were zero mismatches and exit status 0. See
[script](evidence/differential_test.py) and
[results](evidence/stage2-differential.log). This finite evidence supports
implementation/translator adequacy; it is not substituted for the K theorem.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/8-sum-product`. Candidate
`semantics-kompiled`, `verification-kompiled`, bytecode, caches, and prior logs
were not copied or used. The live tools are K 7.1.293
([versions](evidence/stage3-tool-versions.log)).

Fresh concrete definition:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-semantics-kompiled
```

This exited 0. The warnings concern known non-exhaustive functions in unused
supplied-semantics legs, not any used construct. Fresh `krun` execution exited
0 and left these bindings:

```text
empty_result   = (0, 1)
example_result = (10, 24)
signed_result  = (-3, 24)
zero_result    = (99, 0)
```

See [LLVM build](evidence/stage3-kompile-llvm.log) and
[concrete run](evidence/stage3-krun-candidate-smoke.log).

Fresh proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

This exited 0
([build log](evidence/stage3-kompile-haskell.log)). The positive claims are
`SPEC.loop-invariant` and `SPEC.sum-product`. The invariant-focused command
printed `#Top` and exited 0
([log](evidence/stage3-kprove-loop-invariant.log)). The required all-claims
command—needed so the invariant is available as the target's circularity—
also printed `#Top` and exited 0
([log](evidence/stage3-kprove-all-positive.log)). Thus every positive claim is
included in a clean successful run; the entry theorem was not judged from the
candidate's prior cache or log.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`loop-invariant` assumes:

- an arbitrary finite suffix `VS` whose every element is a semantic `Int`;
- the exact submitted `#loop(list(VS), Name("number"), BODY)` control state;
- integer accumulators `S` and `P`; and
- the exact plain four-key function frame for `numbers`, `number`, `total`, and
  `product`, with parent scope 0.

It says the real loop consumes the suffix, leaves `.K`, changes `total` to
`sumFrom(VS,S)` and `product` to `productFrom(VS,P)`, and permits the
unobservable local `number` to contain its actual final value. Other scopes,
the continuation, heap, stack, return/exception state, and exit status are
framed and preserved.

`sum-product` assumes the supplied initial configuration and an arbitrary
finite `VS` satisfying `allInts(VS)`. It loads the exact translated module,
binds and calls its exact `sum_product` closure with `list(VS)`, and says the
returned value is exactly:

```text
(sumFrom(VS,0), productFrom(VS,1))
```

This is an equality to a deterministic two-element tuple, not a fresh result,
tautology, implication, or oracle.

### Mechanical program identity

A reviewer script extracted the balanced `Module(...)` term inside the entry
claim's `#loadAll`, removed layout only, and compared it with both submitted and
trusted-regenerated `solution.mpy`. All three normalized constructor terms have
length 314 and SHA-256
`9202a521559793f6fb50164e8f9a5a7def8f05f73cb8641159ae48d23a041c93`.
The `ImportFrom`, `FuncDef`, initializations, `For`, ordered `+`/`*`
`AugAssign`s, and tuple return are all present. See
[script](evidence/pinning_check.py) and
[result](evidence/stage4-constructor-pinning.log).

The only source normalization is that the fixed semantics treats the typing
import as a no-op and permits bare `list(VS)` for read-only claim inputs.
`core.k` expressly includes bare lists as legal claim values. A bridge-free
reviewer claim importing only fixed `MPY` proves universally that an actual
heap-backed `ref(H)` with `H |-> list(VS)` is dereferenced at `For` entry to the
same bare list loop state
([baseline connections](evidence/stage5-kprove-baseline-connections.log)).
The submitted body never mutates `numbers`.

### Satisfiability, substitution, and sensitivity

`VS = [2,-3,4]` satisfies `allInts`. A ground claim from the exact initial
state executes the exact submitted module and closes at `(3,-24)` with `#Top`
and exit 0
([claim](evidence/spec-ground-witness.k),
[K result](evidence/stage4-ground-witness-kprove.log)). Both Python
implementations return the same `(3,-24)`
([Python result](evidence/stage4-ground-witness-python.log)).

A separate body-sensitivity claim changes product initialization from 1 to 2
in both the module actually loaded and the closure binding asserted after
loading, while preserving the original empty-list obligation. It parses and
executes to `(0,2)`, then fails against `(0,1)` with
`WarnStuckClaimState` and exit 1. This changes the executed program term, not
an external file. See
[mutation](evidence/spec-body-sensitivity-reviewer.k) and
[residual](evidence/stage4-body-sensitivity.log).

The claim therefore pins and depends on the real submitted program.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory covers 26 K files and 949 entries:

```text
232 syntax declarations
709 rules
5 contexts
1 configuration
2 reachability claims
```

It separately marks 150 functions, 112 `total` declarations, 26
symbol/opaque declarations, 45 priority rules, seven simplification rules, and
every complete guard/attribute. Of the 949 entries, 928 are byte-identical
fixed supplied semantics and 21 are candidate proof-local entries. The full
TSV inventory, source hashes, and per-file counts are in
[stage5-rule-inventory.log](evidence/stage5-rule-inventory.log).

For every one of the 928 fixed entries, the decision is: it follows the
selected `SUPPLIED_SEMANTICS` level by definition and is not a candidate proof
extension. That is not an assertion that unused MiniPy behavior is complete
CPython. I additionally mapped every construct actually used by
`solution.mpy` through syntax, configuration, evaluation order, module load,
scope lookup, binding, call/frame lifecycle, assignment, iteration, integer
dispatch, tuple construction, and return. The relevant source is preserved in
[stage5-material-semantics.log](evidence/stage5-material-semantics.log).
No fixed declaration contains the task's result helpers
([separation check](evidence/stage5-task-answer-separation.log)).

The 21 candidate entries are exactly five declarations, 14 rules, and two
claims. Their exhaustive individual decisions are recorded in
[stage5-static-review.md](evidence/stage5-static-review.md). The conclusions
are:

- `allInts` has disjoint, exhaustive empty/cons equations and strictly
  descends. It exactly captures the stated integer-list domain.
- `definedProjectInt` is exactly `isInt`.
- `projectIntTotal` is unspecified for non-integer semantic values, but every
  result-bearing use in these claims is dominated by `allInts`; on integers,
  its guarded cast rules and identity equation uniquely force the underlying
  integer. Cast-rule overlaps agree and their concrete/symbolic orientations
  terminate in the reconstructed proof.
- The guarded `applyBin` `+` and `*` twins have exactly the fixed `MPY-INT`
  right-hand sides after projection. Bridge-free claims against a definition
  importing only `MPY` establish those fixed equations. They do not skip a
  `<k>` operation or alter control/state.
- `sumFrom` and `productFrom` are ordinary structurally descending left folds
  with disjoint/exhaustive constructors. They appear in the invariant and
  postcondition; they never rewrite program execution.
- The loop claim matches the actual loop body and advances through a real
  head/body/tail step before circular reuse. Its existential final `number`
  only forgets an unobservable local.
- The entry claim pins all ten configuration cells and exact result.

There is no proof-local `<k>` operational rewrite, priority rule, call
interception, frame pop, return shortcut, loop shortcut, or fresh result
oracle. Fixed-versus-proof helper checks produce `2`, `-3`, `-1`, and `-6`
on distinct ground values
([positive helper log](evidence/stage5-kprove-helper-values.log)); the opposite
interpretation `projectIntTotal(2) = 3` is rejected with residual `2`
([negative helper log](evidence/stage5-kprove-helper-opposite.log)).

No rule was labeled unsound: the review found no concrete or symbolic false
conclusion witness on the intended domain. The opaque off-domain
`projectIntTotal` interpretation cannot affect either entry precondition's
satisfying executions.

## 6. Fresh non-vacuity test

Candidate `spec-vacuity.k` and `spec-body-mutation.k` were inspected only as
untrusted evidence. The reviewer created a distinct mutation from scratch.
It:

- executes the exact submitted `#loadAll(Module(...))` term;
- uses the satisfying input `[2,-3,4]`;
- changes only the result-constraining expected sum from the true 3 to false
  4; and
- keeps the expected product `-24`.

`kprove --dry-run` generated KORE and exited 0, proving the mutation is
well-formed and builds
([dry run](evidence/stage6-fresh-mutation-dry-run.log)). The real proof run
exited 1 with `WarnStuckClaimState`; its residual contains the reachable true
value `(3,-24)`, which does not unify with false `(4,-24)`. See
[mutation source](evidence/spec-fresh-vacuity-reviewer.k) and
[failure log](evidence/stage6-fresh-mutation-kprove.log). This is an expected
unmet obligation, not a parser error, timeout, missing import, backend crash,
or unreachable mutation.

## 7. Proven versus assumed accounting

### Formally established

Relative to the supplied proof definition, the successful reachability proof
establishes:

> For every finite semantic list `VS` whose elements are all K `Int` values,
> if execution of the exact trusted-regenerated `sum_product` module/call
> terminates from the pinned initial state, the returned value is the tuple of
> the recursive integer sum from 0 and recursive integer product from 1.

The theorem is symbolic in sequence structure and integer values. It is not a
bounded unrolling or finite collection of examples. The loop circularity
connects each real iteration to the folds.

### Trusted or external boundaries

- **K implementation:** K 7.1.293 parsing, kompilation, reachability logic,
  circularity handling, Haskell backend, and its condition reasoning are
  trusted. This is the ordinary machine-checking boundary.
- **K built-ins used materially:** arbitrary-precision `Int`, `+Int`, `*Int`,
  `Bool`/`andBool`, maps, lists, algebraic sequence constructors, generated
  `isInt`, subsort casts, and cell framing are trusted.
- **Fixed supplied semantics:** all 928 baseline entries define the selected
  MiniPy execution model. Their material path was reviewed; unrelated language
  features remain outside the theorem.
- **Unused fixed opaque symbols:** `md5hexCodes`; `intFloatDiv`, `divII`,
  `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`,
  `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
  `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`; and `sortVS`,
  `sortKeyVS`. None is reachable from this program/claim, so none can influence
  control, state, or result.
- **Proof-local totalized projection:** `projectIntTotal` is opaque only outside
  `isInt`; on the theorem domain its equations fix its exact value. Its
  off-domain interpretation is excluded by the exact source precondition and
  is not a trusted program-result oracle.
- **Translator:** `/reference/py2mpy.py` is outside K. Byte-identical trusted
  regeneration plus constructor comparison makes the source-to-term bridge
  mechanical for this immutable candidate.
- **Prompt/canonical intent:** interpreting `List[int]` as arbitrary finite
  integer lists and tuple components as mathematical sum/product is an
  informal source-contract bridge. The recursive equations match that
  definition directly; canonical differential evidence supports it.
- **Bare read-only list input:** this is permitted by the fixed semantics and
  universally connected to the heap-ref loop entry. Concrete heap-backed calls
  and differential Python tests give additional finite evidence.

### Empirical evidence and exclusions

Concrete K and 20,137 Python differential cases support only the tested
translator/model bridge; they do not prove the universal theorem. The proof
does not cover non-integer elements, Python features outside the supplied
subset, input mutation, exceptional behavior outside the stated domain,
annotation evaluation, or a separate liveness/termination theorem.

Gate A passes: the theory is sound on the exact intended domain, the real body
executes, and the result is non-vacuously constrained. Gate B passes: the
precondition covers the full unrestricted HumanEval `List[int]` domain and the
postcondition is the required sum/product pair. Gate C passes: assumptions and
all commands/evidence are explicit and reproducible. The reviewer evidence
index is [evidence/README.md](evidence/README.md).

VERDICT: PASS
LEGITIMACY: LEGIT
