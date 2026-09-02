// spec.k — Probe A: call-in-loop. Claim 1 = digsum's while-invariant (framed, applies inside the
// callee frame at any loc). Claim 2 = the LOAD-BEARING outer range-loop invariant over the real
// Call: fixed store shape (-1 builtins, 0 module, 1 caller frame), <scopeLoc> pinned at 2 — each
// iteration allocates the callee frame at 2 and the wind-back restores the shape. Claim 3 = entry.
//
//   kompile verification.k --backend haskell \
//     --main-module CALL-IN-LOOP-PROBE-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module CALL-IN-LOOP-PROBE-SPEC

requires "verification.k"

module CALL-IN-LOOP-PROBE-SPEC
  imports CALL-IN-LOOP-PROBE-VERIFICATION

  // ---- Claim 1: digsum's numeric-while — from (k = K, s = S) the loop leaves s := digAcc(K, S).
  // Framed over any loc L: it fires inside the callee frame claim 2 allocates.
  claim
    <k>
      #while(Compare(Name("k"), CmpOp(">", Int(0))),
        Assign(Name("s"), BinOp("+", Name("s"), BinOp("%", Name("k"), Int(10))))
        Assign(Name("k"), BinOp("//", Name("k"), Int(10))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "k" <- K:Int ] [ "s" <- S:Int ], PR:Parent)
               => scope(.Map [ "k" <- ?_:Val ] [ "s" <- digAcc(K, S) ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Claim 2 (LOAD-BEARING): the outer range-loop invariant with the REAL Call in the body —
  // no interception. From t = T the loop leaves t := tdFold(I, N, T). The store shape is FIXED:
  // every iteration pushes the digsum frame at loc 2 and deallocation restores exactly this
  // configuration, so the circularity re-applies.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Assign(Name("t"), BinOp("+", Name("t"), Call(Name("digsum"), Name("i")))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map
              [ "digsum" <- closureVal("k",
                  Assign(Name("s"), Int(0))
                  While(Compare(Name("k"), CmpOp(">", Int(0))),
                    Assign(Name("s"), BinOp("+", Name("s"), BinOp("%", Name("k"), Int(10))))
                    Assign(Name("k"), BinOp("//", Name("k"), Int(10))))
                  Return(Name("s")), 0) ]
              [ "total_digsum" <- TDV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "t" <- T:Int ] [ "i" <- _:Val ], parent(0))
           => scope(.Map [ "n" <- NV ] [ "t" <- tdFold(I, N, T) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0
    [all-path]

  // ---- Claim 3: entry — out = total_digsum(N) == tdFold(0, N, 0). The module program verbatim.
  claim
    <k>
      FuncDef("digsum", Params("k"),
        Assign(Name("s"), Int(0))
        While(Compare(Name("k"), CmpOp(">", Int(0))),
          Assign(Name("s"), BinOp("+", Name("s"), BinOp("%", Name("k"), Int(10))))
          Assign(Name("k"), BinOp("//", Name("k"), Int(10))))
        Return(Name("s")))
      FuncDef("total_digsum", Params("n"),
        Assign(Name("t"), Int(0))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), Name("n")),
          Assign(Name("t"), BinOp("+", Name("t"), Call(Name("digsum"), Name("i")))))
        Return(Name("t")))
      Assign(Name("out"), Call(Name("total_digsum"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "digsum" <- ?_:Val ] [ "total_digsum" <- ?_:Val ]
                       [ "out" <- tdFold(0, N, 0) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
