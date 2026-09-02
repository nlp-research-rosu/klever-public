requires "verification.k"

module SPEC
  imports VERIFICATION

  // At a loop head, P is the product accumulated so far and F is the
  // 0-or-1 presence bit.
  claim [digits-loop]:
    <k>
      #while(
        Compare(Name("n"), CmpOp(">", Int(0))),
        If(
          Compare(
            BinOp("%", Name("n"), Int(2)),
            CmpOp("==", Int(1))),
          Assign(
            Name("product"),
            BinOp(
              "*",
              Name("product"),
              BinOp("%", Name("n"), Int(10))))
          Assign(Name("found"), Int(1)),
          .Stmts)
        Assign(Name("n"), BinOp("//", Name("n"), Int(10)))
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "n"       |-> (N:Int => 0)
        "product" |-> (P:Int =>
                         P *Int oddDigitsProduct(N))
        "found"   |-> (F:Int =>
                         F +Int oddDigitSeen(N)
                           -Int (F *Int oddDigitSeen(N))),
        PAR:Parent)
      ...
    </scopes>
    requires N >=Int 0
     andBool (F ==Int 0 orBool F ==Int 1)

  // Exact source body and normal module loading, lookup, argument evaluation,
  // frame setup, execution, return, and frame pop all remain in the theorem.
  claim [digits-entry]:
    <k>
      #loadAll(
        Module(
          FuncDef("digits", Params("n"),
            Assign(Name("product"), Int(1))
            Assign(Name("found"), Int(0))
            While(Compare(Name("n"), CmpOp(">", Int(0))),
              If(
                Compare(
                  BinOp("%", Name("n"), Int(2)),
                  CmpOp("==", Int(1))),
                Assign(
                  Name("product"),
                  BinOp(
                    "*",
                    Name("product"),
                    BinOp("%", Name("n"), Int(10))))
                Assign(Name("found"), Int(1)),
                .Stmts)
              Assign(
                Name("n"),
                BinOp("//", Name("n"), Int(10)))
              .Stmts)
            Return(
              BinOp("*", Name("product"), Name("found")))
            .Stmts)
          .Stmts))
      ~> Call(Name("digits"), Int(N))
      => oddDigitsProduct(N) *Int oddDigitSeen(N)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => ?GLOBALS:Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 0
endmodule
