requires "verification.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION

  // Deliberately false: the material body mutation x + 2 maps [0] to [2],
  // while the original theorem's expected result for [0] is [1].
  claim [changed-body]:
    <k>
      Call(Name("incr_list"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
         "incr_list" |->
           closureVal(
             "l",
             Assign(Name("result"), ListExpr(.Exprs))
             Assign(Name("x"), Int(0))
             For(
               Name("x"),
               Name("l"),
               Expr(
                 Call(
                   Attribute(Name("result"), "append"),
                   (BinOp("+", Name("x"), Int(2)), .Exprs)))
               .Stmts)
             Return(Name("result"))
             .Stmts,
             0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(vCons(0, .ValSeq))
      =>
      0 |-> list(vCons(0, .ValSeq))
      1 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
