requires "verification.k"

module OPPOSITE-THEORY
  imports VERIFICATION

  syntax Float ::= wrongLo() [function, total, symbol(wrongLo), no-evaluators]
                   | wrongHi() [function, total, symbol(wrongHi), no-evaluators]
  rule minVF(vCons(1.0, vCons(2.0, .ValSeq))) => wrongLo()
  rule maxVF(vCons(1.0, vCons(2.0, .ValSeq))) => wrongHi()
endmodule
