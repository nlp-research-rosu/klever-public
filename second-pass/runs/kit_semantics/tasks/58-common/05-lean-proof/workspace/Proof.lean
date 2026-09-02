import Klean58Common.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'orBool'Unds'; frozen source obligations: rule-cd11c71e1459d61e91176cc439f01696c9d8116dd9313d8d67eb714d1144a5b0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _orBool_ (left right : SortBool) : SortBool :=
  left || right
/- KORE symbol: Lbl'UndsEqlsEqls'K'Unds'; frozen source obligations: rule-cd11c71e1459d61e91176cc439f01696c9d8116dd9313d8d67eb714d1144a5b0. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_==K_» (left right : SortK) : SortBool := by
  classical
  exact decide (left = right)
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-cd11c71e1459d61e91176cc439f01696c9d8116dd9313d8d67eb714d1144a5b0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

theorem final :
    Klean58Common.Lemmas.targetStatement _orBool_ «_==K_» notBool_ := by
  simp_all [Klean58Common.Lemmas.targetStatement, _orBool_, «_==K_», notBool_]

end Proof
