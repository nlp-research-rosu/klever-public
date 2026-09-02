import Klean108CountNums.Lemmas
import Init.Omega

namespace Proof

/- Executable equality for the generated K value universe.  K's ==K rules are
   constructor equality, so these mechanically derived BEq instances are the
   direct computational counterpart. -/
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
deriving instance BEq for SortStr
deriving instance BEq for SortCellVars
deriving instance BEq for SortFreeVars
deriving instance BEq for SortParams
deriving instance BEq for SortIterable, SortVal, SortValSeq, SortVals

private def intSeqNil : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

private def intSeqCons (i : Int) (r : SortIntSeq) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» i r

private def valSeqNil : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

private def valsNil : SortVals :=
  SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»

private def strVal (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

private def listVal (vs : SortValSeq) : SortVal :=
  SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» vs)

private def tupleVal (vs : SortValSeq) : SortVal :=
  SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» vs)

private def rangeVal (a b s : Int) : SortVal :=
  SortVal.inj_SortIterable (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» a b s)

private def zipVal (a b : SortValSeq) : SortVal :=
  SortVal.inj_SortIterable (SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» a b)

private def zipStrVal (a b : SortIntSeq) : SortVal :=
  SortVal.inj_SortIterable (SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» a b)

private def noneVal : SortVal := SortVal.«noneV_MPY-CORE_Val»

private def intSeqSnoc : SortIntSeq → Int → SortIntSeq
  | .«.IntSeq_MPY-CORE_IntSeq», i => intSeqCons i intSeqNil
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» h t, i =>
      intSeqCons h (intSeqSnoc t i)

private def intSeqLen : SortIntSeq → Int
  | .«.IntSeq_MPY-CORE_IntSeq» => 0
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ t => 1 + intSeqLen t

private def valSeqLen : SortValSeq → Int
  | .«.ValSeq_MPY-CORE_ValSeq» => 0
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ t => 1 + valSeqLen t

private def allDigitCodesImpl : SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq» => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c r =>
      (48 ≤ c && c ≤ 57) && allDigitCodesImpl r

private def natDecimalCodesAux : Nat → Nat → SortIntSeq
  | 0, _ => intSeqCons 48 intSeqNil
  | fuel + 1, n =>
      if n < 10 then
        intSeqCons (Int.ofNat (48 + n)) intSeqNil
      else
        intSeqSnoc (natDecimalCodesAux fuel (n / 10))
          (Int.ofNat (48 + n % 10))

private def decimalCodesImpl (i : Int) : SortIntSeq :=
  if i < 0 then
    intSeqCons 45 (natDecimalCodesAux (i.natAbs + 1) i.natAbs)
  else
    natDecimalCodesAux (i.toNat + 1) i.toNat

private theorem intSeqSnoc_digits (s : SortIntSeq) (c : Int)
    (hs : allDigitCodesImpl s = true) (hlo : 48 ≤ c) (hhi : c ≤ 57) :
    allDigitCodesImpl (intSeqSnoc s c) = true := by
  induction s with
  | «.IntSeq_MPY-CORE_IntSeq» =>
      simp [intSeqSnoc, intSeqCons, intSeqNil, allDigitCodesImpl, hlo, hhi]
  | «iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» h t ih =>
      simp [allDigitCodesImpl] at hs
      simp [intSeqSnoc, intSeqCons, allDigitCodesImpl, hs.1, ih hs.2]

private theorem natDecimalCodesAux_digits (fuel n : Nat) :
    allDigitCodesImpl (natDecimalCodesAux fuel n) = true := by
  induction fuel generalizing n with
  | zero => simp [natDecimalCodesAux, intSeqCons, intSeqNil, allDigitCodesImpl]
  | succ fuel ih =>
      simp only [natDecimalCodesAux]
      split
      · simp [intSeqCons, intSeqNil, allDigitCodesImpl]
        have hnleNat : n ≤ 9 := by omega
        have hnle : (n : Int) ≤ (9 : Int) := Int.ofNat_le.mpr hnleNat
        constructor
        · exact Int.le_add_of_nonneg_right (Int.ofNat_zero_le n)
        · calc
            48 + (n : Int) ≤ 48 + 9 := Int.add_le_add_left hnle 48
            _ = 57 := by rfl
      · have hm : n % 10 < 10 := Nat.mod_lt _ (by omega)
        apply intSeqSnoc_digits _ _ (ih _)
        · have hloNat : (48 : Nat) ≤ 48 + n % 10 := by omega
          exact Int.ofNat_le.mpr hloNat
        · have hhiNat : 48 + n % 10 ≤ (57 : Nat) := by omega
          exact Int.ofNat_le.mpr hhiNat

private theorem decimalCodes_nonnegative_digits (n : Int) (h : n ≥ 0) :
    allDigitCodesImpl (decimalCodesImpl n) = true := by
  have hn : ¬ n < 0 := by omega
  simp [decimalCodesImpl, hn, natDecimalCodesAux_digits]

private def codeIn (c : Int) : SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» h t =>
      c == h || codeIn c t

private def dedupFrom : SortIntSeq → SortIntSeq → SortIntSeq
  | .«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» h t, acc =>
      if codeIn h acc then dedupFrom t acc
      else dedupFrom t (intSeqSnoc acc h)

private def dedupCodes (s : SortIntSeq) : SortIntSeq :=
  dedupFrom s intSeqNil

private def subsetCodes : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», _ => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» h t, b =>
      codeIn h b && subsetCodes t b

private def sameSet (a b : SortIntSeq) : Bool :=
  subsetCodes a b && subsetCodes b a

private def strPrefix : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», _ => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _, .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      a == b && strPrefix as bs

private def strContains (p : SortIntSeq) : SortIntSeq → Bool
  | x@.«.IntSeq_MPY-CORE_IntSeq» => strPrefix p x
  | x@(.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ xs) =>
      strPrefix p x || strContains p xs

private def strLt : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«.IntSeq_MPY-CORE_IntSeq», .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _, .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      if a < b then true else if a > b then false else strLt as bs

private def dHasKey (keys : SortValSeq) (key : SortVal) : Bool :=
  match keys with
  | .«.ValSeq_MPY-CORE_ValSeq» => false
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» h t =>
      h == key || dHasKey t key

private def dGet (keys vals : SortValSeq) (key : SortVal) : Option SortVal :=
  match keys, vals with
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» k kr,
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v vr =>
      if k == key then some v else dGet kr vr key
  | _, _ => none

private def dSubset (keys vals keys₂ vals₂ : SortValSeq) : Bool :=
  match keys, vals with
  | .«.ValSeq_MPY-CORE_ValSeq», .«.ValSeq_MPY-CORE_ValSeq» => true
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» k kr,
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v vr =>
      dHasKey keys₂ k &&
        (match dGet keys₂ vals₂ k with | some w => w == v | none => false) &&
        dSubset kr vr keys₂ vals₂
  | _, _ => false

private def dictEq (k₁ v₁ k₂ v₂ : SortValSeq) : Bool :=
  valSeqLen k₁ == valSeqLen k₂ && dSubset k₁ v₁ k₂ v₂

private def truthyImpl : SortVal → Option Bool
  | .inj_SortBool b => some b
  | .inj_SortInt i => some (i != 0)
  | .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» s) =>
      some (intSeqLen s != 0)
  | .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» s) =>
      some (valSeqLen s != 0)
  | .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» s) =>
      some (valSeqLen s != 0)
  | .«noneV_MPY-CORE_Val» => some false
  | _ => none

private def rangeLen (lo hi st : Int) : Option Int :=
  if st > 0 then
    some (if lo < hi then (hi - lo + st - 1) / st else 0)
  else if st < 0 then
    some (if hi < lo then (lo - hi - st - 1) / (0 - st) else 0)
  else none

private def maxVals (m : Int) : SortVals → Option Int
  | .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some m
  | .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i) r =>
      maxVals (max m i) r
  | _ => none

private def minVals (m : Int) : SortVals → Option Int
  | .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some m
  | .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i) r =>
      minVals (min m i) r
  | _ => none

private def natBinaryCodesAux : Nat → Nat → SortIntSeq
  | 0, _ => intSeqCons 48 intSeqNil
  | _ + 1, n =>
      if n < 2 then intSeqCons (Int.ofNat (48 + n)) intSeqNil
      else
        intSeqSnoc (natBinaryCodesAux n (n / 2))
          (Int.ofNat (48 + n % 2))

private def binaryCodes (n : Int) : SortIntSeq :=
  let mag := n.natAbs
  let digits := natBinaryCodesAux (mag + 1) mag
  if n < 0 then
    intSeqCons 45 (intSeqCons 48 (intSeqCons 98 digits))
  else
    intSeqCons 48 (intSeqCons 98 digits)

private def intDigitsAcc : SortIntSeq → Int → Int
  | .«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c r, acc =>
      intDigitsAcc r (acc * 10 + (c - 48))

private def intPartAcc : SortIntSeq → Int → Int
  | .«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 _, acc => acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c r, acc =>
      intPartAcc r (acc * 10 + (c - 48))

private def fracAcc : SortIntSeq → Int → Int
  | .«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c r, acc =>
      fracAcc r (acc * 10 + (c - 48))

private def fracPart : SortIntSeq → Int
  | .«.IntSeq_MPY-CORE_IntSeq» => 0
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 r => fracAcc r 0
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ r => fracPart r

private def fracScaleAcc : SortIntSeq → Int → Int
  | .«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ r, acc =>
      fracScaleAcc r (acc * 10)

private def fracScale : SortIntSeq → Int
  | .«.IntSeq_MPY-CORE_IntSeq» => 1
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 r => fracScaleAcc r 1
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ r => fracScale r

private def decimalFloat (s : SortIntSeq) : Option Float :=
  match s with
  | .«.IntSeq_MPY-CORE_IntSeq» => none
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 r =>
      decimalFloat r |>.map (fun f => 0.0 - f)
  | _ =>
      some (Float.ofInt (intPartAcc s 0) +
        Float.ofInt (fracPart s) / Float.ofInt (fracScale s))

/- Decode a binary64 directly, so Float2Int has the arbitrary-precision Int
   range of K rather than silently narrowing through Int64. -/
private def floatIntegralBound (wantCeil : Bool) (f : Float) : Int :=
  let bits := f.toBits.toNat
  let sign := bits / (2 ^ 63) == 1
  let exponent := (bits / (2 ^ 52)) % 2048
  let fraction := bits % (2 ^ 52)
  if exponent == 2047 then
    0
  else
    let mantissa := if exponent == 0 then fraction else 2 ^ 52 + fraction
    let shift : Int :=
      if exponent == 0 then -1074 else Int.ofNat exponent - 1075
    if shift ≥ 0 then
      let magnitude := Int.ofNat (mantissa * (2 ^ shift.toNat))
      if sign then -magnitude else magnitude
    else
      let denominator := 2 ^ (0 - shift).toNat
      let quotient := mantissa / denominator
      let remainder := mantissa % denominator
      let q := Int.ofNat quotient
      if sign then
        if wantCeil || remainder == 0 then -q else -(q + 1)
      else
        if wantCeil && remainder != 0 then q + 1 else q

private def floatFloorInt (f : Float) : Int := floatIntegralBound false f
private def floatCeilInt (f : Float) : Int := floatIntegralBound true f

private def roundFloatInt (f : Float) : Int :=
  let fl := f.floor
  if f - fl == 0.5 then
    let i := fl.toInt64.toInt
    if i % 2 == 0 then i else f.ceil.toInt64.toInt
  else
    (f + 0.5).floor.toInt64.toInt

private def pow10 (n : Int) : Option Int :=
  if 0 ≤ n then some ((10 : Int).pow n.toNat) else none

private def intSeqToList : SortIntSeq → List Int
  | .«.IntSeq_MPY-CORE_IntSeq» => []
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» h t => h :: intSeqToList t

private def tokenizeOps : List Int → List String
  | [] => []
  | 42 :: 42 :: r => "**" :: tokenizeOps r
  | 47 :: 47 :: r => "//" :: tokenizeOps r
  | 42 :: r => "*" :: tokenizeOps r
  | 47 :: r => "/" :: tokenizeOps r
  | 43 :: r => "+" :: tokenizeOps r
  | 45 :: r => "-" :: tokenizeOps r
  | _ :: r => tokenizeOps r

private def takeNumber (acc : Int) : List Int → Int × List Int
  | c :: r =>
      if 48 ≤ c && c ≤ 57 then takeNumber (acc * 10 + c - 48) r
      else (acc, c :: r)
  | [] => (acc, [])

private def tokenizeNumsFuel : Nat → List Int → List Int
  | 0, _ => []
  | _ + 1, [] => []
  | fuel + 1, c :: r =>
      if 48 ≤ c && c ≤ 57 then
        let p := takeNumber (c - 48) r
        p.1 :: tokenizeNumsFuel fuel p.2
      else tokenizeNumsFuel fuel r

private def tokenizeNums (s : List Int) : List Int :=
  tokenizeNumsFuel (s.length + 1) s

private def intPowK (a b : Int) : Int :=
  if b < 0 then 0 else a.pow b.toNat

private def passPow : List String → List Int → List String × List Int
  | [], ns => ([], ns)
  | _, [] => ([], [])
  | op :: ops, n :: ns =>
      let p := passPow ops ns
      if op == "**" then
        match p.2 with
        | m :: rest => (p.1, intPowK n m :: rest)
        | [] => (p.1, [n])
      else
        (op :: p.1, n :: p.2)

private def applyEvalOp (op : String) (a b : Int) : Int :=
  if op == "+" then a + b
  else if op == "-" then a - b
  else if op == "*" then a * b
  else if op == "//" then a / b
  else if op == "**" then intPowK a b
  else a

private def inEvalLevel (level op : String) : Bool :=
  if level == "mul" then op == "*" || op == "//" || op == "/"
  else if level == "add" then op == "+" || op == "-"
  else false

private def passLevelGo (level : String) :
    Int → List String → List Int → List String → List Int →
      List String × List Int
  | cur, [], _, outOps, outNums =>
      (outOps.reverse, (cur :: outNums).reverse)
  | cur, _ :: _, [], outOps, outNums =>
      (outOps.reverse, (cur :: outNums).reverse)
  | cur, op :: ops, n :: ns, outOps, outNums =>
      if inEvalLevel level op then
        passLevelGo level (applyEvalOp op cur n) ops ns outOps outNums
      else
        passLevelGo level n ops ns (op :: outOps) (cur :: outNums)

private def passLevel (level : String)
    (p : List String × List Int) : List String × List Int :=
  match p.2 with
  | [] => (p.1, [])
  | n :: ns => passLevelGo level n p.1 ns [] []

private def evalArith (s : SortIntSeq) : Int :=
  let codes := intSeqToList s
  let p := passPow (tokenizeOps codes) (tokenizeNums codes)
  match (passLevel "add" (passLevel "mul" p)).2 with
  | n :: _ => n
  | [] => 0

private def seqLenImpl : SortVal → Option Int
  | .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» s) => some (intSeqLen s)
  | .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» s) => some (valSeqLen s)
  | .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» s) => some (valSeqLen s)
  | .inj_SortIterable (.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» lo hi st) =>
      rangeLen lo hi st
  | .«setV(_)_MPY-SET_Val_IntSeq» s => some (intSeqLen s)
  | _ => none

/- Complete executable table for the frozen applyCmp rules over every sort
   represented by SortVal. Unsupported combinations are precisely the stuck
   cases of the partial K dispatcher. -/
private def applyCmpImpl : String → SortVal → SortVal → Bool
  | "==", .inj_SortInt a, .inj_SortInt b => a == b
  | "!=", .inj_SortInt a, .inj_SortInt b => a != b
  | "<",  .inj_SortInt a, .inj_SortInt b => a < b
  | "<=", .inj_SortInt a, .inj_SortInt b => a ≤ b
  | ">",  .inj_SortInt a, .inj_SortInt b => a > b
  | ">=", .inj_SortInt a, .inj_SortInt b => a ≥ b
  | "==", .inj_SortBool a, .inj_SortBool b => a == b
  | "!=", .inj_SortBool a, .inj_SortBool b => a != b
  | "==", .inj_SortFloat a, .inj_SortFloat b => a == b
  | "!=", .inj_SortFloat a, .inj_SortFloat b => a != b
  | "<",  .inj_SortFloat a, .inj_SortFloat b => a < b
  | "<=", .inj_SortFloat a, .inj_SortFloat b => !(a > b)
  | ">",  .inj_SortFloat a, .inj_SortFloat b => a > b
  | ">=", .inj_SortFloat a, .inj_SortFloat b => !(a < b)
  | "==", .inj_SortInt a, .inj_SortFloat b => Float.ofInt a == b
  | "!=", .inj_SortInt a, .inj_SortFloat b => Float.ofInt a != b
  | "<",  .inj_SortInt a, .inj_SortFloat b => Float.ofInt a < b
  | ">",  .inj_SortInt a, .inj_SortFloat b => Float.ofInt a > b
  | "==", .inj_SortFloat a, .inj_SortInt b => a == Float.ofInt b
  | "!=", .inj_SortFloat a, .inj_SortInt b => a != Float.ofInt b
  | "<",  .inj_SortFloat a, .inj_SortInt b => a < Float.ofInt b
  | ">",  .inj_SortFloat a, .inj_SortInt b => a > Float.ofInt b
  | "==", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
          .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => a == b
  | "!=", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
          .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => a != b
  | "in", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
          .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => strContains a b
  | "not in", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
              .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => !strContains a b
  | "<", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
         .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => strLt a b
  | ">", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
         .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => strLt b a
  | "<=", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
          .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => !strLt b a
  | ">=", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
          .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => !strLt a b
  | "==", .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» a),
          .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» b) => a == b
  | "!=", .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» a),
          .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» b) => a != b
  | "==", .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» a),
          .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» b) => a == b
  | "!=", .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» a),
          .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» b) => a != b
  | "==", .«setV(_)_MPY-SET_Val_IntSeq» a,
          .«setV(_)_MPY-SET_Val_IntSeq» b => sameSet a b
  | "==", .«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» k₁ v₁,
          .«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» k₂ v₂ =>
      dictEq k₁ v₁ k₂ v₂
  | "==", v, .«noneV_MPY-CORE_Val» => v == noneVal
  | "!=", v, .«noneV_MPY-CORE_Val» => v != noneVal
  | "is", v, .«noneV_MPY-CORE_Val» => v == noneVal
  | "is not", v, .«noneV_MPY-CORE_Val» => v != noneVal
  | _, _, _ => false

private def applyUnImpl : String → SortVal → SortVal
  | "-", .inj_SortInt i => .inj_SortInt (0 - i)
  | "-", .inj_SortFloat f => .inj_SortFloat (0.0 - f)
  | "not", v =>
      match truthyImpl v with
      | some b => .inj_SortBool (!b)
      | none => noneVal
  | _, _ => noneVal

/- Complete executable table for the frozen applyBuiltin rules.  A noneV
   result occurs only when the corresponding K function has no matching
   concrete rule (that is, execution would be stuck). -/
private def applyBuiltinImpl : String → SortVals → SortVal
  | "len", .«_,__MPY-CORE_Vals_Val_Vals» obj .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match seqLenImpl obj with | some n => .inj_SortInt n | none => noneVal
  | "set", .«_,__MPY-CORE_Vals_Val_Vals»
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» s))
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      .«setV(_)_MPY-SET_Val_IntSeq» (dedupCodes s)
  | "abs", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt (Int.natAbs i)
  | "abs", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortFloat f)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortFloat f.abs
  | "floor", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt i
  | "floor", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortFloat f)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt (floatFloorInt f)
  | "ceil", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt i
  | "ceil", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortFloat f)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt (floatCeilInt f)
  | "max", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i) rest =>
      match maxVals i rest with | some n => .inj_SortInt n | none => noneVal
  | "min", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i) rest =>
      match minVals i rest with | some n => .inj_SortInt n | none => noneVal
  | "bin", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => strVal (binaryCodes i)
  | "int", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt i
  | "int", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortFloat f)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      .inj_SortInt (if f ≥ 0.0 then floatFloorInt f else floatCeilInt f)
  | "int", .«_,__MPY-CORE_Vals_Val_Vals»
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» s))
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match s with
      | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c .«.IntSeq_MPY-CORE_IntSeq» =>
          if 48 ≤ c && c ≤ 57 then .inj_SortInt (c - 48) else noneVal
      | _ => if intSeqLen s ≥ 2 then .inj_SortInt (intDigitsAcc s 0) else noneVal
  | "ord", .«_,__MPY-CORE_Vals_Val_Vals»
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq»
        (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c .«.IntSeq_MPY-CORE_IntSeq»)))
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt c
  | "chr", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      if 0 ≤ i && i < 128 then strVal (intSeqCons i intSeqNil) else noneVal
  | "str", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => strVal (decimalCodesImpl i)
  | "str", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortStr s)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortStr s
  | "zip", .«_,__MPY-CORE_Vals_Val_Vals»
      (.inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» a))
      (.«_,__MPY-CORE_Vals_Val_Vals»
        (.inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» b))
        .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => zipVal a b
  | "zip", .«_,__MPY-CORE_Vals_Val_Vals»
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a))
      (.«_,__MPY-CORE_Vals_Val_Vals»
        (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b))
        .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => zipStrVal a b
  | "range", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt stop)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => rangeVal 0 stop 1
  | "range", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt a)
      (.«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt b)
        .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => rangeVal a b 1
  | "range", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt a)
      (.«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt b)
        (.«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt s)
          .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)) =>
      if s != 0 then rangeVal a b s else noneVal
  | "eval", .«_,__MPY-CORE_Vals_Val_Vals»
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» s))
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt (evalArith s)
  | "float", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortFloat (Float.ofInt i)
  | "float", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortFloat f)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortFloat f
  | "float", .«_,__MPY-CORE_Vals_Val_Vals»
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» s))
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match decimalFloat s with | some f => .inj_SortFloat f | none => noneVal
  | "round", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortFloat f)
      .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => .inj_SortInt (roundFloatInt f)
  | "round", .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortFloat f)
      (.«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt n)
        .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      match pow10 n with
      | some p =>
          .inj_SortFloat (Float.ofInt (roundFloatInt (f * Float.ofInt p)) / Float.ofInt p)
      | none => noneVal
  | "isinstance", .«_,__MPY-CORE_Vals_Val_Vals» v
      (.«_,__MPY-CORE_Vals_Val_Vals» (.«typeV(_)_MPY-CORE_Val_String» "int")
        .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      .inj_SortBool (match v with | .inj_SortInt _ => true | _ => false)
  | "isinstance", .«_,__MPY-CORE_Vals_Val_Vals» v
      (.«_,__MPY-CORE_Vals_Val_Vals» (.«typeV(_)_MPY-CORE_Val_String» "str")
        .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      .inj_SortBool (match v with | .inj_SortStr _ => true | _ => false)
  | _, _ => noneVal

private def isIntImpl : SortK → Bool
  | .kseq (.inj_SortInt _) .dotk => true
  | _ => false

private def definedProjectIntImpl : SortVal → Bool
  | .inj_SortInt _ => true
  | _ => false

private def projectIntTotalImpl : SortVal → Int
  | .inj_SortInt i => i
  | _ => 0

private def projectIntPartialImpl : SortK → Option Int
  | .kseq (.inj_SortInt i) .dotk => some i
  | _ => none

private theorem isIntImpl_injected (v : SortVal) :
    isIntImpl (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk) =
      definedProjectIntImpl v := by
  cases v <;> rfl

private theorem projectIntPartialImpl_injected (v : SortVal) :
    (projectIntPartialImpl
      (SortK.kseq ((@inj SortVal SortKItem) v) SortK.dotk)).isSome =
      definedProjectIntImpl v := by
  cases v <;> rfl

private theorem applyCmpImpl_lt_int (a b : Int) :
    applyCmpImpl "<" (.inj_SortInt a) (.inj_SortInt b) =
      decide (a < b) := rfl

private theorem applyUnImpl_neg_int (a : Int) :
    applyUnImpl "-" (.inj_SortInt a) = .inj_SortInt (0 - a) := rfl

private theorem applyBuiltinImpl_str_int (a : Int) :
    applyBuiltinImpl "str"
      (.«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt a) valsNil) =
      strVal (decimalCodesImpl a) := rfl

/- KORE symbol: Lbl'Unds'-Int'Unds'; frozen source obligations: rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2. -/
def «_-Int_» : SortInt → SortInt → SortInt := fun a b => a - b

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da. -/
def _andBool_ : SortBool → SortBool → SortBool := fun a b => a && b

/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da, rule-5af48b88759940f404acea3042b6fa69d00290648ae1c95910aaad61bea89344. -/
def «_>=Int_» : SortInt → SortInt → SortBool := fun a b => a ≥ b

/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69. -/
def «_<Int_» : SortInt → SortInt → SortBool := fun a b => a < b

/- KORE symbol: LblallDigitCodes'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'IntSeq;
   frozen source obligations: rule-5af48b88759940f404acea3042b6fa69d00290648ae1c95910aaad61bea89344. -/
def «allDigitCodes(_)_VERIFICATION_Bool_IntSeq» : SortIntSeq → SortBool :=
  allDigitCodesImpl

/- KORE symbol: LblapplyBuiltin'LParUndsCommUndsRParUnds'MPY-BUILTINS'Unds'Val'Unds'String'Unds'Vals;
   frozen source obligations: rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da. -/
def «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» : SortString → SortVals → SortVal :=
  applyBuiltinImpl

/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val;
   frozen source obligations: rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool :=
  applyCmpImpl

/- KORE symbol: LblapplyUn'LParUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val;
   frozen source obligations: rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2. -/
def «applyUn(_,_)_MPY-CORE_Val_String_Val» : SortString → SortVal → SortVal :=
  applyUnImpl

/- KORE symbol: LbldecimalCodes'LParUndsRParUnds'VERIFICATION'Unds'IntSeq'Unds'Int;
   frozen source obligations: rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da,
   rule-5af48b88759940f404acea3042b6fa69d00290648ae1c95910aaad61bea89344. -/
def «decimalCodes(_)_VERIFICATION_IntSeq_Int» : SortInt → SortIntSeq :=
  decimalCodesImpl

/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val;
   frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool :=
  definedProjectIntImpl

/- KORE symbol: LblisInt; frozen source obligations:
   rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69,
   rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2,
   rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da. -/
def isInt : SortK → SortBool := isIntImpl

/- KORE symbol: LblprojectIntTotal; frozen source obligations:
   rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69,
   rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2,
   rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da.
   The arbitrary fallback is unreachable under definedProjectInt/isInt,
   exactly matching K's guarded total cast boundary. -/
def projectIntTotal : SortVal → SortInt := projectIntTotalImpl

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations:
   rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. -/
def «project:Int?» : SortK → Option SortInt := projectIntPartialImpl

theorem final :
    Klean108CountNums.Lemmas.targetStatement «_-Int_» _andBool_ «_>=Int_» «_<Int_» «allDigitCodes(_)_VERIFICATION_Bool_IntSeq» «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «applyUn(_,_)_MPY-CORE_Val_String_Val» «decimalCodes(_)_VERIFICATION_IntSeq_Int» «definedProjectInt(_)_VERIFICATION_Bool_Val» isInt projectIntTotal «project:Int?» := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro V
    change
      (projectIntPartialImpl
        (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true ↔
        definedProjectIntImpl V = true ∧ True
    rw [projectIntPartialImpl_injected]
    simp
  · intro J V h
    dsimp only [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      «_<Int_», projectIntTotal]
    change isIntImpl
      (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) = true at h
    rw [isIntImpl_injected] at h
    cases V <;>
      simp_all [definedProjectIntImpl, projectIntTotalImpl,
        applyCmpImpl_lt_int]
  · intro V h
    change applyUnImpl "-" V = .inj_SortInt (0 - projectIntTotalImpl V)
    change isIntImpl
      (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) = true at h
    rw [isIntImpl_injected] at h
    cases V <;>
      simp_all [definedProjectIntImpl, projectIntTotalImpl,
        applyUnImpl_neg_int]
  · intro V h
    change applyBuiltinImpl "str"
      (.«_,__MPY-CORE_Vals_Val_Vals» V valsNil) =
      strVal (decimalCodesImpl (projectIntTotalImpl V))
    change
      (isIntImpl
        (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) &&
        projectIntTotalImpl V ≥ 0) = true at h
    rw [isIntImpl_injected] at h
    cases V <;>
      simp_all [definedProjectIntImpl, projectIntTotalImpl,
        applyBuiltinImpl_str_int]
  · intro N h
    dsimp only [«_>=Int_»] at h
    exact decimalCodes_nonnegative_digits N (of_decide_eq_true h)

end Proof
