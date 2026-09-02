requires "verification.k"

module FACTORIZE-BODY-MUTATION-GROUND-SPEC
  imports FACTORIZE-VERIFICATION

  // Satisfiable loop-head witness N=2,D=2,VS=[].
  // The original body appends 2 and reaches n=1; the mutated body appends 3.
  claim [mutated-loop-must-not-have-original-result]:
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(1))), factorizeStep)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("n" |-> 2
         "divisor" |-> 2
         "factors" |-> ref(0)),
        parent(0))
      =>
      1 |-> scope(
        ("n" |-> 1
         "divisor" |-> 2
         "factors" |-> ref(0)),
        parent(0))
    </scopes>
    <heap>
      0 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(2, .ValSeq))
    </heap>
endmodule
