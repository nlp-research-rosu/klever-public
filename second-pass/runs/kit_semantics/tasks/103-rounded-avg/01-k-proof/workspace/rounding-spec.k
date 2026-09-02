requires "verification-base.k"

module ROUNDING-SPEC
  imports VERIFICATION-BASE

  claim [rounded-even-sum]:
    <k>
      roundedInt(N, M)
      =>
      (N +Int M -Int pyMod(N +Int M, 2)) /Int 2
    </k>
    requires N >Int 0 andBool M >Int 0 andBool N <=Int M
      andBool pyMod(N +Int M, 2) ==Int 0

  claim [rounded-odd-even-quotient]:
    <k>
      roundedInt(N, M)
      =>
      (N +Int M -Int pyMod(N +Int M, 2)) /Int 2
    </k>
    requires N >Int 0 andBool M >Int 0 andBool N <=Int M
      andBool pyMod(N +Int M, 2) ==Int 1
      andBool pyMod(
        (N +Int M -Int pyMod(N +Int M, 2)) /Int 2,
        2) ==Int 0

  claim [rounded-odd-odd-quotient]:
    <k>
      roundedInt(N, M)
      =>
      (N +Int M -Int pyMod(N +Int M, 2)) /Int 2 +Int 1
    </k>
    requires N >Int 0 andBool M >Int 0 andBool N <=Int M
      andBool pyMod(N +Int M, 2) ==Int 1
      andBool pyMod(
        (N +Int M -Int pyMod(N +Int M, 2)) /Int 2,
        2) ==Int 1
endmodule
