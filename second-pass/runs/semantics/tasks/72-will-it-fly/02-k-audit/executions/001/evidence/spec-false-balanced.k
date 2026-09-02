requires "verification.k"

module SPEC-FALSE-BALANCED
  imports VERIFICATION

  // Deliberately false: [3,2,3] with w=9 satisfies this precondition, but the
  // real and generated Python functions both return true, not false.
  claim
    <k>
      #loadAll(willItFlyModule)
      ~> Call(Name("will_it_fly"), list(VS:ValSeq), W:Int)
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => "will_it_fly" |-> willItFlyClosure,
                  parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(reverseVS(VS)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
     andBool VS ==K reverseVS(VS)
     andBool sumIntVS(VS) <=Int W
endmodule
