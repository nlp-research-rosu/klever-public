import Klean94Skjkasdkd.Lemmas
import Proof.Operational
import Std.Tactic

namespace Proof

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (x y : SortInt) : SortInt := x - y
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (x y : SortBool) : SortBool := x && y
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (x y : SortInt) : SortBool := decide (x > y)
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (x y : SortInt) : SortBool := decide (x ≥ y)
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914, rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (x y : SortInt) : SortBool := decide (x < y)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x y : SortInt) : SortBool := decide (x ≤ y)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (x y : SortInt) : SortBool := x == y
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» (x y : SortInt) : SortBool := !(x == y)
/- KORE symbol: Lbl'UndsPerc'Int'Unds'; frozen source obligations: rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_%Int_» (x y : SortInt) : SortInt := Int.tmod x y
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: Lbl'UndsSlsh'Int'Unds'; frozen source obligations: rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_/Int_» (x y : SortInt) : SortInt := Int.tdiv x y
/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    (op : SortString) (left right : SortVal) : SortVal :=
  Operational.applyBinaryModel op left right
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (op : SortString) (left right : SortVal) : SortBool :=
  Operational.applyComparisonModel op left right

def projectValueIntOption : SortVal → Option SortInt
  | .inj_SortInt value => some value
  | _ => none

def projectKIntOption : SortK → Option SortInt
  | .kseq (.inj_SortInt value) .dotk => some value
  | .kseq (.inj_SortVal value) .dotk => projectValueIntOption value
  | _ => none

def totalProjectedInteger (value : SortVal) : SortInt :=
  (projectValueIntOption value).getD 0
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» (value : SortVal) : SortBool :=
  (projectValueIntOption value).isSome

def digitSumNatural : Nat → Int
  | 0 => 0
  | n + 1 =>
      Int.ofNat ((n + 1) % 10) + digitSumNatural ((n + 1) / 10)
termination_by n => n
decreasing_by omega

def digitSumModel (n : Int) : Int :=
  if n > 0 then digitSumNatural n.toNat else 0

theorem digitSumNatural_step (n : Nat) (h : 0 < n) :
    Int.ofNat (n % 10) + digitSumNatural (n / 10) = digitSumNatural n := by
  cases n with
  | zero => omega
  | succ k => rw [digitSumNatural]

theorem digitSumModel_ofNat (n : Nat) :
    digitSumModel (Int.ofNat n) = digitSumNatural n := by
  cases n with
  | zero => simp [digitSumModel, digitSumNatural]
  | succ k => simp [digitSumModel]

theorem pythonModuloPositiveTen (n : Int) (h : n > 0) :
    Operational.pythonModulo n 10 = Int.ofNat (n.toNat % 10) := by
  have hn : 0 ≤ n := by omega
  have hr : 0 ≤ n % 10 := Int.emod_nonneg n (by omega)
  have hrs : 0 ≤ n % 10 + 10 := by omega
  simp [Operational.pythonModulo, Int.tmod_eq_emod, hn, hrs, Int.max_eq_left hn]

theorem decimalQuotient (n : Int) (h : n > 0) :
    Int.tdiv (n - Operational.pythonModulo n 10) 10 =
      Int.ofNat (n.toNat / 10) := by
  rw [pythonModuloPositiveTen n h]
  have hn : 0 ≤ n := by omega
  have hr : 0 ≤ n % 10 := Int.emod_nonneg n (by omega)
  have hrlt : n % 10 < 10 := by
    have bound := Int.emod_lt n (show (10 : Int) ≠ 0 by omega)
    omega
  have hcast : Int.ofNat (n.toNat % 10) = n % 10 := by
    simp [Int.natCast_emod, Int.toNat_of_nonneg hn]
  rw [hcast, Int.tdiv_eq_ediv]
  simp only [show 0 ≤ n - n % 10 by omega, true_or, ↓reduceIte, Int.add_zero]
  have hnatdiv : Int.ofNat (n.toNat / 10) = n / 10 := by
    simpa only [Int.toNat_of_nonneg hn] using (Int.natCast_ediv n.toNat 10)
  rw [hnatdiv]
  omega

theorem digitSumModel_step (n : Int) (h : n > 0) :
    Operational.pythonModulo n 10 +
        digitSumModel (Int.tdiv (n - Operational.pythonModulo n 10) 10) =
      digitSumModel n := by
  rw [decimalQuotient n h, pythonModuloPositiveTen n h]
  have hNat : 0 < n.toNat := by omega
  rw [digitSumModel_ofNat, digitSumModel, if_pos h]
  exact digitSumNatural_step n.toNat hNat
/- KORE symbol: LbldigitSum'LParUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int; frozen source obligations: rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «digitSum(_)_VERIFICATION_Int_Int» (n : SortInt) : SortInt :=
  digitSumModel n
/- KORE symbol: LblisInt; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914, rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | .kseq (.inj_SortInt _) .dotk => true
  | .kseq (.inj_SortVal (.inj_SortInt _)) .dotk => true
  | _ => false

def primeTailModel (n d : Int) : Bool :=
  if d < 2 then false
  else if d >= n then true
  else if Operational.pythonModulo n d == 0 then false
  else primeTailModel n (d + 1)
termination_by (n - d).toNat
decreasing_by
  simp_wf
  omega

theorem primeTailModel_previous (n d : Int)
    (hd : d > 2) (hn : d ≤ n)
    (hr : Operational.pythonModulo n (d - 1) ≠ 0) :
    primeTailModel n d = primeTailModel n (d - 1) := by
  symm
  rw [primeTailModel]
  simp [show ¬d - 1 < 2 by omega, show ¬d - 1 ≥ n by omega, hr]
/- KORE symbol: LblprimeTail'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Int'Unds'Int; frozen source obligations: rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «primeTail(_,_)_VERIFICATION_Bool_Int_Int»
    (n d : SortInt) : SortBool :=
  primeTailModel n d
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» (term : SortK) : SortInt :=
  (projectKIntOption term).getD 0
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d, rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081, rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914, rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal (value : SortVal) : SortInt :=
  totalProjectedInteger value
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x y : SortInt) : SortInt :=
  Operational.pythonModulo x y
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» (term : SortK) : Option SortInt :=
  projectKIntOption term

theorem final :
    Klean94Skjkasdkd.Lemmas.targetStatement «_-Int_» _andBool_ «_>Int_» «_>=Int_» «_<Int_» «_<=Int_» «_==Int_» «_=/=Int_» «_%Int_» «_+Int_» «_/Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» «digitSum(_)_VERIFICATION_Int_Int» isInt «primeTail(_,_)_VERIFICATION_Bool_Int_Int» «project:Int» projectIntTotal «pyMod(_,_)_MPY-INT_Int_Int_Int» «project:Int?» := by
  unfold Klean94Skjkasdkd.Lemmas.targetStatement
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro value
    cases value <;>
      simp [inj, «project:Int?», projectKIntOption, projectValueIntOption,
        «definedProjectInt(_)_VERIFICATION_Bool_Val»]
  · intro value h
    cases value <;>
      simp [«definedProjectInt(_)_VERIFICATION_Bool_Val»,
        projectValueIntOption] at h
    simp [inj, «project:Int», projectKIntOption, projectIntTotal,
      totalProjectedInteger, projectValueIntOption]
  · intro value
    simp [projectIntTotal, totalProjectedInteger, projectValueIntOption]
  · intro integer value h
    cases value <;> simp [inj, isInt] at h
    simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      Operational.applyComparisonModel, Operational.integerCompare,
      projectIntTotal, totalProjectedInteger, projectValueIntOption, «_>Int_»]
  · intro integer value h
    cases value <;> simp [inj, isInt] at h
    simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      Operational.applyComparisonModel, Operational.integerCompare,
      projectIntTotal, totalProjectedInteger, projectValueIntOption, «_>=Int_»]
  · intro value integer h
    cases value <;> simp [inj, isInt] at h
    simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      Operational.applyComparisonModel, Operational.integerCompare,
      projectIntTotal, totalProjectedInteger, projectValueIntOption, «_<Int_»]
  · intro integer value h
    cases value <;> simp [inj, isInt] at h
    simp [«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
      Operational.applyBinaryModel, Operational.integerBinary,
      Operational.intValue,
      projectIntTotal, totalProjectedInteger, projectValueIntOption,
      «pyMod(_,_)_MPY-INT_Int_Int_Int»]
  · intro integer value h
    cases value <;> simp [inj, isInt] at h
    simp [«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
      Operational.applyBinaryModel, Operational.integerBinary,
      Operational.intValue,
      projectIntTotal, totalProjectedInteger, projectValueIntOption, «_+Int_»]
  · intro divisor number h
    simp only [_andBool_, «_>=Int_», «_<Int_», «_==Int_»,
      «pyMod(_,_)_MPY-INT_Int_Int_Int», Bool.and_eq_true,
      decide_eq_true_eq, beq_iff_eq] at h
    simp [«primeTail(_,_)_VERIFICATION_Bool_Int_Int», primeTailModel,
      h.1.1, h.1.2, h.2]
  · intro divisor number h
    simp only [_andBool_, «_>Int_», «_<=Int_», «_=/=Int_»,
      «pyMod(_,_)_MPY-INT_Int_Int_Int», «_-Int_», Bool.and_eq_true,
      decide_eq_true_eq] at h
    have hrem : Operational.pythonModulo number (divisor - 1) ≠ 0 := by
      simpa using h.2
    exact primeTailModel_previous number divisor h.1.1 h.1.2 hrem
  · intro number h
    simp only [«_>Int_», decide_eq_true_eq] at h
    simpa [«_+Int_», «pyMod(_,_)_MPY-INT_Int_Int_Int»,
      «digitSum(_)_VERIFICATION_Int_Int», «_/Int_», «_-Int_»] using
      digitSumModel_step number h
  · intro number h
    simp only [«_>Int_», decide_eq_true_eq] at h
    simpa [«_+Int_», «_%Int_», «digitSum(_)_VERIFICATION_Int_Int»,
      «_/Int_», «_-Int_», Operational.pythonModulo] using
      digitSumModel_step number h
  · intro number total h
    simp only [«_>Int_», decide_eq_true_eq] at h
    have step := digitSumModel_step number h
    simp only [«_+Int_», «_%Int_», «digitSum(_)_VERIFICATION_Int_Int»,
      «_/Int_», «_-Int_»]
    rw [← step]
    exact Int.add_assoc total _ _

end Proof
