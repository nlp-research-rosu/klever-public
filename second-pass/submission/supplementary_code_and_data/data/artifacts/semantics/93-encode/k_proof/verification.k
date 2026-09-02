requires "reference-semantics/semantics.k"

module ENCODE-VERIFICATION
  imports MPY

  // Exact loop body emitted by solution.mpy, named once so both proof phases
  // are checked against the same AST.
  syntax Stmts ::= "encodeLoopBody" [macro]
  rule encodeLoopBody
    =>
      Assign(
        Name("char"),
        Call(Attribute(Name("char"), "swapcase"), .Exprs))
      Assign(
        Name("code"),
        Call(Name("ord"), (Name("char"), .Exprs)))
      If(
        BoolOp(
          "or",
          (Compare(Name("code"), CmpOp("==", Int(97))),
           Compare(Name("code"), CmpOp("==", Int(101))),
           Compare(Name("code"), CmpOp("==", Int(105))),
           Compare(Name("code"), CmpOp("==", Int(111))),
           Compare(Name("code"), CmpOp("==", Int(117))),
           Compare(Name("code"), CmpOp("==", Int(65))),
           Compare(Name("code"), CmpOp("==", Int(69))),
           Compare(Name("code"), CmpOp("==", Int(73))),
           Compare(Name("code"), CmpOp("==", Int(79))),
           Compare(Name("code"), CmpOp("==", Int(85))),
           .Exprs)),
        AugAssign(
          Name("result"),
          "+",
          Call(
            Name("chr"),
            (BinOp(
              "+",
              Name("code"),
              Int(2)),
             .Exprs))),
        AugAssign(
          Name("result"),
          "+",
          Name("char")))
      .Stmts

  syntax Stmts ::= "encodeFunctionBody" [macro]
  rule encodeFunctionBody
    =>
      Assign(Name("result"), Str(""))
      Assign(Name("char"), Str(""))
      Assign(Name("code"), Int(0))
      For(Name("char"), Name("message"), encodeLoopBody)
      Return(Name("result"))
      .Stmts

  // Mathematical contract: first swap each ASCII letter's case, then advance
  // every (now case-swapped) vowel by two code points.
  syntax Bool ::= isVowelCode(Int) [function, total]
  rule isVowelCode(C:Int)
    => C ==Int 65  orBool C ==Int 69  orBool C ==Int 73
       orBool C ==Int 79  orBool C ==Int 85
       orBool C ==Int 97  orBool C ==Int 101 orBool C ==Int 105
       orBool C ==Int 111 orBool C ==Int 117

  syntax Int ::= encodeCode(Int) [function, total]
  rule encodeCode(C:Int) => swapC(C) +Int 2
    requires isVowelCode(swapC(C))
  rule encodeCode(C:Int) => swapC(C)
    requires notBool isVowelCode(swapC(C))

  // Accumulator form mirrors the implementation's left-to-right loop.  It is
  // also the induction measure used by the loop claim in spec.k.
  syntax IntSeq ::= encodeAcc(IntSeq, IntSeq) [function, total]
  rule encodeAcc(.IntSeq, ACC:IntSeq) => ACC
  rule encodeAcc(iCons(C:Int, REST:IntSeq), ACC:IntSeq)
    => encodeAcc(
         REST,
         seqConcat(ACC, iCons(encodeCode(C), .IntSeq)))

  syntax IntSeq ::= encodeCodes(IntSeq) [function, total]
  rule encodeCodes(INPUT:IntSeq) => encodeAcc(INPUT, .IntSeq)
endmodule
