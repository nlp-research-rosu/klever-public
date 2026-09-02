import Proof.FrozenDispatch

namespace Proof

/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-2944c4d3c7bc5a2d260f24ca8fd4234701fa8f82f00db7ca3317fa06458082b5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt :=
  left + right

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-2944c4d3c7bc5a2d260f24ca8fd4234701fa8f82f00db7ca3317fa06458082b5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal :=
  FrozenDispatch.applyBin

/- KORE symbol: LblapplyBuiltin'LParUndsCommUndsRParUnds'MPY-BUILTINS'Unds'Val'Unds'String'Unds'Vals; frozen source obligations: rule-7749c9857edd14009417bdaa86b5d4b1c229fa0013cc411eaf35ed3a49ed0842. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» :
    SortString → SortVals → SortVal :=
  FrozenDispatch.applyBuiltin

/- KORE symbol: LblisInt; frozen source obligations: rule-2944c4d3c7bc5a2d260f24ca8fd4234701fa8f82f00db7ca3317fa06458082b5, rule-7749c9857edd14009417bdaa86b5d4b1c229fa0013cc411eaf35ed3a49ed0842. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false

/- KORE symbol: LblminInt'LParUndsCommUndsRParUnds'INT-COMMON'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-7749c9857edd14009417bdaa86b5d4b1c229fa0013cc411eaf35ed3a49ed0842. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «minInt(_,_)_INT-COMMON_Int_Int_Int»
    (left right : SortInt) : SortInt :=
  FrozenDispatch.minInt left right

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-2944c4d3c7bc5a2d260f24ca8fd4234701fa8f82f00db7ca3317fa06458082b5, rule-7749c9857edd14009417bdaa86b5d4b1c229fa0013cc411eaf35ed3a49ed0842. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» : SortK → SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => value
  | _ => 0

theorem final :
    Klean114Minsubarraysum.Lemmas.targetStatement «_+Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» isInt «minInt(_,_)_INT-COMMON_Int_Int_Int» «project:Int» := by
  constructor
  · intro V I h
    cases V <;> first | rfl | cases h
  · intro I V h
    cases V <;> first | rfl | cases h

end Proof
