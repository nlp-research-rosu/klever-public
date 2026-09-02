requires "verification.k"

module AUDIT-FACTORFROM-WITNESS
  imports VERIFICATION

  // The unguarded helper call uses D=3 even though 2 was never eliminated.
  // It therefore returns [6], which is not a prime factorization of 6.
  claim Observe(ValidFactorization(6, FactorFrom(6, 3)))
    => Observe(false)
endmodule

