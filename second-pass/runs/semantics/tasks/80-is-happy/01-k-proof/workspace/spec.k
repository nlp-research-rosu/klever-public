requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  // Loop invariant: starting with i = I, the loop returns exactly the
  // declarative result for all windows beginning at I.
  claim [happy-loop-correct]:
    <k>
      #while(happyLoopCondition, happyLoopBody)
      ~> Return(Bool(true))
      ~> #endcall
    =>
      #pop
    </k>
    <env> L:Int </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
      (L |-> scope(
        .Map
          [ "s" <- str(IS:IntSeq) ]
          [ "i" <- (I:Int => ?FINAL_I:Int) ],
        parent(0)))
      REST:Map
    </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> noRet => retV(happyFrom(IS, I)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0
     andBool L =/=Int 0
     andBool L =/=Int -1
     andBool notBool 0 in_keys(REST)
     andBool notBool -1 in_keys(REST)
     andBool notBool L in_keys(REST)

endmodule

module SPEC
  imports VERIFICATION

  // Public entry-point body after the reference call rules bind parameter s.
  // isHappyClosure above connects this exact body to the translated function.
  // VERIFICATION supplies the loop theorem proved separately in LOOP-SPEC.
  claim [is-happy-correct]:
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
    <ret> noRet => retV(isHappySpec(IS)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires L =/=Int 0
     andBool L =/=Int -1
     andBool notBool 0 in_keys(REST)
     andBool notBool -1 in_keys(REST)
     andBool notBool L in_keys(REST)
endmodule
