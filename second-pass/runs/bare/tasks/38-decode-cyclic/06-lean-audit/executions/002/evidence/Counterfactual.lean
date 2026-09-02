import Klean38DecodeCyclic.Lemmas

namespace Counterfactual

def alwaysTrueLE (_ _ : SortInt) : SortBool := true

def valueOnlyUpdate (_ : SortMap) (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩

def zeroLength (_ : SortString) : SortInt := 0

def identitySubstring (s : SortString) (_ _ : SortInt) : SortString := s

theorem dishonestStillProvesTarget :
    Klean38DecodeCyclic.Lemmas.targetStatement
      alwaysTrueLE valueOnlyUpdate zeroLength identitySubstring := by
  constructor
  · intro V' K M V
    simp [valueOnlyUpdate]
  constructor <;> simp [alwaysTrueLE, zeroLength, identitySubstring]

end Counterfactual
