import Klean118GetClosestVowel.Lemmas
import Std.Tactic

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7, rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool := left && right
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (left right : SortInt) : SortBool := decide (left ≥ right)
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7, rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (left right : SortInt) : SortBool := decide (left < right)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (left right : SortInt) : SortBool := decide (left ≤ right)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt := left + right

private def intSeqNatLengthOperational : SortIntSeq → Nat
  | .«.IntSeq_MPY-CORE_IntSeq» => 0
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      intSeqNatLengthOperational rest + 1

/- KORE symbol: LblisLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'IntSeq; frozen source obligations: rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7, rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isLen(_)_MPY-CORE_Int_IntSeq» (codes : SortIntSeq) : SortInt :=
  Int.ofNat (intSeqNatLengthOperational codes)

private def intSeqAtOperational : SortIntSeq → SortInt → Option SortInt
  | .«.IntSeq_MPY-CORE_IntSeq», _ => none
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest, index =>
      if index = 0 then some head
      else if index > 0 then intSeqAtOperational rest (index - 1)
      else none

private def vowelCodeOperational (code : SortInt) : SortBool :=
  decide
    (code = 97 ∨ code = 101 ∨ code = 105 ∨ code = 111 ∨ code = 117 ∨
     code = 65 ∨ code = 69 ∨ code = 73 ∨ code = 79 ∨ code = 85)

private def closestScanNatOperational (codes : SortIntSeq) :
    Nat → SortIntSeq → SortBool → Option SortIntSeq
  | 0, result, _ => some result
  | Nat.succ index, result, true =>
      closestScanNatOperational codes index result true
  | Nat.succ index, result, false =>
      match intSeqAtOperational codes (Int.ofNat (Nat.succ index)) with
      | none => none
      | some current =>
          if vowelCodeOperational current then
            match intSeqAtOperational codes (Int.ofNat index) with
            | none => none
            | some left =>
                if vowelCodeOperational left then
                  closestScanNatOperational codes index result false
                else
                  match intSeqAtOperational codes
                    (Int.ofNat (Nat.succ (Nat.succ index))) with
                  | none => none
                  | some right =>
                      if vowelCodeOperational right then
                        closestScanNatOperational codes index result false
                      else
                        closestScanNatOperational codes index
                          (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» current
                            .«.IntSeq_MPY-CORE_IntSeq»)
                          true
          else
            closestScanNatOperational codes index result false

/- KORE symbol: LblclosestScan'LParUndsCommUndsCommUndsCommUndsRParUnds'FOUNDATION-SYNTAX'Unds'IntSeq'Unds'IntSeq'Unds'Int'Unds'IntSeq'Unds'Bool; frozen source obligations: rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»
    (codes : SortIntSeq) (index : SortInt) (result : SortIntSeq)
    (found : SortBool) : Option SortIntSeq :=
  if index ≤ 0 then some result
  else closestScanNatOperational codes index.toNat result found
/- KORE symbol: LblintSeqAt'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Int'Unds'IntSeq'Unds'Int; frozen source obligations: rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?»
    (codes : SortIntSeq) (index : SortInt) : Option SortInt :=
  intSeqAtOperational codes index

private theorem intSeqAtOperational_isSome_of_lt
    (codes : SortIntSeq) (index : Nat)
    (bound : index < intSeqNatLengthOperational codes) :
    (intSeqAtOperational codes (Int.ofNat index)).isSome = true := by
  induction codes generalizing index with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      simp [intSeqNatLengthOperational] at bound
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest ih =>
      cases index with
      | zero => simp [intSeqAtOperational]
      | succ index =>
          have smaller : index < intSeqNatLengthOperational rest := by
            simpa [intSeqNatLengthOperational] using bound
          simpa [intSeqAtOperational] using ih index smaller

private theorem closestScanNatOperational_isSome_of_lt
    (codes : SortIntSeq) (index : Nat) (result : SortIntSeq) (found : SortBool)
    (bound : index + 1 < intSeqNatLengthOperational codes) :
    (closestScanNatOperational codes index result found).isSome = true := by
  induction index generalizing result found with
  | zero => simp [closestScanNatOperational]
  | succ index ih =>
      have recursiveBound : index + 1 < intSeqNatLengthOperational codes := by
        omega
      cases found with
      | true =>
          simpa [closestScanNatOperational] using ih result true recursiveBound
      | false =>
          have currentBound : Nat.succ index < intSeqNatLengthOperational codes := by
            omega
          have leftBound : index < intSeqNatLengthOperational codes := by
            omega
          have rightBound : Nat.succ (Nat.succ index) < intSeqNatLengthOperational codes := by
            omega
          have currentSome := intSeqAtOperational_isSome_of_lt codes (Nat.succ index) currentBound
          have leftSome := intSeqAtOperational_isSome_of_lt codes index leftBound
          have rightSome := intSeqAtOperational_isSome_of_lt codes
            (Nat.succ (Nat.succ index)) rightBound
          generalize currentEq : intSeqAtOperational codes (Int.ofNat (Nat.succ index)) = current at currentSome
          cases current <;> simp at currentSome
          simp only [closestScanNatOperational, currentEq]
          split
          · generalize leftEq : intSeqAtOperational codes (Int.ofNat index) = left at leftSome
            cases left <;> simp at leftSome
            simp only
            split
            · exact ih result false recursiveBound
            · generalize rightEq : intSeqAtOperational codes
                  (Int.ofNat (Nat.succ (Nat.succ index))) = right at rightSome
              cases right <;> simp at rightSome
              simp only
              split
              · exact ih result false recursiveBound
              · exact ih _ true recursiveBound
          · exact ih result false recursiveBound

theorem final :
    Klean118GetClosestVowel.Lemmas.targetStatement _andBool_ «_>=Int_» «_<Int_» «_<=Int_» «_+Int_» «isLen(_)_MPY-CORE_Int_IntSeq» «closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?» «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» := by
  unfold Klean118GetClosestVowel.Lemmas.targetStatement
  constructor
  · intro index codes guard
    have conditions : 0 ≤ index ∧ index < Int.ofNat (intSeqNatLengthOperational codes) := by
      simpa [_andBool_, «_<=Int_», «_<Int_», «isLen(_)_MPY-CORE_Int_IntSeq»]
        using guard
    rcases conditions with ⟨nonnegative, upper⟩
    constructor
    · intro _
      trivial
    · intro _
      cases index with
      | ofNat index =>
          apply intSeqAtOperational_isSome_of_lt
          exact Int.ofNat_lt.mp upper
      | negSucc index =>
          simp at nonnegative
  · intro found result index codes guard
    have conditions : 0 ≤ index ∧ index + 1 < Int.ofNat (intSeqNatLengthOperational codes) := by
      simpa [_andBool_, «_>=Int_», «_<Int_», «_+Int_»,
        «isLen(_)_MPY-CORE_Int_IntSeq»] using guard
    rcases conditions with ⟨nonnegative, upper⟩
    constructor
    · intro _
      trivial
    · intro _
      cases index with
      | ofNat index =>
          cases index with
          | zero =>
              simp [«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»]
          | succ index =>
              simp [«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»]
              apply closestScanNatOperational_isSome_of_lt
              apply Int.ofNat_lt.mp
              simpa only [Int.ofNat_eq_coe, Int.natCast_add, Int.natCast_one] using upper
      | negSucc index =>
          simp at nonnegative

end Proof
