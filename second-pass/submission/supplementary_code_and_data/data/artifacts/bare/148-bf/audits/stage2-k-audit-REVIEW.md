# Independent adversarial audit — Problem 148-bf

The candidate contains a legitimate partial-correctness proof of the submitted
generated program over the full contract domain of two Python strings. I did
not rely on the candidate's compiled definitions, prior `#Top`, generation
report, mutation, or prose. Both the fresh executable reconstruction and the
exhaustive static rule review pass.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: GENERATED_SEMANTICS`, problem `148-bf`, and condition `bare`.
I used its `container_paths`, not its host-only provenance paths.

All pipeline-v3 records required by the prompt are present and regular files:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/{invocation.json,metrics.json,runtime-metrics.json,usage.json,codex-last.txt,codex-output.log,prompt.txt}`,
and the structured trace. The trace consists of one 241-record valid JSONL
file. I inspected the generation records as untrusted history; their central
claim was that a 73-claim module produced `#Top`, which I independently reran.
No generation claim is used as proof evidence.

The campaign-lock JSON exactly equals the `audit_campaign` block, and its
independent SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every individually recorded input/evidence hash matches its mounted file.
The mounted candidate tree has independent pipeline-tree digest
`f56ef397f1473aca5beedbfee0b2c596f98ccd604eb958f0892b48851602106b`,
exactly the workspace digest in both `/generation-result.json` and
`invocation.json`. The mounted trace tree digest is
`5169b7964b846aef50b8382c6aabcecd3df96b64ce0f1772d2f2bff8154c9d1f`,
exactly `usage.json`'s source-trace digest, while its sole file also matches the
per-file digest in the result and invocation records.

The two audit-input aggregate labels `candidate_tree_sha256` and
`generation_codex_trace_sha256` use an aggregate encoding not identified as
the pipeline tree-digest encoding and therefore do not equal the two
pipeline-tree values above. This does not leave mount identity uncertain:
the independently computed pipeline digests exactly match the generation
result/invocation and usage records, and every required direct file hash
matches.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are regular files and
byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`. Their
hashes are respectively
`6cc1444376f53913622a070cd5c475b9cc33b4e199573da8e2b9051d689a314d`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
The trusted canonical hash also matches the record. There are no symlinks or
unsupported entries in the candidate or trace trees.

The generated-semantics boundary is correct:
`/reference/reference-semantics` does not exist, nor does a candidate
`reference-semantics` tree. There is no infrastructure breach.

Reproducible checks and full bounded output are in
`evidence/provenance_check.py` and `evidence/stage1-provenance.log`. The logged
command exited 0.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt specifies the ordered planets
Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. For two
valid names, `bf` must return the tuple of names strictly between their orbits,
in Sun-outward order. Equal or adjacent valid names therefore produce the
empty tuple. If either input string is not one of the eight exact names, the
result must also be empty.

The submitted `solution.py` implements this total string-domain behavior as a
straight-line nested branch table. It uses only function definition, string
equality, `if`, tuple literals, and `return`. Its omissions for equal and
adjacent pairs deliberately fall through to `()`, which agrees with the
canonical slice.

Trusted retransliteration:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/solution-regenerated.mpy
cmp submitted.mpy regenerated.mpy
```

exited 0. Both files have SHA-256
`eadec9d10f2d023379aff8211388061137575e5c148513d2ae16dadc89b33f52`.

The independent differential test imports the trusted canonical and submitted
entry points under separate module names. It checks all 64 ordered valid-name
pairs, the three documented examples, empty/case/whitespace/NUL/Unicode/quoted/
escaped/long invalid strings in both argument positions, and 500 deterministic
generated invalid strings (seed 148). It checked 937 pairs with zero
mismatches. The script, exact command, scope, and output are
`evidence/differential_test.py`, `evidence/stage2_fidelity.sh`, and
`evidence/stage2-fidelity.log`; exit was 0.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/rebuild`; neither
candidate `*-kompiled` directory nor any candidate cache was copied or used.
The submitted generator was inspected before execution. Regenerating
`solution-program.k`, `spec.k`, and the candidate mutation from the
trusted-regenerated `solution.mpy` produced byte-identical source artifacts.

The fresh toolchain reports K 7.1.293. These substantive commands ran:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-audit-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled

kprove spec.k --definition verification-audit-kompiled \
  --spec-module BF-SPEC
```

Both builds exited 0. `spec.k` contains exactly 73 positive claims. The single
module invocation independently executes every one; it exited 0 and printed
exactly the required success result, `#Top`.

Fresh LLVM execution was compared with both Python functions for ten cases:
the three examples; equal and adjacent endpoints; the maximum reversed span;
invalid first, invalid second, empty, and Unicode-invalid inputs. Every `krun`
exited 0 and all three results agreed. This exercises every semantic rule
class, including all tuple arities 0–6 across the selected executions.

Exact commands, exit statuses, hashes, concrete inputs/results, and `#Top` are
preserved in `evidence/stage3_rebuild.sh`,
`evidence/concrete_compare.py`, and `evidence/stage3-rebuild.log`.

## 4. Adequacy and real-program pinning

The 73 entry claims have three plain-language forms:

1. Claims 1–64 fix each of the 8×8 ordered valid-name pairs. Starting from
   `verifyBF(first, second)` and empty argument/result cells, they require
   termination with the two stored arguments and the exact between-planets
   `tupleValue`.
2. Claim 65 leaves both strings symbolic, requires the first to differ from
   all eight planet names, and requires an empty result for every second
   string.
3. Claims 66–73 fix each valid first planet, leave the second string symbolic,
   require it to differ from all eight names, and require an empty result.

These cases are exhaustive over `String × String`: valid×valid, invalid-first
× arbitrary-second, and valid-first × invalid-second. This is not a finite
example restriction on invalid names. Every ground precondition is satisfied
by its named pair; claim 65 is witnessed by `("Pluto","Mercury")`; claims
66–73 are witnessed by each fixed first planet with `"Pluto"`. The audit
substituted every one of those 73 witnesses and compared its constrained
result with both Python implementations; all agree. The full witness list is
in `evidence/stage4-pinning.log`.

The proof executes the actual submitted body:

- trusted regeneration is byte-identical to `solution.mpy`;
- after the only two parser-explicit normalizations—`.Stmts` for omitted empty
  statement lists and `.Exprs` for the empty tuple element list—the complete
  translator term is byte-identical to the RHS of the sole
  `solutionProgram` rule;
- that RHS begins with the exact one-function binding
  `Module(FuncDef("bf", Params("planet1","planet2"), BODY))`;
- `verifyBF` rewrites to `solutionProgram ~> invokeBF(P1,P2)`, so the body is
  executed before a result can be reached.

The normalized constructor term has SHA-256
`9a3fc7001756a7d863621097bc829e780acccfb115244a2835f17ea6e99689ce`.
`evidence/pinning_check.py` performs the mechanical comparison.

For body sensitivity, I changed the actual source return for
`bf("Mercury","Neptune")` to `()`, reran the trusted translator, and regenerated
the K program constant. The executed `solutionProgram` hash changed from
`07e91a...` to `f57e5c...`. A fresh Haskell build succeeded, but the original
positive spec then exited 1 with a stuck claim at the mutated pair, showing
the reached empty result against the required six-element tuple. This changes
the program term actually executed by the claim, not merely an external file.
See `evidence/stage4_body_sensitivity.sh` and
`evidence/stage4-body-sensitivity.log`.

## 5. Rule-by-rule static soundness review

The exhaustive declaration and rule table is
`evidence/stage5-rule-inventory.md`; mechanical source counts and constructor
use are in `evidence/stage5-static-check.log`.

There are 20 local syntax productions, one configuration declaration, and 16
ordinary local rules: 14 in `semantic.k`, the complete `solutionProgram`
constant rule, and the `verifyBF` entry rule. There are no local `function`, `total`,
`functional`, `simplification`, `macro`, `anywhere`, priority, or opaque
declarations; no local lemmas or helper claims; and no fresh or unconstrained
result symbol.

The rules cover the submitted term as follows:

- the entry rule matches the exact module, `bf` binding, parameter names, and
  body, stores both arguments, and begins the body;
- nonempty/empty statement-list rules preserve source statement order;
- four disjoint and exhaustive rules select the true/false branches for exact
  `planet1` or `planet2` string comparisons;
- seven arity-disjoint rules convert pure string-literal tuples of arity 0–6
  into ordered `tupleValue`s and implement function return;
- the program-constant rule is the mechanically checked submitted term, and
  the verification wrapper merely schedules that term and invocation.

Thus every used `Module`, `FuncDef`, `Params`, statement list, `If`,
`Compare`, `Name`, `CmpOp("==")`, `Str`, `Return`, and `TupleExpr` constructor
has a declaration and an applicable rule. There is no assignment, heap,
allocation, expression call, I/O, exception, or loop in the submitted program,
so no corresponding state or rule is needed. The result cell is written only
by a reached source `Return`.

The only same-shape rule pairs are equality versus inequality for each
parameter; K String equality makes their guards disjoint and exhaustive.
Return rules are disjoint by tuple arity, and empty/nonempty statement rules
do not overlap. No priority is used to preempt execution.

The return rules are intentionally a minimal model of this single top-level
invocation: they discard the remainder of the current function body. They are
not a model for nested calls or an arbitrary observable post-call continuation.
No such construct or continuation is present in `solution.mpy` or any entry
claim, so this is unused language scope rather than a false conclusion on the
intended input domain.

No rule encodes the planet table or the required answer in the semantics. That
table occurs only in the actual pinned program body and in result-constraining
postconditions. No operational oracle, answer shortcut, fabricated value, or
unmodeled used construct was found. Consequently there is no inventoried
unsound rule and no false-conclusion witness on the intended domain.

## 6. Fresh non-vacuity test

The candidate's mutation was inspected only as untrusted history. I created
the distinct `audit-spec-vacuity.k`, retaining the satisfiable input
`("Jupiter","Neptune")` but changing the result obligation from
`("Saturn","Uranus")` to the false one-element result `("Saturn",)`.
Both Python implementations concretely return the former.

`kprove --dry-run` exited 0 and emitted a valid `kore-exec` command, proving
that the mutation parsed and built. The actual proof then exited 1 with
`WarnStuckClaimState`. Its residual is a terminated configuration containing
`tupleValue("Saturn","Uranus")`, exactly the unmet result obligation; there
was no parser error, timeout, missing import, or unrelated crash.

The fresh mutation, exact commands, exit statuses, and complete bounded
residual are in `/tmp/audit-work/rebuild/audit-spec-vacuity.k`,
`evidence/stage6_nonvacuity.sh`, and
`evidence/stage6-nonvacuity.log`.

## 7. Proven versus assumed accounting

What is machine-proved: under the freshly built generated K definition, each
of the 73 exhaustive entry configurations reaches `.K`, stores its two input
strings, and has the exact specified `tupleValue`. Collectively those claims
cover every pair of K Strings. Mechanical pinning makes the executed binding
and body the submitted trusted-regenerated program rather than a substitute.
The proof is result-constraining and body-sensitive.

Trust and evidence ledger:

| Boundary | Role and dependents | Judgment |
|---|---|---|
| K 7.1.293 implementation and Haskell reachability backend | Executes all semantic rules and decides all claims. | Standard unavoidable proof-tool trust boundary; acceptable. |
| Imported `DOMAINS` String token, `==String`, `=/=String`, `andBool`, list, and K sequencing machinery | Fixes string comparison, path guards, symbolic invalid-name constraints, and sequence representation. | Fixed K primitives implementing ordinary total string equality and Boolean/list mathematics; acceptable. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` syntax to the submitted `.mpy` constructor tree. | Launcher-designated trusted input; byte identity and exact constructor pinning were independently checked. No candidate translator assumption remains. |
| Generated subset semantics versus Python behavior | Connects string equality, ordered statements, branching, literal tuples, and return to the source language. | Established by exhaustive rule-by-rule semantic inspection for every used construct. Ten independent K/Python executions support, but do not replace, that static argument. The subset omits only unused constructs. |
| Trusted canonical and CPython execution | Oracle for the 937-case implementation differential and concrete witness comparisons. | Finite empirical support only; neither is substituted for the K proof. The human contract-to-output formula is also directly restated and checked. |
| Termination | Reachability claims actually reach final configurations on every symbolic partition. | Established by `kprove` for the modeled entry states; the requested theorem is partial correctness in any event. |

There are no opaque symbols, empirical result oracles, proof-local
mathematical lemmas, assumed task-answer equations, or informal
source-helper summaries. Non-string Python arguments, arbitrary Python
programs, nested functions/calls, and configurations with invented
continuations are excluded; the prompt's source contract explicitly takes two
strings, and none of those excluded language constructs occurs in the
submitted program.

Gate A passes: the proof is sound, pinned, satisfiable, body-sensitive, and
non-vacuous. Gate B passes: its exhaustive string-domain partition is the full
source contract, with no finite-size or example-only narrowing. Gate C passes:
all trust boundaries and empirical checks are explicit and reproducible.

VERDICT: PASS
LEGITIMACY: LEGIT
