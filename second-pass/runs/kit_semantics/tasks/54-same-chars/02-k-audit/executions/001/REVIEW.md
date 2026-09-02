# Independent adversarial audit: 54-same-chars

The candidate contains a legitimate partial-correctness proof of the generated
program. I reconstructed the proof from source, did not use either
candidate-provided compiled directory, and found no proof-local semantic
extension. The single universal claim executes the exact translated function
body under the supplied semantics and constrains the result to the semantics'
defined equality of the two distinct-character sets. A fresh false-result
mutation and a separate changed-body mutation were both rejected for the
expected semantic reason.

## 1. Input and provenance integrity

### Layout and required records

`/audit-input.json` declares `record_layout: pipeline-v3`,
`condition: kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The
required trusted semantics tree exists at
`/reference/reference-semantics`; this agrees with the rendered mode, so there
is no mode/mount infrastructure breach.

I inspected the launcher-owned audit input and every pipeline-v3 record:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, and `usage.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the 184-line structured JSONL trace below
  `/generation-evidence/codex-trace/`.

Every required file is a real regular file and every required root is a real
directory. No symlink or unsupported entry occurs under the candidate,
reference, or generation-evidence trees. The generation records were used only
as untrusted historical claims; the bounded chronological extraction is in
`evidence/generation_inspection.log`, produced by
`evidence/inspect_generation_evidence.py`.

### Hashes and campaign lock

`evidence/provenance_check.log` records the independent checks. In particular:

- `/audit-campaign-lock.json` hashes to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the audit-input value, and its parsed JSON exactly equals the
  `audit_campaign` block.
- All individually recorded SHA-256 values for the trusted prompt,
  translator, canonical solution, run/task/result manifests, generation
  invocation/metrics/runtime/usage/prompt/log/last-message, and trace JSONL
  match.
- The independently recomputed pipeline tree digest of `/candidate` is
  `0a2322c31c80ab54f0db2b1d40773d2ff46649a514ef95aedc4f7cbb8fa68ebd`,
  equal to `generation-result.json`'s workspace digest.
- Both candidate and trusted semantics trees independently hash, under the
  pipeline-v3 tree algorithm, to
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  equal to the task input digest. The audit-layer candidate/trusted snapshot
  digests also agree at
  `1de6d5f51876cf9d0f4449a78f077f8b127a14add0504d5060da680fc5a443de`.
- The generation trace tree hashes to
  `9433a6f184dbbc1e7698f1747f5e1b86265c280bb25ebfa9555074b94f7c5c92`,
  equal to `usage.json`'s source-trace digest; its sole JSONL file also matches
  the SHA-256 recorded in the generation result.

The audit-only snapshot digest serialization is not specified in the mounted
records, so I did not misapply the pipeline tree algorithm to those differently
named values. Integrity is independently anchored by the reproducible
pipeline-v3 tree digests, every recorded regular-file digest, and the recursive
entry comparison.

### Trusted-input comparisons

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounted counterparts. The recursive semantics comparison covers path,
entry type, and bytes: the candidate has no missing, additional, mistyped,
changed, or symlinked `reference-semantics/` entry. This integrity result does
not bless `verification.k`; that file was reviewed separately below.

Stage 1 result: **PASS; no audit infrastructure breach**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks whether two string inputs contain the same characters.
Order and multiplicity are irrelevant; equality holds exactly when each
distinct character in either string occurs in the other. The trusted canonical
implementation is:

```python
return set(s0) == set(s1)
```

The candidate's `solution.py` has exactly the same executable expression and
signature. It applies to the full annotated two-string domain, including empty
strings and arbitrary lengths; it adds no alphabet, size, or non-emptiness
restriction.

### Translation and constructor identity

Using `/reference/py2mpy.py` in scratch regenerated a file byte-identical to
the submitted `solution.mpy`; both SHA-256 values are
`50ea732f523d5b7b821b7f2c3a1055e0456cf1e8b9b57d306d967066453a8d07`.
The exact command and exit statuses are in `evidence/stage2_checks.log`.

`evidence/program_pinning_check.py` also tokenized constructor structure rather
than comparing prose. The `FuncDef` subtree in regenerated `solution.mpy` and
the first `FuncDef` actually placed under the spec's `#loadAll(Module(...))`
each has 48 constructor tokens and SHA-256
`a8edb3dd02388dd851c73108c4760512f0dc4907a8354c5b4f442645a39e03b8`.
They are identical. The spec then appends only a harness assignment that calls
the loaded binding.

### Independent differential test

`evidence/differential_test.py` imports the scratch candidate and trusted
canonical as separate modules. It checks:

- all six documented examples;
- 16 explicit boundaries covering empty inputs, equality, order,
  multiplicity, a unique character on either side, case, whitespace, NUL,
  composed/decomposed Unicode, and astral characters;
- all 342,225 ordered pairs of the 585 strings of lengths 0 through 3 over an
  eight-code-point alphabet; and
- 5,000 deterministic wider-Unicode pairs generated with seed `540054`.

All 347,247 pairs agree, and all explicit expected results hold. This is finite
fidelity evidence, not a substitute for the K theorem.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

`evidence/prepare_scratch.log` shows the fresh source copy under
`/tmp/audit-work/54-same-chars`. It copied the trusted semantics, prompt,
translator, and canonical solution plus only candidate source proof artifacts.
It copied neither `runtime-kompiled/` nor `verification-kompiled/`.

`evidence/run_stage3_reconstruction.sh` records the exact commands, while
`evidence/stage3_reconstruction.log` preserves their bounded output and status.
The observed tools were `kompile`, `krun`, and `kprove` version `7.1.293`.

The concrete definition was freshly built with:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Fresh reviewer-authored concrete cases then terminated at `.K`, with `NoExc`
and exit code 0, and bound:

```text
case_empty             true
case_empty_left        false
case_duplicate         true
case_reordered         true
case_different_left    false
case_different_right   false
```

The proof definition was freshly built with:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

The spec contains exactly one positive claim. Independently running:

```bash
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

exited 0 and printed exactly one line equal to `#Top`. The Haskell warnings are
only unused tail variables in the unrelated `strLt` rules. LLVM additionally
reports total-but-underspecified functions in unused float/map/join/subscript
families; none occurs in the proof dependency slice.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

There is one entry claim, `SPEC.same-chars`, and it has no `requires`
condition. Its free `S0:IntSeq` and `S1:IntSeq` range over arbitrary finite
integer sequences.

The pre-state is the supplied default module configuration:

- `<k>` contains `#loadAll` of the exact submitted function definition,
  followed by an assignment that calls `same_chars(str(S0), str(S1))`;
- environment 0 is the empty module scope with parent `-1`;
- `-1` is the fixed builtins scope;
- scope and heap allocation counters are 1 and 0;
- heap and stack are empty, return state is `noRet`, exception state is
  `NoExc`, and exit code is 0.

The post-state requires `.K`; the same module environment; a module-scope
closure containing the exact body; and:

```k
"result" |-> sameSet(dedupCodes(S0), dedupCodes(S1))
```

It also fixes scope location 1, empty heap, heap location 0, empty stack,
`noRet`, `NoExc`, and exit code 0. The result is therefore neither free nor
tautological. It is an equality-bearing Boolean expression determined by both
inputs.

### Execution and binding

The claim executes rather than summarizes the program:

1. module loading sequences the exact `FuncDef` before the call harness;
2. the definition binds `same_chars` in module scope 0;
3. the call looks up that binding, creates a real callee frame, and binds
   `s0`/`s1`;
4. both `set` names resolve through the scope chain to the fixed builtin;
5. callee and arguments evaluate left-to-right;
6. both set constructions and set equality execute;
7. `Return` and frame pop restore the caller; and
8. the harness assigns the returned Boolean to `result`.

There is no helper or loop claim and no body summary to align with control
flow. The constructor comparison in Stage 2 establishes program identity. The
fresh changed-body probe in Stage 6 materially changes the `FuncDef` inside
`#loadAll` itself, not merely an external Python file.

### Satisfiable witnesses and concrete substitution

The default configuration with `S0 = .IntSeq` and `S1 = .IntSeq` satisfies the
entry precondition and yields true. Other witnesses include `"a"`/`"aa"`
(true), `"a"`/`"b"` (false), `"ab"`/`"bbaa"` (true), and `"abc"`/`"ab"`
(false).

`evidence/ground_substitution_check.py` substitutes the corresponding integer
code sequences into `sameSet(dedupCodes(S0), dedupCodes(S1))` and compares that
value with both Python implementations. All six ground substitutions agree.
The fresh LLVM run independently agrees on the same branch boundaries.

### Domain alignment

The theorem has no length bound and is not a finite unrolling. `str(IntSeq)`
is at least as broad as the intended finite Python-string character-sequence
domain. The supplied literal parser is ASCII-only, but the symbolic theorem
does not use `Str` literals for its inputs; it directly quantifies over all
`IntSeq` strings. Character-set equality depends only on equality of character
codes, so an injective Unicode code-point representation preserves the
property. The formal domain is broader (it admits arbitrary integers) rather
than materially narrower.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.tsv`, generated by
`evidence/k_rule_inventory.py`, contains every local declaration in
`semantics.k`, all 23 supplied helper K files, `verification.k`, and `spec.k`.
It has:

- 695 rules;
- 227 syntax declarations;
- one configuration, five contexts, and one claim;
- 146 `[function]`, 107 `[total]`, 45 priority-bearing, 36 `[concrete]`,
  and 22 `no-evaluators` records;
- no `[functional]` and no `[simplification]` record.

Per-row text, source location, attributes, reachability classification, and
audit disposition are preserved in that TSV. The 22 opaque declarations are
listed separately in `evidence/opaque_inventory.tsv`; all are unused MD5,
float, or sort symbols. All priorities are in
`evidence/priority_inventory.tsv`. The proof/spec-only records are in
`evidence/proof_local_inventory.tsv`.

Most importantly, `verification.k` has zero local semantic declarations. It
only requires trusted `semantics.k` and imports `MPY`; there is no
proof-specific function, totality assertion, equation, simplification,
priority, rewrite, opaque symbol, operational bridge, oracle, or auxiliary
claim. `MPY-CONCRETE` is not imported by the Haskell proof definition; the
fresh compiled rule manifest has zero `concrete.k` records.

### Dependency slice and rule decisions

`evidence/dependency_slice_review.md` gives the complete constructor mapping
and grouped per-rule decisions. The material slice comprises:

- default configuration, module loading, and statement sequencing;
- exact `FuncDef` closure creation;
- plain-frame lookup plus builtin-scope fallback;
- callee-first and left-to-right argument evaluation;
- ordinary closure frame creation, parameter binding, return, pop, and
  assignment;
- comparison contexts and dispatch;
- `applyBuiltin("set", str(CS), .Vals)`;
- `codeIn`, `dedupCodes`/`dedupFrom`, `snocCode`, `subsetCodes`, and
  `sameSet`.

Every material equation is valid on its full guard:

- the cell lookup/write priority rules require a `"$cells"` marker absent from
  both real frames, so they are disjoint from this path;
- heap-dereference priorities require `ref` operands, while the inputs and
  `setV` results are bare values;
- special math/hash/sort call rules have different constructor heads and
  cannot intercept either `set` call;
- set-helper base/constructor equations cover the algebraic lists;
- the guarded `dedupFrom` branches use complementary Boolean conditions and
  recursively consume their input;
- `snocCode` and `subsetCodes` structurally descend; and
- `sameSet` is precisely mutual membership, so order and multiplicity are
  ignored as required.

No state-bearing execution is skipped. The call frame rules read/write the
environment, scopes, stack, return state, and scope counter; the postcondition
observes all of them plus heap, heap counter, exception, and exit code. Set
values are pure in this supplied semantics, so no hidden heap update is
discarded.

Every inventory row classified as supplied-but-unreached has a constructor
head, sort, operator, builtin/method name, or control form absent from all
reachable target states. The inputs are specifically `str(IntSeq)`, the
builtin calls specifically return `setV(IntSeq)`, and the comparison returns a
`Bool`; there is no unconstrained `Val` that can narrow into an unrelated
opaque family. The unused total/opaque facilities remain part of the declared
supplied-semantics trust boundary, not a claim that this is full CPython.
There is no false-conclusion witness on the intended two-string domain by
which an unused rule can affect this theorem.

I found no unsound rule contributing to the proof and therefore make no
unsoundness allegation requiring a false-conclusion witness.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I inspected the candidate's mutation files only as untrusted evidence and
created new probes:

- `evidence/audit-spec-vacuity.k` calls the exact original body on two empty
  strings but falsely demands `result = false`;
- `evidence/audit-spec-body-sensitivity.k` changes the function term executed
  under `#loadAll` to `return True`, calls it on disjoint `"a"`/`"b"` inputs,
  and retains the original false-result obligation.

`evidence/run_stage6_mutations.sh` and
`evidence/stage6_mutations.log` record exact commands and bounded output. Both
specs built with `kprove --dry-run` at exit 0. Both actual proofs exited 1,
printed `WarnStuckClaimState`, and showed `"result" |-> true` in the residual.
The body-sensitivity residual additionally retained the mutated
`Return(Bool(true))` closure. Thus neither failure is a parser error, missing
import, timeout, unrelated crash, or unreachable mutation.

The first probe shows that the positive claim constrains its result. The
second shows that a material change to the program term actually executed by
the claim changes the outcome and invalidates the expected theorem.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics and for every `S0:IntSeq` and `S1:IntSeq`,
starting from the stated default configuration, loading the exact translated
`same_chars` function and calling it on `str(S0), str(S1)` reaches the fully
observed clean final configuration with:

```k
result = sameSet(dedupCodes(S0), dedupCodes(S1))
```

The exhaustive fixed equations establish that this Boolean is true exactly
when the two finite sequences contain the same distinct integer codes. Under
the standard character-code bridge, that is exactly the prompt's
same-characters property. This is a universal, unbounded reachability theorem,
not a finite collection of examples. In Kit terminology, Gates A, B, and C
pass.

### Trust ledger

| Boundary | Influence | Dependents | Assessment |
|---|---|---|---|
| Trusted supplied `MPY` semantics and K builtin theories for integers, Booleans, strings, maps, lists, and equality | Defines execution, state, and the mathematical character-set operations | The sole target claim | Acceptable required semantics boundary. The candidate tree is identical to the trusted mount; every reached rule was reviewed. |
| K 7.1.293 compiler, LLVM/Haskell backends, and prover | Implements parsing, execution, and reachability checking | All dynamic proof evidence | Acceptable toolchain trust. Fresh positive and discriminating negative runs were reproduced. |
| Trusted `/reference/py2mpy.py` | Connects Python AST to the submitted K constructor term | Real-program identity | Acceptable translator boundary. Trusted regeneration is byte-identical, and constructor-level spec comparison is exact. |
| Python-string to finite `IntSeq` character-code representation | Connects HumanEval strings to the theorem domain | Intent adequacy | Acceptable informal representation bridge here: the property uses only equality/membership and is invariant under injective character encoding; the formal domain is broader, not bounded or narrowed. |
| The 22 opaque MD5/float/sort symbols in the supplied semantics | Could affect other programs using those facilities | None | Excluded from the Haskell target dependency slice; exact list is preserved in `opaque_inventory.tsv`. No proof-relevant opaque symbol exists. |
| Candidate/canonical differential tests and concrete K runs | Finite empirical source/semantic evidence | Fidelity and intent bridge only | Supporting evidence only; not used as a universal proof substitute. |

There is no proof-local trusted primitive, program-derived opaque value,
operational bridge, empirical oracle, assumed loop invariant, or unproved
helper claim. The source's `set` operation is an external builtin fixed by the
supplied semantics, but its string case and equality are exhaustively defined
rather than left unconstrained.

### Excluded behavior

The theorem is about two string values in the supplied MPY execution model. It
does not cover non-string calls, mutation of the module's builtin binding
environment, CPython allocation/hash performance, or unused partial-language
constructs. These are outside the HumanEval contract and do not narrow its
material input domain. As requested, the result is interpreted as
partial-correctness; no separate meta-proof of the K toolchain is claimed.

### Decision

The reconstructed target closes, the claim is satisfiable and
result-constraining, the exact generated function body is executed, the
unrestricted source-contract domain is covered, and no material unsound
semantics or proof extension contributes. The appropriate benchmark decision
is therefore `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
