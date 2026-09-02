module GCD-SPEC
  imports INT
  imports BOOL

  // Mathematical GCD is characterized by the Euclidean equations below.
  // Keeping gcdSpec constructor-valued makes the equations logical lemmas;
  // it also avoids asking the simplifier to evaluate a symbolic recursion.
  syntax Int ::= "gcdSpec" "(" Int "," Int ")" [function, total]
  syntax Int ::= "finalR" "(" Int "," Int ")" [function, total]
  syntax Int ::= "normInt" "(" Int ")" [function, total]

  // Concrete equations make the reference function executable; symbolic
  // reasoning uses the Euclidean equality simplifications below.
  rule gcdSpec(A, 0) => A
    requires A >=Int 0
  rule gcdSpec(A, B) => gcdSpec(B, A %Int B)
    requires (A >=Int 0) andBool (B >Int 0) [simplification, concrete]

  rule normInt(A) => 0 -Int A
    requires A <Int 0
  rule normInt(A) => A
    requires A >=Int 0

  rule finalR(R, R) => 0 [simplification]
  rule finalR(_B, 0) => 0 [simplification]
  rule finalR(0, R) => R
  rule finalR(B, _R) => 0
    requires B =/=Int 0

  rule { gcdSpec(A, 0) #Equals A } => #Top
    requires A >=Int 0 [simplification]
  rule { A #Equals gcdSpec(A, 0) } => #Top
    requires A >=Int 0 [simplification]
  rule { gcdSpec(A, B) #Equals gcdSpec(B, R) } => #Top
    requires (A >=Int 0) andBool (B >Int 0)
      andBool (R ==Int (A %Int B)) [simplification]
  rule { gcdSpec(B, R) #Equals gcdSpec(A, B) } => #Top
    requires (A >=Int 0) andBool (B >Int 0)
      andBool (R ==Int (A %Int B)) [simplification]
endmodule
