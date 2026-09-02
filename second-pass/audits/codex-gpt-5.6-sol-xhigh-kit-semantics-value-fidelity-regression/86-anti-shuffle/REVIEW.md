# Independent adversarial audit: 86-anti-shuffle

## Headline

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program under the supplied semantics. I reconstructed
both definitions without using candidate caches, independently closed all three
positive proof stages, pinned the entry and loop claims to the submitted MPY
AST, audited all 22 proof-local rules, and obtained the expected failure from a
fresh reachable false-result mutation.

The qualified verdict is `CONCERNS / LEGIT`, rather than an unqualified pass,
because the machine-checked postcondition is the candidate's recursive
`antiShuffle` summary. Its correspondence to the human phrase “sort every word
by ASCII value” is supported by a rule-by-rule induction argument and extensive
finite comparisons, but is not itself a separate machine-checked theorem
against a declarative sorted-permutation specification or the trusted canonical
function. The formal `IntSeq` domain also over-approximates actual Python/ASCII
strings. Neither limitation permits a false program result to be proved.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it: `/reference/reference-semantics` exists. This is not an infrastructure
breach.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace only as candidate claims.
`run-input.json` identifies problem `86-anti-shuffle`, the `kit-semantics`
condition, and semantics/translator hashes. `metrics.json` claims generation
exit 0 without timeout. The prose/log/trace claim `VALIDATED`, three `#Top`
results, expected mutation failures, and 110 differential cases. None of those
claims was used as proof evidence. The trace is a regular file containing 610
valid JSONL records and one final-answer record; see
`evidence/02_trace_summary.log`.

The independent integrity checks in `evidence/01_provenance.sh` and
`evidence/01_provenance.log` establish:

- All required candidate metadata and deliverables are present as regular,
  non-symlink files: `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, the structured trace, `prompt.py`, `py2mpy.py`,
  `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prove.sh`, and
  `PROOF.md`.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `f8a02b...aa972`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485...db16`).
- `diff -qr --no-dereference` reports exact recursive identity between
  candidate and trusted `reference-semantics/`, and the candidate tree contains
  no symlinks. Thus it has no missing, additional, changed, mistyped, or
  symlinked semantics entry.
- The candidate source/proof hashes independently obtained are:
  `solution.py` `97132b...2097`, `solution.mpy` `17b827...9366`,
  `spec.k` `7ec6e2...e748`, and `verification.k` `e1f577...6bf7`.

Candidate `runtime-kompiled/`, `verification-kompiled/`, bytecode, logs, traces,
and prose were ignored for reconstruction. Only the source artifacts listed in
`evidence/03_prepare_scratch.log` were copied, and the semantics, translator,
prompt, and canonical implementation in that copy came from `/reference`.
There are no provenance integrity failures.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires `anti_shuffle(s)` to preserve word order and every
blank space while replacing each code-32-space-delimited word by its characters
in ascending ASCII-value order. The trusted canonical implementation realizes
this as `s.split(" ")`, `sorted` within every component, and `" ".join(...)`.
That formulation preserves leading, trailing, and consecutive spaces.

The submitted implementation performs a streaming insertion sort. It keeps the
current word sorted, inserts each non-space character before the first larger
character (or appends it), flushes the word and one space on code 32, and
appends the final word. The empty-word, less-than, equal/greater-than,
already-inserted, space, and non-space paths are all defined.

### Translation fidelity

In scratch I ran the trusted translator:

```text
cd /tmp/audit-work/anti-shuffle-audit &&
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

It exited 0. `cmp -s` against the submitted MPY exited 0, and both files have
SHA-256 `17b8273aa387c21ba0d812a8212dc8a12abdb6538cc50686a8d9e7ffc4e39366`.
Exact commands and statuses are in `evidence/04_fidelity.log`.

### Independent differential test

`evidence/05_differential.py` independently imports the entry points from
`/reference/canonical.py` and the scratch copy of `solution.py`. It does not use
candidate tests or proof equations. The preserved JSONL at
`evidence/05_differential.jsonl` records every input and both results.

The run exited 0 with 0 mismatches and 0 exceptions over 3,105 unique strings:

- all three prompt examples;
- empty, one/all/leading/trailing/consecutive spaces;
- every insertion branch boundary, including less, greater, equal,
  already-inserted, and empty current word;
- punctuation, control codes, BMP and astral Unicode;
- all strings of lengths 0 through 4 over
  `[" ", "a", "b", "A", "!", NUL, "é"]`;
- 300 deterministic strings of lengths 0 through 64 using seed `860723`.

No material candidate/canonical divergence was found on the intended domain.

## 3. Clean proof reconstruction

The scratch root is `/tmp/audit-work/anti-shuffle-audit`. It contains no copied
candidate definition or cache. The installed live toolchain is K v7.1.293.

### Fresh builds

`evidence/06_build.sh` performed these source builds:

```text
kompile .../reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition .../runtime-kompiled

kompile .../verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX \
  --output-definition .../verification-kompiled
```

Both exited 0 (`evidence/06_build.log`), with bounded compiler output in
`evidence/06_kompile_runtime.log` and
`evidence/06_kompile_verification.log`. Warnings about non-exhaustive
`joinCodes`/`valSeqAt` and unused variables originate in the trusted supplied
tree or framed claim variables; those helpers are not reachable from the target
program.

### Fresh concrete execution

The reviewer-authored `evidence/08_concrete_harness.py` contains the exact same
function AST as `solution.py`; `evidence/08_check_harness_identity.py` verifies
that equality. It adds 14 ASCII assertions covering the examples and normal,
empty, spacing, order, equality, insertion, and punctuation boundaries.
CPython and fresh LLVM execution both exited 0. LLVM ended with `.K`, empty
heap/stack, `NoExc`, and exit code 0; commands and output are in
`evidence/08_concrete_run.log` and `evidence/08_krun_fixed.log`.

An initial reviewer harness also included `"éΩA"`. The fixed supplied semantics
rejected this source literal at `strToCodes` and exited 113 because
`semantics/str.k` explicitly limits source literals to ASCII. That attempt is
preserved in `evidence/08_concrete_run_unicode_attempt.log` and
`evidence/08_krun_fixed_unicode_failure.log`. It is a documented supplied-model
boundary, not a proof failure: the natural contract is ASCII-based, the final
LLVM harness uses only intended literals, the symbolic entry accepts input
codes directly, and CPython differential testing still covers Unicode.

### Positive claims

`evidence/07_positive_proofs.sh` independently ran the candidate's theorem
composition stages against the fresh Haskell definition:

| Target | Prior theorem made available | Exit | Exact success |
|---|---|---:|---|
| `SPEC.insertion-loop` | none | 0 | one `#Top` |
| `SPEC.character-loop` | independently closed `SPEC.insertion-loop` | 0 | one `#Top` |
| `SPEC.anti-shuffle` | independently closed insertion and character loops | 0 | one `#Top` |

The exact commands/statuses are in `evidence/07_positive_proofs.log`; complete
bounded outputs are the three `evidence/07_kprove_*.log` files. The auxiliary
labels passed through `--trusted` are byte-for-byte the same claims first
discharged by preceding exit-0/`#Top` runs. Thus this is theorem composition,
not reliance on an unproved candidate assertion.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.insertion-loop` starts at the real inner `#loop` with any remaining
one-character string sequence `S`, current insertion character code `C`,
accumulator `NW`, flag `B`, exact function/module bindings, empty heap, and an
arbitrary preserved continuation/stack. It says the loop terminates at that
continuation with `new_word = innerWord(NW,B,C,S)` and
`inserted = innerFlag(B,C,S)`. Only the final `existing` value is existentially
irrelevant.

`SPEC.character-loop` starts at the real outer `#loop` with any remaining input
`S` and accumulators `result=A`, `word=W`. It says the loop reaches its
continuation with
`result = scanResult(A,W,S)` and `word = scanWord(W,S)`. The loop variables and
scratch insertion locals are existentially unconstrained after the loop, as
they do not affect the subsequent return. Heap, allocation, stack, return, and
exception state are preserved.

`SPEC.anti-shuffle` starts from the exact initial configuration, executes
`#loadAll` of the submitted module and then
`Call(Name("anti_shuffle"), str(S))` for every `S:IntSeq`. It requires the
returned K value to be exactly `str(antiShuffle(S))`, installs the exact closure
in module scope, restores the allocators/empty heap/empty stack/`noRet`/`NoExc`,
and retains exit code 0. The result is an equality-shaped reachability target,
not a free variable, tautology, or one-way implication.

### Structural pinning and satisfiability

`evidence/13_pinning.py` performs balanced-constructor comparisons rather than
substring guesses. Every check is true:

- the entry's loaded `Module` equals the submitted `solution.mpy` module;
- function name, parameter, closure body, and defining scope are exact;
- both auxiliary loop targets and bodies equal the corresponding submitted
  outer and inner `For` bodies;
- `S` occurs on the entry LHS and the RHS is constrained by
  `str(antiShuffle(S))`.

Explicit satisfying states and substitutions are recorded in
`evidence/11_ground_witnesses.jsonl`:

- Inner-loop witness: remaining `"b"`, `C=97` (`"a"`), `NW=""`,
  `B=false`; the post values are `new_word="ab"` and `inserted=true`.
- Outer-loop witness: remaining `"b a"`, `A=W=""`; the post values are
  `result="b "` and `word="a"`.
- Entry witness: `S="ba  dc"` in the exact initial configuration; the claimed,
  canonical, and candidate results are all `"ab  cd"`.

Ground substitutions for `""`, `"b"`, `"ba  dc"`,
`"Hello World!!!"`, `"dabc"`, and `" "` give identical summary,
canonical, and candidate values. The entry precondition is therefore
satisfiable, and so are both auxiliary preconditions.

## 5. Rule-by-rule static soundness review

### Exhaustive source inventory

`evidence/09_inventory.py` regenerated the inventory from the trusted scratch
tree and proof sources. `evidence/09_rule_inventory.md` reproduces every
declaration/rule block with source path, line numbers, file SHA-256, and
attributes. It covers 26 K files, 230 syntax declarations, the configuration,
five contexts, three claims, and 717 rules: 695 fixed supplied-semantics rules
plus 22 proof-local rules. It identifies 163 `[function]`, 123 `[total]`, 15
`[simplification]`, 47 priority, 26 `owise`, 35 `concrete`, and 25 `symbol`
attribute occurrences. There are no generated-semantics helper files in this
supplied-semantics condition.

The 695 baseline rules are the selected, integrity-checked semantics level.
Rules outside the target dependency slice remain a trusted, irrelevant
language-model boundary; they cannot contribute to these claims. I separately
reviewed every rule reachable from the submitted AST:

| Submitted construct | Declaration and effective rules |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll`, statement sequencing, `.Stmts` |
| `FuncDef`, call, parameter, return | `functions.k` function binding/`#bindP`/return/`#pop`; `call.k` callee and left-to-right argument evaluation/closure application |
| `Name`, `Str`, `Bool` | `core.k` scope lookup and Boolean literal; `str.k` ASCII literal/code sequence |
| `Assign`, `AugAssign` | `controls.k` current-scope updates; string `+` through `operators.k` and `str.k` |
| `If` | strict condition evaluation, `truthy`, fixed `#branch`, plus the audited symbolic bridge |
| `For` over strings | `controls.k` `#loop`/`#loopStep`/`#loopLbl`; `str.k` iterator yield/done; `tuple.k` name-target binding |
| `Compare ==/<`, `BinOp +` | left/right evaluation contexts in `operators.k`; `str.k` equality, concatenation, and lexicographic comparison |

Evaluation is deterministic and left-to-right for every used expression.
Strings are values, so the program allocates no heap object. Calls create one
scope frame, return discards the remainder of the function body, and `#pop`
restores the caller state. The entry and auxiliary claims pin all affected
cells.

### Every proof-local declaration and rule

`VERIFICATION-SYNTAX` declares exactly eight symbols, all
`[function,total]`: `antiClosure`, `innerWord`, `finishWord`, `insertCode`,
`scanResult`, `scanWord`, `antiShuffle`, and `innerFlag`. It declares no
`functional` symbol, opaque symbol, configuration, or cell.

The 22 proof-local rules divide as follows, accounting for every one:

| Rules | Count | Static decision |
|---|---:|---|
| Singleton `strLt` simplification | 1 | Sound. For `A<B`, `A>B`, and `A=B`, it respectively gives true, false, and false, exactly matching the three fixed lexicographic rules followed by the fixed empty/empty rule. All overlaps agree. |
| Symbolic `#branch` true/false bridges, priority 60 | 2 | Sound operational bridges. Guards `B` and `notBool B` are disjoint/exhaustive on `Bool`; each RHS is the corresponding fixed literal transition. Only the head K item changes, the arbitrary continuation is preserved, and no other cell is read or written. |
| `antiClosure` alias | 1 | Sound definitional alias. Its parameter, full submitted body, and defining module scope 0 are exact. It does not intercept name lookup, calling, binding, body execution, return, or frame pop. |
| `innerWord` empty/true/false-less/false-not-less | 4 | Sound and exhaustive. They reproduce each inner-loop assignment in order and structurally consume the remaining `IntSeq`. Base/constructor and Boolean cases are disjoint; numeric guards are complementary. |
| `innerFlag` empty/true/false-less/false-not-less | 4 | Sound and exhaustive projection of the same loop flag; structural descent and guards are valid. |
| `finishWord` true/false | 2 | Sound and exhaustive: append `C` exactly when no earlier insertion occurred. |
| `insertCode` | 1 | Sound composition of the two independently connected inner-loop projections and `finishWord`; it replaces no operational term. |
| `scanResult` empty/space/non-space | 3 | Sound and exhaustive. Space flushes `A ++ W ++ [32]`; non-space preserves `A` and inserts into `W`; recursion consumes one code. |
| `scanWord` empty/space/non-space | 3 | Sound and exhaustive companion projection. Space resets the word; non-space inserts; recursion consumes one code. |
| `antiShuffle` | 1 | Sound composition: concatenate the fully flushed result with the final current word. It is a mathematical result summary, not an execution rewrite. |

The 15 simplification rules are precisely the singleton comparison, four
`innerWord`, four `innerFlag`, three `scanResult`, and three `scanWord` rules.
The two priority rules are the branch bridge; the remaining five are ordinary
definitional rules. All `[total]` declarations have constructor/Boolean/guard
coverage, recursion descends, and overlaps are either disjoint or agree.

The operational-bridge procedure was repeated independently:
`evidence/10_bridge_harness.py` puts observable assignments immediately after
both true and false branches. Fresh fixed-LLVM and extended-Haskell executions
both exited 0 and produced byte-identical complete configurations
(identical SHA-256 `7cf817...5ee`). The symbolic claims in
`evidence/10_bridge_symbolic.k` quantify over `B`, preserve the observable
continuation, and closed with exit 0/`#Top`. See
`evidence/10_bridge_audit.log` and `evidence/10_bridge_symbolic.log`.

No proof-local rule encodes an unconstrained answer, replaces program execution
with an oracle, fabricates a used construct, or has a false conclusion on the
intended domain. I found no unsound rule; consequently no false-conclusion
witness is applicable. The narrower adequacy limitation is the informal
summary-to-natural-contract bridge discussed in stages 2 and 7, not rule
unsoundness.

## 6. Fresh non-vacuity test

I did not use the candidate's `spec-vacuity.k`. The fresh mutation is
`evidence/12_spec_vacuity.k`. It repeats the exact submitted module and takes
the satisfiable empty-string instance of the real entry claim, but changes the
result obligation from the actual empty string to
`str(iCons(33,.IntSeq))`, i.e. `"!"`.

The exact two commands are recorded in `evidence/12_nonvacuity.log`:

- The `kprove ... --dry-run` command exited 0, establishing that the mutation
  imports, parses, and builds successfully.
- The actual proof exited 1 and emitted one `WarnStuckClaimState`.
  `evidence/12_vacuity_proof.log` shows the reachable residual
  `str(.IntSeq)` in `<k>`, while the mutation source demands code 33.

This is the expected unmet result obligation, not a parser failure, missing
import, timeout, unreachable path, or unrelated crash. The main claim is
discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on the supplied semantics and K toolchain, for every semantic
finite `S:IntSeq`, every normally terminating execution from the exact initial
configuration that loads the exact submitted `solution.mpy` function and calls
`anti_shuffle(str(S))` reaches the exact returned value
`str(antiShuffle(S))`, with the stated restored scope allocator, empty
heap/heap allocator, empty call stack, `noRet`, `NoExc`, and exit code 0. The
loop claims machine-check the exact operational connection between both real
loop bodies and the recursive summaries. This is partial correctness; no
complexity, resource-bound, or separate termination theorem is claimed.

### Trust and assumption ledger

| Boundary | Influence and assessment |
|---|---|
| Exact supplied `reference-semantics/` (695 rules) | Defines syntax, values, control, scopes, strings, calls, and returns. Required and acceptable as the problem's fixed semantics; recursive integrity is exact. Only the used slice listed in stage 5 affects the theorem. |
| K v7.1.293 compiler, LLVM/Haskell backends, KORE/SMT engine, and K's integer/Boolean/string/map/list primitives | Establish parsing, rewriting, arithmetic/order, and proof closure. Standard unavoidable verification infrastructure trust. |
| `SPEC.insertion-loop` and `SPEC.character-loop` passed via `--trusted` in dependent runs | Affect theorem composition, but are not informal assumptions: the same source claims independently exited 0 with `#Top` first. |
| Proof-local `strLt` singleton lemma | Affects the inner comparison branch. It is not opaque; the three integer-order cases derive directly from fixed rules and all overlaps agree. |
| Proof-local branch bridge | Affects control only. Exact rule comparison, symbolic continuation claims, and fixed/extended complete-state equality support its direct equivalence. |
| `antiShuffle` and subordinate summaries | Affect the final result. They are fully defined, exhaustive, terminating mathematical functions. The exact operational loop-to-summary connections are machine checked; no result-bearing symbol is free or oracle-like. |

The trusted supplied tree contains 25 named proof-opaque or concrete-only
`[symbol]` boundaries:
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, and `sqrtF`. None is syntactically or
operationally reachable from `solution.mpy` or any target postcondition, so none
can affect claim closure. There is no proof-local opaque symbol and no trusted
sorting primitive in the proof.

### Empirical and informal bridges

- `evidence/05_differential.py`: 3,105 preserved canonical-versus-candidate
  cases, zero mismatches. This supports implementation-to-intent alignment; it
  is not a universal theorem.
- `evidence/11_ground_witnesses.py`: explicit K-code substitutions plus 5,461
  exhaustive strings of lengths 0 through 6 over `[" ", "a", "b", "!"]`,
  comparing the independently executed summary, canonical, and candidate;
  zero mismatches. This supports, but does not prove universally, the
  summary-to-contract bridge.
- `evidence/08_concrete_harness.py`: 14 ASCII program assertions under CPython
  and fresh LLVM semantics.
- `evidence/10_bridge_audit.sh`: fixed/extended ground branch equality plus a
  machine-checked symbolic continuation test.

The remaining intent argument is ordinary induction: `insertCode` preserves a
permutation and ascending order by inserting before the first greater code;
the scan emits every non-space code exactly once within its current word, emits
every code-32 separator in place, and preserves word order. This makes the
summary match the prompt for ASCII inputs. It is convincing and consistent
with all independent evidence, but it is not encoded as a K theorem stating
sortedness and permutation or equivalence to `/reference/canonical.py`. That
documented bridge limitation, together with the formal over-approximation by
arbitrary integer sequences and the supplied ASCII-literal parser boundary, is
why the legitimate proof receives `CONCERNS` rather than `PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
