import Klean94Skjkasdkd.Lemmas
import Std.Tactic

namespace Proof

/- The following helpers give total Lean realizations of the exact integer
   fragment used by the frozen MPY rules.  `noneV` is used only to totalize
   applyBin outside that fragment, where the mapped K rules do not apply. -/

private def boolAsInt : SortBool → SortInt
  | false => 0
  | true => 1

private def arithmeticInt? : SortVal → Option SortInt
  | SortVal.inj_SortInt i => some i
  | SortVal.inj_SortBool b => some (boolAsInt b)
  | _ => none

private def pyModModel (n d : SortInt) : SortInt :=
  ((n % d) + d) % d

private theorem pyModModel_ten (n : SortInt) :
    pyModModel n 10 = n % 10 := by
  simp [pyModModel]

private theorem decimalQuotient (n : SortInt) :
    Int.tdiv (n - pyModModel n 10) 10 = n / 10 := by
  rw [pyModModel_ten]
  have hsplit := Int.emod_add_ediv n 10
  have hrewrite : n - n % 10 = 10 * (n / 10) := by
    calc
      n - n % 10 = (n % 10 + 10 * (n / 10)) - n % 10 :=
        congrArg (fun z => z - n % 10) hsplit.symm
      _ = 10 * (n / 10) :=
        calc
          (n % 10 + 10 * (n / 10)) - n % 10
              = (10 * (n / 10) + n % 10) - n % 10 :=
            congrArg (fun z => z - n % 10)
              (Int.add_comm (n % 10) (10 * (n / 10)))
          _ = 10 * (n / 10) :=
            Int.add_sub_cancel (10 * (n / 10)) (n % 10)
  rw [hrewrite, Int.mul_tdiv_cancel_left (n / 10)
    (by decide : (10 : Int) ≠ 0)]

private def digitSumModel (n : SortInt) : SortInt :=
  if h : n > 0 then
    pyModModel n 10
      + digitSumModel (Int.tdiv (n - pyModModel n 10) 10)
  else
    0
termination_by n.toNat
decreasing_by
  rw [decimalQuotient]
  have hlt := Int.ediv_lt_self_of_pos_of_ne_one h
    (by decide : (10 : Int) ≠ 1)
  have hnonneg := Int.ediv_nonneg
    (by omega : (0 : Int) ≤ n)
    (by decide : (0 : Int) ≤ 10)
  omega

private theorem digitSumModel_step (n : SortInt) (h : n > 0) :
    digitSumModel n =
      pyModModel n 10
        + digitSumModel (Int.tdiv (n - pyModModel n 10) 10) := by
  rw [digitSumModel, dif_pos h]

private def primeTailModel (n d : SortInt) : SortBool :=
  if h₀ : d < 2 then
    false
  else if h₁ : d >= n then
    true
  else
    decide (pyModModel n d ≠ 0)
      && primeTailModel n (d + 1)
termination_by (n - d).toNat
decreasing_by
  have hdn : d < n := Int.lt_of_not_ge h₁
  apply (Int.toNat_lt_toNat (Int.sub_pos_of_lt hdn)).2
  exact Int.sub_lt_sub_left
    (Int.lt_add_one_of_le (Int.le_refl d)) n

private def projectIntOption : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt i) SortK.dotk => some i
  | _ => none

private def projectValIntOption : SortVal → Option SortInt
  | SortVal.inj_SortInt i => some i
  | _ => none

private theorem projectIntOption_injVal (v : SortVal) :
    projectIntOption
      (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk)
      = projectValIntOption v := by
  cases v <;> rfl

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_-Int_» (x y : SortInt) : SortInt := x - y
/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (x y : SortBool) : SortBool := x && y
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (x y : SortInt) : SortBool := decide (x > y)
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (x y : SortInt) : SortBool := decide (x >= y)
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914, rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (x y : SortInt) : SortBool := decide (x < y)
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x y : SortInt) : SortBool := decide (x <= y)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (x y : SortInt) : SortBool := decide (x = y)
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» (x y : SortInt) : SortBool := decide (x ≠ y)
/- KORE symbol: Lbl'UndsPerc'Int'Unds'; frozen source obligations: rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_%Int_» (x y : SortInt) : SortInt := x % y
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: Lbl'UndsSlsh'Int'Unds'; frozen source obligations: rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_/Int_» (x y : SortInt) : SortInt := Int.tdiv x y
/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    (op : SortString) (left right : SortVal) : SortVal :=
  match arithmeticInt? left, arithmeticInt? right with
  | some x, some y =>
      if op = "+" then SortVal.inj_SortInt (x + y)
      else if op = "-" then SortVal.inj_SortInt (x - y)
      else if op = "*" then SortVal.inj_SortInt (x * y)
      else if op = "%" then SortVal.inj_SortInt (pyModModel x y)
      else if op = "//" then
        SortVal.inj_SortInt (Int.tdiv (x - pyModModel x y) y)
      else if op = "**" ∧ 0 <= y then
        SortVal.inj_SortInt (Int.pow x y.toNat)
      else SortVal.inj_SortInt 999
  | _, _ => SortVal.«noneV_MPY-CORE_Val»
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (op : SortString) (left right : SortVal) : SortBool :=
  match arithmeticInt? left, arithmeticInt? right with
  | some x, some y =>
      if op = "<" then decide (x < y)
      else if op = "<=" then decide (x <= y)
      else if op = ">" then decide (x > y)
      else if op = ">=" then decide (x >= y)
      else if op = "==" then decide (x = y)
      else if op = "!=" then decide (x ≠ y)
      else false
  | _, _ => false
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» (v : SortVal) : SortBool :=
  (projectValIntOption v).isSome
/- KORE symbol: LbldigitSum'LParUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int; frozen source obligations: rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51, rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a, rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «digitSum(_)_VERIFICATION_Int_Int» : SortInt → SortInt :=
  digitSumModel
/- KORE symbol: LblisInt; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914, rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt (k : SortK) : SortBool :=
  (projectIntOption k).isSome
/- KORE symbol: LblprimeTail'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Int'Unds'Int; frozen source obligations: rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «primeTail(_,_)_VERIFICATION_Bool_Int_Int» : SortInt → SortInt → SortBool :=
  primeTailModel
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» (k : SortK) : SortInt :=
  (projectIntOption k).getD 0
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d, rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081, rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4, rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914, rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal (v : SortVal) : SortInt :=
  (projectValIntOption v).getD 0
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91, rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06, rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» : SortInt → SortInt → SortInt :=
  pyModModel
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt :=
  projectIntOption

theorem final :
    Klean94Skjkasdkd.Lemmas.targetStatement «_-Int_» _andBool_ «_>Int_» «_>=Int_» «_<Int_» «_<=Int_» «_==Int_» «_=/=Int_» «_%Int_» «_+Int_» «_/Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» «digitSum(_)_VERIFICATION_Int_Int» isInt «primeTail(_,_)_VERIFICATION_Bool_Int_Int» «project:Int» projectIntTotal «pyMod(_,_)_MPY-INT_Int_Int_Int» «project:Int?» := by
  unfold Klean94Skjkasdkd.Lemmas.targetStatement
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro V
    rw [show «project:Int?»
      (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
        = projectValIntOption V by
          exact projectIntOption_injVal V]
    cases V <;>
      simp [
        «definedProjectInt(_)_VERIFICATION_Bool_Val»,
        projectValIntOption]
  · intro V h
    cases V <;>
      simp [«definedProjectInt(_)_VERIFICATION_Bool_Val»,
        projectValIntOption, «project:Int»,
        projectIntOption_injVal, projectIntTotal] at h ⊢
  · intro V
    cases V <;> simp [projectIntTotal, projectValIntOption]
  · intro I V h
    cases V <;>
      simp [isInt, projectIntOption_injVal,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        arithmeticInt?, projectIntTotal, projectValIntOption,
        «_>Int_»] at h ⊢
  · intro I V h
    cases V <;>
      simp [isInt, projectIntOption_injVal,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        arithmeticInt?, projectIntTotal, projectValIntOption,
        «_>=Int_»] at h ⊢
  · intro V I h
    cases V <;>
      simp [isInt, projectIntOption_injVal,
        «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        arithmeticInt?, projectIntTotal, projectValIntOption,
        «_<Int_»] at h ⊢
  · intro I V h
    cases V <;>
      simp [isInt, projectIntOption_injVal,
        «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
        arithmeticInt?, projectIntTotal, projectValIntOption,
        «pyMod(_,_)_MPY-INT_Int_Int_Int»] at h ⊢
  · intro I V h
    cases V <;>
      simp [isInt, projectIntOption_injVal,
        «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
        arithmeticInt?, projectIntTotal, projectValIntOption,
        «_+Int_»] at h ⊢
  · intro D N h
    simp [_andBool_, «_>=Int_», «_<Int_», «_==Int_»,
      «pyMod(_,_)_MPY-INT_Int_Int_Int»] at h
    rcases h with ⟨⟨hD2, hDN⟩, hmod⟩
    change primeTailModel N D = false
    rw [primeTailModel]
    have hlow : ¬ D < 2 := Int.not_lt_of_ge hD2
    have hdone : ¬ D >= N := Int.not_le_of_gt hDN
    rw [dif_neg hlow, dif_neg hdone]
    simp [hmod]
  · intro D N h
    simp [_andBool_, «_>Int_», «_<=Int_», «_=/=Int_»,
      «pyMod(_,_)_MPY-INT_Int_Int_Int», «_-Int_»] at h
    rcases h with ⟨⟨hD2, hDN⟩, hmod⟩
    change primeTailModel N D = primeTailModel N (D - 1)
    symm
    rw [primeTailModel]
    have hlow : ¬ D - 1 < 2 :=
      Int.not_lt_of_ge (Int.le_sub_one_of_lt hD2)
    have hprevlt : D - 1 < N :=
      Int.lt_of_lt_of_le
        (Int.sub_one_lt_of_le (Int.le_refl D)) hDN
    have hdone : ¬ D - 1 >= N := Int.not_le_of_gt hprevlt
    rw [dif_neg hlow, dif_neg hdone]
    simp [hmod]
  · intro N h
    simp [«_>Int_»] at h
    change pyModModel N 10
      + digitSumModel (Int.tdiv (N - pyModModel N 10) 10)
      = digitSumModel N
    exact (digitSumModel_step N h).symm
  · intro N h
    simp [«_>Int_»] at h
    change pyModModel N 10
      + digitSumModel (Int.tdiv (N - pyModModel N 10) 10)
      = digitSumModel N
    exact (digitSumModel_step N h).symm
  · intro N T h
    simp [«_>Int_»] at h
    change (T + pyModModel N 10)
      + digitSumModel (Int.tdiv (N - pyModModel N 10) 10)
      = T + digitSumModel N
    rw [digitSumModel_step N h]
    exact Int.add_assoc T (pyModModel N 10)
      (digitSumModel (Int.tdiv (N - pyModModel N 10) 10))

end Proof
