# Independent adversarial audit — 140-fix-spaces

## Decision

The candidate is **FAIL / NOT_LEGIT**.

Fresh reconstruction does reproduce all eight advertised `#Top` results, and the
entry claim expands to the submitted translated program.  Those successes are
not a legitimate proof under the supplied semantics, however, because the two
priority-20 step-summary rules in `verification.k` are false over their declared
match domains.  Their bridge-free auxiliary claims prove the body only when the
module scope contains exactly `fix_spaces`; the promoted rules accept an
arbitrary module scope and therefore silently assume that `ord` resolves to the
builtin.  Ground fixed-versus-extended K witnesses show both false conclusions:
fixed semantics honors a module-level shadowing `ord` and rejects the proposed
step state, whereas the bridge-enabled definition proves that false state as
`#Top`.

There is also a material candidate-versus-canonical result divergence for
strings whose final run is exactly two spaces.  The candidate agrees with the
literal prompt wording on that boundary, while the trusted canonical
implementation emits only one underscore.  This intent discrepancy is separate
from, and not needed for, the soundness failure above.

All execution and mutation work was done in
`/tmp/audit-work/140-fix-spaces`.  `/candidate` was read only.  Reviewer scripts,
inputs, generated comparison terms, and bounded logs are under
`/audit-output/evidence`; `evidence/MANIFEST.sha256` hashes the 50 evidence
files produced before the manifest.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present.  Thus the trusted mounts do not
contradict the rendered mode and this is not an infrastructure-error case.

`evidence/provenance.log` records artifact types, hashes, comparisons, and exit
statuses:

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`f757e5d21a3d47b21dcd96c7c9f869adfbfe70276370fddb0f4ded8fb1c311f9`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Recursive `diff -r --no-dereference --brief` between the candidate and
  trusted `reference-semantics/` trees exits 0.  Both trees have the same 24
  regular K files, with identical per-file SHA-256 values.  Neither tree
  contains a symlink.  There are no missing, additional, mistyped, changed, or
  symlinked entries within the supplied-semantics tree.
- `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prove.sh`,
  `prompt.py`, and `py2mpy.py` are regular files.  The candidate also contains
  `__pycache__/solution.cpython-310.pyc`; this candidate-built cache was ignored
  and not copied.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are all missing.  No structured generation trace, JSONL,
  or other JSON trace is present.  Consequently none of the requested
  generation metadata could be inspected, and no claim based on that missing
  provenance is credited.

The live independent toolchain is K `v7.1.337` (build date 2026-06-18) with
Python 3.10.12.  `kompile`, `kprove`, `krun`, and `kast` are installed directly;
`kup` is absent.  Exact checks are in `evidence/environment.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The prompt says that spaces are replaced with underscores, except that a
maximal run longer than two spaces is replaced by one hyphen.  Its examples
cover no space, one internal space, one leading space, and three internal
spaces.  The trusted canonical implementation accumulates a pending run and
flushes it at the next non-space or at end of input.

The candidate maintains `result` and a nonnegative `spaces` count.  A code point
other than 32 flushes `spaces` as `""`, `"_"`, `"__"`, or `"-"` and then emits
the character; code point 32 increments `spaces`; the same flush is performed
after the loop.  `ord(char) - 32` is false exactly for the ordinary space
character and true for every other one-character Python string.

### Translation identity

The submitted `solution.mpy` was regenerated from the scratch copy of
`solution.py` with the trusted `/reference/py2mpy.py`.  Both files have SHA-256
`5c42c1a38d15ba4bcbec6313f653bb1dd871da78ec0cfcb5f79257dcab5887dc`;
`cmp -s` exits 0.  Commands and statuses are in
`evidence/provenance.log`.

### Independent differential

`evidence/differential_test.py` imports the trusted canonical entry point and
the scratch candidate under distinct module names.  It tests:

- all four documented examples;
- empty input;
- leading, internal, trailing, and all-space runs of lengths 0, 1, 2, 3, and
  4;
- multiple runs, non-ASCII characters, tab/newline, and NUL;
- every string of length 0 through 7 over `{space, "a", "b"}`;
- 1,000 deterministic generated strings of length 0 through 40 over spaces,
  ASCII, Unicode, other whitespace, and NUL.

After duplicate removal, 4,249 distinct inputs were tested and are preserved
in `evidence/differential-inputs.jsonl`.  The exact command and bounded result
are in `evidence/differential.log`.  The script exits 1 because it finds 254
candidate/canonical mismatches.  Every observed mismatch has a final run of
exactly two spaces, for example:

```text
input "  ": candidate "__", canonical "_"
input "a  ": candidate "a__", canonical "a_"
```

A direct reviewer-authored model of the prompt prose has zero mismatches
against the candidate and the same 254 mismatches against the canonical.  This
is finite evidence, not a universal proof.  It establishes a real trusted
canonical divergence on intended string inputs while also locating the
prompt/canonical inconsistency precisely.

## 3. Clean proof reconstruction

Only source artifacts were copied to scratch.  No candidate definition,
compiled output, Python cache, or K cache was reused.

### Concrete definition

The following fresh checks all exit 0:

- Python execution of the copied candidate assertions:
  `evidence/reconstruct-01-python-tests.log`.
- LLVM compilation of trusted `reference-semantics/semantics.k`, main module
  `MPY-KRUN`, into fresh `runtime-kompiled`:
  `evidence/reconstruct-02-kompile-runtime.log`.
- `krun concrete-tests.mpy --definition runtime-kompiled`, ending with
  `<k> .K </k>` and `<exit-code> 0 </exit-code>`:
  `evidence/reconstruct-03-krun-concrete-tests.log`.

The reviewer also created an independent concrete boundary harness rather than
relying only on candidate assertions.  It contains 19 documented and branch
boundary cases, is translated with the trusted translator, passes in Python,
and reaches `.K` with exit code 0 under the fresh LLVM definition.  See
`evidence/independent-concrete.py`,
`evidence/independent-concrete.mpy`, and
`evidence/independent-concrete.log`.

### Proof definitions and every positive claim

Four Haskell definitions were freshly compiled from source in the same staged
dependency order used by the claimed proof.  All four compilations exit 0:

| Definition | Main module | Evidence |
|---|---|---|
| `proof-base-kompiled` | `FIX-SPACES-BASE` | `evidence/reconstruct-10-kompile-flush.log` |
| `proof-step-kompiled` | `FIX-SPACES-FLUSH-VERIFICATION` | `evidence/reconstruct-20-kompile-step.log` |
| `proof-loop-kompiled` | `FIX-SPACES-STEP-VERIFICATION` | `evidence/reconstruct-30-kompile-loop.log` |
| `proof-main-kompiled` | `FIX-SPACES-VERIFICATION` | `evidence/reconstruct-40-kompile-main.log` |

Each positive target was then invoked independently.  Every command exits 0
and prints `#Top`:

| Claim | Evidence |
|---|---|
| `flush-zero` | `evidence/reconstruct-11-kprove-flush-zero.log` |
| `flush-one` | `evidence/reconstruct-11-kprove-flush-one.log` |
| `flush-two` | `evidence/reconstruct-11-kprove-flush-two.log` |
| `flush-many` | `evidence/reconstruct-11-kprove-flush-many.log` |
| `step-space` | `evidence/reconstruct-21-kprove-step-space.log` |
| `step-non-space` | `evidence/reconstruct-21-kprove-step-non-space.log` |
| structural loop claim | `evidence/reconstruct-31-kprove-loop.log` |
| end-to-end main claim | `evidence/reconstruct-41-kprove-main.log` |

Thus the candidate's reported proof closure is reproducible.  This stage does
not establish that the extensions used for closure are sound.

## 4. Adequacy and real-program pinning

### Plain-language claims

- `flush-zero`: with pending count 0, the tail consumes and leaves `result`
  unchanged.
- `flush-one`: with pending count 1, the tail appends one underscore.
- `flush-two`: with pending count 2, the tail appends two underscores.
- `flush-many`: with pending count `N > 2`, the tail appends one hyphen.
- `step-space`: from `N >= 0` and one-character `char = " "`, one execution of
  the actual loop body leaves `result` unchanged and changes `spaces` to
  `N + 1`.
- `step-non-space`: from `N >= 0` and one-character code `C != 32`, one body
  execution appends the pending-run representation followed by `C`, then sets
  `spaces` to 0.
- The loop claim: from `N >= 0`, executing the actual `#loop` over `str(IS)`
  consumes it, changes `result` to `fixSpacesLoop(A, IS, N)`, changes `spaces`
  to `trailingSpaces(IS, N)`, and records the last iterated character through
  `finalChar`.
- The entry claim: from the fresh initial configuration and any
  `IS:IntSeq`, load the submitted function and call it on `str(IS)`.  The
  returned value is
  `str(appendPending(fixSpacesLoop(.IntSeq, IS, 0),
  trailingSpaces(IS, 0)))`; the callee frame, stack, return state, exception
  state, heap, allocation counters, and exit code are restored, while module
  scope contains the loaded closure.

The entry claim has no `requires` clause.  Its result is a deterministic term
of `IS`, not a fresh variable, tautology, existential, or one-way implication.
Each helper precondition is satisfiable: use empty code sequences and, as
applicable, counts 0, 1, 2, 3, a space code 32, or a non-space code 97.

### Actual program identity

The entry `<k>` cell names the proof-local `solutionModule` macro rather than a
filesystem path.  This is nevertheless the exact submitted program term.
`evidence/run_program_identity.sh` independently parses `solution.mpy` and
parses `solutionModule` with macro expansion, both against the fresh main
definition.  Their KORE outputs are byte-identical (`cmp` exit 0; both SHA-256
`2a82e708bccdb2f46c7c9f202124e958fc434983928b4be61befc48e248feeed`).
The terms are preserved as `evidence/program-identity-solution.kore` and
`evidence/program-identity-macro.kore`.

Consequently the function body, loop body, tail, calls, and return in the claim
match the submitted `solution.mpy`; this is not a substituted-program proof.

### Satisfying state and ground substitutions

`evidence/entry_claim_witness.py` records a fully realizable entry state with
`IS = .IntSeq`, initial module and builtin scopes, `scopeLoc = 1`, empty heap
and stack, `noRet`, `NoExc`, and exit code 0.  It evaluates the K result
functions directly on 11 ground substitutions and compares them with both
Python implementations.  The candidate has zero mismatches against the
claimed result.  The canonical mismatches exactly on the selected trailing
two-space cases (`"  "`, `"a  "`, and `"  a   b  "`).  The command exits 0;
see `evidence/entry-witness.log`.

The formal result therefore describes the submitted program and the literal
prompt interpretation, but not the trusted canonical on that material
boundary.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` scans the fresh sources and
`evidence/k-rule-inventory.md` reproduces every declaration with its exact file
span and complete block.  It inventories 238 syntax declarations, one
configuration, 695 supplied-semantic rules, 20 candidate verification rules
(715 rules total), and eight claims.  It also tags functions, totality, functional declarations,
priority, simplification, macro, concrete, owise, strictness, and symbolic
no-evaluator declarations.  Generation exits 0 in `evidence/inventory.log`.

The per-file rule decisions are:

| File | Syntax / rules | Static decision and proof relevance |
|---|---:|---|
| `semantics.k` | 0 / 0 | Trusted assembly only; imports the exact supplied modules. |
| `assert.k` | 0 / 3 | Trusted baseline; unused by the entry proof. |
| `bool.k` | 0 / 13 | Trusted baseline; general BoolOp rules unused. |
| `builtins.k` | 38 / 137 | Trusted baseline; builtin registry dispatch and the exact one-character `ord` rule are used. Other folds/opaque MD5 are unmatched. |
| `call.k` | 3 / 21 | Used: callee lookup, left-to-right argument evaluation, builtin dispatch, user closure frame creation. |
| `comprehension.k` | 3 / 7 | Unused. |
| `concrete.k` | 5 / 16 | LLVM-only trusted rules; no deep equality or sorting term occurs in this program. |
| `controls.k` | 3 / 34 | Used: Assign, AugAssign, If, For, loop protocol, and current-scope updates. |
| `core.k` | 37 / 46 | Used: configuration, module load, statement sequencing, LEGB lookup, builtins scope, literals, truthiness, argument evaluation, and shared sequence helpers. |
| `dict.k` | 12 / 28 | Unused. |
| `float.k` | 34 / 121 | All Float and math terms are sort/shape-disjoint and unused. |
| `functions.k` | 4 / 15 | Used: ordinary `FuncDef`, parameter bind, `Return`, frame pop, and state restoration; annotated closures are unused. |
| `int.k` | 1 / 16 | Used: integer `+`, `-`, `>`, and `==`; guards are ordinary integer relations. |
| `iter.k` | 1 / 0 | Declares the iterator protocol used by For and strings. |
| `list.k` | 5 / 27 | No list value occurs; unused. |
| `methods.k` | 27 / 75 | No method call occurs; unused. |
| `operators.k` | 0 / 10 | Used generic unary/binary/compare dispatch; ref-special cases are unmatched. |
| `range.k` | 2 / 6 | Unused. |
| `set.k` | 6 / 12 | Unused. |
| `sort.k` | 6 / 19 | `sortVS` and `sortKeyVS` trusted opaque boundaries are unused. |
| `str.k` | 5 / 28 | Used: string iteration, ASCII program literals, concatenation, equality machinery, and code-sequence representation. |
| `subscript.k` | 15 / 40 | Unused. |
| `syntax.k` | 16 / 0 | Declares every submitted AST constructor; strict/seqstrict attributes supply the documented evaluation order. |
| `tuple.k` | 4 / 21 | Used only for `#bindTgt(Name, V)` in the For loop; tuple construction/unpacking is unused. |
| `verification.k` | 11 / 20 | Candidate extensions; assessed individually below. |
| `spec.k` | 0 / 0 plus 8 claims | All eight positive claims were run separately; claims are not semantic axioms. |

Because this is `SUPPLIED_SEMANTICS`, every rule in the identical
`reference-semantics` tree is the selected fixed semantics rather than a
candidate-authored semantic extension.  The table and exhaustive artifact
still account for every rule.  Unused rules cannot match any reachable term in
the submitted AST.  For the used subset, evaluation is left-to-right where
required, local state changes occur in scope 1, string iteration yields
one-code strings, `ord` is obtained by LEGB lookup, the user call allocates and
pops one scope frame, no heap allocation occurs, and all observable cells named
by the entry claim are restored.

The supplied symbolic primitives
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF` are all outside the term dependency graph.
None can affect control, state, or the final result here.

### Every candidate verification declaration and rule

The 20 rules in `verification.k` divide as follows:

1. `pendingSpaces` has one total nested-if equation for all integers.
2. `appendPending` has one total nested-if equation for all
   `(IntSeq, Int)` pairs.
3. `fixSpacesLoop` has three disjoint, structurally decreasing equations:
   empty suffix, leading code 32, and leading code `C != 32`.
4. `trailingSpaces` has the corresponding three disjoint, structurally
   decreasing equations.
5. `finalChar` has two structurally decreasing equations for empty and
   nonempty suffixes.
6. Six macro rules define the loop-body statement, loop-body statement list,
   tail statement, tail statement list, function body, and module.
7. Four operational bridges promote the flush, space step, non-space step,
   and loop summaries.

The first ten function equations are truthful definitions with disjoint or
equivalent branches, complete constructor coverage, and structural descent.
The four `[simplification]` recursive equations do not introduce a false
mathematical equality.  `N >= 0` is established at every operational use:
initially 0, incremented only on space, and reset only to 0.

The six macros are exact AST factoring.  Their combined module identity is
machine-checked by the byte-identical KORE comparison described in stage 4.
They do not replace program execution.

The operational bridges require separate treatment:

| Bridge | Candidate justification | Complete-domain assessment |
|---|---|---|
| Flush, lines 143–179 | Four bridge-free flush claims cover `N=0`, `1`, `2`, and `>2`. | Value/state summary is exhaustive for `N>=0`. The rule accepts an arbitrary continuation while the claims end at `.K`; no bridge-free universal frame theorem was supplied. No false continuation witness was found, so this is recorded as a context-justification gap, not labeled unsound. |
| Space step, lines 186–212 | `step-space` proves the actual body with a module scope containing exactly `fix_spaces` and trusted builtins. | **Unsound.** Promoted rule replaces that exact module scope by arbitrary `MODULE:Scope`, yet the body performs LEGB lookup of `ord`. Priority 20 makes the false bridge preempt fixed execution. |
| Non-space step, lines 214–244 | `step-non-space` has the same exact-module justification. | **Unsound** for the same binding-domain expansion. |
| Loop, lines 252–289 | Structural loop claim proves the actual `#loop` for the exact module and builtins scopes. | Summary equations and state footprint match the real loop. As with flush, promotion broadens `.K` to an arbitrary continuation without a universal frame theorem. This is a narrower evidence gap absent a false witness. Its derivation also depends on the two invalid promoted step rules. |

### Concrete false-conclusion witnesses for both unsound rules

`evidence/bridge-witness.k` contains six ground claims, run by
`evidence/run_bridge_witness.sh`.  All inputs are ordinary one-character strings
within the intended string domain.  Complete configurations fix all allocation,
heap, stack, return, exception, and exit-code cells.

For the non-space rule, local `char` is `"a"`, `spaces` is 0, and `result` is
empty.  Module scope shadows `ord` with a one-argument closure returning 32.
Fixed semantics therefore resolves that closure, computes `32 - 32 = 0`, takes
the space branch, and reaches `result = ""`, `spaces = 1`:

- fixed-correct claim: `#Top`, exit 0
  (`evidence/bridge-01-nonspace-fixed-correct.log`);
- fixed claim of the bridge conclusion `result = "a"`, `spaces = 0`:
  `WarnStuckClaimState`, exit 1
  (`evidence/bridge-02-nonspace-fixed-wrong.log`);
- the same false conclusion with
  `FIX-SPACES-STEP-VERIFICATION` enabled: `#Top`, exit 0
  (`evidence/bridge-03-nonspace-enabled-wrong.log`).

For the space rule, local `char` is `" "`, while module `ord` is a closure
returning 33.  Fixed semantics computes a truthy `33 - 32`, emits the space
character, and leaves `spaces = 0`; the promoted rule instead leaves `result`
empty and sets `spaces = 1`:

- fixed-correct claim: `#Top`, exit 0
  (`evidence/bridge-04-space-fixed-correct.log`);
- fixed claim of the bridge conclusion: `WarnStuckClaimState`, exit 1
  (`evidence/bridge-05-space-fixed-wrong.log`);
- bridge-enabled false conclusion: `#Top`, exit 0
  (`evidence/bridge-06-space-enabled-wrong.log`).

These are not parser failures, timeouts, or unconstrained opposite
interpretations.  They compare fixed and extended semantics on complete
satisfiable ground states and show different values and state updates.  The
entry claim's fresh module does not itself shadow `ord`, but the rules are
globally false over the match domain they declare.  A priority attribute does
not make that broader binding assumption true.  Narrowing both rules to the
exact justified module scope (or proving an independent universal binding
theorem) was required before using them as proof axioms.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to credit.  The reviewer-authored
`evidence/spec-vacuity.k` keeps the exact entry state and program but mutates
the result to append one extra underscore.  This is demonstrably false for the
satisfying input `IS = .IntSeq`: the real and originally claimed result is the
empty string, while the mutation demands `"_"`.

The mutation parses and builds against the fresh main definition.  The exact
command

```text
kprove spec-vacuity.k --definition proof-main-kompiled --spec-module FIX-SPACES-MAIN-VACUITY
```

exits 1 with `WarnStuckClaimState`.  Its residual says that the final terms
unify but the implication between the original result and the result with
`iCons(95, .IntSeq)` fails.  This is the expected unmet result obligation, not
an unrelated crash.  The complete bounded output is in
`evidence/vacuity.log`, and `evidence/run_vacuity.sh` checks both nonzero exit
and the stuck-claim diagnostic.

The entry theorem is therefore result-constraining and non-vacuous.  This does
not repair the false operational rules used to prove it.

## 7. Proven versus assumed accounting

### What `#Top` establishes under the submitted extended theory

Under the supplied MPY semantics plus all four candidate operational bridges,
the reachability proof establishes that, for any finite `IS:IntSeq`, the exact
submitted program term reaches the deterministic fold result stated in stage
4 and restores the named machine cells.  The auxiliary claims establish the
four flush cases, the two body cases in their narrower scopes, and the
structural loop summary.  The proof is a partial-correctness reachability proof;
it is not a proof that the natural-language description or trusted canonical
has a particular external meaning.

Because the theory contains two machine-demonstrated false rewrites, that
conditional closure is not a legitimate proof under the selected fixed
semantics.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.337`, Haskell/LLVM backends, and hooked Int/Bool/String/Map/List operations | All builds and runs | Ordinary unavoidable toolchain trust; commands and actual outputs are preserved. |
| Exact supplied `reference-semantics` tree | All concrete and symbolic execution | Acceptable selected semantics boundary; candidate tree is byte-identical and unsymlinked. |
| `IntSeq` as a Python string code sequence | Input, iteration, `ord`, final string | The formal domain is broader than valid Python Unicode strings, but the program depends only on equality with code 32. All real Python strings embed in it; no false real-string conclusion follows from the overbreadth. |
| Proof-local recursive summaries | Claimed result and loop state | Acceptable mathematical definitions: exhaustive, disjoint, descending, and not opaque. |
| Program macros | Every auxiliary and entry claim | Acceptable after independent KORE identity with submitted `solution.mpy`. |
| Flush bridge | Step and main proof | Exact value cases are proved; arbitrary-continuation connection theorem missing. Concerning evidence gap, not called unsound without a false witness. |
| Space and non-space step bridges | Loop and main proof | Illegitimate. Their arbitrary module scope is broader than the binding context proved, and fixed-versus-extended ground witnesses demonstrate false conclusions. |
| Loop bridge | Main proof | Its summary matches real control flow on the entry scope, but it depends on the invalid step bridges and lacks a universal arbitrary-continuation theorem. |
| Supplied opaque float, sort, and MD5 symbols | None | Inert for this AST and result; they are not correctness oracles for this proof. |
| Natural-language meaning of the fold | Human-facing contract | Informal mathematical bridge plus finite differential evidence only. The candidate matches the direct prose model on 4,249 inputs. |
| Equivalence to trusted canonical | Program-fidelity conclusion | Empirically false on 254 tested inputs, with explicit boundary witnesses. |
| Candidate generation reports/traces | Auditability of construction history | Not available: all four requested provenance files and the structured trace are missing. |

### Gate accounting

- Real-program soundness / extension audit: **FAIL**.  Two result- and
  state-bearing priority rules admit false conclusions under fixed semantics.
- Intent adequacy: the theorem pins the submitted program and agrees with a
  direct reading of the prompt, but materially disagrees with the trusted
  canonical on trailing runs of exactly two spaces.
- Evidence auditability: fresh commands, scripts, inputs, proof logs,
  counterexamples, and mutation are reproducible; candidate generation
  provenance is missing.

The successful `#Top`, concrete tests, differential tests, macro identity, and
non-vacuity test answer different questions.  None substitutes for a
bridge-free proof that each promoted operational rule is true over its complete
domain.  The two fixed-semantics counterexamples make the candidate proof
theory materially unsound, requiring the terminal candidate verdict below.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
