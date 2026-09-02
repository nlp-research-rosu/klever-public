requires "audit-mutated-verification.k"

module AUDIT-LOOP-BODY-MUTATION
  imports AUDIT-MUTATED-VERIFICATION

  // Input [1, 2] reaches the mutated branch and returns 3 while the unmutated
  // nsScan obligation still requires 2.

  claim
    <k>
      #loop(list(intVals(INPUT:Ints)),
            Name("value"),
            auditMutatedLoopBody)
      ~> nextSmallestReturn
      ~> #endcall
    =>
      nsScan(INPUT, SMALLEST:Int, SECOND:Int, COUNT:Int)
      ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(("value" |-> OLD_VALUE:Int
                    "lst" |-> LST:Val
                    "smallest" |-> SMALLEST
                    "second" |-> SECOND
                    "count" |-> COUNT),
                   parent(0)))
    =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map => HEAP </heap>
    <heapLoc> HLOC:Int => HLOC </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) REST:List
    =>
      REST
    </stack>
    <ret> noRet => noRet </ret>
    <exc> EXC:Exc => EXC </exc>
    <exit-code> CODE:Int => CODE </exit-code>
    requires notBool (1 in_keys(SC))
endmodule
