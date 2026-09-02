# Independent adversarial audit: 17-parse-music

The candidate is **not a legitimate proof of the task contract**. Fresh K
reconstruction succeeds, and the claims that were actually written are
non-vacuous and locally sound. The fatal issues are scope and program fidelity:

1. `solution.py` is wrong on empty fields produced by `str.split(" ")`.
   On the intended domain, `parse_music("")` returns `[1]` instead of the
   canonical `[]`; `"o  .|"` returns `[4, 1, 1]` instead of `[4, 1]`.
2. `spec.k` contains no universal end-to-end result claim. It proves four
   ground executions, isolated loop transitions, and source-to-loop reduction
   facts, but never states the result for an arbitrary input.
3. The loop claims do not even match the complete loop states reached by the
   real program: they require an empty `<functions>` map and an `<env>` holding
   only `beats`, while real execution retains the `parse_music` binding and
   `music_string`.

Thus the fresh `#Top` results are genuine results for a materially insufficient
specification, not a correctness proof for the HumanEval task.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount satisfies the
mode boundary: `/reference/reference-semantics` is absent. The only trusted
files in `/reference` are `canonical.py`, `prompt.py`, and `py2mpy.py`.
Evidence: `evidence/01-mount-inventory.log`.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts:

- prompt SHA-256:
  `713553ae9220b08678d575238a702f883cc1d37b1986a6bfa010f8d641601d36`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`
are regular files, not symlinks. One structured generation trace is present
and all 234 JSONL records parse. No required source artifact is missing,
changed, mistyped, or symlinked. Evidence:
`evidence/02-source-inventory-and-integrity.log`,
`evidence/03-trusted-and-candidate-sources.log`, and
`evidence/04-generation-record-summary.log`.

The candidate also contains `__pycache__` and three candidate-built definition
trees. These are extra untrusted build products, not source-integrity
failures; none was copied into or used by the reconstruction. The generation
log and final message claim that all 11 claims closed with `#Top`. That claim
was treated only as untrusted provenance and checked afresh below.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From trusted `prompt.py` and `canonical.py`, `parse_music` parses ASCII
space-separated note spellings and returns their beat durations:

- `o` maps to `4`;
- `o|` maps to `2`;
- `.|` maps to `1`;
- empty fields are ignored, as expressed by `if x` in the canonical list
  comprehension.

The decisive intended domain used here contains only those three legal token
spellings and ASCII spaces. No conclusion depends on behavior for an invalid
nonempty note.

### Translation fidelity

Running the trusted translator over the copied `solution.py` and comparing its
stdout with the submitted `solution.mpy` succeeds byte-for-byte. The submitted
MPY SHA-256 is
`1fb428ec561d73756e95f130d99b6985c7157011cdf2b75d0798c6dfb78e7eec`.
Evidence: `evidence/06-translator-byte-identity.log`.

Therefore `solution.mpy` faithfully represents the submitted Python, but that
Python is not faithful to the task. Its `else` branch appends `1` for every
token other than `o` and `o|`, including the empty strings produced by an
explicit-separator split.

### Independent differential

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch copy of `solution.py`. It covers the
documented example, empty and separator-only boundaries, all three branch
values, leading/trailing/repeated separators, every length-one-to-three legal
token sequence, and four separator formats. All 158 exact inputs and their
SHA-256 are recorded in `evidence/07-differential.log`.

The run exits 1 with **117 mismatches**. Representative witnesses are:

| Input | Trusted canonical | Candidate |
|---|---:|---:|
| `""` | `[]` | `[1]` |
| `" "` | `[]` | `[1, 1]` |
| `" o"` | `[4]` | `[1, 4]` |
| `"o "` | `[4]` | `[4, 1]` |
| `"o  .|"` | `[4, 1]` | `[4, 1, 1]` |

The documented example and all well-formed single-token cases agree, which
explains why the candidate's much thinner checks did not expose the defect.
This is a material result divergence on the intended domain.

## 3. Clean proof reconstruction

All source inputs were copied to `/tmp/audit-work/reconstruction`; hashes
confirm that the five candidate source artifacts used for reconstruction equal
their originals. No `*-kompiled` directory or cache from `/candidate` was
reused. Evidence: `evidence/05-scratch-copy.log` and
`evidence/17-scratch-source-hashes.log`.

The live toolchain was K v7.1.293. Fresh builds succeeded:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-PROGRAM-PARSING \
  --output-definition fresh-semantic-llvm-kompiled
Exit 0

kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-PROGRAM-PARSING \
  --output-definition fresh-verification-kompiled
Exit 0
```

Exact logs: `evidence/08-toolchain.log`, `evidence/09-build-llvm.log`, and
`evidence/10-build-haskell.log`.

### Concrete generated-semantics reconstruction

`evidence/concrete_compare.py` ran the freshly compiled LLVM semantics on the
documented example, the three branches, empty and separator-only inputs, and
leading/trailing/repeated separator boundaries. Each `krun` command, exit
status, normalized `<result>`, and output digest is in
`evidence/11-concrete-generated-semantics.log`.

All nine executions terminate at `.K` and match the submitted Python exactly.
For the five empty-field boundaries they disagree with the canonical Python
exactly as the candidate does. This supports the bridge from `semantic.k` to
the submitted program on the tested subset; it does not repair the program.

### Positive claims

For independent claim selection, the auditor copied `spec.k` to
`spec-labelled.k` and added only a module rename and explicit labels.
`evidence/18-labelled-spec-diff.log` records the complete diff, and the
labelled artifact is preserved as `evidence/spec-labelled.k`.

All 11 claims were then run one at a time against the fresh Haskell definition.
Every invocation exited 0 and printed exactly `#Top`. The individual logs are
`evidence/12-proof-audit-*.log`; the driver and summary are
`evidence/run_positive_claims.sh` and
`evidence/12-positive-proof-summary.log`. The untouched aggregate target also
exited 0 with `#Top`:

```text
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
```

Evidence: `evidence/13-proof-original-aggregate.log`.

The mechanical reconstruction gate therefore passes. This confirms closure
under the submitted theory, not adequacy of the theorem.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

None of the 11 claims has an explicit `requires`; each precondition is the
complete source configuration written on its left-hand side.

| Claims | Precondition | Postcondition | Satisfying witness |
|---|---|---|---|
| `spec.k:7-23`, `72-88`, `90-106` | Fresh standard configuration executing `theProgram` and invoking `parse_music` on `o`, `o|`, or `.|` | Execution is consumed; exact function map, final environment, and result `[4]`, `[2]`, or `[1]` | The displayed ground initial configuration |
| `spec.k:26-70` | Same fresh configuration on the documented 11-token example | Execution is consumed and result is exactly `[4,2,1,2,2,1,1,1,1,4,4]` | The displayed ground initial configuration |
| `spec.k:110-155` | An isolated loop whose next element is respectively `o`, `o|`, or `.|`; empty function map; environment exactly `beats -> PREFIX`; `noResult` | One body iteration appends `4`, `2`, or `1`, binds `note`, and leaves `loop(... REST ...)` | `PREFIX = .List`, `REST = .List` |
| `spec.k:159-168` | An isolated empty loop followed by `Return(beats)`; empty function map; environment exactly `beats -> PREFIX` | Computation is consumed and result becomes exactly `PREFIX` | `PREFIX = .List` |
| `spec.k:171-231` | Fresh execution on `o + " " + T`, `o| + " " + T`, or `.| + " " + T` | The program loads and reaches a loop over the first token followed by `splitWords(T)`, with empty beats; result remains `noResult` | `T = ""` for each claim |

The four end-to-end ground results agree with both Python implementations for
their concrete inputs. This substitution is independently visible in
`evidence/11-concrete-generated-semantics.log`. For the bridge witness
`T = ""`, however, the actual inputs are `"o "`, `"o| "`, and `".| "`.
The candidate returns an extra trailing `1`, while the canonical ignores the
empty field. The bridge claims do not constrain any final value and therefore
remain true despite that divergence.

### Pinning assessment

`theProgram`, `parserFunctionBody`, and `parserBranch` are nullary
definition functions that expand to the exact constructor AST in
`solution.mpy`; they do not replace a property-bearing execution with an
oracle. Translator byte identity, source inspection, concrete execution, and
the body-sensitivity test below support this pinning.

As an independent sensitivity check, the auditor changed only the whole-note
body constant from `4` to `9`, rebuilt a separate Haskell definition, and
reran the ground claim that still expected `[4]`. The mutation built and
dry-ran successfully, but proof exited 1 with a reachable final state containing
`[9]`. Artifacts and logs:

- `evidence/verification-body-mutated.k`
- `evidence/spec-body-sensitivity.k`
- `evidence/15-body-mutation-build.log`
- `evidence/15-body-mutation-dry-run.log`
- `evidence/15-body-mutation-proof.log`

The fixed entry claims consequently are body-sensitive and result-constraining.

### Material adequacy gaps

There is no claim with a symbolic input and a final result describing the
token-to-beat mapping. The three symbolic bridges stop before the loop, while
the symbolic loop claims are separate claims rather than a final theorem.

Moreover, the helper loop claims do not match real control flow as complete
configurations:

- after module loading, real `<functions>` contains the `parse_music` binding,
  but every loop/base helper demands `.Map`;
- after invocation, real `<env>` retains `music_string`, but every loop/base
  helper demands a map containing only `beats` initially.

Because those maps are exact and not framed with ellipses, the helper claims
cannot be circularities at the loop state reached by the entry program. Even
if their local transition facts are mathematically true, they do not compose
into the missing universal end-to-end property.

## 5. Rule-by-rule static soundness review

### Local syntax, configuration, and attributes

`semantic.k` locally declares:

- layout whitespace;
- `Pgm = Module(Stmts)`;
- one-or-more `Stmts` and comma-separated `Exprs`;
- `Params(String)` and `CmpOp(String, Expr)`;
- six statement forms: `ImportFrom`, `FuncDef`, `Assign`, `For`, `If`, and
  `Return`;
- eight expression forms: `Name`, `Str`, `Int`, `ListExpr`, `Attribute`,
  `Call`, `Compare`, and `BinOp`;
- five `PyValue` forms: integers, strings, booleans, lists, and `noResult`;
- stored `function(parameter, body)` values;
- 13 internal continuation forms: `invoke`, `store`, `finishReturn`,
  `prepareMethod`, `applyMethod`, `compareRight`, `compareApply`, `binRight`,
  `binApply`, `choose`, `startFor`, `loop`, and `bind`;
- the `splitWords(String)` function;
- an `<mpy>` configuration with `<k>`, `<functions>`, `<env>`, and `<result>`.

`verification.k` adds exactly three nullary syntax/functions:
`parserBranch : Stmts`, `parserFunctionBody : Stmts`, and
`theProgram : Pgm`. Each is marked `[function, total]` and has one
unconditional equation. `semantic.k` marks `splitWords` `[function]` and
marks three prefix equations `[simplification]`.

There are no local `[functional]`, `[concrete]`, priority, `owise`, `anywhere`,
macro, alias, or opaque declarations. The exhaustive machine-extracted
declaration list is `evidence/14-static-declaration-inventory.log`.

### Every semantic rule

| Rule location | Effect | Static decision |
|---|---|---|
| `semantic.k:73` | Unwrap `Module` | Sound. |
| `semantic.k:74` | Sequence the head statement before the remaining statements | Sound left-to-right ordering. |
| `semantic.k:76` | Ignore `ImportFrom` | Sound for the actual `typing.List` import, which has no result effect. Over-broad as a general Python import model, but no false conclusion is enabled on an intended input to this fixed program. |
| `semantic.k:77-78` | Store a function definition in `<functions>` | Sound for the sole definition. |
| `semantic.k:80-82` | Look up a function, install its argument environment, and execute its body | Sound for the sole top-level invocation. It omits frames/environment restoration for general nested calls, which the submitted program does not use. |
| `semantic.k:85` | Evaluate an assignment RHS before storing | Sound. |
| `semantic.k:86-87` | Rebind the named environment entry | Sound for Python name rebinding here. |
| `semantic.k:89` | Evaluate a return expression | Sound ordering. |
| `semantic.k:90-91` | Put the return value in `<result>` | Sound in the actual tail-return context. It does not abruptly discard a later continuation, so it is not a reusable full Python-return semantics; no such later continuation is reachable in this program. |
| `semantic.k:93` | Evaluate an `if` condition before choosing | Sound. |
| `semantic.k:94` | Execute the true branch | Sound. |
| `semantic.k:95` | Execute the false branch | Sound. |
| `semantic.k:97` | Evaluate the iterable before starting a `for` | Sound. |
| `semantic.k:98` | Turn a list value into an internal loop | Sound for list iteration. |
| `semantic.k:99` | End an empty loop | Sound. |
| `semantic.k:100-101` | Bind the head, execute the body, then iterate over the tail | Sound order and finite-list state transition. |
| `semantic.k:102-103` | Bind the current loop variable | Sound. |
| `semantic.k:106` | Convert an integer literal to `pyInt` | Sound. |
| `semantic.k:107` | Convert a string literal to `pyStr` | Sound. |
| `semantic.k:108-109` | Look up a name in `<env>` | Sound for all reached names. Missing bindings stop visibly rather than fabricate a value. |
| `semantic.k:110` | Evaluate the empty list literal | Sound. |
| `semantic.k:111` | Evaluate the used singleton integer list literal | Sound. Other list-expression shapes remain visibly unmodeled. |
| `semantic.k:119-120` | Simplify splitting `"o " + S` to `"o"` followed by `splitWords(S)` | Truthful for explicit-separator splitting. |
| `semantic.k:121-122` | Same for `"o| " + S` | Truthful. |
| `semantic.k:123-124` | Same for `".| " + S` | Truthful. |
| `semantic.k:125-126` | A string with no space splits to the singleton original string, including `""` | Truthful for Python `str.split(" ")`. |
| `semantic.k:127-131` | Split at the first space and recurse on the shorter suffix | Truthful assuming the imported string primitives. The guard descends after a found separator. |
| `semantic.k:133-134` | Begin evaluating a `.split` receiver | Sound for the used method. |
| `semantic.k:135-136` | Evaluate the argument after the receiver | Sound Python evaluation order. |
| `semantic.k:137-138` | Apply explicit-space split to a string receiver | Sound and calls the fully defined `splitWords`. |
| `semantic.k:141-142` | Evaluate comparison left operand first | Sound. |
| `semantic.k:143-144` | Evaluate comparison right operand second | Sound. |
| `semantic.k:145-146` | Apply string equality | Sound; the swapped metavariable names are harmless because equality is symmetric. |
| `semantic.k:148` | Evaluate binary-operation left operand first | Sound. |
| `semantic.k:149-150` | Evaluate its right operand second | Sound. |
| `semantic.k:151-152` | Concatenate left and right lists | Sound for `beats + [n]`. K lists are immutable values, so rebinding models the program's new-list behavior without an aliasing gap. |

The three special `splitWords` simplifications overlap the general
first-separator rule, but their right-hand sides equal one application of that
general rule. They are mutually disjoint by prefix. The two general guards
(`findString == -1` and `findString >= 0`) are disjoint and cover the imported
`findString` contract. There is no competing priority rule.

### Every verification rule

| Rule location | Effect | Static decision |
|---|---|---|
| `verification.k:9-17` | Define `parserBranch` as the exact nested `if` AST from `solution.mpy` | Truthful definitional expansion; it executes ordinary semantic rules. |
| `verification.k:20-25` | Define `parserFunctionBody` as initialization, the `for`, and tail return | Truthful definitional expansion. |
| `verification.k:28-31` | Define `theProgram` as the exact import plus function definition | Truthful definitional expansion. |

All three functions are nullary, so their one unconditional equation completely
covers their domain and cannot overlap another equation. Their `[total]`
attributes do not supply correctness, but their equations do satisfy totality.
They contain the program text, not a precomputed answer or an opaque summary.

### Construct coverage and control/state audit

Every constructor in `solution.mpy` is covered:

| Submitted constructor | Declaration/rules |
|---|---|
| `Module`, adjacent statements | `semantic.k:8,10-11,73-74` |
| `ImportFrom` | `17,76` |
| `FuncDef`, `Params`, invocation | `14,18,48,50,77-82` |
| `Assign`, `Name` | `19,24,85-87,108-109` |
| empty and singleton-int `ListExpr`, `Int` | `26-27,106,110-111` |
| `For` | `20,60-62,97-103` |
| `Call(Attribute(...,"split"), Str(" "))` | `28-29,53-54,115-138` |
| `If` | `21,59,93-95` |
| `Compare`, `CmpOp`, string equality | `15,30,55-56,141-146` |
| `BinOp("+", list, list)` | `31,57-58,148-152` |
| `Return` | `22,52,89-91` |

Module statements, receiver/argument evaluation, comparisons, binary
operations, loop iterations, and branch selection all have the required
left-to-right order. The function and environment maps carry the only mutable
state needed by this program; immutable list construction plus environment
rebinding accurately models `beats = beats + [n]`. No heap, I/O, exception, or
allocation identity can affect an intended execution.

The import, call, return, and literal rules are intentionally narrower than
general CPython semantics. Their broader-language limitations are evidence
gaps for reuse, not unsoundness findings for this fixed program. This review
does **not** label any local K rule unsound, so no false-rule conclusion is
asserted without the required intended-domain witness. The audit failure comes
from the erroneous real program and the missing/ill-connected theorem, not
from a smuggled false semantic equation.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. The auditor created the independent
`evidence/spec-vacuity-audit.k`, copying the true ground `o` entry claim while
changing only its result obligation from `[4]` to the false `[5]`. The
precondition is satisfiable: the standard initial state on input `o`; both
Python implementations return `[4]`.

The mutation parses and builds successfully:

```text
kprove spec-vacuity-audit.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
Exit 0
```

The real proof run exits 1 with `WarnStuckClaimState`. Its reachable residual
has `.K`, environment `beats -> [4]`, and result `[4]`, which cannot match the
mutated `[5]` destination. Evidence:
`evidence/16-vacuity-build-dry-run.log` and
`evidence/16-vacuity-proof.log`.

This is valid non-vacuity evidence for the ground result claim. It cannot
create the absent universal claim or cure the program/canonical divergence.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the submitted K definition:

1. the exact encoded program returns the stated values on `o`, `o|`, `.|`,
   and the documented example;
2. from three artificial isolated loop states, one legal head token appends
   its expected beat and advances to the tail;
3. from an artificial isolated empty-loop state, returning `beats` yields the
   supplied prefix;
4. for each legal first token followed by a space and arbitrary string `T`,
   program loading and invocation reach a corresponding loop over that token
   followed by `splitWords(T)`.

It does **not** establish an end-to-end result for arbitrary valid input, does
not connect the isolated loop claims to the real program's full state, and
does not establish equivalence with the trusted canonical function.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 compiler, LLVM backend, Haskell backend, and reachability prover | All executions and `#Top` results | Necessary toolchain trust; fresh sources and definitions were used. |
| Imported `Int`, `Bool`, `String`, `List`, and `Map` primitives, especially `findString`, `substrString`, `lengthString`, concatenation, and equality | `splitWords`, comparisons, list accumulation, all result claims | Acceptable low-level language/runtime boundary. The used equations are ordinary mathematics; concrete boundary tests provide finite support. |
| Trusted `py2mpy.py` | Python-to-MPY identity | Trusted mounted translator; byte identity was independently established. |
| `theProgram`/body wrappers equal submitted MPY | All spec entry and bridge claims | Statically exact, empirically exercised, and body-sensitive; no opaque value is introduced. |
| Candidate-generated `semantic.k` corresponds to CPython for the used subset | Interpretation of K claims as facts about `solution.py` | Static rule audit plus nine concrete comparisons; this is finite and informal support, not a universal mechanized compiler-correctness theorem. No tested K/candidate mismatch occurred. |
| Submitted Python corresponds to task intent/canonical behavior | Any claimed HumanEval correctness conclusion | **Disproved** by 117 intended-domain differential mismatches. |
| Separate loop facts compose into a universal program theorem | Candidate's informal assertion of arbitrary finite coverage | **Not established**; no such claim exists, and the helper cells do not match reachable program states. |

There are no local opaque symbols or unconstrained result-bearing oracles.
`[function]`, `[total]`, and `[simplification]` are treated only as rewriting
attributes, not as proofs. Differential testing supports only the tested
semantics/Python bridge and, in this case, directly refutes the
implementation/intent bridge.

### Decision

Clean proof reconstruction and non-vacuity pass for the written claims.
Nevertheless, the actual implementation disagrees with the trusted canonical
contract on empty and repeated-space boundaries, and the specification omits
the universal end-to-end result theorem while its purported loop helpers do
not match real program states. This falls squarely under “proves an
insufficient/substituted property” rather than a concern-level evidence
limitation.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
