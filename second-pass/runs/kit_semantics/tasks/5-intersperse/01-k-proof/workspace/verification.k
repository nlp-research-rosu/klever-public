requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact statement list translated from the body of solution.py.
  syntax Stmts ::= "INTERSPERSE-BODY" [macro]
  rule INTERSPERSE-BODY
    => If(Name("result"),
          Expr(Call(Attribute(Name("result"), "append"),
                    Name("delimeter"))) .Stmts,
          .Stmts)
       Expr(Call(Attribute(Name("result"), "append"), Name("number")))
       .Stmts

  // Mathematical fold: ACC is the output already produced and REST is the
  // unprocessed input.  Every recursive equation removes one item from REST.
  syntax ValSeq ::= intersperseAcc(ValSeq, ValSeq, Val) [function, total]

  rule intersperseAcc(ACC:ValSeq, .ValSeq, _:Val) => ACC

  rule intersperseAcc(.ValSeq, vCons(X:Val, REST:ValSeq), D:Val)
    => intersperseAcc(vCons(X, .ValSeq), REST, D)

  rule intersperseAcc(vCons(A:Val, AS:ValSeq),
                      vCons(X:Val, REST:ValSeq), D:Val)
    => intersperseAcc(
         valSeqConcat(
           valSeqConcat(vCons(A, AS), vCons(D, .ValSeq)),
           vCons(X, .ValSeq)),
         REST,
         D)
endmodule
