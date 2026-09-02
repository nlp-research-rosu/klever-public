requires "verification.k"

module FACTORIZE-GROUND-EVAL
  imports MPY-KRUN
  imports FACTORIZE-VERIFICATION

  syntax Module ::= "Ground" "(" Int ")"
  rule <k> #loadAll(Ground(N:Int)) => primeFactors(N) ... </k>
endmodule
