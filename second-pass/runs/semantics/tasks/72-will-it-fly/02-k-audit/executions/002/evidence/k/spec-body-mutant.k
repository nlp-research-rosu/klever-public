requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // The original <= theorem must not survive the mutated < body.
  claim
    <k>
      #loadAll(mutantWillItFlyModule)
      ~> Call(Name("will_it_fly"), list(VS:ValSeq), W:Int)
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => "will_it_fly" |-> mutantWillItFlyClosure,
                  parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(mutantReverseVS(VS)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires mutantAllInts(VS)
     andBool VS ==K mutantReverseVS(VS)
     andBool mutantSumIntVS(VS) <=Int W
endmodule
