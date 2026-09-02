# Independent adversarial audit: 8-sum-product

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program under its generated K semantics. A
clean rebuild closed the sole target claim with `#Top`, the claim pins the
byte-identical translated program, all local result-bearing functions are
truthfully and exhaustively defined on their reachable domains, and fresh body
and postcondition mutations both failed for the expected semantic reason.

The outcome is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
individually generated semantics deliberately abstracts all imports as no-ops
and recognizes `sum` and `prod` by literal callee name instead of modeling
Python global/import binding. That abstraction is correct for this exact
program in the ordinary execution environment and no false conclusion witness
exists on the intended list-of-integers input domain. It is nevertheless
over-broad as a reusable Python semantics, and its bridge to CPython is a
reviewed mathematical/informal bridge rather than a machine-checked refinement
theorem.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` does not exist. This is recorded in
`evidence/02-integrity-and-sources.log` with exit 0. There is therefore no
hidden or supplied semantics baseline to seek or compare.

All required candidate source and provenance artifacts are present as regular
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, one structured JSONL trace, `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. A recursive symlink scan found no symlinks. No required artifact is
missing, mistyped, changed, additional, or symlinked.

The candidate prompt is byte-identical to `/reference/prompt.py` (SHA-256
`84dc98e731928675a91c68cbff1f89d0677596f849fa0e6b34fa9b40335fce03`).
The candidate translator is byte-identical to `/reference/py2mpy.py`
(SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
See `evidence/02-integrity-and-sources.log`.

The candidate-provided compiled definitions, `__pycache__`, prose claims, logs,
and trace were treated only as untrusted history. The history claims that the
generation run exited 0 and printed `#Top`; it also records an earlier parser
error that was subsequently repaired. The relevant untrusted claims are
bounded in `evidence/03-untrusted-generation-claims.log`. None was used to
establish the verdict.

Only the eight source artifacts listed in
`evidence/01-source-copy.log` were copied to `/tmp/audit-work/source`.
Candidate `semantic-kompiled/`, `verification-kompiled/`, and caches were not
copied or reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every finite list of ordinary Python integers, `sum_product(numbers)` must
return `(sum of all elements, product of all elements)`. The identities are
sum `0` and product `1`, so the empty-list result is `(0, 1)`. The trusted
canonical implementation initializes those identities and updates both in a
loop. The candidate implementation returns
`(sum(numbers), math.prod(numbers))`.

Both algorithms are equivalent over the intended domain of ordinary integers:
Python integers and K `Int` values are arbitrary precision, and the two
component computations are pure. The candidate has no conditional branch.
The canonical loop boundaries are zero iterations, one iteration, and multiple
iterations.

### Translator fidelity

Running the trusted translator against the scratch copy of `solution.py`
produced `/tmp/audit-work/build/regenerated-solution.mpy`. It is byte-identical
to the submitted `solution.mpy`; both have SHA-256
`d061e06bb15ef17ff9a7b6383328564ad6c802b1d3c8c027474caa9bb9bf3f1e`.
The exact command, `cmp`, hashes, and exit 0 are in
`evidence/04-translator-byte-identity.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point from `/reference/canonical.py` and the generated entry point from
the scratch source copy. Its input manifest is
`evidence/differential-inputs.md`. It covers:

- both documented examples;
- 12 named empty, singleton, zero, sign, and arbitrary-precision boundaries;
- all 9,331 lists of length 0 through 5 over
  `(-3, -1, 0, 1, 2, 4)`; and
- 500 deterministic generated lists of length 0 through 32 with seed 8008.

All 9,845 comparisons matched. The command exited 0 and reported
`mismatches=0`; see `evidence/05-python-differential.log`. This is broad finite
evidence for the Python implementation bridge, not a substitute for the K
reachability proof.

## 3. Clean proof reconstruction

The live toolchain is K `v7.1.293`. `kup` is absent, but independently
installed `kompile`, `krun`, and `kprove` are present and version checks
succeed; see `evidence/06-toolchain.log`.

Fresh definitions were built to new scratch paths:

- LLVM semantics:
  `kompile semantic.k --backend llvm --main-module MPY
  --syntax-module MPY-SYNTAX --output-definition
  /tmp/audit-work/build/semantic-kompiled-fresh`
  exited 0 (`evidence/07-fresh-llvm-kompile.log`).
- Haskell proof definition:
  `kompile verification.k --backend haskell
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
  --output-definition
  /tmp/audit-work/build/verification-kompiled-fresh`
  exited 0 (`evidence/08-fresh-haskell-kompile.log`).

`spec.k` contains exactly one target claim, and `verification.k` contains no
auxiliary claim. Independently running the target with the fresh Haskell
definition printed exactly `#Top` and exited 0:
`evidence/09-positive-claim.log`.

Because this is generated semantics, I also executed the fresh LLVM definition
on six normal and boundary inputs: empty, singleton, the documented four
elements, a zero-containing mixed-sign list, an all-negative list, and an
arbitrary-precision case. `evidence/concrete_semantics_compare.py` records each
exact `krun` command and compares the parsed K result with both Python
implementations. Every `krun` exited 0 and all six results matched; see
`evidence/10-generated-semantics-concrete.log`.

These results establish a successful clean dynamic reconstruction independent
of every candidate-provided definition and prior `#Top`.

## 4. Adequacy and real-program pinning

### Entry precondition and postcondition

There is one entry claim and no `requires` clause. Its complete modeled
precondition is:

- `<k>` contains the exact submitted `Module(...)` constructor term;
- `<input>` is `PyList(IS)` for an arbitrary finite K `Ints` list;
- `<functions>` is the empty map; and
- `<result>` is empty computation.

Its postcondition consumes `<k>`, leaves the input unchanged, installs exactly
the `sum_product` closure represented by the submitted body, and changes the
result to:

`expectedSumProduct(IS) =
PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))`.

Thus both tuple components are constrained. There is no free result variable,
tautology, implication-only weakening, framed alternative result, helper
claim, or loop circularity.

The `<k>` source term in `spec.k` and `solution.mpy` compare equal after
whitespace removal. The normalized terms, `cmp`, one target-claim count, and
zero auxiliary-claim finding are recorded in
`evidence/12-program-pinning.log`. The submitted algorithm has no helper or
loop to summarize; all its real control flow executes through the semantics.

### Satisfiable entry states and concrete substitutions

A satisfying state is obtained with `IS = .Ints`, the exact module in `<k>`,
`<input> PyList(.Ints)`, an empty function map, and an empty result. Another is
`IS = 1, 2, 3, 4, .Ints`. The reviewer-authored ground claims in
`evidence/ground-instantiations.k` substitute these inputs and require,
respectively, `(0,1)` and `(10,24)`. Both claims close together with `#Top`
under the fresh definition (`evidence/11-ground-instantiations.log`), and both
results match the trusted canonical and generated Python executions in
`evidence/05-python-differential.log` and
`evidence/10-generated-semantics-concrete.log`.

### Body sensitivity

`evidence/body-sensitivity-mutation.k` changes the second body component from
`prod(numbers)` to `sum(numbers)` on satisfying input `[2,3]`, while retaining
the original `(5,6)` result obligation. It parses/builds with `--dry-run` and
exit 0 (`evidence/13-body-mutation-build.log`). The proof then exits 1 with a
`WarnStuckClaimState` whose reachable result is concretely `(5,5)`, not
`(5,6)` (`evidence/14-body-mutation-proof.log`). The theorem is therefore
sensitive to the executed body; no proof-local bridge bypasses it.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.md` is the exhaustive inventory. It enumerates all 19
local syntax/configuration/function declarations, all 17 semantic rules or
function equations, the one verification equation, the sole target claim, and
the mapping from every submitted constructor to its behavior. The source scan
is in `evidence/17-static-source-scan.log`. Candidate K sources consist only of
`semantic.k`, `verification.k`, and `spec.k`; there are no helper K files.

The configuration is adequate for the used subset: computation, input, a
function map, and result. The exact program has no mutable local state, heap,
allocation, I/O, exceptions on its formal domain, or control stack. Statement
sequencing preserves order; function definition precedes entry invocation;
invocation selects the installed closure, binds its single parameter, and
changes only control/result; name lookup is from the one-entry environment.
Tuple evaluation contains two pure operations, so the semantics' lack of an
observable left-to-right sequencing cell cannot alter a result or state on
ordinary integer lists.

All overlaps are disjoint by constructor, empty/nonempty list shape, or
literal callee name. There are no guards, priority rules, simplification rules,
`[functional]` declarations, fresh variables, or opaque local result-bearing
symbols. The three `[total]` functions have complete coverage:

- `sumInts`: `0` on empty, head plus recursive tail on nonempty;
- `productInts`: `1` on empty, head times recursive tail on nonempty; and
- `expectedSumProduct`: one unguarded equation for every `Ints`.

The two folds descend structurally and use the trusted K integer primitives.
The non-total functions `eval`, `sumValue`, `productValue`, and `lookupValue`
cover every reachable exact-program use and visibly remain unreduced for
unsupported terms.

`sumInts` and `productInts` occur in both execution and the postcondition, but
this is not an unconstrained-oracle pattern: their values are completely fixed
by truthful, disjoint recursive equations on every `Ints` ground term.
`expectedSumProduct` is a definitional mathematical summary and does not
replace execution. The body-sensitivity mutation independently confirms that
changing a program call changes the reachable result and breaks the proof.

The two task-scoped limitations are:

1. `ImportFrom(_,_) => .K` matches more imports than its justification covers.
   For the fixed module, the `typing` import has no relevant runtime effect and
   `math.prod` is modeled by its ordinary fixed primitive semantics. The
   semantics would not be sound as a general model of arbitrary Python
   imports.
2. `sum` and `prod` are dispatched by literal name rather than a modeled
   Python global environment. This agrees with the exact unshadowed program in
   its ordinary module environment but excludes monkey-patching, import
   failure, and exotic binding changes.

Under the instruction requiring an intended-domain false-conclusion witness
before labeling a rule unsound, neither limitation is an unsoundness finding:
for every intended finite list of ordinary integers, the exact fixed program's
observable pair is preserved. The limitations are instead the reason for the
`CONCERNS` verdict. No rule encodes a false task answer, fabricates an
unconstrained result, skips program-defined code, or proves a substituted
program.

The first attempted reviewer source-scan command exited 1 solely because a
no-match `rg` in a command substitution interacted with `pipefail`; its log is
preserved as `evidence/17a-static-source-scan-initial.log`. The corrected scan
exited 0. This was a reviewer diagnostic issue, not candidate or proof
evidence.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation was trusted.
The fresh mutation is `evidence/false-postcondition-mutation.k`. It keeps the
exact submitted program and satisfying input `[1,2,3,4]` but changes only the
result-constraining sum component from the true `10` to false `11`, retaining
product `24`.

The mutated spec parses and builds successfully with `kprove --dry-run`, exit
0 (`evidence/15-false-postcondition-build.log`). Its actual proof exits 1 with
`WarnStuckClaimState`; the residual is a fully executed configuration
containing `(10,24)`, which does not unify with required `(11,24)`. See
`evidence/16-false-postcondition-proof.log`. This is the expected unmet result
obligation, not a parser error, missing import, timeout, unrelated crash, or
unreachable mutation.

The positive claim is therefore discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What is formally established

Relative to the freshly compiled `MPY`/`VERIFICATION` definition, for every
finite `IS:Ints`, executing the exact submitted `solution.mpy` module from the
entry configuration with input `PyList(IS)` reaches empty control, installs the
exact submitted closure, and returns the tuple of the recursively defined
integer-list sum and product. Empty identities are formally fixed to `0` and
`1`. This is a universal K reachability result over the formal integer-list
domain, not merely the finite tests.

The proof does not establish behavior for non-integer elements, infinite
inputs, Python integer subclasses with effects, monkey-patched globals,
arbitrary import environments, import errors, or other programs admitted by
parts of the syntax. These are outside the stated HumanEval domain and the
minimal generated semantics.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Trusted prompt and canonical implementation | Natural-language intent and independent executable oracle | Mounted trusted inputs; prompt/translator integrity checked. The canonical is used for testing and intent comparison, not as a K axiom. |
| Trusted translator | Link from `solution.py` AST to `solution.mpy` | Byte identity was independently regenerated. Translator correctness itself is an explicit trusted input. |
| K toolchain and `domains.md` | Parsing, rewriting, proof search, `Int`, `String`, `Map`, `+Int`, `*Int`, and map operations | Standard low-level trust boundary. Fresh builds and dynamic tests check use, not implementation correctness of K. |
| Python builtin `sum` and `math.prod` contracts on ordinary integer lists | Meaning of the two external operations used by the program | Fixed external primitives, not program-defined code. Their K values are not opaque: R12-R17 define the standard folds completely. The bridge to actual CPython is static mathematical reasoning plus concrete evidence, not a machine-checked CPython refinement theorem. |
| Import/global-name abstraction | Selection of those two primitives | Sound for the exact unshadowed submitted module in the ordinary environment; concerning as a general semantics. No intended-domain false result witness was found. |
| `expectedSumProduct` | Final postcondition | Not assumed or opaque. Its one total equation fixes both components using the fully defined folds. |

There are no local opaque symbols, empirical oracles in the proof, unproved
helper claims, simplification axioms, operational shortcuts, or circular
program summaries. The 9,845-case Python differential and six K/Python
concrete comparisons support only the implementation/semantics bridges they
test; they are not presented as universal proof.

Gate A (real-program soundness) passes: exact body execution, state/control
fidelity on the modeled domain, truthful equations, satisfying witnesses, body
sensitivity, and non-vacuity are all present. Gate B (intent adequacy) passes
for finite ordinary-integer lists, with the task-scoped binding/import
limitation documented. Gate C (trust and auditability) passes: assumptions and
finite evidence are explicit and reproducible. The binding/import abstraction
and absence of a machine-checked CPython refinement justify concerns, but do
not invalidate the legitimate theorem about the real generated program on its
intended domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
