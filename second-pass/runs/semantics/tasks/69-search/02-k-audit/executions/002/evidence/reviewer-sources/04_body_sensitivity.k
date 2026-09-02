requires "verification.k"

module SEARCH-BODY-SENSITIVITY
  imports SEARCH-VERIFICATION

  // Material body mutation: each equality contributes 2 instead of 1.
  // This changes the closure term actually executed by the claim.
  claim
    <k> Call(Name("search"), list(ALL:IntValSeq), .Exprs)
      => greatestFreq(ALL)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "search" |-> closureVal(
               "lst", .ParamNames,
               Assign(Name("result"), UnaryOp("-", Int(1)))
               For(Name("value"), Name("lst"),
                 Assign(Name("count"), Int(0))
                 For(Name("item"), Name("lst"),
                   If(Compare(Name("item"), CmpOp("==", Name("value"))),
                      AugAssign(Name("count"), "+", Int(2)) .Stmts,
                      .Stmts) .Stmts)
                 If(Compare(Name("count"), CmpOp(">=", Name("value"))),
                    If(Compare(Name("value"), CmpOp(">", Name("result"))),
                       Assign(Name("result"), Name("value")) .Stmts,
                       .Stmts) .Stmts,
                    .Stmts) .Stmts)
               Return(Name("result")) .Stmts,
               0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires nonEmpty(ALL)
     andBool allPositive(ALL)
endmodule
