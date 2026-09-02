requires "verification.k"

module SPEC-BODY-SENSITIVITY-AUDIT
  imports VERIFICATION

  // Fresh operational-sensitivity probe: the executed closure differs from the
  // submitted body at the final statement and always returns false there.
  // The selected nonempty input reaches that changed statement, while the
  // submitted body and moveSpec both return true.
  claim [mutated-nonempty-final-return]:
    <k> Call(
          Name("move_one_ball"),
          (list(vCons(3, vCons(4, vCons(5, vCons(1, vCons(2, .ValSeq)))))), .Exprs))
        => true </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
         "move_one_ball" |->
           closureVal(
             "arr",
             If(UnaryOp("not", Name("arr")),
                Return(Bool(true)),
                .Stmts)
             Assign(Name("first"), Subscript(Name("arr"), Int(0)))
             Assign(Name("previous"), Name("first"))
             Assign(Name("current"), Name("first"))
             Assign(Name("drops"), Int(0))
             For(Name("current"), Name("arr"), scanBody)
             Assign(Name("drops"),
               BinOp("+", Name("drops"),
                 Compare(Name("first"), CmpOp("<", Name("previous")))))
             Return(Bool(false)),
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
