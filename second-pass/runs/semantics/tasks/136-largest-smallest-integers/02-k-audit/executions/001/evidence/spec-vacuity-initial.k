requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation: the loop obligation remains unchanged.
  claim [scan-loop]:
    <k> #loop(list(VS:ValSeq), Name("value"), scanBody)
        => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("lst"                 |-> INPUT:Val)
        ("largest_negative"    |-> (A:Int => negFold(VS, A)))
        ("smallest_positive"   |-> (B:Int => posFold(VS, B)))
        ("value"               |-> (OLD:Int => finalValue(VS, OLD))),
        parent(0))
      ...
    </scopes>
    requires allInts(VS)
     andBool A <=Int 0
     andBool B >=Int 0

  // Deliberately false result constraint: the positive component is forced
  // to None.  VS = [1] satisfies allInts but the real result is (None, 1).
  claim [entry-point-wrong-positive]:
    <k> #loadAll(largestSmallestModule)
         ~> Call(Name("largest_smallest_integers"), list(VS:ValSeq))
      => tuple(vCons(optionalNeg(negFold(VS, 0)),
               vCons(noneV, .ValSeq)))
      ... </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "largest_smallest_integers"
           |-> closureVal(("lst", .ParamNames), solutionBody, 0),
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
    requires allInts(VS)
endmodule
