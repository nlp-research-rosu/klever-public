import Klean115MaxFill.Lemmas

namespace Proof

/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'MAX-FILL-SUMMARY'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val» : SortVal → SortBool
  | .inj_SortInt _ => true
  | _ => false
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt
  | .kseq (.inj_SortInt i) .dotk => some i
  | _ => none

theorem final :
    Klean115MaxFill.Lemmas.targetStatement «definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val» «project:Int?» := by
  have andTrue (p : Prop) : p ↔ p ∧ True :=
    ⟨fun hp => ⟨hp, True.intro⟩, fun hp => hp.1⟩
  intro V
  cases V <;> exact andTrue _

end Proof
