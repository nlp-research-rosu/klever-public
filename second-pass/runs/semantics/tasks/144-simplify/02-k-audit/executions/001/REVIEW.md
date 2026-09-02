# Independent adversarial review: 144-simplify

The reconstructed K claim does close, and the false mutation is rejected, but
the candidate does not prove the submitted `solution.mpy` over real encoded
fraction strings. The proof is insensitive to the presence of `solution.mpy`
and depends on two proof-local rules over fresh opaque string constructors for
which there is no connection theorem to concrete decimal code sequences. This
is a real-program and real-input pinning failure, not an infrastructure error.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted directory
`/reference/reference-semantics` is present, so the mount agrees with the
rendered condition and the audit continued.

I compared tree entry presence, type, symlink status, and file bytes. The
candidate's `reference-semantics/` has exactly the same directories and regular
files as the trusted tree, with no missing, additional, changed, mistyped, or
symlinked entry. The candidate `prompt.py` and `py2mpy.py` are also byte
identical to the trusted versions:

- `prompt.py`: SHA-256
  `2a0addf544cd38216f359d1e48649ae659b89cd25c4f7fa72060ee8cbb404735`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The exact check and its exit status are in
`evidence/01-integrity.log`; the recursive manifest is in
`evidence/01-artifact-manifest.log`. The checker itself is preserved as
`evidence/check-integrity.sh`.

The following named generation-evidence artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any top-level structured trace file matching the recorded trace search

Their absence prevents review of the generation narrative, timing, and claimed
trace provenance. It does not prevent independent source reconstruction. No
candidate `PROOF.md` or compiled K definition was used. The candidate's Python
bytecode cache was ignored. All executable artifacts were rebuilt beneath
`/tmp/audit-work`.

The live toolchain was K `v7.1.337` and Python `3.10.12`; see
`evidence/01-toolchain.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

From trusted `prompt.py`, an intended input consists of two strings
`"A/B"` and `"C/D"`, where all four components are positive whole numbers
and denominators are nonzero. The required result is true exactly when

`(A / B) * (C / D)` is a whole number, equivalently when
`(B * D)` divides `(A * C)`.

Trusted `canonical.py` parses the four integers and tests a float quotient
against its integer conversion. Candidate `solution.py` parses the same four
integers and tests

`(A * C) % (B * D) == 0`.

For arbitrary-size positive Python integers, the candidate expression is the
direct exact characterization of the natural-language property. It covers both
true and false branches and is defined throughout the intended domain.

### Translation identity

I invoked the trusted translator directly on candidate `solution.py`. The
regenerated and submitted `solution.mpy` files are byte identical, both with
SHA-256
`d59c7cca5edc79f46581c7072cafd3ce4342798676d80884fa5af2260b084c06`.
The exact command, hashes, and zero statuses are in
`evidence/02-translation-identity.log`.

### Independent differential testing

`evidence/differential_test.py` imports the trusted canonical entry point and
the candidate entry point independently. Its input scope is:

- all three documented examples;
- explicit unit, exact-divisibility, and remainder-one branch boundaries;
- the candidate's additional example and leading-zero decimal spellings;
- empty, zero-numerator, and zero-denominator excluded-domain probes;
- every quadruple `(A,B,C,D)` in `[1,12]^4`, 20,736 valid inputs;
- 500 deterministic generated quadruples in `[1,10^12]^4`, seed 144;
- two valid positive, very-large-integer precision/overflow witnesses.

There were zero mismatches on the 20,736-input grid and zero in the seeded
500-input sample. Empty input raised the same `ValueError`. The zero-denominator
probe, outside the contract, raised `ZeroDivisionError` in both implementations
with different messages.

There are two material canonical-versus-candidate divergences inside the
unbounded positive domain:

- `simplify("18014398509481985/2", "1/1")`: canonical returns `True`
  after float rounding; candidate correctly returns `False`.
- `simplify("10**400/1", "1/1")` with the numerator expanded in the evidence:
  canonical raises `OverflowError`; candidate correctly returns `True`.

These do not count against the candidate implementation: they expose the
trusted dataset solution's float limitation relative to the stated exact
mathematical contract. They also mean canonical differential testing cannot be
a universal oracle over unbounded inputs. Full inputs and results are in
`evidence/02-differential.log`.

## 3. Clean proof reconstruction

I copied trusted semantics sources and candidate proof sources into a fresh
scratch directory. I did not copy or reuse any compiled definition.

The concrete LLVM definition built from
`reference-semantics/semantics.k` with main module `MPY-KRUN`; exit status was
zero (`evidence/03-kompile-runtime.log`). The compiler reported several
non-exhaustive `[total]` warnings in unrelated functions such as `mapStrVS`,
float conversions, `joinCodes`, and `valSeqAt`. None occurs on this program's
used path.

An independently authored concrete harness,
`evidence/concrete_audit.py`, exercised documented, boundary, exact/remainder,
and large-integer cases. The trusted translator produced its `.mpy` file in
scratch, and `krun` finished with empty `<k>`, `NoExc`, and exit code zero.
The final heap shows the real `iCons` decimal character-code lists. See
`evidence/03-krun-concrete.log`.

The Haskell proof definition built from candidate `verification.k` with main
and syntax module `SIMPLIFY-VERIFICATION`; exit status was zero
(`evidence/03-kompile-verification.log`). The only positive target claim is the
single claim in `spec.k`. Independently running it produced `#Top` and exit
status zero (`evidence/03-kprove-positive.log`).

Thus verification under the candidate-extended theory succeeds. This stage
does not establish that the extended theory is an adequate theorem about the
submitted program.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

For arbitrary integers `A,B,C,D` satisfying `A>0`, `B>0`, `C>0`, and `D>0`,
the claim starts from a clean machine and invokes:

`runSimplify(str(fractionCodes(A,B)), str(fractionCodes(C,D)))`.

It requires the builtins and module scopes, empty heap and stack, no return or
exception, heap location zero, and exit code zero. It demands termination with
the exact Boolean

`pyMod(A*C, B*D) ==Int 0`,

two allocated split-result lists containing `str(numCodes(A))`,
`str(numCodes(B))`, `str(numCodes(C))`, and `str(numCodes(D))`, and heap location
two. The result is not a free variable, implication-only condition, or
tautology.

The precondition is satisfiable. One witness is
`A=B=C=D=1` with the exact initial cells written in `spec.k`. The demanded
result reduces to `pyMod(1,1)==0`, i.e. `true`; both Python implementations
return `True` on `("1/1","1/1")`. A false-branch witness is
`A=1,B=6,C=2,D=1`; the demanded result and both Python implementations are
false. These cases are recorded in `evidence/02-differential.log` and the
concrete K run.

There are no loops, circularity claims, or helper reachability claims in this
candidate. The only claim is the entry claim, so there is no separate
loop/helper-to-control-flow correspondence to validate.

### Decisive program-identity failure

The `<k>` cell does not load or execute submitted `solution.mpy`.
`runSimplify` is a fresh proof-local K item whose rule constructs a
`closureVal` containing a hand-copied function body. Neither `verification.k`
nor `spec.k` requires or parses `solution.mpy`.

I tested body sensitivity in a separate scratch tree that contained trusted
semantics, `verification.k`, and `spec.k`, but no `solution.py` or
`solution.mpy`. The source scan records `PROGRAM_PRESENT: no`. Nevertheless,
the proof definition built successfully and the claim again returned `#Top`
with exit status zero:

- `evidence/04-pinning-scan.log`
- `evidence/04-kompile-without-program.log`
- `evidence/04-kprove-without-program.log`

This is a direct witness that changing, deleting, or substituting the submitted
program artifact cannot affect the theorem. The copied closure body happens to
match the current submitted body by manual comparison, and the trusted
translator independently establishes the submitted `.py`/`.mpy` identity, but
neither fact is an input dependency of the K proof. The required real-program
pinning gate therefore fails.

### Decisive real-input failure

Actual input `"1/5"` is represented by the supplied semantics as the concrete
code sequence

`str(iCons(49, iCons(47, iCons(53, .IntSeq))))`.

The entry claim instead uses the distinct fresh constructor
`str(fractionCodes(1,5))`. No rule or theorem equates those terms.
`fractionCodes` cannot unify with the fixed `iCons` constructors. Likewise,
`numCodes(1)` is not connected to `iCons(49,.IntSeq)`.

This ground case is the symbolic false-attribution witness: instantiating
`A=1,B=5` does not instantiate the formal claim with the intended concrete
input `"1/5"`. The proof therefore does not range over any real
`str(iCons(...))` fraction string, despite the prose saying it ranges over
valid fractions.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory-k.sh` generated
`evidence/05-rule-inventory.log`, which enumerates every configuration,
syntax production, context, rule, claim, and relevant attribute occurrence in
the supplied semantics, candidate `verification.k`, and candidate `spec.k`.
It contains 1,316 bounded output lines. There are 695 rules in the supplied
semantics and three proof-local rules.

The per-file disposition below covers every inventoried rule. “Accepted” means
the rule follows the supplied subset's stated operational level or ordinary
mathematics on its declared domain; “unused boundary” means it is outside this
program's dependency slice and is accounted for rather than used to justify the
claim.

| File | Rules | Syntax productions | Disposition |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Assembly imports only; exact trusted copy. |
| `assert.k` | 3 | 0 | Accepted abrupt assertion behavior; unused by proof. |
| `bool.k` | 13 | 0 | Accepted truthiness/short-circuit rules; no problematic overlap. |
| `builtins.k` | 137 | 39 | Registry and folds accepted. Concrete integer parsing is sound for decimal intended inputs. Opaque MD5 is unused. |
| `call.k` | 21 | 3 | Accepted left-to-right callee/argument dispatch and frame creation; used. Priorities only dereference fixed heap objects. |
| `comprehension.k` | 7 | 3 | Accepted macro expansion; unused. |
| `concrete.k` | 16 | 6 | Concrete-only deep equality/keyed sort; not imported by the proof. |
| `controls.k` | 34 | 5 | Accepted assignment/branch/loop control; ordinary assignment support is used. |
| `core.k` | 46 | 53 | Configuration, scope lookup, allocation, sequencing, literals, and helpers accepted; used cells and allocation are fully pinned. |
| `dict.k` | 28 | 14 | Accepted minimal ordered-dict subset; unused. |
| `float.k` | 121 | 34 | Opaque proof-domain floats and concrete twins are an explicit supplied trust boundary; entirely unused here. |
| `functions.k` | 15 | 8 | Accepted binding, return, and frame-pop rules on this non-escaping closure path; used. |
| `int.k` | 16 | 1 | Exact integer arithmetic/comparisons accepted. `pyMod` is used only with positive `B*D`, so division by zero is excluded. |
| `iter.k` | 0 | 1 | Iterator protocol declaration only; unused. |
| `list.k` | 27 | 6 | Accepted list allocation/helpers; only list values allocated by split are relevant. |
| `methods.k` | 75 | 27 | Concrete `str.split("/")` is a terminating, disjoint three-rule recursion on `iCons`; used in concrete runs. Other methods are unused. |
| `operators.k` | 10 | 0 | Accepted strict dispatch and dereferencing; multiplication, modulo, and equality paths are used. |
| `range.k` | 6 | 2 | Accepted nonzero-step range subset; unused. |
| `set.k` | 12 | 7 | Accepted finite-code set functions; unused. |
| `sort.k` | 19 | 7 | `sortVS`/`sortKeyVS` are supplied opaque trust boundaries with concrete insertion-sort rules; unused. |
| `str.k` | 28 | 5 | ASCII literal and code-sequence operations accepted; `Str("/")` reduces to code 47 on the used path. |
| `subscript.k` | 40 | 18 | Totalized/OOB and opaque-sort boundary accounted for; unused by this program. |
| `syntax.k` | 0 | 50 | Grammar, strictness, and sequence strictness accepted. |
| `tuple.k` | 21 | 4 | Target binding and two-element unpacking accepted; used for both split results. |
| `verification.k` | 3 | 3 | Individually analyzed below; two rules are unjustified result-bearing bridges and one is a non-pinning harness definition. |
| `spec.k` | 0 | 0 | One claim, over synthetic rather than concrete strings. |

There are no `[simplification]` rules and no `[functional]` declarations in
the inventoried sources. Every `[function]`, `[total]`, `[concrete]`,
`[no-evaluators]`, `[owise]`, macro/strictness attribute, and priority
occurrence is listed in `evidence/05-rule-inventory.log`. Compiler-reported
non-exhaustive total functions are either unused here or receive only covered
constructors on the used path.

### Mapping the submitted syntax to fixed rules

The full source-line query is preserved in
`evidence/05-used-construct-map.log`.

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; normally `core.k` loads the module and `functions.k` installs the closure. The entry claim bypasses both by injecting a closure directly. |
| `Assign`, `TupleExpr`, `Name` | Strict RHS evaluation from `syntax.k`; tuple dereference/unpack/bind in `tuple.k`; scope lookup/update in `core.k`/`controls.k`. |
| `Call`, `Attribute` | Left-to-right callee and argument evaluation in `call.k`; attribute becomes a bound method. |
| `Str("/")` | `str.k` produces the concrete ASCII `IntSeq` containing 47. |
| `split` | `methods.k` allocates a list and recursively runs fixed `splitSep` on concrete `iCons`; candidate extension supplies a separate opaque-constructor case. |
| `int(...)` | Builtin lookup and call dispatch in `core.k`/`call.k`; concrete one/multi-digit cases in `builtins.k`; candidate extension supplies a separate opaque-constructor case. |
| `BinOp("*")`, `BinOp("%")` | Strict dispatch in `operators.k`; exact `*Int` and `pyMod` rules in `int.k`. |
| `Compare(... == 0)` | Comparison dispatch in `operators.k`; integer equality in `int.k`. |
| `Return` | Strict evaluation, `retV`, and frame restoration in `functions.k`. |

On the used path, `Assign` evaluates its RHS before binding, `Call` evaluates
the callee and then arguments left-to-right through `#evalArgs`, and nested
binary operands use `seqstrict`. Each `split` allocates exactly one heap list;
the two allocations explain the claimed `.Map => 0 |-> ... 1 |-> ...` and
`heapLoc 0 => 2`. The closure call creates scope 1, binds `x` then `n`, and
`#pop` restores environment 0, removes the call scope, empties the frame stack,
and preserves the allocated heap. The fixed split guards
`C ==Int SEP`/`notBool(C ==Int SEP)` are disjoint and exhaustive for concrete
codes; the single- and multi-digit fixed `int` cases are disjoint by length.
The two proof-local parsing rules are constructor-disjoint from those fixed
cases, so the audit found no overlapping contradictory right-hand sides.

### Each proof-local extension

1. `numCodes(Int)` and `fractionCodes(Int,Int)` are fresh data constructors,
   not fixed-semantics decimal encoders. They have no defining equations,
   code-sequence projection, injective decimal representation theorem, or
   concrete connection claim. They are result-bearing because the same
   parameters flow into the final arithmetic result.

2. `splitSep(fractionCodes(A,B),47,.IntSeq) => ...` is a definitional-looking
   summary that supplies execution where fixed `splitSep` has no applicable
   constructor rule. Its match has no guard and covers all integer parameters.
   It does not overlap the fixed `.IntSeq`/`iCons` equations, so there is no
   local critical-pair inconsistency; its defect is the missing connection from
   the synthetic match domain to real decimal strings. It influences both heap
   contents and the returned result.

3. `applyBuiltin("int",str(numCodes(I)),.Vals) => I` directly exposes the
   parameter of the synthetic constructor. It does not overlap the fixed
   concrete-digit rules because `numCodes` is a different constructor. It has
   no guard or bridge-free theorem proving that a concrete numeral parses to
   `I`; it controls all four arithmetic operands and therefore the final
   Boolean.

4. `runSimplify(X,N)` expands a fresh harness item into an ordinary closure call.
   As an equation for that fresh item, the copied control and state behavior is
   consistent with the supplied call semantics and preserves an arbitrary
   continuation. I do not label this rule mathematically false. The narrower,
   decisive defect is artifact sensitivity: it defines a substitute closure
   independently of the submitted program file.

I removed the two symbolic parsing rules in a fresh proof definition while
retaining the same harness and claim. The definition built successfully, but
`kprove` exited 1 with `WarnStuckClaimState` at
`splitSep(fractionCodes(A,B),47,.IntSeq)`. This establishes that the bridges are
essential, not dead declarations:

- `evidence/verification-no-bridges.k`
- `evidence/spec-no-bridges.k`
- `evidence/05-kompile-no-bridges.log`
- `evidence/05-kprove-no-bridges.log`

There is no candidate bridge-free universal connection theorem to audit. I do
not claim that either equation has a concrete false right-hand side on its
fresh-constructor domain: that domain contains no concrete intended string.
The narrower and sufficient failure is that the proof silently gives behavior
to synthetic used constructs and then attributes the resulting theorem to
non-unifying concrete inputs. The `A=1,B=5` representation witness in Stage 4
shows the false attribution precisely.

## 6. Fresh non-vacuity test

I created `evidence/spec-vacuity.k`, a new module independent of any candidate
vacuity file. It changes the result-constraining postcondition from

`pyMod(A*C,B*D) ==Int 0`

to

`pyMod(A*C,B*D) =/=Int 0`.

This mutation is demonstrably false for the satisfiable precondition witness
`A=B=C=D=1`, because `pyMod(1,1)=0`.

`kprove --dry-run` parsed and built the mutation successfully with exit status
zero (`evidence/06-vacuity-dry-run.log`). The real proof then exited 1 with
`WarnStuckClaimState`; the residual reached the final result and reported a
failed implication between the actual equality-to-zero Boolean and the demanded
negation (`evidence/06-vacuity-proof.log`). This is the expected unmet
obligation, not a parser/import error, timeout, or unrelated crash.

The formal claim is therefore result-constraining and non-vacuous under the
candidate-extended theory. Passing non-vacuity does not repair program or input
pinning.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied semantics plus all three proof-local rules, the
machine-checked claim establishes:

- for all positive mathematical integers `A,B,C,D`;
- executing the inline `closureVal` body on the two synthetic values
  `str(fractionCodes(A,B))` and `str(fractionCodes(C,D))`;
- using the stipulated synthetic split and integer-decoding equations;
- terminates in the exact Boolean divisibility result;
- allocates exactly the two stipulated synthetic split lists and restores the
  call frame without exception.

This is a coherent theorem about the added abstract datatype. It is not a
theorem that the submitted `solution.mpy` computes that value for concrete
fraction strings.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `prompt.py`, `canonical.py`, and `py2mpy.py` | Intent and source comparison | Authorized trusted inputs. Canonical has documented large-int float limitations. |
| Byte-identical supplied semantics | All K execution | Authorized semantics level. Opaque float/sort/MD5 primitives and unrelated totality warnings do not occur in this dependency slice. |
| K integer, Boolean, map/list, string, and rewriting primitives | All fixed semantic rules | Ordinary K/toolchain trust boundary; acceptable for a K proof audit. |
| `fractionCodes(A,B)` as an encoding of `"A/B"` | Entry domain, split, heap, result | Illegitimate as an unqualified real-input bridge: no equation or universal connection theorem; concrete and synthetic constructors do not unify. |
| `numCodes(I)` as an encoding of decimal `I` | Integer conversion and final arithmetic | Illegitimate as an unqualified value bridge: no concrete numeral connection theorem. |
| Hand-copied `closureVal` body | Entire reachability claim | Textually matches the current body, but is not pinned to or loaded from `solution.mpy`; proof succeeds with the program absent. |
| Differential testing | Python implementation-to-intent evidence only | Finite support: strong on the recorded domains, not a universal K connection theorem and not proof-file sensitivity. |
| Trusted translator byte identity | `solution.py` to `solution.mpy` fidelity | Strong artifact bridge between those two files, but the K claim imports neither artifact. |
| Manual observation that inline AST matches `solution.mpy` body | Substitute closure relationship | Informal and body-insensitive; insufficient under the required real-program pinning criterion. |

For completeness, every named opaque/symbol boundary in the supplied
semantics is:

- sorting/digest: `sortVS`, `sortKeyVS`, and `md5hexCodes`;
- floats/conversions: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  and `sqrtF`;
- proof-local opaque data: `numCodes` and `fractionCodes`.

The first two groups are fixed supplied primitives with concrete twins or an
explicit supplied abstraction boundary and are unreachable in this proof,
except that ordinary non-opaque integer/string primitives are used. The last
group is candidate-created, result-bearing, and lacks the required connection.

Excluded behavior includes malformed fraction spellings, zero or negative
components, denominator zero, Python exception fidelity outside the positive
domain, and any claim about canonical float behavior on huge integers. The
formal claim also says nothing about arbitrary callers or continuations of the
submitted module because it invokes the substitute harness directly.

### Decision

The candidate implementation itself matches the natural-language property
better than the float-based canonical implementation on unbounded integers.
The positive K claim also reconstructs and is non-vacuous. Those facts do not
overcome the two mandatory adequacy failures:

1. the proof builds and closes without the submitted program artifact, and
2. the entry domain consists of synthetic opaque strings with no theorem
   connecting them to any actual valid fraction string.

Under the stated decision boundary, this is a substituted-program and
unconnected-input proof, so it is not a legitimate partial-correctness proof of
the real generated program. All required tool stages completed without timeout
or infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
