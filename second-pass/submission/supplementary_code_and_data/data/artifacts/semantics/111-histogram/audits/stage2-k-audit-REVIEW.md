# Independent adversarial review: 111-histogram

The candidate does not contain a proof of the full HumanEval contract. It does
contain a reproducible, result-constraining proof of 13 much narrower claims:
five fixed examples and synthetic token lists of lengths one, two, and three.
There is no claim or invariant for an arbitrary-length input. The benchmark
explicitly classifies this material narrowing, even if the smaller theorems are
sound, as `FAIL / NOT_LEGIT`.

No audit-infrastructure breach was found.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The mode and
mounts agree: `/reference/reference-semantics` is present.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required generation records, the
complete 248-line structured trace, and `usage.json`. Historical
`runtime-metrics.json` is absent, which is allowed for this record layout. The
generation records were treated only as untrusted claims. Their material claim
is that the author intentionally bounded the symbolic cases to token-list
lengths at most three.

Independent integrity results:

- The campaign-lock byte hash is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the value in `/audit-input.json`, and its parsed JSON object exactly
  equals the recorded campaign block.
- Every declared regular-file hash checked against its mounted file, including
  the run/task/result/invocation records, prompt, usage, output log, last
  message, metrics, canonical implementation, and translator.
- The independently recomputed pipeline tree hash of `/candidate` is
  `5f637ae13e922306a6730d246d18df5d456cf203c2a1a2df400a8a9311ab5ff8`,
  matching both the stage-1 result and invocation records.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  prompt and translator.
- The candidate and trusted supplied-semantics trees have exactly the same 24 K
  files, entry types, and bytes. Neither tree contains a symlink. Their
  independently recomputed pipeline tree hash is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the recorded semantics-manifest hash.
- The complete structured-trace tree hash matches `usage.json`, and the one
  JSONL file matches both generation manifests. No malformed JSONL event was
  found.
- All required candidate proof artifacts are regular files. No
  candidate-built definition or cache was used.

Evidence:
[integrity script](/audit-output/evidence/stage1_integrity.py),
[integrity log](/audit-output/evidence/stage1-integrity.log), and
[complete trace/record reader](/audit-output/evidence/stage1-generation-records.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a string consisting of space-separated lowercase letters, `histogram`
must return a dictionary containing every letter tied for greatest frequency,
mapped to that frequency. The empty string returns `{}`.

The trusted canonical implementation splits on the literal space, determines
the greatest nonempty-token count, then emits every token at that count. The
candidate uses a two-pass count dictionary and `test.split()`. On the strict
documented domain—single lowercase-letter tokens separated by one ASCII
space—these implementations agree.

Trusted regeneration with
`python3 py2mpy.py solution.py > regenerated-solution.mpy` exited 0.
`cmp` established byte identity with submitted `solution.mpy`; both have
SHA-256
`d324282bd904e34a1ef8f2d5c2f8622dbd9d0bed9ada7e28385e3fb92bc15ed9`.

The independent differential test covered:

- all five documented examples;
- all token sequences of lengths 0 through 7 over `{a,b,c}`;
- 500 deterministic generated sequences of lengths 0 through 64 over
  `{a,b,c,d,e,f}`; and
- explicit empty, first-insertion, repeated-key, strict-maximum, overtaking,
  and tie boundaries.

There were 3,794 comparisons and zero mismatches on that domain.

The test separately records divergences for leading, trailing, repeated,
tab, and newline whitespace. For example, the canonical implementation returns
`{'a': 1, '': 1, 'b': 1}` for `"a  b"`, while the candidate returns
`{'a': 1, 'b': 1}`. I do not count those strings as part of the strict
“space-separated lowercase letters” domain, but the divergence is retained as
an interpretation limitation rather than hidden.

Evidence:
[differential script](/audit-output/evidence/differential_test.py) and
[translation/differential log](/audit-output/evidence/stage2-program-fidelity.log).

## 3. Clean proof reconstruction

I copied only candidate source artifacts, the trusted translator, and the
trusted supplied semantics into `/tmp/audit-work/111-histogram`. I did not copy
or use any candidate definition cache.

The observed tools were K 7.1.293. Fresh reconstruction did all of the
following:

1. Built an LLVM definition from trusted
   `reference-semantics/semantics.k` with main module `MPY-KRUN`.
2. Translated and ran an independent seven-assertion concrete K harness. An AST
   comparison first established that its `histogram` function is exactly the
   submitted Python function. The final K configuration had `.K`, `NoExc`, an
   empty stack, `noRet`, and exit code 0.
3. Built a fresh Haskell definition from candidate `verification.k` with main
   module `VERIFICATION`.
4. Ran the original complete `HISTOGRAM-SPEC`; it exited 0 and printed `#Top`.
5. Added only inert labels to a scratch copy of the 13 claims and ran each
   claim separately. Every one of the 13 commands exited 0 and printed
   `#Top`.

Thus the candidate's positive proof-execution claim is reproducible. That
fact does not establish adequacy of the theorem.

The build emitted fixed-semantics warnings about nonexhaustive total functions
such as unused float, map, join, and indexing helpers. None is exercised on an
uncovered case by this program. They are recorded as fixed-semantics trust
limitations, not silently converted into candidate defects.

Evidence:
[reconstruction commands](/audit-output/evidence/stage3_reconstruct.sh),
[complete reconstruction log](/audit-output/evidence/stage3-reconstruction.log),
and [concrete harness](/audit-output/evidence/k_concrete_audit.py).

## 4. Adequacy and real-program pinning

### Common entry and destination state

Every claim starts from the standard module configuration:
environment 0; module scope 0 with builtins parent `-1`; empty heap and stack;
`scopeLoc = 1`; `heapLoc = 0`; `noRet`; `NoExc`; and exit code 0. The `<k>`
cell loads a module containing the submitted function followed by an assertion
that calls `histogram(INPUT)` and compares the result with `EXPECTED`.

Every destination consumes the complete computation to `.K`, restores
environment 0 and `scopeLoc = 1`, leaves stack empty and `noRet`, preserves
`NoExc` and exit code 0, and existentially permits the resulting scope, heap,
and heap location. Because the fixed assertion rule changes false assertions
to `AssertionError` and exit code 1, this is a genuine result constraint.

### Claim-by-claim meaning

| Claim | Formal input precondition | Required result |
|---|---|---|
| 01 | fixed `""` | `{}` |
| 02 | fixed `"a b c"` | `{"a":1,"b":1,"c":1}` |
| 03 | fixed `"a b b a"` | `{"a":2,"b":2}` |
| 04 | fixed `"a b c a b"` | `{"a":2,"b":2}` |
| 05 | fixed `"b b b b a"` | `{"b":4}` |
| 06 | synthetic `tokenText([A])`, arbitrary `A:IntSeq` | `{A:1}` |
| 07 | synthetic `tokenText([A,A])` | `{A:2}` |
| 08 | synthetic `tokenText([A,B])`, `A != B` | `{A:1,B:1}` |
| 09 | synthetic `tokenText([A,A,A])` | `{A:3}` |
| 10 | synthetic `tokenText([A,A,B])`, `A != B` | `{A:2}` |
| 11 | synthetic `tokenText([A,B,A])`, `A != B` | `{A:2}` |
| 12 | synthetic `tokenText([A,B,B])`, `A != B` | `{B:2}` |
| 13 | synthetic `tokenText([A,B,C])`, pairwise distinct | `{A:1,B:1,C:1}` |

Each precondition is satisfiable. For claims 06–13, the substitutions
`A = "a"`, `B = "b"`, and `C = "c"` satisfy the relevant disequalities. Under
the informal “join tokens with one space” interpretation, both Python
implementations return every displayed expected dictionary. This is finite
ground evidence, not a K theorem connecting `tokenText` to actual strings.

### Mechanical program pinning

I parsed submitted `solution.mpy` and a `histogramCheck` term through the fresh
definition with macro expansion. After separating the wrapper's one trailing
assertion, both function-binding/body constructor trees had SHA-256
`cc50ab2ddc9c62a861e30ac4df79d22dd05908277f0fd4374cb4d0b1bd0117ad`
and compared equal. The claim therefore executes the submitted function body;
it is not a substituted summary.

A body-sensitivity mutation changed the increment in the function term from
`+ 1` to `+ 2`. Macro expansion changed the executed function-constructor hash
to
`0d148e67f22b80ff61859bebed9a3cde55d7bf674aed71d5fafb0cd5fd3eb2f8`.
Claim 03 then failed with a reachable `.K` state containing
`AssertionError`, exit code 1, and the mutated `Int(2)` body. This is a real
body mutation, not a source-file-only mutation.

Evidence:
[constructor comparison](/audit-output/evidence/constructor_compare.py),
[ground witnesses](/audit-output/evidence/claim_witnesses.py), and
[pinning/body-sensitivity log](/audit-output/evidence/stage4-pinning-body-sensitivity.log).
The exact
[body-mutated verification module](/audit-output/evidence/verification-body-mutation.k)
and [retargeted claim module](/audit-output/evidence/spec-body-mutation.k) are
also preserved.

### Fatal adequacy gap

The contract has no length bound. The symbolic claims cover exactly all
equality partitions for lengths one through three; the longer claims are only
four fixed examples. There is no arbitrary `ValSeq`, recursive summary, loop
invariant, or circularity. Inputs of length four and greater, apart from those
few literals, are outside the theorem.

Finite examples, fixed sizes, and bounded unrolling do not prove an
unrestricted HumanEval domain. This is a material narrowing and is independently
fatal under the benchmark decision rule.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The machine-generated inventory covers all 25 K sources in the proof
definition: the 24 trusted supplied-semantics files and candidate
`verification.k`. It contains 932 entries:

- 229 syntax declarations;
- 697 rules;
- 5 contexts; and
- 1 configuration.

The attributes include 146 function declarations, 107 total declarations, 45
priority rules, 35 concrete rules, 26 `owise` rules, 22 opaque
`no-evaluators` declarations, 25 `symbol` declarations, 5 macros, and 1
recursive macro. There are no simplification rules and no `functional`
declarations. The complete body, source file, line, kind, and attributes of
every entry are preserved in
[the exhaustive inventory](/audit-output/evidence/stage5-rule-inventory.txt).

Of these entries, 928 belong to the byte-verified trusted supplied semantics.
I reviewed the whole inventory, then traced the reachable subset in detail.
The generated program uses:

- `Module`, statement sequencing, `Name`, literals, allocation, scope lookup,
  and argument evaluation from `syntax.k` and `core.k`;
- real function definition, call-frame, parameter, return, and pop rules from
  `functions.k` and `call.k`;
- `split()` and fixed `splitWS` for concrete strings from `methods.k`;
- assignment, `If`, `For`, loop steps, and target binding from `controls.k`,
  `iter.k`, and `tuple.k`;
- list allocation, iteration, and membership from `list.k`;
- ordered dictionary construction, insertion/update, keys, read, and equality
  from `dict.k`;
- subscript dispatch and integer/string comparison/arithmetic from
  `subscript.k`, `operators.k`, `int.k`, and `str.k`; and
- the result-observing assertion rules from `assert.k`.

These rules execute all material operations and track scopes, heap allocation,
call stack, return state, exceptions, and exit code. Their guards and
priorities preserve the relevant left-to-right evaluation, reference
dereferencing, method dispatch, call/return control, dictionary insertion
order, and assertion failure. I found no false-conclusion witness for a
reachable fixed rule on the intended lowercase-ASCII domain, so I do not label
one unsound.

The compiler's totality warnings concern fixed rules outside this execution
path. The 22 opaque fixed primitives are float, MD5, and sorting operations;
none occurs in `solution.mpy`, the macro, or a claim result. They cannot affect
this proof.

### Candidate-local declarations and rules

Candidate `verification.k` contributes exactly four entries:

1. `tokenText(ValSeq) [constructor]` extends `IntSeq` with a fresh synthetic
   value. It has no fixed-semantics or CPython constructor counterpart.
2. `splitWS(tokenText(TS), .IntSeq, .ValSeq) => TS` is a result-bearing
   operational bridge. It is unguarded, reads/writes no cells, preserves its
   surrounding continuation, terminates in one step, and is constructor-
   disjoint from the fixed `.IntSeq` and `iCons` split equations. Its value
   controls both loops, branches, and the returned dictionary in claims
   06–13.
3. `histogramCheck(Expr, Expr) [macro]` declares the wrapper syntax.
4. Its macro rule expands to the exact submitted function plus one trailing
   assertion. Constructor comparison and body sensitivity justify this
   definitional expansion.

No bridge-free universal connection theorem establishes that fixed string
execution produces the `TS` supplied to `tokenText`. The same `TS` is inserted
by the split rule and used to construct the expected postcondition, which is
circular evidence for the intended meaning.

Removing only the `splitWS(tokenText(...))` rule left concrete claim 02 at
`#Top`, but made symbolic claim 06 fail at the residual
`splitWS(tokenText(vCons(str(A), .ValSeq)), .IntSeq, .ValSeq)`. This proves
claims 06–13 depend on the bridge rather than fixed string semantics. The
first isolation attempt failed to remove the rule because of a reviewer
pattern-escaping error; that invalid attempt is preserved, and the corrected
diff and run are the evidence used here.

As an equation over a brand-new constructor, the rule is nonoverlapping and
does not by itself make the fixed concrete-string theory inconsistent.
However, it is not a legitimate universal bridge to whitespace-split source
strings. Its complete unguarded domain includes, for example:

- `TS = [str("")]`, which would imply one empty token and `{"":1}`, whereas
  actual `histogram("")` returns `{}`; and
- `TS = [str("a b")]`, which would imply one embedded-space token and
  `{"a b":1}`, whereas actual `histogram("a b")` returns
  `{"a":1,"b":1}`.

Those are concrete false-behavior witnesses for interpreting the fresh
constructor as the claimed general source-string abstraction. Because there
is no alternative formal representation theorem, the narrower correct
description is: the symbolic claims are theorems about synthetic values, not
about arbitrary real input strings.

Evidence:
[bridge-dependency log](/audit-output/evidence/stage5-bridge-dependency.log),
[preserved invalid first probe](/audit-output/evidence/stage5-bridge-dependency-attempt1.log),
[bridge-free verification variant](/audit-output/evidence/verification-no-bridge.k),
and [false-bridge witnesses](/audit-output/evidence/stage5-token-text-witness.log).

## 6. Fresh non-vacuity test

I created a fresh claim using the satisfiable standard initial state and the
real input `""`, but changed the result obligation from `{}` to the false
`{"a":1}`.

`kprove --dry-run` exited 0, so the mutation parsed and built successfully.
The actual proof exited 1 with `WarnStuckClaimState`. Its terminal residual had
`.K`, `AssertionError`, and exit code 1, exactly the unmet result obligation;
there was no parser error, missing import, timeout, or unrelated crash.

This confirms that the original claims discriminate their stated results. It
does not enlarge their domain.

Evidence:
[fresh mutation](/audit-output/evidence/spec-vacuity.k),
[mutation commands](/audit-output/evidence/stage6_nonvacuity.sh), and
[mutation log](/audit-output/evidence/stage6-nonvacuity.log).

## 7. Proven-versus-assumed accounting

### What is machine proved

Conditional on K 7.1.293 and the assembled proof definition, the exact
submitted function body executes and satisfies:

- the five fixed example results; and
- the eight synthetic `tokenText` results for all token-value equality
  patterns at list lengths one, two, and three.

The postconditions constrain results through real assertions, the entry states
are satisfiable, the claims are non-vacuous, and the immutable function body is
mechanically pinned.

### Trust and evidence ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K toolchain and K built-in Int/Bool/String/Map/List equality/arithmetic | all claims | ordinary machine-checking trust |
| Byte-verified supplied MPY semantics | all claims | required fixed semantics; used rules were traced and concretely exercised |
| ASCII `strToCodes` model | fixed string claims | acceptable for documented lowercase-letter inputs |
| Proof-local `tokenText` and split equation | claims 06–13 | illegitimate as a real-string connection: result-bearing, circular, and lacks a universal theorem |
| Macro-to-source constructor comparison | all claims | mechanically checked, not merely asserted |
| CPython canonical/candidate differential testing | implementation-intent bridge only | 3,794 finite cases; supportive evidence, never a universal proof |
| Informal join-with-one-space interpretation of synthetic witnesses | claims 06–13 | finite illustration only; not formal and false over the bridge's unguarded full domain |
| Fixed opaque float/MD5/sort primitives | none | inert for this program and theorem |

### Gate and verdict reasoning

- Positive reconstruction: **pass**. The stated claims genuinely close.
- Program pinning and result non-vacuity: **pass** for the stated claims.
- Proof-local abstraction validation: **fail** as a bridge from synthetic
  `tokenText` values to real strings.
- Intent/domain adequacy: **fail**. No theorem covers arbitrary-length
  space-separated inputs.
- Reproducible evidence: **pass**, with finite-test limitations stated.

Even under the most charitable classification—treating `tokenText` as a
consistent abstract constructor and the smaller claims as sound—the result is
only sound-but-materially-limited. The benchmark prompt explicitly maps that
kind of HumanEval domain narrowing to `FAIL / NOT_LEGIT`, not to concerns.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
