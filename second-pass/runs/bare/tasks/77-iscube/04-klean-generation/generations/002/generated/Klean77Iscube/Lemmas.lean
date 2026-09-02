import Klean77Iscube.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean77Iscube.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    : Prop :=
    (∀ (N : SortInt) (I : SortInt) (D : SortInt) (h : _andBool_ (_andBool_ (_andBool_ (_andBool_ (_andBool_ («_<=Int_» 0 I) («_<=Int_» I («_+Int_» N 1))) («_<=Int_» 0 N)) («_<Int_» 0 D)) («_<Int_» D («_-Int_» («_*Int_» («_*Int_» («_+Int_» N 1) («_+Int_» N 1)) («_+Int_» N 1)) («_*Int_» («_*Int_» N N) N)))) («_<Int_» («_*Int_» («_*Int_» I I) I) («_+Int_» («_*Int_» («_*Int_» N N) N) D)) = true), «_<Int_» I («_+Int_» N 1) = true)
    ∧ (∀ (N : SortInt) (I : SortInt) (D : SortInt) (h : _andBool_ (_andBool_ (_andBool_ (_andBool_ (_andBool_ («_<=Int_» 0 I) («_<=Int_» I («_+Int_» N 1))) («_<=Int_» 0 N)) («_<Int_» 0 D)) («_<Int_» D («_-Int_» («_*Int_» («_*Int_» («_+Int_» N 1) («_+Int_» N 1)) («_+Int_» N 1)) («_*Int_» («_*Int_» N N) N)))) («_>=Int_» («_*Int_» («_*Int_» I I) I) («_+Int_» («_*Int_» («_*Int_» N N) N) D)) = true), «_==Int_» I («_+Int_» N 1) = true)

end Klean77Iscube.Lemmas
