requires "verification.k"

module GROUND-SUMMARY
  imports VERIFICATION

  claim [summary-example]:
    <k>
      sumSquaresAcc(vCons(1, vCons(2, vCons(3, .ValSeq))), 0, 0)
      => 6
    </k>
    <env> E1:Int </env>
    <scopes> S1:Map </scopes>
    <scopeLoc> L1:Int </scopeLoc>
    <heap> H1:Map </heap>
    <heapLoc> N1:Int </heapLoc>
    <stack> ST1:List </stack>
    <ret> R1:RetState </ret>
    <exc> X1:Exc </exc>
    <exit-code> C1:Int </exit-code>

  claim [summary-empty]:
    <k> sumSquaresAcc(.ValSeq, 0, 0) => 0 </k>
    <env> E2:Int </env>
    <scopes> S2:Map </scopes>
    <scopeLoc> L2:Int </scopeLoc>
    <heap> H2:Map </heap>
    <heapLoc> N2:Int </heapLoc>
    <stack> ST2:List </stack>
    <ret> R2:RetState </ret>
    <exc> X2:Exc </exc>
    <exit-code> C2:Int </exit-code>

  claim [summary-negative]:
    <k>
      sumSquaresAcc(
        vCons(-1, vCons(-5, vCons(2, vCons(-1, vCons(-5, .ValSeq))))),
        0,
        0)
      => -126
    </k>
    <env> E3:Int </env>
    <scopes> S3:Map </scopes>
    <scopeLoc> L3:Int </scopeLoc>
    <heap> H3:Map </heap>
    <heapLoc> N3:Int </heapLoc>
    <stack> ST3:List </stack>
    <ret> R3:RetState </ret>
    <exc> X3:Exc </exc>
    <exit-code> C3:Int </exit-code>

  claim [summary-common-multiple]:
    <k>
      sumSquaresAcc(
        vCons(
          0,
          vCons(
            0,
            vCons(
              0,
              vCons(
                0,
                vCons(
                  0,
                  vCons(
                    0,
                    vCons(
                      0,
                      vCons(
                        0,
                        vCons(
                          0,
                          vCons(
                            0,
                            vCons(0, vCons(0, vCons(2, .ValSeq))))))))))))),
        0,
        0)
      => 4
    </k>
    <env> E4:Int </env>
    <scopes> S4:Map </scopes>
    <scopeLoc> L4:Int </scopeLoc>
    <heap> H4:Map </heap>
    <heapLoc> N4:Int </heapLoc>
    <stack> ST4:List </stack>
    <ret> R4:RetState </ret>
    <exc> X4:Exc </exc>
    <exit-code> C4:Int </exit-code>
endmodule
