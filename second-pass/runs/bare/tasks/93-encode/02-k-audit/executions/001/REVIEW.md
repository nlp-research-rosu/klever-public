# Independent adversarial audit — 93-encode

## Executive decision

The submitted Python implementation appears correct, its `.mpy` translation is
authentic, the generated concrete semantics behaves correctly on the tested
domain, and all four submitted positive K claims reconstruct successfully.
Nevertheless, the candidate is **not a legitimate partial-correctness proof of
the requested entry point**.

There are two decisive proof defects:

1. There is no universal entry-point claim. The only symbolic theorem starts
   at the internal `loopString` control term. The three entry claims are ground
   executions for only three fixed strings.
2. The symbolic theorem is proved with a fused operational rule that replaces
   the program-defined loop body by the result-bearing symbols
   `encodedChar` and `advancedVowel`, while those symbols (and
   `swapCaseChar`) have no equations in the proof definition. The postcondition
   defines `encodeSpec` using that same opaque `encodedChar`. This is a
   circular/oracle-parametric summary, not a connection to execution of the
   Python body.

The required concrete false-conclusion witness is input `"a"`. A legal total
interpretation of the candidate's opaque symbols as `encodedChar(_) = "X"`
made K prove both the exact entry execution `encode("a") == "X"` and the
corresponding loop claim with `#Top`; the trusted and submitted Python
implementations both return `"C"`. See
[oracle-witness.k](/audit-output/evidence/oracle-witness.k),
[false-entry log](/audit-output/evidence/15-wrong-oracle-false-entry.log),
[false-loop log](/audit-output/evidence/16-wrong-oracle-false-loop.log), and
[Python counterexample](/audit-output/evidence/17-wrong-oracle-python-counterexample.log).
The correct equations in `concrete.k` provide one empirically credible
interpretation, but the abstract target proof does not import them and proves
no connection theorem.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` is absent. This is the required condition, so
there is no infrastructure breach and no hidden reference semantics was used.
The check and source hashes are in
[01-provenance-integrity.log](/audit-output/evidence/01-provenance-integrity.log).

### Untrusted generation claims

- [run-input.json](/candidate/run-input.json) identifies problem `93-encode`,
  generation condition `bare`, no supplied semantics, and the prompt and
  translator hashes later verified independently.
- [metrics.json](/candidate/metrics.json) claims exit 0, no timeout, and a
  1,589-second generation.
- [codex-last.txt](/candidate/codex-last.txt),
  [codex-output.log](/candidate/codex-output.log), and the structured trace at
  `/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-12-04-019f8986-8c42-7d41-ae4c-953c93b53c81.jsonl`
  claim that `prove.sh` exited 0 and two grouped `kprove` commands printed
  `#Top`. These were treated only as claims; none of their builds or caches was
  reused.

### Integrity results

- Candidate [prompt.py](/candidate/prompt.py) is byte-identical to
  `/reference/prompt.py` (SHA-256
  `856a164439599802d5210e2969c1c5673c84b83b4bdca5db34384d7b10d3d741`).
- Candidate [py2mpy.py](/candidate/py2mpy.py) is byte-identical to
  `/reference/py2mpy.py` (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- All required audit metadata and submitted sources—`solution.py`,
  `solution.mpy`, `semantic.k`, `concrete.k`,
  `concrete-verification.k`, `verification.k`, `spec.k`, and `prove.sh`—are
  regular, non-symlink files. No symlink exists anywhere under `/candidate`.
- The one structured trace is a regular JSONL file. The complete top-level and
  symlink inventory is
  [01b-candidate-artifact-inventory.log](/audit-output/evidence/01b-candidate-artifact-inventory.log).
- No required submitted source is missing, changed against a trusted
  counterpart where one exists, mistyped, or symlinked.
- Extra untrusted generated material is present:
  `verification-kompiled/`, `concrete-verification-kompiled/`,
  `__pycache__/`, and `kore-exec.tar.gz`. It was ignored. `codex-trace/`,
  the metadata files, and logs were read only as provenance claims.
- No candidate `PROOF.md` or `spec-vacuity.k` exists. Neither was a required
  generation deliverable; a fresh reviewer mutation was created in Stage 6.

All source artifacts needed for execution were copied to
`/tmp/audit-work/93-encode`; only those clean copies were built or mutated.
The live tools were K `v7.1.293` and Python `3.10.12`
([00-toolchain.log](/audit-output/evidence/00-toolchain.log)).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, `encode(message)` swaps
letter case and replaces each vowel—case-insensitively—with the character two
English-alphabet positions later. The trusted implementation first calls
`swapcase`, then maps every resulting member of `aeiouAEIOU` through
`chr(ord(character) + 2)`. The required examples are:

- `encode("test") == "TGST"`
- `encode("This is a message") == "tHKS KS C MGSSCGG"`

The prose says “Assume only letters,” while the second example contains
spaces. I therefore treated ASCII English letters plus the demonstrated space
as the intended domain. The canonical Python function itself is defined on
broader strings, but the generated K character semantics is only an ASCII
model.

### Submitted implementation

[solution.py](/candidate/solution.py) iterates left-to-right, advances an
original ASCII vowel by two, then swaps the resulting character's case and
appends it. For ASCII vowels this commutes with the canonical implementation's
case swap because both upper- and lowercase vowels are recognized. For
nonvowels it simply swaps case. The loop handles the empty string.

### Translation identity

Running the trusted scratch copy of `py2mpy.py` over the scratch
`solution.py` produced SHA-256
`041d179bebc6e816f36536b78fe1bdee2f727614fef76283398c99a5d3c86666`,
byte-identical to submitted `solution.mpy`. Exact command, hashes, comparison,
and exit 0 are in
[02-translator-regeneration.log](/audit-output/evidence/02-translator-regeneration.log).

### Independent differential testing

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical entry point and the scratch submitted entry point
independently. Its reproducible input set is
[differential-inputs.json](/audit-output/evidence/differential-inputs.json).
It covers:

- both documented examples and the empty string;
- every lower- and uppercase vowel and representative nonvowel boundaries;
- every single ASCII letter/space;
- all 2,809 ordered pairs of ASCII letters/space;
- lower and uppercase alphabets, alternating branches, repeated spaces;
- 1,000 seeded generated strings of lengths 0–64; and
- a 4,096-character boundary string.

All 3,873 cases agreed, with zero mismatches and exit 0
([03-python-differential.log](/audit-output/evidence/03-python-differential.log)).
This supports program-to-canonical fidelity on the tested domain; it is finite
evidence, not a K proof.

## 3. Clean proof reconstruction

Candidate-provided kompiled definitions, binaries, caches, and `prove.sh`
outputs were not used.

### Fresh builds

- Abstract proof definition:
  `kompile verification.k --backend haskell --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  audit-verification-kompiled` — exit 0
  ([04-build-abstract.log](/audit-output/evidence/04-build-abstract.log)).
- Concrete definition:
  `kompile concrete-verification.k --backend haskell
  --main-module CONCRETE-VERIFICATION --syntax-module MPY-SYNTAX
  --output-definition audit-concrete-verification-kompiled` — exit 0
  ([05-build-concrete.log](/audit-output/evidence/05-build-concrete.log)).

### Every positive claim, run independently

| Claim | Fresh result |
|---|---|
| `SPEC.encode-loop-correct` | `#Top`, exit 0; [log](/audit-output/evidence/06-proof-loop.log) |
| `CONCRETE-SPEC.example-test` | `#Top`, exit 0; [log](/audit-output/evidence/07-proof-example-test.log) |
| `CONCRETE-SPEC.example-message` | `#Top`, exit 0; [log](/audit-output/evidence/08-proof-example-message.log) |
| `CONCRETE-SPEC.ascii-domain` | `#Top`, exit 0; [log](/audit-output/evidence/09-proof-ascii.log) |

The symbolic loop log repeatedly warns that `encodedChar` and
`advancedVowel` have no evaluators. That is evidence of the opaque proof
boundary analyzed below, not a reconstruction failure.

### Fresh concrete generated-semantics execution

The rebuilt concrete definition directly executed regenerated
`solution.mpy`. Empty input, lower- and uppercase vowel/nonvowel pairs, every
vowel with spaces, the long example, and the combined ASCII domain all
terminated and returned exactly the same strings as both Python
implementations. Six cases, zero mismatches, all `krun` exits 0:
[11-k-concrete-boundaries.log](/audit-output/evidence/11-k-concrete-boundaries.log).
An unbounded raw configuration for `"test"` is also preserved in bounded form
at [10-krun-example-test.log](/audit-output/evidence/10-krun-example-test.log).

Thus the dynamic reconstruction gate passes: every positive target closes and
the concrete generated semantics executes the submitted constructor tree on
normal and boundary inputs.

## 4. Adequacy and real-program pinning

### Plain-language claim restatement

1. `SPEC.encode-loop-correct`: for arbitrary K strings `S`, `C`, `M`, and
   `R`, arbitrary `<functions>` map `FS`, and arbitrary existing result `RES`,
   start at the internal term
   `loopString("char", S, encodeLoopBody())` with exactly `char`, `message`,
   and `result` bindings. If the loop reaches its destination, `<k>` is empty,
   `message` is still `M`, and `result` is
   `R +String encodeSpec(S)`; final `char` is existential and the other cells
   are unchanged. There is no `requires` clause beyond K sorts.
2. `example-test`: the exact encoded program plus invocation on `"test"`,
   from empty state, reaches empty `<k>` and returned string `"TGST"`.
3. `example-message`: the same ground entry execution for
   `"This is a message"` returns `"tHKS KS C MGSSCGG"`.
4. `ascii-domain`: one fixed input containing all 52 ASCII letters and one
   space returns the fixed displayed 53-character result.

### Satisfiability

Every entry precondition is realizable:

- Each ground claim starts from the initial empty cells generated by the
  configuration.
- The loop claim is satisfied, for example, by `S = "ab"`, `C = "x"`,
  `M = "ab"`, `R = "P"`, `FS = .Map`, and `RES = noResult`.

The ground loop instance proved `#Top` with final result `"PCB"`
([adequacy-witness.k](/audit-output/evidence/adequacy-witness.k),
[12-adequacy-ground-witness.log](/audit-output/evidence/12-adequacy-ground-witness.log)).
Both Python implementations return `"CB"` on `"ab"`, so with prefix `"P"`
they agree with `"PCB"`
([13-adequacy-python-witness.log](/audit-output/evidence/13-adequacy-python-witness.log)).
The three ground entry substitutions are also checked by the positive claims
and differential evidence.

### Program and body identity

The concrete `krun` commands parse and execute the actual regenerated
`solution.mpy`. The ground proof claims use the nullary function
`encodeProgram()`, whose equation expands constructor-for-constructor to the
same `Module(FuncDef(...))` tree. The symbolic helper uses
`encodeLoopBody()`, whose equation is the exact translated `If` followed by
`AugAssign`. This static mapping is exhaustively recorded in
[rule-inventory.md](/audit-output/evidence/rule-inventory.md).

Consequently the ground entry claims pin the submitted program. The symbolic
claim pins the exact internal loop syntax, but not its actual value semantics:
the high-priority loop rule bypasses execution of that syntax.

### Adequacy failure

There is no claim of the necessary shape
`encodeProgram() ~> invoke("encode", pyStr(M)) => .K` for symbolic `M` with
returned value equal to an independently meaningful encoder. The only
universal-looking claim begins after function definition, invocation, initial
assignment, `For` evaluation, and loop entry.

Although its final `result` is syntactically constrained, `encodeSpec` is
recursively defined from the same opaque `encodedChar` inserted by the fused
execution rule. It therefore does not constrain the result to the natural
language contract. The three concrete entry claims prove three fixed examples,
not all intended inputs.

Stage 4 fails.

## 5. Rule-by-rule static soundness review

The exhaustive declaration and rule inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). It enumerates
every local syntax production, state/control constructor, function,
`[total]` declaration, opaque symbol, configuration cell, ordinary rule,
priority/`owise` rule, simplification, helper equation, and claim in
`semantic.k`, `concrete.k`, `concrete-verification.k`, `verification.k`, and
`spec.k`. There are no local `[functional]` declarations.

### Construct coverage and ordinary execution

Every constructor actually used by `solution.mpy` is both declared and
modeled. The configuration has only the needed computation, environment,
function, and result cells. For the submitted one-function program:

- module sequencing and function registration are ordered correctly;
- the one parameter is bound to the already supplied string argument;
- assignment and `+=` update the environment;
- string iteration takes the first character and then the suffix;
- the ten vowel branches, integer `ord + 2`, `chr`, and ASCII case conversion
  agree with the target behavior;
- `Return` writes the result; and
- maps, integer operations, Boolean guards, and string hooks are the ordinary
  K built-in trust boundary.

The model is intentionally incomplete as general Python: it lacks frames,
exceptions, general name binding, arbitrary conditions, and most syntax.
Minimal coverage is acceptable in generated-semantics mode because none of
those constructs is used.

Several rules are over-broad outside reachable target states. For example, the
`[owise]` vowel branch mishandles an arbitrary empty needle, `Return` would not
discard a following statement, and `[total] swapCaseChar(String)` only
implements one-character ASCII case conversion. No false conclusion from
those limitations is reachable for an intended ASCII-letter/space input to
this submitted program, so they are documented as narrow evidence/coverage
limitations rather than labeled intended-domain unsoundness.

The three string-concatenation simplifications are true monoid laws, agree on
overlaps, and orient associativity to the right. The recursive `encodeSpec`
equations have exhaustive zero/nonzero length guards and consume one
character.

### Fused operational bridge

The rule at `semantic.k` lines 120–146 has `priority(40)` and preempts the
generic loop rule. It matches the entire exact loop body and:

- reads `S` and the `"result"` binding;
- writes `"result"` and `"char"`;
- preserves the remaining environment, functions, result cell, and
  continuation;
- advances `S` by one character; and
- substitutes `encodedChar(first)` and `advancedVowel(first)` for execution of
  the program-defined `If`, assignment, `ord`, addition, `chr`, `swapcase`,
  and accumulation.

Its matched body and state footprint are narrow enough for the submitted
program. A [body mutation](/audit-output/evidence/body-mutation.py) changing
the accumulation to `result += "X"` stopped the fused match, exercised the
generic rules, and returned `"XXXX"` on
`"test"`, demonstrating body sensitivity
([20-operational-sensitivity-body-mutation.log](/audit-output/evidence/20-operational-sensitivity-body-mutation.log)).
An [alpha-renamed equivalent loop](/audit-output/evidence/unfused-equivalent.py),
which also forces generic execution, matched both Python implementations on
six boundary/normal inputs
([21-operational-bridge-unfused-comparison.log](/audit-output/evidence/21-operational-bridge-unfused-comparison.log)).
These finite checks support the concrete bridge's control/state behavior.

They do not discharge value fidelity. In the abstract definition used for
`SPEC.encode-loop-correct`, `swapCaseChar`, `encodedChar`, and
`advancedVowel` are declared `[function,total]` with no equations. They are
program-derived and affect both state and final result. No auxiliary theorem
executes the displaced body under the generic semantics and proves its result
equals those symbols over the full bridge domain.

The false-conclusion witness is explicit:

- satisfying intended input: `"a"`;
- real submitted and canonical result: `"C"`;
- bridge-admitted interpretation: `encodedChar(_) = "X"`;
- K result: exact entry and loop claims requiring `"X"` both prove `#Top`.

This is not merely an untested corner or an assertion that an unreachable rule
is false. It is an intended-domain result divergence made provable by the
result-bearing oracle in the same abstract theory shape as the target proof.
The concrete helper's ASCII equations do not repair the abstract target: that
target was compiled without importing `CONCRETE`, and there is no universal
connection claim.

The bridge therefore violates the real-program soundness gate. Stage 5 fails.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. Two fresh reviewer mutations were used.

### Primary symbolic mutation

[spec-vacuity-loop-audit.k](/audit-output/evidence/spec-vacuity-loop-audit.k)
copies the submitted loop claim but changes its result obligation to
`(R +String encodeSpec(S)) +String "X"`. It is demonstrably false for the
satisfying state `S = R = C = M = ""`, `FS = .Map`, `RES = noResult`.

- `kprove --dry-run` parsed and built the mutation successfully, exit 0:
  [22-vacuity-loop-dry-run.log](/audit-output/evidence/22-vacuity-loop-dry-run.log).
- The actual proof exited 1 with `WarnStuckClaimState`. Its residual contains
  `lengthString(S) = 0` and the failed implication `R = R +String "X"`:
  [23-vacuity-loop-proof-expected-failure.log](/audit-output/evidence/23-vacuity-loop-proof-expected-failure.log).

This is the expected unmet result obligation, not a parse error, missing
import, crash, timeout, or unreachable mutation.

### Independent ground entry mutation

[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k) changes the
`"test"` result from `"TGST"` to `"TGSA"`. Its dry run exits 0
([18-vacuity-dry-run.log](/audit-output/evidence/18-vacuity-dry-run.log)); its
proof exits 1 and shows the completed real configuration returning `"TGST"`
instead
([19-vacuity-proof-expected-failure.log](/audit-output/evidence/19-vacuity-proof-expected-failure.log)).

The submitted claims are discriminating under these mutations. Non-vacuity
passes, but it cannot repair missing theorem scope or the opaque operational
bridge.

## 7. Proven versus assumed accounting

### What the successful reachability proofs establish

- In the abstract `VERIFICATION` theory, executing the exact fused internal
  loop transforms accumulator `R` to `R +String encodeSpec(S)`, where
  `encodeSpec` folds the theory's uninterpreted `encodedChar`. This theorem is
  parametric in an unconstrained character encoder.
- In the concrete theory, three exact ground executions of the submitted
  constructor tree return the three displayed fixed results.
- They do **not** establish a universal partial-correctness theorem for
  `encode(message)` over the intended input domain.
- They do **not** establish that the symbolic `encodedChar` equals execution
  of the program body or the trusted canonical transformation.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K Haskell backend, reachability engine, parser, and compiler | All builds and proofs | Ordinary unavoidable toolchain trust; versions recorded. |
| K `Map`, arbitrary-precision `Int`, `Bool`, and String hooks (`lengthString`, `substrString`, `+String`, `findString`, `ordChar`, `chrChar`) | State, guards, character arithmetic, result | Acceptable low-level primitive boundary on valid ASCII inputs. |
| Trusted `py2mpy.py` | Python-to-constructor identity | Byte-verified and regenerated; acceptable provenance bridge. |
| `encodeProgram()` / `encodeBody()` / `encodeLoopBody()` equations | Program and helper pinning | Statically exact against regenerated `.mpy`; acceptable. |
| `swapCaseChar`, `advancedVowel`, `encodedChar` in abstract `SEMANTIC` | Loop control state, accumulator, postcondition | Illegitimate program-derived opaque boundary; no value-fidelity theorem, and false `"a" -> "X"` interpretation witness succeeds. |
| Equations in `concrete.k` | Ground execution values | Mathematically credible for one-character ASCII letters/spaces, but hand-written task-specific summaries; no universal generic-body connection theorem. |
| Prompt domain interpreted as ASCII English letters plus space | Intent bridge | Informal but reasonable because the prompt names the English alphabet and its example uses spaces. Unicode case behavior is excluded. |
| 3,873 Python differential cases | Candidate implementation versus canonical | Strong finite empirical support only; cannot replace K proof. |
| Six fused and six generic K/Python comparisons | Generated concrete semantics and operational bridge | Finite empirical support only; cannot fix the opaque abstract proof. |
| Static inspection of concrete character equations | Concrete summary versus intended character transform | Straightforward informal mathematics on ASCII, not a machine-checked connection theorem. |

### Gate accounting

- Real-program soundness (Gate A): **FAIL** — result-bearing fused bridge is
  unconstrained in the target proof; concrete false-output witness provided.
- Intent adequacy (Gate B): **FAIL** — no universal entry claim and no
  independently meaningful universal postcondition.
- Trust/evidence auditability (Gate C): **PASS as documentation**, but it
  cannot override Gates A or B. Commands, input scopes, exit statuses, and
  bounded outputs are preserved under `/audit-output/evidence/`.

The implementation's apparent correctness and the successful finite concrete
claims are not substitutes for the missing K theorem. Under the stated
decision boundary, the candidate relies on a materially illegitimate semantic
shortcut and proves only a helper relation plus three fixed examples.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
