import Klean105ByLength.Lemmas

namespace CounterfactualAudit

def constantFalseEq (_left _right : SortInt) : SortBool :=
  false

def constantFalseApplyCmp
    (_operator : SortString) (_left _right : SortVal) : SortBool :=
  false

def honestIsInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false

def honestProjectInt : SortK → SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => value
  | _ => 0

theorem constantFalsePairStillProvesTarget :
    Klean105ByLength.Lemmas.targetStatement
      constantFalseEq
      constantFalseApplyCmp
      honestIsInt
      honestProjectInt := by
  intro I V h
  rfl

end CounterfactualAudit
