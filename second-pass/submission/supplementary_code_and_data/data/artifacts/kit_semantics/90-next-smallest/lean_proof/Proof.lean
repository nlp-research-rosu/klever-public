import Proof.Support

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0, rule-d010c14fc64f0f33dd28b1ec00706ade9980faa201a1db3fac9d2f2e55a066e0, rule-d3f3513c93e027de881c4a1afcfdd26ca1202897eb3fd37f1be702df77bc49a5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ : SortBool → SortBool → SortBool := fun left right => left && right
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-d010c14fc64f0f33dd28b1ec00706ade9980faa201a1db3fac9d2f2e55a066e0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» : SortInt → SortInt → SortBool := fun left right => left < right
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-d3f3513c93e027de881c4a1afcfdd26ca1202897eb3fd37f1be702df77bc49a5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» : SortInt → SortInt → SortBool := fun left right => left != right
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» : SortInt → SortInt → SortInt := fun left right => left + right
/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» : SortString → SortVal → SortVal → SortVal :=
  ProofOperational.applyBinComplete
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-d010c14fc64f0f33dd28b1ec00706ade9980faa201a1db3fac9d2f2e55a066e0, rule-d3f3513c93e027de881c4a1afcfdd26ca1202897eb3fd37f1be702df77bc49a5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool :=
  ProofOperational.applyCmpComplete
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false
/- KORE symbol: LblisInt; frozen source obligations: rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0, rule-d010c14fc64f0f33dd28b1ec00706ade9980faa201a1db3fac9d2f2e55a066e0, rule-d3f3513c93e027de881c4a1afcfdd26ca1202897eb3fd37f1be702df77bc49a5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» : SortK → SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => value
  | _ => 0
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d, rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0, rule-d010c14fc64f0f33dd28b1ec00706ade9980faa201a1db3fac9d2f2e55a066e0, rule-d3f3513c93e027de881c4a1afcfdd26ca1202897eb3fd37f1be702df77bc49a5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal : SortVal → SortInt
  | SortVal.inj_SortInt value => value
  | _ => 0
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => some value
  | _ => none

theorem injectedValue_isInt_only_if_integer
    (value : SortVal)
    (h : isInt (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) = true) :
    ∃ integer, value = SortVal.inj_SortInt integer := by
  cases value <;> simp_all [isInt, inj]

theorem final :
    Klean90NextSmallest.Lemmas.targetStatement _andBool_ «_<Int_» «_=/=Int_» «_+Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» isInt «project:Int» projectIntTotal «project:Int?» := by
  unfold Klean90NextSmallest.Lemmas.targetStatement
  constructor
  · intro value
    cases value <;>
      simp [«project:Int?», «definedProjectInt(_)_VERIFICATION_Bool_Val», inj]
  constructor
  · intro value defined
    cases value <;>
      simp_all [«definedProjectInt(_)_VERIFICATION_Bool_Val», «project:Int»,
        projectIntTotal, inj]
  constructor
  · intro right left integerOperands
    have operands :
        isInt (SortK.kseq ((@inj SortVal SortKItem) left) SortK.dotk) = true ∧
        isInt (SortK.kseq ((@inj SortVal SortKItem) right) SortK.dotk) = true := by
      simpa only [_andBool_, Bool.and_eq_true] using integerOperands
    obtain ⟨leftInt, rfl⟩ := injectedValue_isInt_only_if_integer left operands.1
    obtain ⟨rightInt, rfl⟩ := injectedValue_isInt_only_if_integer right operands.2
    simp [projectIntTotal, «_+Int_»,
      «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
      ProofOperational.applyBinComplete, ProofOperational.stringCodes?]
  constructor
  · intro right left integerOperands
    have operands :
        isInt (SortK.kseq ((@inj SortVal SortKItem) left) SortK.dotk) = true ∧
        isInt (SortK.kseq ((@inj SortVal SortKItem) right) SortK.dotk) = true := by
      simpa only [_andBool_, Bool.and_eq_true] using integerOperands
    obtain ⟨leftInt, rfl⟩ := injectedValue_isInt_only_if_integer left operands.1
    obtain ⟨rightInt, rfl⟩ := injectedValue_isInt_only_if_integer right operands.2
    simp [projectIntTotal, «_<Int_»,
      «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      ProofOperational.applyCmpComplete, ProofOperational.stringCodes?]
  · intro right left integerOperands
    have operands :
        isInt (SortK.kseq ((@inj SortVal SortKItem) left) SortK.dotk) = true ∧
        isInt (SortK.kseq ((@inj SortVal SortKItem) right) SortK.dotk) = true := by
      simpa only [_andBool_, Bool.and_eq_true] using integerOperands
    obtain ⟨leftInt, rfl⟩ := injectedValue_isInt_only_if_integer left operands.1
    obtain ⟨rightInt, rfl⟩ := injectedValue_isInt_only_if_integer right operands.2
    simp [projectIntTotal, «_=/=Int_»,
      «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      ProofOperational.applyCmpComplete, ProofOperational.stringCodes?,
      ProofOperational.isNoneValue]

end Proof
