import Klean95CheckDictCase.Lemmas

namespace Operational

/- The K `==K` used by list.count and tuple.index is structural equality.
   Derive it for the entire generated mutual carrier so those method rules
   cover every value Base can represent, not merely integers. -/
deriving instance BEq for SortIntSeq
deriving instance BEq for SortStr
deriving instance BEq for SortExc, SortExcCell, SortEnvCell,
  SortExitCodeCell, SortGeneratedCounterCell, SortHeapLocCell, SortOptInt,
  SortScopeLocCell, SortParamNames, SortCellVars, SortFreeVars, SortParams
deriving instance BEq for
  SortApplyK, SortBound, SortCmpOp, SortEntries, SortEntry, SortExpr, SortExprs,
  SortGeneratedTopCell, SortHeapCell, SortIndex, SortIterable, SortK, SortKCell,
  SortKItem, SortList, SortMap, SortModule, SortRetCell, SortRetState,
  SortScopesCell, SortStackCell, SortStmt, SortStmts, SortVal, SortValSeq, SortVals

def emptyCodeSequence : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def makeStringValue (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

/- The direct injection is canonical.  The nested case covers raw artificial
   Base values that denote the same transitive K subsort injection. -/
def stringValueCodes? : SortVal → Option SortIntSeq
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) =>
      some codes
  | SortVal.inj_SortIterable
      (SortIterable.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)) =>
      some codes
  | _ => none

def totalStringCodes (value : SortVal) : SortIntSeq :=
  match stringValueCodes? value with
  | some codes => codes
  | none => emptyCodeSequence

def isUpperCode (code : SortInt) : SortBool :=
  decide (65 ≤ code ∧ code ≤ 90)

def isLowerCode (code : SortInt) : SortBool :=
  decide (97 ≤ code ∧ code ≤ 122)

def hasUpperCode : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isUpperCode code || hasUpperCode rest

def hasLowerCode : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isLowerCode code || hasLowerCode rest

def isAlphaCode (code : SortInt) : SortBool :=
  isUpperCode code || isLowerCode code

def isDigitCode (code : SortInt) : SortBool :=
  decide (48 ≤ code ∧ code ≤ 57)

def isWhitespaceCode (code : SortInt) : SortBool :=
  code == 32 || code == 9 || code == 10 || code == 13

def allAlphaCodes : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isAlphaCode code && allAlphaCodes rest

def allDigitCodes : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      isDigitCode code && allDigitCodes rest

def intSeqAppend : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», right => right
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, right =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head
        (intSeqAppend tail right)

def intSeqReverseAux : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulator => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail,
      accumulator =>
      intSeqReverseAux tail
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head accumulator)

def intSeqReverse (codes : SortIntSeq) : SortIntSeq :=
  intSeqReverseAux codes emptyCodeSequence

def intSeqToList : SortIntSeq → List SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      head :: intSeqToList tail

def listToIntSeq : List SortInt → SortIntSeq
  | [] => emptyCodeSequence
  | head :: tail =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head
        (listToIntSeq tail)

def lowerCode (code : SortInt) : SortInt :=
  if isUpperCode code then code + 32 else code

def upperCode (code : SortInt) : SortInt :=
  if isLowerCode code then code - 32 else code

def swapCode (code : SortInt) : SortInt :=
  if isUpperCode code then code + 32
  else if isLowerCode code then code - 32
  else code

def mapLowerCodes : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» (lowerCode head)
        (mapLowerCodes tail)

def mapUpperCodes : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» (upperCode head)
        (mapUpperCodes tail)

def mapSwapCodes : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» (swapCode head)
        (mapSwapCodes tail)

def trimWhitespace : SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      if isWhitespaceCode head then trimWhitespace tail
      else SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail

def stripCodes (codes : SortIntSeq) : SortIntSeq :=
  intSeqReverse (trimWhitespace (intSeqReverse (trimWhitespace codes)))

def startsWithCodes : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      a == b && startsWithCodes as bs

def replaceCode : SortIntSeq → SortInt → SortInt → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _, _ => emptyCodeSequence
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, oldCode,
      newCode =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (if head == oldCode then newCode else head)
        (replaceCode tail oldCode newCode)

def listPrefix : List SortInt → List SortInt → SortBool
  | [], _ => true
  | _ :: _, [] => false
  | a :: as, b :: bs => a == b && listPrefix as bs

def countSubFuel : Nat → List SortInt → List SortInt → Nat
  | 0, _, _ => 0
  | _ + 1, [], _ => 0
  | fuel + 1, source@(_ :: rest), pattern =>
      if pattern.isEmpty then
        countSubFuel fuel rest pattern
      else if listPrefix pattern source then
        1 + countSubFuel fuel (source.drop pattern.length) pattern
      else
        countSubFuel fuel rest pattern

def countSubCodes (source pattern : SortIntSeq) : SortInt :=
  let sourceList := intSeqToList source
  Int.ofNat (countSubFuel sourceList.length sourceList (intSeqToList pattern))

/- `joinCodes` has equations only for empty sequences and string heads.  Its
   one fixed value on a non-string-head state is the empty code sequence;
   recursive string-head equations continue to compose around that value. -/
def joinStringValues (separator : SortIntSeq) : SortValSeq → SortIntSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => emptyCodeSequence
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
      totalStringCodes value
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      match stringValueCodes? value with
      | some headCodes =>
          intSeqAppend headCodes
            (intSeqAppend separator (joinStringValues separator rest))
      | none => emptyCodeSequence

def valuesStructurallyEqual (left right : SortVal) : SortBool :=
  match stringValueCodes? left, stringValueCodes? right with
  | some leftCodes, some rightCodes => leftCodes == rightCodes
  | _, _ => left == right

def countValueOccurrences : SortValSeq → SortVal → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, sought =>
      (if valuesStructurallyEqual head sought then 1 else 0) +
        countValueOccurrences tail sought

def indexOfValueFrom : SortValSeq → SortVal → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => none
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, sought, index =>
      if valuesStructurallyEqual head sought then some index
      else indexOfValueFrom tail sought (index + 1)

/- Executable operational meaning of the frozen md5hexCodes trust symbol. -/
structure Md5State where
  a : UInt32
  b : UInt32
  c : UInt32
  d : UInt32

def nthD {α : Type} : List α → Nat → α → α
  | [], _, fallback => fallback
  | head :: _, 0, _ => head
  | _ :: tail, index + 1, fallback => nthD tail index fallback

def md5Shift (index : Nat) : UInt32 :=
  UInt32.ofNat <| nthD
    [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
     5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
     4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
     6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
    index 0

def md5Constant (index : Nat) : UInt32 :=
  nthD
    [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
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
     0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
    index 0

def rotateLeft32 (word amount : UInt32) : UInt32 :=
  (word <<< amount) ||| (word >>> (32 - amount))

def md5Word (block : List Nat) (word : Nat) : UInt32 :=
  let position := word * 4
  UInt32.ofNat (nthD block position 0) |||
    (UInt32.ofNat (nthD block (position + 1) 0) <<< 8) |||
    (UInt32.ofNat (nthD block (position + 2) 0) <<< 16) |||
    (UInt32.ofNat (nthD block (position + 3) 0) <<< 24)

def md5Rounds (block : List Nat) :
    Nat → Nat → UInt32 → UInt32 → UInt32 → UInt32 → Md5State
  | 0, _, a, b, c, d => ⟨a, b, c, d⟩
  | fuel + 1, index, a, b, c, d =>
      let fg : UInt32 × Nat :=
        if index < 16 then
          ((b &&& c) ||| (~~~b &&& d), index)
        else if index < 32 then
          ((d &&& b) ||| (~~~d &&& c), (5 * index + 1) % 16)
        else if index < 48 then
          (b ^^^ c ^^^ d, (3 * index + 5) % 16)
        else
          (c ^^^ (b ||| ~~~d), (7 * index) % 16)
      let step := a + fg.1 + md5Constant index + md5Word block fg.2
      md5Rounds block fuel (index + 1) d
        (b + rotateLeft32 step (md5Shift index)) b c

def md5Block (state : Md5State) (block : List Nat) : Md5State :=
  let output := md5Rounds block 64 0 state.a state.b state.c state.d
  ⟨state.a + output.a, state.b + output.b,
   state.c + output.c, state.d + output.d⟩

def md5Blocks : Nat → List Nat → Md5State → Md5State
  | 0, _, state => state
  | fuel + 1, bytes, state =>
      md5Blocks fuel (bytes.drop 64) (md5Block state (bytes.take 64))

def natByte (number shift : Nat) : Nat :=
  (number >>> shift) % 256

def paddedMd5Bytes (bytes : List Nat) : List Nat :=
  let withMarker := bytes ++ [128]
  let zeroCount := (56 + 64 - (withMarker.length % 64)) % 64
  let bitLength := (bytes.length * 8) % (2 ^ 64)
  withMarker ++ List.replicate zeroCount 0 ++
    [natByte bitLength 0, natByte bitLength 8, natByte bitLength 16,
     natByte bitLength 24, natByte bitLength 32, natByte bitLength 40,
     natByte bitLength 48, natByte bitLength 56]

def uint32Bytes (word : UInt32) : List Nat :=
  let number := word.toNat
  [natByte number 0, natByte number 8, natByte number 16, natByte number 24]

def hexDigitCode (digit : Nat) : SortInt :=
  Int.ofNat (if digit < 10 then 48 + digit else 87 + digit)

def byteHexCodes (byte : Nat) : List SortInt :=
  [hexDigitCode (byte / 16), hexDigitCode (byte % 16)]

def md5HexCodeSequence (codes : SortIntSeq) : SortIntSeq :=
  let bytes := (intSeqToList codes).map (fun code => Int.toNat (code % 256))
  let padded := paddedMd5Bytes bytes
  let initial : Md5State := ⟨0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476⟩
  let finalState := md5Blocks (padded.length / 64) padded initial
  let digest := uint32Bytes finalState.a ++ uint32Bytes finalState.b ++
    uint32Bytes finalState.c ++ uint32Bytes finalState.d
  listToIntSeq (digest.flatMap byteHexCodes)

def oneArgument : SortVals → Option SortVal
  | SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some value
  | _ => none

def twoArguments : SortVals → Option (SortVal × SortVal)
  | SortVals.«_,__MPY-CORE_Vals_Val_Vals» first
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals» second
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      some (first, second)
  | _ => none

def noArguments : SortVals → SortBool
  | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => true
  | _ => false

def fixedUndefinedMethodValue : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

/- The complete frozen string-receiver portion of `applyMethod`.  Method and
   arity checks reproduce the left-hand sides of methods.k.  A single `noneV`
   totalization is used exactly where none of those equations applies. -/
def dispatchStringMethod
    (codes : SortIntSeq) (method : SortString) (arguments : SortVals) : SortVal :=
  if method == "isupper" && noArguments arguments then
    SortVal.inj_SortBool (hasUpperCode codes && !hasLowerCode codes)
  else if method == "islower" && noArguments arguments then
    SortVal.inj_SortBool (hasLowerCode codes && !hasUpperCode codes)
  else if method == "isalpha" && noArguments arguments then
    SortVal.inj_SortBool
      (!(intSeqToList codes).isEmpty && allAlphaCodes codes)
  else if method == "isdigit" && noArguments arguments then
    SortVal.inj_SortBool
      (!(intSeqToList codes).isEmpty && allDigitCodes codes)
  else if method == "lower" && noArguments arguments then
    makeStringValue (mapLowerCodes codes)
  else if method == "upper" && noArguments arguments then
    makeStringValue (mapUpperCodes codes)
  else if method == "swapcase" && noArguments arguments then
    makeStringValue (mapSwapCodes codes)
  else if method == "join" then
    match oneArgument arguments with
    | some (SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values)) =>
        makeStringValue (joinStringValues codes values)
    | _ => fixedUndefinedMethodValue
  else if method == "count" then
    match oneArgument arguments with
    | some pattern =>
        match stringValueCodes? pattern with
        | some patternCodes => SortVal.inj_SortInt (countSubCodes codes patternCodes)
        | none => fixedUndefinedMethodValue
    | none => fixedUndefinedMethodValue
  else if method == "strip" && noArguments arguments then
    makeStringValue (stripCodes codes)
  else if method == "encode" then
    match oneArgument arguments with
    | some encoding =>
        match stringValueCodes? encoding with
        | some _ => makeStringValue codes
        | none => fixedUndefinedMethodValue
    | none => fixedUndefinedMethodValue
  else if method == "startswith" then
    match oneArgument arguments with
    | some prefixValue =>
        match stringValueCodes? prefixValue with
        | some prefixCodes => SortVal.inj_SortBool (startsWithCodes prefixCodes codes)
        | none => fixedUndefinedMethodValue
    | none => fixedUndefinedMethodValue
  else if method == "replace" then
    match twoArguments arguments with
    | some (oldValue, newValue) =>
        match stringValueCodes? oldValue, stringValueCodes? newValue with
        | some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» oldCode
              SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»),
            some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» newCode
              SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») =>
            makeStringValue (replaceCode codes oldCode newCode)
        | _, _ => fixedUndefinedMethodValue
    | none => fixedUndefinedMethodValue
  else fixedUndefinedMethodValue

/- Complete `applyMethod` table relative to Base's value universe: all frozen
   string methods, list.count, tuple.index, and md5Obj.hexdigest.  The initial
   string projection also gives the raw transitive-injection representation
   the same meaning as the canonical direct injection. -/
def dispatchRepresentableMethod
    (receiver : SortVal) (method : SortString) (arguments : SortVals) : SortVal :=
  match stringValueCodes? receiver with
  | some codes => dispatchStringMethod codes method arguments
  | none =>
      match receiver with
      | SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
          if method == "count" then
            match oneArgument arguments with
            | some argument =>
                SortVal.inj_SortInt (countValueOccurrences values argument)
            | none => fixedUndefinedMethodValue
          else fixedUndefinedMethodValue
      | SortVal.inj_SortIterable
          (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
          if method == "index" then
            match oneArgument arguments with
            | some argument =>
                match indexOfValueFrom values argument 0 with
                | some index => SortVal.inj_SortInt index
                /- `idxOfVS` has no empty-sequence equation.  Zero is its one
                   fixed totalized Int value on every such terminal state. -/
                | none => SortVal.inj_SortInt 0
            | none => fixedUndefinedMethodValue
          else fixedUndefinedMethodValue
      | SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» inputCodes =>
          if method == "hexdigest" && noArguments arguments then
            makeStringValue (md5HexCodeSequence inputCodes)
          else fixedUndefinedMethodValue
      | _ => fixedUndefinedMethodValue

end Operational
