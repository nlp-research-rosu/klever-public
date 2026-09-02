import Klean109MoveOneBall.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d, rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool := left && right
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d, rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (left right : SortInt) : SortBool := decide (left < right)
/- KORE symbol: LblisInt; frozen source obligations: rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d, rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false
/- KORE symbol: LblallInts'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'ValSeq; frozen source obligations: rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «allInts(_)_VERIFICATION_Bool_ValSeq» : SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      isInt (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) &&
        «allInts(_)_VERIFICATION_Bool_ValSeq» rest
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d, rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» :
    SortString → SortVal → SortVal → SortBool
  | "<", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      decide (left < right)
  | "<=", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      decide (left ≤ right)
  | ">", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      decide (left > right)
  | ">=", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      decide (left ≥ right)
  | "==", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      decide (left = right)
  | "!=", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      decide (left ≠ right)
  | _, _, _ => false
/- KORE symbol: LbllastAfter'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Val'Unds'Val'Unds'ValSeq; frozen source obligations: rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» :
    SortVal → SortValSeq → SortVal
  | previous, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => previous
  | _, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      «lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» value rest
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d, rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» : SortK → SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => value
  | _ => 0

private theorem applyCmp_lt_of_int
    (left right : SortVal)
    (left_is_int :
      isInt (SortK.kseq ((@inj SortVal SortKItem) left) SortK.dotk) = true)
    (right_is_int :
      isInt (SortK.kseq ((@inj SortVal SortKItem) right) SortK.dotk) = true) :
    «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" left right =
      «_<Int_»
        («project:Int»
          (SortK.kseq ((@inj SortVal SortKItem) left) SortK.dotk))
        («project:Int»
          (SortK.kseq ((@inj SortVal SortKItem) right) SortK.dotk)) := by
  cases left <;> cases right <;>
    simp_all [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val», «_<Int_»,
      isInt, «project:Int», inj]

private theorem lastAfter_isInt :
    ∀ (previous : SortVal) (values : SortValSeq),
      isInt (SortK.kseq ((@inj SortVal SortKItem) previous) SortK.dotk) = true →
      «allInts(_)_VERIFICATION_Bool_ValSeq» values = true →
      isInt
        (SortK.kseq
          ((@inj SortVal SortKItem)
            («lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» previous values))
          SortK.dotk) = true
  | previous, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», previous_is_int, _ => by
      simpa [«lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq»] using previous_is_int
  | _, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, _, all_ints => by
      have parts :
          isInt (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) = true ∧
            «allInts(_)_VERIFICATION_Bool_ValSeq» rest = true := by
        simpa [«allInts(_)_VERIFICATION_Bool_ValSeq»] using all_ints
      simpa [«lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq»] using
        lastAfter_isInt value rest parts.1 parts.2

theorem final :
    Klean109MoveOneBall.Lemmas.targetStatement _andBool_ «_<Int_» «allInts(_)_VERIFICATION_Bool_ValSeq» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» isInt «lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» «project:Int» := by
  constructor
  · intro B A h
    simp [_andBool_] at h
    exact applyCmp_lt_of_int A B h.1 h.2
  · intro VS P A h
    simp [_andBool_] at h
    exact applyCmp_lt_of_int A
      («lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» P VS)
      h.1.1
      (lastAfter_isInt P VS h.1.2 h.2)

end Proof
