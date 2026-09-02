requires "verification.k"

module FACTORIZE-CONTINUATION-PROBE-SPEC
  imports FACTORIZE-VERIFICATION

  // Observable continuation probe: both fixed execution and the promoted
  // lemma must preserve and execute the assignment after the loop.
  claim [loop-preserves-continuation]:
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(1))), factorizeStep)
      ~> Assign(Name("marker"), Int(9))
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
         "factors" |-> ref(0)
         "marker" |-> 9),
        parent(0))
    </scopes>
    <heap>
      0 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(2, .ValSeq))
    </heap>
endmodule
