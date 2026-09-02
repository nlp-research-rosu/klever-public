requires "reference-semantics/semantics.k"

module CONNECTION
  imports MPY

  syntax IntSeq ::= "auditVowelCodes" [macro]
  rule auditVowelCodes
    => iCons(97, iCons(101, iCons(105, iCons(111, iCons(117,
       iCons(65, iCons(69, iCons(73, iCons(79, iCons(85, .IntSeq))))))))))

  syntax Bool ::= auditIsVowelCode(Int) [function, total]
  rule auditIsVowelCode(C:Int)
    => C ==Int 65  orBool C ==Int 69  orBool C ==Int 73
       orBool C ==Int 79  orBool C ==Int 85  orBool C ==Int 97
       orBool C ==Int 101 orBool C ==Int 105 orBool C ==Int 111
       orBool C ==Int 117

  syntax KItem ::= auditCheck(Int) [macro]
  rule auditCheck(C:Int)
    => If(
         Compare(
           str(iCons(C, .IntSeq)),
           CmpOp("in", Str("aeiouAEIOU"))),
         Assign(Name("$audit"), Int(1)),
         Assign(Name("$audit"), Int(0)))
endmodule
