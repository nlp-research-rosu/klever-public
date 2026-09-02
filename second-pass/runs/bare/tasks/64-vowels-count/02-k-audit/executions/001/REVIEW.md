# Independent adversarial review: 64-vowels-count

## Headline decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted translated program under its generated K semantics. Fresh source
builds succeeded; both target claims independently returned `#Top`; the proof
constrains the returned integer; and an off-by-one mutation compiled but became
stuck on the concrete satisfying branch `S = ""`.

The decision is `CONCERNS / LEGIT`, not `PASS`, because the generated semantics
is deliberately program-specific and is only faithful on the reachable operand
shapes of this program, CPython recursion-resource exceptions are outside its
model, and the trusted canonical implementation disagrees on the empty string.
None of those limitations supplies a false conclusion for a terminating
execution of the submitted program on its intended word inputs.

All execution used source-only copies under `/tmp/audit-work`. Candidate
`semantic-kompiled/`, `verification-kompiled/`, caches, logs, and reported
`#Top` results were not reused.

## 1. Input and provenance integrity

### Trusted-mount boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, so the trusted mounts are consistent with that mode. I did not
look for or infer any hidden reference semantics.

The required trusted files are regular files:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

The required candidate source artifacts are present as regular, non-symlink
files:

- `/candidate/solution.py`
- `/candidate/solution.mpy`
- `/candidate/semantic.k`
- `/candidate/verification.k`
- `/candidate/spec.k`
- `/candidate/prove.sh`

No symlinks occur anywhere under `/candidate`. Candidate `prompt.py` is
byte-identical to trusted `/reference/prompt.py` (SHA-256
`bc81b28f...39c5d8`), and candidate `py2mpy.py` is byte-identical to trusted
`/reference/py2mpy.py` (SHA-256 `406485ea...4db16`). There are no missing,
changed, mistyped, additional, or symlinked required source artifacts.

The candidate additionally contains two compiled-definition trees,
`__pycache__`, provenance logs, and a structured trace. These are untrusted
generated extras, not source-integrity failures; none was copied into the
scratch build.

### Untrusted generation record

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the JSONL trace only as claims. They report a bare run
with no supplied semantics, an exit code of zero, and eventual `#Top`.
`codex-output.log` and the structured trace also contain several earlier parse,
backend-selection, and stuck-proof failures before the claimed success. None of
these records contributes to the verdict.

Evidence:

- `evidence/stage1_integrity.sh`
- `evidence/stage1_integrity.log` — command exit 0, hashes, types, symlink
  search, and byte comparisons
- `evidence/scratch_copy.log` — exact source-only copy command, exit 0

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The prompt requires `vowels_count(s)` to count `a/e/i/o/u` in either case and
add one when `y` or `Y` is the final character. The canonical implementation
computes membership over the whole string, then inspects `s[-1]`.

The submitted implementation recursively consumes one leading character:

1. return 0 for the empty suffix;
2. add one and recurse if the first character is an ordinary vowel;
3. return one if the sole remaining character is `y` or `Y`;
4. otherwise recurse without adding.

This is extensionally the requested algorithm for nonempty words, and gives the
natural total extension 0 on the empty string.

### Trusted regeneration

The exact command was:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/solution.trusted-regenerated.mpy
```

It exited 0. `cmp` exited 0, and both submitted and regenerated `.mpy` files
have SHA-256 `ee74f8f2...5426c`. Thus `solution.mpy` is byte-identical to output
from the trusted translator.

### Independent differential testing

`evidence/differential.py` separately imports the trusted canonical and
scratch-copied candidate and compares both with a third direct contract oracle.
The input set contains:

- both documented examples;
- empty, one-character, terminal-`y`, internal-`y`, vowel, consonant, and
  case boundaries;
- all strings of lengths 0 through 4 over seven representative character
  classes;
- 500 deterministic random strings of lengths 0 through 80;
- accented and astral Unicode characters.

Results over 3,298 distinct cases:

- candidate versus direct contract: 0 mismatches;
- canonical versus direct contract on nonempty strings: 0 mismatches;
- candidate versus canonical: one mismatch, exactly `""`.

For `""`, the canonical raises `IndexError` because of `s[-1]`; the candidate
returns 0. The prompt describes a “word,” which suggests a nonempty intended
domain, but does not state nonemptiness formally. This is an intent-boundary
concern, not evidence that the candidate is wrong on a word.

A separate resource-boundary probe found that, with CPython's recursion limit
of 1,000, the recursive candidate raises `RecursionError` on a 1,000-character
consonant string while the iterative canonical returns 0. Partial correctness
does not promise a result when the implementation fails to return, but this is
an excluded runtime behavior of the K model.

Evidence:

- `evidence/stage2_fidelity.sh`
- `evidence/stage2_fidelity.log` — exit 0 and complete differential summary
- `evidence/differential.py`
- `evidence/python_resource_boundary.py`
- `evidence/python_resource_boundary.log` — exit 0 and lengths 0–2,000

## 3. Clean proof reconstruction

### Fresh concrete definition

Using K `v7.1.293`, I compiled `/tmp/audit-work/candidate-src/semantic.k` with:

```text
kompile --backend llvm /tmp/audit-work/candidate-src/semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/semantic-fresh-kompiled
```

The command exited 0. No candidate-provided compiled directory was present in
the scratch source copy.

I then ran the actual trusted-regenerated/submitted `solution.mpy` through this
fresh definition on 20 normal and boundary inputs. Every `krun` exited 0, ended
with `intVal(N) ~> .K`, and matched the scratch candidate Python result. Inputs
included `""`, both prompt examples, every branch class, terminal and internal
`y/Y`, accented text, an astral character before and inside strings, newline,
quote, and backslash characters. The sole canonical difference remained the
already documented empty string.

The first Unicode harness run encoded an astral character as a UTF-16 surrogate
pair, which K rejected. That reviewer-harness failure is preserved in
`stage3_concrete_compare.log`. The corrected UTF-8-scalar run and extended run
both exited 0 with no mismatches.

### Fresh proof definition and every positive claim

The proof definition was rebuilt from source:

```text
kompile --backend haskell /tmp/audit-work/candidate-src/verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/verification-fresh-kompiled
```

It exited 0. I independently ran:

```text
timeout 300s kprove /tmp/audit-work/candidate-src/spec.k --definition /tmp/audit-work/verification-fresh-kompiled --spec-module SPEC --claims SPEC.program-loads-solution --output pretty
timeout 300s kprove /tmp/audit-work/candidate-src/spec.k --definition /tmp/audit-work/verification-fresh-kompiled --spec-module SPEC --claims SPEC.vowels-count-correct --output pretty
timeout 300s kprove /tmp/audit-work/candidate-src/spec.k --definition /tmp/audit-work/verification-fresh-kompiled --spec-module SPEC --output pretty
```

Each command exited 0 and printed exactly `#Top` as its proof result.

Evidence:

- `evidence/stage3_build_concrete.{sh,log}`
- `evidence/stage3_concrete_compare.py`
- `evidence/stage3_concrete_compare.log` — preserved reviewer encoding failure
- `evidence/stage3_concrete_compare_corrected.log` — exit 0
- `evidence/stage3_concrete_compare_extended.log` — 20 cases, 0 failures,
  exit 0
- `evidence/stage3_build_proof.{sh,log}`
- `evidence/stage3_prove_program_loads.log` — `#Top`, exit 0
- `evidence/stage3_prove_vowels_count.log` — `#Top`, exit 0
- `evidence/stage3_prove_all.log` — `#Top`, exit 0

## 4. Adequacy and real-program pinning

### Plain-language claim meanings

`program-loads-solution` has no logical `requires` clause. Its starting state
contains:

- any K string `S`;
- `solutionProgram ~> #entry(S)` in `<k>`;
- empty environment, function map, and stack.

It proves that module loading consumes the submitted function definition,
installs exactly `"vowels_count" |-> function("s", vowelBody)`, and reaches the
actual call on `S`.

`vowels-count-correct` also has no logical `requires` clause. Its starting state
contains:

- any K string `S`;
- the exact `vowels_count` binding to `vowelBody`;
- a call on `S` followed by arbitrary `KONT`;
- arbitrary caller environment and stack.

It proves that the call reaches `intVal(#vowels(S))` followed by the same
continuation, with the caller environment, function map, and stack unchanged.
The returned value is fixed by a total recursively defined function; it is not
a fresh variable, implication-only condition, or tautology.

Both preconditions are satisfiable. For example, `S = ""`, `KONT = .K`,
`_ENV = .Map`, `_STACK = .List`, and the displayed exact function map satisfy
the second claim. The first claim is satisfied by `S = ""` and its explicitly
empty cells.

### Exact submitted-program identity

The proof uses macros `solutionProgram` and `vowelBody`, so I checked their
identity rather than trusting the comments. `kast --expand-macros` was run
separately on the trusted-regenerated `solution.mpy` and on
`solutionProgram`. Their KORE outputs are byte-identical, with the common
SHA-256:

```text
91be2840fa16303521fce82e20f01902e37fb5944d591b6fb3c461ea5a81bd43
```

Thus the `<k>` pattern is a macro name for the exact submitted AST, not a
substituted implementation.

### Concrete satisfying substitutions

Reviewer-authored whole-program ground claims start from `solutionProgram ~>
#entry(input)` with initial cells and demand these exact results:

- `""` → 0
- `"abcde"` → 2
- `"ACEDY"` → 3
- `"ay"` → 2
- `"ya"` → 1
- `"rhythm"` → 0

These claims do not import the candidate's universal spec claim. They compiled,
unrolled the concrete program, exited 0, and printed `#Top`. The values match
the candidate Python implementation and match the canonical on every nonempty
case; canonical raises on the separately documented empty case.

A body-sensitivity mutation changed only the empty return from 0 to 9. Trusted
translation succeeded, concrete K execution returned 9, and the expanded AST
no longer matched the proof macro (`cmp` exit 1 as expected). This demonstrates
that the pinning check detects a material body change.

Evidence:

- `evidence/solutionProgram.term`
- `evidence/spec-ground.k`
- `evidence/stage4_pinning.{sh,log}` — macro `cmp` exit 0 and ground `#Top`
- `evidence/solution-body-mutated.py`
- `evidence/stage5_body_sensitivity.{sh,log}` — changed result 9 and expected
  macro mismatch

## 5. Rule-by-rule static soundness review

There are no generated helper K source files beyond `semantic.k`,
`verification.k`, and `spec.k`. `semantic.k` contains 44 local rules: two macro
rules and 42 semantic/equational rules. `verification.k` contains four
equations. `spec.k` contains two claims. There are no local `[functional]`,
`[simplification]`, `[concrete]`, `[owise]`, `[anywhere]`, or priority rules,
and no opaque result-bearing symbols.

The complete numbered sources, rule search, attributes, hashes, and counts are
preserved in `evidence/stage5_inventory.log`.

### Local syntax and configuration inventory

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: a list of `Stmt`;
- `Params`: one string parameter;
- `Stmt`: `FuncDef`, strict `Return`, and condition-strict `If`;
- `Expr`: `Int`, `Str`, `Name`, embedded `PyVal`, strict `BinOp`, left-strict
  `BoolOp`, left-strict `Compare`, two `Subscript` forms, and argument-strict
  `Call`;
- `CmpOp`, `Bound` (`Expr` or `NoBound`), and `Slice`;
- `PyVal`: integer, string, and Boolean values;
- `KResult ::= PyVal`.

`SOLUTION` adds the two macros `vowelBody : Stmts` and
`solutionProgram : Program`.

`SEMANTIC` adds the data constructor `function(String, Stmts)`, internal
`#compare`, the two total Boolean functions `#isVowelChar` and `#isYChar`, and
the control items `#entry`, `#return`, and `#endCall`.

The configuration has exactly the state the submitted program needs:
`<k>`, local `<env>`, global `<functions>`, and call `<stack>`. The initial
computation is the parsed program followed by `#entry($INPUT)`.

`VERIFICATION` adds one total function, `#vowels(String) : Int`.

### Exhaustive semantic rule inventory

The following identifiers enumerate every one of the 44 rules in
`semantic.k`.

| IDs | Lines | Rule(s) and assessment |
|---|---:|---|
| M1 | 42–61 | `vowelBody` expands to the exact four-statement translated body. Exact KORE comparison passed. |
| M2 | 64–65 | `solutionProgram` expands to the exact one-function module. Exact KORE comparison passed. |
| S1 | 88 | `Module(SS) => SS`: exposes module statements; correct for the represented module subset. |
| S2 | 89 | nonempty statement-list sequencing: executes the head before the tail; correct control order. |
| S3 | 90 | empty statements consume to `.K`; correct list base case. |
| S4 | 91–92 | `FuncDef` updates the function map with parameter/body and consumes; correct for this top-level definition. |
| S5 | 93 | entry invokes the required public name on the configured string; correct task entry. |
| S6–S7 | 96–97 | integer and string constructors become the corresponding `PyVal`; exact literal semantics. |
| S8 | 98–99 | `Name` reads a present local binding; every used local name is bound. |
| S9 | 102 | `len` on a string uses trusted `lengthString`; correct for the unshadowed built-in call used here. |
| S10 | 103–106 | a user call looks up the function, replaces the local environment, pushes the caller environment, and appends `#endCall`; recursion uses the exact installed binding. |
| S11 | 110 | a value-return becomes the internal abrupt marker `#return(V)`. |
| S12–S13 | 111–112 | `#return` discards remaining statement or statement-list terms within the current function. |
| S14 | 113–115 | at the exact `#endCall` delimiter, return restores one saved environment and leaves the value before the caller continuation. It preserves functions and the preexisting stack. |
| S15–S16 | 119–122 | true and false `If` branches are disjoint and exhaustive for a Boolean value. |
| S17–S18 | 123–124 | Boolean `and` evaluates its RHS only after true and returns false after false; correct short-circuit behavior. |
| S19 | 127 | integer `+` uses trusted `+Int`; the program adds only integer values. |
| S20 | 128 | comparison dispatch evaluates the RHS after a value LHS, preserving the used left-before-right order. |
| S21–S22 | 129–132 | string equality true/false rules have complementary guards and agreeing, disjoint results. |
| S23–S24 | 133–136 | integer equality true/false rules likewise have complementary guards. |
| S25 | 137–138 | membership in the literal `"aeiouAEIOU"` delegates to the fully defined character predicate. Correct for reachable one-character operands. |
| S26 | 139 | membership in literal `"yY"` delegates to the fully defined character predicate. Correct for reachable one-character operands. |
| S27–S36 | 141–150 | ten true equations, individually for `a,e,i,o,u,A,E,I,O,U`. Guards are mutually exclusive. |
| S37 | 151–156 | the vowel false equation is exactly the conjunction of inequality to all ten characters, disjoint from S27–S36 and completing total coverage over all strings. |
| S38–S39 | 158–159 | true equations for exactly `y` and `Y`, mutually exclusive. |
| S40 | 160–161 | false for strings unequal to both `y` and `Y`, completing total coverage. |
| S41 | 162–163 | indexing is modeled by one-character `substrString`; every reachable use is index 0 on a nonempty suffix. |
| S42 | 164–165 | the exact used slice `[1:]` maps to `substrString(S,1,lengthString(S))`; this is the recursive tail. |

The strictness-generated heating/cooling rules are not local hand-written
rules, but their effect was checked. Statement order is sequential. `If`
evaluates only the condition. `BoolOp("and",...)` short-circuits. `Compare`
evaluates the LHS before its RHS. `BinOp` and general subscript strictness may
allow more than one operand order in the abstract syntax, but in the submitted
program the other operands are literals or pure lookups, so no value, state,
control, or exception difference can result.

Calls and returns preserve every modeled observable cell. The `#endCall`
delimiter prevents the return-discard rules from discarding an arbitrary caller
continuation. The recursive call always uses `substrString(S,1,lengthString(S))`,
so it matches the real suffix control flow.

### Exhaustive verification-rule inventory

| ID | Lines | Equation and assessment |
|---|---:|---|
| V1 | 11 | `#vowels("") = 0`, the recursion base. |
| V2 | 13–16 | nonempty vowel-leading strings add one and recurse on the tail. |
| V3 | 18–22 | a non-vowel, length-one `y/Y` contributes one. |
| V4 | 24–29 | every other nonempty non-vowel-leading string recurses without adding. |

V1 is disjoint from V2–V4. V2 is separated by the vowel predicate. Within the
non-vowel region, V3 and V4 are disjoint: V4's disjunction is false exactly
when length is one and the character is `y/Y`. The cases cover every K string.
Both recursive equations take a strict suffix of a nonempty string. Thus the
`[total]` declaration is justified, and no overlapping equations disagree.

`#vowels` is a definitional summary, not an operational bridge: no semantic
rule replaces execution of the program with `#vowels`. The reachability claim
symbolically executes the real body and proves equality to the summary. The
program semantics and summary both use `#isVowelChar`/`#isYChar`, but those
symbols are not opaque or unconstrained: S27–S40 exhaustively fix their values.
This is therefore not a result-bearing oracle cycle.

### Used-construct coverage map

Every constructor in `solution.mpy` is covered:

- `Module`, `FuncDef`, `Params`, and statement lists: M2, S1–S4;
- `If` and `Return`: S11–S16;
- `Int`, `Str`, `Name`: S6–S8;
- `Call(len,...)` and recursive `Call(vowels_count,...)`: S9–S10, S14;
- `Compare` with string/int `==` and the two literal `in` operations:
  S20–S26;
- `BoolOp("and")`: S17–S18;
- `BinOp("+")`: S19;
- index 0 and exact slice `[1:]`: S41–S42.

No used constructor is unmodeled or fabricated by a catch-all rule.

### Narrow scope gaps, not intended-domain unsoundness

Some declarations look more general than the rules are meant to be:

- S25/S26 are not full Python substring-membership semantics. For example,
  Python says `"ae" in "aeiouAEIOU"` is true while `#isVowelChar("ae")` is
  false. The submitted program only supplies `s[0]`, and after the empty guard
  that operand is exactly one character.
- S41 does not model Python's out-of-bounds or negative-index exceptions.
  Actual execution only reaches index 0 for a nonempty suffix.
- S9 pins the unshadowed built-in `len` without general Python name resolution.
  The submitted program defines no `len`, installs only `vowels_count`, and has
  no rebinding construct.
- General Python recursion-depth/resource exceptions are absent.

These are real reuse and language-model limitations. I found no satisfying
input to the submitted entry program on which they enable a false returned
integer, so under the audit instruction I do not label them unsound. They are
the principal reason for `CONCERNS` rather than an unqualified `PASS`.

Evidence:

- `evidence/stage5_inventory.sh`
- `evidence/stage5_inventory.log` — exit 0 and complete numbered inventory
- `evidence/stage5_body_sensitivity.{sh,log}`

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I created
`evidence/spec-vacuity-audit.k`, which changes the result-bearing obligation to:

```text
intVal(#vowels(S) +Int 1)
```

The precondition remains the real function-call precondition. It is
demonstrably false at the satisfying witness:

```text
S = "", KONT = .K, _ENV = .Map, _STACK = .List
```

because actual execution returns `intVal(0)` while the destination requires
`intVal(1)`.

`kprove --dry-run` exited 0, confirming successful parsing and proof-artifact
construction. The actual proof exited 1 with `WarnStuckClaimState`. Its
residual explicitly contains:

```text
<k> intVal ( 0 ) ~> KONT ~> .K </k>
S #Equals ""
```

and reports that the destination does not unify and execution cannot rewrite
further. This is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash.

The first wrapper log ended with status 1 only because its final text assertion
expected an unwrapped error line; the proof behavior was already correct. The
corrected wrapper accepts the backend's line wrap and exits 0 while still
requiring the inner proof exit to be nonzero.

Evidence:

- `evidence/spec-vacuity-audit.k`
- `evidence/stage6_mutation.sh`
- `evidence/stage6_mutation.log` — preserved wrapper-pattern failure
- `evidence/stage6_mutation_corrected.log` — dry run 0, proof 1, expected stuck
  residual, wrapper exit 0

## 7. Proven versus assumed accounting

### Precisely proven

Under the freshly compiled generated K semantics:

1. the exact submitted AST loads the exact `vowels_count` body;
2. for every K string `S`, arbitrary caller environment and stack, and
   arbitrary continuation, calling that exact body reaches
   `intVal(#vowels(S))` before the same continuation;
3. the modeled caller environment, function map, and preexisting stack are
   restored/preserved;
4. `#vowels` is the total recursive character count that adds for ordinary
   vowels and for `y/Y` only in the final position.

This is a partial-correctness result under the modeled semantics. It is not a
claim that the recursive CPython implementation returns within resource limits
for every finite host-language string.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `/reference/py2mpy.py` | Python-source to `.mpy` identity | Acceptable trusted input; byte regeneration passed. |
| K parser and K `v7.1.293` toolchain | All compilation, execution, and proof results | Necessary machine-checking trust boundary. Fresh definitions and exact versions are logged. |
| Built-in `Bool`, unbounded `Int`, `String`, `Map`, and `List` domains | All local semantics | Acceptable low-level K primitives. No proof-local equations redefine them. |
| `lengthString`, `substrString`, string equality, Boolean connectives, `+Int`, integer equality, map update/lookup, and list operations | Calls, comparisons, slicing, recursion, state | Acceptable fixed primitives below the theorem. Unicode and boundary executions provide finite support, not a replacement proof of the hooks. |
| Generated local Python-subset semantics | Connection from `.mpy` execution to Python behavior | Audited rule by rule and concretely tested. Sound for every reachable construct/operand shape of this program; intentionally incomplete and over-broad in the off-path ways listed in Stage 5. |
| `#isVowelChar`, `#isYChar` | Program membership and `#vowels` | Not opaque: exhaustive, disjoint equations fix all string inputs. Acceptable. |
| `#vowels` | Final postcondition | Definitional summary with exhaustive, disjoint, descending equations. It does not replace execution. Its alignment with the English count is ordinary mathematical reasoning plus finite differential evidence. |
| Natural-language “word” domain | Empty-input intent | Ambiguous at `""`; canonical raises while candidate/formal theorem return 0. Documented concern. |
| Idealized call stack/no resource exception | Long CPython inputs | Excluded behavior. The recorded `RecursionError` boundary is a model-to-runtime concern, compatible with partial correctness. |

There are no opaque symbols, unconstrained fresh results, empirical operational
bridges, proof-local semantic shortcuts, or simplification lemmas. Differential
testing supports only the source/intent and concrete-semantics bridges; it is
not used as a substitute for the K reachability proof.

### Gate summary

- Real-program soundness: **PASS**. Exact AST pinning, full source execution,
  state/control preservation, result constraint, body sensitivity, and
  non-vacuity all passed.
- Intent adequacy: **PASS WITH DOCUMENTED LIMITS**. Nonempty-word behavior
  matches the prompt and canonical; empty behavior is ambiguous, and host
  recursion resources are outside the model.
- Trust/evidence auditability: **PASS**. Reviewer-authored sources, exact
  commands, bounded outputs, and exit statuses are preserved under
  `/audit-output/evidence/`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
