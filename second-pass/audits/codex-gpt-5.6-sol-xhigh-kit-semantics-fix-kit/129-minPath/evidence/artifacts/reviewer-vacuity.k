requires "verification.k"

module REVIEWER-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation, different from the candidate probe: the second
  // prompt input with k=1 necessarily starts at value 1, so [2] is false.
  claim [wrong-example-two-first-value]:
    <k> #loadAll(MINPATH-PROGRAM)
        ~> Call(Name("minPath"),
             ( list(vCons(list(vCons(5, vCons(9, vCons(3, .ValSeq)))),
                     vCons(list(vCons(4, vCons(1, vCons(6, .ValSeq)))),
                     vCons(list(vCons(7, vCons(8, vCons(2, .ValSeq)))), .ValSeq))))
             , 1
             , .Exprs))
        => ref(0) </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope) => ?SC:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(2, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
