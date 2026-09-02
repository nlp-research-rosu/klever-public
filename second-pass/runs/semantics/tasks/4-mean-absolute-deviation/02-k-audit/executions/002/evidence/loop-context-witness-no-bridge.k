requires "verification-no-loop.k"

module LOOP-CONTEXT-WITNESS-NO-BRIDGE
  imports MAD-VERIFICATION-NO-LOOP

  claim
    <k> #loop(
          list(vCons(F:Float, .ValSeq)),
          Name("number"),
          AugAssign(
            Name("total_deviation"),
            "+",
            Call(
              Name("abs"),
              BinOp("-", Name("number"), Name("mean")))))
        ~> Name("number")
        => G:Float </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(
         "mean" |-> F
         "number" |-> G
         "total_deviation" |-> 0.0,
         parent(0))
       =>
       1 |-> scope(
         "mean" |-> F
         "number" |-> G
         "total_deviation" |->
           absDeviationFold(vCons(F, .ValSeq), F, 0.0),
         parent(0)))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
