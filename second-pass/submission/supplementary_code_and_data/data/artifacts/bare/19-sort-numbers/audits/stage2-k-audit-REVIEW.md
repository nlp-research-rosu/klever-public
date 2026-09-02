# Independent adversarial review: 19-sort-numbers

The candidate's positive claims reconstruct and are non-vacuous, and the
claimed program is mechanically pinned to the trusted translator output.
Nevertheless, the submitted generated semantics is not a sound language model:
its rule for Python `str.strip()` applies to every modeled string but implements
unconditional last-character deletion. A concrete intended-domain witness lets
the compiled theory prove that `"one".strip()` is `"on"`. The candidate also
contains a malformed, albeit unused, `validNumerals` function that proves the
empty boundary invalid. These are candidate defects, not infrastructure
failures. The over-broad `strip` bridge is on the real program's execution path
and violates the required complete-match-domain soundness obligation, so the
successful `#Top` is not a legitimate proof under a sound semantics.

## 1. Input and provenance integrity

The launcher declares:

- problem `19-sort-numbers`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- complete input provenance.

I read `/audit-input.json` first and used only its `container_paths` mounts,
not the host provenance paths. I then read `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`, all records required for
the declared legacy-selected-stage1 layout, the optional `usage.json`, and the
complete structured trace. Historical runtime metrics are correctly absent
from this legacy layout and were not reconstructed.

The campaign lock matches the embedded `audit_campaign` block key-for-key, and
its SHA-256 is the declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The hashes of the run manifest, task manifest, stage-one result, invocation,
metrics, prompt, usage record, output log, last message, trusted inputs, and
individual trace file all match their launcher declarations. The trace parser
accepted all 164 JSONL records. The generation records were treated only as
untrusted historical claims.

Every required candidate proof artifact is a regular file. No symlink exists
under `/candidate`, `/reference`, or `/generation-evidence`. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted mounted
versions. Generated-semantics mode is consistent with the mounts:
`/reference/reference-semantics` does not exist, so no hidden or inferred
reference semantics was used.

There is no infrastructure breach. Exact hashes, commands, record counts, and
the trace inventory script are preserved in
[stage1-integrity.log](evidence/stage1-integrity.log) and
[trace_inventory.py](evidence/trace_inventory.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py` and `/reference/canonical.py`, the entry point is
`sort_numbers(numbers: str) -> str`. The input is a space-delimited sequence of
the words `zero` through `nine`; the output contains the same numeral tokens
and multiplicities sorted by numeric value. The canonical implementation
filters empty fields, so empty input and extra ASCII-space boundaries naturally
produce the corresponding empty/filtered sequence.

The candidate uses a different but valid counting algorithm. For each numeral
in numeric order it emits `"word "` as many times as `numbers.count(word)`,
concatenates the ten blocks, and strips the final space. On the stated valid
token domain no numeral word is a substring of another, so substring count is
token multiplicity.

### Trusted regeneration

Only source artifacts were copied to `/tmp/audit-work/19-sort-numbers`; no
candidate definition or cache was copied. The command

```text
python3 trusted/py2mpy.py solution.py | cmp - solution.mpy
```

exited 0. Thus trusted regeneration is byte-identical to the submitted
`solution.mpy`.

### Independent differential test

The reviewer script independently imports `/reference/canonical.py` and the
scratch copy of candidate `solution.py`; it does not reuse proof equations. It
checks the documented example, empty input, every singleton numeral,
duplicates, sorted and reverse all-numeral inputs, leading/trailing/repeated
space boundaries, every valid sequence of length zero through four, and seeded
long sequences through 1,000 tokens.

The exact result was:

```text
total_comparisons=11232
mismatch_count=0
```

The script and bounded log are
[differential_test.py](evidence/differential_test.py) and
[stage2-fidelity.log](evidence/stage2-fidelity.log). This is finite fidelity
evidence, not a universal proof.

## 3. Clean proof reconstruction

The independently installed tools are K v7.1.293. `kup` is absent, but
`kompile`, `krun`, and `kprove` run directly, so the live path required by
`using-kit` was available.

### Fresh builds

The concrete semantics and proof definition were built from copied source:

```text
kompile --backend haskell semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantics-haskell-kompiled

kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Both exited 0. I also compiled the semantics with LLVM. Compilation exited 0,
but LLVM `krun` exited 113 at a residual `repeatString("zero ",0)` for every
probe. The `[concrete, simplification]` helper encoding is therefore not LLVM
executable. This is a backend-portability concern, not the basis of the
candidate verdict: the submitted workflow explicitly used Haskell, and a fresh
Haskell concrete definition executes.

### Generated-semantics concrete execution

Nineteen fresh Haskell `krun` cases covered empty input, each numeral,
duplicates, reverse order, extrema, and spacing boundaries. Every execution
exited 0 and agreed with both Python implementations:

```text
concrete_cases=19 mismatch_count=0
```

The exact `krun` commands are printed by
[semantics_differential.py](evidence/semantics_differential.py).

### Positive claims

The original command

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`. Because the five submitted claims are unlabeled, I
copied them verbatim into an audit-only module with labels and ran each one
independently. The universal claim, prompt example, duplicate case,
all-numerals case, and empty case each exited 0 and printed `#Top`.

Full build, concrete-execution, and per-claim output is in
[stage3-reconstruction.log](evidence/stage3-reconstruction.log); the audit-only
labeled claims are in [spec-individual.k](evidence/spec-individual.k).

## 4. Adequacy and real-program pinning

### Plain-language claims

The universal entry claim has no `requires` clause. Its precondition is
therefore every K `String S`, a superset of the source contract. Its
postcondition says that execution consumes the whole computation and returns
the exact `VStr(sortSpec(S))`.

The other four claims also have no precondition and fix their inputs and entire
returned strings:

- `"three one five"` returns `"one three five"`;
- `"two two one zero two"` returns `"zero one two two two"`;
- reverse zero-through-nine returns ascending zero-through-nine;
- `""` returns `""`.

Each starting configuration is realizable. For the universal claim,
`S = "three one five"` is one witness; each ground claim's displayed input is
its own witness. The concrete executions in Stage 3 and both Python
implementations give exactly the claimed values for those substitutions.

### Exact constructor pinning

`solutionProgram` is not an opaque result oracle. It expands through
`solutionBody` and `block` to a constructor tree. An audit-only reachability
claim put `solutionProgram` on one side and the byte-regenerated `solution.mpy`
tree on the other. It exited 0 with `#Top`; K reported the claim trivial after
normalization. A depth-zero parse of the actual `solution.mpy` independently
shows the same `Module(FuncDef("sort_numbers", Params("numbers"), Return(...)))`
tree, including the parser's `.Ids`, `.Exprs`, and `.Stmts` empty-list
normalizations.

The `<k>` entry therefore executes the submitted function binding and body,
not a substituted implementation. There are no loops or helper claims whose
control flow needs separate pinning.

### Body sensitivity

A second audit claim changed the emitted literal inside the actual zero block
from `"zero "` to `"WRONG "` while retaining the original expected result.
`kprove` exited 1 with the meaningful residual:

```text
<k>
  VStr ( "WRONG" ) ~> .K
</k>
```

The mutation changed the program term executed by the claim, not merely
`solution.py` outside the theorem. Pinning artifacts and logs are
[pinning-spec.k](evidence/pinning-spec.k),
[body-sensitivity.k](evidence/body-sensitivity.k), and
[stage4-pinning.log](evidence/stage4-pinning.log).

## 5. Rule-by-rule static soundness review

The complete inventory, including every syntax production, local function,
attribute, semantic equation, operational rule, helper abbreviation, claim,
and used `DOMAINS` primitive, is
[rule-inventory.md](evidence/rule-inventory.md). The following is the
file-by-file audit summary.

### `semantic.k`

The syntax declares list sorts for identifiers, expressions, and statements;
`Params`; the six expression constructors `Name`, `Str`, `Int`, `Attribute`,
`Call`, and `BinOp`; `Return` and `FuncDef`; `Module`; values `VStr` and
`VInt`; and `invoke`. Every constructor in `solution.mpy` is declared. `Int` is
declared but unused.

The configuration has only `<k>`. This is adequate for the submitted pure
expression: it has no mutable state, allocation, I/O, exceptions on the
contract domain, or observable call-stack effects.

The six declared evaluator functions and their rules are:

- `evalProgram`, which matches the exact top-level name, parameter, and
  one-return body;
- `eval` for the parameter name, string/int literals, string `+`, string `*`,
  literal-needle `count`, and zero-argument `strip`;
- `addVals`, `multiplyVals`, `countVal`, and `stripVal`.

The evaluator is compositional and does not replace the body with the task's
answer. Unsupported program shapes or type combinations remain visibly stuck.
Evaluation order is immaterial on the submitted pure operands.

`repeatString` has two disjoint, exhaustive ground-integer equations. The
nonpositive rule returns empty and the positive rule recurses on `N-1`; these
are ordinary string-repetition mathematics. The `[concrete]` attributes leave
symbolic instances summarized but do not leave ground results unconstrained.
`trimTrailingSpace` has disjoint empty/nonempty equations and truthfully defines
last-character deletion.

The operational rule

```text
<k> P:Program ~> invoke(S) => evalProgram(P,S) ...</k>
```

preserves the continuation and every modeled cell. It does not introduce an
abrupt return or discard state.

#### Materially unsound `strip` bridge

The critical rule pair is:

```text
stripVal(VStr(S)) => VStr(trimTrailingSpace(S))
trimTrailingSpace(S) =>
  substrString(S, 0, lengthString(S) -Int 1)
  requires lengthString(S) >Int 0
```

Python `str.strip()` does not delete the last character of every nonempty
string. The bridge's complete match domain is every `VStr(S)`, while its
informal justification covers only the submitted body's special receiver:
empty or a concatenation of `"word "` blocks.

The required false-conclusion witness is machine checked. For the accepted
alternate constructor body `return numbers.strip()` and the intended-domain
input `"one"`, candidate semantics proves:

```text
VStr("on")
```

CPython returns `"one"`. The witness claim printed `#Top`. Thus this is not
merely missing evidence: the submitted semantics can prove a concretely false
Python result. The actual body's receiver-shape argument explains why the 19
real-program test cases happen to agree, but the operational rule is not
guarded by that shape and no bridge-free universal connection theorem narrows
its complete match domain. The main proof executes `.strip()` through this
rule, so the proof relies on a materially unsound semantic bridge.

### `solution-program.k`

`block`, `solutionBody`, and `solutionProgram` are fully defined
constructor-level abbreviations. Their word/literal pairs are zero through nine
in order. Mechanical pinning and the body mutation confirm that they neither
hide an oracle nor bypass execution.

### `verification.k`

`sortSpec` is a fully defined ordered concatenation of ten repeated blocks. On
valid tokens, non-overlapping occurrence counts are precisely multiplicities,
so its human-facing meaning is the required sorted sequence. It is a transparent
definitional summary, not an unconstrained result symbol.

`isNumeral [function,total]` has ten exact true rules and a disjoint `[owise]`
false rule. Its totality and overlaps are sound.

`validNumerals [function]` is not sound as written. The explicit rule
`validNumerals("") => true` overlaps the trailing-space rule because:

```text
findString("", " ", 0) = -1
lengthString("") - 1   = -1
```

The compiled function selects `false`. An audit claim
`validNumerals("") => false` printed `#Top`, while the intended true claim
failed with residual `false`. This is a second concrete false-conclusion
witness on the empty boundary.

`validNumerals` is absent from every submitted claim. A separately rebuilt core
definition deleting both validity helpers still proves the universal theorem
with `#Top`, so this defect does not explain the main claim's closure. It
nevertheless prevents treating the submitted verification theory as wholly
sound.

### Imported primitives and claims

The proof path trusts installed K `DOMAINS` hooks/equations for string
concatenation, length, substring, search, non-overlapping occurrence count,
integer arithmetic, and Booleans. The occurrence-count equations split
disjointly on found/not-found and descend for every submitted nonempty numeral
needle. All intended data is ASCII, so Unicode indexing is immaterial.

There are no opaque symbols, `[functional]` declarations, explicit priority
rules, or loop/circularity claims. The sole local `[total]` declaration is the
sound `isNumeral`. Every submitted claim fixes the complete final `VStr`.

Exact witness commands and the independent core-dependence test are in
[static-witnesses.k](evidence/static-witnesses.k),
[stage5-static-witnesses.log](evidence/stage5-static-witnesses.log),
[verification-core.k](evidence/verification-core.k), and
[spec-core.k](evidence/spec-core.k).

## 6. Fresh non-vacuity test

No candidate-provided vacuity artifact was trusted. The fresh
[spec-vacuity.k](evidence/spec-vacuity.k) executes the real
`solutionProgram` on the satisfiable input `"zero"` but changes the
result-constraining destination from `VStr("zero")` to `VStr("one")`.

The `--dry-run` command exited 0, showing the mutation parses and builds against
the fresh definition. The actual proof exited 1 with `WarnStuckClaimState` and
the expected unmet result:

```text
<k>
  VStr ( "zero" ) ~> .K
</k>
```

This is a meaningful proof failure, not a parser error, timeout, or unreachable
mutation. The candidate proof is result-constraining and non-vacuous. Exact
commands and output are in [stage6-vacuity.log](evidence/stage6-vacuity.log).

## 7. Proven versus assumed accounting

### What `#Top` establishes

Under the submitted K theory, the mechanically pinned constructor program
reduces, for every K `String S`, to:

```text
VStr(sortSpec(S))
```

The four ground instances also reduce to their displayed exact strings. The
false-result and body mutations show this theorem discriminates both the
returned value and the executed body.

### Trust and assumption ledger

- **Trusted translator.** The mounted translator is launcher-trusted, and
  regeneration is byte-identical. Dependents: program identity and all claims.
  This boundary is acceptable.
- **Constructor abbreviations.** `block`, `solutionBody`, and
  `solutionProgram` are local equations. Their equality to regenerated
  constructors is machine checked. This boundary is acceptable.
- **K toolchain and `DOMAINS`.** K v7.1.293 and its String/Int/Bool
  hooks/equations are low-level trusted primitives. Dependents: every
  evaluation and claim. Their roles are general operations, not task-answer
  oracles. This is an ordinary explicit trust boundary.
- **Direct-call evaluator.** The specialized `evalProgram` omits a general
  Python environment and call stack, but it pins the exact name, parameter,
  and body and models every material pure operation used. Dependents: the
  universal and ground claims. This specialization is acceptable for the
  submitted program.
- **Python `count`, concatenation, and repetition bridge.** These are modeled
  by K occurrence count, `+String`, and truthful exhaustive `repeatString`
  equations. The actual needles are nonempty numeral literals. Dependents:
  `sortSpec` and the computed result. Concrete K/Python tests support the
  bridge finitely; the ordinary equations supply its mathematical
  justification.
- **Python `strip` bridge.** This is illegitimate as submitted. Its rule admits
  every string but only deletes the last character. The machine-checked
  opposite witness proves a false Python conclusion. The main program invokes
  this bridge. Finite agreement on the actual receiver shape cannot repair the
  missing guard or universal connection theorem.
- **`sortSpec` to the source contract.** The bridge is the ordinary argument
  that each valid numeral's multiplicity is counted and blocks are emitted in
  numeric order. The 11,232-case Python differential supports implementation
  fidelity but does not replace that mathematical interpretation.
- **`validNumerals`.** The symbol is false on empty input and therefore not a
  trustworthy contract recognizer. It is unused by the theorem, as confirmed
  by the successful core rebuild, but remains a defective submitted rule.
- **Termination and exceptions.** The claim is partial correctness. On the
  stated finite-string domain, CPython counting/repetition/concatenation and
  the modeled ground recursion terminate; invalid-token canonical exceptions
  are outside the source contract.

### Gate and decision summary

- Clean dynamic reconstruction: pass.
- Real-program identity, scope, result constraint, and non-vacuity: pass.
- Source-domain adequacy: pass; the main claim is broader, not narrower.
- Rule-level soundness: fail. The on-path `strip` bridge has a broader match
  domain than its justification and makes a false source-language conclusion
  provable. The malformed validity helper is an additional static defect.

This is not the `SOUND-BUT-LIMITED` domain-narrowing case and not an
infrastructure uncertainty. The candidate would need to implement actual
Python strip semantics or syntactically/semantically narrow the bridge to the
proved safe receiver domain, then rebuild and revalidate. Because the immutable
submitted theory has not done so, the benchmark's materially-unsound-semantics
boundary requires `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
