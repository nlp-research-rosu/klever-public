requires "verification-base.k"

module EXTENSION-LEMMAS
  imports DIGITS-VERIFICATION-BASE

  claim [even-step-equation]:
    <k>
      oddDigitProduct(
        (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
        A)
      =>
      oddDigitProduct(N, A)
    </k>
    requires N >Int 0
     andBool pyMod(N, 2) =/=Int 1

  claim [first-odd-step-equation]:
    <k>
      oddDigitProduct(
        (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
        (N %Int 10 +Int 10) %Int 10)
      =>
      oddDigitProduct(N, 0)
    </k>
    requires N >Int 0
     andBool pyMod(N, 2) ==Int 1

  claim [later-odd-step-equation]:
    <k>
      oddDigitProduct(
        (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
        A *Int ((N %Int 10 +Int 10) %Int 10))
      =>
      oddDigitProduct(N, A)
    </k>
    requires N >Int 0
     andBool A =/=Int 0
     andBool pyMod(N, 2) ==Int 1
endmodule
