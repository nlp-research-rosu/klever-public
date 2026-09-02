requires "verification.k"

module SOURCE-PINNING-SPEC
  imports IS-NESTED-VERIFICATION

  // Exact loop-body constructors from the trusted regeneration of solution.mpy.
  claim [scan-body-constructors]:
    <k>
      scanBody
      =>
      If(Compare(Call(Name("ord"), Name("char")),
                 CmpOp("==", Int(91))),
         If(Compare(Name("state"), CmpOp("<", Int(2))),
            AugAssign(Name("state"), "+", Int(1))
             .Stmts,
            .Stmts)
          .Stmts,
         If(Compare(Name("state"), CmpOp(">", Int(1))),
            If(Compare(Name("state"), CmpOp("<", Int(4))),
               AugAssign(Name("state"), "+", Int(1))
               .Stmts,
               .Stmts)
            .Stmts,
            .Stmts)
         .Stmts)
       .Stmts
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 0 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Exact function binding, parameters, body, and defining environment from
  // the trusted regeneration. This is the closure placed in the entry claims.
  claim [closure-constructors]:
    <k>
      isNestedClosure
      =>
      closureVal(
        ("string", .ParamNames),
        Assign(Name("state"), Int(0))
        Assign(Name("char"), Str(""))
        For(Name("char"), Name("string"),
          If(Compare(Call(Name("ord"), Name("char")),
                     CmpOp("==", Int(91))),
             If(Compare(Name("state"), CmpOp("<", Int(2))),
                AugAssign(Name("state"), "+", Int(1))
                .Stmts,
                .Stmts)
              .Stmts,
             If(Compare(Name("state"), CmpOp(">", Int(1))),
                If(Compare(Name("state"), CmpOp("<", Int(4))),
                   AugAssign(Name("state"), "+", Int(1))
                   .Stmts,
                   .Stmts)
                .Stmts,
                .Stmts)
             .Stmts)
           .Stmts)
        Return(Compare(Name("state"), CmpOp("==", Int(4))))
        .Stmts,
        0)
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 0 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
