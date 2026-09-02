# Independent adversarial audit: 78-hex-key

Audit date: 2026-07-23  
Generation condition: `bare`  
Rendered semantics mode: `GENERATED_SEMANTICS`  
Toolchain: K v7.1.293

The candidate contains a legitimate partial-correctness proof of the submitted
generated program. I rebuilt the semantics and proof definitions only from
source, independently reproduced `#Top`, checked that the claim embeds the
trusted-translator output, audited every local rule, and obtained the expected
stuck obligations from both a body mutation and a false postcondition.

## 1. Input and provenance integrity

### Trusted-mount boundary

The rendered mode and trusted mounts agree:

- `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py` are present as regular files.
- `/reference/reference-semantics` does not exist, as required in
  `GENERATED_SEMANTICS` mode.
- No symlink occurs anywhere under `/candidate`.

The complete type-aware mount and candidate manifest is recorded in
[stage1-mount-and-manifest.log](/audit-output/evidence/stage1-mount-and-manifest.log).
There is no infrastructure breach.

### Required candidate artifacts

The candidate has the required source and run artifacts:

- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`
- `prove.sh`
- `prompt.py`, `py2mpy.py`
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`
- one structured JSONL generation trace

There are no missing, mistyped, or symlinked required artifacts. The candidate
also contains `semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`,
and their generated cache files. Those are extra untrusted build products, not
source-integrity failures; none was copied into or used by the clean builds.

The candidate prompt and translator are byte-identical to the trusted files:

| Artifact | SHA-256 | `cmp` |
|---|---|---|
| prompt | `0f302c2314267fba8ddb3d9fa69d4dbb49dee3249d64a84f1048661f1ad2ae6e` | exit 0 |
| translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exit 0 |

See [stage1-integrity-and-claims.log](/audit-output/evidence/stage1-integrity-and-claims.log).

### Untrusted generation claims

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and all 104 JSON records in the structured trace solely as
claims. They report a successful generation run and `KPROVE_PASSED`; that
status was not relied on. A bounded content extract is in
[stage1-integrity-and-claims.log](/audit-output/evidence/stage1-integrity-and-claims.log),
and full-file/structured-record counts are in
[stage1-untrusted-log-structured-summary.log](/audit-output/evidence/stage1-untrusted-log-structured-summary.log).

Stage result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For an empty string or a valid uppercase hexadecimal string, `hex_key(num)`
must return the number of characters whose hexadecimal digit value is prime.
The prompt explicitly identifies the counted characters as
`2`, `3`, `5`, `7`, `B`, and `D`.

The trusted canonical implementation loops over every input character,
increments once when the character belongs to that six-element tuple, and
returns the total. The source is captured with line numbers in
[stage2-source-inspection.log](/audit-output/evidence/stage2-source-inspection.log).

### Submitted implementation

The submitted `solution.py` returns the sum of six one-character
`str.count` calls, one for each member of `2357BD`. Because those needles are
distinct one-character strings, this is extensionally the same algorithm on
the intended domain. It handles the empty string and repeated characters.

I regenerated the constructor program with the trusted translator copied to
scratch:

```text
python3 /tmp/audit-work/78-hex-key/reference/py2mpy.py \
  /tmp/audit-work/78-hex-key/candidate-src/solution.py \
  > /tmp/audit-work/78-hex-key/regenerated-solution.mpy
```

The submitted and regenerated `solution.mpy` files both have SHA-256
`19e936a519a63db4e4fcc3f41ac8aae3fabb6415c2fd65cef5025e2d87e724b6`;
`cmp` exited 0. Exact command and status:
[stage2-trusted-retranslation.log](/audit-output/evidence/stage2-trusted-retranslation.log).

### Independent differential test

[differential_hex_key.py](/audit-output/evidence/differential_hex_key.py)
loads the trusted canonical and scratch-copy candidate through separate module
objects. It tests:

- the empty string and all five documented examples;
- every one-character uppercase hexadecimal input, exercising both outcomes
  of the canonical membership branch;
- every uppercase hexadecimal string of lengths 0 through 4;
- 300 deterministic generated strings of lengths 5 through 256, seed 780078.

There were 70,208 unique inputs, zero implementation mismatches, and zero
documented-example oracle failures. The command exited 0:
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).
Every input and both results are preserved in
[differential-inputs-and-results.jsonl](/audit-output/evidence/differential-inputs-and-results.jsonl).
This is strong finite evidence, not a universal proof.

Stage result: **PASS**.

## 3. Clean proof reconstruction

I copied only candidate source artifacts to
`/tmp/audit-work/78-hex-key/candidate-src` and the three trusted Python files
to `/tmp/audit-work/78-hex-key/reference`. Candidate-supplied compiled
definitions and caches were not copied or referenced. Source hashes and the
scratch layout are recorded in
[stage3-scratch-isolation.log](/audit-output/evidence/stage3-scratch-isolation.log).

The available tools are `/usr/bin/kompile`, `/usr/bin/krun`, and
`/usr/bin/kprove`, all K v7.1.293; see
[toolchain-version.log](/audit-output/evidence/toolchain-version.log).

### Fresh generated-semantics build

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/78-hex-key/clean-semantic-kompiled
```

Exit status: 0. Log:
[stage3-build-semantic.log](/audit-output/evidence/stage3-build-semantic.log).

I then ran the fresh definition on 25 boundary and normal inputs: empty,
every single hexadecimal digit, all documented examples, all-nonprime
repetitions, and all-prime repetitions. Every `krun` exited 0 and its
`intVal` matched both independent Python implementations. The full commands,
configurations, statuses, and summary (`mismatch_count=0`) are in
[stage3-concrete-semantics-vs-python.log](/audit-output/evidence/stage3-concrete-semantics-vs-python.log);
machine-readable results are in
[semantic-concrete-results.jsonl](/audit-output/evidence/semantic-concrete-results.jsonl).

### Fresh proof build and positive target

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/78-hex-key/clean-verification-kompiled
```

Exit status: 0. Log:
[stage3-build-verification.log](/audit-output/evidence/stage3-build-verification.log).

There is one positive target claim:

```text
kprove spec.k \
  --definition /tmp/audit-work/78-hex-key/clean-verification-kompiled \
  --spec-module HEX-KEY-SPEC
```

It exited 0 and printed exactly `#Top`. Log:
[stage3-positive-claim.log](/audit-output/evidence/stage3-positive-claim.log).

Stage result: **PASS**.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no `requires` side condition. Its effective precondition is the
exact start configuration:

- `S` is any K `String`, which is stronger than the intended valid-uppercase-
  hexadecimal-or-empty domain;
- `<k>` contains the complete submitted `Module(FuncDef(...))` term followed
  by `#invoke("hex_key", S)`;
- `<env>` is `.Map`;
- `<result>` is `noResult`.

Its postcondition requires:

- `<k>` is fully consumed to `.K`;
- `<env>` contains `"num" |-> strVal(S)`;
- `<result>` is exactly `intVal(primeHexCount(S))`.

`primeHexCount(S)` is not existential or free. Its sole equation expands it to
the sum of `countAllOccurrences(S, digit)` for the six exact digits
`2`, `3`, `5`, `7`, `B`, and `D`. The claim is an equality-bearing
reachability target, not a tautology or a one-way implication that leaves the
result unconstrained.

### Program identity and control-flow alignment

[check_program_pinning.py](/audit-output/evidence/check_program_pinning.py)
extracts the `Module(...)` term from the entry claim and compares it, modulo
whitespace only, with the trusted-translator output. Both compact forms have
length 379 and are equal. It also confirms the `hex_key` invocation and the
absence of a claim side condition. See
[stage4-program-pinning.log](/audit-output/evidence/stage4-program-pinning.log).

The source has no helper function, branch, or loop. Accordingly, there are no
helper or loop claims to align. The only claim executes the actual
straight-line translated body.

### Satisfiable precondition and ground substitution

One satisfying state uses the exact submitted module, empty environment,
`noResult`, and `S = "ABED1A33"`. Substituting that input gives
`primeHexCount(S) = 4`; the trusted canonical returns 4, the submitted Python
returns 4, and fresh K execution returns `intVal(4)`.
[stage4-concrete-satisfying-witness.log](/audit-output/evidence/stage4-concrete-satisfying-witness.log)
records the postcondition and both Python values; the K result is in
[stage3-concrete-semantics-vs-python.log](/audit-output/evidence/stage3-concrete-semantics-vs-python.log).
The empty-string state is a second satisfying boundary witness and yields 0.

Stage result: **PASS**.

## 5. Rule-by-rule static soundness review

There are no candidate helper K files beyond `semantic.k`,
`verification.k`, and `spec.k`. The raw declaration inventory is in
[stage5-local-rule-inventory.log](/audit-output/evidence/stage5-local-rule-inventory.log).
The reviewer-authored mutation specs are excluded from the candidate
inventory.

### Local syntax, attributes, and configuration inventory

| Location | Declaration or productions | Audit |
|---|---|---|
| `semantic.k:7` | `Program ::= Module(FunctionDef)` | Exact outer constructor used by `solution.mpy`. |
| `semantic.k:8` | `FunctionDef ::= FuncDef(String, Params, Stmt)` | Carries the submitted function name, parameters, and body without desugaring. |
| `semantic.k:9` | `Params ::= Params(String)` | Exact one-parameter form used by the program. |
| `semantic.k:11` | `Stmt ::= Return(Expr)` | Exact sole statement form used. |
| `semantic.k:13-17` | `Expr ::= Name(String) \| Str(String) \| BinOp(String, Expr, Expr) \| Attribute(Expr, String) \| Call(Expr, Expr)` | Covers every and only expression constructor needed here. String-valued operator/attribute tags outside the modeled tags remain stuck rather than receiving fabricated behavior. |
| `semantic.k:26-28` | `Val ::= strVal(String) \| intVal(Int) \| countMethod(String)` | Separates source strings, integers, and a bound count method. |
| `semantic.k:29` | `Result ::= noResult \| Val` | Explicit before/after result state. |
| `semantic.k:30` | `KItem ::= #invoke(String, String)` | Invocation carries function name and already supplied string argument. |
| `semantic.k:34` | `Val ::= eval(Expr, Map) [function]` | Partial evaluator; intentionally not declared total. |
| `semantic.k:35` | `String ::= asString(Val) [function]` | Partial type projection; intentionally not total. |
| `semantic.k:36` | `String ::= countReceiver(Val) [function]` | Partial bound-receiver projection; intentionally not total. |
| `semantic.k:37` | `Int ::= asInt(Val) [function]` | Partial type projection; intentionally not total. |
| `verification.k:9` | `Int ::= primeHexCount(String) [function, total]` | One unguarded equation covers every `String`; no overlap or missing case. |
| `semantic.k:53-58` | `<hexKey><k> PGM ~> #invoke("hex_key", INPUT) </k><env>.Map</env><result>noResult</result></hexKey>` | Exactly the state components needed by this program. No heap, I/O, exception, or allocation cell is silently modified. |

There are no local `[functional]`, opaque, priority, `[simplification]`,
`[concrete]`, `[owise]`, or trusted declarations. There are no local guards
or overlapping equations.

### Every ordinary local rule

| Rule | Complete domain used by this program | Soundness decision |
|---|---|---|
| `eval(Name(X), X |-> V) => V` | A name looked up in the exact singleton local map | Sound. The invocation rule creates exactly that singleton map and the only used name is the parameter. Unsupported maps remain unmodeled. |
| `eval(Str(S), _) => strVal(S)` | A translated string literal in any local map | Sound and state-independent. |
| `eval(Attribute(E, "count"), ENV) => countMethod(asString(eval(E, ENV)))` | Attribute lookup for `count` on the string-valued parameter | Sound for the used receiver and binding. Other attributes have no rule and cannot be silently fabricated. |
| `eval(Call(F, A), ENV) => intVal(countAllOccurrences(countReceiver(eval(F, ENV)), asString(eval(A, ENV))))` | The one-argument calls whose function reduces to `countMethod` and argument to `strVal` | Sound for all six actual calls. Bad receiver or argument kinds become stuck at a partial projection. |
| `eval(BinOp("+", L, R), ENV) => intVal(asInt(eval(L, ENV)) +Int asInt(eval(R, ENV)))` | The five integer additions in the translated body | Sound. Every operand is a pure integer-valued count. |
| `asString(strVal(S)) => S` | String values only | Truthful projection; non-string values remain stuck. |
| `countReceiver(countMethod(S)) => S` | Bound count methods only | Truthful projection. |
| `asInt(intVal(I)) => I` | Integer values only | Truthful projection. |
| load/invoke rule at `semantic.k:62-64` | Exact `<k>` content `Module(FuncDef(F, Params(P), BODY)) ~> #invoke(F, ARG)`, with empty environment | Sound binding and control transition. The same `F` on both sides prevents invoking a different definition. It changes only `.Map` to the one parameter binding and replaces the exact computation with the real body. |
| return rule at `semantic.k:66-68` | Exact `<k>` content `Return(E)`, current environment `ENV`, and `noResult` | Sound for the actual return. It consumes the exact continuation, preserves the environment, and sets the result to evaluation of the real expression. It cannot discard an arbitrary suffix because the `<k>` pattern has no ellipsis. |
| `primeHexCount(S)` equation at `verification.k:10-16` | Every K `String` | Sound definitional summary. It does not rewrite or bypass program execution; it only names the desired sum in the postcondition. The six literals are distinct and exactly match the trusted prompt. |

### Used-syntax coverage

Every translated constructor is pinned to a declaration and behavior:

| `solution.mpy` construct | Declaration | Behavior |
|---|---|---|
| one `Module` | `Program` | exact load/invoke rule |
| one `FuncDef` and one `Params` | `FunctionDef`, `Params` | same-name invocation and singleton binding |
| one `Return` | `Stmt` | exact return rule |
| five `BinOp("+",...)` | `Expr` | integer-addition evaluator |
| six `Call` | `Expr` | bound string-count evaluator |
| six `Attribute(...,"count")` | `Expr` | count-method binding |
| six `Name("num")` | `Expr` | singleton-map lookup |
| six `Str` literals | `Expr` | string-value rule |

No used construct depends on a catch-all, oracle, task-specific semantic
shortcut, or missing rule.

### Evaluation, state, and imported primitives

The evaluator is a pure K function rather than a small-step Python evaluator.
That representation is adequate here because every source subexpression is
pure on the intended string input: there are no user callbacks, mutations,
exceptions, allocations, or observable sequencing effects. All operands are
evaluated through their actual translated subtrees. The generated semantics
does retain the local environment after return, unlike CPython frame disposal,
but that internal cell is not an observable required by the task and does not
affect the result.

`countAllOccurrences` is an imported K `STRING` hook, not a candidate-defined
oracle. K documents it as `[function, total,
hook(STRING.countAllOccurrences)]`; its reference equations count an occurrence
and recurse after advancing by the needle length. See
[stage5-k-string-primitive.log](/audit-output/evidence/stage5-k-string-primitive.log).
For the six nonempty one-character needles, this is exactly Python
`str.count` and character multiplicity. `+Int` supplies mathematical integer
addition, compatible with Python's unbounded integers for these nonnegative
counts. Built-in `String`, `Map`, cell, and sequencing behavior is used in its
standard role.

There is no unsound local rule, so no false-conclusion witness is applicable.
The narrower evidence limitation is that K built-in hooks and their Python
correspondence are part of the low-level trust/model boundary rather than
theorems proved in this candidate. That boundary is acceptable for the
ASCII-only intended domain and is additionally supported by the concrete and
differential evidence.

### Independent body sensitivity

I changed only the real body's final `count("D")` to `count("E")` while
retaining the original postcondition. The mutation is preserved as
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k).
It built successfully with `--dry-run` (exit 0):
[stage5-body-mutation-build.log](/audit-output/evidence/stage5-body-mutation-build.log).
Proof then exited 1 with `WarnStuckClaimState` at the expected equality between
the `D`-count and `E`-count sums:
[stage5-body-mutation-proof.log](/audit-output/evidence/stage5-body-mutation-proof.log).
The satisfying witness `S = "D"` gives mutated body result 0 and original
postcondition 1:
[stage5-body-mutation-witness.log](/audit-output/evidence/stage5-body-mutation-witness.log).

Stage result: **PASS**.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I authored a fresh mutation,
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k), which preserves the
exact submitted body but changes the result obligation from
`primeHexCount(S)` to `primeHexCount(S) +Int 1`.

The mutation built successfully:

```text
kprove spec-vacuity.k \
  --definition /tmp/audit-work/78-hex-key/clean-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run --output none
```

Exit status: 0. Log:
[stage6-vacuity-mutation-build.log](/audit-output/evidence/stage6-vacuity-mutation-build.log).

The actual proof command:

```text
kprove spec-vacuity.k \
  --definition /tmp/audit-work/78-hex-key/clean-verification-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. Its residual is precisely the unmet
`sum +Int 1 #Equals sum` implication, not a parse failure, missing import,
timeout, or unrelated crash. See
[stage6-vacuity-mutation-proof.log](/audit-output/evidence/stage6-vacuity-mutation-proof.log).
The satisfying input `S = ""` makes the real/original result 0 and mutated
required result 1:
[stage6-vacuity-mutation-witness.log](/audit-output/evidence/stage6-vacuity-mutation-witness.log).

Stage result: **PASS**.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's generated semantics and imported K domains, for every K
string `S`, starting from the exact translated submitted program followed by
`#invoke("hex_key", S)`, empty environment, and `noResult`, any modeled
terminating execution reaches `.K`, binds `num` to `S`, and returns:

```text
intVal(
  countAllOccurrences(S, "2")
  + countAllOccurrences(S, "3")
  + countAllOccurrences(S, "5")
  + countAllOccurrences(S, "7")
  + countAllOccurrences(S, "B")
  + countAllOccurrences(S, "D")
)
```

This is a partial-correctness theorem. It is not a proof about invalid Python
argument types, exceptions, side effects, resource usage, or a full Python
semantics.

### Trust ledger

| Boundary | Effect and dependents | Assessment and evidence |
|---|---|---|
| Trusted `py2mpy.py` | Connects `solution.py` to the `Module(...)` term used by the claim | Accepted trusted input. Fresh translation is byte-identical, and the claim's embedded term matches it exactly. |
| K parser/compiler/Haskell backend/prover | Supplies parsing, rewrite execution, symbolic reasoning, and `#Top` | Standard unavoidable toolchain trust boundary. Fresh builds and independent negative residuals show the intended artifacts and obligations were exercised. |
| K `STRING.countAllOccurrences` hook and String primitives | Determines every one-character count in execution and postcondition | Acceptable fixed external primitive, explicitly documented and not program-defined. Static reference equations, 25 K/Python concrete comparisons, and 70,208 Python differential cases support the bridge. |
| K `+Int`, `Map`, `~>`, and cell machinery | Integer sums, binding storage, computation order, and state rewrites | Acceptable core semantic primitives. Integer behavior matches Python on this nonnegative, unbounded task domain. |
| Generated `semantic.k` as a model of the used Python fragment | Connects constructor execution to parameter binding, `str.count`, addition, and return | Not assumed wholesale: all local syntax and rules are audited above. It is deliberately partial outside the exact used fragment and stops rather than fabricating unused behavior. |
| `primeHexCount` to natural-language intent | Identifies the required result with occurrences of `2357BD` | Directly justified by the trusted prompt's explicit digit list and distinct one-character needles. This is ordinary mathematical interpretation, not a proof shortcut. |
| Trusted canonical Python and CPython execution | Empirical source-fidelity oracle | Finite supporting evidence only. It does not substitute for `kprove` or universally prove the semantics bridge. |

There are no candidate-local opaque symbols, trusted claims, circular result
oracles, operational proof bridges, loop summaries, or unproved helper claims.

### Validation gates and decision

- Gate A, real-program soundness: **PASS**. The actual translated body executes,
  the result is fixed, every local rule is sound on its use, body sensitivity
  is demonstrated, and the false result is rejected.
- Gate B, intent adequacy: **PASS**. The formal theorem covers the complete
  intended domain and its six counted characters are exactly those named by
  the trusted prompt.
- Gate C, trust and auditability: **PASS**. Assumptions are explicit and all
  dynamic, differential, build, positive-proof, and negative-proof evidence is
  reproducible under `/audit-output/evidence`.

The low-level K/CPython model bridge is necessarily outside the reachability
claim, but it is narrow, directly inspectable for this straight-line program,
and not a material adequacy gap. The appropriate completed-audit decision is
`PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
