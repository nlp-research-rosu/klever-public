# Independent adversarial review: 153-Strongest-Extension

## Decision

The candidate is **not a legitimate proof**. All four submitted target claims
can be rebuilt and produce `#Top`, and a fresh false-result mutation is rejected.
However, the final proof definition imports a priority-40 operational rule that
bypasses lexical function lookup. A concrete bridge-free witness shows that the
supplied semantics returns `99`, while the candidate rule fabricates `1` and
makes that false result prove as `#Top`. The supporting helper claim has a
strictly narrower precondition and does not justify the rule's complete match
domain.

This is a candidate defect, not an audit infrastructure failure. The trusted
mounts agree with `SUPPLIED_SEMANTICS`, K v7.1.337 was available, all builds
completed, and the false-rule witness is reproducible.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode. I did not use `writing-semantics`.

The recursive, no-dereference comparison found:

- `/candidate/reference-semantics` and
  `/reference/reference-semantics` are identical (`diff -qr
  --no-dereference`, exit 0).
- Neither semantics tree contains a symlink.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- All submitted proof/program artifacts inspected are ordinary files or
  directories. There are no changed, additional, missing, mistyped, or
  symlinked entries in the candidate semantics tree.

The following required provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present. The existing
`proof-*.out` files each claim `#Top`, and `concrete_tests.out` claims clean
termination, but I treated them only as untrusted claims and reconstructed the
results independently. `prove.sh`, the submitted concrete tests, and their
outputs were also read as untrusted evidence.

Exact inventory/comparison commands and exit statuses are in
[stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh) and
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical behavior

For a class-name string and a nonempty list of extension-name strings, assign
each extension the number of alphabetic uppercase characters minus the number
of alphabetic lowercase characters. Return
`class_name + "." + first_extension_with_maximal_score`. The first element wins
a tie. Nonemptiness is implicit in the trusted canonical implementation's
unconditional `extensions[0]`.

The trusted canonical implementation explicitly includes `x.isalpha()` before
counting `x.isupper()` or `x.islower()`. The submitted implementation omits the
`isalpha()` test. It implements the intended stable maximum correctly for the
ASCII model but differs for some Python Unicode characters for which
`isupper()` is true while `isalpha()` is false.

### Translation identity

The trusted translator regenerated `solution.mpy` from the submitted
`solution.py` with exit 0. The regenerated and submitted MPY files are byte
identical:

```text
24670b765dd24f42df1c6da80d90056f056127bffefdc581e74a72f6f8030c43
```

Commands, hashes, and statuses are in
[stage2_fidelity.sh](/audit-output/evidence/stage2_fidelity.sh) and
[stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) independently
loads the trusted canonical and submitted entry points. It tests both documented
examples; empty class, empty extension, and empty extension-list boundaries;
singleton/tie/strict-improvement/nonletter cases; list lengths one through five;
every uppercase/lowercase/neutral and `>`/`<=` branch shape; and 5,000
deterministically generated ASCII cases.

The command exited 0. There were no ASCII mismatches. Both implementations raise
`IndexError` for an empty extension list. There were two visible Unicode
mismatches among 5,015 total cases. One concrete witness is:

```text
input:      ("C", ["Ⅰ", "A", "a"])
canonical:  "C.A"
submitted:  "C.Ⅰ"
```

The Roman numeral `Ⅰ` is not alphabetic according to Python `isalpha()` but is
uppercase according to `isupper()`. This is a real implementation-to-prompt
scope gap because the prompt does not restrict strings to ASCII. Differential
testing is finite evidence only; it is not part of the K proof.

## 3. Clean proof reconstruction

All source inputs needed for execution were copied to
`/tmp/audit-work/reconstruction`. The scratch directory was deleted and
recreated first. Only source artifacts were copied; no candidate kompiled
definition, cache, or generated proof output was reused.

[stage3_reconstruct.sh](/audit-output/evidence/stage3_reconstruct.sh) records the
complete reconstruction. The aggregate transcript with every exact command and
status is
[stage3_reconstruction.log](/audit-output/evidence/stage3_reconstruction.log).

### Concrete definition

The trusted candidate-matching semantics was compiled afresh with the LLVM
backend:

```text
kompile .../reference-semantics/semantics.k --backend llvm
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX
exit 0
```

The reviewer test program has an AST prefix identical to all two top-level nodes
of submitted `solution.py`, followed by seven reviewer assertions. Fresh `krun`
execution exited 0 with `.K`, `NoExc`, and exit code 0. It covers the examples,
an empty class/extension, ties, branch improvement, neutral characters, and
lists of two, three, and four elements. Sources and logs:
[runtime_tests.py](/audit-output/evidence/runtime_tests.py),
[stage3_llvm_build.log](/audit-output/evidence/stage3_llvm_build.log), and
[stage3_krun.log](/audit-output/evidence/stage3_krun.log).

The LLVM compiler warned about several nonexhaustive `[total]` functions in the
supplied semantics. The only warning touching a used operation is
`valSeqAt`; the formal entry uses index 0 of an explicitly three-element
`vCons`, so its defined in-bounds rule applies. The other warned functions are
not on this program's execution path.

### Proof definitions and positive claims

Each proof stage was compiled from source with the Haskell backend and each
positive target was run independently. Every build exited 0. Every claim
command exited 0 and printed `#Top`:

| Fresh definition | Selected claim | Result |
|---|---|---|
| `STRONGEST-EXTENSION-VERIFICATION` | `character-loop-correct` | exit 0, `#Top` |
| `STRONGEST-EXTENSION-WITH-CHAR-LOOP-LEMMA` | `extension-strength-correct` | exit 0, `#Top` |
| `STRONGEST-EXTENSION-WITH-STRENGTH-LEMMA` | `selection-loop-correct` | exit 0, `#Top` |
| `STRONGEST-EXTENSION-WITH-LOOP-LEMMAS` | `strongest-extension-correct` | exit 0, `#Top` |

The bounded claim logs are
[stage3_character_claim.log](/audit-output/evidence/stage3_character_claim.log),
[stage3_strength_claim.log](/audit-output/evidence/stage3_strength_claim.log),
[stage3_selection_claim.log](/audit-output/evidence/stage3_selection_claim.log),
and [stage3_entry_claim.log](/audit-output/evidence/stage3_entry_claim.log).
These establish derivability under each submitted theory, not the soundness of
the added rules.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `character-loop-correct` starts at a nonempty remaining string iterator in a
   fixed helper-call frame. It says the loop consumes the remaining characters,
   adds their ASCII uppercase/lowercase contributions to `score`, stores the
   final character, and resumes the arbitrary continuation. Its explicit cell
   shape is its precondition; it has no separate `requires`.

2. `extension-strength-correct` starts a call to `_extension_strength` on an
   arbitrary `str(CS)` in a normal caller frame. Its precondition requires that
   the caller's local map not shadow `_extension_strength`. It says the call
   returns `extensionStrength(CS)` and otherwise restores the caller state.

3. `selection-loop-correct` starts the outer loop over exactly three arbitrary
   string values. Its local state contains an initial best extension/strength,
   and `score` is constrained to the strength of the recorded last extension.
   It says the loop updates the state to the stable first-maximum fold over
   those three values.

4. `strongest-extension-correct` starts
   `Strongest_Extension(CLASS, [E1,E2,E3])` in a pristine, preconstructed module
   scope. It says the exact return value is
   `CLASS + "." + bestExtension([E1,E2,E3], E1,
   extensionStrength(E1))`.

The entry result is not a free variable, existential, tautology, or one-way
implication. It is an exact string expression. The theorem is nevertheless
limited to exactly three extensions. It proves nothing about nonempty lists of
length one, two, four, or more, although those are within the prompt and the
submitted Python happens to handle them.

### Program identity

The entry claim does not load `solution.mpy`. Instead, `verification.k` defines
four zero-argument AST constants and a `solutionScope` containing two closures.
Static comparison found those closure bodies to be the exact semantic ASTs in
the byte-verified submitted MPY:

- `characterStrengthBody`: both case tests and augmented assignments;
- `extensionStrengthBody`: initializations, character loop, and return;
- `selectionLoopBody`: helper call, strict comparison, and conditional updates;
- `strongestExtensionBody`: index 0, initial helper call, outer loop, and
  concatenating return.

Thus the current body is externally pinned by byte-identical translation plus
exact AST transcription, and the fixed call/frame/control rules execute those
bodies in the base helper claims. This pin is not itself a K theorem and is not
file-sensitive: the final `<k>` cell executes a duplicated AST closure rather
than loading the submitted MPY module. The formal entry also supplies a bare
read-only `list(ValSeq)` argument rather than a heap `ref` produced by a
`ListExpr`; the supplied semantics explicitly permits such bare claim inputs,
but equivalence to the ordinary heap-ref caller path is an informal
read-only-input bridge.

### Satisfiable precondition and ground substitution

An explicit satisfying instance is `CLASS = "C"`,
`E1 = "a"`, `E2 = "A"`, and `E3 = "B"`. The scores are `-1, 1, 1`, so stable
tie-breaking returns `C.A`. Both trusted and submitted Python return `C.A`.
The ground K claim also exits 0 with `#Top`.

The witness, exact configuration, commands, and statuses are in
[ground-entry-spec.k](/audit-output/evidence/ground-entry-spec.k) and
[stage4_ground.log](/audit-output/evidence/stage4_ground.log).

Adequacy limitations independent of the soundness failure are:

- exactly three extensions rather than every nonempty list;
- ASCII case predicates rather than the trusted canonical's full Python
  `isalpha()`/case behavior;
- an external AST-copy and unboxed-read-only-input bridge.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[k_rule_inventory.md](/audit-output/evidence/k_rule_inventory.md) is the
reviewer-generated exhaustive lexical inventory of every declaration, syntax
alternative, rule, claim, context, and relevant attribute line in
`reference-semantics`, `verification.k`, and `spec.k`. It has 1,429 lines and
SHA-256
`44cd1fb93b6321e0a2b75b0b8320a33fcdb8ec6a77733e190a7c36109d8a471a`.
Its generation command exited 0.

Inventory totals include 718 ordinary rules, 233 `syntax` declaration lines,
72 continued syntax alternatives, five contexts, one configuration, and four
claims. Of the 718 rules, 695 are in the byte-identical supplied semantics and
23 are candidate-local rules in `verification.k`.

All 695 supplied-semantics rules are part of the selected, trusted semantics
level rather than candidate proof extensions. Every one is enumerated in the
inventory. The program-relevant subset was traced rule by rule below; the
remaining supplied rules have heads for unused syntax, builtins, collections,
floats, comprehensions, dictionaries, sorting, slicing, or exceptions and
cannot rewrite any submitted-program or postcondition term. Opaque/concrete
float and sort boundaries are therefore not dependencies of these claims.

### Used-syntax coverage and control/state mapping

| Submitted construct | Declaration and operative supplied rules |
|---|---|
| `Module`, `FuncDef`, statements | `syntax.k`; `core.k` `#loadAll`/statement sequencing; `functions.k` closure binding |
| `Name`, `Int`, `Str` | `core.k` lexical `#look` and literal rules; `str.k` ASCII code model |
| `Assign`, `AugAssign` | `controls.k`; integer `+`/`-` in `int.k` |
| `For` over list/string | `controls.k` `#loop`; `list.k` and `str.k` iterator rules |
| `If` | strict syntax plus `controls.k` truth/branch rules |
| `Call`, `Attribute`, methods | `call.k` callee-before-arguments routing, frame lifecycle in `functions.k`, and `methods.k` `isupper`/`islower` |
| `Subscript(..., 0)` | evaluation contexts and in-bounds `valSeqAt` in `subscript.k` |
| `Compare(">")` | ordered evaluation in `operators.k`, integer comparison in `int.k` |
| `BinOp("+")` | left-to-right strictness, `operators.k`, and string concatenation in `str.k` |
| `Return` | strict return, `#pop`, environment/stack/scope restoration in `functions.k` |

For the formal exact-three/bare-list domain, the fixed rules have the required
evaluation order, lexical binding, stable strict comparison, local updates,
and call/return restoration. No used construct is silently fabricated by a
missing supplied rule.

### Candidate-local syntax, functions, and definitional rules

The six `syntax` declaration lines contain 12 proof-local productions. There
are no local `[simplification]`, `[concrete]`, `[functional]`, or
`[symbol]` declarations.

The first 19 local rules are definitional:

- `charContribution`, both `strengthAcc` equations, and
  `extensionStrength` truthfully define the ASCII score and structurally
  descend.
- Both `lastCharacter` equations truthfully preserve the previous character
  on empty input and select the last character on nonempty input.
- The three `bestExtension` and three `bestStrength` equations have disjoint
  `>` and `<=` guards and implement strict-improvement/stable-tie folds.
- Both `lastExtension` equations truthfully select the last processed string.
- The four AST-body equations and `solutionScope` are exact transcriptions of
  the submitted program.

`bestExtension`, `bestStrength`, and `lastExtension` are declared `[total]` but
only have head rules for empty sequences or `str` elements. Since `ValSeq` also
admits other `Val` constructors, these declarations are not exhaustively
covered globally. On the formal claim domain every element is explicitly a
`str`, so no opaque ill-typed case reaches the result. This is an over-broad
totality declaration/evidence gap, not the witnessed false equation.

### Four operational bridge rules

All four remaining local rules are priority-40 operational bridges:

1. The character-loop bridge (verification.k:107) skips the fixed loop and
   installs `strengthAcc`/`lastCharacter`. Its supporting claim fixes env `2`,
   module/builtin scopes, parent `0`, `scopeLoc = 3`, and normal
   return/exception/exit cells. The rule accepts arbitrary env location,
   surrounding scopes, parent, and omitted cells. The equations describe the
   intended normal state, but no bridge-free theorem covers the rule's complete
   match domain. I found no concrete false outcome on the intended normal
   states, so this is recorded as an unjustified context-broadening gap rather
   than labeled mathematically false.

2. The direct helper-call bridge (verification.k:142) rewrites
   `Call(Name("_extension_strength"), Name(X))` directly to
   `extensionStrength(CS)` whenever the current scope binds `X` to `str(CS)`.
   It does not perform or constrain lookup of `_extension_strength`. This rule
   is false.

3. The `#applyK` helper bridge (verification.k:156) matches the exact closure
   body and argument, but omits the normal return, stack, allocation, scope, and
   exception context covered by the helper claim. Its value equation is correct
   in the intended well-formed call state, but no bridge-free theorem covers its
   full matched context. Without a false witness on the intended normal state,
   this is an evidence/containment gap rather than an additional unsoundness
   finding.

4. The exact-three outer-loop bridge (verification.k:171) has the intended
   fold equations and fixes the relevant lexical maps, but omits
   `scopeLoc`, heap, stack, return, exception, and exit cells constrained by its
   supporting claim. Again, the supporting theorem's domain is narrower than
   the rule. No separate false conclusion is asserted for this rule.

### Concrete false conclusion witness for bridge 2

[bridge-shadow-spec.k](/audit-output/evidence/bridge-shadow-spec.k) uses ordinary
ASCII input `"A"` and a well-formed local scope in which
`_extension_strength` is lexically shadowed by a closure that returns `99`.
This state lies directly in the bridge rule's match domain.

The four-way comparison in
[stage5_bridge_witness.log](/audit-output/evidence/stage5_bridge_witness.log)
shows:

| Theory and obligation | Exit/result |
|---|---|
| Fixed supplied semantics, expected `99` | exit 0, `#Top` |
| Fixed supplied semantics, false expected `1` | exit 1, stuck at actual `99` |
| Candidate strength-lemma definition, false expected `1` | exit 0, `#Top` |
| Candidate strength-lemma definition, correct expected `99` | exit 1, stuck at fabricated `1` |

This is not an inference from a timeout or parser failure. Both successful
claims build and close; both rejected claims reach a final concrete value and
fail unification with the destination.

The candidate's `extension-strength-correct` claim does not repair the defect:
it requires no local `_extension_strength` binding and starts with a value
argument `str(CS)`. The operational bridge accepts a `Name(X)` argument and a
local shadow. Therefore the bridge match domain is not contained in the
bridge-free claim's justification domain. Priority makes the bad bridge preempt
the supplied `Call` rule; it does not establish lexical equivalence.

The final definition imports this false rule, and the entry derivation uses it
for the initial helper call with `Name("strongest")`; the selection proof also
uses the same strength-lemma definition. A globally false proof rule cannot be
validated merely because its use in one target state happens to select the
intended binding.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. I created
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k), copied it into scratch,
and changed the satisfying ground instance from its correct result `C.A` to the
false result `C.B`.

The dry run built the mutation successfully and exited 0. The actual proof run
exited 1 with `WarnStuckClaimState`; its residual contains the fully evaluated
actual result codes for `C.A` while the destination requires `C.B`. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.

Exact commands and statuses are in
[stage6_nonvacuity.sh](/audit-output/evidence/stage6_nonvacuity.sh) and
[stage6_nonvacuity.log](/audit-output/evidence/stage6_nonvacuity.log). The
bounded backend residual is
[stage6_mutation_proof.log](/audit-output/evidence/stage6_mutation_proof.log).

The entry claim is therefore result-constraining and non-vacuous under the
candidate theory. This does not rehabilitate the false operational rule used by
that theory.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

Under the candidate's extended theory, for arbitrary `IntSeq` values `CLASS`,
`E1`, `E2`, and `E3`, the preconstructed call configuration with exactly the
three bare string values terminates at:

```text
str(CLASS ++ "." ++
    stableFirstMaximum([E1,E2,E3], ASCIIUpperMinusLowerScore))
```

The three helper claims derive the character fold, helper value, and
exact-three selection fold used to obtain that result. The result is exact and
the fresh mutation proves that the theory discriminates a wrong return value.

Because the derivation imports a witnessed false operational rule, it does
**not** establish that theorem under the supplied semantics alone and is not a
legitimate partial-correctness proof of the real program.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Byte-identical supplied semantics | All execution, control, state, calls, and data representation | Authorized baseline; integrity passed |
| K Int/Bool/String/Map/List primitives and Haskell/LLVM backends | Arithmetic, maps, sequences, rewriting, proof search | Ordinary low-level toolchain trust |
| ASCII `str`/case model | Every helper score and formal result | Sound for ASCII; narrower than prompt/Python Unicode |
| In-bounds `valSeqAt` | Initial `extensions[0]` | Exact-three input makes the supplied concrete rule apply; OOB totality is not used |
| Candidate mathematical fold functions | Formal postcondition | Equations are truthful on the explicit all-string domain; some `[total]` annotations are globally incomplete |
| Duplicated AST bodies and `solutionScope` | Link from file to formal entry | Current AST matches byte-verified MPY, but the link is external rather than a K loading theorem |
| Bare list input | Formal API state | Sound-looking for this read-only function; equivalence to normal heap-ref caller is informal |
| Four operational bridges | Closure of helper/entry claims | One is concretely false; the other three lack full-domain connection theorems |
| Differential tests | Python/canonical intent bridge | Finite evidence only; exposes Unicode divergence |
| Missing provenance records | Reproducibility of generation history | Deficiency, though not an infrastructure blocker for this independent reconstruction |

There are no result-bearing external primitives or proof-local opaque symbols
that legitimately fix the target result. Unused opaque/concrete symbols in
float and sort portions of the supplied semantics are not dependencies.

### Final rationale

The clean reconstruction and non-vacuity gates pass, but legitimacy fails at
the mandatory static soundness gate. The direct helper-call bridge replaces
real lexical lookup with an answer-bearing summary on a broader domain than its
supporting claim. The preserved witness proves a false result under that rule.
The exactly-three and ASCII/Unicode restrictions, missing provenance files, and
external AST/unboxed-input bridges are additional adequacy and evidence
limitations, but the false operational rule alone requires `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
