# Independent adversarial audit: 26-remove-duplicates

The candidate contains a legitimate partial-correctness proof of the generated
program for the full HumanEval contract domain of finite integer lists. The
proof was rebuilt from source using the trusted supplied semantics, both
positive claims closed, the claim executes the exact translated program, and a
fresh false-result mutation was rejected for the intended reason. No
proof-local operational bridge, answer oracle, unsound lemma, or material
domain restriction is present.

The main reproducibility record is
`evidence/COMMAND_LOG.md`. Exhaustive static evidence is in
`evidence/K_RULE_INVENTORY.md` and `evidence/STATIC_REVIEW.md`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `26-remove-duplicates`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- a mounted trusted semantics at `/reference/reference-semantics`.

This agrees with the rendered audit condition. The trusted semantics exists,
so there is no mode/mount contradiction.

The audit campaign object in `/audit-input.json` is deeply equal to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded hash.

All pipeline-v3 records required by the prompt are present, readable regular
files or directories, and are not symlinks:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, `prompt.txt`;
  and
- the structured JSONL trace under `/generation-evidence/codex-trace`.

Their file hashes match the values recorded in `/audit-input.json` and
`/generation-result.json`. In particular, the run, task, result, invocation,
metrics, runtime metrics, usage, last-message, console-log, prompt, and trace
file hashes all matched. The complete 311-record JSONL trace parsed, all 51
recorded calls and 17 messages were inspected, and all 21,248 console-log
lines were read into bounded summaries. See
`evidence/GENERATION_TRACE_SUMMARY.md` and
`evidence/GENERATION_OUTPUT_SUMMARY.md`. These records were treated only as
historical claims.

The candidate prompt and translator are byte-identical to trusted mounts:

```text
prompt:     7823eea9be9599563c786fa16e792f3da2482016607d75ee06ca40b2d33c7dca
translator: 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
```

A recursive, no-dereference comparison of
`/candidate/reference-semantics` with
`/reference/reference-semantics` exited 0. Independent
symlink-sensitive manifests contain the same 25 entries and the same content
digest
`dd4afae8d7a4e2c1b06b8840d070f4d19aff1ba09e353f19de57e7f9c6af3fe3`.
There are no missing, additional, changed, mistyped, or symlinked semantics
entries. The full candidate tree has 783 independently inventoried entries
and zero symlinks; see `evidence/CANDIDATE_TREE_MANIFEST.txt`.

The source hashes also match the candidate's prose record, but that agreement
was not used as proof evidence. Candidate-built `runtime-kompiled`,
`verification-kompiled`, bytecode, logs, and caches were not used.

The generation run records a generation-time Kit commit distinct from the
later audit-campaign Kit commit. They describe different stages; the
audit-campaign block itself matches its lock exactly, and the actual proof was
reviewed against the mounted approved audit skills. This is not a mount or
provenance contradiction.

No audit infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires:

> For a list of integers, remove every value that occurs more than once, while
> preserving the order of the values that remain.

The documented example maps `[1, 2, 3, 2, 4]` to `[1, 3, 4]`.

The trusted canonical implementation constructs a `Counter` and retains each
input element whose counter value is at most one. Because the predicate is
tested only on elements drawn from the input, each tested count is at least
one; canonical `count <= 1` is therefore equivalent to `count == 1`.

`solution.py` iterates the input in order, checks
`numbers.count(number) == 1`, appends exactly those values, and does not
mutate the input. It accepts arbitrary finite list lengths and arbitrary
Python integer signs and magnitudes.

Trusted regeneration was run in scratch:

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated terms have identical
SHA-256
`0a1f3742d1a9870e83de95c510044b37d3cf3899be7c16f12e61b33bea7360de`.

The independent script `evidence/independent_differential.py` imports the
trusted canonical and generated functions separately. It tests ten named
cases, every sequence of lengths 0 through 6 over `{-2,-1,0,1,2}` (19,531
cases), and 3,000 deterministic generated lists of lengths 0 through 60 with
large signed integers. It includes empty, singleton, exactly-two,
exactly-three, mixed multiplicity, all-unique, all-repeated, prompt, negative,
zero, and unbounded-large-integer cases. It also checks that neither function
mutates its input and independently evaluates the claimed `rdAcc` equations.
All 22,541 cases matched.

This is finite fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/audit-26`, using trusted
prompt, canonical, translator, and supplied semantics plus candidate
`solution.py`, `solution.mpy`, `verification.k`, and `spec.k`. No candidate
definition or cache was copied.

The live toolchain is K v7.1.293 for `kompile`, `krun`, and `kprove`, with
Python 3.10.12.

A new LLVM definition was built as `runtime-audit-kompiled`. The independent
`evidence/k_smoke.py` was translated with the trusted translator and executed.
Its six assertions cover empty, singleton, duplicate-pair, prompt,
negative/mixed, and very large integer inputs. `krun` exited 0 with `.K`, an
empty stack, `noRet`, `NoExc`, and exit code 0; its heap exposed the expected
result lists.

A new Haskell proof definition was built as
`verification-audit-kompiled`:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0. The focused loop target then exited 0 and printed `#Top`:

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.remove-duplicates-loop
```

The complete unfiltered proof also exited 0 and printed `#Top`:

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

The unfiltered command proves both positive claims jointly, making the proved
loop claim available as the entry claim's circularity. Thus every positive
target is included in an independently successful run. The only Haskell
warnings concern unused tail variables in trusted string-order equations.

The LLVM compiler additionally noted non-exhaustive cases for six unrelated
total functions. None is reachable from this integer-list program or its
proof; their disposition is recorded in stage 5.

## 4. Adequacy and real-program pinning

### Loop claim

`SPEC.remove-duplicates-loop` assumes:

- `<k>` begins with the exact submitted `#loop` term and loop body, followed
  by an arbitrary framed continuation;
- the active scope binds `numbers` to the complete unboxed list `ALL`,
  `result` to heap reference `H`, and `number` to some current value;
- heap `H` contains accumulator sequence `ACC`; and
- `REST` and `ALL` contain only K integers.

It establishes that the loop term is consumed, the same continuation and
framed cells remain, the unobservable final local `number` has some actual
value, and heap `H` contains `rdAcc(ACC, REST, ALL)`.

The claim is satisfiable. One witness is `L=1`, `H=0`,
`ALL=REST=vCons(1,.ValSeq)`, `ACC=.ValSeq`, `number=0`, a scope map containing
the stated three bindings and parent 0, and a heap map containing
`0 |-> list(.ValSeq)`.

### Entry claim

`SPEC.remove-duplicates` assumes the standard initial MPY configuration and
an arbitrary finite `INPUT` satisfying `allInts(INPUT)`. It loads the module
term, creates the exact function closure, calls it on `list(INPUT)`, and
requires normal cleanup.

The destination constrains the returned value to `ref(0)`, the only heap
entry to `0 |-> list(rdAcc(.ValSeq,INPUT,INPUT))`, heap location to 1, the
module and builtins scopes, an empty stack, `noRet`, `NoExc`, and exit code 0.
The return is therefore not a free variable, tautology, or one-way
implication.

The empty input and the prompt input are concrete satisfying states. Direct
substitution gives:

```text
rdAcc([], [], []) = []
rdAcc([], [1,2,3,2,4], [1,2,3,2,4]) = [1,3,4]
rdAcc([], [7,7], [7,7]) = []
```

These equal both trusted-canonical and generated-Python results in the
independent differential evidence.

### Mechanical program identity

`evidence/extract_claim_program.py` balances and extracts the sole `Module`
under the entry claim's `#loadAll`. K's program parser parsed regenerated
`solution.mpy`; K's rule parser parsed the claim spelling, including explicit
empty-list constructors. `evidence/compare_program_ast.py` then compared the
normalized K ASTs. Both module ASTs have SHA-256
`9795cb92042d4dc5299d1cbba98d933d9e025056ba24e034b3a8e74cb1c86937`
and are deeply identical.

Thus the claim executes the same function name, parameter, binding, and body
as trusted regeneration. No typing-only normalization beyond parser
canonicalization was needed.

The independent body-sensitivity artifact
`evidence/spec-body-sensitivity-audit.k` changes the executed comparison to
`count == 2` while retaining the original result summary. It dry-builds, then
exits 1 with `WarnStuckClaimState` on the expected
`1 #Equals cntOccVS(ALL,V)` path. The theorem is sensitive to a material body
change.

The formal domain is every finite K `ValSeq` whose elements are integers.
There is no bound on length, sign, magnitude, or multiplicity. Separate K
Boolean values are excluded, consistent with the benchmark's ordinary
`List[int]`/“list of integers” domain; this is not a finite-size or example
restriction.

## 5. Rule-by-rule static soundness review

`evidence/K_RULE_INVENTORY.md` exhaustively enumerates every selected local
syntax declaration, function, total declaration, opaque symbol, priority
rule, ordinary rule, context, configuration, and claim. Its key totals are:

```text
26 files; 229 syntax declarations; 699 rules
461 equational rules; 238 operational rules
148 function declarations; 109 total declarations
0 functional declarations; 0 simplification rules
45 priority rules; 26 owise rules; 22 opaque symbols
```

`evidence/STATIC_REVIEW.md` supplies the per-rule disposition and the complete
constructor-to-rule map. The material findings are:

- `allInts` has exhaustive, disjoint empty/nonempty equations and descends on
  the tail. It only restricts the theorem domain.
- `rdAcc` has exhaustive, disjoint empty/nonempty `REST` equations. Its sole
  recursive call descends on `REST`; its conditional is total. It is a
  definitional result summary and never rewrites `<k>`.
- There are no proof-local operational rules, priority rules, `owise` rules,
  simplifiers, opaque symbols, or trusted result primitives.
- The loop claim is an auxiliary reachability theorem/circularity over the
  exact fixed-semantics loop context, not a rule that skips an unproved
  program region.
- Fixed semantics executes the complete material path: module load and
  sequencing; typing-import no-op; closure creation; name lookup; callee and
  left-to-right argument evaluation; frame creation and parameter binding;
  list allocation; assignment; list iteration; target binding; count;
  integer equality; branching; in-place append; return; frame popping; heap
  preservation; and all final cells.
- `cntOccVS` splits on empty/equal-head/unequal-head cases with complementary
  guards and structural descent. Under `allInts`, its `==K` test is ordinary
  integer equality.
- Program `cntOccVS ==Int 1` and summary
  `1 ==Int cntOccVS` are equivalent by symmetry of integer equality.
- The reached append priority rule matches exactly the mutating receiver and
  preserves the heap location while appending one element. All other priority
  call patterns are disjoint from this program.
- The 22 supplied opaque functions cover md5, floats, and sorting. None
  occurs in the program, proof extension, claims, reached path, or
  postcondition, so none influences a branch, result, state, exception, or
  proof obligation here.
- LLVM's unrelated uncovered total-function constructors likewise cannot be
  reached for any satisfying `List[int]` input.

Every inventoried rule was assigned either proof-local/reviewed,
fixed/reached/reviewed, or fixed/unreached/accepted-as-the-selected-semantics
boundary. The unused rules share no globally active simplifier and no
matching reached redex that could discharge this theorem. No rule encodes
the task answer or creates an unconstrained result.

No rule was found unsound on the intended domain. Therefore no
false-conclusion witness is asserted; the required mutation witnesses test
discrimination rather than support an unsoundness allegation.

## 6. Fresh non-vacuity test

Candidate `spec-vacuity.k` was not reused. The reviewer-authored
`evidence/spec-false-result-audit.k` keeps the exact submitted program and
changes the concrete singleton result obligation from the true `[1]` to the
false `[99]`.

First:

```bash
kprove spec-false-result-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-FALSE-RESULT-AUDIT --dry-run
```

exited 0 and emitted the complete backend invocation. The mutation therefore
parses and builds.

The actual proof command exited 1 with `WarnStuckClaimState`, not a parser
error, timeout, or unrelated crash. Its final normal configuration contains:

```text
<k> ref(0) ~> .K </k>
<heap> 0 |-> list(vCons(1,.ValSeq)) </heap>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

This is the expected unmet result obligation: satisfying input `[1]`
actually returns `[1]`, not the mutated `[99]`. The positive proof is
non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### What is formally proven

Under the supplied MPY semantics, for every finite integer sequence `INPUT`
satisfying `allInts(INPUT)`, the submitted module and function body satisfy
this partial-correctness statement: if execution terminates from the specified
initial configuration, it returns the fresh result-list reference and the
referenced list contains exactly
`rdAcc(.ValSeq,INPUT,INPUT)`, with normal stack, return, exception, and exit
state.

The `rdAcc` definition retains an input element exactly when its total
occurrence count in the original input is one and processes elements
left-to-right. Consequently its empty-accumulator instance is precisely the
requested order-preserving list of values that do not occur more than once.

The proof does not establish termination or resource bounds; that is the
stated Kit partial-correctness boundary.

### Trust and assumption ledger

| Boundary | Effect on this theorem | Assessment and evidence |
|---|---|---|
| K v7.1.293 parser, kompilers, Haskell backend, solver, and reachability-logic implementation | Establishes parsing, symbolic execution, circularity, and `#Top` | Standard proof-checker trust boundary. Fresh builds, two positive runs, and two meaningful rejected mutations support correct use. |
| Supplied MPY semantics | Defines Python-subset binding, control, heap, integers, lists, `count`, `append`, call, and return | Required fixed boundary in `SUPPLIED_SEMANTICS` mode. Candidate copy is byte-identical to the trusted tree. Every reached rule was statically inspected and concrete boundary cases executed. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Translation implementation is outside the K theorem. Deterministic byte regeneration and K-parser AST identity connect the submitted translation and executed claim term. |
| K built-in integers, Booleans, maps, lists, equality, and arithmetic | Supplies ordinary mathematical operations used by semantics and summaries | Standard K prelude boundary. Only unbounded integer equality/count and finite algebraic sequences are materially used. |
| MPY-to-CPython adequacy | Connects the formal MPY theorem to the HumanEval Python contract | Not a universal formal refinement. The relevant rule slice was reviewed, source-level integer/list reasoning is direct, LLVM executed boundary cases, and 22,541 independent CPython differentials had zero mismatches. |
| Supplied opaque md5/float/sort symbols | None | They have no dependent claim or reached term in this proof. Their interpretations cannot change this theorem's result or control. |
| Candidate prose, traces, caches, and prior `#Top` | None | Treated solely as untrusted historical claims and independently reconstructed. |

Gate A passes: the exact body executes under fixed semantics, every
proof-local extension is sound, the result is constrained, and both result
and body mutations are rejected. Gate B passes: the theorem covers the full
material source-contract domain and the summary is the requested property.
Gate C passes: trust boundaries and finite evidence are explicit and all
reviewer evidence is reproducible below `/audit-output/evidence`.

VERDICT: PASS
LEGITIMACY: LEGIT
