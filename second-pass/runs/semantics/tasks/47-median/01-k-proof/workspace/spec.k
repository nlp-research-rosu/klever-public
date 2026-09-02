requires "verification.k"

module MEDIAN-SPEC
  imports MEDIAN-VERIFICATION

  claim [median-odd]:
    <k>
      #loadAll(Module(
        FuncDef("median", Params("l"),
          Assign(Name("values"), Call(Name("sorted"), Name("l")))
          Assign(
            Name("middle"),
            BinOp("//", Call(Name("len"), Name("values")), Int(2)))
          If(Compare(
            BinOp("%", Call(Name("len"), Name("values")), Int(2)),
            CmpOp("==", Int(1))),
            Return(Subscript(Name("values"), Name("middle"))),
            .Stmts)
          Return(
            BinOp(
              "/",
              BinOp(
                "+",
                Subscript(Name("values"), Name("middle")),
                Subscript(
                  Name("values"),
                  BinOp("+", Name("middle"), Int(1)))),
              Float(2.0)))
        )))
      ~> Call(Name("median"), list(VS:ValSeq))
      =>
      sortedIntAt(VS, (vsLen(VS) -Int 1) /Int 2)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?_:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
     andBool vsLen(VS) >Int 0
     andBool pyMod(vsLen(VS), 2) ==Int 1

  claim [median-even]:
    <k>
      #loadAll(Module(
        FuncDef("median", Params("l"),
          Assign(Name("values"), Call(Name("sorted"), Name("l")))
          Assign(
            Name("middle"),
            BinOp("//", Call(Name("len"), Name("values")), Int(2)))
          If(Compare(
            BinOp("%", Call(Name("len"), Name("values")), Int(2)),
            CmpOp("==", Int(1))),
            Return(Subscript(Name("values"), Name("middle"))),
            .Stmts)
          Return(
            BinOp(
              "/",
              BinOp(
                "+",
                Subscript(Name("values"), Name("middle")),
                Subscript(
                  Name("values"),
                  BinOp("+", Name("middle"), Int(1)))),
              Float(2.0)))
        )))
      ~> Call(Name("median"), list(VS:ValSeq))
      =>
      intFloatDiv(
        sortedIntAt(VS, vsLen(VS) /Int 2)
        +Int sortedIntAt(VS, vsLen(VS) /Int 2 +Int 1),
        2.0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?_:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
     andBool vsLen(VS) >=Int 4
     andBool pyMod(vsLen(VS), 2) ==Int 0
endmodule
