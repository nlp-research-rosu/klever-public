requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  // Loop invariant / total-correctness lemma.  Starting at candidate DIVISOR,
  // the remaining MPY loop returns the same answer as primeFrom.
  claim
    <k> #loop(rangeObj(DIVISOR:Int, LENGTH:Int, 1),
              Name("divisor"), divisorBody)
        ~> (Return(Str("YES")) .Stmts) ~> #endcall
      => primeFrom(LENGTH, DIVISOR) ~> KONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      SC:Map
       1 |-> scope(
         "interval1" |-> INTERVAL1:Val
         "interval2" |-> INTERVAL2:Val
         "left"      |-> LEFT:Int
         "right"     |-> RIGHT:Int
         "length"    |-> LENGTH
         "divisor"   |-> OLD:Int,
         parent(0))
      => SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack> ListItem(frame(KONT, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    requires 2 <=Int DIVISOR andBool DIVISOR <=Int LENGTH
    [label(loop-correct)]

endmodule

module SPEC
  imports VERIFICATION

  // The complete, universally quantified function contract.  A..B and C..D
  // are valid closed intervals.  The result is YES exactly when
  // min(B,D)-max(A,C) is prime according to the divisor definition above.
  claim
    <k> Call(Name("intersection"),
             TupleExpr(Int(A:Int), Int(B:Int), .Exprs),
             TupleExpr(Int(C:Int), Int(D:Int), .Exprs),
             .Exprs)
      => primeResult(overlapLength(A, B, C, D))
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
    [label(intersection-correct)]
endmodule
