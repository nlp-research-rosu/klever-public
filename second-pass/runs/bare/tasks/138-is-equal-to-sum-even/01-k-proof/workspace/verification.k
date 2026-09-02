requires "semantic.k"

module VERIFICATION
  imports MPY

  // Arithmetic characterization of being a sum of four positive even
  // integers.  The reverse direction has the constructive witnesses
  // N - 6, 2, 2, 2; SPEC proves that these really meet the original wording.
  syntax Bool ::= sumFourPositiveEvens(Int) [function, total]
  rule sumFourPositiveEvens(N)
    => N >=Int 8 andBool N %Int 2 ==Int 0

  syntax Bool ::= canonicalWitnessesAreValid(Int) [function, total]
  rule canonicalWitnessesAreValid(N)
    => N -Int 6 >Int 0
       andBool (N -Int 6) %Int 2 ==Int 0
       andBool 2 >Int 0 andBool 2 %Int 2 ==Int 0
       andBool (N -Int 6) +Int 2 +Int 2 +Int 2 ==Int N

  syntax KItem ::= checkCanonicalWitnesses(Int)
  rule <k> checkCanonicalWitnesses(N) => .K </k>
       <result> noResult => BoolValue(canonicalWitnessesAreValid(N)) </result>
endmodule
