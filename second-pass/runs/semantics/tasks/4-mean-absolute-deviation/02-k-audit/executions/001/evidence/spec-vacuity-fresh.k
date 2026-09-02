requires "verification.k"

module MAD-SPEC-VACUITY-FRESH
  imports MAD-VERIFICATION

  // For every non-empty finite Float sequence, execution returns exactly
  // average(abs(x - average(numbers))).  The floating-point primitives and
  // the two finite folds remain structural symbols, as required by MPY-FLOAT.
  claim
    // Deliberately false: e.g. [1.0, 2.0, 3.0, 4.0] satisfies the
    // precondition and returns 1.0, not 0.0.
    <k> #runMad(list(VS:ValSeq)) => 0.0 </k>
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
