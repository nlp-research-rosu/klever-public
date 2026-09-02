import Klean57Monotonic.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'orBool'Unds'; frozen source obligations: rule-9da3d0e2a43f2a59d88512067068ed2de6ddc5b6972e73b0a57e10a6e46fc33d, rule-26e479bca972e68e6643e9eb5546744b4b881a595b804fd4fd237f23c16a00d4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _orBool_ : SortBool → SortBool → SortBool := fun a b => a || b
/- KORE symbol: Lbl'UndsEqlsEqls'Bool'Unds'; frozen source obligations: rule-9da3d0e2a43f2a59d88512067068ed2de6ddc5b6972e73b0a57e10a6e46fc33d, rule-26e479bca972e68e6643e9eb5546744b4b881a595b804fd4fd237f23c16a00d4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Bool_» : SortBool → SortBool → SortBool := fun a b => a == b
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-26e479bca972e68e6643e9eb5546744b4b881a595b804fd4fd237f23c16a00d4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ : SortBool → SortBool := fun a => !a

theorem final :
    Klean57Monotonic.Lemmas.targetStatement _orBool_ «_==Bool_» notBool_ := by
  constructor
  · intro B A h
    cases A
    · cases h
    · cases B <;> rfl
  · intro B A h
    cases A
    · cases B <;> rfl
    · cases h

end Proof
