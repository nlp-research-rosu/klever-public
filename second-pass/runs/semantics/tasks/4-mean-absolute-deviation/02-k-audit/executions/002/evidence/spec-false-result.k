requires "verification.k"

module MAD-SPEC-FALSE-RESULT
  imports MAD-VERIFICATION

  // Fresh non-vacuity mutation: demand result - result instead of result.
  // For the satisfying witness [1.0, 2.0, 3.0, 4.0], the true result is 1.0
  // and this mutation denotes 0.0 under the trusted concrete float primitives.
  claim
    <k> #runMad(list(VS:ValSeq))
        => subF(
             divFloatIntV(
               absDeviationFold(
                 VS,
                 divFloatIntV(sumFloatSeq(VS), vsLen(VS)),
                 0.0),
               vsLen(VS)),
             divFloatIntV(
               absDeviationFold(
                 VS,
                 divFloatIntV(sumFloatSeq(VS), vsLen(VS)),
                 0.0),
               vsLen(VS))) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map
               => "mean_absolute_deviation" |->
                    closureVal("numbers", .ParamNames,
                      Expr(Str("Return the mean absolute deviation of a non-empty list of numbers."))
                      Assign(Name("mean"),
                        BinOp("/",
                          Call(Name("sum"), Name("numbers")),
                          Call(Name("len"), Name("numbers"))))
                      Assign(Name("total_deviation"), Float(0.0))
                      For(Name("number"), Name("numbers"),
                        AugAssign(Name("total_deviation"), "+",
                          Call(Name("abs"),
                            BinOp("-", Name("number"), Name("mean")))))
                      Return(BinOp("/", Name("total_deviation"),
                        Call(Name("len"), Name("numbers")))),
                      0), parent(-1))
             -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires nonEmptyFloats(VS)
endmodule
