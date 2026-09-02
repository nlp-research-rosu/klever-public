requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [sum-loop]:
    <k>
      #loop(
        list(ITEMS:ValSeq),
        Name("string"),
        AugAssign(Name("total"), "+", Call(Name("len"), Name("string")))
      )
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      0 |-> scope(MODULE:Map, parent(-1))
      -1 |-> builtinsScope
      L |-> scope(
        "strings" |-> ORIGINAL:Val
        "total" |-> (ACC:Int => totalLenFrom(ACC, ITEMS))
        "string" |-> (OLD:Val => lastLoopValue(ITEMS, OLD)),
        parent(0)
      )
      OTHER:Map
    </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> HP:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires L >Int 0
     andBool notBool ("len" in_keys(MODULE))
     andBool onlyStrings(ITEMS)

  claim [entry-first]:
    <k>
      #loadAll(Module(
        FuncDef("_total_length", Params("strings"),
          Assign(Name("total"), Int(0))
          Assign(Name("string"), NoneVal)
          For(Name("string"), Name("strings"),
            AugAssign(Name("total"), "+", Call(Name("len"), Name("string"))))
          Return(Name("total")))
        FuncDef("total_match", Params("lst1", "lst2"),
          If(Compare(
            Call(Name("_total_length"), Name("lst1")),
            CmpOp("<=", Call(Name("_total_length"), Name("lst2")))),
            Return(Name("lst1")),
            .Stmts)
          Return(Name("lst2")))
      ))
      ~> Call(
        Name("total_match"),
        list(A:ValSeq),
        list(B:ValSeq)
      )
      => list(A)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "_total_length" |-> closureVal(
          ("strings", .ParamNames),
          Assign(Name("total"), Int(0))
          Assign(Name("string"), NoneVal)
          For(Name("string"), Name("strings"),
            AugAssign(Name("total"), "+", Call(Name("len"), Name("string"))))
          Return(Name("total")),
          0
        )
        "total_match" |-> closureVal(
          ("lst1", "lst2", .ParamNames),
          If(Compare(
            Call(Name("_total_length"), Name("lst1")),
            CmpOp("<=", Call(Name("_total_length"), Name("lst2")))),
            Return(Name("lst1")),
            .Stmts)
          Return(Name("lst2")),
          0
        ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires onlyStrings(A)
     andBool onlyStrings(B)
     andBool totalLen(A) <=Int totalLen(B)

  claim [entry-second]:
    <k>
      #loadAll(Module(
        FuncDef("_total_length", Params("strings"),
          Assign(Name("total"), Int(0))
          Assign(Name("string"), NoneVal)
          For(Name("string"), Name("strings"),
            AugAssign(Name("total"), "+", Call(Name("len"), Name("string"))))
          Return(Name("total")))
        FuncDef("total_match", Params("lst1", "lst2"),
          If(Compare(
            Call(Name("_total_length"), Name("lst1")),
            CmpOp("<=", Call(Name("_total_length"), Name("lst2")))),
            Return(Name("lst1")),
            .Stmts)
          Return(Name("lst2")))
      ))
      ~> Call(
        Name("total_match"),
        list(A:ValSeq),
        list(B:ValSeq)
      )
      => list(B)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "_total_length" |-> closureVal(
          ("strings", .ParamNames),
          Assign(Name("total"), Int(0))
          Assign(Name("string"), NoneVal)
          For(Name("string"), Name("strings"),
            AugAssign(Name("total"), "+", Call(Name("len"), Name("string"))))
          Return(Name("total")),
          0
        )
        "total_match" |-> closureVal(
          ("lst1", "lst2", .ParamNames),
          If(Compare(
            Call(Name("_total_length"), Name("lst1")),
            CmpOp("<=", Call(Name("_total_length"), Name("lst2")))),
            Return(Name("lst1")),
            .Stmts)
          Return(Name("lst2")),
          0
        ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires onlyStrings(A)
     andBool onlyStrings(B)
     andBool totalLen(A) >Int totalLen(B)
endmodule
