requires "verification.k"

module AUDIT-LOOP-CONNECTION
  imports NEXT-SMALLEST-VERIFICATION

  // Reviewer-authored bridge-free theorem matching the installed loop rule's
  // complete context and exact state footprint, including scope cleanup.
  claim
    <k>
      #loop(list(intVals(INPUT:Ints)),
            Name("value"),
            nextSmallestLoopBody)
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
      ((SC
        1 |-> scope(("value" |-> OLD_VALUE
                     "lst" |-> LST
                     "smallest" |-> SMALLEST
                     "second" |-> SECOND
                     "count" |-> COUNT),
                    parent(0))) [1 <- undef])
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
