requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // This equation is the exact constructor tree emitted in solution.mpy
  // (SHA-256 8b1459d8f7e47fe17ad740613f5b14392282cdd23d81b304779d1994f6c83e5b).
  syntax Pgm ::= "solutionProgram" [function, total, symbol(solutionProgram)]
  rule solutionProgram =>
    Module(
      FuncDef("compare", Params("game", "guess"),
        If(Compare(Name("game"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(.Exprs)),
          .Stmts)
        Assign(
          Name("difference"),
          BinOp("-",
            Subscript(Name("game"), Int(0)),
            Subscript(Name("game"), Int(0))))
        If(Compare(Name("difference"), CmpOp("<", Int(0))),
          Assign(Name("difference"), UnaryOp("-", Name("difference"))),
          .Stmts)
        Return(
          BinOp("+",
            ListExpr(Name("difference")),
            Call(Name("compare"),
              Subscript(Name("game"), Slice(Int(1), NoBound, NoBound)),
              Subscript(Name("guess"), Slice(Int(1), NoBound, NoBound)))))))

  // Independent mathematical contract.  On the prompt's domain, every value
  // is VInt and the lists have equal length.  The total definitions outside
  // that domain merely keep symbolic execution defined.
  syntax Values ::= expected(Values, Values) [function, total, symbol(expected)]
  rule expected(GS, _) => VNil
    requires isEmptyValues(GS)
  rule expected(GS, US)
    => VCons(
         VInt(0 -Int (valueAsInt(headValue(GS))
                      -Int valueAsInt(headValue(US)))),
         expected(tailValues(GS), tailValues(US)))
    requires notBool isEmptyValues(GS)
     andBool (valueAsInt(headValue(GS))
              -Int valueAsInt(headValue(US)) <Int 0)
  rule expected(GS, US)
    => VCons(
         VInt(valueAsInt(headValue(GS))
              -Int valueAsInt(headValue(US))),
         expected(tailValues(GS), tailValues(US)))
    requires notBool isEmptyValues(GS)
     andBool notBool (valueAsInt(headValue(GS))
                      -Int valueAsInt(headValue(US)) <Int 0)
endmodule
