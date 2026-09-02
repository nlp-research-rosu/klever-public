requires "verification.k"

module SPEC-VACUITY-REVIEWER
  imports VERIFICATION

  // Deliberately false: negate the result-constraining public postcondition.
  // Witness: IS = [97, 98, 99] ("abc"), L = 1, REST = .Map.
  // Both Python implementations and isHappySpec return true, but this asks false.
  claim [is-happy-wrong-negated-result]:
    <k> isHappyBody ~> #endcall => #pop </k>
    <env> L:Int </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (L |-> scope(.Map [ "s" <- str(IS:IntSeq) ], parent(0)))
      REST:Map
    =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> noRet => retV(notBool isHappySpec(IS)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires L =/=Int 0
     andBool L =/=Int -1
     andBool notBool 0 in_keys(REST)
     andBool notBool -1 in_keys(REST)
     andBool notBool L in_keys(REST)
endmodule
