requires "verification-body-mutated.k"

module MAD-SPEC-BODY-MUTATED
  imports MAD-VERIFICATION-BODY-MUTATED

  // The destination pins the mutated closure body, but deliberately retains
  // the original result formula whose deviation fold starts from 0.0.
  claim
    <k> #runMad(list(VS:ValSeq))
        => divFloatIntV(
             absDeviationFold(
               VS,
               divFloatIntV(sumFloatSeq(VS), vsLen(VS)),
               0.0),
             vsLen(VS)) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map
               => "mean_absolute_deviation" |->
                    closureVal("numbers", .ParamNames,
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
