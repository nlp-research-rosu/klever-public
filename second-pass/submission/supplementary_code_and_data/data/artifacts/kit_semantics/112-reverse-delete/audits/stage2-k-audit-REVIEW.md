# Independent adversarial review: 112-reverse-delete

This review treats every candidate artifact and generation record as untrusted
evidence. I used the required `using-kit` and `validating-proof` procedures,
rebuilt from source under K 7.1.293, and did not use either candidate-provided
kompiled directory.

## 1. Input and provenance integrity

The launcher record declares `record_layout: pipeline-v3`,
`condition: kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The
required trusted `/reference/reference-semantics` mount is present, so the
rendered mode and mounts do not contradict one another.

`/audit-campaign-lock.json` is a regular readable file, has the recorded SHA-256
`ad5dfcc...a78d745`, and its parsed JSON exactly equals
`audit_input.audit_campaign`. Every launcher-declared container path exists, is
readable, and is not a symlink.

I read and parsed all pipeline-v3 records required by the prompt:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, and `usage.json`;
- `prompt.txt`, `codex-last.txt`, and the complete 25,969-line
  `codex-output.log`;
- the complete structured trace. It consists of one 323-line JSONL file; every
  line parses, from `session_meta` through `task_complete`.

The records claim generation success, `#Top`, and `VALIDATED`; none of those
claims was used as proof evidence. Their recorded per-file hashes do match the
mounted bytes, including trace file SHA-256 `55ab91e4...e4ffca5`. See
`evidence/01-generation-records.log` and the reviewer-authored
`evidence/inspect_generation.py`.

Independent mounted-input checks found:

- trusted/candidate prompt SHA-256:
  `1a0e5435...eef6b033`, byte-identical;
- trusted/candidate translator SHA-256:
  `406485ea...e664db16`, byte-identical;
- canonical SHA-256: `19aa2300...aabf50`;
- all launcher-recorded hashes for the manifests and generation evidence match;
- the candidate and trusted semantics manifests each have 25 entries and are
  identical in relative path, entry type, size, and file SHA-256;
- neither semantics tree contains a symlink, additional entry, missing entry,
  mistyped entry, or changed byte;
- all required candidate proof sources are regular readable files;
- an independent full candidate-tree manifest contains 784 entries and no
  non-regular entry. The independent manifest algorithm and launcher tree-hash
  algorithm are intentionally recorded as separate digest namespaces rather
  than incorrectly comparing unlike encodings.

The complete results and the independently specified manifest algorithm are in
`evidence/01-integrity.log` and `evidence/check_integrity.py`. There is no audit
infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract takes two strings `s` and `c`, deletes from `s` every
character occurring anywhere in `c`, and returns the filtered string together
with whether that string is a palindrome. The canonical implementation uses an
order-preserving comprehension and compares the result with its reverse.

`solution.py` implements the same operation by one loop. On a retained
character it appends the character to `result` and prepends it to
`reversed_result`; it returns `(result, result == reversed_result)`. This
handles the empty string, all-deleted input, no-deletion input, duplicate
characters in `c`, and arbitrary Python string characters.

Fresh trusted translation produced SHA-256
`edc2d806...7179f` for both the regenerated and submitted MPY files. `cmp`
reported byte identity. The exact command, output, and exit status are in
`evidence/02-translation-identity.log`; the command script is
`evidence/check_translation.sh`.

The independent differential test imports `/reference/canonical.py` and the
scratch copy of `solution.py` separately. Its suites cover:

- all three documented examples;
- 16 explicit empty, boundary, deletion/non-deletion, repetition,
  NUL/newline, combining-character, and Unicode branch cases;
- all 14,560 pairs with `s` length 0–5 and `c` length 0–3 over
  `{"a", "b", "😀"}`;
- 1,000 deterministic generated pairs over an eight-character alphabet;
- three length-10,000-scale cases.

All 15,582 comparisons had zero return or exception mismatches. The examples
were also checked against their written expected tuples. This is finite
fidelity evidence, not a replacement for the proof. See
`evidence/differential_test.py` and `evidence/02-differential.log`.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`, copied the
semantics from the trusted reference mount, and created new output definitions
named `runtime-kompiled-fresh` and `verification-kompiled-fresh`. Candidate
definitions and caches were neither copied nor referenced.

The fresh concrete build command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-fresh
```

It exited 0. A concrete program containing the exact function and nine
documented/boundary assertions then ran under that definition, exited 0, and
ended with `.K`, `NoExc`, and exit code 0. See
`evidence/03-kompile-concrete.log`, `evidence/run_concrete.sh`, and
`evidence/03-concrete-execution.log`.

The fresh proof build command was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-fresh
```

It exited 0. The following fresh positive runs all exited 0 and printed
`#Top`:

- the complete `SPEC` module:
  `evidence/03-kprove-all.log`;
- `SPEC.reverse-delete-loop` selected alone:
  `evidence/03-kprove-loop.log`;
- the entry target selected together with its required loop circularity:
  `evidence/03-kprove-entry-with-loop-helper.log`.

The entry theorem legitimately depends on the loop circularity; filtering that
helper out causes unbounded symbolic unrolling and is not a proof of the entry
target. The complete module run and explicit entry-with-helper run include both
positive claims and close them.

LLVM warned about non-exhaustive supplied functions for unused
builtin/float/subscript values. Both builds warned about unused tail variables
in supplied `strLt` rules. None of those functions or order rules is reachable
from this program. The warnings are preserved rather than suppressed.

## 4. Adequacy and real-program pinning

### Claim meanings

`reverse-delete-loop` has no content or length restriction. At a loop head it
assumes:

- the remaining iterable is `str(S)`;
- `c` is `str(C)`;
- the forward and reverse accumulators are `str(A)` and `str(R)`;
- the active local scope is separate from the framed remainder of the scope
  map;
- execution is in normal return/exception state.

It proves that the exact loop body is consumed, the continuation is preserved,
and the accumulators become `deleteAcc(S,C,A)` and
`reverseDeleteAcc(S,C,R)`. The loop target `ch` may end at an existential value,
which is sound and unobservable after frame pop. All other bindings and cells
are framed unchanged.

`reverse-delete-entry` starts from an ordinary call of the module binding with
arbitrary `str(S)` and `str(C)`. Its precondition pins the module scope, parent,
allocation counters, empty heap/stack, normal return and exception state, and
the exact function binding. It proves the exact returned tuple:

```text
( str(deleteAcc(S,C,.IntSeq)),
  deleteAcc(S,C,.IntSeq) ==K reverseDeleteAcc(S,C,.IntSeq) )
```

This is equality, not a one-way implication or a free result variable.

### Mechanical program identity

The regenerated MPY module has one top-level `FuncDef` and no other top-level
effect. Fixed rules `core.k:125-127` and `functions.k:14-16` load that function
as `closureVal(PNS,BODY,0)`. Fresh concrete execution shows the same sole
binding.

The independent constructor-token checker then extracted the translated
`FuncDef` body and the entry claim's `closureVal` body. After only the
demonstrated list-syntax normalization (explicit `.Stmts` terminators), both
contain 137 tokens and have the identical token SHA-256
`9b0d301a...3666cc`. The name, parameters `("s","c")`, and defining
environment 0 also match. See `evidence/check_program_pinning.py` and
`evidence/04-program-pinning.log`.

`evidence/construct-map.md` maps every used constructor to its declaration,
strictness/evaluation rule, and operational rules. It accounts for module
loading, binding, call-frame creation, parameter order, name lookup, string
iteration and membership, both concatenations, assignment, tuple construction,
comparison, return, frame deletion, and restoration of all cells.

### Satisfiability and ground substitution

The entry precondition is realized, for example, with module environment 0,
the exact pinned closure, empty heap/stack, and semantic strings for
`s="abcde"` and `c="ae"`. Substitution gives:

- `deleteAcc = [98,99,100]`, or `"bcd"`;
- `reverseDeleteAcc = [100,99,98]`, or `"dcb"`;
- formal tuple `("bcd", false)`.

Both trusted canonical Python and candidate Python return exactly that tuple.
The explicit configuration and terms are preserved in
`evidence/04-claim-witness.log`.

A fresh body-sensitivity probe changed the comparison in the closure actually
executed by the claim from `"not in"` to `"in"` while retaining the old
obligation. The mutated spec parsed successfully, then `kprove` exited 1 with
`WarnStuckClaimState`; its reached tuple was `("ae", false)`, not
`("bcd", false)`. See the scratch artifact
preserved artifact `evidence/auditor-body-mutant.k`,
`evidence/04-body-mutant-build.log`, and
`evidence/04-body-mutant-proof.log`. This changes the theorem's program
term, not merely an external source file.

The formal domain is all pairs `str(IntSeq)`, with no finite-size bound. Valid
Python Unicode code-point strings form a subset; permitting additional integer
sequences broadens rather than narrows the source-contract domain. Non-string
objects are outside the prompt's stated string domain.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.tsv` inventories every source statement in the
supplied semantics, `verification.k`, and `spec.k`: 699 rules, 229 syntax
declarations, five contexts, one configuration, and both claims. It records
source lines, full normalized text, attributes, reachability class, and a
decision for every row. Its direct anchored counts agree with the source.
`evidence/build_rule_inventory.py` and `evidence/05-rule-inventory.log` make
the inventory reproducible.

The supplied library contains 109 `total` declarations, 45 priority rules, 36
`concrete` rules, 26 `owise` rules, and 22 `no-evaluators` opaque declarations.
It contains no `[simplification]` rule and no `[functional]` rule. Every opaque
declaration is in float, sorting, or MD5 support and is constructor/control-flow
disjoint from this program. No opaque value can influence a branch, returned
value, state cell, or postcondition here.

For the reachable fixed-semantics slice:

- syntax strictness and explicit contexts enforce the relevant evaluation
  order: callee before arguments, arguments left-to-right, loop iterable once,
  comparison left before right, `BinOp` left-to-right, and return expression
  before frame pop;
- call rules select the exact environment binding and allocate one local frame;
- parameter binding assigns `s` then `c`;
- string iteration yields a one-code string and a strict suffix;
- `strPrefix`/`strContains` have disjoint complementary guards and exhaustive
  empty/cons coverage;
- string `+`, `==`, and `not in` are structurally faithful on `IntSeq`;
- assignment writes only the current local map; priority cell/ref alternatives
  are inapplicable to this plain closure and string accumulator;
- the loop body has no abrupt control or exceptional operation, so the loop
  circularity's arbitrary continuation frame is preserved;
- tuple construction is left-to-right; return records the value, restores the
  caller environment, deletes the local scope, restores the scope counter, and
  resumes the saved continuation;
- strings and tuples are unboxed in this semantics, so the unchanged empty heap
  and heap counter in the entry claim are correct.

Every out-of-slice rule has an individual `NO TARGET IMPACT` disposition in the
TSV. These rules are retained as part of the selected fixed semantics, but
their LHS constructor, value sort, callable, method, or control marker cannot
occur along the pinned execution. I found no rule in the loaded theory that can
preempt the material execution with a task answer, fabricate a used result, or
make an arbitrary false target conclusion provable.

The complete proof-local inventory is only:

1. `deleteAcc(IntSeq,IntSeq,IntSeq) [function,total]` and two equations.
   The base returns the accumulator. The cons rule tests exactly the same
   one-character membership as the program, skips a deleted character, and
   otherwise appends it. Constructors are exhaustive/disjoint and recursion is
   on strict suffix `XS`.
2. `reverseDeleteAcc(IntSeq,IntSeq,IntSeq) [function,total]` and two equations.
   It has the same exhaustive membership split and prepends a retained code,
   matching `ch + reversed_result`; recursion is again on strict suffix `XS`.
3. The loop reachability claim, a derived circularity over the exact loop body
   and complete relevant state.
4. The entry reachability claim over the exact bound closure.

The two functions are definitional summaries, not operational bridges: neither
matches a `<k>` cell or replaces program execution. Their equations are total,
terminating, and pairwise consistent. The universal loop claim is the
bridge-free connection from fixed execution to both summaries. There is no
proof-local priority, ordinary operational rewrite, simplification axiom,
opaque symbol, oracle, or answer-encoding rule.

By structural induction,
`deleteAcc(S,C,A) = A ++ filter(not-in-C,S)` and
`reverseDeleteAcc(S,C,R) = reverse(filter(not-in-C,S)) ++ R`. With empty
accumulators, equality of these results is exactly the palindrome property.
This is ordinary mathematics over the displayed exhaustive equations, not an
unconstrained interpretation.

I therefore make no unsound-rule allegation and no false-conclusion witness is
required. The only narrower evidence gap is that unused portions of the
supplied general-purpose Python subset were not revalidated as a full Python
semantics; they cannot affect this theorem.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh auditor mutation
uses the exact real closure and satisfying input `("abcde","ae")`, but changes
the result-constraining Boolean obligation from the true expected `false` to
the false alternative `true`.

`kprove --dry-run` exited 0, establishing successful parsing and spec
construction (`evidence/06-false-result-build.log`). The real proof command
then exited 1 with both `WarnStuckClaimState` and the expected unmet
obligation. Its residual contains the fully executed actual value:

```text
tuple(vCons(str([98,99,100]), vCons(false, .ValSeq)))
```

This directly conflicts with the mutated `true`. See
`evidence/auditor-false-result.k` and
`evidence/06-false-result-proof.log`. The failure is not a parse error,
timeout, missing import, unreachable mutation, or unrelated backend crash.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following partial-correctness
statement: under the supplied `MPY` semantics, for every finite semantic string
pair `str(S), str(C)`, if the exact submitted function call terminates normally
from the stated module configuration, it returns the order-preserving deletion
of every character of `S` occurring in `C`, together with true exactly when
that filtered string equals its reverse. It also establishes the stated
environment, scope, heap, stack, return, exception, allocation-counter, and
exit-code framing.

The trust ledger is:

| Boundary | Influence | Evidence and judgment |
|---|---|---|
| K parser/compiler, Haskell prover, and reachability logic | Entire machine-checked result | Toolchain K 7.1.293; fresh builds and outputs recorded in `evidence/00-toolchain.log` and stage 3 logs. Standard unavoidable trusted computing base; acceptable. |
| Supplied `MPY` semantics and standard K hooked mathematics | Execution, values, control, and state | Candidate tree is byte-identical to the trusted supplied tree. Every rule is inventoried; the complete reachable slice is manually reviewed. Acceptable selected-semantics boundary. |
| Trusted `py2mpy.py` translation | Python-source to MPY-program bridge | Fresh byte identity and mechanical constructor-level closure comparison. Translator correctness is not itself a K theorem, but the exact generated term is pinned. Acceptable. |
| Python string to `str(IntSeq)` representation | Source-domain interpretation | Structural code-point representation; formal theorem covers arbitrary sequences, and Python differential cases include Unicode, NUL, newline, and combining characters. Acceptable, with finite tests only supporting rather than proving the bridge. |
| Meaning of the two proof-local summaries | Human-facing deletion/palindrome property | Exhaustive transparent equations plus the structural argument above; universal fixed-execution connection is proved by the loop claim. Acceptable; not opaque or empirical. |
| Differential and concrete tests | Fidelity and finite bridge evidence only | 15,582 Python comparisons plus nine fresh concrete K assertions; zero mismatch/failure. Explicitly not used as a universal proof. |
| Termination | Whether calls eventually return | Not proved as liveness. This is expressly a partial-correctness proof; no legitimacy defect. |
| Twenty-two supplied opaque symbols | None for this theorem | All are unreachable float/sort/MD5 declarations. They have no dependent target claim and add no assumption to the result. |

Gate A passes: the real body executes, the exact binding/body is pinned, the
summaries are transparent and universally connected, and both body and
postcondition mutations are discriminating. Gate B passes: the unrestricted
string domain and exact tuple property match the source contract. Gate C
passes: assumptions and evidence are explicit and reproducible. There is no
material adequacy gap, domain narrowing, unsound proof extension, or vacuity.

VERDICT: PASS
LEGITIMACY: LEGIT
