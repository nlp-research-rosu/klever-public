requires "verification.k"

module OPPOSITE-HARNESS
  imports VERIFICATION
  imports MPY-KRUN

  rule minVF(vCons(1.0, vCons(2.0, .ValSeq))) => 2.0
  rule maxVF(vCons(1.0, vCons(2.0, .ValSeq))) => 1.0

  syntax Stmt ::= "RunOpposite"
  rule <k> RunOpposite ~> .Stmts
        => #runRescale(vCons(1.0, vCons(2.0, .ValSeq)))
       </k>
endmodule
