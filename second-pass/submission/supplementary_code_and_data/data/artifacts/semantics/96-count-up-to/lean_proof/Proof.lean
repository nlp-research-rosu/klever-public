import Proof.Outer

namespace Proof

theorem final :
    Klean96CountUpTo.Lemmas.targetStatement
      _Map_ _andBool_ «_<=Int_» «_|->_» noDivisor primesAcc := by
  unfold Klean96CountUpTo.Lemmas.targetStatement
  constructor
  · intros _Gen6 _Gen5 _Gen4 _Gen3 _Gen2 _Gen1 VS _Gen0 N B D C
      BI MOD rest h
    have bounds : 2 ≤ D ∧ D ≤ C := by
      simpa [_andBool_, «_<=Int_», Bool.and_eq_true] using h
    simpa [machine, heapList, innerLoop, innerCondition, innerBody,
      allScopes, ambientScopes] using
      (innerProof C D B N BI MOD VS _Gen0 _Gen1 _Gen2 _Gen3 _Gen4
        _Gen5 _Gen6 rest bounds.1 bounds.2)
  · intros _Gen6 _Gen5 _Gen4 _Gen3 _Gen2 _Gen1 VS _Gen0 I N
      BI MOD rest h
    have bounds : 2 ≤ I ∧ I ≤ N := by
      simpa [_andBool_, «_<=Int_», Bool.and_eq_true] using h
    simpa [machine, heapList, outerLoop, outerCondition, outerBody,
      innerWhileStatement, outerTail, allScopes, ambientScopes] using
      (outerProof I N BI MOD VS _Gen0 _Gen1 _Gen2 _Gen3 _Gen4
        _Gen5 _Gen6 rest bounds.1 bounds.2)

end Proof
