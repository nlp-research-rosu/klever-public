# Exhaustive local K inventory

This inventory covers the candidate source files copied byte-for-byte to
`/tmp/audit-work/93-encode`. Line numbers are those of the candidate files.
`OK(target)` means sound for the exact submitted program and its intended
ASCII-letter/space executions; it does not claim a general Python semantics.

## `semantic.k`: syntax and configuration

- Lines 7–15: `Pgm = Module(Stmts)`; list sorts `Stmts`, `Exprs`, `CmpOps`,
  and `Strings`; constructors `Params(Strings)` and `CmpOp(String,Expr)`.
- Lines 17–23: expression constructors `Name`, `Str`, `Int`, `BinOp`,
  `Compare`, `Call`, and `Attribute`.
- Lines 25–30: statement constructors `FuncDef`, `Assign`, `AugAssign`,
  `For`, `If`, and `Return`.
- Lines 41–43: values `pyStr`, `pyInt`, `pyBool`; closures
  `closure(Params,Stmts)`; results `noResult` and `returned(KItem)`.
- Lines 45–50: injections plus control terms `execStmts`, `invoke`,
  `startFor`, `loopString`, and `vowelBranch`.
- Lines 54, 161–166, 189, and 191–192: local function declarations:
  `encodeLoopBody`; `eval`; `plusValue`; `inValue`; `ordValue`; `chrValue`;
  `swapCaseValue`; and `swapCaseChar`, `encodedChar`, `advancedVowel`.
  The final three have `[function,total]`; in the abstract `SEMANTIC` module
  they have no defining equations and are result-bearing opaque symbols.
  There are no local `[functional]` declarations.
- Lines 68–74: one `<python>` configuration containing `<k>`, `<env>`,
  `<functions>`, and `<result>`. Initial `<k>` parses `$PGM` and then invokes
  `encode` on `$MESSAGE`; the three state cells start empty/no-result.

Every constructor in `solution.mpy` is declared: `Module`, `FuncDef`,
`Params`, `Assign`, `Name`, `Str`, `For`, `If`, `Compare`, `CmpOp`, `Call`,
`BinOp`, `Int`, `AugAssign`, `Attribute`, and `Return`, including empty
`Stmts` and `Exprs`. There are no used-but-undeclared constructs.

## `semantic.k`: rules

1. Lines 55–66, `encodeLoopBody`: exact syntactic abbreviation for the
   translated `If` followed by `AugAssign`. `OK(target)`.
2. Line 76, `Module`: enters sequential statement execution. `OK(target)`.
3. Lines 78–79, `execStmts`: empty and head/tail sequencing. `OK(target)`.
4. Lines 81–82, `FuncDef`: records a closure in `<functions>`.
   `OK(target)` for the module-level, capture-free function.
5. Lines 84–86, `invoke`: selects the stored closure, binds its one parameter,
   and starts its body. It has no call frame or environment restoration, but
   the submitted program has one top-level invocation and no user-function
   calls. `OK(target)`; incomplete as general Python.
6. Lines 88–89, `Assign`: atomically evaluates and updates a named binding.
   `OK(target)` because all target expressions are pure in this subset.
7. Lines 91–92, `AugAssign("+")`: looks up the old value, evaluates the RHS,
   and stores `plusValue`. `OK(target)` for the string accumulation.
8. Lines 94–96, exact vowel-membership `If`: reads the named string and enters
   `vowelBranch`. `OK(target)` for one-character loop values.
9. Lines 98–107: ten separate true-branch rules for
   `a,e,i,o,u,A,E,I,O,U`. Each is `OK(target)`.
10. Line 108: `[owise]` false-branch rule for every other string.
    `OK(target)` for reachable one-character values. It is over-broad for an
    arbitrary empty string (`"" in "aeiouAEIOU"` is true in Python), but no
    submitted-program execution supplies an empty loop element, so this is
    recorded as a scope limitation rather than an intended-domain
    unsoundness.
11. Lines 110–111, `For`: evaluates the iterable once and starts a loop.
    `OK(target)` for a string iterable.
12. Line 113, `startFor`: converts a `pyStr` to `loopString`. `OK(target)`.
13. Lines 115–116, empty `loopString`: terminates at length zero. `OK`.
14. Lines 120–146, exact fused loop iteration, `[priority(40)]`: matches the
    entire submitted loop body, consumes one character, directly appends
    `encodedChar(first)`, directly writes `advancedVowel(first)` to `char`,
    and preserves the remaining map and continuation. In `CONCRETE`, its
    footprint and result agree with the generic rules on the tested
    one-character ASCII domain. In the abstract proof definition, however,
    both RHS values are opaque; the rule is an operational bridge from a
    program-defined body to unconstrained, result-bearing oracles. **FAIL**.
    The concrete false-conclusion witness is input `"a"` with result `"X"`:
    `oracle-witness.k` supplies a permitted wrong interpretation and both its
    false loop and false entry claims prove `#Top`, while both Python programs
    return `"C"`.
15. Lines 148–155, nonempty generic `loopString`, `[owise]`: binds the first
    character, executes the body, then recurs on the suffix. `OK(target)`.
    The `owise` makes it secondary to the exact fused rule.
16. Lines 157–159, `Return`: stores the evaluated result and removes only the
    `Return` term. The target `Return` is last, so this is `OK(target)`.
    It would incorrectly continue statements after a return in a broader
    language; no such control flow exists in the submitted program.
17. Line 168, `eval(Name)`: map lookup. `OK(target)`.
18. Line 169, map-update lookup `[simplification]`: reads back the most recent
    update. This is a valid map equation.
19. Lines 170–171, `eval(Str)` and `eval(Int)`: literal injection.
    `OK(target)`.
20. Lines 172–175, `eval(BinOp("+"))` and `eval(Compare(...,"in",...))`:
    dispatch to pure helpers. `OK(target)`.
21. Lines 176–179, calls to `ord`, `chr`, and zero-argument `swapcase`:
    dispatch to their helpers. `OK(target)` with the exact bindings and
    one-character values used here; this is not a general name-resolution or
    method model.
22. Lines 181–182, integer and string `plusValue`: valid K integer addition
    and string concatenation.
23. Lines 183–184, string `inValue`: uses `findString >= 0`; valid string
    containment for its modeled values.
24. Lines 185–187, `ordValue`, `chrValue`, and `swapCaseValue`: bridge to
    `ordChar`, `chrChar`, and the local `swapCaseChar`. `OK(target)` for
    reachable one-character ASCII values. `ordChar`/`chrChar` behavior outside
    their valid domains is not modeled.

The only local simplification rule is line 169. The only explicit numeric
priority is the fused rule's `priority(40)`. The two local `[owise]` rules are
line 108 (vowel else) and lines 148–155 (generic loop).

## `concrete.k`

1. Lines 9–17, `swapCaseChar(C)`: ASCII uppercase adds 32, ASCII lowercase
   subtracts 32, otherwise preserves `C`. This matches Python `swapcase` for
   all reachable ASCII letters and spaces. Because `C` is syntactically any
   `String` and the declaration is `[total]`, empty/multi-character inputs can
   leave `ordChar(C)` outside its supported domain, and non-ASCII letters do
   not implement Python Unicode case conversion. Those cases are outside the
   intended English-letter domain, so this is a documented coverage/totality
   limitation, not an intended-domain false-rule finding.
2. Lines 19–27, `advancedVowel(C)`: adds two code points for exactly the ten
   ASCII vowels and otherwise preserves `C`. `OK(target)`.
3. Line 29, `encodedChar(C) = swapCaseChar(advancedVowel(C))`:
   mathematically correct for one reachable ASCII character. It is the
   property-bearing summary used by the fused bridge, not a fixed external
   primitive. The candidate supplies no auxiliary fixed-semantics connection
   theorem, and the abstract proof does not import these equations.

There are no local syntax declarations, priorities, simplifications, claims,
or `[functional]` declarations in `concrete.k`.
`concrete-verification.k` has only imports and no declarations or rules.

## `verification.k`

1. Line 8: `encodeSpec(String) [function]`.
2. Lines 10–14: base equation at length zero and recursive equation at
   nonzero length. Guards are exhaustive for K strings; recursion removes one
   character. The equations truthfully fold `encodedChar`, but therefore do
   not independently define the prompt's encoding while `encodedChar` is
   opaque.
3. Lines 17–18: right and left identity for `+String`,
   `[simplification]`. Valid.
4. Lines 19–20: right-association of `+String`, `[simplification]`. Valid and
   oriented toward decreasing left nesting. The three string equations agree
   on overlaps.
5. Lines 24–25: nullary functions `encodeBody()` and `encodeProgram()`.
6. Lines 27–30: `encodeBody` expands to the exact translated assignment,
   `For` over `message` with `encodeLoopBody`, and final `Return`.
7. Lines 32–34: `encodeProgram` expands to the exact `Module(FuncDef(...))`
   constructor tree. Together with `encodeLoopBody`, it is constructor-for-
   constructor identical to regenerated `solution.mpy`.

No declaration is `[total]` or `[functional]` here. There are no priorities
or `owise` rules.

## `spec.k` claims

1. `SPEC.encode-loop-correct` (lines 9–21): a symbolic internal-loop claim
   over arbitrary strings/maps/result state. It is not an entry-point claim
   and its postcondition is defined with the same opaque `encodedChar` used by
   the fused bridge.
2. `CONCRETE-SPEC.example-test` (lines 30–34): exact ground entry execution
   for `"test"` returning `"TGST"`.
3. `CONCRETE-SPEC.example-message` (lines 36–40): exact ground entry
   execution for `"This is a message"`.
4. `CONCRETE-SPEC.ascii-domain` (lines 44–55): one exact ground entry
   execution containing all 52 ASCII letters and one space.

There is no universal entry-point reachability claim and no claim connecting
unfused execution of the program-defined loop body to `encodedChar`.

## Imported trust boundary

The local files rely on K's built-in `Map` lookup/update, arbitrary-precision
`Int` operations and comparisons, `Bool` operations and `#if`, and String
operations `lengthString`, `substrString`, `+String`, `findString`, `ordChar`,
and `chrChar`. These are ordinary low-level K primitives and are acceptable
for this proof level on valid ASCII inputs. They do not supply the missing
program-body-to-`encodedChar` theorem.
