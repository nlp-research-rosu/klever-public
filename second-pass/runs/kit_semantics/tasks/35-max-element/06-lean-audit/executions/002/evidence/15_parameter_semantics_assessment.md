# Independent operational-parameter assessment

`11_candidate_structure.out` records the exact manifest type, KORE symbol,
source-rule IDs, candidate line, and candidate body for every parameter. The
semantic decisions below compare those bodies with the frozen K equations and
the `return max(l)` source path.

| Candidate parameter (line) | Independent operational comparison | Result |
|---|---|---|
| `_andBool_` (441) | `Bool.and` on both operands, matching K `andBool` in the numeric/string guards. | Match |
| `_orBool_` (443) | `Bool.or` on both operands, matching K `orBool` in the sort-disjointness rules. | Match |
| `«_>Int_»` (445) | Lean integer `>` over unbounded `Int`, matching K `>Int`. | Match |
| `«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»` (447) | For every source-obligation domain (`">"` on Int/Bool/Float mixtures or Str/Str), dispatch, Bool promotion, exact Int/Float comparison, and string direction match `int.k`, `bool.k`, `float.k`, and `str.k`. | Match on the complete obligation/source-program domain |
| `«codesOf(_)_VERIFICATION_IntSeq_Str»` (449) | Projects the sole `str(IntSeq)` constructor, exactly the line 93 definition. | Match |
| `isBool` (451) | True exactly for the Bool injection in a one-item K sequence. | Match |
| `isFloat` (453) | True exactly for the Float injection in a one-item K sequence. | Match |
| `isInt` (455) | True exactly for the Int injection in a one-item K sequence. | Match |
| `«isNumericV(_)_VERIFICATION_Bool_Val»` (457) | True exactly for Int, Bool, or Float `Val`, matching lines 29–31. | Match |
| `isStr` (459) | True exactly for the Str injection in a one-item K sequence. | Match |
| `maxFOpaque` (461) | Bound to `floatMaxImpl`. Frozen line 62 makes this concrete twin evaluate as K `maxFloat`. The helper returns a NaN operand instead of K `FLOAT.max`'s non-NaN operand. | **Mismatch** |
| `«maxFloat(_,_)_FLOAT_Float_Float_Float»` (463) | Also bound to the same incorrect `floatMaxImpl`; direct frozen K executions give `maxFloat(NaN, 1.0) = 1.0` and `maxFloat(1.0, NaN) = 1.0`, whereas both candidate calls report `isNaN = true`. | **Mismatch** |
| `«numericGt(_,_)_VERIFICATION_Bool_NumericView_NumericView»` (465) | Exhaustive Int/Bool/Float table and `nOther` default match lines 113–129, including exact mixed Int/Float comparisons and strict greater-than. | Match |
| `«numericView(_)_VERIFICATION_NumericView_Val»` (467) | Tags Int, Bool, and Float and sends all other `Val` constructors to `nOther`, matching lines 101–109. | Match |
| `«project:Bool»` (469) | Returns the Bool payload on the guarded cast domain; its off-domain default is not observed by its guarded obligation. | Match on obligation domain |
| `«project:Float»` (471) | Returns the Float payload on the guarded cast domain; its off-domain default is not observed by its guarded obligation. | Match on obligation domain |
| `«project:Int»` (473) | Returns the Int payload on the guarded cast domain; its off-domain default is not observed by its guarded obligation. | Match on obligation domain |
| `«project:Str»` (475) | Returns the Str payload on the guarded cast domain; its off-domain default is not observed by its guarded obligation. | Match on obligation domain |
| `projectBoolTotal` (477) | Returns the Bool payload for a Bool-valued `Val`, exactly the guarded proof-local total projection use. | Match |
| `projectFloatTotal` (479) | Returns the Float payload for a Float-valued `Val`, exactly the guarded proof-local total projection use. | Match |
| `projectIntTotal` (481) | Returns the Int payload for an Int-valued `Val`, exactly the guarded proof-local total projection use. | Match |
| `projectStrTotal` (483) | Returns the Str payload for a Str-valued `Val`, exactly the guarded proof-local total projection use. | Match |
| `«strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq»` (485) | Structural lexicographic order matches all six cases at `str.k` lines 48–54. | Match |
| `«project:Bool?»` (487) | `some` exactly for the Bool cast pattern and `none` otherwise, matching the partial K cast's definedness. | Match |
| `«project:Float?»` (489) | `some` exactly for the Float cast pattern and `none` otherwise, matching the partial K cast's definedness. | Match |
| `«project:Int?»` (491) | `some` exactly for the Int cast pattern and `none` otherwise, matching the partial K cast's definedness. | Match |
| `«project:Str?»` (493) | `some` exactly for the Str cast pattern and `none` otherwise, matching the partial K cast's definedness. | Match |

## Adversarial and counterfactual results

- `09b_k_adversarial_run.out`: the pinned K 7.1.293 LLVM semantics reduces both
  `maxFloat(NaN, 1.0)` and `maxFloat(1.0, NaN)` to `1.0`.
- `13_frozen_program_adversarial.out`: the actual frozen source program passes
  assertions that `max_element([NaN, 1.0])` and `max_element([1.0, NaN])` are
  `1.0`; both executions terminate normally.
- `08_lean_adversarial.out`: the corresponding candidate `maxFOpaque` and
  `maxFloat` calls all return a NaN (`true` from `.isNaN`).
- `10_counterfactual.out`: replacing both public Float-max parameter bodies by
  the constant `fun _ _ => 0.0` still clean-builds `Proof.final`, with the same
  axiom list. Thus the proof only uses the convenient equality of the two
  definitions and does not establish either definition's operational meaning.

This is an operational-bridge failure on the formal source domain, not an
unreachable edge case: Stage 1's Float claim has no finite/non-NaN precondition,
and `NaN` is a represented `Float` in the supplied semantics.
