# Independent adversarial audit: 10-make-palindrome

## Executive decision

The candidate's artifacts rebuild, all eight positive claims independently print
`#Top`, and the submitted `.mpy` is the byte-identical output of the trusted
translator. Those facts do not make the universal proof legitimate.

The decisive defect is the priority rule in `verification.k`:

```k
rule #call("make_palindrome", strVal(S), P)
  => strVal(#reference(S))
  requires P ==K #solution
  [priority(40)]
```

It replaces execution of the program-defined function with the exact
result-bearing symbol used in the postcondition. There is no auxiliary
reachability claim proving that fixed execution of the body yields that value.
The reviewer body-sensitivity experiment changed only the body represented by
`#solution` to `return "WRONG"` while leaving the bridge and specification
unchanged. Fixed semantics then returned `"WRONG"` and rejected the ground
`"cat" -> "catac"` claim, but the augmented universal claim still returned
`#Top`. Thus claim closure is insensitive to the displaced computation and
assumes the missing program-to-summary theorem.

I do not assert that the bridge equation is false for the original submitted
body: the recursive implementation appears extensionally correct on ordinary
inputs, and the independent finite tests support that. The narrower and
decisive finding is that the candidate contains no K proof of that connection;
it installs the desired connection as an operational rule. Under the required
proof-extension validation standard, this is an illegitimate proof shortcut.

There are also two real-Python modeling limitations: the recursive Python
implementation raises `RecursionError` on a documented long satisfying input
where the K model returns normally, and the candidate's concrete `krun`
configuration-input route mishandles non-ASCII text as UTF-8 bytes. These are
additional adequacy/bridge defects, not substitutes for the primary Gate A
failure.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` is absent, so there is no infrastructure
contradiction and no hidden semantics was sought or used. See
[01-integrity.log](/audit-output/evidence/01-integrity.log).

### Candidate artifacts

The following required generation artifacts are present as regular files:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`;
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

The structured trace is present at
`codex-trace/2026/07/22/rollout-2026-07-22T04-00-32-019f890e-20e7-7911-b8f2-adfeda820084.jsonl`.
It contains 208 valid JSONL records. No symlinks occur anywhere under
`/candidate`. The candidate has no `PROOF.md`, but that was not a required
generation deliverable and its absence is not an integrity failure. The
candidate-built `semantic-kompiled/`, `execution-kompiled/`,
`execution-proof-kompiled/`, `__pycache__/`, mutation files, and logs are extra
generated evidence; none was used as a trusted definition or cache.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions:

- prompt SHA-256:
  `60e80406bde04ba96808271e9ba8fd58129b6e8570d3ef23a2eb4c8a79370913`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The checks, complete root inventory, symlink scan, and untrusted JSON summaries
are preserved in
[01-integrity.log](/audit-output/evidence/01-integrity.log),
[01a-provenance-json.log](/audit-output/evidence/01a-provenance-json.log), and
[01b-symlink-scan.log](/audit-output/evidence/01b-symlink-scan.log).

### Untrusted generation claims

`codex-last.txt` and `codex-output.log` claim that two module-level proof runs
printed `#Top`, six concrete runs passed, a mutation failed, and 1,093 Python
inputs agreed. Fresh reconstruction confirms the positive K closure and
independently reproduces zero short-input Python mismatches. The claimed
1,093-case candidate test is not preserved as a standalone candidate script or
bounded log, so it is not accepted as candidate audit evidence. The reviewer
created an independent replacement in Stage 2.

One candidate comment is factually inverted: `verification.k` says concrete
runs use `SEMANTIC` and therefore do not import the proof rule, but module
`SEMANTIC` imports `VERIFICATION`. The candidate script actually uses the clean
module `EXECUTION` for concrete runs, so the rebuilt concrete tests were not
contaminated.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For every Python `str`, `make_palindrome(string)` is to return the shortest
palindrome having `string` as its prefix. The trusted canonical implementation:

1. returns `""` for the empty input;
2. finds the earliest position at which the remaining suffix is a palindrome;
3. appends the reverse of the preceding prefix.

The submitted implementation uses a different recursive algorithm. It returns
the input immediately if it is already a palindrome; otherwise, for
`string = first + tail`, it returns
`first + make_palindrome(tail) + first`. This is plausibly equivalent: if the
whole nonempty string is not a palindrome, its longest palindromic suffix is
also a suffix of `tail`, and the recursive construction adds the displaced
first character at the opposite end. That mathematical observation is not the
candidate's K connection proof.

### Translation fidelity

The trusted command

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0, and `cmp` reported byte identity with the submitted `solution.mpy`.
Both files have SHA-256
`dfd4a00dfcd76ba357ecbc59ebeb64e7dbe9586b062fbd9253b979cf78e379e7`.
See [02-regenerate.log](/audit-output/evidence/02-regenerate.log).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) separately
imports `/reference/canonical.py` and the scratch copy of `solution.py`. It
covers:

- all three prompt examples;
- empty, one-character, immediate-palindrome, and first-recursive cases;
- both candidate branches and the canonical zero/multiple-loop boundaries;
- combining Unicode, an astral Unicode character, and an embedded NUL;
- every string over `{a,b,c}` through length 6 (1,093 generated strings);
- a recursion-depth boundary, `"a" * 1200 + "b"`.

All 1,093 generated short strings and the ordinary named cases agree. The long
case is a material result divergence over the unrestricted annotated `str`
domain: the canonical function returns a palindrome of length 2,401, while the
submitted recursive function raises `RecursionError`. The complete bounded
record is [03-differential.log](/audit-output/evidence/03-differential.log).
This does not falsify partial correctness for normal returns, but it does show
that a K claim giving a normal result for every string is not a full model of
the real CPython program.

## 3. Clean proof reconstruction

All candidate-built definitions and caches were ignored. Only regular source
files were copied to `/tmp/audit-work`. The available tools were K
v7.1.293 and Python 3.10.12; see
[00-tool-versions.log](/audit-output/evidence/00-tool-versions.log).

### Fresh builds

All three independent builds exited 0:

| Definition | Command purpose | Evidence |
|---|---|---|
| `execution-llvm-kompiled` | LLVM concrete `EXECUTION` semantics | [10-build-execution-llvm.log](/audit-output/evidence/10-build-execution-llvm.log) |
| `execution-haskell-kompiled` | Haskell clean `EXECUTION` proof semantics | [11-build-execution-haskell.log](/audit-output/evidence/11-build-execution-haskell.log) |
| `proof-haskell-kompiled` | Haskell `SEMANTIC` with `VERIFICATION` | [12-build-proof-haskell.log](/audit-output/evidence/12-build-proof-haskell.log) |

### Every positive claim, run independently

Every claim was selected by its fully qualified label. Each command exited 0
and printed `#Top`:

| Claim | Definition | Evidence |
|---|---|---|
| `CONCRETE-SPEC.empty` | clean | [20-proof-concrete-empty.log](/audit-output/evidence/20-proof-concrete-empty.log) |
| `CONCRETE-SPEC.cat` | clean | [21-proof-concrete-cat.log](/audit-output/evidence/21-proof-concrete-cat.log) |
| `CONCRETE-SPEC.cata` | clean | [22-proof-concrete-cata.log](/audit-output/evidence/22-proof-concrete-cata.log) |
| `CONCRETE-SPEC.xyx` | clean | [23-proof-concrete-xyx.log](/audit-output/evidence/23-proof-concrete-xyx.log) |
| `CONCRETE-SPEC.abcd` | clean | [24-proof-concrete-abcd.log](/audit-output/evidence/24-proof-concrete-abcd.log) |
| `CONCRETE-SPEC.aabb` | clean | [25-proof-concrete-aabb.log](/audit-output/evidence/25-proof-concrete-aabb.log) |
| `SPEC.functional-correctness` | proof-augmented | [26-proof-functional.log](/audit-output/evidence/26-proof-functional.log) |
| `SPEC.helper-correctness` | proof-augmented | [27-proof-helper.log](/audit-output/evidence/27-proof-helper.log) |

This establishes verification under the supplied theory. It does not validate
the theory's priority call rule.

### Fresh concrete execution

The reviewer-authored
[krun_compare.py](/audit-output/evidence/krun_compare.py) ran the fresh LLVM
definition on empty, branch-boundary, prompt, recursive, Unicode, and long
inputs and compared each result with both Python implementations. All ASCII
normal cases matched both implementations. The long input returned the
canonical 2,401-character result in K but raised `RecursionError` in the real
candidate.

The non-ASCII run exposes a concrete input-bridge split. Passing `"a🙂b"`
through the configuration variable produces a K token containing its UTF-8
bytes. The slice/reverse rules then return the invalid byte sequence represented
as:

```text
"a\xf0\x9f\x99\x82b\x82\x99\x9f\xf0a"
```

Both Python implementations instead return the valid code-point string
`"a🙂b🙂a"`. The mismatch and exact per-case `krun` commands are in
[15-krun-compare.log](/audit-output/evidence/15-krun-compare.log); raw LLVM and
Haskell outputs are in
[14a-krun-unicode-raw.log](/audit-output/evidence/14a-krun-unicode-raw.log) and
[53-haskell-krun-unicode.log](/audit-output/evidence/53-haskell-krun-unicode.log).
Using a literal `\U0001f642` spelling at `-cINPUT` has the same behavior
([55-krun-unicode-escaped.log](/audit-output/evidence/55-krun-unicode-escaped.log)).

A K-source ground claim containing the same Unicode characters compiled and
proved `#Top`
([51-unicode-witness-build.log](/audit-output/evidence/51-unicode-witness-build.log),
[52-unicode-witness-proof.log](/audit-output/evidence/52-unicode-witness-proof.log)).
That isolates the observed mismatch to the concrete configuration-input
representation rather than proving that the abstract `#reverse` equations are
globally false. I therefore record this as a material, empirically false
Python-to-K input bridge, not as an unsupported claim that a particular
equation is mathematically false over every internal K `String`.

Two retained diagnostic logs are not audit gates:
[14-krun-compare.log](/audit-output/evidence/14-krun-compare.log) records the
first harness version failing to decode K's `\xHH` printer output, and
[54-kast-unicode.log](/audit-output/evidence/54-kast-unicode.log) records an
incorrect diagnostic `kast` invocation. They were superseded by the successful
bounded tests above and are retained for transparency.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`SPEC.functional-correctness` has no explicit `requires`; its sort gives the
domain of every K `String`. It starts with the full configuration whose
computation is `#run(#solution, S)`, program is exactly `#solution`, input is
`S`, `ast-match` is `true`, and result is empty. It requires termination with
empty computation and result exactly `strVal(#reference(S))`.

`SPEC.helper-correctness` has the same unrestricted domain and full
configuration, but runs the exact `is_palindrome` binding and requires result
`boolVal(#isPalindrome(S))`.

The six `CONCRETE-SPEC` claims have ground entry states and exact ground result
strings. There are no loop or loop-invariant claims. The candidate recursion is
the control-flow feature that needs a connection argument.

### Pinning

The formal claims execute the hardcoded K constant `#solution`, not the
`solution.mpy` file directly. Three independent facts connect them:

1. trusted regeneration is byte-identical to `solution.mpy`;
2. manual constructor comparison finds the same two function bodies;
3. fresh `krun solution.mpy` executions initialize `<ast-match>` to `true`,
   proving the parsed module is K-equal to `#solution`.

Thus the claims are syntactically pinned to the submitted AST. The failure is
not substitution of a different original program; it is the proof rule that
preempts that pinned body's execution.

### Satisfiable entry states and ground substitution

For both universal entry claims, choose `S = "cat"`. Fresh `krun` constructs
exactly the claimed initial program, input, empty result, and `ast-match = true`;
it reaches `strVal("catac")`. The helper call returns `false`, which equals
`#isPalindrome("cat")`. The ground substitutions `""`, `"cat"`, `"cata"`,
`"xyx"`, `"abcd"`, and `"aabb"` agree with both Python implementations and
the clean K semantics. These executions are recorded in
[13-krun-empty.log](/audit-output/evidence/13-krun-empty.log) and
[15-krun-compare.log](/audit-output/evidence/15-krun-compare.log).

The postcondition is not a free variable or a one-way implication: it fixes the
result to `#reference(S)`. Stage 6 confirms that changing this result is
rejected. However, the operational bridge itself returns that same symbol, so
the result constraint does not establish that real execution computes it.

### Intent adequacy

No K claim states or proves that `#reference(S)`:

- begins with `S`;
- is a palindrome;
- is no longer than every other palindrome beginning with `S`.

The recurrence is a reasonable executable characterization, and the
independent differential results support its agreement with the canonical
implementation on the tested normal inputs. The shortest-palindrome meaning is
nevertheless an informal mathematical bridge, not a theorem in this candidate.
That limitation would warrant at least `CONCERNS` if Gate A were otherwise
sound.

## 5. Rule-by-rule static soundness review

Line numbers below refer to the complete numbered source record in
[50-numbered-sources.log](/audit-output/evidence/50-numbered-sources.log).

### Exhaustive local declaration inventory

| Location | Declarations |
|---|---|
| `semantic.k:6-26` | `Module(Module(Stmts))`; list sort `Stmts`; statement constructors `FuncDef`, `Return`, `If`; `Params`; expression constructors `Name`, `Str`, `Int`, `UnaryOp`, `BinOp`, `Compare`, `Subscript`, `Slice`, `Call`; `CmpOp`; bounds `Expr` and `NoBound`. All constructors are `[symbol]`. |
| `semantic.k:34` | `#solution : Module [function]`. |
| `semantic.k:68-87` | value constructors `strVal`, `boolVal`, `intVal`; `env`; `function`; outcomes `normal`, `returned`; entry items `#run`, `#runFunction`; functions `#lookup`, `#call`, `#apply`, `#eval`, `#exec`, `#resume`, `#branch`, `#valueEq`, and `#reverse`. |
| `semantic.k:114,150-154` | functions `#outcomeValue`, `#negate`, `#add`, `#indexZero`, `#tail`, and `#reversed`. |
| `verification.k:8-9,31` | proof-local functions `#reference`, `#referenceChoice`, and `#isPalindrome`. |

The only local `[total]` declarations are `#branch`, `#reverse`, `#reference`,
and `#referenceChoice`. There are no local `[functional]`, `[opaque]`,
`[simplification]`, or `[concrete]` declarations or rules. The sole priority
attribute is `[priority(40)]` on the proof bridge.

The configuration has only `<k>`, immutable observational `<program>` and
`<input>` cells, diagnostic `<ast-match>`, and `<result>`. No target construct
needs a heap, allocation, mutation, output, or exceptions; none is modeled.
The missing call-stack/exception component is material at the CPython
recursion-limit boundary described above.

### Exhaustive rule inventory

| ID | Line(s) | Rule and judgment |
|---|---:|---|
| S1 | `semantic.k:35-58` | `#solution` expands to the exact submitted AST. Supported by regeneration and `ast-match = true`. |
| S2 | 98-99 | `#run(P,S)` empties `<k>` and puts the `make_palindrome` call in `<result>`. Correct for this pure result-only model. |
| S3 | 100-101 | `#runFunction` analogously dispatches a named helper. Correct. |
| S4 | 103-104 | `#lookup` returns the first exactly named function and parameter/body. Correct for the ordered module. |
| S5 | 105-107 | Unequal-name lookup skips one definition. Its guard is disjoint from S4. |
| S6 | 109-110 | Ordinary `#call` performs lookup then apply. This is the fixed behavior preempted by V4. |
| S7 | 111-112 | `#apply` binds the sole parameter and executes the body. Correct for the target's one-argument functions; no Python stack behavior is modeled. |
| S8 | 115 | `#outcomeValue(returned(V)) = V`. Correct; a `normal` outcome intentionally remains stuck. Both target functions return on modeled paths. |
| S9 | 117 | Empty statement list yields `normal`. Correct. |
| S10 | 118 | `Return(E)` evaluates `E`, returns it, and discards following statements. Correct abrupt-return behavior. |
| S11 | 119-122 | `If` evaluates the condition, executes the selected statements, then resumes the suffix. Correct target control flow. |
| S12 | 123 | A returned branch propagates its value and suppresses the suffix. Correct. |
| S13 | 124 | A normal branch continues with the suffix. Correct. |
| S14 | 126-127 | `boolVal(true)` selects the then branch. Correct. |
| S15 | 128-129 | `boolVal(false)` selects the else branch. Correct and disjoint from S14. |
| S16 | 131 | Name lookup succeeds only for the sole environment binding. Sufficient for this program. |
| S17 | 132 | String literals become `strVal`. Correct. |
| S18 | 133 | Integer literals become `intVal`. Correct. |
| S19 | 134-135 | Unary `-` delegates to integer negation. Correct for the slice step `-1`. |
| S20 | 136-137 | `+` evaluates nested operands and delegates to `#add`. The target operands are pure strings, so omitted side-effect/exception ordering is immaterial on modeled normal paths. |
| S21 | 138-139 | `==` evaluates both values and delegates to `#valueEq`. Correct for target strings. |
| S22 | 140-141 | Index zero delegates to `#indexZero`. Its nonempty requirement is enforced in S28 and is reached only after a false whole-string palindrome test. |
| S23 | 142-143 | `[1:]` delegates to `#tail`. Correct over the internal K string model; the concrete configuration-input Unicode bridge is empirically inadequate. |
| S24 | 144-146 | `[::-1]` delegates to `#reversed`. Correct shape for the only reverse slice used. |
| S25 | 147-148 | A named one-argument call evaluates its argument then calls through the current module. Correct binding for the exact program. |
| S26 | 155 | Integer negation computes `0 -Int I`. Correct. |
| S27 | 156 | String addition uses `+String`. Correct in the internal string model. |
| S28 | 157-158 | Index zero is `substrString(S,0,1)` for nonempty `S`. Guard is appropriate; the Python/K external string representation remains an unproved boundary. |
| S29 | 159-160 | Tail is `substrString(S,1,lengthString(S))` for nonempty `S`. It strictly decreases internal length. Same external string boundary as S28. |
| S30 | 161 | `#reversed(strVal(S))` wraps `#reverse(S)`. Correct. |
| S31 | 163 | String value equality is `==String`. Correct. |
| S32 | 165 | Empty string reversal is empty. Correct. |
| S33 | 166-169 | Nonempty reversal takes the final unit and recurses on the preceding units. Guard is disjoint from S32 and internal length decreases. Concrete `-cINPUT` Unicode evidence shows byte behavior at the execution interface; the K-source Unicode ground proof prevents attributing a universally false equation without further evidence. |
| V1 | `verification.k:10-11` | `#reference` dispatches on equality with its reverse. A definitional summary, not a proof of the human-facing property. |
| V2 | 12-13 | True reference choice returns `S`. Correct and disjoint from V3. |
| V3 | 14-18 | False, nonempty choice wraps the recursively summarized tail with the first unit. It decreases length and matches the submitted algorithm's recurrence. |
| V4 | 24-27 | Priority operational bridge replaces the exact program-defined `make_palindrome` call with `strVal(#reference(S))`. It preempts S6, affects the final result, and has no machine-checked connection theorem. The same `#reference(S)` occurs in the postcondition. This is circular proof evidence and is illegitimate. |
| V5 | 32 | `#isPalindrome(S)` is definitionally equality with `#reverse(S)`. It matches the helper body in the modeled string theory. |

### Construct coverage map

Every constructor actually present in `solution.mpy` has both syntax and
behavior:

| Submitted construct | Declaration | Operational path |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement list | `semantic.k:6-13` | S4-S7 |
| `Return` | `semantic.k:10` | S10, S12 |
| `If` with empty else | `semantic.k:11` | S11, S14-S15, S12-S13 |
| `Name` | `semantic.k:15` | S16 |
| `Int(0)`, `Int(1)` | `semantic.k:17` | S18, S22-S23 |
| `UnaryOp("-")` | `semantic.k:18` | S19, S26 |
| `BinOp("+")` | `semantic.k:19` | S20, S27 |
| `Compare`/`CmpOp("==")` | `semantic.k:20,25` | S21, S31 |
| three used `Subscript`/`Slice` shapes and `NoBound` | `semantic.k:21-23,26` | S22-S24, S28-S30, S32-S33 |
| named one-argument `Call` | `semantic.k:23` | S25, S4-S8 |

There are no assignments, loops, mutation, allocation, I/O, multi-argument
calls, closures, or exceptions in the submitted syntax.

### Guards, overlaps, and totality

The hit/miss lookup rules, true/false branch rules, outcome rules, expression
patterns, reverse base/step rules, and reference-choice branches are pairwise
disjoint on their guards or constructors.

Two `[total]` declarations are globally broader than their equations:

- `#branch` has sort `Val` but only handles `boolVal`; the satisfiable ground
  term `#branch(strVal("x"), .Stmts, .Stmts)` has no equation.
- `#referenceChoice("", false)` satisfies neither V2 nor V3.

These are concrete coverage witnesses, not witnesses to a false equality. Both
terms are outside the uses reached by the submitted program/reference
dispatcher, so I record them as totality declaration gaps rather than material
false conclusions for this target. `#reverse` covers empty/nonempty strings,
and `#reference`'s actual calls to `#referenceChoice` avoid the uncovered
`("",false)` pair.

### Operational-bridge validation

V4 matches any pure occurrence of the exact call whose module is K-equal to
`#solution`; because calls are represented as functions, it can occur in any
functional continuation. The fixed execution it displaces performs lookup,
parameter binding, condition evaluation, helper execution, recursive calls,
and return propagation. There are no mutable cells or observable output to
preserve, so value fidelity is the central obligation.

No connection claim establishes that fixed execution yields
`#reference(S)`. V4 and the functional postcondition use the same
result-bearing symbol, which is circular rather than evidence of equivalence.

The reviewer operational-sensitivity mutation is preserved under
[body-sensitivity/](/audit-output/evidence/body-sensitivity/). It changed the
hardcoded body and matching translated program to `return "WRONG"` without
changing `verification.k` or `spec.k`:

- both mutated definitions built successfully:
  [40-body-build-execution.log](/audit-output/evidence/40-body-build-execution.log),
  [41-body-build-proof.log](/audit-output/evidence/41-body-build-proof.log);
- fixed concrete execution on `"cat"` returned `"WRONG"` with
  `ast-match = true`:
  [42-body-concrete-run.log](/audit-output/evidence/42-body-concrete-run.log);
- the clean ground `"cat" -> "catac"` claim failed with residual `"WRONG"`:
  [43-body-fixed-claim.log](/audit-output/evidence/43-body-fixed-claim.log);
- the augmented universal functional claim still printed `#Top`:
  [44-body-augmented-functional.log](/audit-output/evidence/44-body-augmented-functional.log).

The exact semantic mutation is in
[45-body-semantic-diff.log](/audit-output/evidence/45-body-semantic-diff.log).
This is a concrete false-conclusion witness for the unchanged bridge/spec proof
architecture on the satisfying input `"cat"` and shows that the alleged
"symbolic execution lemma" is not body-derived. It does not purport to prove
the original equation false; it proves the candidate's derivation is
body-insensitive and therefore missing its mandatory connection theorem.

## 6. Fresh non-vacuity test

The candidate's mutation files were inspected only as untrusted evidence. The
reviewer created the independent
[fresh-vacuity.k](/audit-output/evidence/fresh-vacuity.k). It preserves the
original satisfying `"cat"` entry state but changes the result obligation from
`#reference("cat")` to `#reference("cat") +String "x"`.

The dry run built the mutation successfully and exited 0:
[30-vacuity-build.log](/audit-output/evidence/30-vacuity-build.log).
The actual proof exited 1 with `WarnStuckClaimState`; its residual result is
`strVal("catac")`, demonstrating the unmet false obligation rather than a
parser/import/backend failure:
[31-vacuity-proof.log](/audit-output/evidence/31-vacuity-proof.log).

The proof is therefore result-constraining in the narrow non-vacuity sense.
This does not repair V4: a postcondition can discriminate among results while
an operational bridge assumes the selected result.

## 7. Proven-versus-assumed accounting

### What successful reachability establishes

Conditional on every rule in the proof definition:

- the exact hardcoded `#solution` entry reaches
  `strVal(#reference(S))` for every internal K `String`;
- the exact helper entry reaches the K string-equality/reversal predicate;
- six ground ASCII executions reach their stated results.

For the universal target, the first item is obtained by S2 followed by V4. It
does not establish by symbolic execution that the submitted recursive body
computes the reference.

### Trust ledger

| Boundary or assumption | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, Haskell/LLVM backends, and core Bool/Int/String/K-equality builtins | all builds, executions, proofs | Ordinary low-level trust boundary; version and commands recorded. |
| Trusted `py2mpy.py` transliteration | program/AST identity | Acceptable and byte-checked. |
| Hardcoded `#solution` equals parsed `solution.mpy` | all formal claims | Supported by byte regeneration, manual structure, and `ast-match = true`; not itself the proof defect. |
| Generated Python subset semantics S2-S33 | bridge from K execution to real Python | Adequate on exercised normal ASCII paths, but incomplete for CPython recursion exceptions and empirically failing at the concrete non-ASCII configuration-input boundary. |
| V4: fixed body execution equals `#reference(S)` | universal functional claim | Illegitimate program-derived operational bridge. No auxiliary theorem; body-sensitivity test shows proof closure survives a false body. |
| V1-V3 recurrence means "shortest palindrome beginning with S" | human-facing contract | Informal mathematical argument plus finite differential evidence only; no K theorem for prefix, palindrome, or minimality. |
| Python differential test | implementation/canonical bridge on tested inputs | 1,093 exhaustive short generated inputs plus named boundaries; finite support only. It also exposes the long-input divergence. |
| Termination and exception behavior | all-string claim about the real Python function | Not modeled. The K program returns on the long witness where CPython raises `RecursionError`. |

### Gate results

- **Gate A — real-program soundness: FAIL.** V4 bypasses a
  program-defined, result-bearing computation and uses the same summary symbol
  as the postcondition without a machine-checked connection theorem. The
  operational-sensitivity experiment demonstrates body-insensitive `#Top`.
- **Gate B — intent adequacy: FAIL independently as a full real-program
  account.** The formal postcondition is only a recursive summary, not the
  stated prefix/palindrome/minimality property; CPython recursion and the
  concrete Unicode input bridge also diverge.
- **Gate C — auditability: mixed.** The candidate retained substantial logs and
  sources but no successful-proof validation report or standalone claimed
  differential artifact. This review supplies reproducible independent
  evidence; finite tests do not replace the missing theorem.

All positive reconstruction and non-vacuity conditions were met. The verdict
is nevertheless `FAIL / NOT_LEGIT` because the candidate's universal K proof
assumes, via an operational priority rule, the central program-to-result fact
it was required to prove.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
