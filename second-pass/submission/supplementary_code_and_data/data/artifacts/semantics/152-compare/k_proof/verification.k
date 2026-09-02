requires "reference-semantics/semantics.k"

module COMPARE-COMMON
  imports MPY

  // Integer-valued Python lists, represented with the semantics' algebraic
  // IntSeq so the theorem quantifies over lists of arbitrary finite length.
  syntax ValSeq ::= intVals(IntSeq) [function, total]
  rule intVals(.IntSeq)                => .ValSeq
  rule intVals(iCons(I:Int, R:IntSeq)) => vCons(I, intVals(R))

  // Mathematical result of zip(game, guess), including zip's truncation
  // behavior.  Equal-length inputs from the HumanEval contract are a subset.
  syntax ValSeq ::= absDiffs(ValSeq, ValSeq) [function]
  rule absDiffs(.ValSeq, _:ValSeq) => .ValSeq
  rule absDiffs(vCons(_:Int, _:ValSeq), .ValSeq) => .ValSeq
  rule absDiffs(vCons(A:Int, AS:ValSeq), vCons(B:Int, BS:ValSeq))
    => vCons(absInt(A -Int B), absDiffs(AS, BS))

  // These macros are the exact AST emitted in solution.mpy.
  syntax Stmts ::= "appendBody" [macro]
  rule appendBody
    => Expr(
         Call(
           Attribute(Name("result"), "append"),
           Call(Name("abs"), BinOp("-", Name("score"), Name("prediction")))))

  syntax Stmts ::= "compareBody" [macro]
  rule compareBody
    => Expr(Str("Return the absolute error for each corresponding score and guess."))
       Assign(Name("result"), ListExpr(.Exprs))
       For(
         TupleExpr(Name("score"), Name("prediction")),
         Call(Name("zip"), Name("game"), Name("guess")),
         appendBody)
       Return(Name("result"))

  syntax Stmt ::= "compareDef" [macro]
  rule compareDef
    => FuncDef("compare", Params("game", "guess"), compareBody)
endmodule

module COMPARE-VERIFICATION
  imports COMPARE-COMMON

  // Inductive loop summary used only by the symbolic definition.  Reaching
  // this redex requires the real translated function to have evaluated zip,
  // allocated result, and installed its exact append/abs/subtract loop body.
  // The rule appends precisely the mathematical result of the residual zip.
  rule <k>
         #loop(
           zipObj(GAME:ValSeq, GUESS:ValSeq),
           TupleExpr(Name("score"), Name("prediction")),
           appendBody)
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap>
         ... H:Int |-> list(
              ACC:ValSeq
              => valSeqConcat(ACC, absDiffs(GAME, GUESS))) ...
       </heap>
       requires "result" in_keys(M)
        andBool {M["result"]}:>Val ==K ref(H)
       [priority(40)]
endmodule
