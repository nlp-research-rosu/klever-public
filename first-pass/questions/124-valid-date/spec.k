requires "verification.k"

module VALID-DATE-SPEC
  imports VALID-DATE-VERIFICATION

  // ---- Entry — result == vDate(stripped codes); straight-line, no loops.
  claim
    <k>
      FuncDef("valid_date", Params("date"),
          Assign(Name("date"), Call(Attribute(Name("date"), "strip"), .Exprs))
          Assign(
            Name("parts"),
            Call(Attribute(Name("date"), "split"), Str("-")))
          If(Compare(Call(Name("len"), Name("parts")), CmpOp("!=", Int(3))),
            Return(Bool(false)),
            .Stmts)
          Assign(
            TupleExpr(Name("month"), Name("day"), Name("year")),
            Name("parts"))
          If(UnaryOp(
            "not",
            BoolOp(
              "and",
              Call(Attribute(Name("month"), "isdigit"), .Exprs),
              Call(Attribute(Name("day"), "isdigit"), .Exprs),
              Call(Attribute(Name("year"), "isdigit"), .Exprs))),
            Return(Bool(false)),
            .Stmts)
          Assign(
            TupleExpr(Name("month"), Name("day"), Name("year")),
            TupleExpr(
              Call(Name("int"), Name("month")),
              Call(Name("int"), Name("day")),
              Call(Name("int"), Name("year"))))
          If(BoolOp(
            "or",
            Compare(Name("month"), CmpOp("<", Int(1))),
            Compare(Name("month"), CmpOp(">", Int(12)))),
            Return(Bool(false)),
            .Stmts)
          If(BoolOp(
            "or",
            BoolOp(
              "and",
              Compare(
                Name("month"),
                CmpOp(
                  "in",
                  ListExpr(
                    Int(1),
                    Int(3),
                    Int(5),
                    Int(7),
                    Int(8),
                    Int(10),
                    Int(12)))),
              Compare(Name("day"), CmpOp("<", Int(1)))),
            Compare(Name("day"), CmpOp(">", Int(31)))),
            Return(Bool(false)),
            .Stmts)
          If(BoolOp(
            "or",
            BoolOp(
              "and",
              Compare(
                Name("month"),
                CmpOp("in", ListExpr(Int(4), Int(6), Int(9), Int(11)))),
              Compare(Name("day"), CmpOp("<", Int(1)))),
            Compare(Name("day"), CmpOp(">", Int(30)))),
            Return(Bool(false)),
            .Stmts)
          If(BoolOp(
            "or",
            BoolOp(
              "and",
              Compare(Name("month"), CmpOp("==", Int(2))),
              Compare(Name("day"), CmpOp("<", Int(1)))),
            Compare(Name("day"), CmpOp(">", Int(29)))),
            Return(Bool(false)),
            .Stmts)
          Return(Bool(true)))
      Assign(Name("result"), Call(Name("valid_date"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "valid_date" <- ?_:Val ]
                       [ "result" <- vDate(revIS(trimWS(revIS(trimWS(CS))))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    // domain: exactly three '-'-fields after strip — the canonical guards the
    // unpack with try/except (removed in the rewrite), so the modeled program
    // is partial outside this domain (vDate's non-3 arm is the except branch)
    requires splitCount(revIS(trimWS(revIS(trimWS(CS))))) ==Int 3
    [all-path]
endmodule
