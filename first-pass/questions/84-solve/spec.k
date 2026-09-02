// spec.k — solve on the UNIFIED semantics (src/). Digit-sum while invariant + base-2 while invariant
// + entry. See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module SOLVE-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SOLVE-SPEC

requires "verification.k"

module SOLVE-SPEC
  imports SOLVE-VERIFICATION

  // ---- Loop 1: digit-sum numeric-while. From (N=NV, s=SV) the loop leaves s := digitAcc(NV, SV),
  // N havoc'd (dead after). Scope at loop 1: {N, s}.
  claim
    <k>
      #while(Compare(Name("N"), CmpOp(">", Int(0))),
        Assign(Name("s"), BinOp("+", Name("s"), BinOp("%", Name("N"), Int(10))))
        Assign(Name("N"), BinOp("//", Name("N"), Int(10))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "N" <- NV:Int ] [ "s" <- SV:Int ], P:Parent) =>
        scope(.Map [ "N" <- ?_:Val ] [ "s" <- digitAcc(NV, SV) ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires NV >=Int 0
    [all-path]

  // ---- Loop 2: base-2 code build (change_base's baseFold). From (s=X, ret=str(RC)) the loop leaves
  // ret := str(baseFold(X, 2, RC)), s havoc'd. `str(s%2)` reduces to the digit char via the interception
  // (s%2 = pyMod(X,2) in {0,1}). Scope at loop 2: {N, s, ret} (N dead but still bound).
  claim
    <k>
      #while(Compare(Name("s"), CmpOp(">", Int(0))),
        Assign(Name("ret"), BinOp("+", Call(Name("str"), BinOp("%", Name("s"), Int(2))), Name("ret")))
        Assign(Name("s"), BinOp("//", Name("s"), Int(2))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "solve" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "N" <- NNV:Val ] [ "s" <- X:Int ] [ "ret" <- str(RC:IntSeq) ], parent(GLB:Int)) =>
        scope(.Map [ "N" <- NNV ] [ "s" <- ?_:Val ] [ "ret" <- str(baseFold(X, 2, RC)) ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires X >=Int 0
    [all-path]

  // ---- Entry — result = solve(N) == solveRes(N): the binary string of N's decimal digit sum.
  // The `if s==0` splits on digitAcc(N,0)==0, matching solveRes's two guarded rules. Domain N >= 0.
  claim
    <k>
      FuncDef("solve", Params("N"),
        Assign(Name("s"), Int(0))
        While(Compare(Name("N"), CmpOp(">", Int(0))),
          Assign(Name("s"), BinOp("+", Name("s"), BinOp("%", Name("N"), Int(10))))
          Assign(Name("N"), BinOp("//", Name("N"), Int(10))))
        If(Compare(Name("s"), CmpOp("==", Int(0))),
          Return(Str("0")),
          .Stmts)
        Assign(Name("ret"), Str(""))
        While(Compare(Name("s"), CmpOp(">", Int(0))),
          Assign(Name("ret"), BinOp("+", Call(Name("str"), BinOp("%", Name("s"), Int(2))), Name("ret")))
          Assign(Name("s"), BinOp("//", Name("s"), Int(2))))
        Return(Name("ret")))
      Assign(Name("result"), Call(Name("solve"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "solve" <- ?_:Val ] [ "result" <- solveRes(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
