# Independent adversarial review: 53-add

The candidate contains a legitimate, universal partial-correctness proof of the
submitted integer-addition program. I did not reuse its compiled definitions or
accept its prior `#Top`; both K backends and every audit probe were rebuilt from
source in `/tmp/audit-work/53-add-clean`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the rendered mode and
mount topology agree.

The independent checker in
[provenance_check.py](/audit-output/evidence/provenance_check.py) established:

- `/audit-campaign-lock.json` is a real regular file, its SHA-256 is
  `ad5dfc...d745`, and its parsed object exactly equals the
  `audit_campaign` block in `/audit-input.json`.
- All required legacy-selected-stage1 records are real and readable:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json`
  is present and was also checked. Every recorded per-file hash matches.
  Historical `runtime-metrics.json` is not required for this legacy layout.
- The retained candidate tree recomputes to pipeline digest
  `03f83b...cb60`, exactly the invocation's recorded retained-workspace hash.
  The one-file structured trace recomputes to both its recorded file hash
  `023d71...da2` and recorded tree hash `be8d56...2d63`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts and match their recorded hashes.
- The candidate and trusted `reference-semantics/` trees each contain the same
  25 regular entries, with identical relative paths, types, and file hashes.
  There are no missing, additional, mistyped, or symlinked entries. Both
  recompute to the recorded manifest digest `4e0639...789f`; the trusted
  file-only legacy digest also recomputes to `36288f...e26`.

The complete results and exact command are in
[01-provenance-check.log](/audit-output/evidence/01-provenance-check.log).
The structured trace contains 120 valid JSON records. Its summarized tool
history shows that the generator first invoked `kprove` without the required
spec-module selection and received exit 113, then used
`--spec-module ADD-SPEC` and received exit 0 with `#Top`. The final `prove.sh`
contains the corrected command. This history is untrusted generation evidence,
not proof evidence; its independent inspection is recorded in
[01-generation-trace-summary.log](/audit-output/evidence/01-generation-trace-summary.log).

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires:

> For two integer parameters `x` and `y`, `add(x, y)` returns their arithmetic
> sum. The examples are `add(2, 3) == 5` and `add(5, 7) == 12`.

The trusted canonical body is `return x + y`. The submitted
[solution.py](/candidate/solution.py:1) has the same signature and body, with no
branches, hidden bounds, state, or helper calls.

Running the trusted translator on the scratch copy produced a file byte-for-byte
identical to submitted `solution.mpy`, with SHA-256
`67c61c...98ee`. The exact command, both hashes, and exit 0 are in
[02-translation-identity.log](/audit-output/evidence/02-translation-identity.log).
The constructor term is:

`Module(FuncDef("add", Params("x", "y"), Return(BinOp("+", Name("x"), Name("y")))))`.

The independent differential test imports the trusted canonical and submitted
entry points separately. It covers both examples; zero, sign, cancellation,
64-bit overflow, and arbitrary-precision boundaries; every pair in
`[-8,8] x [-8,8]`; and 128 deterministically generated signed integers up to
256 bits. All 429 input pairs and outputs are preserved in
[02-python-differential.log](/audit-output/evidence/02-python-differential.log):
the mismatch count is 0 and the command exits 0. “Empty input” is inapplicable
to two scalar parameters, and the program has no branch boundary.

The formal domain is all K `Int` values. This is not a finite-size restriction:
K integers and CPython integers are unbounded, and it covers the prompt's
`x: int, y: int` domain.

## 3. Clean proof reconstruction

The installed `kompile`, `krun`, and `kprove` independently report K
v7.1.293; see
[03-tool-versions.log](/audit-output/evidence/03-tool-versions.log).
No candidate-built definition was copied into scratch.

Fresh commands and results:

1. `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled`
   exited 0. The compiler's unrelated non-exhaustiveness warnings are preserved
   in [03-kompile-llvm.log](/audit-output/evidence/03-kompile-llvm.log).
2. `krun concrete-tests.mpy --definition reviewer-runtime-kompiled` exited 0
   with `.K`, empty heap/stack, `NoExc`, and exit code 0 after checking the two
   prompt examples and `add(-10,3) == -7`; see
   [03-krun-concrete-tests.log](/audit-output/evidence/03-krun-concrete-tests.log).
3. `kompile verification.k --backend haskell --main-module ADD-VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-verification-kompiled`
   exited 0; see
   [03-kompile-haskell.log](/audit-output/evidence/03-kompile-haskell.log).
4. `kprove spec.k --definition reviewer-verification-kompiled --spec-module ADD-SPEC`
   exited 0 and printed `#Top`; see
   [03-kprove-positive.log](/audit-output/evidence/03-kprove-positive.log).

`spec.k` contains exactly one positive target claim, so every positive target
was reconstructed and closed.

## 4. Adequacy and real-program pinning

The entry claim has no side condition beyond its sorts. In plain language, its
precondition is:

- `X` and `Y` are arbitrary K integers;
- execution starts in module environment 0;
- module scope 0 is empty and has the builtins scope at location -1 as parent;
- the next scope location is 1;
- heap and call stack are empty, return state is `noRet`, exception state is
  `NoExc`, and exit code is 0.

Its postcondition says that the `<k>` result is exactly `X +Int Y`, module scope
0 contains the `add` closure with the exact submitted parameter list and body,
and every other listed cell has returned to its initial value. The result is
neither free nor guarded by a one-way implication.

The sole candidate rule does not summarize addition. It replaces the fresh
entry marker `#callAdd(X,Y)` with:

1. `#loadAll` of the complete submitted module constructor; then
2. an ordinary fixed-semantics call to the dynamically loaded `"add"` binding
   with `Int(X)` and `Int(Y)`.

The mechanical balanced-parenthesis extraction in
[term_pinning_check.py](/audit-output/evidence/term_pinning_check.py) proves that
the loaded constructor term and submitted `solution.mpy` are textually equal
after removing whitespace outside strings. Both normalized terms have SHA-256
`afde83...377`; the call and result-constraining entry shape are also checked in
[04-term-pinning.log](/audit-output/evidence/04-term-pinning.log).

Concrete initial states exist. Reviewer-authored claims for `(2,3)`,
`(-10,3)`, and `(2^63-1,1)` satisfy the exact precondition and close with
`#Top`; see
[spec-instances.k](/audit-output/evidence/spec-instances.k) and
[04-kprove-satisfying-instances.log](/audit-output/evidence/04-kprove-satisfying-instances.log).
Their claimed results `5`, `-7`, and `2^63` agree with both Python
implementations in the differential record.

There is no helper or loop claim to pin. The theorem covers the complete
annotated integer domain rather than examples or bounded unrollings.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is in
[05-rule-inventory.log](/audit-output/evidence/05-rule-inventory.log), generated
by [k_rule_inventory.py](/audit-output/evidence/k_rule_inventory.py). It
enumerates all 931 local records:

- 228 syntax declarations, including every function/total/opaque/macro and
  strictness attribute;
- one configuration and five evaluation contexts;
- 696 ordinary semantic rules, including all guards, `priority`, `owise`, and
  concrete-only attributes;
- the one candidate harness rule and the one target claim.

The attribute inventory finds 148 `function`, 110 `total`, 25 `symbol`, 25
`no-evaluators`, 52 priority, 30 `owise`, 55 concrete, three macro, one
macro-rec, three strict, and one seqstrict occurrences. There are no local
`functional` or `simplification` declarations.

### Target construct and rule map

| Submitted construct | Declaration and material behavior |
|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k` expands `#loadAll`, sequences the sole `FuncDef`, and removes `.Stmts`. |
| `FuncDef`, `Params` | `functions.k` installs `closureVal(("x","y"), body, 0)` in the current module scope. |
| `Call`, `Name("add")` | `call.k` evaluates the callee before arguments; `core.k` lookup finds the newly installed module binding, not a builtin. |
| `Int(X)`, `Int(Y)` | `core.k` converts literal constructors to the same K integers; the shared argument loop evaluates left-to-right and preserves order. |
| function frame and binding | `call.k` allocates a fresh scope, pushes the exact continuation, and `functions.k` binds `x` then `y`; the empty-frame guards exclude the cell-binding priority rule. |
| `Return(BinOp(...))` | `Return` strictness evaluates the expression; `BinOp` seqstrictness evaluates `x` then `y`; both lookups resolve in the callee frame. |
| integer `+` | `operators.k` dispatches cooled integer operands to `applyBin`; `int.k` has the general equation `applyBin("+", I1:Int, I2:Int) => I1 +Int I2`. |
| return/pop | `functions.k` records the value, discards only the callee remainder, restores the saved caller continuation and environment, removes the callee frame, and leaves the module closure intact. |

The active overlaps are controlled and disjoint on this state: cell lookup and
cell parameter binding require a `"$cells"` marker absent from the ordinary
frame; ref/list/float operator rules cannot match `Int` operands; syntactic
math/hash call interceptions cannot match `Call(Name("add"),...)`. No active
priority rule preempts the integer-add path, and no local equation is recursive
on a non-decreasing argument.

`verification.k` adds no function, totality declaration, opaque symbol, lemma,
or result rewrite. Its `#callAdd` rule is a definitional execution harness for a
fresh marker, not an operational bridge over an existing program term: it
skips no fixed behavior, preserves an arbitrary following continuation, and
touches no state cell. Consequently it needs no program-derived oracle or
connection theorem; its right-hand side is the actual program execution whose
constructor identity was checked above.

As a sensitivity test independent of postcondition mutation, I changed the
program term actually loaded and executed from `BinOp("+",...)` to
`BinOp("-",...)`, while updating the expected final closure to the mutated
body. The altered definition builds successfully, but its claim still demanding
`X +Int Y` exits 1 with a reachable residual requiring
`X -Int Y = X +Int Y`. Evidence:
[verification-body-mutation.k](/audit-output/evidence/verification-body-mutation.k),
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k),
[05-kompile-body-mutation.log](/audit-output/evidence/05-kompile-body-mutation.log),
and
[05-kprove-body-mutation.log](/audit-output/evidence/05-kprove-body-mutation.log).

The supplied semantics deliberately imports much more than this program uses.
The inventory marks 20 inactive modeling limitations, including restricted
ASCII/string behavior, shallow symbolic equality for nested heap objects,
restricted `eval`/conversion behavior, snapshot list iteration, and the
no-escaping-closure frame discipline. These are not evidence of an unsound
target theorem: none of their left-hand sides or opaque results is reachable
from the submitted constructor on any integer input, so none can enable a false
conclusion on the intended domain. For example, the restricted
multi-character `int(str)` and arithmetic-`eval` rules differ from CPython on
nonnumeric or `/` inputs, but this program constructs no string, builtin call,
collection, float, import, branch, or loop. The active frame-pop assumption is
satisfied because `add` creates and returns no closure.

I found no answer-encoding rule, unconstrained result oracle, fabricated used
operation, or false rule conclusion reachable on the intended integer domain.

## 6. Fresh non-vacuity test

The reviewer mutation changes only the result obligation to
`(X +Int Y) +Int 1` while retaining the actual program and all final-state
constraints. It is demonstrably false at the satisfying input `X=2,Y=3`,
where it demands `5 = 6`.

`kprove ... --dry-run` exits 0 and emits the backend command, establishing that
the distinct spec parses and builds; see
[06-vacuity-dry-run.log](/audit-output/evidence/06-vacuity-dry-run.log).
The real proof then exits 1 with `WarnStuckClaimState` at the reachable terminal
configuration. Its residual is precisely the failed implication between
`X +Int Y` and `X +Int Y +Int 1`, not a parser error, timeout, missing import,
or unrelated crash. The artifact and complete output are
[spec-vacuity-reviewer.k](/audit-output/evidence/spec-vacuity-reviewer.k) and
[06-kprove-vacuity-mutation.log](/audit-output/evidence/06-kprove-vacuity-mutation.log).

The proof is therefore result-sensitive and non-vacuous.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics, from the exact standard initial configuration
and for every K integer `X,Y`, executing the exact translated submitted module,
looking up its newly defined `add`, calling it with `X,Y`, evaluating its real
body, and returning normally reaches result `X +Int Y`. The module retains the
exact `add` closure, and scope counter, heap, heap counter, stack, return,
exception, and exit-code cells have the specified final values.

This is a partial-correctness statement about the actual submitted program, not
a proof that an external summary has a desired meaning.

### Trust boundary and assumptions

- **K implementation and built-in domains.** The result depends on
  `kompile`/`kore-exec`, K's rewrite/reachability logic, unbounded `+Int`, and
  the imported `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, and `K-EQUAL` primitives.
  On the active path, map lookup/update, stack framing, and mathematical integer
  addition are the material primitives. These are the ordinary low-level K
  trust boundary, not task-answer axioms.
- **Supplied MPY rules.** The active module-load, binding, call, strictness,
  lookup, integer dispatch, return, and frame rules are trusted as the supplied
  language semantics after the static review above. Their state footprint and
  control behavior were also exercised by fresh concrete execution, ground
  claims, body sensitivity, and the universal proof.
- **Translator bridge.** The fixed translator is trusted to represent the
  simple CPython AST by its homomorphic constructors. This particular output was
  regenerated byte-identically, and the claim's embedded module was
  mechanically compared to it. There is no automatic source-to-spec generation,
  but that is only a maintenance observation for this immutable candidate.
- **Contract interpretation.** Treating the prompt annotations `x: int,
  y: int` as the intended integer domain is an informal HumanEval intent bridge.
  The formal claim does not cover floats, strings, booleans as Python's
  `int` subclass, overloaded objects, or arbitrary values supporting `+`.
  Those are outside the annotated source contract, so this is not a material
  narrowing.
- **Empirical bridge.** The 429-case CPython differential and three LLVM
  assertions support candidate/canonical and concrete-semantics agreement only
  on their recorded finite inputs. They do not replace the universal K proof.

All proof-definition opaque symbols are inherited from unrelated supplied
modules and are inactive here. The complete list is:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None influences a branch,
state cell, returned value, or postcondition in this proof. There is no
candidate-defined opaque symbol, empirical oracle, proof-local summary, or
unproved lemma.

The evidence index is
[evidence/INDEX.md](/audit-output/evidence/INDEX.md). Gates A (real-program
soundness), B (intent adequacy), and C (trust/evidence auditability) all pass.

VERDICT: PASS
LEGITIMACY: LEGIT
