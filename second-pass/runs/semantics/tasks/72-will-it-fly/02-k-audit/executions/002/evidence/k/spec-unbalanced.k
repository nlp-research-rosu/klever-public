requires "verification.k"

module SPEC-UNBALANCED
  imports VERIFICATION

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
     andBool notBool (VS ==K reverseVS(VS))
endmodule
