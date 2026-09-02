// spec.k — modp proof on the UNIFIED semantics (src/).
// Symbolic-count range(n) loop computing 2^n mod p; induct on the remaining range.

requires "verification.k"

module MODP-SPEC
  imports MODP-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(I, N, 1) (the remaining range) from
  // ret=R the loop leaves ret := modIter(N -Int I, R, P). Induction on the range: #iterNext
  // splits I<N (step: i:=I, ret:=pyMod(2*R,P), recurse on rangeObj(I+1,N,1)) vs I>=N (done).
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Assign(Name("ret"), BinOp("%", BinOp("*", Int(2), Name("ret")), Name("p"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "n" <- NV:Int ] [ "p" <- P:Int ] [ "ret" <- R:Int ] [ "i" <- _:Val ], PR:Parent) =>
        scope(.Map [ "n" <- NV ] [ "p" <- P ] [ "ret" <- modIter(N -Int I, R, P) ] [ "i" <- ?_:Val ], PR)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = modp(N, P) == modIter(N, 1, P) (= 2^N mod P). range(N) =
  // rangeObj(0, N, 1), so the loop leaves modIter(N - 0, 1, P). N, P symbolic Ints.
  claim
    <k>
      FuncDef("modp", Params("n", "p"),
        Assign(Name("ret"), Int(1))
        For(Name("i"), Call(Name("range"), Name("n")),
          Assign(Name("ret"), BinOp("%", BinOp("*", Int(2), Name("ret")), Name("p"))))
        Return(Name("ret")))
      Assign(Name("result"), Call(Name("modp"), (Int(N:Int), Int(P:Int))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "modp" <- ?_:Val ] [ "result" <- modIter(N, 1, P) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
