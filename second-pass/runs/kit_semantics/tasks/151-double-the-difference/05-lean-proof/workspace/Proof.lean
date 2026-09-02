import Klean151DoubleTheDifference.Lemmas

namespace Proof

/- Executable structural equality for the generated K term datatypes.  The
   mutual `SortVal` derivation also produces equality for its mutually-defined
   component sorts; the preceding instances discharge its non-mutual fields. -/
deriving instance BEq for SortExc
deriving instance BEq for SortExcCell
deriving instance BEq for SortEnvCell
deriving instance BEq for SortExitCodeCell
deriving instance BEq for SortGeneratedCounterCell
deriving instance BEq for SortHeapLocCell
deriving instance BEq for SortIntSeq
deriving instance BEq for SortOptInt
deriving instance BEq for SortScopeLocCell
deriving instance BEq for SortParamNames
deriving instance BEq for SortCellVars
deriving instance BEq for SortFreeVars
deriving instance BEq for SortParams
deriving instance BEq for SortVal
deriving instance BEq for SortValSeq

private def valIntProjection? : SortVal → Option SortInt
  | SortVal.inj_SortInt i => some i
  | _ => none

private def valIntProjectionTotal (v : SortVal) : SortInt :=
  (valIntProjection? v).getD 0

private def kIntProjection? : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt i) SortK.dotk => some i
  | _ => none

/- K's `%Int` is truncating remainder.  Python's remainder is the frozen
   two-remainder adjustment from MPY-INT. -/
private def pythonMod? (i₁ i₂ : SortInt) : Option SortInt :=
  if i₂ = 0 then none
  else some (Int.tmod (Int.tmod i₁ i₂ + i₂) i₂)

private def pythonModTotal (i₁ i₂ : SortInt) : SortInt :=
  (pythonMod? i₁ i₂).getD 0

private def boolAsInt : SortBool → SortInt
  | true => 1
  | false => 0

private def intPower? (base exponent : SortInt) : Option SortInt :=
  match exponent with
  | Int.ofNat n => some (Int.pow base n)
  | Int.negSucc _ => none

private def floatFromInt (i : SortInt) : SortFloat :=
  Float.ofInt i

private def pythonFloatMod (f₁ f₂ : SortFloat) : SortFloat :=
  f₁ - Float.floor (f₁ / f₂) * f₂

private def intSeqMember (code : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      (code == head) || intSeqMember code tail

private def intSeqSubset : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, other =>
      intSeqMember head other && intSeqSubset tail other

private def intSeqSetEq (left right : SortIntSeq) : SortBool :=
  intSeqSubset left right && intSeqSubset right left

private def valSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      valSeqLength tail + 1

private def dictLookup? : SortValSeq → SortValSeq → SortVal → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keys,
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values,
    sought =>
      if key == sought then some value else dictLookup? keys values sought
  | _, _, _ => none

private def dictSubsetOperational :
    SortValSeq → SortValSeq → SortValSeq → SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
    SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keys,
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values,
    otherKeys, otherValues =>
      match dictLookup? otherKeys otherValues key with
      | some otherValue =>
          (otherValue == value) &&
            dictSubsetOperational keys values otherKeys otherValues
      | none => false
  | _, _, _, _ => false

private def dictEqOperational
    (keys₁ values₁ keys₂ values₂ : SortValSeq) : SortBool :=
  (valSeqLength keys₁ == valSeqLength keys₂) &&
    dictSubsetOperational keys₁ values₁ keys₂ values₂

private def oddSquareOperational (i : SortInt) : SortInt :=
  if decide (i > 0) && decide (pythonModTotal i 2 = 1) then i * i else 0

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-c3d4bdc727e825560b34733f473eca514ee7daf812bf838c8e485dc9499825dc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (b₁ b₂ : SortBool) : SortBool := b₁ && b₂
/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (i₁ i₂ : SortInt) : SortBool := decide (i₁ > i₂)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-04549f60991829d3658a3f2aa1db8529f345e1f464cd668bbe8ba2f031f4ed18. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (i₁ i₂ : SortInt) : SortInt := i₁ + i₂
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-c3d4bdc727e825560b34733f473eca514ee7daf812bf838c8e485dc9499825dc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (i₁ i₂ : SortInt) : SortInt := i₁ * i₂
/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-c3d4bdc727e825560b34733f473eca514ee7daf812bf838c8e485dc9499825dc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal
  | "+", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      SortVal.inj_SortInt (i₁ + i₂)
  | "+", SortVal.inj_SortInt i, SortVal.inj_SortBool b =>
      SortVal.inj_SortInt (i + boolAsInt b)
  | "+", SortVal.inj_SortBool b, SortVal.inj_SortInt i =>
      SortVal.inj_SortInt (boolAsInt b + i)
  | "-", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      SortVal.inj_SortInt (i₁ - i₂)
  | "*", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      SortVal.inj_SortInt (i₁ * i₂)
  | "%", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      SortVal.inj_SortInt (pythonModTotal i₁ i₂)
  | "//", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      if i₂ = 0 then SortVal.«noneV_MPY-CORE_Val»
      else SortVal.inj_SortInt (Int.tdiv (i₁ - pythonModTotal i₁ i₂) i₂)
  | "**", SortVal.inj_SortInt base, SortVal.inj_SortInt exponent =>
      match intPower? base exponent with
      | some value => SortVal.inj_SortInt value
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "/", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      SortVal.inj_SortFloat (floatFromInt i / f)
  | "/", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      SortVal.inj_SortFloat (floatFromInt i₁ / floatFromInt i₂)
  | "%", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      SortVal.inj_SortFloat (pythonFloatMod f₁ f₂)
  | "-", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      SortVal.inj_SortFloat (f₁ - f₂)
  | "/", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      SortVal.inj_SortFloat (f₁ / f₂)
  | "+", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      SortVal.inj_SortFloat (f₁ + f₂)
  | "*", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      SortVal.inj_SortFloat (f₁ * f₂)
  | "**", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      SortVal.inj_SortFloat (Float.pow f₁ f₂)
  | "**", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      SortVal.inj_SortFloat (Float.pow (floatFromInt i) f)
  | "**", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      SortVal.inj_SortFloat (Float.pow f (floatFromInt i))
  | "-", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      SortVal.inj_SortFloat (floatFromInt i - f)
  | "-", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      SortVal.inj_SortFloat (f - floatFromInt i)
  | "+", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      SortVal.inj_SortFloat (floatFromInt i + f)
  | "+", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      SortVal.inj_SortFloat (f + floatFromInt i)
  | "*", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      SortVal.inj_SortFloat (floatFromInt i * f)
  | "*", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      SortVal.inj_SortFloat (f * floatFromInt i)
  | "/", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      SortVal.inj_SortFloat (f / floatFromInt i)
  | _, _, _ => SortVal.«noneV_MPY-CORE_Val»
/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» :
    SortString → SortVal → SortVal → SortBool
  | "==", SortVal.inj_SortBool b₁, SortVal.inj_SortBool b₂ => b₁ == b₂
  | "!=", SortVal.inj_SortBool b₁, SortVal.inj_SortBool b₂ => b₁ != b₂
  | "<", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      decide (i₁ < i₂)
  | "<=", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      decide (i₁ ≤ i₂)
  | ">", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      decide (i₁ > i₂)
  | ">=", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ =>
      decide (i₁ ≥ i₂)
  | "==", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ => i₁ == i₂
  | "!=", SortVal.inj_SortInt i₁, SortVal.inj_SortInt i₂ => i₁ != i₂
  | "==", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ => f₁ == f₂
  | "!=", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ => !(f₁ == f₂)
  | "<", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      decide (f₁ < f₂)
  | ">", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      decide (f₁ > f₂)
  | ">=", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      !(decide (f₁ < f₂))
  | "<=", SortVal.inj_SortFloat f₁, SortVal.inj_SortFloat f₂ =>
      !(decide (f₁ > f₂))
  | "==", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      floatFromInt i == f
  | "==", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      f == floatFromInt i
  | "!=", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      !(floatFromInt i == f)
  | "!=", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      !(f == floatFromInt i)
  | "<", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      decide (floatFromInt i < f)
  | "<", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      decide (f < floatFromInt i)
  | ">", SortVal.inj_SortInt i, SortVal.inj_SortFloat f =>
      decide (floatFromInt i > f)
  | ">", SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      decide (f > floatFromInt i)
  | "==", SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values₁),
      SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values₂) =>
      values₁ == values₂
  | "!=", SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values₁),
      SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values₂) =>
      values₁ != values₂
  | "==", SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values₁),
      SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values₂) =>
      values₁ == values₂
  | "!=", SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values₁),
      SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values₂) =>
      values₁ != values₂
  | "==", SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₁ values₁,
      SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₂ values₂ =>
      dictEqOperational keys₁ values₁ keys₂ values₂
  | "==", SortVal.«setV(_)_MPY-SET_Val_IntSeq» codes₁,
      SortVal.«setV(_)_MPY-SET_Val_IntSeq» codes₂ =>
      intSeqSetEq codes₁ codes₂
  | "==", value, SortVal.«noneV_MPY-CORE_Val» =>
      value == SortVal.«noneV_MPY-CORE_Val»
  | "!=", value, SortVal.«noneV_MPY-CORE_Val» =>
      value != SortVal.«noneV_MPY-CORE_Val»
  | "is", value, SortVal.«noneV_MPY-CORE_Val» =>
      value == SortVal.«noneV_MPY-CORE_Val»
  | "is not", value, SortVal.«noneV_MPY-CORE_Val» =>
      value != SortVal.«noneV_MPY-CORE_Val»
  | _, _, _ => false
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false
/- KORE symbol: Lbldtd'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'ValSeq; frozen source obligations: rule-04549f60991829d3658a3f2aa1db8529f345e1f464cd668bbe8ba2f031f4ed18, rule-663dfaf9b65e6ba3e1928de01c21ec78aeceec06ef94896d881e0da14372c17c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt i) tail =>
      oddSquareOperational i + «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortFloat _) tail =>
      «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» tail
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» tail
/- KORE symbol: LblisFloat; frozen source obligations: rule-663dfaf9b65e6ba3e1928de01c21ec78aeceec06ef94896d881e0da14372c17c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isFloat : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortFloat _) SortK.dotk => true
  | _ => false
/- KORE symbol: LblisInt; frozen source obligations: rule-04549f60991829d3658a3f2aa1db8529f345e1f464cd668bbe8ba2f031f4ed18, rule-e0cb703bc5de627528842cad9c26edce5c5ccfba97a015cd76b3ffa227523e1e, rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-c3d4bdc727e825560b34733f473eca514ee7daf812bf838c8e485dc9499825dc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false
/- KORE symbol: LblisIntV'LParUndsRParUnds'MPY-BUILTINS'Unds'Bool'Unds'Val; frozen source obligations: rule-e0cb703bc5de627528842cad9c26edce5c5ccfba97a015cd76b3ffa227523e1e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isIntV(_)_MPY-BUILTINS_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false
/- KORE symbol: LbloddIntSquare'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Int'Unds'Int; frozen source obligations: rule-04549f60991829d3658a3f2aa1db8529f345e1f464cd668bbe8ba2f031f4ed18. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «oddIntSquare(_)_VERIFICATION-SYNTAX_Int_Int» (i : SortInt) : SortInt :=
  oddSquareOperational i
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-04549f60991829d3658a3f2aa1db8529f345e1f464cd668bbe8ba2f031f4ed18, rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081, rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388, rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a, rule-c3d4bdc727e825560b34733f473eca514ee7daf812bf838c8e485dc9499825dc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal (v : SortVal) : SortInt :=
  valIntProjectionTotal v
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» (i₁ i₂ : SortInt) : SortInt :=
  pythonModTotal i₁ i₂
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» (k : SortK) : Option SortInt :=
  kIntProjection? k

private theorem isIntGuardValue
    (v : SortVal)
    (h : isInt (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk) = true) :
    ∃ i, v = SortVal.inj_SortInt i := by
  cases v <;> simp_all [isInt, inj]

private theorem isFloatGuardValue
    (v : SortVal)
    (h : isFloat (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk) = true) :
    ∃ f, v = SortVal.inj_SortFloat f := by
  cases v <;> simp_all [isFloat, inj]

private theorem andTrueLeft (a b : SortBool)
    (h : _andBool_ a b = true) : a = true := by
  cases a <;> simp_all [_andBool_]

private theorem andTrueRight (a b : SortBool)
    (h : _andBool_ a b = true) : b = true := by
  cases a <;> cases b <;> simp_all [_andBool_]

theorem final :
    Klean151DoubleTheDifference.Lemmas.targetStatement _andBool_ «_>Int_» «_+Int_» «_*Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» «dtd(_)_VERIFICATION-SYNTAX_Int_ValSeq» isFloat isInt «isIntV(_)_MPY-BUILTINS_Bool_Val» «oddIntSquare(_)_VERIFICATION-SYNTAX_Int_Int» projectIntTotal «pyMod(_,_)_MPY-INT_Int_Int_Int» «project:Int?» := by
  unfold Klean151DoubleTheDifference.Lemmas.targetStatement
  constructor
  · intro VS V h
    obtain ⟨i, rfl⟩ := isIntGuardValue V h
    rfl
  constructor
  · intro VS V h
    obtain ⟨f, rfl⟩ := isFloatGuardValue V h
    rfl
  constructor
  · intro V
    cases V <;>
      simp [«project:Int?», kIntProjection?, inj,
        «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val»]
  constructor
  · intro V
    rfl
  constructor
  · intro V
    cases V <;>
      rfl
  constructor
  · intro I V h
    obtain ⟨i, rfl⟩ := isIntGuardValue V h
    rfl
  constructor
  · intro I V h
    obtain ⟨i, rfl⟩ := isIntGuardValue V h
    rfl
  · intro V₂ V₁ h
    have h₁ :
        isInt (SortK.kseq ((@inj SortVal SortKItem) V₁) SortK.dotk) = true :=
      andTrueLeft _ _ h
    have h₂ :
        isInt (SortK.kseq ((@inj SortVal SortKItem) V₂) SortK.dotk) = true :=
      andTrueRight _ _ h
    obtain ⟨i₁, rfl⟩ := isIntGuardValue V₁ h₁
    obtain ⟨i₂, rfl⟩ := isIntGuardValue V₂ h₂
    rfl

end Proof
