requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [encrypt-loop]:
    <k>
      #loop(
        str(S:IntSeq),
        Name("c"),
        If(
          BoolOp(
            "and",
            Compare(
              Call(Name("ord"), Name("c")),
              CmpOp(">=", Int(97))),
            Compare(
              Call(Name("ord"), Name("c")),
              CmpOp("<=", Int(122)))),
          AugAssign(
            Name("out"),
            "+",
            Call(
              Name("chr"),
              BinOp(
                "+",
                BinOp(
                  "%",
                  BinOp(
                    "+",
                    BinOp("-", Call(Name("ord"), Name("c")), Int(97)),
                    Int(4)),
                  Int(26)),
                Int(97)))),
          AugAssign(Name("out"), "+", Name("c"))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope("encrypt" |-> _ENC:Val, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        ("s"   |-> str(_INPUT:IntSeq))
        ("out" |-> (str(A:IntSeq) => str(encryptFold(A, S))))
        ("c"   |-> (C0:Val => finalLoopChar(S, C0))),
        parent(0))
    </scopes>

  claim [encrypt-entry]:
    <k>
      #loadAll(Module(
        FuncDef(
          "encrypt",
          Params("s"),
          Expr(
            Str("Rotate lowercase letters four places and preserve other characters."))
          Assign(Name("out"), Str(""))
          Assign(Name("c"), Str(""))
          For(
            Name("c"),
            Name("s"),
            If(
              BoolOp(
                "and",
                Compare(
                  Call(Name("ord"), Name("c")),
                  CmpOp(">=", Int(97))),
                Compare(
                  Call(Name("ord"), Name("c")),
                  CmpOp("<=", Int(122)))),
              AugAssign(
                Name("out"),
                "+",
                Call(
                  Name("chr"),
                  BinOp(
                    "+",
                    BinOp(
                      "%",
                      BinOp(
                        "+",
                        BinOp("-", Call(Name("ord"), Name("c")), Int(97)),
                        Int(4)),
                      Int(26)),
                    Int(97)))),
              AugAssign(Name("out"), "+", Name("c"))))
          Return(Name("out")))
        Assign(
          Name("result"),
          Call(Name("encrypt"), str(S:IntSeq)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        ("encrypt" |->
          closureVal(
            "s",
            Expr(
              Str("Rotate lowercase letters four places and preserve other characters."))
            Assign(Name("out"), Str(""))
            Assign(Name("c"), Str(""))
            For(
              Name("c"),
              Name("s"),
              If(
                BoolOp(
                  "and",
                  Compare(
                    Call(Name("ord"), Name("c")),
                    CmpOp(">=", Int(97))),
                  Compare(
                    Call(Name("ord"), Name("c")),
                    CmpOp("<=", Int(122)))),
                AugAssign(
                  Name("out"),
                  "+",
                  Call(
                    Name("chr"),
                    BinOp(
                      "+",
                      BinOp(
                        "%",
                        BinOp(
                          "+",
                          BinOp("-", Call(Name("ord"), Name("c")), Int(97)),
                          Int(4)),
                        Int(26)),
                      Int(97)))),
                AugAssign(Name("out"), "+", Name("c"))))
            Return(Name("out")),
            0))
        ("result" |-> str(encryptResult(S))),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
