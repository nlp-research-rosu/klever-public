requires "reference-semantics/semantics.k"

module SUM-PRODUCT-VERIFICATION
  imports MPY

  // These macros are a direct transcription of solution.mpy.  Keeping the
  // loop body separate makes the inductive claim in spec.k readable.
  syntax Stmts ::= "sumProductLoopBody" [macro]
  rule sumProductLoopBody
    => AugAssign(Name("total"), "+", Name("number"))
       AugAssign(Name("product"), "*", Name("number"))
       .Stmts

  syntax Stmts ::= "sumProductBody" [macro]
  rule sumProductBody
    => Expr(Str("Return the sum and product of all integers in numbers."))
       Assign(Name("total"), Int(0))
       Assign(Name("product"), Int(1))
       Assign(Name("number"), Int(0))
       For(Name("number"), Name("numbers"), sumProductLoopBody)
       Return(TupleExpr(Name("total"), Name("product")))
       .Stmts

  syntax Module ::= "sumProductModule" [macro]
  rule sumProductModule
    => Module(
         ImportFrom("typing", "List", "Tuple")
         FuncDef("sum_product", Params("numbers"), sumProductBody)
         .Stmts)

  // A symbolic generator for arbitrary finite sequences of Int values.  The
  // two iterator rules are the constructor-specialized image of MPY-LIST's
  // .ValSeq/vCons equations; they expose exactly two induction cases without
  // adding any behavior to the Python program.
  syntax ValSeq ::= intVals(IntSeq)
  rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>
  rule <k> #iterNext(list(intVals(iCons(I:Int, IS:IntSeq))))
        => #iterYield(I, list(intVals(IS))) ... </k>

  // Mathematical left folds matching the two accumulator updates.
  syntax Int ::= intSeqSumFrom(Int, IntSeq) [function, total]
  rule intSeqSumFrom(ACC:Int, .IntSeq) => ACC
  rule intSeqSumFrom(ACC:Int, iCons(I:Int, IS:IntSeq))
    => intSeqSumFrom(ACC +Int I, IS)

  syntax Int ::= intSeqProductFrom(Int, IntSeq) [function, total]
  rule intSeqProductFrom(ACC:Int, .IntSeq) => ACC
  rule intSeqProductFrom(ACC:Int, iCons(I:Int, IS:IntSeq))
    => intSeqProductFrom(ACC *Int I, IS)

  syntax Int ::= lastInt(IntSeq, Int) [function, total]
  rule lastInt(.IntSeq, CURRENT:Int) => CURRENT
  rule lastInt(iCons(I:Int, IS:IntSeq), _:Int) => lastInt(IS, I)
endmodule

// This module promotes the separately proved loop claim to a rewrite lemma
// for the end-to-end proof.  prove.sh first closes the same statement as a
// claim against SUM-PRODUCT-VERIFICATION, then compiles this staging module.
module SUM-PRODUCT-LEMMA
  imports SUM-PRODUCT-VERIFICATION

  rule
    <k>
      #loop(list(intVals(IS)), Name("number"), sumProductLoopBody)
      ~> CONT:K
      => CONT
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(GLOBAL:Map, parent(-1))
      1 |-> scope(
        "numbers" |-> INPUT:Val
        "total" |-> SUM:Int
        "product" |-> PRODUCT:Int
        "number" |-> CURRENT:Int,
        parent(0))
      REST:Map
      =>
      0 |-> scope(GLOBAL, parent(-1))
      1 |-> scope(
        "numbers" |-> INPUT
        "total" |-> intSeqSumFrom(SUM, IS)
        "product" |-> intSeqProductFrom(PRODUCT, IS)
        "number" |-> lastInt(IS, CURRENT),
        parent(0))
      REST
    </scopes>
    [priority(40)]
endmodule
