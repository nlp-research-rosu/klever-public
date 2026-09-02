import Proof.Operational

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-1684a1226f0f56832d19a2311f81f35f276a3945a3d87268f06be40436a1f20b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool :=
  left && right
/- KORE symbol: LblapplyBuiltin'LParUndsCommUndsRParUnds'MPY-BUILTINS'Unds'Val'Unds'String'Unds'Vals; frozen source obligations: rule-ec057976d8c8f7e9534ebd2d518671f034dd02fd1170d6411f89c1fd1a2417c3. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»
    (name : SortString) (args : SortVals) : SortVal :=
  Operational.dispatchBuiltin name args
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-1684a1226f0f56832d19a2311f81f35f276a3945a3d87268f06be40436a1f20b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortBool :=
  Operational.dispatchComparison operator left right
/- KORE symbol: LblcodesOf'LParUndsRParUnds'VERIFICATION'Unds'IntSeq'Unds'Str; frozen source obligations: rule-ec057976d8c8f7e9534ebd2d518671f034dd02fd1170d6411f89c1fd1a2417c3, rule-1684a1226f0f56832d19a2311f81f35f276a3945a3d87268f06be40436a1f20b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «codesOf(_)_VERIFICATION_IntSeq_Str» (value : SortStr) : SortIntSeq :=
  Operational.stringPayload value
/- KORE symbol: LbldedupCodes'LParUndsRParUnds'MPY-SET'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-ec057976d8c8f7e9534ebd2d518671f034dd02fd1170d6411f89c1fd1a2417c3. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «dedupCodes(_)_MPY-SET_IntSeq_IntSeq»
    (codes : SortIntSeq) : SortIntSeq :=
  Operational.deduplicateCharacterCodes codes
/- KORE symbol: LbldefinedProjectStr'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0dda33275c7cbd1779ea25ffe3285879bf6652eca3210dd703138ffe06f5bf83, rule-ec057976d8c8f7e9534ebd2d518671f034dd02fd1170d6411f89c1fd1a2417c3, rule-1684a1226f0f56832d19a2311f81f35f276a3945a3d87268f06be40436a1f20b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectStr(_)_VERIFICATION_Bool_Val»
    (value : SortVal) : SortBool :=
  Operational.projectStringDefined value
/- KORE symbol: LblprojectStrTotal; frozen source obligations: rule-f85e27b93f985712e161e1d9f93c9edc4bb9b998f80b67e076ae37e57255f5e0, rule-ec057976d8c8f7e9534ebd2d518671f034dd02fd1170d6411f89c1fd1a2417c3, rule-1684a1226f0f56832d19a2311f81f35f276a3945a3d87268f06be40436a1f20b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectStrTotal (value : SortVal) : SortStr :=
  Operational.totalStringProjection value
/- KORE symbol: LblstrLt'LParUndsCommUndsRParUnds'MPY-STR'Unds'Bool'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-1684a1226f0f56832d19a2311f81f35f276a3945a3d87268f06be40436a1f20b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
    (left right : SortIntSeq) : SortBool :=
  Operational.lexicographicallyLess left right
/- KORE symbol: Lblproject'Coln'Str; frozen source obligations: rule-0dda33275c7cbd1779ea25ffe3285879bf6652eca3210dd703138ffe06f5bf83. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Str?» (term : SortK) : Option SortStr :=
  Operational.optionalStringProjection term

theorem final :
    Klean158FindMax.Lemmas.targetStatement _andBool_ «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «codesOf(_)_VERIFICATION_IntSeq_Str» «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» «definedProjectStr(_)_VERIFICATION_Bool_Val» projectStrTotal «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» «project:Str?» := by
  simp only [Klean158FindMax.Lemmas.targetStatement]
  constructor
  · intro value
    cases value <;>
      simp [«project:Str?», Operational.optionalStringProjection,
        «definedProjectStr(_)_VERIFICATION_Bool_Val»,
        Operational.projectStringDefined, inj]
  constructor
  · intro value
    cases value <;> rfl
  constructor
  · intro value isString
    cases value <;>
      simp_all [
        «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»,
        Operational.dispatchBuiltin,
        «definedProjectStr(_)_VERIFICATION_Bool_Val»,
        Operational.projectStringDefined,
        projectStrTotal,
        Operational.totalStringProjection,
        «codesOf(_)_VERIFICATION_IntSeq_Str»,
        Operational.stringPayload,
        «dedupCodes(_)_MPY-SET_IntSeq_IntSeq»
      ]
  · intro right left bothStrings
    cases left <;> cases right <;>
      simp_all [
        _andBool_,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        Operational.dispatchComparison,
        Operational.compareStrings,
        «definedProjectStr(_)_VERIFICATION_Bool_Val»,
        Operational.projectStringDefined,
        projectStrTotal,
        Operational.totalStringProjection,
        «codesOf(_)_VERIFICATION_IntSeq_Str»,
        Operational.stringPayload,
        «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
      ]

end Proof
