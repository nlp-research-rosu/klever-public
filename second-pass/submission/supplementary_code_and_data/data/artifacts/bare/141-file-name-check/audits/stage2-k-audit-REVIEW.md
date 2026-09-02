# Independent adversarial review: 141-file-name-check

## Executive finding

The candidate has a real, result-constraining Haskell-backend reachability
claim, and that claim cleanly reconstructs to exit 0 and `#Top`. The submitted
Python is also faithfully translated and the claim's checked-in constructor
term is mechanically identical to `solution.mpy`.

The proof is nevertheless not a legitimate proof of the real generated
program over the source contract's full string domain. On the satisfying input
`S = ""`, both Python implementations return `"No"` and the fresh Haskell
definition returns `VStr("No")`, but the fresh LLVM definition built from the
same `semantic.k` aborts with an invalid string-slice exception. The generated
conditional encoding constructs and evaluates an unchosen continuation that
contains `file_name[0]`; `subscriptVal("", 0)` invokes `substrString("", 0, 1)`
outside the hook's defined index domain. An audit-only guard/sentinel mutation
removes that abort and makes the LLVM run return `"No"`, confirming the cause.

This is not an infrastructure uncertainty: K 7.1.293 built both definitions,
14 other LLVM cases executed normally, the defect reproduced in a standalone
witness, and the proof backend and concrete backend disagree specifically on
this intended-domain boundary. A `#Top` under the Haskell simplifier cannot
validate a generated semantics that does not execute the same control flow on
an ordinary source input.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `141-file-name-check`;
- condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

The campaign lock is a regular file, has the recorded SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and parses to exactly the `audit_campaign` object embedded in
`/audit-input.json`. The declared audit image ID, prompt hash, K version, Kit
commit/tree, and toolchain lock values therefore agree.

All launcher-declared container paths exist, are readable, and are not
symlinks. For the declared legacy layout I inspected `/run.json`,
`/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`,
`usage.json` (present), `codex-last.txt`, `codex-output.log`, `prompt.txt`,
the legacy records, and all 200 valid JSONL records in the structured trace.
Historical runtime metrics are not required for this layout and were not
invented.

The independently computed hashes of the run manifest, task manifest, stage-1
result/invocation, trusted inputs, generation prompt/output/last/metrics/usage,
and every file named by the invocation manifest match their recorded values.
Every candidate, reference, and trace file also has a reviewer-generated
per-file hash manifest. There are no symlinks below `/candidate`, `/reference`,
or `/generation-evidence`. Evidence:

- [provenance commands and comparisons](/audit-output/evidence/01-provenance.log)
- [all mounted file hashes](/audit-output/evidence/01-mounted-tree-hashes.log)
- [full structured-trace parse summary](/audit-output/evidence/01-trace-summary.log)

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounted versions. `/reference/reference-semantics` is absent, as
required for `GENERATED_SEMANTICS`. Thus there is no mode/mount contradiction
and no audit-infrastructure breach.

The generation records are treated only as untrusted historical claims. In
particular, their reported `KPROVE_PASSED`, six selected concrete tests, and
candidate mutation were not reused as proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py`, a filename is valid exactly when:

1. the whole filename contains at most three ASCII digits `0` through `9`;
2. it contains exactly one dot;
3. the substring before that dot is nonempty and begins with an ASCII Latin
   letter `a`-`z` or `A`-`Z`; and
4. the substring after the dot is exactly `txt`, `exe`, or `dll`.

The required return is `"Yes"` exactly for valid names and `"No"` otherwise.
The domain stated by the prompt is strings; it has no nonempty-string
precondition.

The trusted canonical implementation uses Python's Unicode-wide `isalpha()`
and `isdigit()` instead of the prompt's explicit ASCII ranges. Consequently,
the canonical returns `"Yes"` for `"é.txt"` while the literal prompt and
candidate return `"No"`; it also rejects `"a١٢٣٤.txt"` while the prompt and
candidate accept it because Arabic-Indic digits are not `0`-`9`. This is a
canonical/prompt discrepancy, not a narrowing introduced by the candidate.

### Translation identity

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced a file byte-identical to submitted `solution.mpy`.
Both SHA-256 values are:

`8b599b1860c8633b4dbb68bce7b2fcf8b276139506a85bcb7df42801e4969883`.

See [translation and byte comparison](/audit-output/evidence/02-fidelity.log).

### Independent differential test

The reviewer-authored test imports both trusted canonical and generated entry
points and implements a third oracle directly from the literal prompt. It
covers the two examples, empty strings, dot-count boundaries, all rejection
branches, ASCII first-character boundaries, three/four-digit boundaries,
suffix variants, Unicode witnesses, and deterministic generated strings.

Across 16,684 distinct strings:

- generated implementation versus literal prompt oracle: **0 mismatches**;
- generated implementation versus canonical: **276 mismatches**;
- canonical versus literal prompt oracle: **276 mismatches**.

The equal mismatch sets establish that the observed generated/canonical
differences are the canonical's Unicode-wide classifications, while the
candidate follows the explicit prompt. This is finite evidence, not a
universal proof. The script and complete bounded result are
[02-differential.py](/audit-output/evidence/02-differential.py) and
[02-differential.log](/audit-output/evidence/02-differential.log).

## 3. Clean proof reconstruction

I copied only source artifacts and trusted inputs into
`/tmp/audit-work/141-file-name-check`; no candidate-provided kompiled
definition, cache, `kprove.out`, or trace was used.

The live tools are K 7.1.293. `kup` is absent, but independently installed
`kompile`, `krun`, and `kprove` all run at the campaign-recorded version.

### Fresh builds and positive target claim

The concrete definition was built from `semantic.k` under the new output name
`audit-semantics-kompiled` with:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantics-kompiled --warnings none
```

The proof definition was independently built from `verification.k` under
`audit-verification-kompiled` with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled --warnings none
```

There is exactly one positive target claim, at `/candidate/spec.k:6`. Its
fresh command exited 0 and printed `#Top`:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --warnings all
```

It also emitted `WarnTrivialClaim: Claim proven without rewriting`. This means
definition-time functional simplification normalized the two claim sides to
the same term; it does not by itself establish semantic fidelity.

The full build/proof output and claim inventory are in
[03-positive-proof.log](/audit-output/evidence/03-positive-proof.log).

### Required generated-semantics executions

Fresh LLVM execution agreed with generated Python on 14 normal/boundary
inputs, including all ordinary branches, digit limits, Unicode witnesses, and
suffix boundaries. It failed on the fifteenth input, the empty string:

```text
Python generated("") = "No"
Python canonical("") = "No"
Haskell krun("")      = VStr("No"), exit 0
LLVM krun("")         = abort, invalid string slice, exit 255
```

The first failing batch is
[03-reconstruction.log](/audit-output/evidence/03-reconstruction.log). The
standalone cross-backend reproduction is
[03-empty-boundary-witness.log](/audit-output/evidence/03-empty-boundary-witness.log).
Because the same freshly built LLVM definition runs the other cases, this is a
candidate semantics defect rather than a timeout, parser failure, missing
tool, malformed mount, or general container failure.

Stage 3 therefore has mixed results: the positive claim closes, but the
mandatory generated-semantics boundary execution fails on an intended-domain
input.

## 4. Adequacy and real-program pinning

### Claim in plain language

The sole entry claim has no `requires` clause. Its precondition is simply that
`S` is any K `String`. It states:

> Executing the checked-in `solutionProgram` with input `S` reaches a `<k>`
> cell containing `contractResult(S)`.

There are no omitted state cells: this generated semantics puts its
environment inside functional terms and has only a `<k>` configuration cell.
The postcondition is result-constraining; it is not a free variable or a
one-way implication.

Examples of realizable pre-states include `S = "example.txt"`,
`S = "a1234.txt"`, and `S = ""`; every K string satisfies the entry
precondition.

### Mechanical source-to-claim pinning

The proof does not parse `solution.mpy` at proof time; it uses the
`solutionProgram` constant in `/candidate/verification.k:62-136`. I therefore
checked all three links independently:

1. trusted regeneration is byte-identical to `solution.mpy`;
2. K's parser produces identical constructor JSON for `solution.mpy` and the
   Program RHS copied into an audit pinning claim; both canonical constructor
   hashes are
   `7575d9abfa9e7aae3ac808040974483efcf2747f85f7694b048b270fa2f5f751`;
3. `kprove pinning-spec.k` exits 0 with `#Top`, showing
   `solutionProgram` rewrites to that exact constructor term.

The only normalization is the mechanically demonstrated equivalence between
the translator's blank list field and K's explicit `.Stmts` unit. Evidence is
in [04-compare-constructors.py](/audit-output/evidence/04-compare-constructors.py)
and [04-adequacy-rerun.log](/audit-output/evidence/04-adequacy-rerun.log).

Thus this proof does pin the submitted function name, parameter binding, and
body; it is not proving a substituted program.

### Ground substitutions and body sensitivity

Six ground specializations—including `"example.txt"`, `""`, exactly three
digits, four digits, and both Unicode discrepancy witnesses—close with
`#Top` under the Haskell definition and agree with generated Python. The
standalone empty LLVM run remains the contradictory concrete result.

For body sensitivity, I changed the actual `solutionProgram` constructor's
valid branch from `Return(Str("Yes"))` to `Return(Str("No"))`, rebuilt a
separate definition successfully, and reran the unchanged universal
postcondition. `kprove` exited 1 with `WarnStuckClaimState` and a residual
`VStr("No")` branch. This mutation changes the exact Program term the claim
executes; it does not merely edit an ignored external source file. See the
diff, build, and residual in
[04-adequacy-rerun.log](/audit-output/evidence/04-adequacy-rerun.log).

### Postcondition meaning

`contractResult` is a nested decision tree over exact dot count, ASCII digit
count, nonemptiness, ASCII first-letter ranges, and one of the three exact
suffixes. With exactly one dot and an accepted final suffix, checking the
first character of the whole string is equivalent to checking the first
character of the stem. Thus the tree matches the literal prompt.

`validFileName` at `/candidate/verification.k:40-45` states the Boolean
contract but is not used by the claim and no K lemma proves
`contractResult(S) == "Yes"` iff `validFileName(S)`. That equivalence is an
auditable but informal intent bridge, not part of the machine theorem. By
itself that would be a non-fatal limitation; it is not the reason for the
final failure.

## 5. Rule-by-rule static soundness review

The full source-numbered inventory is preserved in
[05-rule-inventory.log](/audit-output/evidence/05-rule-inventory.log).
There are no generated helper K files beyond `semantic.k`; `verification.k`
is the proof-local module.

### Local syntax, attributes, and configuration

`MPY-SYNTAX` declares all 31 local constructor/collection productions:

- `Module`;
- lists `Stmts`, `Exprs`, `CmpOps`, and `Strings`;
- `Params` and `CmpOp`;
- statements `FuncDef`, `Assign`, `If`, and `Return`;
- expressions `Name`, `Int`, `Str`, `Bool`, `BinOp`, `UnaryOp`, `BoolOp`,
  `Compare`, `Subscript`, `Attribute`, and `Call`;
- values `VInt`, `VStr`, `VBool`, and `IteVal`;
- environments `EmptyEnv` and `Bind`;
- results `Normal`, `Returned`, and `IfExec`.

Every constructor in `solution.mpy` is declared. The used constructor counts
are also recorded in the inventory log. The unused `Bool` literal is harmless;
missing semantics for other untranslated Python constructs is not a defect in
this generated-semantics mode.

The 14 semantics functions declared `[function,total,symbol]` are
`runProgram`, `eval`, `lookupVal`, `exec`, `continue`, `asBool`,
`compareVals`, `endsWith`, `addVals`, `subscriptVal`, `boolOp`,
`resultValue`, `occurrences`, and `getString`. The six verification functions
with the same attributes are `solutionProgram`, `digitCount`,
`startsWithAsciiLetter`, `hasAcceptedSuffix`, `validFileName`, and
`contractResult`.

Many semantics functions are not actually total over their full declared K
sorts: for example, there is no `lookupVal` equation for `EmptyEnv`,
`asBool` handles only `VBool`, `addVals` only handles integer values, and
`endsWith(S, "")` would request an invalid zero-width `substrString`. These
are over-broad declarations. Most unsupported cases are unused by this exact
program, so I record them as scope/totality evidence gaps rather than invent
false-conclusion witnesses. The empty-input failure below is different: it is
reached by the submitted program.

The only configuration is:

```text
<k> runProgram($PGM:Program, $INPUT:String) </k>
```

No heap, allocation, I/O, exception, or external mutable state is modeled.
That is sufficient for this pure function only if control flow prevents
invalid indexing as Python does.

There are no local `functional`, priority, `simplification`, `anywhere`,
`owise`, macro, alias, or trusted-rule attributes. `occurrences` has the sole
`[concrete]` rule. `IteVal` and `IfExec` are ordinary rewrite constructors;
the remaining local rules are function equations.

### All 42 `semantic.k` rules

The following groups account for every rule, with no omissions:

| Lines | Rule(s) and decision |
|---|---|
| 64 | `occurrences -> countAllOccurrences [concrete]`: correct for the actual fixed nonempty one-character needles, conditional on K's string-count hook. Symbolically opaque; trust boundary discussed below. |
| 68-71 | `runProgram`: exactly selects the single `file_name_check(file_name)` binding and initializes `file_name`; correct for the pinned module. |
| 73; 74-75 | `resultValue(Returned)` and `resultValue(IfExec)`: value extraction and pointwise symbolic conditional construction. The latter contributes to the strictness defect when its branch arguments contain partial hooks. |
| 77; 78 | `IteVal(true/false)`: disjoint Boolean selectors with the expected result. |
| 79; 80 | `IfExec(true/false)`: disjoint branch selectors. Their equations are locally truthful, but their branch arguments have already been constructed by the flawed `exec(If)` rule. |
| 82 | Empty statement sequence returns the environment; correct. |
| 83-84 | Name assignment evaluates the RHS and shadows through `Bind`; correct for the two used assignments. |
| 85 | `Return` discards the suffix and returns the evaluated expression; correct. |
| 86-91 | `exec(If)` constructs both `continue(exec(THEN), SS)` and `continue(exec(ELSE), SS)` below `IfExec`. This does not preserve Python's selected-branch evaluation when an unchosen branch contains a partial operation. **Material failure.** |
| 93; 94 | `continue(Normal)` runs the suffix and `continue(Returned)` discards it; individually correct. |
| 95-96 | `continue(IfExec)` distributes the suffix into both branch terms. Correct as a pure symbolic tree transformation only when both branches are safe to construct/evaluate; it participates in the empty-input failure. |
| 98 | Name evaluation delegates to lookup; correct. |
| 99; 100-101 | Head-binding lookup and guarded recursive lookup have disjoint guards and preserve lexical shadowing; correct for reachable environments. |
| 102; 103; 104 | Integer, string, and Boolean literals; direct and correct. |
| 105-106 | Binary `+` evaluates both operands and delegates to integer addition. Python's left-to-right order is collapsed, but all submitted operands are pure integer count calls, so no observable difference here. |
| 107 | Unary `not`; correct on the submitted Boolean expression. |
| 108 | Boolean-operation dispatcher; see lines 130-137 for its eager behavior. |
| 109-110 | Single comparison dispatcher; the submitted AST has only single comparisons, and evaluation is value-correct for its pure operands. |
| 111-112 | Subscript dispatcher; correct only where `subscriptVal` is defined. |
| 115 | `getString(VStr)`; correct for all submitted call receivers. |
| 117-118 | `len` on strings via `lengthString`; acceptable built-in bridge and value-correct in tested Unicode cases. |
| 119-120 | `str.count` via `occurrences`; an external primitive boundary, not a proof of counting itself. |
| 121-122 | `str.endswith` via `endsWith`; correct for the three fixed suffixes. |
| 124 | Integer addition; correct. |
| 125-126 | String indexing by `substrString(S,I,I+1)` has no bounds guard. It is value-correct for the actual `I=0` when `S` is nonempty, but partial for `S=""`; combined with lines 86-96 it is reached on an unchosen Python path. **Material failure.** |
| 128 | Boolean projection; correct for submitted guards. |
| 130-131; 132-133; 134-137 | Two-argument `and`, two-argument `or`, and three-argument `or`: truth-value correct for the submitted pure, defined operands. They do not implement Python short-circuit effects, but no used operand has side effects or raises after the source's nonempty guard. |
| 139; 140; 141; 142 | Integer `==`, `!=`, `>` and string `<=`: disjoint operator cases and correct for submitted operand types. One-character ASCII-boundary comparisons agree with Python/K Unicode lexicographic order in the tested scope. |
| 144-150; 151-152 | `endsWith` for long-enough and too-short strings: guards are disjoint and exhaustive for integer lengths; the substring is valid for the submitted nonempty suffixes. |

The decisive witness for lines 86-96 plus 125-126 is `S=""`. Python evaluates
the first dot-count `if`, returns `"No"`, and never evaluates `file_name[0]`.
Fresh LLVM execution instead aborts inside `substrString`. Fresh Haskell
execution returns `VStr("No")`, so the candidate's asserted universal result
does not describe one consistent executable generated semantics.

The cause was checked rather than guessed: in an audit-only copy I guarded the
valid index equation and returned a diagnostic sentinel for out-of-range
indices. The mutated semantics built successfully and LLVM then returned
`VStr("No")` on `""`. The exact four-line mutation, build, and result are in
[05-empty-cause-diagnostic.log](/audit-output/evidence/05-empty-cause-diagnostic.log).
This experiment is diagnostic evidence, not a repair to the immutable
candidate.

This is the required concrete false-behavior witness: instantiating the
purported all-string execution at `""` says the generated semantics computes
`"No"`, while the required concrete semantics aborts. I do not label the
remaining globally over-broad declarations “unsound” without such a witness.

### All six `verification.k` rules

| Lines | Rule and decision |
|---|---|
| 13-23 | `digitCount`: sum of occurrences for exactly ASCII `"0"` through `"9"`; matches the prompt, conditional on `occurrences`. |
| 25-30 | `startsWithAsciiLetter`: correct for nonempty strings; uses invalid `substrString(S,0,1)` on empty strings and is therefore not genuinely total over its declared domain. |
| 32-35 | `hasAcceptedSuffix`: exact disjunction of `.txt`, `.exe`, `.dll`; correct. |
| 40-45 | `validFileName`: direct Boolean form of the prompt; not imported into the postcondition proof. Its eager conjunction can also expose the empty-string partial substring if evaluated standalone. |
| 49-58 | `contractResult`: result-valued decision tree matching the prompt. Its nested `IteVal` relies on selected-branch rewriting to avoid the empty substring; Haskell does so, LLVM execution of the program does not. |
| 62-136 | `solutionProgram`: exact pinned submitted constructor term, mechanically checked in Stage 4. |

There are no overlapping verification equations for the same head symbol.
There are no proof-local lemmas or rewrite rules that directly assert the
desired `"Yes"`/`"No"` answer for a concrete filename. The serious problem is
the generated operational model, not a hidden task-answer axiom.

### Result-bearing primitives and control

`occurrences` is the only locally introduced symbol opaque on symbolic
strings. It affects dot-count branches, digit-count branches, and the final
postcondition. The same symbol appears in execution and `contractResult`, so
the `#Top` does not itself prove what occurrence counting means. I classify it
as an externally trusted primitive for Python's fixed `str.count`, not as
program-defined computation: its concrete rule maps every actual nonempty
needle used here to K's `countAllOccurrences`, and the theorem is
interpretation-parametric/conditional on that primitive. Concrete K/Python
tests support the bridge on the fixed needles, but finite tests do not prove a
universal connection theorem.

That boundary is acceptable with an explicit condition for the used
single-character needles. It does not excuse the conditional/index defect,
which involves the program's own control flow and has a concrete
intended-domain counterexample.

## 6. Fresh non-vacuity test

I did not reuse `/candidate/mutation-spec.k`. The fresh mutation uses
`"a123.txt"`, a filename satisfying the contract with exactly three ASCII
digits, and changes the required result from the true `"Yes"` to false
`"No"`.

Independent Python execution first confirmed `"Yes"`. Then:

1. `kprove --dry-run` exited 0, demonstrating that the mutation parsed and
   built successfully;
2. the actual proof exited 1 with `WarnStuckClaimState`;
3. the residual `<k>` cell was `VStr("Yes")`, exactly the unmet
   result obligation.

This is meaningful non-vacuity evidence, not a parser error, timeout, unrelated
crash, or unreachable mutation. The mutation source, commands, statuses, and
residual are in [06-nonvacuity.log](/audit-output/evidence/06-nonvacuity.log).

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the Haskell interpretation and simplification of the submitted generated
theory, for every K string `S`, the exact pinned constructor term
`solutionProgram` normalizes through the functional evaluator to the same
`contractResult(S)` decision tree. The proof is universal, result-constraining,
constructor-pinned, and body-sensitive. The false-result mutation is rejected.

It does **not** establish:

- that the LLVM executable generated from the same semantics agrees on every
  string (it demonstrably does not on `""`);
- a machine theorem connecting `contractResult` to the unused
  `validFileName` Boolean;
- an internal symbolic derivation of Python `str.count`; or
- total correctness/termination of arbitrary Python programs.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| Trusted CPython-AST translator | Program identity | Byte identity plus constructor equality checked; acceptable. |
| K 7.1.293 parser, compiler, Haskell prover | All formal results | Normal toolchain trust. Exact versions and commands recorded. |
| K integer/Boolean/string hooks (`lengthString`, lexicographic comparisons, `substrString`, `countAllOccurrences`) | Evaluator and contract summaries | Low-level semantic trust. Finite Unicode/branch tests support used cases. The invalid empty substring exposes a violated hook precondition and is fatal. |
| `occurrences` concrete bridge | Dot and ASCII digit counts, `contractResult` | Externally trusted `str.count` abstraction for fixed nonempty needles. Symbolically opaque and shared with the postcondition; theorem is conditional on its meaning. Acceptable as a named primitive boundary, not as proof of counting. |
| `endsWith` equations | Accepted suffix branch | Guarded, disjoint, and correct for the three nonempty suffixes; supported by concrete tests. |
| Informal `contractResult` ↔ English contract equivalence | Human-facing correctness statement | Straightforward and independently differential-tested, but not a K lemma. Non-fatal in isolation. |
| Canonical Unicode behavior | Differential comparison | Canonical conflicts with the prompt's explicit ASCII wording. Reported, not silently used to redefine the source domain. |
| Partial-correctness interpretation | Final theorem | Termination is not proved. This is the requested proof class and is acceptable. |

### Gate and decision accounting

- **Gate A, real-program soundness: FAIL.** Program identity and non-vacuity
  pass, but conditional control plus partial indexing fails on the satisfying
  input `""`; the proof and concrete generated semantics disagree.
- **Gate B, intent adequacy: FAIL at language-model adequacy.** The formal
  claim syntactically quantifies over every string, including empty, but the
  required concrete generated semantics does not cover that source-contract
  boundary.
- **Gate C, evidence auditability: PASS.** Commands, source mutations,
  statuses, and bounded outputs are preserved; empirical evidence is not
  presented as universal proof.

The positive `#Top`, constructor pinning, and rejected false mutation are
genuine but insufficient. The material generated-semantics/control failure
means the proof cannot legitimately be transferred to the real generated
program on its unrestricted string domain. Under the benchmark's mapping, this
is `FAIL / NOT_LEGIT`, not a merely evidentiary concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
