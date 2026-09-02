// spec.k — how_many_times, TRAP-FREE (P18). Inner window-scan invariant (the
// REAL inline body) + outer count invariant CONTAINING the inner For (nested-
// loop rung; inner claim fires as a circularity) + entry. len() resolves
// inside the outer body -> pinned -1 chain.
//
//   kompile verification.k --backend haskell --main-module HOW-MANY-TIMES-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module HOW-MANY-TIMES-SPEC

requires "verification.k"

module HOW-MANY-TIMES-SPEC
  imports HOW-MANY-TIMES-VERIFICATION

  // ---- inner window scan: ok := OK andBool winEq(SC, SUBC, IV, J)
  claim
    <k>
      #loop(rangeObj(J:Int, M:Int, 1), Name("j"),
        If(Compare(
            Subscript(Name("string"), BinOp("+", Name("i"), Name("j"))),
            CmpOp("!=", Subscript(Name("substring"), Name("j")))),
          Assign(Name("ok"), Bool(false)),
          .Stmts))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "string" <- str(SC:IntSeq) ] [ "substring" <- str(SUBC:IntSeq) ]
                              [ "times" <- T:Val ] [ "i" <- IV:Int ] [ "ok" <- OK:Bool ] [ "j" <- _:Val ], PR:Parent)
               => scope(.Map [ "string" <- str(SC) ] [ "substring" <- str(SUBC) ]
                              [ "times" <- T ] [ "i" <- IV ] [ "ok" <- OK andBool winEq(SC, SUBC, IV, J) ] [ "j" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires J >=Int 0 andBool M ==Int isLen(SUBC)
     andBool IV >=Int 0 andBool IV +Int isLen(SUBC) <=Int isLen(SC)
    [all-path]

  // ---- outer count invariant (body CONTAINS the inner For)
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Assign(Name("ok"), Bool(true))
        Assign(Name("j"), Int(0))
        For(Name("j"), Call(Name("range"), Call(Name("len"), Name("substring"))),
          If(Compare(
            Subscript(Name("string"), BinOp("+", Name("i"), Name("j"))),
            CmpOp("!=", Subscript(Name("substring"), Name("j")))),
          Assign(Name("ok"), Bool(false)),
          .Stmts))
        If(Name("ok"),
          AugAssign(Name("times"), "+", Int(1)),
          .Stmts))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... -1 |-> builtinsScope
          GLB |-> scope(.Map [ "how_many_times" <- FB0:Val ], parent(-1))
          L0 |-> ( scope(.Map [ "string" <- str(SC:IntSeq) ] [ "substring" <- str(SUBC:IntSeq) ]
                              [ "times" <- C:Int ] [ "i" <- _:Val ] [ "ok" <- _:Bool ] [ "j" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "string" <- str(SC) ] [ "substring" <- str(SUBC) ]
                              [ "times" <- countFold(I, N, SC, SUBC, C) ] [ "i" <- ?_:Val ] [ "ok" <- ?_:Val ] [ "j" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool isLen(SUBC) >=Int 1
     andBool N ==Int isLen(SC) -Int isLen(SUBC) +Int 1
    [all-path]

  // ---- entry
  claim
    <k>
      FuncDef("how_many_times", Params("string", "substring"),
        Assign(Name("times"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("ok"), Bool(true))
        Assign(Name("j"), Int(0))
        For(Name("i"), Call(Name("range"),
            BinOp("+", BinOp("-", Call(Name("len"), Name("string")), Call(Name("len"), Name("substring"))), Int(1))),
          Assign(Name("ok"), Bool(true))
        Assign(Name("j"), Int(0))
        For(Name("j"), Call(Name("range"), Call(Name("len"), Name("substring"))),
          If(Compare(
            Subscript(Name("string"), BinOp("+", Name("i"), Name("j"))),
            CmpOp("!=", Subscript(Name("substring"), Name("j")))),
          Assign(Name("ok"), Bool(false)),
          .Stmts))
        If(Name("ok"),
          AugAssign(Name("times"), "+", Int(1)),
          .Stmts))
        Return(Name("times")))
      Assign(Name("result"), Call(Name("how_many_times"), (str(SC:IntSeq), str(SUBC:IntSeq))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "how_many_times" <- ?_:Val ]
                       [ "result" <- countFold(0, isLen(SC) -Int isLen(SUBC) +Int 1, SC, SUBC, 0) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(SUBC) >=Int 1
    [all-path]
endmodule
