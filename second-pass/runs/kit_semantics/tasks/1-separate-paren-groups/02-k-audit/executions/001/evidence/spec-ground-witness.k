requires "verification.k"

module SPEC-GROUND-WITNESS
  imports VERIFICATION

  claim [ground-witness]:
    <k>
      Call(Name("separate_paren_groups"),
           str(iCons(40, iCons(41, .IntSeq))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |->
        scope(
          "separate_paren_groups" |->
            closureVal(
              "paren_string",
              Assign(Name("groups"), ListExpr(.Exprs))
              Assign(Name("current"), Str(""))
              Assign(Name("depth"), Int(0))
              Assign(Name("char"), Str(""))
              For(
                Name("char"),
                Name("paren_string"),
                If(
                  Compare(Name("char"), CmpOp("!=", Str(" "))),
                  AugAssign(Name("current"), "+", Name("char"))
                  If(
                    Compare(Name("char"), CmpOp("==", Str("("))),
                    AugAssign(Name("depth"), "+", Int(1)) .Stmts,
                    AugAssign(Name("depth"), "-", Int(1)) .Stmts)
                  If(
                    Compare(Name("depth"), CmpOp("==", Int(0))),
                    Expr(
                      Call(
                        Attribute(Name("groups"), "append"),
                        Name("current")))
                    Assign(Name("current"), Str("")) .Stmts,
                    .Stmts)
                  .Stmts,
                  .Stmts)
                .Stmts)
              Return(Name("groups"))
              .Stmts,
              0),
          parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |->
           list(
             vCons(
               str(iCons(40, iCons(41, .IntSeq))),
               .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      validParenInput(iCons(40, iCons(41, .IntSeq)))
endmodule
