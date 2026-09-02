# Independent adversarial review: 11-string-xor

## Overall finding

The candidate contains a legitimate, result-constraining partial-correctness
proof under the supplied MPY semantics. I rebuilt both definitions from source,
ran the loop claim independently, ran the complete positive claim set, and
obtained exit status 0 with `#Top`. The entry theorem executes an exact K
embedding of the submitted `solution.mpy`; it does not replace the function
call, loop, comparison, concatenation, or return with an oracle. A fresh false
result mutation and a separate body-sensitivity mutation both built and failed
on the expected obligations.

I select `CONCERNS / LEGIT`, rather than an unqualified pass, because four
provenance artifacts explicitly requested by the audit protocol are absent:
`run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`.
Their absence prevents review of the generation history, but it does not
invalidate the independently reconstructed proof.

All commands below ran against reviewer-controlled copies under
`/tmp/audit-work`. No candidate-built definition or cache was used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory is present, so there is no
mode/mount contradiction and no infrastructure breach.

I recursively compared `/candidate/reference-semantics` with the trusted tree
using:

```text
diff --no-dereference -r \
  /reference/reference-semantics \
  /candidate/reference-semantics
```

The command exited 0. The candidate tree has the same directory and regular-file
manifest, no additional or missing entry, and no symlink. The candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted counterparts.
Hashes and complete manifests are in
`/audit-output/evidence/01-input-integrity.log`.

The candidate proof sources and program artifacts are regular files. The
candidate also contains an irrelevant `__pycache__` directory; it was neither
copied into the reconstruction nor used. Source hashes and scratch-copy hashes
are recorded in `/audit-output/evidence/17-source-and-evidence-hashes.log` and
match for `solution.py`, `solution.mpy`, `spec.k`, and `verification.k`.

### Missing provenance evidence

The following requested files are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present. Therefore there were no generation
claims to credit or refute. I did not treat `prove.sh`, candidate tests, or any
candidate prose as authoritative.

**Stage 1 result:** semantics, prompt, translator, and proof-source provenance
are intact; generation-history provenance is incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` requires `string_xor(a, b)` for strings containing only
`0` and `1`, returning their characterwise binary XOR as a string. The trusted
canonical implementation applies XOR to `zip(a, b)`, so the behavior for
unequal lengths is explicitly truncation to the shorter input. The documented
example is:

```text
string_xor("010", "110") == "100"
```

The submitted implementation initializes an empty result, iterates over
`zip(a, b)`, appends `"0"` when the current characters are equal and `"1"`
otherwise, and returns the result. Initializing `x` and `y` is behaviorally
irrelevant to the result but makes the final loop-variable state defined when
the loop is empty. On the intended binary-string domain, the algorithm matches
the canonical one, including empty and unequal-length inputs.

### Trusted translation

I regenerated the MPY artifact with the trusted translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py
```

The regenerated file and submitted `solution.mpy` are byte-identical, with
SHA-256:

```text
6dc4a5199d3c6f87b07ef8a7a901fad25e3105d323aa76e079880a67ce6be154
```

See `/audit-output/evidence/02-translation-identity.log`.

### Independent differential test

The reviewer-authored script is
`/audit-output/evidence/differential_test.py`. It imports the trusted canonical
entry point and the scratch-copy candidate entry point independently. Its exact
scope was:

- 12 explicit cases: the documented example, both-empty and one-empty
  boundaries, unequal lengths, and all four one-character pairs `00`, `11`,
  `01`, and `10`;
- all 16,129 ordered pairs of binary strings where each input length is 0
  through 6;
- 2,000 deterministic generated pairs with each length selected from 0 through
  64.

The command exited 0 over 18,141 total cases with zero mismatches. The script,
seed, explicit inputs, scope, results, and status are preserved in
`/audit-output/evidence/03-python-differential.log`.

**Stage 2 result:** pass. The source is faithful to the natural-language and
canonical behavior, and `solution.mpy` is the trusted translation of that
source.

## 3. Clean proof reconstruction

### Clean source layout

I copied candidate source files, not compiled artifacts, into
`/tmp/audit-work/reconstruction`. The semantics used for compilation were a
fresh copy of the trusted `/reference/reference-semantics`. The scratch
directories did not contain a candidate-provided `*-kompiled` directory.

### Concrete definition and execution

The LLVM definition was built with:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0; see `/audit-output/evidence/05-kompile-runtime.log`.

The reviewer concrete driver is
`/audit-output/evidence/reviewer_concrete.py`. Its function AST is identical to
the candidate function AST, and its MPY translation was made with the trusted
translator. It checks the documented, empty, unequal-length, and all branch
boundary cases. Running it under the fresh LLVM definition exited 0 with empty
`<k>`, `NoExc`, and exit code 0:

```text
krun reviewer_concrete.mpy --definition runtime-kompiled
```

See `/audit-output/evidence/04-concrete-driver-translation.log` and
`/audit-output/evidence/06-krun-reviewer-concrete.log`.

I also ran the exact submitted `solution.mpy` under the fresh definition. It
exited 0 and installed a closure whose body is the exact submitted MPY AST.
That final configuration is in
`/audit-output/evidence/20-krun-submitted-solution.log`.

### Proof definition and positive claims

The Haskell proof definition was built with:

```text
kompile verification.k \
  --backend haskell \
  --main-module STRING-XOR-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; see `/audit-output/evidence/07-kompile-verification.log`.

The loop claim was then run on its own:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module STRING-XOR-SPEC \
  --claims STRING-XOR-SPEC.loop-invariant
```

It exited 0 and printed `#Top`; see
`/audit-output/evidence/08-kprove-loop-invariant.log`.

The entry theorem depends on that loop claim as its circularity. I therefore
ran the complete positive claim set:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module STRING-XOR-SPEC \
  --claims STRING-XOR-SPEC.loop-invariant,STRING-XOR-SPEC.solution-correct
```

It exited 0 and printed `#Top`; see
`/audit-output/evidence/12-kprove-all-positive.log`. Because the loop claim
already closed independently, this aggregate success establishes closure of
the remaining entry claim with its declared support.

For completeness, I attempted a diagnostic run selecting only
`solution-correct`, which also excluded its loop circularity. It kept unrolling
the symbolic loop and was auditor-interrupted after ten minutes. That diagnostic
is documented as exit 130 in
`/audit-output/evidence/09-kprove-solution-correct.log`; it is not used as a
candidate-failure signal.

The compiler warnings concern unused variables in the supplied `strLt` rules
and concrete-backend totality warnings for unrelated supplied functions. None
of those symbols occurs on this program's proof path.

**Stage 3 result:** pass. Both positive targets close in a clean reconstruction,
and the concrete supplied semantics executes the exact program and boundary
tests successfully.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop-invariant` says:

- the current environment is scope `L`;
- `A` and `B` are the remaining binary-code sequences of an exact
  `zipObjS` loop;
- the loop target is exactly `(x, y)` and the loop body is exactly the
  candidate equality test and result append;
- `P` is the accumulated result before the remaining iterations;
- after the loop, the continuation `CONT` is unchanged, `result` is
  `xorAcc(P, A, B)`, and `x` and `y` contain the last consumed characters (or
  their initial values if no pair was consumed);
- the input bindings, parent, unrelated scopes, and framed cells are preserved.

Its precondition requires `A` and `B` to contain only ASCII 48/49 and requires
`L` not to collide with the framed scope map.

`solution-correct` says:

- from the clean MPY configuration, load the exact `stringXorModule` and call
  `string_xor` on arbitrary code sequences `A` and `B`;
- when both sequences contain only ASCII 48/49, execution reaches
  `str(xorAcc(.IntSeq, A, B))`;
- the temporary call frame is removed, the module scope contains exactly the
  installed `string_xor` closure, and environment, scope allocator, heap,
  stack, return state, exception state, and exit code are restored to their
  stated final values.

The return is not a free variable and there is no implication-only result
escape: the same symbolic `A` and `B` from the call appear in the fully defined
`xorAcc` postcondition.

### Satisfiable preconditions and ground substitution

A loop-claim witness is:

```text
L = 1, SC = .Map, PAR = parent(0)
A = [48], B = [49], P = [], X = [], Y = []
```

Both binary predicates are true and `L` is absent from `SC`.

An entry witness is `A = B = .IntSeq`; both binary predicates are true. Ground
substitutions for the documented input, empty input, and both unequal-length
directions reduce as follows:

```text
010 xor 110 -> xorAcc codes [49,48,48] -> "100"
""  xor ""  -> xorAcc codes []         -> ""
10  xor 1   -> xorAcc codes [48]       -> "0"
1   xor 10  -> xorAcc codes [48]       -> "0"
```

All four values match both Python implementations. The exact witness artifact
and command output are in `/audit-output/evidence/claim_witness.py` and
`/audit-output/evidence/11-claim-witnesses.log`.

### Pinning the submitted program

`stringXorModule`, `stringXorClosure`, `stringXorBody`,
`stringXorLoopBody`, and `stringXorTarget` are terminating definitional
constants, not execution shortcuts. Their right-hand sides reproduce every
node in submitted `solution.mpy`: import, function parameters, docstring,
initializations, `zip` call, tuple target, equality comparison, both branch
assignments, concatenation, and return.

The pinning evidence has three independent parts:

1. the trusted translator reproduces submitted `solution.mpy` byte-for-byte;
2. static inspection shows that the K constants reproduce that MPY AST;
3. concrete execution of submitted `solution.mpy` installs the same closure
   printed by the final proof configuration.

The K prover does not read an external MPY file during symbolic proof; it proves
the exact embedded syntax term. Consequently, the external-file-to-term link is
an audited syntactic bridge, not itself a reachability theorem. Here the bridge
is exact rather than approximate.

As an additional sensitivity check, I changed the embedded else branch from
appending `"1"` to appending `"0"` in the isolated artifact
`/audit-output/evidence/verification-body-mutated.k`, rebuilt successfully, and
reran both claims. The proof exited 1 with `WarnStuckClaimState`; the residual
distinguishes the incorrect accumulated 48 from the required accumulated 49
when the two current input codes differ. See
`/audit-output/evidence/18-kompile-body-mutation.log` and
`/audit-output/evidence/19-kprove-body-mutation.log`.

**Stage 4 result:** pass. The claims are satisfiable, execute the real submitted
program term, constrain its result, and are sensitive to its property-bearing
branch.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and dispositions

The reviewer-authored inventory generator is
`/audit-output/evidence/k_inventory.py`. Its complete line-numbered output is
`/audit-output/evidence/rule-inventory.md`. It enumerates all supplied
semantics files, `verification.k`, and `spec.k`:

- 237 syntax declarations;
- 1 configuration;
- 5 contexts;
- 476 equational rules;
- 238 operational rules;
- 2 claims;
- all modules, imports, includes, and attributes;
- 1,126 total top-level records.

The inventory records every `function`, `total`, `symbol`,
`no-evaluators`, `priority`, `owise`, `concrete`, strictness, and macro
attribute. No `functional` declaration and no simplification/simplifier rule is
present. Generation command, status, size, and hash are in
`/audit-output/evidence/16-regenerate-rule-inventory.log`; focused special-rule
output is in `/audit-output/evidence/15-special-rule-attributes.log`.

Every inventoried supplied-semantics item has one of two dispositions:

1. **Used-path rule/declaration:** reviewed below against the exact program
   transition it implements.
2. **Constructor-, sort-, or literal-disjoint rule:** unreachable from this
   program and from all proof-local terms. It contributes no rewrite or equation
   to claim closure. This includes the unused behavior in `assert.k`, `bool.k`,
   `comprehension.k`, `concrete.k`, `dict.k`, `float.k`, `int.k`, `list.k`,
   `methods.k`, `range.k`, `set.k`, `sort.k`, and `subscript.k`, plus the
   unused cases in the partially used files.

Because the mode is `SUPPLIED_SEMANTICS`, those unchanged rules are the selected
fixed semantic theory, not candidate proof extensions. I do not infer full
Python fidelity for their unused constructs; the relevant question is whether
any can rewrite the reachable terms or introduce a false result here. Their
head constructors, value sorts, operator strings, builtin names, or guards
exclude that.

### Program construct-to-rule map

| Submitted construct | Declaration and operative rules | Review |
|---|---|---|
| `Module`, statement list | `syntax.k:56,61`; `core.k:124-127` | Loads and sequences each submitted statement in order. |
| `ImportFrom("typing","List")` | `syntax.k:43`; `controls.k:35-44` | The non-`math` owise rule makes this unused typing import a no-op, matching its runtime irrelevance. |
| `FuncDef`, closure | `syntax.k:53`; `functions.k:14-16` | Installs the exact parameter list/body at module scope 0. |
| Function and `zip` calls | `call.k:20-21,31,69-74`; `core.k:185-191` | Evaluates callee then arguments left-to-right, dispatches the builtin, allocates the call frame, binds arguments, and preserves the continuation. |
| Name lookup/binding | `core.k:129-154`; `functions.k:63-75`; `controls.k:9-18` | Resolves local parameters/result/loop variables before builtins; plain-frame assignments update the current scope. Cell rules have false guards here. |
| String literals | `str.k:13-17` | Converts the fixed ASCII literals to their exact code sequences. |
| `zip(a,b)` | `builtins.k:163-174` | Creates `zipObjS`, yields one-character string pairs in order, and stops when either input is empty. |
| `For` and iteration | `controls.k:62-74`; `iter.k:8` | Evaluates the iterable once, binds each yielded tuple, executes the body, then advances the exact residual iterator. |
| Tuple target `(x,y)` | `tuple.k:31-46,49-57` | Unpacks the two yielded values left-to-right into the current scope. |
| `Compare(x == y)` | `operators.k:14-17`; `str.k:25` | Evaluates both operands and compares the one-character code sequences structurally. |
| `If` | `controls.k:50-54`; `core.k:198-205` | Uses the resulting Boolean and chooses exactly one branch. |
| String `+` | `operators.k:12`; `str.k:20-24` | Concatenates the accumulated code sequence with the selected one-character string. |
| `Return` and frame cleanup | `functions.k:77-90` | Evaluates the result, records it, restores the caller continuation/environment, deletes the callee frame, and resets the scope allocator. |

Evaluation order is therefore the submitted order: arguments left-to-right,
each `zip` pair left-to-right into `x` and `y`, comparison before branch,
concatenation before assignment, and return after loop completion. The program
allocates no heap object; the proof correctly keeps `<heap>` empty and
`<heapLoc>` at 0. The only scope allocation is the call frame, which is removed
by `#pop`. No exception, output, break/continue, or abrupt-return path is
abstracted.

The potentially overlapping fixed priority rules are cell- or heap-reference
specializations. The call frame has no `"$cells"` marker and the heap is empty,
so those guards cannot overlap the plain assignment, parameter binding, tuple
binding, comparison, or concatenation rules on this execution. The generic
call and comparison rules are `owise`, but there is no proof-local interception
and no higher-priority matching special call. Thus priority does not bypass the
program.

### Proof-local declarations and rules

`verification.k` adds 10 syntax-declaration records and 19 equational rules. It
adds no operational `<k>` rewrite, priority rule, simplification rule, opaque
symbol, or unconstrained result.

- `binaryCode(C)` is total and exactly tests `C == 48 or C == 49`.
- `xorCode(A,B)` has two disjoint guards under `binaryCode(A)` and
  `binaryCode(B)`: equality returns 48 and inequality returns 49. The two guards
  cover every use in `xorAcc`; there is no overlap.
- `xorAcc(P,A,B)` has three constructor-disjoint cases: left empty, left
  nonempty/right empty, and both nonempty. The recursive case consumes one
  constructor from both inputs and appends the correct `xorCode`, so it
  terminates and implements truncation to the shorter input.
- `binaryCodes` is a total structural recursion over `IntSeq`.
- `xorLastX` and `xorLastY` have the same three exhaustive,
  constructor-disjoint cases as `xorAcc`; each recursive call consumes both
  remaining sequences and records the just-consumed one-character code.
- `stringXorTarget`, `stringXorLoopBody`, `stringXorBody`,
  `stringXorClosure`, and `stringXorModule` each have one ground defining
  equation. They are terminating exact syntax abbreviations. They neither
  summarize nor replace an executing source operation.

The `loop-invariant` claim is the sole execution summary. It matches the exact
`#loop(zipObjS(A,B), stringXorTarget, stringXorLoopBody)` and accepts an
arbitrary continuation while preserving that continuation. Its universal match
domain includes the full current environment and modified scope and frames all
other configuration cells. The body has no heap, control-stack, exception, or
abrupt-control effect. The claim itself closes under the fixed semantics without
an operational bridge, providing the required connection theorem from exact
loop execution to `xorAcc`/`xorLastX`/`xorLastY`.

There is no circular result oracle: `xorAcc` is independently and exhaustively
defined, and no rule rewrites the source loop or call directly to it. The same
symbol in the postcondition is justified by the proved loop reachability claim,
not merely by being named in both execution and specification.

### Opaque and special supplied symbols

The supplied theory declares these symbolic/opaque operations:

```text
sortVS, sortKeyVS,
intFloatDiv, divII, floatMod, floatLt, absF, floorFI, toF, ceilF,
subF, divF, addF, mulF, powF, gtF, eqF, decStrToF,
divFloatIntV, intToF, truncF, roundF, roundFN, sqrtF,
md5hexCodes
```

None appears in `solution.mpy`, `verification.k`, either claim, or a reachable
right-hand side on this execution. They influence neither control nor the final
result. The program's only result-bearing mathematical functions are the fully
defined `binaryCode`, `xorCode`, `xorAcc`, and fixed `seqConcat`.

I found no unsound candidate rule and therefore make no unsoundness allegation
requiring a false-conclusion witness. The two failing mutations below are
sensitivity/non-vacuity witnesses, not allegations that an original rule is
false.

**Stage 5 result:** pass. The complete source inventory contains no
proof-local execution bypass, unconstrained oracle, false overlap, priority
abuse, or reachable opaque value.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I created the fresh mutation
`/audit-output/evidence/spec-false.k`. It keeps the original supporting loop
claim and changes only the entry result to:

```k
str(seqConcat(xorAcc(.IntSeq, A, B), iCons(48, .IntSeq)))
```

This demands one extra trailing `"0"`. The ground witness
`A = B = .IntSeq` satisfies the original precondition; the actual result is
`""`, while the mutation requires `"0"`.

The mutated spec parsed and compiled to KORE successfully with `kprove
--dry-run`, exit 0; see
`/audit-output/evidence/13-false-mutation-dry-run.log`. The actual proof exited
1 with `WarnStuckClaimState` and the expected failed implication:

```text
seqConcat(xorAcc(.IntSeq,A,B), iCons(48,.IntSeq))
  #Equals xorAcc(.IntSeq,A,B)
```

It failed after reaching the real final result configuration, not from a parser
error, missing import, unrelated crash, or unreachable claim. Full residual and
status are in `/audit-output/evidence/14-kprove-false-mutation.log`.

**Stage 6 result:** pass. The proof discriminates a meaningful false result.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY theory, for arbitrary finite `IntSeq` values `A` and `B`
whose elements are ASCII 48 or 49, executing the exact submitted function from
the stated clean configuration reaches a returned string that:

- has length `min(length(A), length(B))`;
- has code 48 at each consumed position when the two input codes are equal;
- has code 49 at each consumed position when they differ;
- is exactly `xorAcc(.IntSeq,A,B)`;
- leaves only the installed module closure and restores the stated environment,
  scope allocator, empty heap, heap allocator, empty stack, return state,
  exception state, and exit code.

This is a partial-correctness report. I do not elevate it to a separately proved
termination theorem, even though the concrete finite loop and structurally
decreasing summary are terminating.

### Trust ledger

| Boundary | Effect and dependents | Evidence and judgment |
|---|---|---|
| K parser, compiler, Haskell backend, and reachability logic | Underlie both `#Top` results and both failing mutations. | Necessary machine-checking trust boundary; fresh builds and coherent positive/negative behavior support it. |
| Trusted supplied semantics tree | Defines execution, state, calls, loop behavior, strings, and `zip`. | Mandated by `SUPPLIED_SEMANTICS`; candidate tree is exactly identical. Used-path rules were statically reviewed and concretely exercised. Acceptable. |
| K built-in Int/Bool/String/Map/List/K equality operations | Implement code comparison, map state, and structural sequences. | Low-level mathematical/runtime primitives, not task-answer oracles. Acceptable. |
| External `solution.mpy` to `stringXorModule` syntax link | Pins the file being audited to the term proved. | Trusted-translator byte identity, exact static AST comparison, and concrete closure output. Strong audited bridge, but external to the reachability theorem itself. |
| Meaning of `xorAcc` as binary XOR | Connects the formal postcondition to the English word “XOR.” | Fully defined equations: equal binary codes map to `0`, unequal binary codes map to `1`, stopping at `zip` exhaustion. Ordinary mathematical inspection; no opaque value. Acceptable. |
| Canonical/Python comparison | Supports implementation-to-intent fidelity. | Independent canonical source plus 18,141 finite differential cases with zero mismatches. Empirical support only; not substituted for the K proof. |
| Supplied opaque symbols listed in Stage 5 | Could model sort, float, or digest behavior in other programs. | None is reachable or result-bearing here; no claim depends on one. Acceptable nondependency. |
| Missing generation metadata | Would describe how the candidate was produced. | Four requested files are absent. This limits provenance auditability but not reconstructed theorem soundness. Concern. |

The body-sensitivity failure shows that the proof relies on the source branch
semantics. The false-postcondition failure shows that it constrains the final
result. Differential testing supports only the source/canonical and
external-file bridges; the universal program theorem comes from `kprove`.

**Stage 7 result:** the proof is legitimate and its trust boundaries are
acceptable for this theorem. Generation-history auditability remains the sole
documented concern.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
