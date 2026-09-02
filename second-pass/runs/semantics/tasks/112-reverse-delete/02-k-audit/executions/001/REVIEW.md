# Independent adversarial audit: 112-reverse-delete

## Overall decision

The reconstructed K proof is legitimate and result-constraining. It proves the
exact submitted function body under the supplied MiniPython semantics, and its
only operational bridge—the loop summary—has a separate `#Top` connection proof
against a definition that excludes the bridge. I found no rule that can enable
a false conclusion on the intended string domain.

The verdict is `CONCERNS / LEGIT`, not `PASS`, for two evidence/adequacy
limitations:

1. `run-input.json`, `metrics.json`, `codex-last.txt`,
   `codex-output.log`, and a structured generation trace are absent.
2. The final bridge from the K summary functions to the English notions
   “delete every character in `c`” and “palindrome” is a straightforward
   informal induction supported by finite differential testing, not a separate
   machine-checked K theorem. The entry claim also invokes an exact closure body
   rather than executing the top-level `Module(FuncDef(...))`; mechanical AST
   checks show that this does not substitute a different body, but it leaves
   top-level definition/name resolution outside the theorem.

All commands and statuses are recorded in
[evidence/COMMANDS.md](evidence/COMMANDS.md).

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode: `/reference/reference-semantics` exists and is a directory, so there
is no infrastructure breach.

The condition-aware integrity script
[evidence/integrity_check.py](evidence/integrity_check.py) reported:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- All required proof sources are present as regular files:
  `solution.py`, `solution.mpy`, `spec.k`, and `verification.k`.
- The candidate and trusted `reference-semantics/` trees each have 25
  recursively inventoried entries. There are no missing, additional,
  type-mismatched, content-mismatched, or symlinked entries. A separate
  `diff -r --no-dereference` also exited 0.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are missing. No `.jsonl`, `.trace`, or trace-named file is
  present.

The complete result is
[evidence/integrity-result.log](evidence/integrity-result.log). Candidate
`__pycache__` contents were treated as untrusted build residue and were not
copied into the reconstruction.

Stage 1 result: integrity of the prompt, translator, proof sources, and supplied
semantics passes; generation provenance is incomplete.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For string inputs `s` and `c`, preserve the characters of `s` whose character
does not occur anywhere in `c`, in their original order. Return a pair
containing that filtered string and a Boolean saying whether it equals its own
reverse. The three documented examples are:

- `("abcde", "ae") -> ("bcd", False)`
- `("abcdef", "b") -> ("acdef", False)`
- `("abcdedcba", "ab") -> ("cdedc", True)`

This restatement follows `/reference/prompt.py` and the trusted implementation
in `/reference/canonical.py`.

### Submitted implementation

`/candidate/solution.py` iterates left-to-right. On the retained branch it
appends the character to `result` and prepends it to `reversed_result`; it then
returns `(result, result == reversed_result)`. It covers both membership
branches and correctly leaves the accumulators unchanged for an empty input.

The trusted translator regenerated `solution.mpy` with exit 0. `cmp` exited 0,
and both files have SHA-256
`09c57fd0ede380bbe643760e1cb8402fd153ddd32dfb1d8a97b2c92c6344137e`;
see [evidence/translation-result.log](evidence/translation-result.log).

### Independent differential test

[evidence/differential_test.py](evidence/differential_test.py) independently
imports `/reference/canonical.py` and the scratch copy of `solution.py`. It
ran:

- all three documented examples;
- 13 named empty, single-character, branch-boundary, all-kept/all-deleted,
  duplicate, palindrome, non-palindrome, and Unicode cases;
- every pair with `s` of length 0–5 and `c` of length 0–3 over `{a,b,c}`
  (14,560 pairs);
- 3,000 deterministic broader cases over `abcXYZ09😀é`.

All 17,576 comparisons matched. The exact generated inputs are preserved in
[evidence/differential-inputs.json](evidence/differential-inputs.json), and the
summary with zero mismatches is in
[evidence/differential-result.log](evidence/differential-result.log).

Stage 2 result: pass. No material implementation/canonical divergence was
found.

## 3. Clean proof reconstruction

I copied source artifacts only to
`/tmp/audit-work/review-112/reconstruction`. The semantics in that directory
came from the trusted `/reference/reference-semantics`, not a candidate cache.
No candidate-compiled definition was copied or used.

### Concrete definition

The LLVM definition was freshly built from `semantics.k` using
`MPY-KRUN`/`MPY-SYNTAX`; `kompile` exited 0. A reviewer-authored harness whose
first nine lines were byte-compared to the submitted `solution.py` was
translated with the trusted translator and executed. `krun` exited 0 with
`<k> .K </k>`, `NoExc`, and exit code 0 after all normal and boundary
assertions. Evidence:

- [evidence/concrete_harness.py](evidence/concrete_harness.py)
- [evidence/runtime-kompile.log](evidence/runtime-kompile.log)
- [evidence/concrete-krun.log](evidence/concrete-krun.log)

Compiler warnings concern non-exhaustive total functions or unused variables in
unrelated supplied-semantics features; no warned symbol is in the proof
dependency described in Stage 5.

### Proof definitions and every positive target

| Reconstruction | Claim | Exit | Result |
|---|---|---:|---|
| `MPY-VERIFICATION` Haskell definition | `LOOP-SPEC` | 0 | `#Top` |
| `MPY-VERIFICATION` Haskell definition | `SPEC` | 0 | `#Top` |
| `MPY-VERIFICATION-BASE` Haskell definition, excluding the summary bridge | `LOOP-SPEC` | 0 | `#Top` |

The first definition build is in
[evidence/verification-kompile.log](evidence/verification-kompile.log), and
the positive runs are in
[evidence/loop-proof-full-definition.log](evidence/loop-proof-full-definition.log)
and [evidence/entry-proof.log](evidence/entry-proof.log).

The candidate script compiles the installed loop-summary rule before proving
`LOOP-SPEC`, which by itself would be weak evidence against circular
self-justification. I therefore built `MPY-VERIFICATION-BASE`, which contains
the helper equations but not the operational summary rule, and reproved the
loop claim there. Both the build and proof exited 0, and the proof printed
`#Top`; see
[evidence/verification-base-kompile.log](evidence/verification-base-kompile.log)
and
[evidence/loop-proof-base-definition.log](evidence/loop-proof-base-definition.log).
This independently establishes the connection required before installing the
summary as a rule.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`LOOP-SPEC` has no `requires` clause. Its precondition is:

- `<k>` begins with the exact evaluated `#loop` corresponding to the submitted
  `for character in s` and its exact `if` body; an arbitrary continuation is
  framed.
- The current environment is an arbitrary location `L`.
- The scope at `L` contains exactly the five relevant bindings:
  `s = str(ORIG)`, `c = str(C)`, `result = str(A)`,
  `reversed_result = str(RA)`, and `character = V`, with arbitrary parent `P`.
- All unmentioned cells and other scope entries are framed.

Its postcondition consumes the loop, preserves `s`, `c`, the parent, the
continuation, and all framed cells, and changes only:

- `result` to `str(keptAcc(S,C,A))`;
- `reversed_result` to `str(reversedKeptAcc(S,C,RA))`;
- `character` to `lastCharacter(S,V)`.

`SPEC` also has no `requires` clause. `S` and `C` range over arbitrary
`IntSeq`s, and the precondition directly calls a closure with the exact
two-parameter submitted body and definition environment 0. The machine cells
are pinned to the initial module state: environment 0, scopes 0 and -1,
fresh-scope location 1, empty heap/stack, `noRet`, `NoExc`, and exit code 0.

The postcondition is not free or implication-only. It fixes the returned value
to the exact two-element tuple:

```text
(str(keptAcc(S,C,.IntSeq)),
 keptAcc(S,C,.IntSeq) ==K reversedKeptAcc(S,C,.IntSeq))
```

and pins the remaining machine cells to the restored initial state.

### Pinning to the submitted AST

[evidence/pinning_check.py](evidence/pinning_check.py) mechanically normalizes
the harmless pretty-print difference between an elided empty statement-list
terminator and `.Stmts`. It verifies all of the following:

- the complete body extracted from submitted `solution.mpy` occurs in the
  entry claim's closure call;
- the complete `For` term occurs in that entry body;
- after the real semantics has evaluated the iterable, the exact corresponding
  `#loop(str(S), target, body)` occurs in both `LOOP-SPEC` and the installed
  bridge.

All checks exited 0; see
[evidence/pinning-result.log](evidence/pinning-result.log). Thus the direct
closure invocation does not replace the submitted function with another
algorithm. It excludes only top-level execution of the otherwise side-effect
free `Module(FuncDef(...))`.

### Satisfiable states and ground substitution

The entry precondition is satisfied, for example, by:

```text
S = [97,98,99,100,101]     ("abcde")
C = [97,101]               ("ae")
```

The formal target reduces to `("bcd", false)`, equal to both trusted canonical
Python and generated Python. Two additional witnesses reduce as follows:

| `s`, `c` | Formal target | Canonical | Generated |
|---|---|---|---|
| `""`, `""` | `("", true)` | `("", true)` | `("", true)` |
| `"abcdedcba"`, `"ab"` | `("cdedc", true)` | `("cdedc", true)` | `("cdedc", true)` |

A ground loop precondition witness is `L=1`, `ORIG=S="a"`, `C=A=RA=""`,
`V=str("")`, and `P=parent(0)`. Its target has both accumulators equal to
`"a"` and the loop target bound to `"a"`. The executable substitutions are in
[evidence/satisfying_witnesses.py](evidence/satisfying_witnesses.py) and
[evidence/satisfying-witnesses.log](evidence/satisfying-witnesses.log).

Stage 4 result: pass, with the documented direct-closure scope limitation.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[evidence/k_rule_inventory.py](evidence/k_rule_inventory.py) inventories every
statement beginning with `configuration`, `syntax`, `context`, `rule`, or
`claim` across the supplied semantics, `verification.k`, and `spec.k`. Its 942
records exactly equal an independent count of those source statement starts:

| Class | Count |
|---|---:|
| Syntax declarations, including function/total/functional attributes | 230 |
| Ordinary rules | 654 |
| Simplification rules | 4 |
| Priority rules | 46 |
| Evaluation contexts | 5 |
| Configuration | 1 |
| Reachability claims | 2 |

The full untruncated source, attributes, line spans, opacity flags, and file
hashes are in [evidence/k-inventory.json](evidence/k-inventory.json); a readable
table is in [evidence/k-inventory.md](evidence/k-inventory.md).

Every record has an explicit audit disposition in
[evidence/k-inventory-assessed.json](evidence/k-inventory-assessed.json) and
[evidence/k-inventory-assessed.md](evidence/k-inventory-assessed.md):

- 12 candidate proof-extension entries;
- 2 candidate claims;
- 99 reached fixed-semantics rules and 57 reached declarations;
- 596 fixed rules and 176 declarations whose redex/construct/value sort is
  unreachable from the exact claim.

The unreached rules remain byte-identical trusted supplied semantics. They do
not contribute to proof closure; in particular, rules for floats, lists,
dictionaries, sets, ranges, slicing, comprehensions, sorting, methods,
builtins, assertions, and concrete-only keyed sorting cannot match a reached
redex in this string-only closure.

### Construct-to-semantics map

| Submitted construct | Declaration/execution path |
|---|---|
| `Call(closureVal(...), str(S), str(C))` | `syntax.k`, `core.k` argument evaluation, `call.k` closure dispatch, `functions.k` binding/frame/pop |
| `Name`, `Assign`, `AugAssign` | `core.k` scope lookup, `controls.k` scope updates |
| `Str("")`, string iteration and concatenation | `str.k` literal, `#iterNext`, `seqConcat`, `applyBin("+",...)` |
| `For`, `If` | `controls.k` `#loop/#loopStep`, target binding through `tuple.k`, `#branch/truthy` |
| `not in`, `==`, `BinOp` | comparison contexts in `operators.k`, `strContains/strPrefix` and string equality in `str.k` |
| `Return(TupleExpr(...))` | `tuple.k` left-to-right element evaluation, `functions.k` return/pop |

The supplied configuration has the cells used by the entry claim. Argument and
tuple evaluation are left-to-right. Closure dispatch allocates a fresh scope at
1, binds `s` and `c`, executes the body, records the return, restores the caller
environment, removes the callee scope, and resets the return cell. The loop
evaluates `s` once, iterates its finite sequence left-to-right, binds the target
before the body, and preserves the continuation. No heap allocation, exception,
output, or external state is reachable in this program.

### Candidate-local equations

All candidate-local functions are structural and result-bearing, but none is
opaque:

- `keptAcc([], C, A) = A`.
- On `X :: XS`, if the singleton `X` occurs in `C`, `keptAcc` drops `X`;
  otherwise it recurses with `A ++ [X]`.
- `reversedKeptAcc([], C, A) = A`.
- On `X :: XS`, it drops a member and otherwise recurses with `X :: A`.
- `lastCharacter([], V) = V`; on `X :: XS`, it recurses with the singleton
  string for `X`.

For each accumulator, the base/constructor patterns are disjoint. On the
constructor pattern, `strContains(singleton(X),C)` and its Boolean negation are
disjoint and exhaustive because `strContains` is total. Each recursive call is
on `XS`, so the total declarations terminate. `lastCharacter` has one base and
one constructor rule and likewise terminates. The four simplification
attributes expose these true equations to the prover; they introduce no extra
case or overlap.

### Operational loop bridge

The priority-40 rule in `/candidate/verification.k:44` is an operational bridge,
not merely a name for a value. Its complete match is narrow:

- exact evaluated iterable `str(S)`, target, condition, two body statements,
  and empty else;
- exact current scope with the five named bindings and arbitrary parent;
- arbitrary but preserved continuation and all omitted cells.

It updates only `result`, `reversed_result`, and `character`. It preserves the
input bindings, parent, heap, stack, return/exception state, allocation
counters, and the entire continuation. Its priority only selects the already
justified transition over ordinary loop unrolling.

The bridge-free universal connection theorem is `LOOP-SPEC` checked against
`MPY-VERIFICATION-BASE`; that compiled module does not contain the bridge. The
theorem accepts the same arbitrary continuation and omitted cells as the rule,
so the match domain is contained in the justification domain.

I also put an observable `after = "z"` assignment immediately after the loop.
Both base and bridge-enabled definitions proved that the assignment is
preserved (`#Top`, exit 0):
[evidence/bridge-context-spec.k](evidence/bridge-context-spec.k),
[evidence/bridge-context-base.log](evidence/bridge-context-base.log), and
[evidence/bridge-context-full.log](evidence/bridge-context-full.log).

Finally, I changed the submitted body to append rather than prepend when
building `reversed_result`, without changing the claimed summary. The bridge no
longer matched, and `kprove` exited 1 with `WarnStuckClaimState`; its residual
exhibits two retained distinct characters and an actual `true` result where the
unchanged palindrome summary differs. This is a concrete false-conclusion
witness for the mutated body and confirms body sensitivity:
[evidence/body-sensitivity-spec.k](evidence/body-sensitivity-spec.k) and
[evidence/body-sensitivity-proof.log](evidence/body-sensitivity-proof.log).

### Opaque and priority audit

The inventory found 22 supplied `no-evaluators` symbols:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
`divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`,
and `sortKeyVS`. None occurs in the submitted AST, helper equations, entry
postcondition, or reached semantics dependency. Therefore none can influence a
branch, control effect, state, or returned value in this proof.

The remaining priority rules in supplied semantics are either reached
cell/heap alternatives whose guards are false in the exact plain frame, or are
unreachable construct-specific rules. The one candidate priority rule is the
independently derived loop bridge above. No overlap yielded conflicting
right-hand sides on a satisfiable reached state.

Stage 5 result: pass. No unsound candidate rule and hence no required
false-conclusion witness for an accepted rule was found.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I created a fresh mutation,
[evidence/spec-vacuity.k](evidence/spec-vacuity.k), that leaves the entire
executed closure body unchanged and negates only the returned Boolean in the
postcondition.

The mutation is demonstrably false on the satisfying entry state `S=C=[]`: the
program and original claim return `("", true)`, while the mutation requires
`("", false)`.

`kprove --dry-run` exited 0 and produced KORE, proving that the mutation parsed
and built; its size/hash and status are in
[evidence/vacuity-dry-run.log](evidence/vacuity-dry-run.log). The real proof
then exited 1 with `WarnStuckClaimState`, not a parser error, import failure,
timeout, or unrelated crash. The residual explicitly compares the actual
summary equality with its negation:
[evidence/vacuity-proof.log](evidence/vacuity-proof.log).

Stage 6 result: pass. The positive theorem discriminates a meaningful false
result obligation.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the supplied MPY definition plus the truthful helper equations and the
independently derived loop bridge, for every `S,C : IntSeq`, a call to the exact
submitted closure body from the pinned initial state reaches:

```text
tuple(
  str(keptAcc(S,C,[])),
  keptAcc(S,C,[]) == reversedKeptAcc(S,C,[]))
```

with the caller environment, scopes, allocation counters, heap, stack, return,
exception, and exit-code cells restored as specified. This is a
partial-correctness reachability theorem; it is not a claim about inputs of
types other than strings.

The proof also machine-checks the universal loop execution summary, including
arbitrary initial accumulators, previous target value, parent, framed state,
and continuation.

### Trusted or informal boundaries

| Boundary | Influence | Status |
|---|---|---|
| K v7.1.337 parser, compiler, Haskell/LLVM backends, and builtin theories (`Int`, `Bool`, `String`, `Map`, `List`, `K-EQUAL`) | All machine-checking | Necessary low-level toolchain trust. Fresh builds and independent negative residuals reduce, but cannot eliminate, this trust. |
| `/reference/reference-semantics` | Execution, control, scopes, string operations | Authorized fixed supplied semantics; candidate copy is recursively exact. The audit still reviewed every reached rule and all candidate extensions. |
| Trusted `py2mpy.py` | Python-to-MPY bridge | Authorized trusted input. Regeneration is byte-identical; translator correctness itself is not proved in K. |
| Direct closure invocation versus top-level `Module(FuncDef(...))` | Function binding only | The exact params/body/environment are mechanically pinned. Top-level definition/name lookup is excluded; harmless for this module, which contains only that definition, but documented. |
| `keptAcc` meaning “delete characters in `c`” | First returned component | Informal structural induction: each head is dropped exactly on singleton membership, otherwise appended. Supported by 17,576 differential cases, not replaced by them. |
| `reversedKeptAcc(S,C,[]) = reverse(keptAcc(S,C,[]))` | Palindrome Boolean | Informal structural induction over `S`; not a separate K lemma. The equality therefore matches the English palindrome predicate conditionally on that ordinary mathematical bridge. Differential evidence is finite only. |
| Python canonical implementation | Intent comparison | Trusted executable oracle for tests, not part of the K theorem. |
| Missing generation provenance | Auditability, not theorem closure | Concern: the candidate's generation record cannot be independently correlated with its final source artifacts. |

There is no result-bearing opaque primitive in the proof dependency. The 22
opaque symbols listed in Stage 5 are unreachable. There is no empirical oracle
inside `verification.k`, no rule encoding a concrete task answer, no body
bypass lacking a connection theorem, and no free postcondition variable.

The formal `IntSeq` input domain is broader than valid Unicode code points, but
the operations are sound sequence operations there and include the intended
Python-string domain. The supplied literal conversion is ASCII-limited; the
submitted body uses only the empty literal, while symbolic inputs enter
directly as `str(S)` and `str(C)`, so that limitation does not exclude intended
input strings.

Stage 7 result: the formal proof is sound and pins the real generated function.
The missing provenance and informal summary-to-English bridge warrant concerns
but do not enable a false conclusion or make the proof illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
