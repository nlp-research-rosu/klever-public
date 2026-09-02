requires "/tmp/audit-work/fresh/verification.k"

module AUDIT-BRIDGE-GENERALIZATION
  imports EVEN-ODD-VERIFICATION

  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"), #digitLoopBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        "num"        |-> N:Int
        "even_count" |-> E:Int
        "odd_count"  |-> O:Int
        "digit"      |-> D:Val,
        parent(0))
    =>
      1 |-> scope(
        "num"        |-> N
        "even_count" |-> E +Int evenDigits(CS)
        "odd_count"  |-> O +Int oddDigits(CS)
        "digit"      |-> lastSeen(CS, D),
        parent(0))
      ...
    </scopes>
endmodule
