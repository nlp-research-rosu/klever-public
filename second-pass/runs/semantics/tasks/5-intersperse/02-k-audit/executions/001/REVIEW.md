# Independent adversarial audit — 5-intersperse

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied semantics. The proof was rebuilt from source, all
dependency-closed positive targets returned `#Top` with exit 0, the entry claim
pins the parsed submitted `.mpy` AST, and a fresh false-result mutation was
rejected after real execution exposed the correct result.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, solely because
four requested generation-provenance artifacts are absent. That prevents an
independent check of the generation narrative and metrics, but it does not
affect the reconstructed proof.

## 1. Input and provenance integrity

### Mode and trusted mounts

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mount is consistent
with that mode; there is no infrastructure breach. I did not invoke the
generated-semantics workflow.

The recursive, no-symlink-dereference comparison of
`/candidate/reference-semantics` with the trusted tree returned exit 0.
Relative entry names and types are identical: one directory, one helper
directory, and 24 regular `.k` files; there are no symlinks, missing entries,
extra entries, type changes, or content changes inside the candidate semantics
tree. See [01_integrity.log](/audit-output/evidence/01_integrity.log) and its
reproducible driver
[01_integrity.sh](/audit-output/evidence/01_integrity.sh).

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted counterparts:

- prompt SHA-256:
  `388474ac71e5b893802f5971102df2e4ea82ddf2f916a4a55361c19370f54012`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

### Missing and auxiliary artifacts

The following explicitly requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace-like file was present. A structured generation trace was
required to be read only “when present,” so its absence is recorded but not
treated as an additional mandatory-file failure.

The candidate has auxiliary `prove.sh`, concrete test sources, a Python
`__pycache__`, and proof/source files. These are regular entries, not symlinks.
The cache was ignored, never copied into the proof scratch area, and never used.
No candidate-provided kompiled K definition was present or reused. `PROOF.md`
was also absent, so no prose proof claim was available to rely on.

Live tools were independently available: K `v7.1.337` and Python `3.10.12`.

Stage 1 result: source and supplied-semantics integrity pass; provenance
packaging has the four-file limitation above.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, the contract is:
for a list of integers `numbers` and integer `delimeter`, return a fresh list
containing the same elements in order, with `delimeter` inserted between every
two consecutive elements. The empty list returns empty; a singleton is
unchanged.

The submitted `solution.py` creates a new empty list, traverses `numbers` once,
appends the delimiter before every element except the first (detected by
nonempty result truthiness), appends the element, and returns the new list. It
does not modify `numbers`. This is a different but equivalent algorithm to the
canonical slice-based implementation on the intended `List[int] × int` domain.

### Trusted translation identity

I regenerated `solution.mpy` in scratch with the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

The command exited 0. `cmp` and `diff` both exited 0, and both files have
SHA-256
`280eebaf33f134914b4a86291b12cbcbc1a4f1e43338807d881f8de4243d413d`.
The commands and output are in
[02_fidelity.log](/audit-output/evidence/02_fidelity.log).

### Independent differential test

The reviewer-authored test
[02_differential.py](/audit-output/evidence/02_differential.py) imports the
trusted canonical entry point from `/reference/canonical.py` and the scratch
copy of the candidate entry point. Its deterministic input stream comprises:

- both documented examples;
- nine explicit empty, singleton, pair, repeated-zero, negative, and large-int
  boundary cases;
- every list of length 0 through 5 over `[-2,-1,0,1,2]`, crossed with seven
  delimiters (27,342 cases);
- 500 seeded generated lists of length 0 through 20.

The complete 27,853-case stream is fixed by seed 5005 and SHA-256
`0d220ea6e91b28a418f68d61db70a68faa5a5be413ecf3cf1bc8eddf61b453b3`.
There were zero result mismatches, zero input mutations, and zero non-fresh
results. The command exited 0. The script itself defines all inputs, and the
scope, digest, command, status, and results are preserved in
[02_fidelity.log](/audit-output/evidence/02_fidelity.log).

Stage 2 result: pass.

## 3. Clean proof reconstruction

All source artifacts required for execution were copied to
`/tmp/audit-work/candidate`; build outputs remained below `/tmp/audit-work`.
Before the first build, a search found no `*-kompiled` or `.kompile-*`
directory. Source hashes were recorded before compilation.

### Fresh concrete definition

The supplied semantics was freshly compiled with LLVM:

```text
kompile /tmp/audit-work/candidate/reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/candidate/runtime-kompiled
```

It exited 0. A reviewer-authored concrete program containing the exact submitted
function body plus six normal/boundary assertions was translated with the
trusted translator and executed with the new definition. `krun` reached a final
`<k> .K </k>`, normal exception/exit cells, and exited 0. The result heaps show
the expected empty, singleton, pair, example, repeated-zero, and negative cases.
See [03_concrete_program.py](/audit-output/evidence/03_concrete_program.py) and
[03_reconstruct.log](/audit-output/evidence/03_reconstruct.log).

The LLVM compiler emitted non-exhaustive-match warnings for unrelated supplied
helpers (`mapStrVS`, several float conversions, and `joinCodes`). None is on the
submitted path. They are fixed-semantics warnings, not candidate proof
extensions.

### Fresh proof definition and original spec

The proof definition was freshly compiled:

```text
kompile /tmp/audit-work/candidate/verification.k \
  --backend haskell \
  --main-module INTERSPERSE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/candidate/verification-kompiled
```

It exited 0. The exact submitted spec was then run:

```text
kprove /tmp/audit-work/candidate/spec.k \
  --definition /tmp/audit-work/candidate/verification-kompiled \
  --spec-module INTERSPERSE-SPEC
```

It printed `#Top` and exited 0. Full bounded output is in
[03_reconstruct.log](/audit-output/evidence/03_reconstruct.log).

### Every positive target

For distinct commands, I added labels only—the claim bodies are unchanged—and
selected each target with its required circularity dependency closure:

| Target | Required claims in that run | Result |
|---|---|---|
| empty loop | `loop-empty` | `#Top`, exit 0 |
| recurrent loop | `loop-rest` | `#Top`, exit 0 |
| first iteration | `loop-first,loop-rest` | `#Top`, exit 0 |
| entry | all three loop claims plus `entry` | `#Top`, exit 0 |

The labeled but otherwise identical spec is
[03_spec_labeled.k](/audit-output/evidence/03_spec_labeled.k); exact commands,
outputs, and statuses are in
[03_claim_dependencies.log](/audit-output/evidence/03_claim_dependencies.log).

An early diagnostic attempt removed the recurrent claim and tried
`loop-first` alone. It was interrupted because that malformed isolation removes
the circularity the target explicitly needs; it is not a failed candidate
target. It is retained transparently in
[03_isolation_diagnostic.log](/audit-output/evidence/03_isolation_diagnostic.log)
and
[03_claim_selector_diagnostic.log](/audit-output/evidence/03_claim_selector_diagnostic.log).
The dependency-closed commands above are the positive-target results.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **Empty loop.** If `result` points to an empty list and the remaining
   iterator is empty, the loop consumes no control, scope, or heap state.
2. **First/nonempty loop.** Starting with an empty `result` and at least one
   input value, execute the actual loop. On completion, `result` is exactly
   `intersperseAcc(empty,input,D)`, and local `number` is the last iterated
   value.
3. **Recurrent loop.** Starting with a nonempty accumulator and any remaining
   tail, execute the actual remaining loop. Each iteration appends `D` then its
   value; the heap becomes `intersperseAcc(accumulator,tail,D)`, and `number`
   becomes the last value if the tail is nonempty.
4. **Entry.** From the exact module/builtin initial state, load the submitted
   function and call it on semantic list `NUMBERS` and integer `D`. It returns
   `ref(0)`; heap location 0 contains exactly
   `list(intersperseVS(NUMBERS,D))`; allocation, scope, stack, return,
   exception, and exit cells have the stated final values.

The formal domain inferred from the K sorts is
`NUMBERS:ValSeq` and `D:Int`. It includes the intended lists of integers and is
soundly broader in element type: the program never operates on an element, it
only carries it through append. The delimiter remains constrained to `Int`.

### Program identity

The balanced `Module(...)` inside the entry claim was independently extracted.
K rule syntax spells empty lists as `.Exprs`/`.Stmts`, so only those identity
tokens were rendered as their empty program-surface forms. Both that term and
the submitted `solution.mpy` were parsed by `kast` as sort `Module`. The two
canonical JSON K ASTs are byte-identical, both with SHA-256
`9797d16613167fd791090512f0c308f997734602e69719e10bf0d76da663ae30`.
See [04_extract_entry.py](/audit-output/evidence/04_extract_entry.py) and
[04_adequacy.log](/audit-output/evidence/04_adequacy.log).

Thus `<k>` executes the actual submitted translation; it does not call a
substituted function or summary redex.

### Satisfying states and ground substitutions

All preconditions are satisfiable. Representative states are:

- empty loop: `L=1`, `H=0`, empty remainder, empty heap list at 0, and no other
  `SCOPES`/`HEAP` entry at those keys;
- first loop: the same fresh frame/heap with remainder `[1,2,3]`;
- recurrent loop: local `number=1`, nonempty result `[1]`, and remainder
  `[2,3]`;
- entry: the exact displayed initial module configuration with
  `NUMBERS=[1,2,3]`, `D=4`.

For `NUMBERS=[]`, `D=4`, the claimed heap value reduces to `[]`. For
`NUMBERS=[1,2,3]`, `D=4`, it reduces to `[1,4,2,4,3]`. Reviewer ground entry
claims with those concrete post-heaps printed `#Top` and exited 0. Both Python
implementations returned the same values. Sources and results are in
[04_ground_spec.k](/audit-output/evidence/04_ground_spec.k),
[04_witnesses.py](/audit-output/evidence/04_witnesses.py), and
[04_adequacy.log](/audit-output/evidence/04_adequacy.log).

The result is not a free variable, tautology, existential oracle, or one-way
implication. It is the exact heap sequence reached through the returned
reference.

Stage 4 result: pass.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory covers `reference-semantics/semantics.k`, all
23 supplied helper `.k` files, and `verification.k`. It records the complete
source block and attributes for every anchor:

- 230 syntax declarations;
- one configuration;
- five contexts;
- 701 rules;
- 937 total declaration anchors.

The attribute inventory has 148 function-containing blocks, 110 total,
zero functional, 25 symbol, zero literal `opaque`, 22 `no-evaluators`,
45 priority, zero simplification, 35 concrete, 26 owise, four macro, two
strict, and one seqstrict-containing block.

Every anchor has an explicit assessment row in
[05_rule_decisions.csv](/audit-output/evidence/05_rule_decisions.csv):
84 used-path/overlap anchors, 844 fixed-semantics anchors unreachable from this
program, and nine proof-local function/rule anchors. Complete source blocks are
in [05_rule_inventory.md](/audit-output/evidence/05_rule_inventory.md), with
generation commands and count checks in
[05_inventory.log](/audit-output/evidence/05_inventory.log) and
[05_decisions.log](/audit-output/evidence/05_decisions.log).

The detailed module-by-module decision, construct map, cell/state analysis,
overlap analysis, and proof-local equation audit are in
[05_static_assessment.md](/audit-output/evidence/05_static_assessment.md).

### Used execution path

The active path is:

```text
#loadAll / statement sequencing
  -> no-op typing import
  -> bind exact closure
  -> resolve/evaluate call and bind two parameters
  -> allocate fresh result list at heap 0
  -> iterate the unboxed input list
  -> bind number
  -> dereference result for truthiness
  -> exact priority-40 list append mutation(s)
  -> return ref(0), pop frame, preserve heap
```

Strictness and manual call evaluation preserve left-to-right evaluation.
`If(ref(H),...)` correctly preempts generic truthiness, and exact mutating
`append` correctly preempts generic method dispatch. No rule mutates the input.
The entry postcondition accounts for the relevant control, environment, scope,
heap, allocation, stack, return, exception, and exit cells.

### Proof-local rules

`verification.k` has no semantic `<k>` rewrite, simplification, concrete rule,
priority, opaque symbol, oracle, or task-answer shortcut. It adds three total
mathematical functions with six equations:

- `intersperseAcc`: empty remainder returns the accumulator; empty accumulator
  plus a nonempty remainder starts with the first value; nonempty accumulator
  plus nonempty remainder appends delimiter/value and recurses;
- `intersperseVS`: calls `intersperseAcc` with an empty accumulator;
- `lastNumber`: returns the carried value on empty remainder and otherwise
  recurses with the next head.

The constructor cases are disjoint and exhaustive, and recursion strictly
decreases the second `ValSeq`. `intersperseAcc` uses the supplied truthful
`valSeqConcat` equations. These functions determine values; they never replace
a program redex.

The loop summaries are claims, not ordinary rules. They match the real
`#loop` control term and exact body. They quantify over arbitrary `CONT` and
are themselves proved under that full context, so there is no
broader-continuation bridge. The recurrent claim is a guarded circularity
reached only after real loop progress.

### Opaque and unused facilities

The 25 supplied symbolic/opaque candidates are:

`md5hexCodes`; `intFloatDiv`; `divII`; `floatMod`; `floatLt`; `absF`;
`floorFI`; `toF`; `ceilF`; `subF`; `divF`; `addF`; `mulF`; `powF`; `gtF`;
`eqF`; `decStrToF`; `divFloatIntV`; `intToF`; `truncF`; `roundF`; `roundFN`;
`sqrtF`; `sortVS`; and `sortKeyVS`.

None is reachable or result-bearing for this theorem. The program performs no
operation on its elements, so even arbitrary `Val` elements cannot activate
those functions. No empirical or symbolic bridge to any opaque value is used.

I found no materially unsound proof or used-semantics rule and therefore make
no false-rule unsoundness allegation. For unused supplied facilities, the
narrower evidence statement is that their universal Python fidelity is outside
this theorem and was not needed or established.

Stage 5 result: pass.

## 6. Fresh non-vacuity test

The fresh mutation uses the satisfiable ground input
`numbers=[1,2,3]`, `delimeter=4`. It keeps the actual program and all final
cells but changes the result-bearing heap obligation from the true
`[1,4,2,4,3]` to the false `[1,4,2,4,4]`.

The mutation is
[06_spec_vacuity.k](/audit-output/evidence/06_spec_vacuity.k). A `kprove
--dry-run` parsed and built it successfully (exit 0). The real proof then
executed to `ref(0)` and a heap containing the correct
`[1,4,2,4,3]`, emitted `WarnStuckClaimState`, reported that the final term did
not unify with the false destination, and exited 1. This is the expected unmet
result obligation, not a parser error, missing import, timeout, unrelated
crash, or unreachable mutation.

Exact commands, full bounded residual, and statuses are in
[06_nonvacuity.log](/audit-output/evidence/06_nonvacuity.log).

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### What is machine-checked

Relative to the selected supplied K semantics, the successful entry
reachability claim establishes:

For every finite `NUMBERS:ValSeq` and `D:Int`, starting from the exact module
configuration in the claim, executing the exact submitted translated module
and calling `intersperse(list(NUMBERS),D)` reaches normal return `ref(0)`;
heap location 0 contains
`list(intersperseAcc(.ValSeq,NUMBERS,D))`; the module closure remains correctly
bound; the callee frame is removed; `scopeLoc`, `heapLoc`, stack, return,
exception, and exit cells have the claimed values. The supporting claims
establish the corresponding empty, first, and recurrent loop transitions.

Through the exhaustive proof-local equations, that sequence is the original
sequence with `D` between consecutive elements. This is a partial-correctness
statement under the K execution model; it does not turn differential tests or
candidate prose into proof premises.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied semantics tree and its K built-in hooks for maps, lists, integers, Booleans, strings, equality, strictness, and cells | Every reachability step | Acceptable and mandatory under `SUPPLIED_SEMANTICS`; candidate copy is byte/type identical. Used rules were also statically checked on this path. |
| K `v7.1.337`, LLVM backend for concrete execution, Haskell backend for proof | Build, `krun`, `kprove` results | Normal machine-checking trust boundary. Definitions were rebuilt from source; backend agreement is supported by concrete and ground runs. |
| Trusted `/reference/py2mpy.py` | Python-to-`.mpy` bridge | Explicit trusted input. The submitted translation is byte-identical to fresh output, and the entry claim's parsed AST is identical to it. |
| Trusted prompt and canonical implementation | Human-facing intent and independent Python oracle | Explicit trusted inputs. The natural-language summary follows them directly; broad finite differential evidence has zero mismatches. |
| Mathematical reading of `intersperseAcc` as “insert between” | Intent adequacy | Informal but transparent structural induction on the six exhaustive equations; ground and 27,853-case differentials support, but do not replace, the K proof. |
| 25 supplied opaque/symbolic functions listed in Stage 5 | None | Acceptable here because no target redex, branch, state, or result depends on them. |
| Candidate generation narrative/metrics | None in the proof | Unavailable because four provenance files are missing. This is the reason for `CONCERNS`, not a soundness failure. |

There is no candidate trusted primitive, program-derived oracle, operational
bridge, empirical rewrite, or informal lemma used to close the claim. The
differential test supports only the finite Python implementation-to-canonical
bridge. It is not presented as universal proof.

### Gate results and decision

- Real-program soundness: pass.
- Intent adequacy: pass.
- Reproducible reviewer evidence and trust accounting: pass.
- Candidate generation-provenance completeness: concern (four files missing).

The missing provenance does not make a false result provable, weaken the entry
precondition, replace execution, or prevent reconstruction. The proof is
therefore legitimate, with a documented auditability limitation.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
