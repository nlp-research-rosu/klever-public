requires "/tmp/audit-work/fresh/verification.k"

module AUDIT-BRIDGE-MALFORMED-WITNESS
  imports EVEN-ODD-VERIFICATION-SUMMARY

  claim
    <k>
      #loop(str(iCons(49, .IntSeq)), Name("digit"), #digitLoopBody)
      ~> Name("odd_count")
    =>
      1
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "num"        |-> 1
        "even_count" |-> 0
        "odd_count"  |-> 0
        "digit"      |-> 0,
        parent(0))
    =>
      1 |-> scope(
        "num"        |-> 1
        "even_count" |-> 0
        "odd_count"  |-> 1
        "digit"      |-> str(iCons(49, .IntSeq)),
        parent(0))
    </scopes>
endmodule
