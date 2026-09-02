# Independent adversarial review: 38-decode-cyclic

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program under its generated K semantics. The
proof reconstructs cleanly, pins the immutable `solution.mpy` term, is
body-sensitive, and rejects a fresh false postcondition. I assign
`CONCERNS / LEGIT`, rather than `PASS`, for two non-fatal validation limits:
the equivalence between the K summary `decodeFrom` and the prompt's supplied
`encode_cyclic(encode_cyclic(s))` characterization is an elementary but
informal intent bridge, and direct non-ASCII `krun -cS` injection has a
serialization mismatch that required compiled K-literal tests. Neither limit
makes a false conclusion provable or narrows the material string domain of the
formal claim.

## 1. Input and provenance integrity

Status: PASS.

`/audit-input.json` declares:

- problem `38-decode-cyclic`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`.

The campaign object is byte-for-byte equal as JSON data to
`/audit-campaign-lock.json`, and the lock's SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The mode boundary is consistent: `/reference/reference-semantics` is absent,
the launcher says it was not mounted, and all reference-semantics hash fields
are null.

I required real regular files for `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, the invocation and metrics records, `codex-last`,
`codex-output`, `prompt.txt`, all three trusted reference files, and the
present optional `usage.json`. I required real directories for the candidate,
generation evidence, structured trace, and trusted reference root. The
candidate and trace tree scans reject symlinks and unsupported node types.
Nothing required by the declared layout was missing, linked, mistyped, or
unreadable.

Every recorded per-file hash matched. This includes the run/task/result
manifests; invocation and metrics; usage; prompt; last/output logs; canonical,
prompt, and translator; the single trace JSONL file; and the present legacy
metrics/run-input records. An independent reimplementation of the
pipeline-v2 length-delimited tree digest produced
`f600725fab73470246ba886f9bf3af31bb1d72edca63918399cd60d871f1bc73`
for `/candidate`, matching both producer retained-workspace hashes. The trace
tree digest similarly matched usage's
`e97a39249028dd7077249669b1b3f7e5221b946e264bed267b5c9d05138bb630`.
The launcher also records audit-specific high-level tree digests whose
encoding is not specified in the mounted JSON; all constituent hashes and
producer-native tree hashes independently matched.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. The candidate has all required proof artifacts:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. There are no candidate helper K files.

I parsed all 185 structured trace records. Counts were 126 response items, 56
events, one session metadata record, one turn context, and one world state.
The generation records and their reported `#Top` were treated only as
historical claims. The full bounded call/message summary is
[stage1-generation-trace-summary.log](/audit-output/evidence/logs/stage1-generation-trace-summary.log).
The independent integrity implementation and complete final run are
[verify_provenance.py](/audit-output/evidence/verify_provenance.py) and
[stage1-provenance-final.log](/audit-output/evidence/logs/stage1-provenance-final.log);
the latter exited 0 with `FAILURE_COUNT: 0`.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

The trusted prompt defines `encode_cyclic` as follows: split the input into
consecutive groups of at most three characters; rotate a full three-character
group left once; leave a final group of one or two characters unchanged. The
requested `decode_cyclic` must invert that operation. The trusted canonical
implementation applies `encode_cyclic` twice, so on every full block
`(a,b,c)` it returns `(c,a,b)` and leaves a short tail unchanged.

The candidate implementation does exactly that with a loop. At each index
`i`, while a complete triple remains, it appends `s[i+2] + s[i:i+2]`,
advances by three, and finally appends `s[i:]`. A different algorithm is
permitted, and this one is extensionally the same as the canonical algorithm.
Because the encoder is a blockwise permutation, every string is in its range;
the phrase "encoded with encode_cyclic" does not impose a narrower subset.

Trusted regeneration used:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/rebuild/solution.regenerated.mpy
cmp /tmp/audit-work/rebuild/solution.regenerated.mpy /candidate/solution.mpy
```

It exited 0. Both files have SHA-256
`3d2fa824ef26d25a4275888898b0c5cb30c7d70fe71b6e7df714e0c42199a11f`;
see
[stage2-translation-identity.log](/audit-output/evidence/logs/stage2-translation-identity.log).

The independent differential test imports the trusted canonical entry point,
trusted prompt encoder, and submitted generated entry point by exact path. It
tests the empty input; lengths 1 through 8 around every loop and remainder
boundary; punctuation, quotes, slash, newline, tab, NUL; BMP, combining, CJK,
and astral Unicode; and 4,160 deterministic generated inputs over lengths
0 through 64. The prompt contains no explicit call/result examples to replay.
All 4,173 inputs had zero canonical/generated mismatches and zero inverse
failures. The corpus is fully specified by seed, alphabet, and SHA-256 in
[differential_test.py](/audit-output/evidence/differential_test.py) and
[stage2-differential.log](/audit-output/evidence/logs/stage2-differential.log).

## 3. Clean proof reconstruction

Status: PASS.

I copied source artifacts into `/tmp/audit-work/rebuild` and did not copy or
reuse a candidate K compiled definition or cache. The observed toolchain is K
v7.1.293, matching the campaign lock. The concrete and proof definitions were
built independently:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

Both exited 0; see
[stage3-kompile-concrete.log](/audit-output/evidence/logs/stage3-kompile-concrete.log)
and
[stage3-kompile-proof.log](/audit-output/evidence/logs/stage3-kompile-proof.log).

The candidate-shaped target command was then reconstructed against the fresh
concrete definition:

```text
kprove spec.k --definition concrete-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0. Against the independently compiled proof
definition, the complete spec again printed `#Top` and exited 0:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The loop claim also closes when selected independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-correct
```

The exact records are
[stage3-kprove-candidate-shape.log](/audit-output/evidence/logs/stage3-kprove-candidate-shape.log),
[stage3-kprove-all.log](/audit-output/evidence/logs/stage3-kprove-all.log), and
[stage3-kprove-loop.log](/audit-output/evidence/logs/stage3-kprove-loop.log).

For completeness, I attempted to select only `SPEC.program-correct`.
That filter also removes the `loop-correct` circularity on which the entry
claim depends, so it unrolled rather than representing the submitted complete
target and was manually stopped after 60 seconds. This diagnostic is not a
failed positive target. It is explicitly labeled, with observed exit 130, in
[stage3-kprove-program.log](/audit-output/evidence/logs/stage3-kprove-program.log).

Fresh concrete K execution used the actual regenerated `solution.mpy`. Thirteen
configuration-safe empty, branch-boundary, escaped-control, ordinary, and
longer ASCII cases all terminated with empty `<k>`, empty `<env>`, and exactly
the values returned by both Python implementations; see
[semantics_differential.py](/audit-output/evidence/semantics_differential.py)
and
[stage3-semantics-config-safe.log](/audit-output/evidence/logs/stage3-semantics-config-safe.log).

Direct `krun -cS` serialization of non-ASCII text represents the configuration
variable differently from compiled K string literals; that experiment is
preserved, including its two apparent mismatches, in
[stage3-semantics-nonascii-injection-limitation.log](/audit-output/evidence/logs/stage3-semantics-nonascii-injection-limitation.log).
I isolated that external bridge rather than attributing it to the candidate
semantics. A fresh wrapper imports the unchanged candidate semantics and
injects BMP, combining, CJK, and astral input as compiled K literals.
Its final K string tokens are exactly equal to independently compiled expected
K literals, and both expected text values equal the canonical and submitted
Python results. The commands and zero-failure comparison are in
[unicode-wrapper.k](/audit-output/evidence/unicode-wrapper.k),
[unicode_semantics_compare.py](/audit-output/evidence/unicode_semantics_compare.py),
and
[stage5-unicode-semantic-compare.log](/audit-output/evidence/logs/stage5-unicode-semantic-compare.log).

## 4. Adequacy and real-program pinning

Status: PASS, with a non-fatal intent-bridge concern.

The two entry claims mean:

1. `loop-correct`: from the exact loop head followed by the exact submitted
   return statement, with environment bindings `s=S`, `i=I`, and
   `result=ACC`, no prior result, and `0 <= I <= length(S)`, terminating
   execution empties the computation and environment and returns
   `decodeFrom(S,I,ACC)`.
2. `program-correct`: for every K String `S`, from empty environment and no
   result, terminating `run(solutionProgram,S)` empties computation and
   environment and returns `decodeFrom(S,0,"")`.

Both preconditions are satisfiable. Examples are:

- loop state `S=""`, `I=0`, `ACC=""`, expected `""`;
- loop state `S="bcaefdgh"`, `I=3`, `ACC="abc"`, expected `"abcdefgh"`;
- program state `S="bcaefdgh"`, expected `"abcdefgh"`.

The final example agrees with `decodeFrom`, trusted canonical Python, submitted
Python, and rebuilt K execution. These substitutions are recorded in
[adequacy_witnesses.py](/audit-output/evidence/adequacy_witnesses.py) and
[stage4-adequacy-witnesses.log](/audit-output/evidence/logs/stage4-adequacy-witnesses.log).

The entry claim does not read `solution.mpy` at proof time; it executes the
closed `solutionProgram` constructor term. This is permitted only if that term
is mechanically pinned. After trusted byte-identical regeneration, an
independent lexer compared all 208 constructor tokens. The two hashes are
identical, and `decodeBody`, `decodeTest`, and `decodeReturn` each occur as an
exact unique subterm of `solutionProgram`. See
[check_program_pinning.py](/audit-output/evidence/check_program_pinning.py) and
[stage4-program-pinning.log](/audit-output/evidence/logs/stage4-program-pinning.log).

Body sensitivity also succeeds. In a separate definition I changed only the
executed `solutionProgram` initialization from `result = ""` to
`result = "!"`; the external Python or MPY file was not the mutation target.
The mutated definition compiled, but the complete proof failed with a
`WarnStuckClaimState` residual requiring
`decodeFrom(S,0,"!") = decodeFrom(S,0,"")`. The artifact and logs are
[body-mutation.semantic.k](/audit-output/evidence/body-mutation.semantic.k),
[stage4-body-mutation-diff.log](/audit-output/evidence/logs/stage4-body-mutation-diff.log),
[stage4-body-mutation-kompile.log](/audit-output/evidence/logs/stage4-body-mutation-kompile.log),
and
[stage4-body-mutation-kprove.log](/audit-output/evidence/logs/stage4-body-mutation-kprove.log).

The returned value is not free, existential, tautological, or guarded by a
one-way implication. It is exactly the recursive block-rotation function. The
remaining concern is that the theorem does not separately formalize the
prompt's supplied encoder and prove
`decodeFrom(S,0,"") = encode_cyclic(encode_cyclic(S))`. That bridge is an
ordinary blockwise argument: `(a,b,c)` becomes `(b,c,a)` after one encode,
`(c,a,b)` after two, exactly the recursive `decodeFrom` step; tails shorter
than three are unchanged by both definitions. This is convincing and broadly
tested, but it remains outside the machine-checked reachability theorem.

## 5. Rule-by-rule static soundness review

Status: PASS.

The exhaustive inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md), backed by the
line-numbered immutable sources in
[stage5-numbered-sources.log](/audit-output/evidence/logs/stage5-numbered-sources.log).
It enumerates all 17 local syntax declarations, all 40 ordinary/definitional
rules in `semantic.k`, all three proof-local simplifications in
`verification.k`, the configuration, and both claims. It also records every
`function`/`total` attribute. There are no local `functional` declarations,
opaque symbols, priorities, `owise` rules, or extra helper K files.

All submitted constructor forms are covered:

- module/function/parameters and statement lists;
- assignments, names, string and integer values;
- left-to-right binary and comparison evaluation;
- `len`, valid integer indexing, bounded slices, and tail slices;
- while guard, body, back-edge, exit, return, and final environment/result.

The configuration has only the three state components required by the program.
Evaluation order is explicit through continuation terms. The true/false
comparison and loop rules have complementary guards. Integer/string addition
is disjoint by value sort. Index and two slice forms are disjoint by syntax.
All reachable accesses satisfy the explicit bounds. `decodeFrom`'s two guards
are disjoint and exhaustive under claim preconditions, and recursion advances
`I` by three.

The top-level return rule discards its suffix and clears locals. That rule
would be too broad in a language with callers, `finally`, output, heap, or
exception state, but none of those constructs or cells exists in this minimal
generated language. `doReturn` is introduced only by evaluating a source
`Return`, and its reachable suffix is precisely the remaining function
statement continuation. It is sound for the modeled program.

The three proof-local simplifications are true equations:

- equality of the same map updated at the same key is equivalent to equality
  of the two new values;
- string length is nonnegative;
- the full `[0,length)` substring is the original string.

They neither bypass execution nor introduce an opaque result. `solutionProgram`
and the three control macros are truthful closed definitions. `decodeFrom` is
a specification function; no operational rule rewrites program execution to
it. Thus there is no circular program-derived oracle or task-answer shortcut.

The generated language is intentionally incomplete for unused Python
constructs, which is allowed in this mode. It soundly covers every material
construct of the submitted program. K's imported `INT`, `STRING`, `BOOL`,
`MAP`, and `MAP-SYMBOLIC` operations remain trusted primitives, accounted for
in stage 7. I found no false local equation or operational conclusion and
therefore make no unsupported unsoundness allegation.

## 6. Fresh non-vacuity test

Status: PASS.

The candidate did not supply a vacuity spec. I created
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k), copied the
valid loop circularity, and changed only the entry result obligation to:

```text
pyStr(decodeFrom(S,0,"") +String "!")
```

This is demonstrably false for the satisfying entry input `S=""`: actual result
is `""`, while the mutation requires `"!"`; see
[stage6-vacuity-witness.log](/audit-output/evidence/logs/stage6-vacuity-witness.log).

The mutation built successfully under:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

which exited 0. The real proof command exited 1 with
`WarnStuckClaimState`; its residual requires
`decodeFrom(S,0,"") +String "!" = decodeFrom(S,0,"")`. This is the expected
unmet result obligation, not a parser error, timeout, missing import, or
unreachable mutation. See
[stage6-vacuity-dry-run.log](/audit-output/evidence/logs/stage6-vacuity-dry-run.log)
and
[stage6-vacuity-kprove.log](/audit-output/evidence/logs/stage6-vacuity-kprove.log).

## 7. Proven versus assumed accounting

Status: PASS for soundness and material domain; CONCERN for the two explicit
validation boundaries below.

What the reachability proof establishes:

- Under the rebuilt MPY semantics plus the three audited simplifications, for
  every K String `S`, if the exact submitted function invocation terminates,
  it ends with empty computation and locals and result
  `pyStr(decodeFrom(S,0,""))`.
- More generally, every satisfiable modeled loop state with
  `0 <= I <= length(S)` terminates only with the corresponding
  `decodeFrom(S,I,ACC)` result.
- This is partial correctness. Termination is not part of the theorem required
  by the benchmark.

Trusted or informal boundaries:

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 compiler, Haskell backend, and `kprove` | Parsing, rewriting, symbolic reachability | Standard low-level proof checker trust. Rebuilt from source; no candidate compiled artifacts used. |
| Imported `INT`, `STRING`, `BOOL`, `MAP`, `MAP-SYMBOLIC` hooks | Arithmetic, string concatenation/length/substrings, booleans, environments, symbolic map reasoning | Standard K primitives outside the generated language theorem. Boundary/Unicode concrete probes support the exercised behavior. |
| Trusted `py2mpy.py` | Python AST to constructor identity | Launcher-authenticated input; byte-identical regeneration proves the submitted MPY is its output. Trust in the translator's intended constructor interpretation remains external. |
| Generated MPY operational rules | Actual control, bindings, and values | Exhaustively reviewed in stage 5 and concretely exercised. No operation used by the program is replaced by `decodeFrom`. |
| Standard builtin binding of `len` | Selects Python's built-in `len` rather than a rebound global | Acceptable HumanEval execution assumption; the submitted function never rebinds `len`. |
| `decodeFrom` means the prompt's decoder | Final human-facing correctness intent | Elementary blockwise argument plus 4,173 Python differential/inverse cases and compiled-literal K tests. Not a separate machine-checked encoder-equivalence theorem; this is the main non-fatal concern. |
| Python/K external string injection | Relates host strings to K `String` inputs | ASCII/control `-cS` tests pass. Direct non-ASCII `-cS` serialization is misleading, so Unicode was validated using compiled K literals and normalized K tokens. The formal claim itself remains universal over K Strings, but this bridge limitation is documented rather than hidden. |
| Python annotations, exceptions, globals, function objects, call stacks | Potential broader Python behavior | Typing annotations are operationally irrelevant to this body; all accesses are in bounds; the HumanEval harness supplies an ordinary builtins environment. Unused general-language behavior is outside this minimal semantics. |

Differential testing and concrete traces support only the Python/K intent and
primitive bridges. They are not substitutes for the successful K proof.
Likewise, the candidate's generation report and earlier `#Top` played no role
in accepting the reconstructed theorem.

Gate summary:

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS, with an informal but direct blockwise
  summary-to-prompt bridge.
- Gate C, trust and evidence auditability: PASS, with the documented
  non-ASCII configuration-injection limitation.

These are non-fatal concerns under the benchmark decision boundary: the proof
is sound, pins the real generated program, and covers arbitrary material
string lengths rather than examples or bounded unrollings. There is no
material source-contract narrowing, substituted body, vacuity, or unsound
proof rule.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
