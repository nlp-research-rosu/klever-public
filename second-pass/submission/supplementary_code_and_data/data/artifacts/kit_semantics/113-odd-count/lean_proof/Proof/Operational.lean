import Proof.ValueEq

namespace Proof.Operational

private abbrev emptyCodeSequence : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def codeSequenceLength : SortIntSeq → Nat
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      codeSequenceLength rest + 1

def codeSequencePrefix : SortIntSeq → SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» p ps,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» s ss =>
      p == s && codeSequencePrefix ps ss

def appendCodeSequences : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», right => right
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, right =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (appendCodeSequences tail right)

def dropCodeSequence : Nat → SortIntSeq → SortIntSeq
  | 0, source => source
  | _ + 1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | n + 1, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      dropCodeSequence n rest

def substringCountFuel : Nat → SortIntSeq → SortIntSeq → SortInt
  | 0, _, _ => 0
  | _ + 1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => 0
  | _ + 1, _, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | fuel + 1,
      source@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest),
      pattern@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _) =>
      if codeSequencePrefix pattern source then
        1 + substringCountFuel fuel
          (dropCodeSequence (codeSequenceLength pattern) source) pattern
      else
        substringCountFuel fuel rest pattern

/- The exact cntSub recurrence from methods.k, totalized by source-length
   fuel because every recursive rule consumes at least one source code. -/
def nonoverlapSubstringCount (source pattern : SortIntSeq) : SortInt :=
  substringCountFuel (codeSequenceLength source) source pattern

def recognizesStringValue : SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | _ => false

def projectStringCodeSequence : SortVal → SortIntSeq
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) => codes
  | _ => emptyCodeSequence

def isUpperCode (code : SortInt) : Bool :=
  decide (65 ≤ code ∧ code ≤ 90)

def isLowerCode (code : SortInt) : Bool :=
  decide (97 ≤ code ∧ code ≤ 122)

def isAlphaCode (code : SortInt) : Bool :=
  isUpperCode code || isLowerCode code

def isDigitCode (code : SortInt) : Bool :=
  decide (48 ≤ code ∧ code ≤ 57)

def isWhitespaceCode (code : SortInt) : Bool :=
  code == 32 || code == 9 || code == 10 || code == 13

def containsUpperCode : SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isUpperCode code || containsUpperCode rest

def containsLowerCode : SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isLowerCode code || containsLowerCode rest

def everyCodeAlpha : SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isAlphaCode code && everyCodeAlpha rest

def everyCodeDigit : SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isDigitCode code && everyCodeDigit rest

def lowerMappedCode (code : SortInt) : SortInt :=
  if isUpperCode code then code + 32 else code

def upperMappedCode (code : SortInt) : SortInt :=
  if isLowerCode code then code - 32 else code

def swapMappedCode (code : SortInt) : SortInt :=
  if isUpperCode code then code + 32
  else if isLowerCode code then code - 32
  else code

def lowerMappedSequence : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (lowerMappedCode code) (lowerMappedSequence rest)

def upperMappedSequence : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (upperMappedCode code) (upperMappedSequence rest)

def swapMappedSequence : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (swapMappedCode code) (swapMappedSequence rest)

def trimLeadingWhitespace : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | source@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest) =>
      if isWhitespaceCode code then trimLeadingWhitespace rest else source

def reverseCodeSequenceAcc : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, acc =>
      reverseCodeSequenceAcc rest
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code acc)

def reverseCodeSequence (source : SortIntSeq) : SortIntSeq :=
  reverseCodeSequenceAcc source emptyCodeSequence

def strippedCodeSequence (source : SortIntSeq) : SortIntSeq :=
  reverseCodeSequence
    (trimLeadingWhitespace
      (reverseCodeSequence (trimLeadingWhitespace source)))

def joinedCodeSequence : SortIntSeq → SortValSeq → Option SortIntSeq
  | _, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some emptyCodeSequence
  | _, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some codes
  | separator,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        rest@(SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _) => do
      let tail ← joinedCodeSequence separator rest
      pure (appendCodeSequences codes (appendCodeSequences separator tail))
  | _, _ => none

def replacedCodeSequence : SortIntSeq → SortInt → SortInt → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _, _ => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest,
      before, after =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (if code = before then after else code)
        (replacedCodeSequence rest before after)

def countValueOccurrences : SortValSeq → SortVal → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest, sought =>
      (if ValueEq.valueStructuralEq head sought then 1 else 0) +
        countValueOccurrences rest sought

def findValueIndex : SortValSeq → SortVal → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => none
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head rest,
      sought, index =>
      if ValueEq.valueStructuralEq head sought then some index
      else findValueIndex rest sought (index + 1)

/- The frozen md5hexCodes symbol has no K evaluator. This executable
   interpretation supplies its documented MD5 digest meaning. -/
private def md5Modulus : Nat := 0x100000000

private def md5Word (value : Nat) : Nat := value % md5Modulus

private def md5Not (value : Nat) : Nat := Nat.xor value 0xffffffff

private def md5RotateLeft (value distance : Nat) : Nat :=
  md5Word
    (Nat.lor (Nat.shiftLeft value distance)
      (Nat.shiftRight value (32 - distance)))

private def md5Shifts : List Nat := [
  7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

private def md5Constants : List Nat := [
  0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
  0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
  0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
  0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
  0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
  0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
  0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
  0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
  0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
  0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
  0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
  0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
  0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
  0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
  0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
  0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]

private def inputBytes : SortIntSeq → List Nat
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      (code.emod 256).toNat :: inputBytes rest

private def littleEndianBytes (value count : Nat) : List Nat :=
  match count with
  | 0 => []
  | n + 1 => (value % 256) :: littleEndianBytes (value / 256) n

private def md5PaddedBytes (bytes : List Nat) : List Nat :=
  let withMarker := bytes ++ [0x80]
  let zeroCount := (56 + 64 - (withMarker.length % 64)) % 64
  withMarker ++ List.replicate zeroCount 0 ++
    littleEndianBytes (bytes.length * 8) 8

private def md5BlockWord (block : List Nat) (wordIndex : Nat) : Nat :=
  let offset := wordIndex * 4
  md5Word (
    block.getD offset 0 +
    Nat.shiftLeft (block.getD (offset + 1) 0) 8 +
    Nat.shiftLeft (block.getD (offset + 2) 0) 16 +
    Nat.shiftLeft (block.getD (offset + 3) 0) 24)

private def md5RoundChoice (index b c d : Nat) : Nat × Nat :=
  if index < 16 then
    (Nat.lor (Nat.land b c) (Nat.land (md5Not b) d), index)
  else if index < 32 then
    (Nat.lor (Nat.land d b) (Nat.land (md5Not d) c),
      (5 * index + 1) % 16)
  else if index < 48 then
    (Nat.xor (Nat.xor b c) d, (3 * index + 5) % 16)
  else
    (Nat.xor c (Nat.lor b (md5Not d)), (7 * index) % 16)

private def runMd5Rounds :
    Nat → Nat → List Nat → Nat → Nat → Nat → Nat →
      Nat × Nat × Nat × Nat
  | 0, _, _, a, b, c, d => (a, b, c, d)
  | fuel + 1, index, block, a, b, c, d =>
      let choice := md5RoundChoice index b c d
      let rotated := md5RotateLeft
        (md5Word
          (a + choice.1 + md5Constants.getD index 0 +
            md5BlockWord block choice.2))
        (md5Shifts.getD index 0)
      runMd5Rounds fuel (index + 1) block d
        (md5Word (b + rotated)) b c

private def runMd5Blocks :
    Nat → List Nat → Nat → Nat → Nat → Nat →
      Nat × Nat × Nat × Nat
  | 0, _, a, b, c, d => (a, b, c, d)
  | _ + 1, [], a, b, c, d => (a, b, c, d)
  | fuel + 1, bytes, a, b, c, d =>
      let round := runMd5Rounds 64 0 (bytes.take 64) a b c d
      runMd5Blocks fuel (bytes.drop 64)
        (md5Word (a + round.1))
        (md5Word (b + round.2.1))
        (md5Word (c + round.2.2.1))
        (md5Word (d + round.2.2.2))

private def md5DigestBytes (source : SortIntSeq) : List Nat :=
  let padded := md5PaddedBytes (inputBytes source)
  let digest := runMd5Blocks (padded.length / 64 + 1) padded
    0x67452301 0xefcdab89 0x98badcfe 0x10325476
  littleEndianBytes digest.1 4 ++
    littleEndianBytes digest.2.1 4 ++
    littleEndianBytes digest.2.2.1 4 ++
    littleEndianBytes digest.2.2.2 4

private def hexadecimalCode (nibble : Nat) : Nat :=
  if nibble < 10 then 48 + nibble else 87 + nibble

private def hexadecimalCodes : List Nat → List Nat
  | [] => []
  | byte :: rest =>
      hexadecimalCode (byte / 16) :: hexadecimalCode (byte % 16) ::
        hexadecimalCodes rest

private def naturalCodesToSequence : List Nat → SortIntSeq
  | [] => emptyCodeSequence
  | code :: rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (Int.ofNat code) (naturalCodesToSequence rest)

def md5HexadecimalSequence (source : SortIntSeq) : SortIntSeq :=
  naturalCodesToSequence (hexadecimalCodes (md5DigestBytes source))

def makeStringValue (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr
    (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

def makeBooleanValue (value : Bool) : SortVal :=
  SortVal.inj_SortBool value

def makeIntegerValue (value : SortInt) : SortVal :=
  SortVal.inj_SortInt value

/- Complete direct method table from methods.k, tuple.k, builtins.k, and the
   guarded verification.k count extension. noneV is used only when no frozen
   rule matches or a frozen partial helper has no result. -/
def dispatchStringMethodMeaning
    (codes : SortIntSeq) (method : SortString) (args : SortVals) : SortVal :=
  if method = "isupper" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeBooleanValue (containsUpperCode codes && !containsLowerCode codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "islower" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeBooleanValue (containsLowerCode codes && !containsUpperCode codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "isalpha" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeBooleanValue (codeSequenceLength codes > 0 && everyCodeAlpha codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "isdigit" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeBooleanValue (codeSequenceLength codes > 0 && everyCodeDigit codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "lower" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeStringValue (lowerMappedSequence codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "upper" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeStringValue (upperMappedSequence codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "swapcase" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeStringValue (swapMappedSequence codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "join" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        match joinedCodeSequence codes values with
        | some result => makeStringValue result
        | none => SortVal.«noneV_MPY-CORE_Val»
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "count" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» pattern))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeIntegerValue (nonoverlapSubstringCount codes pattern)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "strip" then
    match args with
    | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeStringValue (strippedCodeSequence codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "encode" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr _)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeStringValue codes
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "startswith" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» pattern))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        makeBooleanValue (codeSequencePrefix pattern codes)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else if method = "replace" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
              before SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                after SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
        makeStringValue (replacedCodeSequence codes before after)
    | _ => SortVal.«noneV_MPY-CORE_Val»
  else
    SortVal.«noneV_MPY-CORE_Val»

def dispatchMethodMeaning
    (receiver : SortVal) (method : SortString) (args : SortVals) : SortVal :=
  match receiver with
  | SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) =>
      dispatchStringMethodMeaning codes method args
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
      if method = "count" then
        match args with
        | SortVals.«_,__MPY-CORE_Vals_Val_Vals» sought
            SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
            makeIntegerValue (countValueOccurrences values sought)
        | _ => SortVal.«noneV_MPY-CORE_Val»
      else
        SortVal.«noneV_MPY-CORE_Val»
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
      if method = "index" then
        match args with
        | SortVals.«_,__MPY-CORE_Vals_Val_Vals» sought
            SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
            match findValueIndex values sought 0 with
            | some index => makeIntegerValue index
            | none => SortVal.«noneV_MPY-CORE_Val»
        | _ => SortVal.«noneV_MPY-CORE_Val»
      else
        SortVal.«noneV_MPY-CORE_Val»
  | SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» codes =>
      if method = "hexdigest" then
        match args with
        | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
            makeStringValue (md5HexadecimalSequence codes)
        | _ => SortVal.«noneV_MPY-CORE_Val»
      else
        SortVal.«noneV_MPY-CORE_Val»
  | _ => SortVal.«noneV_MPY-CORE_Val»

end Proof.Operational
