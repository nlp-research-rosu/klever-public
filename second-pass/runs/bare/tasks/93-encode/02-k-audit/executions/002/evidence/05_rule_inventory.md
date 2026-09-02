# Local K rule inventory

This inventory covers every local declaration, rule, and claim in
`semantic.k`, `concrete.k`, `concrete-verification.k`, `verification.k`, and
`spec.k`. Imported K builtins are accounted for separately in the trust ledger.

## Syntax and configuration

- `semantic.k:7`: `Pgm ::= Module(Stmts)`.
- `semantic.k:9-12`: list sorts `Stmts`, `Exprs`, `CmpOps`, and `Strings`.
- `semantic.k:14-15`: `Params(Strings)` and `CmpOp(String, Expr)`.
- `semantic.k:17-23`: expression constructors `Name`, `Str`, `Int`, `BinOp`,
  `Compare`, `Call`, and `Attribute`.
- `semantic.k:25-30`: statement constructors `FuncDef`, `Assign`, `AugAssign`,
  `For`, `If`, and `Return`.
- `semantic.k:41-43`: values `pyStr`, `pyInt`, `pyBool`; closures; and
  `noResult`/`returned`.
- `semantic.k:45-50`: K-item injections plus `execStmts`, `invoke`, `startFor`,
  `loopString`, and `vowelBranch`.
- `semantic.k:54`: function-valued statement macro `encodeLoopBody`.
- `semantic.k:68-74`: cells `<k>`, `<env>`, `<functions>`, and `<result>`;
  initial execution is `$PGM ~> invoke("encode", pyStr($MESSAGE))`.
- `semantic.k:161-166`: functions `eval`, `plusValue`, `inValue`, `ordValue`,
  `chrValue`, and `swapCaseValue`.
- `semantic.k:189-192`: total functions `swapCaseChar`, `encodedChar`, and
  `advancedVowel`. They have no equations in module `SEMANTIC` and are opaque
  in the submitted universal proof definition.
- `verification.k:8,24-25`: functions `encodeSpec`, `encodeBody`, and
  `encodeProgram`.
- There are no local `[functional]` or separately named opaque declarations.
  Opacity here means that a declared `[function,total]` has no imported
  evaluator in the definition used for the universal claim.

## `semantic.k` rules (41)

1. `55-66`: `encodeLoopBody` expands to the exact `if` plus `AugAssign` body.
2. `76`: a module schedules its statement list.
3. `78`: empty statement execution terminates.
4. `79`: a nonempty statement list executes head before tail.
5. `81-82`: a function definition installs a closure by name.
6. `84-86`: invocation looks up a one-parameter closure and binds its argument.
7. `88-89`: name assignment evaluates then updates the environment.
8. `91-92`: `+=` reads the old binding and updates it with `plusValue`.
9. `94-96`: the exact used membership test becomes `vowelBranch`.
10. `98`: lowercase `a` chooses the then branch.
11. `99`: lowercase `e` chooses the then branch.
12. `100`: lowercase `i` chooses the then branch.
13. `101`: lowercase `o` chooses the then branch.
14. `102`: lowercase `u` chooses the then branch.
15. `103`: uppercase `A` chooses the then branch.
16. `104`: uppercase `E` chooses the then branch.
17. `105`: uppercase `I` chooses the then branch.
18. `106`: uppercase `O` chooses the then branch.
19. `107`: uppercase `U` chooses the then branch.
20. `108`: `[owise]` chooses the else branch for other strings.
21. `110-111`: the used `for` form evaluates the iterable.
22. `113`: a string iterable becomes a string loop.
23. `115-116`: a zero-length string loop terminates.
24. `120-146`: `[priority(40)]` fused exact-body loop step. It consumes one
    character but directly writes `encodedChar(first)` and
    `advancedVowel(first)`, bypassing `If`, `Assign`, `ord`, `chr`,
    `swapcase`, and `AugAssign`.
25. `148-155`: generic `[owise]` string loop step, which binds the first
    character, executes the real body, and recurs.
26. `157-159`: return records the evaluated value.
27. `168`: name evaluation performs map lookup.
28. `169`: `[simplification]` says lookup after update at the same key returns
    the updated value.
29. `170`: string literal evaluation.
30. `171`: integer literal evaluation.
31. `172-173`: `+` evaluation delegates to `plusValue`.
32. `174-175`: `in` evaluation delegates to `inValue`.
33. `176`: builtin `ord` call evaluation.
34. `177`: builtin `chr` call evaluation.
35. `178-179`: zero-argument `swapcase` method evaluation.
36. `181`: integer addition.
37. `182`: string concatenation.
38. `183-184`: string membership via `findString`.
39. `185`: `ord` bridge to K's `ordChar`.
40. `186`: `chr` bridge to K's `chrChar`.
41. `187`: `swapcase` delegates to opaque `swapCaseChar`.

Rules 1-23 and 25-41 are adequate for the exact submitted ASCII-English
program path: pure subexpressions have no state-order issue; the closure does
not need captured globals; `Return` is last; and the loop guards are disjoint.
The vowel rules and `[owise]` are disjoint, as are zero/nonzero loop guards.
The semantics is intentionally incomplete for unused Python forms.

Rule 24 is an operational bridge and is not justified in the abstract proof
definition. Its result-bearing `encodedChar` is the same symbol used by the
postcondition's `encodeSpec`; no bridge-free connection theorem fixes its
value. Evidence `05_bridge_opposite_fused.log` and
`05_bridge_opposite_bridgefree.log` gives a false conclusion on input `"a"`:
bridge-enabled execution returns `"!"`, while fixed body execution under the
same legal interpretation returns `"c"`. Evidence
`05_bridgefree_positive_residual.log` shows the submitted proof then fails on
the missing equality.

## `concrete.k` rules (3)

1. `9-17`: `swapCaseChar` changes ASCII A-Z/a-z by 32 and otherwise preserves
   its argument.
2. `19-27`: `advancedVowel` adds two code points exactly for the ten listed
   ASCII vowels and otherwise preserves its argument.
3. `29`: `encodedChar = swapCaseChar(advancedVowel(C))`.

The rules do not overlap because each symbol has one equation. They are correct
for one-character English letters and the spaces exercised by the program.
They are not full Python `str.swapcase` semantics on arbitrary Unicode letters:
`05_unicode_semantics_witness.log` records Python `"é" -> "É"` while the K
definition returns `"é"`. The prompt's reference to the English alphabet makes
this an excluded-model limitation rather than the primary verdict basis.

`concrete-verification.k` only imports `CONCRETE` and `VERIFICATION`; it adds no
syntax or rules.

## `verification.k` rules (7)

1. `10`: `encodeSpec` returns empty for a zero-length string.
2. `11-14`: for nonempty strings, `encodeSpec` prepends `encodedChar(first)`
   and recurses on the tail.
3. `17`: `[simplification]` right identity of string concatenation.
4. `18`: `[simplification]` left identity of string concatenation.
5. `19-20`: `[simplification]` associativity, oriented to the right.
6. `27-30`: `encodeBody` expands to initialization, the exact loop, and return.
7. `32-34`: `encodeProgram` expands to the exact one-function module.

The `encodeSpec` guards are disjoint and cover K strings; recursion decreases
length. All three string simplifications are ordinary true equalities.
`encodeBody` and `encodeProgram` are definitional constructors. The problem is
not these equations themselves; it is that `encodeSpec` and fused execution
share the unconstrained `encodedChar`.

## Claims in `spec.k` (4)

1. `SPEC.encode-loop-correct` (`9-21`): universal loop summary in the abstract
   definition.
2. `CONCRETE-SPEC.example-test` (`30-34`): ground entry claim for `"test"`.
3. `CONCRETE-SPEC.example-message` (`36-40`): ground entry claim for
   `"This is a message"`.
4. `CONCRETE-SPEC.ascii-domain` (`44-55`): one ground entry claim containing
   each ASCII English letter once plus one space.

The last claim is not an ASCII-domain theorem: it proves one 53-character
input, not arbitrary strings over that alphabet. No claim universally connects
`encodeProgram() ~> invoke("encode", pyStr(S))` to `encodeSpec(S)` or to the
source contract.
