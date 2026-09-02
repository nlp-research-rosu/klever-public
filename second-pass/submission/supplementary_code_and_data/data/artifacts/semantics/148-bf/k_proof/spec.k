requires "verification.k"

module BF-SPEC
  imports BF-VERIFICATION

  // All 64 valid-name pairs.
  claim
    <k> #validCases(0, 0) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // If the first name is invalid, short-circuiting makes the second arbitrary.
  claim
    <k> bfRun(str(A), str(_B)) => tuple(.ValSeq) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A =/=K strToCodes("Mercury")
     andBool A =/=K strToCodes("Venus")
     andBool A =/=K strToCodes("Earth")
     andBool A =/=K strToCodes("Mars")
     andBool A =/=K strToCodes("Jupiter")
     andBool A =/=K strToCodes("Saturn")
     andBool A =/=K strToCodes("Uranus")
     andBool A =/=K strToCodes("Neptune")

  // If the first name is valid and the second is invalid.
  claim
    <k> bfRun(str(A), str(B)) => tuple(.ValSeq) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires (A ==K strToCodes("Mercury")
       orBool A ==K strToCodes("Venus")
       orBool A ==K strToCodes("Earth")
       orBool A ==K strToCodes("Mars")
       orBool A ==K strToCodes("Jupiter")
       orBool A ==K strToCodes("Saturn")
       orBool A ==K strToCodes("Uranus")
       orBool A ==K strToCodes("Neptune"))
     andBool B =/=K strToCodes("Mercury")
     andBool B =/=K strToCodes("Venus")
     andBool B =/=K strToCodes("Earth")
     andBool B =/=K strToCodes("Mars")
     andBool B =/=K strToCodes("Jupiter")
     andBool B =/=K strToCodes("Saturn")
     andBool B =/=K strToCodes("Uranus")
     andBool B =/=K strToCodes("Neptune")
endmodule
