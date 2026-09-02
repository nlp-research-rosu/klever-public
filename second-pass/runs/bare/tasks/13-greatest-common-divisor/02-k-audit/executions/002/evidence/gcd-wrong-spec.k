requires "gcd-eval.k"

module GCD-WRONG-SPEC
  imports GCD-EVAL

  // Deliberately false on the covered nonnegative domain: gcd(25,15) is 5.
  claim <k> gcdSpec(25, 15) => 25 </k>
endmodule
