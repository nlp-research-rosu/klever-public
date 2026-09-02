# Independent adversarial audit: 23-strlen

This audit treats every candidate file, candidate log, generation trace, and
prior `#Top` as an untrusted claim. I followed the required `using-kit` then
`validating-proof` workflow, reconstructed the definitions from source in
`/tmp/audit-work/23-strlen`, and used only reviewer-authored evidence under
`/audit-output/evidence`.

The reconstructed theorem is legitimate. It executes the exact
trusted-regenerated program, covers arbitrary model strings rather than a
finite or ASCII-only subset, returns an exact recursively defined sequence
length, and contains no candidate-local proof rule or abstraction.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout = pipeline-v3`;
- `problem_id = 23-strlen`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `mount_reference_semantics = true`.

That is consistent with the mounted `/reference/reference-semantics`. There is
no rendered-mode/mount contradiction.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required file under
`/generation-evidence`, and the structured JSONL trace. The required
pipeline-v3 records are present as regular files, and the trace is a real
directory. The generation records say the candidate succeeded, but that claim
was not used as proof evidence.

Independent checks in `evidence/stage1_integrity.py` and
`evidence/stage1_integrity.log` established:

- the campaign lock JSON exactly equals the `audit_campaign` block;
- the campaign-lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value;
- every directly recorded regular-file digest checked for the run/task/result,
  invocation, metrics, runtime metrics, usage, prompt, output, final message,
  trace JSONL, canonical, trusted prompt, and trusted translator matches;
- both `/generation-result.json` and the invocation manifest name the same
  per-file evidence digests that were independently recomputed;
- all 218 JSONL trace records parse, with one task start, one final answer, and
  one task completion;
- the generation tree has no symlink or special-file entry;
- all six required candidate proof deliverables are regular files;
- all 775 candidate tree entries were independently typed and hashed, with no
  symlink or special-file entry. The reviewer manifest digest is recorded in
  the log.

The generation output was also scanned end-to-end for its command, success,
failure, and verdict claims; those untrusted claims are preserved in
`evidence/stage1_generation_claims.log`.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The candidate and trusted
`reference-semantics` trees contain exactly the same one subdirectory and 24
regular files. Relative paths, entry types, and every file digest agree. There
are no missing, additional, changed, mistyped, or symlinked semantics entries.
Thus the supplied-semantics integrity boundary passes.

There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for:

```python
def strlen(string: str) -> int:
    """Return the length of the given string."""
```

Its examples require `strlen("") == 0` and `strlen("abc") == 3`. The trusted
canonical implementation returns Python's `len(string)`.

The candidate implementation is:

```python
def strlen(string: str) -> int:
    return len(string)
```

It preserves the required signature and applies the same operation as the
canonical implementation on the intended string domain.

Using the copied trusted translator, the exact command

```text
python3 reference/py2mpy.py solution.py > solution.regenerated.mpy
```

exited 0. `solution.regenerated.mpy` and the submitted `solution.mpy` are byte
identical, both with SHA-256
`508c92dec7b8810291f0fa18ef567c25d5e8f398d62952cff2bd359697d6aebf`.
See `evidence/stage2_translation.log`.

The independent differential program is
`evidence/stage2_differential.py`; its complete generated input manifest is
`evidence/stage2_inputs.json`. It compared independently imported trusted and
generated entry points on:

- 13 named examples and boundaries, including empty, lengths one and two,
  whitespace, embedded NUL, combining text, precomposed text, BMP boundaries,
  astral characters, explicit surrogates, and length 4096;
- all 3,906 strings through length five over a five-character alphabet
  spanning ASCII, NUL, combining, BMP, and astral values;
- 1,000 deterministic generated strings of lengths 0 through 128, seed
  `230023`.

The implementation contains no conditional branch, so there is no omitted
branch boundary. All 4,919 comparisons matched. The exact command exited 0;
see `evidence/stage2_differential.log`.

Stage 2 passes.

## 3. Clean proof reconstruction

No candidate-provided `runtime-kompiled`, `verification-kompiled`, cache,
bytecode, proof log, or trace was copied into scratch. The scratch tree contains
the candidate source proof files, the trusted source semantics, trusted
translator, trusted prompt, and trusted canonical.

The live tools were K v7.1.293 and Python 3.10.12
(`evidence/tool_versions.log`).

### Fresh concrete definition

The exact fresh LLVM build was:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0 (`evidence/stage3_kompile_llvm.log`). A reviewer-authored concrete
program checked empty, one-character, prompt, whitespace, decimal, and
32-character cases. Trusted translation exited 0, and:

```text
krun stage3_concrete.mpy --definition audit-runtime-kompiled
```

exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>` (`evidence/stage3_concrete.py`,
`evidence/stage3_concrete_translation.log`, and
`evidence/stage3_krun.log`).

### Fresh proof definition and every positive claim

The exact fresh Haskell build was:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0 (`evidence/stage3_kompile_haskell.log`). A source claim inventory
found exactly one positive claim, `SPEC.strlen`; neither `verification.k` nor
the supplied semantics contains another claim
(`evidence/stage3_positive_claim_inventory.log`).

The independent target command was:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`
(`evidence/stage3_kprove_SPEC.log`).

The LLVM compiler reported non-exhaustive matches for several unused,
off-target helpers. The Haskell build/proof reported unused variables in
`strLt`. Static Stage 5 confirms none is reachable on this program path; these
warnings did not hide a target residual.

Stage 3 passes.

## 4. Adequacy and real-program pinning

### Plain-language claim

The sole entry claim has no `requires` clause. Its starting state is satisfiable
for every finite `CS:IntSeq`:

- the exact `strlen` module is about to be loaded;
- the next computation calls `strlen` on the model string `str(CS)`;
- environment 0 is active;
- module scope 0 is empty with builtin parent -1;
- the builtin scope is exactly `builtinsScope`;
- heap and stack are empty, allocation counters are zero/one as configured,
  return state is `noRet`, exception state is `NoExc`, and exit code is 0.

The destination requires:

- the exact computation result `isLen(CS)`, not a free result variable or an
  implication;
- module scope 0 to contain the exact loaded `strlen` closure and body;
- every other modeled cell to have the stated restored/unchanged value.

There is no helper or loop claim.

### Exact submitted program

`evidence/stage4_extract_claim_term.py` mechanically extracted the sole
`Module(...)` passed to `#loadAll` in the target claim. K's own parser then
parsed:

1. the trusted-regenerated `solution.mpy`; and
2. a rule wrapper around the extracted claim module, which permits the claim's
   explicit `.Exprs`/`.Stmts` list terminators.

`evidence/stage4_compare_kast.py` extracted the `#loadAll` argument from the
second KAST and compared it structurally with the first KAST. Both canonical
constructor trees have SHA-256
`032e542e6377aa1c7640c30eb5fa82bd139f9ae3b887daa42b7d0b4aa713c647`;
the comparison is exactly equal. Commands and results are in
`evidence/stage4_pinning.log`, with both KAST documents preserved.

This demonstrates the permitted surface normalization: the translator's
singleton statement/argument syntax and the spec's explicit internal list
terminators parse to the same constructors. The claim then calls the loaded
binding named `"strlen"` with `str(CS)`.

### Satisfying substitutions

Reviewer-authored ground claims instantiated the same precondition and program
at:

| Witness | K result | Trusted Python | Generated Python |
|---|---:|---:|---:|
| `CS = .IntSeq` / `""` | 0 | 0 | 0 |
| codes 97, 98, 99 / `"abc"` | 3 | 3 | 3 |
| code 128578 / `"🙂"` | 1 | 1 | 1 |

All three K claims proved together with `#Top` and exit 0. See
`evidence/stage4_ground.k` and `evidence/stage4_ground_kprove.log`.

### Body sensitivity

The fresh reviewer mutation `evidence/stage4_body_mutation.k` changes the
program term actually executed by the claim to `Return(Int(0))`, updates the
expected closure body consistently, and keeps the one-character result
obligation at 1. It parsed and executed, then exited 1 with
`WarnStuckClaimState` at `<k> 0 ~> .K </k>`. This is direct evidence that the
proof depends on the actual function body, not merely an external source file
or function name (`evidence/stage4_body_mutation.log`).

### Domain adequacy

The source contract's material domain is finite Python strings. The formal
domain is every finite `IntSeq`, including sequences broader than valid Python
character values. It therefore does not impose an ASCII, size, example, or
bounded-unrolling restriction. The supplied concrete `Str(String)` literal
front-end is ASCII-only, but the symbolic entry theorem starts from the
semantic value `str(CS)` and never uses that front-end. This is not a source
domain narrowing.

Stage 4 passes.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is `evidence/stage5_rule_inventory.md`, generated by
`evidence/stage5_rule_inventory.py`. It covers `semantics.k`, all 23 helper K
files below `semantics/`, `verification.k`, and `spec.k`. It contains 929
itemized source statements:

- 695 ordinary semantic rules;
- 227 syntax declarations;
- five contexts;
- one configuration;
- one claim.

It separately identifies 146 function declarations, 107 total declarations,
25 symbolic/opaque declarations, 45 priority-bearing rules, 35 concrete rules,
26 `owise` rules, and all syntax macros. There are no `functional` or
`simplification` declarations. The full source and command checks are in
`evidence/stage5_static_checks.log`.

`verification.k` contributes no declaration or rule of any kind. `spec.k`
contributes only the target claim. Thus there is no proof-local equation,
lemma, circularity, opaque result, priority rule, operational bridge, oracle,
or smuggled task answer.

The complete constructor/rule mapping and per-rule target-slice assessment are
in `evidence/stage5_target_slice.md`. The reachable path is:

1. `#loadAll` unwraps the exact module and statement sequencing executes the
   exact `FuncDef`.
2. The definition rule installs the exact closure in module scope 0.
3. Generic call routing resolves that closure through normal name lookup,
   evaluates the direct string argument left-to-right, creates a real frame,
   binds the real parameter, and executes the exact body.
4. The body resolves `"len"` by walking scope 1 → scope 0 → builtin scope -1.
5. Builtin dispatch rewrites only
   `applyBuiltin("len", str(CS), .Vals)` to `seqLen(str(CS))`, then exactly to
   `isLen(CS)`.
6. `Return` and `#pop` restore the saved caller continuation, environment,
   temporary scope allocation, stack, and return cell.

The two `isLen` equations are:

```text
isLen(.IntSeq)                => 0
isLen(iCons(_, S:IntSeq))     => 1 +Int isLen(S)
```

They are constructor-disjoint, exhaustive over finite `IntSeq`, and strictly
decrease on the tail. Ordinary structural induction establishes that they
count sequence elements. They are fixed supplied semantics, not a
candidate-created result oracle.

Priority and overlap checks found no alternate target route:

- closure-cell lookup/binding priorities require a `$cells` marker absent here;
- heap dereference priorities require `ref(H)`, while the argument is
  `str(CS)`;
- special call intercepts require `math.<fn>` or `hashlib.md5` syntax, not
  `Name("strlen")` or `Name("len")`;
- collection, loop, assertion, dict, sort, float, and concrete-only rules
  require constructors or control markers never produced by this path;
- `MPY-CONCRETE` is imported by the fresh LLVM definition but not by the
  Haskell `VERIFICATION` definition.

Every remaining inventoried rule was read and classified by its source
constructor/sort and guards. It is fixed supplied semantics and
target-unreachable from the fully pinned entry state. Some deliberately model
only an unused Python subset or leave unused operations opaque. No such rule
can unify with a reachable target intermediate or enable a conclusion about
this result. Under the required witness rule, there is no false-conclusion
witness on the intended `strlen` domain and no basis to label an off-slice rule
unsound for this theorem.

Stage 5 passes.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh reviewer artifact
is `evidence/stage6_false_result.k`. It executes the exact submitted body on
the satisfiable input `"abc"` but changes the required result from 3 to 4.

First:

```text
kprove stage6_false_result.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run
```

exited 0, proving the mutation parsed and built
(`evidence/stage6_false_result_build.log`).

Then the same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. The residual is exactly `<k> 3 ~> .K </k>` against the
required result 4, followed by the normal prover message that the
configuration cannot be rewritten further
(`evidence/stage6_false_result_kprove.log`). This is the intended unmet
result obligation, not a parser error, timeout, missing import, or unrelated
crash.

Stage 6 passes.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics and the exact pinned initial configuration,
for arbitrary finite `CS:IntSeq`, executing the exact trusted-regenerated
module and then calling its `strlen` binding on `str(CS)` reaches:

- computation result exactly `isLen(CS)`;
- the exact loaded module closure;
- restored caller environment, scope allocator, empty stack, and `noRet`;
- unchanged empty heap/heap allocator;
- `NoExc` and exit code 0.

Together with the fixed, exhaustive `isLen` equations, this is the requested
partial-correctness property: the function returns the number of elements in
the model string. It is not a proof of resource bounds, backend
implementations, or full Python semantics.

### Trust ledger

| Boundary | Exact content and dependents | Assessment |
|---|---|---|
| Supplied semantics | Configuration; module load; lookup; builtin registry; call/frame/bind/return/pop; `applyBuiltin("len", ...)`; `seqLen`; `isLen`; K's generated strictness rules. These determine all target value, control, and state behavior. | Acceptable and required by `SUPPLIED_SEMANTICS`. The candidate copy is byte-identical to the trusted mount, and the complete target slice was statically reviewed. |
| K builtin theories | `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, `K-EQUAL`, parser/list injections, and their hooks. | Standard low-level proof-engine boundary. The target needs only ordinary maps/lists, equality, and integer addition. |
| K implementation | K v7.1.293 parser, LLVM/Haskell compilers, runtime, and prover. | Standard toolchain trust. Fresh independent builds, positive proof, ground proofs, body mutation, and false-result mutation all behaved consistently. |
| Trusted translator | CPython AST mappings for module, function, parameter, return, call, and name. | Byte regeneration proves artifact identity, not universal translator correctness. For this tiny source, constructor-level KAST equality and direct mapping inspection make the bridge adequate. |
| String representation | A Python string is represented by one `IntSeq` element per Python string element; `str(CS)` is the semantic value. | Informal model-to-source bridge, but non-narrowing and directly aligned with Python `len`. Ground Unicode witnesses and 4,919 differential cases support it finitely. |
| Trusted canonical and CPython | The canonical `return len(string)` and Python executions are the independent source-level oracle. | Finite differential evidence only; it supports implementation/intent alignment and does not replace the universal K proof. |
| Opaque supplied symbols | Sorting: `sortVS`, `sortKeyVS`. Float/conversion: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`. Digest: `md5hexCodes`. | All 25 are target-unreachable and have no dependent target claim or result. They are neither used as a program-derived abstraction nor shared with the postcondition. |
| Finite concrete/differential evidence | LLVM assertions, three ground K/Python witnesses, and 4,919 Python differential cases. | Supports the tested bridges only. Universal closure comes from the reconstructed `kprove`, not these tests. |

### Gate results

- Gate A — real-program soundness: **PASS**. Exact body executes through fixed
  semantics, no extension bypasses it, result and state are constrained, the
  entry state is satisfiable, constructor pinning passes, and both body/result
  mutations are rejected for the expected reasons.
- Gate B — intent adequacy: **PASS**. The theorem covers every finite model
  string, a superset of the material Python string domain, and returns its
  element count. There is no fixed-size, example-only, bounded-unrolling, or
  ASCII restriction in the formal claim.
- Gate C — trust and evidence: **PASS**. Every dependency and opaque symbol is
  accounted for, every cited reviewer artifact exists with exact commands and
  statuses, and finite evidence is not presented as a universal theorem.

The clean proof closes, is non-vacuous, pins the real generated program, and
has no material soundness or adequacy gap. The correct benchmark mapping is
`PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
