import Klean0HasCloseElements.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (lhs rhs : SortBool) : SortBool :=
  lhs && rhs

/- `applyBin` is partial in the K definition. The cases below are every
   arithmetic case whose values are represented by the generated `SortVal`.
   The final branch totalizes genuinely stuck K combinations; it is unreachable
   under the float-sort guard in the frozen source rule. -/
private def pyMod (lhs rhs : SortInt) : SortInt :=
  Int.emod (Int.emod lhs rhs + rhs) rhs

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal
  | "-", SortVal.inj_SortFloat lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (lhs - rhs)
  | "-", SortVal.inj_SortInt lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (Float.ofInt lhs - rhs)
  | "-", SortVal.inj_SortFloat lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortFloat (lhs - Float.ofInt rhs)
  | "-", SortVal.inj_SortInt lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortInt (lhs - rhs)
  | "+", SortVal.inj_SortFloat lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (lhs + rhs)
  | "+", SortVal.inj_SortInt lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (Float.ofInt lhs + rhs)
  | "+", SortVal.inj_SortFloat lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortFloat (lhs + Float.ofInt rhs)
  | "+", SortVal.inj_SortInt lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortInt (lhs + rhs)
  | "+", SortVal.inj_SortInt lhs, SortVal.inj_SortBool rhs =>
      SortVal.inj_SortInt (lhs + if rhs then 1 else 0)
  | "+", SortVal.inj_SortBool lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortInt ((if lhs then 1 else 0) + rhs)
  | "*", SortVal.inj_SortFloat lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (lhs * rhs)
  | "*", SortVal.inj_SortInt lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (Float.ofInt lhs * rhs)
  | "*", SortVal.inj_SortFloat lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortFloat (lhs * Float.ofInt rhs)
  | "*", SortVal.inj_SortInt lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortInt (lhs * rhs)
  | "/", SortVal.inj_SortFloat lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (lhs / rhs)
  | "/", SortVal.inj_SortInt lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (Float.ofInt lhs / rhs)
  | "/", SortVal.inj_SortFloat lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortFloat (lhs / Float.ofInt rhs)
  | "/", SortVal.inj_SortInt lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortFloat (Float.ofInt lhs / Float.ofInt rhs)
  | "%", SortVal.inj_SortFloat lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (lhs - Float.floor (lhs / rhs) * rhs)
  | "%", SortVal.inj_SortInt lhs, SortVal.inj_SortInt rhs =>
      if rhs = 0 then SortVal.«noneV_MPY-CORE_Val»
      else SortVal.inj_SortInt (pyMod lhs rhs)
  | "//", SortVal.inj_SortInt lhs, SortVal.inj_SortInt rhs =>
      if rhs = 0 then SortVal.«noneV_MPY-CORE_Val»
      else SortVal.inj_SortInt (Int.tdiv (lhs - pyMod lhs rhs) rhs)
  | "**", SortVal.inj_SortFloat lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (lhs ^ rhs)
  | "**", SortVal.inj_SortInt lhs, SortVal.inj_SortFloat rhs =>
      SortVal.inj_SortFloat (Float.ofInt lhs ^ rhs)
  | "**", SortVal.inj_SortFloat lhs, SortVal.inj_SortInt rhs =>
      SortVal.inj_SortFloat (lhs ^ Float.ofInt rhs)
  | "**", SortVal.inj_SortInt lhs, SortVal.inj_SortInt (Int.ofNat rhs) =>
      SortVal.inj_SortInt (Int.pow lhs rhs)
  | _, _, _ =>
      SortVal.«noneV_MPY-CORE_Val»

/- KORE symbol: LblasFloat'LParUndsRParUnds'VERIFICATION'Unds'Float'Unds'Val; frozen source obligations: rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «asFloat(_)_VERIFICATION_Float_Val» : SortVal → SortFloat
  | SortVal.inj_SortFloat value => value
  | _ => 0.0

/- KORE symbol: LblisFloat; frozen source obligations: rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isFloat : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortFloat _) SortK.dotk => true
  | _ => false

/- KORE symbol: LblsubF; frozen source obligations: rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf. Replace this stub with its honest total meaning from the frozen K semantics. -/
def subF (lhs rhs : SortFloat) : SortFloat :=
  lhs - rhs

private theorem isFloat_injected_iff (value : SortVal) :
    isFloat
        (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) = true ↔
      ∃ floatValue, value = SortVal.inj_SortFloat floatValue := by
  cases value <;> simp [isFloat, inj]

theorem final :
    Klean0HasCloseElements.Lemmas.targetStatement _andBool_ «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «asFloat(_)_VERIFICATION_Float_Val» isFloat subF := by
  unfold Klean0HasCloseElements.Lemmas.targetStatement
  intro B A h
  simp only [_andBool_, Bool.and_eq_true] at h
  rcases (isFloat_injected_iff A).mp h.1 with ⟨lhs, rfl⟩
  rcases (isFloat_injected_iff B).mp h.2 with ⟨rhs, rfl⟩
  rfl

end Proof
