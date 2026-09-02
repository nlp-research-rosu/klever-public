import Klean103RoundedAvg.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52, rule-555ac2e26b8914f371e3c4e9148f353eb28acaaa57ec7204eaaac93ef182837f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (x y : SortBool) : SortBool := x && y
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52, rule-555ac2e26b8914f371e3c4e9148f353eb28acaaa57ec7204eaaac93ef182837f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (x y : SortInt) : SortBool := decide (x > y)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (x y : SortInt) : SortInt := x * y
/- KORE symbol: LblallBits'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'IntSeq; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52, rule-555ac2e26b8914f371e3c4e9148f353eb28acaaa57ec7204eaaac93ef182837f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» : SortIntSeq → SortBool
  | .«.IntSeq_MPY-CORE_IntSeq» => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c rest =>
      ((c == 48) || (c == 49)) &&
        «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» rest
/- KORE symbol: LblbitWeight'LParUndsRParUnds'VERIFICATION-BASE'Unds'Int'Unds'IntSeq; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» : SortIntSeq → SortInt
  | .«.IntSeq_MPY-CORE_IntSeq» => 1
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      2 * «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» rest
/- KORE symbol: LblbitValue'LParUndsRParUnds'VERIFICATION-BASE'Unds'Int'Unds'IntSeq; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» : SortIntSeq → SortInt
  | .«.IntSeq_MPY-CORE_IntSeq» => 0
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c rest =>
      (c - 48) * «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» rest +
        «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» rest

private def loopDigitsNat (v : Nat) (acc : SortIntSeq) : SortIntSeq :=
  if _h : v ≤ 1 then
    acc
  else
    loopDigitsNat (v / 2)
      (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        ((48 : Int) + Int.ofNat (v % 2)) acc)
termination_by v
decreasing_by omega

/- KORE symbol: LblloopDigits; frozen source obligations: rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804, rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52, rule-555ac2e26b8914f371e3c4e9148f353eb28acaaa57ec7204eaaac93ef182837f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def loopDigits (v : SortInt) (acc : SortIntSeq) : SortIntSeq :=
  loopDigitsNat v.toNat acc

private theorem loopDigitsNat_value
    (v : Nat) (hv : 0 < v) (acc : SortIntSeq) :
    «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» (loopDigitsNat v acc) +
        «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» (loopDigitsNat v acc) =
      (v : Int) * «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» acc +
        «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» acc := by
  rw [loopDigitsNat]
  split
  next hbase =>
    have hv_one : v = 1 := by omega
    subst v
    simp
  next hstep =>
    let nextAcc : SortIntSeq :=
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        ((48 : Int) + Int.ofNat (v % 2)) acc
    have hhalf_pos : 0 < v / 2 := by omega
    have hrec := loopDigitsNat_value (v / 2) hhalf_pos nextAcc
    change
      «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq»
            (loopDigitsNat (v / 2) nextAcc) +
          «bitValue(_)_VERIFICATION-BASE_Int_IntSeq»
            (loopDigitsNat (v / 2) nextAcc) =
        (v : Int) * «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» acc +
          «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» acc
    rw [hrec]
    dsimp [nextAcc]
    simp only
      [«bitWeight(_)_VERIFICATION-BASE_Int_IntSeq»,
       «bitValue(_)_VERIFICATION-BASE_Int_IntSeq»]
    have hdiv :
        ((v / 2 : Nat) : Int) * 2 + ((v % 2 : Nat) : Int) = (v : Int) := by
      omega
    have hcast_div :
        (v : Int) / 2 = ((v / 2 : Nat) : Int) := by
      omega
    have hcast_mod :
        (v : Int) % 2 = ((v % 2 : Nat) : Int) := by
      omega
    rw [hcast_div, hcast_mod]
    have hoffset :
        (48 : Int) + ((v % 2 : Nat) : Int) - 48 =
          ((v % 2 : Nat) : Int) := by
      omega
    rw [hoffset]
    calc
      ((v / 2 : Nat) : Int) *
            (2 * «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» acc) +
          (((v % 2 : Nat) : Int) *
              «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» acc +
            «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» acc) =
        (((v / 2 : Nat) : Int) * 2 + ((v % 2 : Nat) : Int)) *
            «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» acc +
          «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» acc := by
            rw [Int.add_mul, Int.mul_assoc, Int.add_assoc]
      _ = (v : Int) * «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» acc +
            «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» acc := by
              rw [hdiv]
termination_by v
decreasing_by omega

private theorem loopDigitsNat_allBits
    (v : Nat) (acc : SortIntSeq)
    (hacc : «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» acc = true) :
    «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» (loopDigitsNat v acc) = true := by
  rw [loopDigitsNat]
  split
  next _ =>
    exact hacc
  next hstep =>
    let nextAcc : SortIntSeq :=
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        ((48 : Int) + Int.ofNat (v % 2)) acc
    have hmod : v % 2 = 0 ∨ v % 2 = 1 := by omega
    have hnext :
        «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» nextAcc = true := by
      rcases hmod with hzero | hone
      · simp [nextAcc, hzero, hacc,
          «allBits(_)_VERIFICATION-BASE_Bool_IntSeq»]
      · simp [nextAcc, hone, hacc,
          «allBits(_)_VERIFICATION-BASE_Bool_IntSeq»]
    exact loopDigitsNat_allBits (v / 2) nextAcc hnext
termination_by v
decreasing_by omega

theorem final :
    Klean103RoundedAvg.Lemmas.targetStatement _andBool_ «_>Int_» «_+Int_» «_*Int_» «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» «bitValue(_)_VERIFICATION-BASE_Int_IntSeq» «bitWeight(_)_VERIFICATION-BASE_Int_IntSeq» loopDigits := by
  unfold Klean103RoundedAvg.Lemmas.targetStatement
  constructor
  · intro acc v h
    have hguard :
        «_>Int_» v 0 = true ∧
          «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» acc = true := by
      simpa [_andBool_] using h
    have hv : 0 < v := by
      simpa [«_>Int_»] using hguard.1
    have hv_nat : 0 < v.toNat := Int.pos_iff_toNat_pos.mp hv
    have hv_cast : (v.toNat : Int) = v :=
      Int.toNat_of_nonneg (Int.le_of_lt hv)
    have hvalue := loopDigitsNat_value v.toNat hv_nat acc
    simpa [«_+Int_», «_*Int_», loopDigits, hv_cast] using hvalue
  constructor
  · intro acc v h
    have hguard :
        «_>Int_» v 0 = true ∧
          «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» acc = true := by
      simpa [_andBool_] using h
    have hv : 0 < v := by
      simpa [«_>Int_»] using hguard.1
    have hv_nat : 0 < v.toNat := Int.pos_iff_toNat_pos.mp hv
    have hv_cast : (v.toNat : Int) = v :=
      Int.toNat_of_nonneg (Int.le_of_lt hv)
    have hvalue := loopDigitsNat_value v.toNat hv_nat acc
    simpa [«_+Int_», «_*Int_», loopDigits, hv_cast] using hvalue
  · intro acc v h
    have hguard :
        «_>Int_» v 0 = true ∧
          «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» acc = true := by
      simpa [_andBool_] using h
    have hacc :
        «allBits(_)_VERIFICATION-BASE_Bool_IntSeq» acc = true :=
      hguard.2
    exact loopDigitsNat_allBits v.toNat acc hacc

end Proof
