requires "semantic.k"

module VERIFICATION
  imports SEMANTIC
  imports BOOL

  // A canonical positive number has a nonnegative integer component and a
  // proper nonnegative fractional numerator.
  syntax Bool ::= "validPositive" "(" Value ")" [function, total]
  rule validPositive(num(I, F, S))
    => S >Int 0
       andBool I >=Int 0
       andBool F >=Int 0
       andBool F <Int S
       andBool (I >Int 0 orBool F >Int 0)
  rule validPositive(intValue(_)) => false

  syntax Bool ::= "validFraction" "(" Value ")" [function, total]
  rule validFraction(num(I, F, S))
    => I ==Int 0 andBool S >Int 0 andBool F >=Int 0 andBool F <Int S
  rule validFraction(intValue(_)) => false
endmodule
