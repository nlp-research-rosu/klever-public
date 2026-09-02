requires "reference-semantics/semantics.k"

module MAD-VERIFICATION-BODY-MUTATED
  imports MPY

  // Reviewer mutation of the actual executed AST: accumulator starts at 1.0.
  syntax Module ::= "madSolution" [function, total]
  rule madSolution =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("mean_absolute_deviation", Params("numbers"),
        Expr(Str("Return the mean absolute deviation of a non-empty list of numbers."))
        Assign(Name("mean"),
          BinOp("/",
            Call(Name("sum"), Name("numbers")),
            Call(Name("len"), Name("numbers"))))
        Assign(Name("total_deviation"), Float(1.0))
        For(Name("number"), Name("numbers"),
          AugAssign(Name("total_deviation"), "+",
            Call(Name("abs"),
              BinOp("-", Name("number"), Name("mean")))))
        Return(BinOp("/", Name("total_deviation"),
          Call(Name("len"), Name("numbers"))))))

  syntax KItem ::= #runMad(Val)
  rule <k> #runMad(V:Val) => #loadAll(madSolution)
                              ~> Call(Name("mean_absolute_deviation"), V) ... </k>

  syntax Bool ::= allFloats(ValSeq) [function, total]
                | nonEmptyFloats(ValSeq) [function, total]
  rule allFloats(.ValSeq) => true
  rule allFloats(vCons(_:Float, R:ValSeq)) => allFloats(R)
  rule allFloats(vCons(_:Val, _:ValSeq)) => false [owise]
  rule nonEmptyFloats(.ValSeq) => false
  rule nonEmptyFloats(vCons(_:Float, R:ValSeq)) => allFloats(R)
  rule nonEmptyFloats(vCons(_:Val, _:ValSeq)) => false [owise]

  syntax Float ::= sumFloatSeq(ValSeq) [function, symbol(sumFloatSeq)]
                 | sumFloatTail(ValSeq, Float) [function, symbol(sumFloatTail)]
                 | absDeviationFold(ValSeq, Float, Float)
                   [function, symbol(absDeviationFold)]
  rule sumFloatSeq(.ValSeq) => intToF(0)
  rule sumFloatSeq(vCons(F:Float, R:ValSeq))
    => sumFloatTail(R, addF(intToF(0), F))
  rule sumFloatTail(.ValSeq, ACC:Float) => ACC
  rule sumFloatTail(vCons(F:Float, R:ValSeq), ACC:Float)
    => sumFloatTail(R, addF(ACC, F))
  rule absDeviationFold(.ValSeq, _:Float, ACC:Float) => ACC
  rule absDeviationFold(vCons(F:Float, R:ValSeq), MEAN:Float, ACC:Float)
    => absDeviationFold(R, MEAN, addF(ACC, absF(subF(F, MEAN))))

  rule <k> #applyK(toCall(builtinV("sum")),
                   (list(VS:ValSeq), .Vals))
        => sumFloatSeq(VS) ... </k>
       requires nonEmptyFloats(VS)
       [priority(40)]

  rule <k> #loop(list(VS:ValSeq), Name("number"),
                 AugAssign(Name("total_deviation"), "+",
                   Call(Name("abs"),
                     BinOp("-", Name("number"), Name("mean")))))
        => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map
          => M [ "total_deviation" <-
                 absDeviationFold(VS,
                   {M["mean"]}:>Float,
                   {M["total_deviation"]}:>Float) ], P:Parent) ... </scopes>
       requires nonEmptyFloats(VS)
        andBool "mean" in_keys(M)
        andBool "total_deviation" in_keys(M)
        andBool isFloat({M["mean"]}:>Val)
        andBool isFloat({M["total_deviation"]}:>Val)
       [priority(40)]
endmodule
