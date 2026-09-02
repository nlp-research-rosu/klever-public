requires "verification.k"

// This admissible ground interpretation witnesses that the candidate never
// connects oddDigits to execution of _all_digits_odd.
module UNIQUE-DIGITS-WRONG-ORACLE
  imports UNIQUE-DIGITS-VERIFICATION

  rule oddDigits(2) => true
endmodule
