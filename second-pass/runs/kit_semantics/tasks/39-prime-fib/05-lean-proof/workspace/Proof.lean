import Klean39PrimeFib.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (x y : SortBool) : SortBool :=
  x && y
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2, rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (x y : SortInt) : SortBool :=
  decide (x ≥ y)
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (x y : SortInt) : SortBool :=
  decide (x < y)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt :=
  x + y
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (x : SortBool) : SortBool :=
  !x

/- Operational implementation of the frozen `primeScan` recurrence.  On its
   guarded domain the fuel cannot expire: for nonnegative `a`, `a.toNat + 1`
   transitions pass the square-root bound, while negative `a` stops at once. -/
private def frozenPythonModulo (x y : SortInt) : SortInt :=
  Int.tmod (Int.tmod x y + y) y

private def runPrimeDivisorScan (a d : SortInt) : Nat → SortBool
  | 0 => true
  | fuel + 1 =>
      if d * d > a then
        true
      else if frozenPythonModulo a d = 0 then
        false
      else
        runPrimeDivisorScan a (d + 1) fuel

/- The frozen summary is guarded by `d >= 2`; `false` is the single fixed
   totalization below that domain. -/
private def computePrimeScan
    (a d : SortInt) (isPrime : SortBool) : SortBool :=
  if d < 2 then
    false
  else if isPrime then
    runPrimeDivisorScan a d (a.toNat + 1)
  else
    false

private def candidatePrimeIncrement (b : SortInt) : SortInt :=
  Klean39PrimeFib.Lemmas.kite
    (computePrimeScan b 2 («_>=Int_» b 2))
    1
    0

private structure FibonacciSearchState where
  count : SortInt
  a : SortInt
  b : SortInt

private def stepFibonacciSearch
    (state : FibonacciSearchState) : FibonacciSearchState where
  count := state.count + candidatePrimeIncrement state.b
  a := state.b
  b := state.a + state.b

private def iterateFibonacciSearch :
    Nat → FibonacciSearchState → FibonacciSearchState
  | 0, state => state
  | steps + 1, state =>
      iterateFibonacciSearch steps (stepFibonacciSearch state)

private def firstReachedFibonacciValue
    (target : SortInt) (initial : FibonacciSearchState) : Nat → SortInt
  | 0 => initial.a
  | fuel + 1 =>
      if target ≤ initial.count then
        initial.a
      else
        firstReachedFibonacciValue target (stepFibonacciSearch initial) fuel

/- On terminating executions this scans to the first state meeting `target`.
   The constant zero is the one fixed totalization when no such state exists,
   so all divergent states in a frozen successor chain receive the same value. -/
private noncomputable def completeFibonacciSearch
    (target : SortInt) (initial : FibonacciSearchState) : SortInt := by
  classical
  exact
    if reaches : ∃ steps : Nat,
        target ≤ (iterateFibonacciSearch steps initial).count then
      firstReachedFibonacciValue target initial (Classical.choose reaches)
    else
      0
/- KORE symbol: LblprimeFibSearch'LParUndsCommUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»
    (target count a b : SortInt) : SortInt :=
  if target ≤ count then
    a
  else if target < 1 then
    0
  else if b < 1 then
    0
  else
    let next := stepFibonacciSearch { count := count, a := a, b := b }
    if target ≤ next.count then
      next.a
    else if a < 0 then
      0
    else
      completeFibonacciSearch target next
/- KORE symbol: LblprimeScan'LParUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Int'Unds'Int'Unds'Bool; frozen source obligations: rule-577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2, rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»
    (a d : SortInt) (isPrime : SortBool) : SortBool :=
  computePrimeScan a d isPrime

theorem final :
    Klean39PrimeFib.Lemmas.targetStatement _andBool_ «_>=Int_» «_<Int_» «_+Int_» notBool_ «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int» «primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool» := by
  constructor
  · intro d _a h
    simp only [«_>=Int_», decide_eq_true_eq] at h
    simp [«primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»,
      computePrimeScan, Int.not_lt.mpr h]
  · intro b a count target h
    simp only [_andBool_, «_>=Int_», «_<Int_», «_+Int_», notBool_,
      Bool.and_eq_true, decide_eq_true_eq] at h
    rcases h with
      ⟨⟨⟨targetPositive, countLtTarget⟩, nextNotLtTarget⟩, bPositive⟩
    have nextDecisionFalse :
        decide
            (count +
                Klean39PrimeFib.Lemmas.kite
                  («primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»
                    b 2 («_>=Int_» b 2))
                  1
                  0 <
              target) =
          false :=
      Eq.mp (Bool.not_eq_true' _) nextNotLtTarget
    have nextNotLt :
        ¬count +
              Klean39PrimeFib.Lemmas.kite
                («primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»
                  b 2 («_>=Int_» b 2))
                1
                0 <
            target :=
      decide_eq_false_iff_not.mp nextDecisionFalse
    have targetLeNext :
        target ≤
          count +
            Klean39PrimeFib.Lemmas.kite
              («primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»
                b 2 («_>=Int_» b 2))
              1
              0 :=
      Int.not_lt.mp nextNotLt
    have targetLeComputedNext :
        target ≤
          count +
            Klean39PrimeFib.Lemmas.kite
              (computePrimeScan b 2 («_>=Int_» b 2))
              1
              0 := by
      simpa [«primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»] using
        targetLeNext
    simp [
      «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»,
      stepFibonacciSearch, candidatePrimeIncrement,
      Int.not_le.mpr countLtTarget, Int.not_lt.mpr targetPositive,
      Int.not_lt.mpr bPositive, targetLeComputedNext]

end Proof
