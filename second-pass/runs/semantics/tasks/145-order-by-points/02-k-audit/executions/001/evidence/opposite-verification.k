requires "verification.k"

module ORDER-BY-POINTS-OPPOSITE-VERIFICATION
  imports ORDER-BY-POINTS-VERIFICATION

  // A deliberately wrong but otherwise admissible interpretation of the
  // equation-free result-bearing symbol: keyed sort is the identity.
  rule sortKeyVS(VS:ValSeq, _:Val) => VS
endmodule
