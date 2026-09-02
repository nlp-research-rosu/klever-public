import Klean9RollingMax.Lemmas

namespace Proof

/- KORE symbol: LblisInt; frozen source obligations: rule-8722c58a66500d998b33e9332efe3c98d027270e2a8119c0d9554459c8d55f9c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false

theorem final :
    Klean9RollingMax.Lemmas.targetStatement isInt := by
  intro V
  cases V <;> simp [isInt, inj]

end Proof
