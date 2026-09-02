import Klean63Fibfib.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-0680c25a908725567264bc3a1d17a1d702f13c46cc6da2b783839bbc14a5d477. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» : SortInt → SortInt → SortInt := Int.sub
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-0680c25a908725567264bc3a1d17a1d702f13c46cc6da2b783839bbc14a5d477. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» : SortInt → SortInt → SortInt := Int.add

theorem final :
    Klean63Fibfib.Lemmas.targetStatement «_-Int_» «_+Int_» := by
  intro N I
  change Int.sub I (Int.add N 1) = Int.add (Int.sub I N) (-1)
  exact (Int.sub_sub I N 1).symm

end Proof
