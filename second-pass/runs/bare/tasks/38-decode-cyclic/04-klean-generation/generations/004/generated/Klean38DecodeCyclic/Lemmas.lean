import Klean38DecodeCyclic.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean38DecodeCyclic.Lemmas

def targetStatement
    («_<=Int_» : SortInt → SortInt → SortBool)
    («Map:update» : SortMap → SortKItem → SortKItem → SortMap)
    («lengthString(_)_STRING-COMMON_Int_String» : SortString → SortInt)
    («substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» : SortString → SortInt → SortInt → SortString)
    : Prop :=
    (∀ (V' : SortKItem) (K : SortKItem) (M : SortMap) (V : SortKItem), ((«Map:update» M K V : SortMap) = («Map:update» M K V' : SortMap)) ↔ ((V : SortKItem) = (V' : SortKItem)))
    ∧ (∀ (_S : SortString), («_<=Int_» 0 («lengthString(_)_STRING-COMMON_Int_String» _S) : SortBool) = (true : SortBool))
    ∧ (∀ (S : SortString), («substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» S 0 («lengthString(_)_STRING-COMMON_Int_String» S) : SortString) = (S : SortString))

end Klean38DecodeCyclic.Lemmas
