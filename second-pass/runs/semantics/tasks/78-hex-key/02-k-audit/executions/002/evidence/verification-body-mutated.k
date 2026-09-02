requires "reference-semantics/semantics.k"

module HEX-KEY-VERIFICATION-BODY-MUTATED
  imports MPY

  syntax Stmts ::= "hexKeyLoopBodyMutated" [macro]
  rule hexKeyLoopBodyMutated
    => If(Compare(Name("digit"), CmpOp("in", Str("2357BD"))),
          AugAssign(Name("count"), "+", Int(2)),
          .Stmts)

  syntax Stmts ::= "hexKeyBodyMutated" [macro]
  rule hexKeyBodyMutated
    => Assign(Name("count"), Int(0))
       Assign(Name("digit"), Str(""))
       For(Name("digit"), Name("num"), hexKeyLoopBodyMutated)
       Return(Name("count"))

  syntax Bool ::= isPrimeHexCodeMutated(Int) [function, total]
  rule isPrimeHexCodeMutated(C:Int)
    => strContains(iCons(C, .IntSeq),
                   iCons(50, iCons(51, iCons(53, iCons(55,
                   iCons(66, iCons(68, .IntSeq)))))))

  syntax Int ::= primeHexBitMutated(Int) [function, total]
  rule primeHexBitMutated(C:Int)
    => #if isPrimeHexCodeMutated(C) #then 1 #else 0 #fi

  syntax Int ::= hexCountMutated(IntSeq) [function, total]
  rule hexCountMutated(.IntSeq) => 0
  rule hexCountMutated(iCons(C:Int, REST:IntSeq))
    => primeHexBitMutated(C) +Int hexCountMutated(REST)

  syntax Val ::= finalDigitMutated(IntSeq, Val) [function, total]
  rule finalDigitMutated(.IntSeq, OLD:Val) => OLD
  rule finalDigitMutated(iCons(C:Int, REST:IntSeq), _OLD:Val)
    => finalDigitMutated(REST, str(iCons(C, .IntSeq)))
endmodule
