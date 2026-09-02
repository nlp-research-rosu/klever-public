requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact source fragments, used only as parse-time abbreviations in claims.
  syntax Stmts ::= "decodeLoopBody" [macro]
  rule decodeLoopBody
    => Assign(Name("group"), BinOp("+", Name("group"), Name("char")))
       If(
         Compare(Call(Name("len"), Name("group")), CmpOp("==", Int(3))),
         Assign(
           Name("result"),
           BinOp(
             "+",
             Name("result"),
             BinOp(
               "+",
               Subscript(Name("group"), Int(2)),
               Subscript(
                 Name("group"),
                 Slice(NoBound, Int(2), NoBound)))))
         Assign(Name("group"), Str("")),
         .Stmts)

  syntax Stmts ::= "decodeFunctionBody" [macro]
  rule decodeFunctionBody
    => Expr(
         Str(
           "\n    Takes a string encoded by rotating each complete three-character group\n    left once, and restores the original string.\n    "))
       Assign(Name("result"), Str(""))
       Assign(Name("group"), Str(""))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("s"), decodeLoopBody)
       Return(BinOp("+", Name("result"), Name("group")))

  // Exact accumulator after processing every complete three-character group.
  syntax IntSeq ::= decodedResult(IntSeq, IntSeq) [function, total]
  rule decodedResult(ACC:IntSeq, .IntSeq) => ACC
  rule decodedResult(ACC:IntSeq, iCons(_:Int, .IntSeq)) => ACC
  rule decodedResult(
         ACC:IntSeq,
         iCons(_:Int, iCons(_:Int, .IntSeq)))
    => ACC
  rule decodedResult(
         ACC:IntSeq,
         iCons(A:Int, iCons(B:Int, iCons(C:Int, R:IntSeq))))
    => decodedResult(
         seqConcat(
           ACC,
           iCons(C, iCons(A, iCons(B, .IntSeq)))),
         R)

  // The final incomplete group, which the source leaves unchanged.
  syntax IntSeq ::= decodedTail(IntSeq) [function, total]
  rule decodedTail(.IntSeq) => .IntSeq
  rule decodedTail(iCons(A:Int, .IntSeq)) => iCons(A, .IntSeq)
  rule decodedTail(iCons(A:Int, iCons(B:Int, .IntSeq)))
    => iCons(A, iCons(B, .IntSeq))
  rule decodedTail(iCons(_:Int, iCons(_:Int, iCons(_:Int, R:IntSeq))))
    => decodedTail(R)

  syntax IntSeq ::= decodeCodes(IntSeq) [function, total]
  rule decodeCodes(IS:IntSeq)
    => seqConcat(decodedResult(.IntSeq, IS), decodedTail(IS))

  // Exact final value of the loop target. It preserves the old value for an
  // empty iterator and otherwise records the last one-character string.
  syntax Val ::= finalLoopChar(IntSeq, Val) [function, total]
  rule finalLoopChar(.IntSeq, OLD:Val) => OLD
  rule finalLoopChar(iCons(C:Int, R:IntSeq), _:Val)
    => finalLoopChar(R, str(iCons(C, .IntSeq)))

endmodule
