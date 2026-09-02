requires "verification.k"

module FILE-NAME-CHECK-SPEC
  imports FILE-NAME-CHECK-VERIFICATION

  // ---- Digit-filter comp invariant, variant B (x bound; circularity).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("x"),
        If(BoolOp("and", Call(Attribute(Name("x"), "isdigit"), .Exprs)),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ] [ "x" <- _:Val ], P:Parent) =>
        scope((.Map [ "$acc" <- ref(?AN2:Int) ]) [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLM:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K digSeq(CS, R)
    [all-path]

  // ---- Variant A (comp start; existential post rest covers empty fields).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("x"),
        If(BoolOp("and", Call(Attribute(Name("x"), "isdigit"), .Exprs)),
          Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(Name("x")))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "$acc" <- ref(AN:Int) ], P:Parent) =>
        scope((.Map [ "$acc" <- ref(?AN2:Int) ]) ?XM:Map, P)
      ) ...
    </scopes>
    <heap> (AN |-> list(R:ValSeq)) HREST:Map
        => (?AN2 |-> list(?RO:ValSeq)) ?_:Map </heap>
    <heapLoc> HLM:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int AN andBool AN <Int HLM andBool keysBelow(HREST, HLM)
    ensures ?RO ==K digSeq(CS, R)
    [all-path]

  // ---- Entry — result == fnRes(CS); total domain (arm 1 covers bad splits).
  claim
    <k>
      FuncDef("file_name_check", Params("file_name"),
          Assign(Name("suf"), ListExpr(Str("txt"), Str("exe"), Str("dll")))
          Assign(
            Name("lst"),
            Call(
              Attribute(Name("file_name"), "split"),
              KwArg("sep", Str("."))))
          If(Compare(Call(Name("len"), Name("lst")), CmpOp("!=", Int(2))),
            Return(Str("No")),
            .Stmts)
          If(UnaryOp(
            "not",
            Compare(Subscript(Name("lst"), Int(1)), CmpOp("in", Name("suf")))),
            Return(Str("No")),
            .Stmts)
          If(Compare(
            Call(Name("len"), Subscript(Name("lst"), Int(0))),
            CmpOp("==", Int(0))),
            Return(Str("No")),
            .Stmts)
          If(UnaryOp(
            "not",
            Call(
              Attribute(
                Subscript(Subscript(Name("lst"), Int(0)), Int(0)),
                "isalpha"),
              .Exprs)),
            Return(Str("No")),
            .Stmts)
          Assign(
            Name("t"),
            Call(
              Name("len"),
              ListComp(Name("x"),
                CompFor(
                  Name("x"),
                  Subscript(Name("lst"), Int(0)),
                  Call(Attribute(Name("x"), "isdigit"), .Exprs)))))
          If(Compare(Name("t"), CmpOp(">", Int(3))),
            Return(Str("No")),
            .Stmts)
          Return(Str("Yes")))
      Assign(Name("result"), Call(Name("file_name_check"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "file_name_check" <- ?_:Val ]
                       [ "result" <- fnRes(CS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
