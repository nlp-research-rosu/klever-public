// spec.k — fruit_distribution, TRAP-FREE (P67). Element-loop invariant over
// the abstract token seq with the Probe-B FIXED-ref append shape; the sum-fold
// circularity consumes the built list; entry over the real single FuncDef.
//
//   kompile verification.k --backend haskell --main-module FRUIT-DISTRIBUTION-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FRUIT-DISTRIBUTION-SPEC

requires "verification.k"

module FRUIT-DISTRIBUTION-SPEC
  imports FRUIT-DISTRIBUTION-VERIFICATION

  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(Call(Attribute(Name("i"), "isdigit"), .Exprs),
          Expr(Call(Attribute(Name("lis"), "append"), Call(Name("int"), Name("i")))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fruit_distribution" <- FDV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "s" <- SV:Val ] [ "n" <- NV:Val ] [ "lis" <- ref(LR:Int) ], parent(0))
           => scope(.Map [ "s" <- SV ] [ "n" <- NV ] [ "lis" <- ref(LR) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(dFilt(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <Int vsLen(VS) andBool allStr(VS)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(Call(Attribute(Name("i"), "isdigit"), .Exprs),
          Expr(Call(Attribute(Name("lis"), "append"), Call(Name("int"), Name("i")))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fruit_distribution" <- FDV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "s" <- SV:Val ] [ "n" <- NV:Val ] [ "lis" <- ref(LR:Int) ] [ "i" <- _:Val ], parent(0))
           => scope(.Map [ "s" <- SV ] [ "n" <- NV ] [ "lis" <- ref(LR) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(dFilt(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]

  claim <k> #sumAcc(list(VS2:ValSeq), ACC2:Int) => ?R:Int ... </k>
        requires allInt(VS2)
        ensures  ?R ==Int sumOf(VS2, ACC2)
        [all-path]

  claim
    <k>
      FuncDef("fruit_distribution", Params("s", "n"),
        Assign(Name("lis"), Call(Name("list"), .Exprs))
        For(Name("i"), Call(Attribute(Name("s"), "split"), Str(" ")),
          If(Call(Attribute(Name("i"), "isdigit"), .Exprs),
          Expr(Call(Attribute(Name("lis"), "append"), Call(Name("int"), Name("i")))),
          .Stmts))
        Return(BinOp("-", Name("n"), Call(Name("sum"), Name("lis")))))
      Assign(Name("result"), Call(Name("fruit_distribution"), (str(CS:IntSeq), N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fruit_distribution" <- ?_:Val ] [ "result" <- fdRes(CS, N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
