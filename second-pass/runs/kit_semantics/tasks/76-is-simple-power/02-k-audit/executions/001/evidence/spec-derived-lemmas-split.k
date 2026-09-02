requires "verification-base.k"

module SPEC-DERIVED-LEMMAS-SPLIT
  imports VERIFICATION-BASE

  claim [nondivisible-x-is-one]:
    <k>
      ((X:Int ==Int 1) ==Bool simplePower(X, N:Int))
      => true
      ...
    </k>
    requires X ==Int 1
     andBool (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) =/=Int 0

  claim [nondivisible-x-other]:
    <k>
      ((X:Int ==Int 1) ==Bool simplePower(X, N:Int))
      => true
      ...
    </k>
    requires X =/=Int 0 andBool X =/=Int 1
     andBool (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) =/=Int 0

  claim [exact-factor-core]:
    <k>
      simplePower(X:Int, N:Int)
      => simplePower(X /Int N, N)
      ...
    </k>
    requires X =/=Int 0 andBool X =/=Int 1
     andBool (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) ==Int 0
endmodule
