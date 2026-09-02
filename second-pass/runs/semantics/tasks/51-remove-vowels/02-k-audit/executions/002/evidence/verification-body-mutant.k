requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax IntSeq ::= "vowelCodes" [macro]
  rule vowelCodes
    => iCons(97, iCons(101, iCons(105, iCons(111, iCons(117,
       iCons(65, iCons(69, iCons(73, iCons(79, iCons(85, .IntSeq))))))))))

  syntax Bool ::= isVowelCode(Int) [function, total]
  rule isVowelCode(C:Int)
    => C ==Int 65  orBool C ==Int 69  orBool C ==Int 73
       orBool C ==Int 79  orBool C ==Int 85  orBool C ==Int 97
       orBool C ==Int 101 orBool C ==Int 105 orBool C ==Int 111
       orBool C ==Int 117

  // This is a proved-by-definition specialization of MPY-STR's substring
  // search for a one-character needle and this fixed ten-character haystack.
  // It prevents symbolic execution from forking once per haystack position.
  rule strContains(iCons(C:Int, .IntSeq), vowelCodes)
    => isVowelCode(C)
    [priority(40)]

  syntax IntSeq ::= removeVowelCodesAcc(IntSeq, IntSeq) [function, total]
  rule removeVowelCodesAcc(ACC:IntSeq, .IntSeq) => ACC
  rule removeVowelCodesAcc(ACC:IntSeq, iCons(C:Int, REST:IntSeq))
    => removeVowelCodesAcc(ACC, REST)
    requires isVowelCode(C)
  rule removeVowelCodesAcc(ACC:IntSeq, iCons(C:Int, REST:IntSeq))
    => removeVowelCodesAcc(
         seqConcat(ACC, iCons(C, .IntSeq)),
         REST)
    requires notBool isVowelCode(C)

  syntax IntSeq ::= removeVowelCodes(IntSeq) [function, total]
  rule removeVowelCodes(CODES:IntSeq)
    => removeVowelCodesAcc(.IntSeq, CODES)

  syntax Stmts ::= "removeVowelsLoopBody" [macro]
  rule removeVowelsLoopBody
    => If(Compare(Name("char"), CmpOp("not in", Str("aeiouAEIOU"))),
         .Stmts,
         .Stmts)

  syntax Stmts ::= "removeVowelsBody" [macro]
  rule removeVowelsBody
    => Assign(Name("result"), Str(""))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("text"), removeVowelsLoopBody)
       Return(Name("result"))

  syntax Module ::= "removeVowelsProgram" [macro]
  rule removeVowelsProgram
    => Module(
         FuncDef("remove_vowels", Params("text"), removeVowelsBody))
endmodule
