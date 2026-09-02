requires "verification.k"

module AUDIT-FALSE-RESULT-SPEC
  imports VERIFICATION

  // Fresh audit mutation: [0, 1, 2, 3] satisfies the intended input domain
  // and returns true, so requiring false must leave a result obligation.
  claim [audit-false-result]:
    <k> IS-SORTED-CALL => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope("input" |->
                     list(vCons(0, vCons(1, vCons(2,
                       vCons(3, .ValSeq))))),
                   parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("input" |->
                     list(vCons(0, vCons(1, vCons(2,
                       vCons(3, .ValSeq)))))
                   "is_sorted" |-> IS-SORTED-CLOSURE,
                   parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool false
endmodule
