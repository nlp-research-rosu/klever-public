import Klean39PrimeFib.Lemmas

namespace Probe

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

/- Operational implementation of the frozen `primeScan` recurrence.  The
   public binding below starts the divisor at least at two.  For nonnegative
   `a`, `a.toNat + 1` transitions suffice to pass the square-root bound; for
   negative `a`, the first transition stops. -/
private def runPrimeDivisorScan (a d : SortInt) : Nat → SortBool
  | 0 => true
  | fuel + 1 =>
      if d * d > a then
        true
      else if a % d = 0 then
        false
      else
        runPrimeDivisorScan a (d + 1) fuel

private def computePrimeScan
    (a d : SortInt) (isPrime : SortBool) : SortBool :=
  if isPrime then
    let start := if d < 2 then 2 else d
    runPrimeDivisorScan a start (a.toNat + 1)
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

/- The K search can be partial.  This totalization agrees with every
   terminating K execution: a chosen reachable bound is scanned from the
   initial state, returning the first state whose count reaches the target.
   When no such state exists, the final branch supplies a total value outside
   the terminating behavior of the frozen function. -/
private noncomputable def completeFibonacciSearch
    (target : SortInt) (initial : FibonacciSearchState) : SortInt := by
  classical
  exact
    if reaches : ∃ steps : Nat,
        target ≤ (iterateFibonacciSearch steps initial).count then
      firstReachedFibonacciValue target initial (Classical.choose reaches)
    else
      initial.a
/- KORE symbol: LblprimeFibSearch'LParUndsCommUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»
    (target count a b : SortInt) : SortInt :=
  if target ≤ count then
    a
  else
    let next := stepFibonacciSearch { count := count, a := a, b := b }
    if target ≤ next.count then
      next.a
    else
      completeFibonacciSearch target next
/- KORE symbol: LblprimeScan'LParUndsCommUndsCommUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Int'Unds'Int'Unds'Bool; frozen source obligations: rule-577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2, rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool»
    (a d : SortInt) (isPrime : SortBool) : SortBool :=
  computePrimeScan a d isPrime

private theorem increment_of_multiple_four
    (k : SortInt) (hk : 1 ≤ k) : candidatePrimeIncrement (4 * k) = 0 := by
  change (1 : Int) ≤ k at hk
  have h2 : (2 : Int) ≤ 4 * k := by omega
  have h4 : ¬(4 * k : Int) < 4 := by omega
  have hmod : (4 * k : Int) % 2 = 0 := by omega
  simp [candidatePrimeIncrement, computePrimeScan, runPrimeDivisorScan,
    «_>=Int_», Klean39PrimeFib.Lemmas.kite, h2, h4, hmod]

private def multipleFourState (state : FibonacciSearchState) : Prop :=
  state.count = 0 ∧
    ∃ ka : Int, 1 ≤ ka ∧ state.a = 4 * ka ∧
    ∃ kb : Int, 1 ≤ kb ∧ state.b = 4 * kb

private theorem step_preserves_multiple_four
    (state : FibonacciSearchState) (h : multipleFourState state) :
    multipleFourState (stepFibonacciSearch state) := by
  rcases h with ⟨hcount, ka, hka, ha, kb, hkb, hb⟩
  refine ⟨?_, kb, hkb, ?_, ka + kb, by omega, ?_⟩
  · simp [stepFibonacciSearch, hcount, hb, increment_of_multiple_four kb hkb]
  · simp [stepFibonacciSearch, hb]
  · simp [stepFibonacciSearch, ha, hb]
    rw [Int.mul_add]

private theorem iterate_preserves_multiple_four
    (steps : Nat) (state : FibonacciSearchState)
    (h : multipleFourState state) :
    multipleFourState (iterateFibonacciSearch steps state) := by
  induction steps generalizing state with
  | zero => simpa [iterateFibonacciSearch]
  | succ steps ih =>
      simp only [iterateFibonacciSearch]
      exact ih (stepFibonacciSearch state)
        (step_preserves_multiple_four state h)

private theorem multiple_four_never_reaches_one
    (state : FibonacciSearchState) (h : multipleFourState state) :
    ¬∃ steps : Nat, (1 : Int) ≤ (iterateFibonacciSearch steps state).count := by
  intro reaches
  rcases reaches with ⟨steps, reaches⟩
  have invariant := iterate_preserves_multiple_four steps state h
  have count_zero := invariant.1
  change (iterateFibonacciSearch steps state).count = (0 : Int) at count_zero
  change (1 : Int) ≤ (iterateFibonacciSearch steps state).count at reaches
  rw [count_zero] at reaches
  have impossible : ¬((1 : Int) ≤ 0) := by decide
  exact impossible reaches

private theorem state_4_8 :
    multipleFourState { count := 0, a := 4, b := 8 } := by
  exact ⟨rfl, 1, by omega, rfl, 2, by omega, rfl⟩

private theorem state_8_12 :
    multipleFourState { count := 0, a := 8, b := 12 } := by
  exact ⟨rfl, 2, by omega, rfl, 3, by omega, rfl⟩

theorem search_1_0_4_4 :
    «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»
      1 0 4 4 = 4 := by
  have inc4 : candidatePrimeIncrement 4 = 0 := by
    simpa using increment_of_multiple_four 1 (by decide)
  have complete4 :
      completeFibonacciSearch 1 { count := 0, a := 4, b := 8 } = 4 := by
    simp [completeFibonacciSearch,
      multiple_four_never_reaches_one _ state_4_8]
  simp [«primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»,
    stepFibonacciSearch, inc4, complete4]

theorem search_1_0_4_8 :
    «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»
      1 0 4 8 = 8 := by
  have inc8 : candidatePrimeIncrement 8 = 0 := by
    simpa using increment_of_multiple_four 2 (by decide)
  have complete8 :
      completeFibonacciSearch 1 { count := 0, a := 8, b := 12 } = 8 := by
    simp [completeFibonacciSearch,
      multiple_four_never_reaches_one _ state_8_12]
  simp [«primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»,
    stepFibonacciSearch, inc8, complete8]

theorem divergent_recurrence_counterexample :
    «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»
      1 0 4 8 ≠
    «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int»
      1 0 4 4 := by
  rw [search_1_0_4_8, search_1_0_4_4]
  decide

theorem final :
    Klean39PrimeFib.Lemmas.targetStatement _andBool_ «_>=Int_» «_<Int_» «_+Int_» notBool_ «primeFibSearch(_,_,_,_)_VERIFICATION-SYNTAX_Int_Int_Int_Int_Int» «primeScan(_,_,_)_VERIFICATION-SYNTAX_Bool_Int_Int_Bool» := by
  constructor
  · intro _d _a _h
    rfl
  · intro b a count target h
    simp only [_andBool_, «_>=Int_», «_<Int_», «_+Int_», notBool_,
      Bool.and_eq_true, decide_eq_true_eq] at h
    rcases h with
      ⟨⟨⟨_targetPositive, countLtTarget⟩, nextNotLtTarget⟩, _bPositive⟩
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
      Int.not_le.mpr countLtTarget, targetLeComputedNext]

end Probe

#print Probe.divergent_recurrence_counterexample
#print axioms Probe.divergent_recurrence_counterexample
