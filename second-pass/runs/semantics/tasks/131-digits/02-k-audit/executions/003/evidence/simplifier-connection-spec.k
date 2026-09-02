requires "verification-base.k"

module SIMPLIFIER-CONNECTION-SPEC
  imports DIGITS-VERIFICATION-BASE

  // Each claim runs the defining recurrence without importing any of the
  // candidate's three [simplification] equality lemmas.
  claim [even-step-connection]:
    <k>
      oddDigitProduct(N, A)
      =>
      oddDigitProduct(
        (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
        A)
    </k>
    requires N >Int 0
     andBool pyMod(N, 2) =/=Int 1

  claim [first-odd-step-connection]:
    <k>
      oddDigitProduct(N, 0)
      =>
      oddDigitProduct(
        (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
        (N %Int 10 +Int 10) %Int 10)
    </k>
    requires N >Int 0
     andBool pyMod(N, 2) ==Int 1

  claim [later-odd-step-connection]:
    <k>
      oddDigitProduct(N, A)
      =>
      oddDigitProduct(
        (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
        A *Int ((N %Int 10 +Int 10) %Int 10))
    </k>
    requires N >Int 0
     andBool A =/=Int 0
     andBool pyMod(N, 2) ==Int 1
endmodule
