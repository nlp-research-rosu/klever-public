requires "verification.k"

module SIMPLIFY-SPEC
  imports SIMPLIFY-VERIFICATION

  // ---- Entry — result == simpRes(XCS, NCS) over well-formed 'a/b' inputs
  // (the 2-field domain premises let the unpacks destructure).
  claim
    <k>
      FuncDef("simplify", Params("x", "n"),
          Assign(
            TupleExpr(Name("a"), Name("b")),
            Call(Attribute(Name("x"), "split"), Str("/")))
          Assign(
            TupleExpr(Name("c"), Name("d")),
            Call(Attribute(Name("n"), "split"), Str("/")))
          Assign(
            Name("numerator"),
            BinOp(
              "*",
              Call(Name("int"), Name("a")),
              Call(Name("int"), Name("c"))))
          Assign(
            Name("denom"),
            BinOp(
              "*",
              Call(Name("int"), Name("b")),
              Call(Name("int"), Name("d"))))
          If(Compare(
            BinOp("/", Name("numerator"), Name("denom")),
            CmpOp(
              "==",
              Call(Name("int"), BinOp("/", Name("numerator"), Name("denom"))))),
            Return(Bool(true)),
            .Stmts)
          Return(Bool(false)))
      Assign(Name("result"), Call(Name("simplify"), str(XCS:IntSeq), str(NCS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "simplify" <- ?_:Val ]
                       [ "result" <- simpRes(XCS, NCS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires splitCountC(XCS, 47) ==Int 2 andBool splitCountC(NCS, 47) ==Int 2
     andBool notBool (isLen(fieldSeqC(0, XCS, 47)) ==Int 0) andBool dgN(fieldSeqC(0, XCS, 47)) ==Int 1
     andBool notBool (isLen(fieldSeqC(1, XCS, 47)) ==Int 0) andBool dgN(fieldSeqC(1, XCS, 47)) ==Int 1
     andBool notBool (isLen(fieldSeqC(0, NCS, 47)) ==Int 0) andBool dgN(fieldSeqC(0, NCS, 47)) ==Int 1
     andBool notBool (isLen(fieldSeqC(1, NCS, 47)) ==Int 0) andBool dgN(fieldSeqC(1, NCS, 47)) ==Int 1
    [all-path]
endmodule
