requires "/tmp/audit-work/4mad-review/candidate-source/verification.k"

module LOOP-SIDE-EFFECT-EXTENDED
  imports MAD-VERIFICATION

  // This is the same false destination as LOOP-SIDE-EFFECT-FIXED.  The
  // proof-local priority-40 loop bridge closes it by omitting number's write.
  // A concrete satisfying counterexample is F=2.0, OLD=9.0, MEAN=2.0,
  // ACC=0.0.
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
       1 |-> scope(
              "mean" |-> MEAN:Float
              "total_deviation" |-> (ACC:Float
                => addF(ACC, absF(subF(F, MEAN))))
              "number" |-> OLD:Float,
              parent(0))
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
