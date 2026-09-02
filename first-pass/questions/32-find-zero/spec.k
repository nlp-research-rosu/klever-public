// spec.k — find_zero on the UNIFIED semantics (reference/src/).  Two co-inductive loop invariants +
// entry (PARTIAL correctness — if the loops halt).  See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module FINDZERO-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FINDZERO-SPEC

requires "verification.k"

module FINDZERO-SPEC
  imports FINDZERO-VERIFICATION

  // ---- loop 1 invariant (bracket, PARTIAL): if the doubling loop halts, (begin,end) := bracket(XS,B,E).
  claim
    <k>
      #while(Compare(BinOp("*", Call(Name("poly"), Name("xs"), Name("begin")), Call(Name("poly"), Name("xs"), Name("end"))), CmpOp(">", Float(0.0))),
        Assign(Name("begin"), BinOp("*", Name("begin"), Float(2.0)))
        Assign(Name("end"), BinOp("*", Name("end"), Float(2.0))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "xs" <- list(XS:ValSeq) ] [ "begin" <- B:Float ] [ "end" <- E:Float ] [ "center" <- CV:Val ], PR:Parent)
               => scope(.Map [ "xs" <- list(XS) ] [ "begin" <- brB(bracket(XS, B, E)) ] [ "end" <- brE(bracket(XS, B, E)) ] [ "center" <- CV ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- loop 2 invariant (bisect, PARTIAL): if the halving loop halts, begin := bisect(XS,B,E).
  claim
    <k>
      #while(Compare(BinOp("-", Name("end"), Name("begin")), CmpOp(">", Float(1e-10))),
        Assign(Name("center"), BinOp("/", BinOp("+", Name("begin"), Name("end")), Float(2.0)))
        If(Compare(BinOp("*", Call(Name("poly"), Name("xs"), Name("center")), Call(Name("poly"), Name("xs"), Name("begin"))), CmpOp(">", Float(0.0))),
          Assign(Name("begin"), Name("center")),
          Assign(Name("end"), Name("center"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "xs" <- list(XS:ValSeq) ] [ "begin" <- B:Float ] [ "end" <- E:Float ] [ "center" <- _:Val ], PR:Parent)
               => scope(.Map [ "xs" <- list(XS) ] [ "begin" <- bisect(XS, B, E) ] [ "end" <- ?_:Val ] [ "center" <- ?_:Val ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- entry (PARTIAL): if the loops halt, out = findZeroRes(XS).
  claim
    <k>
      FuncDef("find_zero", Params("xs"),
        Assign(Name("begin"), UnaryOp("-", Float(1.0)))
        Assign(Name("end"), Float(1.0))
        Assign(Name("center"), Float(0.0))
        While(Compare(BinOp("*", Call(Name("poly"), Name("xs"), Name("begin")), Call(Name("poly"), Name("xs"), Name("end"))), CmpOp(">", Float(0.0))),
          Assign(Name("begin"), BinOp("*", Name("begin"), Float(2.0)))
          Assign(Name("end"), BinOp("*", Name("end"), Float(2.0))))
        While(Compare(BinOp("-", Name("end"), Name("begin")), CmpOp(">", Float(1e-10))),
          Assign(Name("center"), BinOp("/", BinOp("+", Name("begin"), Name("end")), Float(2.0)))
          If(Compare(BinOp("*", Call(Name("poly"), Name("xs"), Name("center")), Call(Name("poly"), Name("xs"), Name("begin"))), CmpOp(">", Float(0.0))),
            Assign(Name("begin"), Name("center")),
            Assign(Name("end"), Name("center"))))
        Return(Name("begin")))
      Assign(Name("out"), Call(Name("find_zero"), list(XS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "find_zero" <- ?_:Val ] [ "out" <- findZeroRes(XS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
