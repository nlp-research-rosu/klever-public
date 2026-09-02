requires "verification-base.k"

module SPEC-DERIVED-LEMMAS
  imports VERIFICATION-BASE

  claim [nondivisible-exit]:
    <k>
      ((X:Int ==Int 1) ==Bool simplePower(X, N:Int))
      => true
      ...
    </k>
    requires (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) =/=Int 0

  claim [exact-factor]:
    <k>
      simplePower(X:Int, N:Int)
      => simplePower(X /Int N, N)
      ...
    </k>
    requires X =/=Int 0
     andBool (N <=Int -2 orBool N >=Int 2)
     andBool pyMod(X, N) ==Int 0
endmodule
