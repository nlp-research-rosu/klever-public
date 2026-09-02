requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The only body change is the empty branch's `return False`.  The original
  // empty-list postcondition `true` must therefore be rejected.
  claim [mutated-empty-branch]:
    <k> Call(Name("move_one_ball"), (list(.ValSeq), .Exprs))
        => true </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
         "move_one_ball" |->
           closureVal(
             "arr",
             If(UnaryOp("not", Name("arr")),
                Return(Bool(false)),
                .Stmts)
             Assign(Name("first"), Subscript(Name("arr"), Int(0)))
             Assign(Name("previous"), Name("first"))
             Assign(Name("current"), Name("first"))
             Assign(Name("drops"), Int(0))
             For(Name("current"), Name("arr"), scanBody)
             Assign(Name("drops"),
               BinOp("+", Name("drops"),
                 Compare(Name("first"), CmpOp("<", Name("previous")))))
             Return(Compare(Name("drops"), CmpOp("<=", Int(1)))),
             0),
         parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
