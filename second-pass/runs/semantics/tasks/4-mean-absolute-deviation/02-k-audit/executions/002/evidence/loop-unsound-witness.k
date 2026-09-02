requires "verification.k"

module LOOP-UNSOUND-WITNESS
  imports MAD-VERIFICATION

  // The candidate bridge skips the ordinary for-target binding.  On this
  // satisfying one-float input it therefore proves that the local map remains
  // unchanged, although fixed loop execution binds "number" to 1.0.
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
        => .K </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(
         "mean" |-> F
         "total_deviation" |-> 0.0,
         parent(0))
       =>
       1 |-> scope(
         "mean" |-> F
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
