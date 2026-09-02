# Independent adversarial review: 118-get-closest-vowel

The candidate's K claims reconstruct and close, and the postcondition is
non-vacuous. They nevertheless do **not** constitute a legitimate proof of the
real generated Python program. The generated semantics (1) replaces membership
evaluation with a task-specific rule that ignores the value bound to `vowels`,
and (2) models unbounded recursion while the submitted recursive Python raises
`RecursionError` on valid, unbounded source-contract inputs. Both have concrete
false-behavior witnesses below.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. I read the complete launcher record,
its `container_paths`, hashes, integrity fields, and all records required for
that layout:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- all 459 JSON objects in the one structured trace file under
  `/generation-evidence/codex-trace/`.

The trace was valid JSONL and ended in the recorded final answer, token-count,
and task-complete events. The generation records claim `KPROVE_PASSED`; that
claim was not used as proof evidence.

The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. The lock's independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value. All launcher-declared direct file hashes match,
including the trusted canonical, prompt, translator, manifests, generation
log, trace file, metrics, and usage record. Required entries are real regular
files/directories; there are no symlinks in the candidate, reference, or
generation-evidence trees.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The trusted and candidate
`reference-semantics` paths are both absent, as GENERATED_SEMANTICS requires.
No hidden or inferred semantics was used.

The audit record contains two tree-digest fields without declaring their
digest algorithm. Independently reproducing the benchmark pipeline's
`sha256_tree` gives candidate digest
`100ee288dffad91c4a5c156b8441b26b67494a49cbff6330877767292bab518f`,
which exactly equals both `generation-result.json`'s workspace digest and
`invocation.json`'s retained-workspace digest. The reproduced trace digest
`ac1344152801194b580847f8c47021526d206cfa8f1e3808000334c54c94fa61`
exactly equals `usage.json`'s source-trace digest. The opaque audit-level tree
fields have different values, but every file-level binding and the
generation-owned tree bindings are intact; this is not a missing, unreadable,
or contradictory mount.

Evidence:
[provenance checker](evidence/provenance/provenance_check.py),
[checker log](evidence/provenance/provenance_check.log), and
[bounded generation-record inspection](evidence/provenance/generation_records.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a string consisting only of English letters, inspect eligible internal
positions from right to left. Return the first character that is one of the ten
case-sensitive vowels `aeiouAEIOU` and has consonants immediately on both
sides. A vowel at either endpoint is ineligible. Return `""` if no position
qualifies. The prompt imposes no maximum word length.

The trusted canonical scans indices `len(word)-2` down to `1`. The submitted
`solution.py` checks the final three-character window and recursively calls
itself on `word[:-1]` after a failed window. This is extensionally equivalent
while the recursive Python call returns normally, but it is not equivalent on
the full stated domain because actual CPython has a recursion-depth limit.

### Translation identity

Running the trusted translator on the scratch copy of `solution.py` exited 0.
The regenerated `solution.mpy` is byte-identical to the submission; both have
SHA-256
`5a27c86d126b711ee0b3782bccec213e7d90df3b5fb2cc7dea054291e9e2ffa1`.

### Independent differential test

The reviewer-authored test imports the trusted canonical and submitted entry
point independently. It covers:

- all four prompt examples and 18 curated empty/boundary/branch cases;
- every string over representative vowel/consonant/case alphabet `aAbB` at
  lengths 0 through 8 (87,381 cases);
- 20,000 deterministic strings over all 52 English letters at lengths 0
  through 80; and
- vowel-free valid English strings of lengths 900, 950, 975, 990, 1000, 1050,
  and 1200.

There were zero mismatches in the first 107,407 cases. At lengths 1000, 1050,
and 1200, the canonical returned `""` and the submission raised
`RecursionError: maximum recursion depth exceeded while calling a Python
object`. These are valid source-contract inputs, not excluded resource or
non-English cases. This is a material real-program divergence over an
unrestricted HumanEval domain.

Evidence:
[differential script](evidence/fidelity/differential.py) and
[translation/differential log](evidence/fidelity/fidelity_checks.log).

## 3. Clean proof reconstruction

I copied source artifacts to
`/tmp/audit-work/118-get-closest-vowel/candidate-src` and used no
candidate-provided kompiled definition or cache. K reports version 7.1.293.

Fresh builds from source:

- LLVM concrete definition:
  `kompile semantic.k --backend llvm --main-module MPY --syntax-module
  MPY-SYNTAX --output-definition
  /tmp/audit-work/118-get-closest-vowel/build/concrete-kompiled --warnings
  none` — exit 0.
- Haskell proof definition:
  `kompile semantic.k --backend haskell --main-module MPY --syntax-module
  MPY-SYNTAX --output-definition
  /tmp/audit-work/118-get-closest-vowel/build/proof-kompiled --warnings none`
  — exit 0.

The fresh positive target command

`kprove spec.k --definition
/tmp/audit-work/118-get-closest-vowel/build/proof-kompiled --spec-module SPEC
--warnings none`

exited 0 and printed exactly `#Top`. This aggregate invocation checks all 13
claims in the mutually structural spec. Reviewer-added labels also allowed the
seven base claims C01-C05, C09, and C12 to be selected individually; each
printed `#Top`. Selecting inductive C06 alone removes the other constructor
case circularities and was interrupted after about 120 seconds; that altered
diagnostic is not a candidate positive target command and is not used as a
failure.

The fresh LLVM definition executed empty, length-1, length-2, the length-3
branch boundary, success and failure branches, all prompt examples, and
recursive-window cases. K agreed with both Python functions on the normal
cases. On the actual-program witness `"b"*1000`, K exited 0 and returned
`pyStr(.Chars)`; the trusted canonical returned `""`, but submitted Python
raised `RecursionError`. Thus clean reconstruction verifies the K theorem and
simultaneously confirms that the generated semantics does not model the real
program on the full intended domain.

Evidence:
[LLVM build](evidence/build/kompile-llvm.log),
[Haskell build](evidence/build/kompile-haskell.log),
[aggregate proof](evidence/build/kprove-all.log),
[individual diagnostics](evidence/build/kprove-individual.log),
[individual addendum](evidence/build/kprove-individual-addendum.log), and
[concrete comparison](evidence/build/concrete-compare.log).

## 4. Adequacy and real-program pinning

### Claim meaning and preconditions

None of the 13 claims has a `requires` or `ensures` clause. Each precondition
fixes:

- `<k>` to `invoke("get_closest_vowel", pyStr(CS)) ~> KREST`;
- `<program>` to `solutionProgram`; and
- arbitrary caller `ENV`, `STACK`, and continuation `KREST`.

The input-shape patterns partition finite `Chars` as follows:

1. C01-C03 cover lengths 0, 1, and 2 and return empty.
2. C04 covers a rightmost consonant-vowel-consonant triple and returns its
   vowel.
3. C05-C08 cover a failed window with a consonant in its middle, using base and
   predecessor shapes.
4. C09-C11 cover a failed window whose left and middle characters are vowels.
5. C12-C13 cover a failed consonant-vowel-vowel window.

The inductive destinations use `closestSpec` on the one-character-shorter
predecessor. All returned values are fixed to either the empty string, the
identified vowel, or the fully defined `closestSpec`; no free/existential
result or one-way Boolean implication weakens the postcondition.

For every claim, a complete satisfying state is obtained with
`KREST = .K`, `ENV = .Map`, and `STACK = .Frames`. Concrete input witnesses,
respectively, are:

`""`, `"b"`, `"bb"`, `"bab"`, `"bbb"`, `"bbbb"`, `"aabb"`, `"babb"`,
`"aab"`, `"aaab"`, `"baab"`, `"baa"`, and `"bbaa"`.

Instantiating each destination produced exactly the result returned by both
Python functions on those witnesses.

### Program pinning

The trusted-regenerated `.mpy` has 222 constructor tokens. The
`solutionProgram` RHS has those same 222 tokens plus four explicit `.Stmts`
empty-list units required by K's inner parser. Independent token-level
comparison succeeds, and `solutionProgram` has exactly one defining rule.
Consequently the claims syntactically pin the submitted function binding and
body rather than a hand-substituted algorithm.

### Material body sensitivity

Syntactic pinning is not sufficient because the semantics ignores a material
part of that body. In scratch I changed the actual assignment to
`vowels = ""`, regenerated `solution.mpy` with the trusted translator, and
changed `program.k` to that translated constructor. The program-term SHA-256
changed from
`e1e51be40d646b7f6528c796fcfc33b9e878234ef27c79bb06b832c65e9b0a81`
to
`793ec31590124b575912a7c51826e112c38e5dac14c5a96ea7c106d8699b4fea`.
This is therefore an executed-term mutation, not merely an external source
edit.

For valid input `"bab"`:

- mutated Python returned `""`;
- freshly rebuilt K returned `"a"`; and
- the unchanged 13 target claims still exited 0 with `#Top`.

The proof is insensitive to the assignment because the specialized membership
rule matches the textual name `vowels` and never reads its environment value.
That is a material source-operation bypass.

Evidence:
[pinning checker](evidence/static/pinning_check.py),
[witness checker](evidence/static/entry_witnesses.py),
[pinning/witness log](evidence/static/pinning-and-witnesses.log), and
[body-sensitivity log](evidence/static/body-sensitivity.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory contains 40 local syntax/configuration declaration
groups, 85 rules in `semantic.k`, one program-constructor rule, seven
`closestSpec` equations, and 13 reachability claims. There are no local
`[total]`, `[functional]`, `[simplification]`, explicit numeric-priority rules,
or opaque symbols. Four rules use `[owise]`. The inventory enumerates every
declaration and rule with line numbers, overlap/coverage/descent analysis, and
construct mapping:
[detailed rule inventory](evidence/static/rule_inventory.md) and
[raw inventory](evidence/static/raw-rule-inventory.log).

### Used-construct coverage

Every constructor in `solution.mpy` is declared: `Module`, `FuncDef`,
`Params`, statement lists, `Assign`, `If`, `Return`, `Name`, `Str`, `Int`,
`Call`, `Compare`, `CmpOp`, `UnaryOp`, `Subscript`, `Slice`, and `NoBound`.
The configuration has precisely the required control, program, environment,
and call-stack cells. Invocation installs the real extracted body and one
argument binding; call frames preserve the exact caller continuation and
environment; return discards only the current function's remaining
computation. Slice/index rules cover the used `[:-1]`, `[-1]`, `[-2]`, and
`[-3]` operations under the preceding length guard.

The `closestSpec` equations are truthful, pairwise disjoint by length and
`vow`/`con` shapes, exhaustive over `Chars`, and structurally descending. It is
a legitimate result specification rather than an execution oracle: it occurs
in claim destinations, not in the machine rules.

### Unsound task-specific operational bridge

The rules at `/candidate/semantic.k:113-125` are not a semantics of the
submitted membership expression:

`doStmt(If(Compare(L, CmpOp(OP, Name("vowels")), ...), ...))`

rewrites to `memberBranch(OP, eval(L,...),...)`. It does not evaluate
`Name("vowels")`, look it up, or guard that its binding is `vowelSet`.
`memberBranch` then decides from the task-specific `vow`/`con` tag. These rules
preempt the generic `If` rule through `[owise]`.

Concrete false-conclusion witness over valid English input `"bab"`:

1. The mechanically translated body with `vowels = ""` creates the real
   environment binding `vowels |-> pyStr(.Chars)`.
2. Python evaluates `"a" in ""` as false and returns `""`.
3. The K bridge ignores that binding, observes `vow(v_a)`, takes the true
   branch, and returns `"a"`.
4. `kprove` still proves the original `"a"` postcondition.

The full matched domain of the rule admits that state, but there is no
bridge-free universal connection theorem and no binding guard restricting it
to the one state in which its shortcut would agree with real evaluation. This
is exactly the kind of answer-encoding/body-bypassing rule that cannot be
accepted as a low-level primitive. The false behavior and exact commands are
in `evidence/static/body-sensitivity.log`.

I do not label the remaining rules unsound. Their equations are true on their
guards for the exercised subset; overlaps are disjoint or agree (notably the
special `intNat` cases agree with the positive recursive case); recursive
functions descend; and unsupported unused forms remain visibly partial.

### Missing real recursion/exception behavior

Independently of the bad membership bridge, the generated stack is unbounded
and has no recursion-depth or exception state. This is not merely absent
coverage for an unused construct: recursive self-call is the submitted
algorithm's main control flow. The actual-source witness `"b"*1000` causes
CPython `RecursionError`, while K proves and executes a normal empty-string
return. The model therefore establishes a false normal-result conclusion about
the real program on a valid intended-domain input.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created a fresh scratch mutation
in a distinct `SPEC-VACUITY` module. It changes C04's
consonant-vowel-consonant destination from the identified vowel to the empty
string. The complete satisfying witness is `"bab"` with `KREST = .K`,
`ENV = .Map`, and `STACK = .Frames`; both trusted canonical and submitted
Python return `"a"`, so the mutation is demonstrably false.

`kprove ... --dry-run` exited 0, confirming that the mutation parses and builds.
The actual proof exited 1 with `WarnStuckClaimState`. Its residual contains
`callResult(pyStr(snoc(.Chars, vow(V))))`, which cannot unify with the mutated
empty destination. This is the expected unmet result obligation, not a parser
error, timeout, unrelated crash, or unreachable mutation.

Evidence:
[preserved mutation](evidence/nonvacuity/spec-vacuity.k),
[dry-run log](evidence/nonvacuity/dry-run.log), and
[failed-proof log](evidence/nonvacuity/proof.log).

Non-vacuity therefore passes. It does not repair the real-program and semantics
failures.

## 7. Proven versus assumed accounting

### What `#Top` establishes

Under the candidate's own K theory, for every finite constructor-level
`Chars` value and arbitrary caller continuation/environment/stack, a
terminating invocation of the function body represented by `solutionProgram`
has the `callResult` described by `closestSpec`. The proof is structural,
result-constraining, and connected to the submitted translated constructor
term.

It does **not** establish that the actual submitted CPython program returns
that result for every English-letter string in the prompt's domain. In
particular it does not establish the normal result for `"b"*1000`, and it does
not establish that program membership depends on the source assignment's
value.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 toolchain/backends and imported `BOOL`, `INT`, `STRING`, `MAP` operations | compilation, all execution/proofs | Ordinary accepted verification infrastructure. |
| Trusted `/reference/py2mpy.py` | source-to-constructor identity | Accepted; fresh output is byte-identical. |
| `solutionProgram` constructor normalization via explicit empty `Stmts` units | all claims | Accepted; independently checked token-for-token. |
| Host-string length/substrings inside `litChars` | mapping English input to `Chars` | Acceptable on the stated English-letter domain; concretely exercised but also defined by transparent K equations. |
| `closestSpec` | every inductive destination | Not assumed/opaque: seven exhaustive, disjoint, descending equations and exact-execution reachability claims. |
| Specialized S16-S20 membership bridge | all three source membership tests, returned result, all non-base claims | Illegitimate. It is program-derived, result-bearing, ignores the actual RHS binding, has no universal connection theorem, and admits the recorded wrong result. |
| Unlimited K call stack / absence of `RecursionError` | recursive fallback and theorem domain | Illegitimate for a proof of the real submitted Python on the unbounded source contract; concrete actual-program counterexample recorded. |
| Differential and concrete tests | empirical source/semantics bridges only | Finite evidence, not a substitute for the K proof. They expose rather than justify the two failed bridges. |

Gate A (real-program soundness) fails because the membership bridge is
body-insensitive and unsound over its complete matched domain. Gate B (intent
adequacy) fails because the K model returns normally where the real submitted
program raises on valid, unrestricted inputs. Gate C evidence is reproducible,
but it cannot rescue either failure.

The successful reconstruction and meaningful false mutation show an honest
theorem about the candidate theory, not a legitimate partial-correctness proof
of the real generated program required by this benchmark.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
