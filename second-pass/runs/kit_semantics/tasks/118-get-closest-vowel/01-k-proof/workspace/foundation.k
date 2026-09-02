requires "reference-semantics/semantics.k"

module FOUNDATION-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE

  syntax Stmts ::= "isVowelBody" [macro]
  syntax Stmts ::= "getClosestBody" [macro]
  syntax Stmts ::= "getClosestLoopBody" [macro]
  syntax Module ::= "getClosestProgram" [macro]

  syntax IntSeq ::= closestCandidate(IntSeq, Int) [function]
  syntax Bool ::= vowelPred(Int) [function, total]
  syntax Bool ::= isVowelCode(Int) [function, total]
  syntax Bool ::= closestQualifies(IntSeq, Int) [function]
  syntax IntSeq ::= closestScan(IntSeq, Int, IntSeq, Bool) [function]
  syntax IntSeq ::= closestVowel(IntSeq) [function, total]
endmodule

module FOUNDATION
  imports FOUNDATION-SYNTAX
  imports MPY

  rule isVowelBody =>
    Assign(Name("result"), Bool(false))
    While(
      Compare(Name("ch"), CmpOp("==", Str("a"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("e"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("i"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("o"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("u"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("A"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("E"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("I"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("O"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    While(
      Compare(Name("ch"), CmpOp("==", Str("U"))),
      Assign(Name("result"), Bool(true))
      Assign(Name("ch"), Str("")))
    Return(Name("result"))

  rule getClosestLoopBody =>
    While(
      BoolOp("and",
        ( UnaryOp("not", Name("found")),
          Call(
            Name("_is_vowel"),
            Subscript(Name("word"), Name("i"))),
          UnaryOp(
            "not",
            Call(
              Name("_is_vowel"),
              Subscript(
                Name("word"),
                BinOp("-", Name("i"), Int(1))))),
          UnaryOp(
            "not",
            Call(
              Name("_is_vowel"),
              Subscript(
                Name("word"),
                BinOp("+", Name("i"), Int(1))))),
          .Exprs)),
      Assign(Name("result"), Subscript(Name("word"), Name("i")))
      Assign(Name("found"), Bool(true)))
    Assign(Name("i"), BinOp("-", Name("i"), Int(1)))

  rule getClosestBody =>
    Assign(Name("result"), Str(""))
    Assign(Name("found"), Bool(false))
    Assign(
      Name("i"),
      BinOp("-", Call(Name("len"), Name("word")), Int(2)))
    While(Compare(Name("i"), CmpOp(">", Int(0))), getClosestLoopBody)
    Return(Name("result"))

  rule getClosestProgram =>
    Module(
      FuncDef(
        "_is_vowel",
        Params("ch"),
        isVowelBody)
      FuncDef(
        "get_closest_vowel",
        Params("word"),
        getClosestBody))

  rule closestCandidate(CS, I)
    => iCons(intSeqAt(CS, I), .IntSeq)

  rule vowelPred(C)
    => C ==Int 97
     orBool C ==Int 101
     orBool C ==Int 105
     orBool C ==Int 111
     orBool C ==Int 117
     orBool C ==Int 65
     orBool C ==Int 69
     orBool C ==Int 73
     orBool C ==Int 79
     orBool C ==Int 85
  rule isVowelCode(C)
    => true
    requires vowelPred(C)
  rule isVowelCode(C)
    => false
    requires notBool vowelPred(C)

  rule closestQualifies(CS, I)
    => isVowelCode(intSeqAt(CS, I))
       andBool notBool isVowelCode(intSeqAt(CS, I -Int 1))
       andBool notBool isVowelCode(intSeqAt(CS, I +Int 1))

  rule closestScan(_CS, I, R, _F) => R
    requires I <=Int 0
    [simplification]
  rule closestScan(CS, I, R, true)
    => closestScan(CS, I -Int 1, R, true)
    requires I >Int 0
    [simplification]
  rule closestScan(CS, I, R, false)
    => closestScan(
         CS,
         I -Int 1,
         closestCandidate(CS, I),
         true)
    requires I >Int 0
     andBool vowelPred(intSeqAt(CS, I))
     andBool notBool vowelPred(intSeqAt(CS, I -Int 1))
     andBool notBool vowelPred(intSeqAt(CS, I +Int 1))
    [simplification]
  rule closestScan(CS, I, R, false)
    => closestScan(CS, I -Int 1, R, false)
    requires I >Int 0
     andBool notBool vowelPred(intSeqAt(CS, I))
    [simplification]
  rule closestScan(CS, I, R, false)
    => closestScan(CS, I -Int 1, R, false)
    requires I >Int 0
     andBool vowelPred(intSeqAt(CS, I))
     andBool vowelPred(intSeqAt(CS, I -Int 1))
    [simplification]
  rule closestScan(CS, I, R, false)
    => closestScan(CS, I -Int 1, R, false)
    requires I >Int 0
     andBool vowelPred(intSeqAt(CS, I))
     andBool notBool vowelPred(intSeqAt(CS, I -Int 1))
     andBool vowelPred(intSeqAt(CS, I +Int 1))
    [simplification]

  rule closestVowel(CS)
    => closestScan(CS, isLen(CS) -Int 2, .IntSeq, false)

  // intSeqAt has rules only for in-bounds constructor cases in the supplied
  // semantics.  This derived definedness lemma exposes the corresponding
  // structural induction fact to the symbolic backend.
  rule #Ceil(intSeqAt(CS, I)) => #Top
    requires 0 <=Int I
     andBool I <Int isLen(CS)
    [simplification]

  rule #Ceil(closestScan(CS, I, R, F)) => #Top
    requires I >=Int 0
     andBool I +Int 1 <Int isLen(CS)
    [simplification]

endmodule
