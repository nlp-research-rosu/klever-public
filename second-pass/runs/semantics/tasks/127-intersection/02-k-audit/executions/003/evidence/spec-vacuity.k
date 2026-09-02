requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: valid intervals with prime overlap (for example,
  // (0,2) and (0,2)) must return YES, but this mutation requires NO always.
  claim
    <k> Call(Name("intersection"),
             TupleExpr(Int(A:Int), Int(B:Int), .Exprs),
             TupleExpr(Int(C:Int), Int(D:Int), .Exprs),
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
    requires A <=Int B andBool C <=Int D
    [label(false-postcondition)]
endmodule
