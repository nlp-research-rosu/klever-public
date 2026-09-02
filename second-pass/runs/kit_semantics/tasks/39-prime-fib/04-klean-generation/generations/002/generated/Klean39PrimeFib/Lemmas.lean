import Klean39PrimeFib.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean39PrimeFib.Lemmas

def kite {α : Type} (c : SortBool) (t e : α) : α := cond c t e

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    (notBool_ : SortBool → SortBool)
    («primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int» : SortInt → SortInt → SortInt → SortInt → SortInt)
    («primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool» : SortInt → SortInt → SortBool → SortBool)
    : Prop :=
    (∀ (D : SortInt) (_A : SortInt) (h : («_>=Int_» D 2) = true), («primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool» _A D false : SortBool) = (false : SortBool))
    ∧ (∀ (B : SortInt) (_A : SortInt) (C : SortInt) (N : SortInt) (h : (_andBool_ (_andBool_ (_andBool_ («_>=Int_» N 1) («_<Int_» C N)) (notBool_ («_<Int_» («_+Int_» C (kite («primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool» B 2 («_>=Int_» B 2)) 1 0)) N))) («_>=Int_» B 1)) = true), («primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int» N C _A B : SortInt) = (B : SortInt))

end Klean39PrimeFib.Lemmas
