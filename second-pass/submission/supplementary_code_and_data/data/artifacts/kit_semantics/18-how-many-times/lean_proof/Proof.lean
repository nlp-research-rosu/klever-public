import Klean18HowManyTimes.Lemmas
import Std.Tactic

namespace Proof

def intSeqToList : SortIntSeq → List SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs =>
      x :: intSeqToList xs

def listToIntSeq : List SortInt → SortIntSeq
  | [] => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | x :: xs =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x (listToIntSeq xs)

theorem listToIntSeq_intSeqToList (xs : SortIntSeq) :
    listToIntSeq (intSeqToList xs) = xs := by
  induction xs with
  | «.IntSeq_MPY-CORE_IntSeq» => rfl
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs ih =>
      simp [intSeqToList, listToIntSeq, ih]

def intSeqAtNat? : SortIntSeq → Nat → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => none
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x _, 0 => some x
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ xs, n + 1 =>
      intSeqAtNat? xs n

def intSeqAt? (xs : SortIntSeq) (i : SortInt) : Option SortInt :=
  if i < 0 then none else intSeqAtNat? xs i.toNat

/- This is the two guarded buildIS K equations, with source length as a
   termination bound. An invalid lookup is the total fallback outside the
   K rules' defined indexing domain. -/
def buildISFuel
    (xs : SortIntSeq) (i stop step : SortInt) : Nat → SortIntSeq
  | 0 => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | fuel + 1 =>
      if ((0 < step ∧ i < stop) ∨ (step < 0 ∧ stop < i)) then
        match intSeqAt? xs i with
        | some x =>
            SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x
              (buildISFuel xs (i + step) stop step fuel)
        | none => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
      else
        SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

noncomputable local instance : DecidableEq SortK :=
  Classical.typeDecidableEq SortK

/- KORE symbol: Lbl'UndsEqlsEqls'K'Unds'; frozen source obligations: rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536. -/
noncomputable def «_==K_» (x y : SortK) : SortBool :=
  if x = y then true else false

/- KORE symbol: LblbuildIS'LParUndsCommUndsCommUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'IntSeq'Unds'IntSeq'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536.
   The unit-stride branch is the extensional drop/take form of the exact K
   recurrence; other strides follow that recurrence through buildISFuel. -/
def «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
    (xs : SortIntSeq) (i stop step : SortInt) : SortIntSeq :=
  if step = 1 then
    if i < 0 then
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    else
      listToIntSeq
        (((intSeqToList xs).drop i.toNat).take (stop - i).toNat)
  else
    buildISFuel xs i stop step (intSeqToList xs).length

/- KORE symbol: LblclampHi'LParUndsCommUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536. -/
def «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int»
    (i len step : SortInt) : SortInt :=
  if i < len then i else if step < 0 then len - 1 else len

/- KORE symbol: LblisLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'IntSeq; frozen source obligations: rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536. -/
def «isLen(_)_MPY-CORE_Int_IntSeq» (xs : SortIntSeq) : SortInt :=
  Int.ofNat (intSeqToList xs).length

/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536. -/
def notBool_ (b : SortBool) : SortBool := !b

/- KORE symbol: LbltailIS'LParUndsRParUnds'VERIFICATION'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536. -/
def «tailIS(_)_VERIFICATION_IntSeq_IntSeq» : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ xs => xs

theorem final :
    Klean18HowManyTimes.Lemmas.targetStatement «_==K_» «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» «isLen(_)_MPY-CORE_Int_IntSeq» notBool_ «tailIS(_)_VERIFICATION_IntSeq_IntSeq» := by
  intro S h
  cases S with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      simp [notBool_, «_==K_»] at h
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs =>
      cases xs with
      | «.IntSeq_MPY-CORE_IntSeq» => rfl
      | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y ys =>
          have hnonneg :
              (0 : Int) ≤ Int.ofNat (intSeqToList ys).length :=
            Int.natCast_nonneg _
          have hpos :
              (1 : Int) <
                «isLen(_)_MPY-CORE_Int_IntSeq»
                  (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x
                    (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y ys)) := by
            simp [«isLen(_)_MPY-CORE_Int_IntSeq», intSeqToList]
            omega
          have hclamp :
              «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» 1
                  («isLen(_)_MPY-CORE_Int_IntSeq»
                    (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x
                      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y ys)))
                  1 = 1 := by
            simp [«clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int», hpos]
          rw [hclamp]
          simp [«buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»,
            «isLen(_)_MPY-CORE_Int_IntSeq», intSeqToList, listToIntSeq,
            listToIntSeq_intSeqToList,
            «tailIS(_)_VERIFICATION_IntSeq_IntSeq»]

end Proof
