# Independent adversarial review: 52-below-threshold

The candidate contains a legitimate universal reachability proof for the
integer-list domain of the HumanEval task. I rebuilt both definitions from
source, proved the helper and entry claims independently, ran the untouched
full specification, compared the proof's program term mechanically with the
trustedly regenerated submission, audited every local declaration and rule,
and rejected fresh false body/postcondition mutations.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. The trusted
mount is consistent with that mode: `/reference/reference-semantics` does not
exist. No hidden or inferred reference semantics was used.

The campaign block in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`; the lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
the recorded value. All launcher-declared container paths are present with the
required regular-file or real-directory type. Recursive scans found no
symlinked or unsupported entries in `/candidate`, `/reference`, or
`/generation-evidence`.

I read the required legacy-selected-stage1 records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and `usage.json`;
- the complete structured trace under `codex-trace/`.

`runtime-metrics.json` is absent, as permitted for this historical layout.
The additional `legacy-metrics.json` and `legacy-run-input.json` records are
present and match the hashes in the selected-stage evidence map.

Every audit-input file hash with a mounted byte object matched independently,
including:

| Object | SHA-256 |
|---|---|
| trusted/candidate prompt | `b8e47fee4b6fffb27f872307ef74803b1e427e22802413851b9f0c61bb05306e` |
| trusted/candidate translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| trusted canonical | `8366f2dfbca9cf6e22f4bf243182d627708a738a2dec04ffd8b37a580416f1d2` |
| run manifest | `16ab5496e5b7251ecd747d4b58693a614cb2f6d680317214f597d0437ab39c24` |
| task manifest | `e32a4e466e0ac27d2a711384dad7bb15754f335c200622f09ba4ed06d6714e64` |
| stage-1 result | `19174c6340545e98e0a0f5b8216d27d017bb121a5c21f99fb577970cad41a94d` |
| invocation | `05ba3cd6cd8c39ee467997bd98d57f4388f74809c48b722b157985cea8799464` |
| generation output | `b649bfe03461b86b9811ef148f7119cb4575c15766e8bffd1af31a45ad999e50` |
| structured trace file | `2d49fce8dac3d29afb9fa83d65784ec65c42b447ba07c95f7807e5f5878619d3` |

Using the pipeline's documented content-tree algorithm, the mounted candidate
hash is
`08cd07c4989c2c1d70ef03650a7f884cfc26a5488e8da37c8c1528ac309d1d6a`,
exactly the retained workspace hash in both the invocation and stage-1 result.
The trace tree hash is
`1db38dc82f0eaf252b7b8020c484d68ea4f0d1da1af3e49e2178340ffb931050`,
exactly `usage.json`'s source-trace hash. The audit record also carries
launcher-specific aggregate snapshot digests; their values are recorded in the
evidence log, while the selected invocation and every constituent evidence
file provide the independently reproducible mount binding.

The candidate prompt and translator are byte-identical to their trusted
versions. The structured trace contains 218 valid JSON records, zero malformed
records, and 44 recorded tool/function calls. I treated its prior `#Top` and
final report only as untrusted historical claims.

Evidence:
[provenance checker](/audit-output/evidence/provenance_check.py),
[provenance log](/audit-output/evidence/01-provenance.log),
[trace inventory](/audit-output/evidence/trace_inventory.py), and
[trace log](/audit-output/evidence/01-trace.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and source comparison

On the benchmark's integer domain, `below_threshold(l, t)` takes a finite list
of integers and an integer threshold and returns `True` exactly when every
element `e` satisfies `e < t`. Equivalently, it returns `False` as soon as some
element satisfies `e >= t`; the empty list returns `True`.

The trusted canonical loops over `l`, returns `False` on `e >= t`, and otherwise
returns `True`. Candidate `solution.py` is the same algorithm with the loop
variable renamed from `e` to `x` and the docstring omitted. Neither difference
changes execution.

I copied only source artifacts into `/tmp/audit-work/rebuild-52`. Running the
trusted `/reference/py2mpy.py` on the copied `solution.py` produced
`solution.regenerated.mpy`. It is byte-identical to submitted `solution.mpy`;
both hashes are
`ab83d1f82b73af6aa67b6272b8cce230d0a9034553bfa8fd44c9ab3f751a9186`.

Exact regeneration command and result:
[command](/audit-output/evidence/02-regenerate-mpy.command),
[log](/audit-output/evidence/02-regenerate-mpy.log), exit `0`.

### Independent differential test

The reviewer-authored test imports the trusted canonical and copied candidate
by distinct file paths and also uses the independent oracle
`all(x < t for x in l)`. Its input scope is:

- 14 named prompt, empty, equality, branch-position, negative, and large-integer
  cases;
- exhaustive lists of lengths 0 through 4 over elements `-3..3`, with
  thresholds `-3..3`;
- 2,000 deterministic random lists of lengths 0 through 30 over
  `[-10^12, 10^12]`, seed `520052`.

All 21,621 comparisons agreed; mismatch count was zero. The deterministic
input/result stream hash was
`4419af4b0feaa6bd04ea22b6751056d91e489b46ec5b5cdae1ac737265a71e35`.
This is finite fidelity evidence, not a replacement for the K proof.

Evidence:
[test script](/audit-output/evidence/differential_test.py),
[command](/audit-output/evidence/02-differential.command), and
[log](/audit-output/evidence/02-differential.log), exit `0`.

## 3. Clean proof reconstruction

No candidate-compiled definition or cache was copied. The scratch tree began
with `semantic.k`, `verification.k`, `spec.k`, `solution.py`, and
`solution.mpy` source, plus trusted reference copies.

### Fresh concrete definition

Command:

```text
/usr/bin/kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled
```

It exited `0`. See
[command](/audit-output/evidence/03-kompile-concrete.command) and
[log](/audit-output/evidence/03-kompile-concrete.log).

Eight fresh `krun` executions exercised every used control-flow outcome:

| Case | K result | Python/math result |
|---|---:|---:|
| prompt true | `true` | `true` |
| prompt false | `false` | `false` |
| empty list | `true` | `true` |
| element equals threshold | `false` | `false` |
| negative values pass | `true` | `true` |
| first element fails | `false` | `false` |
| last element fails | `false` | `false` |
| 100-digit integer boundary passes | `true` | `true` |

Every run exited `0`, ended with `<k> .K </k>`, and had the expected
`<result>` cell. Evidence:
[comparison script](/audit-output/evidence/concrete_compare.py),
[command](/audit-output/evidence/03-concrete-compare.command), and
[bounded output](/audit-output/evidence/03-concrete-compare.log).

### Fresh proof definition and positive claims

The Haskell proof definition was built with:

```text
/usr/bin/kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-haskell-kompiled
```

It exited `0`; see
[command](/audit-output/evidence/03-kompile-proof.command) and
[log](/audit-output/evidence/03-kompile-proof.log).

Positive proof reconstruction:

| Target | Isolation method | Exit | Output |
|---|---|---:|---|
| `SPEC.loop-invariant` | `--claims SPEC.loop-invariant` | 0 | `#Top` |
| entry claim | both labels retained; separately proved loop claim marked trusted only for this dependency-isolation run | 0 | `#Top` |
| untouched complete `SPEC` | no filtering or trusted flags | 0 | `#Top` |

Logs:
[loop claim](/audit-output/evidence/03-kprove-loop-invariant.log),
[entry with proved helper](/audit-output/evidence/03-kprove-entry.log), and
[untouched full spec](/audit-output/evidence/03-kprove-all.log).
Their exact commands and exits are in the adjacent `.command` and `.exit`
files.

An initial diagnostic that selected only the entry label removed the loop
circularity from the proof theory and consequently began unbounded symbolic
unrolling. I interrupted that altered-theory run after 150 seconds; it is
preserved as
[entry-alone diagnostic](/audit-output/evidence/03-kprove-entry-alone-diagnostic.log)
and is not used as positive-proof evidence. The actual helper was separately
proved, the entry closed with that proved dependency, and the untouched full
spec independently closed both claims.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable preconditions

`loop-invariant` starts at the exact loop head for the submitted loop body,
with remaining integer sequence `XS`, threshold `T`, the final
`Return(True)` continuation, arbitrary well-sorted prior `x`, and no result.
It says execution consumes the computation and returns exactly
`allBelow(XS,T)`. It is deliberately more general than reachable entry states:
`INPUT` need not be related to `XS`. That generality is sound because the loop
body reads only the current element and `t`; it never rereads `l` or
`<input>`.

A satisfying state is, for example, `XS = nil`, `INPUT = nil`, `T = 0`,
`x = unbound`, and `result = noResult`. The destination permits the actual
unchanged `x` through an existential final slot and requires `result(true)`.

`below-threshold-correct` starts from `boot`, the exact program macro, arbitrary
`XS:IntSeq` and `T:Int`, unbound argument/local slots, and no result. It says
the actual execution terminates with empty `<k>`, binds `l` and `t` to those
inputs, leaves some well-sorted final `x`, and returns exactly
`allBelow(XS,T)`. A satisfying state is `XS = nil`, `T = 0`, and all default
cells.

The result is not free, tautological, or one-way: the destination cell is
`result(allBelow(XS,T))`. Ground substitutions agree with both Python
implementations and concrete K execution: `nil,0` gives `true`;
`cons(5,nil),5` gives `false`; and
`cons(1,cons(2,cons(4,cons(10,nil)))),100` gives `true`.

### Mechanical program identity

I parsed `solutionProgram` in module `VERIFICATION` with macro expansion and
parsed trustedly regenerated `solution.mpy` in `MPY-SYNTAX`, both to KAST JSON.
The 4,224-byte JSON terms are byte-identical, with common hash
`03a98ad423b6b745e1371445002663d7995490d199e0bc1a3ce52d94ef27158e`.

Evidence:
[pinning command](/audit-output/evidence/04-program-pinning.command),
[pinning log](/audit-output/evidence/04-program-pinning.log),
[expanded macro](/audit-output/evidence/04-macro-expanded.json), and
[submitted MPY term](/audit-output/evidence/04-solution-mpy.json).
Together with trusted regeneration, this mechanically connects
`solution.py -> solution.mpy -> solutionProgram`. The omitted annotation and
docstring are transliterator-level, semantically inert metadata.

The loop claim's K suffix is the real control state produced by decomposing the
submitted `For` followed by `Return(True)`. The entry claim starts at the real
`boot`, which matches the exact function name, exact two parameters, and body.

### Body sensitivity

In a distinct scratch definition I changed the macro's actually executed final
statement from `Return(Bool(true))` to `Return(Bool(false))`, leaving the
postcondition unchanged. The mutated definition compiled (exit `0`), but
`kprove` exited `1` with `WarnStuckClaimState`. Its concrete residual is the
empty-list branch with `result(false)` where the theorem requires true. This
changes the program term used by the claim, not merely an external Python file.

Evidence:
[mutated source](/audit-output/evidence/verification-body-mutant.k),
[mutation build](/audit-output/evidence/04-body-mutation-kompile.log), and
[rejected proof](/audit-output/evidence/04-body-mutation-kprove.log).

## 5. Rule-by-rule static soundness review

The hash-bound source inventory is preserved in
[the static source log](/audit-output/evidence/05-static-source-inventory.log).
There are no generated helper K files besides `semantic.k`,
`verification.k`, and `spec.k`.

### Complete local declaration inventory

`MPY-SYNTAX` declares:

- `Pgm = Module(Stmts)`;
- `Stmts = List{Stmt,""}`;
- four `Stmt` constructors: `FuncDef`, `For`, `If`, and `Return`;
- `ParamItems = List{String,","}` and `Params`;
- three `Expr` constructors: `Name`, `Bool`, and `Compare`;
- `CmpOp`;
- `IntSeq = nil | cons(Int,IntSeq)`.

`MPY` declares:

- `Value = VInt | VBool | VList`;
- `Slot = unbound | slot(Value)`;
- `Result = noResult | result(Bool)`;
- nine control KItems: `boot`, `exec`, `eval`, `ifK`, `forK`, `loop`,
  `cmpRight`, `cmpValues`, and `returnK`;
- one `<bt>` configuration containing `<k>`, `<program>`, `<input>`,
  `<threshold>`, `<l>`, `<t>`, `<x>`, and `<result>`.

`VERIFICATION` declares `allBelow(IntSeq,Int):Bool [function,total]` and
`solutionProgram:Pgm [macro]`.

There are no local `[functional]`, opaque, priority, simplification,
`[concrete]`, or axiom declarations. The only total local function is
`allBelow`. The only claims are the loop circularity and entry theorem
inventoried above.

### Every operational rule

| ID and source | Complete role and soundness decision |
|---|---|
| S1 `semantic.k:57-64` | `boot` matches exactly one `below_threshold(l,t)` binding/body, copies the external `IntSeq`/`Int` arguments into the two slots, and starts that body. Sound entry-harness rule; it neither invents nor summarizes the result. |
| S2 `:67` | Empty statement execution becomes `.K`. Sound sequence base. |
| S3 `:68` | Executes the head statement before the tail. Sound left-to-right statement order. |
| S4 `:71` | `Bool(B)` evaluates to `VBool(B)`. Sound literal rule. |
| S5 `:72-73` | `Name("l")` returns the bound `l` value. Sound lookup for a used name. |
| S6 `:74-75` | `Name("t")` returns the bound threshold. Sound lookup. |
| S7 `:76-77` | `Name("x")` returns the current loop binding. Sound lookup. |
| S8 `:80-81` | Starts the submitted `>=` comparison by evaluating its left expression. Sound order. |
| S9 `:82-83` | After the left value, evaluates the right expression while retaining the left value. Sound order and binding. |
| S10 `:84-85` | With left `I1` and right `I2`, returns `I1 >=Int I2`. The apparently reversed pattern variable names still compute the correct operand order. Sound integer comparison. |
| S11 `:88-89` | Evaluates an `If` guard before either branch. Sound control order. |
| S12 `:90-91` | Boolean true executes only the then branch. Sound and disjoint from S13. |
| S13 `:92-93` | Boolean false executes only the else branch. Sound and disjoint from S12. |
| S14 `:96-97` | Evaluates the `For` iterable before entering iteration. Sound order. |
| S15 `:98-99` | Converts a `VList(XS)` into the explicit loop state. Sound representation step. |
| S16 `:100` | An empty remaining sequence consumes the loop. Ignoring target/body is sound because neither executes on an empty iterable. |
| S17 `:101-103` | A nonempty sequence binds `x` to its head, executes the real body, then loops over its tail. This preserves Python list iteration order and final loop-variable behavior. |
| S18 `:106` | `Return(E)` evaluates `E` and discards the remaining current-function computation. This semantics has one active entry frame and no calls/cleanup/exception stack, so every admitted suffix is the current function's continuation. The early-failure concrete cases show the following loop/final-true continuation is discarded. Sound for every used return. |
| S19 `:107-108` | A returned boolean empties `<k>` and changes `noResult` to exactly that boolean. Sound terminal return; the submitted function returns only booleans. |

The configuration footprint is complete for the submitted program. S1 writes
only argument slots; S17 writes only `x`; S19 writes only `result`; all other
cells are preserved unless explicitly read. There is no heap, output,
allocation, exception, function stack, or mutable list operation in the
program requiring an omitted cell. Every expression/statement rule is
deterministic on the used well-sorted states. The literal/name/comparison,
true/false, nil/cons, and `noResult` patterns have either disjoint match domains
or sequential control states, so there is no conflicting overlap.

### Verification rules and claims

| ID and source | Decision |
|---|---|
| V1 `verification.k:8` | `allBelow(nil,T) = true`. True definition of universal quantification over an empty sequence. |
| V2 `:9-10` | `allBelow(cons(I,XS),T) = (I<T) and allBelow(XS,T)`. True inductive definition; recursive descent is structural. |
| V3 `:14-21` | `solutionProgram` macro expands to the exact submitted term. This is a compile-time spelling, not an execution bridge; mechanical equality is established in Stage 4. |
| C1 `spec.k:8-25` | Sound loop circularity. Base `nil` executes final `Return(True)`. For `cons(I,XS)`, `I>=T` returns false, matching `I<T = false`; otherwise `I<T = true` and the claim recurs only after consuming one list element. |
| C2 `spec.k:27-37` | Sound entry theorem. S1-S15 execute the exact body to C1's loop-head configuration, then the proved loop result becomes the exact destination result. |

`allBelow` is total because `IntSeq` has exactly `nil` and `cons`; its rule
domains are disjoint, and V2 strictly descends. It is neither opaque nor an
oracle. No proof-local ordinary rewrite preempts program execution, and no
fresh result-bearing symbol appears in both semantics and postcondition.

Construct coverage is exact: submitted `Module`/`FuncDef`/`Params` are handled
by S1; `For` by S14-S17; `Name` by S5-S7; `If` by S11-S13;
`Compare`/`CmpOp(">=")` by S8-S10; `Return` by S18-S19; `Bool` by S4; and
statement lists by S2-S3. Missing semantics for unused Python constructs is
permitted in generated-semantics mode.

I found no unsound local rule, so there is no false-conclusion witness to
report against a rule. The rejected body and postcondition mutations instead
serve as positive sensitivity evidence.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I authored
[a fresh mutation](/audit-output/evidence/spec-vacuity.k) whose entry
destination requires
`result(notBool allBelow(XS,T))`. The starting state is satisfiable; at
`XS=nil,T=0` the real program and canonical return true while the mutation
requires false.

The mutated spec dry-run built successfully (exit `0`):
[command](/audit-output/evidence/06-vacuity-dry-run.command) and
[log](/audit-output/evidence/06-vacuity-dry-run.log).
The real proof then exited `1` with `WarnStuckClaimState`; its residual states
the failed implication between `allBelow(XS,T)` and its negation:
[command](/audit-output/evidence/06-vacuity-kprove.command) and
[log](/audit-output/evidence/06-vacuity-kprove.log).
This is the expected reachable unmet obligation, not a parser error, timeout,
or unrelated crash.

I additionally mutated the helper claim itself in
[spec-vacuity-loop.k](/audit-output/evidence/spec-vacuity-loop.k). It also
dry-ran successfully and then exited `1`, exposing the concrete `XS=nil`
branch with `result(true)` where false was required:
[dry run](/audit-output/evidence/06-vacuity-loop-dry-run.log) and
[rejected proof](/audit-output/evidence/06-vacuity-loop-kprove.log).
Thus both result-bearing claims discriminate false results.

## 7. Proven versus assumed accounting

### What is formally established

Under the rebuilt K theory, for every finite `XS:IntSeq` and mathematical
integer `T`, starting the exact submitted `below_threshold` function through
`boot` consumes its computation and produces:

```text
result(allBelow(XS,T))
```

where `allBelow` is structurally defined as true exactly when every sequence
element is strictly less than `T`. The proof is universal over sequence length
and integer magnitude; it is not a finite unrolling or bounded-size theorem.
It establishes the requested partial-correctness property (and the modeled
finite executions also reach a result).

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, kompiler, Haskell prover, LLVM runtime, and reachability-logic implementation | All parsing, execution, and proof closure | Standard low-level proof-tool trust boundary; version observed independently. |
| Imported K `INT`, `BOOL`, and syntax modules | Integer order, boolean conjunction/negation, tokens | Acceptable fixed primitives. No task answer is encoded in them. |
| Trusted `py2mpy.py` and CPython AST parsing | Source-to-constructor bridge | Launcher-designated trusted input; byte identity was rechecked and regenerated output matched exactly. |
| Generated `semantic.k` model of the used Python subset | Binding, iteration, comparison, branch, and return behavior | Audited rule by rule, state-footprint checked, concretely exercised on all used paths, and body-sensitive. It contains no oracle or answer shortcut. |
| Harness representation `list[int] <-> IntSeq`, `int <-> Int` | Connects Python inputs to K configuration | Direct structural representation preserving order and unbounded integers; supported by the concrete and differential evidence. |
| Trusted canonical and differential execution | Empirical source-fidelity support | Finite evidence only; not used as a substitute for the reachability proof. |
| `allBelow` | Final mathematical result | Proved by transparent exhaustive equations, not assumed or opaque. |
| `solutionProgram` | Program identity in both claims | Macro only; exact KAST equality to trustedly regenerated submission is mechanical. |

There are no opaque symbols, unconstrained fresh result values, empirical
operational bridges, assumed task lemmas, simplification rules, or priority
rules. The temporary `--trusted` flag in the entry-isolation run names only the
same loop claim already proved separately; the untouched full-spec run uses no
trusted claim flags.

The theorem's input sort is integer sequences. This matches the task's
integer threshold, all trusted examples, and the intended HumanEval integer
list domain. Python's implementation may incidentally accept floats, booleans,
or custom comparable objects; those behaviors, comparison exceptions, and
non-list iterables are outside this formal contract. Nothing in the trusted
task artifacts requires that broader accidental Python domain. The generated
semantics is intentionally minimal and visibly gets stuck outside its declared
subset.

Gate A (real-program soundness): pass. Gate B (intent adequacy): pass. Gate C
(trust and reproducible evidence): pass.

The fresh builds and proofs close, the postcondition is exact and
non-vacuous, the theorem is unbounded over the material source domain, the
actual regenerated program is pinned mechanically, and exhaustive static
review found no materially unsound rule or proof shortcut.

VERDICT: PASS
LEGITIMACY: LEGIT
