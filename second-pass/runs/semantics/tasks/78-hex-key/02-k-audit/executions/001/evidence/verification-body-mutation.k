requires "reference-semantics/semantics.k"

module HEX-KEY-VERIFICATION-BODY-MUTATION
  imports MPY

  // Fresh material body mutation: a matching digit increments by 2, not 1.
  syntax Stmts ::= "hexKeyLoopBody" [macro]
  rule hexKeyLoopBody
    => If(Compare(Name("digit"), CmpOp("in", Str("2357BD"))),
          AugAssign(Name("count"), "+", Int(2)),
          .Stmts)

  syntax Stmts ::= "hexKeyBody" [macro]
  rule hexKeyBody
    => Assign(Name("count"), Int(0))
       Assign(Name("digit"), Str(""))
       For(Name("digit"), Name("num"), hexKeyLoopBody)
       Return(Name("count"))

  syntax Bool ::= isPrimeHexCode(Int) [function, total]
  rule isPrimeHexCode(C:Int)
    => strContains(iCons(C, .IntSeq),
                   iCons(50, iCons(51, iCons(53, iCons(55,
                   iCons(66, iCons(68, .IntSeq)))))))

  syntax Int ::= primeHexBit(Int) [function, total]
  rule primeHexBit(C:Int)
    => #if isPrimeHexCode(C) #then 1 #else 0 #fi

  syntax Int ::= hexCount(IntSeq) [function, total]
  rule hexCount(.IntSeq) => 0
  rule hexCount(iCons(C:Int, REST:IntSeq))
    => primeHexBit(C) +Int hexCount(REST)

  syntax Val ::= finalDigit(IntSeq, Val) [function, total]
  rule finalDigit(.IntSeq, OLD:Val) => OLD
  rule finalDigit(iCons(C:Int, REST:IntSeq), _OLD:Val)
    => finalDigit(REST, str(iCons(C, .IntSeq)))
endmodule
