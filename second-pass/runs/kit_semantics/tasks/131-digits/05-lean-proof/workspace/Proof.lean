import Klean131Digits.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-b09bdfe5e2bc74b215bed27c498fc03e78a4929071d23d07a626110c519fed02. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (x y : SortInt) : SortInt := x - y
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-b09bdfe5e2bc74b215bed27c498fc03e78a4929071d23d07a626110c519fed02. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-082958cd68b6ff48e923703bfbdc398fbdc293247656d1a01d3339fbcf725de4, rule-2ab4c7bc73ad01bbe3db34c2b3cc0d6c95c87c850e1e3f40e6891b9a061c05a7, rule-6c033d38e2e8c948160d245d94624fb6c578d69ea99fc1c15c896b557eaa1ee3. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (x y : SortInt) : SortInt := x * y

theorem final :
    Klean131Digits.Lemmas.targetStatement «_-Int_» «_+Int_» «_*Int_» := by
  simp only [Klean131Digits.Lemmas.targetStatement, «_-Int_», «_+Int_»,
    «_*Int_»]
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro X
    simp
  · intro X
    simp
  · intro X
    simpa [Int.add_comm] using Int.add_sub_cancel 1 X
  · intro Z Y X
    exact Int.mul_assoc X Y Z

end Proof
