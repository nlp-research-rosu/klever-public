requires "verification.k"

module CHOOSE-NUM-SPEC
  imports CHOOSE-NUM-VERIFICATION

  claim
    <k>
      FuncDef("choose_num", Params("x", "y"),
        If(Compare(Name("x"), CmpOp(">", Name("y"))), Return(UnaryOp("-", Int(1))), .Stmts)
        If(Compare(BinOp("%", Name("y"), Int(2)), CmpOp("==", Int(0))), Return(Name("y")), .Stmts)
        If(Compare(Name("x"), CmpOp("==", Name("y"))), Return(UnaryOp("-", Int(1))), .Stmts)
        Return(BinOp("-", Name("y"), Int(1))))
      Assign(Name("result"), Call(Name("choose_num"), X:Int , Y:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "choose_num" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Int #if (X >Int Y) #then -1
             #else (#if (pyMod(Y, 2) ==Int 0) #then Y
             #else (#if (X ==Int Y) #then -1
             #else (Y -Int 1) #fi) #fi) #fi
    [all-path]
endmodule
