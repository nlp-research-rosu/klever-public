import Klean84Solve.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean84Solve.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_andBool_ : SortBool → SortBool → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    («_%Int_» : SortInt → SortInt → SortInt)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_/Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (Q : SortInt) (D : SortInt) (h : (_andBool_ («_<=Int_» 0 D) («_<Int_» D 10)) = true), («_%Int_» («_+Int_» («_%Int_» («_+Int_» D («_*Int_» 10 Q)) 10) 10) 10 : SortInt) = (D : SortInt))
    ∧ (∀ (D : SortInt) (Q : SortInt) (h : (_andBool_ («_<=Int_» 0 D) («_<Int_» D 10)) = true), («_/Int_» («_-Int_» («_+Int_» D («_*Int_» 10 Q)) D) 10 : SortInt) = (Q : SortInt))

end Klean84Solve.Lemmas
