requires "verification.k"

module AUDITOR-BODY-SENSITIVITY
  imports VERIFICATION

  // The actual loaded and closure-bound body appends unconditionally.
  // The original filtered postcondition must therefore fail.
  claim [unconditional-append]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "filter_by_prefix",
            Params("strings", "prefix"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("string"), Str(""))
            For(
              Name("string"),
              Name("strings"),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Name("string"))))
            Return(Name("result")))))
      ~> Call(
           Name("filter_by_prefix"),
           list(
             vCons(
               str(strToCodes("abc")),
               vCons(
                 str(strToCodes("bcd")),
                 .ValSeq))),
           str(strToCodes("a")))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             .Map
             => "filter_by_prefix" |->
                  closureVal(
                    ("strings", "prefix"),
                    Assign(Name("result"), ListExpr(.Exprs))
                    Assign(Name("string"), Str(""))
                    For(
                      Name("string"),
                      Name("strings"),
                      Expr(
                        Call(
                          Attribute(Name("result"), "append"),
                          Name("string"))))
                    Return(Name("result")),
                    0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(
             str(strToCodes("abc")),
             .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
