// spec.k — rounded_avg, TRAP-FREE (P103). Range-sum invariant pair + entry;
// the float route stays opaque (divII/roundF) with trusted non-negativity.
//
//   kompile verification.k --backend haskell --main-module ROUNDED-AVG-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module ROUNDED-AVG-SPEC

requires "verification.k"

module ROUNDED-AVG-SPEC
  imports ROUNDED-AVG-VERIFICATION

  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        AugAssign(Name("summation"), "+", Name("i")))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "n" <- NV:Val ] [ "m" <- MV:Val ] [ "summation" <- ACC:Int ], PR:Parent)
               => scope(.Map [ "n" <- NV ] [ "m" <- MV ] [ "summation" <- ACC +Int sumRange(I, HI) ]
                          [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I <Int HI
    [all-path]

  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        AugAssign(Name("summation"), "+", Name("i")))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "n" <- NV:Val ] [ "m" <- MV:Val ] [ "summation" <- ACC:Int ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- NV ] [ "m" <- MV ] [ "summation" <- ACC +Int sumRange(I, HI) ]
                          [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  claim
    <k>
      FuncDef("rounded_avg", Params("n", "m"),
        If(Compare(Name("m"), CmpOp("<", Name("n"))),
          Return(UnaryOp("-", Int(1))),
          .Stmts)
        Assign(Name("summation"), Int(0))
        For(Name("i"), Call(Name("range"), Name("n"), BinOp("+", Name("m"), Int(1))),
          AugAssign(Name("summation"), "+", Name("i")))
        Return(Call(Name("bin"), Call(Name("round"),
          BinOp("/", Name("summation"), BinOp("+", BinOp("-", Name("m"), Name("n")), Int(1)))))))
      Assign(Name("result"), Call(Name("rounded_avg"), N:Int, M:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "rounded_avg" <- ?_:Val ] [ "result" <- raRes(N, M) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    [all-path]
endmodule
