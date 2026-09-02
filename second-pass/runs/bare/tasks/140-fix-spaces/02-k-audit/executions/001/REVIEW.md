# Independent adversarial review: 140-fix-spaces

## Outcome

This is a legitimate, result-constraining K reachability proof of the submitted
constructor program under the candidate's generated, idealized semantics. A
clean source rebuild produced `#Top`; the actual `solution.mpy` function map was
matched byte-for-byte against the function map used by the claims; every used
language construct has an operational rule; no rule bypasses either submitted
function; and a fresh false-result claim parsed but failed at the expected final
result.

The result has concerns rather than a clean pass:

1. The trusted canonical and the submitted implementation disagree for a final
   run of exactly two spaces. For example, the submission returns `"a__"` for
   `"a  "`, while the canonical returns `"a_"`. The submission agrees with a
   literal run-based reading of the prompt on this case, so the trusted prompt
   and trusted canonical are themselves in tension.
2. The generated K semantics has an unbounded call model and no
   `RecursionError`. The recursive submitted CPython function raises
   `RecursionError` on tested 1,100-character inputs for which the iterative
   canonical and the direct prompt oracle return normally.

Those are material intent and execution-model limitations. They do not let the
K theory prove a false result about a modeled execution and therefore do not
make the reconstructed proof illegitimate.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The required boundary holds:
`/reference/reference-semantics` is absent. The trusted mount contains exactly
the three expected inputs, and K 7.1.293 is installed. See
[00-infrastructure-and-tree.log](/audit-output/evidence/00-infrastructure-and-tree.log).

The required candidate source artifacts are all regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. There are no source symlinks and no helper K files. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to the trusted files:

- prompt SHA-256:
  `f757e5d21a3d47b21dcd96c7c9f869adfbfe70276370fddb0f4ded8fb1c311f9`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The comparisons and complete provenance inventory are recorded in
[01-provenance-integrity.log](/audit-output/evidence/01-provenance-integrity.log).
No required artifact is missing, changed, mistyped, additional, or symlinked.

The candidate also contains `semantic-kompiled/` and
`verification-kompiled/`. These are generated caches, not source inputs. I did
not copy or use them. `run-input.json` identifies problem `140-fix-spaces`,
condition `bare`, and no supplied semantics, consistent with the rendered mode.
`metrics.json`, `codex-last.txt`, `codex-output.log`, and the structured JSONL
trace claim a successful generation and `#Top`; I read them only as untrusted
provenance. No candidate `PROOF.md` or `spec-vacuity.k` exists.

Only the candidate source deliverables and the trusted reference files were
copied into `/tmp/audit-work/src`; hashes of that scratch copy are in
[02-scratch-copy.log](/audit-output/evidence/02-scratch-copy.log).

Stage result: integrity pass; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The prompt says to replace spaces with underscores, except that a run of more
than two consecutive spaces becomes one hyphen. A direct run-based reading is:

- a run of one space becomes `_`;
- a run of two spaces becomes `__`;
- a run of at least three spaces becomes `-`;
- non-space characters are preserved.

The trusted [canonical.py](/reference/canonical.py:6) implements that behavior
for internal runs, but its final-run branch at lines 32–35 emits only one
underscore for either one or two trailing spaces. The recursive submitted
[solution.py](/candidate/solution.py:1) emits two underscores for a final
two-space run and otherwise implements the run-based reading. Its helper drops
the remainder of a run after the first three spaces.

The trusted translator regenerated the submitted constructor tree with byte
identity. Both files have SHA-256
`1cf1f5712a4eb9e60c1d5567ffac3ab3a9267a726459cfcb53c6fc6786e8fd01`;
see
[03-translation-byte-identity.log](/audit-output/evidence/03-translation-byte-identity.log).

### Independent differential evidence

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and the submitted entry point independently. It also contains
a third, independently written run-based oracle. Its complete inputs are in
[differential_inputs.jsonl](/audit-output/evidence/differential_inputs.jsonl).
The scope was:

- all four documented examples;
- 34 explicit cases covering empty input, each decision boundary, leading,
  internal, and trailing runs of lengths 1–4, mixed characters, Unicode, and
  lengths around CPython's recursion limit;
- every string over `{space, "a", "b"}` of lengths 0 through 8;
- 9,855 unique inputs in total.

The command and full bounded summary are in
[04-differential-test.log](/audit-output/evidence/04-differential-test.log).
The nonzero status intentionally reports observed behavioral differences, not a
harness failure:

- all four documented examples passed;
- there were 731 submission/canonical differences: 729 final-two-space
  differences in the short scope and two `RecursionError` differences at length
  1,100;
- there were two submission/direct-prompt-oracle differences, both
  `RecursionError` cases at length 1,100;
- the submitted program agreed with the direct prompt oracle on every tested
  normally returning input.

Concrete witnesses are:

- `"a  "`: submitted `"a__"`, canonical `"a_"`, prompt oracle `"a__"`;
- `"a" * 1100`: submitted `RecursionError`, canonical and prompt oracle return
  the unchanged string;
- `" " * 1100`: submitted `RecursionError`, canonical and prompt oracle return
  `"-"`.

Stage result: translation and ordinary functional behavior pass, with a
material canonical discrepancy and an unmodeled CPython recursion boundary.

## 3. Clean proof reconstruction

I ignored both candidate-provided compiled directories and built new
definitions under `/tmp/audit-work/src`.

The generated semantics compiled from source with:

```text
kompile --backend haskell semantic.k --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition audit-semantic-kompiled
```

It exited 0; see
[05-kompile-semantic.log](/audit-output/evidence/05-kompile-semantic.log).

The reviewer-authored
[concrete_semantics_test.py](/audit-output/evidence/concrete_semantics_test.py)
then ran the actual `solution.mpy` through this fresh definition on 17 normal
and boundary inputs. Every `krun` exited 0 and every K result equaled the
submitted Python result. Inputs include the examples, empty input, run lengths
1–4, internal and trailing runs, and non-ASCII text. The expected three
canonical discrepancies for final two-space runs remain explicit. See
[06-concrete-semantics-vs-python.log](/audit-output/evidence/06-concrete-semantics-vs-python.log).
Two earlier reviewer-harness parser mistakes are preserved as
`06a-...` and `06b-...`; neither was treated as candidate evidence.

The proof definition compiled from source with:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0; see
[07-kompile-verification.log](/audit-output/evidence/07-kompile-verification.log).
The two claims form one mutually circular proof target, so they must be supplied
together. The candidate's positive command was independently rerun:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

It exited 0 and printed exactly `#Top`; see
[08-kprove-positive.log](/audit-output/evidence/08-kprove-positive.log).

Stage result: clean reconstruction pass.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The first [spec.k claim](/candidate/spec.k:10) has no explicit `requires`
condition. For every finite structural string `S`, arbitrary continuation `K`,
arbitrary current input/environment/result cells, and exactly the submitted
function map, it says:

> Calling `fix_spaces` with `pyStr(S)` returns exactly `pyStr(fixRef(S))`,
> resumes the same continuation, and preserves the framed cells.

The second [spec.k claim](/candidate/spec.k:21) has the same pre-state shape and
says that `_drop_spaces` returns exactly `pyStr(dropRef(S))`.

These are result-constraining equivalences, not existential results,
implications, or tautologies. `S`, `K`, and the framed cell variables are
universally quantified; there is no fresh opaque result on the right.

Satisfying states plainly exist. For example, choose `K = .K`,
`INPUT = ""`, `ENV = .Env`, `RESULT = .K`, and the required
`FUNS = solutionFuns`. Choose:

- `S = ch("a") sp sp .PString` for `fix_spaces`, yielding `"a__"`;
- `S = sp sp ch("a") sp sp .PString` for `_drop_spaces`, yielding `"a__"`.

The independent ground claims in
[spec-ground-witnesses.k](/audit-output/evidence/spec-ground-witnesses.k)
execute those states without importing the candidate spec. They produced
`#Top` with exit 0
([09b-ground-claim-kprove.log](/audit-output/evidence/09b-ground-claim-kprove.log)).
Direct submitted Python gives the same two results
([09c-ground-python-results.log](/audit-output/evidence/09c-ground-python-results.log)).
For the first witness, the trusted canonical entry point instead gives `"a_"`,
as already recorded in Stage 2.

### Pinning the submitted program

The claims do not start with `Module(...)`; they run the ordinary interpreter
with `solutionFuns` in the `<funs>` cell. This would be a substitution risk if
`solutionFuns` differed from the submitted module.

It does not differ. The rule at
[verification.k lines 18–49](/candidate/verification.k:18) is the exact two
`FuncDef` constructor bodies in [solution.mpy](/candidate/solution.mpy:1).
For a machine-observable check, I compiled the same source with the
`VERIFICATION` parser exposed, ran the actual `solution.mpy` for one semantic
step, ran the `Verify` wrapper for one semantic step, extracted both complete
`<funs>` cells, and compared them. They have the same SHA-256
`ad2faaa3d29664e71951e8b17f121d22bd9b8856fc990785c9847f3d2802f392`;
`cmp` exited 0. See
[15-kompile-pinning-parser.log](/audit-output/evidence/15-kompile-pinning-parser.log)
and
[16-program-pinning-depth1.log](/audit-output/evidence/16-program-pinning-depth1.log).

Both function bodies execute through ordinary `call`, `enter`, `exec`, `eval`,
and return rules. There is no `fix_spaces` or `_drop_spaces` summary rule that
preempts a body. The helper claim matches the actual helper invocation and is
needed by the mutual recursion.

The formal postcondition is the structural `fixRef` relation. It agrees with the
literal prompt reading, but not with the trusted canonical on exactly the
trailing-two-space boundary. This is an implementation/reference adequacy
disagreement, not a free or unconstrained result.

Stage result: real-program pinning and formal result adequacy pass; natural
intent/canonical alignment has the stated concern.

## 5. Rule-by-rule static soundness review

The numbered source and declaration index are preserved in
[10-static-source-inventory.log](/audit-output/evidence/10-static-source-inventory.log).
There are no generated helper K files beyond the three reviewed K sources.

### Syntax, configuration, attributes, and construct coverage

`MPY-SYNTAX` declares:

- `Program = Module(Stmts)`;
- statement lists and `FuncDef`, `Return`, and `If`;
- parameter and expression lists;
- `Name`, `Str`, `Int`, `BinOp`, `Compare`, `Call`, and `Subscript`;
- comparison operators, integer indices, slices, bounds, and `NoBound`.

`MPY-SEMANTIC` adds structural strings, values, environments, function maps,
closures, the `<py>` configuration, and explicit continuation terms. The
configuration has exactly the state needed here: `<k>`, `<input>`, `<env>`,
`<funs>`, and `<result>`.

The `solution.mpy` construct map is exhaustive:

| Submitted construct | Declaration | Behavior |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | semantic.k 8–16 | module loading, `collect`, lookup, call entry |
| `If`, `Return` | semantic.k 11–13 | lines 133–139 |
| `Name`, `Str`, `Int` | semantic.k 19–21 | lines 142–144 |
| string `BinOp("+",...)` | semantic.k 22 | lines 146–148 |
| one-element `Compare` with `==` or `>` | semantic.k 23, 27–28 | lines 150–155 and decision machines |
| `Call` of `len`, `fix_spaces`, `_drop_spaces` | semantic.k 24 | lines 157–161 and call rules |
| integer subscript and slices `0:3`, `1:`, `3:` | semantic.k 25, 30–32 | lines 163–168 and `pindex`/`pdrop`/`ptake` |

No submitted construct is silently fabricated or left unmodeled.

The local `[function]` symbols are `decode`, `decodeChar`, `encode`, `collect`,
`lookupFun`, `lookup`, `sconcat`, `pconcat`, `pdrop`, `ptake`, `pindex`,
`solutionFuns`, `fixRef`, and `dropRef`. There are no `[total]`,
`[functional]`, `[simplification]`, or `[concrete]` declarations and no
explicit priority rules. The only priority-like attribute is the truthful
`[owise]` non-space case of `decodeChar`. There are no opaque result symbols.
Operational continuation symbols such as `finishCall`, `cmpApply`, and
`subApply` all have rules on every state reachable from this program.

### `semantic.k` ordinary rules

Each source rule was classified and checked as follows:

| Line(s) | Rule decision |
|---|---|
| 63–65 | `Module` collects the actual top-level definitions and calls the required entry point on decoded input. Sound for this module, whose top level contains only function definitions. |
| 67–69 | A top-level returned `pyStr` empties `<k>`, clears functions, and writes the encoded result. Exact `<k>` matching prevents it from firing inside a call continuation. |
| 74 | `decode("") = .PString`; true base equation. |
| 75–76 | Nonempty `decode` removes exactly one K string unit and recurses on the suffix; structurally descending. |
| 79 | A decoded literal space becomes `sp`; true. |
| 80 | The `[owise]` case becomes `ch(C)` only when line 79 does not match; disjoint. `decode` supplies one-unit substrings. |
| 83 | Empty structural string encodes to `""`; true. |
| 84 | `sp REST` encodes one space then the rest; true. |
| 85 | `ch(C) REST` encodes `C` then the rest; true on reachable decoded strings. |
| 89 | Empty statement collection gives an empty function map; true. |
| 90 | Each top-level `FuncDef` is collected in source order; true for the submitted module. `collect` is intentionally partial on non-definition top-level statements and is not declared total. |
| 93 | Matching function-map head returns its closure; true. |
| 94–95 | A differently named head is skipped under a disjoint inequality guard; true and descending. Missing names remain visibly stuck. |
| 98 | Matching environment head returns its bound value; true. |
| 99–100 | A differently named binding is skipped under a disjoint guard; true and descending. Missing variables remain visibly stuck. |
| 121–122 | `call` resolves the named submitted function through the actual map; no body bypass. |
| 123–125 | `enter` binds the sole parameter, saves the complete old environment, and begins the real body. Correct for both one-argument definitions. |
| 126–127 | A returned value restores the saved environment and preserves the continuation. Correct call/return control. |
| 130 | Concatenating an empty statement list returns the second list; true. |
| 131 | `sconcat` preserves the head and descends through the first list; true. |
| 133 | `Return(E)` evaluates `E` and discards the remaining function statements, matching return control. |
| 134–135 | `If` evaluates its condition before selecting a branch and saves the following statements. |
| 136–137 | True selects `THEN` and then the saved suffix; correct. |
| 138–139 | False selects `ELSE` and then the saved suffix; correct. |
| 142 | `Name` reads the current environment; correct for parameter `text`. |
| 143 | String literals decode into structural strings; correct. |
| 144 | Integer literals become `pyInt`; correct. |
| 146 | Binary evaluation starts with the left operand; correct Python order. |
| 147 | After the left value, the right operand is evaluated; correct order. |
| 148 | The used string `+` concatenates left `A` before right `B`; correct. No unsupported operator is fabricated. |
| 150–151 | The used single comparison evaluates its left operand first. Chained comparisons are outside this program. |
| 152 | Comparison then evaluates the right operand and retains the left value; correct order. |
| 153 | Structural string `==` delegates to the explicit equality machine. |
| 154 | Integer `A > B` is computed with the operands in the correct order. |
| 155 | `len(A) > B` delegates to the explicit length machine; used only with `B = 2`. |
| 157 | The unshadowed built-in `len` evaluates its argument first. The submitted environment cannot shadow `len`. |
| 158 | Length of a structural string becomes `pyLen(S)` for explicit comparison. |
| 159–160 | A non-`len` named call evaluates its argument first; the inequality guard is disjoint from line 157. |
| 161 | The evaluated argument is passed to ordinary function call machinery. |
| 163 | Subscript evaluation evaluates the base before applying the already-syntactic index; all submitted indices are constant expressions. |
| 164 | Integer indexing uses `pindex`; submitted index 0 is reached only after a nonempty check. |
| 165–166 | Open-ended slicing drops `L`; submitted starts 1 and 3 are in bounds on every reached path. |
| 167–168 | Bounded slicing drops `L` then takes `U-L`; correct for submitted `0:3`, including short strings. |
| 172 | Empty equals empty. |
| 173 | Empty differs from a leading `sp`. |
| 174 | Empty differs from a leading `ch`. |
| 175 | Leading `sp` differs from empty. |
| 176 | Leading `ch` differs from empty. |
| 177 | Two leading spaces are equal exactly when their tails are equal. |
| 178 | Leading `sp` differs from leading `ch`. |
| 179 | Leading `ch` differs from leading `sp`. |
| 180 | Equal leading `ch(C)` values reduce equality to the tails. |
| 181–182 | Unequal leading character payloads yield false under a guard disjoint from line 180. Thus lines 172–182 are exhaustive and nonoverlapping on `PString × PString`. |
| 184–185 | An empty string is not longer than nonnegative `N`; used domain and guard are correct. |
| 186 | A nonempty `sp` string is longer than zero. |
| 187 | A nonempty `ch` string is longer than zero. |
| 188–189 | For positive `N`, remove a leading `sp` and decrement `N`; true and descending. |
| 190–191 | The corresponding leading-`ch` case is true and descending. Lines 184–191 decide exactly `length(S) > N` for used nonnegative `N`. |
| 194 | Empty prefix concatenation returns `B`; true. |
| 195 | Concatenation preserves a leading `sp` and descends. |
| 196 | Concatenation preserves a leading `ch(C)` and descends. These three cases are total on structural strings. |
| 199 | Dropping zero returns the original string; true. |
| 200 | Positive drop removes one leading `sp` and decrements; true. |
| 201 | Positive drop removes one leading `ch` and decrements; true. `pdrop` intentionally remains stuck for negative or out-of-bounds drops; neither is reachable here. |
| 204 | Taking zero returns empty; true. |
| 205 | Taking a positive amount from empty returns empty; true. |
| 206 | Positive take preserves a leading `sp` and decrements. |
| 207 | Positive take preserves a leading `ch` and decrements. These cases cover every reached nonnegative take. |
| 210 | Index zero of leading `sp` returns the one-element space string; true. |
| 211 | Index zero of leading `ch(C)` returns that one-element string; true. |
| 212 | Positive index skips a leading `sp` and decrements; true. |
| 213 | Positive index skips a leading `ch` and decrements; true. Out-of-range and negative indices remain visibly stuck and are unreachable in the submitted control flow. |

State and control footprints are exact for the used subset. Module loading
changes `<funs>`; call entry changes `<env>`; return restores it; finalization
changes `<funs>` and `<result>`; the other evaluator rules affect only `<k>`.
No rule silently changes input, result, or bindings. There is no allocation,
heap, I/O, exception, or global mutation in the submitted program.

### `verification.k` rules and claims

| Line(s) | Rule decision |
|---|---|
| 9–10 | `Verify(S)` is a new test wrapper that installs `solutionFuns` and calls the ordinary `fix_spaces` body. It does not preempt any source construct. |
| 11–12 | `VerifyDrop(S)` is the analogous helper wrapper. |
| 18–49 | `solutionFuns` is a definitional constant for the exact submitted constructor bodies. Stage 4 independently pins it to the actual module. It is not an oracle and carries no result. |
| 55 | `fixRef(empty) = empty`; true. |
| 56 | A non-space head is preserved and recursion descends; true. |
| 57 | A final one-space run becomes one underscore; true under the prompt reading and the canonical. |
| 58 | One space before a non-space becomes `_`, preserves that character, and resumes; true. |
| 59 | A final two-space run becomes two underscores; true under the literal prompt reading, but this is the exact point of disagreement with the canonical witness `"  "` → `"_"`. The equation is not mathematically inconsistent; it defines the theorem's reference relation. |
| 60 | Two spaces before a non-space become two underscores and resume; agrees with prompt and canonical. |
| 61 | Three or more leading spaces emit one hyphen, then `dropRef` consumes the rest of that run; true under the prompt reading. |
| 64 | `dropRef(empty) = empty`; true. |
| 65 | `dropRef` removes a leading space and descends; true. |
| 66 | On a non-space, `dropRef` preserves it and resumes `fixRef`; true. |

The `fixRef` cases are pairwise constructor-disjoint and exhaustive over finite
`PString`; the `dropRef` cases are likewise disjoint and exhaustive. Recursive
calls descend structurally. The two [spec.k](/candidate/spec.k:10) claims are
reachability circularities, not ordinary semantic rules. They execute the
exact bodies and summarize calls on structurally smaller suffixes. No local
simplification lemma, operational bridge, priority rule, opaque value, or
unconstrained oracle contributes to closure.

### Language-model limitation, not an unsound local rule

The semantics intentionally omits CPython's finite recursion limit and
`RecursionError`. Therefore its unbounded recursive execution is not a complete
model of resource-bounded CPython. The length-1,100 witnesses in Stage 2 expose
that bridge gap. I do not label any local recursion rule unsound: within the
idealized language defined here, ordinary call/return behavior is consistent
and no rule concludes a wrong `PString`. The narrower supported claim is about
normal execution in an unbounded-stack Python subset.

Stage result: static soundness pass for every local rule and every construct
used by the submitted program; execution-model and canonical adequacy concerns
remain.

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation artifact.

An initial reviewer mutation changed the universal result to prefix `"!"`. It
parsed, but the backend stopped earlier on `DecidePredicateUnknown`; that is not
an unmet-result residual and is explicitly rejected as non-vacuity evidence.
It remains visible in
[11-vacuity-dry-run.log](/audit-output/evidence/11-vacuity-dry-run.log) and
[12-vacuity-proof-failure.log](/audit-output/evidence/12-vacuity-proof-failure.log).

The valid fresh mutation is
[spec-vacuity-ground-audit.k](/audit-output/evidence/spec-vacuity-ground-audit.k).
It keeps the realizable entry state

```text
S = .PString, K = .K, INPUT = "", ENV = .Env,
FUNS = solutionFuns, RESULT = .K
```

but falsely requires `fix_spaces("")` to return `"!"`.

The dry run compiled this spec successfully and exited 0; see
[13-ground-vacuity-dry-run.log](/audit-output/evidence/13-ground-vacuity-dry-run.log).
The actual proof exited 1 with `WarnStuckClaimState`. Its final residual is the
fully terminated configuration with `<result> "" ~> .K </result>`, which does
not unify with the false destination. This is the expected unmet result, not a
parser error, timeout, or unrelated crash; see
[14-ground-vacuity-proof-failure.log](/audit-output/evidence/14-ground-vacuity-proof-failure.log).

Stage result: non-vacuity pass.

## 7. Proven versus assumed accounting

### What is formally proved

Under `MPY-SEMANTIC`, for every finite structural string `S`:

- execution of the exact submitted `fix_spaces` constructor body from the
  claimed call state returns exactly `pyStr(fixRef(S))`;
- execution of the exact submitted `_drop_spaces` body returns exactly
  `pyStr(dropRef(S))`;
- the saved continuation resumes and the framed input, old environment, and
  result state are preserved.

This is partial correctness. It is not a K termination theorem, a CPython
resource theorem, or a theorem that `fixRef` equals the trusted canonical.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, parser, Haskell backend, and reachability logic | all build, run, and proof results | Necessary low-level trusted base; fresh source reconstruction avoids candidate caches. |
| K built-in `Bool`, `Int`, and `String` primitives, including integer comparison/subtraction and string length/substring/concatenation | decode/encode, comparisons, slices | Acceptable fixed primitive boundary; operations are outside the submitted program-defined code. |
| Trusted `/reference/py2mpy.py` | bridge from `solution.py` to `solution.mpy` | Acceptable input boundary; regenerated bytes are identical. This establishes syntactic identity, not translator semantic correctness, which is trusted by the audit instructions. |
| Generated `MPY-SEMANTIC` as a Python-subset model | bridge from the K theorem to Python behavior | Audited rule-by-rule and concretely supported on 17 cases. Sound for every used construct in its idealized normal-execution subset, but does not model CPython stack limits or exceptions. |
| `solutionFuns` hardcoded constructor data | both entry claims | Acceptable after exact source inspection and the fresh depth-one `<funs>` byte comparison. It contains no computed answer. |
| `fixRef`/`dropRef` structural definitions | final postconditions | Truthful, terminating definitions of the literal prompt reading. The reachability proof connects execution to them. Their identification with English intent is an informal bridge supported by finite differential tests, not a separate K theorem. |
| Trusted canonical as task oracle | intent judgment only | Concerning: it disagrees with `fixRef` and the submission for exactly two trailing spaces. No proof rule assumes canonical equivalence. |
| CPython unbounded-normal-execution idealization | applicability to long real inputs | Concerning: 1,100-character witnesses raise `RecursionError` in the submission while K, canonical, and prompt-level mathematics have a value. |

There are no opaque program-derived symbols, fresh result variables, empirical
operational bridges, or proof-local rules that skip the submitted body.
Differential and concrete tests support only the finite bridges they exercise;
they are not substituted for the `kprove` result.

### Gate accounting and verdict rationale

- Real-program soundness: pass. The bodies execute, program data is pinned,
  results are exact, local equations are consistent, and the valid false-result
  mutation is rejected.
- Intent adequacy: concern. The trusted canonical conflicts with the theorem at
  the trailing-two-space boundary, and actual CPython recursion bounds are
  outside the generated semantics.
- Evidence auditability: pass with the same stated scope limits. Commands,
  statuses, sources, inputs, and bounded outputs are preserved under
  `/audit-output/evidence/`.

The reconstructed proof is therefore legitimate but cannot receive an
unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
