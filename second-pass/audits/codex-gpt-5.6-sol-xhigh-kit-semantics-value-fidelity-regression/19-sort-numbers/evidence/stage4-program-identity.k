requires "verification.k"

module AUDIT-PROGRAM-IDENTITY
  imports VERIFICATION

  claim [submitted-constructor-identity]:
    <k> solutionProgram
      => Module(
           FuncDef("_number_rank", Params("number", .ParamNames),
             If(Compare(Name("number"), CmpOp("==", Str("zero"))),
               Return(Int(0)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("one"))),
               Return(Int(1)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("two"))),
               Return(Int(2)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("three"))),
               Return(Int(3)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("four"))),
               Return(Int(4)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("five"))),
               Return(Int(5)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("six"))),
               Return(Int(6)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("seven"))),
               Return(Int(7)) .Stmts, .Stmts)
             If(Compare(Name("number"), CmpOp("==", Str("eight"))),
               Return(Int(8)) .Stmts, .Stmts)
             Return(Int(9)) .Stmts)
           FuncDef("sort_numbers", Params("numbers", .ParamNames),
             Return(
               Call(
                 Attribute(Str(" "), "join"),
                 (Call(
                   Name("sorted"),
                   (Call(Attribute(Name("numbers"), "split"), .Exprs),
                    KwArg("key", Name("_number_rank")),
                    .Exprs)),
                  .Exprs)))
             .Stmts)
           .Stmts) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
