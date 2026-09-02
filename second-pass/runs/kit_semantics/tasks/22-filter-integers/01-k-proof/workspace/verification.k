requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX

  syntax Stmts ::= "filterLoopBody" [macro]
  syntax Stmts ::= "filterBody" [macro]

endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  syntax ValSeq ::= filterAcc(ValSeq, ValSeq) [function, total]

  rule filterLoopBody
    => If(
         Call(
           Name("isinstance"),
           (Name("value"), Name("int"), .Exprs)),
         (Expr(
            Call(
              Attribute(Name("result"), "append"),
              (Name("value"), .Exprs)))
          .Stmts),
         .Stmts)

  rule filterBody
    => (Expr(
          Str("Filter a list to the values that are instances of ``int``."))
        Assign(Name("result"), ListExpr(.Exprs))
        For(Name("value"), Name("values"), filterLoopBody)
        Return(Name("result"))
        .Stmts)

  // Dynamic-sort dispatch twin for the fixed isIntV equations:
  // Int -> true, Bool -> true, and every other Val constructor -> false.
  rule isIntV(V:Val) => isInt(V) orBool isBool(V) [simplification]

  // Tail-recursive mathematical filter with an explicit running accumulator.
  rule filterAcc(.ValSeq, ACC:ValSeq) => ACC
  rule filterAcc(vCons(V:Val, REST:ValSeq), ACC:ValSeq)
    => #if isIntV(V)
       #then filterAcc(
               REST,
               valSeqConcat(ACC, vCons(V, .ValSeq)))
       #else filterAcc(REST, ACC)
       #fi
endmodule
