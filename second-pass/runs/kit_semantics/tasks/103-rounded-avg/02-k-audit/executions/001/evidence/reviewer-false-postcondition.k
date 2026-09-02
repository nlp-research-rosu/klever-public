requires "verification.k"

module REVIEWER-FALSE-POSTCONDITION
  imports VERIFICATION

  // Fresh reviewer mutation: the real submitted body at satisfying input
  // (2, 2) returns "0b10", so demanding "0b11" is deliberately false.
  claim [two-two-is-not-three]:
    <k>
      #loadAll(Module(
        FuncDef("rounded_avg", Params("n", "m"),
          If(Compare(Name("n"), CmpOp(">", Name("m"))),
            Return(UnaryOp("-", Int(1))),
            .Stmts)
          Assign(
            Name("value"),
            BinOp(
              "+",
              BinOp(
                "//",
                BinOp("+", Name("n"), Name("m")),
                Int(2)),
              BinOp(
                "*",
                BinOp(
                  "%",
                  BinOp("+", Name("n"), Name("m")),
                  Int(2)),
                BinOp(
                  "%",
                  BinOp(
                    "//",
                    BinOp("+", Name("n"), Name("m")),
                    Int(2)),
                  Int(2)))))
          Assign(Name("digits"), Str(""))
          While(
            Compare(Name("value"), CmpOp(">", Int(1))),
            Assign(
              Name("digits"),
              BinOp(
                "+",
                Call(
                  Name("chr"),
                  BinOp(
                    "+",
                    Int(48),
                    BinOp("%", Name("value"), Int(2)))),
                Name("digits")))
            Assign(
              Name("value"),
              BinOp("//", Name("value"), Int(2))))
          Assign(
            Name("digits"),
            BinOp("+", Str("1"), Name("digits")))
          Return(BinOp("+", Str("0b"), Name("digits"))))))
      ~> Call(Name("rounded_avg"), Int(2), Int(2))
      =>
      str(iCons(
        48,
        iCons(
          98,
          iCons(
            49,
            iCons(49, .IntSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
