import Klean94Skjkasdkd.Lemmas

namespace AuditDegenerate

def badMap (_left right : SortMap) : SortMap := right
def badInKeys (_key : SortKItem) (_map : SortMap) : SortBool := false
def badDelete (map : SortMap) (_key : SortKItem) : SortMap := map
def badItem (_key _value : SortKItem) : SortMap := ⟨[]⟩
def badUpdate (map : SortMap) (_key _value : SortKItem) : SortMap := map
def honestNot (value : SortBool) : SortBool := !value

theorem degenerate_parameters_still_prove_target :
    Klean94Skjkasdkd.Lemmas.targetStatement
      badMap badInKeys badDelete badItem badUpdate honestNot := by
  constructor <;> simp [badMap, badInKeys, badDelete, badItem, badUpdate]

end AuditDegenerate
