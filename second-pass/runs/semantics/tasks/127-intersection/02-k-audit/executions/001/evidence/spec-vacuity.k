requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: both implementations return YES for overlap length 2.
  // This changes the original entry claim's result-constraining destination.
  claim
    <k> Call(Name("intersection"),
             TupleExpr(Int(0), Int(2), .Exprs),
             TupleExpr(Int(0), Int(2), .Exprs),
             .Exprs)
      => noV
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "intersection" |->
          closureVal(("interval1", "interval2", .ParamNames),
                     intersectionBody, 0),
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
    [label(false-result)]

endmodule
