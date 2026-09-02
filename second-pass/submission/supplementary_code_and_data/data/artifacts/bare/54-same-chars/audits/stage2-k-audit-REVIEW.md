# Independent adversarial review: 54-same-chars

The candidate contains a legitimate partial-correctness proof of its submitted
program under a small generated semantics. The submitted Python body is the
canonical body, trusted regeneration pins the exact `.mpy` constructor tree,
fresh concrete execution agrees with both Python implementations, and every
positive claim closes from a clean Haskell definition. The generated semantics
is narrow, but it covers every construct used by this program for the full
string domain; it has no fixed-size bound or example-only restriction.

All candidate reports, old `#Top` output, and generation traces were treated as
untrusted. The findings below come from fresh inspection and execution.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `54-same-chars`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference semantics.

The required launcher records are present as real regular files:
`/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, and the required invocation, metrics, prompt, usage,
last-message, raw-output, and structured-trace records below
`/generation-evidence`. Candidate, reference, generation, and trace roots are
real directories. Recursive inspection found no symlink or unsupported entry.
The absence of `runtime-metrics.json` is allowed by the declared historical
layout. `/reference/reference-semantics` is absent, as
`GENERATED_SEMANTICS` requires.

The campaign lock is structurally identical to the `audit_campaign` block in
`/audit-input.json`. Its independently computed file hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `audit_campaign_lock_sha256`. The mounted audit prompt hashes to
`999526823ad89bcd9b6e77db8f5f1189f629c86c9ecb308094b84c7161c04e5a`,
also matching the campaign record.

Every launcher-recorded regular-file hash checked by
[check_provenance.py](/audit-output/evidence/check_provenance.py) matches,
including the run/task/result/invocation records, canonical, prompt,
translator, generation prompt, metrics, usage, raw output, final output, and
every evidence file named by `generation-result.json`. The candidate prompt
and translator are byte-identical to their trusted mounts. The independently
reimplemented pipeline content-tree digest of `/candidate` is
`018fcb10add2ae00dbb0e2bc6762d07b27d108db105c8665e706ea8305289a23`,
which matches both the invocation and result workspace digests. The
audit-input-only aggregate tree hashes use a launcher-specific encoding, but
the underlying candidate and trace bytes are independently pinned by the
pipeline digests and per-file hashes.

The sole structured trace file has the recorded SHA-256
`c9eb932a829c31659331c2a3457245f327c7365b15e67b3134c4fd45d53af67b`.
All 112 JSONL records parse, and the trace content-tree digest is
`2e3d8e69633f35f41520183075a9715b6e85182bf501dc1d07b6f18826976ae5`,
matching `usage.json`. The trace and generation logs merely claim that seven
claims passed; that claim was not relied on.

Candidate proof sources and required artifacts are present:
`solution.py`, `solution.mpy`, `semantic.k`, `solution-program.k`,
`verification.k`, `spec.k`, `embed_mpy.py`, and `prove.sh`. Candidate Python
bytecode was ignored, and no candidate K definition or cache was copied into
the clean build.

Evidence:

- [provenance checks](/audit-output/evidence/01-provenance-check.log), exit 0;
- [campaign prompt hash](/audit-output/evidence/01-campaign-prompt-hash.log),
  exit 0;
- [structured trace inspection](/audit-output/evidence/01-structured-trace-summary.log),
  exit 0;
- [candidate and trusted sources](/audit-output/evidence/01-candidate-and-reference-sources.log),
  exit 0;
- [toolchain](/audit-output/evidence/00-toolchain.log): K 7.1.293 and Python
  3.10.12.

Stage 1 result: integrity established; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks whether two words have the same characters. The trusted
canonical implementation makes that precise as:

```python
return set(s0) == set(s1)
```

Thus order and repeated occurrences do not matter, while any character present
on only one side makes the result false. The documented type domain is pairs
of Python strings; no length or alphabet bound is stated.

The submitted [solution.py](/candidate/solution.py) has the same two parameters
and exactly the same return expression. Running the trusted translator on that
file produced bytes identical to submitted
[solution.mpy](/candidate/solution.mpy), SHA-256
`50ea732f523d5b7b821b7f2c3a1055e0456cf1e8b9b57d306d967066453a8d07`.

The independent [differential test](/audit-output/evidence/differential_test.py)
imports the trusted canonical and copied candidate as distinct modules. Its
scope was:

- all six documented examples;
- 15 empty, singleton, duplicate, order, extra-character, NUL, newline, BMP,
  combining-sequence, and astral-Unicode boundaries;
- all 116,281 pairs of strings of length at most four over
  `("a", "b", "é", "😀")`;
- 20,000 deterministic generated pairs of length 0 through 32 over an
  eight-character mixed alphabet.

It executed 136,302 pairs, reached both result branches
(`13,511` true and `122,791` false), found zero mismatches, and exited 0.
This is finite fidelity evidence, not a substitute for the K proof.

Evidence:

- [translation byte identity](/audit-output/evidence/02-translation-byte-identity.log),
  exit 0;
- [Python differential results](/audit-output/evidence/02-python-differential.log),
  exit 0.

Stage 2 result: no implementation/canonical divergence.

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/54-same-chars/candidate`. Trusted translation and embedding
were rerun there. No candidate-provided compiled definition was present or
used.

Fresh concrete definition:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
```

Exit 0. See [LLVM build log](/audit-output/evidence/03-build-concrete-llvm.log).

Fresh proof definition:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Exit 0. See
[Haskell build log](/audit-output/evidence/03-build-proof-haskell.log).

The independent
[concrete semantics test](/audit-output/evidence/concrete_semantics_test.py)
ran the fresh LLVM definition on 12 normal and boundary input pairs. It covered
documented true/false cases, empty strings, one empty side, duplicate and
reordered characters, an extra character, NUL, newline, BMP Unicode, canonically
distinct Unicode spellings, and astral Unicode. Every K result agreed with both
Python functions; mismatch count was zero and the script exited 0. The exact
per-case `krun` commands and outcomes are in
[the concrete log](/audit-output/evidence/03-concrete-semantics-vs-python.log).

The unmodified candidate spec was proved as one target:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

It printed exactly `#Top` and exited 0; see
[the original-spec log](/audit-output/evidence/03-proof-all-original.log).

For independent per-claim execution, an audit copy added labels without
changing any claim body:
[spec-labeled-audit.k](/audit-output/evidence/spec-labeled-audit.k). Each
command used `kprove spec-labeled.k --definition proof-kompiled
--spec-module SPEC-LABELED --claims <label>`. The universal claim and example
claims 1 through 6 each printed `#Top` and exited 0:

- [universal](/audit-output/evidence/03-proof-universal.log);
- [example 1](/audit-output/evidence/03-proof-example-1.log);
- [example 2](/audit-output/evidence/03-proof-example-2.log);
- [example 3](/audit-output/evidence/03-proof-example-3.log);
- [example 4](/audit-output/evidence/03-proof-example-4.log);
- [example 5](/audit-output/evidence/03-proof-example-5.log);
- [example 6](/audit-output/evidence/03-proof-example-6.log).

The consolidated
[evidence-status audit](/audit-output/evidence/07-evidence-status-audit.log)
checks all build/proof exits and all eight fresh `#Top` outputs.

Stage 3 result: both fresh dynamic reconstruction gates pass.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The universal claim has no `requires` clause. Its starting state is:

- `<k>` contains `solutionProgram`;
- `<s0>` and `<s1>` contain arbitrary K strings `S0` and `S1`;
- `<env>` is empty;
- `<result>` is `noResult`.

It requires complete consumption of `<k>`, exact bindings
`s0 -> stringValue(S0)` and `s1 -> stringValue(S1)`, and the final result

```text
boolValue(sameCharsSpec(S0, S1))
```

where `sameCharsSpec(S0,S1)` rewrites to
`charSet(S0) ==K charSet(S1)`. This is an exact returned Boolean, not a fresh
right-hand variable, implication, or unconstrained destination.

The six example claims have the same empty-environment/no-result starting
shape, substitute the six prompt pairs, and demand respectively
`true, true, true, false, false, false`. The input cells remain unchanged and
the environment bindings are constrained in every destination.

Every precondition is satisfiable. For the universal claim,
`S0 = ""` and `S1 = ""` is one witness. For each example claim, its displayed
concrete pair together with `.Map` and `noResult` is a witness. Substituting
those values yields the stated canonical/candidate results, as independently
checked in Stages 2 and 3.

### Mechanical program identity

[check_program_pinning.py](/audit-output/evidence/check_program_pinning.py)
performed four independent checks:

1. after removing only the canonical docstring, canonical and candidate
   function bodies have identical CPython AST dumps;
2. trusted translation equals submitted `solution.mpy`;
3. K's own parser gives the same `Program` constructor JSON for translated
   `solution.mpy` and the right-hand side of the `solutionProgram` rule;
4. all seven entry claims begin with `solutionProgram => .K`.

All checks passed. See
[program-pinning log](/audit-output/evidence/04-program-pinning.log).
`solutionProgram` is therefore the exact translated binding and body, not a
substituted algorithm or prose-level surrogate.

The direct-entry `Module(FuncDef(...))` rule is the semantics' invocation
harness: it binds the actual two formal parameter names to the two input cells
and then executes the actual body. Ignoring the function-name variable is
over-broad for other hypothetical modules but does not change the selected
binding here: the mechanically pinned module contains the sole
`same_chars` definition, and the source contains no rebinding of `set`.

### Body sensitivity

A separate source mutation changed the body to the demonstrably wrong
`return s0 == s1`. Trusted translation changed the constructor tree from calls
to `set` into direct name comparison. The mutated definition built
successfully, but the target proof exited 1 with `WarnStuckClaimState` at:

```text
stringValue(S1) ~> compareValues(stringValue(S0)) ~> finishReturn
```

Thus the proof executes and depends on the material body. Mutation artifacts
are under [body-mutant](/audit-output/evidence/body-mutant/); see the
[generation](/audit-output/evidence/04-body-mutation-generate.log),
[build](/audit-output/evidence/04-body-mutation-build.log), and
[expected proof failure](/audit-output/evidence/04-body-mutation-proof-expected-failure.log).

Stage 4 result: the claims are satisfiable, result-constraining, and pinned to
the real generated program.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

`semantic.k` declares:

- `Program`: `Module(Function)`;
- `Function`: `FuncDef(String, Params, Statement)`;
- `Params`: exactly two `String` names;
- `Statement`: `Return(Expr)`;
- `Expr`: `Name(String)`, `Call(Expr,Expr)`, and
  `Compare(Expr,CmpOp)`;
- `CmpOp`: `CmpOp(String,Expr)`;
- `Value`: `stringValue(String)`, `setValue(Set)`, and
  `boolValue(Bool)`;
- `Result`: `noResult` and `result(Value)`;
- `Set`: `charSet(String) [function]`;
- `KItem`: `eval(Expr)`, `makeSet`, `compareRight(Expr)`,
  `compareValues(Value)`, and `finishReturn`.

Its configuration contains exactly `<k>`, the two immutable string-input cells,
an environment map, and a result cell. No unused heap, stack, allocation,
exception, I/O, or mutable-object cell is present.

`solution-program.k` adds the nullary
`solutionProgram : Program [function]`. `verification.k` adds
`sameCharsSpec(String,String) : Bool [function,total]`.

There are no local `[functional]`, simplification, priority, `owise`, macro,
strictness, or opaque declarations. There are no local lemmas or auxiliary
reachability claims outside `spec.k`. The mechanical inventory and counts are
preserved in
[05-local-rule-inventory.log](/audit-output/evidence/05-local-rule-inventory.log).

### Complete rule inventory and decisions

| ID | Rule | Static decision |
|---|---|---|
| S1 | `charSet("") => .Set [concrete]` | Sound base case: the empty string contains no characters. |
| S2 | Nonempty `charSet(S)` becomes `SetItem(substrString(S,0,1)) \|Set charSet(substrString(S,1,lengthString(S))) [concrete]` | Sound for every concrete nonempty string. The head is one code point, the tail drops it, and recursion strictly decreases length. Set insertion/union removes duplicates and ignores order. Its nonempty guard is disjoint from S1. |
| S3 | `Module(FuncDef(_F,Params(P0,P1),BODY)) => BODY`, initializing the two bindings from `<s0>/<s1>` | Sound as the explicit entry-function invocation harness for the pinned two-argument program. It writes only `<env>` and `<k>`, and preserves both inputs and result. |
| S4 | `Return(E) => eval(E) ~> finishReturn` | Sound sequencing of return-expression evaluation before result storage. |
| S5 | `eval(Name(N)) => V` when the environment contains `N |-> V` | Sound lexical lookup for the only used parameter names. |
| S6 | `eval(Call(Name("set"),E)) => eval(E) ~> makeSet` | Sound left-to-right argument evaluation for the builtin selected in the actual source. No local/global `set` rebinding exists. |
| S7 | `stringValue(S) ~> makeSet => setValue(charSet(S))` | Sound implementation of Python `set` on a string in the modeled domain. It is transparent through S1/S2, not an unconstrained oracle. |
| S8 | Equality comparison begins by evaluating `E0`, then records `E1` | Sound Python operand order. |
| S9 | The evaluated left `Value` is saved while `E1` is evaluated | Sound continuation and binding of the left value. |
| S10 | Right `setValue(CHARS1)` with saved left `setValue(CHARS0)` becomes `boolValue(CHARS0 ==K CHARS1)` | Sound set equality. The apparent variable order correctly restores left-then-right values, and equality is symmetric in any event. |
| S11 | `V ~> finishReturn` consumes `<k>` and changes `noResult` to `result(V)` | Sound final return transition; it changes only control and result. |
| G1 | `solutionProgram =>` the complete submitted constructor tree | Sound nullary definitional constant. Mechanical KAST comparison establishes exact identity. |
| V1 | `sameCharsSpec(S0,S1) => charSet(S0) ==K charSet(S1)` | Sound, unconditional definitional summary of the canonical contract. Its single equation covers the declared total domain. |

For `charSet`, `[concrete]` deliberately prevents symbolic recursion; it does
not fabricate a symbolic result. S1/S2 cover every ground K string, are
disjoint, and S2 terminates by induction on string length. The universal proof
can retain the transparent `charSet(S)` term symbolically, while every ground
instance has the above unique computation. There is no opposite ground
interpretation admitted by these equations.

Construct coverage is complete:

- `Module`, `FuncDef`, and `Params` use G1 and S3;
- `Return` uses S4 and S11;
- both `Call(Name("set"),Name(...))` terms use S5–S7;
- `Compare` and `CmpOp("==",...)` use S8–S10;
- concrete set construction uses S1/S2.

All material operations and control effects in `solution.mpy` therefore
execute. The environment is initialized once from `.Map`; comparison evaluates
left before right; the only state change after binding is the exact result
write. No used construct is silently dropped or assigned a fabricated value.
Rule front shapes and the S1/S2 guards are disjoint, so no priority is needed.

`sameCharsSpec` is a definitional summary, not an operational bridge.
`solutionProgram` is a generated source constant. The implementation of the
external Python builtin `set` belongs to the generated semantics and is fixed
by exhaustive ground equations. There is no proof-local rewrite that skips a
program-defined body, no result-bearing opaque symbol, and no task-answer rule.

No rule was classified unsound, so no false-conclusion witness is asserted.
Potential general-language omissions are irrelevant here because the generated
semantics rejects rather than guesses at syntax outside its grammar, and every
construct in the submitted program is covered.

Stage 5 result: the local theory is sound for the actual program and intended
typed inputs.

## 6. Fresh non-vacuity test

The fresh mutation
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k) uses the
satisfying input state `s0 = ""`, `s1 = ""`, `.Map`, and `noResult`, but changes
the result obligation to the false `boolValue(false)`.

Parsing/building the proof input:

```text
kprove spec-vacuity-audit.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited 0 and emitted a valid `kore-exec ... --prove ...` command. See
[dry-run log](/audit-output/evidence/06-vacuity-mutation-dry-run.log).

Running the mutation without `--dry-run` exited 1 with
`WarnStuckClaimState`. The residual was a completed computation with:

```text
<k> .K </k>
<result> result ( boolValue ( true ) ) </result>
```

This is the expected unmet result obligation, not a parser error, missing
import, unreachable mutation, timeout, or unrelated crash. See
[expected-failure log](/audit-output/evidence/06-vacuity-mutation-proof-expected-failure.log).

Stage 6 result: the proof is non-vacuous and discriminates a false result.

## 7. Proven versus assumed accounting

### What is formally established

Under the freshly compiled generated MPY semantics, for every pair of finite K
strings, execution of the exact translated `same_chars` binding and body from
the configured entry state reaches `.K`, preserves the two input cells, creates
the exact two parameter bindings, and stores:

```text
result(boolValue(charSet(S0) ==K charSet(S1)))
```

The six documented concrete instances reach the expected exact Boolean.
Because this is a partial-correctness proof, the reachability result is stated
conditional on termination. The transparent `charSet` recursion terminates on
every finite concrete string, but total-correctness/termination is not a
separate claimed theorem.

### Trust ledger

| Boundary | Dependents and effect | Assessment |
|---|---|---|
| K 7.1.293 compiler, parser, Haskell prover, LLVM executor, and kernel/runtime correctness | All parsing, execution, and `#Top` results | Standard unavoidable toolchain trust; version and fresh commands recorded. |
| Imported `STRING`, `SET`, `MAP`, `BOOL`, `INT`, and `K-EQUAL` primitives, especially `substrString`, `lengthString`, `SetItem`, set union, map lookup, and `==K` | Character decomposition, duplicate removal, set equality, bindings, and final Boolean | Acceptable low-level semantic boundary. Local rules use these primitives in their ordinary domains; NUL, newline, BMP, combining, and astral cases were concretely checked. |
| Trusted `py2mpy.py` transliteration | Python-source-to-constructor identity | Launcher-trusted input, byte-matched against the candidate copy, rerun from scratch, and mechanically compared with the K embedded term. |
| Direct-entry interpretation of a single two-argument `FuncDef` | Parameter binding and execution start | Acceptable explicit harness for a HumanEval entry point. Exact source shape, formal names, sole binding, and body were mechanically checked. |
| Static induction that S1/S2 implement the mathematical character set | Summary-to-natural-contract meaning | Acceptable transparent argument: exhaustive disjoint ground cases and strict descent. It is additionally supported, but not replaced, by fresh K/Python concrete tests. |
| Trusted canonical Python implementation | Intent oracle for finite differential testing | Evidence only; it was not imported by or used to close the K proof. |

There are no additional opaque symbols, empirical oracles, proof-local
operational bridges, assumed lemmas, or simplification equations. Behavior for
non-string Python arguments and general Python modules is outside the prompt's
typed domain and outside this deliberately minimal semantics. String length
and alphabet are unrestricted.

Kit validation gates:

- Gate A (real-program soundness and non-vacuity): pass.
- Gate B (intent and domain adequacy): pass.
- Gate C (trust and reproducible evidence): pass.

The reconstructed proof is sound, result-constraining, body-sensitive, and
covers the material source-contract domain without bounded unrolling or
example-only restriction.

VERDICT: PASS
LEGITIMACY: LEGIT
