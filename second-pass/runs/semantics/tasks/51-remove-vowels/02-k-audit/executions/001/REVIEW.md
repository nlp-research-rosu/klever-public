# Independent adversarial audit: 51-remove-vowels

The candidate contains a legitimate partial-correctness proof under the supplied
semantics. Fresh builds and proofs close; the formal result is constrained; the
submitted program term is pinned exactly; and the only proof-local execution
specialization is a true equation over its complete domain. The status is
`CONCERNS / LEGIT`, rather than an unqualified pass, because the requested
generation/provenance records are absent and the last bridge from the supplied
code-point semantics to full CPython string behavior is supported by inspection
and differential evidence, not by a formal cross-semantics theorem.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. This is consistent; there is no
infrastructure breach.

The candidate `reference-semantics/` and the trusted tree have identical
recursive entry sets, regular-file types, and bytes. There are no symlinks,
missing entries, added entries, or changed entries in the candidate semantics
tree. The recursive `diff` exited 0
([log](evidence/stage1-semantics-diff.log)); hashes are recorded
[here](evidence/stage1-trusted-hashes.log).

The candidate `/candidate/prompt.py` and `/candidate/py2mpy.py` are regular
files and byte-identical to `/reference/prompt.py` and
`/reference/py2mpy.py`; both `cmp` commands exited 0
([prompt](evidence/stage1-prompt-cmp.log),
[translator](evidence/stage1-translator-cmp.log)). No candidate artifact is a
symlink.

### Missing and extra provenance material

The following requested untrusted provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any filename indicating a structured generation trace

The complete root inventory and explicit missing results are in
[stage1-artifact-inventory.log](evidence/stage1-artifact-inventory.log).
Consequently, no generation narrative, metric, or trace could be corroborated.
This is an auditability concern, but it does not prevent independent
reconstruction from the source proof artifacts.

The candidate also contains `__pycache__/*.pyc`. Those are candidate-built
caches, not proof sources. They were not copied or used. No candidate compiled K
definition was present or reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt says `remove_vowels(text)` returns the string with vowels
removed. The trusted canonical implementation retains each input character
exactly when `character.lower()` is not one of `a,e,i,o,u`. Thus, for CPython
strings, the concrete contract is: remove the ten ASCII letters
`a,e,i,o,u,A,E,I,O,U`; preserve every other character, order, multiplicity, and
line break.

The candidate implementation initializes an accumulator, iterates left to
right, appends a character exactly when it is not in the ten-character ASCII
haystack, and returns the accumulator. The redundant initial assignment to
`char` is behaviorally harmless.

### Translation identity

The trusted translator regenerated `solution.mpy` from the scratch copy of
`solution.py`; generation exited 0, and `cmp` against the submitted
`solution.mpy` exited 0
([generation](evidence/stage2-regenerate-solution.log),
[identity](evidence/stage2-solution-mpy-cmp.log)). Both translated files have
SHA-256
`b3cf89a61dce62002983fda7137a9b82d2a85a369ed4d4a56d14ae3d2cad2534`
([hash log](evidence/stage2-artifact-hashes.log)). The independently dumped
CPython AST confirms the intended `Assign`, `For`, `If`, `Compare(NotIn)`,
`AugAssign(Add)`, and `Return` structure
([AST log](evidence/stage2-source-ast.log)).

### Independent differential testing

The reviewer-authored
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and the scratch candidate entry point as separate
modules. It tested:

- all 6 documented examples;
- 27 explicit empty, one-character, case, first/middle/last branch, whitespace,
  NUL, combining-character, and non-ASCII boundary cases;
- 5,000 seeded strings of lengths 0 through 64 from a mixed alphabet;
- every valid Unicode singleton, 1,112,064 code points.

There were zero mismatches; the exact seed, corpus digest, counts, result
digest, command, and exit 0 are in
[stage2-differential.log](evidence/stage2-differential.log). Exhaustive
singletons are particularly relevant because both Python implementations are
characterwise and order-preserving.

An additional `python -m doctest` attempt could not parse the trusted docstring:
the example containing `\n` is stored as a literal newline and violates
doctest's indentation grammar. That command exited 1 before executing any
example ([log](evidence/stage2-python-examples.log)); it is not a behavioral
divergence. The independent differential test explicitly executed all six
documented inputs.

Stage 2 passes.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/51-remove-vowels`; candidate caches were excluded. The
toolchain was K v7.1.337 with OpenJDK 17.0.19
([versions](evidence/toolchain-versions.log)).

### Concrete definition

The supplied source semantics was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The build exited 0
([log](evidence/stage3-kompile-runtime.log)). The fresh definition executed the
candidate's six translated concrete assertions; `krun` exited 0 with final
`.K`, `NoExc`, and exit code 0
([log](evidence/stage3-krun-concrete-tests.log)).

### Proof definition and positive claims

The proof definition was freshly compiled with Haskell:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

The build exited 0
([log](evidence/stage3-kompile-verification.log)). Proving the submitted
four-claim `SPEC` as a whole exited 0 and printed `#Top`
([log](evidence/stage3-kprove-all.log)).

The claims were then labeled in the reviewer-only
[spec-labeled.k](evidence/spec-labeled.k):

- the empty-loop claim closes alone with exit 0 and `#Top`
  ([log](evidence/stage3-kprove-loop-empty.log));
- the vowel-head and non-vowel-head claims are a mutually inductive pair, since
  the unknown tail can next enter either branch; selecting the pair closes with
  exit 0 and `#Top`
  ([log](evidence/stage3-kprove-loop-recursive-pair.log));
- after those three helper theorems were established, the reviewer-only
  [entry spec](evidence/spec-entry-proved-helpers.k) marks them trusted and
  targets only the entry claim; that run exits 0 and prints `#Top`
  ([log](evidence/stage3-kprove-entry-with-proved-helpers-final.log)).

An exploratory concurrent run produced a transient Java-detection error and
two interrupted sessions; it was discarded and all relied-upon runs were
serialized. The exact incident and exit statuses are documented
[here](evidence/stage3-concurrency-incident.md).

Every positive claim is therefore reconstructed: the empty case independently,
the recursive cases as their necessary mutual circularity, and the entry using
those already-proved helpers. Stage 3 passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. **Empty-loop helper.** If the remaining iterator is the empty string in a
   plain callee scope containing `text`, `result = ACC`, and `char = CHAR`, the
   loop consumes no body step, leaves the accumulator and `char` unchanged, and
   terminates normally.
2. **Vowel-head helper.** If the next code `C` is one of the ten vowel codes,
   the loop discards `C`, processes `REST`, and finishes with
   `result = removeVowelCodesAcc(ACC, REST)`. The final `char` is existential
   because it is irrelevant to the returned value.
3. **Non-vowel-head helper.** If `C` is not a vowel code, the loop appends `C`
   to `ACC`, processes `REST`, and finishes with the corresponding filtered
   accumulator. Again, only the irrelevant final `char` is existential.
4. **Entry claim.** From the exact initial module configuration and any finite
   `CODES:IntSeq`, load the submitted program, call `remove_vowels` with
   `str(CODES)`, and return exactly `str(removeVowelCodes(CODES))`. The claim
   pins module scope, builtins scope, allocation counters, heap, stack, return
   state, exception state, and exit code.

The entry result is neither free nor implied only one way: it is the explicit
right-hand side of the reachability rewrite. The helper existential
`?FINALCHAR` cannot influence the accumulator, return value, or postcondition.

### Real-program identity

The spec names a macro rather than reading `solution.mpy` at proof time, so its
identity was checked structurally. `kast --expand-macros` parsed the submitted
`solution.mpy` and independently expanded `removeVowelsProgram`. The two KAST
files are byte-identical, both with SHA-256
`8a6b7f2b315d8ad09b49d17e8cd3df484d796585fdfac72e11ba741a43cf427f`
([comparison](evidence/stage4-program-macro-cmp.log),
[hashes](evidence/stage4-program-macro-hashes.log),
[expanded terms](evidence/stage4-kast-expanded-content.log)). The `<k>` cell
therefore executes the actual submitted program term, not a substituted body.

### Satisfying states and ground substitution

All helper preconditions are satisfiable. For example, choose callee location
1, `OUTER = .Map`, `TEXT = .IntSeq`, `ACC = .IntSeq`,
`CHAR = str(.IntSeq)`, and parent 0. Use empty iteration for claim 1,
`C = 97, REST = .IntSeq` for claim 2, and
`C = 98, REST = .IntSeq` for claim 3. The entry precondition is satisfied by
the exact displayed initial configuration with, for example,
`CODES = [97,98]`.

Substitution gives `removeVowelCodes([97,98]) = [98]`, hence return `"b"`.
Reviewer ground cases `""`, `"a"`, `"b"`, and `"abEcdU"` agree among the
formal code filter and both Python implementations
([Python log](evidence/stage4-witness-python.log)). The trusted translator
produced [stage4_k_witness.mpy](evidence/stage4_k_witness.mpy), and the fresh
LLVM semantics executed all four assertions to final `.K` with exit 0
([K log](evidence/stage4-witness-krun.log)).

Stage 4 passes.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored [inventory script](evidence/k_inventory.py) records the
full multiline text and attributes of every local source declaration. The
exhaustive results are [JSON](evidence/k-inventory.json) and
[TSV](evidence/k-inventory.tsv):

- 949 declarations across 26 source files;
- 234 syntax declarations, 705 rules, 5 contexts, 1 configuration, and 4
  claims;
- 928 supplied-semantics declarations and 21 candidate-local declarations;
- 149 functions, 110 total declarations, 46 priority rules, 26 `owise`
  declarations, 35 concrete declarations, 25 symbolic/opaque declarations, 9
  macros, 3 strictness declarations, and no simplification or functional
  declarations.

The selected fixed semantics is byte-identical to the trusted supplied
baseline. Every inventoried declaration was classified; the complete
candidate-local disposition table and the execution-relevant fixed-semantics
map are in [static-review.md](evidence/static-review.md).

### Candidate-local rules

The 17 declarations in `verification.k` are:

- exact macros/equations for the ten vowel codes, loop body, function body, and
  full module;
- an unconditional total Boolean predicate for those ten codes;
- a structurally recursive, total accumulator filter with disjoint
  vowel/non-vowel guards;
- a wrapper starting that filter at the empty accumulator;
- one priority-40 specialization of fixed one-character substring membership.

The four remaining local declarations are the claims reviewed in Stage 4.
There is no local opaque symbol, simplification rule, result oracle, fabricated
return, call interception, or rule that bypasses the submitted function body.

The filter equations cover both `IntSeq` constructors, the guarded cases are
Boolean complements, and recursion strictly shortens the remaining sequence.
The macros expand to the exact submitted KAST. No overlap changes a result.

### Membership specialization

The rule

```text
strContains(iCons(C,.IntSeq), vowelCodes) => isVowelCode(C)
```

is a result-bearing pure specialization, so it was audited as a proof
extension rather than trusted because of its name or priority. It reads and
writes no cells, introduces no control effect, and its complete domain is a
one-code needle and the fixed ten-code haystack.

A separate Haskell definition was built from the supplied semantics plus only
reviewer definitions of the fixed list and predicate—without importing
`verification.k` or the specialization
([theory](evidence/bridge-audit.k),
[build log](evidence/stage5-kompile-bridge-audit.log)). An initial undivided
symbolic equality did not let the backend choose the guarded fixed-semantic
branches; its equality residual is retained
[here](evidence/stage5-kprove-bridge-connection.log). The proof was therefore
partitioned exhaustively into the ten exact vowel integers and the universal
case in which `C` differs from all ten. This bridge-free connection proof exits
0 with `#Top`
([spec](evidence/bridge-connection-exhaustive-spec.k),
[log](evidence/stage5-kprove-bridge-connection-exhaustive.log)).

Opposite interpretations were also attempted in exact ground configurations.
Code 97 reduces to `true`, so the claim that it is `false` gets stuck; code 98
reduces to `false`, so the claim that it is `true` gets stuck
([97 log](evidence/stage5-bridge-opposite-vowel-exact.log),
[98 log](evidence/stage5-bridge-opposite-consonant-exact.log)). An earlier
opposite test used unconstrained cell ellipses and wandered into an unrelated
unsupported float hook; it is preserved but not counted as validation
([discarded log](evidence/stage5-bridge-opposite-vowel.log)).

Thus the priority rule is an acceleration of the fixed result over its entire
match domain, not an oracle or smuggled correctness conclusion.

### Fixed-semantics dependency and state/control review

The submitted term uses only the supplied declarations for module loading and
statement sequencing; function definition, call, argument binding, return, and
frame pop; plain-scope name lookup and updates; string literal conversion,
iteration, concatenation, and membership; `for`, `if`, and target binding.
Their exact file/line map is in
[static-review.md](evidence/static-review.md).

Evaluation order is preserved: call callee before arguments, assignments and
`AugAssign` evaluate RHS values first, the `for` iterable is evaluated once,
comparison evaluates left then right, and `if` evaluates its guard before one
branch. Scope 1 is allocated for the call, `text` is bound there, `char` is
overwritten by target binding, `result` is updated in place, and return pops
the frame and restores the caller. The submitted program performs no heap
allocation and has no modeled exceptional branch.

The string-literal rule is ASCII-only, but every literal used by this program
is ASCII. The input is already the abstract value `str(CODES)`, so it does not
pass through the literal parser. Fresh-build non-exhaustiveness warnings affect
unused mapping, float, join, and indexing helpers.

The supplied definition imports 25 named opaque/symbolic facilities (float
operations/conversions, MD5, and sorts); all are enumerated in
[static-review.md](evidence/static-review.md). None occurs in the program,
claims, filter summary, or successful proof residuals. No opaque value can
influence this proof's branch or result.

No rule with a concrete or symbolic false-conclusion witness was found. Stage 5
passes.

## 6. Fresh non-vacuity test

The fresh mutation
[spec-vacuity.k](evidence/spec-vacuity.k) changes only the entry result from

```text
str(removeVowelCodes(CODES))
```

to

```text
str(seqConcat(removeVowelCodes(CODES), iCons(120,.IntSeq)))
```

That claims an extra trailing `"x"`. It is demonstrably false for the
satisfying empty input: the real/formal return is empty, while the mutation
requires `[120]`.

The mutated spec compiled through `kprove --dry-run` with exit 0
([log](evidence/stage6-vacuity-dry-run.log)). The real proof run exited 1 with
`WarnStuckClaimState`. Its residual contains the expected unmet equality

```text
removeVowelCodesAcc(.IntSeq, REST)
  = seqConcat(removeVowelCodesAcc(.IntSeq, REST), iCons(120,.IntSeq))
```

([proof log](evidence/stage6-vacuity-proof.log)). This is a reached,
result-constraining failure, not a parser error, missing import, timeout, or
unrelated crash. Stage 6 passes.

## 7. Proven versus assumed accounting

### What is formally proven

Under the supplied MPY semantics and its K builtins, for every finite
`CODES:IntSeq`, if execution from the exact entry configuration terminates,
loading the exact submitted `solution.mpy` term and calling
`remove_vowels(str(CODES))` returns
`str(removeVowelCodes(CODES))`. The recursive mathematical function preserves
the original order and removes exactly codes
65,69,73,79,85,97,101,105,111,117. The reachability post-state also restores
the pinned stack, return, exception, heap, allocation, and environment state.

This is partial correctness. The K theorem is not a separately stated
termination theorem, although the actual loop and the filter equations
structurally consume a finite sequence.

### Trust and assumption ledger

| Boundary | Dependence and assessment |
|---|---|
| Supplied semantics | The theorem is relative to the trusted, byte-identical supplied semantics. The used execution slice was reviewed rule by rule. This is the intended semantics boundary for `SUPPLIED_SEMANTICS`. |
| K implementation | `kompile`, Haskell `kprove`, LLVM `krun`, reachability/circularity logic, SMT discharge, and hooked Int/Bool/String/Map/List/K-equality primitives are trusted. This is the ordinary low-level proof checker boundary. |
| Proof-local membership specialization | Not assumed after audit: a bridge-free exhaustive K connection proof covers its complete domain, and opposite ground values are rejected. |
| Filter meaning | Not opaque or empirical: its total equations define the exact code-point filter, and the proved loop claims connect actual execution to it. Ordinary arithmetic facts identify the ten constants with ASCII vowels. |
| Source-to-MPY bridge | Byte identity proves the submitted MPY is what the trusted translator emits. The translator's faithfulness to CPython AST semantics is not itself a K theorem; the simple AST was independently inspected. Acceptable but informal. |
| MPY-to-CPython intent bridge | The formal input is `str(IntSeq)`, while CPython strings are Unicode sequences and the canonical implementation uses `lower()`. Agreement is supported by all examples, branch cases, 5,000 generated strings, and exhaustive valid Unicode singletons, but no universal cross-language semantics theorem is supplied. This is the main documented concern. |
| Imported opaque symbols | The 25 float/MD5/sort symbols are in the fixed imported definition but outside the proof dependency cone; they affect neither control nor result here. |
| Generation provenance | The missing run input, metrics, logs, and structured trace prevent auditing how the candidate was generated. Independent reconstruction replaces those claims for proof legitimacy, but the provenance gap remains a concern. |

Differential testing is used only to support implementation/intent and
cross-language bridges. It is not treated as the K proof and does not replace
the reachability claims or the bridge-free specialization theorem.

### Final decision

Gate A (real-program soundness and non-vacuity) passes. Gate B (intent adequacy)
is supported but retains an informal/empirical CPython-to-MPY bridge. Gate C
(auditability) is limited by absent generation records, although all reviewer
evidence is reproducible. These limitations do not permit a false theorem, do
not free the result, and do not substitute another program. They warrant
`CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
