requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant/summary.  This is a proof claim, not a trusted rule: after
  // one concrete semantic iteration it recurs on REST with the two updated
  // extrema, while the empty-list branch closes directly.
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

  // Entry-point theorem: for every finite list containing only integers,
  // executing the translated function returns the modeled extrema.  The
  // optional conversion gives None exactly when the corresponding set is
  // empty.
  claim [entry-point-correct]:
    <k> #loadAll(largestSmallestModule)
         ~> Call(Name("largest_smallest_integers"), list(VS:ValSeq))
      => tuple(vCons(optionalNeg(negFold(VS, 0)),
               vCons(optionalPos(posFold(VS, 0)), .ValSeq)))
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
