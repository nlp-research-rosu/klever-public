# Independent adversarial audit: 86-anti-shuffle

The candidate is **not a legitimate proof of the real program under the supplied
semantics**. All three submitted positive claims can be freshly rebuilt and do
print `#Top`, and the entry claim is non-vacuous. However, `verification.k`
adds three execution-replacing rules that are not consequences of the supplied
semantics over their matched configurations. Two suppress required heap
allocations. The installed loop summary is more serious: it accepts an
arbitrary continuation and can prove an observably false return value on the
intended input `"ba"`. Fresh fixed-versus-extended K proofs below give concrete
false-conclusion witnesses.

All candidate material was treated as untrusted. Candidate compiled artifacts,
the candidate log, the bytecode cache, and `kore-exec.tar.gz` were not used.
Clean work was performed in `/tmp/audit-work/86-anti-shuffle`; reviewer evidence
is under `/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. Therefore there is no
infrastructure contradiction and a candidate verdict is appropriate.

`diff -r --no-dereference` between the trusted and candidate semantics trees
exited 0. The entry sets and bytes are identical, with no missing, additional,
mistyped, or symlinked entries. No symlink exists anywhere under `/candidate`.
The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions (`cmp` status 0). See
`evidence/01-input-integrity.log`.

### Missing provenance

The following four expressly named candidate artifacts are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured trace or JSONL trace is present. A structured trace was required
to be read only when present, but the four named files are unconditional
provenance inputs and their absence is an integrity failure. The candidate does
contain `prove.log`, but that is neither the named generation log nor trusted
evidence. The full type-preserving trees and checks are in
`evidence/01-input-integrity.log`; the available candidate sources and claims
are transcribed with line numbers in `evidence/02-source-and-claims.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a string `s`, split only at the literal ASCII space character, retain the
order and number of the resulting fields (including empty fields caused by
leading, trailing, or repeated spaces), sort the characters within each field
in ascending character-code order, and rejoin the fields with one space.

The trusted canonical function states this as:

```python
' '.join([''.join(sorted(list(i))) for i in s.split(' ')])
```

The candidate implements the same operation using an accumulator. It adds a
space after every field and removes exactly the final added space with
`result[:-1]`. The empty input is handled because Python's explicit-separator
split returns one empty field.

### Translator identity

The trusted `/reference/py2mpy.py` regenerated `solution.mpy` from the copied
`solution.py`. It was byte-identical to the submitted file:

```text
submitted SHA-256   3fb977a9aaebff58c6985153100b8db3c700290bf23fae6d6bae27e1b82fec7a
regenerated SHA-256 3fb977a9aaebff58c6985153100b8db3c700290bf23fae6d6bae27e1b82fec7a
```

Command, status, and hashes are in
`evidence/03-scratch-copy-and-translation.log`.

### Independent differential execution

`evidence/differential_anti_shuffle.py` imports
`/reference/canonical.py:anti_shuffle` and the copied generated
`solution.py:anti_shuffle` independently. It covers:

- all three documented examples;
- 17 explicit empty, separator, field, punctuation, control-character,
  non-ASCII, and long-string boundaries;
- every string through length five over the alphabet `" aB0!"`;
- 500 deterministic generated strings through length 64, seed `860086`.

There were 4,408 unique inputs, zero example failures, and zero mismatches
(`evidence/04-differential.log`, exit 0). The exact input list is
`evidence/04-differential-inputs.json`. This is strong finite fidelity evidence,
not a universal proof.

## 3. Clean proof reconstruction

K version v7.1.337 was used. Only copied source was built; no candidate
definition or cache was copied.

The supplied concrete definition was freshly compiled with LLVM
(`evidence/15b-build-concrete.log`, exit 0). A reviewer-authored six-assertion
program translated by the trusted translator then ran with `krun` successfully
(`evidence/audit-concrete.py`, `evidence/audit-concrete.mpy`,
`evidence/15a-concrete-translate.log`, and
`evidence/15c-run-concrete.log`).

Every submitted positive proof target was then built independently with the
Haskell backend:

| Target | Clean build | Fresh proof |
|---|---|---|
| `WORD-SPEC` | `evidence/05a-build-word.log`: exit 0 | `evidence/05b-prove-word.log`: exit 0, `#Top` |
| `ANTI-LOOP-SPEC` | `evidence/05c-build-loop.log`: exit 0 | `evidence/05d-prove-loop.log`: exit 0, `#Top` |
| `ANTI-SHUFFLE-SPEC` | `evidence/05e-build-final.log`: exit 0 | `evidence/05f-prove-final.log`: exit 0, `#Top` |

Thus clean dynamic reconstruction succeeds. These results establish closure
only in the submitted extended theory. They do not establish that the
proof-local operational rules are sound.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **`sort-word-summary` (`spec.k:8-29`).** Starting in module environment 0
   with the builtins scope, empty control stack, no return or exception, and
   fresh heap locations `N` and `N+1`, executing
   `"".join(sorted(list(str(W))))` returns `str(sortWord(W))`. Final heap and
   heap location are unconstrained.

2. **`anti-loop` (`spec.k:37-57`).** In function environment 1, with
   `result = A`, arbitrary `s`, arbitrary initial `word`, and a custom iterable
   `wordsObj(WS)`, executing the submitted loop body and then reading `result`
   returns `A ++ emitWordSeq(WS)`. Final scopes, heap, and heap location are
   unconstrained.

3. **`anti-shuffle-correct` (`spec.k:65-84`).** From the normal initial
   module/builtins configuration, directly call a closure with parameter `s`,
   body `antiBody`, and argument `str(S)`. On termination its value is
   `antiShuffleSpec(S)`. There is no `requires` clause: the formal domain is
   every `IntSeq`, not a stated ASCII range. Final heap and heap location are
   existential; stack, return, exception, environment, and exit status must
   have returned to the displayed values.

### Program identity

`antiBody` expands to the exact constructor sequence in the freshly regenerated
`solution.mpy`: the two assignments, the `For`, both `AugAssign` statements,
and the final `result[:-1]` return all match. The entry claim directly calls a
closure containing that exact body rather than loading the `.mpy` file.
For the current artifacts the manual structural pin is exact, supported by the
trusted-translator byte-identity check. It is not automatically body-sensitive:
changing `solution.mpy` alone would not change the hard-coded macro.

The return is not a free variable or tautology. `antiShuffleSpec(S)` is the
specific slice of `emitWordSeq(splitWords(S, 32, .IntSeq))`. The false-result
mutation in stage 6 confirms that the entry result is discriminating.
Nevertheless, using `splitWords` both in an execution-replacing bridge and in
the postcondition is circular unless supplied-semantics execution is
independently connected to that value. No such connection theorem exists.

### Satisfiability and ground substitution

The entry precondition is satisfied, for example, by `S = .IntSeq` and exactly
the displayed initial cells. For the word claim, `H = .Map`, `N = 0` satisfies
both freshness guards. For the loop claim, `A = .IntSeq`, `WS = .Words`,
`H = .Map`, and `N = 0` supplies a ground state.

Four concrete substitutions for the entry result were checked:

| Input | Claimed value | Canonical Python | Generated Python |
|---|---|---|---|
| `""` | `""` | `""` | `""` |
| `"ba"` | `"ab"` | `"ab"` | `"ab"` |
| `" a"` | `" a"` | `" a"` | `" a"` |
| `"  ba  dc "` | `"  ab  cd "` | `"  ab  cd "` | `"  ab  cd "` |

The K ground summary obligations closed in
`evidence/10-ground-summary.log`; the explicit Python results are in
`evidence/10b-ground-python.log`. These witnesses establish satisfiability and
ground agreement, not universal bridge soundness.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and baseline disposition

`evidence/08-rule-inventory.txt`, generated by
`evidence/generate_rule_inventory.sh`, enumerates every local `syntax`, `rule`,
`configuration`, and `context` start, every relevant attribute, every opaque or
uninterpreted declaration, and SHA-256 hashes for all source files.

The supplied tree has 227 syntax declarations, 695 rules, one configuration,
and five contexts. `verification.k` adds nine syntax declarations and 18 rules.
The supplied rules are byte-identical to the selected trusted semantics, so
their inventory disposition is **selected semantics boundary**, not
candidate-provided proof extension. Every supplied rule unused by
`solution.mpy` is inert for this theorem. The used subset was traced
individually in `evidence/09-used-construct-map.log`:

| Program construct | Supplied declaration and execution path |
|---|---|
| `Module`, sequencing, `Name`, `Str`, `Int` | `syntax.k`; `core.k` load, lookup, literal, and sequence rules |
| `FuncDef`, closure call, parameter, return | `functions.k` and `call.k` frame/bind/pop rules |
| `Assign`, `AugAssign`, `For` | `controls.k`; `operators.k`; `str.k` concatenation |
| `s.split(" ")` | `methods.k:94-102`, allocation via `#alloc`, list iteration |
| `list(word)` | `builtins.k:32-38`, one allocation |
| `sorted(...)` | `sort.k:18-37`, `sortVS`, a second allocation |
| `"".join(...)` | `methods.k:26-31` |
| `result[:-1]` | `subscript.k:49-120`, negative stop normalization and `buildIS` |

The configuration, evaluation order, binding, function-frame restoration,
loop control, string updates, slice behavior, and the two temporary allocations
all follow the supplied rules on this path. The complete relevant source
listing is preserved in `evidence/07-relevant-semantics.log`.

The only reachable supplied opaque value is `sortVS`, declared
`[function, total, symbol(sortVS), no-evaluators]`. On ground lists the
`[concrete]` insertion-sort equations run; on symbolic lists its interpretation
is trusted. Other inventoried opaque symbols—`sortKeyVS`, `md5hexCodes`, and
the float-operation family—are unreachable. `strLt` is recursively defined on
constructor sequences but remains inert for an abstract non-constructor
sequence. `valSeqAt` is total and underspecified off its in-bounds constructor
cases, also unreachable in this program. These boundaries do not license new
proof-local state transitions.

### Complete `verification.k` declaration inventory

The nine declarations are:

1. `antiLoopBody : Stmts` macro.
2. `antiBody : Stmts` macro.
3. `sortWord(IntSeq) : IntSeq`, function and total.
4. `.Words`/`wCons(IntSeq, Words) : Words`.
5. `wordVals(Words) : ValSeq`, function and total.
6. `splitWords(IntSeq, Int, IntSeq) : Words`, function and total.
7. `emitWordSeq(Words) : IntSeq`, function and total.
8. `antiShuffleSpec(IntSeq) : Val`, function and total.
9. `wordsObj(Words) : Iterable`.

There is no proof-local opaque or `functional` declaration. The total
functions have constructor coverage. The `splitWords` separator and
non-separator guards are complementary; the recursive equations descend on the
remaining sequence. No contradictory equation overlap was found.

### Disposition of all 18 proof-local rules

1. `antiLoopBody` expansion: **sound macro**, exact submitted loop body.
2. `antiBody` expansion: **sound macro**, exact submitted function body.
3. `sortWord(W)`: **sound definitional summary conditional on supplied
   `sortVS`**.
4. `wordVals(.Words)`: **sound constructor equation**.
5. `wordVals(wCons(...))`: **sound constructor equation**.
6. `splitWords(.IntSeq, ...)`: **sound split base equation**.
7. `splitWords` when `C == SEP`: **sound separator equation**.
8. `splitWords` when `C != SEP`: **sound non-separator equation**.
9. `emitWordSeq(.Words)`: **sound base equation**.
10. `emitWordSeq(wCons(...))`: **sound emission equation**.
11. `antiShuffleSpec(S)`: **sound definition of the candidate's intended
    summary**, conditional on `sortVS`; it is not itself a theorem connecting
    execution to the summary.
12. `seqConcat(A, .IntSeq) => A [simplification]`: **true right-identity
    lemma** under the supplied recursive `seqConcat`.
13. right-association of nested `seqConcat [simplification]`: **true
    associativity lemma**, oriented toward a terminating right-associated form.
14. `#iterNext(wordsObj(.Words))`: **sound rule for the new custom
    representation**.
15. `#iterNext(wordsObj(wCons(...)))`: **sound rule for the new custom
    representation**.
16. priority-35 `str.split` bridge: **unsound operational bridge**.
17. priority-40 word-sort-call bridge: **unsound operational bridge**.
18. priority-40 installed loop summary: **unsound operational bridge**.

The last three failures are witnessed, not inferred from missing prose:

#### Rule 16: split bridge false conclusion

For ground intended input `"a b"`, the proof-local rule rewrites
`#applyK(...split...)` to `wordsObj(...)` while retaining
`<heap> .Map </heap>` and `<heapLoc> 0 </heapLoc>`. That extended-theory claim
prints `#Top` (`evidence/12a-split-bridge-extended.log`).

The supplied semantics instead returns `ref(0)`, places the two strings in a
list at heap location 0, and advances `heapLoc` to 1. The exact
supplied-semantics transition also prints `#Top`
(`evidence/12b-split-bridge-base.log`). The witness source is
`evidence/split-bridge-witness.k`.

Thus the bridge's conclusion is false over its complete matched state. It
preempts the fixed priority-40 split rule with priority 35, accepts an arbitrary
continuation, and has no bridge-free universal connection theorem. Its
iteration value is plausibly observationally related to the list, but that
informal fact does not justify the globally different state transition.

#### Rule 17: word-sort bridge false conclusion

For ground `word = "ba"`, the proof-local bridge claims the final abstract
string with an unchanged empty heap and `heapLoc = 0`. The extended claim prints
`#Top` (`evidence/13a-sort-bridge-extended.log`).

Without that bridge, the identical no-allocation claim fails with a concrete
residual containing the `list(word)` object at heap 0, the sorted list at heap
1, and `heapLoc = 2` (`evidence/13b-sort-bridge-false-base.log`). The exact real
two-allocation transition separately prints `#Top`
(`evidence/13c-sort-bridge-true-base.log`). See
`evidence/sort-bridge-witness.k`.

The auxiliary `WORD-SPEC` constrains the returned value but existentially
forgets final heap and heap location. It therefore does not prove the
state-preserving rule installed over an arbitrary continuation. The installed
guard checks only `word`; it also fails to pin possible `list` or `sorted`
shadowing over its general match domain. The actual candidate function does not
shadow them, but a globally false rule cannot be justified by this one use.

#### Rule 18: loop summary proves a false observable result

`ANTI-LOOP-SPEC` proves only the exact continuation
`#loop(...) ~> Name("result")` and existentially forgets final scopes. The
installed rule instead accepts every continuation, preserves every binding
other than `result`, and deletes the loop from `<k>`.

The fresh intended-domain witness uses the one-element word sequence `"ba"` and
places `Name("word")` immediately after the loop. With the installed summary,
K proves that the continuation returns the *initial empty string*
(`evidence/11b-loop-bridge-extended.log`, exit 0, `#Top`). Without the installed
summary, the same claim fails, and the residual is the actual `"ba"` value
bound by the loop (`evidence/11c-loop-bridge-base.log`, exit 1,
`WarnStuckClaimState`). The source is
`evidence/loop-bridge-witness.k`.

This is a direct false result, not merely an omitted heap effect. The actual
entry continuation is a `Return` over the accumulator slice, whereas the
auxiliary theorem justifies only `Name("result")`; no theorem establishes the
rule over either that actual continuation or all continuations it accepts.

`evidence/11a-loop-bridge-extended.log` preserves an initial reviewer test that
also constrained the unrelated final `result` binding and consequently failed.
The corrected witness existentially frames final scopes; only the observable
`<k>` result differs, as shown by 11b and 11c.

These witnesses satisfy the required false-conclusion standard. Because the
rules are globally false and contribute to entry-claim closure, their use is
illegitimate even though the particular Python implementation happens to be
correct and the entry postcondition happens to agree on tested values.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. A fresh mutation was written at
`evidence/spec-vacuity.k`. It keeps the exact entry configuration but
instantiates the satisfying input `"ba"` and falsely requires the empty string
instead of `"ab"`.

`kprove --dry-run` exited 0, establishing that the mutation parses and builds
against the fresh definition (`evidence/14a-vacuity-dry-run.log`). The real
proof exited 1 with `WarnStuckClaimState`; the residual `<k>` value is precisely
`str(iCons(97, iCons(98, .IntSeq)))`, i.e. `"ab"`
(`evidence/14b-vacuity-proof.log`).

This is valid non-vacuity evidence: the mutation is reachable, materially
changes the result obligation, builds successfully, and fails for the expected
unmet result. Non-vacuity passes, but it does not establish operational-bridge
soundness.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the supplied MPY rules **plus all 18 rules in `verification.k`**, K proves
partial correctness of a direct closure call containing the exact current
candidate body:

```text
result = doSlice(
  str(emitWordSeq(splitWords(S, 32, .IntSeq))),
  noB, someB(-1), noB)
```

for every symbolic `IntSeq S`, if the extended-theory execution terminates.
The word and custom-loop auxiliary claims establish their displayed summaries
under their respective extended modules. The proof does not establish total
correctness.

It does **not** establish that supplied-semantics execution of the real
program has this result, because closure depends on the false split, sort-call,
and loop operational bridges. In particular, the same `splitWords` value is
introduced by a bridge and consumed by the postcondition without a bridge-free
connection theorem.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Supplied MPY semantics and K builtins/hooks for integers, booleans, strings, maps, lists, cells, rewriting, and backend execution | All claims | Approved fixed semantics boundary; candidate copy has exact integrity. |
| `sortVS(ValSeq)` opaque symbolic sorted value | `sortWord`, word claim, loop claim, entry postcondition | Acceptable only as a named supplied primitive. The K theorem is conditional on interpreting it as real ascending `sorted`; the natural-language ordering bridge is not proved in K. |
| Unreachable supplied opaque symbols: `sortKeyVS`, `md5hexCodes`, and the inventoried float symbols (`intFloatDiv`, `divII`, `floatMod`, comparisons, conversions, arithmetic, rounding, and square root) | None on the submitted body | Trusted but irrelevant. Exact declarations are listed in `evidence/08-rule-inventory.txt`. |
| Trusted translator byte identity | Manual source/AST/body pin | Strong reproducible identity evidence for the current artifact, not a K theorem and not automatically body-sensitive. |
| Trusted canonical Python implementation | Differential and ground comparison only | Independent finite intent oracle; 4,408 inputs support the Python-to-contract bridge but do not prove K extensions. |
| Reviewer concrete MPY run | Six ground assertions | Finite evidence that the supplied concrete semantics handles ordinary/boundary cases; not symbolic proof. |
| Informal recurrence argument that `splitWords` matches supplied `splitSep` through iteration | Split bridge and entry | Concerning and insufficient: no bridge-free universal theorem, and the installed rule has a concretely false state transition. |
| Informal argument that the auxiliary loop theorem can be installed for arbitrary continuations | Entry proof | Illegitimate: contradicted by the `"ba"`/`Name("word")` machine-checked witness. |
| Existentially forgotten final heap/heap location | All three positive claims | Permissible for those postconditions, but it cannot justify globally state-preserving operational rules. |

### Gate accounting and decision

- Input/provenance integrity: **FAIL** (four named artifacts missing), while the
  semantics-mode boundary and source integrity checks pass.
- Program fidelity: **PASS** for the current Python/MPY artifact.
- Fresh reconstruction: **PASS** for build and `#Top` closure in the extended
  theory.
- Real-program soundness / operational extensions: **FAIL**, with three
  concrete false-transition witnesses and one directly false observable result.
- Entry result constraint and non-vacuity: **PASS**.
- Natural-language bridge: empirically supported but conditional on the
  supplied `sortVS` trust boundary.

The failed real-program soundness gate is material and independently sufficient
for rejection. The successful Python differential, fresh `#Top` results, ground
examples, and false-result mutation cannot substitute for sound proof rules.

Evidence integrity hashes are in `evidence/16-evidence-manifest.log`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
